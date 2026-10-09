"""``coodie`` CLI — migration management, auto-generation, and schema diff.

Usage::

    coodie migrate                          # apply all pending migrations
    coodie migrate --dry-run                # show planned CQL without applying
    coodie migrate --target 20260203_002    # apply up to a specific migration
    coodie migrate --rollback --steps 1    # rollback the last migration
    coodie migrate --status                 # show migration status (with checksum validation)

    coodie makemigration --name <description> \\
        --keyspace <ks> --module <app.models>  # auto-generate a migration file

    coodie schema-diff --keyspace <ks> \\
        --module <app.models>               # show diff without creating a file
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Any


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="coodie",
        description="coodie migration management CLI",
    )
    sub = parser.add_subparsers(dest="command")

    # ------------------------------------------------------------------
    # migrate
    # ------------------------------------------------------------------
    migrate = sub.add_parser("migrate", help="Apply or manage migrations")
    migrate.add_argument(
        "--hosts",
        nargs="+",
        default=["127.0.0.1"],
        help="Cassandra/ScyllaDB contact points (default: 127.0.0.1)",
    )
    migrate.add_argument(
        "--keyspace",
        required=True,
        help="Target keyspace",
    )
    migrate.add_argument(
        "--migrations-dir",
        default="migrations",
        help="Path to migration files directory (default: migrations)",
    )
    migrate.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned CQL without executing",
    )
    migrate.add_argument(
        "--status",
        action="store_true",
        help="Show migration status",
    )
    migrate.add_argument(
        "--rollback",
        action="store_true",
        help="Rollback migrations",
    )
    migrate.add_argument(
        "--steps",
        type=int,
        default=1,
        help="Number of migrations to rollback (default: 1)",
    )
    migrate.add_argument(
        "--target",
        type=str,
        default=None,
        help="Stop after applying migration matching this prefix",
    )
    migrate.add_argument(
        "--driver-type",
        default="scylla",
        choices=["scylla", "cassandra"],
        help="Driver type (default: scylla)",
    )

    # ------------------------------------------------------------------
    # makemigration  (C.3)
    # ------------------------------------------------------------------
    makemig = sub.add_parser(
        "makemigration",
        help="Auto-generate a migration file by diffing the live DB against model classes",
    )
    makemig.add_argument(
        "--name",
        required=True,
        help="Short description for the migration (used in filename and description)",
    )
    makemig.add_argument(
        "--hosts",
        nargs="+",
        default=["127.0.0.1"],
        help="Cassandra/ScyllaDB contact points (default: 127.0.0.1)",
    )
    makemig.add_argument(
        "--keyspace",
        required=True,
        help="Target keyspace",
    )
    makemig.add_argument(
        "--module",
        required=True,
        help="Python module path containing Document subclasses (e.g. myapp.models)",
    )
    makemig.add_argument(
        "--migrations-dir",
        default="migrations",
        help="Directory where the migration file will be written (default: migrations)",
    )
    makemig.add_argument(
        "--driver-type",
        default="scylla",
        choices=["scylla", "cassandra"],
        help="Driver type (default: scylla)",
    )

    # ------------------------------------------------------------------
    # schema-diff  (C.3 / companion command)
    # ------------------------------------------------------------------
    sdiff = sub.add_parser(
        "schema-diff",
        help="Show the diff between the live DB and Document class definitions (no file written)",
    )
    sdiff.add_argument(
        "--hosts",
        nargs="+",
        default=["127.0.0.1"],
        help="Cassandra/ScyllaDB contact points (default: 127.0.0.1)",
    )
    sdiff.add_argument(
        "--keyspace",
        required=True,
        help="Target keyspace",
    )
    sdiff.add_argument(
        "--module",
        required=True,
        help="Python module path containing Document subclasses (e.g. myapp.models)",
    )
    sdiff.add_argument(
        "--driver-type",
        default="scylla",
        choices=["scylla", "cassandra"],
        help="Driver type (default: scylla)",
    )

    return parser


# ---------------------------------------------------------------------------
# migrate subcommand
# ---------------------------------------------------------------------------


async def _run_migrate(args: argparse.Namespace) -> int:
    """Execute the ``migrate`` subcommand."""
    from coodie.drivers import init_coodie
    from coodie.migrations.runner import MigrationRunner

    driver = init_coodie(
        hosts=args.hosts,
        keyspace=args.keyspace,
        driver_type=args.driver_type,
    )

    runner = MigrationRunner(
        driver=driver,
        keyspace=args.keyspace,
        migrations_dir=args.migrations_dir,
    )

    try:
        if args.status:
            return await _show_status(runner)
        elif args.rollback:
            return await _do_rollback(runner, steps=args.steps, dry_run=args.dry_run)
        else:
            return await _do_apply(runner, dry_run=args.dry_run, target=args.target)
    finally:
        driver.close()


async def _show_status(runner: Any) -> int:
    from coodie.migrations.base import Migration
    from coodie.migrations.runner import discover_migrations

    statuses = await runner.status()
    if not statuses:
        print("No migrations found.")
        return 0

    applied_map = await runner.get_applied()

    print(f"{'Status':<10} {'Migration':<50} {'Applied At':<28} {'Checksum'}")
    print("-" * 110)
    exit_code = 0
    for s in statuses:
        marker = "[x]" if s["applied"] else "[ ]"
        applied_at = str(s["applied_at"] or "")

        # C.5 — Checksum validation for applied migrations
        checksum_note = ""
        if s["applied"]:
            info = applied_map.get(s["name"])
            stored_checksum = info["checksum"] if info else None
            all_infos = discover_migrations(runner._migrations_dir)
            file_info = next((m for m in all_infos if m.name == s["name"]), None)
            if file_info and stored_checksum:
                current_checksum = Migration.compute_checksum(file_info.path)
                if current_checksum != stored_checksum:
                    checksum_note = " [CHECKSUM MISMATCH]"
                    exit_code = 1

        print(f"{marker:<10} {s['name']:<50} {applied_at:<28}{checksum_note}")
    return exit_code


async def _do_apply(runner: Any, *, dry_run: bool, target: str | None) -> int:
    results = await runner.apply(dry_run=dry_run, target=target)
    if not results:
        print("No pending migrations.")
        return 0

    prefix = "[DRY RUN] " if dry_run else ""
    for r in results:
        print(f"{prefix}Applied: {r['name']}")
        if r["description"]:
            print(f"  {r['description']}")
        if dry_run and r["planned_cql"]:
            print("  Planned CQL:")
            for cql in r["planned_cql"]:
                print(f"    {cql}")
    return 0


async def _do_rollback(runner: Any, *, steps: int, dry_run: bool) -> int:
    results = await runner.rollback(steps=steps, dry_run=dry_run)
    if not results:
        print("No migrations to roll back.")
        return 0

    prefix = "[DRY RUN] " if dry_run else ""
    for r in results:
        print(f"{prefix}Rolled back: {r['name']}")
        if r["description"]:
            print(f"  {r['description']}")
        if dry_run and r["planned_cql"]:
            print("  Planned CQL:")
            for cql in r["planned_cql"]:
                print(f"    {cql}")
    return 0


# ---------------------------------------------------------------------------
# makemigration / schema-diff shared helpers
# ---------------------------------------------------------------------------


def _load_document_classes(module_path: str, keyspace: str) -> list[Any]:
    """Import *module_path* and return all concrete Document subclasses."""
    import importlib

    mod = importlib.import_module(module_path)

    from coodie.aio.document import Document as AioDocument
    from coodie.sync.document import Document as SyncDocument

    candidates: list[Any] = []
    for name in dir(mod):
        obj = getattr(mod, name)
        if not (isinstance(obj, type) and (issubclass(obj, AioDocument) or issubclass(obj, SyncDocument))):
            continue
        if obj is AioDocument or obj is SyncDocument:
            continue
        settings = getattr(obj, "Settings", None)
        if settings and getattr(settings, "__abstract__", False):
            continue
        candidates.append(obj)

    return candidates


async def _run_diff_for_classes(
    driver: Any,
    keyspace: str,
    doc_classes: list[Any],
) -> list[Any]:
    """Return a list of :class:`SchemaDiff` objects, one per document class."""
    from coodie.migrations.autogen import diff_schema, introspect_table
    from coodie.schema import build_schema

    diffs = []
    for cls in doc_classes:
        table = cls._get_table()
        schema = build_schema(cls)
        table_exists, db_columns, db_indexes = await introspect_table(driver, keyspace, table)
        d = diff_schema(keyspace, table, db_columns, schema, db_indexes, table_exists)
        diffs.append(d)
    return diffs


# ---------------------------------------------------------------------------
# makemigration subcommand
# ---------------------------------------------------------------------------


async def _run_makemigration(args: argparse.Namespace) -> int:
    """Execute the ``makemigration`` subcommand."""
    from coodie.drivers import init_coodie
    from coodie.migrations.autogen import (
        format_diff,
        next_migration_filename,
        render_migration,
    )

    driver = init_coodie(
        hosts=args.hosts,
        keyspace=args.keyspace,
        driver_type=args.driver_type,
    )

    try:
        doc_classes = _load_document_classes(args.module, args.keyspace)
        if not doc_classes:
            print(f"No Document subclasses found in module {args.module!r}.")
            return 1

        diffs = await _run_diff_for_classes(driver, args.keyspace, doc_classes)
    finally:
        driver.close()

    # Print summary of detected changes
    any_changes = False
    for diff in diffs:
        summary = format_diff(diff)
        print(summary)
        if not diff.is_empty or not diff.table_exists:
            any_changes = True

    if not any_changes:
        print("No schema changes detected. Migration file not created.")
        return 0

    # Ensure migrations directory exists
    migrations_dir = Path(args.migrations_dir)
    migrations_dir.mkdir(parents=True, exist_ok=True)

    filename = next_migration_filename(migrations_dir, args.name)
    output_path = migrations_dir / filename

    if len(diffs) == 1:
        source = render_migration(diffs[0], args.name)
    else:
        source = _render_combined_migration(diffs, args.name)

    output_path.write_text(source, encoding="utf-8")
    print(f"\nCreated migration file: {output_path}")

    if any(d.has_unsafe_changes for d in diffs):
        print(
            "\nWARNING: The migration contains unsafe or unsupported operations. "
            "Review the generated file and resolve all TODO comments before applying."
        )
        return 2

    return 0


def _render_combined_migration(diffs: list[Any], description: str) -> str:
    """Render a single migration file covering changes from multiple diffs."""
    import textwrap
    from datetime import datetime, timezone

    from coodie.migrations.autogen import render_migration

    upgrade_parts: list[str] = []
    downgrade_parts: list[str] = []

    for diff in diffs:
        single = render_migration(diff, description)
        upgrade_parts.append(f"# --- {diff.keyspace}.{diff.table} ---")
        downgrade_parts.append(f"# --- {diff.keyspace}.{diff.table} ---")

        lines = single.splitlines()
        in_upgrade = False
        in_downgrade = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("async def upgrade"):
                in_upgrade = True
                in_downgrade = False
                continue
            if stripped.startswith("async def downgrade"):
                in_upgrade = False
                in_downgrade = True
                continue
            if in_upgrade:
                upgrade_parts.append(line[8:] if line.startswith("        ") else line.lstrip())
            if in_downgrade and stripped:
                downgrade_parts.append(line[8:] if line.startswith("        ") else line.lstrip())

    allow_destructive = any(d.has_destructive_changes for d in diffs)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    safe_desc = description.replace('"', '\\"')
    upgrade_body = textwrap.indent("\n".join(upgrade_parts) or "pass", "        ")
    downgrade_body = textwrap.indent("\n".join(downgrade_parts) or "pass", "        ")

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
# schema-diff subcommand
# ---------------------------------------------------------------------------


async def _run_schema_diff(args: argparse.Namespace) -> int:
    """Execute the ``schema-diff`` subcommand."""
    from coodie.drivers import init_coodie
    from coodie.migrations.autogen import format_diff

    driver = init_coodie(
        hosts=args.hosts,
        keyspace=args.keyspace,
        driver_type=args.driver_type,
    )

    try:
        doc_classes = _load_document_classes(args.module, args.keyspace)
        if not doc_classes:
            print(f"No Document subclasses found in module {args.module!r}.")
            return 1

        diffs = await _run_diff_for_classes(driver, args.keyspace, doc_classes)
    finally:
        driver.close()

    any_changes = False
    for diff in diffs:
        print(format_diff(diff))
        if not diff.is_empty or not diff.table_exists:
            any_changes = True

    if not any_changes:
        print("No schema changes detected.")

    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``coodie`` CLI."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    if args.command == "migrate":
        return asyncio.run(_run_migrate(args))

    if args.command == "makemigration":
        return asyncio.run(_run_makemigration(args))

    if args.command == "schema-diff":
        return asyncio.run(_run_schema_diff(args))

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
