"""Extended integration tests — merged sync + async.

Covers: all CQL types, collections, LWT, batch, composite keys,
ordering, schema migration, extended types, and QuerySet enhancements.
Every test runs twice (sync and async) via the ``variant`` fixture.
"""

from __future__ import annotations

import decimal
import ipaddress
from datetime import date, datetime, timezone
from datetime import time as dt_time
from uuid import uuid1, uuid4

import pytest

from tests.conftest import _maybe_await

pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio(loop_scope="session"),
]


class TestExtended:
    """Extended sync+async tests: all CQL types, collections, LWT, batch, ordering."""

    # ------------------------------------------------------------------
    # DDL
    # ------------------------------------------------------------------

    async def test_all_types_sync_table(self, coodie_driver, AllTypes) -> None:
        await _maybe_await(AllTypes.sync_table)

    async def test_event_sync_table(self, coodie_driver, Event) -> None:
        await _maybe_await(Event.sync_table)

    # ------------------------------------------------------------------
    # CQL scalar types round-trip
    # ------------------------------------------------------------------

    async def test_scalar_types_roundtrip(self, coodie_driver, AllTypes) -> None:
        """All supported scalar types survive a save/load round-trip."""
        await _maybe_await(AllTypes.sync_table)
        rid = uuid4()
        today = date.today()  # noqa: DTZ011 - any date value works for the round-trip
        now = datetime.now(timezone.utc).replace(microsecond=0)
        original = AllTypes(
            id=rid,
            flag=True,
            count=42,
            score=3.14,
            amount=decimal.Decimal("12.34"),
            blob_val=b"\x00\xff",
            ts=now,
            day=today,
            ip4=ipaddress.IPv4Address("10.0.0.1"),
            ip6=ipaddress.IPv6Address("::1"),
        )
        await _maybe_await(original.save)

        fetched = await _maybe_await(AllTypes.find_one, id=rid)
        assert fetched is not None
        assert fetched.flag is True
        assert fetched.count == 42
        assert abs(fetched.score - 3.14) < 0.01
        assert fetched.amount == decimal.Decimal("12.34")
        assert fetched.blob_val == b"\x00\xff"
        assert fetched.ts.replace(tzinfo=timezone.utc) == now
        assert fetched.day == today
        assert str(fetched.ip4) == "10.0.0.1"
        assert str(fetched.ip6) == "::1"

        await _maybe_await(AllTypes(id=rid).delete)

    # ------------------------------------------------------------------
    # Collection types
    # ------------------------------------------------------------------

    async def test_set_collection_roundtrip(self, coodie_driver, AllTypes) -> None:
        """set[str] column survives a save/load round-trip."""
        await _maybe_await(AllTypes.sync_table)
        rid = uuid4()
        await _maybe_await(AllTypes(id=rid, tags_set={"apple", "banana"}).save)

        fetched = await _maybe_await(AllTypes.find_one, id=rid)
        assert fetched is not None
        assert fetched.tags_set == {"apple", "banana"}

        await _maybe_await(AllTypes(id=rid).delete)

    async def test_map_collection_roundtrip(self, coodie_driver, AllTypes) -> None:
        """dict[str, int] column survives a save/load round-trip."""
        await _maybe_await(AllTypes.sync_table)
        rid = uuid4()
        await _maybe_await(AllTypes(id=rid, scores_map={"a": 1, "b": 2}).save)

        fetched = await _maybe_await(AllTypes.find_one, id=rid)
        assert fetched is not None
        assert fetched.scores_map == {"a": 1, "b": 2}

        await _maybe_await(AllTypes(id=rid).delete)

    # ------------------------------------------------------------------
    # LWT — INSERT IF NOT EXISTS
    # ------------------------------------------------------------------

    async def test_insert_if_not_exists_creates(self, coodie_driver, AllTypes) -> None:
        """insert() (IF NOT EXISTS) inserts when the row is absent."""
        await _maybe_await(AllTypes.sync_table)
        rid = uuid4()
        row = AllTypes(id=rid, count=7)
        await _maybe_await(row.insert)

        fetched = await _maybe_await(AllTypes.find_one, id=rid)
        assert fetched is not None
        assert fetched.count == 7

        await _maybe_await(AllTypes(id=rid).delete)

    async def test_insert_if_not_exists_no_overwrite(self, coodie_driver, AllTypes) -> None:
        """insert() (IF NOT EXISTS) does NOT overwrite an existing row."""
        await _maybe_await(AllTypes.sync_table)
        rid = uuid4()
        await _maybe_await(AllTypes(id=rid, count=1).save)

        # Second insert with a different count — must not overwrite
        await _maybe_await(AllTypes(id=rid, count=99).insert)

        fetched = await _maybe_await(AllTypes.find_one, id=rid)
        assert fetched is not None
        assert fetched.count == 1  # original value preserved

        await _maybe_await(AllTypes(id=rid).delete)

    # ------------------------------------------------------------------
    # Batch writes
    # ------------------------------------------------------------------

    async def test_batch_insert(self, coodie_driver, AllTypes, variant) -> None:
        """build_insert statements combined in a batch insert atomically."""
        from coodie.cql_builder import build_insert

        await _maybe_await(AllTypes.sync_table)
        table = AllTypes.Settings.name
        rid1, rid2 = uuid4(), uuid4()

        row1 = AllTypes(id=rid1, count=10)
        row2 = AllTypes(id=rid2, count=20)
        stmt1, p1 = build_insert(table, "test_ks", row1.model_dump())
        stmt2, p2 = build_insert(table, "test_ks", row2.model_dump())

        if variant == "sync":
            from coodie.batch import BatchQuery

            with BatchQuery() as batch:
                batch.add(stmt1, p1)
                batch.add(stmt2, p2)
        else:
            from coodie.batch import AsyncBatchQuery

            async with AsyncBatchQuery() as batch:
                batch.add(stmt1, p1)
                batch.add(stmt2, p2)

        assert await _maybe_await(AllTypes.find_one, id=rid1) is not None
        assert await _maybe_await(AllTypes.find_one, id=rid2) is not None

        await _maybe_await(AllTypes(id=rid1).delete)
        await _maybe_await(AllTypes(id=rid2).delete)

    # ------------------------------------------------------------------
    # Composite partition key + multiple clustering columns
    # ------------------------------------------------------------------

    async def test_composite_pk_and_clustering(self, coodie_driver, Event, QS) -> None:
        """Composite partition key rows are correctly partitioned and retrieved."""
        await _maybe_await(Event.sync_table)
        pa, pb = "alpha", f"beta_{uuid4().hex[:6]}"
        await _maybe_await(Event(partition_a=pa, partition_b=pb, seq=1, sub=3, payload="first").save)
        await _maybe_await(Event(partition_a=pa, partition_b=pb, seq=1, sub=2, payload="second").save)
        await _maybe_await(Event(partition_a=pa, partition_b=pb, seq=2, sub=1, payload="third").save)

        results = await _maybe_await(Event.find(partition_a=pa, partition_b=pb).all)
        assert len(results) == 3

        await _maybe_await(QS(Event).filter(partition_a=pa, partition_b=pb).delete)

    async def test_clustering_asc_order(self, coodie_driver, Event, QS) -> None:
        """ASC clustering key (seq) returns rows in ascending order."""
        await _maybe_await(Event.sync_table)
        pa, pb = "order_test", f"asc_{uuid4().hex[:6]}"
        for seq in [3, 1, 2]:
            await _maybe_await(Event(partition_a=pa, partition_b=pb, seq=seq, sub=0).save)

        results = await _maybe_await(Event.find(partition_a=pa, partition_b=pb).all)
        seqs = [r.seq for r in results]
        assert seqs == sorted(seqs)

        await _maybe_await(QS(Event).filter(partition_a=pa, partition_b=pb).delete)

    # ------------------------------------------------------------------
    # QuerySet.order_by and __len__
    # ------------------------------------------------------------------

    async def test_queryset_order_by_clustering(self, coodie_driver, Review) -> None:
        """order_by() on a clustering column returns expected sort order."""
        await _maybe_await(Review.sync_table)
        pid = uuid4()
        t1 = datetime(2024, 6, 1, 0, 0, 0, tzinfo=timezone.utc)
        t2 = datetime(2024, 6, 2, 0, 0, 0, tzinfo=timezone.utc)
        await _maybe_await(Review(product_id=pid, created_at=t1, author="X", rating=1).save)
        await _maybe_await(Review(product_id=pid, created_at=t2, author="Y", rating=2).save)

        results_asc = await _maybe_await(Review.find(product_id=pid).order_by("created_at").all)
        assert results_asc[0].created_at <= results_asc[-1].created_at

        await _maybe_await(Review.find(product_id=pid).delete)

    async def test_queryset_len(self, coodie_driver, Product, variant) -> None:
        """len(queryset) uses count() under the hood (sync only)."""
        if variant == "async":
            pytest.skip("len() is sync-only; async uses count()")

        brand = f"LenBrand_{uuid4().hex[:6]}"
        ids = [uuid4(), uuid4()]
        for pid in ids:
            Product(id=pid, name="LenTest", brand=brand).save()

        from coodie.sync.query import QuerySet

        qs = QuerySet(Product).filter(brand=brand).allow_filtering()
        assert len(qs) >= 2

        for pid in ids:
            Product(id=pid, name="").delete()

    async def test_queryset_first(self, coodie_driver, Product) -> None:
        """first() returns exactly one document or None."""
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="FirstTest").save)

        result = await _maybe_await(Product.find(id=pid).first)
        assert result is not None
        assert result.id == pid

        assert await _maybe_await(Product.find(id=uuid4()).first) is None

        await _maybe_await(Product(id=pid, name="").delete)

    # ------------------------------------------------------------------
    # Schema migration — ALTER TABLE ADD column
    # ------------------------------------------------------------------

    async def test_schema_migration_add_column(self, coodie_driver, driver_type, variant) -> None:
        """sync_table adds a new column to an existing table without data loss."""
        if variant == "async":
            pytest.skip("schema migration test uses driver.execute() directly (sync)")

        from coodie.drivers import get_driver
        from coodie.schema import ColumnDefinition

        ks = "test_ks"
        tbl = "it_migration_test"

        drv = get_driver()
        initial_cols = [
            ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ]
        drv.sync_table(tbl, ks, initial_cols)

        rid = uuid4()
        drv.execute(f'INSERT INTO {ks}.{tbl} ("id") VALUES (?)', [rid])

        extended_cols = [
            ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
            ColumnDefinition(name="label", cql_type="text"),
        ]
        drv.sync_table(tbl, ks, extended_cols)

        rows = drv.execute(f'SELECT "id", "label" FROM {ks}.{tbl} WHERE "id" = ?', [rid])
        assert rows
        assert str(rows[0]["id"]) == str(rid)
        assert rows[0].get("label") is None

        drv.execute(f"DROP TABLE IF EXISTS {ks}.{tbl}", [])

    # ------------------------------------------------------------------
    # Phase-1 extended types round-trip
    # ------------------------------------------------------------------

    async def test_extended_types_sync_table(self, coodie_driver, ExtendedTypes) -> None:
        """sync_table for extended types should succeed."""
        await _maybe_await(ExtendedTypes.sync_table)

    @pytest.mark.parametrize(
        "field_name, write_value",
        [
            pytest.param("big_val", 2**40, id="bigint"),
            pytest.param("small_val", 32_000, id="smallint"),
            pytest.param("tiny_val", 127, id="tinyint"),
            pytest.param("var_val", 10**30, id="varint"),
            pytest.param("dbl_val", 3.141592653589793, id="double"),
            pytest.param("ascii_val", "hello", id="ascii"),
        ],
    )
    async def test_extended_type_roundtrip(
        self, coodie_driver, ExtendedTypes, driver_type, field_name, write_value
    ) -> None:
        """Extended scalar type column survives a save/load round-trip."""
        if driver_type == "acsylla":
            pytest.skip("acsylla prepared binding does not support extended CQL types")
        await _maybe_await(ExtendedTypes.sync_table)
        rid = uuid4()
        await _maybe_await(ExtendedTypes(id=rid, **{field_name: write_value}).save)
        fetched = await _maybe_await(ExtendedTypes.find_one, id=rid)
        assert fetched is not None
        actual = getattr(fetched, field_name)
        if isinstance(write_value, float):
            assert abs(actual - write_value) < 1e-12
        else:
            assert actual == write_value
        await _maybe_await(ExtendedTypes(id=rid).delete)

    async def test_timeuuid_roundtrip(self, coodie_driver, ExtendedTypes, driver_type) -> None:
        """TimeUUID (timeuuid) column survives a save/load round-trip."""
        if driver_type == "acsylla":
            pytest.skip("acsylla prepared binding does not support extended CQL types")
        await _maybe_await(ExtendedTypes.sync_table)
        rid = uuid4()
        tuuid = uuid1()
        await _maybe_await(ExtendedTypes(id=rid, timeuuid_val=tuuid).save)
        fetched = await _maybe_await(ExtendedTypes.find_one, id=rid)
        assert fetched is not None
        assert fetched.timeuuid_val == tuuid
        await _maybe_await(ExtendedTypes(id=rid).delete)

    async def test_time_roundtrip(self, coodie_driver, ExtendedTypes, driver_type) -> None:
        """CQL time column survives a save/load round-trip."""
        if driver_type == "acsylla":
            pytest.skip("acsylla prepared binding does not support extended CQL types")
        await _maybe_await(ExtendedTypes.sync_table)
        rid = uuid4()
        t = dt_time(13, 45, 30)
        await _maybe_await(ExtendedTypes(id=rid, time_val=t).save)
        fetched = await _maybe_await(ExtendedTypes.find_one, id=rid)
        assert fetched is not None
        assert fetched.time_val is not None
        assert fetched.time_val.hour == 13
        assert fetched.time_val.minute == 45
        assert fetched.time_val.second == 30
        await _maybe_await(ExtendedTypes(id=rid).delete)

    @pytest.mark.parametrize(
        "field_name, write_value",
        [
            pytest.param("frozen_list", ["a", "b", "c"], id="frozen-list"),
            pytest.param("frozen_set", {10, 20, 30}, id="frozen-set"),
            pytest.param("frozen_map", {"x": 1, "y": 2}, id="frozen-map"),
        ],
    )
    async def test_frozen_collection_roundtrip(
        self, coodie_driver, ExtendedTypes, driver_type, field_name, write_value
    ) -> None:
        """Frozen collection column survives a save/load round-trip."""
        if driver_type == "acsylla":
            pytest.skip("acsylla prepared binding does not support extended CQL types")
        await _maybe_await(ExtendedTypes.sync_table)
        rid = uuid4()
        await _maybe_await(ExtendedTypes(id=rid, **{field_name: write_value}).save)
        fetched = await _maybe_await(ExtendedTypes.find_one, id=rid)
        assert fetched is not None
        assert getattr(fetched, field_name) == write_value
        await _maybe_await(ExtendedTypes(id=rid).delete)

    async def test_extended_types_all_fields_roundtrip(self, coodie_driver, ExtendedTypes, driver_type) -> None:
        """All extended type fields set together survive a save/load round-trip."""
        if driver_type == "acsylla":
            pytest.skip("acsylla prepared binding does not support extended CQL types")
        await _maybe_await(ExtendedTypes.sync_table)
        rid = uuid4()
        t = dt_time(9, 15, 0)
        tuuid = uuid1()
        original = ExtendedTypes(
            id=rid,
            big_val=2**40,
            small_val=1000,
            tiny_val=42,
            var_val=10**20,
            dbl_val=2.718281828,
            ascii_val="test",
            timeuuid_val=tuuid,
            time_val=t,
            frozen_list=["x"],
            frozen_set={7},
            frozen_map={"k": 99},
        )
        await _maybe_await(original.save)

        fetched = await _maybe_await(ExtendedTypes.find_one, id=rid)
        assert fetched is not None
        assert fetched.big_val == 2**40
        assert fetched.small_val == 1000
        assert fetched.tiny_val == 42
        assert fetched.var_val == 10**20
        assert abs(fetched.dbl_val - 2.718281828) < 1e-6
        assert fetched.ascii_val == "test"
        assert fetched.timeuuid_val == tuuid
        assert fetched.time_val is not None
        assert fetched.time_val.hour == 9
        assert fetched.frozen_list == ["x"]
        assert fetched.frozen_set == {7}
        assert fetched.frozen_map == {"k": 99}

        await _maybe_await(ExtendedTypes(id=rid).delete)


class TestContainerMutations:
    """Integration tests for list, set, and map collection mutation operators."""

    async def test_list_append(self, coodie_driver, ContainerDoc, QS) -> None:
        """list__append adds an element to the end of a list column."""
        await _maybe_await(ContainerDoc.sync_table)
        rid = uuid4()
        await _maybe_await(ContainerDoc(id=rid, items=["a", "b"]).save)

        await _maybe_await(QS(ContainerDoc).filter(id=rid).update, items__append=["c"])

        fetched = await _maybe_await(ContainerDoc.find_one, id=rid)
        assert fetched is not None
        assert fetched.items == ["a", "b", "c"]

        await _maybe_await(ContainerDoc(id=rid).delete)

    async def test_list_prepend(self, coodie_driver, ContainerDoc, QS) -> None:
        """list__prepend adds an element to the beginning of a list column."""
        await _maybe_await(ContainerDoc.sync_table)
        rid = uuid4()
        await _maybe_await(ContainerDoc(id=rid, items=["b", "c"]).save)

        await _maybe_await(QS(ContainerDoc).filter(id=rid).update, items__prepend=["a"])

        fetched = await _maybe_await(ContainerDoc.find_one, id=rid)
        assert fetched is not None
        assert fetched.items[0] == "a"

        await _maybe_await(ContainerDoc(id=rid).delete)

    async def test_list_remove(self, coodie_driver, ContainerDoc, QS) -> None:
        """list__remove removes all occurrences of the given elements from a list."""
        await _maybe_await(ContainerDoc.sync_table)
        rid = uuid4()
        await _maybe_await(ContainerDoc(id=rid, items=["a", "b", "a", "c"]).save)

        await _maybe_await(QS(ContainerDoc).filter(id=rid).update, items__remove=["a"])

        fetched = await _maybe_await(ContainerDoc.find_one, id=rid)
        assert fetched is not None
        assert "a" not in fetched.items
        assert "b" in fetched.items
        assert "c" in fetched.items

        await _maybe_await(ContainerDoc(id=rid).delete)

    async def test_set_add(self, coodie_driver, ContainerDoc, QS) -> None:
        """set__add adds an element to a set column."""
        await _maybe_await(ContainerDoc.sync_table)
        rid = uuid4()
        await _maybe_await(ContainerDoc(id=rid, tags={"apple"}).save)

        await _maybe_await(QS(ContainerDoc).filter(id=rid).update, tags__add={"banana"})

        fetched = await _maybe_await(ContainerDoc.find_one, id=rid)
        assert fetched is not None
        assert "apple" in fetched.tags
        assert "banana" in fetched.tags

        await _maybe_await(ContainerDoc(id=rid).delete)

    async def test_set_remove(self, coodie_driver, ContainerDoc, QS) -> None:
        """set__remove removes an element from a set column."""
        await _maybe_await(ContainerDoc.sync_table)
        rid = uuid4()
        await _maybe_await(ContainerDoc(id=rid, tags={"apple", "banana"}).save)

        await _maybe_await(QS(ContainerDoc).filter(id=rid).update, tags__remove={"banana"})

        fetched = await _maybe_await(ContainerDoc.find_one, id=rid)
        assert fetched is not None
        assert "banana" not in fetched.tags
        assert "apple" in fetched.tags

        await _maybe_await(ContainerDoc(id=rid).delete)

    async def test_map_update(self, coodie_driver, ContainerDoc, QS) -> None:
        """map__update upserts key-value pairs into a map column."""
        await _maybe_await(ContainerDoc.sync_table)
        rid = uuid4()
        await _maybe_await(ContainerDoc(id=rid, meta={"k1": "v1"}).save)

        await _maybe_await(QS(ContainerDoc).filter(id=rid).update, meta__update={"k2": "v2"})

        fetched = await _maybe_await(ContainerDoc.find_one, id=rid)
        assert fetched is not None
        assert fetched.meta.get("k1") == "v1"
        assert fetched.meta.get("k2") == "v2"

        await _maybe_await(ContainerDoc(id=rid).delete)

    async def test_map_remove(self, coodie_driver, ContainerDoc, QS) -> None:
        """map__remove removes a key from a map column."""
        await _maybe_await(ContainerDoc.sync_table)
        rid = uuid4()
        await _maybe_await(ContainerDoc(id=rid, meta={"k1": "v1", "k2": "v2"}).save)

        await _maybe_await(QS(ContainerDoc).filter(id=rid).update, meta__remove={"k1"})

        fetched = await _maybe_await(ContainerDoc.find_one, id=rid)
        assert fetched is not None
        assert "k1" not in fetched.meta
        assert fetched.meta.get("k2") == "v2"

        await _maybe_await(ContainerDoc(id=rid).delete)


class TestStaticColumn:
    """Integration tests for STATIC column behaviour."""

    async def test_static_value_shared_across_clustering_rows(self, coodie_driver, SensorReading) -> None:
        """A static column value is shared across all clustering rows in a partition."""
        await _maybe_await(SensorReading.sync_table)
        sid = f"sensor_{uuid4().hex[:6]}"

        # Write two clustering rows with the same static sensor_name
        await _maybe_await(
            SensorReading(sensor_id=sid, reading_time="2024-01-01T00:00", sensor_name="TempSensor", value=22.5).save
        )
        await _maybe_await(
            SensorReading(sensor_id=sid, reading_time="2024-01-01T01:00", sensor_name="TempSensor", value=23.0).save
        )

        rows = await _maybe_await(SensorReading.find(sensor_id=sid).all)
        assert len(rows) == 2
        # Both rows share the same static sensor_name
        for row in rows:
            assert row.sensor_name == "TempSensor"

        await _maybe_await(SensorReading(sensor_id=sid, reading_time="2024-01-01T00:00").delete)
        await _maybe_await(SensorReading(sensor_id=sid, reading_time="2024-01-01T01:00").delete)

    async def test_static_update_reflects_across_rows(self, coodie_driver, SensorReading) -> None:
        """Updating the static column value updates all clustering rows in the partition."""
        await _maybe_await(SensorReading.sync_table)
        sid = f"sensor_{uuid4().hex[:6]}"

        await _maybe_await(SensorReading(sensor_id=sid, reading_time="t1", sensor_name="Old", value=1.0).save)
        await _maybe_await(SensorReading(sensor_id=sid, reading_time="t2", sensor_name="Old", value=2.0).save)

        # Update the static column by saving a new row with updated sensor_name
        await _maybe_await(SensorReading(sensor_id=sid, reading_time="t1", sensor_name="New", value=1.0).save)

        rows = await _maybe_await(SensorReading.find(sensor_id=sid).all)
        for row in rows:
            assert row.sensor_name == "New"

        await _maybe_await(SensorReading(sensor_id=sid, reading_time="t1").delete)
        await _maybe_await(SensorReading(sensor_id=sid, reading_time="t2").delete)


class TestQueryOperators:
    """Integration tests for comparison and membership query operators."""

    async def test_filter_multi_pk_in(self, coodie_driver, AllTypes) -> None:
        """filter with __in returns a specific subset of rows by PK."""
        await _maybe_await(AllTypes.sync_table)
        rid1, rid2, rid3 = uuid4(), uuid4(), uuid4()
        await _maybe_await(AllTypes(id=rid1, count=10).save)
        await _maybe_await(AllTypes(id=rid2, count=20).save)
        await _maybe_await(AllTypes(id=rid3, count=30).save)

        # Fetch all three rows by PK using __in and verify count values.
        # gte/lte on clustering columns is covered in test_datetime_range_filter.
        results = await _maybe_await(AllTypes.find(id__in=[rid1, rid2, rid3]).all)
        in_range = [r for r in results if 10 <= r.count <= 20]
        assert len(in_range) == 2

        for rid in [rid1, rid2, rid3]:
            await _maybe_await(AllTypes(id=rid).delete)

    async def test_filter_in(self, coodie_driver, AllTypes) -> None:
        """filter with __in returns only rows whose PK is in the given list."""
        await _maybe_await(AllTypes.sync_table)
        rid1, rid2, rid3 = uuid4(), uuid4(), uuid4()
        await _maybe_await(AllTypes(id=rid1, flag=True).save)
        await _maybe_await(AllTypes(id=rid2, flag=True).save)
        await _maybe_await(AllTypes(id=rid3, flag=False).save)

        results = await _maybe_await(AllTypes.find(id__in=[rid1, rid2]).all)
        assert len(results) == 2
        ids = {r.id for r in results}
        assert rid1 in ids
        assert rid2 in ids
        assert rid3 not in ids

        for rid in [rid1, rid2, rid3]:
            await _maybe_await(AllTypes(id=rid).delete)

    async def test_datetime_range_filter(self, coodie_driver, Review) -> None:
        """filter on a datetime clustering column with __gte/__lte returns correct rows."""
        await _maybe_await(Review.sync_table)
        pid = uuid4()
        t_early = datetime(2024, 1, 1, tzinfo=timezone.utc)
        t_mid = datetime(2024, 6, 1, tzinfo=timezone.utc)
        t_late = datetime(2024, 12, 1, tzinfo=timezone.utc)

        await _maybe_await(Review(product_id=pid, created_at=t_early, author="A", rating=1).save)
        await _maybe_await(Review(product_id=pid, created_at=t_mid, author="B", rating=2).save)
        await _maybe_await(Review(product_id=pid, created_at=t_late, author="C", rating=3).save)

        results = await _maybe_await(Review.find(product_id=pid, created_at__gte=t_mid).all)
        # DESC clustering: t_late, t_mid should be returned; t_early is excluded
        assert len(results) == 2
        returned_times = {r.created_at.replace(tzinfo=timezone.utc) for r in results}
        assert t_early not in returned_times

        await _maybe_await(Review.find(product_id=pid).delete)


class TestPolymorphismIntegration:
    """Integration tests for discriminator-based polymorphic models."""

    async def test_save_concrete_fetch_via_base(self, coodie_driver, Animal, Cat, Dog) -> None:
        """Saving a concrete subclass and fetching via the base returns the right type."""
        await _maybe_await(Animal.sync_table)
        cid = uuid4()
        did = uuid4()

        cat_instance = Cat(id=cid, name="Whiskers")
        dog_instance = Dog(id=did, name="Rex")
        await _maybe_await(cat_instance.save)
        await _maybe_await(dog_instance.save)

        fetched_cat = await _maybe_await(Animal.find_one, id=cid)
        fetched_dog = await _maybe_await(Animal.find_one, id=did)

        assert fetched_cat is not None
        assert fetched_dog is not None
        assert type(fetched_cat).__name__ in ("SyncCat", "AsyncCat")
        assert type(fetched_dog).__name__ in ("SyncDog", "AsyncDog")

        await _maybe_await(Animal(id=cid, name="", animal_type="").delete)
        await _maybe_await(Animal(id=did, name="", animal_type="").delete)

    async def test_find_subclass_adds_discriminator_filter(self, coodie_driver, Animal, Cat) -> None:
        """Querying via a subclass automatically filters by discriminator value."""
        await _maybe_await(Animal.sync_table)
        cid = uuid4()
        did = uuid4()

        await _maybe_await(Cat(id=cid, name="Felix").save)
        # Write a raw "dog" row via the base class — it should NOT appear in Cat.find()
        await _maybe_await(Animal(id=did, name="Brutus", animal_type="dog").save)

        cats = await _maybe_await(Cat.find().allow_filtering().all)
        cat_ids = {c.id for c in cats}
        assert cid in cat_ids
        assert did not in cat_ids

        await _maybe_await(Animal(id=cid, name="", animal_type="").delete)
        await _maybe_await(Animal(id=did, name="", animal_type="").delete)


class TestSchemaManagement:
    """Integration tests for DDL edge cases: drop-table idempotency and compaction."""

    async def test_drop_table_idempotent(self, coodie_driver, variant) -> None:
        """drop_table (IF EXISTS) can be called multiple times without error."""
        if variant == "async":
            pytest.skip("Uses sync driver.execute() directly")

        from coodie.drivers import get_driver
        from coodie.schema import ColumnDefinition

        drv = get_driver()
        ks = "test_ks"
        tbl = "it_drop_idempotent"

        cols = [ColumnDefinition(name="id", cql_type="uuid", primary_key=True)]
        drv.sync_table(tbl, ks, cols)
        # First drop
        drv.execute(f"DROP TABLE IF EXISTS {ks}.{tbl}", [])
        # Second drop — must not raise
        drv.execute(f"DROP TABLE IF EXISTS {ks}.{tbl}", [])

    async def test_compaction_settings_applied(self, coodie_driver, variant) -> None:
        """Table created with __options__ compaction has the expected strategy."""
        if variant == "async":
            pytest.skip("Uses sync driver.execute() directly")

        from coodie.drivers import get_driver
        from coodie.schema import ColumnDefinition

        drv = get_driver()
        ks = "test_ks"
        tbl = "it_compaction_test"

        from coodie.cql_builder import build_create_table

        cols = [ColumnDefinition(name="id", cql_type="uuid", primary_key=True)]
        options = {"compaction": {"class": "LeveledCompactionStrategy"}}
        cql = build_create_table(tbl, ks, cols, table_options=options)
        drv.execute(cql, [])

        rows = drv.execute(
            "SELECT compaction FROM system_schema.tables WHERE keyspace_name = ? AND table_name = ?",
            [ks, tbl],
        )
        assert rows
        compaction = rows[0].get("compaction", {})
        assert "LeveledCompactionStrategy" in str(compaction)

        drv.execute(f"DROP TABLE IF EXISTS {ks}.{tbl}", [])
