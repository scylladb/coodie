"""Mixed-case, quoted and reserved-word table names (#298) — merged sync + async."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID, uuid4

import pytest
from pydantic import Field

from coodie.aio.document import Document as AsyncDocument
from coodie.fields import PrimaryKey
from coodie.sync.document import Document as SyncDocument
from tests.conftest import _maybe_await

pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio(loop_scope="session"),
]


def _models(base: type, table: str) -> tuple[type, type]:
    class V1(base):  # type: ignore[valid-type,misc]
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        name: str = ""

        class Settings:
            name = table
            keyspace = "test_ks"

    class V2(base):  # type: ignore[valid-type,misc]
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        name: str = ""
        extra: str | None = None

        class Settings:
            name = table
            keyspace = "test_ks"

    return V1, V2


@pytest.mark.parametrize(
    ("table", "stored"),
    [("ItMixedCase", "itmixedcase"), ('"ItQuotedCase"', "ItQuotedCase"), ("order", "order")],
)
async def test_sync_table_adds_column_and_round_trips(coodie_driver, execute_raw_fn, variant, table, stored) -> None:
    V1, V2 = _models(SyncDocument if variant == "sync" else AsyncDocument, table)
    await _maybe_await(V1.drop_table)
    await _maybe_await(V1.sync_table)
    await _maybe_await(V2.sync_table)

    rows = await _maybe_await(
        execute_raw_fn,
        "SELECT column_name FROM system_schema.columns WHERE keyspace_name = ? AND table_name = ?",
        ["test_ks", stored],
    )
    assert {r["column_name"] for r in rows} == {"id", "name", "extra"}

    doc = V2(name="n", extra="e")
    await _maybe_await(doc.save)
    fetched = await _maybe_await(V2.get, id=doc.id)
    assert fetched.extra == "e"
    await _maybe_await(V1.drop_table)
