# Sync vs Async API

coodie provides two parallel APIs with identical functionality:

- **`coodie.sync`** — synchronous (blocking) API
- **`coodie.aio`** — asynchronous (async/await) API

Both share the same schema definitions, field types, and CQL builder.
The only difference is whether database calls block the current thread
or yield to the event loop.

## Side-by-Side Comparison

### Initialization

```python
# === Sync ===
from coodie.sync import Document, init_coodie

init_coodie(hosts=["127.0.0.1"], keyspace="my_ks")

# === Async ===
from coodie.aio import Document, init_coodie

await init_coodie(hosts=["127.0.0.1"], keyspace="my_ks")
```

### Defining Models

Models are defined the same way — the `Document` base class comes from
different modules, but the field annotations are identical:

```python
from coodie.fields import PrimaryKey
from typing import Annotated
from uuid import UUID, uuid4
from pydantic import Field

class User(Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    email: str

    class Settings:
        name = "users"
```

### Schema Sync

```python
User.sync_table()                # sync
await User.sync_table()          # async
```

### CRUD Operations

```python
# --- Create ---
user = User(name="Alice", email="alice@example.com")
user.save()                      # sync
await user.save()                # async

# --- Read ---
user = User.get(id=some_id)             # sync
user = await User.get(id=some_id)       # async

# --- Update ---
user.update(name="Bob")                 # sync
await user.update(name="Bob")           # async

# --- Delete ---
user.delete()                    # sync
await user.delete()              # async
```

### Querying

```python
# --- Find all ---
users = User.find(name="Alice").all()            # sync
users = await User.find(name="Alice").all()      # async

# --- Count ---
n = User.find().count()                          # sync
n = await User.find().count()                    # async

# --- Create via QuerySet ---
User.find().create(name="Carol", email="carol@example.com")       # sync
await User.find().create(name="Carol", email="carol@example.com") # async
```

### Batches

```python
# --- Sync ---
from coodie.sync import BatchQuery

with BatchQuery() as batch:
    user1.save(batch=batch)
    user2.save(batch=batch)

# --- Async ---
from coodie.aio import AsyncBatchQuery

async with AsyncBatchQuery() as batch:
    await user1.save(batch=batch)
    await user2.save(batch=batch)
```

### Raw CQL

```python
from coodie.sync import execute_raw
rows = execute_raw("SELECT * FROM users WHERE id = ?", [some_id])

from coodie.aio import execute_raw
rows = await execute_raw("SELECT * FROM users WHERE id = ?", [some_id])
```

### Keyspace Management

```python
# --- Sync ---
from coodie.sync import create_keyspace, drop_keyspace
create_keyspace("my_ks", replication_factor=3)
drop_keyspace("my_ks")

# --- Async ---
from coodie.aio import create_keyspace, drop_keyspace
await create_keyspace("my_ks", replication_factor=3)
await drop_keyspace("my_ks")
```

## What's Shared

Both APIs share these modules — no separate sync/async versions needed:

| Module | Purpose |
|--------|---------|
| `coodie.fields` | `PrimaryKey`, `ClusteringKey`, `Counter`, `Frozen`, `Indexed` |
| `coodie.types` | Custom CQL type mappings |
| `coodie.schema` | Schema introspection (`build_schema`) |
| `coodie.cql_builder` | CQL generation functions |
| `coodie.results` | `LWTResult`, `PagedResult` |
| `coodie.exceptions` | All exception classes |

## API Reference

| Feature | `coodie.sync` | `coodie.aio` |
|---------|--------------|--------------|
| Document | `Document` | `Document` |
| CounterDocument | `CounterDocument` | `CounterDocument` |
| MaterializedView | `MaterializedView` | `MaterializedView` |
| QuerySet | `QuerySet` | `QuerySet` |
| Batch | `BatchQuery` | `AsyncBatchQuery` (or `BatchQuery` with `async with`) |
| Init | `init_coodie()` | `init_coodie()` (async) |
| Raw CQL | `execute_raw()` | `execute_raw()` (async) |
| Create keyspace | `create_keyspace()` | `create_keyspace()` (async) |
| Drop keyspace | `drop_keyspace()` | `drop_keyspace()` (async) |

## When to Use Which

| Scenario | Recommendation |
|----------|----------------|
| **FastAPI / aiohttp / Starlette** | `coodie.aio` — these frameworks are async-native |
| **Flask / Django (without async views)** | `coodie.sync` — blocking calls match the request model |
| **Scripts and CLI tools** | `coodie.sync` — simpler, no event loop to manage |
| **High-concurrency I/O** | `coodie.aio` — concurrent queries without threads |
| **Jupyter notebooks** | Either — notebooks support `await` natively |

## Using Both Modes on One Model

Every model supports both modes, whichever base class it uses. The base
class only picks what the un-suffixed names (`save()`, `get()`, `all()`, ...)
do. Each I/O method also exists as an explicit `*_sync` and `*_async` twin:

```python
from coodie.aio import Document   # default mode: async

class User(Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str

user = User(name="Alice")
await user.save()             # default mode
await user.save_async()       # always async
user.save_sync()              # always sync: same object, same table

users = User.find(name="Alice").all_sync()
n = await User.find().count_async()

for u in User.find(): ...         # `for` is always sync
async for u in User.find(): ...   # `async for` is always async
```

`BatchQuery` works with both `with` and `async with`, so one batch can hold
writes from either mode.

To set an application-wide default, define an abstract base once:

```python
from coodie.sync import Document

class Model(Document):
    class Settings:
        __abstract__ = True

class User(Model): ...    # user.save() is sync; await user.save_async() also works
```

### Overriding methods

Override the explicit twins. The un-suffixed alias calls them, so the
override applies in both modes:

```python
class User(Document):
    def save_sync(self, **kw):
        self.touch()
        return super().save_sync(**kw)

    async def save_async(self, **kw):
        self.touch()
        return await super().save_async(**kw)
```

Models that override only the un-suffixed `save()` keep working as before.
If such a model then calls `save_sync()` / `save_async()` directly, which
skips that override, coodie emits a `UserWarning`.

### Blocking calls inside an event loop

On an async-default model, a `*_sync` call made while an event loop is
running blocks the loop, and coodie emits
{class}`~coodie.exceptions.BlockingCallWarning`. Use the `*_async` twin there.
To silence it, or to turn it into an error in tests, use the standard
`warnings` filters:

```python
import warnings
from coodie.exceptions import BlockingCallWarning

warnings.simplefilter("error", BlockingCallWarning)
```

Sync-default models don't emit this warning, so existing `coodie.sync` code
is unaffected.

```{note}
`AcsyllaDriver(session=...)` built from a session you created yourself is
async-only. Use `init_coodie(hosts=...)` or `init_coodie_async(hosts=...)`
for an Acsylla driver that supports both modes.
```

## What's Next?

- {doc}`drivers` — driver configuration and multi-cluster setups
- {doc}`batch-operations` — batch multiple statements into one round-trip
- {doc}`lwt` — conditional writes with IF NOT EXISTS / IF EXISTS
- {doc}`exceptions` — error handling patterns
