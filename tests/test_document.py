"""Merged sync + async Document tests.

Every test is parametrised over ``variant`` ("sync" / "async") so that a
single test body exercises both the synchronous and asynchronous code paths.
"""

from typing import Annotated
from uuid import UUID, uuid4

import pytest
from pydantic import Field

from coodie.fields import PrimaryKey, ClusteringKey
from coodie.exceptions import (
    DocumentNotFound,
    MultipleDocumentsFound,
    InvalidQueryError,
)
from tests.conftest import _maybe_await
from tests.models import make_product, make_tagged_product, make_page_view, make_products_by_brand, make_sensor_reading


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


@pytest.fixture(params=["sync", "async"])
def variant(request):
    return request.param


@pytest.fixture
def document_cls(variant):
    if variant == "sync":
        from coodie.sync.document import Document

        return Document
    from coodie.aio.document import Document

    return Document


@pytest.fixture
def counter_document_cls(variant):
    if variant == "sync":
        from coodie.sync.document import CounterDocument

        return CounterDocument
    from coodie.aio.document import CounterDocument

    return CounterDocument


@pytest.fixture
def mv_cls(variant):
    if variant == "sync":
        from coodie.sync.document import MaterializedView

        return MaterializedView
    from coodie.aio.document import MaterializedView

    return MaterializedView


@pytest.fixture
def Product(document_cls):
    return make_product(document_cls)


@pytest.fixture
def TaggedProduct(document_cls):
    return make_tagged_product(document_cls)


@pytest.fixture
def PageView(counter_document_cls):
    return make_page_view(counter_document_cls)


@pytest.fixture
def ProductsByBrand(mv_cls):
    return make_products_by_brand(mv_cls)


@pytest.fixture
def SensorReading(document_cls):
    return make_sensor_reading(document_cls)


# ------------------------------------------------------------------
# Basic CRUD tests
# ------------------------------------------------------------------


async def test_sync_table(Product, registered_mock_driver):
    await _maybe_await(Product.sync_table)
    assert any("SYNC_TABLE" in stmt for stmt, _ in registered_mock_driver.executed)


async def test_save(Product, registered_mock_driver):
    p = Product(name="Widget", price=9.99)
    await _maybe_await(p.save)
    assert len(registered_mock_driver.executed) == 1
    stmt, params = registered_mock_driver.executed[0]
    assert "INSERT INTO test_ks.products" in stmt


async def test_insert_if_not_exists(Product, registered_mock_driver):
    p = Product(name="Widget")
    await _maybe_await(p.insert)
    stmt, _ = registered_mock_driver.executed[0]
    assert "IF NOT EXISTS" in stmt


async def test_insert_returns_lwt_result_applied(Product, registered_mock_driver):
    registered_mock_driver.set_return_rows([{"[applied]": True}])
    result = await _maybe_await(Product(name="Widget").insert)
    assert result is not None
    assert result.applied is True


async def test_insert_returns_lwt_result_not_applied(Product, registered_mock_driver):
    registered_mock_driver.set_return_rows([{"[applied]": False, "name": "Existing"}])
    result = await _maybe_await(Product(name="Widget").insert)
    assert result is not None
    assert result.applied is False
    assert result.existing == {"name": "Existing"}


# -- Phase 5: Document.save_json() ----------------------------------------


async def test_save_json(Product, registered_mock_driver):
    p = Product(name="Widget", price=9.99)
    await _maybe_await(p.save_json)
    assert len(registered_mock_driver.executed) == 1
    stmt, params = registered_mock_driver.executed[0]
    assert "INSERT INTO test_ks.products JSON ?" in stmt
    assert len(params) == 1
    import json

    data = json.loads(params[0])
    assert data["name"] == "Widget"
    assert data["price"] == 9.99


async def test_save_json_with_ttl(Product, registered_mock_driver):
    p = Product(name="Widget")
    await _maybe_await(p.save_json, ttl=300)
    stmt, _ = registered_mock_driver.executed[0]
    assert "INSERT INTO test_ks.products JSON ?" in stmt
    assert "USING TTL 300" in stmt


async def test_save_json_with_timestamp(Product, registered_mock_driver):
    p = Product(name="Widget")
    await _maybe_await(p.save_json, timestamp=123456)
    stmt, _ = registered_mock_driver.executed[0]
    assert "INSERT INTO test_ks.products JSON ?" in stmt
    assert "USING TIMESTAMP 123456" in stmt


async def test_delete(Product, registered_mock_driver):
    p = Product(name="Widget")
    await _maybe_await(p.delete)
    stmt, _ = registered_mock_driver.executed[0]
    assert "DELETE FROM test_ks.products" in stmt


async def test_find_returns_queryset(variant, Product, registered_mock_driver):
    if variant == "sync":
        from coodie.sync.query import QuerySet
    else:
        from coodie.aio.query import QuerySet

    qs = Product.find(brand="Acme")
    assert isinstance(qs, QuerySet)


async def test_find_one_returns_document(Product, registered_mock_driver):
    pid = uuid4()
    registered_mock_driver.set_return_rows(
        [{"id": pid, "name": "X", "brand": "Acme", "price": 1.0, "description": None}]
    )
    doc = await _maybe_await(Product.find_one, brand="Acme")
    assert isinstance(doc, Product)
    assert doc.brand == "Acme"


async def test_find_one_returns_none_when_empty(Product, registered_mock_driver):
    doc = await _maybe_await(Product.find_one, brand="NoSuch")
    assert doc is None


async def test_get_raises_document_not_found(Product, registered_mock_driver):
    with pytest.raises(DocumentNotFound):
        await _maybe_await(Product.get, brand="NoSuch")


async def test_find_one_raises_multiple_found(Product, registered_mock_driver):
    pid1, pid2 = uuid4(), uuid4()
    registered_mock_driver.set_return_rows(
        [
            {"id": pid1, "name": "A", "brand": "Acme", "price": 1.0, "description": None},
            {"id": pid2, "name": "B", "brand": "Acme", "price": 2.0, "description": None},
        ]
    )
    with pytest.raises(MultipleDocumentsFound):
        await _maybe_await(Product.find_one, brand="Acme")


def test_get_table_name(Product):
    assert Product._get_table() == "products"


def test_snake_case_default_table_name(document_cls):
    class MyDocument(document_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)

        class Settings:
            name = ""
            keyspace = "test_ks"

    assert MyDocument._get_table() == "my_document"


# ------------------------------------------------------------------
# Model equality tests
# ------------------------------------------------------------------


def test_model_equality(Product):
    """Two instances with the same field values are equal (Pydantic __eq__)."""
    pid = uuid4()
    a = Product(id=pid, name="Widget", price=9.99)
    b = Product(id=pid, name="Widget", price=9.99)
    assert a == b


def test_model_inequality_different_fields(Product):
    """Instances with different field values are not equal."""
    a = Product(name="Widget", price=9.99)
    b = Product(name="Gadget", price=19.99)
    assert a != b


def test_model_inequality_non_model(Product):
    """A Document instance is not equal to a non-model object."""
    p = Product(name="Widget", price=9.99)
    assert p != "not a model"
    assert p != 42
    assert p is not None


# ------------------------------------------------------------------
# CounterDocument tests
# ------------------------------------------------------------------


async def test_counter_save_raises(PageView, registered_mock_driver):
    pv = PageView(url="/home")
    with pytest.raises(InvalidQueryError, match="do not support save"):
        await _maybe_await(pv.save)


async def test_counter_insert_raises(PageView, registered_mock_driver):
    pv = PageView(url="/home")
    with pytest.raises(InvalidQueryError, match="do not support insert"):
        await _maybe_await(pv.insert)


async def test_counter_increment(PageView, registered_mock_driver):
    pv = PageView(url="/home")
    await _maybe_await(pv.increment, view_count=1)
    assert len(registered_mock_driver.executed) == 1
    stmt, params = registered_mock_driver.executed[0]
    assert "UPDATE test_ks.page_views" in stmt
    assert '"view_count" = "view_count" + ?' in stmt
    assert 'WHERE "url" = ?' in stmt
    assert params == [1, "/home"]


async def test_counter_increment_multiple(PageView, registered_mock_driver):
    pv = PageView(url="/home")
    await _maybe_await(pv.increment, view_count=5, unique_visitors=1)
    stmt, params = registered_mock_driver.executed[0]
    assert '"view_count" = "view_count" + ?' in stmt
    assert '"unique_visitors" = "unique_visitors" + ?' in stmt
    assert params == [5, 1, "/home"]


async def test_counter_decrement(PageView, registered_mock_driver):
    pv = PageView(url="/home")
    await _maybe_await(pv.decrement, view_count=1)
    stmt, params = registered_mock_driver.executed[0]
    assert '"view_count" = "view_count" + ?' in stmt
    assert params == [-1, "/home"]


# --- Phase 3: Document.update() ---


async def test_update_basic(TaggedProduct, registered_mock_driver):
    p = TaggedProduct(name="Widget", price=9.99)
    await _maybe_await(p.update, name="Gadget", price=19.99)
    assert len(registered_mock_driver.executed) == 1
    stmt, params = registered_mock_driver.executed[0]
    assert "UPDATE test_ks.tagged_products" in stmt
    assert '"name" = ?' in stmt
    assert '"price" = ?' in stmt
    assert "Gadget" in params
    assert 19.99 in params


async def test_update_updates_local_fields(TaggedProduct, registered_mock_driver):
    p = TaggedProduct(name="Widget", price=9.99)
    await _maybe_await(p.update, name="Gadget")
    assert p.name == "Gadget"


async def test_update_with_ttl(TaggedProduct, registered_mock_driver):
    p = TaggedProduct(name="Widget")
    await _maybe_await(p.update, ttl=600, name="Gadget")
    stmt, _ = registered_mock_driver.executed[0]
    assert "USING TTL 600" in stmt


async def test_update_with_if_conditions(TaggedProduct, registered_mock_driver):
    p = TaggedProduct(name="Widget")
    await _maybe_await(p.update, if_conditions={"name": "Widget"}, name="Gadget")
    stmt, params = registered_mock_driver.executed[0]
    assert 'IF "name" = ?' in stmt
    assert "Widget" in params


async def test_update_collection_add(TaggedProduct, registered_mock_driver):
    p = TaggedProduct(name="Widget")
    await _maybe_await(p.update, tags__add={"new_tag"})
    stmt, params = registered_mock_driver.executed[0]
    assert '"tags" = "tags" + ?' in stmt
    assert {"new_tag"} in params


async def test_update_collection_remove(TaggedProduct, registered_mock_driver):
    p = TaggedProduct(name="Widget")
    await _maybe_await(p.update, tags__remove={"old_tag"})
    stmt, params = registered_mock_driver.executed[0]
    assert '"tags" = "tags" - ?' in stmt
    assert {"old_tag"} in params


async def test_update_collection_append(TaggedProduct, registered_mock_driver):
    p = TaggedProduct(name="Widget")
    await _maybe_await(p.update, items__append=["z"])
    stmt, params = registered_mock_driver.executed[0]
    assert '"items" = "items" + ?' in stmt
    assert ["z"] in params


async def test_update_collection_prepend(TaggedProduct, registered_mock_driver):
    p = TaggedProduct(name="Widget")
    await _maybe_await(p.update, items__prepend=["a"])
    stmt, params = registered_mock_driver.executed[0]
    assert '"items" = ? + "items"' in stmt
    assert ["a"] in params


async def test_update_noop_when_empty(TaggedProduct, registered_mock_driver):
    p = TaggedProduct(name="Widget")
    await _maybe_await(p.update)
    assert len(registered_mock_driver.executed) == 0
    assert p.name == "Widget"


# ------------------------------------------------------------------
# Phase 2: Additional collection mutation tests
# ------------------------------------------------------------------


async def test_update_list_remove(TaggedProduct, registered_mock_driver):
    p = TaggedProduct(name="Widget")
    await _maybe_await(p.update, items__remove=["old_item"])
    stmt, params = registered_mock_driver.executed[0]
    assert '"items" = "items" - ?' in stmt
    assert ["old_item"] in params


async def test_update_map_update(TaggedProduct, registered_mock_driver):
    p = TaggedProduct(name="Widget")
    await _maybe_await(p.update, meta__update={"key": "value"})
    stmt, params = registered_mock_driver.executed[0]
    assert '"meta" = "meta" + ?' in stmt
    assert {"key": "value"} in params


async def test_update_map_remove(TaggedProduct, registered_mock_driver):
    p = TaggedProduct(name="Widget")
    await _maybe_await(p.update, meta__remove={"key"})
    stmt, params = registered_mock_driver.executed[0]
    assert '"meta" = "meta" - ?' in stmt
    assert {"key"} in params


# ------------------------------------------------------------------
# Phase 2: Counter accumulation tests
# ------------------------------------------------------------------


async def test_counter_increment_accumulates(PageView, registered_mock_driver):
    """Multiple increments generate independent UPDATE statements."""
    pv = PageView(url="/home")
    await _maybe_await(pv.increment, view_count=1)
    await _maybe_await(pv.increment, view_count=3)
    assert len(registered_mock_driver.executed) == 2
    stmt1, params1 = registered_mock_driver.executed[0]
    stmt2, params2 = registered_mock_driver.executed[1]
    assert '"view_count" = "view_count" + ?' in stmt1
    assert params1 == [1, "/home"]
    assert '"view_count" = "view_count" + ?' in stmt2
    assert params2 == [3, "/home"]


# ------------------------------------------------------------------
# Phase 2: Static column tests
# ------------------------------------------------------------------


async def test_static_column_in_schema(SensorReading):
    """Static column should appear as STATIC in the schema."""
    from coodie.schema import build_schema

    schema = build_schema(SensorReading)
    sensor_name_col = next(c for c in schema if c.name == "sensor_name")
    assert sensor_name_col.static is True
    value_col = next(c for c in schema if c.name == "value")
    assert value_col.static is False


async def test_static_column_in_create_table(SensorReading):
    """Static column should produce STATIC keyword in CREATE TABLE CQL."""
    from coodie.cql_builder import build_create_table
    from coodie.schema import build_schema

    schema = build_schema(SensorReading)
    cql = build_create_table("sensor_readings", "test_ks", schema)
    assert '"sensor_name" text STATIC' in cql
    assert '"value" float STATIC' not in cql


# ------------------------------------------------------------------
# LWT / update() tests
# ------------------------------------------------------------------


async def test_update_generates_update_cql(Product, registered_mock_driver):
    p = Product(name="Widget", price=9.99)
    await _maybe_await(p.update, name="NewWidget")
    assert len(registered_mock_driver.executed) == 1
    stmt, params = registered_mock_driver.executed[0]
    assert "UPDATE test_ks.products" in stmt
    assert 'SET "name" = ?' in stmt
    assert "NewWidget" in params


async def test_update_with_if_conditions_not_applied(Product, registered_mock_driver):
    registered_mock_driver.set_return_rows([{"[applied]": False, "name": "OtherName"}])
    p = Product(name="Widget", price=9.99)
    result = await _maybe_await(p.update, if_conditions={"name": "Widget"}, name="NewWidget")
    assert result is not None
    assert result.applied is False
    assert result.existing == {"name": "OtherName"}


async def test_update_with_if_exists(Product, registered_mock_driver):
    registered_mock_driver.set_return_rows([{"[applied]": True}])
    p = Product(name="Widget", price=9.99)
    result = await _maybe_await(p.update, if_exists=True, name="NewWidget")
    stmt, _ = registered_mock_driver.executed[0]
    assert "IF EXISTS" in stmt
    assert result is not None
    assert result.applied is True


async def test_update_no_kwargs_noop(Product, registered_mock_driver):
    p = Product(name="Widget", price=9.99)
    result = await _maybe_await(p.update)
    assert result is None
    assert len(registered_mock_driver.executed) == 0


async def test_delete_if_exists(Product, registered_mock_driver):
    registered_mock_driver.set_return_rows([{"[applied]": True}])
    p = Product(name="Widget")
    result = await _maybe_await(p.delete, if_exists=True)
    stmt, _ = registered_mock_driver.executed[0]
    assert "DELETE FROM test_ks.products" in stmt
    assert "IF EXISTS" in stmt
    assert result is not None
    assert result.applied is True


async def test_delete_if_exists_not_applied(Product, registered_mock_driver):
    registered_mock_driver.set_return_rows([{"[applied]": False}])
    p = Product(name="Widget")
    result = await _maybe_await(p.delete, if_exists=True)
    assert result is not None
    assert result.applied is False


async def test_delete_without_if_exists_returns_none(Product, registered_mock_driver):
    p = Product(name="Widget")
    result = await _maybe_await(p.delete)
    assert result is None


# ------------------------------------------------------------------
# Column-level delete (§1.8)
# ------------------------------------------------------------------


async def test_delete_columns_generates_delete_cols_cql(Product, registered_mock_driver):
    p = Product(name="Widget", price=9.99, description="old")
    with pytest.warns(UserWarning, match="delete_columns\\(\\)"):
        await _maybe_await(p.delete_columns, "description", "price")
    assert len(registered_mock_driver.executed) == 1
    stmt, params = registered_mock_driver.executed[0]
    assert 'DELETE "description", "price" FROM test_ks.products' in stmt
    assert "WHERE" in stmt


async def test_delete_columns_single(Product, registered_mock_driver):
    p = Product(name="Widget", description="to delete")
    with pytest.warns(UserWarning, match="delete_columns\\(\\)"):
        await _maybe_await(p.delete_columns, "description")
    stmt, _ = registered_mock_driver.executed[0]
    assert 'DELETE "description" FROM test_ks.products' in stmt


async def test_delete_columns_with_timestamp(Product, registered_mock_driver):
    p = Product(name="Widget")
    with pytest.warns(UserWarning, match="delete_columns\\(\\)"):
        await _maybe_await(p.delete_columns, "description", timestamp=1234567890)
    stmt, _ = registered_mock_driver.executed[0]
    assert "USING TIMESTAMP 1234567890" in stmt


async def test_delete_columns_with_consistency(Product, registered_mock_driver):
    p = Product(name="Widget")
    with pytest.warns(UserWarning, match="delete_columns\\(\\)"):
        await _maybe_await(p.delete_columns, "description", consistency="LOCAL_QUORUM")
    assert registered_mock_driver.last_consistency == "LOCAL_QUORUM"


async def test_delete_columns_with_timeout(Product, registered_mock_driver):
    p = Product(name="Widget")
    with pytest.warns(UserWarning, match="delete_columns\\(\\)"):
        await _maybe_await(p.delete_columns, "description", timeout=5.0)
    assert registered_mock_driver.last_timeout == 5.0


async def test_delete_columns_with_batch(variant, Product, registered_mock_driver):
    if variant == "sync":
        from coodie.batch import BatchQuery as BQ
    else:
        from coodie.batch import AsyncBatchQuery as BQ

    p = Product(name="Widget")
    batch = BQ()
    with pytest.warns(UserWarning, match="delete_columns\\(\\)"):
        await _maybe_await(p.delete_columns, "description", batch=batch)
    # Nothing executed on the driver yet — statement is buffered in the batch
    assert len(registered_mock_driver.executed) == 0
    assert len(batch._statements) == 1
    stmt, _ = batch._statements[0]
    assert 'DELETE "description" FROM test_ks.products' in stmt


async def test_delete_columns_warns_about_migration(Product, registered_mock_driver):
    """delete_columns() must emit a UserWarning mentioning sync_table/migrate."""
    p = Product(name="Widget")
    with pytest.warns(UserWarning, match="sync_table|coodie migrate"):
        await _maybe_await(p.delete_columns, "description")


# ------------------------------------------------------------------
# Phase 5: Query Execution Options on Document
# ------------------------------------------------------------------


async def test_save_with_timestamp(Product, registered_mock_driver):
    p = Product(name="Widget", price=9.99)
    await _maybe_await(p.save, timestamp=1234567890)
    stmt, _ = registered_mock_driver.executed[0]
    assert "USING TIMESTAMP 1234567890" in stmt


async def test_save_with_ttl_and_timestamp(Product, registered_mock_driver):
    p = Product(name="Widget", price=9.99)
    await _maybe_await(p.save, ttl=60, timestamp=1234567890)
    stmt, _ = registered_mock_driver.executed[0]
    assert "USING TTL 60 AND TIMESTAMP 1234567890" in stmt


async def test_save_with_consistency(Product, registered_mock_driver):
    p = Product(name="Widget", price=9.99)
    await _maybe_await(p.save, consistency="LOCAL_QUORUM")
    assert registered_mock_driver.last_consistency == "LOCAL_QUORUM"


async def test_save_with_timeout(Product, registered_mock_driver):
    p = Product(name="Widget", price=9.99)
    await _maybe_await(p.save, timeout=5.0)
    assert registered_mock_driver.last_timeout == 5.0


async def test_insert_with_timestamp(Product, registered_mock_driver):
    p = Product(name="Widget")
    await _maybe_await(p.insert, timestamp=1234567890)
    stmt, _ = registered_mock_driver.executed[0]
    assert "USING TIMESTAMP 1234567890" in stmt


async def test_insert_with_consistency(Product, registered_mock_driver):
    p = Product(name="Widget")
    await _maybe_await(p.insert, consistency="LOCAL_QUORUM")
    assert registered_mock_driver.last_consistency == "LOCAL_QUORUM"


async def test_delete_with_timestamp(Product, registered_mock_driver):
    p = Product(name="Widget")
    await _maybe_await(p.delete, timestamp=1234567890)
    stmt, _ = registered_mock_driver.executed[0]
    assert "USING TIMESTAMP 1234567890" in stmt


async def test_delete_with_consistency(Product, registered_mock_driver):
    p = Product(name="Widget")
    await _maybe_await(p.delete, consistency="LOCAL_QUORUM")
    assert registered_mock_driver.last_consistency == "LOCAL_QUORUM"


# ------------------------------------------------------------------
# execute_raw tests
# ------------------------------------------------------------------


async def test_execute_raw(variant, registered_mock_driver):
    if variant == "sync":
        from coodie.sync import execute_raw
    else:
        from coodie.aio import execute_raw

    registered_mock_driver.set_return_rows([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])
    rows = await _maybe_await(execute_raw, "SELECT * FROM test_ks.users")
    assert len(rows) == 2
    assert rows[0]["name"] == "Alice"
    stmt, params = registered_mock_driver.executed[0]
    assert stmt == "SELECT * FROM test_ks.users"
    assert params == []


async def test_execute_raw_with_params(variant, registered_mock_driver):
    if variant == "sync":
        from coodie.sync import execute_raw
    else:
        from coodie.aio import execute_raw

    registered_mock_driver.set_return_rows([{"id": 1, "name": "Alice"}])
    rows = await _maybe_await(execute_raw, "SELECT * FROM test_ks.users WHERE id = ?", [1])
    assert len(rows) == 1
    stmt, params = registered_mock_driver.executed[0]
    assert stmt == "SELECT * FROM test_ks.users WHERE id = ?"
    assert params == [1]


async def test_execute_raw_empty_result(variant, registered_mock_driver):
    if variant == "sync":
        from coodie.sync import execute_raw
    else:
        from coodie.aio import execute_raw

    rows = await _maybe_await(execute_raw, "SELECT * FROM test_ks.users WHERE id = ?", [999])
    assert rows == []


async def test_execute_raw_insert(variant, registered_mock_driver):
    if variant == "sync":
        from coodie.sync import execute_raw
    else:
        from coodie.aio import execute_raw

    await _maybe_await(execute_raw, "INSERT INTO test_ks.users (id, name) VALUES (?, ?)", [1, "Alice"])
    stmt, params = registered_mock_driver.executed[0]
    assert "INSERT INTO" in stmt
    assert params == [1, "Alice"]


# ------------------------------------------------------------------
# Phase 8: Model Enhancements
# ------------------------------------------------------------------


async def test_create_classmethod(Product, registered_mock_driver):
    """8.1 – Document.create(**kwargs) constructs + saves."""
    doc = await _maybe_await(Product.create, name="NewWidget", price=42.0)
    assert isinstance(doc, Product)
    assert doc.name == "NewWidget"
    assert doc.price == 42.0
    assert len(registered_mock_driver.executed) == 1
    stmt, _ = registered_mock_driver.executed[0]
    assert "INSERT INTO test_ks.products" in stmt


async def test_abstract_skips_sync_table(document_cls, registered_mock_driver):
    """8.2 – __abstract__ = True prevents table creation."""

    class AbstractBase(document_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)

        class Settings:
            name = "abstract_base"
            keyspace = "test_ks"
            __abstract__ = True

    await _maybe_await(AbstractBase.sync_table)
    assert len(registered_mock_driver.executed) == 0


async def test_default_ttl_in_sync_table(document_cls, registered_mock_driver):
    """8.3 – __default_ttl__ is passed as table_options."""

    class TTLModel(document_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)

        class Settings:
            name = "ttl_models"
            keyspace = "test_ks"
            __default_ttl__ = 86400

    await _maybe_await(TTLModel.sync_table)
    options = TTLModel._get_table_options()
    assert options == {"default_time_to_live": 86400}


async def test_options_in_sync_table(document_cls, registered_mock_driver):
    """8.4 – __options__ dict is passed as table_options."""

    class OptionsModel(document_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)

        class Settings:
            name = "options_models"
            keyspace = "test_ks"
            __options__ = {"gc_grace_seconds": 864000, "comment": "test table"}

    await _maybe_await(OptionsModel.sync_table)
    options = OptionsModel._get_table_options()
    assert options == {"gc_grace_seconds": 864000, "comment": "test table"}


def test_default_ttl_merged_with_options(document_cls):
    """8.3+8.4 – __default_ttl__ is merged into __options__."""

    class MergedModel(document_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)

        class Settings:
            name = "merged"
            keyspace = "test_ks"
            __default_ttl__ = 3600
            __options__ = {"gc_grace_seconds": 1000}

    options = MergedModel._get_table_options()
    assert options == {"default_time_to_live": 3600, "gc_grace_seconds": 1000}


async def test_connection_setting(document_cls, registered_mock_driver):
    """8.5 – Settings.connection selects named driver."""
    from coodie.drivers import register_driver

    second = type(registered_mock_driver)()
    register_driver("secondary", second)

    class ConnectedModel(document_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        name: str = ""

        class Settings:
            name = "connected"
            keyspace = "test_ks"
            connection = "secondary"

    doc = ConnectedModel(name="Hi")
    await _maybe_await(doc.save)
    assert len(second.executed) == 1
    assert len(registered_mock_driver.executed) == 0


async def test_drop_table(Product, registered_mock_driver):
    """8.6 – drop_table() classmethod."""
    await _maybe_await(Product.drop_table)
    assert len(registered_mock_driver.executed) == 1
    stmt, params = registered_mock_driver.executed[0]
    assert stmt == "DROP TABLE IF EXISTS test_ks.products"
    assert params == []


def test_table_name(Product):
    """8.7 – table_name() wraps _get_table()."""
    assert Product.table_name() == "products"


def test_table_name_snake_case(document_cls):
    """8.7 – table_name() uses snake_case when no Settings.name."""

    class MySpecialDocument(document_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)

        class Settings:
            name = ""
            keyspace = "test_ks"

    assert MySpecialDocument.table_name() == "my_special_document"


# ------------------------------------------------------------------
# Phase 12: Materialized View
# ------------------------------------------------------------------


async def test_materialized_view_sync_view(ProductsByBrand, registered_mock_driver):
    """12.3 – sync_view() generates CREATE MATERIALIZED VIEW."""
    await _maybe_await(ProductsByBrand.sync_view)
    assert len(registered_mock_driver.executed) == 1
    stmt, params = registered_mock_driver.executed[0]
    assert "CREATE MATERIALIZED VIEW IF NOT EXISTS test_ks.products_by_brand" in stmt
    assert "AS SELECT * FROM test_ks.products" in stmt
    assert '"brand" IS NOT NULL' in stmt
    assert '"id" IS NOT NULL' in stmt
    assert params == []


async def test_materialized_view_drop_view(ProductsByBrand, registered_mock_driver):
    """12.3 – drop_view() generates DROP MATERIALIZED VIEW."""
    await _maybe_await(ProductsByBrand.drop_view)
    assert len(registered_mock_driver.executed) == 1
    stmt, params = registered_mock_driver.executed[0]
    assert stmt == "DROP MATERIALIZED VIEW IF EXISTS test_ks.products_by_brand"
    assert params == []


async def test_materialized_view_save_raises(ProductsByBrand, registered_mock_driver):
    """12.3 – save() is forbidden on materialized views."""
    mv = ProductsByBrand(brand="Acme")
    with pytest.raises(InvalidQueryError, match="read-only"):
        await _maybe_await(mv.save)


async def test_materialized_view_insert_raises(ProductsByBrand, registered_mock_driver):
    """12.3 – insert() is forbidden on materialized views."""
    mv = ProductsByBrand(brand="Acme")
    with pytest.raises(InvalidQueryError, match="read-only"):
        await _maybe_await(mv.insert)


async def test_materialized_view_delete_raises(ProductsByBrand, registered_mock_driver):
    """12.3 – delete() is forbidden on materialized views."""
    mv = ProductsByBrand(brand="Acme")
    with pytest.raises(InvalidQueryError, match="read-only"):
        await _maybe_await(mv.delete)


async def test_materialized_view_update_raises(ProductsByBrand, registered_mock_driver):
    """12.3 – update() is forbidden on materialized views."""
    mv = ProductsByBrand(brand="Acme")
    with pytest.raises(InvalidQueryError, match="read-only"):
        await _maybe_await(mv.update, name="X")


async def test_materialized_view_find(variant, ProductsByBrand, registered_mock_driver):
    """12.3 – find() works on materialized views (read operations allowed)."""
    if variant == "sync":
        from coodie.sync.query import QuerySet
    else:
        from coodie.aio.query import QuerySet

    qs = ProductsByBrand.find(brand="Acme")
    assert isinstance(qs, QuerySet)


async def test_materialized_view_find_one(ProductsByBrand, registered_mock_driver):
    """12.3 – find_one() works on materialized views."""
    pid = uuid4()
    registered_mock_driver.set_return_rows([{"brand": "Acme", "id": pid, "name": "Widget", "price": 9.99}])
    doc = await _maybe_await(ProductsByBrand.find_one, brand="Acme")
    assert isinstance(doc, ProductsByBrand)
    assert doc.brand == "Acme"


def test_materialized_view_no_base_table_raises(mv_cls):
    """12.3 – Missing __base_table__ raises InvalidQueryError."""

    class BadView(mv_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)

        class Settings:
            name = "bad_view"
            keyspace = "test_ks"

    with pytest.raises(InvalidQueryError, match="__base_table__"):
        BadView._get_base_table()


async def test_materialized_view_custom_where_clause(mv_cls, registered_mock_driver):
    """12.3 – Custom __where_clause__ is used."""

    class CustomWhereView(mv_cls):
        brand: Annotated[str, PrimaryKey()]
        id: Annotated[UUID, ClusteringKey()] = Field(default_factory=uuid4)
        name: str = ""

        class Settings:
            name = "custom_where_view"
            keyspace = "test_ks"
            __base_table__ = "products"
            __where_clause__ = '"brand" IS NOT NULL AND "id" IS NOT NULL AND "brand" = \'Acme\''

    await _maybe_await(CustomWhereView.sync_view)
    stmt, _ = registered_mock_driver.executed[0]
    assert "\"brand\" = 'Acme'" in stmt


async def test_materialized_view_custom_columns(mv_cls, registered_mock_driver):
    """12.3 – Custom __view_columns__ selects specific columns."""

    class ColumnsView(mv_cls):
        brand: Annotated[str, PrimaryKey()]
        id: Annotated[UUID, ClusteringKey()] = Field(default_factory=uuid4)
        name: str = ""

        class Settings:
            name = "columns_view"
            keyspace = "test_ks"
            __base_table__ = "products"
            __view_columns__ = ["brand", "id", "name"]

    await _maybe_await(ColumnsView.sync_view)
    stmt, _ = registered_mock_driver.executed[0]
    assert 'SELECT "brand", "id", "name" FROM test_ks.products' in stmt


# ------------------------------------------------------------------
# Phase 1: Document.truncate()
# ------------------------------------------------------------------


async def test_truncate_executes_truncate_cql(Product, registered_mock_driver):
    await _maybe_await(Product.truncate)
    stmt, params = registered_mock_driver.executed[0]
    assert stmt == "TRUNCATE TABLE test_ks.products"
    assert params == []
