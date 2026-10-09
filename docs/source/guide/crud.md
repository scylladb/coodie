# CRUD Operations

This guide covers creating, reading, updating, and deleting documents.
All examples are shown in both **sync** and **async** forms.

## Setup

The examples below assume this Document definition:

```python
from coodie.fields import PrimaryKey, Indexed
from pydantic import Field
from typing import Annotated, Optional
from uuid import UUID, uuid4

class Task(Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    title: str
    status: Annotated[str, Indexed()] = "todo"
    assignee: Optional[str] = None
    priority: int = 0

    class Settings:
        name = "tasks"
```

For **sync** usage, import from `coodie.sync`:

```python
from coodie.sync import Document, init_coodie
init_coodie(hosts=["127.0.0.1"], keyspace="my_ks")
```

For **async** usage, import from `coodie.aio`:

```python
from coodie.aio import Document, init_coodie
await init_coodie(hosts=["127.0.0.1"], keyspace="my_ks")
```

Don't forget to sync the table first:

```python
Task.sync_table()          # sync
await Task.sync_table()    # async
```

## Create

### `save()` — Upsert

`save()` performs an INSERT with all fields. If a row with the same
primary key already exists, it is overwritten:

```python
task = Task(title="Write docs", status="in_progress", priority=1)
task.save()              # sync
await task.save()        # async
```

### `insert()` — Create Only

`insert()` uses `IF NOT EXISTS` under the hood. If the row already exists,
the insert is a no-op:

```python
task = Task(title="Deploy v2")
task.insert()            # sync
await task.insert()      # async
```

### With TTL

Both `save()` and `insert()` accept a `ttl` parameter (seconds until the
row expires):

```python
# Row expires after 1 hour
task.save(ttl=3600)
task.insert(ttl=3600)
```

## Read

### `get()` — Fetch One (or Raise)

`get()` fetches a single document by primary key. Raises
`DocumentNotFound` if no row matches:

```python
from coodie.exceptions import DocumentNotFound

try:
    task = Task.get(id=some_uuid)              # sync
    # task = await Task.get(id=some_uuid)      # async
    print(task.title)
except DocumentNotFound:
    print("Task not found")
```

### `find_one()` — Fetch One (or None)

`find_one()` returns `None` instead of raising an exception:

```python
task = Task.find_one(id=some_uuid)             # sync
# task = await Task.find_one(id=some_uuid)     # async
if task:
    print(task.title)
```

### `find()` — Query Multiple

`find()` returns a `QuerySet` that you can chain and execute:

```python
# Sync
tasks = Task.find(status="todo").all()

urgent = (
    Task.find(status="todo")
    .filter(priority__gte=5)
    .order_by("-priority")
    .limit(10)
    .allow_filtering()
    .all()
)

# Async — same chain, just await the terminal method
tasks = await Task.find(status="todo").all()
```

#### Counting Results

```python
count = Task.find(status="todo").count()          # sync
count = await Task.find(status="todo").count()     # async
```

#### Async Iteration

```python
async for task in Task.find(status="todo"):
    print(task.title)
```

## Update

### `update()` — Partial Update

`update()` modifies specific fields on an existing document:

```python
task = Task.get(id=some_uuid)                  # sync
# task = await Task.get(id=some_uuid)          # async

task.update(status="done", assignee="Alice")   # sync
# await task.update(status="done", assignee="Alice")  # async
```

### With TTL

```python
task.update(ttl=7200, status="in_progress")
```

### Conditional Update (LWT)

Use `if_exists=True` to update only if the row exists:

```python
from coodie.results import LWTResult

result = task.update(if_exists=True, status="done")
if result and not result.applied:
    print("Row was already deleted")
```

Use `if_conditions` for custom conditions:

```python
result = task.update(
    if_conditions={"status": "in_progress"},
    status="done",
)
```

### Collection Updates

For set, list, and map columns, use special prefixes:

```python
# Add to a set
task.update(add__tags={"urgent"})

# Remove from a set
task.update(remove__tags={"stale"})

# Append to a list
task.update(append__comments="Fixed in v2")

# Prepend to a list
task.update(prepend__comments="IMPORTANT")
```

## Delete

### `delete()` — Remove a Row

```python
task = Task.get(id=some_uuid)         # sync
task.delete()

# task = await Task.get(id=some_uuid) # async
# await task.delete()
```

### Conditional Delete (LWT)

```python
result = task.delete(if_exists=True)
if result and not result.applied:
    print("Row was already gone")
```

### Bulk Delete via QuerySet

```python
Task.find(status="cancelled").delete()           # sync
await Task.find(status="cancelled").delete()      # async
```

### `truncate()` — Remove All Rows

Issue `TRUNCATE TABLE` to empty the table while keeping its schema. Handy
for test fixtures and data resets:

```python
Task.truncate()           # sync
await Task.truncate()     # async
```

## Counter Operations

`CounterDocument` instances use `increment()` and `decrement()` instead of
`save()`:

```python
from coodie.sync import CounterDocument
from coodie.fields import PrimaryKey, Counter

class PageHits(CounterDocument):
    url: Annotated[str, PrimaryKey()]
    hits: Annotated[int, Counter()]

PageHits.sync_table()

page = PageHits(url="/home")
page.increment(hits=1)
page.decrement(hits=1)
```

```{warning}
`save()` and `insert()` are not available on `CounterDocument`.
Only `increment()` and `decrement()` modify counter values.
```

## What's Next?

- {doc}`querying` — QuerySet chaining and terminal methods
- {doc}`filtering` — Django-style lookup operators for WHERE clauses
- {doc}`collections` — set, list, and map operations
- {doc}`counters` — counter tables and increment/decrement
- {doc}`ttl` — time-to-live support
