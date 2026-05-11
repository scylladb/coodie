"""Polymorphic CMS models — single-table inheritance with Discriminator column.

All content types (Article, Video, Podcast) share the ``contents`` table.
The ``content_type`` discriminator column lets coodie route queries to the
correct subclass automatically.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Optional
from uuid import UUID, uuid4

from pydantic import Field

from coodie.aio import Document
from coodie.fields import Discriminator, Indexed, PrimaryKey


class Content(Document):
    """Base content document — the single table for all content types.

    Partition key = ``id``; ``content_type`` is the discriminator column.
    """

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    content_type: Annotated[str, Discriminator()] = ""
    title: str
    author: Annotated[str, Indexed()]
    summary: Optional[str] = None
    published: bool = False
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    class Settings:
        name = "contents"
        keyspace = "cms"


class Article(Content):
    """A written article with body text and word count."""

    body: Optional[str] = None
    word_count: int = 0

    class Settings:
        __discriminator_value__ = "article"


class Video(Content):
    """A video entry with URL, duration, and resolution."""

    video_url: Optional[str] = None
    duration_seconds: int = 0
    resolution: str = "1080p"

    class Settings:
        __discriminator_value__ = "video"


class Podcast(Content):
    """A podcast episode with audio URL, duration, and episode number."""

    audio_url: Optional[str] = None
    duration_seconds: int = 0
    episode_number: int = 0

    class Settings:
        __discriminator_value__ = "podcast"
