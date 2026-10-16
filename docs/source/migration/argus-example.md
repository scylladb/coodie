# Real-World Example: scylladb/argus

[Argus](https://github.com/scylladb/argus) is ScyllaDB's test-run tracking
system — a production application with users, test runs, events,
notifications, and comments. It ran on cqlengine from 2021 until 2026, when
it moved to coodie: first the models
([argus#1058](https://github.com/scylladb/argus/pull/1058)), then the
service layer to `coodie.aio`
([argus#1106](https://github.com/scylladb/argus/pull/1106)). Argus is
coodie's first production user.

Below is a walkthrough of migrating its key models and operations, showing
the cqlengine version next to the coodie one. The models are simplified for
readability; see the Argus repository for the real code.

## Models

### User — secondary indexes, list column, defaults

**cqlengine:**

```python
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
import uuid
from datetime import datetime, timezone

class ArgusUser(Model):
    __table_name__ = "argus_user"
    __keyspace__ = "argus"

    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    username = columns.Text(index=True)
    full_name = columns.Text()
    email = columns.Text(index=True)
    registration_date = columns.DateTime(default=lambda: datetime.now(timezone.utc))
    roles = columns.List(value_type=columns.Text)
    picture_id = columns.UUID()
    api_token = columns.Text(index=True)
```

**coodie:**

```python
from coodie.sync import Document
from coodie.fields import PrimaryKey, Indexed
from pydantic import Field
from typing import Annotated, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

class ArgusUser(Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    username: Annotated[str, Indexed()] = ""
    full_name: str = ""
    email: Annotated[str, Indexed()] = ""
    registration_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    roles: list[str] = Field(default_factory=list)
    picture_id: Optional[UUID] = None
    api_token: Annotated[Optional[str], Indexed()] = None

    class Settings:
        name = "argus_user"
        keyspace = "argus"
```

What changed:

- `columns.UUID(primary_key=True, default=uuid.uuid4)` →
  `Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)`
- `columns.Text(index=True)` → `Annotated[str, Indexed()]`
- `columns.List(value_type=columns.Text)` → `list[str]`
- `columns.UUID()` (nullable) → `Optional[UUID] = None`
- `columns.DateTime(default=...)` →
  `datetime = Field(default_factory=...)`
- `__table_name__` / `__keyspace__` → `Settings` inner class

### TestRun — composite partition key, clustering order, many indexes

**cqlengine:**

```python
class ArgusTestRun(Model):
    __table_name__ = "argus_test_run"
    __keyspace__ = "argus"

    build_id = columns.Text(primary_key=True, partition_key=True)
    start_time = columns.DateTime(
        primary_key=True,
        clustering_order="DESC",
        default=lambda: datetime.now(timezone.utc),
    )
    id = columns.UUID(index=True, default=uuid.uuid4)
    release_id = columns.UUID(index=True)
    group_id = columns.UUID(index=True)
    test_id = columns.UUID(index=True)
    assignee = columns.UUID(index=True)
    status = columns.Text(default=lambda: "created")
    investigation_status = columns.Text(default=lambda: "not_investigated")
    heartbeat = columns.Integer(default=lambda: 0)
    end_time = columns.DateTime()
    build_job_url = columns.Text()
    scylla_version = columns.Text()
```

**coodie:**

```python
from coodie.fields import PrimaryKey, ClusteringKey, Indexed

class ArgusTestRun(Document):
    build_id: Annotated[str, PrimaryKey()]
    start_time: Annotated[datetime, ClusteringKey(order="DESC")] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)
    release_id: Annotated[Optional[UUID], Indexed()] = None
    group_id: Annotated[Optional[UUID], Indexed()] = None
    test_id: Annotated[Optional[UUID], Indexed()] = None
    assignee: Annotated[Optional[UUID], Indexed()] = None
    status: str = "created"
    investigation_status: str = "not_investigated"
    heartbeat: int = 0
    end_time: Optional[datetime] = None
    build_job_url: Optional[str] = None
    scylla_version: Optional[str] = None

    class Settings:
        name = "argus_test_run"
        keyspace = "argus"
```

What changed:

- `primary_key=True, partition_key=True` → `PrimaryKey()`
- `primary_key=True, clustering_order="DESC"` → `ClusteringKey(order="DESC")`
- `columns.UUID(index=True)` → `Annotated[Optional[UUID], Indexed()]`
- `columns.Integer(default=lambda: 0)` → `int = 0`
- `columns.Text(default=lambda: "created")` → `str = "created"`

### Notification — partition + TimeUUID clustering

**cqlengine:**

```python
class ArgusNotification(Model):
    __table_name__ = "argus_notification"
    __keyspace__ = "argus"

    receiver = columns.UUID(primary_key=True, partition_key=True)
    id = columns.TimeUUID(primary_key=True, clustering_order="DESC", default=uuid.uuid1)
    type = columns.Text()
    state = columns.Integer(default=lambda: 0)
    sender = columns.UUID()
    source_type = columns.Text()
    source_id = columns.UUID()
    title = columns.Text()
    content = columns.Text()
```

**coodie:**

```python
from coodie.fields import PrimaryKey, ClusteringKey, TimeUUID
from uuid import uuid1

class ArgusNotification(Document):
    receiver: Annotated[UUID, PrimaryKey()]
    id: Annotated[UUID, TimeUUID(), ClusteringKey(order="DESC")] = Field(
        default_factory=uuid1
    )
    type: str = ""
    state: int = 0
    sender: Optional[UUID] = None
    source_type: str = ""
    source_id: Optional[UUID] = None
    title: str = ""
    content: str = ""

    class Settings:
        name = "argus_notification"
        keyspace = "argus"
```

What changed:

- `columns.TimeUUID(primary_key=True, clustering_order="DESC")` →
  `Annotated[UUID, TimeUUID(), ClusteringKey(order="DESC")]` — markers
  compose inside `Annotated`
- `columns.UUID(primary_key=True, partition_key=True)` → `Annotated[UUID, PrimaryKey()]`

### Event — UUID partition, multiple indexes

**cqlengine:**

```python
class ArgusEvent(Model):
    __table_name__ = "argus_event"
    __keyspace__ = "argus"

    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    release_id = columns.UUID(index=True)
    group_id = columns.UUID(index=True)
    test_id = columns.UUID(index=True)
    run_id = columns.UUID(index=True)
    user_id = columns.UUID(index=True)
    kind = columns.Text(index=True)
    body = columns.Text()
    created_at = columns.DateTime(default=lambda: datetime.now(timezone.utc))
```

**coodie:**

```python
class ArgusEvent(Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    release_id: Annotated[Optional[UUID], Indexed()] = None
    group_id: Annotated[Optional[UUID], Indexed()] = None
    test_id: Annotated[Optional[UUID], Indexed()] = None
    run_id: Annotated[Optional[UUID], Indexed()] = None
    user_id: Annotated[Optional[UUID], Indexed()] = None
    kind: Annotated[str, Indexed()] = ""
    body: str = ""
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "argus_event"
        keyspace = "argus"
```

What changed:

- Six `columns.UUID(index=True)` fields → `Annotated[Optional[UUID], Indexed()]`
- `columns.Text(index=True)` → `Annotated[str, Indexed()]`

### Comment — BigInt clustering, Map and List collections

**cqlengine:**

```python
class ArgusComment(Model):
    __table_name__ = "argus_comment"
    __keyspace__ = "argus"

    id = columns.UUID(primary_key=True, partition_key=True, default=uuid.uuid4)
    test_run_id = columns.UUID(index=True)
    user_id = columns.UUID(index=True)
    release_id = columns.UUID(index=True)
    posted_at = columns.BigInt(primary_key=True, clustering_order="DESC")
    message = columns.Text()
    mentions = columns.List(value_type=columns.UUID, default=[])
    reactions = columns.Map(key_type=columns.Text, value_type=columns.Integer)
```

**coodie:**

```python
from coodie.fields import PrimaryKey, ClusteringKey, Indexed, BigInt

class ArgusComment(Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    test_run_id: Annotated[Optional[UUID], Indexed()] = None
    user_id: Annotated[Optional[UUID], Indexed()] = None
    release_id: Annotated[Optional[UUID], Indexed()] = None
    posted_at: Annotated[int, BigInt(), ClusteringKey(order="DESC")] = 0
    message: str = ""
    mentions: list[UUID] = Field(default_factory=list)
    reactions: dict[str, int] = Field(default_factory=dict)

    class Settings:
        name = "argus_comment"
        keyspace = "argus"
```

What changed:

- `columns.BigInt(primary_key=True, clustering_order="DESC")` →
  `Annotated[int, BigInt(), ClusteringKey(order="DESC")]`
- `columns.List(value_type=columns.UUID, default=[])` →
  `list[UUID] = Field(default_factory=list)`
- `columns.Map(key_type=columns.Text, value_type=columns.Integer)` →
  `dict[str, int] = Field(default_factory=dict)`

## Operations

### Connection and table setup

**cqlengine:**

```python
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table

connection.setup(["127.0.0.1"], "argus", protocol_version=4)
sync_table(ArgusUser)
sync_table(ArgusTestRun)
sync_table(ArgusNotification)
sync_table(ArgusComment)
```

**coodie:**

```python
from coodie.sync import init_coodie

init_coodie(hosts=["127.0.0.1"], keyspace="argus")
ArgusUser.sync_table()
ArgusTestRun.sync_table()
ArgusNotification.sync_table()
ArgusComment.sync_table()
```

### Get-or-create user

**cqlengine:**

```python
try:
    user = ArgusUser.get(id=user_id)
except ArgusUser.DoesNotExist:
    user = ArgusUser.create(
        id=user_id,
        username="alice",
        email="alice@example.com",
        roles=["ROLE_USER"],
    )
```

**coodie:**

```python
from coodie.exceptions import DocumentNotFound

try:
    user = ArgusUser.get(id=user_id)
except DocumentNotFound:
    user = ArgusUser(
        id=user_id,
        username="alice",
        email="alice@example.com",
        roles=["ROLE_USER"],
    )
    user.save()
```

### Query latest test runs (partition + limit)

**cqlengine:**

```python
runs = list(
    ArgusTestRun.filter(build_id="nightly-x86")
    .limit(10)
    .all()
)
```

**coodie:**

```python
runs = ArgusTestRun.find(build_id="nightly-x86").limit(10).all()
```

### Status update (read-modify-save)

**cqlengine:**

```python
runs = list(ArgusTestRun.filter(build_id="nightly-x86").limit(1).all())
run = runs[0]
run.status = "running"
run.heartbeat = int(time.time())
run.save()
```

**coodie:**

```python
run = ArgusTestRun.find(build_id="nightly-x86").limit(1).all()[0]
run.update(status="running", heartbeat=int(time.time()))
```

### Batch event creation

**cqlengine:**

```python
from cassandra.cqlengine.query import BatchQuery

with BatchQuery() as b:
    for event_data in events:
        ArgusEvent.batch(b).create(
            release_id=release_id,
            run_id=run_id,
            user_id=event_data["user"],
            kind="STATUS_CHANGE",
            body=event_data["body"],
        )
```

**coodie:**

```python
from coodie.sync import BatchQuery

with BatchQuery() as batch:
    for event_data in events:
        evt = ArgusEvent(
            release_id=release_id,
            run_id=run_id,
            user_id=event_data["user"],
            kind="STATUS_CHANGE",
            body=event_data["body"],
        )
        evt.save(batch=batch)
```

### Notification feed (time-ordered partition read)

**cqlengine:**

```python
notifications = list(
    ArgusNotification.filter(receiver=user_id)
    .limit(20)
    .all()
)
```

**coodie:**

```python
notifications = (
    ArgusNotification.find(receiver=user_id)
    .limit(20)
    .all()
)
```

### Comment with collections

**cqlengine:**

```python
ArgusComment.create(
    test_run_id=run_id,
    user_id=user_id,
    release_id=release_id,
    posted_at=int(time.time() * 1000),
    message="Investigating flaky test.",
    mentions=[reviewer_id, assignee_id],
    reactions={"+1": 3, "eyes": 1},
)
```

**coodie:**

```python
comment = ArgusComment(
    test_run_id=run_id,
    user_id=user_id,
    release_id=release_id,
    posted_at=int(time.time() * 1000),
    message="Investigating flaky test.",
    mentions=[reviewer_id, assignee_id],
    reactions={"+1": 3, "eyes": 1},
)
comment.save()
```
