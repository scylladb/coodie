# Migration Gotchas: cqlengine → coodie

Comprehensive list of breaking changes, subtle differences, and common pitfalls
when migrating from cqlengine to coodie. Each gotcha includes an example of the
broken pattern and the correct fix.

---

## G1: No `Model.objects` Attribute

**Impact:** `AttributeError: type object 'Product' has no attribute 'objects'`

cqlengine queries start from `Model.objects`. coodie uses class methods directly.

```python
# ❌ cqlengine pattern — fails in coodie
products = Product.objects.filter(brand="Acme").all()

# ✅ coodie
products = Product.find(brand="Acme").all()
```

**Affected patterns:** `.objects.all()`, `.objects.filter()`, `.objects.get()`,
`.objects.count()`, `.objects.first()`.

---

## G2: Fields Without Defaults Are Required

**Impact:** `pydantic.ValidationError` when instantiating a model without all fields.

In cqlengine, `columns.Text()` without `required=True` is implicitly optional
(Cassandra stores `null`). In coodie, a field without a default is **required**
by Pydantic v2.

```python
# cqlengine — this is optional, stores null
description = columns.Text()

# ❌ coodie — this is REQUIRED, Pydantic raises ValidationError if omitted
description: str

# ✅ coodie — explicitly optional
description: Optional[str] = None
```

**Rule of thumb:** If the cqlengine field doesn't have `required=True`, make it
`Optional[T] = None` in coodie.

---

## G3: Table Metadata Moves to `Settings` Class

**Impact:** Table created with the class name instead of the intended table name.

```python
# ❌ Ignored in coodie — has no effect
class Product(Document):
    __table_name__ = "products"
    __keyspace__ = "catalog"

# ✅ Use Settings inner class
class Product(Document):
    class Settings:
        name = "products"
        keyspace = "catalog"
```

**Also applies to:** `__default_ttl__` → `Settings.__default_ttl__`,
`__options__` → `Settings.__options__`, `__connection__` → `Settings.connection`
(no dunders; the name passed to `init_coodie(name=...)`).

---

## G4: `default=callable` Requires `Field(default_factory=...)`

**Impact:** Assigning the callable itself stores the function object as the
default instead of calling it per instance.

```python
# cqlengine — callable default
id = columns.UUID(primary_key=True, default=uuid.uuid4)
tags = columns.List(columns.Text, default=list)

# ❌ coodie — default is the uuid4 function, not a UUID
id: Annotated[UUID, PrimaryKey()] = uuid4

# ✅ coodie — use Field(default_factory=...)
id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
tags: list[str] = []  # fine too: Pydantic copies mutable defaults per instance
```

**Applies to:** Any field with `default=<callable>`, especially `uuid4`,
`uuid1`, `datetime.now`.

---

## G5: `sync_table()` Is Now a Class Method

**Impact:** `NameError` — no `sync_table` function to import.

```python
# ❌ cqlengine pattern
from cassandra.cqlengine.management import sync_table
sync_table(Product)

# ✅ coodie
Product.sync_table()          # sync
await Product.sync_table()    # async
```

---

## G6: Connection Setup Signature Differs

**Impact:** Connection fails with unexpected keyword argument errors.

```python
# ❌ cqlengine
from cassandra.cqlengine import connection
connection.setup(["127.0.0.1"], "catalog", protocol_version=4)

# ✅ coodie (sync)
from coodie.sync import init_coodie
init_coodie(hosts=["127.0.0.1"], keyspace="catalog")

# ✅ coodie (async)
from coodie.aio import init_coodie
await init_coodie(hosts=["127.0.0.1"], keyspace="catalog")
```

---

## G7: Batch API Is Different

**Impact:** `AttributeError` — no `.batch()` method on Document.

```python
# ❌ cqlengine
with BatchQuery() as b:
    Product.batch(b).create(id=uuid4(), name="A")

# ✅ coodie
from coodie.sync import BatchQuery

with BatchQuery() as batch:
    Product(id=uuid4(), name="A").save(batch=batch)
```

---

## G8: Exception Classes Renamed

**Impact:** Uncaught exceptions in `try/except` blocks.

```python
# ❌ cqlengine
try:
    product = Product.get(id=pid)
except Product.DoesNotExist:
    ...

# ✅ coodie
from coodie.exceptions import DocumentNotFound

try:
    product = Product.get(id=pid)
except DocumentNotFound:
    ...
```

| cqlengine Exception | coodie Exception |
|---------------------|------------------|
| `Model.DoesNotExist` | `coodie.exceptions.DocumentNotFound` |
| `Model.MultipleObjectsReturned` | `coodie.exceptions.MultipleDocumentsFound` |
| `LWTException` | _(not raised)_ — check `LWTResult.applied`, see [G14](#g14-conditional-insert-return-type-differs-by-api-path) |

---

## G9: UDT Column Wrapper Removed

**Impact:** Unnecessary `columns.UserDefinedType()` wrapper causes errors.

```python
# ❌ cqlengine pattern
home = columns.UserDefinedType(Address)
addresses = columns.List(columns.UserDefinedType(Address))

# ✅ coodie — use the type directly
home: Address
addresses: list[Address] = Field(default_factory=list)
```

---

## G10: Counter Columns Require `CounterDocument`

**Impact:** Counter columns on a regular `Document` do not work correctly.

```python
# ❌ Wrong — counter on regular Document
class PageViews(Document):
    url: Annotated[str, PrimaryKey()]
    views: Annotated[int, Counter()] = 0

# ✅ Correct — inherit from CounterDocument
class PageViews(CounterDocument):
    url: Annotated[str, PrimaryKey()]
    views: Annotated[int, Counter()] = 0

# Use increment/decrement instead of assignment
page.increment(views=1)
page.decrement(views=1)
```

CQL restriction: counter and non-counter columns cannot coexist in the same table.

---

## G11: `partition_key=True` Is Not the Same as `PrimaryKey()`

**Impact:** Composite partition keys produce wrong CQL.

In cqlengine, multiple columns can have `primary_key=True, partition_key=True`
to form a composite partition key. In coodie, use `partition_key_index=N`:

```python
# cqlengine
tenant_id = columns.UUID(primary_key=True, partition_key=True)
bucket = columns.Text(primary_key=True, partition_key=True)
created_at = columns.DateTime(primary_key=True, clustering_order="DESC")

# coodie
tenant_id: Annotated[UUID, PrimaryKey(partition_key_index=0)]
bucket: Annotated[str, PrimaryKey(partition_key_index=1)]
created_at: Annotated[datetime, ClusteringKey(order="DESC")]
```

The `partition_key_index` controls the order of columns within the
composite partition key.

---

## G12: `clustering_order` Moves to `ClusteringKey(order=...)`

**Impact:** Clustering columns created without the intended sort order.

```python
# cqlengine
created_at = columns.DateTime(primary_key=True, clustering_order="DESC")

# coodie
created_at: Annotated[datetime, ClusteringKey(order="DESC")]
```

---

## G13: Query Filter Operator Syntax Is Preserved

**Impact:** None — this works the same way. Noting it to avoid confusion.

Both cqlengine and coodie use double-underscore filter operators:

```python
# cqlengine
Product.objects.filter(price__gt=10.0)

# coodie — same operators
Product.find(price__gt=10.0).all()
```

Supported operators: `__gt`, `__gte`, `__lt`, `__lte`, `__in`, `__contains`,
`__like` (requires SASI/SAI index), `__token__gt`, `__token__gte`,
`__token__lt`, `__token__lte`.

---

## G14: Conditional Insert Return Type Differs by API Path

**Impact:** Duplicate-insert checks silently stop working. cqlengine raises
`LWTException` when the insert is not applied; coodie never raises.

```python
# cqlengine
try:
    Product.if_not_exists().create(id=pid, name="Widget")
except LWTException:
    ...

# coodie — QuerySet conditional create returns LWTResult
result = Product.find().if_not_exists().create(id=pid, name="Widget")
if result and not result.applied:
    ...  # what used to be the LWTException branch

# ❌ coodie instance insert does IF NOT EXISTS, but returns None either way
Product(id=pid, name="Widget").insert()
```

---

## G15: `ttl()` Chain Method Replaced by Parameter

**Impact:** No `.ttl()` chain method on the model.

```python
# cqlengine
Product.ttl(60).create(id=pid, name="Widget")

# coodie — pass ttl as parameter
Product(id=pid, name="Widget").save(ttl=60)
```

---

## G16: `save()` Rewrites Every Column

**Impact:** None for correctness — assign + `save()` still persists. But
`save()` is a full `INSERT` of every column (unset ones written as null),
while cqlengine's `save()` on a loaded instance only updated changed columns.

```python
# cqlengine — UPDATE of changed columns only
product.name = "New Name"
product.save()

# coodie — works, but writes all columns
product.name = "New Name"
product.save()

# coodie — preferred for partial writes: UPDATE of the given columns only
product.update(name="New Name")
```

---

## G17: Frozen Collections Need Explicit Marker

**Impact:** Collection not stored as frozen in CQL when it should be.

```python
# cqlengine — frozen is automatic for UDT collections
addresses = columns.List(columns.UserDefinedType(Address))  # always frozen

# coodie — UDTs in collections are auto-frozen, but plain frozen collections
# need the Frozen() marker
coords: Annotated[list[float], Frozen()] = Field(default_factory=list)
```

Note: UDTs nested inside collections are automatically `frozen<>` — you only
need the explicit `Frozen()` marker for plain collection types.
