from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from typing import Any

_DDL_PREFIXES = ("CREATE ", "DROP ", "ALTER ", "TRUNCATE ")


def _is_ddl(cql: str) -> bool:
    """Return ``True`` if *cql* is a DDL statement (cannot be prepared)."""
    return cql.lstrip().upper().startswith(_DDL_PREFIXES)


class AbstractDriver(ABC):
    """Abstract base class for coodie execution backends."""

    def _warn_if_sai_unsupported(self, exc: Exception) -> None:
        """Warn when vector index creation is not supported by the database; re-raise anything else."""
        msg = str(exc)
        # Known patterns indicating vector index creation is not supported in this configuration:
        # - "Non-supported custom class": index class not available (older ScyllaDB/Cassandra)
        # - "use tablets": keyspace must be tablets-enabled for vector indexes (newer ScyllaDB).
        #   Full message: "Vector index requires the base table's keyspace to use tablets."
        if (
            "Non-supported custom class" in msg
            or "use tablets" in msg
            or "not supported on base tables with tablets" in msg
        ):
            warnings.warn(
                f"Vector index creation skipped: vector search not supported by this database. {exc}",
                stacklevel=3,
            )
        else:
            raise exc

    # Set to ``True`` in driver subclasses whose rows may contain raw
    # types that require Pydantic coercion (e.g. UUID strings instead of
    # ``uuid.UUID``).  When ``True`` the QuerySet auto-selects
    # ``model_validate()`` instead of the fast ``model_construct()`` path.
    needs_row_validation: bool = False

    # ------------------------------------------------------------------
    # Synchronous interface
    # ------------------------------------------------------------------

    @abstractmethod
    def execute(
        self,
        stmt: str,
        params: list[Any],
        consistency: str | None = None,
        timeout: float | None = None,
        fetch_size: int | None = None,
        paging_state: bytes | None = None,
    ) -> list[dict[str, Any]]:
        """Execute *stmt* with *params*; return rows as a list of dicts."""

    @abstractmethod
    def sync_table(
        self,
        table: str,
        keyspace: str,
        cols: list[Any],  # list[ColumnDefinition]
        table_options: dict[str, Any] | None = None,
        dry_run: bool = False,
        drop_removed_indexes: bool = False,
    ) -> list[str]:
        """Idempotent CREATE TABLE + ALTER TABLE ADD for new columns.

        Returns the list of CQL statements that were (or would be) executed.
        When *dry_run* is ``True`` the database is not modified.
        """

    @abstractmethod
    def close(self) -> None:
        """Release sync resources."""

    # ------------------------------------------------------------------
    # Asynchronous interface
    # ------------------------------------------------------------------

    @abstractmethod
    async def execute_async(
        self,
        stmt: str,
        params: list[Any],
        consistency: str | None = None,
        timeout: float | None = None,
        fetch_size: int | None = None,
        paging_state: bytes | None = None,
    ) -> list[dict[str, Any]]:
        """Async version of :meth:`execute`."""

    @abstractmethod
    async def sync_table_async(
        self,
        table: str,
        keyspace: str,
        cols: list[Any],  # list[ColumnDefinition]
        table_options: dict[str, Any] | None = None,
        dry_run: bool = False,
        drop_removed_indexes: bool = False,
    ) -> list[str]:
        """Async version of :meth:`sync_table`."""

    # ------------------------------------------------------------------
    # One-row helpers (default implementations; drivers may override)
    # ------------------------------------------------------------------

    def execute_one(
        self,
        stmt: str,
        params: list[Any],
        consistency: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        """Execute *stmt* and return the first column of the first row, or ``None``."""
        rows = self.execute(stmt, params, consistency=consistency, timeout=timeout)
        if rows:
            return next(iter(rows[0].values()))
        return None

    async def execute_one_async(
        self,
        stmt: str,
        params: list[Any],
        consistency: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        """Async version of :meth:`execute_one`."""
        rows = await self.execute_async(stmt, params, consistency=consistency, timeout=timeout)
        if rows:
            return next(iter(rows[0].values()))
        return None

    @abstractmethod
    async def close_async(self) -> None:
        """Release async resources."""
