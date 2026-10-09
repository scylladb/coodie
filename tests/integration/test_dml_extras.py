"""Integration tests for the Phase 1 CQL gap features.

Covers docs/plans/cql-gap-analysis.md Phase 1 (§4.2):
  - ``Document.truncate()``
  - ``QuerySet.distinct()``
  - ``QuerySet.group_by()``
  - ``QuerySet.sum()/avg()/min()/max()/aggregate()``
  - ``filter(col__isnull=...)`` / ``is_not_null()`` / ``is_null()``
  - ``QuerySet.cast()``

Every test runs twice (sync and async) via the ``variant`` fixture.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from tests.conftest import _maybe_await

pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio(loop_scope="session"),
]


async def _seed(SensorReading, sid: str, values: list[float]) -> None:
    await _maybe_await(SensorReading.sync_table)
    for i, v in enumerate(values):
        await _maybe_await(SensorReading(sensor_id=sid, reading_time=f"t{i}", value=v).save)


class TestDmlExtras:
    async def test_truncate(self, coodie_driver, SensorReading) -> None:
        sid = f"trunc-{uuid4().hex[:8]}"
        await _seed(SensorReading, sid, [1.0, 2.0])
        assert await _maybe_await(SensorReading.find(sensor_id=sid).count) == 2

        await _maybe_await(SensorReading.truncate)

        assert await _maybe_await(SensorReading.find(sensor_id=sid).count) == 0

    async def test_distinct_partition_keys(self, coodie_driver, SensorReading) -> None:
        a, b = f"dist-a-{uuid4().hex[:8]}", f"dist-b-{uuid4().hex[:8]}"
        await _seed(SensorReading, a, [1.0, 2.0, 3.0])
        await _seed(SensorReading, b, [4.0, 5.0])

        rows = await _maybe_await(
            SensorReading.find(sensor_id__in=[a, b]).only("sensor_id").distinct().values_list("sensor_id").all
        )

        assert sorted(rows) == sorted([(a,), (b,)])

    async def test_group_by_partition_key(self, coodie_driver, SensorReading) -> None:
        a, b = f"grp-a-{uuid4().hex[:8]}", f"grp-b-{uuid4().hex[:8]}"
        await _seed(SensorReading, a, [1.0, 2.0, 3.0])
        await _seed(SensorReading, b, [4.0, 5.0])

        docs = await _maybe_await(SensorReading.find(sensor_id__in=[a, b]).group_by("sensor_id").all)

        # One row per group, not one per clustering row.
        assert sorted(d.sensor_id for d in docs) == sorted([a, b])

    async def test_aggregates(self, coodie_driver, SensorReading) -> None:
        sid = f"agg-{uuid4().hex[:8]}"
        await _seed(SensorReading, sid, [1.5, 2.5, 5.0])
        qs = SensorReading.find(sensor_id=sid)

        assert await _maybe_await(qs.sum, "value") == pytest.approx(9.0)
        assert await _maybe_await(qs.avg, "value") == pytest.approx(3.0)
        assert await _maybe_await(qs.min, "value") == pytest.approx(1.5)
        assert await _maybe_await(qs.max, "value") == pytest.approx(5.0)

        result = await _maybe_await(qs.aggregate, total="sum(value)", top="max(value)")
        assert result == {"total": pytest.approx(9.0), "top": pytest.approx(5.0)}

    async def test_isnull_rejected_outside_materialized_views(self, coodie_driver, Product) -> None:
        """ScyllaDB only accepts ``IS NOT NULL`` in materialized view definitions.

        coodie renders the restriction, but the server rejects it on a plain
        SELECT, and ``IS NULL`` is not valid CQL at all.  Pin that behaviour so
        a server-side change is noticed.
        """
        await _maybe_await(Product.sync_table)
        base = Product.find(brand="any").allow_filtering()

        for qs in (base.filter(description__isnull=False), base.is_not_null("description")):
            with pytest.raises(Exception, match="(?i)materialized view"):
                await _maybe_await(qs.all)

        for qs in (base.filter(description__isnull=True), base.is_null("description")):
            with pytest.raises(Exception):  # noqa: B017 - syntax error, message is driver-specific
                await _maybe_await(qs.all)

    async def test_cast(self, coodie_driver, SensorReading) -> None:
        sid = f"cast-{uuid4().hex[:8]}"
        await _seed(SensorReading, sid, [2.5])

        rows = await _maybe_await(
            SensorReading.find(sensor_id=sid).only("sensor_id").cast("value", "text").all, lazy=True
        )

        assert len(rows) == 1
        # The cast column isn't a model field, so read it from the raw row.
        assert rows[0]._raw_data["cast(value as text)"] == "2.5"
