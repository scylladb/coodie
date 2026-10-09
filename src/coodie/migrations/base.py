"""Migration base class and execution context."""

from __future__ import annotations

import asyncio
import hashlib
import logging
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

logger = logging.getLogger("coodie")

# Cassandra/ScyllaDB murmur3 token range
_TOKEN_MIN = -(2**63)
_TOKEN_MAX = 2**63 - 1


class MigrationContext:
    """Execution context passed to :meth:`Migration.upgrade` and :meth:`Migration.downgrade`.

    Wraps a coodie driver and provides a simple ``execute`` interface
    for running arbitrary CQL statements inside a migration.
    """

    __slots__ = ("_driver", "_dry_run", "_executed_cql")

    def __init__(self, driver: Any, *, dry_run: bool = False) -> None:
        self._driver = driver
        self._dry_run = dry_run
        self._executed_cql: list[str] = []

    async def execute(self, cql: str, params: list[Any] | None = None) -> list[dict[str, Any]]:
        """Execute a CQL statement.

        In dry-run mode the statement is recorded but not sent to the database.
        """
        self._executed_cql.append(cql)
        if self._dry_run:
            return []
        return await self._driver.execute_async(cql, params or [])

    @property
    def planned_cql(self) -> list[str]:
        """Return the list of CQL statements executed (or planned in dry-run)."""
        return list(self._executed_cql)

    # ------------------------------------------------------------------
    # D.1–D.4 — Data migration helpers
    # ------------------------------------------------------------------

    async def _get_all_columns(self, keyspace: str, table: str) -> list[dict[str, Any]]:
        """Fetch all column metadata for *keyspace*.*table* from system_schema.

        Uses only the primary-key columns of ``system_schema.columns``
        (``keyspace_name`` + ``table_name``) so no ALLOW FILTERING is needed.
        """
        return await self._driver.execute_async(
            "SELECT column_name, kind, position, clustering_order FROM system_schema.columns WHERE keyspace_name = ? AND table_name = ?",
            [keyspace, table],
        )

    async def _get_key_columns(self, keyspace: str, table: str) -> tuple[list[str], list[dict[str, Any]]]:
        """Return ``(partition_key_columns, clustering_column_rows)`` in schema order."""
        rows = await self._get_all_columns(keyspace, table)

        def _cols(kind: str) -> list[dict[str, Any]]:
            return sorted((r for r in rows if r.get("kind") == kind), key=lambda r: r.get("position", 0))

        pk_cols = [r["column_name"] for r in _cols("partition_key")]
        if not pk_cols:
            raise ValueError(f"No partition key columns found for {keyspace}.{table}")
        return pk_cols, _cols("clustering")

    async def column_exists(self, keyspace: str, table: str, column: str) -> bool:
        if self._dry_run:
            return False
        rows = await self._get_all_columns(keyspace, table)
        return any(r.get("column_name") == column for r in rows)

    async def index_exists(self, keyspace: str, table: str, index_name: str) -> bool:
        """Return ``True`` if a secondary index named *index_name* exists on *keyspace*.*table*.

        Queries ``system_schema.indexes`` using only (keyspace_name, table_name)
        to avoid ALLOW FILTERING, then matches by index_name in Python.
        In dry-run mode always returns ``False``.
        """
        if self._dry_run:
            return False
        rows = await self._driver.execute_async(
            "SELECT index_name FROM system_schema.indexes WHERE keyspace_name = ? AND table_name = ?",
            [keyspace, table],
        )
        return any(r.get("index_name") == index_name for r in rows)

    async def scan_table(
        self,
        keyspace: str,
        table: str,
        *,
        page_size: int = 1000,
        num_ranges: int = 1000,
        resume_token: int | None = None,
        throttle_seconds: float = 0.0,
    ) -> AsyncIterator[dict[str, Any]]:
        """Iterate over all rows in a table using token-range queries.

        Uses ``token()`` on the partition key to walk through the full
        token ring in *num_ranges* sub-ranges, fetching at most
        *page_size* rows per query and paging within each sub-range until
        it is exhausted.  Rows are yielded one at a time so the entire
        table is never loaded into memory.

        Parameters
        ----------
        keyspace:
            Keyspace containing the target table.
        table:
            Table name.
        page_size:
            Maximum rows per token-range query (``LIMIT``).
        num_ranges:
            Number of sub-ranges to divide the token ring into.
        resume_token:
            If provided, skip all ranges whose start token is ``<=``
            this value.  Useful for resuming a failed migration from
            where it stopped.
        throttle_seconds:
            If ``> 0``, sleep this many seconds between each token-range
            query to avoid overloading the cluster.

        Yields
        ------
        dict[str, Any]
            One row at a time from the table.

        Notes
        -----
        In dry-run mode the scan is skipped entirely and a single
        placeholder row ``{"__dry_run__": True}`` is yielded.
        """
        if self._dry_run:
            self._executed_cql.append(f"-- scan_table {keyspace}.{table} (dry-run)")
            yield {"__dry_run__": True}
            return

        pk_cols, ck_rows = await self._get_key_columns(keyspace, table)
        ck_cols = [r["column_name"] for r in ck_rows]
        pk_list = ", ".join(f'"{c}"' for c in pk_cols)
        token_expr = f"token({pk_list})"
        pk_token = f"token({', '.join('?' * len(pk_cols))})"
        select = f"SELECT * FROM {keyspace}.{table} WHERE "
        limit = f" LIMIT {page_size}"
        first_cql = f"{select}{token_expr} > ? AND {token_expr} <= ?{limit}"
        # Next partitions: strictly after the last seen partition's token.
        next_cql = f"{select}{token_expr} > {pk_token} AND {token_expr} <= ?{limit}"
        # Other partitions sharing that token (murmur3 collision), so they are not skipped.
        same_token_cql = f"SELECT DISTINCT {pk_list} FROM {keyspace}.{table} WHERE {token_expr} = {pk_token}"
        # One partition, in storage order: after_cql[k] fixes the first k
        # clustering columns and slices on column k in its clustering order.
        pk_eq = " AND ".join(f'"{c}" = ?' for c in pk_cols)
        partition_cql = f"{select}{pk_eq}{limit}"
        after_cql = [
            f"{select}{pk_eq}"
            + "".join(f' AND "{c}" = ?' for c in ck_cols[:k])
            + f' AND "{ck_cols[k]}" {"<" if str(ck_rows[k].get("clustering_order")).lower() == "desc" else ">"} ?{limit}'
            for k in range(len(ck_cols))
        ]

        async def run(cql: str, params: list[Any]) -> list[dict[str, Any]]:
            self._executed_cql.append(cql)
            return await self._driver.execute_async(cql, params)

        async def partition_rows(pk_vals: list[Any], last: dict[str, Any] | None) -> AsyncIterator[dict[str, Any]]:
            """Yield the rows of one partition after *last* (all rows if ``None``)."""
            if last is None:
                rows = await run(partition_cql, pk_vals)
                for row in rows:
                    yield row
                if len(rows) < page_size:
                    return
                last = rows[-1]
            ck_vals = [last.get(c) for c in ck_cols]
            if None in ck_vals:  # static-only row: no clustering rows to continue from
                return
            k = len(ck_cols) - 1
            while k >= 0:
                rows = await run(after_cql[k], pk_vals + ck_vals[: k + 1])
                for row in rows:
                    yield row
                if len(rows) < page_size:
                    k -= 1
                else:
                    ck_vals = [rows[-1][c] for c in ck_cols]
                    k = len(ck_cols) - 1

        # Build sub-range boundaries
        range_size = (_TOKEN_MAX - _TOKEN_MIN) // num_ranges
        boundaries: list[int] = []
        for i in range(num_ranges):
            boundaries.append(_TOKEN_MIN + range_size * i)
        boundaries.append(_TOKEN_MAX)

        total_ranges = len(boundaries) - 1
        ranges_done = 0

        for i in range(total_ranges):
            range_start = boundaries[i]
            range_end = boundaries[i + 1]

            # D.3 — Resume-from-token: skip already-processed ranges
            if resume_token is not None and range_start <= resume_token:
                ranges_done += 1
                continue

            # Page through the sub-range.  A full page may end mid-partition,
            # so finish that partition (and any partition sharing its token)
            # before resuming from the next token.
            cql, params = first_cql, [range_start, range_end]
            while True:
                rows = await run(cql, params)
                for row in rows:
                    yield row
                if len(rows) < page_size:
                    break
                pk_vals = [rows[-1][c] for c in pk_cols]
                async for row in partition_rows(pk_vals, rows[-1]):
                    yield row
                seen = [[r[c] for c in pk_cols] for r in rows]
                for other in await run(same_token_cql, pk_vals):
                    other_vals = [other[c] for c in pk_cols]
                    if other_vals not in seen:
                        async for row in partition_rows(other_vals, None):
                            yield row
                cql, params = next_cql, [*pk_vals, range_end]

            ranges_done += 1

            # D.2 — Progress reporting
            pct = (ranges_done / total_ranges) * 100
            if ranges_done % max(1, total_ranges // 10) == 0 or ranges_done == total_ranges:
                logger.info(
                    "scan_table %s.%s — %d/%d ranges (%.1f%%), last_token=%d",
                    keyspace,
                    table,
                    ranges_done,
                    total_ranges,
                    pct,
                    range_end,
                )

            # D.4 — Rate limiting / throttle
            if throttle_seconds > 0:
                await asyncio.sleep(throttle_seconds)


class Migration:
    """Base class for coodie migration files.

    Subclass this in a migration file and override :meth:`upgrade` (and
    optionally :meth:`downgrade`) to define schema or data changes.

    Example::

        from coodie.migrations import Migration

        class ForwardMigration(Migration):
            description = "Add rating column to reviews table"
            allow_destructive = False

            async def upgrade(self, ctx):
                await ctx.execute(
                    'ALTER TABLE catalog.reviews ADD "rating" int'
                )

            async def downgrade(self, ctx):
                await ctx.execute(
                    'ALTER TABLE catalog.reviews DROP "rating"'
                )
    """

    description: str = ""
    allow_destructive: bool = False
    reversible: bool = True

    async def upgrade(self, ctx: MigrationContext) -> None:
        """Apply the migration. Must be overridden."""
        raise NotImplementedError("Migration.upgrade() must be implemented")

    async def downgrade(self, ctx: MigrationContext) -> None:
        """Reverse the migration. Optional — override when reversible."""
        raise NotImplementedError("Migration.downgrade() is not implemented for this migration")

    @staticmethod
    def compute_checksum(path: Path) -> str:
        """Compute a SHA-256 checksum of a migration file."""
        return hashlib.sha256(path.read_bytes()).hexdigest()
