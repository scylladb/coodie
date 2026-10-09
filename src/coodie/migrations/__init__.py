"""coodie migration framework — production-grade schema evolution for Cassandra/ScyllaDB.

Provides:

- :class:`Migration` — base class for migration files with ``upgrade`` / ``downgrade``
- :class:`MigrationContext` — execution context passed to migration methods
- :func:`discover_migrations` — find and order migration files in a directory
- :class:`MigrationRunner` — apply, rollback, and track migrations
"""

from __future__ import annotations

from coodie.migrations.autogen import (
    ColumnChange,
    DbColumnInfo,
    IndexChange,
    SchemaDiff,
    diff_schema,
    format_diff,
    introspect_table,
    next_migration_filename,
    render_migration,
)
from coodie.migrations.base import Migration, MigrationContext
from coodie.migrations.runner import MigrationRunner, discover_migrations

__all__ = [
    "ColumnChange",
    "DbColumnInfo",
    "IndexChange",
    "Migration",
    "MigrationContext",
    "MigrationRunner",
    "SchemaDiff",
    "diff_schema",
    "discover_migrations",
    "format_diff",
    "introspect_table",
    "next_migration_filename",
    "render_migration",
]
