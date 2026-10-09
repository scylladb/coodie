from __future__ import annotations

from typing import Annotated
from uuid import UUID, uuid4

from pydantic import Field

from coodie.aio.document import Document as AsyncDocument
from coodie.batch import AsyncBatchQuery, BatchQuery
from coodie.cql_builder import build_batch
from coodie.fields import PrimaryKey
from coodie.results import LWTResult
from coodie.sync.document import Document


class BatchItem(Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""

    class Settings:
        name = "batch_items"
        keyspace = "test_ks"


# ------------------------------------------------------------------
# build_batch() enhancements
# ------------------------------------------------------------------


def test_build_batch_counter_type():
    stmts = [
        ("UPDATE ks.t SET c = c + ?", [1]),
    ]
    cql, params = build_batch(stmts, batch_type="COUNTER")
    assert "BEGIN COUNTER BATCH" in cql
    assert "APPLY BATCH" in cql
    assert params == [1]


def test_build_batch_unlogged_type():
    stmts = [
        ("INSERT INTO ks.t (id) VALUES (?)", ["1"]),
    ]
    cql, _params = build_batch(stmts, batch_type="UNLOGGED")
    assert "BEGIN UNLOGGED BATCH" in cql


def test_build_batch_type_overrides_logged():
    stmts = [
        ("INSERT INTO ks.t (id) VALUES (?)", ["1"]),
    ]
    cql, _ = build_batch(stmts, logged=True, batch_type="UNLOGGED")
    assert "BEGIN UNLOGGED BATCH" in cql


# ------------------------------------------------------------------
# BatchQuery (sync context manager)
# ------------------------------------------------------------------


def test_batch_query_accumulates(registered_mock_driver):
    batch = BatchQuery()
    batch.add("INSERT INTO ks.t (id) VALUES (?)", ["1"])
    batch.add("INSERT INTO ks.t (id) VALUES (?)", ["2"])
    assert len(batch._statements) == 2


def test_batch_query_context_manager(registered_mock_driver):
    with BatchQuery() as batch:
        batch.add("INSERT INTO ks.t (id) VALUES (?)", ["1"])
        batch.add("INSERT INTO ks.t (id) VALUES (?)", ["2"])

    assert len(registered_mock_driver.executed) == 1
    stmt, params = registered_mock_driver.executed[0]
    assert "BEGIN BATCH" in stmt
    assert "APPLY BATCH" in stmt
    assert params == ["1", "2"]


def test_batch_query_unlogged(registered_mock_driver):
    with BatchQuery(logged=False) as batch:
        batch.add("INSERT INTO ks.t (id) VALUES (?)", ["1"])

    stmt, _ = registered_mock_driver.executed[0]
    assert "BEGIN UNLOGGED BATCH" in stmt


def test_batch_query_counter_type(registered_mock_driver):
    with BatchQuery(batch_type="COUNTER") as batch:
        batch.add("UPDATE ks.t SET c = c + ?", [1])

    stmt, _ = registered_mock_driver.executed[0]
    assert "BEGIN COUNTER BATCH" in stmt


def test_batch_query_empty_noop(registered_mock_driver):
    with BatchQuery() as _batch:
        pass  # no statements added

    assert len(registered_mock_driver.executed) == 0


def test_batch_query_exception_no_execute(registered_mock_driver):
    try:
        with BatchQuery() as batch:
            batch.add("INSERT INTO ks.t (id) VALUES (?)", ["1"])
            raise ValueError("boom")
    except ValueError:
        pass

    assert len(registered_mock_driver.executed) == 0


def test_batch_query_clears_after_execute(registered_mock_driver):
    batch = BatchQuery()
    batch.add("INSERT INTO ks.t (id) VALUES (?)", ["1"])
    batch.execute()
    assert len(batch._statements) == 0


def test_batch_query_reusable(registered_mock_driver):
    with BatchQuery() as batch:
        batch.add("INSERT INTO ks.t (id) VALUES (?)", ["1"])

    assert len(registered_mock_driver.executed) == 1

    with batch:
        batch.add("INSERT INTO ks.t (id) VALUES (?)", ["2"])

    assert len(registered_mock_driver.executed) == 2


def test_batch_query_non_conditional_returns_none(registered_mock_driver):
    batch = BatchQuery()
    batch.add("INSERT INTO ks.t (id) VALUES (?)", ["1"])
    assert batch.execute() is None
    assert batch.result is None


def test_batch_query_conditional_returns_lwt_result(registered_mock_driver):
    registered_mock_driver.set_return_rows([{"[applied]": False, "id": "1"}])
    with BatchQuery() as batch:
        BatchItem(name="X").insert(batch=batch)

    assert batch.result == LWTResult(applied=False, existing={"id": "1"})


def test_batch_query_conditional_execute_applied(registered_mock_driver):
    registered_mock_driver.set_return_rows([{"[applied]": True, "id": None, "name": None}])
    batch = BatchQuery()
    batch.add("INSERT INTO ks.t (id) VALUES (?) IF NOT EXISTS", ["1"])
    result = batch.execute()
    assert result == LWTResult(applied=True)
    assert batch.result is result


# ------------------------------------------------------------------
# Document.save/insert/delete with batch parameter (sync)
# ------------------------------------------------------------------


def test_save_with_batch(registered_mock_driver):
    batch = BatchQuery()
    p = BatchItem(name="A")
    p.save(batch=batch)

    assert len(registered_mock_driver.executed) == 0
    assert len(batch._statements) == 1
    stmt, _ = batch._statements[0]
    assert "INSERT INTO test_ks.batch_items" in stmt


def test_insert_with_batch(registered_mock_driver):
    batch = BatchQuery()
    p = BatchItem(name="B")
    p.insert(batch=batch)

    assert len(registered_mock_driver.executed) == 0
    assert len(batch._statements) == 1
    stmt, _ = batch._statements[0]
    assert "IF NOT EXISTS" in stmt


def test_delete_with_batch(registered_mock_driver):
    batch = BatchQuery()
    p = BatchItem(name="C")
    result = p.delete(batch=batch)

    assert result is None
    assert len(registered_mock_driver.executed) == 0
    assert len(batch._statements) == 1
    stmt, _ = batch._statements[0]
    assert "DELETE FROM test_ks.batch_items" in stmt


def test_full_batch_workflow(registered_mock_driver):
    with BatchQuery() as batch:
        BatchItem(name="A").save(batch=batch)
        BatchItem(name="B").save(batch=batch)
        BatchItem(name="C").insert(batch=batch)

    assert len(registered_mock_driver.executed) == 1
    stmt, _params = registered_mock_driver.executed[0]
    assert "BEGIN BATCH" in stmt
    assert "APPLY BATCH" in stmt
    assert stmt.count("INSERT INTO") == 3


# ------------------------------------------------------------------
# AsyncBatchQuery (async context manager)
# ------------------------------------------------------------------


async def test_async_batch_query_accumulates(registered_mock_driver):
    batch = AsyncBatchQuery()
    batch.add("INSERT INTO ks.t (id) VALUES (?)", ["1"])
    batch.add("INSERT INTO ks.t (id) VALUES (?)", ["2"])
    assert len(batch._statements) == 2


async def test_async_batch_query_context_manager(registered_mock_driver):
    async with AsyncBatchQuery() as batch:
        batch.add("INSERT INTO ks.t (id) VALUES (?)", ["1"])
        batch.add("INSERT INTO ks.t (id) VALUES (?)", ["2"])

    assert len(registered_mock_driver.executed) == 1
    stmt, params = registered_mock_driver.executed[0]
    assert "BEGIN BATCH" in stmt
    assert "APPLY BATCH" in stmt
    assert params == ["1", "2"]


async def test_async_batch_query_unlogged(registered_mock_driver):
    async with AsyncBatchQuery(logged=False) as batch:
        batch.add("INSERT INTO ks.t (id) VALUES (?)", ["1"])

    stmt, _ = registered_mock_driver.executed[0]
    assert "BEGIN UNLOGGED BATCH" in stmt


async def test_async_batch_query_counter_type(registered_mock_driver):
    async with AsyncBatchQuery(batch_type="COUNTER") as batch:
        batch.add("UPDATE ks.t SET c = c + ?", [1])

    stmt, _ = registered_mock_driver.executed[0]
    assert "BEGIN COUNTER BATCH" in stmt


async def test_async_batch_query_empty_noop(registered_mock_driver):
    async with AsyncBatchQuery() as _batch:
        pass

    assert len(registered_mock_driver.executed) == 0


async def test_async_batch_query_exception_no_execute(registered_mock_driver):
    try:
        async with AsyncBatchQuery() as batch:
            batch.add("INSERT INTO ks.t (id) VALUES (?)", ["1"])
            raise ValueError("boom")
    except ValueError:
        pass

    assert len(registered_mock_driver.executed) == 0


async def test_async_batch_query_non_conditional_returns_none(registered_mock_driver):
    batch = AsyncBatchQuery()
    batch.add("INSERT INTO ks.t (id) VALUES (?)", ["1"])
    assert await batch.execute() is None
    assert batch.result is None


async def test_async_batch_query_conditional_returns_lwt_result(registered_mock_driver):
    registered_mock_driver.set_return_rows([{"[applied]": False, "id": "1"}])
    async with AsyncBatchQuery() as batch:
        batch.add("UPDATE ks.t SET name = ? WHERE id = ? IF name = ?", ["n", "1", "old"])

    assert batch.result == LWTResult(applied=False, existing={"id": "1"})


async def test_async_batch_query_conditional_execute_applied(registered_mock_driver):
    registered_mock_driver.set_return_rows([{"[applied]": True}])
    batch = AsyncBatchQuery()
    batch.add("DELETE FROM ks.t WHERE id = ? IF EXISTS", ["1"])
    assert await batch.execute() == LWTResult(applied=True)


# ------------------------------------------------------------------
# Async Document.save/insert/delete with batch parameter
# ------------------------------------------------------------------


class AsyncBatchProduct(AsyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""

    class Settings:
        name = "async_batch_products"
        keyspace = "test_ks"


async def test_async_save_with_batch(registered_mock_driver):
    batch = AsyncBatchQuery()
    p = AsyncBatchProduct(name="A")
    await p.save(batch=batch)

    assert len(registered_mock_driver.executed) == 0
    assert len(batch._statements) == 1
    stmt, _ = batch._statements[0]
    assert "INSERT INTO test_ks.async_batch_products" in stmt


async def test_async_insert_with_batch(registered_mock_driver):
    batch = AsyncBatchQuery()
    p = AsyncBatchProduct(name="B")
    await p.insert(batch=batch)

    assert len(registered_mock_driver.executed) == 0
    assert len(batch._statements) == 1
    stmt, _ = batch._statements[0]
    assert "IF NOT EXISTS" in stmt


async def test_async_delete_with_batch(registered_mock_driver):
    batch = AsyncBatchQuery()
    p = AsyncBatchProduct(name="C")
    result = await p.delete(batch=batch)

    assert result is None
    assert len(registered_mock_driver.executed) == 0
    assert len(batch._statements) == 1
    stmt, _ = batch._statements[0]
    assert "DELETE FROM test_ks.async_batch_products" in stmt


async def test_async_full_batch_workflow(registered_mock_driver):
    async with AsyncBatchQuery() as batch:
        await AsyncBatchProduct(name="A").save(batch=batch)
        await AsyncBatchProduct(name="B").save(batch=batch)
        await AsyncBatchProduct(name="C").insert(batch=batch)

    assert len(registered_mock_driver.executed) == 1
    stmt, _params = registered_mock_driver.executed[0]
    assert "BEGIN BATCH" in stmt
    assert "APPLY BATCH" in stmt
    assert stmt.count("INSERT INTO") == 3


# ------------------------------------------------------------------
# Import tests
# ------------------------------------------------------------------


def test_batch_importable_from_sync():
    from coodie.sync import BatchQuery as SyncBQ

    assert SyncBQ is BatchQuery


def test_batch_importable_from_aio():
    from coodie.aio import AsyncBatchQuery as AioBQ

    assert AioBQ is AsyncBatchQuery


def test_batch_importable_from_top_level():
    from coodie import AsyncBatchQuery as ABQ
    from coodie import BatchQuery as BQ

    assert BQ is BatchQuery
    assert ABQ is AsyncBatchQuery


def test_batch_query_has_slots():
    """BatchQuery should use __slots__ for memory efficiency."""
    batch = BatchQuery()
    assert hasattr(BatchQuery, "__slots__")
    assert not hasattr(batch, "__dict__")
