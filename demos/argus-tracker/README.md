# 🐙 coodie Argus-Style Test Tracker Demo

> *Dimension-13: The Panopticon Protocol* — ARGUS-PRIME, a thousand-eyed
> entity, tracks every CI/CD pipeline in every universe using composite
> partition keys, batch event ingestion, and TimeUUID notifications.

A runnable CLI demo showcasing **coodie**'s support for complex real-world
data models inspired by [scylladb/argus](https://github.com/scylladb/argus),
with [rich](https://rich.readthedocs.io/) progress bars and partition-scoped
query demonstrations.

## Features Demonstrated

| Feature | How It's Used |
|---|---|
| **Composite PK + Clustering** | `TestRun` partitions by `build_id`, clusters by `start_time DESC` |
| **Compound Partition Key** | `Event` partitions by `(run_id, kind)` — events grouped by run + category |
| **TimeUUID Clustering** | `Notification` uses `TimeUUID()` + `ClusteringKey(order="DESC")` for chronological feeds |
| **Batch Ingestion** | Logged batches for test runs, unlogged batches for events and notifications |
| **Prepared-Statement Caching** | coodie drivers automatically cache prepared statements; repeated inserts/queries reuse them |
| **Partition-Scoped Queries** | Queries by `build_id`, `(run_id, kind)`, and `receiver` — single-partition reads |
| **List/Map Collections** | `User.roles` (List), `TestRun.tags` (List), `Event.metadata` (Map) |
| **Secondary Indexes** | Multiple indexed columns on `User`, `TestRun`, and `Event` for flexible lookups |

## Quick Start

```bash
cd demos/argus-tracker
make seed
```

This single command starts ScyllaDB, creates the keyspace, and seeds the
tracker with 5 users, 20 test runs, 100 events, and notifications.

## Prerequisites

* Python ≥ 3.10
* [uv](https://docs.astral.sh/uv/) (recommended) or pip
* Docker & Docker Compose (for ScyllaDB)

## Step-by-Step

### 1. Start ScyllaDB and create keyspace

```bash
make db-up
```

### 2. Seed the test tracker

```bash
make seed                                   # defaults: 5 users, 20 runs, 100 events
uv run python seed.py --users 10            # 10 users
uv run python seed.py --runs 50             # 50 test runs
uv run python seed.py --events 500          # 500 events
uv run python seed.py --batch-size 10       # smaller batches
```

### 3. Run the smoke test

```bash
make test
```

### 4. Clean up

```bash
make clean
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SCYLLA_HOSTS` | `127.0.0.1` | Comma-separated ScyllaDB contact points |
| `SCYLLA_KEYSPACE` | `argus` | Keyspace to use |

## Makefile Targets

| Target | Description |
|---|---|
| `make db-up` | Start ScyllaDB and create the `argus` keyspace |
| `make db-down` | Stop ScyllaDB |
| `make seed` | Seed test tracker data (depends on `db-up`) |
| `make clean` | Stop DB and remove data volumes |
| `make test` | Run the smoke test |

## Models

### User

```python
class User(Document):
    id: Annotated[UUID, PrimaryKey()]
    username: Annotated[str, Indexed()]
    full_name: str
    email: Annotated[str, Indexed()]
    registration_date: datetime
    roles: List[str]                    # CQL list<text>
    picture_id: Optional[UUID]
    api_token: Annotated[Optional[str], Indexed()]
```

**Key pattern:** Single partition key (`id`), secondary indexes on `username`,
`email`, `api_token` for fast lookups.

### TestRun — Composite PK + Clustering

```python
class TestRun(Document):
    build_id: Annotated[str, PrimaryKey()]
    start_time: Annotated[datetime, ClusteringKey(order="DESC")]
    id: Annotated[UUID, Indexed()]
    release_id: Annotated[Optional[UUID], Indexed()]
    assignee: Annotated[Optional[UUID], Indexed()]
    status: Annotated[str, Indexed()]
    tags: List[str]                     # CQL list<text>
    ...
```

**Key pattern:** Partition by `build_id`, cluster by `start_time DESC`.
Query "latest run for build X" hits a single partition and returns the
most recent run first.

### Event — Compound Partition Key

```python
class Event(Document):
    run_id: Annotated[UUID, PrimaryKey(partition_key_index=0)]
    kind: Annotated[str, PrimaryKey(partition_key_index=1)]
    created_at: Annotated[datetime, ClusteringKey(order="DESC")]
    id: Annotated[UUID, Indexed()]
    severity: Annotated[str, Indexed()]
    metadata: Dict[str, str]            # CQL map<text, text>
    ...
```

**Key pattern:** Compound partition `(run_id, kind)` groups events by
category within a run.  Query "all errors for run X" is a single-partition
scan: `Event.find(run_id=..., kind="error")`.

### Notification — TimeUUID Clustering

```python
class Notification(Document):
    receiver: Annotated[UUID, PrimaryKey()]
    id: Annotated[UUID, TimeUUID(), ClusteringKey(order="DESC")]
    type: str
    state: int
    sender: Optional[UUID]
    ...
```

**Key pattern:** Partition by `receiver`, cluster by TimeUUID DESC.
TimeUUID guarantees chronological ordering even for sub-millisecond
inserts — ideal for notification feeds.

## Batch Ingestion Patterns

### Logged Batches (Test Runs)

```python
with BatchQuery(logged=True) as bq:
    for run in runs:
        TestRun(**run).save(batch=bq)
```

* **Atomic** — all-or-nothing; if one fails, none are applied
* **Use for** critical data where partial writes are unacceptable

### Unlogged Batches (Events & Notifications)

```python
with BatchQuery(logged=False) as bq:
    for event in events:
        Event(**event).save(batch=bq)
```

* **Best-effort** — maximum throughput, no atomicity guarantee
* **Use for** high-volume event streams and notification feeds

## Prepared-Statement Caching

coodie's CassandraDriver automatically caches prepared statements:

```python
# Internal driver behavior (no user action needed):
# First call:  session.prepare("INSERT INTO argus_events ...")  → cached
# Second call: reuse cached PreparedStatement                   → no re-prepare
```

Every `Document.save()` and `Document.find()` call benefits
from this cache.  The seed script's batch ingestion demonstrates this —
hundreds of inserts use the same prepared statement transparently.

## Partition-Scoped Queries

After ingestion, the seed script demonstrates efficient partition reads:

```python
# All runs for a build (single partition)
TestRun.find(build_id="scylla-oss/nightly/1234").all()

# All errors for a specific run (single partition)
Event.find(run_id=run_uuid, kind="error").all()

# All notifications for a user (single partition)
Notification.find(receiver=user_uuid).all()
```

These queries are the most efficient access pattern in Cassandra/ScyllaDB —
they hit exactly one partition on one node.

## Cleanup

```bash
make clean
```
