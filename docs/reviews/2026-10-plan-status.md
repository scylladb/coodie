# coodie — docs/plans audit (2026-10-09)

Status was checked against code, tests, docs and workflows on the current branch (base e2a6e66). It does not rely on the plans' own checkmarks, which are stale in both directions.
Legend: DONE · PARTIAL · MISSING · OPEN PR · OBSOLETE · BLOCKED (waiting on upstream)

## 1. Summary table

| Plan | Status | Done phases | Open PR | Remaining |
|---|---|---|---|---|
| client-encryption.md | COMPLETE → archive | 1, 2, 3 | — | — |
| cqlengine-feature-parity.md | COMPLETE → archive | 1–13 | #121 (overlaps the §5 migration guide) | UDT driver registration is tracked in udt-support Ph6; stale §1.4/§1.5 text |
| cqlengine-missing-features.md | COMPLETE → archive (duplicates parity + udt) | Features 3–8, A, B | — | Leftover UDT items belong to udt-support Ph4/Ph6 |
| cqlengine-test-coverage-plan.md | NEARLY COMPLETE | 1, 2, 3, 5 | — | 4.5 UDT-in-list round-trip; Ph6 (LWTException/`iff()`) superseded by `LWTResult` + `if_conditions` → mark won't-do. The file is truncated mid-row at 6.2 |
| cql-gap-analysis.md | OPEN (most remaining work) | 4 | — | Ph1 integration tests + docs; Ph2 duration integration test + docs; Ph3 mostly missing; Ph5 partial; Ph6 mostly missing |
| demos-extension-plan.md | OPEN | 1–6, 10 | #232 (7.2), #231 (8.1/8.2) | 8.3 migration-guide demo; Ph9 README/polish; §11 CI smoke tests; §10 monitoring "War Room" |
| documentation-plan.md | COMPLETE (content stale) | 1–6 | #116 (archive, conflicting) | Refresh llms.txt/llms-full.txt; fix stale "planned Phase C" note |
| github-actions-testing-plan.md | COMPLETE except obsolete Ph4 → archive | 1, 2, 3 | #247 (touches it; stale), #116 | Ph4 targets `/rebase`/`/squash`, which #219 removed → mark obsolete |
| integration-test-coverage.md | OBSOLETE (every gap closed) → archive or rewrite | all 8 items | — | Optional new gap list (see details) |
| migration-strategy.md | NEARLY COMPLETE | A, B, C (except C.1 options), D | — | C.1 table-options diff; document `makemigration`/`schema-diff`/`scan_table` |
| performance-improvement.md | OPEN | 1–7, 8b, 9; 8 partial | — | Ph10: 10.3, 10.5, 10.6, 10.7, 10.8, 10.9; §13C.5 results; stale §13G.6 |
| plan-phase-continuation-action.md | COMPLETE → archive | 1–6 | — | Gap: `.github/scripts/test_parse_plan.py` never runs in CI |
| python-rs-driver-support.md | MOSTLY DONE | 2, 5; 4 mostly | — | 1.1/1.4/1.5 build target + docs; Ph3 namespace check; 4.6 report |
| python-rs-feature-gaps.md | OPEN | 2 | — | Ph1 + Ph6 doable now; Ph3/4/5 BLOCKED upstream |
| raw-dc-benchmark-plan.md | COMPLETE → archive | 1 | — | — |
| rewrite-coodie-plan.md | HISTORICAL → archive | 0–5 | #116 | — |
| silent-exception-pass.md | COMPLETE → archive | 1 | — | Unaudited `except ImportError: pass` at `drivers/cassandra.py:211` |
| sync-api-support.md | NEARLY COMPLETE | 1–4 | — | Ph5 docs (5.2 docstrings, 5.4 drivers.md section, stale acsylla note) |
| test-refactoring-plan.md | COMPLETE → archive | Tasks 1–6 | #116 | The 5 unchecked boxes are "verify in CI" items, already covered by the CI matrix |
| udt-support.md | OPEN (Ph4 ✅ is wrong) | 1, 2, 3 | — | Ph4 partial (driver sync_type/ALTER/auto-sync); Ph5 partial; Ph6 missing; 7.5 demo |

**Archive candidates (10):** client-encryption, cqlengine-feature-parity, cqlengine-missing-features, integration-test-coverage, plan-phase-continuation-action, raw-dc-benchmark-plan, rewrite-coodie-plan, silent-exception-pass, test-refactoring-plan, github-actions-testing-plan (after marking Ph4 obsolete). documentation-plan can join them once llms.txt is refreshed. cqlengine-test-coverage-plan can join once Ph6 is marked won't-do.

**Gotcha for archiving:** `.github/scripts/test_parse_plan.py:427-503` hard-codes `docs/plans/{documentation-plan,udt-support,migration-strategy}.md`, and it asserts `udt-support` has `next_phase == 5`. Moving or editing those files breaks these tests. Nobody notices today because the tests are not run in CI.

---

## 2. Per-plan details

### client-encryption.md — COMPLETE
- Ph1 docs: DONE. `docs/source/guide/encryption.md`, drivers.md:221 (#93).
- Ph2 integration tests: DONE. `tests/integration/test_encryption.py` (scylla and acsylla, `@pytest.mark.ssl`) (#93, #96).
- Ph3 explicit `ssl_context`: DONE. `drivers/__init__.py:57,142` and `tests/test_drivers.py:220` (#96).

### cqlengine-feature-parity.md — COMPLETE
All 13 phases are DONE: #11 types, #12 counters, #13 partial update, #14 LWT, #15/#92 exec options, #86 UDT, #19 batch, #20 model enhancements, #23 polymorphic, #24/#84 pagination, #27 queryset, #28 MVs, #30 keyspace.
Stale text: §1.4 marks `sync_type` ❌ and §1.5 says "UDT entirely missing". The leftover UDT driver registration lives in udt-support Ph6.

### cqlengine-missing-features.md — COMPLETE (duplicate)
- Phase A (UDT): DONE, #86. The remaining A.9 register / auto-sync / ALTER items are tracked in udt-support Ph4/Ph6.
- Phase B (static columns): DONE (#55), even though the plan still says "Implementing Now". Evidence: `Static` in fields.py; `TestStaticColumn` in `tests/integration/test_extended.py:526`.

### cqlengine-test-coverage-plan.md — NEARLY COMPLETE
- Ph1, Ph2, Ph3, Ph5: DONE (#95, #133, #123).
- Ph4: PARTIAL. 4.5 `test_udt_in_list_roundtrip` is missing.
- Ph6: superseded. coodie returns `LWTResult` and uses `if_conditions`/`if_exists` (`tests/integration/test_lwt.py`), and does not raise `LWTException` or offer `iff()`. LWT inside a batch was not done.
- The file is truncated at task 6.2.

### cql-gap-analysis.md — OPEN
- **Ph1 Core DML: PARTIAL** (#184).
  - Done: truncate, distinct, group_by, sum/avg/min/max, `__isnull`, plus `cast()` and `select_token()`.
  - Missing: 1.8 integration tests for all of these (they have unit tests only), and user docs.
- **Ph2 Data types: PARTIAL** (#193, #155).
  - Done: `CqlDuration`/`Duration`, `Vector`/`VectorIndex`/ANN with docs.
  - Missing: duration integration round-trip test and duration docs.
- **Ph3 DDL & keyspace: MOSTLY MISSING.**
  - Missing: 3.1/3.2 `build_alter_keyspace` and `alter_keyspace()`; 3.3 `durable_writes`; 3.4 `tablets`; 3.8 KEYS/VALUES/ENTRIES/FULL collection index targets; 3.9 tests.
  - 3.5 column drop: covered by migrations autogen `ALTER TABLE … DROP`.
  - 3.6/3.7 PARTIAL: `build_create_custom_index` exists but is only wired to `VectorIndex`, and `Indexed` has only `index_name`. Issue #271 (VectorIndex `name`) is related.
- **Ph4 LWT & collections: DONE** (#194). Minor gaps: no docs for `put`/`setindex`, and no unit test for batch timestamp.
- **Ph5 JSON & metadata: PARTIAL** (#197).
  - Done: `build_insert_json`, `save_json`, `build_select_json`, `QuerySet.json()`, `writetime()`/`column_ttl()`.
  - Missing: `create_json`, 5.5 `Json()` marker, 5.7 docs, 5.9 integration tests.
  - 5.6 `to_json()` is redundant with `model_dump_json` → drop it.
- **Ph6 ScyllaDB ext: MOSTLY MISSING.**
  - Done: 6.3 delete collection element; 6.4 `select_token()` (unit test only).
  - Missing: 6.1 `bypass_cache()`; 6.2 UDT alter/drop migration docs; 6.5 ALTER MATERIALIZED VIEW; 6.6–6.8 role helpers, `as_role`, `init_coodie(role=)`; 6.9 tests.
- The §1 gap tables are very stale: about 20 items still marked ❌ are implemented.

### demos-extension-plan.md — OPEN
- **Done:**
  - Ph1 (#62). Leftover `demo/README.md` should be deleted.
  - Ph2 (#79), Ph3 (#81).
  - Ph4 (#129, #176, #131).
  - Ph5 (#132, #147, #149).
  - Ph6 (#155, #150).
  - 7.1 (#180), Ph10 (#183).
- **7.2 polymorphic-cms:** OPEN PR #232. Its `_schema()` fix in sync/aio `document.py` uses `cls.__dict__` instead of `hasattr`, a real library bug fix bundled into a demo PR.
- **Ph8:** 8.1/8.2/8.4 argus-tracker are in OPEN PR #231. 8.3 `demos/migration-guide/` is MISSING.
- **Ph9: MISSING.**
  - `demos/README.md` lists only 6 of 12 demos.
  - Root README has no link to demos.
  - No consistency pass. Only 3 demos have `smoke_test.py`/`test` targets.
- **§11 CI: PARTIAL.** `test-demos.yml` covers only 4 demos, does only `py_compile`, starts no ScyllaDB, runs no smoke tests and has no nightly schedule.
- **§10 monitoring "War Room":** MISSING. Low value; consider dropping it.

### documentation-plan.md — COMPLETE (content stale)
- Ph1–5 are DONE (#38, #43, #45, #47, #50, #56, #58, #77).
- Ph6 llms.txt is DONE (#60), but its links miss schema-management, UDT, vector-search, encryption, benchmarks and api/usertype.
- `guide/schema-management.md:377` still says auto-gen is "planned Phase C".

### github-actions-testing-plan.md — COMPLETE except Ph4
- Ph1 actionlint (pre-commit), Ph2 Bats (#82; scope reduced by #219), Ph3 `tests/test_workflow_conventions.py`: DONE.
- Ph4 smoke tests: OBSOLETE. All its cases target the `/rebase`/`/squash` workflows that #219 removed. CONTRIBUTING.md:196 already documents a manual plan-continuation smoke test.

### integration-test-coverage.md — OBSOLETE
Every gap is closed:
- views (#28), pagination (#84), update LWT, counters (#123), build_update (#146)
- per_partition_limit (#225), custom index_name (#230), acsylla in the CI matrix

It still references the removed `tests/test_integration.py`. Real new gaps (no integration test yet): TRUNCATE/DISTINCT/GROUP BY/aggregates/CAST/`__isnull`/select_token, CqlDuration, JSON/writetime/ttl, batch timestamp. These are covered by the cql-gap-analysis Ph1/2/5 briefs below, so archive this plan.

### migration-strategy.md — NEARLY COMPLETE
- A (#44), B (#68), D (#143): DONE.
- C (#127): DONE for autogen, `makemigration`, `schema-diff`, unsafe-change detection and checksum.
- C.1 table-options introspection/diff: MISSING.
- The Phase C table has no ✅ marks.
- The schema-management guide documents only `coodie migrate`, not `makemigration`/`schema-diff`/`scan_table`.

### performance-improvement.md — OPEN
- DONE: Ph1 (#46), Ph2 (#57), Ph3 (#61), Ph4 (#72), Ph5 (#78), Ph6 dict_factory (#113), Ph7 `__slots__` (#120), Ph8b (#128), Ph9 (#196).
- Ph8: 8.1/8.2/8.3 DONE (#201). 8.4 UDT field-type cache and 8.6 dirty tracking MISSING.
- Ph10 (§15, plan #202): 10.1/10.2/10.4 DONE (#201). **Open:**
  - 10.3 `UserType._get_field_cql_types` cache
  - 10.5 module-level `get_driver` import in `sync/document.py:74,86`
  - 10.6 class-attribute discriminator cache
  - 10.7 `isinstance(list)` fast path in `CassandraDriver._rows_to_dicts`
  - 10.8 dirty-field tracking
  - 10.9 native async for paged queries (`cassandra.py:365` still uses `run_in_executor`)
- Doc gaps: §13C.5 results still say "Pending"; the §13G.6 matrix is stale.

### plan-phase-continuation-action.md — COMPLETE
- All 6 phases DONE (#111, #114, #122, #137, #141, #151, #182).
- Gap: `.github/scripts/test_parse_plan.py` (40 tests) sits outside `testpaths=["tests"]`, and no workflow runs it.

### python-rs-driver-support.md — MOSTLY DONE
- Ph1: PARTIAL. The extra, the uv git source and the CI matrix exist. Missing: 1.1 make target, 1.4 install docs (no mention of python-rs in docs/source), 1.5 OS caveats.
- Ph2: DONE (#97, #246).
- Ph3 namespace conflicts: MISSING. `[tool.uv] conflicts` covers only scylla/cassandra. There is no `tests/test_driver_namespace.py` and no doc.
- Ph4: DONE (#174) except 4.6, the cross-driver pass/fail report.
- Ph5: DONE (#148). §7.4 shows no actual python-rs numbers.

### python-rs-feature-gaps.md — OPEN
- Ph1 per-query consistency/timeout: MISSING. Silently ignored at `python_rs.py:249-265`. Doable now.
- Ph2 sync bridge: DONE (#156). It duplicates sync-api-support Ph3.
- Ph3 pagination, Ph4 close, Ph5 non-row results: BLOCKED on upstream python-rs-driver.
- Ph6 SSL/auth: MISSING. `_build_python_rs_session_builder` only passes kwargs through. Doable now if `SessionBuilder` supports TLS/auth.

### raw-dc-benchmark-plan.md — COMPLETE
Ph1 DONE (#187, with analysis in #190).

### rewrite-coodie-plan.md — HISTORICAL
Phases 0–5 were DONE (#2, #3, #6, #10). Later restructures changed the paths (#42, #48, #62).

### silent-exception-pass.md — COMPLETE
Ph1 DONE (#172). Its §1.1 table still shows ❌. There is a new unaudited `except ImportError: pass` at `drivers/cassandra.py:211`.

### sync-api-support.md — NEARLY COMPLETE
- Ph1 (#145), Ph2 (#157), Ph3 (#97, #156), Ph4 (#174): DONE.
- Ph5 docs: PARTIAL.
  - 5.2: `init_coodie` and `init_coodie_async` have no docstrings.
  - 5.4: `guide/drivers.md` has no sync-bridge or python-rs section. Its note at about line 106 wrongly says sync `init_coodie` can't build an acsylla session from hosts. Its parameter table omits python-rs.

### test-refactoring-plan.md — COMPLETE
Tasks 1–6 DONE (#40, #42, #48, #52, #53). The 5 unchecked boxes are CI verification items, now covered by the test-integration and benchmark matrices.

### udt-support.md — OPEN
- Ph1–3: DONE (#86).
- Ph4: PARTIAL, despite the ✅.
  - Done: `UserType.sync_type()` with dependency ordering.
  - Missing: driver `_get_existing_type_fields`, driver-level `sync_type`, `ALTER TYPE ADD` for new fields (the builder exists but nothing calls it), and auto-sync of UDTs from `Document.sync_table()` (`extract_udt_classes` is never called).
- Ph5: PARTIAL. It works through driver/pydantic paths. There is no integration round-trip for UDTs inside list/set/map, and acsylla round-trips are skipped.
- Ph6 `register_user_type`: MISSING. Low value unless raw cassandra-driver reads need it.
- Ph7: DONE except 7.5 (no demo uses UDT) and stale 7.4.

---

## 3. Stale PR recommendations

| PR | State | Recommendation |
|---|---|---|
| #116 archive plans (draft) | CONFLICTING, untouched since 2026-02-27; includes `pr-comment-rebase-squash-action.md`, which no longer exists | **Close.** Replace it with a fresh archive PR (brief A1) covering the 10 candidates, and update `test_parse_plan.py` in the same PR. |
| #80 UNIMPLEMENTED.md | Mergeable, last refreshed 2026-04-15, already stale (e.g. lists integration-test gaps that #230 closed) | **Close.** It duplicates the plans, and a second source of truth goes stale. Fix the plan checkmarks in the plans themselves instead. |
| #247 "Align PR commit subjects with commitlint" | CONFLICTING since 2026-06-03; failing Lint Commit Messages and python-rs integration checks; title is not conventional; content (deletes issue-manager.yml, edits plan docs) doesn't match the title | **Close.** If removing issue-manager.yml is wanted, open it as its own `chore(ci):` PR. |
| #232 polymorphic-cms demo | Mergeable, green, idle since 2026-04-16 | **Merge after review**, ideally splitting out the `_schema()` `cls.__dict__` fix as `fix(document):` with a unit test (it is a real inheritance bug). Body needs `Plan: docs/plans/demos-extension-plan.md` / `Phase: 7`. |
| #231 argus-tracker demo | Mergeable, green, idle since 2026-04-15 | **Review + merge.** Add `Plan:`/`Phase: 8` lines. Note that it alone does not finish Ph8 (8.3 is still missing). |
| #121 cqlengine migration skill | Mergeable, idle since 2026-04-15 | **Review + merge** (low risk, docs-only). It is not tied to a plan phase. |

Not plan-related: renovate PRs #243/#264/#266/#268/#269/#270 and #272 (ruff fix) are active. Issue #271 (VectorIndex `name`) overlaps cql-gap-analysis 3.6/3.7.

---

## 4. PR briefs (ordered by priority)

### P1

**A1. Archive completed plans (housekeeping; replaces #116)** — size S
- Branch: `docs/archive-completed-plans`
- Title: `docs(plans): archive completed and obsolete plans`
- Body: Moves 10 completed/obsolete plans to `docs/plans/archive/`. Marks github-actions-testing Ph4 obsolete (#219). Points `test_parse_plan.py` fixtures at plans that are still active (or at archive paths). Supersedes #116.
- Scope: `docs/plans/*.md` → `docs/plans/archive/`, `.github/scripts/test_parse_plan.py`. Check that `plan-continuation.yml` ignores `archive/`.
- No Plan/Phase lines (cross-plan).

**B1. Run parse-plan tests in CI** — S
- Branch: `plan/plan-phase-continuation-action/phase-1`
- Title: `ci(plan-continuation): run parse-plan unit tests in CI`
- Body: The 40 parser tests in `.github/scripts/test_parse_plan.py` live outside `testpaths` and never run. Add the path to `test-unit.yml` (or to testpaths) so plan edits can't silently break the continuation workflow.
  `Plan: docs/plans/plan-phase-continuation-action.md`
  `Phase: 1`
- Scope: `.github/workflows/test-unit.yml` or `pyproject.toml` `[tool.pytest.ini_options]`.

**C1. Sync-bridge + python-rs driver docs** — S
- Branch: `plan/sync-api-support/phase-5`
- Title: `docs(drivers): document sync bridge and python-rs driver`
- Body: Add docstrings to `init_coodie`/`init_coodie_async`. Add a "Sync bridge" section and a python-rs section to `guide/drivers.md`, including install via the `python-rs` extra. Remove the stale note that sync `init_coodie` can't create acsylla sessions. Add python-rs to the parameter table. Also covers python-rs-driver-support 1.4/1.5.
  `Plan: docs/plans/sync-api-support.md`
  `Phase: 5`
- Scope: `src/coodie/drivers/__init__.py`, `docs/source/guide/drivers.md`, `docs/source/installation.md`.

**D1. CQL gap Phase 1 — integration tests + docs** — M
- Branch: `plan/cql-gap-analysis/phase-1`
- Title: `test(integration): cover truncate, distinct, group_by, aggregates, isnull and cast`
- Body: These Phase 1 features have only unit tests. Add `tests/integration/test_dml_extras.py` covering all drivers. Document them in `guide/querying.md`.
  `Plan: docs/plans/cql-gap-analysis.md`
  `Phase: 1`
- Scope: `tests/integration/`, `docs/source/guide/querying.md`, `docs/source/guide/crud.md`.

**E1. UDT schema evolution + auto-sync** — M
- Branch: `plan/udt-support/phase-4`
- Title: `feat(usertype): alter existing UDTs and auto-sync them from sync_table`
- Body: `sync_type()` only issues `CREATE TYPE IF NOT EXISTS`. Read the existing type fields from system_schema, issue `ALTER TYPE ADD` for new fields, and call `extract_udt_classes()` from `Document.sync_table()` so referenced UDTs are created first. Update the `test_parse_plan.py` expectation (next_phase).
  `Plan: docs/plans/udt-support.md`
  `Phase: 4`
- Scope: `src/coodie/usertype.py`, `src/coodie/{sync,aio}/document.py`, `src/coodie/drivers/{base,cassandra,acsylla,python_rs}.py`, `tests/test_usertype.py`, `tests/integration/test_udt.py`, `.github/scripts/test_parse_plan.py`.

**F1. Demos index & polish** — S
- Branch: `plan/demos-extension-plan/phase-9`
- Title: `docs(demos): list all demos in index and link from root README`
- Body: `demos/README.md` lists 6 of 12 demos. Add the missing 6 (plus #231/#232 if merged first), link demos from the root README, and delete the leftover `demo/README.md`. Standardize the Makefile targets.
  `Plan: docs/plans/demos-extension-plan.md`
  `Phase: 9`
- Scope: `demos/README.md`, `README.md`, `demo/README.md` (delete), `demos/*/Makefile`.

**G1. python-rs per-query consistency/timeout** — S/M
- Branch: `plan/python-rs-feature-gaps/phase-1`
- Title: `fix(drivers): honor per-query consistency and timeout in PythonRsDriver`
- Body: `consistency` and `timeout` are accepted and silently dropped in `_execute_async_impl`. Map coodie consistency names to python-rs enums via `with_consistency`/`with_request_timeout`. Add mocked unit tests. Un-skip consistency-dependent integration tests.
  `Plan: docs/plans/python-rs-feature-gaps.md`
  `Phase: 1`
- Scope: `src/coodie/drivers/python_rs.py`, `tests/test_python_rs_driver.py`, `tests/integration/`.
- First check that the upstream API exists in the pinned scylla git revision.

### P2

**H2. Performance Phase 10 quick wins** — S
- Branch: `plan/performance-improvement/phase-10`
- Title: `perf: cache UDT field types, hoist get_driver import, fast-path list rows`
- Body: Implement 10.3 (`lru_cache` on `UserType._get_field_cql_types`), 10.5 (module-level `get_driver` in sync/aio document), 10.6 (class-attribute discriminator cache) and 10.7 (an `isinstance(list)` early return in `CassandraDriver._rows_to_dicts`). Defer 10.8 dirty tracking and 10.9 paged native async to separate PRs.
  `Plan: docs/plans/performance-improvement.md`
  `Phase: 10`
- Scope: `src/coodie/usertype.py`, `src/coodie/{sync,aio}/document.py`, `src/coodie/drivers/cassandra.py`, `docs/plans/performance-improvement.md`.

**I2. CQL gap Phase 5 — JSON/metadata completion** — M
- Branch: `plan/cql-gap-analysis/phase-5`
- Title: `feat(query): add create_json and integration tests for JSON, writetime and ttl`
- Body: Add `QuerySet.create_json`. Add integration tests for `save_json`/`json()`/`writetime()`/`column_ttl()`. Document JSON coercion. Drop 5.6 `to_json()` from the plan (`model_dump_json` covers it). Decide whether to keep 5.5 `Json()`.
  `Plan: docs/plans/cql-gap-analysis.md`
  `Phase: 5`
- Scope: `src/coodie/{sync,aio}/query.py`, `tests/integration/`, `docs/source/guide/`.

**J2. CQL gap Phase 3 — keyspace DDL + index targets** — M
- Branch: `plan/cql-gap-analysis/phase-3`
- Title: `feat(keyspace): add alter_keyspace with durable_writes and tablets options`
- Body: Add `build_alter_keyspace` + `alter_keyspace()`, `durable_writes` and `tablets` options on create/alter, and KEYS/VALUES/ENTRIES/FULL index targets on `Indexed`. Optionally fold in issue #271 (custom index `name` on VectorIndex) here or in a separate PR.
  `Plan: docs/plans/cql-gap-analysis.md`
  `Phase: 3`
- Scope: `src/coodie/cql_builder.py`, `src/coodie/fields.py`, `src/coodie/drivers/*`, `tests/test_cql_builder.py`, `tests/integration/`.

**K2. Demos CI smoke tests** — M
- Branch: `plan/demos-extension-plan/phase-9` (or `/phase-11` if §11 is treated as a phase)
- Title: `ci(demos): run smoke tests against ScyllaDB for all demos`
- Body: `test-demos.yml` only compiles 4 demos. Start a ScyllaDB service, add `smoke_test.py` + `make test` to fastapi-catalog and flask-blog, extend the matrix to all demos, and add a nightly schedule.
  `Plan: docs/plans/demos-extension-plan.md`
  `Phase: 9`
- Scope: `.github/workflows/test-demos.yml`, `demos/*/smoke_test.py`, `demos/*/Makefile`.

**L2. Docs refresh: llms.txt + migrations CLI** — S
- Branch: `plan/documentation-plan/phase-6`
- Title: `docs: refresh llms.txt and document makemigration and schema-diff`
- Body: llms.txt/llms-full.txt miss schema-management, UDT, vector-search, encryption and benchmarks. `schema-management.md` still says autogen is "planned Phase C" and doesn't document `makemigration`/`schema-diff`/`scan_table`. This unblocks archiving documentation-plan and migration-strategy.
  `Plan: docs/plans/documentation-plan.md`
  `Phase: 6`
- Scope: `docs/source/llms*.txt`, `docs/source/guide/schema-management.md`.

**M2. python-rs SSL/TLS & auth** — M
- Branch: `plan/python-rs-feature-gaps/phase-6`
- Title: `feat(drivers): support ssl_context and credentials for PythonRsDriver`
- Body: Wire `ssl_context`/username/password from `init_coodie` into the python-rs `SessionBuilder`. Add a python-rs case to `tests/integration/test_encryption.py`.
  `Plan: docs/plans/python-rs-feature-gaps.md`
  `Phase: 6`
- Scope: `src/coodie/drivers/__init__.py`, `src/coodie/drivers/python_rs.py`, `tests/integration/test_encryption.py`.

**N2. CQL gap Phase 2 — duration round-trip** — S
- Branch: `plan/cql-gap-analysis/phase-2`
- Title: `test(integration): add CqlDuration round-trip and duration docs`
- Body: Duration has only unit tests. Add a round-trip on all drivers and a section in `guide/field-types.md`.
  `Plan: docs/plans/cql-gap-analysis.md`
  `Phase: 2`
- Scope: `tests/integration/test_extended.py`, `docs/source/guide/field-types.md`.

**O2. Migration-guide demo** — M
- Branch: `plan/demos-extension-plan/phase-8`
- Title: `feat(demos): add cqlengine-to-coodie migration-guide demo`
- Body: Add side-by-side `cqlengine_models.py`/`coodie_models.py`, `migrate.py` and `verify.py`, showing both libraries reading the same tables. Phase 8 completes once #231 merges.
  `Plan: docs/plans/demos-extension-plan.md`
  `Phase: 8`
- Scope: `demos/migration-guide/`, `demos/README.md`.

### P3

**P3a. UDT collection round-trips** — S
- Branch: `plan/udt-support/phase-5`
- Title: `test(udt): round-trip UDTs inside list, set and map`
- Body: Covers udt-support 5.6 and cqlengine-test-coverage 4.5. Un-skip acsylla if supported.
  `Plan: docs/plans/udt-support.md`
  `Phase: 5`
- Scope: `tests/integration/test_udt.py`.

**P3b. Table-options diff in autogen** — M
- Branch: `plan/migration-strategy/phase-C`
- Title: `feat(migrations): detect table option changes in makemigration`
- Body: Introspect `system_schema.tables` options (compaction, default_ttl, gc_grace…), diff them against `__options__`/`__default_ttl__`, and render `ALTER TABLE … WITH`.
  `Plan: docs/plans/migration-strategy.md`
  `Phase: C`
- Scope: `src/coodie/migrations/autogen.py`, `tests/test_migrations_autogen.py`.

**P3c. CQL gap Phase 6 — bypass_cache + ALTER MV** — M
- Branch: `plan/cql-gap-analysis/phase-6`
- Title: `feat(query): add bypass_cache and alter materialized view support`
- Body: Add ScyllaDB `BYPASS CACHE` on QuerySet and `build_alter_materialized_view`. Split the role helpers (6.6–6.8) into a separate PR or mark them won't-do (they are admin tooling, not ODM).
  `Plan: docs/plans/cql-gap-analysis.md`
  `Phase: 6`
- Scope: `src/coodie/cql_builder.py`, `src/coodie/{sync,aio}/query.py`, `src/coodie/views.py`, tests.

**P3d. Paged native async + dirty-field tracking** — L, two separate PRs
- Branch: `plan/performance-improvement/phase-10` (follow-up)
- Title: `perf(drivers): use native async for paged queries in CassandraDriver`
- Body: Covers 10.9: `cassandra.py:365` falls back to `run_in_executor` when `fetch_size` is set. Dirty tracking (10.8) needs a design note first.
  `Plan: docs/plans/performance-improvement.md`
  `Phase: 10`

**P3e. python-rs namespace check** — S
- Branch: `plan/python-rs-driver-support/phase-3`
- Title: `test(drivers): verify scylla and python-rs drivers coexist in one venv`
- Body: Add `tests/test_driver_namespace.py`, which imports both drivers and asserts no `scylla` module shadowing. Document the supported extra combinations and extend `[tool.uv] conflicts` if needed.
  `Plan: docs/plans/python-rs-driver-support.md`
  `Phase: 3`
- Scope: `tests/test_driver_namespace.py`, `pyproject.toml`, `docs/source/installation.md`.

**Won't do / drop from the plans:**
- udt-support Ph6 `register_user_type` (reads already work via `_coerce_namedtuple`; revisit only on user demand).
- cqlengine-test-coverage Ph6 `LWTException`/`iff()` (superseded by `LWTResult`).
- demos §10 monitoring War Room.
- python-rs-feature-gaps Ph3–5 until upstream ships the APIs.
