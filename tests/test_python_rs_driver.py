"""Unit tests for PythonRsDriver with mocked scylla.Session."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from coodie.drivers import (
    _build_python_rs_session_builder,
    _python_rs_contact_points,
    _registry,
    get_driver,
    init_coodie,
    init_coodie_async,
)
from coodie.exceptions import ConfigurationError


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def _mock_scylla_modules() -> dict[str, MagicMock]:
    """Return a dict suitable for ``patch.dict("sys.modules", ...)``.

    Mocks the ``scylla`` package and its sub-modules so that
    ``import scylla`` and ``from scylla.session_builder import SessionBuilder``
    succeed without the real package installed.
    """
    scylla_mod = MagicMock()
    return {
        "scylla": scylla_mod,
        "scylla.session_builder": scylla_mod.session_builder,
    }


def test_python_rs_contact_points_without_port():
    assert _python_rs_contact_points(["127.0.0.1", "127.0.0.2"], None) == ("127.0.0.1", "127.0.0.2")


def test_python_rs_contact_points_with_port():
    assert _python_rs_contact_points(["127.0.0.1", "127.0.0.2"], "9042") == (
        ("127.0.0.1", 9042),
        ("127.0.0.2", 9042),
    )


def test_python_rs_contact_points_with_integer_port():
    assert _python_rs_contact_points(["127.0.0.1"], 9042) == (("127.0.0.1", 9042),)


def test_build_python_rs_session_builder_sets_contact_points_and_forwards_kwargs():
    builder = MagicMock()
    builder.contact_points.return_value = builder
    session_builder_cls = MagicMock(return_value=builder)

    result = _build_python_rs_session_builder(
        session_builder_cls,
        ["127.0.0.1"],
        {"port": "9042", "compression": "lz4"},
    )

    assert result is builder
    session_builder_cls.assert_called_once_with(compression="lz4")
    builder.contact_points.assert_called_once_with((("127.0.0.1", 9042),))


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


@pytest.fixture
def mock_scylla_session():
    """Build a mock python-rs-driver Session for PythonRsDriver tests."""
    session = MagicMock()
    prepared = MagicMock()

    # prepare is async
    session.prepare = AsyncMock(return_value=prepared)
    # execute is async — returns a RequestResult-like object
    result = MagicMock()
    result.iter_rows.return_value = iter([{"id": "1", "name": "Alice"}])
    session.execute = AsyncMock(return_value=result)

    return session


@pytest.fixture
def python_rs_driver(mock_scylla_session):
    """Create a PythonRsDriver with ``scylla`` import mocked."""
    with patch.dict("sys.modules", _mock_scylla_modules()):
        from coodie.drivers.python_rs import PythonRsDriver

        return PythonRsDriver(session=mock_scylla_session, default_keyspace="test_ks")


# ------------------------------------------------------------------
# Instantiation & import guard
# ------------------------------------------------------------------


def test_python_rs_driver_import_error_when_scylla_missing():
    """PythonRsDriver raises ImportError when scylla is not installed."""
    with patch.dict("sys.modules", {"scylla": None}):
        with pytest.raises(ImportError, match="python-rs-driver is required"):
            from coodie.drivers.python_rs import PythonRsDriver

            PythonRsDriver(session=MagicMock())


def test_python_rs_driver_has_slots():
    with patch.dict("sys.modules", _mock_scylla_modules()):
        from coodie.drivers.python_rs import PythonRsDriver

        assert hasattr(PythonRsDriver, "__slots__")
        assert "_session" in PythonRsDriver.__slots__
        assert "_bg_loop" in PythonRsDriver.__slots__
        assert "_bg_thread" in PythonRsDriver.__slots__
        assert "_bridge_to_bg_loop" in PythonRsDriver.__slots__


# ------------------------------------------------------------------
# execute_async
# ------------------------------------------------------------------


async def test_python_rs_driver_execute_async(python_rs_driver, mock_scylla_session):
    rows = await python_rs_driver.execute_async("SELECT * FROM test_ks.t", ["p1"])
    assert rows == [{"id": "1", "name": "Alice"}]
    mock_scylla_session.prepare.assert_awaited_once_with("SELECT * FROM test_ks.t")


async def test_python_rs_driver_execute_async_ddl_bypasses_prepare(python_rs_driver, mock_scylla_session):
    """DDL statements should be executed directly, bypassing prepare."""
    result = MagicMock()
    result.iter_rows.return_value = iter([])
    mock_scylla_session.execute = AsyncMock(return_value=result)

    await python_rs_driver.execute_async("CREATE TABLE test_ks.t (id uuid PRIMARY KEY)", [])
    # prepare should NOT have been called for DDL
    mock_scylla_session.prepare.assert_not_awaited()
    mock_scylla_session.execute.assert_awaited_once_with("CREATE TABLE test_ks.t (id uuid PRIMARY KEY)", None)


async def test_python_rs_driver_execute_async_ddl_case_insensitive(python_rs_driver, mock_scylla_session):
    """DDL detection should be case-insensitive."""
    result = MagicMock()
    result.iter_rows.return_value = iter([])
    mock_scylla_session.execute = AsyncMock(return_value=result)

    await python_rs_driver.execute_async("  drop TABLE test_ks.t", [])
    mock_scylla_session.prepare.assert_not_awaited()


async def test_python_rs_driver_execute_async_alter_bypasses_prepare(python_rs_driver, mock_scylla_session):
    """ALTER is also DDL."""
    result = MagicMock()
    result.iter_rows.return_value = iter([])
    mock_scylla_session.execute = AsyncMock(return_value=result)

    await python_rs_driver.execute_async('ALTER TABLE test_ks.t ADD "col" text', [])
    mock_scylla_session.prepare.assert_not_awaited()


async def test_python_rs_driver_execute_async_truncate_bypasses_prepare(python_rs_driver, mock_scylla_session):
    """TRUNCATE is also DDL."""
    result = MagicMock()
    result.iter_rows.return_value = iter([])
    mock_scylla_session.execute = AsyncMock(return_value=result)

    await python_rs_driver.execute_async("TRUNCATE test_ks.t", [])
    mock_scylla_session.prepare.assert_not_awaited()


# ------------------------------------------------------------------
# Prepared statement caching
# ------------------------------------------------------------------


async def test_python_rs_driver_prepared_cache(python_rs_driver, mock_scylla_session):
    await python_rs_driver.execute_async("SELECT * FROM test_ks.t", [])

    # Reset the result so iter_rows() works again on second call
    result2 = MagicMock()
    result2.iter_rows.return_value = iter([{"id": "2"}])
    mock_scylla_session.execute = AsyncMock(return_value=result2)

    await python_rs_driver.execute_async("SELECT * FROM test_ks.t", [])
    # prepare should only be called once due to caching
    mock_scylla_session.prepare.assert_awaited_once()


# ------------------------------------------------------------------
# _rows_to_dicts
# ------------------------------------------------------------------


def test_python_rs_driver_rows_to_dicts_none():
    with patch.dict("sys.modules", _mock_scylla_modules()):
        from coodie.drivers.python_rs import PythonRsDriver

        assert PythonRsDriver._rows_to_dicts(None) == []


def test_python_rs_driver_rows_to_dicts_normal():
    with patch.dict("sys.modules", _mock_scylla_modules()):
        from coodie.drivers.python_rs import PythonRsDriver

        result = MagicMock()
        result.iter_rows.return_value = iter([{"id": "1"}, {"id": "2"}])
        assert PythonRsDriver._rows_to_dicts(result) == [{"id": "1"}, {"id": "2"}]


def test_python_rs_driver_rows_to_dicts_empty():
    with patch.dict("sys.modules", _mock_scylla_modules()):
        from coodie.drivers.python_rs import PythonRsDriver

        result = MagicMock()
        result.iter_rows.return_value = iter([])
        assert PythonRsDriver._rows_to_dicts(result) == []


def test_python_rs_driver_rows_to_dicts_new_api():
    """New python-rs-driver API uses iter_current_page() instead of iter_rows()."""
    with patch.dict("sys.modules", _mock_scylla_modules()):
        from coodie.drivers.python_rs import PythonRsDriver

        class NewRequestResult:
            def iter_current_page(self):
                return iter([{"id": "1"}, {"id": "2"}])

        assert PythonRsDriver._rows_to_dicts(NewRequestResult()) == [{"id": "1"}, {"id": "2"}]


# ------------------------------------------------------------------
# _is_ddl helper
# ------------------------------------------------------------------


def test_is_ddl():
    with patch.dict("sys.modules", _mock_scylla_modules()):
        from coodie.drivers.python_rs import _is_ddl

        assert _is_ddl("CREATE TABLE ks.t (id uuid PRIMARY KEY)")
        assert _is_ddl("ALTER TABLE ks.t ADD col text")
        assert _is_ddl("DROP TABLE ks.t")
        assert _is_ddl("TRUNCATE ks.t")
        assert _is_ddl("  create TABLE ks.t (id uuid PRIMARY KEY)")
        assert not _is_ddl("SELECT * FROM ks.t")
        assert not _is_ddl("INSERT INTO ks.t (id) VALUES (?)")
        assert not _is_ddl("UPDATE ks.t SET col = ? WHERE id = ?")
        assert not _is_ddl("DELETE FROM ks.t WHERE id = ?")


# ------------------------------------------------------------------
# sync_table_async
# ------------------------------------------------------------------


async def test_python_rs_driver_sync_table_async(python_rs_driver, mock_scylla_session):
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="email", cql_type="text", index=True),
    ]
    # DDL calls return empty result; introspection returns columns
    ddl_result = MagicMock()
    ddl_result.iter_rows = MagicMock(return_value=iter([]))
    introspection_result = MagicMock()
    introspection_result.iter_rows = MagicMock(return_value=iter([{"column_name": "id"}, {"column_name": "email"}]))

    call_count = 0

    async def fake_execute(stmt, params):
        nonlocal call_count
        call_count += 1
        # Call 1: CREATE TABLE (DDL via _execute_cql_async)
        # Call 2: SELECT column_name (prepared, introspection via execute_async)
        # Call 3: CREATE INDEX (DDL via _execute_cql_async)
        if call_count == 1:
            return ddl_result
        elif call_count == 2:
            return introspection_result
        else:
            return ddl_result

    mock_scylla_session.execute = AsyncMock(side_effect=fake_execute)

    planned = await python_rs_driver.sync_table_async("users", "test_ks", cols)
    assert any("CREATE TABLE" in s for s in planned)
    assert any("CREATE INDEX" in s for s in planned)


async def test_python_rs_driver_sync_table_async_cache_skips_second_call(python_rs_driver, mock_scylla_session):
    """Second sync_table_async call for the same table is a no-op (cache hit)."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
    ]
    ddl_result = MagicMock()
    ddl_result.iter_rows = MagicMock(return_value=iter([]))
    introspection_result = MagicMock()
    introspection_result.iter_rows = MagicMock(return_value=iter([{"column_name": "id"}]))

    call_count = 0

    async def fake_execute(stmt, params):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return ddl_result
        return introspection_result

    mock_scylla_session.execute = AsyncMock(side_effect=fake_execute)

    await python_rs_driver.sync_table_async("cached_table", "test_ks", cols)
    first_call_count = mock_scylla_session.execute.await_count

    # Second call — should be a no-op due to _known_tables cache
    await python_rs_driver.sync_table_async("cached_table", "test_ks", cols)
    assert mock_scylla_session.execute.await_count == first_call_count


async def test_python_rs_driver_sync_table_async_skips_alter_on_new_table(python_rs_driver, mock_scylla_session):
    """When existing columns match model columns, ALTER TABLE is skipped."""
    from coodie.schema import ColumnDefinition

    cols = [
        ColumnDefinition(name="id", cql_type="uuid", primary_key=True),
        ColumnDefinition(name="name", cql_type="text"),
    ]
    ddl_result = MagicMock()
    ddl_result.iter_rows = MagicMock(return_value=iter([]))
    introspection_result = MagicMock()
    introspection_result.iter_rows = MagicMock(return_value=iter([{"column_name": "id"}, {"column_name": "name"}]))

    call_count = 0

    async def fake_execute(stmt, params):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return ddl_result
        return introspection_result

    mock_scylla_session.execute = AsyncMock(side_effect=fake_execute)

    await python_rs_driver.sync_table_async("new_table", "test_ks", cols)
    # Only 2 calls: CREATE TABLE + introspection — no ALTER TABLE
    assert mock_scylla_session.execute.await_count == 2


# ------------------------------------------------------------------
# close
# ------------------------------------------------------------------


async def test_python_rs_driver_close_async(python_rs_driver):
    """close_async is a no-op but should be callable."""
    await python_rs_driver.close_async()


# ------------------------------------------------------------------
# init_coodie / init_coodie_async registration
# ------------------------------------------------------------------


def test_init_coodie_python_rs_requires_session():
    _registry.clear()
    with patch.dict("sys.modules", _mock_scylla_modules()):
        with pytest.raises(ConfigurationError, match="pre-created python-rs-driver session or hosts"):
            init_coodie(driver_type="python-rs", keyspace="ks")
    _registry.clear()


def test_init_coodie_python_rs_with_session():
    _registry.clear()
    mock_session = MagicMock()
    with patch.dict("sys.modules", _mock_scylla_modules()):
        driver = init_coodie(session=mock_session, keyspace="ks", driver_type="python-rs")
    assert get_driver() is driver
    _registry.clear()


async def test_init_coodie_async_python_rs_with_hosts():
    _registry.clear()
    mock_scylla = MagicMock()
    mock_builder = MagicMock()
    mock_session = MagicMock()
    mock_scylla.session_builder.SessionBuilder = MagicMock(return_value=mock_builder)
    mock_builder.contact_points.return_value = mock_builder
    mock_builder.connect = AsyncMock(return_value=mock_session)

    modules = {
        "scylla": mock_scylla,
        "scylla.session_builder": mock_scylla.session_builder,
    }
    with patch.dict("sys.modules", modules):
        driver = await init_coodie_async(
            hosts=["127.0.0.1"],
            keyspace="ks",
            driver_type="python-rs",
        )
    assert get_driver() is driver
    # connect() creates session on background loop via session_factory
    mock_scylla.session_builder.SessionBuilder.assert_called_once()
    mock_builder.contact_points.assert_called_once_with(("127.0.0.1",))
    mock_builder.connect.assert_awaited_once()
    assert driver._bridge_to_bg_loop is True
    _registry.clear()


async def test_init_coodie_async_python_rs_requires_session():
    """When no hosts and no session, python-rs should raise ConfigurationError."""
    _registry.clear()
    with patch.dict("sys.modules", _mock_scylla_modules()):
        with pytest.raises(ConfigurationError, match="pre-created python-rs-driver session"):
            await init_coodie_async(driver_type="python-rs", keyspace="ks")
    _registry.clear()


def test_init_coodie_unknown_driver_type_includes_python_rs():
    """Error message for unknown driver_type should mention python-rs."""
    _registry.clear()
    with pytest.raises(ConfigurationError, match="python-rs"):
        init_coodie(driver_type="unknown", keyspace="ks")
    _registry.clear()


# ------------------------------------------------------------------
# Background-thread sync bridge & connect() classmethod
# ------------------------------------------------------------------


def test_python_rs_driver_init_sets_bridge_false():
    """__init__ sets _bridge_to_bg_loop to False."""
    with patch.dict("sys.modules", _mock_scylla_modules()):
        from coodie.drivers.python_rs import PythonRsDriver

        driver = PythonRsDriver(session=MagicMock(), default_keyspace="ks")
        assert driver._bridge_to_bg_loop is False
        assert driver._bg_loop is not None
        assert driver._bg_thread.is_alive()
        driver.close()


def test_python_rs_driver_connect_classmethod():
    """connect() creates a driver with _bridge_to_bg_loop = True."""
    mock_session = MagicMock()

    async def factory():
        return mock_session

    with patch.dict("sys.modules", _mock_scylla_modules()):
        from coodie.drivers.python_rs import PythonRsDriver

        driver = PythonRsDriver.connect(session_factory=factory, default_keyspace="ks")
        assert driver._bridge_to_bg_loop is True
        assert driver._session is mock_session
        assert driver._default_keyspace == "ks"
        assert driver._bg_loop is not None
        assert driver._bg_thread.is_alive()
        driver.close()


def test_python_rs_driver_connect_import_error():
    """connect() raises ImportError when scylla is not installed."""
    with patch.dict("sys.modules", {"scylla": None}):
        with pytest.raises(ImportError, match="python-rs-driver is required"):
            from coodie.drivers.python_rs import PythonRsDriver

            PythonRsDriver.connect(session_factory=AsyncMock())


def test_python_rs_driver_execute_via_run_coroutine_threadsafe():
    """Sync execute() dispatches to _bg_loop via run_coroutine_threadsafe."""
    with patch.dict("sys.modules", _mock_scylla_modules()):
        from coodie.drivers.python_rs import PythonRsDriver

        mock_session = MagicMock()
        prepared = MagicMock()
        mock_session.prepare = AsyncMock(return_value=prepared)
        result = MagicMock()
        result.iter_rows.return_value = iter([{"id": "1"}])
        mock_session.execute = AsyncMock(return_value=result)

        async def factory():
            return mock_session

        driver = PythonRsDriver.connect(session_factory=factory, default_keyspace="ks")
        rows = driver.execute("SELECT * FROM ks.t", [])
        assert rows == [{"id": "1"}]
        driver.close()


def test_init_coodie_python_rs_with_hosts():
    """init_coodie(hosts=..., driver_type='python-rs') uses PythonRsDriver.connect()."""
    _registry.clear()
    mock_scylla = MagicMock()
    mock_builder = MagicMock()
    mock_session = MagicMock()
    mock_scylla.session_builder.SessionBuilder = MagicMock(return_value=mock_builder)
    mock_builder.contact_points.return_value = mock_builder
    mock_builder.connect = AsyncMock(return_value=mock_session)

    modules = {
        "scylla": mock_scylla,
        "scylla.session_builder": mock_scylla.session_builder,
    }
    with patch.dict("sys.modules", modules):
        driver = init_coodie(hosts=["127.0.0.1"], keyspace="ks", driver_type="python-rs")
    assert get_driver() is driver
    assert driver._bridge_to_bg_loop is True
    mock_scylla.session_builder.SessionBuilder.assert_called_once()
    mock_builder.contact_points.assert_called_once_with(("127.0.0.1",))
    mock_builder.connect.assert_awaited_once()
    _registry.clear()
