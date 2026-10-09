"""Integration tests for advanced query features.

Covers:
- per_partition_limit(N) returns exactly N rows per partition.
- Token-range queries with __token__gt / __token__lt.
- values_list() returns tuples instead of Documents.
- only(*cols) and defer(*cols) column projection.

Every test runs twice (sync and async) via the ``variant`` fixture.

See docs/plans/cqlengine-test-coverage-plan.md §1.10.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from tests.conftest import _maybe_await
from tests.integration.conftest import MIN_MURMUR3_TOKEN

pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio(loop_scope="session"),
]


class TestPerPartitionLimit:
    """Integration tests for PER PARTITION LIMIT."""

    async def test_per_partition_limit_returns_n_rows(self, coodie_driver, Event, QS) -> None:
        """per_partition_limit(N) returns at most N rows per partition."""
        await _maybe_await(Event.sync_table)

        pa = f"ppl_{uuid4().hex[:6]}"
        pb = "ppl_test"

        # Insert 5 rows in the same partition
        for seq in range(5):
            await _maybe_await(Event(partition_a=pa, partition_b=pb, seq=seq, payload=f"p{seq}").save)

        # Query with per_partition_limit=2
        results = await _maybe_await(QS(Event).filter(partition_a=pa, partition_b=pb).per_partition_limit(2).all)
        assert len(results) <= 2

        # Cleanup
        await _maybe_await(QS(Event).filter(partition_a=pa, partition_b=pb).delete)

    async def test_per_partition_limit_multiple_partitions(self, coodie_driver, Event, QS) -> None:
        """per_partition_limit(N) limits rows independently per partition."""
        await _maybe_await(Event.sync_table)

        pb = f"ppl_multi_{uuid4().hex[:6]}"
        pa1 = f"part1_{uuid4().hex[:6]}"
        pa2 = f"part2_{uuid4().hex[:6]}"

        # Insert 4 rows in partition A and 4 in partition B
        for seq in range(4):
            await _maybe_await(Event(partition_a=pa1, partition_b=pb, seq=seq, payload="a").save)
            await _maybe_await(Event(partition_a=pa2, partition_b=pb, seq=seq, payload="b").save)

        # Query each partition individually with per_partition_limit=2
        results_a = await _maybe_await(QS(Event).filter(partition_a=pa1, partition_b=pb).per_partition_limit(2).all)
        results_b = await _maybe_await(QS(Event).filter(partition_a=pa2, partition_b=pb).per_partition_limit(2).all)

        assert len(results_a) <= 2
        assert len(results_b) <= 2

        # Cleanup
        await _maybe_await(QS(Event).filter(partition_a=pa1, partition_b=pb).delete)
        await _maybe_await(QS(Event).filter(partition_a=pa2, partition_b=pb).delete)


class TestTokenRangeQueries:
    """Integration tests for token-range queries."""

    async def test_token_gt_returns_rows(self, coodie_driver, Product) -> None:
        """Token-range filter with __token__gt returns matching rows."""
        await _maybe_await(Product.sync_table)
        ids = [uuid4() for _ in range(3)]
        for pid in ids:
            await _maybe_await(Product(id=pid, name="TokenGT").save)

        # TOKEN(pk) > MIN_TOKEN should return all rows
        results = await _maybe_await(Product.find(id__token__gt=MIN_MURMUR3_TOKEN).allow_filtering().all)
        assert isinstance(results, list)
        found_ids = {r.id for r in results}
        for pid in ids:
            assert pid in found_ids

        # Cleanup
        for pid in ids:
            await _maybe_await(Product(id=pid, name="").delete)

    async def test_token_lt_returns_rows(self, coodie_driver, Product) -> None:
        """Token-range filter with __token__lt returns matching rows."""
        await _maybe_await(Product.sync_table)
        ids = [uuid4() for _ in range(3)]
        for pid in ids:
            await _maybe_await(Product(id=pid, name="TokenLT").save)

        # TOKEN(pk) < MAX_TOKEN should return all rows
        max_token = 2**63 - 1
        results = await _maybe_await(Product.find(id__token__lt=max_token).allow_filtering().all)
        assert isinstance(results, list)
        found_ids = {r.id for r in results}
        for pid in ids:
            assert pid in found_ids

        # Cleanup
        for pid in ids:
            await _maybe_await(Product(id=pid, name="").delete)

    async def test_token_range_gt_and_lt(self, coodie_driver, Product) -> None:
        """Token-range filter with both __token__gt and __token__lt returns rows in range."""
        await _maybe_await(Product.sync_table)
        ids = [uuid4() for _ in range(3)]
        for pid in ids:
            await _maybe_await(Product(id=pid, name="TokenRange").save)

        # Full ring: MIN_TOKEN < TOKEN(pk) < MAX_TOKEN
        max_token = 2**63 - 1
        results = await _maybe_await(
            Product.find(id__token__gt=MIN_MURMUR3_TOKEN, id__token__lt=max_token).allow_filtering().all
        )
        assert isinstance(results, list)
        found_ids = {r.id for r in results}
        for pid in ids:
            assert pid in found_ids

        # Cleanup
        for pid in ids:
            await _maybe_await(Product(id=pid, name="").delete)


class TestValuesListProjection:
    """Integration tests for values_list() returning tuples."""

    async def test_values_list_returns_tuples(self, coodie_driver, Product, QS) -> None:
        """values_list('col1', 'col2') returns a list of tuples."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="VLTuple", brand="VLBrand", price=9.99).save)

        results = await _maybe_await(QS(Product).filter(id=pid).values_list("id", "name").all)
        assert len(results) >= 1
        assert isinstance(results[0], tuple)

        # Find our row
        matching = [r for r in results if str(r[0]) == str(pid)]
        assert len(matching) == 1
        assert matching[0][1] == "VLTuple"

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_values_list_single_column(self, coodie_driver, Product, QS) -> None:
        """values_list('name') returns single-element tuples."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="VLSingle").save)

        results = await _maybe_await(QS(Product).filter(id=pid).values_list("name").all)
        assert len(results) >= 1
        assert isinstance(results[0], tuple)
        assert len(results[0]) == 1
        matching = [r for r in results if r[0] == "VLSingle"]
        assert len(matching) == 1

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_values_list_multiple_columns(self, coodie_driver, Product, QS) -> None:
        """values_list with multiple columns returns correct column values."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="VLMulti", brand="TestBrand", price=12.5).save)

        results = await _maybe_await(QS(Product).filter(id=pid).values_list("name", "brand", "price").all)
        assert len(results) >= 1
        matching = [r for r in results if r[0] == "VLMulti"]
        assert len(matching) == 1
        assert matching[0][1] == "TestBrand"
        assert abs(matching[0][2] - 12.5) < 0.01

        await _maybe_await(Product(id=pid, name="").delete)


class TestColumnProjection:
    """Integration tests for only() and defer() column projection."""

    async def test_only_returns_selected_columns(self, coodie_driver, Product, QS) -> None:
        """only('id', 'name') returns Documents with only selected columns populated."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="OnlyTest", brand="OnlyBrand", price=5.0).save)

        results = await _maybe_await(QS(Product).filter(id=pid).only("id", "name").all)
        assert len(results) >= 1
        found = next(r for r in results if r.id == pid)
        assert found.name == "OnlyTest"

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_only_multiple_columns(self, coodie_driver, Product, QS) -> None:
        """only() with multiple columns returns all selected columns."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="OnlyMulti", brand="TestBrand", price=7.5).save)

        results = await _maybe_await(QS(Product).filter(id=pid).only("id", "name", "brand").all)
        assert len(results) >= 1
        found = next(r for r in results if r.id == pid)
        assert found.name == "OnlyMulti"
        assert found.brand == "TestBrand"

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_defer_excludes_columns(self, coodie_driver, Product, QS) -> None:
        """defer('description') excludes the specified column from the SELECT."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="DeferTest", brand="DeferBrand", price=7.0, description="hidden").save)

        results = await _maybe_await(QS(Product).filter(id=pid).defer("description").all)
        assert len(results) >= 1
        found = next(r for r in results if r.id == pid)
        assert found.name == "DeferTest"
        assert found.brand == "DeferBrand"
        # description should be default (None) since it was deferred
        assert found.description is None

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_defer_multiple_columns(self, coodie_driver, Product, QS) -> None:
        """defer() with multiple columns excludes all of them."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="DeferMulti", brand="TestBrand", price=15.0, description="desc").save)

        results = await _maybe_await(QS(Product).filter(id=pid).defer("description", "price").all)
        assert len(results) >= 1
        found = next(r for r in results if r.id == pid)
        assert found.name == "DeferMulti"
        assert found.brand == "TestBrand"
        # Deferred fields should have default values
        assert found.description is None
        assert found.price == 0.0

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_only_and_values_list_combined(self, coodie_driver, Product, QS) -> None:
        """Combining only() and values_list() returns tuples of selected columns."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="Combo", brand="ComboBrand").save)

        results = await _maybe_await(QS(Product).filter(id=pid).only("id", "name").values_list("id", "name").all)
        assert len(results) >= 1
        assert isinstance(results[0], tuple)
        matching = [r for r in results if str(r[0]) == str(pid)]
        assert len(matching) == 1
        assert matching[0][1] == "Combo"

        await _maybe_await(Product(id=pid, name="").delete)
