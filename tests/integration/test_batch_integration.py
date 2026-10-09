"""Integration tests for batch writes against a real ScyllaDB instance.

Covers:
- Logged batch with multiple models.
- Unlogged batch.
- Counter batch.
- Batch context manager rollback (exception during batch).

Every test runs twice (sync and async) via the ``variant`` fixture.

See docs/plans/cqlengine-test-coverage-plan.md §1.9.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from coodie.cql_builder import build_counter_update, build_insert
from tests.conftest import _maybe_await

pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio(loop_scope="session"),
]


class TestBatchWrites:
    """Integration tests for batch write operations."""

    async def test_logged_batch_multiple_models(self, coodie_driver, AllTypes, Product, variant) -> None:
        """A LOGGED batch atomically inserts rows across multiple tables."""
        await _maybe_await(AllTypes.sync_table)
        await _maybe_await(Product.sync_table)

        rid_at = uuid4()
        rid_prod = uuid4()

        at_row = AllTypes(id=rid_at, count=42)
        prod_row = Product(id=rid_prod, name="BatchProd", brand="BatchBrand")

        stmt1, p1 = build_insert(
            AllTypes.Settings.name,
            AllTypes.Settings.keyspace,
            at_row.model_dump(),
        )
        stmt2, p2 = build_insert(
            Product.Settings.name,
            Product.Settings.keyspace,
            prod_row.model_dump(),
        )

        if variant == "sync":
            from coodie.batch import BatchQuery

            with BatchQuery(logged=True) as batch:
                batch.add(stmt1, p1)
                batch.add(stmt2, p2)
        else:
            from coodie.batch import AsyncBatchQuery

            async with AsyncBatchQuery(logged=True) as batch:
                batch.add(stmt1, p1)
                batch.add(stmt2, p2)

        # Both rows should exist
        fetched_at = await _maybe_await(AllTypes.find_one, id=rid_at)
        assert fetched_at is not None
        assert fetched_at.count == 42

        fetched_prod = await _maybe_await(Product.find_one, id=rid_prod)
        assert fetched_prod is not None
        assert fetched_prod.name == "BatchProd"

        # Cleanup
        await _maybe_await(AllTypes(id=rid_at).delete)
        await _maybe_await(Product(id=rid_prod, name="").delete)

    async def test_unlogged_batch(self, coodie_driver, Product, variant) -> None:
        """An UNLOGGED batch inserts multiple rows (no atomicity guarantee)."""
        await _maybe_await(Product.sync_table)

        rid1, rid2 = uuid4(), uuid4()
        row1 = Product(id=rid1, name="Unlog1")
        row2 = Product(id=rid2, name="Unlog2")

        stmt1, p1 = build_insert(
            Product.Settings.name,
            Product.Settings.keyspace,
            row1.model_dump(),
        )
        stmt2, p2 = build_insert(
            Product.Settings.name,
            Product.Settings.keyspace,
            row2.model_dump(),
        )

        if variant == "sync":
            from coodie.batch import BatchQuery

            with BatchQuery(logged=False) as batch:
                batch.add(stmt1, p1)
                batch.add(stmt2, p2)
        else:
            from coodie.batch import AsyncBatchQuery

            async with AsyncBatchQuery(logged=False) as batch:
                batch.add(stmt1, p1)
                batch.add(stmt2, p2)

        fetched1 = await _maybe_await(Product.find_one, id=rid1)
        fetched2 = await _maybe_await(Product.find_one, id=rid2)
        assert fetched1 is not None
        assert fetched1.name == "Unlog1"
        assert fetched2 is not None
        assert fetched2.name == "Unlog2"

        # Cleanup
        await _maybe_await(Product(id=rid1, name="").delete)
        await _maybe_await(Product(id=rid2, name="").delete)

    async def test_counter_batch(self, coodie_driver, PageView, variant) -> None:
        """A COUNTER batch increments counter columns atomically."""
        await _maybe_await(PageView.sync_table)

        url1 = f"/batch-ctr1-{uuid4().hex[:6]}"
        url2 = f"/batch-ctr2-{uuid4().hex[:6]}"

        stmt1, p1 = build_counter_update(
            PageView.Settings.name,
            PageView.Settings.keyspace,
            {"view_count": 5},
            [("url", "=", url1)],
        )
        stmt2, p2 = build_counter_update(
            PageView.Settings.name,
            PageView.Settings.keyspace,
            {"view_count": 3, "unique_visitors": 1},
            [("url", "=", url2)],
        )

        if variant == "sync":
            from coodie.batch import BatchQuery

            with BatchQuery(batch_type="COUNTER") as batch:
                batch.add(stmt1, p1)
                batch.add(stmt2, p2)
        else:
            from coodie.batch import AsyncBatchQuery

            async with AsyncBatchQuery(batch_type="COUNTER") as batch:
                batch.add(stmt1, p1)
                batch.add(stmt2, p2)

        fetched1 = await _maybe_await(PageView.find_one, url=url1)
        assert fetched1 is not None
        assert fetched1.view_count == 5

        fetched2 = await _maybe_await(PageView.find_one, url=url2)
        assert fetched2 is not None
        assert fetched2.view_count == 3
        assert fetched2.unique_visitors == 1

    async def test_batch_context_manager_rollback_on_exception(self, coodie_driver, Product, variant) -> None:
        """When an exception occurs inside a batch context manager, the batch is NOT executed."""
        await _maybe_await(Product.sync_table)

        rid = uuid4()
        row = Product(id=rid, name="ShouldNotExist")
        stmt, p = build_insert(
            Product.Settings.name,
            Product.Settings.keyspace,
            row.model_dump(),
        )

        if variant == "sync":
            from coodie.batch import BatchQuery

            with pytest.raises(ValueError, match="intentional"), BatchQuery() as batch:
                batch.add(stmt, p)
                raise ValueError("intentional error")
        else:
            from coodie.batch import AsyncBatchQuery

            with pytest.raises(ValueError, match="intentional"):
                async with AsyncBatchQuery() as batch:
                    batch.add(stmt, p)
                    raise ValueError("intentional error")

        # The row should NOT exist because the batch was not executed
        fetched = await _maybe_await(Product.find_one, id=rid)
        assert fetched is None

    async def test_empty_batch_no_execute(self, coodie_driver, variant) -> None:
        """An empty batch (no statements added) executes without error."""
        if variant == "sync":
            from coodie.batch import BatchQuery

            with BatchQuery() as _batch:
                pass  # no statements added
            # Should complete without error — nothing to verify beyond no exception
        else:
            from coodie.batch import AsyncBatchQuery

            async with AsyncBatchQuery() as _batch:
                pass  # no statements added
            # Should complete without error — nothing to verify beyond no exception
