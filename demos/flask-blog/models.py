"""Blog document definitions for the coodie Flask demo."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import Field

from coodie.fields import ClusteringKey, Indexed, PrimaryKey
from coodie.sync import Document


class Post(Document):
    """A blog post.

    Partition key = ``id``; secondary indexes on ``author`` and ``category``.
    Tags stored as a list field.
    """

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    title: str
    author: Annotated[str, Indexed()]
    category: Annotated[str, Indexed()]
    content: str | None = None
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    class Settings:
        name = "posts"
        keyspace = "blog"


class Comment(Document):
    """A comment on a blog post.

    Partition key = ``post_id``; clustering = ``created_at DESC`` (newest-first).
    """

    post_id: Annotated[UUID, PrimaryKey()]
    created_at: Annotated[datetime, ClusteringKey(order="DESC")] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    id: UUID = Field(default_factory=uuid4)
    author: str
    content: str | None = None

    class Settings:
        name = "comments"
        keyspace = "blog"
