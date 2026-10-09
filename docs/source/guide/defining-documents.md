# Defining Documents

A **Document** in coodie is a Python class that maps to a Cassandra table.
It inherits from `pydantic.BaseModel`, so you get validation, serialisation,
and type hints for free.

## Basic Document

```python
from coodie.sync import Document
from coodie.fields import PrimaryKey, ClusteringKey
from typing import Annotated, Optional
from uuid import UUID
from datetime import datetime

class BlogPost(Document):
    blog_id: Annotated[UUID, PrimaryKey()]
    published_at: Annotated[datetime, ClusteringKey(order="DESC")]
    title: str
    body: str
    author: Optional[str] = None
    views: int = 0

    class Settings:
        name = "blog_posts"
        keyspace = "my_ks"
```

This maps to the CQL table:

```sql
CREATE TABLE my_ks.blog_posts (
    blog_id uuid,
    published_at timestamp,
    title text,
    body text,
    author text,
    views int,
    PRIMARY KEY (blog_id, published_at)
) WITH CLUSTERING ORDER BY (published_at DESC);
```

## The `Settings` Inner Class

Every Document can declare a `Settings` inner class to control table metadata:

| Setting | Default | Description |
|---------|---------|-------------|
| `name` | Snake-cased class name | CQL table name |
| `keyspace` | Driver's default keyspace | Target keyspace |

```python
class Product(Document):
    id: Annotated[UUID, PrimaryKey()]
    name: str

    class Settings:
        name = "products"          # Table name in Cassandra
        keyspace = "ecommerce"     # Keyspace (overrides the driver default)
```

Table, keyspace and UDT names follow CQL rules: unquoted names are
case-insensitive (`"MyTable"` is the table `mytable`), and reserved words such
as `"order"` are quoted for you. To make a name case-sensitive, include the
double quotes: `name = '"MyTable"'`.

If you omit `Settings.name`, coodie uses the snake-cased class name:
`BlogPost` → `blog_post`, `HTTPRequest` → `http_request`.

## Field Defaults

Because Document inherits from Pydantic's `BaseModel`, you can use all the
standard default-value patterns:

```python
from pydantic import Field
from uuid import uuid4

class Order(Document):
    # Required field — must be provided at instantiation
    customer_name: str

    # Default value
    status: str = "pending"

    # Default factory — generates a new UUID each time
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)

    # Optional field — can be None
    notes: Optional[str] = None
```

## Pydantic Integration

Since Document extends `pydantic.BaseModel`, you get:

- **Validation** — type mismatches raise `ValidationError` at instantiation
- **Serialisation** — `.model_dump()` returns a plain dict
- **Schema generation** — `.model_json_schema()` produces JSON Schema

```python
# Pydantic validation in action
try:
    p = Product(id="not-a-uuid", name=42)
except Exception as e:
    print(e)  # Pydantic ValidationError with details

# Serialise to dict
p = Product(id=uuid4(), name="Widget")
print(p.model_dump())
# {'id': UUID('...'), 'name': 'Widget'}
```

## Schema Sync

After defining a Document, call `sync_table()` to create or update the
table in Cassandra:

```python
# Sync — creates the table if it doesn't exist,
# or adds new columns if you've added fields
Product.sync_table()

# Async equivalent
await Product.sync_table()
```

`sync_table()` is idempotent — call it as many times as you like.
It will **not** drop columns or change column types.

## Counter Documents

For Cassandra counter tables, use `CounterDocument`:

```python
from coodie.sync import CounterDocument
from coodie.fields import PrimaryKey, Counter

class PageViews(CounterDocument):
    page_url: Annotated[str, PrimaryKey()]
    views: Annotated[int, Counter()]
    unique_visitors: Annotated[int, Counter()]

    class Settings:
        name = "page_views"
```

Counter documents use `increment()` / `decrement()` instead of `save()`.
See the CRUD guide for details.

## Materialized Views

For Cassandra materialized views, use `MaterializedView`:

```python
from coodie.sync import MaterializedView
from coodie.fields import PrimaryKey, ClusteringKey

class ProductsByCategory(MaterializedView):
    category: Annotated[str, PrimaryKey()]
    id: Annotated[UUID, ClusteringKey()]
    name: str
    price: float

    class Settings:
        name = "products_by_category"
        __base_table__ = "products"
```

Materialized views are read-only — `save()`, `insert()`, `update()`, and
`delete()` will raise `InvalidQueryError`.

## What's Next?

- {doc}`field-types` — every type annotation explained
- {doc}`keys-and-indexes` — primary keys, clustering keys, and secondary indexes
- {doc}`crud` — save, insert, update, delete, and query operations
