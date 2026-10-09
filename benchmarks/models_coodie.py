"""coodie model definitions for benchmarks.

These mirror the cqlengine models so that benchmarks compare equivalent schemas.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import Field, field_validator

from coodie.fields import ClusteringKey, Indexed, PrimaryKey, Vector, VectorIndex
from coodie.sync.document import Document


class CoodieProduct(Document):
    """Product model — basic CRUD benchmark target."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    brand: Annotated[str, Indexed()] = "Unknown"
    category: Annotated[str, Indexed()] = "general"
    price: float = 0.0
    tags: list[str] = Field(default_factory=list)
    description: str | None = None

    @field_validator("tags", mode="before")
    @classmethod
    def _coerce_tags(cls, v: object) -> object:
        return v if v is not None else []

    class Settings:
        name = "bench_products"
        keyspace = "bench_ks"


class CoodieReview(Document):
    """Review model — composite key benchmark target."""

    product_id: Annotated[UUID, PrimaryKey()]
    created_at: Annotated[datetime, ClusteringKey(order="DESC")] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    author: str
    rating: Annotated[int, Indexed()] = 0

    class Settings:
        name = "bench_reviews"
        keyspace = "bench_ks"


class CoodieEvent(Document):
    """Event model — used for batch and bulk benchmarks."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    event_type: str
    payload: str = ""

    class Settings:
        name = "bench_events"
        keyspace = "bench_ks"


# Vector dimensions used across vector benchmarks (small to keep inserts fast)
BENCH_VECTOR_DIMS = 16


class CoodieVectorProduct(Document):
    """Product with a vector embedding — ANN search benchmark target."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    embedding: Annotated[
        list[float],
        Vector(dimensions=BENCH_VECTOR_DIMS),
        VectorIndex(similarity_function="COSINE"),
    ] = Field(default_factory=list)

    class Settings:
        name = "bench_vector_products"
        keyspace = "bench_vector_ks"
