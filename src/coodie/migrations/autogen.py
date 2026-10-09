"""Migration auto-generation — Phase C.

Introspects the live database schema via ``system_schema.columns`` /
``system_schema.tables`` / ``system_schema.indexes``, diffs against the
current ``Document`` class definitions, and generates migration files.

.. warning::

    The functions in this module are **low-level building blocks**.  For
    production use, prefer the managed CLI workflow which adds distributed
    locking, schema-agreement waiting, and applied-migration tracking:

    .. code-block:: bash

        # Introspect the live DB, diff against your models, and write a file:
        coodie makemigration --name "add rating column" \\
            --keyspace catalog --module myapp.models

        # Preview the diff without writing a file:
        coodie schema-diff --keyspace catalog --module myapp.models

        # Apply pending migrations safely:
        coodie migrate --keyspace catalog

    Calling :func:`introspect_table`, :func:`diff_schema`, or
    :func:`render_migration` directly bypasses the LWT-based single-writer
    lock, schema-agreement check, and ``_coodie_migrations`` state tracking
    that the runner provides.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from coodie.cql_builder import qualified_name, quote_ident, schema_name

if TYPE_CHECKING:
    from coodie.schema import ColumnDefinition

# Pattern: YYYYMMDD_NNN_description.py (mirrors runner._MIGRATION_RE)
_MIGRATION_RE = re.compile(r"^(\d{8}_\d{3})_.+\.py$")

# CQL type widening — these are safe to generate an ALTER without a TODO.
# Keys are (from_type, to_type) pairs.
_SAFE_WIDENING: frozenset[tuple[str, str]] = frozenset(
    {
        ("int", "bigint"),
        ("int", "varint"),
        ("bigint", "varint"),
        ("float", "double"),
        ("text", "blob"),
        ("ascii", "text"),
        ("ascii", "blob"),
        ("timeuuid", "uuid"),
    }
)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class DbColumnInfo:
    """Metadata for a single column returned by ``system_schema.columns``."""

    name: str
    cql_type: str  # e.g. "text", "int", "list<frozen<text>>"
    kind: str  # "partition_key" | "clustering" | "regular" | "static"
    position: int = 0  # position within pk or ck
    clustering_order: str = "ASC"


@dataclass
class ColumnChange:
    """Describes a single detected column change."""

    name: str
    change_type: str  # "add" | "drop" | "type_change" | "pk_change"
    db_type: str | None = None
    model_type: str | None = None
    db_kind: str | None = None  # current kind in DB
    model_kind: str | None = None  # desired kind from model
    unsafe: bool = False
    warning: str = ""


@dataclass
class IndexChange:
    """Describes a single detected index change."""

    index_name: str
    change_type: str  # "add" | "drop"
    column_name: str


@dataclass
class SchemaDiff:
    """Result of comparing a DB table schema with a model schema."""

    keyspace: str
    table: str
    table_exists: bool
    column_changes: list[ColumnChange] = field(default_factory=list)
    index_changes: list[IndexChange] = field(default_factory=list)

    @property
    def has_unsafe_changes(self) -> bool:
        """Return ``True`` when any change cannot be applied automatically."""
        return any(c.unsafe for c in self.column_changes)

    @property
    def has_destructive_changes(self) -> bool:
        """Return ``True`` when any change drops a column or index."""
        return any(c.change_type == "drop" for c in self.column_changes) or any(
            c.change_type == "drop" for c in self.index_changes
        )

    @property
    def is_empty(self) -> bool:
        """Return ``True`` when there are no changes to apply."""
        return not self.column_changes and not self.index_changes


# ---------------------------------------------------------------------------
# C.1 — Database schema introspection
# ---------------------------------------------------------------------------


async def introspect_table(
    driver: Any,
    keyspace: str,
    table: str,
) -> tuple[bool, list[DbColumnInfo], set[str]]:
    """Introspect a single table from the live database.

    .. note::

        Prefer ``coodie schema-diff`` or ``coodie makemigration`` over calling
        this function directly.  The CLI commands wrap introspection with
        schema-agreement checks, distributed locking, and migration tracking.

    Parameters
    ----------
    driver:
        A coodie driver instance.
    keyspace:
        Keyspace name.
    table:
        Table name.

    Returns
    -------
    A 3-tuple ``(table_exists, columns, index_names)`` where

    * ``table_exists`` is ``True`` when the table is present in the DB.
    * ``columns`` is a list of :class:`DbColumnInfo` objects.
    * ``index_names`` is the set of secondary index names on the table.
    """
    # Check whether the table exists
    table_rows = await driver.execute_async(
        "SELECT table_name FROM system_schema.tables WHERE keyspace_name = ? AND table_name = ?",
        [schema_name(keyspace), schema_name(table)],
    )
    if not table_rows:
        return False, [], set()

    # Fetch full column metadata
    col_rows = await driver.execute_async(
        "SELECT column_name, type, kind, position, clustering_order "
        "FROM system_schema.columns "
        "WHERE keyspace_name = ? AND table_name = ?",
        [schema_name(keyspace), schema_name(table)],
    )

    columns: list[DbColumnInfo] = []
    for row in col_rows:
        columns.append(
            DbColumnInfo(
                name=row["column_name"],
                cql_type=row["type"],
                kind=row["kind"],
                position=row.get("position") or 0,
                clustering_order=row.get("clustering_order") or "ASC",
            )
        )

    # Fetch index names
    idx_rows = await driver.execute_async(
        "SELECT index_name FROM system_schema.indexes WHERE keyspace_name = ? AND table_name = ?",
        [schema_name(keyspace), schema_name(table)],
    )
    index_names = {row["index_name"] for row in idx_rows}

    return True, columns, index_names


# ---------------------------------------------------------------------------
# C.2 — Model-to-schema diff engine
# ---------------------------------------------------------------------------


def _model_kind(col: ColumnDefinition) -> str:
    """Return the system_schema ``kind`` string for a model column."""
    if col.primary_key:
        return "partition_key"
    if col.clustering_key:
        return "clustering"
    if col.static:
        return "static"
    return "regular"


def diff_schema(
    keyspace: str,
    table: str,
    db_columns: list[DbColumnInfo],
    model_columns: list[ColumnDefinition],
    db_indexes: set[str],
    table_exists: bool,
) -> SchemaDiff:
    """Compute the diff between the live DB schema and the model schema.

    .. note::

        Prefer ``coodie makemigration`` to generate a migration file from
        the diff, or ``coodie schema-diff`` to preview it.  Applying the
        resulting CQL directly (without going through
        :class:`~coodie.migrations.MigrationRunner`) skips distributed
        locking, schema-agreement waits, and applied-migration tracking.

    Parameters
    ----------
    keyspace / table:
        Fully-qualified table identity.
    db_columns:
        Column metadata from ``system_schema.columns``.
    model_columns:
        Column definitions from the coodie ``Document`` model.
    db_indexes:
        Index names currently present in the DB.
    table_exists:
        ``False`` when the table is not yet in the database.

    Returns
    -------
    A :class:`SchemaDiff` describing all detected changes.
    """
    diff = SchemaDiff(keyspace=keyspace, table=table, table_exists=table_exists)

    if not table_exists:
        # Table is completely missing — no per-column diffs needed;
        # the migration should run CREATE TABLE.
        return diff

    db_by_name: dict[str, DbColumnInfo] = {c.name: c for c in db_columns}
    model_by_name: dict[str, ColumnDefinition] = {c.name: c for c in model_columns}

    # --- Columns in model but not in DB → ADD ---
    for col in model_columns:
        if col.name not in db_by_name:
            desired_kind = _model_kind(col)
            unsafe = desired_kind in ("partition_key", "clustering")
            warning = (
                f'Column "{col.name}" is a {desired_kind.replace("_", " ")} — '
                "adding key columns to an existing table is not supported in CQL."
                if unsafe
                else ""
            )
            diff.column_changes.append(
                ColumnChange(
                    name=col.name,
                    change_type="pk_change" if unsafe else "add",
                    model_type=col.cql_type,
                    model_kind=desired_kind,
                    unsafe=unsafe,
                    warning=warning,
                )
            )

    # --- Columns in DB but not in model → DROP (destructive) ---
    for db_col in db_columns:
        if db_col.name not in model_by_name:
            diff.column_changes.append(
                ColumnChange(
                    name=db_col.name,
                    change_type="drop",
                    db_type=db_col.cql_type,
                    db_kind=db_col.kind,
                    unsafe=False,
                    warning="",
                )
            )

    # --- Columns in both — check for type and key-role changes ---
    for col in model_columns:
        if col.name not in db_by_name:
            continue
        db_col = db_by_name[col.name]
        desired_kind = _model_kind(col)
        kind_changed = db_col.kind != desired_kind

        if kind_changed:
            # PK/CK role changed — impossible in CQL
            diff.column_changes.append(
                ColumnChange(
                    name=col.name,
                    change_type="pk_change",
                    db_type=db_col.cql_type,
                    model_type=col.cql_type,
                    db_kind=db_col.kind,
                    model_kind=desired_kind,
                    unsafe=True,
                    warning=(
                        f'Column "{col.name}" key role changed from '
                        f"{db_col.kind!r} to {desired_kind!r}. "
                        "Changing primary/clustering key columns is not supported in CQL."
                    ),
                )
            )
        elif db_col.cql_type != col.cql_type:
            # Type changed
            safe = (db_col.cql_type, col.cql_type) in _SAFE_WIDENING
            diff.column_changes.append(
                ColumnChange(
                    name=col.name,
                    change_type="type_change",
                    db_type=db_col.cql_type,
                    model_type=col.cql_type,
                    db_kind=db_col.kind,
                    model_kind=desired_kind,
                    unsafe=not safe,
                    warning=(
                        ""
                        if safe
                        else (
                            f'Column "{col.name}" type change from '
                            f"{db_col.cql_type!r} to {col.cql_type!r} "
                            "is not a safe widening and may not be supported."
                        )
                    ),
                )
            )

    # --- Index changes ---
    model_indexes: dict[str, str] = {}  # index_name → column_name
    for col in model_columns:
        if col.index:
            idx_name = col.index_name or f"{schema_name(table)}_{col.name}_idx"
            model_indexes[idx_name] = col.name
    model_index_names = {schema_name(n) for n in model_indexes}

    for idx_name, col_name in model_indexes.items():
        if schema_name(idx_name) not in db_indexes:
            diff.index_changes.append(IndexChange(index_name=idx_name, change_type="add", column_name=col_name))

    for idx_name in db_indexes:
        if idx_name not in model_index_names:
            diff.index_changes.append(IndexChange(index_name=idx_name, change_type="drop", column_name=""))

    return diff


# ---------------------------------------------------------------------------
# C.3 — Migration file rendering
# ---------------------------------------------------------------------------


def _indent(text: str, prefix: str) -> str:
    """Indent every non-empty line of *text* with *prefix*."""
    return "\n".join(prefix + line if line.strip() else line for line in text.splitlines())


def render_migration(diff: SchemaDiff, description: str) -> str:
    """Generate the Python source for a migration file from a :class:`SchemaDiff`.

    The generated file always defines a ``ForwardMigration(Migration)`` class
    with ``upgrade()`` and ``downgrade()`` methods.  Unsafe or unsupported
    operations are flagged with ``# TODO`` and ``# WARNING`` comments.
    """
    ks = diff.keyspace
    tbl = diff.table

    upgrade_lines: list[str] = []
    downgrade_lines: list[str] = []
    allow_destructive = diff.has_destructive_changes

    if not diff.table_exists:
        # Table doesn't exist — emit a placeholder comment
        upgrade_lines.append(f"# TODO: Table {ks}.{tbl} does not exist in the database.")
        upgrade_lines.append("# Run Document.sync_table() to create it, or add a CREATE TABLE statement here.")
        downgrade_lines.append(f"# await ctx.execute('DROP TABLE IF EXISTS {ks}.{tbl}')")
    else:
        for change in diff.column_changes:
            if change.change_type == "add":
                cql = f'ALTER TABLE {qualified_name(ks, tbl)} ADD "{change.name}" {change.model_type}'
                upgrade_lines.append(f"await ctx.execute({cql!r})")
                drop_cql = f'ALTER TABLE {qualified_name(ks, tbl)} DROP "{change.name}"'
                downgrade_lines.append(f"await ctx.execute({drop_cql!r})")

            elif change.change_type == "drop":
                cql = f'ALTER TABLE {qualified_name(ks, tbl)} DROP "{change.name}"'
                upgrade_lines.append(f'# Destructive: drops column "{change.name}" ({change.db_type})')
                upgrade_lines.append(f"await ctx.execute({cql!r})")
                add_cql = f'ALTER TABLE {qualified_name(ks, tbl)} ADD "{change.name}" {change.db_type}'
                downgrade_lines.append(f"await ctx.execute({add_cql!r})")

            elif change.change_type == "type_change":
                if change.unsafe:
                    upgrade_lines.append(f'# TODO: Unsafe type change for column "{change.name}"')
                    upgrade_lines.append(f"# WARNING: {change.warning}")
                    upgrade_lines.append(f"# Current DB type: {change.db_type!r}  →  desired: {change.model_type!r}")
                    upgrade_lines.append("# Consider a data migration or create a new table.")
                else:
                    # Safe widening — Cassandra 3.x+ allows some type alterations
                    cql = f'ALTER TABLE {qualified_name(ks, tbl)} ALTER "{change.name}" TYPE {change.model_type}'
                    upgrade_lines.append(f"await ctx.execute({cql!r})")
                    rev_cql = f'ALTER TABLE {qualified_name(ks, tbl)} ALTER "{change.name}" TYPE {change.db_type}'
                    downgrade_lines.append(f"await ctx.execute({rev_cql!r})")

            elif change.change_type == "pk_change":
                upgrade_lines.append(f'# TODO: Primary/clustering key change for column "{change.name}"')
                upgrade_lines.append(f"# WARNING: {change.warning}")
                upgrade_lines.append("# Primary key columns cannot be added, removed, or reordered in CQL.")
                upgrade_lines.append("# You must create a new table, migrate the data, and rename.")
                downgrade_lines.append(f'# TODO: Reverse the table-copy migration for "{change.name}"')

        for idx_change in diff.index_changes:
            if idx_change.change_type == "add":
                cql = f'CREATE INDEX IF NOT EXISTS {quote_ident(idx_change.index_name)} ON {qualified_name(ks, tbl)} ("{idx_change.column_name}")'
                upgrade_lines.append(f"await ctx.execute({cql!r})")
                drop_idx_cql = f"DROP INDEX IF EXISTS {qualified_name(ks, idx_change.index_name)}"
                downgrade_lines.append(f"await ctx.execute({drop_idx_cql!r})")
            else:
                cql = f"DROP INDEX IF EXISTS {qualified_name(ks, idx_change.index_name)}"
                upgrade_lines.append(f"# Destructive: drops index {idx_change.index_name!r}")
                upgrade_lines.append(f"await ctx.execute({cql!r})")
                # Can't easily reconstruct the index — leave a TODO
                downgrade_lines.append(f"# TODO: recreate index {idx_change.index_name!r} if needed")

    if not upgrade_lines:
        upgrade_lines.append("pass  # no changes detected")
    if not downgrade_lines:
        downgrade_lines.append("pass  # no changes to reverse")

    upgrade_body = _indent("\n".join(upgrade_lines), "        ")
    downgrade_body = _indent("\n".join(downgrade_lines), "        ")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    safe_desc = description.replace('"', '\\"')

    return textwrap.dedent(f'''\
        # Auto-generated by coodie makemigration on {timestamp}
        from coodie.migrations import Migration


        class ForwardMigration(Migration):
            description = "{safe_desc}"
            allow_destructive = {allow_destructive!s}

            async def upgrade(self, ctx: "MigrationContext") -> None:
        {upgrade_body}

            async def downgrade(self, ctx: "MigrationContext") -> None:
        {downgrade_body}
        ''')


# ---------------------------------------------------------------------------
# Filename helpers
# ---------------------------------------------------------------------------


def next_migration_filename(migrations_dir: Path, description: str) -> str:
    """Return the filename (without directory) for the next migration.

    Finds the highest existing ``NNN`` sequence number across all migration
    files in *migrations_dir* and returns ``YYYYMMDD_{NNN+1:03d}_{slug}.py``.

    Parameters
    ----------
    migrations_dir:
        Directory containing existing migration files.
    description:
        Human-readable description; converted to a safe filename slug.
    """
    from coodie.migrations.runner import discover_migrations

    max_seq = 0
    for info in discover_migrations(migrations_dir):
        # sort_key is "YYYYMMDD_NNN"
        parts = info.sort_key.split("_")
        if len(parts) >= 2:
            try:
                seq = int(parts[1])
                max_seq = max(max_seq, seq)
            except ValueError:
                pass

    next_seq = max_seq + 1
    date_str = datetime.now().strftime("%Y%m%d")  # noqa: DTZ005 - local date is intended for filenames
    slug = re.sub(r"[^a-z0-9]+", "_", description.lower()).strip("_") or "migration"
    return f"{date_str}_{next_seq:03d}_{slug}.py"


# ---------------------------------------------------------------------------
# Human-readable diff summary
# ---------------------------------------------------------------------------


def format_diff(diff: SchemaDiff) -> str:
    """Return a human-readable multi-line summary of *diff*."""
    lines: list[str] = []
    lines.append(f"Schema diff for {diff.keyspace}.{diff.table}:")

    if not diff.table_exists:
        lines.append("  Table does not exist in the database.")
        return "\n".join(lines)

    if diff.is_empty:
        lines.append("  No changes detected.")
        return "\n".join(lines)

    for change in diff.column_changes:
        if change.change_type == "add":
            lines.append(f'  [+] ADD column "{change.name}" {change.model_type}')
        elif change.change_type == "drop":
            lines.append(f'  [-] DROP column "{change.name}" ({change.db_type})')
        elif change.change_type == "type_change":
            marker = "[!]" if change.unsafe else "[~]"
            lines.append(f'  {marker} TYPE CHANGE "{change.name}": {change.db_type} → {change.model_type}')
            if change.unsafe:
                lines.append(f"      WARNING: {change.warning}")
        elif change.change_type == "pk_change":
            lines.append(f'  [!] UNSAFE: "{change.name}" — {change.warning}')

    for idx_change in diff.index_changes:
        if idx_change.change_type == "add":
            lines.append(f'  [+] CREATE INDEX {idx_change.index_name} ON "{idx_change.column_name}"')
        else:
            lines.append(f"  [-] DROP INDEX {idx_change.index_name}")

    return "\n".join(lines)
