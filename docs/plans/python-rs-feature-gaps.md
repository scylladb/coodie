# python-rs-driver Feature Gaps — Continuation Plan

> **Goal:** Track the coodie features that `PythonRsDriver` does not yet support
> due to upstream limitations in
> [python-rs-driver](https://github.com/scylladb-zpp-2025-python-rs-driver/python-rs-driver).
> Each phase is gated on an upstream improvement and can be picked up
> independently once the underlying driver adds the required API.
> This plan serves as a living checklist — re-evaluate after every
> python-rs-driver release.

---

## Table of Contents

1. [Current Limitation Summary](#1-current-limitation-summary)
2. [Feature Gap Analysis](#2-feature-gap-analysis)
   - [2.1 Synchronous API](#21-synchronous-api)
   - [2.2 Pagination](#22-pagination)
   - [2.3 Per-Query Consistency Level](#23-per-query-consistency-level)
   - [2.4 Per-Query Timeout](#24-per-query-timeout)
   - [2.5 Session Close / Shutdown](#25-session-close--shutdown)
   - [2.6 Non-Row Result Handling](#26-non-row-result-handling)
   - [2.7 SSL/TLS & Authentication](#27-ssltls--authentication)
3. [Implementation Phases](#3-implementation-phases)
4. [Test Plan](#4-test-plan)
   - [4.1 Tests to Unskip](#41-tests-to-unskip)
   - [4.2 New Tests per Phase](#42-new-tests-per-phase)
5. [References](#5-references)

---

## 1. Current Limitation Summary

The table below summarizes every coodie feature that is skipped, silently
ignored, or worked around when using `driver_type="python-rs"`.

| # | Feature | Impact | Upstream Blocker | Skipped Tests |
|---|---------|--------|------------------|---------------|
| 1 | Synchronous API | All sync variant tests skipped | async-only; `loop.run_until_complete()` fails inside running loop | `variant == "sync"` (68 tests) |
| 2 | Pagination (`fetch_size` / `paging_state`) | `fetch_size` and `paging_state` silently ignored; all rows returned in one response | `Session.execute()` calls `execute_unpaged` internally | `test_fetch_size_limits_page`, `test_full_table_scan_spanning_multiple_pages`, `test_fetch_size_limits_rows_per_page` |
| 3 | ~~Per-query consistency level~~ | ✅ Fixed in Phase 1 — mapped to `scylla.Consistency` and assigned to a copy's `consistency` attribute | — | — |
| 4 | ~~Per-query timeout~~ | ✅ Fixed in Phase 1 — assigned to a copy's `request_timeout` attribute (seconds) | — | — |
| 5 | Session close | `close_async()` is a no-op | `Session` has no `close()` method | — (no dedicated test) |
| 6 | Non-row result handling | `_rows_to_dicts()` catches `RuntimeError` for INSERT/UPDATE/DELETE | `iter_rows()` raises `RuntimeError: Result does not have rows` | — (workaround in driver) |
| 7 | SSL/TLS | Not supported | Not exposed to Python | — (not tested) |
| 8 | Authentication | Not supported | Not exposed to Python | — (not tested) |

---

## 2. Feature Gap Analysis

Legend:
- ✅ **Implemented** — working today in python-rs-driver
- 🔧 **Partial** — infrastructure exists but limited or not wired through in coodie
- ❌ **Missing** — not yet available upstream

### 2.1 Synchronous API

| coodie Need | python-rs-driver Equivalent | Status |
|---|---|---|
| `execute()` sync method | — | 🔧 `loop.run_until_complete()` bridge; fails inside running loop |
| `sync_table()` sync method | — | 🔧 same bridge limitation |
| `close()` sync method | — | 🔧 same bridge limitation |
| Background-thread sync bridge (like AcsyllaDriver) | — | ❌ not implemented |

**Gap summary — synchronous API:**
- Current bridge uses `loop.run_until_complete()` which raises `RuntimeError: This event loop is already running` inside pytest-asyncio, ASGI middleware, or any running loop
- Fix → implement a background-thread bridge (same pattern as `AcsyllaDriver.connect()` which creates a dedicated background loop in a daemon thread and dispatches via `run_coroutine_threadsafe`)
- Upstream dependency → none; this is a coodie-side improvement

### 2.2 Pagination

| coodie Need | python-rs-driver Equivalent | Status |
|---|---|---|
| `fetch_size` limits rows per page | `PreparedStatement.with_page_size(n)` | 🔧 exists in stubs but no effect — `execute` always uses unpaged |
| `paging_state` resume token | — | ❌ no `paging_state` on `RequestResult` |
| `PagedResult` with `has_more_pages` | — | ❌ |

**Gap summary — pagination:**
- `Session.execute()` internally calls `execute_unpaged`/`query_unpaged` in Rust
- Fix → upstream must expose `execute_paged` or `execute_iter` with a page-state token
- Coodie changes → wire `fetch_size` to `PreparedStatement.with_page_size()`, extract `paging_state` from result, set `self._last_paging_state`

### 2.3 Per-Query Consistency Level

| coodie Need | python-rs-driver Equivalent | Status |
|---|---|---|
| `consistency` parameter on `execute_async()` | `Statement.with_consistency(Consistency.*)` / `ExecutionProfile` | ✅ API exists upstream |

**Gap summary — consistency:**
- The upstream API (`Statement.with_consistency()`, `ExecutionProfile`) supports per-query consistency
- Fix → in `PythonRsDriver.execute_async()`, map the coodie `consistency` string to `scylla.enums.Consistency` and call `prepared.with_consistency(c)` before execute
- Upstream dependency → none; this is a coodie-side wiring fix

### 2.4 Per-Query Timeout

| coodie Need | python-rs-driver Equivalent | Status |
|---|---|---|
| `timeout` parameter on `execute_async()` | `Statement.with_request_timeout(seconds: float)` / `ExecutionProfile` | ✅ API exists upstream |

**Gap summary — timeout:**
- The upstream API (`Statement.with_request_timeout()`) supports per-query timeout
- Fix → in `PythonRsDriver.execute_async()`, call `prepared.with_request_timeout(timeout)` before execute (upstream takes seconds as `float`, not milliseconds)
- Upstream dependency → none; this is a coodie-side wiring fix

### 2.5 Session Close / Shutdown

| coodie Need | python-rs-driver Equivalent | Status |
|---|---|---|
| `close_async()` releases resources | — | ❌ no `close()` on `Session` |
| `close()` sync wrapper | — | ❌ |

**Gap summary — session close:**
- The Rust session drops resources when garbage-collected (Python `__del__`)
- Fix → upstream must expose an explicit `close()` or `shutdown()` method on `Session`
- Workaround → current no-op is acceptable; document that resources are released on GC

### 2.6 Non-Row Result Handling

| coodie Need | python-rs-driver Equivalent | Status |
|---|---|---|
| `execute()` returns `[]` for INSERT/UPDATE/DELETE | `iter_rows()` raises `RuntimeError` | 🔧 caught with try/except in `_rows_to_dicts` |

**Gap summary — non-row results:**
- `RequestResult.iter_rows()` raises `RuntimeError: Result does not have rows` for non-SELECT
- Fix → upstream should return an empty iterator (or expose `has_rows()` / `is_rows_result()`)
- Workaround → current try/except is targeted and safe; no action until upstream improves

### 2.7 SSL/TLS & Authentication

| coodie Need | python-rs-driver Equivalent | Status |
|---|---|---|
| `ssl_context` / `ssl_enabled` on connect | — | ❌ not exposed to Python |
| Username/password authentication | — | ❌ not exposed to Python |
| Mutual TLS (client cert) | — | ❌ not exposed to Python |

**Gap summary — SSL/TLS & authentication:**
- The underlying Rust driver (scylla-rust-driver) supports SSL and auth natively
- Fix → upstream must expose `SessionBuilder` options for TLS config and credentials
- Coodie changes → add `ssl_context` / auth kwargs to `init_coodie_async(driver_type="python-rs", ...)`

---

## 3. Implementation Phases

### Phase 1: Per-Query Consistency & Timeout (Priority: High) ✅ Done

**Goal:** Wire the `consistency` and `timeout` parameters through to the Rust driver — no upstream changes needed.

| Task | Description |
|---|---|
| 1.1 | Map coodie consistency strings (`"ONE"`, `"QUORUM"`, etc.) to `scylla.enums.Consistency` enum values in `PythonRsDriver` |
| 1.2 | In `execute_async()`, call `prepared.with_consistency(c)` when `consistency` is not `None` |
| 1.3 | In `execute_async()`, call `prepared.with_request_timeout(timeout)` when `timeout` is not `None` (upstream takes seconds) |
| 1.4 | Add unit tests verifying consistency and timeout are forwarded to the prepared statement |
| 1.5 | Integration test: a read at `EACH_QUORUM` is rejected by the server, proving the consistency is forwarded (`test_per_query_consistency_reaches_server`) |

### Phase 2: Background-Thread Sync Bridge (Priority: High)

**Goal:** Replace the `loop.run_until_complete()` sync bridge with a background-thread bridge so sync methods work inside running event loops.

| Task | Description |
|---|---|
| 2.1 | Add `_bg_loop` and `_bg_thread` attributes to `PythonRsDriver` (same pattern as `AcsyllaDriver`) |
| 2.2 | Add `connect()` classmethod that creates the session on the background loop |
| 2.3 | Rewrite `execute()`, `sync_table()`, and `close()` to use `run_coroutine_threadsafe` against `_bg_loop` |
| 2.4 | Add `_run_on_bg_loop()` helper for dispatching coroutines (same as AcsyllaDriver) |
| 2.5 | Unskip sync variant integration tests for `python-rs` |
| 2.6 | Unit tests verifying the sync bridge works from both async and non-async contexts |

### Phase 3: Pagination Support (Priority: Medium)

**Goal:** Enable `fetch_size` and `paging_state` when the upstream driver adds paged execution.

| Task | Description |
|---|---|
| 3.1 | **Prerequisite:** verify upstream exposes `execute_paged` or equivalent with page-state token |
| 3.2 | In `execute_async()`, call `prepared.with_page_size(fetch_size)` when `fetch_size` is not `None` |
| 3.3 | Extract `paging_state` from the result object and store in `self._last_paging_state` |
| 3.4 | Pass `paging_state` to the execute call when provided (set page state on statement or result) |
| 3.5 | Unskip `test_fetch_size_limits_page`, `test_full_table_scan_spanning_multiple_pages`, `test_fetch_size_limits_rows_per_page` |
| 3.6 | Add unit tests for pagination state handling with mocked session |

### Phase 4: Session Close (Priority: Low)

**Goal:** Implement explicit session shutdown when the upstream driver exposes a `close()` API.

| Task | Description |
|---|---|
| 4.1 | **Prerequisite:** verify upstream exposes `Session.close()` or `Session.shutdown()` |
| 4.2 | Implement `close_async()` to call the upstream close method |
| 4.3 | Implement `close()` to dispatch via the sync bridge |
| 4.4 | Unit test verifying close is called on the underlying session |

### Phase 5: Non-Row Result Handling (Priority: Low)

**Goal:** Remove the `RuntimeError` workaround when upstream provides clean non-row result handling.

| Task | Description |
|---|---|
| 5.1 | **Prerequisite:** verify upstream returns empty iterator or exposes `has_rows()` for non-SELECT results |
| 5.2 | Update `_rows_to_dicts()` to use the clean API instead of try/except |
| 5.3 | Unit test verifying INSERT/UPDATE/DELETE results return `[]` without exception |

### Phase 6: SSL/TLS & Authentication (Priority: Medium)

**Goal:** Enable encrypted and authenticated connections when the upstream driver exposes the Rust driver's TLS and auth config.

| Task | Description |
|---|---|
| 6.1 | **Prerequisite:** verify upstream exposes TLS config on `SessionBuilder` |
| 6.2 | **Prerequisite:** verify upstream exposes auth credentials on `SessionBuilder` |
| 6.3 | Add `ssl_context` / `ssl_enabled` kwargs to `init_coodie_async(driver_type="python-rs", ...)` |
| 6.4 | Add auth kwargs (`username`, `password`) to `init_coodie_async(driver_type="python-rs", ...)` |
| 6.5 | Integration tests for SSL and auth connections (reuse patterns from `test_encryption.py`) |

---

## 4. Test Plan

### 4.1 Tests to Unskip

These tests are currently skipped for `driver_type="python-rs"` and should be
unskipped when the corresponding phase is complete.

| Test | File | Phase |
|---|---|---|
| All sync variant tests (68 tests) | `tests/integration/conftest.py` variant fixture | 2 |
| `test_fetch_size_limits_page[async]` | `tests/integration/test_basic.py:257` | 3 |
| `test_full_table_scan_spanning_multiple_pages[async]` | `tests/integration/test_pagination.py:58` | 3 |
| `test_fetch_size_limits_rows_per_page[async]` | `tests/integration/test_pagination.py:91` | 3 |

### 4.2 New Tests per Phase

#### `tests/test_python_rs_driver.py` (unit)

| Test Case | Phase |
|---|---|
| `execute_async()` maps consistency string to `Consistency` enum | 1 |
| `execute_async()` calls `with_request_timeout(ms)` on prepared statement | 1 |
| Sync bridge `execute()` works from non-async context | 2 |
| Sync bridge `execute()` works from inside running event loop | 2 |
| `execute_async()` sets page size on prepared statement | 3 |
| `execute_async()` extracts and stores paging state | 3 |
| `close_async()` calls upstream `Session.close()` | 4 |
| `_rows_to_dicts()` uses clean API for non-row results | 5 |

#### `tests/integration/test_encryption.py` (integration)

| Test Case | Phase |
|---|---|
| `PythonRsDriver` async execute succeeds over SSL | 6 |
| `PythonRsDriver` connection with username/password auth | 6 |

---

## 5. References

- [python-rs-driver repository](https://github.com/scylladb-zpp-2025-python-rs-driver/python-rs-driver)
- [scylla-rust-driver](https://github.com/scylladb/scylla-rust-driver) — underlying Rust driver
- [python-rs-driver-support.md](python-rs-driver-support.md) — original support plan with API gap analysis and maturity matrix
- [PythonRsDriver source](../../src/coodie/drivers/python_rs.py) — current implementation
- [AcsyllaDriver source](../../src/coodie/drivers/acsylla.py) — reference for background-thread sync bridge pattern
- [Integration test conftest](../../tests/integration/conftest.py) — skip logic for python-rs
