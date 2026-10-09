"""Basic CRUD integration tests — merged sync + async.

Every test runs twice (sync and async) via the ``variant`` fixture.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from coodie.exceptions import DocumentNotFound, MultipleDocumentsFound
from tests.conftest import _maybe_await
from tests.integration.conftest import MIN_MURMUR3_TOKEN

pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio(loop_scope="session"),
]


class TestIntegration:
    """Full CRUD tests against a real ScyllaDB container."""

    async def test_sync_table_creates_table(self, coodie_driver, Product) -> None:
        """sync_table should create the table without raising."""
        await _maybe_await(Product.sync_table)

    async def test_sync_table_idempotent(self, coodie_driver, Product) -> None:
        """Calling sync_table twice must not raise."""
        await _maybe_await(Product.sync_table)
        await _maybe_await(Product.sync_table)

    async def test_save_and_find_one(self, coodie_driver, Product) -> None:
        """save() inserts a row; find_one() retrieves it."""
        pid = uuid4()
        p = Product(id=pid, name="Widget", brand="Acme", price=9.99)
        await _maybe_await(p.save)

        fetched = await _maybe_await(Product.find_one, id=pid)
        assert fetched is not None
        assert fetched.id == pid
        assert fetched.name == "Widget"
        assert fetched.brand == "Acme"

    async def test_get_by_pk(self, coodie_driver, Product) -> None:
        """get() retrieves a document and raises DocumentNotFound when absent."""
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="Gadget").save)

        doc = await _maybe_await(Product.get, id=pid)
        assert isinstance(doc, Product)

        with pytest.raises(DocumentNotFound):
            await _maybe_await(Product.get, id=uuid4())

    async def test_per_query_consistency_reaches_server(self, coodie_driver, driver_type) -> None:
        """The server rejects reads at EACH_QUORUM, so an error proves the consistency was forwarded."""
        if driver_type == "acsylla":
            pytest.xfail("AcsyllaDriver passes consistency as str; acsylla.bind() expects acsylla.Consistency")
        with pytest.raises(Exception, match="EACH_QUORUM"):
            await coodie_driver.execute_async("SELECT release_version FROM system.local", [], consistency="EACH_QUORUM")

    async def test_delete(self, coodie_driver, Product) -> None:
        """delete() removes the row; subsequent find_one returns None."""
        pid = uuid4()
        p = Product(id=pid, name="Temp")
        await _maybe_await(p.save)
        assert await _maybe_await(Product.find_one, id=pid) is not None

        await _maybe_await(p.delete)
        assert await _maybe_await(Product.find_one, id=pid) is None

    async def test_save_write_read_cycle(self, coodie_driver, Product) -> None:
        """Multiple saves then find_one returns the correct rows."""
        ids = [uuid4() for _ in range(3)]
        for i, pid in enumerate(ids):
            await _maybe_await(Product(id=pid, name=f"Item{i}", brand="BrandX").save)

        for pid in ids:
            assert await _maybe_await(Product.find_one, id=pid) is not None

        for pid in ids:
            await _maybe_await(Product(id=pid, name="").delete)

    async def test_queryset_filtering_by_secondary_index(self, coodie_driver, Product) -> None:
        """find(brand=...) filters via the secondary index."""
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="IndexTest", brand="AcmeFiltered").save)

        results = await _maybe_await(Product.find(brand="AcmeFiltered").allow_filtering().all)
        assert any(r.id == pid for r in results)

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_queryset_limit(self, coodie_driver, Product) -> None:
        """limit(n) restricts the number of rows returned."""
        ids = [uuid4() for _ in range(5)]
        for pid in ids:
            await _maybe_await(Product(id=pid, name="LimitTest").save)

        results = await _maybe_await(Product.find().limit(2).allow_filtering().all)
        assert len(results) <= 2

        for pid in ids:
            await _maybe_await(Product(id=pid, name="").delete)

    async def test_queryset_count(self, coodie_driver, Product) -> None:
        """count() returns the correct integer."""
        ids = [uuid4() for _ in range(3)]
        for pid in ids:
            await _maybe_await(Product(id=pid, name="CountTest", brand="CountBrand").save)

        count = await _maybe_await(Product.find(brand="CountBrand").allow_filtering().count)
        assert count >= 3

        for pid in ids:
            await _maybe_await(Product(id=pid, name="").delete)

    async def test_queryset_first(self, coodie_driver, Product) -> None:
        """first() returns exactly one document or None."""
        ids = [uuid4() for _ in range(3)]
        for pid in ids:
            await _maybe_await(Product(id=pid, name="FirstCountTest", brand="FirstCountBrand").save)

        first = await _maybe_await(Product.find(brand="FirstCountBrand").allow_filtering().first)
        assert first is not None

        for pid in ids:
            await _maybe_await(Product(id=pid, name="").delete)

    async def test_queryset_delete(self, coodie_driver, Product) -> None:
        """QuerySet.delete() removes matching rows."""
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="ToDelete", brand="DeleteMe").save)
        assert await _maybe_await(Product.find_one, id=pid) is not None

        await _maybe_await(Product.find(id=pid).delete)
        assert await _maybe_await(Product.find_one, id=pid) is None

    async def test_collections_list(self, coodie_driver, Product) -> None:
        """list[str] field round-trips correctly."""
        pid = uuid4()
        tags = ["alpha", "beta", "gamma"]
        await _maybe_await(Product(id=pid, name="TagTest", tags=tags).save)

        fetched = await _maybe_await(Product.find_one, id=pid)
        assert fetched is not None
        assert sorted(fetched.tags) == sorted(tags)

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_optional_field_none_roundtrip(self, coodie_driver, Product) -> None:
        """Optional[str] field set to None round-trips correctly."""
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="OptNone", description=None).save)

        fetched = await _maybe_await(Product.find_one, id=pid)
        assert fetched is not None
        assert fetched.description is None

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_optional_field_value_roundtrip(self, coodie_driver, Product) -> None:
        """Optional[str] field set to a value round-trips correctly."""
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="OptVal", description="hello").save)

        fetched = await _maybe_await(Product.find_one, id=pid)
        assert fetched is not None
        assert fetched.description == "hello"

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_ttl_row_expires(self, coodie_driver, Product) -> None:
        """Row inserted with ttl=2 disappears after ~2 seconds."""
        pid = uuid4()
        p = Product(id=pid, name="TTLTest")
        await _maybe_await(p.save, ttl=2)
        assert await _maybe_await(Product.find_one, id=pid) is not None

        await asyncio.sleep(3)
        assert await _maybe_await(Product.find_one, id=pid) is None

    async def test_clustering_key_order(self, coodie_driver, Review) -> None:
        """Reviews with DESC clustering key return newest first."""
        await _maybe_await(Review.sync_table)
        pid = uuid4()
        t1 = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        t2 = datetime(2024, 1, 2, 12, 0, 0, tzinfo=timezone.utc)

        await _maybe_await(Review(product_id=pid, created_at=t1, author="Alice", rating=3).save)
        await _maybe_await(Review(product_id=pid, created_at=t2, author="Bob", rating=5).save)

        results = await _maybe_await(Review.find(product_id=pid).all)
        assert len(results) == 2
        # DESC order: newest (t2) first
        assert results[0].created_at.replace(tzinfo=timezone.utc) >= results[1].created_at.replace(tzinfo=timezone.utc)

        await _maybe_await(Review.find(product_id=pid).delete)

    async def test_multiple_documents_found(self, coodie_driver, Product) -> None:
        """find_one raises MultipleDocumentsFound when > 1 rows match."""
        brand = f"DupBrand_{uuid4().hex[:8]}"
        ids = [uuid4(), uuid4()]
        for pid in ids:
            await _maybe_await(Product(id=pid, name="Dup", brand=brand).save)

        with pytest.raises(MultipleDocumentsFound):
            await _maybe_await(Product.find_one, brand=brand)

        for pid in ids:
            await _maybe_await(Product(id=pid, name="").delete)

    async def test_multi_model_isolation(self, coodie_driver, Product, Review) -> None:
        """Two Document subclasses write to separate tables without cross-contamination."""
        await _maybe_await(Review.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="Isolated").save)
        await _maybe_await(Review(product_id=pid, author="Tester", rating=5).save)

        assert await _maybe_await(Product.find_one, id=pid) is not None
        assert await _maybe_await(Review.find_one, product_id=pid) is not None

        await _maybe_await(Product(id=pid, name="").delete)
        await _maybe_await(Review.find(product_id=pid).delete)

    # --- Pagination & Token Queries ---

    async def test_paged_all_pagination(self, coodie_driver, Product, driver_type) -> None:
        """paged_all() with fetch_size returns PagedResult and paginates."""
        from coodie.results import PagedResult

        brand = f"PageBrand_{uuid4().hex[:8]}"
        ids = [uuid4() for _ in range(5)]
        for pid in ids:
            await _maybe_await(Product(id=pid, name="PageTest", brand=brand).save)

        result = await _maybe_await(Product.find(brand=brand).fetch_size(2).allow_filtering().paged_all)
        assert isinstance(result, PagedResult)
        assert len(result.data) > 0
        for doc in result.data:
            assert isinstance(doc, Product)

        all_docs = list(result.data)
        while result.paging_state is not None:
            result = await _maybe_await(
                Product.find(brand=brand).fetch_size(2).page(result.paging_state).allow_filtering().paged_all
            )
            assert isinstance(result, PagedResult)
            all_docs.extend(result.data)

        found_ids = {d.id for d in all_docs}
        for pid in ids:
            assert pid in found_ids

        for pid in ids:
            await _maybe_await(Product(id=pid, name="").delete)

    async def test_fetch_size_limits_page(self, coodie_driver, Product, driver_type) -> None:
        """fetch_size(n) limits the number of rows returned per page."""
        if driver_type == "python-rs":
            pytest.skip("python-rs-driver uses execute_unpaged — no pagination support")
        from coodie.results import PagedResult

        brand = f"FetchBrand_{uuid4().hex[:8]}"
        ids = [uuid4() for _ in range(4)]
        for pid in ids:
            await _maybe_await(Product(id=pid, name="FetchSizeTest", brand=brand).save)

        result = await _maybe_await(Product.find(brand=brand).fetch_size(2).allow_filtering().paged_all)
        assert isinstance(result, PagedResult)
        assert len(result.data) <= 2

        for pid in ids:
            await _maybe_await(Product(id=pid, name="").delete)

    async def test_token_range_query(self, coodie_driver, Product, driver_type) -> None:
        """Token-range filter queries execute without error."""
        ids = [uuid4() for _ in range(3)]
        for pid in ids:
            await _maybe_await(Product(id=pid, name="TokenTest").save)

        results = await _maybe_await(Product.find(id__token__gt=MIN_MURMUR3_TOKEN).allow_filtering().all)
        assert isinstance(results, list)
        found_ids = {r.id for r in results}
        for pid in ids:
            assert pid in found_ids

        for pid in ids:
            await _maybe_await(Product(id=pid, name="").delete)

    async def test_aiter(self, coodie_driver, Product, variant) -> None:
        """async for iterates over QuerySet results."""
        if variant == "sync":
            # Sync QuerySet uses __iter__, not __aiter__
            pytest.skip("__aiter__ is async-only")

        ids = [uuid4() for _ in range(2)]
        brand = f"AiterBrand_{uuid4().hex[:8]}"
        for pid in ids:
            await _maybe_await(Product(id=pid, name="AiterTest", brand=brand).save)

        from coodie.aio.query import QuerySet

        collected = [item async for item in QuerySet(Product).filter(brand=brand).allow_filtering()]
        assert len(collected) >= 2

        for pid in ids:
            await _maybe_await(Product(id=pid, name="").delete)

    async def test_queryset_iter(self, coodie_driver, Product, variant) -> None:
        """Iterating over a sync QuerySet yields Document instances."""
        if variant == "async":
            pytest.skip("__iter__ is sync-only; __aiter__ tested separately")

        brand = f"IterBrand_{uuid4().hex[:6]}"
        ids = [uuid4(), uuid4()]
        for pid in ids:
            Product(id=pid, name="IterTest", brand=brand).save()

        from coodie.sync.query import QuerySet

        items = list(QuerySet(Product).filter(brand=brand).allow_filtering())
        assert all(isinstance(i, Product) for i in items)
        assert len(items) >= 2

        for pid in ids:
            Product(id=pid, name="").delete()

    # --- QuerySet Enhancements ---

    async def test_only_column_projection(self, coodie_driver, Product, QS) -> None:
        """`.only()` returns Documents with only the selected columns populated."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="OnlyTest", brand="OnlyBrand", price=5.0).save)

        results = await _maybe_await(QS(Product).filter(id=pid).only("id", "name").all)
        assert len(results) >= 1
        found = [r for r in results if r.id == pid][0]
        assert found.name == "OnlyTest"

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_defer_excludes_columns(self, coodie_driver, Product, QS) -> None:
        """`.defer()` excludes the specified columns from the SELECT."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="DeferTest", brand="DeferBrand", price=7.0).save)

        results = await _maybe_await(QS(Product).filter(id=pid).defer("description").all)
        assert len(results) >= 1
        found = [r for r in results if r.id == pid][0]
        assert found.name == "DeferTest"

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_values_list_returns_tuples(self, coodie_driver, Product, QS) -> None:
        """`.values_list()` returns a list of tuples."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="VLTest", brand="VLBrand", price=3.0).save)

        results = await _maybe_await(QS(Product).filter(id=pid).values_list("id", "name").all)
        assert len(results) >= 1
        assert isinstance(results[0], tuple)
        matching = [r for r in results if str(r[0]) == str(pid)]
        assert len(matching) == 1
        assert matching[0][1] == "VLTest"

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_per_partition_limit(self, coodie_driver, Event, QS) -> None:
        """`.per_partition_limit()` limits rows per partition."""
        await _maybe_await(Event.sync_table)
        pa = f"ppl_{uuid4().hex[:6]}"
        pb = "ppl_b"
        for seq in range(5):
            await _maybe_await(Event(partition_a=pa, partition_b=pb, seq=seq, payload=f"p{seq}").save)

        results = await _maybe_await(QS(Event).filter(partition_a=pa, partition_b=pb).per_partition_limit(2).all)
        assert len(results) <= 2

        await _maybe_await(QS(Event).filter(partition_a=pa, partition_b=pb).delete)
