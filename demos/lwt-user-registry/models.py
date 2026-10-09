"""User Registry document definitions for the coodie LWT demo."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import Field

from coodie.aio import Document
from coodie.fields import Indexed, PrimaryKey


class UserRegistration(Document):
    """A registered user identity.

    Partition key = ``username`` (text) — one row per username.
    LWT ``INSERT IF NOT EXISTS`` enforces global uniqueness.
    """

    username: Annotated[str, PrimaryKey()]
    email: Annotated[str, Indexed()]
    display_name: str
    dimension: Annotated[str, Indexed()]
    registered_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    user_id: UUID = Field(default_factory=uuid4)

    class Settings:
        name = "user_registrations"
        keyspace = "registry"


class UserProfile(Document):
    """Extended profile for a registered user.

    Partition key = ``user_id``.
    Uses ``UPDATE IF EXISTS`` / ``UPDATE IF <conditions>``
    (optimistic locking) to prevent lost-update races.
    """

    user_id: Annotated[UUID, PrimaryKey()]
    username: str
    bio: str | None = None
    status: str = "active"
    version: int = 1
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    class Settings:
        name = "user_profiles"
        keyspace = "registry"
