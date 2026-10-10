"""One model, both modes, against a real ScyllaDB: write with one mode, read with the other."""

from __future__ import annotations

from uuid import uuid4

import pytest

from coodie.batch import BatchQuery

pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio(loop_scope="session"),
    # Sync calls on an async-default model inside the test's event loop are the point here.
    pytest.mark.filterwarnings("ignore::coodie.exceptions.BlockingCallWarning"),
]


class TestMixedModes:
    async def test_write_sync_read_async(self, coodie_driver, Product) -> None:
        await Product.sync_table_async()
        pid = uuid4()
        Product(id=pid, name="Widget").save_sync()

        fetched = await Product.get_async(id=pid)
        assert fetched.name == "Widget"
        assert [p.id async for p in Product.find(id=pid)] == [pid]

    async def test_write_async_read_sync(self, coodie_driver, Product) -> None:
        Product.sync_table_sync()
        pid = uuid4()
        doc = Product(id=pid, name="Gadget")
        await doc.save_async()
        doc.update_sync(name="Gadget 2")

        assert Product.get_sync(id=pid).name == "Gadget 2"
        assert [p.id for p in Product.find(id=pid)] == [pid]
        assert await Product.find(id=pid).count_async() == 1

        await doc.delete_async()
        assert Product.find_one_sync(id=pid) is None

    async def test_one_batch_both_protocols(self, coodie_driver, Product) -> None:
        await Product.sync_table_async()
        a, b = uuid4(), uuid4()
        with BatchQuery() as batch:
            Product(id=a, name="A").save_sync(batch=batch)
        async with BatchQuery() as batch:
            await Product(id=b, name="B").save_async(batch=batch)

        assert Product.get_sync(id=b).name == "B"
        assert (await Product.get_async(id=a)).name == "A"
