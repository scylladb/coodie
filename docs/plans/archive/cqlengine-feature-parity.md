# coodie → cqlengine Feature-Parity Plan

> **Goal:** Make coodie a complete, drop-in-spirit replacement for
> `cassandra.cqlengine` — covering every public feature of `cqlengine`'s
> models, columns, query, and usertype APIs — using Pydantic-native typing,
> zero cqlengine imports, pluggable drivers, and first-class sync + async support.

---

## Table of Contents

1. [Feature Gap Analysis](#1-feature-gap-analysis)
   - [1.1 Column / Type System](#11-column--type-system)
   - [1.2 Model API](#12-model-api)
   - [1.3 QuerySet / Query API](#13-queryset--query-api)
   - [1.4 Schema / DDL Management](#14-schema--ddl-management)
   - [1.5 User-Defined Types (UDT)](#15-user-defined-types-udt)
   - [1.6 Batch Operations](#16-batch-operations)
   - [1.7 Connection / Session Management](#17-connection--session-management)
   - [1.8 Advanced Features](#18-advanced-features)
2. [Implementation Phases](#2-implementation-phases)
3. [Test Plan](#3-test-plan)
4. [Performance Benchmarks](#4-performance-benchmarks)
5. [cqlengine → coodie Migration Guide](#5-cqlengine--coodie-migration-guide)
6. [References](#6-references)

---

## 1. Feature Gap Analysis

Legend:
- ✅ **Implemented** — working in coodie today
- 🔧 **Partial** — infrastructure exists but not fully exposed via public API
- ❌ **Missing** — not yet implemented

### 1.1 Column / Type System

#### Scalar Types

| cqlengine Column | CQL Type | Python Type (coodie) | Status |
|---|---|---|---|
| `columns.Text()` | `text` | `str` | ✅ |
| `columns.Ascii()` | `ascii` | `Annotated[str, Ascii()]` | ✅ |
| `columns.Integer()` | `int` | `int` | ✅ |
| `columns.BigInt()` | `bigint` | `Annotated[int, BigInt()]` | ✅ |
| `columns.SmallInt()` | `smallint` | `Annotated[int, SmallInt()]` | ✅ |
| `columns.TinyInt()` | `tinyint` | `Annotated[int, TinyInt()]` | ✅ |
| `columns.VarInt()` | `varint` | `Annotated[int, VarInt()]` | ✅ |
| `columns.Float()` | `float` | `float` | ✅ |
| `columns.Double()` | `double` | `Annotated[float, Double()]` | ✅ |
| `columns.Decimal()` | `decimal` | `Decimal` | ✅ |
| `columns.Boolean()` | `boolean` | `bool` | ✅ |
| `columns.UUID()` | `uuid` | `UUID` | ✅ |
| `columns.TimeUUID()` | `timeuuid` | `Annotated[UUID, TimeUUID()]` | ✅ |
| `columns.DateTime()` | `timestamp` | `datetime` | ✅ |
| `columns.Date()` | `date` | `date` | ✅ |
| `columns.Time()` | `time` | `datetime.time` | ✅ |
| `columns.Blob()` | `blob` | `bytes` | ✅ |
| `columns.Inet()` | `inet` | `IPv4Address` / `IPv6Address` | ✅ |
| `columns.Counter()` | `counter` | `Annotated[int, Counter()]` | ✅ `CounterDocument` with `increment()`/`decrement()` |
| `columns.Static()` | N/A (modifier) | `Annotated[T, Static()]` | ✅ emits `STATIC` in DDL |

#### Collection Types

| cqlengine Column | CQL Type | Python Type (coodie) | Status |
|---|---|---|---|
| `columns.List(value_type)` | `list<T>` | `list[T]` | ✅ |
| `columns.Set(value_type)` | `set<T>` | `set[T]` | ✅ |
| `columns.Map(key_type, value_type)` | `map<K,V>` | `dict[K,V]` | ✅ |
| `columns.Tuple(type1, type2, …)` | `tuple<…>` | `tuple[T1, T2, …]` | ✅ |
| `frozen<T>` (any collection) | `frozen<T>` | `Annotated[T, Frozen()]` | ✅ |

#### User-Defined Types

| cqlengine Feature | Status | Notes |
|---|---|---|
| `UserType` base class | ✅ | `coodie.usertype.UserType(BaseModel)` |
| `columns.UserDefinedType(MyUDT)` column | ✅ | Auto-detected via type annotation — no wrapper needed |
| `management.sync_type()` | ✅ | `MyUDT.sync_type()` classmethod (sync + async) |
| `__type_name__` override | ✅ | `Settings.__type_name__` |
| Nested UDTs | ✅ | Recursive depth-first dependency resolution |
| UDTs inside collections (`list<frozen<my_udt>>`) | ✅ | Auto-detected in `python_type_to_cql_type_str()` |

### 1.2 Model API

| cqlengine Feature | coodie Equivalent | Status |
|---|---|---|
| `class MyModel(Model)` | `class MyModel(Document)` | ✅ |
| `__table_name__` | `Settings.name` | ✅ |
| `__keyspace__` | `Settings.keyspace` | ✅ |
| `__connection__` | `Settings.connection` / `_get_driver()` | ✅ routes to named driver |
| `__default_ttl__` | `Settings.__default_ttl__` | ✅ |
| `__abstract__ = True` | `Settings.__abstract__` | ✅ |
| `__discriminator_value__` (polymorphism) | `Settings.__discriminator_value__` + `Discriminator` marker | ✅ |
| `__options__` (table options: compaction, etc.) | `Settings.__options__` | ✅ |
| `Model.create(**kwargs)` | `Document.create(**kwargs)` | ✅ |
| `Model.save()` | `Document.save()` | ✅ |
| `Model.update(**kwargs)` | `Document.update(**kwargs)` | ✅ |
| `Model.delete()` | `Document.delete()` | ✅ |
| `Model.insert()` (IF NOT EXISTS) | `Document.insert()` | ✅ |
| `Model.validate()` | Pydantic `model_validate()` | ✅ (via Pydantic) |
| `Model.column_family_name()` | `Document.table_name()` / `_get_table()` | ✅ |
| `Model.objects` (returns QuerySet) | `Document.find()` | ✅ different API surface |
| `Model.timeout(seconds)` on instance operations | `Document.save(timeout=...)` etc. | ✅ |
| `Model.consistency(level)` on instance operations | `Document.save(consistency=...)` etc. | ✅ |
| `Model.if_not_exists()` on save | `Document.insert()` | ✅ |
| `Model.if_exists()` on update/delete | `Document.delete(if_exists=True)` / `update(if_exists=True)` | ✅ |
| `Model.batch(batch_query)` | `doc.save(batch=batch)` / `doc.delete(batch=batch)` | ✅ |
| `Model.timestamp(ts)` on write ops | `Document.save(timestamp=...)` etc. | ✅ |

### 1.3 QuerySet / Query API

| cqlengine Feature | coodie Equivalent | Status |
|---|---|---|
| `Model.objects.all()` | `Document.find().all()` | ✅ |
| `Model.objects.filter(**kwargs)` | `Document.find(**kwargs)` / `.filter()` | ✅ |
| `Model.objects.get(**kwargs)` | `Document.get(**kwargs)` | ✅ |
| `.first()` | `QuerySet.first()` | ✅ |
| `.count()` | `QuerySet.count()` | ✅ |
| `.limit(n)` | `QuerySet.limit(n)` | ✅ |
| `.order_by(*cols)` | `QuerySet.order_by(*cols)` | ✅ |
| `.allow_filtering()` | `QuerySet.allow_filtering()` | ✅ |
| `.delete()` (bulk) | `QuerySet.delete()` | ✅ |
| `__iter__` (sync) | `QuerySet.__iter__` | ✅ |
| `__len__` (sync) | `QuerySet.__len__` | ✅ |
| `__aiter__` (async) | `AsyncQuerySet.__aiter__` | ✅ |
| `.update(**kwargs)` (bulk UPDATE) | `QuerySet.update(**kwargs)` | ✅ |
| `.if_not_exists()` on QuerySet | `QuerySet.if_not_exists()` | ✅ |
| `.if_exists()` on QuerySet | `QuerySet.if_exists()` | ✅ |
| `.ttl(seconds)` on QuerySet | `QuerySet.ttl(seconds)` | ✅ |
| `.timestamp(ts)` on QuerySet | `QuerySet.timestamp(ts)` | ✅ |
| `.consistency(level)` on QuerySet | `QuerySet.consistency(level)` | ✅ |
| `.using(ttl=, timestamp=)` | `QuerySet.using(ttl=, timestamp=, consistency=, timeout=)` | ✅ |
| `.values_list()` (column projection) | `QuerySet.values_list(*columns)` | ✅ |
| `.only(*columns)` (column projection) | `QuerySet.only(*columns)` | ✅ |
| `.defer(*columns)` (exclude columns) | `QuerySet.defer(*columns)` | ✅ |
| `.per_partition_limit(n)` | `QuerySet.per_partition_limit(n)` | ✅ |
| Token-range queries / paging | `QuerySet.fetch_size(n)` / `.page(state)` / `.paged_all()` | ✅ |
| Named queries / raw CQL execution | `execute_raw(stmt, params)` | ✅ |

#### Filter Operators

| cqlengine Operator | coodie `__` lookup | Status |
|---|---|---|
| `__gt` | `__gt` | ✅ |
| `__gte` | `__gte` | ✅ |
| `__lt` | `__lt` | ✅ |
| `__lte` | `__lte` | ✅ |
| `__in` | `__in` | ✅ |
| `__contains` | `__contains` | ✅ |
| `__contains_key` (map) | `__contains_key` | ✅ |
| `__like` (SASI index) | `__like` | ✅ |
| `__token` (token range) | `__token__gt`, `__token__gte`, `__token__lt`, `__token__lte` | ✅ |

### 1.4 Schema / DDL Management

| cqlengine Feature | coodie Equivalent | Status |
|---|---|---|
| `management.sync_table(Model)` | `Document.sync_table()` | ✅ |
| `management.drop_table(Model)` | `Document.drop_table()` | ✅ |
| `management.sync_type(UserType)` | — | ❌ |
| `management.create_keyspace_simple()` | `create_keyspace(ks, replication_factor=N)` | ✅ |
| `management.create_keyspace_network_topology()` | `create_keyspace(ks, dc_replication_map={...})` | ✅ |
| `management.drop_keyspace()` | `drop_keyspace(ks)` | ✅ |
| `ALTER TABLE ADD column` (schema migration) | Handled inside `sync_table` via driver | ✅ |
| `CREATE INDEX IF NOT EXISTS` | Handled inside `sync_table` for `Indexed` fields | ✅ |
| `CREATE MATERIALIZED VIEW` | `MaterializedView.sync_view()` | ✅ |
| `DROP MATERIALIZED VIEW` | `MaterializedView.drop_view()` | ✅ |
| Table options (`WITH compaction = …`) | `Settings.__options__` | ✅ |

### 1.5 User-Defined Types (UDT)

cqlengine provides a `UserType` base class in `cassandra.cqlengine.usertype` with:
- Field declaration using `columns.*` attributes
- `__type_name__` override
- `management.sync_type()` DDL
- `columns.UserDefinedType(MyUDT)` for embedding in models
- Nested UDTs
- UDTs inside collections

**coodie status: Entirely missing.** This is the only significant remaining gap.
Use `frozen<>` collections or separate tables as a workaround.

#### UDT Implementation Tasks

| Task | Description |
|---|---|
| A.1 | Create `coodie.usertype` module with `UserType(BaseModel)` base class |
| A.2 | Add `__type_name__` override (default: snake_case of class name) |
| A.3 | Add `build_create_type()` / `build_drop_type()` to `cql_builder.py` |
| A.4 | Add `sync_type()` classmethod to `UserType` |
| A.5 | Register UDT types in `python_type_to_cql_type_str()` → emit `frozen<type_name>` |
| A.6 | Support UDTs inside collections (`list[MyUDT]` → `list<frozen<my_udt>>`) |
| A.7 | Support nested UDTs |
| A.8 | Serialization/deserialization of UDT values to/from dicts |
| A.9 | Register UDT with driver (e.g. `cluster.register_user_type()`) |
| A.10 | Unit + integration tests |

### 1.6 Batch Operations

| cqlengine Feature | coodie Equivalent | Status |
|---|---|---|
| `BatchQuery()` context manager | `BatchQuery` / `AsyncBatchQuery` in `coodie.batch` | ✅ |
| `Model.batch(batch_query).create()` | `doc.insert(batch=batch)` | ✅ |
| `Model.batch(batch_query).save()` | `doc.save(batch=batch)` | ✅ |
| `Model.batch(batch_query).delete()` | `doc.delete(batch=batch)` | ✅ |
| Logged batch | `BatchQuery(logged=True)` | ✅ |
| Unlogged batch | `BatchQuery(logged=False)` | ✅ |
| Counter batch | `BatchQuery(batch_type="COUNTER")` | ✅ |

### 1.7 Connection / Session Management

| cqlengine Feature | coodie Equivalent | Status |
|---|---|---|
| `connection.setup(hosts, keyspace)` | `init_coodie(hosts, keyspace)` | ✅ |
| `connection.register_connection(name, ...)` | `register_driver(name, driver)` | ✅ |
| `connection.set_default_connection(name)` | default driver in registry | ✅ |
| Per-model `__connection__` | `Settings.connection` routes to named driver | ✅ |
| Multiple named connections in same app | Driver registry supports named drivers | ✅ |
| Lazy connection (connect on first use) | `init_coodie(..., lazy=True)` | ✅ |
| Connection pooling options | Delegated to underlying driver | ✅ (passthrough) |

### 1.8 Advanced Features

| cqlengine Feature | coodie Status | Notes |
|---|---|---|
| Polymorphic models (`__discriminator_value__`) | ✅ | `Discriminator` marker + `Settings.__discriminator_value__` |
| Abstract models (`__abstract__`) | ✅ | `Settings.__abstract__ = True` |
| Default TTL (`__default_ttl__`) | ✅ | `Settings.__default_ttl__` → `WITH default_time_to_live` |
| Table options (`__options__`) | ✅ | `Settings.__options__` dict |
| Lightweight transactions (IF EXISTS / IF conditions) | ✅ | `Document.update(if_exists=True)`, `delete(if_exists=True)`, `update(if_conditions={...})` |
| USING TIMESTAMP | ✅ | `save(timestamp=...)`, `delete(timestamp=...)` etc. |
| Consistency level per operation | ✅ | `save(consistency=...)`, `QuerySet.consistency(level)` |
| Timeout per operation | ✅ | `save(timeout=...)`, `QuerySet.timeout(seconds)` |
| Pagination (`paging_state`, `fetch_size`) | ✅ | `QuerySet.fetch_size(n)` / `.page(state)` / `.paged_all()` |
| Token-range queries | ✅ | `__token__gt`, `__token__gte`, `__token__lt`, `__token__lte` |
| Materialized views | ✅ | `MaterializedView` base class with `sync_view()` / `drop_view()` |
| SASI / SAI index support | ✅ | `__like` filter operator |
| Counter increment/decrement API | ✅ | `CounterDocument.increment()` / `decrement()` |
| Static columns | ✅ | `Annotated[T, Static()]` marker |
| Column-level delete | ✅ | `Document.delete_columns(*column_names)` (sync + async) |

---

## 2. Implementation Phases

### Phase 1: Extended Type System (Priority: High)

**Goal:** Support all CQL scalar types that cqlengine covers.

| Task | Description |
|---|---|
| 1.1 | Add type annotation markers to `fields.py`: `BigInt`, `SmallInt`, `TinyInt`, `VarInt`, `Double`, `Ascii`, `TimeUUID`, `Time` |
| 1.2 | Update `types.py` `_SCALAR_CQL_TYPES` to map `datetime.time → time`, and handle the new annotation markers |
| 1.3 | Add `Frozen` annotation marker to `fields.py` for `frozen<T>` support |
| 1.4 | Update `python_type_to_cql_type_str()` to handle `Frozen` wrapping |
| 1.5 | Unit tests for all new type mappings |

### Phase 2: Counter Column API (Priority: High)

**Goal:** Provide a working counter column model and increment/decrement operations.

| Task | Description |
|---|---|
| 2.1 | Add `CounterDocument` base class (or mixin) that forbids `save()` / `insert()` and instead exposes `increment(**field_deltas)` / `decrement(**field_deltas)` |
| 2.2 | Add `build_counter_update()` to `cql_builder.py` generating `UPDATE … SET col = col + ?` |
| 2.3 | Enforce at schema level: counter tables can only have counter + PK columns |
| 2.4 | Unit + integration tests |

### Phase 3: Partial Update API (Priority: High)

**Goal:** Allow updating individual fields without a full INSERT (upsert).

| Task | Description |
|---|---|
| 3.1 | Add `Document.update(**kwargs)` / `await Document.update(**kwargs)` that calls `build_update()` |
| 3.2 | Support `ttl` and `if_conditions` parameters |
| 3.3 | Add `QuerySet.update(**kwargs)` for bulk UPDATE |
| 3.4 | Support collection mutation operators: `column__add`, `column__remove`, `column__append`, `column__prepend` |
| 3.5 | Unit + integration tests |

### Phase 4: Lightweight Transactions (Priority: Medium)

**Goal:** Full LWT support matching cqlengine.

| Task | Description |
|---|---|
| 4.1 | Expose `if_conditions` on `Document.update()` → `UPDATE … IF col = ?` |
| 4.2 | Add `Document.delete(if_exists=True)` → `DELETE … IF EXISTS` |
| 4.3 | Add `QuerySet.if_not_exists()` / `QuerySet.if_exists()` chain methods |
| 4.4 | Return LWT result (`[applied]` column) as a typed result |
| 4.5 | Unit + integration tests |

### Phase 5: Query Execution Options (Priority: Medium)

**Goal:** Per-query consistency, timeout, and write timestamp.

| Task | Description |
|---|---|
| 5.1 | Add `.consistency(level)` to QuerySet and Document write methods |
| 5.2 | Add `.timeout(seconds)` to QuerySet and Document write methods |
| 5.3 | Add `timestamp` parameter to `save()`, `insert()`, `update()`, `delete()` |
| 5.4 | Add `.using(ttl=, timestamp=, consistency=)` chain method to QuerySet |
| 5.5 | Plumb parameters through to `AbstractDriver.execute()` / `execute_async()` |
| 5.6 | Unit + integration tests |

### Phase 6: User-Defined Types (Priority: Medium)

**Goal:** Full UDT support matching cqlengine's `UserType`.

| Task | Description |
|---|---|
| 6.1 | Create `coodie.usertype` module with a `UserType(BaseModel)` base class |
| 6.2 | Add `__type_name__` override support (default: snake_case of class name) |
| 6.3 | Add `build_create_type()` / `build_drop_type()` to `cql_builder.py` |
| 6.4 | Add `sync_type()` classmethod to `UserType` (like `Document.sync_table()`) |
| 6.5 | Register UDT types with `python_type_to_cql_type_str()` to emit `frozen<type_name>` |
| 6.6 | Support UDTs inside collections (`list[MyUDT]` → `list<frozen<my_udt>>`) |
| 6.7 | Support nested UDTs |
| 6.8 | Serialization/deserialization of UDT values to/from dicts |
| 6.9 | Unit + integration tests |

### Phase 7: Batch API (Priority: Medium)

**Goal:** High-level batch context manager matching cqlengine's `BatchQuery`.

| Task | Description |
|---|---|
| 7.1 | Create `coodie.batch` module with `BatchQuery` context manager (sync) and `AsyncBatchQuery` async context manager |
| 7.2 | Allow `Document.save()` / `insert()` / `delete()` to accept an optional `batch` parameter |
| 7.3 | Accumulate statements and execute as a single `build_batch()` on context exit |
| 7.4 | Support logged / unlogged / counter batch types |
| 7.5 | Unit + integration tests |

### Phase 8: Model Enhancements (Priority: Medium)

**Goal:** Fill remaining model-level API gaps.

| Task | Description |
|---|---|
| 8.1 | Add `Document.create(**kwargs)` classmethod (convenience: construct + save) |
| 8.2 | Add `__abstract__` support: mark a Document subclass so it does not create a table |
| 8.3 | Add `__default_ttl__` in `Settings` → emitted as `WITH default_time_to_live = N` |
| 8.4 | Add `__options__` in `Settings` → `WITH` clause for table options |
| 8.5 | Add per-model `Settings.connection` → named driver from registry |
| 8.6 | Add `drop_table()` classmethod on Document |
| 8.7 | Add public `table_name()` classmethod (wrapping `_get_table()`) |
| 8.8 | Unit tests |

### Phase 9: Polymorphic Models (Priority: Low)

**Goal:** Single-table inheritance with discriminator column.

| Task | Description |
|---|---|
| 9.1 | Add `__discriminator_value__` support in `Settings` |
| 9.2 | Auto-add a `_type` (or configurable name) column as discriminator |
| 9.3 | On `find()` / `get()`, automatically filter by discriminator value |
| 9.4 | On `save()`, automatically set discriminator column |
| 9.5 | Return correct subclass when querying base class |
| 9.6 | Unit + integration tests |

### Phase 10: Pagination & Token Queries (Priority: Low)

**Goal:** Support cursor-based pagination and token-range full-table scans.

| Task | Description |
|---|---|
| 10.1 | Add `fetch_size` parameter to `execute()` / `execute_async()` in drivers |
| 10.2 | Plumb `paging_state` through to enable page-by-page iteration |
| 10.3 | Add `QuerySet.fetch_size(n)` chain method |
| 10.4 | Add `QuerySet.page(paging_state)` chain method |
| 10.5 | Add `__token` filter operator for token-range queries |
| 10.6 | Add `build_token_select()` or enhance `build_select()` with token support |
| 10.7 | Unit + integration tests |

### Phase 11: QuerySet Enhancements (Priority: Low)

**Goal:** Column projection, deferred loading, and advanced query features.

| Task | Description |
|---|---|
| 11.1 | Add `.only(*columns)` → SELECT specific columns |
| 11.2 | Add `.defer(*columns)` → SELECT all except specified columns |
| 11.3 | Add `.values_list(*columns)` → return tuples instead of Documents |
| 11.4 | Add `.per_partition_limit(n)` chain method (already in `build_select`) |
| 11.5 | Add `__like` filter operator (SASI/SAI index support) |
| 11.6 | Unit tests |

### Phase 12: Materialized Views (Priority: Low)

**Goal:** DDL support for materialized views.

| Task | Description |
|---|---|
| 12.1 | Add `build_create_materialized_view()` to `cql_builder.py` |
| 12.2 | Add `build_drop_materialized_view()` |
| 12.3 | Add a `MaterializedView` Document subclass or decorator |
| 12.4 | Unit + integration tests |

### Phase 13: Keyspace Management (Priority: Low)

**Goal:** Full keyspace lifecycle management.

| Task | Description |
|---|---|
| 13.1 | Add `create_keyspace_network_topology()` support |
| 13.2 | Add `build_drop_keyspace()` to `cql_builder.py` |
| 13.3 | Add public `create_keyspace()` / `drop_keyspace()` functions |
| 13.4 | Unit tests |

---

## 3. Test Plan

### 3.1 Unit Tests (MockDriver — no live DB)

Each phase should add unit tests alongside implementation. Tests use the
existing `MockDriver` fixture from `tests/conftest.py`.

#### Type System Tests (`tests/test_types.py`)

| Test Case | Phase |
|---|---|
| `bigint`, `smallint`, `tinyint`, `varint` annotation → correct CQL string | 1 |
| `double` annotation → `"double"` | 1 |
| `ascii` annotation → `"ascii"` | 1 |
| `timeuuid` annotation → `"timeuuid"` | 1 |
| `time` annotation → `"time"` | 1 |
| `Frozen[list[str]]` → `"frozen<list<text>>"` | 1 |
| `Frozen[MyUDT]` → `"frozen<my_udt>"` | 6 |
| Nested UDT type resolution | 6 |

#### Schema Tests (`tests/test_schema.py`)

| Test Case | Phase |
|---|---|
| Counter table: only counter + PK columns allowed | 2 |
| `__default_ttl__` in Settings → stored in schema metadata | 8 |
| `__abstract__` → build_schema skips or marks abstract | 8 |
| `__options__` → stored in schema metadata | 8 |
| Discriminator column auto-added for polymorphic models | 9 |
| UDT field detection and type name resolution | 6 |

#### CQL Builder Tests (`tests/test_cql_builder.py`)

| Test Case | Phase |
|---|---|
| `build_counter_update()` generates `SET col = col + ?` | 2 |
| `build_update()` with `if_conditions` → `IF col = ?` | 3/4 |
| `build_update()` with collection mutation operators | 3 |
| `build_insert()` with `timestamp` parameter | 5 |
| `build_update()` with `timestamp` parameter | 5 |
| `build_create_type()` / `build_drop_type()` | 6 |
| `build_create_materialized_view()` | 12 |
| `build_drop_materialized_view()` | 12 |
| `build_create_keyspace()` with NetworkTopologyStrategy | 13 |
| `build_drop_keyspace()` | 13 |
| `build_select()` with token range | 10 |
| `build_select()` with column projection | 11 |

#### Document Tests (`tests/sync/test_document.py`, `tests/aio/test_document.py`)

| Test Case | Phase |
|---|---|
| `Document.update(**kwargs)` generates UPDATE CQL | 3 |
| `Document.update(if_conditions={...})` generates UPDATE … IF | 4 |
| `Document.delete(if_exists=True)` generates DELETE … IF EXISTS | 4 |
| `Document.create(**kwargs)` → construct + save | 8 |
| `Document.drop_table()` → DROP TABLE | 8 |
| `Document.table_name()` returns table name | 8 |
| `Document.save(timestamp=...)` | 5 |
| `Document.save()` with `Settings.default_ttl` | 8 |
| Abstract Document → no `sync_table()` | 8 |
| Polymorphic Document → discriminator set on save | 9 |
| Polymorphic Document → filter by discriminator on find | 9 |
| Counter Document → `increment()` / `decrement()` | 2 |
| Batch context: save/insert/delete accumulate | 7 |

#### QuerySet Tests (`tests/sync/test_query.py`, `tests/aio/test_query.py`)

| Test Case | Phase |
|---|---|
| `.update(**kwargs)` generates UPDATE CQL | 3 |
| `.if_not_exists()` chain → `IF NOT EXISTS` in generated CQL | 4 |
| `.if_exists()` chain → `IF EXISTS` in generated CQL | 4 |
| `.ttl(n)` chain → `USING TTL n` | 5 |
| `.timestamp(ts)` chain → `USING TIMESTAMP ts` | 5 |
| `.consistency(level)` chain | 5 |
| `.per_partition_limit(n)` chain | 11 |
| `.only(*cols)` → SELECT specific columns | 11 |
| `.defer(*cols)` → SELECT excluding columns | 11 |
| `.values_list()` → returns tuples | 11 |
| `.fetch_size(n)` chain | 10 |

#### Driver Tests (`tests/test_drivers.py`)

| Test Case | Phase |
|---|---|
| `execute()` / `execute_async()` with consistency parameter | 5 |
| `execute()` / `execute_async()` with timeout parameter | 5 |
| `execute()` / `execute_async()` with `fetch_size` and `paging_state` | 10 |

#### API Parity Tests (`tests/test_api_parity.py`)

| Test Case | Phase |
|---|---|
| New methods added in sync match async (and vice versa) | All |

### 3.2 Integration Tests (Real ScyllaDB via testcontainers)

Integration tests run against a real ScyllaDB container and are marked with
`@pytest.mark.integration`.

| Test Area | Test Cases | Phase |
|---|---|---|
| **Extended scalar types** | Insert/read round-trip for `bigint`, `smallint`, `tinyint`, `varint`, `double`, `ascii`, `timeuuid`, `time` | 1 |
| **Frozen collections** | Create table with `frozen<list<text>>` PK; insert and read | 1 |
| **Counter tables** | Create counter table; `increment()`; verify count; `decrement()` | 2 |
| **Partial update** | `update(field=new_value)` → verify only that field changed | 3 |
| **Collection mutations** | `update(tags__add={"new"})` on a `set` column | 3 |
| **LWT: IF NOT EXISTS** | `insert()` twice → second fails / returns `[applied]=false` | 4 |
| **LWT: IF conditions** | `update(if_conditions={...})` with matching and non-matching | 4 |
| **LWT: IF EXISTS** | `delete(if_exists=True)` on existing and non-existing row | 4 |
| **Consistency** | Set `consistency=LOCAL_QUORUM` on a read; verify no error | 5 |
| **Write timestamp** | Insert with explicit `timestamp`; verify `WRITETIME()` | 5 |
| **UDT creation** | `sync_type()` → type exists in `system_schema.types` | 6 |
| **UDT round-trip** | Insert model with UDT field; read back; verify field values | 6 |
| **Nested UDT** | UDT containing another UDT; full round-trip | 6 |
| **UDT in collection** | `list[MyUDT]` field round-trip | 6 |
| **Batch: logged** | Batch insert 3 rows; verify all present | 7 |
| **Batch: unlogged** | Unlogged batch; verify all present | 7 |
| **`create()` classmethod** | `MyModel.create(...)` → row exists | 8 |
| **Default TTL** | Model with `__default_ttl__=2`; insert; wait; verify row gone | 8 |
| **Table options** | Model with `__options__`; verify via `system_schema.tables` | 8 |
| **Abstract model** | Abstract base + concrete subclass; only subclass table exists | 8 |
| **Per-model connection** | Two models on different connections/keyspaces | 8 |
| **Polymorphic models** | Base + two subclasses; insert both; query base returns correct types | 9 |
| **Pagination** | Insert 100 rows; fetch with `fetch_size=10`; iterate all pages | 10 |
| **Token range** | Full-table scan via token range query | 10 |
| **Column projection** | `.only("name", "price")` → verify only those columns returned | 11 |
| **Per-partition limit** | `.per_partition_limit(2)` on multi-partition table | 11 |
| **Materialized view** | Create MV; insert base row; query MV | 12 |

---

## 4. Performance Benchmarks

Every major feature should be benchmarked **side-by-side** against cqlengine to
ensure coodie introduces no regressions and to surface bottlenecks early.

### 4.1 Recommended Tooling

| Tool | Purpose | Install |
|---|---|---|
| [pytest-benchmark](https://pytest-benchmark.readthedocs.io/) | Micro-benchmarks integrated into pytest; produces min/max/mean/stddev tables, JSON export, and historical comparison | `pip install pytest-benchmark` |
| [memray](https://bloomberg.github.io/memray/) | Memory profiler — flame graphs, allocation tracking, leak detection | `pip install memray` |
| [py-spy](https://github.com/benfred/py-spy) | Sampling CPU profiler — flame graphs and top-like live view, zero-overhead attach to running process | `pip install py-spy` |
| [scalene](https://github.com/plasma-umass/scalene) | CPU + memory + GPU profiler — line-level attribution, separates Python vs C time | `pip install scalene` |
| [cProfile + snakeviz](https://jiffyclub.github.io/snakeviz/) | Built-in deterministic profiler with interactive visualization | `pip install snakeviz` |
| [cassandra-stress](https://cassandra.apache.org/doc/latest/cassandra/tools/cassandra_stress.html) | Cassandra/ScyllaDB native load generator — stress test at the driver/cluster level | Ships with ScyllaDB/Cassandra |

### 4.2 Benchmark Infrastructure

```
benchmarks/
├── conftest.py              # shared fixtures: ScyllaDB container, cqlengine setup, coodie setup
├── models_cqlengine.py      # cqlengine model definitions (Product, Review, Event, etc.)
├── models_coodie.py         # coodie model definitions (identical schema)
├── bench_insert.py          # INSERT benchmarks
├── bench_read.py            # SELECT / query benchmarks
├── bench_update.py          # UPDATE benchmarks
├── bench_delete.py          # DELETE benchmarks
├── bench_batch.py           # Batch operation benchmarks
├── bench_schema.py          # DDL / sync_table benchmarks
├── bench_collections.py     # Collection type read/write benchmarks
├── bench_udt.py             # UDT benchmarks (Phase 6)
├── bench_pagination.py      # Pagination benchmarks (Phase 10)
└── README.md                # How to run, interpret results, and compare
```

Benchmarks use `@pytest.mark.benchmark` and run against a real ScyllaDB
container (same testcontainers setup as integration tests).

### 4.3 Benchmark Matrix — by Feature

Each benchmark runs the same operation via **cqlengine** and **coodie**, measuring
latency (p50/p95/p99), throughput (ops/sec), and memory allocation.

#### Write Operations

| Benchmark | cqlengine Operation | coodie Operation | Phase |
|---|---|---|---|
| Single INSERT | `Model.create(...)` | `Document(...).save()` | 1 |
| INSERT IF NOT EXISTS | `Model.if_not_exists().create(...)` | `Document(...).insert()` | 4 |
| INSERT with TTL | `Model.ttl(60).create(...)` | `Document(...).save(ttl=60)` | 5 |
| Partial UPDATE | `Model.objects(...).update(field=val)` | `Document.update(field=val)` | 3 |
| UPDATE with IF condition | `Model.objects(...).iff(col=val).update(...)` | `Document.update(if_conditions={...})` | 4 |
| Single DELETE | `instance.delete()` | `document.delete()` | 1 |
| Bulk DELETE | `Model.objects.filter(...).delete()` | `QuerySet.delete()` | 1 |
| Batch INSERT (10 rows) | `BatchQuery` context | `BatchQuery` context | 7 |
| Batch INSERT (100 rows) | `BatchQuery` context | `BatchQuery` context | 7 |
| Counter increment | `Model.objects(...).update(col__add=1)` | `CounterDocument.increment(col=1)` | 2 |

#### Read Operations

| Benchmark | cqlengine Operation | coodie Operation | Phase |
|---|---|---|---|
| GET by PK | `Model.objects.get(pk=val)` | `Document.get(pk=val)` | 1 |
| Filter (secondary index) | `Model.objects.filter(indexed_col=val)` | `Document.find(indexed_col=val).all()` | 1 |
| Filter + LIMIT | `.filter(...).limit(100)` | `.find(...).limit(100).all()` | 1 |
| Filter + ORDER BY | `.filter(...).order_by("-col")` | `.find(...).order_by("-col").all()` | 1 |
| COUNT | `Model.objects.count()` | `Document.find().count()` | 1 |
| Paginated read (1000 rows) | Manual `paging_state` | `QuerySet.fetch_size(100)` | 10 |
| Collection field read | Read `list[str]` / `map<K,V>` column | Same | 1 |
| UDT field read | Read `UserDefinedType` column | Read `UserType` field | 6 |

#### Schema / DDL

| Benchmark | cqlengine Operation | coodie Operation | Phase |
|---|---|---|---|
| `sync_table` (create) | `management.sync_table(Model)` | `Document.sync_table()` | 1 |
| `sync_table` (idempotent, no-op) | `management.sync_table(Model)` (2nd call) | `Document.sync_table()` (2nd call) | 1 |
| `sync_table` (add column) | Add field + `sync_table` | Add field + `sync_table` | 1 |
| `sync_type` (UDT create) | `management.sync_type(MyUDT)` | `UserType.sync_type()` | 6 |

#### Serialization / Deserialization Overhead

| Benchmark | What It Measures | Phase |
|---|---|---|
| Model instantiation (10 fields) | Time to construct model from dict (Pydantic vs cqlengine metaclass) | 1 |
| Model serialization (10 fields) | Time to convert model to dict for INSERT | 1 |
| Collection round-trip (list, set, map) | Serialize + INSERT + SELECT + deserialize | 1 |
| UDT round-trip | Serialize + INSERT + SELECT + deserialize | 6 |

### 4.4 How to Run Benchmarks

```bash
# Run all benchmarks (requires Docker for ScyllaDB container)
pytest benchmarks/ -v --benchmark-enable --benchmark-sort=mean

# Run a specific benchmark file
pytest benchmarks/bench_insert.py -v --benchmark-enable

# Compare coodie vs cqlengine side by side
pytest benchmarks/ -v --benchmark-enable --benchmark-group-by=group

# Save results for historical tracking
pytest benchmarks/ --benchmark-enable --benchmark-save=baseline
pytest benchmarks/ --benchmark-enable --benchmark-compare=0001_baseline

# Generate HTML report
pytest benchmarks/ --benchmark-enable --benchmark-histogram=bench_results

# Profile a specific bottleneck with py-spy
py-spy record -o profile.svg -- python -m pytest benchmarks/bench_insert.py -v

# Memory profiling with memray
memray run -o output.bin -m pytest benchmarks/bench_insert.py -v
memray flamegraph output.bin

# Line-level profiling with scalene
scalene --- -m pytest benchmarks/bench_insert.py -v
```

### 4.5 Bottleneck Investigation Workflow

When a benchmark shows coodie is slower than cqlengine:

1. **Identify the hot path** — Run `py-spy` flame graph to see where time is spent
2. **Separate Python vs C time** — Use `scalene` to distinguish Python overhead from driver/C extension time
3. **Check memory** — Run `memray` to verify no excessive allocations (e.g., from Pydantic model construction)
4. **Isolate the layer** — Run the same CQL via raw `driver.execute()` to determine if overhead is in coodie's ORM layer or the driver
5. **Compare serialization** — Benchmark `model_dump()` vs cqlengine's internal serialization separately
6. **Check prepared statements** — Verify coodie's prepared-statement cache is hit (cache miss = extra round-trip)

### 4.6 Performance Targets

| Metric | Target |
|---|---|
| Single INSERT latency | ≤ 1.2× cqlengine (Pydantic validation overhead accepted) |
| Single GET by PK latency | ≤ 1.1× cqlengine |
| Bulk INSERT (100 rows, batch) | ≤ 1.1× cqlengine |
| Model instantiation from dict | ≤ 2× cqlengine (Pydantic validation cost) |
| Memory per 1000 model instances | ≤ 1.5× cqlengine |
| `sync_table` DDL | ≤ 1.05× cqlengine (one-time cost, less critical) |

> **Note:** Pydantic validation adds inherent overhead compared to cqlengine's
> lighter metaclass approach. The targets above accept this trade-off in exchange
> for type safety, better IDE support, and FastAPI integration. If benchmarks
> exceed these targets, the bottleneck investigation workflow (§4.5) should be
> used to determine if the overhead is justified or optimizable.

### 4.7 CI Integration

Add a `benchmark.yml` GitHub Actions workflow:

```
Triggers : push to main, weekly schedule (for trend tracking)
Runner   : ubuntu-latest (consistent hardware for reproducible results)
Steps    : checkout → setup-python → install deps
           → pytest benchmarks/ --benchmark-enable --benchmark-json=output.json
           → upload artifact (output.json)
           → (optional) post results to PR comment via github-action-benchmark
```

Use [github-action-benchmark](https://github.com/benchmark-action/github-action-benchmark)
to track performance trends over time and alert on regressions (configurable
threshold, e.g., >10% degradation triggers a warning).

---

## 5. cqlengine → coodie Migration Guide

### 5.1 Core Concepts Mapping

| cqlengine | coodie | Notes |
|---|---|---|
| `from cassandra.cqlengine.models import Model` | `from coodie.sync import Document` (sync) or `from coodie.aio import Document` (async) | — |
| `from cassandra.cqlengine import columns` | `from typing import Annotated` + `from coodie import PrimaryKey, ClusteringKey, Indexed, Counter` | Use Python type annotations |
| `from cassandra.cqlengine import connection` | `from coodie import init_coodie` | — |
| `from cassandra.cqlengine.management import sync_table` | `Document.sync_table()` | Called on the class |

### 5.2 Model Definition

#### cqlengine

```python
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Product(Model):
    __table_name__ = "products"
    __keyspace__ = "catalog"
    __default_ttl__ = 86400

    id = columns.UUID(primary_key=True)
    name = columns.Text(required=True)
    brand = columns.Text(index=True)
    category = columns.Text(index=True)
    price = columns.Float()
    description = columns.Text(required=False)
    tags = columns.List(columns.Text)
    metadata = columns.Map(columns.Text, columns.Text)
    created_at = columns.DateTime()
```

#### coodie (sync)

```python
from typing import Annotated, Optional
from uuid import UUID
from datetime import datetime
from coodie.sync import Document
from coodie import PrimaryKey, Indexed

class Product(Document):
    id: Annotated[UUID, PrimaryKey()]
    name: str
    brand: Annotated[str, Indexed()]
    category: Annotated[str, Indexed()]
    price: float
    description: Optional[str] = None
    tags: list[str] = []
    metadata: dict[str, str] = {}
    created_at: datetime

    class Settings:
        name = "products"
        keyspace = "catalog"
        # default_ttl = 86400  # Phase 8
```

#### coodie (async — identical model, different import)

```python
from coodie.aio import Document  # only this import changes
from coodie import PrimaryKey, Indexed
# ... identical field declarations ...
```

### 5.3 Connection Setup

#### cqlengine

```python
from cassandra.cqlengine import connection

connection.setup(["127.0.0.1"], "catalog", protocol_version=4)
```

#### coodie (sync)

```python
from coodie.sync import init_coodie

init_coodie(hosts=["127.0.0.1"], keyspace="catalog")
```

#### coodie (async)

```python
from coodie.aio import init_coodie

await init_coodie(hosts=["127.0.0.1"], keyspace="catalog")
```

### 5.4 Table Sync

#### cqlengine

```python
from cassandra.cqlengine.management import sync_table

sync_table(Product)
```

#### coodie

```python
Product.sync_table()          # sync
await Product.sync_table()    # async
```

### 5.5 CRUD Operations

#### Create / Insert

| Operation | cqlengine | coodie (sync) | coodie (async) |
|---|---|---|---|
| Upsert | `Product.create(id=..., name=...)` | `Product(id=..., name=...).save()` | `await Product(id=..., name=...).save()` |
| Insert if not exists | `Product.if_not_exists().create(...)` | `Product(...).insert()` | `await Product(...).insert()` |
| With TTL | `Product.ttl(60).create(...)` | `Product(...).save(ttl=60)` | `await Product(...).save(ttl=60)` |

#### Read / Query

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
| Chained filters | `.filter(a=1).filter(b=2)` | `.find(a=1).filter(b=2).all()` | `await .find(a=1).filter(b=2).all()` |

#### Update

| Operation | cqlengine | coodie (sync) — after Phase 3 | coodie (async) — after Phase 3 |
|---|---|---|---|
| Instance update | `product.name = "New"; product.save()` | `product.update(name="New")` | `await product.update(name="New")` |
| Bulk update | `Product.objects.filter(...).update(price=9.99)` | `Product.find(...).update(price=9.99)` | `await Product.find(...).update(price=9.99)` |

#### Delete

| Operation | cqlengine | coodie (sync) | coodie (async) |
|---|---|---|---|
| Instance delete | `product.delete()` | `product.delete()` | `await product.delete()` |
| Bulk delete | `Product.objects.filter(...).delete()` | `Product.find(...).delete()` | `await Product.find(...).delete()` |

### 5.6 Column Type Migration Reference

| cqlengine | coodie (Python type annotation) |
|---|---|
| `columns.Text()` | `str` |
| `columns.Ascii()` | `Annotated[str, Ascii()]` *(Phase 1)* |
| `columns.Integer()` | `int` |
| `columns.BigInt()` | `Annotated[int, BigInt()]` *(Phase 1)* |
| `columns.SmallInt()` | `Annotated[int, SmallInt()]` *(Phase 1)* |
| `columns.TinyInt()` | `Annotated[int, TinyInt()]` *(Phase 1)* |
| `columns.VarInt()` | `Annotated[int, VarInt()]` *(Phase 1)* |
| `columns.Float()` | `float` |
| `columns.Double()` | `Annotated[float, Double()]` *(Phase 1)* |
| `columns.Decimal()` | `Decimal` |
| `columns.Boolean()` | `bool` |
| `columns.UUID(primary_key=True)` | `Annotated[UUID, PrimaryKey()]` |
| `columns.UUID()` | `UUID` |
| `columns.TimeUUID()` | `Annotated[UUID, TimeUUID()]` *(Phase 1)* |
| `columns.DateTime()` | `datetime` |
| `columns.Date()` | `date` |
| `columns.Time()` | `Annotated[time, Time()]` *(Phase 1)* |
| `columns.Blob()` | `bytes` |
| `columns.Inet()` | `IPv4Address` or `IPv6Address` |
| `columns.Counter()` | `Annotated[int, Counter()]` |
| `columns.List(columns.Text)` | `list[str]` |
| `columns.Set(columns.Integer)` | `set[int]` |
| `columns.Map(columns.Text, columns.Integer)` | `dict[str, int]` |
| `columns.Tuple(columns.Text, columns.Integer)` | `tuple[str, int]` |
| `columns.UserDefinedType(Address)` | `Address` (Pydantic model extending `UserType`) *(Phase 6)* |

### 5.7 Column Options Migration

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

### 5.8 Batch Migration

#### cqlengine

```python
from cassandra.cqlengine.query import BatchQuery

with BatchQuery() as b:
    Product.batch(b).create(id=uuid4(), name="A", ...)
    Product.batch(b).create(id=uuid4(), name="B", ...)
```

#### coodie (Phase 7)

```python
from coodie.sync import BatchQuery  # or coodie.aio.AsyncBatchQuery

with BatchQuery() as batch:
    Product(id=uuid4(), name="A", ...).save(batch=batch)
    Product(id=uuid4(), name="B", ...).save(batch=batch)
```

### 5.9 User-Defined Types Migration

#### cqlengine

```python
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine import columns

class Address(UserType):
    street = columns.Text()
    zipcode = columns.Integer()

class User(Model):
    id = columns.UUID(primary_key=True)
    addr = columns.UserDefinedType(Address)
```

#### coodie (Phase 6)

```python
from coodie.usertype import UserType

class Address(UserType):
    street: str
    zipcode: int

class User(Document):
    id: Annotated[UUID, PrimaryKey()]
    addr: Address  # auto-detected as frozen<address>
```

### 5.10 Migration Checklist

Use this checklist when converting a cqlengine application to coodie:

- [ ] **Replace imports:** `cassandra.cqlengine` → `coodie` / `coodie.sync` / `coodie.aio`
- [ ] **Convert models:** `Model` → `Document`; `columns.*` → Python type annotations with `Annotated` markers
- [ ] **Convert column options:** `primary_key=True` → `PrimaryKey()`; `index=True` → `Indexed()`; etc.
- [ ] **Convert `__table_name__` / `__keyspace__`:** Move to inner `Settings` class
- [ ] **Convert connection setup:** `connection.setup()` → `init_coodie()`
- [ ] **Convert table sync:** `sync_table(Model)` → `Model.sync_table()`
- [ ] **Convert creates:** `Model.create(...)` → `Model(...).save()` (or `.create()` after Phase 8)
- [ ] **Convert queries:** `Model.objects.filter(...)` → `Model.find(...)`
- [ ] **Convert `objects.get()`:** `Model.objects.get(...)` → `Model.get(...)`
- [ ] **Convert batch operations:** `BatchQuery()` → coodie's `BatchQuery()` (Phase 7)
- [ ] **Convert UDTs:** `UserType` → coodie `UserType(BaseModel)` (Phase 6)
- [ ] **Handle async:** If migrating to async, add `await` before all Document and QuerySet terminal methods
- [ ] **Test thoroughly:** Run existing test suite against coodie to verify parity

---

## 6. References

### cqlengine Documentation

- [cassandra.cqlengine.models](https://python-driver.docs.scylladb.com/stable/api/cassandra/cqlengine/models.html) — Model class, table options, polymorphism
- [cassandra.cqlengine.columns](https://python-driver.docs.scylladb.com/stable/api/cassandra/cqlengine/columns.html) — All column types and options
- [cassandra.cqlengine.query](https://python-driver.docs.scylladb.com/stable/api/cassandra/cqlengine/query.html) — QuerySet API, filter operators, LWT
- [cassandra.cqlengine.usertype](https://python-driver.docs.scylladb.com/stable/api/cassandra/cqlengine/usertype.html) — User-Defined Types

### coodie Documentation

- [coodie rewrite plan](rewrite-coodie-plan.md) — Original architecture and design decisions
- [Integration test coverage](https://github.com/scylladb/coodie/blob/341a470b35bf60696e2c067d6a22aaf448461102/docs/plans/integration-test-coverage.md) — Current test coverage and gaps
- Source code: `src/coodie/` — current implementation
