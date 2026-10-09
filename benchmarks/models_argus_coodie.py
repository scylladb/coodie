"""coodie model definitions inspired by scylladb/argus patterns.

Equivalent coodie models matching the cqlengine Argus-style models.
"""

from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid1, uuid4

from pydantic import Field, field_validator

from coodie.fields import BigInt, ClusteringKey, Indexed, PrimaryKey, TimeUUID
from coodie.sync.document import Document


class CoodieArgusUser(Document):
    """User model — secondary-index lookups, List[str] roles, save-after-mutate."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    username: Annotated[str, Indexed()] = ""
    full_name: str = ""
    email: Annotated[str, Indexed()] = ""
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    roles: list[str] = Field(default_factory=list)
    picture_id: UUID | None = None
    api_token: Annotated[str | None, Indexed()] = None

    @field_validator("roles", mode="before")
    @classmethod
    def _coerce_roles(cls, v: object) -> object:
        return v if v is not None else []

    class Settings:
        name = "bench_argus_user"
        keyspace = "bench_ks"


class CoodieArgusTestRun(Document):
    """TestRun model — composite partition key + clustering, many indexes."""

    build_id: Annotated[str, PrimaryKey()]
    start_time: Annotated[datetime, ClusteringKey(order="DESC")] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)
    release_id: Annotated[UUID | None, Indexed()] = None
    group_id: Annotated[UUID | None, Indexed()] = None
    test_id: Annotated[UUID | None, Indexed()] = None
    assignee: Annotated[UUID | None, Indexed()] = None
    status: str = "created"
    investigation_status: str = "not_investigated"
    heartbeat: int = 0
    end_time: datetime | None = None
    build_job_url: str | None = None
    scylla_version: str | None = None

    class Settings:
        name = "bench_argus_test_run"
        keyspace = "bench_ks"


class CoodieArgusEvent(Document):
    """Event model — UUID partition + multiple indexes."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    release_id: Annotated[UUID | None, Indexed()] = None
    group_id: Annotated[UUID | None, Indexed()] = None
    test_id: Annotated[UUID | None, Indexed()] = None
    run_id: Annotated[UUID | None, Indexed()] = None
    user_id: Annotated[UUID | None, Indexed()] = None
    kind: Annotated[str, Indexed()] = ""
    body: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "bench_argus_event"
        keyspace = "bench_ks"


class CoodieArgusNotification(Document):
    """Notification model — partition by receiver, TimeUUID clustering DESC."""

    receiver: Annotated[UUID, PrimaryKey()]
    id: Annotated[UUID, TimeUUID(), ClusteringKey(order="DESC")] = Field(default_factory=uuid1)
    type: str = ""
    state: int = 0
    sender: UUID | None = None
    source_type: str = ""
    source_id: UUID | None = None
    title: str = ""
    content: str = ""

    class Settings:
        name = "bench_argus_notification"
        keyspace = "bench_ks"


class CoodieArgusComment(Document):
    """Comment model — partition by id, clustering by posted_at DESC."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    test_run_id: Annotated[UUID | None, Indexed()] = None
    user_id: Annotated[UUID | None, Indexed()] = None
    release_id: Annotated[UUID | None, Indexed()] = None
    posted_at: Annotated[int, BigInt(), ClusteringKey(order="DESC")] = 0
    message: str = ""
    mentions: list[UUID] = Field(default_factory=list)
    reactions: dict[str, int] = Field(default_factory=dict)

    @field_validator("mentions", mode="before")
    @classmethod
    def _coerce_mentions(cls, v: object) -> object:
        return v if v is not None else []

    @field_validator("reactions", mode="before")
    @classmethod
    def _coerce_reactions(cls, v: object) -> object:
        return v if v is not None else {}

    class Settings:
        name = "bench_argus_comment"
        keyspace = "bench_ks"
