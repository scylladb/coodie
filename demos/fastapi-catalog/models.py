"""Product Catalog document definitions for the coodie FastAPI demo."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import Field

from coodie.aio import Document
from coodie.fields import ClusteringKey, Indexed, PrimaryKey


class Product(Document):
    """A product in the catalog.

    Partition key = ``id``; secondary indexes on ``brand`` and ``category``.
    """

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    brand: Annotated[str, Indexed()]
    category: Annotated[str, Indexed()]
    price: float
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    class Settings:
        name = "products"
        keyspace = "catalog"


class Review(Document):
    """A product review.

    Partition key = ``product_id``; clustering = ``created_at DESC`` (newest-first).
    """

    product_id: Annotated[UUID, PrimaryKey()]
    created_at: Annotated[datetime, ClusteringKey(order="DESC")] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    id: UUID = Field(default_factory=uuid4)
    author: str
    rating: Annotated[int, Indexed()]
    content: str | None = None

    class Settings:
        name = "reviews"
        keyspace = "catalog"
