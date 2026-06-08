# Unimplemented Features — Ready Prompts

> **Auto-generated summary** of features planned in `/docs/plans/` that are
> **not yet implemented**. Each item is a self-contained prompt you can give
> to an AI coding agent (or a developer) to implement the feature.
>
> **Last reviewed:** 2026-04-15 (post-merge: vector-search demo, schema-migrations
> demo, CQL Phase 4, CQL Phase 5, and performance Phase 9 are now merged to
> `master`. No currently-open implementation PRs were found for the remaining
> prompts below.)

---

## Table of Contents

1. [Migration Framework](#1-migration-framework)
2. [python-rs Feature Gaps](#2-python-rs-feature-gaps)
3. [Demo Suite Extension](#3-demo-suite-extension)
4. [cqlengine Test Coverage Gaps](#4-cqlengine-test-coverage-gaps)
5. [Integration Test Coverage Gaps](#5-integration-test-coverage-gaps)
6. [Sync API Support](#6-sync-api-support)
7. [CQL Gap Analysis](#7-cql-gap-analysis)
8. [Silent Exception Pass](#8-silent-exception-pass)
9. [Performance Improvement Plan](#9-performance-improvement-plan)

---

## 1. Migration Framework

*Source: `migration-strategy.md`*

> *Phase A (enhanced `sync_table`) is ✅ Done. Phase B (migration framework core) is ✅ Done. Phase C (auto-generation) is ✅ Done. Phase D (data migrations) is ✅ Done — `ctx.scan_table()` with token-range iteration, progress logging, `resume_token`, `throttle_seconds`, 15 tests. All migration phases complete.*

*No remaining items — entire migration framework is implemented.*

---

## 2. python-rs Feature Gaps

*Source: `python-rs-feature-gaps.md`*

> *Continuation plan for PythonRsDriver feature gaps blocked by upstream python-rs-driver limitations. Each phase is gated on an upstream improvement. Phase 2 (background-thread sync bridge) is ✅ Done — PythonRsDriver uses `_bg_loop`, `_bg_thread`, `_bridge_to_bg_loop`, `connect()` classmethod, `run_coroutine_threadsafe()` (implemented via sync-api-support Phase 3). 5 phases remain.*

### 2.1 Per-Query Consistency & Timeout

> **Prompt:** Implement per-query consistency level and timeout support in `PythonRsDriver`. Currently these parameters are silently ignored in `execute_async()`. Wire `consistency` through `Statement.with_consistency()` and `timeout` through `Statement.with_request_timeout()`. Add unit tests with mocked session and update integration tests to un-skip consistency-dependent tests. See `docs/plans/python-rs-feature-gaps.md` Phase 1.

### 2.2 Pagination Support

> **Prompt:** Implement pagination in `PythonRsDriver` once upstream python-rs-driver adds `execute_paged()`. Wire `fetch_size` through `PreparedStatement.with_page_size()`, extract `paging_state` from `RequestResult`, and return it for `paged_all()` continuation. Un-skip 3 pagination integration tests. See `docs/plans/python-rs-feature-gaps.md` Phase 3.

### 2.3 Session Close / Shutdown

> **Prompt:** Implement proper `close_async()` and `close()` in `PythonRsDriver` once upstream python-rs-driver adds `Session.close()`. Currently these are no-ops. See `docs/plans/python-rs-feature-gaps.md` Phase 4.

### 2.4 Non-Row Result Handling

> **Prompt:** Improve non-row result handling in `PythonRsDriver._rows_to_dicts()`. Currently catches `RuntimeError("does not have rows")` — improve once upstream adds `has_rows()` or `ResultType` enum. See `docs/plans/python-rs-feature-gaps.md` Phase 5.

### 2.5 SSL/TLS & Authentication

> **Prompt:** Add SSL/TLS and authentication support to `PythonRsDriver` once upstream python-rs-driver adds `SessionBuilder` TLS and auth configuration. Wire `ssl_context`, `ssl_enabled`, and auth parameters from `init_coodie()` / `init_coodie_async()`. See `docs/plans/python-rs-feature-gaps.md` Phase 6.

---

## 3. Demo Suite Extension

*Source: `demos-extension-plan.md`*

> *12 demos now exist: `demos/fastapi-catalog/`, `demos/flask-blog/`, `demos/django-taskboard/`, `demos/lwt-user-registry/`, `demos/ttl-sessions/`, `demos/batch-importer/`, `demos/materialized-views/`, `demos/collections-tags/`, `demos/realtime-counters/`, `demos/timeseries-iot/`, `demos/schema-migrations/`, and `demos/vector-search/`. Demo CI workflow `test-demos.yml` is ✅ Done. The plan calls for additional demos beyond these shipped examples.*

### 3.1 Polymorphic CMS Demo

> **Prompt:** Create `demos/polymorphic-cms/` — a content management system demo showcasing coodie's single-table inheritance with `Discriminator` column. Define `Article`, `Video`, and `Podcast` subtypes sharing a single table. Add `seed.py`, colorful UI, `Makefile`, and `README.md`. See `docs/plans/demos-extension-plan.md` Phase 7 (task 7.2).

### 3.2 Argus-Style Test Tracker Demo

> **Prompt:** Create `demos/argus-tracker/` — a scaled-down test tracker inspired by scylladb/argus. Define complex models: User, TestRun (composite PK + clustering), Event (compound partition), Notification (TimeUUID). Include batch event ingestion, prepared-statement caching patterns, and partition-scoped queries. Add `seed.py`, `Makefile`, and `README.md`. See `docs/plans/demos-extension-plan.md` Phase 8 (task 8.1).

### 3.3 cqlengine → coodie Migration Guide Demo

> **Prompt:** Create `demos/migration-guide/` — a side-by-side migration walkthrough from cqlengine to coodie. Include `cqlengine_models.py` and `coodie_models.py` with equivalent models, a `migrate.py` script that syncs tables, and a `verify.py` that checks data round-trip. Reference argus model patterns. Add `README.md` with step-by-step walkthrough. See `docs/plans/demos-extension-plan.md` Phase 8 (task 8.3).

---

## 4. cqlengine Test Coverage Gaps

*Source: `cqlengine-test-coverage-plan.md`*

> *Phase 1 (unit test completeness) is ✅ Done. `map__update` collection operator is ✅ Done. Counter integration tests are ✅ Done. Phase 2 (container mutations) is ✅ Done. Phase 3 (query operators) is ✅ Done. Phase 4 (UDT) is ✅ Done. Phase 5 (polymorphism + schema) is ✅ Done. §1.5 LWT conditionals is ✅ Done. §1.6 TTL/timestamp coverage is ✅ Done (`tests/integration/test_ttl_timestamp.py`). §1.9 batch write coverage is ✅ Done (`tests/integration/test_batch_integration.py`). §1.10 advanced query coverage is ✅ Done (`tests/integration/test_advanced_query.py`).*

*No remaining items — this coverage plan is fully implemented.*

---

## 5. Integration Test Coverage Gaps

*Source: `integration-test-coverage.md`*

> *These are features that exist in the codebase but lack integration test coverage. Pagination tests are ✅ Done. Partial UPDATE tests are ✅ Done (`tests/integration/test_update.py` — 257 lines: partial field update, TTL, IF conditions, IF EXISTS, collection mutations).*

### 5.1 Custom Index Name Integration Tests

> **Prompt:** Add integration tests verifying that `Indexed(index_name="my_custom_idx")` creates a named secondary index and that the index is queryable. See `docs/plans/integration-test-coverage.md` §"Secondary index with custom index_name".

### 5.2 AcsyllaDriver Integration Tests

> **Prompt:** Add CI workflow support and integration tests for the `AcsyllaDriver` (async native driver at `src/coodie/drivers/acsylla.py`). Currently all async integration tests run through the `CassandraDriver` asyncio bridge. Add a separate CI workflow or matrix entry targeting the `acsylla` driver. See `docs/plans/integration-test-coverage.md` §"AcsyllaDriver".

---

## 6. Sync API Support

*Source: `sync-api-support.md`*

> *Phase 1 is ✅ Done — `init_coodie_async(driver_type="acsylla", hosts=...)` routes through `AcsyllaDriver.connect()` with `_bridge_to_bg_loop = True`. Phase 2 is ✅ Done — `AcsyllaDriver.connect_sync()` + `init_coodie(driver_type="acsylla", hosts=...)` auto-create sync session + `UserWarning`. Phase 3 is ✅ Done — `PythonRsDriver` uses bg-thread sync bridge with `_bg_loop`, `_bg_thread`, `_bridge_to_bg_loop`, `connect()` classmethod, `run_coroutine_threadsafe()`. Phase 4 is ✅ Done — python-rs integration fixtures, CI matrix, variant fixture (tasks 4.1–4.5 all ✅). Phase 5 remains.*

### 6.1 Sync API Documentation

> **Prompt:** Document the sync bridge pattern, supported init paths, and caveats for AcsyllaDriver and PythonRsDriver. Update class docstrings and `init_coodie()`/`init_coodie_async()` docstrings. See `docs/plans/sync-api-support.md` Phase 5 (tasks 5.1–5.3).

---

## 7. CQL Gap Analysis

*Source: `cql-gap-analysis.md`*

> *New plan comparing coodie against the ScyllaDB CQL Reference. Identifies 41 missing CQL features across data types, DDL, DML, LWT, and ScyllaDB extensions. Phase 1 (core DML gaps) is ✅ Done. Phase 2 (data types: `duration` + `vector`) is ✅ Done. Phase 4 (LWT & collection operations) is ✅ Done. Phase 5 (JSON & metadata features) is ✅ Done. 2 phases remain.*

### 7.1 DDL & Keyspace Gaps (Phase 3)

> **Prompt:** Implement DDL gaps: (1) `ALTER TABLE DROP column`, `ALTER TABLE RENAME`. (2) Custom SAI index class support. (3) Index options (`WITH OPTIONS`). (4) Collection element indexes (`KEYS`, `VALUES`, `ENTRIES`, `FULL`). (5) `ALTER MATERIALIZED VIEW`. (6) `ALTER TYPE RENAME field`. (7) `ALTER KEYSPACE` with `durable_writes` and `tablets` options. Add unit + integration tests. See `docs/plans/cql-gap-analysis.md` Phase 3.

### 7.2 ScyllaDB Extensions & Low-Priority Gaps (Phase 6)

> **Prompt:** Implement ScyllaDB-specific extensions and low-priority gaps: (1) `BYPASS CACHE` hint. (2) `USING TIMEOUT` in CQL statements. (3) Tablets-enabled keyspace creation. (4) Role/user management DDL (`CREATE ROLE`, `GRANT`, `REVOKE`, etc.) — evaluate if appropriate for an ORM. Add unit + integration tests. See `docs/plans/cql-gap-analysis.md` Phase 6.

---

## 8. Silent Exception Pass

*Source: `silent-exception-pass.md`*

> *Audit of `except … pass` and overly broad exception handlers. Phase 1 is ✅ Done — narrowed `_cached_type_hints` to `(NameError, AttributeError, TypeError)` and added `logging.warning()` for CassandraDriver `dict_factory` import failure. All identified problematic cases are fixed.*

*No remaining items — the single implementation phase is complete.*

---

## 9. Performance Improvement Plan

*Source: `performance-improvement.md`*

> *Phases 1–9 are ✅ Done. Phase 10 contains remaining quick wins.*

### 9.1 Remaining Quick Wins (Phase 10)

> **Prompt:** Implement Phase 10 tasks from `docs/plans/performance-improvement.md` §15, prioritizing the P0 quick wins first (`_snake_case` caching, CQL cache expansion for count/update/delete, UDT field-type caching, and timestamp-building micro-optimizations), then measure impact with the benchmark suite and update the plan status/results.
