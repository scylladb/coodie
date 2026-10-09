"""LazyDriver — defers Cassandra/ScyllaDB connection until first use."""

from __future__ import annotations

import asyncio
import ssl as _ssl
import threading
from typing import TYPE_CHECKING, Any

from coodie.drivers.base import AbstractDriver

if TYPE_CHECKING:
    from coodie.drivers.cassandra import CassandraDriver


class LazyDriver(AbstractDriver):
    """Driver proxy that defers Cassandra/ScyllaDB connection until first use.

    Created by ``init_coodie(..., lazy=True)``.  The underlying
    :class:`~coodie.drivers.cassandra.CassandraDriver` is instantiated on the
    first call to :meth:`execute`, :meth:`execute_async`, :meth:`sync_table`,
    or :meth:`sync_table_async`.
    """

    __slots__ = ("_driver", "_hosts", "_keyspace", "_kwargs", "_lock", "_ssl_context")

    def __init__(
        self,
        hosts: list[str] | None,
        keyspace: str | None,
        ssl_context: _ssl.SSLContext | None,
        kwargs: dict[str, Any],
    ) -> None:
        self._hosts = hosts
        self._keyspace = keyspace
        self._ssl_context = ssl_context
        self._kwargs = kwargs
        self._driver: CassandraDriver | None = None
        self._lock = threading.Lock()

    def _ensure_connected(self) -> None:
        """Connect to Cassandra/ScyllaDB if not already connected (thread-safe)."""
        if self._driver is not None:
            return
        with self._lock:
            if self._driver is not None:
                return
            try:
                from cassandra.cluster import Cluster  # type: ignore[import-untyped]
            except ImportError as exc:
                raise ImportError(
                    "cassandra-driver (or scylla-driver) is required for CassandraDriver. "
                    "Install it with: pip install scylla-driver"
                ) from exc
            kw = dict(self._kwargs)
            if self._ssl_context is not None:
                kw["ssl_context"] = self._ssl_context
            cluster = Cluster(self._hosts or ["127.0.0.1"], **kw)
            session = cluster.connect(self._keyspace)
            from coodie.drivers.cassandra import CassandraDriver

            self._driver = CassandraDriver(session=session, default_keyspace=self._keyspace)

    async def _ensure_connected_async(self) -> None:
        """Async wrapper for :meth:`_ensure_connected` using a thread-pool executor."""
        if self._driver is None:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._ensure_connected)

    # ------------------------------------------------------------------
    # Synchronous interface
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
        self._ensure_connected()
        assert self._driver is not None
        return self._driver.execute(
            stmt,
            params,
            consistency=consistency,
            timeout=timeout,
            fetch_size=fetch_size,
            paging_state=paging_state,
        )

    def sync_table(
        self,
        table: str,
        keyspace: str,
        cols: list[Any],
        table_options: dict[str, Any] | None = None,
        dry_run: bool = False,
        drop_removed_indexes: bool = False,
    ) -> list[str]:
        self._ensure_connected()
        assert self._driver is not None
        return self._driver.sync_table(
            table,
            keyspace,
            cols,
            table_options=table_options,
            dry_run=dry_run,
            drop_removed_indexes=drop_removed_indexes,
        )

    def close(self) -> None:
        if self._driver is not None:
            self._driver.close()

    # ------------------------------------------------------------------
    # Asynchronous interface
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
        await self._ensure_connected_async()
        assert self._driver is not None
        return await self._driver.execute_async(
            stmt,
            params,
            consistency=consistency,
            timeout=timeout,
            fetch_size=fetch_size,
            paging_state=paging_state,
        )

    async def sync_table_async(
        self,
        table: str,
        keyspace: str,
        cols: list[Any],
        table_options: dict[str, Any] | None = None,
        dry_run: bool = False,
        drop_removed_indexes: bool = False,
    ) -> list[str]:
        await self._ensure_connected_async()
        assert self._driver is not None
        return await self._driver.sync_table_async(
            table,
            keyspace,
            cols,
            table_options=table_options,
            dry_run=dry_run,
            drop_removed_indexes=drop_removed_indexes,
        )

    async def close_async(self) -> None:
        if self._driver is not None:
            await self._driver.close_async()
