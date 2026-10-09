"""Migration runner — discovery, ordering, execution, and state tracking."""

from __future__ import annotations

import importlib.util
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from coodie.migrations.base import Migration, MigrationContext

logger = logging.getLogger("coodie")

# Pattern: YYYYMMDD_NNN_description.py
_MIGRATION_RE = re.compile(r"^(\d{8}_\d{3})_.+\.py$")

# CQL for the migrations state table
_CREATE_STATE_TABLE = (
    'CREATE TABLE IF NOT EXISTS {keyspace}."_coodie_migrations" ('
    "migration_name text PRIMARY KEY, "
    "applied_at timestamp, "
    "description text, "
    "checksum text)"
)

# CQL for the lock table (LWT-based single-writer lock)
_CREATE_LOCK_TABLE = (
    'CREATE TABLE IF NOT EXISTS {keyspace}."_coodie_migrations_lock" ('
    "lock_id text PRIMARY KEY, "
    "acquired_at timestamp, "
    "owner text)"
)

_ACQUIRE_LOCK = (
    'INSERT INTO {keyspace}."_coodie_migrations_lock" '
    "(lock_id, acquired_at, owner) "
    "VALUES (?, ?, ?) IF NOT EXISTS USING TTL {ttl}"
)

_RELEASE_LOCK = 'DELETE FROM {keyspace}."_coodie_migrations_lock" WHERE lock_id = ?'


class MigrationInfo:
    """Metadata about a single discovered migration file."""

    __slots__ = ("name", "path", "sort_key")

    def __init__(self, name: str, path: Path, sort_key: str) -> None:
        self.name = name
        self.path = path
        self.sort_key = sort_key

    def __repr__(self) -> str:
        return f"MigrationInfo(name={self.name!r})"


def discover_migrations(directory: str | Path) -> list[MigrationInfo]:
    """Discover migration files in *directory*, sorted by timestamp prefix.

    Migration files must match ``YYYYMMDD_NNN_<description>.py`` (e.g.
    ``20260115_001_add_rating_column.py``).
    """
    directory = Path(directory)
    if not directory.is_dir():
        return []

    migrations: list[MigrationInfo] = []
    for p in sorted(directory.iterdir()):
        if not p.is_file():
            continue
        m = _MIGRATION_RE.match(p.name)
        if m:
            sort_key = m.group(1)
            name = p.stem  # filename without .py
            migrations.append(MigrationInfo(name=name, path=p, sort_key=sort_key))

    migrations.sort(key=lambda mi: mi.sort_key)
    return migrations


def _load_migration_class(info: MigrationInfo) -> Migration:
    """Import a migration file and return an instance of its ``ForwardMigration`` class."""
    spec = importlib.util.spec_from_file_location(info.name, info.path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load migration file: {info.path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]

    cls = getattr(module, "ForwardMigration", None)
    if cls is None:
        raise ImportError(f"Migration file {info.path} must define a 'ForwardMigration' class")
    if not (isinstance(cls, type) and issubclass(cls, Migration)):
        raise ImportError(  # noqa: TRY004 - callers expect ImportError for invalid migration modules
            f"ForwardMigration in {info.path} must be a subclass of coodie.migrations.Migration"
        )
    return cls()


class MigrationRunner:
    """Coordinates migration discovery, execution, and state tracking.

    Parameters
    ----------
    driver:
        A coodie driver instance (``CassandraDriver`` or ``AcsyllaDriver``).
    keyspace:
        The keyspace where the ``_coodie_migrations`` table lives.
    migrations_dir:
        Path to the directory containing migration files.
    lock_ttl:
        TTL in seconds for the distributed lock (default 300 = 5 minutes).
    """

    def __init__(
        self,
        driver: Any,
        keyspace: str,
        migrations_dir: str | Path,
        lock_ttl: int = 300,
    ) -> None:
        self._driver = driver
        self._keyspace = keyspace
        self._migrations_dir = Path(migrations_dir)
        self._lock_ttl = lock_ttl

    # ------------------------------------------------------------------
    # B.3 — State tracking table
    # ------------------------------------------------------------------

    async def _ensure_state_table(self) -> None:
        """Create the ``_coodie_migrations`` tracking table if it does not exist."""
        cql = _CREATE_STATE_TABLE.format(keyspace=self._keyspace)
        await self._driver.execute_async(cql, [])

    async def _ensure_lock_table(self) -> None:
        """Create the ``_coodie_migrations_lock`` table if it does not exist."""
        cql = _CREATE_LOCK_TABLE.format(keyspace=self._keyspace)
        await self._driver.execute_async(cql, [])

    async def get_applied(self) -> dict[str, dict[str, Any]]:
        """Return a dict of applied migration names → metadata."""
        await self._ensure_state_table()
        rows = await self._driver.execute_async(
            f'SELECT migration_name, applied_at, description, checksum FROM {self._keyspace}."_coodie_migrations"',
            [],
        )
        return {row["migration_name"]: row for row in rows}

    async def _record_applied(self, name: str, description: str, checksum: str) -> None:
        """Record a migration as applied in the state table."""
        await self._driver.execute_async(
            f'INSERT INTO {self._keyspace}."_coodie_migrations" '
            f"(migration_name, applied_at, description, checksum) VALUES (?, ?, ?, ?)",
            [name, datetime.now(timezone.utc), description, checksum],
        )

    async def _remove_applied(self, name: str) -> None:
        """Remove a migration record from the state table (on rollback)."""
        await self._driver.execute_async(
            f'DELETE FROM {self._keyspace}."_coodie_migrations" WHERE migration_name = ?',
            [name],
        )

    # ------------------------------------------------------------------
    # B.5 — LWT-based single-writer lock
    # ------------------------------------------------------------------

    async def _acquire_lock(self, owner: str = "coodie-migrate") -> bool:
        """Attempt to acquire the distributed migration lock via LWT.

        Returns ``True`` if the lock was acquired, ``False`` if another
        process holds it.
        """
        await self._ensure_lock_table()
        cql = _ACQUIRE_LOCK.format(keyspace=self._keyspace, ttl=self._lock_ttl)
        rows = await self._driver.execute_async(cql, ["coodie_migration_lock", datetime.now(timezone.utc), owner])
        return not (rows and not rows[0].get("[applied]", True))

    async def _release_lock(self) -> None:
        """Release the distributed migration lock."""
        cql = _RELEASE_LOCK.format(keyspace=self._keyspace)
        await self._driver.execute_async(cql, ["coodie_migration_lock"])

    # ------------------------------------------------------------------
    # B.6 — Schema agreement wait
    # ------------------------------------------------------------------

    async def _wait_for_schema_agreement(self, timeout: float = 30.0) -> bool:
        """Wait until all nodes agree on the schema version.

        Queries ``system.local`` and ``system.peers`` to compare schema
        versions.  Returns ``True`` when agreement is reached or ``False``
        if *timeout* is exceeded.
        """
        import asyncio

        deadline = asyncio.get_event_loop().time() + timeout
        while True:
            local_rows = await self._driver.execute_async(
                "SELECT schema_version FROM system.local WHERE key = 'local'", []
            )
            peer_rows = await self._driver.execute_async("SELECT schema_version FROM system.peers", [])

            versions: set[Any] = set()
            if local_rows:
                versions.add(local_rows[0].get("schema_version"))
            for row in peer_rows:
                versions.add(row.get("schema_version"))

            if len(versions) <= 1:
                return True

            if asyncio.get_event_loop().time() >= deadline:
                logger.warning(
                    "Schema agreement not reached within %.1fs — %d distinct versions detected",
                    timeout,
                    len(versions),
                )
                return False

            await asyncio.sleep(0.5)

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    async def pending(self) -> list[MigrationInfo]:
        """Return the list of migrations that have not yet been applied."""
        all_migrations = discover_migrations(self._migrations_dir)
        applied = await self.get_applied()
        return [m for m in all_migrations if m.name not in applied]

    async def status(self) -> list[dict[str, Any]]:
        """Return the status of all discovered migrations.

        Each entry has ``name``, ``applied`` (bool), ``applied_at``, and
        ``description``.
        """
        all_migrations = discover_migrations(self._migrations_dir)
        applied = await self.get_applied()
        result = []
        for m in all_migrations:
            info = applied.get(m.name)
            result.append(
                {
                    "name": m.name,
                    "applied": m.name in applied,
                    "applied_at": info["applied_at"] if info else None,
                    "description": info["description"] if info else "",
                }
            )
        return result

    async def apply(
        self,
        *,
        dry_run: bool = False,
        target: str | None = None,
    ) -> list[dict[str, Any]]:
        """Apply pending migrations.

        Parameters
        ----------
        dry_run:
            When ``True``, migrations are executed in dry-run mode: CQL
            statements are collected but not sent to the database.
        target:
            Stop after applying the migration whose name starts with this
            prefix.  ``None`` means apply all pending.

        Returns
        -------
        A list of dicts with ``name``, ``description``, and ``planned_cql``
        for each migration that was applied (or would be in dry-run).
        """
        await self._ensure_state_table()

        if not dry_run and not await self._acquire_lock():
            from coodie.exceptions import MigrationError

            raise MigrationError("Cannot acquire migration lock — another migration may be in progress")

        try:
            return await self._apply_inner(dry_run=dry_run, target=target)
        finally:
            if not dry_run:
                await self._release_lock()

    async def _apply_inner(
        self,
        *,
        dry_run: bool,
        target: str | None,
    ) -> list[dict[str, Any]]:
        pending = await self.pending()
        if not pending:
            logger.info("No pending migrations.")
            return []

        results: list[dict[str, Any]] = []
        for info in pending:
            migration = _load_migration_class(info)
            checksum = Migration.compute_checksum(info.path)
            ctx = MigrationContext(self._driver, dry_run=dry_run)

            logger.info("Applying migration: %s — %s", info.name, migration.description)

            if not dry_run:
                await self._wait_for_schema_agreement()

            await migration.upgrade(ctx)

            if not dry_run:
                await self._record_applied(info.name, migration.description, checksum)

            results.append(
                {
                    "name": info.name,
                    "description": migration.description,
                    "planned_cql": ctx.planned_cql,
                }
            )

            if target and info.name.startswith(target):
                break

        return results

    async def rollback(self, *, steps: int = 1, dry_run: bool = False) -> list[dict[str, Any]]:
        """Rollback the last *steps* applied migrations (most-recent first).

        Parameters
        ----------
        steps:
            Number of migrations to roll back.
        dry_run:
            When ``True``, collect planned CQL without executing.

        Returns
        -------
        A list of dicts with ``name``, ``description``, and ``planned_cql``.
        """
        await self._ensure_state_table()

        if not dry_run and not await self._acquire_lock():
            from coodie.exceptions import MigrationError

            raise MigrationError("Cannot acquire migration lock — another migration may be in progress")

        try:
            return await self._rollback_inner(steps=steps, dry_run=dry_run)
        finally:
            if not dry_run:
                await self._release_lock()

    async def _rollback_inner(
        self,
        *,
        steps: int,
        dry_run: bool,
    ) -> list[dict[str, Any]]:
        all_migrations = discover_migrations(self._migrations_dir)
        applied = await self.get_applied()

        # Only rollback migrations that are applied, in reverse order
        applied_migrations = [m for m in all_migrations if m.name in applied]
        to_rollback = list(reversed(applied_migrations))[:steps]

        if not to_rollback:
            logger.info("No migrations to roll back.")
            return []

        results: list[dict[str, Any]] = []
        for info in to_rollback:
            migration = _load_migration_class(info)

            if not migration.reversible:
                from coodie.exceptions import MigrationError

                raise MigrationError(f"Migration {info.name!r} is not reversible")

            ctx = MigrationContext(self._driver, dry_run=dry_run)
            logger.info("Rolling back migration: %s — %s", info.name, migration.description)

            if not dry_run:
                await self._wait_for_schema_agreement()

            await migration.downgrade(ctx)

            if not dry_run:
                await self._remove_applied(info.name)

            results.append(
                {
                    "name": info.name,
                    "description": migration.description,
                    "planned_cql": ctx.planned_cql,
                }
            )

        return results
