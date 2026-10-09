"""Cargo manifest document definitions for the coodie batch-importer demo."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import Field

from coodie.fields import ClusteringKey, Indexed, PrimaryKey
from coodie.sync import Document


class CargoEntry(Document):
    """A single cargo manifest entry.

    Partition key = ``id``; secondary indexes on ``origin_system``,
    ``destination_system``, ``cargo_type``, and ``status``.
    """

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    origin_system: Annotated[str, Indexed()]
    destination_system: Annotated[str, Indexed()]
    cargo_type: Annotated[str, Indexed()]
    mass_kg: float
    status: Annotated[str, Indexed()] = "pending"

    class Settings:
        name = "cargo_entries"
        keyspace = "cargo"


class ShipmentLog(Document):
    """Event log for a cargo shipment.

    Partition key = ``shipment_id``; clustering = ``logged_at DESC``
    (most-recent event first).
    """

    shipment_id: Annotated[UUID, PrimaryKey()]
    logged_at: Annotated[datetime, ClusteringKey(order="DESC")] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    entry_id: UUID
    event_type: Annotated[str, Indexed()]
    notes: str | None = None

    class Settings:
        name = "shipment_logs"
        keyspace = "cargo"
