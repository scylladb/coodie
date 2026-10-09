"""Product catalog models with materialized views for the coodie demo."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, ClassVar
from uuid import UUID, uuid4

from pydantic import Field

from coodie.aio import Document, MaterializedView
from coodie.fields import ClusteringKey, Indexed, PrimaryKey


class Product(Document):
    """A product in the catalog (base table).

    Partition key = ``id``; secondary indexes on ``category`` and ``brand``.
    """

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    category: Annotated[str, Indexed()]
    brand: Annotated[str, Indexed()]
    price: float
    description: str | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    class Settings:
        name = "products"
        keyspace = "viewdemo"


class ProductByCategory(MaterializedView):
    """Materialized view: products partitioned by category.

    Enables efficient ``SELECT * FROM products_by_category WHERE category = ?``
    without ``ALLOW FILTERING``.
    """

    category: Annotated[str, PrimaryKey()]
    id: Annotated[UUID, ClusteringKey()]
    name: str
    brand: str
    price: float
    description: str | None = None
    created_at: datetime | None = None

    class Settings:
        name = "products_by_category"
        keyspace = "viewdemo"
        __base_table__ = "products"
        __view_columns__: ClassVar[list[str]] = ["*"]
        __where_clause__ = '"category" IS NOT NULL AND "id" IS NOT NULL'


class ProductByBrand(MaterializedView):
    """Materialized view: products partitioned by brand.

    Enables efficient ``SELECT * FROM products_by_brand WHERE brand = ?``
    without ``ALLOW FILTERING``.
    """

    brand: Annotated[str, PrimaryKey()]
    id: Annotated[UUID, ClusteringKey()]
    name: str
    category: str
    price: float
    description: str | None = None
    created_at: datetime | None = None

    class Settings:
        name = "products_by_brand"
        keyspace = "viewdemo"
        __base_table__ = "products"
        __view_columns__: ClassVar[list[str]] = ["*"]
        __where_clause__ = '"brand" IS NOT NULL AND "id" IS NOT NULL'
