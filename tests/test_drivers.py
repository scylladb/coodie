from __future__ import annotations

import importlib.util
import logging
from collections import namedtuple
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import coodie.drivers as _drivers_mod
from coodie.drivers import (
    _registry,
    get_driver,
    init_coodie,
    init_coodie_async,
    register_driver,
)
from coodie.drivers.base import AbstractDriver
from coodie.exceptions import ConfigurationError

# ------------------------------------------------------------------
# Registry tests
# ------------------------------------------------------------------


def test_register_and_get_driver(mock_driver):
    _registry.clear()
    register_driver("test", mock_driver, default=True)
    assert get_driver("test") is mock_driver
    assert get_driver() is mock_driver
    _registry.clear()


def test_get_driver_no_registration_raises():
    _registry.clear()
    with pytest.raises(ConfigurationError):
        get_driver()
    _registry.clear()


def test_register_driver_on_empty_registry(mock_driver):
    """register_driver succeeds on a completely empty registry."""
    _registry.clear()
    _drivers_mod._default_driver_name = None
    register_driver("fresh", mock_driver)
    assert get_driver("fresh") is mock_driver
    # Also becomes the default since no default existed
    assert get_driver() is mock_driver
    _registry.clear()
    _drivers_mod._default_driver_name = None


def test_mock_driver_execute(mock_driver):
    mock_driver.set_return_rows([{"id": "1", "name": "Alice"}])
    rows = mock_driver.execute("SELECT * FROM ks.t", [])
    assert rows == [{"id": "1", "name": "Alice"}]
    assert mock_driver.executed[0][0] == "SELECT * FROM ks.t"


async def test_mock_driver_execute_async(mock_driver):
    mock_driver.set_return_rows([{"id": "2"}])
    rows = await mock_driver.execute_async("SELECT * FROM ks.t", [])
    assert rows == [{"id": "2"}]


def test_abstract_driver_cannot_instantiate():
    with pytest.raises(TypeError):
        AbstractDriver()


# ------------------------------------------------------------------
# Phase 5: consistency and timeout parameters
# ------------------------------------------------------------------


def test_mock_driver_execute_with_consistency(mock_driver):
    mock_driver.set_return_rows([{"id": "1"}])
    mock_driver.execute("SELECT * FROM ks.t", [], consistency="LOCAL_QUORUM")
    assert mock_driver.last_consistency == "LOCAL_QUORUM"


def test_mock_driver_execute_with_timeout(mock_driver):
    mock_driver.set_return_rows([{"id": "1"}])
    mock_driver.execute("SELECT * FROM ks.t", [], timeout=5.0)
    assert mock_driver.last_timeout == 5.0


async def test_mock_driver_execute_async_with_consistency(mock_driver):
    mock_driver.set_return_rows([{"id": "1"}])
    await mock_driver.execute_async("SELECT * FROM ks.t", [], consistency="LOCAL_QUORUM")
    assert mock_driver.last_consistency == "LOCAL_QUORUM"


async def test_mock_driver_execute_async_with_timeout(mock_driver):
    mock_driver.set_return_rows([{"id": "1"}])
    await mock_driver.execute_async("SELECT * FROM ks.t", [], timeout=5.0)
    assert mock_driver.last_timeout == 5.0


def test_mock_driver_defaults_none_consistency(mock_driver):
    mock_driver.execute("SELECT * FROM ks.t", [])
    assert mock_driver.last_consistency is None


def test_mock_driver_defaults_none_timeout(mock_driver):
    mock_driver.execute("SELECT * FROM ks.t", [])
    assert mock_driver.last_timeout is None


# ------------------------------------------------------------------
# Phase 6: init_coodie / init_coodie_async tests
# ------------------------------------------------------------------


def test_init_coodie_with_session():
    _registry.clear()
    mock_session = MagicMock()
    mock_session.cluster = MagicMock()
    driver = init_coodie(session=mock_session, keyspace="ks")
    assert get_driver() is driver
    _registry.clear()


def test_init_coodie_cassandra_alias():
    _registry.clear()
    mock_session = MagicMock()
    mock_session.cluster = MagicMock()
    driver = init_coodie(session=mock_session, keyspace="ks", driver_type="cassandra")
    assert get_driver() is driver
    _registry.clear()


def test_init_coodie_unknown_driver_type():
    _registry.clear()
    with pytest.raises(ConfigurationError, match="Unknown driver_type"):
        init_coodie(driver_type="unknown", keyspace="ks")
    _registry.clear()


def test_init_coodie_acsylla_requires_session():
    _registry.clear()
    with (
        patch.dict("sys.modules", {"acsylla": MagicMock()}),
        pytest.raises(ConfigurationError, match="hosts or a pre-created acsylla session"),
    ):
        init_coodie(driver_type="acsylla", keyspace="ks")
    _registry.clear()


def test_init_coodie_acsylla_with_session():
    _registry.clear()
    mock_session = MagicMock()
    with patch.dict("sys.modules", {"acsylla": MagicMock()}), pytest.warns(UserWarning, match="sync calls.*may hang"):
        driver = init_coodie(session=mock_session, keyspace="ks", driver_type="acsylla")
    assert get_driver() is driver
    _registry.clear()


def test_init_coodie_acsylla_with_hosts_returns_sync_capable_driver():
    """init_coodie(driver_type='acsylla', hosts=...) returns a driver with _bridge_to_bg_loop=True."""
    _registry.clear()
    mock_acsylla = MagicMock()
    mock_cluster = MagicMock()
    mock_session = MagicMock()
    mock_acsylla.create_cluster = MagicMock(return_value=mock_cluster)
    mock_cluster.create_session = AsyncMock(return_value=mock_session)

    with patch.dict("sys.modules", {"acsylla": mock_acsylla}):
        driver = init_coodie(hosts=["127.0.0.1"], keyspace="ks", driver_type="acsylla")
    assert get_driver() is driver
    assert driver._bridge_to_bg_loop is True
    mock_acsylla.create_cluster.assert_called_once()
    mock_cluster.create_session.assert_awaited_once_with(keyspace="ks")
    _registry.clear()


async def test_init_coodie_async_acsylla_with_hosts():
    _registry.clear()
    mock_acsylla = MagicMock()
    mock_cluster = MagicMock()
    mock_session = MagicMock()
    mock_acsylla.create_cluster = MagicMock(return_value=mock_cluster)
    mock_cluster.create_session = AsyncMock(return_value=mock_session)

    with patch.dict("sys.modules", {"acsylla": mock_acsylla}):
        driver = await init_coodie_async(
            hosts=["127.0.0.1"],
            keyspace="ks",
            driver_type="acsylla",
        )
    assert get_driver() is driver
    mock_acsylla.create_cluster.assert_called_once()
    mock_cluster.create_session.assert_awaited_once_with(keyspace="ks")
    # AcsyllaDriver.connect() routes session to bg loop for sync bridge
    assert driver._bridge_to_bg_loop is True
    _registry.clear()


async def test_init_coodie_async_acsylla_with_session_no_bridge():
    """Pre-created session passed to init_coodie_async keeps _bridge_to_bg_loop=False."""
    _registry.clear()
    mock_session = MagicMock()
    with patch.dict("sys.modules", {"acsylla": MagicMock()}), pytest.warns(UserWarning, match="sync calls.*may hang"):
        driver = await init_coodie_async(
            session=mock_session,
            keyspace="ks",
            driver_type="acsylla",
        )
    assert get_driver() is driver
    assert driver._bridge_to_bg_loop is False
    _registry.clear()


# ------------------------------------------------------------------
# Phase 3 (client-encryption): explicit SSL parameter tests
# ------------------------------------------------------------------


def test_init_coodie_ssl_context_forwarded_to_cluster():
    """ssl_context= is forwarded into Cluster() when creating a new session."""
    import ssl

    _registry.clear()
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    mock_cluster_cls = MagicMock()
    mock_cluster_inst = MagicMock()
    mock_session = MagicMock()
    mock_cluster_cls.return_value = mock_cluster_inst
    mock_cluster_inst.connect.return_value = mock_session
    mock_session.cluster = mock_cluster_inst

    with (
        patch("coodie.drivers.cassandra.CassandraDriver"),
        patch.dict("sys.modules", {"cassandra": MagicMock(), "cassandra.cluster": MagicMock(Cluster=mock_cluster_cls)}),
    ):
        init_coodie(
            hosts=["node1"],
            keyspace="ks",
            ssl_context=ctx,
        )
    mock_cluster_cls.assert_called_once_with(["node1"], ssl_context=ctx)
    _registry.clear()


def test_init_coodie_ssl_context_not_added_when_none():
    """When ssl_context is None, it is NOT passed to Cluster()."""
    _registry.clear()

    mock_cluster_cls = MagicMock()
    mock_cluster_inst = MagicMock()
    mock_session = MagicMock()
    mock_cluster_cls.return_value = mock_cluster_inst
    mock_cluster_inst.connect.return_value = mock_session
    mock_session.cluster = mock_cluster_inst

    with (
        patch("coodie.drivers.cassandra.CassandraDriver"),
        patch.dict("sys.modules", {"cassandra": MagicMock(), "cassandra.cluster": MagicMock(Cluster=mock_cluster_cls)}),
    ):
        init_coodie(
            hosts=["node1"],
            keyspace="ks",
        )
    mock_cluster_cls.assert_called_once_with(["node1"])
    _registry.clear()


async def test_init_coodie_async_ssl_params_forwarded_to_acsylla():
    """ssl_enabled, ssl_trusted_cert, etc. are forwarded to acsylla.create_cluster()."""
    _registry.clear()
    mock_acsylla = MagicMock()
    mock_cluster = MagicMock()
    mock_session = MagicMock()
    mock_acsylla.create_cluster = MagicMock(return_value=mock_cluster)
    mock_cluster.create_session = AsyncMock(return_value=mock_session)

    with patch.dict("sys.modules", {"acsylla": mock_acsylla}):
        await init_coodie_async(
            hosts=["node1"],
            keyspace="ks",
            driver_type="acsylla",
            ssl_enabled=True,
            ssl_trusted_cert="-----BEGIN CERTIFICATE-----\nfake\n-----END CERTIFICATE-----",
            ssl_verify_flags=0,
        )

    call_kwargs = mock_acsylla.create_cluster.call_args
    assert call_kwargs[1]["ssl_enabled"] is True
    assert "BEGIN CERTIFICATE" in call_kwargs[1]["ssl_trusted_cert"]
    assert call_kwargs[1]["ssl_verify_flags"] == 0
    _registry.clear()


async def test_init_coodie_async_ssl_params_not_added_when_none():
    """When ssl_* params are None, they are NOT passed to acsylla.create_cluster()."""
    _registry.clear()
    mock_acsylla = MagicMock()
    mock_cluster = MagicMock()
    mock_session = MagicMock()
    mock_acsylla.create_cluster = MagicMock(return_value=mock_cluster)
    mock_cluster.create_session = AsyncMock(return_value=mock_session)

    with patch.dict("sys.modules", {"acsylla": mock_acsylla}):
        await init_coodie_async(
            hosts=["node1"],
            keyspace="ks",
            driver_type="acsylla",
        )

    call_kwargs = mock_acsylla.create_cluster.call_args
    assert "ssl_enabled" not in call_kwargs[1]
    assert "ssl_trusted_cert" not in call_kwargs[1]
    assert "ssl_verify_flags" not in call_kwargs[1]
    _registry.clear()


async def test_init_coodie_async_ssl_cert_and_key_forwarded():
    """ssl_cert and ssl_private_key are forwarded for mutual TLS."""
    _registry.clear()
    mock_acsylla = MagicMock()
    mock_cluster = MagicMock()
    mock_session = MagicMock()
    mock_acsylla.create_cluster = MagicMock(return_value=mock_cluster)
    mock_cluster.create_session = AsyncMock(return_value=mock_session)

    with patch.dict("sys.modules", {"acsylla": mock_acsylla}):
        await init_coodie_async(
            hosts=["node1"],
            keyspace="ks",
            driver_type="acsylla",
            ssl_enabled=True,
            ssl_trusted_cert="ca-pem",
            ssl_cert="client-cert-pem",
            ssl_private_key="client-key-pem",
        )

    call_kwargs = mock_acsylla.create_cluster.call_args
    assert call_kwargs[1]["ssl_cert"] == "client-cert-pem"
    assert call_kwargs[1]["ssl_private_key"] == "client-key-pem"
    _registry.clear()


async def test_init_coodie_async_ssl_context_forwarded_to_cassandra():
    """ssl_context= on init_coodie_async() with cassandra driver forwards to init_coodie()."""
    import ssl

    _registry.clear()
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    mock_cluster_cls = MagicMock()
    mock_cluster_inst = MagicMock()
    mock_session = MagicMock()
    mock_cluster_cls.return_value = mock_cluster_inst
    mock_cluster_inst.connect.return_value = mock_session
    mock_session.cluster = mock_cluster_inst

    with (
        patch("coodie.drivers.cassandra.CassandraDriver"),
        patch.dict("sys.modules", {"cassandra": MagicMock(), "cassandra.cluster": MagicMock(Cluster=mock_cluster_cls)}),
    ):
        await init_coodie_async(
            hosts=["node1"],
            keyspace="ks",
            ssl_context=ctx,
        )
    mock_cluster_cls.assert_called_once_with(["node1"], ssl_context=ctx)
    _registry.clear()


# ------------------------------------------------------------------
# Phase 6: CassandraDriver with mock Session
# ------------------------------------------------------------------


Row = namedtuple("Row", ["id", "name"])


@pytest.fixture
def mock_cassandra_session():
    """Build a mock cassandra.cluster.Session for CassandraDriver tests."""
    session = MagicMock()
    prepared = MagicMock()
    session.prepare.return_value = prepared
    prepared.bind.return_value = prepared
    session.cluster = MagicMock()
    return session


@pytest.fixture
def cassandra_driver(mock_cassandra_session):
    from coodie.drivers.cassandra import CassandraDriver

    return CassandraDriver(session=mock_cassandra_session, default_keyspace="test_ks")


def test_cassandra_driver_execute(cassandra_driver, mock_cassandra_session):
    mock_cassandra_session.execute.return_value = [Row(id="1", name="Alice")]
    rows = cassandra_driver.execute("SELECT * FROM test_ks.t", [])
    assert rows == [{"id": "1", "name": "Alice"}]
    mock_cassandra_session.prepare.assert_called_once_with("SELECT * FROM test_ks.t")


def test_cassandra_driver_prepared_cache(cassandra_driver, mock_cassandra_session):
    mock_cassandra_session.execute.return_value = []
    cassandra_driver.execute("SELECT * FROM test_ks.t", [])
    cassandra_driver.execute("SELECT * FROM test_ks.t", [])
    # prepare() should only be called once due to caching
    mock_cassandra_session.prepare.assert_called_once_with("SELECT * FROM test_ks.t")


@pytest.mark.skipif(not importlib.util.find_spec("cassandra"), reason="cassandra-driver not installed")
def test_cassandra_driver_execute_with_consistency(cassandra_driver, mock_cassandra_session):
    from cassandra import ConsistencyLevel  # type: ignore[import-untyped]

    mock_cassandra_session.execute.return_value = []
    cassandra_driver.execute("SELECT * FROM test_ks.t", ["p1"], consistency="LOCAL_QUORUM")
    prepared = mock_cassandra_session.prepare.return_value
    prepared.bind.assert_called_once_with(["p1"])
    bound = prepared.bind.return_value
    assert bound.consistency_level == ConsistencyLevel.LOCAL_QUORUM


def test_cassandra_driver_execute_with_timeout(cassandra_driver, mock_cassandra_session):
    mock_cassandra_session.execute.return_value = []
    cassandra_driver.execute("SELECT * FROM test_ks.t", [], timeout=5.0)
    # CassandraDriver always binds params first, then passes bound statement
    bound = mock_cassandra_session.prepare.return_value.bind.return_value
    mock_cassandra_session.execute.assert_called_with(bound, timeout=5.0)


def test_cassandra_driver_rows_to_dicts_none():
    from coodie.drivers.cassandra import CassandraDriver

    assert CassandraDriver._rows_to_dicts(None) == []


def test_cassandra_driver_rows_to_dicts_asdict():
    from coodie.drivers.cassandra import CassandraDriver

    rows = [Row(id="1", name="Alice"), Row(id="2", name="Bob")]
    result = CassandraDriver._rows_to_dicts(rows)
    assert result == [{"id": "1", "name": "Alice"}, {"id": "2", "name": "Bob"}]


def test_cassandra_driver_rows_to_dicts_dict_fallback():
    from coodie.drivers.cassandra import CassandraDriver

    rows = [{"id": "3", "name": "Carol"}]
    result = CassandraDriver._rows_to_dicts(rows)
    assert result == [{"id": "3", "name": "Carol"}]


def test_cassandra_driver_rows_to_dicts_dict_zero_copy():
    """When rows are already dicts, _rows_to_dicts skips per-row conversion."""
    from coodie.drivers.cassandra import CassandraDriver

    original = {"id": "1", "name": "Alice"}
    rows = [original, {"id": "2", "name": "Bob"}]
    result = CassandraDriver._rows_to_dicts(rows)
    assert result[0] is original  # same dict objects, no dict() wrapping


def test_cassandra_driver_rows_to_dicts_empty_iterable():
    from coodie.drivers.cassandra import CassandraDriver

    assert CassandraDriver._rows_to_dicts([]) == []


@pytest.mark.skipif(not importlib.util.find_spec("cassandra"), reason="cassandra-driver not installed")
def test_cassandra_driver_sets_dict_factory(mock_cassandra_session):
    """CassandraDriver sets dict_factory on the session so rows arrive as dicts."""
    from cassandra.query import dict_factory  # type: ignore[import-untyped]

    from coodie.drivers.cassandra import CassandraDriver

    CassandraDriver(session=mock_cassandra_session, default_keyspace="ks")
    assert mock_cassandra_session.row_factory is dict_factory


def test_cassandra_driver_sync_table(cassandra_driver, mock_cassandra_session):
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="name", cql_type="text"),
    ]
    # Simulate that only "id" already exists in the table
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE
        [SysRow(column_name="id")],  # system_schema query
        None,  # ALTER TABLE ADD "name"
    ]
    cassandra_driver.sync_table("my_table", "test_ks", cols)
    calls = mock_cassandra_session.execute.call_args_list
    # First call: CREATE TABLE
    assert "CREATE TABLE" in str(calls[0])
    # Second call: system_schema introspection
    assert "system_schema" in str(calls[1])
    # Third call: ALTER TABLE ADD for the missing column
    assert "ALTER TABLE" in str(calls[2])
    assert '"name"' in str(calls[2])


def test_cassandra_driver_sync_table_with_index(cassandra_driver, mock_cassandra_session):
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="email", cql_type="text", index=True),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE
        [SysRow(column_name="id"), SysRow(column_name="email")],  # system_schema
        None,  # CREATE INDEX
    ]
    cassandra_driver.sync_table("users", "test_ks", cols)
    calls = mock_cassandra_session.execute.call_args_list
    assert "CREATE INDEX" in str(calls[2])


def test_cassandra_driver_sync_table_cache_skips_second_call(cassandra_driver, mock_cassandra_session):
    """Second sync_table call for the same table is a no-op (cache hit)."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE
        [SysRow(column_name="id")],  # system_schema
    ]
    cassandra_driver.sync_table("cached_table", "test_ks", cols)
    first_call_count = mock_cassandra_session.execute.call_count

    # Second call — should be a no-op due to _known_tables cache
    cassandra_driver.sync_table("cached_table", "test_ks", cols)
    assert mock_cassandra_session.execute.call_count == first_call_count


def test_cassandra_driver_sync_table_cache_different_tables(cassandra_driver, mock_cassandra_session):
    """Different tables are cached independently."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE t1
        [SysRow(column_name="id")],  # system_schema t1
        None,  # CREATE TABLE t2
        [SysRow(column_name="id")],  # system_schema t2
    ]
    cassandra_driver.sync_table("t1", "test_ks", cols)
    cassandra_driver.sync_table("t2", "test_ks", cols)
    # Both should have been synced (4 execute calls: 2 per table)
    assert mock_cassandra_session.execute.call_count == 4


def test_cassandra_driver_sync_table_skips_alter_on_new_table(cassandra_driver, mock_cassandra_session):
    """When existing columns match model columns, ALTER TABLE is skipped."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="name", cql_type="text"),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE
        [SysRow(column_name="id"), SysRow(column_name="name")],  # system_schema — all cols present
    ]
    cassandra_driver.sync_table("new_table", "test_ks", cols)
    calls = mock_cassandra_session.execute.call_args_list
    # Only 2 calls: CREATE TABLE + system_schema introspection — no ALTER TABLE
    assert len(calls) == 2
    assert "ALTER TABLE" not in str(calls)


def test_cassandra_driver_sync_table_cache_invalidates_on_new_columns(cassandra_driver, mock_cassandra_session):
    """sync_table re-runs when called with additional columns (schema migration)."""
    from coodie.schema import ColumnDefinition

    cols_v1 = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    cols_v2 = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="label", cql_type="text"),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE (v1)
        [SysRow(column_name="id")],  # system_schema (v1)
        None,  # CREATE TABLE (v2)
        [SysRow(column_name="id")],  # system_schema (v2) — "label" missing
        None,  # ALTER TABLE ADD "label"
    ]
    cassandra_driver.sync_table("migrating", "test_ks", cols_v1)
    first_count = mock_cassandra_session.execute.call_count

    # Second call with new column — cache miss, full sync runs
    cassandra_driver.sync_table("migrating", "test_ks", cols_v2)
    assert mock_cassandra_session.execute.call_count > first_count
    calls = mock_cassandra_session.execute.call_args_list
    assert "ALTER TABLE" in str(calls[-1])


def test_cassandra_driver_close(cassandra_driver, mock_cassandra_session):
    cassandra_driver.close()
    mock_cassandra_session.cluster.shutdown.assert_called_once()


def test_cassandra_driver_has_slots():
    from coodie.drivers.cassandra import CassandraDriver

    assert hasattr(CassandraDriver, "__slots__")
    assert "_session" in CassandraDriver.__slots__


async def test_cassandra_driver_execute_async(cassandra_driver, mock_cassandra_session):
    """Test the asyncio bridge for execute_async."""
    import asyncio

    result_rows = [Row(id="1", name="Alice")]

    def fake_execute_async(stmt, **kwargs):
        future = MagicMock()

        def add_callbacks(on_success, on_error):
            loop = asyncio.get_event_loop()
            loop.call_soon(on_success, result_rows)

        future.add_callbacks = add_callbacks
        return future

    mock_cassandra_session.execute_async.side_effect = fake_execute_async
    rows = await cassandra_driver.execute_async("SELECT * FROM test_ks.t", [])
    assert rows == [{"id": "1", "name": "Alice"}]


async def test_cassandra_driver_sync_table_async(cassandra_driver, mock_cassandra_session):
    """sync_table_async uses native async callbacks — no run_in_executor."""
    import asyncio

    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])

    # The CREATE TABLE call uses raw CQL via execute_async (not prepared)
    # The introspection call also uses execute_async with params
    call_count = 0

    def fake_execute_async(stmt, *args, **kwargs):
        nonlocal call_count
        call_count += 1
        future = MagicMock()

        if call_count == 1:
            # CREATE TABLE — returns None
            result = None
        else:
            # system_schema introspection — returns rows
            result = [SysRow(column_name="id")]

        def add_callbacks(on_success, on_error):
            loop = asyncio.get_event_loop()
            loop.call_soon(on_success, result)

        future.add_callbacks = add_callbacks
        return future

    mock_cassandra_session.execute_async.side_effect = fake_execute_async
    await cassandra_driver.sync_table_async("t", "test_ks", cols)
    assert mock_cassandra_session.execute_async.call_count >= 1


async def test_cassandra_driver_execute_async_with_paging(cassandra_driver, mock_cassandra_session):
    """execute_async delegates paginated queries to sync execute via run_in_executor."""
    SysRow = namedtuple("SysRow", ["id", "name"])
    result = MagicMock()
    result.current_rows = [SysRow(id="1", name="Alice")]
    result.paging_state = b"page-token"
    result.__iter__ = MagicMock(return_value=iter([]))  # not used for paginated

    mock_cassandra_session.execute.return_value = result
    rows = await cassandra_driver.execute_async("SELECT * FROM test_ks.t", [], fetch_size=10)
    assert rows == [{"id": "1", "name": "Alice"}]
    assert cassandra_driver._last_paging_state == b"page-token"
    # Verify fetch_size was set on the bound statement
    prepared = mock_cassandra_session.prepare.return_value
    assert prepared.bind.return_value.fetch_size == 10


async def test_cassandra_driver_execute_async_with_paging_state(cassandra_driver, mock_cassandra_session):
    """execute_async passes paging_state through to sync execute for paginated queries."""
    SysRow = namedtuple("SysRow", ["id", "name"])
    result = MagicMock()
    result.current_rows = [SysRow(id="2", name="Bob")]
    result.paging_state = None
    result.__iter__ = MagicMock(return_value=iter([]))  # not used for paginated

    mock_cassandra_session.execute.return_value = result
    rows = await cassandra_driver.execute_async(
        "SELECT * FROM test_ks.t", [], fetch_size=10, paging_state=b"prev-token"
    )
    assert rows == [{"id": "2", "name": "Bob"}]
    assert cassandra_driver._last_paging_state is None
    # Verify paging_state was passed to sync execute
    call_kwargs = mock_cassandra_session.execute.call_args
    assert call_kwargs.kwargs.get("paging_state") == b"prev-token"


async def test_cassandra_driver_sync_table_async_cache_hit(cassandra_driver, mock_cassandra_session):
    """sync_table_async returns [] on cache hit without any DB calls."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    # Pre-populate the cache
    cassandra_driver._known_tables["test_ks.t"] = frozenset(["id"])
    result = await cassandra_driver.sync_table_async("t", "test_ks", cols)
    assert result == []
    # No DB calls should have been made
    mock_cassandra_session.execute_async.assert_not_called()


async def test_cassandra_driver_close_async(cassandra_driver, mock_cassandra_session):
    await cassandra_driver.close_async()
    mock_cassandra_session.cluster.shutdown.assert_called_once()


# ------------------------------------------------------------------
# Phase 6: AcsyllaDriver with mock acsylla session
# ------------------------------------------------------------------


@pytest.fixture
def mock_acsylla_session():
    """Build a mock acsylla session for AcsyllaDriver tests."""
    session = MagicMock()
    prepared = MagicMock()
    prepared.bind.return_value = MagicMock()

    # create_prepared is async
    session.create_prepared = AsyncMock(return_value=prepared)
    # execute is async
    session.execute = AsyncMock(return_value=[{"id": "1", "name": "Alice"}])
    # close is async
    session.close = AsyncMock()

    return session


@pytest.fixture
def acsylla_driver(mock_acsylla_session):
    """Create an AcsyllaDriver with import of acsylla mocked out."""
    import warnings

    with patch.dict("sys.modules", {"acsylla": MagicMock()}):
        from coodie.drivers.acsylla import AcsyllaDriver

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            driver = AcsyllaDriver(session=mock_acsylla_session, default_keyspace="test_ks")
        try:
            yield driver
        finally:
            # Stop the background event loop thread started by the driver
            driver._bg_loop.call_soon_threadsafe(driver._bg_loop.stop)
            driver._bg_thread.join(timeout=10)


async def test_acsylla_driver_execute_async(acsylla_driver, mock_acsylla_session):
    rows = await acsylla_driver.execute_async("SELECT * FROM test_ks.t", ["p1"])
    assert rows == [{"id": "1", "name": "Alice"}]
    mock_acsylla_session.create_prepared.assert_awaited_once_with("SELECT * FROM test_ks.t")


async def test_acsylla_driver_prepared_cache(acsylla_driver, mock_acsylla_session):
    await acsylla_driver.execute_async("SELECT * FROM test_ks.t", [])
    await acsylla_driver.execute_async("SELECT * FROM test_ks.t", [])
    # create_prepared should only be called once due to caching
    mock_acsylla_session.create_prepared.assert_awaited_once()


async def test_acsylla_driver_execute_async_with_consistency(acsylla_driver, mock_acsylla_session):
    await acsylla_driver.execute_async("SELECT * FROM test_ks.t", [], consistency="LOCAL_QUORUM")
    prepared = await mock_acsylla_session.create_prepared("SELECT * FROM test_ks.t")
    prepared.bind.assert_called_with([], consistency=acsylla_driver._acsylla.Consistency.LOCAL_QUORUM)


async def test_acsylla_driver_sync_table_async(acsylla_driver, mock_acsylla_session):
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="email", cql_type="text", index=True),
    ]
    # The introspection query returns existing columns as dicts;
    # session.execute must return an iterable result for both DDL (no rows)
    # and the system_schema SELECT (column_name rows).
    introspection_result = MagicMock()
    introspection_result.__iter__ = MagicMock(return_value=iter([{"column_name": "id"}, {"column_name": "email"}]))
    ddl_result = MagicMock()
    ddl_result.__iter__ = MagicMock(return_value=iter([]))
    mock_acsylla_session.execute = AsyncMock(side_effect=[ddl_result, introspection_result, ddl_result])
    await acsylla_driver.sync_table_async("users", "test_ks", cols)
    calls = mock_acsylla_session.execute.await_args_list
    # CREATE TABLE + introspection query + CREATE INDEX
    assert len(calls) >= 3


async def test_acsylla_driver_sync_table_cache_skips_second_call(acsylla_driver, mock_acsylla_session):
    """Second sync_table_async call for the same table is a no-op (cache hit)."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    introspection_result = MagicMock()
    introspection_result.__iter__ = MagicMock(return_value=iter([{"column_name": "id"}]))
    ddl_result = MagicMock()
    ddl_result.__iter__ = MagicMock(return_value=iter([]))
    mock_acsylla_session.execute = AsyncMock(side_effect=[ddl_result, introspection_result])
    await acsylla_driver.sync_table_async("cached_table", "test_ks", cols)
    first_call_count = mock_acsylla_session.execute.await_count

    # Second call — should be a no-op due to _known_tables cache
    await acsylla_driver.sync_table_async("cached_table", "test_ks", cols)
    assert mock_acsylla_session.execute.await_count == first_call_count


async def test_acsylla_driver_sync_table_skips_alter_on_new_table(acsylla_driver, mock_acsylla_session):
    """When existing columns match model columns, ALTER TABLE is skipped."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="name", cql_type="text"),
    ]
    introspection_result = MagicMock()
    introspection_result.__iter__ = MagicMock(return_value=iter([{"column_name": "id"}, {"column_name": "name"}]))
    ddl_result = MagicMock()
    ddl_result.__iter__ = MagicMock(return_value=iter([]))
    mock_acsylla_session.execute = AsyncMock(side_effect=[ddl_result, introspection_result])
    await acsylla_driver.sync_table_async("new_table", "test_ks", cols)
    # Only 2 calls: CREATE TABLE + introspection (via execute_async) — no ALTER TABLE
    # Note: introspection goes through execute_async which uses create_prepared + session.execute
    # but the DDL call goes through session.execute directly
    assert mock_acsylla_session.execute.await_count == 2


async def test_acsylla_driver_close_async(acsylla_driver, mock_acsylla_session):
    await acsylla_driver.close_async()
    mock_acsylla_session.close.assert_awaited_once()


def test_acsylla_driver_rows_to_dicts():
    with patch.dict("sys.modules", {"acsylla": MagicMock()}):
        from coodie.drivers.acsylla import AcsyllaDriver

        rows = [{"id": "1", "name": "Alice"}, {"id": "2", "name": "Bob"}]
        result = AcsyllaDriver._rows_to_dicts(rows)
        assert result == [{"id": "1", "name": "Alice"}, {"id": "2", "name": "Bob"}]


def test_acsylla_driver_rows_to_dicts_empty():
    with patch.dict("sys.modules", {"acsylla": MagicMock()}):
        from coodie.drivers.acsylla import AcsyllaDriver

        assert AcsyllaDriver._rows_to_dicts([]) == []


async def test_acsylla_driver_execute_async_with_paging(acsylla_driver, mock_acsylla_session):
    """AcsyllaDriver passes page_size to bind() and reads paging state from result."""
    mock_result = MagicMock()
    mock_result.__iter__ = MagicMock(return_value=iter([{"id": "1"}, {"id": "2"}]))
    mock_result.has_more_pages.return_value = True
    mock_result.page_state.return_value = b"next-page-token"
    mock_acsylla_session.execute = AsyncMock(return_value=mock_result)

    rows = await acsylla_driver.execute_async("SELECT * FROM test_ks.t", [], fetch_size=2)
    assert rows == [{"id": "1"}, {"id": "2"}]
    assert acsylla_driver._last_paging_state == b"next-page-token"

    # Verify page_size was passed to bind via the prepared mock
    prepared = mock_acsylla_session.create_prepared.return_value
    prepared.bind.assert_called_with([], page_size=2)


async def test_acsylla_driver_execute_async_with_paging_state(acsylla_driver, mock_acsylla_session):
    """AcsyllaDriver sets page_state on statement when paging_state is provided."""
    mock_result = MagicMock()
    mock_result.__iter__ = MagicMock(return_value=iter([{"id": "3"}]))
    mock_result.has_more_pages.return_value = False
    mock_acsylla_session.execute = AsyncMock(return_value=mock_result)

    rows = await acsylla_driver.execute_async("SELECT * FROM test_ks.t", [], fetch_size=2, paging_state=b"page-token")
    assert rows == [{"id": "3"}]
    assert acsylla_driver._last_paging_state is None

    # Verify set_page_state was called on the statement
    prepared = mock_acsylla_session.create_prepared.return_value
    statement = prepared.bind.return_value
    statement.set_page_state.assert_called_once_with(b"page-token")


# ------------------------------------------------------------------
# Sync bridge: execute(), sync_table(), close() via background loop
# ------------------------------------------------------------------


def test_acsylla_driver_sync_execute(acsylla_driver, mock_acsylla_session):
    """execute() works from a non-async context via the background loop."""
    rows = acsylla_driver.execute("SELECT * FROM test_ks.t", ["p1"])
    assert rows == [{"id": "1", "name": "Alice"}]


def test_acsylla_driver_sync_execute_from_running_loop(acsylla_driver, mock_acsylla_session):
    """execute() works even when called from within a running event loop."""
    import asyncio

    async def call_sync_from_loop():
        # run_in_executor ensures execute() is called from a thread while the
        # current loop is still running — this would have raised RuntimeError
        # with the old run_until_complete approach.
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, acsylla_driver.execute, "SELECT * FROM test_ks.t", ["p1"])

    rows = asyncio.run(call_sync_from_loop())
    assert rows == [{"id": "1", "name": "Alice"}]


def test_acsylla_driver_sync_close(acsylla_driver, mock_acsylla_session):
    """close() runs close_async() on the background loop and stops it."""
    acsylla_driver.close()
    mock_acsylla_session.close.assert_called_once()
    # Background loop should be stopped and thread should have exited after close()
    assert not acsylla_driver._bg_loop.is_running()
    assert not acsylla_driver._bg_thread.is_alive()


def test_acsylla_driver_sync_execute_with_fetch_size(acsylla_driver, mock_acsylla_session):
    """Sync execute() with fetch_size correctly propagates _last_paging_state."""
    mock_result = MagicMock()
    mock_result.__iter__ = MagicMock(return_value=iter([{"id": "1"}, {"id": "2"}]))
    mock_result.has_more_pages.return_value = True
    mock_result.page_state.return_value = b"next-page-token"
    mock_acsylla_session.execute = AsyncMock(return_value=mock_result)

    rows = acsylla_driver.execute("SELECT * FROM test_ks.t", [], fetch_size=2)

    assert rows == [{"id": "1"}, {"id": "2"}]
    # _last_paging_state must be readable from the calling thread after execute() returns
    assert acsylla_driver._last_paging_state == b"next-page-token"

    prepared = mock_acsylla_session.create_prepared.return_value
    prepared.bind.assert_called_with([], page_size=2)


def test_acsylla_driver_sync_execute_no_more_pages(acsylla_driver, mock_acsylla_session):
    """Sync execute() clears _last_paging_state when there are no more pages."""
    mock_result = MagicMock()
    mock_result.__iter__ = MagicMock(return_value=iter([{"id": "3"}]))
    mock_result.has_more_pages.return_value = False
    mock_acsylla_session.execute = AsyncMock(return_value=mock_result)

    acsylla_driver.execute("SELECT * FROM test_ks.t", [], fetch_size=2)

    assert acsylla_driver._last_paging_state is None


def test_acsylla_driver_sync_execute_with_paging_state(acsylla_driver, mock_acsylla_session):
    """Sync execute() passes paging_state to the statement (cursor-based pagination)."""
    mock_result = MagicMock()
    mock_result.__iter__ = MagicMock(return_value=iter([{"id": "4"}]))
    mock_result.has_more_pages.return_value = False
    mock_acsylla_session.execute = AsyncMock(return_value=mock_result)

    rows = acsylla_driver.execute("SELECT * FROM test_ks.t", [], fetch_size=2, paging_state=b"page-token")

    assert rows == [{"id": "4"}]
    assert acsylla_driver._last_paging_state is None
    prepared = mock_acsylla_session.create_prepared.return_value
    statement = prepared.bind.return_value
    statement.set_page_state.assert_called_once_with(b"page-token")


# ------------------------------------------------------------------
# Phase A: Enhanced sync_table — dry_run, drift, options, indexes
# ------------------------------------------------------------------


def test_cassandra_driver_sync_table_returns_planned_cql(cassandra_driver, mock_cassandra_session):
    """sync_table should return the list of planned CQL statements."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="name", cql_type="text"),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE
        [SysRow(column_name="id")],  # system_schema.columns
        None,  # ALTER TABLE ADD "name"
    ]
    planned = cassandra_driver.sync_table("my_table", "test_ks", cols)
    assert isinstance(planned, list)
    assert any("CREATE TABLE" in s for s in planned)
    assert any("ALTER TABLE" in s and '"name"' in s for s in planned)


def test_cassandra_driver_sync_table_dry_run(cassandra_driver, mock_cassandra_session):
    """dry_run=True should return CQL without executing DDL."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="name", cql_type="text"),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    # Only the introspection query (system_schema.columns) should be called
    mock_cassandra_session.execute.side_effect = [
        [SysRow(column_name="id")],  # system_schema.columns
    ]
    planned = cassandra_driver.sync_table("my_table", "test_ks", cols, dry_run=True)
    assert isinstance(planned, list)
    assert any("CREATE TABLE" in s for s in planned)
    assert any("ALTER TABLE" in s and '"name"' in s for s in planned)
    # Only 1 execute call: the system_schema introspection
    assert mock_cassandra_session.execute.call_count == 1
    assert "system_schema" in str(mock_cassandra_session.execute.call_args_list[0])


def test_cassandra_driver_sync_table_schema_drift_warning(cassandra_driver, mock_cassandra_session, caplog):
    """Should warn when DB has columns not in the model."""
    import logging

    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE
        [SysRow(column_name="id"), SysRow(column_name="old_column")],  # system_schema
    ]
    with caplog.at_level(logging.WARNING, logger="coodie"):
        cassandra_driver.sync_table("my_table", "test_ks", cols)
    assert "Schema drift detected" in caplog.text
    assert "old_column" in caplog.text


def test_cassandra_driver_sync_table_no_drift_no_warning(cassandra_driver, mock_cassandra_session, caplog):
    """No warning when all DB columns are in the model."""
    import logging

    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="name", cql_type="text"),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE
        [SysRow(column_name="id"), SysRow(column_name="name")],  # system_schema
    ]
    with caplog.at_level(logging.WARNING, logger="coodie"):
        cassandra_driver.sync_table("my_table", "test_ks", cols)
    assert "Schema drift" not in caplog.text


def test_cassandra_driver_sync_table_table_options_change(cassandra_driver, mock_cassandra_session):
    """Should detect changed table options and ALTER TABLE WITH."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    TableRow = namedtuple("TableRow", ["default_time_to_live"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE
        [SysRow(column_name="id")],  # system_schema.columns
        [TableRow(default_time_to_live=0)],  # system_schema.tables
        None,  # ALTER TABLE WITH
    ]
    planned = cassandra_driver.sync_table("my_table", "test_ks", cols, table_options={"default_time_to_live": 3600})
    assert any("ALTER TABLE" in s and "default_time_to_live = 3600" in s for s in planned)


def test_cassandra_driver_sync_table_table_options_no_change(cassandra_driver, mock_cassandra_session):
    """Should not ALTER TABLE when options match."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    TableRow = namedtuple("TableRow", ["default_time_to_live"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE
        [SysRow(column_name="id")],  # system_schema.columns
        [TableRow(default_time_to_live=3600)],  # system_schema.tables
    ]
    planned = cassandra_driver.sync_table("my_table", "test_ks", cols, table_options={"default_time_to_live": 3600})
    # No ALTER TABLE WITH in the planned statements
    assert not any("ALTER TABLE" in s and "WITH" in s for s in planned)


def test_cassandra_driver_sync_table_drop_removed_indexes(cassandra_driver, mock_cassandra_session):
    """Should drop indexes not in model when drop_removed_indexes=True."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="email", cql_type="text", index=True),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    IndexRow = namedtuple("IndexRow", ["index_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE
        [SysRow(column_name="id"), SysRow(column_name="email")],  # system_schema.columns
        None,  # CREATE INDEX email
        [IndexRow(index_name="my_table_email_idx"), IndexRow(index_name="my_table_old_idx")],  # indexes
        None,  # DROP INDEX old_idx
    ]
    planned = cassandra_driver.sync_table("my_table", "test_ks", cols, drop_removed_indexes=True)
    assert any("DROP INDEX" in s and "my_table_old_idx" in s for s in planned)
    # The current model index should NOT be dropped
    assert not any("DROP INDEX" in s and "my_table_email_idx" in s for s in planned)


def test_cassandra_driver_sync_table_no_drop_indexes_by_default(cassandra_driver, mock_cassandra_session):
    """Should NOT drop indexes when drop_removed_indexes is False (default)."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE
        [SysRow(column_name="id")],  # system_schema.columns
    ]
    planned = cassandra_driver.sync_table("my_table", "test_ks", cols)
    assert not any("DROP INDEX" in s for s in planned)


async def test_acsylla_driver_sync_table_dry_run(acsylla_driver, mock_acsylla_session):
    """AcsyllaDriver dry_run=True returns CQL without executing DDL."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="name", cql_type="text"),
    ]
    # Introspection queries go through execute_async (prepared), not raw session.execute
    introspection_result = MagicMock()
    introspection_result.__iter__ = MagicMock(return_value=iter([{"column_name": "id"}]))
    mock_acsylla_session.execute = AsyncMock(return_value=introspection_result)

    planned = await acsylla_driver.sync_table_async("my_table", "test_ks", cols, dry_run=True)
    assert isinstance(planned, list)
    assert any("CREATE TABLE" in s for s in planned)
    assert any("ALTER TABLE" in s and '"name"' in s for s in planned)


async def test_acsylla_driver_sync_table_schema_drift_warning(acsylla_driver, mock_acsylla_session, caplog):
    """AcsyllaDriver should warn on schema drift."""
    import logging

    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    ddl_result = MagicMock()
    ddl_result.__iter__ = MagicMock(return_value=iter([]))
    introspection_result = MagicMock()
    introspection_result.__iter__ = MagicMock(return_value=iter([{"column_name": "id"}, {"column_name": "legacy_col"}]))
    mock_acsylla_session.execute = AsyncMock(side_effect=[ddl_result, introspection_result])

    with caplog.at_level(logging.WARNING, logger="coodie"):
        await acsylla_driver.sync_table_async("my_table", "test_ks", cols)
    assert "Schema drift detected" in caplog.text
    assert "legacy_col" in caplog.text


# ------------------------------------------------------------------
# Lazy connection tests (§1.7 cqlengine feature parity)
# ------------------------------------------------------------------


def test_init_coodie_lazy_returns_lazy_driver():
    """init_coodie(lazy=True) returns a LazyDriver without connecting."""
    from coodie.drivers.lazy import LazyDriver

    _registry.clear()
    driver = init_coodie(hosts=["node1"], keyspace="ks", lazy=True)
    assert isinstance(driver, LazyDriver)
    assert driver._driver is None  # no connection yet
    assert get_driver() is driver
    _registry.clear()


def test_init_coodie_lazy_false_connects_immediately():
    """init_coodie(lazy=False, session=...) returns a CassandraDriver immediately."""
    from coodie.drivers.cassandra import CassandraDriver

    _registry.clear()
    mock_session = MagicMock()
    mock_session.cluster = MagicMock()
    driver = init_coodie(session=mock_session, keyspace="ks", lazy=False)
    assert isinstance(driver, CassandraDriver)
    _registry.clear()


def test_init_coodie_lazy_session_provided_ignores_lazy():
    """When session= is provided, lazy=True is ignored and CassandraDriver is used."""
    from coodie.drivers.cassandra import CassandraDriver

    _registry.clear()
    mock_session = MagicMock()
    mock_session.cluster = MagicMock()
    driver = init_coodie(session=mock_session, keyspace="ks", lazy=True)
    assert isinstance(driver, CassandraDriver)
    _registry.clear()


def test_lazy_driver_connects_on_execute():
    """LazyDriver establishes a real connection the first time execute() is called."""
    from coodie.drivers.lazy import LazyDriver

    _registry.clear()
    mock_cluster_cls = MagicMock()
    mock_cluster_inst = MagicMock()
    mock_session = MagicMock()
    mock_cluster_cls.return_value = mock_cluster_inst
    mock_cluster_inst.connect.return_value = mock_session
    mock_session.cluster = mock_cluster_inst

    with patch("coodie.drivers.lazy.LazyDriver._ensure_connected") as mock_ensure:
        driver = LazyDriver(hosts=["node1"], keyspace="ks", ssl_context=None, kwargs={})
        assert driver._driver is None

        # Simulate _ensure_connected setting _driver
        from coodie.drivers.cassandra import CassandraDriver

        def side_effect():
            driver._driver = MagicMock(spec=CassandraDriver)
            driver._driver.execute.return_value = [{"id": "1"}]

        mock_ensure.side_effect = side_effect
        rows = driver.execute("SELECT * FROM ks.t", [])
        mock_ensure.assert_called_once()
        assert rows == [{"id": "1"}]
    _registry.clear()


def test_lazy_driver_no_cluster_connect_until_first_use():
    """LazyDriver does NOT call Cluster() or cluster.connect() during init_coodie()."""
    _registry.clear()
    mock_cluster_cls = MagicMock()

    with patch.dict(
        "sys.modules", {"cassandra": MagicMock(), "cassandra.cluster": MagicMock(Cluster=mock_cluster_cls)}
    ):
        driver = init_coodie(hosts=["node1"], keyspace="ks", lazy=True)

    mock_cluster_cls.assert_not_called()
    assert get_driver() is driver
    _registry.clear()


def test_lazy_driver_ssl_context_forwarded_on_connect():
    """LazyDriver forwards ssl_context to Cluster() on first connection."""
    import ssl

    from coodie.drivers.lazy import LazyDriver

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    mock_cluster_cls = MagicMock()
    mock_cluster_inst = MagicMock()
    mock_session = MagicMock()
    mock_cluster_cls.return_value = mock_cluster_inst
    mock_cluster_inst.connect.return_value = mock_session

    with (
        patch("coodie.drivers.cassandra.CassandraDriver"),
        patch.dict("sys.modules", {"cassandra": MagicMock(), "cassandra.cluster": MagicMock(Cluster=mock_cluster_cls)}),
    ):
        driver = LazyDriver(hosts=["node1"], keyspace="ks", ssl_context=ctx, kwargs={})
        driver._ensure_connected()

    mock_cluster_cls.assert_called_once_with(["node1"], ssl_context=ctx)
    mock_cluster_inst.connect.assert_called_once_with("ks")


def test_lazy_driver_close_noop_when_not_connected():
    """LazyDriver.close() does not raise when the driver was never connected."""
    from coodie.drivers.lazy import LazyDriver

    driver = LazyDriver(hosts=["node1"], keyspace="ks", ssl_context=None, kwargs={})
    driver.close()  # should not raise


async def test_lazy_driver_close_async_noop_when_not_connected():
    """LazyDriver.close_async() does not raise when the driver was never connected."""
    from coodie.drivers.lazy import LazyDriver

    driver = LazyDriver(hosts=["node1"], keyspace="ks", ssl_context=None, kwargs={})
    await driver.close_async()  # should not raise


async def test_lazy_driver_connects_on_execute_async():
    """LazyDriver connects on first execute_async() call."""
    from coodie.drivers.cassandra import CassandraDriver
    from coodie.drivers.lazy import LazyDriver

    driver = LazyDriver(hosts=["node1"], keyspace="ks", ssl_context=None, kwargs={})

    mock_inner = MagicMock(spec=CassandraDriver)
    mock_inner.execute_async = AsyncMock(return_value=[{"id": "2"}])

    with patch.object(driver, "_ensure_connected_async", new_callable=AsyncMock) as mock_ensure:

        async def side_effect():
            driver._driver = mock_inner

        mock_ensure.side_effect = side_effect
        rows = await driver.execute_async("SELECT * FROM ks.t", [])
        mock_ensure.assert_awaited_once()
        assert rows == [{"id": "2"}]


# ------------------------------------------------------------------
# §14.5.6 Connection-level optimizations
# ------------------------------------------------------------------


def test_init_coodie_compression_forwarded_to_cluster():
    """compression= is forwarded to Cluster() when not None."""
    _registry.clear()

    mock_cluster_cls = MagicMock()
    mock_cluster_inst = MagicMock()
    mock_session = MagicMock()
    mock_cluster_cls.return_value = mock_cluster_inst
    mock_cluster_inst.connect.return_value = mock_session
    mock_session.cluster = mock_cluster_inst

    with (
        patch("coodie.drivers.cassandra.CassandraDriver"),
        patch.dict("sys.modules", {"cassandra": MagicMock(), "cassandra.cluster": MagicMock(Cluster=mock_cluster_cls)}),
    ):
        init_coodie(hosts=["node1"], keyspace="ks", compression="lz4")
    mock_cluster_cls.assert_called_once_with(["node1"], compression="lz4")
    _registry.clear()


def test_init_coodie_compression_not_added_when_none():
    """When compression is None, it is NOT passed to Cluster()."""
    _registry.clear()

    mock_cluster_cls = MagicMock()
    mock_cluster_inst = MagicMock()
    mock_session = MagicMock()
    mock_cluster_cls.return_value = mock_cluster_inst
    mock_cluster_inst.connect.return_value = mock_session
    mock_session.cluster = mock_cluster_inst

    with (
        patch("coodie.drivers.cassandra.CassandraDriver"),
        patch.dict("sys.modules", {"cassandra": MagicMock(), "cassandra.cluster": MagicMock(Cluster=mock_cluster_cls)}),
    ):
        init_coodie(hosts=["node1"], keyspace="ks")
    call_kwargs = mock_cluster_cls.call_args[1]
    assert "compression" not in call_kwargs
    _registry.clear()


def test_init_coodie_speculative_execution_policy_forwarded_to_cluster():
    """speculative_execution_policy= is forwarded to Cluster() when not None."""
    _registry.clear()

    mock_cluster_cls = MagicMock()
    mock_cluster_inst = MagicMock()
    mock_session = MagicMock()
    mock_cluster_cls.return_value = mock_cluster_inst
    mock_cluster_inst.connect.return_value = mock_session
    mock_session.cluster = mock_cluster_inst

    mock_policy = MagicMock()

    with (
        patch("coodie.drivers.cassandra.CassandraDriver"),
        patch.dict("sys.modules", {"cassandra": MagicMock(), "cassandra.cluster": MagicMock(Cluster=mock_cluster_cls)}),
    ):
        init_coodie(hosts=["node1"], keyspace="ks", speculative_execution_policy=mock_policy)
    mock_cluster_cls.assert_called_once_with(["node1"], speculative_execution_policy=mock_policy)
    _registry.clear()


def test_init_coodie_speculative_execution_policy_not_added_when_none():
    """When speculative_execution_policy is None, it is NOT passed to Cluster()."""
    _registry.clear()

    mock_cluster_cls = MagicMock()
    mock_cluster_inst = MagicMock()
    mock_session = MagicMock()
    mock_cluster_cls.return_value = mock_cluster_inst
    mock_cluster_inst.connect.return_value = mock_session
    mock_session.cluster = mock_cluster_inst

    with (
        patch("coodie.drivers.cassandra.CassandraDriver"),
        patch.dict("sys.modules", {"cassandra": MagicMock(), "cassandra.cluster": MagicMock(Cluster=mock_cluster_cls)}),
    ):
        init_coodie(hosts=["node1"], keyspace="ks")
    call_kwargs = mock_cluster_cls.call_args[1]
    assert "speculative_execution_policy" not in call_kwargs
    _registry.clear()


def test_cassandra_driver_sync_table_warms_prepared_cache(cassandra_driver, mock_cassandra_session):
    """sync_table() pre-prepares SELECT-by-PK and INSERT queries after table sync."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="name", cql_type="text"),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE
        [SysRow(column_name="id"), SysRow(column_name="name")],  # system_schema
    ]
    cassandra_driver.sync_table("my_table", "test_ks", cols)

    prepared_stmts = list(cassandra_driver._prepared.keys())
    assert any("SELECT" in s and "my_table" in s and '"id" = ?' in s for s in prepared_stmts)
    assert any("INSERT" in s and "my_table" in s for s in prepared_stmts)


def test_cassandra_driver_sync_table_warm_skipped_on_dry_run(cassandra_driver, mock_cassandra_session):
    """dry_run=True should NOT warm the prepared statement cache."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="name", cql_type="text"),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        [SysRow(column_name="id")],  # system_schema introspection only
    ]
    cassandra_driver.sync_table("my_table", "test_ks", cols, dry_run=True)
    assert cassandra_driver._prepared == {}


def test_cassandra_driver_sync_table_warm_skipped_on_cache_hit(cassandra_driver, mock_cassandra_session):
    """Warming is not triggered again when sync_table returns early (cache hit)."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [
        None,  # CREATE TABLE (first sync)
        [SysRow(column_name="id")],  # system_schema (first sync)
    ]
    cassandra_driver.sync_table("my_table", "test_ks", cols)
    prepare_count_after_first = mock_cassandra_session.prepare.call_count

    # Second call — cache hit, no new prepares
    cassandra_driver.sync_table("my_table", "test_ks", cols)
    assert mock_cassandra_session.prepare.call_count == prepare_count_after_first


async def test_cassandra_driver_sync_table_async_warms_prepared_cache(cassandra_driver, mock_cassandra_session):
    """sync_table_async() also pre-prepares SELECT-by-PK and INSERT queries."""
    import asyncio

    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="value", cql_type="text"),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    call_count = 0

    def fake_execute_async(stmt, *args, **kwargs):
        nonlocal call_count
        call_count += 1
        future = MagicMock()
        if call_count == 1:
            result = None
        else:
            result = [SysRow(column_name="id"), SysRow(column_name="value")]

        def add_callbacks(on_success, on_error):
            loop = asyncio.get_event_loop()
            loop.call_soon(on_success, result)

        future.add_callbacks = add_callbacks
        return future

    mock_cassandra_session.execute_async.side_effect = fake_execute_async
    await cassandra_driver.sync_table_async("warm_table", "test_ks", cols)

    prepared_stmts = list(cassandra_driver._prepared.keys())
    assert any("SELECT" in s and "warm_table" in s and '"id" = ?' in s for s in prepared_stmts)
    assert any("INSERT" in s and "warm_table" in s for s in prepared_stmts)


def test_cassandra_driver_logs_warning_on_missing_dict_factory(mock_cassandra_session, caplog):
    """CassandraDriver logs a warning when cassandra.query.dict_factory cannot be imported."""
    from coodie.drivers.cassandra import CassandraDriver

    with patch.dict("sys.modules", {"cassandra.query": None}), caplog.at_level(logging.WARNING, logger="coodie"):
        CassandraDriver(session=mock_cassandra_session, default_keyspace="ks")
    assert "dict_factory" in caplog.text


@pytest.mark.parametrize(
    ("table", "stored", "ref"),
    [("MyTable", "mytable", "MyTable"), ('"MyTable"', "MyTable", '"MyTable"'), ("order", "order", '"order"')],
)
def test_cassandra_driver_sync_table_identifier_case(cassandra_driver, mock_cassandra_session, table, stored, ref):
    """Schema lookups use the name as stored in system_schema; CQL quotes it when needed (#298)."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="name", cql_type="text"),
    ]
    SysRow = namedtuple("SysRow", ["column_name"])
    mock_cassandra_session.execute.side_effect = [None, [SysRow(column_name="id")], None]
    cassandra_driver.sync_table(table, "test_ks", cols)
    calls = mock_cassandra_session.execute.call_args_list
    assert calls[1].args[1] == ("test_ks", stored)
    assert calls[2].args[0] == f'ALTER TABLE test_ks.{ref} ADD "name" text'
