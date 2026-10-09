# Plan: cqlengine Missing-Feature Coverage

> **Goal:** Address the eight cqlengine features listed as "not available" in
> coodie.  This plan documents the current status of each feature, provides
> implementation guidance for genuinely missing items, and notes workarounds.

---

## Feature Status Overview

| # | cqlengine Feature | coodie Status | Action |
|---|---|---|---|
| 1 | User-Defined Types (UDT) | ✅ Implemented | Phase A — complete |
| 2 | Static columns | ❌ Missing | Phase B — small addition |
| 3 | `Model.create()` class method | ✅ Implemented | None — already exists |
| 4 | `__like` filter operator (SASI / SAI) | ✅ Implemented | None — already in parser |
| 5 | Token-range queries (`__token`) | ✅ Implemented | None — parser + WHERE builder |
| 6 | Per-model `__connection__` | ✅ Implemented | None — `Settings.connection` |
| 7 | `create_keyspace_network_topology()` | ✅ Implemented | None — `dc_replication_map` |
| 8 | Counter columns on regular models | ✅ Implemented | None — `CounterDocument` |

---

## Already-Implemented Features (No Code Changes Needed)

### 3. `Model.create()` class method

Both sync and async `Document` have a `create()` classmethod:

```python
# coodie.sync.document / coodie.aio.document
@classmethod
def create(cls, **kwargs) -> Document:
    doc = cls(**kwargs)
    doc.save()  # or `await doc.save()` in async
    return doc
```

**Usage:**

```python
user = User.create(id=uuid4(), name="Alice")          # sync
user = await User.create(id=uuid4(), name="Alice")     # async
```

### 4. `__like` filter operator

The `parse_filter_kwargs()` in `cql_builder.py` already includes `"like": "LIKE"`
in its operators dict (line 171).  This enables:

```python
# Filter with LIKE (requires SASI or SAI index on the column)
results = MyModel.find(name__like="prefix%").all()
```

### 5. Token-range queries

Token operators are defined in `parse_filter_kwargs()` (lines 173-178):
`token__gt`, `token__gte`, `token__lt`, `token__lte`.  `build_where_clause()`
generates `TOKEN("col") > ?` syntax.

```python
# Token-range scan
results = MyModel.find(id__token__gt=some_token).all()
```

### 6. Per-model `__connection__`

`Document._get_driver()` reads `Settings.connection` and passes it to
`get_driver(name=connection)`:

```python
class UserOnCluster2(Document):
    id: Annotated[UUID, PrimaryKey()]
    name: str

    class Settings:
        connection = "cluster2"   # ← routes to a named driver
```

### 7. `create_keyspace_network_topology()`

`build_create_keyspace()` accepts an optional `dc_replication_map` dict.
When provided, it automatically switches to `NetworkTopologyStrategy`:

```python
from coodie.sync import create_keyspace

# NetworkTopologyStrategy
create_keyspace("my_ks", dc_replication_map={"dc1": 3, "dc2": 2})

# SimpleStrategy (default)
create_keyspace("my_ks", replication_factor=3)
```

### 8. Counter columns

`CounterDocument` (sync + async) provides `increment()` / `decrement()`.
Schema validation in `build_schema()` enforces that counter tables only have
counter + primary-key columns.

```python
from coodie.sync import CounterDocument

class PageViews(CounterDocument):
    url: Annotated[str, PrimaryKey()]
    view_count: Annotated[int, Counter()]

page = PageViews(url="/home", view_count=0)
page.increment(view_count=1)
page.decrement(view_count=1)
```

---

## Phase A: User-Defined Types (UDT) — ✅ Complete

**Priority:** Medium
**Effort:** Large (new module, type system changes, serialization)
**Status:** ✅ Implemented in `src/coodie/usertype.py`

Completed tasks:

| Task | Description | Status |
|---|---|---|
| A.1 | Create `coodie.usertype` module with `UserType(BaseModel)` base class | ✅ |
| A.2 | Add `__type_name__` override (default: snake_case of class name) | ✅ |
| A.3 | Add `build_create_type()` / `build_drop_type()` / `build_alter_type_add()` to `cql_builder.py` | ✅ |
| A.4 | Add `sync_type()` classmethod to `UserType` (sync + async) | ✅ |
| A.5 | Register UDT types in `python_type_to_cql_type_str()` → emit `frozen<type_name>` | ✅ |
| A.6 | Support UDTs inside collections (`list[MyUDT]` → `list<frozen<my_udt>>`) | ✅ |
| A.7 | Support nested UDTs with recursive depth-first dependency resolution | ✅ |
| A.8 | Serialization/deserialization via Pydantic `model_dump()`/`model_validate()` | ✅ |
| A.9 | Register UDT with driver (e.g. `cluster.register_user_type()`) | ❌ Future |
| A.10 | Unit + integration tests | ✅ Unit (46 tests); integration pending |

Remaining work for future PRs:
- **Driver registration** (A.9): `cluster.register_user_type()` for native UDT handling
- **Integration tests**: Full round-trip with real ScyllaDB
- **Auto-sync in sync_table()**: Auto-sync UDTs referenced by a Document before table creation
- **ALTER TYPE ADD**: Detect new fields and alter existing types

---

## Phase B: Static Columns — Implementing Now

**Priority:** High
**Effort:** Small (new marker, schema change, CQL builder change)

Static columns in CQL are shared across all rows within a partition.
They are declared with the `STATIC` keyword in `CREATE TABLE`.

### Tasks

| Task | Description | File |
|---|---|---|
| B.1 | Add `Static` dataclass marker | `src/coodie/fields.py` |
| B.2 | Add `static` field to `ColumnDefinition` | `src/coodie/schema.py` |
| B.3 | Handle `Static` marker in `build_schema()` | `src/coodie/schema.py` |
| B.4 | Emit `STATIC` keyword in `build_create_table()` | `src/coodie/cql_builder.py` |
| B.5 | Export `Static` from `coodie.__init__` and `coodie.fields` | `src/coodie/__init__.py` |
| B.6 | Add unit tests | `tests/test_schema.py`, `tests/test_cql_builder.py` |

### Usage

```python
from coodie.sync import Document
from coodie.fields import PrimaryKey, ClusteringKey, Static

class SensorReading(Document):
    sensor_id: Annotated[str, PrimaryKey()]
    reading_time: Annotated[str, ClusteringKey()]
    sensor_name: Annotated[str, Static()]    # shared across partition
    value: float

    class Settings:
        keyspace = "iot"
```

This generates:

```sql
CREATE TABLE IF NOT EXISTS iot.sensor_reading (
    "sensor_id" text,
    "reading_time" text,
    "sensor_name" text STATIC,
    "value" float,
    PRIMARY KEY ("sensor_id", "reading_time")
)
```

---

## References

- Existing feature-parity plan: `docs/plans/cqlengine-feature-parity.md`
- CQL `STATIC` column docs: https://cassandra.apache.org/doc/latest/cql/ddl.html
- CQL UDT docs: https://cassandra.apache.org/doc/latest/cql/types.html#udts
