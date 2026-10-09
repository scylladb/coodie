# coodie: architecture and code review (`src/coodie/`)

Reviewed at `e2a6e66` (branch `am/plans-audit-review`). Every module under `src/coodie/` (about 8.4k lines) was read, along with the test layout, `pyproject.toml` and the CI workflows.

**How findings were checked:**
- Unit suite: `uv run pytest tests -q` gives **1068 passed, 62 skipped, 82% branch coverage**.
- Small repro scripts against a fake `AbstractDriver`, run on Python 3.10, 3.12 and 3.14.
- `mypy` (using the repo's own config) and `ruff`.

Findings marked **(verified)** were reproduced. Findings marked **(suspected)** come from reading the code or from known driver behaviour, and were not run against a live cluster.

---

## 1. Executive summary

coodie's layering is clean and easy to follow:
- `cql_builder` is a set of pure functions.
- Drivers sit behind an ABC.
- `Document` and `QuerySet` are thin.
- Pydantic `Annotated` markers form the schema DSL.

Unit coverage is good, CI runs on 3 OSes × 5 Pythons, and an API-parity test keeps sync and aio in step.

However, several **correctness bugs affect common, documented paths**, and the unit suite misses them because it runs against a mock driver:

1. **`X | None` annotations crash on Python 3.10–3.13** (verified). Model definition raises `InvalidQueryError`, although the docs recommend this syntax. CI only passes because the test models use `Optional[...]`.
2. **`Document.insert()` returns `None`**, but the docs promise an `LWTResult`. The documented "deploy lock" example fails with `AttributeError`, and callers cannot find out whether `IF NOT EXISTS` was applied (verified).
3. **`MigrationContext.scan_table()` silently skips rows.** It reads each token sub-range with `LIMIT page_size` and never pages within the range. Data migrations on large or skewed tables lose rows without any error.
4. **Multiple connections are broken.**
   - Reads (`QuerySet`), batches and UDT sync always use the *default* driver, ignoring `Settings.connection`. Writes to the same model go to the named connection (verified).
   - Every `init_coodie(name=...)` call also makes the new connection the default.
5. **Using `only()` or `defer()` and then calling `save()` erases data.** The columns that were not loaded are written back as their defaults, e.g. `NULL` or `[]` (verified).
6. **Statement-cache problems:**
   - TTL and TIMESTAMP values are written directly into the CQL text instead of being bound, so every distinct timestamp creates a new cache entry and a new prepared statement on the server. The module-level caches never evict (verified: 1000 timestamps give 1001 entries).
   - The `UPDATE` cache key ignores `IN` arity, so later calls reuse a statement with the wrong number of placeholders (verified).
7. **Pagination state is stored on the shared driver object** (`driver._last_paging_state`).
   - This races under asyncio concurrency.
   - It is always `None` with `LazyDriver`.
   - It is ignored completely by the python-rs driver, which also silently drops `consistency` and `timeout`.

The sync and aio packages are **written twice by hand** (no unasync or similar generator). After normalising async keywords, the diff shows almost no drift. The bigger duplication is `sync_table`, which is implemented four times across the drivers and has already drifted: only `CassandraDriver` creates vector indexes.

---

## 2. Architecture overview

```
                       coodie/__init__.py  (re-exports aio API as default!)
                                 │
          ┌──────────────────────┴───────────────────────┐
     coodie.aio                                       coodie.sync
   document.py / query.py   ◄── hand-duplicated ──►  document.py / query.py
          │   (Document, CounterDocument, MaterializedView, QuerySet)
          ├──────────────► batch.py (BatchQuery / AsyncBatchQuery)
          ├──────────────► lazy.py (LazyDocument), results.py (LWTResult, PagedResult)
          │
          ▼
   schema.py (build_schema, ColumnDefinition, lru-cached introspection, polymorphism)
     ├─ fields.py   (Annotated markers: PrimaryKey, ClusteringKey, Indexed, Vector, …)
     ├─ types.py    (Python → CQL type mapping, None→empty collection coercion)
     └─ usertype.py (UserType base, sync_type, dependency walk)
          │
          ▼
   cql_builder.py  (pure string builders + module-level, unbounded template caches)
          │
          ▼
   drivers/__init__.py  (global _registry + _default_driver_name, init_coodie[_async])
   drivers/base.py      (AbstractDriver: execute/execute_async/sync_table/…)
     ├─ cassandra.py  (cassandra-/scylla-driver; asyncio bridge via add_callbacks)
     ├─ acsylla.py    (native async; sync bridge = bg event loop thread)
     ├─ python_rs.py  (native async; sync bridge = bg event loop thread)
     └─ lazy.py       (deferred CassandraDriver proxy)

   migrations/  base.py (Migration, MigrationContext.scan_table)
                runner.py (discover/apply/rollback, LWT lock, schema agreement)
                autogen.py (introspect + diff + render), cli.py (`coodie` entry point)
```

**Global state:**
- `drivers._registry` and `_default_driver_name`.
- Module-level CQL template caches in `cql_builder` (`_select_cql_cache`, `_update_cql_cache`, …).
- `functools.lru_cache(maxsize=128)` on per-class introspection helpers.
- Per-driver `_prepared`, `_known_tables` and `_last_paging_state`.

None of this is guarded by a lock. That is acceptable under the GIL, except for `_last_paging_state` (H5).

**Lazy loading:** `LazyDriver` defers the connection, and `LazyDocument` defers Pydantic parsing. Optional driver imports happen inside functions, which is good.

---

## 3. Findings (ranked)

| # | Sev | Area | Finding | Location |
|---|---|---|---|---|
| C1 | Critical | types | `X \| None` / `list[int] \| None` not supported on Py 3.10–3.13 (verified) | types.py:113, :206; usertype.py:237 |
| C2 | Critical | LWT/API | `Document.insert()` drops the LWT result and returns `None`; docs say `LWTResult` (verified) | sync/document.py:224-256, aio/document.py same; docs/source/guide/lwt.md:49, exceptions.md:159 |
| C3 | Critical | migrations | `scan_table` reads ≤ `page_size` rows per token range with no paging, so rows are silently dropped | migrations/base.py:165-170 |
| H1 | High | data loss | `only()`/`defer()` + `save()` overwrites unloaded columns with defaults (verified) | sync/query.py:274-280, 336-345; sync/document.py:184-201 |
| H2 | High | connections | `QuerySet`, `BatchQuery`, `UserType.sync_type`, `_get_keyspace` ignore `Settings.connection`; `init_coodie` always steals default (verified) | sync/query.py:265; batch.py:56,114; usertype.py:90,126; sync/document.py:74-79; drivers/__init__.py:132,176,188,209,221 |
| H3 | High | drivers | `LazyDriver` has no `_default_keyspace` ("No keyspace configured", verified), no `_last_paging_state` (paging silently off), and drops `compression`/`speculative_execution_policy` | drivers/lazy.py:25-39; drivers/__init__.py:102-105 |
| H4 | High | paging | Paging state kept on the shared driver instance, so concurrent aio queries clobber each other | aio/query.py:392; cassandra.py:93,394; acsylla.py:281-283 |
| H5 | High | drivers | (suspected) `CassandraDriver.execute_async` returns only the first page (callback bridge), so aio `all()` truncates at about 5000 rows | cassandra.py:392-395 |
| H6 | High | cql_builder | `UPDATE … IF col IN (…)` cache key ignores arity; `DELETE` cached path doesn't flatten IN params (verified) | cql_builder.py:683, 785 |
| H7 | High | perf/memory | TTL/TIMESTAMP inlined into CQL; caches keyed on their values; unbounded caches and prepared-stmt growth (verified). Batches are prepared as one text blob per shape | cql_builder.py:453-464, 507, 690-693, 768, 849-869; cassandra.py:42-45; acsylla.py:220; python_rs.py:163 |
| H8 | High | schema | `Document._schema()` returns the *parent's* cached schema for subclasses (verified) | sync/document.py:93-96; aio/document.py same |
| H9 | High | python-rs | Silently ignores `consistency`, `timeout`, `fetch_size`, `paging_state`; (suspected) `iter_current_page` returns only first page | python_rs.py:249-266, 215 |
| H10 | High | UDT | Two different snake_case algorithms: column type `frozen<httpaddress>` vs created type `http_address` (verified) | types.py:162,185 vs usertype.py:29-37,80 |
| M1 | Medium | arch | sync/aio hand-duplicated (no generator). Little drift today (sync-only `__len__`) but 2× maintenance | aio/*, sync/* |
| M2 | Medium | arch | `sync_table` implemented 4× with drift: acsylla/python-rs never create vector indexes; ALTER built inline; `_is_ddl` duplicated with different semantics | cassandra.py:98-199, 407-508; acsylla.py:306-398; python_rs.py:317-409; python_rs.py:12-17 vs drivers/base.py:9-11 |
| M3 | Medium | schema sync | `_known_tables` not invalidated by `drop_table()`, so `drop_table(); sync_table()` is a no-op in the same session | sync/document.py:148-151; cassandra.py:109 |
| M4 | Medium | schema sync | `sync_table` silently ignores type changes and PK/CK changes; ALTER ADD of a new key column fails at runtime | cassandra.py:133-139 |
| M5 | Medium | migrations | Lock release is unconditional (may delete another owner's lock after TTL); 300 s TTL never renewed; `allow_destructive` never enforced; schema-agreement failure ignored | runner.py:42,181-184,119,312; autogen.py:389; base.py:218 |
| M6 | Medium | autogen | Emits `ALTER … TYPE` "safe widening" (unsupported in ScyllaDB / Cassandra ≥3.0.11); vector indexes diffed as drops; CLI ignores per-model keyspace, includes MVs; no auth/SSL flags | autogen.py:48-58,419,350-362; cli.py:270-310, 37-156 |
| M7 | Medium | API | `Document.update()` bypasses validation (`object.__setattr__`), no consistency/timeout/batch/timestamp; `QuerySet.update` drops LWT result; `QuerySet.create` ignores consistency/timeout | sync/document.py:344-388; sync/query.py:503-538 |
| M8 | Medium | perf/types | Default `model_construct` fast path: driver-native types leak (SortedSet, OrderedMapSerializedKey, UDT namedtuples). (suspected) | sync/query.py:332-354; drivers/base.py:21 |
| M9 | Medium | quoting | Identifiers quoted but not escaped; keyspace/table never quoted; string option values not escaped (`comment = 'it's'` verified); MV `where_clause` raw | cql_builder.py:16,73-77,129-133,37,173 |
| M10 | Medium | save | `save()` writes every `None` field, causing tombstones and clobbering concurrent writers' columns | sync/document.py:185 |
| M11 | Medium | typing | Strict mypy config, `py.typed` shipped, but mypy not in CI: **67 errors** | pyproject.toml `[tool.mypy]`; .github/workflows/ci.yml |
| M12 | Medium | packaging | `python-rs` extra = `scylla>=0.1.0` resolves from PyPI for pip users (uv `sources` only applies in-repo). (suspected dependency-confusion) | pyproject.toml:33, 104-107 |
| M13 | Medium | UDT | `sync_type` is CREATE-only (docs say "create or update"); `build_alter_type_add` dead; `sync_table` never syncs UDTs | usertype.py:116-144; cql_builder.py:840; docs/source/guide/user-defined-types.md:176 |
| M14 | Medium | API | sync `QuerySet.__len__` runs `COUNT(*)`, so `bool(qs)` does a full scan; aio lacks it (parity drift) | sync/query.py:543-544 |
| L1 | Low | drivers | `AcsyllaDriver.__init__` always warns and spawns a thread even for pure async; non-bridged close leaks thread (same in python-rs) | acsylla.py:109-124, 449-453; python_rs.py:92-99 |
| L2 | Low | API | `CounterDocument.save/insert` and MV overrides reject `batch=` with TypeError; MV `delete_columns` not blocked | sync/document.py:437-453, 570-580 |
| L3 | Low | lazy | `LazyDocument` defines `__eq__` without `__hash__` (unhashable); isinstance checks fail | lazy.py:51-54 |
| L4 | Low | query | `aggregate(x="count(*)")` produces `COUNT("*")`; `IN []` produces `IN ()`; `delete()`/`update()` with no filters produce invalid CQL instead of a clear error | sync/query.py:431-435; cql_builder.py:249, 731-732 |
| L5 | Low | migrations | `--target` with no match applies everything; `asyncio.get_event_loop()` in coroutine; checksum only checked in `--status` | runner.py:327,199,215 |
| L6 | Low | schema | `_cached_type_hints` silently falls back to raw string annotations, giving a confusing later error | schema.py:18-22 |
| L7 | Low | arch | Three copies of `_snake_case` (sync/query, aio/query, usertype) + a 4th regex in types.py | sync/query.py:557-564; usertype.py:29-37; types.py:162 |
| L8 | Low | autogen | `render_migration` escapes only `"` in description (backslash/newline breaks generated file) | autogen.py:453 |
| N1 | Nit | exports | `"Vector"`, `"VectorIndex"` listed twice in `__all__`; top-level `coodie.Document` is the **async** one (surprising; document it) | __init__.py:97-99, 14-23 |
| N2 | Nit | packaging | No `Programming Language :: Python :: 3.x` classifiers; loose `acsylla>=0.1.0`, `pydantic>=2.0` floors | pyproject.toml:12-27 |

---

## 4. Detailed findings

### C1: PEP 604 unions not supported on Python 3.10–3.13
`python_type_to_cql_type_str` checks `origin is Union`. On Python < 3.14, `int | None` has origin `types.UnionType`, not `typing.Union`. Python 3.14 merged the two, which is why the code works there.

```
$ uv run --python 3.10 … build_schema(B)   # B.name: str | None = None
InvalidQueryError: Cannot map Python type str | None to a CQL type
$ uv run --python 3.12 …                    # same failure
```

`docs/source/guide/field-types.md:159-166` explicitly recommends `int | None`. The same check is repeated in `_unwrap_annotation` (types.py:206), so None-to-empty collection coercion is also skipped for `list[int] | None`. It also appears in `_find_udt_types_in_annotation` (usertype.py:237), so nested UDTs inside `X | None` are not discovered.

Unit CI runs on 3.10–3.13, but `tests/models.py` uses only `Optional`. Integration runs only on 3.12/3.14.

**Fix:** `if origin is Union or origin is types.UnionType`, in all three places. Add a model that uses `X | None` to the unit tests.

### C2: `Document.insert()` loses the LWT result
`insert()` builds `INSERT … IF NOT EXISTS`, executes it, and returns `None` (sync/document.py:253-256). The docs (`lwt.md:49-56`, `exceptions.md:159-163`, `llms-full.txt:286`) show `result = lock.insert(); if result.applied: …`. That code raises `AttributeError`, and a caller has no way to tell whether the insert was applied. This undermines exactly the use case (locks, uniqueness) that LWT exists for.

Related: `QuerySet.update(if_conditions=…)` also discards the result (sync/query.py:519-538), and batches discard `[applied]`.

### C3: `scan_table` drops rows
```python
cql = f"SELECT * FROM {ks}.{tbl} WHERE {tok} > ? AND {tok} <= ? LIMIT {page_size}"
rows = await self._driver.execute_async(cql, [range_start, range_end])
```

Defaults are `num_ranges=1000` and `page_size=1000`. Any sub-range with more than 1000 rows is truncated without a warning. This happens for any table above about 1M rows, or for a skewed partition distribution.

There is a second issue: the paged-callback bridge (H5) caps each result at the driver's fetch size anyway.

**Fix:** within each range, loop with `token(pk) > last_seen_token`, or use driver paging (`fetch_size` + `paging_state`) until it is exhausted. Also quote the PK identifiers in `token(...)`.

### H1: Partial projection followed by `save()` erases data
`.only()` / `.defer()` select a subset of columns. `model_construct()` then fills the missing fields with their defaults, and `save()` writes *all* `model_fields`:

```
U.find(id=uid).only("id","name").first().save()
→ INSERT INTO ks.u ("id","name","email","tags") VALUES (?, ?, ?, ?)  [uid, 'n', None, []]
```

As a result, `email` becomes null and `tags` is deleted.

**Options:**
- (a) `save()` writes only `model_fields_set`, or
- (b) partially loaded docs are marked read-only, or
- (c) `save()` raises if the doc was loaded with a projection.

### H2: Multi-connection routing
- `Document._get_driver()` honours `Settings.connection` (sync/document.py:85-90).
- `QuerySet._get_driver()` calls `get_driver()` with no name (sync/query.py:265-266). A repro showed `save()` going to `analytics` while `find().all()` went to `default`.
- `BatchQuery.execute` (batch.py:56-64, 114-122) and `UserType.sync_type` (usertype.py:126) also use the default.
- `_get_keyspace()` reads `_default_keyspace` from the **default** driver, not the model's connection (sync/document.py:74-79).
- `init_coodie`/`init_coodie_async` call `register_driver(name, driver, default=True)` on every path. Initialising a secondary connection therefore re-targets every model that has no `connection` setting.

**Fix:**
- `QuerySet._get_driver` should return `self._doc_cls._get_driver()`.
- Batch should take a `connection=` argument or infer it from the first document added.
- Only make a driver the default when `name == "default"` or it is the first one registered.

### H3: `LazyDriver` is incomplete
- It stores `_keyspace` but not `_default_keyspace`, so `init_coodie(lazy=True, keyspace="ks")` combined with a model without `Settings.keyspace` raises `InvalidQueryError: No keyspace configured` (verified).
- It has no `_last_paging_state`, so `paged_all()` always returns `paging_state=None`.
- The lazy branch in `drivers/__init__.py:102-105` runs *before* `compression` / `speculative_execution_policy` are added to kwargs, so those arguments are silently ignored.

**Fix:** forward attribute access to the real driver with `__getattr__`, and build kwargs before the branch.

### H4: Paging state on the shared driver (concurrency)
`paged_all()` awaits `execute_async` and then reads `driver._last_paging_state`. Between those two steps, any other coroutine can run a query that resets or overwrites the attribute (cassandra.py:394 sets it to `None` on every non-paged async execute). The same applies to threads in sync code.

**Fix:** have `execute` return the paging state with the rows, for example a `ResultPage(rows, paging_state)` or an `execute_paged()` method on the ABC. This also makes `_last_paging_state` part of the declared interface instead of an implicit `getattr` contract.

### H5 (suspected): aio `CassandraDriver` returns only the first page
`ResponseFuture.add_callbacks` receives only the first page of rows (the code comment at cassandra.py:366-369 acknowledges this). Non-paged `execute_async` therefore returns at most `fetch_size` rows (5000 by default), and aio `all()` truncates large result sets silently. The sync path iterates a `ResultSet` and fetches all pages.

**Fix:** in the callback, call `start_fetching_next_page()` while `has_more_pages`, or use `ResponseFuture.result()` in an executor.

### H6: Incorrect statement-cache keys
```
build_update(..., if_conditions={"y__in":[1,2]})    → … IF "y" IN (?, ?)   [1,1,1,2]
build_update(..., if_conditions={"y__in":[1,2,3]})  → … IF "y" IN (?, ?)   [1,1,1,2,3]   ← 5 params, 4 markers
build_delete(..., if_conditions={"y__in":[1,2]}) ×2 → second call params [1, [1,2]]      ← not flattened
```

**Fix:** derive the IF shape the same way as `_where_to_shape`, and share one param extractor between the cached and uncached paths.

### H7: Inlined TTL/TIMESTAMP and unbounded caches
`_build_using_clause` produces `USING TTL 5 AND TIMESTAMP 123` as literal text. The consequences:
- Every distinct timestamp is a new CQL string.
- That string becomes a new `session.prepare()` (a server round-trip, plus a server-side prepared-cache entry).
- It is cached forever in `driver._prepared`.
- In `build_update`/`build_delete` it is also a new key in the module-level caches.

A repro showed 1000 timestamps producing 1001 cache entries.

`build_batch` concatenates statements into one text, so each distinct batch composition is prepared separately as well.

**Fix:**
- Use `USING TTL ? AND TIMESTAMP ?` bind markers.
- Bound the caches (`lru_cache` / an LRU dict).
- Use the driver-native `BatchStatement` (or acsylla's batch API) for batches.

### H8: `_schema()` returns the inherited schema
`_schema()` checks `hasattr(cls, "__schema__") and cls.__schema__ is not None`. That is true for a subclass once the parent's schema has been built. `build_schema` itself correctly checks `"__schema__" in doc_cls.__dict__`.

Repro: `Base._schema(); class Child(Base): extra: Optional[str]` gives `Child._schema()` = `['id']`. `Child.sync_table()` would then miss `extra`.

**Fix:** have `_schema` simply call `build_schema(cls)`.

### H9: python-rs driver ignores per-query options
`_execute_async_impl` accepts `consistency`, `timeout`, `fetch_size` and `paging_state` but never uses them. A user asking for `QUORUM` silently gets the driver default. That is a consistency bug, not just a missing feature. Integration tests skip pagination for python-rs. `_rows_to_dicts` uses `iter_current_page()` (suspected: returns only the first page of a multi-page result).

**Fix:** raise `NotImplementedError` (or warn) when these options are passed until they are supported.

### H10: UDT name mismatch
`types._udt_type_name` uses `(?<=[a-z0-9])(?=[A-Z])`, while `UserType.type_name()` uses the two-regex Django-style algorithm:

```
HTTPAddress.type_name() == "http_address"   python_type_to_cql_type_str(HTTPAddress) == "frozen<httpaddress>"
```

The table DDL references a type that `sync_type()` never creates. **Fix:** have the types layer call `cls.type_name()` when the class is a `UserType`, and keep one `_snake_case` helper.

### M1: Hand-written sync and aio duplication
There is no unasync or codegen. After normalising `async`/`await` and the `aio`/`sync` names, the only real code drift is:
- sync `QuerySet.__len__` (COUNT, see M14)
- `__iter__` vs `__aiter__`
- import ordering and line wrapping

`tests/test_api_parity.py` is a good guard, but every fix in this report has to be made twice.

**Recommendation:** make `aio` the source of truth and generate `sync` with `unasync` (or a small token-replacement script, checked in a pre-commit hook). Alternatively, pull the shared non-I/O logic (CQL planning, LWT parsing, row hydration) into a common mixin so that only the I/O call differs.

### M2: `sync_table` implemented four times
CassandraDriver has a sync and an async copy, and AcsyllaDriver and PythonRsDriver have one each. They have drifted: vector-index creation and `_warm_prepared_cache` exist only in CassandraDriver, and the ALTER statements are built inline instead of through `cql_builder`. python_rs.py re-defines `_is_ddl` without the `not params` guard.

**Recommendation:** add a pure `plan_sync_table(existing_cols, existing_indexes, current_options, model)` function that returns a list of CQL statements. Each driver then only introspects and executes. That also makes the whole planner unit-testable without mocks.

### M3 / M4: Schema sync safety
- `_known_tables` is a per-session memo. `drop_table()` does not clear it, so a subsequent `sync_table()` returns `[]` and the table stays missing (a common pattern in test fixtures).
- `sync_table` only ever adds columns. A changed type, or a column that changed between regular and key, is silently ignored (and adding a new key column fails at runtime). At minimum it should log a warning, as is already done for schema drift.

### M5: Migration runner concurrency
- `_RELEASE_LOCK` is an unconditional `DELETE … WHERE lock_id = ?`. If a migration runs longer than `lock_ttl` (300 s, never renewed, and data migrations easily exceed this), the lock expires, another runner acquires it, and the first runner's `finally` deletes the second runner's lock. Use `DELETE … IF owner = ?` with a unique owner (host + pid + uuid), plus heartbeat renewal or a TTL sized for the migration.
- `allow_destructive` is rendered into generated files but never checked by the runner, so it gives a false sense of safety.
- `_wait_for_schema_agreement()` returns `False` on timeout and the runner proceeds anyway.
- State-table reads and writes use the driver's default consistency (LOCAL_ONE for cassandra-driver). Suspected: a stale read can re-apply a migration. Use QUORUM/SERIAL for the state table.

### M6: Autogen and CLI
- `_SAFE_WIDENING` produces `ALTER TABLE … ALTER col TYPE …`. ScyllaDB does not support this, and Cassandra removed it in 3.0.11/3.10, so the "safe" path generates a migration that fails.
- `diff_schema` builds `model_indexes` only from `col.index`. A vector index created by `sync_table` shows up as a destructive DROP.
- `_load_document_classes` ignores per-model `Settings.keyspace`, diffs `MaterializedView` subclasses as tables, and treats polymorphic subclasses as separate tables (suspected: produces spurious drops of sibling columns).
- The CLI has no `--username/--password/--ssl` options, so it cannot reach most production clusters. Only scylla/cassandra drivers are offered.

### M7: Update API inconsistencies
`Document.update(**kwargs)` writes the raw value to the instance with `object.__setattr__`, without Pydantic validation, and does not reflect collection operations in memory. Unlike `save()` and `delete()`, it has no `consistency`, `timeout`, `batch` or `timestamp` parameters.

### M8 (suspected): Fast path leaks driver-native types
`needs_row_validation=False` for CassandraDriver means `model_construct()` stores whatever the driver returns. That includes `SortedSet` for `set[...]`, `OrderedMapSerializedKey` for `dict`, and namedtuple UDTs (so `UserType._coerce_namedtuple` never runs). Values look right but `isinstance(doc.addr, Address)` is False and `model_dump()` differs.

**Fix:** keep the fast path for scalar-only models and switch to validation per class when a model has collection or UDT fields.

### M9: Quoting and escaping
- Column identifiers are wrapped in `"…"` but embedded `"` is not doubled.
- Keyspace and table are never quoted, so mixed-case names are lowercased by the server.
- String table-option values and `dc` names are interpolated into single quotes without escaping. Verified: `comment = 'it's'` produces invalid CQL. This is not user-input injection in normal use, since these are developer-supplied, but it should be fixed by adding `_q_ident()` / `_q_str()` helpers in `cql_builder`. The MV `__where_clause__` is passed through raw by design; document it.

### M10: `save()` and nulls
`save()` binds `None` for every unset Optional field. That creates a cell tombstone per null column per write, and overwrites columns that another writer may have set (lost-update). cqlengine skips `None` on insert for this reason.

**Recommendation:** add `save(skip_none=True)` (or make that the default) and use `UNSET_VALUE` (protocol v4+) where the driver supports it.

### M11: Typing
`pyproject.toml` enables strict mypy (`disallow_untyped_defs`, `warn_unused_ignores`, …), and `py.typed` is shipped. However, nothing runs mypy: no pre-commit hook and no CI job. `uv run --with mypy mypy src/coodie` reports 67 errors, mostly unused-ignore, attr-defined and type-arg.

Return types also lose precision. `find_one()` and `get()` return `Document`, not `Self`, and `all()` returns a 3-way union, so users have to cast everywhere.

**Recommendation:** use `typing_extensions.Self` / `Generic[DocT]` on `QuerySet`, split `values_list()` into its own return type, and add mypy to CI.

### M12 (suspected): `python-rs` extra
`python-rs = ["scylla>=0.1.0"]` is resolved from PyPI when users run `pip install coodie[python-rs]`, because `[tool.uv.sources]` applies only to uv in this repo. The PyPI name `scylla` is not controlled by this project. This is a supply-chain risk.

**Fix:** remove the extra, or point it at a direct URL reference until the driver is published.

### M13: UDT lifecycle
- `sync_type` is only `CREATE TYPE IF NOT EXISTS`, so adding a field to a `UserType` never reaches the database. The docs say "Create or update".
- `build_alter_type_add` exists but is unused.
- `extract_udt_classes` is unused: `Document.sync_table()` does not sync UDTs, although that would be easy since the dependency walk already exists.

### M14: `__len__` triggers COUNT
`len(qs)` and, more dangerously, `if qs:` issue `SELECT COUNT(*)`. Without a partition key this is a full-cluster scan, and it fails on large tables. Remove `__len__` (aio does not have it), or implement `__bool__` with `LIMIT 1`.

---

## 5. Strengths
- **`cql_builder` is pure and side-effect free**, so most of it can be unit-tested without a cluster. Shape-based template caching is a good idea once the keys are fixed.
- The **schema DSL based on `Annotated` markers** is idiomatic and Pydantic-native. Validation of counter tables and vector-index constraints in `build_schema` gives good early errors.
- `LWTResult` and `PagedResult` are typed result objects rather than raw rows.
- The exception hierarchy is small and coherent.
- Drivers handle **sync-in-async** properly: background-loop bridges for acsylla and python-rs avoid "event loop already running".
- Migrations cover a lot: dry-run, LWT lock, schema agreement, checksums, rollback, autogen with explicit TODO markers for unsafe changes.
- Tests: 1068 unit tests, 82% branch coverage, an API-parity test, workflow-convention tests, and an integration matrix over 4 drivers. CI pins action SHAs and runs 3 OSes × 5 Pythons.
- Very little exception swallowing. The only `except …: pass` blocks are harmless (cassandra.py:211, autogen.py:501).

## 6. Test and CI gaps that let these bugs through
- Unit tests use a mock driver that records CQL. They check the generated strings but not end-to-end semantics, such as projection plus save, connection routing, `IN` arity across calls, or the inherited schema cache.
- No unit test uses `X | None` (C1), `Document.insert()` return values (C2), `scan_table` with more rows than `page_size` per range (C3), `LazyDriver` keyspace or paging (H3), or `CamelCase` UDT names with acronyms (H10).
- Integration runs only on Python 3.12/3.14. Add a 3.10 leg for the scylla driver.
- `migrations/cli.py` has 26% coverage. Driver modules are at 61–71% (cassandra async paths largely untested).
- mypy is not enforced (M11). The newest ruff reports 60 issues beyond the pinned pre-commit version (informational only).

---

## 7. Suggested follow-up PRs (in priority order)

1. **`fix(types): support PEP 604 unions`**: handle `types.UnionType` in types.py and usertype.py, and add tests with `X | None` (run on 3.10). *(C1)*
2. **`fix(document): return LWTResult from insert() and conditional QuerySet.update()`**, with tests that match the docs examples. *(C2, M7)*
3. **`fix(migrations): page within token ranges in scan_table`**, and harden the lock with an owner-conditional release, renewal, and enforcement of `allow_destructive`. *(C3, M5)*
4. **`fix(document): don't clobber unloaded columns`** (save only `model_fields_set`, or refuse after a projection), and fix `_schema()` inheritance. *(H1, H8, M10)*
5. **`fix(drivers): route by connection`**: `QuerySet` and `Batch` use the model's driver; `register_driver` should not steal the default; `LazyDriver` should delegate attributes and keep its kwargs. *(H2, H3)*
6. **`refactor(drivers): return paging state with results`** instead of a shared attribute; fix the cassandra aio multi-page fetch; make python-rs raise on unsupported options. *(H4, H5, H9)*
7. **`perf(cql_builder): bind TTL/TIMESTAMP, bound caches, fix IF-IN shape`**, and use native batch statements. *(H6, H7)*
8. **`fix(usertype): single type_name source; ALTER TYPE ADD for new fields; sync UDTs from sync_table`**. *(H10, M13)*
9. **`refactor: driver-agnostic sync_table planner`** so drivers only introspect and execute. This fixes vector-index drift and `_known_tables` invalidation, and warns on type and key changes. *(M2, M3, M4)*
10. **`build: generate coodie.sync from coodie.aio with unasync`**, and add mypy to CI. *(M1, M11)*
11. **`fix(autogen/cli)`**: drop `ALTER TYPE` widening, include vector indexes, respect per-model keyspace, skip MVs, add auth/SSL flags. *(M6)*
12. **`build(packaging)`**: fix the `python-rs` extra, add Python classifiers, de-duplicate `__all__`. *(M12, N1, N2)*
