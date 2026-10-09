"""Article document definitions for the coodie collections demo."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import Field

from coodie.aio import Document
from coodie.fields import ClusteringKey, Frozen, Indexed, PrimaryKey


class Article(Document):
    """A tagged article showcasing CQL collection types.

    Partition key = ``article_id`` (UUID).

    Collection fields:
    - ``tags``       → CQL ``set<text>``   — unique labels, mutated via ``add__`` / ``remove__``
    - ``metadata``   → CQL ``map<text, text>`` — key-value properties, mutated via ``add__`` / ``remove__``
    - ``revisions``  → CQL ``list<text>``  — ordered history, mutated via ``append__`` / ``prepend__``
    """

    article_id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    title: str
    author: Annotated[str, Indexed()]
    tags: set[str] = Field(default_factory=set)
    metadata: dict[str, str] = Field(default_factory=dict)
    revisions: list[str] = Field(default_factory=list)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    class Settings:
        name = "articles"
        keyspace = "tagmind"


class FrozenTagSnapshot(Document):
    """Demonstrates a frozen collection column.

    ``frozen_tags`` is stored as ``frozen<set<text>>`` — immutable once written,
    compared by value, and usable as a clustering key or in secondary indexes.
    """

    article_id: Annotated[UUID, PrimaryKey()]
    snapshot_at: Annotated[datetime, ClusteringKey()]
    frozen_tags: Annotated[set[str] | None, Frozen()] = None
    note: str = ""

    class Settings:
        name = "tag_snapshots"
        keyspace = "tagmind"
