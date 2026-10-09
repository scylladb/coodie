# QuerySet & Chaining

`Document.find()` returns a `QuerySet` — a lazy query builder that
doesn't hit the database until you call a **terminal method** such as
`all()`, `first()`, or `count()`. Chain as many modifiers as you like
before executing.

## Setup

The examples below assume this Document definition:

```python
from coodie.fields import PrimaryKey, ClusteringKey, Indexed
from pydantic import Field
from typing import Annotated, Optional
from uuid import UUID, uuid4
from datetime import datetime

class BugReport(Document):
    project: Annotated[str, PrimaryKey()]
    created_at: Annotated[datetime, ClusteringKey(order="DESC")]
    title: str
    severity: Annotated[str, Indexed()] = "low"
    status: str = "open"
    assignee: Optional[str] = None

    class Settings:
        name = "bug_reports"
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

## Chainable Methods

Chainable methods return a new `QuerySet`, so you can stack them:

```python
qs = (
    BugReport.find(project="coodie")
    .filter(severity="critical")
    .order_by("-created_at")
    .limit(10)
    .allow_filtering()
)
```

### `filter(**kwargs)`

Add extra WHERE conditions. Supports Django-style lookups
(see {doc}`filtering` for the full list):

```python
qs = BugReport.find(project="coodie").filter(severity="critical")
```

### `limit(n)`

Cap the number of rows returned:

```python
qs = BugReport.find(project="coodie").limit(5)
```

### `per_partition_limit(n)`

Cap the number of rows **per partition**:

```python
qs = BugReport.find().per_partition_limit(3).allow_filtering()
```

### `order_by(*columns)`

Set the clustering order. Prefix a column name with `-` for descending:

```python
# Newest first (descending)
qs = BugReport.find(project="coodie").order_by("-created_at")

# Oldest first (ascending)
qs = BugReport.find(project="coodie").order_by("created_at")
```

```{warning}
`order_by` only works on clustering columns and must match or reverse
the table's declared clustering order.
```

### `only(*columns)` / `defer(*columns)`

Select a subset of columns:

```python
# Fetch only title and severity
qs = BugReport.find(project="coodie").only("title", "severity")

# Fetch everything except assignee
qs = BugReport.find(project="coodie").defer("assignee")
```

### `values_list(*columns)`

Return raw tuples instead of Document instances. This avoids the
overhead of constructing full Document objects and is useful when you
only need a few column values — for example, feeding data into a
report, building a quick lookup dict, or exporting rows:

```python
rows = BugReport.find(project="coodie").values_list("title", "severity").all()
# [("Crash on startup", "critical"), ...]
```

### `allow_filtering()`

Enable `ALLOW FILTERING` in the generated CQL. Use this when
Cassandra/ScyllaDB refuses a query because it would require a full
table scan:

```python
qs = BugReport.find(status="open").allow_filtering()
```

```{warning}
`ALLOW FILTERING` can be expensive on large tables. Prefer queries that
hit the partition key or a secondary index.
```

### `ttl(seconds)`

Set a TTL (time-to-live) for write operations (`create`, `update`).
The written cells will expire after the given number of seconds:

```python
qs = BugReport.find(project="coodie").ttl(3600)
```

See {doc}`ttl` for full details.

### `timestamp(ts)`

Set an explicit write timestamp (in **microseconds** since epoch) for
`create` or `update` operations. This overrides the server-assigned
timestamp and can be used for deterministic replays or conflict
resolution:

```python
import time

qs = BugReport.find(project="coodie").timestamp(int(time.time() * 1_000_000))
```

### `if_not_exists()` / `if_exists()`

Enable lightweight-transaction guards:

```python
# Insert only if row doesn't already exist
BugReport.find().if_not_exists().create(
    project="coodie", created_at=datetime.now(), title="New bug"
)

# Delete only if row exists
BugReport.find(project="coodie", created_at=some_dt).if_exists().delete()
```

### `consistency(level)`

Override the consistency level for this query. The `level` is a string
matching a `cassandra.ConsistencyLevel` attribute:

| Level | Description |
|-------|-------------|
| `"ONE"` | Response from one replica (fastest) |
| `"TWO"` | Response from two replicas |
| `"THREE"` | Response from three replicas |
| `"QUORUM"` | Majority of all replicas across all data centres |
| `"LOCAL_QUORUM"` | Majority of replicas in the local data centre |
| `"EACH_QUORUM"` | Quorum in each data centre (writes only) |
| `"ALL"` | All replicas must respond (slowest, highest consistency) |
| `"LOCAL_ONE"` | One replica in the local data centre |
| `"ANY"` | At least one node (writes only, includes hinted handoff) |
| `"SERIAL"` | For LWT reads — linearisable consistency |
| `"LOCAL_SERIAL"` | Like `SERIAL` but local data centre only |

```python
qs = BugReport.find(project="coodie").consistency("LOCAL_QUORUM")
```

### `timeout(seconds)`

Override the query timeout:

```python
qs = BugReport.find(project="coodie").timeout(5.0)
```

### `using(ttl=, timestamp=, consistency=, timeout=)`

Set multiple query options at once:

```python
qs = BugReport.find(project="coodie").using(
    ttl=3600, consistency="LOCAL_QUORUM", timeout=5.0
)
```

### `fetch_size(n)` / `page(paging_state)`

Control pagination:

```python
qs = BugReport.find(project="coodie").fetch_size(100)
```

### `distinct()`

Emit `SELECT DISTINCT`. CQL only allows partition key (and static)
columns here, so pair it with `only()`:

```python
projects = BugReport.find().only("project").distinct().values_list("project").all()
# [("coodie",), ("scylla",)]
```

### `group_by(*columns)`

Append a `GROUP BY` clause. CQL restricts grouping to the primary key
columns, in order (partition key first, then clustering columns). Without
aggregates, each group returns its first row:

```python
latest_per_project = BugReport.find(project__in=["coodie", "scylla"]).group_by("project").all()
```

### `cast(column, cql_type)`

Add `CAST("column" AS type)` to the selected columns. The cast value is
not a model field, so read it from the raw row via `all(lazy=True)`:

```python
rows = BugReport.find(project="coodie").only("project").cast("created_at", "date").all(lazy=True)
rows[0]._raw_data["cast(created_at as date)"]
```

### `is_not_null(column)` / `filter(col__isnull=False)`

Render a `"col" IS NOT NULL` restriction. ScyllaDB and Cassandra only accept
it in materialized view definitions — a plain `SELECT` is rejected by the
server. `is_null()` / `col__isnull=True` render `IS NULL`, which is not valid
CQL.

## Terminal Methods

Terminal methods execute the query. In async mode, `await` the call.

### `all()`

Execute the query and return a list of documents:

```python
bugs = BugReport.find(project="coodie").all()             # sync
bugs = await BugReport.find(project="coodie").all()        # async
```

### `paged_all()`

Like `all()`, but returns a `PagedResult` with a `paging_state` for
cursor-based pagination. When `paging_state` is `None`, there are no
more pages:

```python
from coodie.results import PagedResult

# Fetch the first page
result = BugReport.find(project="coodie").fetch_size(50).paged_all()
bugs = result.data              # list of documents for this page

# Fetch subsequent pages
while result.paging_state is not None:
    result = (
        BugReport.find(project="coodie")
        .fetch_size(50)
        .page(result.paging_state)
        .paged_all()
    )
    bugs.extend(result.data)
```

In async mode:

```python
result = await BugReport.find(project="coodie").fetch_size(50).paged_all()
while result.paging_state is not None:
    result = await (
        BugReport.find(project="coodie")
        .fetch_size(50)
        .page(result.paging_state)
        .paged_all()
    )
```

### `first()`

Return the first matching document, or `None`:

```python
bug = BugReport.find(project="coodie").first()             # sync
bug = await BugReport.find(project="coodie").first()        # async
```

### `count()`

Return the number of matching rows:

```python
total = BugReport.find(project="coodie").count()           # sync
total = await BugReport.find(project="coodie").count()      # async
```

### `sum()` / `avg()` / `min()` / `max()` / `aggregate()`

Run a CQL aggregate over the matching rows and return the scalar result:

```python
qs = BugReport.find(project="coodie")
qs.min("created_at")                                     # sync
await qs.max("created_at")                               # async

# Several aggregates at once, each as "func(column)"
qs.aggregate(first="min(created_at)", last="max(created_at)")
# {"first": datetime(...), "last": datetime(...)}
```

`sum()` and `avg()` work on numeric columns. Each aggregate is its own query.

### `create(**kwargs)`

Insert a new row. Combine with `if_not_exists()` for conditional
inserts:

```python
result = BugReport.find().if_not_exists().create(
    project="coodie",
    created_at=datetime.now(),
    title="New bug",
)
```

### `update(**kwargs)`

Bulk update matching rows:

```python
BugReport.find(project="coodie", created_at=some_dt).update(
    status="closed"
)
```

### `delete()`

Delete matching rows:

```python
BugReport.find(project="coodie", created_at=some_dt).delete()    # sync
await BugReport.find(project="coodie", created_at=some_dt).delete()  # async
```

## Iteration

### Sync

```python
for bug in BugReport.find(project="coodie").all():
    print(bug.title)
```

### Async

```python
async for bug in BugReport.find(project="coodie"):
    print(bug.title)
```

## What's Next?

- {doc}`filtering` — Django-style lookup operators for WHERE clauses
- {doc}`collections` — set, list, and map operations
- {doc}`ttl` — time-to-live support
- {doc}`counters` — counter tables and increment/decrement
