# Test Refactoring Plan

> **Goal:** Reduce test duplication, improve maintainability, and shrink file
> sizes by applying `pytest.mark.parametrize`, merging mirrored sync/async
> tests, and splitting the monolithic integration test file into focused modules.
>
> Guided by the [test-refactoring skill](../../.github/skills/test-refactoring/SKILL.md).

---

## Table of Contents

1. [Current State](#1-current-state)
2. [Task 1 — Parametrize `test_types.py`](#2-task-1--parametrize-test_typespy)
3. [Task 2 — Parametrize `test_cql_builder.py`](#3-task-2--parametrize-test_cql_builderpy)
4. [Task 3 — Merge sync/async unit tests](#4-task-3--merge-syncasync-unit-tests)
5. [Task 4 — Split `test_integration.py`](#5-task-4--split-test_integrationpy)
6. [Task 5 — Parametrize extended-type roundtrips](#6-task-5--parametrize-extended-type-roundtrips)
7. [Task 6 — Deduplicate ScyllaDB testcontainer fixtures with benchmarks](#7-task-6--deduplicate-scylladb-testcontainer-fixtures-with-benchmarks)
8. [Implementation Order](#8-implementation-order)
9. [Verification](#9-verification)

---

## 1. Current State

| File | Lines | Problem |
|------|-------|---------|
| `tests/test_types.py` | 242 | ~15 one-liner type-mapping functions + ~7 coercion functions with identical structure |
| `tests/test_cql_builder.py` | 706 | Repetitive filter-operator, collection-op, and USING-clause tests |
| ~~`tests/sync/test_document.py`~~ | ~~699~~ | ✅ Merged into `tests/test_document.py` (725 lines) |
| ~~`tests/aio/test_document.py`~~ | ~~609~~ | ✅ Merged into `tests/test_document.py` |
| ~~`tests/sync/test_query.py`~~ | ~~432~~ | ✅ Merged into `tests/test_query.py` (475 lines) |
| ~~`tests/aio/test_query.py`~~ | ~~408~~ | ✅ Merged into `tests/test_query.py` |
| ~~`tests/sync/test_polymorphic.py`~~ | ~~320~~ | ✅ Merged into `tests/test_polymorphic.py` (319 lines) |
| ~~`tests/aio/test_polymorphic.py`~~ | ~~183~~ | ✅ Merged into `tests/test_polymorphic.py` |
| `tests/test_integration.py` | ~~2,435~~ | ✅ Split into `tests/integration/` (1663 lines, 7 files) |
| **Total** | **~5,547** | |

---

## 2. Task 1 — Parametrize `test_types.py`

**Status:** ✅ Done
**Effort:** Low
**Target:** ~242 → ~130 lines (achieved ~179 after ruff formatting)

### 2.1 Collapse `python_type_to_cql_type_str` basic type tests

The following 15 individual functions all call `python_type_to_cql_type_str(X)` and
assert `== "cql_string"`:

- `test_str_to_text`, `test_int_to_int`, `test_float_to_float`, `test_bool_to_boolean`,
  `test_bytes_to_blob`, `test_uuid_to_uuid`, `test_datetime_to_timestamp`, `test_date_to_date`,
  `test_decimal_to_decimal`, `test_ipv4_to_inet`, `test_list_str`, `test_set_int`,
  `test_dict_str_int`, `test_optional_str`, `test_annotated_unwraps`

**Replace with:**

```python
@pytest.mark.parametrize("python_type, expected_cql", [
    pytest.param(str,           "text",            id="str-to-text"),
    pytest.param(int,           "int",             id="int-to-int"),
    pytest.param(float,         "float",           id="float-to-float"),
    pytest.param(bool,          "boolean",         id="bool-to-boolean"),
    pytest.param(bytes,         "blob",            id="bytes-to-blob"),
    pytest.param(UUID,          "uuid",            id="uuid-to-uuid"),
    pytest.param(datetime,      "timestamp",       id="datetime-to-timestamp"),
    pytest.param(date,          "date",            id="date-to-date"),
    pytest.param(Decimal,       "decimal",         id="decimal-to-decimal"),
    pytest.param(IPv4Address,   "inet",            id="ipv4-to-inet"),
    pytest.param(dt_time,       "time",            id="time-to-time"),
    pytest.param(list[str],     "list<text>",      id="list-str"),
    pytest.param(set[int],      "set<int>",        id="set-int"),
    pytest.param(dict[str,int], "map<text, int>",  id="dict-str-int"),
    pytest.param(Optional[str], "text",            id="optional-str"),
    pytest.param(Annotated[UUID, PrimaryKey()], "uuid", id="annotated-unwraps"),
])
def test_python_type_to_cql_type_str(python_type, expected_cql):
    assert python_type_to_cql_type_str(python_type) == expected_cql
```

### 2.2 Collapse extended-type marker tests

The 8 marker tests (`test_bigint_marker` through `test_time_marker`) become:

```python
@pytest.mark.parametrize("annotated_type, expected_cql", [
    pytest.param(Annotated[int, BigInt()],     "bigint",   id="bigint"),
    pytest.param(Annotated[int, SmallInt()],   "smallint", id="smallint"),
    pytest.param(Annotated[int, TinyInt()],    "tinyint",  id="tinyint"),
    pytest.param(Annotated[int, VarInt()],     "varint",   id="varint"),
    pytest.param(Annotated[float, Double()],   "double",   id="double"),
    pytest.param(Annotated[str, Ascii()],      "ascii",    id="ascii"),
    pytest.param(Annotated[UUID, TimeUUID()],  "timeuuid", id="timeuuid"),
    pytest.param(Annotated[dt_time, Time()],   "time",     id="time-marker"),
])
def test_extended_type_marker(annotated_type, expected_cql):
    assert python_type_to_cql_type_str(annotated_type) == expected_cql
```

### 2.3 Collapse frozen-type tests

The 4 frozen tests (`test_frozen_list` through `test_frozen_tuple`) become:

```python
@pytest.mark.parametrize("annotated_type, expected_cql", [
    pytest.param(Annotated[list[str], Frozen()],       "frozen<list<text>>",       id="frozen-list"),
    pytest.param(Annotated[set[int], Frozen()],        "frozen<set<int>>",         id="frozen-set"),
    pytest.param(Annotated[dict[str,int], Frozen()],   "frozen<map<text, int>>",   id="frozen-map"),
    pytest.param(Annotated[tuple[str,int], Frozen()],  "frozen<tuple<text, int>>", id="frozen-tuple"),
])
def test_frozen_type(annotated_type, expected_cql):
    assert python_type_to_cql_type_str(annotated_type) == expected_cql
```

### 2.4 Collapse `coerce_row_none_collections` tests

The 5 `_FakeDoc` coercion tests become:

```python
@pytest.mark.parametrize("field, input_val, expected", [
    pytest.param("tags",        None,       [],          id="none-list-to-empty"),
    pytest.param("labels",      None,       set(),       id="none-set-to-empty"),
    pytest.param("meta",        None,       {},          id="none-dict-to-empty"),
    pytest.param("tags",        ["a","b"],  ["a","b"],   id="non-none-unchanged"),
    pytest.param("description", None,       None,        id="scalar-none-unchanged"),
])
def test_coerce_row_none_collections(field, input_val, expected):
    row = {field: input_val}
    if field == "tags" and input_val is not None:
        row["name"] = "x"
    result = coerce_row_none_collections(_FakeDoc, row)
    assert result[field] == expected
```

**Keep separate:** `test_coerce_annotated_collection` and `test_coerce_optional_collection`
(they need their own doc classes), `test_unsupported_type_raises`, `test_no_cqlengine_import`,
`test_marker_with_primary_key`, `test_frozen_with_marker`.

---

## 3. Task 2 — Parametrize `test_cql_builder.py`

**Status:** ✅ Done
**Effort:** Low–Medium
**Target:** ~706 → ~500 lines (achieved ~689 after ruff formatting)

### 3.1 Collapse `parse_filter_kwargs` operator variants

Tests: `test_parse_filter_kwargs_eq`, `test_parse_filter_kwargs_operators`,
`test_parse_filter_kwargs_in`, `test_parse_filter_kwargs_like`

```python
@pytest.mark.parametrize("kwargs, expected_triple", [
    pytest.param({"name": "Alice"},     ("name", "=", "Alice"),     id="eq"),
    pytest.param({"rating__gte": 4},    ("rating", ">=", 4),       id="gte"),
    pytest.param({"price__lt": 100},    ("price", "<", 100),       id="lt"),
    pytest.param({"id__in": [1,2,3]},   ("id", "IN", [1,2,3]),    id="in"),
    pytest.param({"name__like": "Al%"}, ("name", "LIKE", "Al%"),   id="like"),
])
def test_parse_filter_kwargs(kwargs, expected_triple):
    result = parse_filter_kwargs(kwargs)
    assert expected_triple in result
```

### 3.2 Collapse token-range `parse_filter_kwargs` variants

Tests: `test_parse_filter_kwargs_token_gt`, `test_parse_filter_kwargs_token_gte`,
`test_parse_filter_kwargs_token_lt`, `test_parse_filter_kwargs_token_lte`

```python
@pytest.mark.parametrize("kwargs, expected_triple", [
    pytest.param({"id__token__gt": 100},  ("id", "TOKEN >", 100),  id="token-gt"),
    pytest.param({"id__token__gte": 100}, ("id", "TOKEN >=", 100), id="token-gte"),
    pytest.param({"id__token__lt": 200},  ("id", "TOKEN <", 200),  id="token-lt"),
    pytest.param({"id__token__lte": 200}, ("id", "TOKEN <=", 200), id="token-lte"),
])
def test_parse_filter_kwargs_token(kwargs, expected_triple):
    result = parse_filter_kwargs(kwargs)
    assert result == [expected_triple]
```

### 3.3 Collapse collection operation tests

Tests: `test_build_update_collection_add`, `test_build_update_collection_remove`,
`test_build_update_collection_append`, `test_build_update_collection_prepend`

```python
@pytest.mark.parametrize("op_key, op_name, value, expected_fragment", [
    pytest.param("tags",  "add",     {"new_tag"}, '"tags" = "tags" + ?',   id="set-add"),
    pytest.param("tags",  "remove",  {"old_tag"}, '"tags" = "tags" - ?',   id="set-remove"),
    pytest.param("items", "append",  ["z"],       '"items" = "items" + ?', id="list-append"),
    pytest.param("items", "prepend", ["a"],       '"items" = ? + "items"', id="list-prepend"),
])
def test_build_update_collection_op(op_key, op_name, value, expected_fragment):
    cql, params = build_update(
        "products", "ks", set_data={},
        where=[("id", "=", "1")],
        collection_ops=[(op_key, op_name, value)],
    )
    assert expected_fragment in cql
```

### 3.4 Collapse USING clause tests

Tests: `test_build_insert_ttl`, `test_build_insert_timestamp`,
`test_build_insert_ttl_and_timestamp`, `test_build_update_with_ttl`,
`test_build_update_timestamp`, `test_build_update_ttl_and_timestamp`,
`test_build_delete_timestamp`

```python
@pytest.mark.parametrize("builder, extra_kwargs, expected_fragment", [
    pytest.param("insert", {"ttl": 60},                         "USING TTL 60",                        id="insert-ttl"),
    pytest.param("insert", {"timestamp": 1234567890},           "USING TIMESTAMP 1234567890",          id="insert-ts"),
    pytest.param("insert", {"ttl": 60, "timestamp": 1234567890}, "USING TTL 60 AND TIMESTAMP 1234567890", id="insert-ttl-ts"),
    pytest.param("update", {"ttl": 300},                        "USING TTL 300",                       id="update-ttl"),
    pytest.param("update", {"timestamp": 1234567890},           "USING TIMESTAMP 1234567890",          id="update-ts"),
    pytest.param("update", {"ttl": 60, "timestamp": 1234567890}, "USING TTL 60 AND TIMESTAMP 1234567890", id="update-ttl-ts"),
    pytest.param("delete", {"timestamp": 1234567890},           "USING TIMESTAMP 1234567890",          id="delete-ts"),
])
def test_using_clause(builder, extra_kwargs, expected_fragment):
    if builder == "insert":
        cql, _ = build_insert("products", "ks", {"id": "1"}, **extra_kwargs)
    elif builder == "update":
        cql, _ = build_update("products", "ks", set_data={"name": "Y"}, where=[("id", "=", "1")], **extra_kwargs)
    else:
        cql, _ = build_delete("products", "ks", [("id", "=", "1")], **extra_kwargs)
    assert expected_fragment in cql
```

**Keep separate:** Tests with unique structure (e.g., `test_create_table_*`,
`test_build_batch`, counter tests, materialized view tests).

---

## 4. Task 3 — Merge sync/async unit tests

**Status:** ✅ Done
**Effort:** Medium
**Target:** Eliminate `tests/sync/` and `tests/aio/` directories; move to unified test files
**Result:** 8 files (2656 lines) → 5 files (1720 lines, −35%). Test count increased from 463 → 489.

### 4.1 Extract shared model definitions

Create `tests/models.py` with factory functions:

```python
def _make_product(base_cls):
    class Product(base_cls):
        class Settings:
            name = "products"
            keyspace = "test_ks"
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        name: str
        brand: Annotated[str, Indexed()] = "Unknown"
        price: float = 0.0
        description: Optional[str] = None
    return Product
```

**⚠️ PEP 563 caveat:** Do NOT use `from __future__ import annotations` in files
that define Document subclasses inside functions. PEP 563 stores annotations as
strings, and `get_type_hints()` cannot resolve them for classes in local scope,
causing `build_schema()` to return empty columns. **Workaround:** define model
factories at module level without the `__future__` import. See
`benchmarks/bench_schema.py` for a verified example. This may be resolved by
PEP 649 (deferred evaluation) in Python 3.14+.

### 4.2 Add `_maybe_await` helper to `tests/conftest.py`

```python
import inspect

async def _maybe_await(fn, *args, **kwargs):
    result = fn(*args, **kwargs)
    if inspect.isawaitable(result):
        return await result
    return result
```

### 4.3 Merge `test_document.py` sync/async pair

Current state:
- `tests/sync/test_document.py` — 699 lines, 40+ test functions
- `tests/aio/test_document.py` — 609 lines, 35+ test functions

Target: Single `tests/test_document.py` with a `document_cls` fixture parametrized
over sync/async:

```python
@pytest.fixture(params=["sync", "async"], ids=["sync", "async"])
def document_cls(request):
    if request.param == "sync":
        from coodie.sync.document import Document
        return Document
    from coodie.aio.document import Document
    return Document
```

Each test method runs twice — once sync, once async — via `_maybe_await`.

### 4.4 Merge `test_query.py` sync/async pair

Current state:
- `tests/sync/test_query.py` — 432 lines
- `tests/aio/test_query.py` — 408 lines

Target: Single `tests/test_query.py` (if different from existing `test_cql_builder.py`)
or integrated into existing files.

### 4.5 Merge `test_polymorphic.py` sync/async pair

Current state:
- `tests/sync/test_polymorphic.py` — 320 lines (16 tests)
- `tests/aio/test_polymorphic.py` — 183 lines (10 tests)

Note: The async version has fewer tests. The merged version should include ALL
tests from the sync version, running both variants.

### 4.6 Merge `test_keyspace.py` sync/async pair

Current state:
- `tests/sync/test_keyspace.py` — 30 lines
- `tests/aio/test_keyspace.py` — 35 lines

These are tiny and can be merged trivially.

---

## 5. Task 4 — Split `test_integration.py`

**Status:** ✅ Done
**Effort:** Medium
**Target:** ~2,435 → 5 files, each < 500 lines
**Result:** 1 file (2297 lines) → 7 files (1663 lines, −28%). Test count increased from 118 → 130.

### 5.1 Create package structure

```
tests/integration/
├── __init__.py
├── conftest.py          # Session fixtures + shared models + _maybe_await
├── test_basic.py        # CRUD: save, find_one, filter, delete, update, pagination
├── test_raw_cql.py      # Raw CQL execution tests
├── test_keyspace.py     # Keyspace create/drop/sync
├── test_extended.py     # Extended type roundtrips, collections, batch
└── test_views.py        # Materialized view tests
```

### 5.2 Move session fixtures to `conftest.py`

Move from `test_integration.py`:
- `scylla_container` fixture (lines 56–78)
- `_LocalhostTranslator` class (lines 81–94)
- `scylla_session` fixture (lines 97–199)
- `coodie_driver` fixture (lines 200–229)
- All model definitions (`SyncProduct`, `AsyncProduct`, `SyncReview`, `AsyncReview`,
  `SyncProductsByBrand`, `AsyncProductsByBrand`, `SyncAllTypes`, `AsyncAllTypes`,
  `SyncEvent`, `AsyncEvent`, `SyncExtendedTypes`, `AsyncExtendedTypes`)

### 5.3 Merge sync/async class pairs

Each sync/async class pair becomes a single test class using `_maybe_await` +
parametrized fixture:

| Current (2 classes) | Merged (1 class) | Target file |
|---|---|---|
| `TestSyncIntegration` + `TestAsyncIntegration` | `TestIntegration` | `test_basic.py` |
| `TestSyncRawCQL` + `TestAsyncRawCQL` | `TestRawCQL` | `test_raw_cql.py` |
| `TestSyncKeyspaceManagement` + `TestAsyncKeyspaceManagement` | `TestKeyspaceManagement` | `test_keyspace.py` |
| `TestSyncExtended` + `TestAsyncExtended` | `TestExtended` | `test_extended.py` |
| `TestSyncMaterializedView` + `TestAsyncMaterializedView` | `TestMaterializedView` | `test_views.py` |

### 5.4 Actual line counts after split

| File | Lines |
|------|-------|
| `conftest.py` | 612 (fixtures + models + helpers) |
| `test_basic.py` | 378 (merged CRUD + QuerySet enhancements) |
| `test_raw_cql.py` | 59 (merged raw CQL) |
| `test_keyspace.py` | 57 (merged keyspace) |
| `test_extended.py` | 474 (merged extended + collections + batch) |
| `test_views.py` | 83 (merged materialized view) |

### 5.5 Update `pyproject.toml` test configuration

Ensure `testpaths` and markers still work:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = ["integration: requires a running ScyllaDB instance"]
```

The integration marker is already applied at the class/module level and will
carry over to the new package.

---

## 6. Task 5 — Parametrize extended-type roundtrips

**Status:** ✅ Done
**Effort:** Low (depends on Task 4 completing first)
**Target:** Eliminate 8 near-identical roundtrip methods per sync/async class
**Result:** 474 → 403 lines (−15%). 11 individual methods → 2 parametrized + 1 separate. Test count unchanged (54).

### 6.1 Current repetition

In `TestSyncExtended` and `TestAsyncExtended`, these 8 methods share identical
structure (create doc → save → read back → assert value):

- `test_bigint_roundtrip`
- `test_smallint_roundtrip`
- `test_tinyint_roundtrip`
- `test_varint_roundtrip`
- `test_double_roundtrip`
- `test_ascii_roundtrip`
- `test_timeuuid_roundtrip`
- `test_time_roundtrip`

Plus 3 frozen collection roundtrips: `test_frozen_list_roundtrip`,
`test_frozen_set_roundtrip`, `test_frozen_map_roundtrip`.

### 6.2 Replace with parametrized test

```python
@pytest.mark.parametrize("field_name, write_value", [
    pytest.param("big",       2**40,        id="bigint"),
    pytest.param("small",     32_000,       id="smallint"),
    pytest.param("tiny",      127,          id="tinyint"),
    pytest.param("var",       10**30,       id="varint"),
    pytest.param("dbl",       3.14,         id="double"),
    pytest.param("ascii_val", "hello",      id="ascii"),
])
async def test_extended_type_roundtrip(coodie_driver, field_name, write_value):
    # create doc with field_name set to write_value
    # save, read back, assert field matches
    ...
```

`timeuuid` and `time` roundtrips need special value generation (uuid1 for
timeuuid, `datetime.time` for time) so they may warrant separate parametrize
entries with custom comparison logic, or separate tests.

Frozen collections (`frozen_list`, `frozen_set`, `frozen_map`) can be a separate
parametrized test since the model and assertion differ.

---

## 7. Task 6 — Deduplicate ScyllaDB testcontainer fixtures with benchmarks

**Status:** ✅ Done
**Effort:** Medium
**Depends on:** Task 4, PR #31 (benchmarks)

### 7.1 Problem

PR #31 adds `benchmarks/conftest.py` with ScyllaDB testcontainer fixtures that
are nearly identical to the ones in `tests/test_integration.py`:

| Fixture / helper | `tests/test_integration.py` | `benchmarks/conftest.py` |
|---|---|---|
| `scylla_container` | ✅ session-scoped, DockerContainer | ✅ session-scoped, DockerContainer (identical) |
| `_LocalhostTranslator` | ✅ translates to 127.0.0.1 | ✅ translates to 127.0.0.1 (identical) |
| `scylla_session` / `cql_session` | ✅ Cluster → Session, retry loop | ✅ Cluster → Session, retry loop (same logic, different keyspace) |

When Task 4 moves integration fixtures to `tests/integration/conftest.py`, the
duplication becomes two separate `conftest.py` files with copy-pasted container
setup code. Changes to the container image, startup flags, or retry logic would
need to be applied in both places.

### 7.2 Solution — Extract shared fixtures to a `conftest_shared.py` plugin

Create a shared module that both `tests/integration/conftest.py` and
`benchmarks/conftest.py` can import:

```
tests/
├── conftest_scylla.py          # Shared ScyllaDB container + session helpers
├── conftest.py                 # Existing: MockDriver, driver_type option
├── integration/
│   └── conftest.py             # imports from conftest_scylla
benchmarks/
    └── conftest.py             # imports from conftest_scylla
```

**`tests/conftest_scylla.py`** (new shared module):

```python
"""Shared ScyllaDB testcontainer fixtures.

Import these into integration test or benchmark conftest.py files to avoid
duplicating the container setup, address translator, and session creation.
"""
from __future__ import annotations

import time
from typing import Any

import pytest


class LocalhostTranslator:
    """Translate container-internal IPs back to 127.0.0.1."""
    def translate(self, addr: str) -> str:
        return "127.0.0.1"


@pytest.fixture(scope="session")
def scylla_container():
    """Start a ScyllaDB container once for the entire test session."""
    try:
        from testcontainers.core.container import DockerContainer
        from testcontainers.core.waiting_utils import wait_for_logs
    except ImportError as exc:
        pytest.skip(f"testcontainers not installed: {exc}")

    with (
        DockerContainer("scylladb/scylla:latest")
        .with_command(
            "--smp 1 --memory 512M --developer-mode 1 "
            "--skip-wait-for-gossip-to-settle=0"
        )
        .with_exposed_ports(9042) as container
    ):
        wait_for_logs(container, "Starting listening for CQL clients", timeout=120)
        yield container


def create_cql_session(scylla_container: Any, keyspace: str) -> Any:
    """Create a cassandra-driver Session connected to the given keyspace.

    Handles the retry loop for container startup and creates the keyspace
    if it doesn't exist.
    """
    from cassandra.cluster import Cluster, NoHostAvailable

    port = int(scylla_container.get_exposed_port(9042))
    cluster = Cluster(
        ["127.0.0.1"],
        port=port,
        connect_timeout=10,
        address_translator=LocalhostTranslator(),
    )

    for attempt in range(10):
        try:
            session = cluster.connect()
            break
        except NoHostAvailable:
            if attempt == 9:
                raise
            time.sleep(2)

    session.execute(
        f"CREATE KEYSPACE IF NOT EXISTS {keyspace} "
        "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}"
    )
    return session, cluster
```

### 7.3 Update integration `conftest.py`

```python
# tests/integration/conftest.py
from tests.conftest_scylla import scylla_container, create_cql_session  # noqa: F401

@pytest.fixture(scope="session")
def scylla_session(scylla_container, driver_type):
    if driver_type == "acsylla":
        yield None
        return
    session, cluster = create_cql_session(scylla_container, "test_ks")
    yield session
    cluster.shutdown()
```

### 7.4 Update benchmarks `conftest.py` — add `driver_type` support

The current benchmarks only use `cassandra-driver`. They should support the
same `--driver-type` option as integration tests (`scylla`, `cassandra`,
`acsylla`) so benchmarks can be run against any driver backend.

```python
# benchmarks/conftest.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tests.conftest_scylla import scylla_container, create_cql_session, create_acsylla_session  # noqa: F401

# Reuse the same --driver-type option from tests/conftest.py
# (pytest_addoption and driver_type fixture are inherited from the root conftest)

@pytest.fixture(scope="session")
def cql_session(scylla_container, driver_type):
    """CQL session — skipped when driver_type is acsylla."""
    if driver_type == "acsylla":
        yield None
        return
    session, cluster = create_cql_session(scylla_container, "bench_ks")
    session.set_keyspace("bench_ks")
    yield session
    cluster.shutdown()

@pytest.fixture(scope="session")
def coodie_connection(cql_session, scylla_container, driver_type):
    """Register the coodie driver — supports all driver backends."""
    from coodie.drivers import _registry, init_coodie

    _registry.clear()
    if driver_type == "acsylla":
        # Create acsylla session + AcsyllaDriver (same pattern as integration tests)
        driver = await create_acsylla_session(scylla_container, "bench_ks")
    else:
        driver = init_coodie(session=cql_session, keyspace="bench_ks", driver_type=driver_type)
    yield driver
    _registry.clear()
```

The shared `create_acsylla_session` helper in `conftest_scylla.py` should
encapsulate the acsylla cluster/session creation and `AcsyllaDriver`
registration logic currently duplicated in `tests/test_integration.py`'s
`coodie_driver` fixture.

**Benchmark run commands with driver selection:**

```bash
# Default (scylla-driver)
uv run pytest benchmarks/ -v --benchmark-enable

# With acsylla driver
uv run pytest benchmarks/ -v --benchmark-enable --driver-type=acsylla

# With cassandra-driver
uv run pytest benchmarks/ -v --benchmark-enable --driver-type=cassandra
```

### 7.5 Audit checklist

Before merging, verify:

- [x] `tests/conftest_scylla.py` contains the single source of truth for `scylla_container`, `LocalhostTranslator`, `create_cql_session`, and `create_acsylla_session`
- [x] `tests/integration/conftest.py` imports (not copies) the shared fixtures
- [x] `benchmarks/conftest.py` imports (not copies) the shared fixtures
- [x] `benchmarks/conftest.py` supports `--driver-type` for all three backends (scylla, cassandra, acsylla)
- [x] No duplicate `DockerContainer("scylladb/scylla:latest")` code exists outside `conftest_scylla.py`
- [ ] Integration tests pass: `uv run pytest -m integration -v --timeout=120`
- [ ] Integration tests pass with acsylla: `uv run pytest -m integration -v --timeout=120 --driver-type=acsylla`
- [ ] Benchmarks pass: `uv run pytest benchmarks/ -v --benchmark-enable` (requires Docker)
- [ ] Benchmarks pass with acsylla: `uv run pytest benchmarks/ -v --benchmark-enable --driver-type=acsylla`
- [ ] Both `test_ks` and `bench_ks` keyspaces are created correctly (different keyspaces to avoid interference)

---

## 8. Implementation Order

Tasks are independent; each can be merged as a separate PR.

| Step | Task | Files changed | Depends on |
|------|------|---------------|------------|
| 1 | Parametrize `test_types.py` | `tests/test_types.py` | — |
| 2 | Parametrize `test_cql_builder.py` | `tests/test_cql_builder.py` | — |
| 3 | Merge sync/async unit tests | `tests/sync/`, `tests/aio/`, `tests/conftest.py` | — |
| 4 | Split `test_integration.py` | `tests/test_integration.py` → `tests/integration/` | — |
| 5 | Parametrize extended roundtrips | `tests/integration/test_extended.py` | Task 4 |
| 6 | Deduplicate ScyllaDB fixtures | `tests/conftest_scylla.py`, `tests/integration/conftest.py`, `benchmarks/conftest.py` | Task 4 + PR #31 |

**Recommended start:** Task 1 (lowest risk, validates the approach).

---

## 9. Verification

After each task:

1. **Run unit tests:**
   ```bash
   uv run pytest tests/ -v --ignore=tests/test_integration.py
   ```

2. **Compare test count** — must be equal or higher than before:
   ```bash
   uv run pytest tests/ --collect-only -q --ignore=tests/test_integration.py | tail -1
   ```

3. **Run linter:**
   ```bash
   uv run ruff check tests/ && uv run ruff format --check tests/
   ```

4. **Run integration tests** (Tasks 4 & 5 only):
   ```bash
   uv run pytest -m integration -v --timeout=120
   uv run pytest -m integration -v --timeout=120 --driver-type=acsylla
   ```

5. **Check file sizes:**
   ```bash
   wc -l tests/*.py tests/**/*.py
   ```
   All files should be < 400 lines (target) or < 500 lines (hard limit).
