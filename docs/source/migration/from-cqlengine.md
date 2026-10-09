# Migrating from cqlengine

This guide walks you through converting a `cassandra.cqlengine` application
to **coodie**. coodie replaces cqlengine's custom column classes with standard
Python type annotations and Pydantic v2, giving you validation, serialisation,
and first-class async support out of the box.

## Core Concepts Mapping

| cqlengine | coodie | Notes |
|---|---|---|
| `from cassandra.cqlengine.models import Model` | `from coodie.sync import Document` (sync) or `from coodie.aio import Document` (async) | — |
| `from cassandra.cqlengine import columns` | `from typing import Annotated` + `from coodie.fields import PrimaryKey, ClusteringKey, Indexed, Counter` | Use Python type annotations |
| `from cassandra.cqlengine import connection` | `from coodie.sync import init_coodie` or `from coodie.aio import init_coodie` | — |
| `from cassandra.cqlengine.management import sync_table` | `Document.sync_table()` | Called on the class itself |

## Model Definition

### cqlengine

```python
import uuid
from datetime import datetime, timezone
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Product(Model):
    __table_name__ = "products"
    __keyspace__ = "catalog"
    __default_ttl__ = 86400                         # table-level TTL (seconds)
    __options__ = {"gc_grace_seconds": 864000}       # table options

    # — keys —
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    category = columns.Text(primary_key=True, partition_key=True)
    created_at = columns.DateTime(
        primary_key=True,
        clustering_order="DESC",
        default=lambda: datetime.now(timezone.utc),
    )

    # — scalar types —
    name = columns.Text(required=True)
    sku = columns.Ascii()
    price = columns.Float()
    weight = columns.Double()
    quantity = columns.Integer()
    total_sold = columns.BigInt(default=lambda: 0)
    rating = columns.SmallInt()
    flags = columns.TinyInt()
    is_active = columns.Boolean(default=lambda: True)
    cost = columns.Decimal()

    # — temporal / binary / network —
    revision_id = columns.TimeUUID(default=uuid.uuid1)
    launch_date = columns.Date()
    description = columns.Text(required=False)
    thumbnail = columns.Blob()
    origin_ip = columns.Inet()

    # — indexed columns —
    brand = columns.Text(index=True)
    supplier = columns.Text(index=True)

    # — collections —
    tags = columns.List(columns.Text)
    warehouses = columns.Set(columns.Text)
    metadata = columns.Map(columns.Text, columns.Text)
    dimensions = columns.Tuple(columns.Float, columns.Float, columns.Float)
```

### coodie

```python
from datetime import date, datetime, timezone
from decimal import Decimal
from ipaddress import IPv4Address
from typing import Annotated, Optional
from uuid import UUID, uuid1, uuid4

from pydantic import Field
from coodie.sync import Document          # or coodie.aio for async
from coodie.fields import (
    Ascii, BigInt, ClusteringKey, Double, Indexed,
    PrimaryKey, SmallInt, TimeUUID, TinyInt,
)

class Product(Document):
    # — keys —
    id: Annotated[UUID, PrimaryKey(partition_key_index=0)] = Field(
        default_factory=uuid4
    )
    category: Annotated[str, PrimaryKey(partition_key_index=1)]
    created_at: Annotated[datetime, ClusteringKey(order="DESC")] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    # — scalar types —
    name: str
    sku: Annotated[str, Ascii()] = ""
    price: float = 0.0
    weight: Annotated[float, Double()] = 0.0
    quantity: int = 0
    total_sold: Annotated[int, BigInt()] = 0
    rating: Annotated[int, SmallInt()] = 0
    flags: Annotated[int, TinyInt()] = 0
    is_active: bool = True
    cost: Optional[Decimal] = None

    # — temporal / binary / network —
    revision_id: Annotated[UUID, TimeUUID()] = Field(default_factory=uuid1)
    launch_date: Optional[date] = None
    description: Optional[str] = None
    thumbnail: Optional[bytes] = None
    origin_ip: Optional[IPv4Address] = None

    # — indexed columns —
    brand: Annotated[str, Indexed()] = ""
    supplier: Annotated[str, Indexed()] = ""

    # — collections —
    tags: list[str] = Field(default_factory=list)
    warehouses: set[str] = Field(default_factory=set)
    metadata: dict[str, str] = Field(default_factory=dict)
    dimensions: Optional[tuple[float, float, float]] = None

    class Settings:
        name = "products"
        keyspace = "catalog"
        __default_ttl__ = 86400
        __options__ = {"gc_grace_seconds": 864000}
```

Key differences:

- **`Model` → `Document`** — inherit from `coodie.sync.Document` (or `coodie.aio.Document` for async).
- **`columns.*` → Python type annotations** — no special column classes needed.
- **`__table_name__` / `__keyspace__` → `Settings` inner class** — table metadata moves to a nested `Settings` class.
- **`required=True` → no default value** — a field without a default is required by Pydantic.
- **`required=False` → `Optional[T] = None`** — nullable fields use `Optional` with a `None` default.
- **`default=callable` → `Field(default_factory=callable)`** — Pydantic uses `Field(default_factory=...)` for callable defaults.
- **`columns.BigInt()` → `Annotated[int, BigInt()]`** — sub-types of `int` and `float` use `Annotated` markers.
- **`columns.TimeUUID()` → `Annotated[UUID, TimeUUID()]`** — `timeuuid` requires a marker on `UUID`.
- **`columns.Set(columns.Text)` → `set[str]`** — collections use native Python generics.
- **`columns.Tuple(...)` → `tuple[float, float, float]`** — tuples use standard tuple syntax.
- **Composite partition key** — use `PrimaryKey(partition_key_index=N)` to define multi-column partition keys.
- **Clustering order** — use `ClusteringKey(order="DESC")` instead of `clustering_order="DESC"`.
- **Table options** — `__default_ttl__` and `__options__` move into the `Settings` class.
- **Async is the same model** — only the import changes (`coodie.aio` instead of `coodie.sync`).

## Connection Setup

### cqlengine

```python
from cassandra.cqlengine import connection

connection.setup(["127.0.0.1"], "catalog", protocol_version=4)
```

### coodie (sync)

```python
from coodie.sync import init_coodie

init_coodie(hosts=["127.0.0.1"], keyspace="catalog")
```

### coodie (async)

```python
from coodie.aio import init_coodie

await init_coodie(hosts=["127.0.0.1"], keyspace="catalog")
```

## Table Sync

### cqlengine

```python
from cassandra.cqlengine.management import sync_table

sync_table(Product)
```

### coodie

```python
Product.sync_table()          # sync
await Product.sync_table()    # async
```

In coodie, `sync_table()` is a class method on the Document itself — no
separate management module needed.

## CRUD Operations

### Create / Insert

| Operation | cqlengine | coodie (sync) | coodie (async) |
|---|---|---|---|
| Upsert | `Product.create(id=..., name=...)` | `Product(id=..., name=...).save()` | `await Product(id=..., name=...).save()` |
| Insert if not exists | `Product.if_not_exists().create(...)` | `Product(...).insert()` | `await Product(...).insert()` |
| With TTL | `Product.ttl(60).create(...)` | `Product(...).save(ttl=60)` | `await Product(...).save(ttl=60)` |

### Read / Query

| Operation | cqlengine | coodie (sync) | coodie (async) |
|---|---|---|---|
| Get all | `Product.objects.all()` | `Product.find().all()` | `await Product.find().all()` |
| Filter | `Product.objects.filter(brand="Acme")` | `Product.find(brand="Acme").all()` | `await Product.find(brand="Acme").all()` |
| Get one | `Product.objects.get(id=pid)` | `Product.get(id=pid)` | `await Product.get(id=pid)` |
| Get one or None | `Product.objects.filter(id=pid).first()` | `Product.find_one(id=pid)` | `await Product.find_one(id=pid)` |
| Count | `Product.objects.count()` | `Product.find().count()` | `await Product.find().count()` |
| Limit | `Product.objects.all().limit(10)` | `Product.find().limit(10).all()` | `await Product.find().limit(10).all()` |
| Order by | `Product.objects.order_by("-created_at")` | `Product.find().order_by("-created_at").all()` | `await Product.find().order_by("-created_at").all()` |
| Allow filtering | `Product.objects.filter(price__gt=10).allow_filtering()` | `Product.find(price__gt=10).allow_filtering().all()` | `await Product.find(price__gt=10).allow_filtering().all()` |

### Update

| Operation | cqlengine | coodie (sync) | coodie (async) |
|---|---|---|---|
| Instance update | `product.name = "New"; product.save()` | `product.update(name="New")` | `await product.update(name="New")` |
| Bulk update | `Product.objects.filter(...).update(price=9.99)` | `Product.find(...).update(price=9.99)` | `await Product.find(...).update(price=9.99)` |

### Delete

| Operation | cqlengine | coodie (sync) | coodie (async) |
|---|---|---|---|
| Instance delete | `product.delete()` | `product.delete()` | `await product.delete()` |
| Bulk delete | `Product.objects.filter(...).delete()` | `Product.find(...).delete()` | `await Product.find(...).delete()` |

## Column Type Reference

| cqlengine | coodie (Python type annotation) |
|---|---|
| `columns.Text()` | `str` |
| `columns.Ascii()` | `Annotated[str, Ascii()]` |
| `columns.Integer()` | `int` |
| `columns.BigInt()` | `Annotated[int, BigInt()]` |
| `columns.SmallInt()` | `Annotated[int, SmallInt()]` |
| `columns.TinyInt()` | `Annotated[int, TinyInt()]` |
| `columns.VarInt()` | `Annotated[int, VarInt()]` |
| `columns.Float()` | `float` |
| `columns.Double()` | `Annotated[float, Double()]` |
| `columns.Decimal()` | `Decimal` |
| `columns.Boolean()` | `bool` |
| `columns.UUID(primary_key=True)` | `Annotated[UUID, PrimaryKey()]` |
| `columns.UUID()` | `UUID` |
| `columns.TimeUUID()` | `Annotated[UUID, TimeUUID()]` |
| `columns.DateTime()` | `datetime` |
| `columns.Date()` | `date` |
| `columns.Time()` | `Annotated[int, Time()]` |
| `columns.Blob()` | `bytes` |
| `columns.Inet()` | `IPv4Address` or `IPv6Address` |
| `columns.Counter()` | `Annotated[int, Counter()]` |
| `columns.List(columns.Text)` | `list[str]` |
| `columns.Set(columns.Integer)` | `set[int]` |
| `columns.Map(columns.Text, columns.Integer)` | `dict[str, int]` |
| `columns.Tuple(columns.Text, columns.Integer)` | `tuple[str, int]` |

See {doc}`/guide/field-types` for the full list of type annotations and markers.

## Column Options

| cqlengine Option | coodie Equivalent |
|---|---|
| `primary_key=True` | `Annotated[T, PrimaryKey()]` |
| `primary_key=True, partition_key=True` | `Annotated[T, PrimaryKey(partition_key_index=N)]` |
| `clustering_order="DESC"` | `Annotated[T, ClusteringKey(order="DESC")]` |
| `index=True` | `Annotated[T, Indexed()]` |
| `required=True` | Field has no default value |
| `required=False` | `Optional[T] = None` or `T = default_value` |
| `default=value` | `field: T = value` or `Field(default=value)` |
| `default=callable` | `field: T = Field(default_factory=callable)` |

See {doc}`/guide/keys-and-indexes` for detailed usage of keys and indexes.

## Batch Operations

### cqlengine

```python
from cassandra.cqlengine.query import BatchQuery

with BatchQuery() as b:
    Product.batch(b).create(id=uuid4(), name="A", ...)
    Product.batch(b).create(id=uuid4(), name="B", ...)
```

### coodie

```python
from coodie.sync import BatchQuery  # or coodie.aio.AsyncBatchQuery

with BatchQuery() as batch:
    Product(id=uuid4(), name="A", ...).save(batch=batch)
    Product(id=uuid4(), name="B", ...).save(batch=batch)
```

## Real-World Example: scylladb/argus

For a detailed, end-to-end migration walkthrough — covering 5 Argus-inspired
models (User, TestRun, Notification, Event, Comment) and 7 operation patterns —
see the dedicated page:

> {doc}`/migration/argus-example`

## What's Better in coodie

coodie is not just a 1:1 port of cqlengine — it improves the developer
experience in several ways:

- **Pydantic v2 validation** — every field is validated at instantiation, with
  clear error messages. No more silent type coercion.
- **Standard Python type hints** — your IDE autocompletes fields, catches
  typos, and understands your models. No more `columns.Text()` — just `str`.
- **First-class async support** — the same model works with both sync and
  async drivers. Add `await` in front of terminal methods, and you're done.
- **Pluggable drivers** — switch between `scylla-driver` (cassandra-driver
  fork) and `acsylla` (C++ async driver) without changing model code.
- **Schema sync returns CQL** — `sync_table()` returns the list of CQL
  statements it plans to execute, so you can review or log them.

## Migrating User-Defined Types (UDTs)

coodie provides full UDT support via the `UserType` base class.

### Before (cqlengine)

```python
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine import columns
from cassandra.cqlengine.management import sync_type

class Address(UserType):
    __type_name__ = "address"
    street = columns.Text()
    city = columns.Text()
    zipcode = columns.Integer()

class User(Model):
    id = columns.UUID(primary_key=True)
    home = columns.UserDefinedType(Address)
    others = columns.List(columns.UserDefinedType(Address))

# Must sync types manually in dependency order
sync_type("my_ks", Address)
sync_table(User)
```

### After (coodie)

```python
from coodie.usertype import UserType
from coodie.sync import Document
from coodie.fields import PrimaryKey

class Address(UserType):
    street: str
    city: str
    zipcode: int

    class Settings:
        __type_name__ = "address"   # optional — defaults to snake_case

class User(Document):
    id: Annotated[UUID, PrimaryKey()]
    home: Address                       # auto-detected as frozen<address>
    others: list[Address] = []          # list<frozen<address>>

# sync_type() auto-resolves dependencies
Address.sync_type()
User.sync_table()
```

Key differences:
- **No `columns.UserDefinedType()` wrapper** — just use the `UserType` class directly as a type annotation.
- **No `columns.*` field declarations** — use standard Python type annotations.
- **Automatic dependency resolution** — `sync_type()` recursively syncs nested UDT dependencies.
- **`Settings.__type_name__`** instead of class-level `__type_name__`.

See the {doc}`/guide/user-defined-types` guide for full details.

(cqlengine-features-different-syntax)=
## cqlengine Features with a Different Syntax

These cqlengine features exist in coodie, but are spelled differently.

| cqlengine Feature | coodie |
|---|---|
| **Static columns** — `columns.Text(static=True)` | `Annotated[str, Static()]` |
| **`Model.create()` class method** | `Model.create(**kwargs)` (or `Model(**kwargs).save()`) |
| **`__like` filter operator** (SASI / SAI indexes) | `Model.find(name__like="prefix%")` |
| **Token-range queries** — `__token` filter | `Model.find(id__token__gt=token)` |
| **Cursor-based `paging_state`** | `Model.find().fetch_size(n).page(state).paged_all()` returns `PagedResult(data, paging_state)` |
| **Per-model `__connection__`** | `class Settings: connection = "name"` with `init_coodie(name="name", ...)` |
| **`create_keyspace_network_topology()`** | `create_keyspace("ks", strategy="NetworkTopologyStrategy", dc_replication_map={"dc1": 3})` |
| **Counter columns** | Inherit from `CounterDocument` and use `increment()`/`decrement()`. You cannot mix counter and non-counter columns in a single model, matching the CQL restriction. |

## Common Gotchas

1. **No `Model.objects` attribute.** cqlengine uses `Model.objects.filter(...)`.
   In coodie, use `Model.find(...)` directly on the class.

2. **`Model.create()` still works.** `Product.create(id=uuid4(), name="Widget")`
   is equivalent to `Product(id=uuid4(), name="Widget").save()`.

3. **`__table_name__` moves to `Settings`.** Don't put table metadata as class
   attributes. Use the inner `Settings` class:

   ```python
   class Settings:
       name = "my_table"
       keyspace = "my_ks"
   ```

4. **`required=True` is the default.** In cqlengine, fields without
   `required=True` are optional. In coodie (via Pydantic), a field without a
   default value is required. Add `= None` or `Optional[T] = None` to make a
   field optional.

5. **Async needs `await`.** If you import from `coodie.aio`, all terminal
   operations (`save()`, `delete()`, `get()`, `find().all()`, etc.) must be
   awaited. The model definition itself is identical.

6. **`sync_table()` is a class method.** No separate `management.sync_table()`
   function — call `Product.sync_table()` on the Document class directly.

## Migration Checklist

Use this checklist when converting a cqlengine application to coodie:

- [ ] **Replace imports:** `cassandra.cqlengine` → `coodie` / `coodie.sync` / `coodie.aio`
- [ ] **Convert models:** `Model` → `Document`; `columns.*` → Python type annotations with `Annotated` markers
- [ ] **Convert column options:** `primary_key=True` → `PrimaryKey()`; `index=True` → `Indexed()`; etc.
- [ ] **Convert `__table_name__` / `__keyspace__`:** Move to inner `Settings` class
- [ ] **Convert connection setup:** `connection.setup()` → `init_coodie()`
- [ ] **Convert table sync:** `sync_table(Model)` → `Model.sync_table()`
- [ ] **Convert queries:** `Model.objects.filter(...)` → `Model.find(...)`
- [ ] **Convert `objects.get()`:** `Model.objects.get(...)` → `Model.get(...)`
- [ ] **Convert batch operations:** `BatchQuery()` context manager → coodie `BatchQuery()` with `.save(batch=batch)`
- [ ] **Handle async:** If migrating to async, add `await` before all Document and QuerySet terminal methods
- [ ] **Check syntax differences:** Review the [different syntax](#cqlengine-features-different-syntax) table for static columns, counters, token queries and per-model connections
- [ ] **Migrate UDTs:** Convert `UserType` + `columns.*` to `UserType` + type annotations; replace `sync_type()` with `Address.sync_type()` (see above)
- [ ] **Test thoroughly:** Run your existing test suite against coodie to verify parity

## What's Next?

- {doc}`/quickstart` — get started with coodie in 60 seconds
- {doc}`/guide/defining-documents` — learn how Document classes work
- {doc}`/guide/field-types` — all the type annotations you can use
- {doc}`/guide/crud` — the full CRUD reference
