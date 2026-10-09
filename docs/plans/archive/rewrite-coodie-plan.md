# coodie Rewrite Plan

> **coodie** = cassandra + beanie (hoodie)
>
> A ground-up rewrite of coodie as a **Pydantic-based ODM for ScyllaDB/Cassandra**,
> inspired by [BeanieODM](https://github.com/BeanieODM/beanie).
> Key constraints: **no cqlengine**, **pluggable drivers**, **sync and async APIs**.

---

## Background & Goals

The current codebase wraps `cassandra.cqlengine` with a metaclass hack that tries
to combine Pydantic's `BaseModel` and cqlengine's `Model` in one class.  This is
brittle, limits async support, and ties the library to a single driver
implementation.

The rewrite starts fresh:

| Goal | Detail |
|---|---|
| No cqlengine | All CQL generated from scratch via `cql_builder.py`; raw `cassandra.cluster.Session` only |
| Pydantic-first | `Document(BaseModel)` — pure Pydantic validation, serialisation, and field declaration |
| Pluggable drivers | `CassandraDriver` (cassandra-driver / scylla-driver) or `AcsyllaDriver` ([acsylla](https://github.com/acsylla/acsylla)) |
| Sync + async | Separate `coodie.sync` and `coodie.aio` modules (like Bunnet vs Beanie), both in the same codebase to prevent API drift, sharing all infrastructure (`schema`, `types`, `cql_builder`, `drivers`) |
| Full test coverage | Unit tests with `MockDriver` (no DB) + integration tests with real ScyllaDB via testcontainers |
| FastAPI demo | Runnable Product Catalog API showcasing every major feature |

## Design principle: separate sync and async modules

Inspired by the [Beanie](https://github.com/BeanieODM/beanie) (async) /
[Bunnet](https://github.com/BeanieODM/bunnet) (sync) split, coodie ships two
distinct public modules in a **single codebase**:

| Module | Import path | Driver requirement | Use case |
|---|---|---|---|
| Async API | `coodie.aio` | async-capable driver (CassandraDriver via asyncio bridge, AcsyllaDriver) | FastAPI, async frameworks |
| Sync API | `coodie.sync` | sync driver (CassandraDriver sync execute path) | Scripts, Django, Flask, testing |

Both modules are backed by identical shared infrastructure
(`schema`, `types`, `cql_builder`, `drivers`, `exceptions`, `fields`) —
keeping a single source of truth and preventing the drift that affects
Beanie/Bunnet as separate repos.

The `coodie` top-level package re-exports the async API by default (matching
Beanie's convention), but the sync API is a first-class citizen reachable
via `coodie.sync`.

---

## Intended Public API

### Async API (`coodie.aio`)

```python
from typing import Annotated, Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import Field
from coodie.aio import Document, init_coodie
from coodie import PrimaryKey, ClusteringKey, Indexed

class Review(Document):
    product_id: Annotated[UUID, PrimaryKey()]
    created_at: Annotated[datetime, ClusteringKey(order="DESC")] = Field(
        default_factory=datetime.utcnow
    )
    author: str
    rating: Annotated[int, Indexed()]
    content: Optional[str] = None

    class Settings:
        name = "reviews"
        keyspace = "catalog"

# FastAPI lifespan
await init_coodie(hosts=["127.0.0.1"], keyspace="catalog", driver_type="cassandra")
await Review.sync_table()

# Async CRUD
await review.save()
results = await Review.find(product_id=pid).order_by("-created_at").limit(20).all()
```

### Sync API (`coodie.sync`)

```python
from coodie.sync import Document, init_coodie
from coodie import PrimaryKey, ClusteringKey, Indexed

class Review(Document):
    # identical field declarations — shared schema infrastructure
    ...

    class Settings:
        name = "reviews"
        keyspace = "catalog"

# Script / Django / Flask setup
init_coodie(hosts=["127.0.0.1"], keyspace="catalog")
Review.sync_table()

# Sync CRUD — identical method names, no await
review.save()
results = Review.find(product_id=pid).order_by("-created_at").limit(20).all()
```

**Key point:** model definitions (field annotations, `Settings` inner class) are
100% identical between `coodie.aio` and `coodie.sync` — a model can be switched
between sync and async simply by changing the import.

---

## cqlengine Feature-Parity Targets

Everything cqlengine provides today will be reimplemented **without** importing it.

### Column / type system
- Scalar types: `text`, `int`, `bigint`, `float`, `double`, `boolean`, `uuid`, `timeuuid`,
  `timestamp`, `date`, `blob`, `decimal`, `varint`, `smallint`, `tinyint`, `inet`
- Collection types: `list<T>`, `set<T>`, `map<K,V>`, `tuple<…>`, `frozen<…>`
- Counter columns
- User-Defined Types (UDT) — post-MVP

### Schema / DDL management
- `CREATE KEYSPACE IF NOT EXISTS … WITH replication = {…}`
- `CREATE TABLE IF NOT EXISTS` with composite partition key, clustering keys, ordering
- `CREATE INDEX IF NOT EXISTS` (secondary index)
- `DROP TABLE` / `DROP INDEX`
- `sync_table` — idempotent CREATE + `ALTER TABLE … ADD` for new columns
- `__table_name__` override (default: `snake_case` of class name)
- `Settings.keyspace`

### Field annotations
- `PrimaryKey()` — partition key; `partition_key_index` for composite keys
- `ClusteringKey(order="ASC"|"DESC")` — clustering column; `clustering_key_index`
- `Indexed()` — secondary index
- `Counter()` — counter column marker

### Write operations
- `INSERT INTO … VALUES (?)` — upsert (`save()` / `asave()`)
- `INSERT … IF NOT EXISTS` — create-only (`insert()` / `ainsert()`)
- `UPDATE … SET … WHERE …` — partial update (`update()` / `aupdate()`)
- `DELETE FROM … WHERE …` — row delete (`delete()` / `adelete()`)
- `DELETE col FROM … WHERE …` — column-level delete
- `USING TTL ?` — time-to-live on INSERT/UPDATE
- `USING TIMESTAMP ?` — explicit write timestamp
- Lightweight transactions: `INSERT … IF NOT EXISTS`, `UPDATE … IF col = ?`
- Batch writes (`BATCH … APPLY BATCH`) — sync and async

### Read operations
- `SELECT * FROM … WHERE …` with Django-style operators:
  `__gt`, `__gte`, `__lt`, `__lte`, `__in`, `__contains`, `__contains_key`
- `SELECT COUNT(*)`
- `LIMIT n`
- `ORDER BY col ASC|DESC` (clustering columns only)
- `ALLOW FILTERING`
- Token-range queries (full-table scans)
- `PER PARTITION LIMIT n` (ScyllaDB extension)

### QuerySet API (chainable builder — identical surface in `coodie.sync` and `coodie.aio`)
- `.filter(**kwargs)` — add WHERE clauses
- `.limit(n)`
- `.order_by(*cols)` — prefix `-` for DESC
- `.allow_filtering()`
- `.all()` — returns `list[Document]` (sync) / `Coroutine[list[Document]]` (async)
- `.first()` — returns `Document | None` (sync) / `Coroutine[Document | None]` (async)
- `.count()` — returns `int` (sync) / `Coroutine[int]` (async)
- `.delete()` — sync or async bulk delete
- `__iter__` (sync) / `__aiter__` (async)
- `__len__`

---

## Module Architecture

```
src/coodie/
├── __init__.py            # re-exports coodie.aio as default; exposes shared helpers
├── exceptions.py          # shared — DocumentNotFound, MultipleDocumentsFound, ConfigurationError, InvalidQueryError
├── fields.py              # shared — PrimaryKey(), ClusteringKey(), Indexed() — Annotated metadata helpers
├── schema.py              # shared — ColumnDefinition dataclass; build_schema(doc_cls)
├── types.py               # shared — Python type → CQL type string (zero cqlengine)
├── cql_builder.py         # shared — Pure-string DDL/DML generators
├── drivers/               # shared — pluggable execution backends
│   ├── __init__.py        # DriverRegistry, init_coodie() (sync), init_coodie_async()
│   ├── base.py            # AbstractDriver ABC (both sync + async methods)
│   ├── cassandra.py       # CassandraDriver (cassandra-driver / scylla-driver)
│   └── acsylla.py         # AcsyllaDriver (async-only; optional dep)
├── sync/                  # Synchronous API — like Bunnet
│   ├── __init__.py        # exports Document, QuerySet, init_coodie
│   ├── document.py        # SyncDocument(BaseModel) — sync CRUD only
│   └── query.py           # SyncQuerySet — sync __iter__, __len__, all(), first(), count()
└── aio/                   # Asynchronous API — like Beanie
    ├── __init__.py        # exports Document, QuerySet, init_coodie
    ├── document.py        # AsyncDocument(BaseModel) — async CRUD only (all methods are coroutines)
    └── query.py           # AsyncQuerySet — async __aiter__, all(), first(), count()
```

### Shared vs API-specific responsibilities

| Layer | Module | Shared? | Notes |
|---|---|---|---|
| Field metadata | `fields.py` | ✅ Yes | `PrimaryKey`, `ClusteringKey`, `Indexed` used identically in both APIs |
| Schema building | `schema.py` | ✅ Yes | `build_schema()` result is the same `list[ColumnDefinition]` for both |
| Type mapping | `types.py` | ✅ Yes | Python type → CQL type string |
| CQL generation | `cql_builder.py` | ✅ Yes | Produces `(str, list)` tuples; unaware of sync/async |
| Driver execution | `drivers/` | ✅ Yes | Both sync and async paths live in `CassandraDriver`; `AbstractDriver` defines both |
| Document base | `sync/document.py` | ❌ Sync only | No coroutines; `save()`, `delete()`, `find()` return values directly |
| Document base | `aio/document.py` | ❌ Async only | All public methods are `async def`; `save()`, `delete()`, `find()` are coroutines |
| QuerySet | `sync/query.py` | ❌ Sync only | `__iter__`, `all()` → `list[Document]` |
| QuerySet | `aio/query.py` | ❌ Async only | `__aiter__`, `all()` → `Coroutine[list[Document]]` |

### How they stay in sync

- `SyncDocument` and `AsyncDocument` both inherit from a shared `_BaseDocument(BaseModel)` in `sync/document.py` / `aio/document.py` respectively, where `_BaseDocument` holds all Pydantic field introspection, schema caching, and `Settings` parsing — the only difference is how the driver is called.
- `SyncQuerySet` and `AsyncQuerySet` both inherit from a shared `_QueryBuilder` (in `cql_builder.py`) that holds the immutable filter/limit/order state — only `_execute()` differs.
- A CI job compares the public method signatures of `coodie.sync.Document` and `coodie.aio.Document` to catch drift (simple `inspect`-based parity test in `tests/test_api_parity.py`).

### Module responsibilities (shared infrastructure)

#### `schema.py`
- `ColumnDefinition` dataclass: `name`, `cql_type`, `primary_key`, `partition_key`,
  `partition_key_index`, `clustering_key`, `clustering_key_index`, `clustering_order`,
  `index`, `index_name`, `required`
- `build_schema(doc_cls)` — inspects Pydantic `__fields__` + `Annotated` metadata;
  result cached on `cls.__schema__`

#### `types.py` (zero cqlengine)
- `_SCALAR_CQL_TYPES: dict[type, str]` — e.g. `{str: "text", UUID: "uuid", …}`
- `python_type_to_cql_type_str(annotation) → str` — handles `Optional[X]`,
  `list[X]`, `set[X]`, `dict[K,V]`

#### `cql_builder.py` (pure string generation)
- `build_create_keyspace(keyspace, replication_factor, strategy) → str`
- `build_create_table(table, keyspace, cols) → str`
- `build_create_index(table, keyspace, col) → str`
- `build_drop_table(table, keyspace) → str`
- `parse_filter_kwargs(kwargs) → list[tuple[col, op, value]]`
- `build_where_clause(filter_kwargs) → (str, list)`
- `build_select(table, keyspace, …) → (str, list)`
- `build_count(table, keyspace, …) → (str, list)`
- `build_insert(table, keyspace, data, ttl, if_not_exists) → (str, list)`
- `build_update(table, keyspace, set_data, where, ttl, if_conditions) → (str, list)`
- `build_delete(table, keyspace, where, columns) → (str, list)`
- `build_batch(statements, logged) → (str, list)`

#### `drivers/base.py`
```python
class AbstractDriver(ABC):
    def execute(self, stmt: str, params: list) -> list[dict]: ...
    async def execute_async(self, stmt: str, params: list) -> list[dict]: ...
    def sync_table(self, table, keyspace, cols): ...
    async def sync_table_async(self, table, keyspace, cols): ...
    def close(self): ...
    async def close_async(self): ...
```

#### `drivers/cassandra.py` — `CassandraDriver`
- Constructor: takes an already-connected `cassandra.cluster.Session`
- `execute()` → `session.execute(SimpleStatement(cql), params)`; rows normalised to
  `list[dict]` via `row._asdict()`
- `execute_async()` → `session.execute_async()`; `ResponseFuture` bridged to asyncio
  via `loop.call_soon_threadsafe` + `Future` callbacks
- `sync_table()` → DDL execution; uses `system_schema.columns` introspection for
  idempotent `ALTER TABLE … ADD`
- Prepared-statement cache keyed by CQL string for DML

#### `drivers/acsylla.py` — `AcsyllaDriver`
- Optional dependency (`try: import acsylla`); helpful `ImportError` if absent
- Constructor: takes an acsylla `Session`
- `execute_async()` → `await session.execute(statement)`; rows as `dict`-like objects
- `execute()` → `asyncio.get_event_loop().run_until_complete(execute_async(…))`
- Prepared statement support via `await session.create_prepared(cql)` + `prepared.bind(params)`

#### `drivers/__init__.py`
- `_registry: dict[str, AbstractDriver]`
- `register_driver(name, driver, default=False)`
- `get_driver(name=None) → AbstractDriver` — raises `ConfigurationError` if none registered
- `init_coodie(hosts=None, session=None, keyspace=None, driver_type="cassandra", name="default", **kwargs) → AbstractDriver`
- `async init_coodie_async(…) → AbstractDriver`

---

## Phase 0 — modern-python Skill (GitHub Copilot format)

Convert [`trailofbits/skills/plugins/modern-python`](https://github.com/trailofbits/skills/tree/main/plugins/modern-python)
from Claude plugin format to GitHub Copilot instruction format.

| Source (Claude plugin) | Destination (GitHub Copilot) |
|---|---|
| `skills/modern-python/SKILL.md` | `.github/instructions/modern-python.instructions.md` (`applyTo: "**/*.py"`) |
| `skills/modern-python/references/*.md` | `.github/instructions/references/*.instructions.md` |
| `skills/modern-python/templates/` | `.github/skill-templates/` |
| `hooks/shims/` + `hooks/setup-shims.sh` | `.github/hooks/` (unchanged, portable) |
| `.claude-plugin/plugin.json`, `hooks.json` | Dropped (Claude-specific runtime config) |

### Files to create

- `.github/instructions/modern-python.instructions.md`
- `.github/instructions/references/dependabot.instructions.md`
- `.github/instructions/references/migration-checklist.instructions.md`
- `.github/instructions/references/pep723-scripts.instructions.md`
- `.github/instructions/references/prek.instructions.md`
- `.github/instructions/references/pyproject.instructions.md`
- `.github/instructions/references/ruff-config.instructions.md`
- `.github/instructions/references/security-setup.instructions.md`
- `.github/instructions/references/testing.instructions.md`
- `.github/instructions/references/uv-commands.instructions.md`
- `.github/skill-templates/dependabot.yml`
- `.github/skill-templates/pre-commit-config.yaml`
- `.github/hooks/setup-shims.sh`
- `.github/hooks/setup-shims.bats`
- `.github/hooks/shims/python`
- `.github/hooks/shims/python3`
- `.github/hooks/shims/pip`
- `.github/hooks/shims/pip3`
- `.github/hooks/shims/pipx`
- `.github/hooks/shims/uv`
- `.github/hooks/shims/python-shim.bats`
- `.github/hooks/shims/pip-shim.bats`
- `.github/hooks/shims/pipx-shim.bats`
- `.github/hooks/shims/uv-shim.bats`

---

## Phase 1 — ODM rewrite: foundations

### 1a — Remove old code
- Delete `src/coodie/cassanandra_model.py`
- Strip all `cassandra.cqlengine` imports from `types.py`, `document.py`, `query.py`,
  `__init__.py`

### 1b — New core modules
- `src/coodie/schema.py`
- `src/coodie/types.py` (rewrite)
- `src/coodie/cql_builder.py`

### 1c — Pluggable driver layer
- `src/coodie/drivers/base.py`
- `src/coodie/drivers/cassandra.py`
- `src/coodie/drivers/acsylla.py`
- `src/coodie/drivers/__init__.py`

### 1d — Sync and async Document + QuerySet modules
- `src/coodie/sync/__init__.py` — exports `Document`, `QuerySet`, `init_coodie`
- `src/coodie/sync/document.py` — `SyncDocument(BaseModel)`; sync-only CRUD
- `src/coodie/sync/query.py` — `SyncQuerySet`; sync `__iter__`, `all()`, `first()`, `count()`, `delete()`
- `src/coodie/aio/__init__.py` — exports `Document`, `QuerySet`, `init_coodie`
- `src/coodie/aio/document.py` — `AsyncDocument(BaseModel)`; all methods are `async def`
- `src/coodie/aio/query.py` — `AsyncQuerySet`; async `__aiter__`, `all()`, `first()`, `count()`, `delete()`
- Remove `src/coodie/document.py` and `src/coodie/query.py` (replaced by the above)
- Update `src/coodie/__init__.py` — re-export from `coodie.aio` by default

---

## Phase 2 — Unit tests (no live DB)

All unit tests use a `MockDriver` fixture — no ScyllaDB instance required.

### Changes to `pyproject.toml`
- Add `pytest-asyncio` to dev-dependencies
- Set `asyncio_mode = "auto"` in `[tool.pytest.ini_options]`
- Register `integration` marker; default `addopts` excludes integration tests:
  `addopts = "-v --cov=coodie -m 'not integration'"`

### New / rewritten test files

| File | What it tests |
|---|---|
| `tests/conftest.py` | Add `MockSyncDriver` and `MockAsyncDriver` fixtures (record CQL/params) |
| `tests/test_schema.py` | `ColumnDefinition`, `build_schema()`, Annotated metadata, Optional handling |
| `tests/test_types.py` | Python → CQL type strings; zero cqlengine |
| `tests/test_cql_builder.py` | Every builder: DDL strings, WHERE operator parsing, DML strings, batch |
| `tests/sync/test_document.py` | `coodie.sync.Document` — all sync CRUD paths; `sync_table` |
| `tests/sync/test_query.py` | `SyncQuerySet` chaining; `__iter__`, `__len__`, `all()`, `first()`, `count()`, `delete()` |
| `tests/aio/test_document.py` | `coodie.aio.Document` — all async CRUD paths; `sync_table` |
| `tests/aio/test_query.py` | `AsyncQuerySet` chaining; `__aiter__`, `all()`, `first()`, `count()`, `delete()` |
| `tests/test_drivers.py` | `CassandraDriver`: mock Session; `AcsyllaDriver`: mock acsylla session |
| `tests/test_api_parity.py` | Uses `inspect` to assert `coodie.sync.Document` and `coodie.aio.Document` expose identical public method names (CI drift guard) |

---

## Phase 3 — Integration tests (real ScyllaDB via testcontainers)

### Why testcontainers instead of ccm

| | `ccm` (current) | `testcontainers` (new) |
|---|---|---|
| Setup | Download ScyllaDB binary; `~/.cql-test` scratch dir | `docker pull scylladb/scylla` |
| CI support | Fragile; platform-specific | First-class on GHA `ubuntu-latest` |
| Teardown | Manual `cluster.remove()` | Automatic on context-manager exit |
| Dependencies | `ccmlib` git install | `testcontainers[cassandra]` from PyPI |

### Fixture design

```python
@pytest.fixture(scope="session")
def scylla_container():
    # --smp 1 --memory 512M --developer-mode 1 keeps resource use within GHA limits
    with CassandraContainer("scylladb/scylla:latest").with_command(
        "--smp 1 --memory 512M --developer-mode 1"
    ) as container:
        yield container

@pytest.fixture(scope="session")
def scylla_session(scylla_container):
    cluster = Cluster([scylla_container.get_container_host_ip()],
                      port=scylla_container.get_exposed_port(9042))
    session = cluster.connect()
    session.execute(
        "CREATE KEYSPACE IF NOT EXISTS test_ks "
        "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}"
    )
    yield session
    cluster.shutdown()

@pytest.fixture(scope="session")
def coodie_driver(scylla_session):
    driver = init_coodie(session=scylla_session, keyspace="test_ks")
    yield driver
    driver.close()
```

All three fixtures are tagged `pytest.mark.integration` so `pytest` (no flags) skips them.

### `tests/test_integration.py` coverage

Two test classes share the same ScyllaDB container — one exercises `coodie.sync`,
the other `coodie.aio` — verifying identical behaviour from both APIs.

- **DDL**: `sync_table` creates table; safe to call twice (idempotent); `ALTER TABLE … ADD`
  used when a new column is added to the model
- **Scalar CRUD (sync)**: `save` → `find_one` → `get` by PK → `delete` → `DocumentNotFound`
- **Scalar CRUD (async)**: same sequence via `coodie.aio.Document`; all `await`-ed
- **Sync write/read cycle**: `save` → `all` → verify count and field values
- **Async write/read cycle**: `await save()` → `await all()` → verify; `await delete()` → `await find_one()` → `None`
- **QuerySet filtering**: `find(category="gadgets")`, `find(rating__gte=4)`,
  `.limit(5).allow_filtering()`
- **QuerySet ordering**: clustering-key DESC; `.order_by("-created_at")` newest-first
- **QuerySet async**: `await all()`, `await first()`, `await count()`, `async for`
- **Collections**: `list[str]`, `set[str]`, `dict[str, int]` — insert and retrieve
- **Secondary index**: `Indexed()` field; `find(brand="Acme")` via secondary index
- **Optional fields**: `None` round-trip; update to non-None; update back to `None`
- **TTL**: insert with `ttl=2`; sleep; verify row gone
- **Bulk insert**: `insert_many` (sync) / `await insert_many()` (async); `count()` returns N
- **Error paths**: `MultipleDocumentsFound`; `DocumentNotFound`
- **Multi-model isolation**: two `Document` subclasses → separate tables; no cross-contamination
- **API parity check**: `tests/test_api_parity.py` asserts both modules expose the same public method names
- **Acsylla driver** (optional, skipped if acsylla not installed): full CRUD via `AcsyllaDriver`

---

## Phase 4 — GitHub Actions workflows

### `test-unit.yml` (new)

```
Triggers : push to main, all pull_request events
Matrix   : Python 3.10 / 3.11 / 3.12  ×  ubuntu-latest / windows-latest / macos-latest
Docker   : not required
Steps    : checkout → setup-python → install-poetry → poetry install
           → pytest -m "not integration" --cov-report=xml
           → codecov upload
```

### `test-integration.yml` (new)

```
Triggers : push to main, pull_request (paths: src/**, tests/**)
Runner   : ubuntu-latest only (Docker required; macOS/Windows unreliable on free GHA)
Python   : 3.12 (single version — integration breadth covered by unit matrix)
Steps    : checkout → setup-python → install-poetry → poetry install
           → pytest -m integration -v --timeout=120
           → codecov upload (flags: integration)
Notes    : testcontainers pulls scylladb/scylla:latest automatically
           ScyllaDB flags (--smp 1 --memory 512M --developer-mode 1) stay within
           GHA's 2-core / 7 GB resource limits
           --timeout=120 guards against hung containers per test
```

### Update `ci.yml` (existing)

- Update Python matrix from `3.7–3.10` → `3.10`, `3.11`, `3.12`
  (aligned with `requires-python = "^3.10"`)
- Change `poetry run pytest` → `poetry run pytest -m "not integration"`
- Add `test-integration` to the `release` job's `needs` list
  (release only after both unit + integration pass on `main`)

---

## Phase 5 — FastAPI demo app

### Location: `demo/`

### Data models

| Document | Fields | CQL design |
|---|---|---|
| `Product` | `id` (UUID PK), `name`, `brand` (Indexed), `category` (Indexed), `price` (float), `description` (Optional[str]), `tags` (list[str]), `created_at` (datetime) | Partition key = `id`; secondary indexes on `brand`, `category` |
| `Review` | `product_id` (UUID, partition PK), `created_at` (datetime, clustering DESC), `id` (UUID), `author`, `rating` (int, Indexed), `content` (Optional[str]) | Partition key = `product_id`; clustering = `created_at DESC` → newest-first |

### API surface

```
GET    /products                    list (optional ?category=&brand= filters)
POST   /products                    create product
GET    /products/{id}               get by PK
PUT    /products/{id}               partial update
DELETE /products/{id}               delete
GET    /products/{id}/reviews       paginated, newest-first
POST   /products/{id}/reviews       add review
DELETE /products/{id}/reviews/{ts}  delete specific review
```

### Features highlighted
- `lifespan` startup: `from coodie.aio import init_coodie, Document` + `await init_coodie(…)` + `await Model.sync_table()`
- All route handlers are `async def` — uses `coodie.aio` API (`save()`, `delete()`, `find_one()`, `all()`)
- FastAPI request/response models re-use `Document` subclasses (Pydantic serialisation free)
- `404` from `DocumentNotFound`; `409` from `MultipleDocumentsFound`

### Files
```
demo/
├── README.md          # docker run scylladb/scylla + uvicorn startup instructions
├── requirements.txt   # fastapi, uvicorn[standard], coodie (local path)
├── models.py          # Product, Review document definitions
└── main.py            # FastAPI app with lifespan, routes, error handlers
```

---

## Implementation Order

Steps are sequential; each passes tests before the next begins.

1. Phase 0 — remaining Copilot skill files
2. Phase 1a — delete old code; strip cqlengine imports
3. Phase 1b — `schema.py` + `test_schema.py`
4. Phase 1b — `types.py` rewrite + update `test_types.py`
5. Phase 1b — `cql_builder.py` + `test_cql_builder.py`
6. Phase 1c — all four `drivers/` files + `test_drivers.py`
7. Phase 1d — `coodie.sync` subpackage (`document.py`, `query.py`) + `tests/sync/`
8. Phase 1d — `coodie.aio` subpackage (`document.py`, `query.py`) + `tests/aio/`
9. Phase 2 — `test_api_parity.py`; finalize `pyproject.toml` changes
10. Phase 3 — testcontainers fixtures + `test_integration.py` (both sync and async test classes)
11. Phase 4 — `test-unit.yml`, `test-integration.yml`, update `ci.yml`
12. Phase 5 — FastAPI demo app (uses `coodie.aio`)
13. Full test run; code review; CodeQL scan
