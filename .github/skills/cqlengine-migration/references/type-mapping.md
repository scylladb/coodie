# cqlengine → coodie Type Mapping Reference

Complete mapping of every cqlengine column type to its coodie equivalent.

## Scalar Types

| cqlengine Column | CQL Type | coodie Python Type | Notes |
|---|---|---|---|
| `columns.Text()` | `text` | `str` | Direct mapping |
| `columns.Ascii()` | `ascii` | `Annotated[str, Ascii()]` | Marker needed for CQL `ascii` vs `text` |
| `columns.Integer()` | `int` | `int` | Direct mapping |
| `columns.BigInt()` | `bigint` | `Annotated[int, BigInt()]` | Marker needed |
| `columns.SmallInt()` | `smallint` | `Annotated[int, SmallInt()]` | Marker needed |
| `columns.TinyInt()` | `tinyint` | `Annotated[int, TinyInt()]` | Marker needed |
| `columns.VarInt()` | `varint` | `Annotated[int, VarInt()]` | Marker needed |
| `columns.Float()` | `float` | `float` | Direct mapping |
| `columns.Double()` | `double` | `Annotated[float, Double()]` | Marker needed |
| `columns.Decimal()` | `decimal` | `Decimal` | Import from `decimal` stdlib |
| `columns.Boolean()` | `boolean` | `bool` | Direct mapping |
| `columns.UUID()` | `uuid` | `UUID` | Import from `uuid` stdlib |
| `columns.TimeUUID()` | `timeuuid` | `Annotated[UUID, TimeUUID()]` | Marker needed to distinguish from plain UUID |
| `columns.DateTime()` | `timestamp` | `datetime` | Import from `datetime` stdlib |
| `columns.Date()` | `date` | `date` | Import from `datetime` stdlib |
| `columns.Time()` | `time` | `Annotated[int, Time()]` | CQL `time` maps to nanoseconds-since-midnight |
| `columns.Blob()` | `blob` | `bytes` | Direct mapping |
| `columns.Inet()` | `inet` | `IPv4Address` or `IPv6Address` | Import from `ipaddress` stdlib |
| `columns.Counter()` | `counter` | `Annotated[int, Counter()]` | Must use `CounterDocument` base class |

## Collection Types

| cqlengine Column | CQL Type | coodie Python Type | Default |
|---|---|---|---|
| `columns.List(columns.Text)` | `list<text>` | `list[str]` | `Field(default_factory=list)` |
| `columns.Set(columns.Integer)` | `set<int>` | `set[int]` | `Field(default_factory=set)` |
| `columns.Map(columns.Text, columns.Integer)` | `map<text,int>` | `dict[str, int]` | `Field(default_factory=dict)` |
| `columns.Tuple(columns.Text, columns.Integer)` | `tuple<text,int>` | `tuple[str, int]` | `None` (tuples are typically optional) |
| `columns.List(columns.UserDefinedType(Addr))` | `list<frozen<addr>>` | `list[Address]` | `Field(default_factory=list)` |
| Frozen collection | `frozen<list<text>>` | `Annotated[list[str], Frozen()]` | — |

## Key and Index Annotations

| cqlengine Option | coodie Annotation | Example |
|---|---|---|
| `primary_key=True` | `Annotated[T, PrimaryKey()]` | `id: Annotated[UUID, PrimaryKey()]` |
| `primary_key=True, partition_key=True` | `Annotated[T, PrimaryKey(partition_key_index=N)]` | `category: Annotated[str, PrimaryKey(partition_key_index=1)]` |
| `clustering_order="DESC"` | `Annotated[T, ClusteringKey(order="DESC")]` | `created_at: Annotated[datetime, ClusteringKey(order="DESC")]` |
| `index=True` | `Annotated[T, Indexed()]` | `brand: Annotated[str, Indexed()]` |
| `static=True` | `Annotated[T, Static()]` | `group_name: Annotated[str, Static()]` |

## Column Options

| cqlengine Option | coodie Equivalent | Example |
|---|---|---|
| `required=True` | No default value | `name: str` (no `= ...`) |
| `required=False` (default) | `Optional[T] = None` | `description: Optional[str] = None` |
| `default=value` | `field: T = value` | `status: str = "active"` |
| `default=callable` | `Field(default_factory=callable)` | `id: UUID = Field(default_factory=uuid4)` |

## Composite Annotations

Multiple markers compose inside `Annotated`:

```python
# TimeUUID + clustering key
id: Annotated[UUID, TimeUUID(), ClusteringKey(order="DESC")] = Field(
    default_factory=uuid1
)

# BigInt + clustering key
posted_at: Annotated[int, BigInt(), ClusteringKey(order="DESC")] = 0

# Optional + indexed
user_id: Annotated[Optional[UUID], Indexed()] = None
```

## User-Defined Types

| cqlengine | coodie |
|-----------|--------|
| `class Addr(cqlengine.UserType):` | `class Addr(coodie.usertype.UserType):` |
| `street = columns.Text()` | `street: str` |
| `home = columns.UserDefinedType(Addr)` | `home: Addr` |
| `others = columns.List(columns.UserDefinedType(Addr))` | `others: list[Addr] = []` |
| `management.sync_type("ks", Addr)` | `Addr.sync_type()` |
| `__type_name__ = "addr"` | `class Settings: __type_name__ = "addr"` |

## Imports Cheat Sheet

```python
# coodie core
from coodie.sync import Document, init_coodie, BatchQuery       # sync
from coodie.aio import Document, init_coodie, AsyncBatchQuery   # async

# Field markers (import only what you need)
from coodie.fields import (
    Ascii,
    BigInt,
    ClusteringKey,
    Counter,
    Double,
    Frozen,
    Indexed,
    PrimaryKey,
    SmallInt,
    Static,
    Time,
    TimeUUID,
    TinyInt,
    VarInt,
)

# UDT
from coodie.usertype import UserType

# Exceptions
from coodie.exceptions import DocumentNotFound, MultipleDocumentsReturned

# Standard library (commonly needed)
from datetime import date, datetime, timezone
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address
from typing import Annotated, Optional
from uuid import UUID, uuid1, uuid4

# Pydantic
from pydantic import Field
```
