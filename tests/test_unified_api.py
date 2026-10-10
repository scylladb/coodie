"""Unified sync/async API: every model supports both modes on the same instance.

The core property: for each I/O method, the un-suffixed default, the explicit
``*_sync`` twin and the explicit ``*_async`` twin issue the same CQL and
return the same result, on both sync-default and async-default models.

Sync calls run outside any event loop (async calls go through
``asyncio.run``), so they don't trigger ``BlockingCallWarning``.
"""

import asyncio
import inspect
import warnings
from typing import Annotated
from uuid import UUID, uuid4

import pytest
from pydantic import Field

from coodie import aio, sync
from coodie.batch import AsyncBatchQuery, BatchQuery
from coodie.exceptions import BlockingCallWarning, InvalidQueryError
from coodie.fields import PrimaryKey
from tests.models import make_page_view, make_product, make_products_by_brand

UID = UUID("12345678-1234-5678-1234-567812345678")
ROW = {"id": UID, "name": "x", "brand": "b", "price": 1.0, "description": None}

MODES = ["default", "sync", "async"]


@pytest.fixture(params=["sync", "aio"])
def pkg(request):
    return sync if request.param == "sync" else aio


@pytest.fixture
def Product(pkg):
    return make_product(pkg.Document)


def run(target, name, mode, /, *args, **kwargs):
    """Call *name* on *target* in *mode*, resolving coroutines with ``asyncio.run``."""
    attr = name if mode == "default" else f"{name}_{mode}"
    result = getattr(target, attr)(*args, **kwargs)
    return asyncio.run(result) if inspect.iscoroutine(result) else result


def run_all_modes(driver, target_factory, name, /, *args, rows=None, **kwargs):
    """Run *name* in every mode; return ``[(executed_cql, result), ...]``."""
    outcomes = []
    for mode in MODES:
        driver.executed.clear()
        driver._return_rows.clear()
        if rows is not None:
            driver.set_return_rows([dict(r) for r in rows])
        result = run(target_factory(), name, mode, *args, **kwargs)
        outcomes.append((list(driver.executed), result))
    return outcomes


DOCUMENT_CALLS = [
    # (method, args, kwargs, rows, on_instance)
    ("save", (), {"ttl": 5}, None, True),
    ("save_json", (), {}, None, True),
    ("insert", (), {}, [{"[applied]": True}], True),
    ("delete", (), {}, None, True),
    ("delete", (), {"if_exists": True}, [{"[applied]": False}], True),
    ("update", (), {"name": "y"}, None, True),
    ("delete_columns", ("description",), {}, None, True),
    ("sync_table", (), {}, None, False),
    ("drop_table", (), {}, None, False),
    ("truncate", (), {}, None, False),
    ("create", (), {"id": UID, "name": "x"}, None, False),
    ("find_one", (), {"id": UID}, [ROW], False),
    ("get", (), {"id": UID}, [ROW], False),
]


@pytest.mark.filterwarnings("ignore:delete_columns:UserWarning")
@pytest.mark.parametrize(("name", "args", "kwargs", "rows", "on_instance"), DOCUMENT_CALLS)
def test_document_methods_same_in_every_mode(Product, registered_mock_driver, name, args, kwargs, rows, on_instance):
    def target():
        return Product(id=UID, name="x") if on_instance else Product

    outcomes = run_all_modes(registered_mock_driver, target, name, *args, rows=rows, **kwargs)
    assert outcomes[0][0], f"{name} executed nothing"
    assert outcomes[0] == outcomes[1] == outcomes[2]


QUERYSET_CALLS = [
    ("all", (), {}, [ROW]),
    ("paged_all", (), {}, [ROW]),
    ("first", (), {}, [ROW]),
    ("count", (), {}, [{"count": 3}]),
    ("aggregate", (), {"total": "sum(price)"}, [{"s": 9.0}]),
    ("sum", ("price",), {}, [{"s": 9.0}]),
    ("avg", ("price",), {}, [{"s": 9.0}]),
    ("min", ("price",), {}, [{"s": 9.0}]),
    ("max", ("price",), {}, [{"s": 9.0}]),
    ("json", (), {}, [{"[json]": "{}"}]),
    ("writetime", ("name",), {}, [{"w": 1}]),
    ("column_ttl", ("name",), {}, [{"t": 1}]),
    ("delete", (), {}, None),
    ("create", (), {"id": UID, "name": "x"}, None),
    ("update", (), {"name": "y"}, None),
]


@pytest.mark.parametrize(("name", "args", "kwargs", "rows"), QUERYSET_CALLS)
def test_queryset_methods_same_in_every_mode(Product, registered_mock_driver, name, args, kwargs, rows):
    outcomes = run_all_modes(
        registered_mock_driver, lambda: Product.find(id=UID).ttl(7), name, *args, rows=rows, **kwargs
    )
    assert outcomes[0][0], f"{name} executed nothing"
    assert outcomes[0] == outcomes[1] == outcomes[2]


@pytest.mark.parametrize("name", ["increment", "decrement"])
def test_counter_methods_same_in_every_mode(pkg, registered_mock_driver, name):
    PageView = make_page_view(pkg.CounterDocument)
    outcomes = run_all_modes(registered_mock_driver, lambda: PageView(url="/"), name, view_count=2)
    assert outcomes[0][0]
    assert outcomes[0] == outcomes[1] == outcomes[2]


@pytest.mark.parametrize("name", ["sync_view", "drop_view"])
def test_view_methods_same_in_every_mode(pkg, registered_mock_driver, name):
    View = make_products_by_brand(pkg.MaterializedView)
    outcomes = run_all_modes(registered_mock_driver, lambda: View, name)
    assert outcomes[0][0]
    assert outcomes[0] == outcomes[1] == outcomes[2]


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("name", ["save", "insert"])
def test_counter_rejects_writes_in_every_mode(pkg, registered_mock_driver, name, mode):
    PageView = make_page_view(pkg.CounterDocument)
    with pytest.raises(InvalidQueryError):
        run(PageView(url="/"), name, mode)


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("name", ["save", "insert", "delete", "update"])
def test_view_rejects_writes_in_every_mode(pkg, registered_mock_driver, name, mode):
    View = make_products_by_brand(pkg.MaterializedView)
    with pytest.raises(InvalidQueryError):
        run(View.model_construct(), name, mode)


# ------------------------------------------------------------------
# Default mode follows the base class
# ------------------------------------------------------------------


def test_default_mode_follows_base_class():
    assert not inspect.iscoroutinefunction(sync.Document.save)
    assert inspect.iscoroutinefunction(sync.Document.save_async)
    assert inspect.iscoroutinefunction(aio.Document.save)
    assert not inspect.iscoroutinefunction(aio.Document.save_sync)
    assert not inspect.iscoroutinefunction(sync.QuerySet.all)
    assert inspect.iscoroutinefunction(aio.QuerySet.all)


def test_sync_and_aio_models_stay_distinct():
    SyncProduct = make_product(sync.Document)
    assert issubclass(SyncProduct, sync.Document)
    assert not issubclass(SyncProduct, aio.Document)
    assert issubclass(sync.CounterDocument, sync.Document)
    assert issubclass(aio.MaterializedView, aio.Document)


# ------------------------------------------------------------------
# Iteration, batches
# ------------------------------------------------------------------


def test_queryset_supports_for_and_async_for(Product, registered_mock_driver):
    qs = Product.find(id=UID)
    registered_mock_driver.set_return_rows([dict(ROW)])
    assert [p.id for p in qs] == [UID]

    async def collect():
        return [p.id async for p in qs]

    registered_mock_driver.set_return_rows([dict(ROW)])
    assert asyncio.run(collect()) == [UID]


def test_one_batch_class_for_both_protocols(registered_mock_driver):
    SyncProduct = make_product(sync.Document)
    AioProduct = make_product(aio.Document)

    with BatchQuery() as batch:
        SyncProduct(name="a").save(batch=batch)
        AioProduct(name="b").save_sync(batch=batch)
    assert len(registered_mock_driver.executed) == 1

    async def async_batch():
        async with BatchQuery() as batch:
            await AioProduct(name="a").save(batch=batch)
            SyncProduct(name="b").save(batch=batch)

    asyncio.run(async_batch())
    assert len(registered_mock_driver.executed) == 2
    assert registered_mock_driver.executed[0][0].startswith("BEGIN BATCH")


def test_async_batch_query_execute_is_still_a_coroutine(registered_mock_driver):
    assert inspect.iscoroutinefunction(AsyncBatchQuery.execute)
    assert not inspect.iscoroutinefunction(BatchQuery.execute)
    assert issubclass(AsyncBatchQuery, BatchQuery)


# ------------------------------------------------------------------
# Overrides
# ------------------------------------------------------------------


class Stamped(aio.Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""
    calls: list[str] = Field(default_factory=list)

    def save_sync(self, **kw):
        self.calls.append("sync")
        return super().save_sync(**kw)

    async def save_async(self, **kw):
        self.calls.append("async")
        return await super().save_async(**kw)

    class Settings:
        name = "stamped"
        keyspace = "test_ks"


def test_overriding_explicit_twins_applies_to_alias_and_create(registered_mock_driver):
    doc = Stamped()
    asyncio.run(doc.save())
    doc.save_sync()
    assert doc.calls == ["async", "sync"]
    assert Stamped.create_sync().calls == ["sync"]
    assert asyncio.run(Stamped.create()).calls == ["async"]


class LegacyOverride(sync.Document):
    """Existing-style model: overrides the un-suffixed save()."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    calls: list[str] = Field(default_factory=list)

    def save(self, **kw):
        self.calls.append("override")
        return super().save(**kw)

    class Settings:
        name = "legacy"
        keyspace = "test_ks"


class DelegatingOverride(sync.Document):
    """Override that delegates straight to the explicit twin."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)

    def save(self, **kw):
        return self.save_sync(**kw)

    class Settings:
        name = "delegating"
        keyspace = "test_ks"


def test_legacy_override_still_used_by_default_api_without_warnings(registered_mock_driver):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        doc = LegacyOverride()
        doc.save()
        assert LegacyOverride.create().calls == ["override"]
        DelegatingOverride().save()
    assert doc.calls == ["override"]


def test_calling_twin_that_skips_legacy_override_warns(registered_mock_driver):
    doc = LegacyOverride()
    with pytest.warns(UserWarning, match=r"overrides save\(\)") as record:
        doc.save_sync()
    assert record[0].filename == __file__

    async def main():
        await doc.save_async()

    with pytest.warns(UserWarning, match=r"overrides save\(\)") as record:
        asyncio.run(main())
    assert record[0].filename == __file__


# ------------------------------------------------------------------
# Blocking-call guard
# ------------------------------------------------------------------


def test_sync_call_inside_loop_on_async_model_warns_once(registered_mock_driver):
    AioProduct = make_product(aio.Document)

    async def main():
        registered_mock_driver.set_return_rows([dict(ROW)])
        AioProduct.get_sync(id=UID)

    with pytest.warns(BlockingCallWarning, match="get_async|_async") as record:
        asyncio.run(main())
    assert len(record) == 1
    assert record[0].filename == __file__


def test_sync_model_inside_loop_does_not_warn(registered_mock_driver):
    SyncProduct = make_product(sync.Document)

    async def main():
        SyncProduct(name="a").save()

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        asyncio.run(main())


def test_sync_call_outside_loop_does_not_warn(registered_mock_driver):
    AioProduct = make_product(aio.Document)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        AioProduct(name="a").save_sync()
