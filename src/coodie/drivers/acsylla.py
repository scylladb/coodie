from __future__ import annotations

import asyncio
import threading
import warnings
from collections.abc import Awaitable, Callable
from typing import Any

from coodie.cql_builder import qualified_name, schema_name
from coodie.drivers.base import AbstractDriver, _is_ddl


class AcsyllaDriver(AbstractDriver):
    """Driver backed by the `acsylla <https://github.com/acsylla/acsylla>`_ async-native library.

    .. note::
       ``needs_row_validation`` is ``True`` because acsylla returns UUID
       values as strings rather than ``uuid.UUID`` objects.

    ``acsylla`` is an **optional** dependency — install it separately::

        pip install acsylla

    **Typical async usage** (FastAPI / asyncio application):

    .. code-block:: python

        import acsylla
        from coodie.aio import Document, init_coodie
        from coodie.drivers import register_driver
        from coodie.drivers.acsylla import AcsyllaDriver
        from coodie import PrimaryKey
        from typing import Annotated
        from uuid import UUID, uuid4
        from pydantic import Field

        class Product(Document):
            id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
            name: str

            class Settings:
                name = "products"
                keyspace = "catalog"

        # Build an acsylla session, then wrap it in AcsyllaDriver
        cluster = acsylla.create_cluster(["127.0.0.1"])
        session = await cluster.create_session(keyspace="catalog")

        driver = AcsyllaDriver(session=session, default_keyspace="catalog")
        register_driver("default", driver, default=True)

        await Product.sync_table()

        product = Product(name="Widget")
        await product.save()

        results = await Product.find(name="Widget").all()

    **Sync bridge** — ``execute()``, ``sync_table()``, and ``close()`` dispatch
    to a dedicated background event loop that is started in a daemon thread at
    construction time.  This means they work correctly even when called from
    within an already-running event loop (e.g. inside pytest-asyncio, ASGI
    middleware, or ``asyncio.run()``), avoiding the
    ``RuntimeError: This event loop is already running`` that
    ``loop.run_until_complete()`` would raise in those contexts.

    For the sync bridge to function correctly the acsylla session must be
    created on the background loop so that its internal futures are bound to
    that loop.  Use the :meth:`connect` factory classmethod — it creates the
    session on the background loop automatically.  The standard
    ``__init__(session=...)`` form is intended for **pure async** usage where
    the sync bridge is not needed.
    """

    needs_row_validation: bool = True

    __slots__ = (
        "_acsylla",
        "_bg_loop",
        "_bg_thread",
        "_bridge_to_bg_loop",
        "_default_keyspace",
        "_known_tables",
        "_last_paging_state",
        "_prepared",
        "_session",
    )

    def __init__(
        self,
        session: Any,
        default_keyspace: str | None = None,
    ) -> None:
        try:
            import acsylla  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError("acsylla is required for AcsyllaDriver. Install it with: pip install acsylla") from exc
        self._acsylla = acsylla
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
        self._bg_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self._bg_thread = threading.Thread(
            target=self._bg_loop.run_forever,
            daemon=True,
            name="coodie-acsylla-sync",
        )
        self._bg_thread.start()
        self._bridge_to_bg_loop: bool = False
        warnings.warn(
            "AcsyllaDriver(session=...) creates a driver whose session is not on "
            "the background loop; sync calls (execute, sync_table, close) may hang. "
            "Use AcsyllaDriver.connect_sync() or init_coodie(hosts=...) for a "
            "sync-capable driver.",
            UserWarning,
            stacklevel=2,
        )

    @classmethod
    def connect(
        cls,
        session_factory: Callable[[], Awaitable[Any]],
        default_keyspace: str | None = None,
    ) -> AcsyllaDriver:
        """Create a driver whose acsylla session lives on the background loop.

        ``session_factory`` is a zero-argument callable that returns an
        **awaitable** (e.g. an ``async def`` function or a lambda wrapping one).
        It is invoked on the background loop,
        so the resulting session is properly bound to that loop.  This enables
        both the sync bridge (``execute``, ``sync_table``, ``close``) and the
        async interface (``execute_async``, …) to work correctly from any
        calling context, including an already-running event loop.

        Example::

            import acsylla, asyncio
            from coodie.drivers.acsylla import AcsyllaDriver

            async def make_session():
                cluster = acsylla.create_cluster(["127.0.0.1"])
                return await cluster.create_session(keyspace="catalog")

            driver = AcsyllaDriver.connect(make_session, default_keyspace="catalog")
        """
        try:
            import acsylla  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError("acsylla is required for AcsyllaDriver. Install it with: pip install acsylla") from exc

        # Bootstrap the infrastructure before creating the session so the
        # session is bound to _bg_loop from the start.
        bg_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        bg_thread = threading.Thread(
            target=bg_loop.run_forever,
            daemon=True,
            name="coodie-acsylla-sync",
        )
        bg_thread.start()

        session = asyncio.run_coroutine_threadsafe(session_factory(), bg_loop).result()

        driver: AcsyllaDriver = cls.__new__(cls)
        driver._acsylla = acsylla
        driver._session = session
        driver._default_keyspace = default_keyspace
        driver._prepared = {}
        driver._last_paging_state = None
        driver._known_tables = {}
        driver._bg_loop = bg_loop
        driver._bg_thread = bg_thread
        driver._bridge_to_bg_loop = True
        return driver

    @classmethod
    def connect_sync(
        cls,
        hosts: list[str],
        keyspace: str | None = None,
        **kwargs: Any,
    ) -> AcsyllaDriver:
        """Blocking factory that creates a sync-capable driver from *hosts*.

        Bootstraps a background event loop, creates the acsylla session **on
        that loop** via ``run_coroutine_threadsafe``, and returns a driver with
        ``_bridge_to_bg_loop = True`` so that the synchronous interface
        (``execute``, ``sync_table``, ``close``) works correctly.

        This is the recommended entry-point when calling ``init_coodie()`` with
        ``driver_type="acsylla"`` and ``hosts=...``.

        Extra ``**kwargs`` are forwarded to ``acsylla.create_cluster(hosts, **kwargs)``.

        Example::

            driver = AcsyllaDriver.connect_sync(["127.0.0.1"], keyspace="catalog")
        """
        try:
            import acsylla  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError("acsylla is required for AcsyllaDriver. Install it with: pip install acsylla") from exc

        async def _make_session() -> Any:
            cluster = acsylla.create_cluster(hosts, **kwargs)
            return await cluster.create_session(keyspace=keyspace)

        return cls.connect(session_factory=_make_session, default_keyspace=keyspace)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _prepare(self, cql: str) -> Any:
        if cql not in self._prepared:
            self._prepared[cql] = await self._session.create_prepared(cql)
        return self._prepared[cql]

    @staticmethod
    def _rows_to_dicts(result: Any) -> list[dict[str, Any]]:
        return [dict(row) for row in result]

    def _cql_to_statement(self, cql: str) -> Any:
        """Wrap a raw CQL string in an acsylla Statement for session.execute()."""
        return self._acsylla.create_statement(cql, parameters=0)

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
        if not params and _is_ddl(stmt):
            result = await self._session.execute(self._cql_to_statement(stmt))
            return self._rows_to_dicts(result)
        prepared = await self._prepare(stmt)
        bind_kwargs: dict[str, Any] = {}
        if consistency is not None:
            bind_kwargs["consistency"] = consistency
        if timeout is not None:
            bind_kwargs["timeout"] = timeout
        if fetch_size is not None:
            bind_kwargs["page_size"] = fetch_size
        statement = prepared.bind(params, **bind_kwargs)
        if paging_state is not None:
            statement.set_page_state(paging_state)
        result = await self._session.execute(statement)
        if fetch_size is not None:
            has_more = result.has_more_pages()
            self._last_paging_state = result.page_state() if has_more else None
        else:
            self._last_paging_state = None
        return self._rows_to_dicts(result)

    async def _get_existing_columns_async(self, table: str, keyspace: str) -> set[str]:
        """Introspect the existing column names via system_schema."""
        stmt = "SELECT column_name FROM system_schema.columns WHERE keyspace_name = ? AND table_name = ?"
        rows = await self._execute_async_impl(stmt, [schema_name(keyspace), schema_name(table)])
        return {row["column_name"] for row in rows}

    async def _get_current_table_options_async(self, table: str, keyspace: str) -> dict[str, Any]:
        """Introspect current table options from ``system_schema.tables``."""
        stmt = "SELECT * FROM system_schema.tables WHERE keyspace_name = ? AND table_name = ?"
        rows = await self._execute_async_impl(stmt, [schema_name(keyspace), schema_name(table)])
        if rows:
            return rows[0]
        return {}

    async def _get_existing_indexes_async(self, table: str, keyspace: str) -> set[str]:
        """Introspect existing index names from ``system_schema.indexes``."""
        stmt = "SELECT index_name FROM system_schema.indexes WHERE keyspace_name = ? AND table_name = ?"
        rows = await self._execute_async_impl(stmt, [schema_name(keyspace), schema_name(table)])
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
            build_alter_table_options,
            build_create_index,
            build_create_table,
            build_drop_index,
        )

        planned: list[str] = []

        # 1. CREATE TABLE IF NOT EXISTS
        create_cql = build_create_table(table, keyspace, cols, table_options=table_options)
        planned.append(create_cql)
        if not dry_run:
            await self._session.execute(self._cql_to_statement(create_cql))

        # 2. Introspect existing columns and add missing ones
        existing = await self._get_existing_columns_async(table, keyspace)
        model_col_names = {col.name for col in cols}
        is_new_table = existing == model_col_names

        if not is_new_table:
            for col in cols:
                if col.name not in existing:
                    alter = f'ALTER TABLE {qualified_name(keyspace, table)} ADD "{col.name}" {col.cql_type}'
                    planned.append(alter)
                    if not dry_run:
                        await self._session.execute(self._cql_to_statement(alter))

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
                    await self._session.execute(self._cql_to_statement(alter_cql))

        # 5. Create secondary indexes
        model_indexes: dict[str, Any] = {}
        for col in cols:
            if col.index:
                idx_name = col.index_name or f"{schema_name(table)}_{col.name}_idx"
                model_indexes[schema_name(idx_name)] = col
                index_cql = build_create_index(table, keyspace, col)
                planned.append(index_cql)
                if not dry_run:
                    await self._session.execute(self._cql_to_statement(index_cql))

        # 6. Drop removed indexes
        if drop_removed_indexes:
            existing_indexes = await self._get_existing_indexes_async(table, keyspace)
            for idx_name in existing_indexes:
                if idx_name not in model_indexes:
                    drop_cql = build_drop_index(idx_name, keyspace)
                    planned.append(drop_cql)
                    if not dry_run:
                        await self._session.execute(self._cql_to_statement(drop_cql))

        if not dry_run:
            self._known_tables[cache_key] = col_names

        return planned

    async def _close_async_impl(self) -> None:
        await self._session.close()

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

    async def close_async(self) -> None:
        if self._bridge_to_bg_loop:
            await self._run_on_bg_loop(self._close_async_impl())
        else:
            await self._close_async_impl()

    # ------------------------------------------------------------------
    # Synchronous interface (event-loop bridge)
    # Submits coroutines to the dedicated background loop via
    # run_coroutine_threadsafe, then blocks with .result().  This is safe
    # to call from any thread — including one that already has a running
    # event loop (e.g. pytest-asyncio, ASGI request handlers).
    # The session must be on _bg_loop (use connect() to ensure this).
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
