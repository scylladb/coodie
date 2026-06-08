from __future__ import annotations

import asyncio
import threading
from collections.abc import Awaitable, Callable
from typing import Any

from pydantic import BaseModel

from coodie.drivers.base import AbstractDriver

_DDL_PREFIXES = ("CREATE ", "ALTER ", "DROP ", "TRUNCATE ")


def _is_ddl(stmt: str) -> bool:
    """Return ``True`` if *stmt* is a DDL statement that must not be prepared."""
    return stmt.lstrip().upper().startswith(_DDL_PREFIXES)


class PythonRsDriver(AbstractDriver):
    """Driver backed by `python-rs-driver <https://github.com/scylladb-zpp-2025-python-rs-driver/python-rs-driver>`_.

    .. note::
       ``needs_row_validation`` is ``True`` because python-rs-driver returns
       UDT values as plain dicts rather than Pydantic model instances.

    ``python-rs-driver`` wraps the Rust-based *scylla-rust-driver* via PyO3 and
    provides a **native async** interface.  Sync methods use an event-loop
    bridge (same pattern as :class:`~coodie.drivers.acsylla.AcsyllaDriver`).

    .. note::

        python-rs-driver is not published on PyPI.  Build from source::

            git clone https://github.com/scylladb-zpp-2025-python-rs-driver/python-rs-driver
            cd python-rs-driver
            maturin develop --release

    **Typical async usage**:

    .. code-block:: python

        from scylla.session_builder import SessionBuilder
        from coodie.aio import Document, init_coodie
        from coodie.drivers import register_driver
        from coodie.drivers.python_rs import PythonRsDriver

        builder = SessionBuilder().contact_points((("127.0.0.1", 9042),))
        session = await builder.connect()

        driver = PythonRsDriver(session=session, default_keyspace="catalog")
        register_driver("default", driver, default=True)
    """

    needs_row_validation: bool = True

    __slots__ = (
        "_session",
        "_default_keyspace",
        "_prepared",
        "_bg_loop",
        "_bg_thread",
        "_bridge_to_bg_loop",
        "_last_paging_state",
        "_known_tables",
    )

    def __init__(
        self,
        session: Any,
        default_keyspace: str | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        try:
            import scylla  # noqa: F401  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError(
                "python-rs-driver is required for PythonRsDriver. "
                "Build from source: https://github.com/scylladb-zpp-2025-python-rs-driver/python-rs-driver"
            ) from exc
        self._session = session
        self._default_keyspace = default_keyspace
        self._prepared: dict[str, Any] = {}
        self._last_paging_state: bytes | None = None
        self._known_tables: dict[str, frozenset[str]] = {}
        # Spin up a dedicated background event loop in a daemon thread for the
        # sync bridge.  When _bridge_to_bg_loop is False (default for __init__)
        # the async public methods run directly on the caller's loop so that
        # a session created externally works unchanged.  When True (set by
        # connect()) the session lives on _bg_loop and all operations are
        # dispatched there.
        self._bg_loop: asyncio.AbstractEventLoop = loop or asyncio.new_event_loop()
        self._bg_thread = threading.Thread(
            target=self._bg_loop.run_forever,
            daemon=True,
            name="coodie-python-rs-sync",
        )
        self._bg_thread.start()
        self._bridge_to_bg_loop: bool = False

    @classmethod
    def connect(
        cls,
        session_factory: Callable[[], Awaitable[Any]],
        default_keyspace: str | None = None,
    ) -> "PythonRsDriver":
        """Create a driver whose python-rs session lives on the background loop.

        ``session_factory`` is a zero-argument callable that returns an
        **awaitable** (e.g. an ``async def`` function or a lambda wrapping one).
        It is invoked on the background loop,
        so the resulting session is properly bound to that loop.  This enables
        both the sync bridge (``execute``, ``sync_table``, ``close``) and the
        async interface (``execute_async``, …) to work correctly from any
        calling context, including an already-running event loop.

        Example::

            from scylla.session_builder import SessionBuilder
            from coodie.drivers.python_rs import PythonRsDriver

            async def make_session():
                builder = SessionBuilder().contact_points((("127.0.0.1", 9042),))
                return await builder.connect()

            driver = PythonRsDriver.connect(make_session, default_keyspace="catalog")
        """
        try:
            import scylla  # noqa: F401  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError(
                "python-rs-driver is required for PythonRsDriver. "
                "Build from source: https://github.com/scylladb-zpp-2025-python-rs-driver/python-rs-driver"
            ) from exc

        # Bootstrap the infrastructure before creating the session so the
        # session is bound to _bg_loop from the start.
        bg_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        bg_thread = threading.Thread(
            target=bg_loop.run_forever,
            daemon=True,
            name="coodie-python-rs-sync",
        )
        bg_thread.start()

        session = asyncio.run_coroutine_threadsafe(session_factory(), bg_loop).result()

        driver: "PythonRsDriver" = cls.__new__(cls)
        driver._session = session
        driver._default_keyspace = default_keyspace
        driver._prepared = {}
        driver._last_paging_state = None
        driver._known_tables = {}
        driver._bg_loop = bg_loop
        driver._bg_thread = bg_thread
        driver._bridge_to_bg_loop = True
        return driver

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _prepare(self, cql: str) -> Any:
        if cql not in self._prepared:
            self._prepared[cql] = await self._session.prepare(cql)
        return self._prepared[cql]

    @staticmethod
    def _serialize_param(p: Any) -> Any:
        """Recursively serialize a single param value for python-rs-driver.

        python-rs-driver requires UDT values to be plain dicts, not Pydantic
        model instances.  Pydantic's ``model_dump()`` handles nested models
        recursively, so a top-level conversion is sufficient for UDTs.
        Collection types (lists, sets, tuples) are iterated so that any
        model instances within them are also converted.
        """
        if isinstance(p, BaseModel):
            return p.model_dump()
        if isinstance(p, list):
            return [PythonRsDriver._serialize_param(x) for x in p]
        if isinstance(p, tuple):
            return tuple(PythonRsDriver._serialize_param(x) for x in p)
        if isinstance(p, set):
            return {PythonRsDriver._serialize_param(x) for x in p}
        if isinstance(p, dict):
            return {k: PythonRsDriver._serialize_param(v) for k, v in p.items()}
        return p

    @staticmethod
    def _serialize_params(params: list[Any]) -> list[Any]:
        """Serialize all params for python-rs-driver, converting BaseModel instances.

        python-rs-driver requires UDT values to be plain dicts.  This converts
        any ``BaseModel`` in the params list (including inside collection types)
        to its ``model_dump()`` dict representation.
        """
        return [PythonRsDriver._serialize_param(p) for p in params]

    @staticmethod
    def _rows_to_dicts(result: Any) -> list[dict[str, Any]]:
        """Convert a ``RequestResult`` to a list of dicts.

        python-rs-driver yields dicts from its row iterators.
        Supports both the old API (``iter_rows()``) and the new paging API
        (``iter_current_page()``).  Non-row-returning statements
        (INSERT/UPDATE/DELETE) raise ``RuntimeError`` — return ``[]``.
        """
        if result is None:
            return []
        # Prefer iter_current_page (new paging API, 2026-03-13+),
        # fall back to iter_rows (old API).  We check the *type* rather
        # than the instance so that unittest MagicMock auto-attributes
        # don't produce false positives.
        method_name = "iter_current_page" if hasattr(type(result), "iter_current_page") else "iter_rows"
        try:
            return list(getattr(result, method_name)())
        except RuntimeError as exc:
            if "does not have rows" in str(exc):
                return []
            raise

    # ------------------------------------------------------------------
    # Background-loop bridge
    # ------------------------------------------------------------------

    async def _run_on_bg_loop(self, coro: Any) -> Any:
        """Bridge *coro* to the background loop from any calling loop.

        If we are already running on *_bg_loop* the coroutine is awaited
        directly (zero overhead).  Otherwise it is submitted via
        ``run_coroutine_threadsafe`` and the caller awaits a
        ``concurrent.futures.Future`` wrapped as an asyncio Future on the
        current loop.
        """
        try:
            current_loop: asyncio.AbstractEventLoop | None = asyncio.get_running_loop()
        except RuntimeError:
            current_loop = None

        if current_loop is self._bg_loop:
            return await coro
        return await asyncio.wrap_future(asyncio.run_coroutine_threadsafe(coro, self._bg_loop))

    # ------------------------------------------------------------------
    # Core async implementations — always run on _bg_loop
    # ------------------------------------------------------------------

    async def _execute_async_impl(
        self,
        stmt: str,
        params: list[Any],
        consistency: str | None = None,
        timeout: float | None = None,
        fetch_size: int | None = None,
        paging_state: bytes | None = None,
    ) -> list[dict[str, Any]]:
        if _is_ddl(stmt):
            result = await self._session.execute(stmt, None)
            self._last_paging_state = None
            return self._rows_to_dicts(result)

        prepared = await self._prepare(stmt)
        result = await self._session.execute(prepared, self._serialize_params(params) if params else None)
        self._last_paging_state = None
        return self._rows_to_dicts(result)

    # ------------------------------------------------------------------
    # Asynchronous public interface
    # ------------------------------------------------------------------

    async def execute_async(
        self,
        stmt: str,
        params: list[Any],
        consistency: str | None = None,
        timeout: float | None = None,
        fetch_size: int | None = None,
        paging_state: bytes | None = None,
    ) -> list[dict[str, Any]]:
        coro = self._execute_async_impl(
            stmt,
            params,
            consistency=consistency,
            timeout=timeout,
            fetch_size=fetch_size,
            paging_state=paging_state,
        )
        if self._bridge_to_bg_loop:
            return await self._run_on_bg_loop(coro)
        return await coro

    async def _execute_cql_async(self, cql: str) -> Any:
        """Execute a raw CQL string asynchronously."""
        return await self._session.execute(cql, None)

    async def _get_existing_columns_async(self, table: str, keyspace: str) -> set[str]:
        """Introspect existing column names via system_schema."""
        stmt = "SELECT column_name FROM system_schema.columns WHERE keyspace_name = ? AND table_name = ?"
        rows = await self._execute_async_impl(stmt, [keyspace, table])
        return {row["column_name"] for row in rows}

    async def _get_current_table_options_async(self, table: str, keyspace: str) -> dict[str, Any]:
        """Introspect current table options from ``system_schema.tables``."""
        stmt = "SELECT * FROM system_schema.tables WHERE keyspace_name = ? AND table_name = ?"
        rows = await self._execute_async_impl(stmt, [keyspace, table])
        if rows:
            return rows[0]
        return {}

    async def _get_existing_indexes_async(self, table: str, keyspace: str) -> set[str]:
        """Introspect existing index names from ``system_schema.indexes``."""
        stmt = "SELECT index_name FROM system_schema.indexes WHERE keyspace_name = ? AND table_name = ?"
        rows = await self._execute_async_impl(stmt, [keyspace, table])
        return {row["index_name"] for row in rows}

    async def _sync_table_async_impl(
        self,
        table: str,
        keyspace: str,
        cols: list[Any],
        table_options: dict[str, Any] | None = None,
        dry_run: bool = False,
        drop_removed_indexes: bool = False,
    ) -> list[str]:
        cache_key = f"{keyspace}.{table}"
        col_names = frozenset(col.name for col in cols)
        if not dry_run and not drop_removed_indexes and self._known_tables.get(cache_key) == col_names:
            return []  # table already synced this session with same columns

        from coodie.cql_builder import (
            build_create_table,
            build_create_index,
            build_drop_index,
            build_alter_table_options,
        )

        planned: list[str] = []

        # 1. CREATE TABLE IF NOT EXISTS
        create_cql = build_create_table(table, keyspace, cols, table_options=table_options)
        planned.append(create_cql)
        if not dry_run:
            await self._execute_cql_async(create_cql)

        # 2. Introspect existing columns and add missing ones
        existing = await self._get_existing_columns_async(table, keyspace)
        model_col_names = {col.name for col in cols}
        is_new_table = existing == model_col_names

        if not is_new_table:
            for col in cols:
                if col.name not in existing:
                    alter = f'ALTER TABLE {keyspace}.{table} ADD "{col.name}" {col.cql_type}'
                    planned.append(alter)
                    if not dry_run:
                        await self._execute_cql_async(alter)

        # 3. Schema drift detection — warn on DB columns not in model
        drift_cols = existing - model_col_names
        if drift_cols:
            import logging

            logger = logging.getLogger("coodie")
            logger.warning(
                "Schema drift detected: columns %s exist in %s.%s but are not defined in the model",
                drift_cols,
                keyspace,
                table,
            )

        # 4. Table option changes
        if table_options:
            current_options = await self._get_current_table_options_async(table, keyspace)
            changed = {}
            for k, v in table_options.items():
                if str(current_options.get(k)) != str(v):
                    changed[k] = v
            if changed:
                alter_cql = build_alter_table_options(table, keyspace, changed)
                planned.append(alter_cql)
                if not dry_run:
                    await self._execute_cql_async(alter_cql)

        # 5. Create secondary indexes
        model_indexes: dict[str, Any] = {}
        for col in cols:
            if col.index:
                idx_name = col.index_name or f"{table}_{col.name}_idx"
                model_indexes[idx_name] = col
                index_cql = build_create_index(table, keyspace, col)
                planned.append(index_cql)
                if not dry_run:
                    await self._execute_cql_async(index_cql)

        # 6. Drop removed indexes
        if drop_removed_indexes:
            existing_indexes = await self._get_existing_indexes_async(table, keyspace)
            for idx_name in existing_indexes:
                if idx_name not in model_indexes:
                    drop_cql = build_drop_index(idx_name, keyspace)
                    planned.append(drop_cql)
                    if not dry_run:
                        await self._execute_cql_async(drop_cql)

        if not dry_run:
            self._known_tables[cache_key] = col_names

        return planned

    async def sync_table_async(
        self,
        table: str,
        keyspace: str,
        cols: list[Any],
        table_options: dict[str, Any] | None = None,
        dry_run: bool = False,
        drop_removed_indexes: bool = False,
    ) -> list[str]:
        coro = self._sync_table_async_impl(
            table,
            keyspace,
            cols,
            table_options=table_options,
            dry_run=dry_run,
            drop_removed_indexes=drop_removed_indexes,
        )
        if self._bridge_to_bg_loop:
            return await self._run_on_bg_loop(coro)
        return await coro

    async def _close_async_impl(self) -> None:
        """No-op — python-rs-driver has no explicit ``close()`` on Session."""

    async def close_async(self) -> None:
        if self._bridge_to_bg_loop:
            await self._run_on_bg_loop(self._close_async_impl())
        else:
            await self._close_async_impl()

    # ------------------------------------------------------------------
    # Synchronous interface (event-loop bridge)
    # Uses the stored event loop so the python-rs-driver session — which
    # is bound to a specific tokio runtime — is always accessed correctly.
    # Must only be called from non-async contexts.
    # ------------------------------------------------------------------

    def execute(
        self,
        stmt: str,
        params: list[Any],
        consistency: str | None = None,
        timeout: float | None = None,
        fetch_size: int | None = None,
        paging_state: bytes | None = None,
    ) -> list[dict[str, Any]]:
        return asyncio.run_coroutine_threadsafe(
            self._execute_async_impl(
                stmt,
                params,
                consistency=consistency,
                timeout=timeout,
                fetch_size=fetch_size,
                paging_state=paging_state,
            ),
            self._bg_loop,
        ).result()

    def sync_table(
        self,
        table: str,
        keyspace: str,
        cols: list[Any],
        table_options: dict[str, Any] | None = None,
        dry_run: bool = False,
        drop_removed_indexes: bool = False,
    ) -> list[str]:
        return asyncio.run_coroutine_threadsafe(
            self._sync_table_async_impl(
                table,
                keyspace,
                cols,
                table_options=table_options,
                dry_run=dry_run,
                drop_removed_indexes=drop_removed_indexes,
            ),
            self._bg_loop,
        ).result()

    def close(self) -> None:
        asyncio.run_coroutine_threadsafe(self._close_async_impl(), self._bg_loop).result()
        self._bg_loop.call_soon_threadsafe(self._bg_loop.stop)
        self._bg_thread.join(timeout=10)
