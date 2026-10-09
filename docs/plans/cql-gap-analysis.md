# coodie vs. CQL Specification — Gap Analysis Plan

> **Goal:** Systematically compare coodie's implementation against the
> [ScyllaDB CQL Reference](https://docs.scylladb.com/manual/stable/cql/)
> and identify every missing or partially-implemented CQL feature.
> Produce a prioritized implementation roadmap that closes these gaps,
> covering data types, DDL statements, DML features, and ScyllaDB-specific
> extensions.

---

## Table of Contents

1. [Feature Gap Analysis](#1-feature-gap-analysis)
   - [1.1 Data Types](#11-data-types)
   - [1.2 DDL — Keyspace Operations](#12-ddl--keyspace-operations)
   - [1.3 DDL — Table Operations](#13-ddl--table-operations)
   - [1.4 DDL — Index Operations](#14-ddl--index-operations)
   - [1.5 DDL — Materialized Views](#15-ddl--materialized-views)
   - [1.6 DDL — User-Defined Types](#16-ddl--user-defined-types)
   - [1.7 DML — INSERT](#17-dml--insert)
   - [1.8 DML — SELECT](#18-dml--select)
   - [1.9 DML — UPDATE](#19-dml--update)
   - [1.10 DML — DELETE](#110-dml--delete)
   - [1.11 DML — BATCH](#111-dml--batch)
   - [1.12 Secondary Indexes & Filtering](#112-secondary-indexes--filtering)
   - [1.13 Lightweight Transactions (LWT)](#113-lightweight-transactions-lwt)
   - [1.14 ScyllaDB CQL Extensions](#114-scylladb-cql-extensions)
   - [1.15 Security & Access Control](#115-security--access-control)
2. [Gap Summary](#2-gap-summary)
3. [Implementation Phases](#3-implementation-phases)
4. [Test Plan](#4-test-plan)
5. [References](#5-references)

---

## 1. Feature Gap Analysis

Legend:
- ✅ **Implemented** — working in coodie today
- 🔧 **Partial** — infrastructure exists but not fully exposed via public API
- ❌ **Missing** — not yet implemented
- ⊘ **Out of scope** — admin/operational feature, not appropriate for an ORM

### 1.1 Data Types

#### Native Scalar Types

| CQL Type | Python Type (coodie) | Status |
|---|---|---|
| `ascii` | `Annotated[str, Ascii()]` | ✅ |
| `bigint` | `Annotated[int, BigInt()]` | ✅ |
| `blob` | `bytes` | ✅ |
| `boolean` | `bool` | ✅ |
| `counter` | `Annotated[int, Counter()]` via `CounterDocument` | ✅ |
| `date` | `datetime.date` | ✅ |
| `decimal` | `Decimal` | ✅ |
| `double` | `Annotated[float, Double()]` | ✅ |
| `duration` | — | ❌ |
| `float` | `float` | ✅ |
| `inet` | `IPv4Address` / `IPv6Address` | ✅ |
| `int` | `int` | ✅ |
| `smallint` | `Annotated[int, SmallInt()]` | ✅ |
| `text` | `str` | ✅ |
| `time` | `datetime.time` / `Annotated[datetime.time, Time()]` | ✅ |
| `timestamp` | `datetime.datetime` | ✅ |
| `timeuuid` | `Annotated[UUID, TimeUUID()]` | ✅ |
| `tinyint` | `Annotated[int, TinyInt()]` | ✅ |
| `uuid` | `UUID` | ✅ |
| `varchar` | `str` (alias for `text`) | ✅ implicit |
| `varint` | `Annotated[int, VarInt()]` | ✅ |

#### Collection & Complex Types

| CQL Type | Python Type (coodie) | Status |
|---|---|---|
| `list<T>` | `list[T]` | ✅ |
| `set<T>` | `set[T]` | ✅ |
| `map<K,V>` | `dict[K,V]` | ✅ |
| `tuple<T1,T2,...>` | `tuple[T1,T2,...]` | ✅ |
| `frozen<T>` | `Annotated[T, Frozen()]` | ✅ |
| `vector<float, N>` | — | ❌ |
| User-Defined Types | `UserType(BaseModel)` subclass | ✅ |

**Gap summary — data types:**
- `duration` → Add a `Duration` marker class in `fields.py` and map to CQL `duration`. Python representation could use a custom dataclass or `datetime.timedelta` (note: CQL duration has months+days+nanoseconds which `timedelta` cannot fully represent). A custom `CqlDuration` dataclass with `months`, `days`, `nanoseconds` fields is the recommended approach.
- `vector<float, N>` → Add a `Vector(dimensions=N)` marker class in `fields.py`. Map `Annotated[list[float], Vector(dimensions=5)]` to `vector<float, 5>`. Add `VectorIndex` for ANN index creation and `order_by_ann()` for similarity searches. Note: this is experimental in ScyllaDB and requires specific driver support.

### 1.2 DDL — Keyspace Operations

| CQL Statement | coodie API | Status |
|---|---|---|
| `CREATE KEYSPACE IF NOT EXISTS` | `create_keyspace()` | ✅ |
| `DROP KEYSPACE IF EXISTS` | `drop_keyspace()` | ✅ |
| `ALTER KEYSPACE` | — | ❌ |
| `USE keyspace` | — (implicit via `Settings.keyspace` or `init_coodie(keyspace=)`) | ✅ implicit |
| `durable_writes` option | — | ❌ |
| `tablets` option (ScyllaDB) | — | ❌ |

**Gap summary — keyspace operations:**
- `ALTER KEYSPACE` → Add `alter_keyspace(name, replication_factor=, dc_replication_map=, durable_writes=)` function and `build_alter_keyspace()` in `cql_builder.py`.
- `durable_writes` → Add as optional parameter to `create_keyspace()` and `alter_keyspace()`.
- `tablets` → Add as optional parameter to `create_keyspace()` for ScyllaDB tablet-enabled keyspaces (e.g. `tablets = {'enabled': true}`).

### 1.3 DDL — Table Operations

| CQL Statement | coodie API | Status |
|---|---|---|
| `CREATE TABLE IF NOT EXISTS` | `Document.sync_table()` | ✅ |
| `DROP TABLE IF EXISTS` | `Document.drop_table()` | ✅ |
| `ALTER TABLE ADD column` | `sync_table()` (auto-detects new columns) | ✅ |
| `ALTER TABLE DROP column` | — | ❌ |
| `ALTER TABLE RENAME column` | — | ❌ |
| `ALTER TABLE WITH options` | `sync_table()` (auto-detects option changes) | ✅ |
| `TRUNCATE TABLE` | — | ❌ |
| Table compaction options | `Settings.__options__` | ✅ |
| `default_time_to_live` | `Settings.__default_ttl__` | ✅ |
| `CLUSTERING ORDER BY` | `ClusteringKey(order="DESC")` | ✅ |
| Composite partition key | `PrimaryKey(partition_key_index=N)` | ✅ |
| Static columns | `Annotated[T, Static()]` | ✅ |

**Gap summary — table operations:**
- `TRUNCATE TABLE` → Add `Document.truncate()` (sync + async) that generates `TRUNCATE TABLE keyspace.table` and `build_truncate()` in `cql_builder.py`. This is a commonly-needed operation for test fixtures and data resets.
- `ALTER TABLE DROP` → Destructive schema change — should be handled through coodie's **migration framework** (Tier 2 migration files) rather than an ad-hoc `sync_table()` flag. Add `ctx.execute("ALTER TABLE … DROP …")` support and a `build_alter_table_drop()` helper in `cql_builder.py`. See [Migration Strategy — Tier 2](migration-strategy.md#54-tier-2--migration-files-production-schema-changes) for the migration file workflow.
- `ALTER TABLE RENAME` → Destructive schema change — should also go through the migration framework. Low priority; rarely used in CQL and only supported for clustering columns in Cassandra ≥ 4.0 / ScyllaDB. See [Migration Strategy — Cassandra Constraints](migration-strategy.md#4-cassandra--scylladb-schema-constraints).

### 1.4 DDL — Index Operations

| CQL Feature | coodie API | Status |
|---|---|---|
| `CREATE INDEX IF NOT EXISTS` | `Indexed()` marker → auto-created by `sync_table()` | ✅ |
| `DROP INDEX IF EXISTS` | `sync_table(drop_removed_indexes=True)` | ✅ |
| Custom index name | `Indexed(index_name="my_idx")` | ✅ |
| Custom index class (SAI) | — | ❌ |
| Index options (`WITH OPTIONS`) | — | ❌ |
| Index on collection elements (`KEYS`, `VALUES`, `ENTRIES`, `FULL`) | — | ❌ |

**Gap summary — index operations:**
- Custom index class → Extend `Indexed()` to accept `index_class="org.apache.cassandra.index.sai.StorageAttachedIndex"` and emit `USING 'class'` in `build_create_index()`.
- Index options → Extend `Indexed()` to accept `options={"case_sensitive": "false"}` for SAI/SASI configuration.
- Collection index targets → Support `KEYS(col)`, `VALUES(col)`, `ENTRIES(col)`, `FULL(col)` as index targets for map/set/list columns.

### 1.5 DDL — Materialized Views

| CQL Feature | coodie API | Status |
|---|---|---|
| `CREATE MATERIALIZED VIEW` | `MaterializedView.sync_view()` | ✅ |
| `DROP MATERIALIZED VIEW` | `MaterializedView.drop_view()` | ✅ |
| `ALTER MATERIALIZED VIEW` | — | ❌ |
| View with custom table options | — | 🔧 clustering order supported, but not compaction/TTL on view |

**Gap summary — materialized views:**
- `ALTER MATERIALIZED VIEW` → DDL change — should be handled through coodie's **migration framework** (Tier 2 migration files) for controlled, reversible schema evolution. Add `build_alter_materialized_view()` helper in `cql_builder.py` for changing view table properties (compaction, TTL). See [Migration Strategy — Tier 2](migration-strategy.md#54-tier-2--migration-files-production-schema-changes) for the migration file workflow.
- View table options → Allow `Settings.__options__` on `MaterializedView` to emit `WITH` clause on view creation.

### 1.6 DDL — User-Defined Types

| CQL Feature | coodie API | Status |
|---|---|---|
| `CREATE TYPE IF NOT EXISTS` | `UserType.sync_type()` / `sync_type_async()` | ✅ |
| `DROP TYPE IF EXISTS` | `build_drop_type()` exists, no public API | 🔧 |
| `ALTER TYPE ADD field` | `build_alter_type_add()` exists, no public API | 🔧 |
| `ALTER TYPE RENAME field` | — | ❌ |
| Nested UDTs | Recursive dependency resolution | ✅ |
| UDTs inside collections | Auto-detected | ✅ |

**Gap summary — UDT operations:**
- All UDT DDL changes (`DROP TYPE`, `ALTER TYPE ADD`, `ALTER TYPE RENAME`) are **schema mutations** and should flow through coodie's **migration framework** (Tier 2 migration files) per [migration-strategy.md](migration-strategy.md). Users can execute these via raw CQL calls inside versioned migration files — no extra ORM helpers needed. The existing `build_drop_type()` and `build_alter_type_add()` internal builders remain available for migration authors who want programmatic CQL generation, but no new public API (e.g. `UserType.drop_type()`) is required.

### 1.7 DML — INSERT

| CQL Feature | coodie API | Status |
|---|---|---|
| `INSERT INTO ... VALUES (...)` | `Document.save()` | ✅ |
| `IF NOT EXISTS` | `Document.insert()` | ✅ |
| `USING TTL` | `save(ttl=N)` | ✅ |
| `USING TIMESTAMP` | `save(timestamp=N)` | ✅ |
| `INSERT INTO ... JSON '{...}'` | — | ❌ |

**Gap summary — INSERT / JSON support across the board:**
- `INSERT JSON` → Add `Document.save_json()` or `QuerySet.create_json()` that serializes the document to JSON and uses `INSERT INTO ... JSON '...'`. Useful for bulk data loading from JSON sources.
- `SELECT JSON` → Add `QuerySet.json()` that emits `SELECT JSON *` and returns raw JSON strings per row (see also §1.8).
- **JSON field storage** → Consider a `Json()` field marker (e.g. `Annotated[dict, Json()]`) that transparently serializes Python dicts to JSON text on write and deserializes on read, stored as a CQL `text` column. This enables schema-less sub-documents within a typed model.
- **JSON round-trip fidelity** → Document how CQL `INSERT JSON` / `SELECT JSON` handles type coercion (e.g. `bigint` ↔ JSON number, `uuid` ↔ JSON string, `date` ↔ JSON string). Ensure coodie's serialization/deserialization matches CQL's JSON encoding rules.
- **JSON API ergonomics** → For web-framework integration (FastAPI, Flask), a `.to_json()` method on `Document` or `QuerySet` results would allow direct HTTP response streaming without intermediate Python object materialization.

### 1.8 DML — SELECT

| CQL Feature | coodie API | Status |
|---|---|---|
| `SELECT * FROM` | `Document.find().all()` | ✅ |
| `SELECT col1, col2` | `QuerySet.only("col1", "col2")` | ✅ |
| `WHERE` clause | `QuerySet.filter()` | ✅ |
| `ORDER BY` | `QuerySet.order_by()` | ✅ |
| `LIMIT` | `QuerySet.limit(N)` | ✅ |
| `PER PARTITION LIMIT` | `QuerySet.per_partition_limit(N)` | ✅ |
| `ALLOW FILTERING` | `QuerySet.allow_filtering()` | ✅ |
| `DISTINCT` (partition-level) | — | ❌ |
| `GROUP BY` (clustering columns) | — | ❌ |
| `COUNT(*)` | `QuerySet.count()` | ✅ |
| `SUM()`, `AVG()`, `MIN()`, `MAX()` | — | ❌ |
| `CAST()` | — | ❌ |
| `SELECT JSON` | — | ❌ |
| `WRITETIME(col)` | — | ❌ |
| `TTL(col)` | — | ❌ |
| `TOKEN()` in WHERE | `__token__gt`, `__token__gte`, etc. | ✅ |
| `TOKEN()` in SELECT | — | ❌ |
| Paging (`fetch_size`, `paging_state`) | `QuerySet.fetch_size()`, `.page()`, `.paged_all()` | ✅ |

**Gap summary — SELECT:**
- `DISTINCT` → Add `QuerySet.distinct()` that emits `SELECT DISTINCT`. Only meaningful for partition key columns.
- `GROUP BY` → Add `QuerySet.group_by(*cols)` that appends `GROUP BY` clause. Restricted to clustering columns in CQL.
- Aggregate functions (`SUM`, `AVG`, `MIN`, `MAX`) → Add `QuerySet.aggregate("sum", "col")` or dedicated methods like `QuerySet.sum("col")`, `QuerySet.avg("col")`. These generate `SELECT SUM("col") FROM ...`.
- `SELECT JSON` → Add `QuerySet.json()` that returns raw JSON strings per row. Useful for direct API responses. See §1.7 for full JSON support discussion (INSERT JSON, Json() field, to_json(), type coercion).
- `WRITETIME(col)` / `TTL(col)` → Add `QuerySet.with_writetime("col")` and `QuerySet.with_ttl("col")` to include metadata columns in the result set. Lower priority.
- `CAST()` → Very low priority; mostly used in ad-hoc CQL. Can be done via `execute_raw()`.

### 1.9 DML — UPDATE

| CQL Feature | coodie API | Status |
|---|---|---|
| `UPDATE ... SET col = ?` | `Document.update(col=val)` | ✅ |
| `USING TTL` | `update(ttl=N)` | ✅ |
| `USING TIMESTAMP` | `update(timestamp=N)` via `build_update` | ✅ |
| `IF EXISTS` | `update(if_exists=True)` | ✅ |
| `IF col = ?` (LWT conditions) | `update(if_conditions={...})` | ✅ |
| Collection `+` / `-` (append/remove) | `update(tags__add={...})`, `tags__remove={...}` | ✅ |
| List prepend (`[val] + col`) | `update(tags__prepend=[...])` | ✅ |
| Map put (`col[key] = val`) | — | ❌ |
| List set by index (`col[idx] = val`) | — | ❌ |
| Counter `SET col = col + ?` | `CounterDocument.increment()` / `decrement()` | ✅ |

**Gap summary — UPDATE:**
- Map put (`col[key] = val`) → Add `col__put` or `col__setitem` collection operator to set a specific map key.
- List set by index → Add `col__setindex` collection operator. Generates `SET "col"[?] = ?`.

### 1.10 DML — DELETE

| CQL Feature | coodie API | Status |
|---|---|---|
| `DELETE FROM table WHERE ...` | `Document.delete()` / `QuerySet.delete()` | ✅ |
| `DELETE col FROM table WHERE ...` | `Document.delete_columns("col")` | ✅ |
| `IF EXISTS` | `delete(if_exists=True)` | ✅ |
| `USING TIMESTAMP` | `delete(timestamp=N)` | ✅ |
| `DELETE col[key] FROM ...` (map element) | — | ❌ |
| `DELETE col[idx] FROM ...` (list element) | — | ❌ |

**Gap summary — DELETE:**
- Collection element delete → Add support for `delete_columns("col[key]")` or a dedicated `delete_map_element()` / `delete_list_element()` API. Generates `DELETE "col"[?] FROM ...`.

### 1.11 DML — BATCH

| CQL Feature | coodie API | Status |
|---|---|---|
| `BEGIN BATCH ... APPLY BATCH` | `BatchQuery` / `AsyncBatchQuery` | ✅ |
| `BEGIN UNLOGGED BATCH` | `BatchQuery(logged=False)` | ✅ |
| `BEGIN COUNTER BATCH` | `BatchQuery(batch_type="COUNTER")` | ✅ |
| `USING TIMESTAMP` on batch | — | ❌ |

**Gap summary — BATCH:**
- `USING TIMESTAMP` on batch → Add optional `timestamp` parameter to `BatchQuery` and `AsyncBatchQuery` that emits `BEGIN BATCH USING TIMESTAMP ?`.

### 1.12 Secondary Indexes & Filtering

| CQL Feature | coodie API | Status |
|---|---|---|
| `=` | `filter(col=val)` | ✅ |
| `>`, `>=`, `<`, `<=` | `filter(col__gt=val)`, etc. | ✅ |
| `IN` | `filter(col__in=[...])` | ✅ |
| `CONTAINS` | `filter(col__contains=val)` | ✅ |
| `CONTAINS KEY` | `filter(col__contains_key=val)` | ✅ |
| `LIKE` (SASI/SAI) | `filter(col__like=pattern)` | ✅ |
| `!=` | `filter(col__ne=val)` | ✅ |
| `TOKEN()` range queries | `filter(col__token__gt=val)` | ✅ |
| `IS NOT NULL` | — | ❌ |

**Gap summary — filtering:**
- `IS NOT NULL` → Add `filter(col__isnull=False)` that generates `"col" IS NOT NULL`. Useful for materialized view queries and sparse data patterns.

### 1.13 Lightweight Transactions (LWT)

| CQL Feature | coodie API | Status |
|---|---|---|
| `INSERT ... IF NOT EXISTS` | `Document.insert()` | ✅ |
| `UPDATE ... IF EXISTS` | `update(if_exists=True)` | ✅ |
| `UPDATE ... IF col = ?` | `update(if_conditions={col: val})` | ✅ |
| `DELETE ... IF EXISTS` | `delete(if_exists=True)` | ✅ |
| `DELETE ... IF col = ?` | — | ❌ |
| LWT result parsing (`[applied]`) | `LWTResult` dataclass | ✅ |
| `IF col != ?` | — | ❌ |
| `IF col IN (?)` | — | ❌ |
| `IF col > ?` / `IF col < ?` | — | ❌ |

**Gap summary — LWT:**
- `DELETE ... IF col = ?` → Add `if_conditions` parameter to `Document.delete()` and `QuerySet.delete()`.
- Rich LWT conditions (`!=`, `IN`, `>`, `<`) → Extend `if_conditions` to accept operator-suffixed keys (e.g. `if_conditions={"col__ne": val}`) or a separate `if_condition_triples` parameter.

### 1.14 ScyllaDB CQL Extensions

| ScyllaDB Extension | coodie API | Status |
|---|---|---|
| `USING TIMEOUT` | Driver-level `timeout=` parameter | 🔧 passed to driver, not CQL |
| `BYPASS CACHE` | — | ❌ |
| `USING TIMEOUT` in CQL statement | — | ❌ |
| Workload prioritization | — | ⊘ operational concern |
| Tablets-enabled keyspace | — | ❌ (see §1.2) |

**Gap summary — ScyllaDB extensions:**
- `BYPASS CACHE` → Add `QuerySet.bypass_cache()` that appends `BYPASS CACHE` to SELECT statements. Useful for analytics queries that should not pollute the cache.
- `USING TIMEOUT` in CQL → Currently timeout is passed to the driver at execution time. Could optionally emit `USING TIMEOUT Nms` in the CQL itself for ScyllaDB. Low priority since driver-level timeout works for all backends.

### 1.15 Security & Access Control

| CQL Statement | coodie API | Status |
|---|---|---|
| `CREATE ROLE` / `DROP ROLE` / `ALTER ROLE` | — | ❌ |
| `GRANT` / `REVOKE` | — | ❌ |
| `LIST USERS` / `LIST ROLES` | — | ❌ |
| `CREATE USER` / `DROP USER` / `ALTER USER` | — | ❌ |
| Execute query as specific role | — | ❌ |

**Gap summary — security:**
- The ODM must make roles/users easy to use at every layer: init, QuerySet, and Document operations.
- **Connection-level role** → `init_coodie(driver, hosts=..., role="app_reader")` sets the default role for the session. All queries use this role unless overridden.
- **Per-query role** → `QuerySet.as_role(role_name)` executes a single query under a different role. Example: `User.objects().as_role("admin").all()`. This chains naturally with existing QuerySet methods (`filter()`, `limit()`, `order_by()`, etc.).
- **Document operations** → `Document.save(role="writer")`, `Document.delete(role="writer")` pass the role through to the underlying query execution, so CRUD operations respect role-based access without extra boilerplate.
- **Role management helpers** → `create_role()`, `drop_role()`, `alter_role()`, `grant()`, `revoke()`, `list_roles()`, `list_users()` provide ODM-level functions for role administration. Users can also execute raw CQL through the driver for advanced role configurations.
- **Multi-tenant pattern** → Applications that serve multiple tenants can store a `current_role` in request context and apply it via `QuerySet.as_role()` in middleware, keeping role switching transparent to business logic.

---

## 2. Gap Summary

### High Priority (commonly used, broad impact)

| # | Feature | Scope | Notes |
|---|---|---|---|
| H1 | `TRUNCATE TABLE` | DDL | Essential for test fixtures and data resets |
| H2 | `duration` data type | Types | CQL native type with no coodie mapping |
| H3 | `SELECT DISTINCT` | DML | Partition key unique retrieval |
| H4 | `GROUP BY` | DML | Aggregate queries by clustering columns |
| H5 | Aggregate functions (`SUM`, `AVG`, `MIN`, `MAX`) | DML | Server-side aggregation |
| H6 | `ALTER KEYSPACE` | DDL | Modify replication strategy at runtime |
| H7 | `IS NOT NULL` filter | DML | Used in MV queries and sparse data |
| H8 | `DELETE ... IF conditions` | LWT | Conditional deletes beyond `IF EXISTS` |

### Medium Priority (useful, less commonly needed)

| # | Feature | Scope | Notes |
|---|---|---|---|
| M1 | JSON support (`INSERT JSON`, `SELECT JSON`, `Json()` field, `to_json()`) | DML | Full JSON serialization: CQL round-trip, field storage, API ergonomics |
| M2 | Custom index class (SAI) | DDL | Storage-attached index configuration |
| M3 | Index on collection elements | DDL | `KEYS()`, `VALUES()`, `ENTRIES()`, `FULL()` targets |
| M4 | Map put / list set-by-index | DML | Fine-grained collection mutation |
| M5 | `USING TIMESTAMP` on batch | DML | Batch-level timestamp control |
| M6 | `BYPASS CACHE` (ScyllaDB) | Extension | Analytics query cache bypass |
| M7 | `ALTER TABLE DROP column` | DDL | Destructive — use migration framework (see [migration-strategy.md](migration-strategy.md)) |
| M8 | Rich LWT conditions (`!=`, `IN`, `>`, `<`) | LWT | Operator-based conditional mutations |
| M9 | `WRITETIME()` / `TTL()` functions | DML | Metadata column projection |
| M10 | `vector<float, N>` data type | Types | Vector search / ANN support |
| M11 | Role/user management & per-query role | Security | ODM-level role support: `init_coodie(role=)`, `QuerySet.as_role()`, `Document.save(role=)` |

### Low Priority (rarely used, edge cases)

| # | Feature | Scope | Notes |
|---|---|---|---|
| L1 | `ALTER MATERIALIZED VIEW` | DDL | DDL change — use migration framework (see [migration-strategy.md](migration-strategy.md)) |
| L2 | `ALTER TYPE RENAME` | DDL | DDL change — use migration framework (see [migration-strategy.md](migration-strategy.md)) |
| L3 | `ALTER TABLE RENAME` | DDL | Destructive — use migration framework (see [migration-strategy.md](migration-strategy.md)) |
| L4 | `CAST()` in SELECT | DML | Type conversion in queries |
| L5 | `USING TIMEOUT` in CQL | Extension | CQL-level timeout (driver timeout works) |
| L6 | `TOKEN()` in SELECT | DML | Include token value in result set |
| L7 | Delete collection elements | DML | `DELETE col[key]` syntax |
| L8 | `durable_writes` on keyspace | DDL | Keyspace creation option |
| L9 | `tablets` on keyspace | DDL | ScyllaDB tablet-enabled keyspaces |
| L10 | UDT DDL (`DROP TYPE`, `ALTER TYPE ADD`) | DDL | Use migration framework — raw CQL in migration files; no new public API needed |

---

## 3. Implementation Phases

### Phase 1: Core DML Gaps (Priority: High)

**Goal:** Close the most impactful DML gaps — `TRUNCATE`, `DISTINCT`, `GROUP BY`, aggregates, and `IS NOT NULL`.

| Task | Description |
|---|---|
| 1.1 | Add `build_truncate(table, keyspace)` to `cql_builder.py` |
| 1.2 | Add `Document.truncate()` and async variant to `aio/document.py` and `sync/document.py` |
| 1.3 | Add `QuerySet.distinct()` that emits `SELECT DISTINCT` in `build_select()` |
| 1.4 | Add `QuerySet.group_by(*cols)` that appends `GROUP BY` clause to `build_select()` |
| 1.5 | Add `QuerySet.sum(col)`, `.avg(col)`, `.min(col)`, `.max(col)` aggregate methods |
| 1.6 | Add `build_aggregate(table, keyspace, func, col, where, ...)` to `cql_builder.py` |
| 1.7 | Add `__isnull` filter operator mapping to `IS NOT NULL` / `IS NULL` in `parse_filter_kwargs()` |
| 1.8 | Unit + integration tests for all Phase 1 features |

### Phase 2: Data Type Gaps (Priority: High)

**Goal:** Add the `duration` CQL type and lay groundwork for the `vector` type.

| Task | Description |
|---|---|
| 2.1 | Create `CqlDuration` dataclass in `coodie/types.py` with `months`, `days`, `nanoseconds` fields |
| 2.2 | Add `Duration` marker class to `fields.py` |
| 2.3 | Register `CqlDuration` → `"duration"` in `_SCALAR_CQL_TYPES` |
| 2.4 | Add serialization/deserialization for `CqlDuration` ↔ CQL duration encoding |
| 2.5 | Add `Vector(dimensions=N)` marker class to `fields.py` |
| 2.6 | Map `Annotated[list[float], Vector(dimensions=N)]` → `vector<float, N>` in `python_type_to_cql_type_str()` |
| 2.7 | Add `VectorIndex` marker for ANN index creation |
| 2.8 | Unit + integration tests for duration and vector types |

### Phase 3: DDL & Keyspace Gaps (Priority: Medium)

**Goal:** Add `ALTER KEYSPACE`, `ALTER TABLE DROP`, keyspace options, and custom index support.

| Task | Description |
|---|---|
| 3.1 | Add `build_alter_keyspace()` to `cql_builder.py` |
| 3.2 | Add `alter_keyspace()` to `aio/__init__.py` and `sync/__init__.py` |
| 3.3 | Add `durable_writes` parameter to `build_create_keyspace()` and `create_keyspace()` |
| 3.4 | Add `tablets` parameter to `build_create_keyspace()` for ScyllaDB |
| 3.5 | Add `build_alter_table_drop()` helper in `cql_builder.py`; integrate column-drop as a migration operation (Tier 2) per [migration-strategy.md](migration-strategy.md) |
| 3.6 | Extend `Indexed()` to accept `index_class` and `options` parameters |
| 3.7 | Update `build_create_index()` to emit `USING 'class'` and `WITH OPTIONS` |
| 3.8 | Add collection index targets (`KEYS`, `VALUES`, `ENTRIES`, `FULL`) support to `Indexed()` |
| 3.9 | Unit + integration tests for all Phase 3 features |

### Phase 4: LWT & Collection Operations (Priority: Medium)

**Goal:** Enrich LWT conditions and fine-grained collection mutation support.

| Task | Description |
|---|---|
| 4.1 | Add `if_conditions` parameter to `Document.delete()` and `QuerySet.delete()` |
| 4.2 | Add `build_delete()` support for `IF col = ?` conditions |
| 4.3 | Extend `if_conditions` to support operator-suffixed keys (`col__ne`, `col__gt`, `col__in`) |
| 4.4 | Add map put operator (`col__put`) to `parse_update_kwargs()` → generates `"col"[?] = ?` |
| 4.5 | Add list set-by-index operator (`col__setindex`) → generates `"col"[?] = ?` |
| 4.6 | Add batch-level `USING TIMESTAMP` to `build_batch()` and `BatchQuery` |
| 4.7 | Unit + integration tests for all Phase 4 features |

### Phase 5: JSON & Metadata Features (Priority: Medium)

**Goal:** Add comprehensive JSON support (INSERT JSON, SELECT JSON, JSON field storage) and metadata projection.

| Task | Description |
|---|---|
| 5.1 | Add `build_insert_json()` to `cql_builder.py` |
| 5.2 | Add `Document.save_json()` / `QuerySet.create_json()` methods |
| 5.3 | Add `build_select_json()` variant that emits `SELECT JSON` |
| 5.4 | Add `QuerySet.json()` method that returns JSON string rows |
| 5.5 | Add `Json()` field marker for transparent JSON serialization of `dict` fields stored as CQL `text` |
| 5.6 | Add `Document.to_json()` convenience method for web-framework integration |
| 5.7 | Document CQL JSON type-coercion rules (bigint ↔ number, uuid ↔ string, etc.) and ensure coodie round-trip fidelity |
| 5.8 | Add `QuerySet.with_writetime(*cols)` / `QuerySet.with_ttl(*cols)` for metadata projection |
| 5.9 | Unit + integration tests for all Phase 5 features |

### Phase 6: ScyllaDB Extensions & Low-Priority Gaps (Priority: Low)

**Goal:** Add ScyllaDB-specific CQL extensions and remaining low-priority features.

| Task | Description |
|---|---|
| 6.1 | Add `QuerySet.bypass_cache()` that appends `BYPASS CACHE` to SELECT |
| 6.2 | Document UDT DDL operations (`DROP TYPE`, `ALTER TYPE ADD/RENAME`) as migration-only operations; add example migration files |
| 6.3 | Add delete-collection-element support (`DELETE col[key]`) |
| 6.4 | Add `TOKEN()` in SELECT projection |
| 6.5 | Add `build_alter_materialized_view()` helper in `cql_builder.py`; integrate as a migration operation (Tier 2) per [migration-strategy.md](migration-strategy.md) |
| 6.6 | Add role/user management helpers (`create_role()`, `drop_role()`, `grant()`, `revoke()`, `list_roles()`) |
| 6.7 | Add `QuerySet.as_role(role_name)` for per-query role execution; add `role=` parameter to `Document.save()` / `Document.delete()` |
| 6.8 | Add `role=` parameter to `init_coodie()` / `init_coodie_async()` for connection-level default role |
| 6.9 | Unit + integration tests for all Phase 6 features |

---

## 4. Test Plan

### 4.1 Unit Tests

#### `tests/test_cql_builder.py`

| Test Case | Phase |
|---|---|
| `build_truncate()` returns correct CQL | 1 |
| `build_select()` with `distinct=True` emits `SELECT DISTINCT` | 1 |
| `build_select()` with `group_by` emits `GROUP BY` clause | 1 |
| `build_aggregate()` generates `SELECT SUM/AVG/MIN/MAX` | 1 |
| `parse_filter_kwargs()` handles `__isnull` → `IS NOT NULL` / `IS NULL` | 1 |
| `build_alter_keyspace()` generates correct CQL | 3 |
| `build_create_keyspace()` with `durable_writes` parameter | 3 |
| `build_create_keyspace()` with `tablets` parameter | 3 |
| `build_create_index()` with `index_class` and `options` | 3 |
| `build_delete()` with `if_conditions` parameter | 4 |
| `parse_update_kwargs()` handles `col__put` and `col__setindex` | 4 |
| `build_batch()` with `timestamp` parameter | 4 |
| `build_insert_json()` generates `INSERT INTO ... JSON` | 5 |
| `build_select_json()` generates `SELECT JSON *` | 5 |
| `Json()` field marker serializes dict to JSON text | 5 |
| `build_select()` with `bypass_cache=True` emits `BYPASS CACHE` | 6 |
| `create_role()` / `drop_role()` generates correct CQL | 6 |
| `grant()` / `revoke()` generates correct CQL | 6 |
| `QuerySet.as_role()` sets role execution context | 6 |
| `Document.save(role=)` passes role to query execution | 6 |
| `Document.delete(role=)` passes role to query execution | 6 |
| `init_coodie(role=)` sets connection-level default role | 6 |

#### `tests/test_types.py`

| Test Case | Phase |
|---|---|
| `CqlDuration` → `"duration"` mapping | 2 |
| `Annotated[CqlDuration, Duration()]` → `"duration"` | 2 |
| `Annotated[list[float], Vector(dimensions=5)]` → `"vector<float, 5>"` | 2 |

### 4.2 Integration Tests

| Test Area | Test Cases | Phase |
|---|---|---|
| **TRUNCATE** | Create rows, truncate, verify empty | 1 |
| **DISTINCT** | Insert multi-partition data, SELECT DISTINCT, verify unique partitions | 1 |
| **GROUP BY** | Insert grouped data, GROUP BY clustering column, verify aggregation | 1 |
| **Aggregates** | Insert numeric data, verify SUM/AVG/MIN/MAX results | 1 |
| **IS NOT NULL** | Filter with `__isnull=False`, verify results | 1 |
| **Duration** | Insert/read duration values, verify round-trip | 2 |
| **Vector** | Insert/read vector values, create vector index, ANN query | 2 |
| **ALTER KEYSPACE** | Create keyspace, alter replication, verify change | 3 |
| **Custom index** | Create SAI index, query with it | 3 |
| **LWT DELETE** | Conditional delete with `if_conditions`, verify result | 4 |
| **Map put** | Update specific map key, verify | 4 |
| **JSON round-trip** | INSERT JSON / SELECT JSON, verify fidelity with all CQL types | 5 |
| **Json() field** | Store dict as JSON text, read back, verify round-trip | 5 |
| **to_json()** | Serialize Document to JSON string, verify correct encoding | 5 |
| **BYPASS CACHE** | SELECT with BYPASS CACHE, verify no error | 6 |
| **Role management** | Create role, grant permissions, execute query as role, verify access | 6 |
| **Role via ODM** | `QuerySet.as_role()`, `Document.save(role=)`, `init_coodie(role=)` — verify role propagation end-to-end | 6 |

---

## 5. References

- [ScyllaDB CQL Reference](https://docs.scylladb.com/manual/stable/cql/)
- [ScyllaDB Data Types](https://docs.scylladb.com/manual/stable/cql/types.html)
- [ScyllaDB Data Definition (DDL)](https://docs.scylladb.com/manual/stable/cql/ddl.html)
- [ScyllaDB Data Manipulation (DML)](https://docs.scylladb.com/manual/stable/cql/dml.html)
- [ScyllaDB CQL Extensions](https://docs.scylladb.com/manual/stable/cql/cql-extensions.html)
- [Apache Cassandra CQL Reference](https://cassandra.apache.org/doc/stable/cassandra/developing/cql/)
- [coodie cqlengine Feature-Parity Plan](archive/cqlengine-feature-parity.md)
- [coodie Python-RS Driver Support Plan](python-rs-driver-support.md)
