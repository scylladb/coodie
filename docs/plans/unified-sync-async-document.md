# Unified Sync/Async Document Plan

> **Goal:** One model class supports both the sync and the async API, on the
> same instance. Users pick a default mode once. The other mode is always one
> explicit method name away, with no extra classes or boilerplate.
>
> **Hard requirement:** no breaking change. Every existing import, class,
> method name, signature and return type keeps working exactly as today, and
> code that only uses today's API sees no new warnings or errors.

---

## 1. The Problem

coodie ships two parallel model hierarchies: `coodie.sync.Document` and
`coodie.aio.Document` (and likewise `QuerySet`, `CounterDocument`,
`MaterializedView`, `BatchQuery` / `AsyncBatchQuery`). A model is either sync
or async, never both.

Python allows only one method per name, so a class can't have both a blocking
`save()` and an `async def save()`. Everything under the model is already
shared: the schema, the CQL builder, the driver registry, and every driver
implements both `execute()` and `execute_async()`. Only the model layer forces
a choice.

That hurts users who need both, which is common. Examples are an async web app
that also has sync scripts, CLI tools, migrations, Celery tasks or tests. Today
the cleanest way is a hand-written shared-fields mixin that nobody would guess:

```python
class UserFields(BaseModel):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""

class UserSettings:
    name = "users"
    keyspace = "ks"

class User(UserFields, coodie.sync.Document):
    class Settings(UserSettings): pass

class AsyncUser(UserFields, coodie.aio.Document):
    class Settings(UserSettings): pass
```

That's three classes per model, and instances can't move between them without
`AsyncUser.model_validate(user.model_dump())`.

---

## 2. Proposed Solution

Every model supports both modes. Each I/O method exists under three names:

| Name | Behaviour |
|---|---|
| `save_sync(...)` | Always blocking |
| `save_async(...)` | Always a coroutine |
| `save(...)` | Follows the class's **default mode** |

The same model now looks like this:

```python
class User(coodie.Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""

    class Settings:
        name = "users"
        keyspace = "ks"
```

### 2.1 Using both modes on one object

```python
user = User(name="alice")

await user.save()            # default mode (async for coodie.Document)
await user.save_async()      # explicitly async
user.save_sync()             # explicitly sync: same object, same table

user = User.get_sync(id=uid)
await user.update_async(name="bob")
await user.delete_async()
```

### 2.2 Queries

Chain builders (`filter`, `limit`, `order_by`, …) don't do I/O and have a single
name. Terminal methods get the three names. Iteration needs no suffix, because
`for` vs `async for` already says which mode is meant.

```python
qs = User.find(name="alice").limit(10)

rows = await qs.all()          # default
rows = qs.all_sync()           # explicit sync
n    = await qs.count_async()  # explicit async

for u in qs: ...               # always sync
async for u in qs: ...         # always async
```

### 2.3 Batches

One `BatchQuery` class works with both context-manager protocols:

```python
with BatchQuery() as batch:
    user.save(batch=batch)

async with BatchQuery() as batch:
    user.save(batch=batch)
```

`AsyncBatchQuery` stays as an alias for compatibility.

### 2.4 Choosing the default mode

The default mode comes from the base class:

| Base class | `save()` means |
|---|---|
| `coodie.Document` / `coodie.aio.Document` | `save_async()` (same as today) |
| `coodie.sync.Document` | `save_sync()` (same as today) |

An application sets its default once, in its own abstract base:

```python
class Model(coodie.sync.Document):
    class Settings:
        __abstract__ = True

class User(Model): ...

user.save()                # sync, the app default
await user.save_async()    # still available
```

The base class is the configuration point, rather than a global flag, because
it's the only choice a type checker can follow. mypy and IDEs then show
`save()` as returning `None` or a coroutine correctly, per model.

### 2.5 Compatibility

Nothing existing changes. The new API is purely additive:

- `coodie.Document`, `coodie.sync.Document`, `coodie.aio.Document`,
  `CounterDocument`, `MaterializedView`, `QuerySet`, `BatchQuery`,
  `AsyncBatchQuery`, `init_coodie`, `execute_raw`, `create_keyspace` and
  `drop_keyspace` keep their import paths, names and signatures.
- `coodie.sync` users keep calling `save()`, and `coodie.aio` users keep
  calling `await save()`. Both just gain the `*_sync` / `*_async` twins.
- `issubclass(Model, coodie.sync.Document)` and
  `issubclass(Model, coodie.aio.Document)` still answer the same way: the
  two stay separate classes over one shared base.
- Existing models that override `save()` keep working as they do today.
- The new guards in [section 3](#3-pitfalls-and-how-the-design-handles-them)
  only fire when the *other* mode is used, so code using only today's API
  never sees them.

### 2.6 Overriding methods

Customise behaviour by overriding the explicit methods. The default-mode name
delegates to them, so the override applies everywhere:

```python
class User(coodie.Document):
    updated_at: datetime | None = None

    def save_sync(self, **kw):
        self.updated_at = datetime.now(UTC)
        return super().save_sync(**kw)

    async def save_async(self, **kw):
        self.updated_at = datetime.now(UTC)
        return await super().save_async(**kw)
```

### 2.7 Naming

Explicit methods use `*_sync` / `*_async` suffixes. They're symmetric, they
read clearly, and they match the driver API (`execute_async`,
`sync_table_async`). The one awkward name, `sync_table_sync()`, is accepted.

Django's `a` prefix (`asave()`, `aget()`, `aall()`) was considered and
rejected. It isn't obvious to readers who don't know Django, and it only names
the async side.

Libraries with the same suffix convention:

- [scylla-driver / cassandra-driver](https://github.com/scylladb/python-driver),
  which coodie wraps: `Session.execute()` / `Session.execute_async()`
- [stripe-python](https://github.com/stripe/stripe-python):
  `Customer.create()` / `Customer.create_async()` on the same resource classes
- [twilio-python](https://github.com/twilio/twilio-python):
  `client.messages.create()` / `create_async()`
- [Pydantic AI](https://ai.pydantic.dev/agents/): `Agent.run()` (async) /
  `Agent.run_sync()`, the async-default mirror of the same idea

---

## 3. Pitfalls and How the Design Handles Them

| Pitfall | Handling |
|---|---|
| Duplicated models, mixins, a forgotten `Settings` silently pointing at the wrong table | Gone: one class, one `Settings` |
| Converting instances between sync and async classes | Gone: one instance type |
| Forgetting `await` on an async call | Explicit names make the mode visible at the call site, and Python still warns "coroutine was never awaited" |
| A sync call inside a running event loop blocks the loop | On an async-default model, `*_sync` emits a `BlockingCallWarning` naming the `*_async` twin. Sync-default models behave exactly as today (no new warning). Users can silence or escalate it with the standard `warnings` filters. |
| Overriding `save()` only, then calling the other mode's twin skips the override | Warn when the bypassing twin is called, not when the class is defined, so existing models that override `save()` see nothing until they use the new API |

### Rejected alternatives

- **Auto-detect the mode** (return a coroutine when a loop is running): the
  return type depends on where it's called. Sync code inside an async app
  silently gets coroutines.
- **Global default-mode switch:** a type checker can't follow it, so `save()`
  would have to be typed `Any`.
- **Class keyword** (`class User(coodie.Document, mode="sync")`): this is the
  same configuration as picking the base class, but mypy can't read the
  keyword. The static type of `save()` would then come from the base and
  disagree with the runtime behaviour. Choosing `coodie.sync.Document` is
  just as short and is typed correctly.
- **Accessor namespaces** (`user.aio.save()`): these collide with user field
  names on a pydantic model.

---

## 4. Testing Focus

- **Main focus: one behavioural suite run in both modes.** Parametrize the
  model tests over mode (sync / async) instead of keeping two copied suites.
  The core property to protect is that both modes produce the same CQL and the
  same results. This also replaces today's API-parity check.
- **Back-compat:** the existing sync and async test suites must pass unchanged.
  That is the proof that current users aren't broken.
- **Integration tests mixing modes:** per driver, write in one mode and read in
  the other on the same model, in one process. This is where real driver and
  event-loop issues show up.
- **A small typing check** (mypy over a fixture file), since correct static
  types for `save()` are the reason for choosing the default by base class.
- Guard warnings and errors need only a few targeted unit tests.
