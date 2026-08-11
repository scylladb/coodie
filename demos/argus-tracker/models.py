"""Argus-inspired test tracker models for the coodie argus-tracker demo.

Demonstrates complex real-world patterns from scylladb/argus:

- **User** — secondary-index lookups, ``List[str]`` roles collection
- **TestRun** — composite partition key (``build_id``) + clustering
  (``start_time DESC``) for time-ordered test results within a build
- **Event** — compound partition key (``run_id`` + ``kind``) groups
  related events together; clustering by ``created_at DESC``
- **Notification** — partition by ``receiver``, ``TimeUUID`` clustering
  DESC for time-ordered notification feeds
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Dict, List, Optional
from uuid import UUID, uuid1, uuid4

from pydantic import Field, field_validator

from coodie.fields import ClusteringKey, Indexed, PrimaryKey, TimeUUID
from coodie.sync import Document


class User(Document):
    """A test-tracker user.

    Partition key = ``id``; secondary indexes on ``username``, ``email``,
    and ``api_token`` for fast lookups.  The ``roles`` list column stores
    a CQL ``list<text>`` of role names (e.g. ``["admin", "viewer"]``).
    """

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    username: Annotated[str, Indexed()] = ""
    full_name: str = ""
    email: Annotated[str, Indexed()] = ""
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    roles: List[str] = Field(default_factory=list)
    picture_id: Optional[UUID] = None
    api_token: Annotated[Optional[str], Indexed()] = None

    @field_validator("roles", mode="before")
    @classmethod
    def _coerce_roles(cls, v: object) -> object:
        """Coerce NULL roles from Cassandra into an empty list."""
        return v if v is not None else []

    class Settings:
        name = "argus_users"
        keyspace = "argus"


class TestRun(Document):
    """A CI/CD test run with composite primary key.

    Partition key = ``build_id``; clustering = ``start_time DESC``.
    This layout groups all runs of the same build together and surfaces
    the most recent run first — matching the argus pattern of querying
    "latest run for build X".

    Multiple secondary indexes enable lookups by ``id``, ``release_id``,
    ``assignee``, and ``status``.
    """

    build_id: Annotated[str, PrimaryKey()]
    start_time: Annotated[datetime, ClusteringKey(order="DESC")] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)
    release_id: Annotated[Optional[UUID], Indexed()] = None
    group_id: Optional[UUID] = None
    test_id: Optional[UUID] = None
    assignee: Annotated[Optional[UUID], Indexed()] = None
    status: Annotated[str, Indexed()] = "created"
    investigation_status: str = "not_investigated"
    heartbeat: int = 0
    end_time: Optional[datetime] = None
    build_job_url: Optional[str] = None
    scylla_version: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    @field_validator("tags", mode="before")
    @classmethod
    def _coerce_tags(cls, v: object) -> object:
        """Coerce NULL tags from Cassandra into an empty list."""
        return v if v is not None else []

    class Settings:
        name = "argus_test_runs"
        keyspace = "argus"


class Event(Document):
    """A test-run event with compound partition key.

    Partition key = ``(run_id, kind)``; clustering = ``created_at DESC``.
    This layout groups events by their originating run *and* kind (e.g.
    ``("run-uuid", "error")``), keeping each event category in a
    separate partition for efficient partition-scoped queries like
    "all errors for run X".
    """

    run_id: Annotated[UUID, PrimaryKey(partition_key_index=0)]
    kind: Annotated[str, PrimaryKey(partition_key_index=1)]
    created_at: Annotated[datetime, ClusteringKey(order="DESC")] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)
    user_id: Optional[UUID] = None
    body: str = ""
    severity: Annotated[str, Indexed()] = "info"
    metadata: Dict[str, str] = Field(default_factory=dict)

    @field_validator("metadata", mode="before")
    @classmethod
    def _coerce_metadata(cls, v: object) -> object:
        """Coerce NULL metadata from Cassandra into an empty dict."""
        return v if v is not None else {}

    class Settings:
        name = "argus_events"
        keyspace = "argus"


class Notification(Document):
    """A user notification with TimeUUID clustering.

    Partition key = ``receiver``; clustering = ``id DESC`` where ``id``
    is a ``timeuuid``.  TimeUUID ordering guarantees that notifications
    are stored in exact chronological order — even when two arrive in
    the same millisecond — and enables efficient "latest N notifications
    for user X" queries.
    """

    receiver: Annotated[UUID, PrimaryKey()]
    id: Annotated[UUID, TimeUUID(), ClusteringKey(order="DESC")] = Field(default_factory=uuid1)
    type: str = ""
    state: int = 0
    sender: Optional[UUID] = None
    source_type: str = ""
    source_id: Optional[UUID] = None
    title: str = ""
    content: str = ""

    class Settings:
        name = "argus_notifications"
        keyspace = "argus"
