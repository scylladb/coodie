"""Unit tests for coodie.migrations.autogen (Phase C)."""

from __future__ import annotations

import textwrap
from unittest.mock import AsyncMock, MagicMock

import pytest

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
from coodie.schema import ColumnDefinition

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_db_col(
    name: str,
    cql_type: str = "text",
    kind: str = "regular",
    position: int = 0,
    clustering_order: str = "ASC",
) -> DbColumnInfo:
    return DbColumnInfo(
        name=name,
        cql_type=cql_type,
        kind=kind,
        position=position,
        clustering_order=clustering_order,
    )


def _make_model_col(
    name: str,
    cql_type: str = "text",
    primary_key: bool = False,
    clustering_key: bool = False,
    index: bool = False,
    index_name: str | None = None,
    static: bool = False,
) -> ColumnDefinition:
    return ColumnDefinition(
        name=name,
        cql_type=cql_type,
        primary_key=primary_key,
        clustering_key=clustering_key,
        index=index,
        index_name=index_name,
        static=static,
    )


# ---------------------------------------------------------------------------
# C.1 — introspect_table
# ---------------------------------------------------------------------------


class TestIntrospectTable:
    async def test_table_not_found(self):
        driver = AsyncMock()
        driver.execute_async.return_value = []
        exists, cols, indexes = await introspect_table(driver, "ks", "tbl")
        assert exists is False
        assert cols == []
        assert indexes == set()

    async def test_table_found_with_columns(self):
        driver = AsyncMock()
        driver.execute_async.side_effect = [
            [{"table_name": "tbl"}],  # system_schema.tables
            [
                {
                    "column_name": "id",
                    "type": "uuid",
                    "kind": "partition_key",
                    "position": 0,
                    "clustering_order": "ASC",
                },
                {
                    "column_name": "name",
                    "type": "text",
                    "kind": "regular",
                    "position": -1,
                    "clustering_order": "ASC",
                },
            ],
            [],  # system_schema.indexes
        ]
        exists, cols, indexes = await introspect_table(driver, "ks", "tbl")
        assert exists is True
        assert len(cols) == 2
        assert cols[0].name == "id"
        assert cols[0].cql_type == "uuid"
        assert cols[0].kind == "partition_key"
        assert cols[1].name == "name"
        assert indexes == set()

    async def test_table_found_with_indexes(self):
        driver = AsyncMock()
        driver.execute_async.side_effect = [
            [{"table_name": "tbl"}],
            [
                {
                    "column_name": "id",
                    "type": "uuid",
                    "kind": "partition_key",
                    "position": 0,
                    "clustering_order": "ASC",
                },
            ],
            [{"index_name": "tbl_name_idx"}],
        ]
        exists, _cols, indexes = await introspect_table(driver, "ks", "tbl")
        assert exists is True
        assert indexes == {"tbl_name_idx"}

    async def test_null_position_defaults_to_zero(self):
        driver = AsyncMock()
        driver.execute_async.side_effect = [
            [{"table_name": "tbl"}],
            [
                {
                    "column_name": "col",
                    "type": "text",
                    "kind": "regular",
                    "position": None,
                    "clustering_order": None,
                },
            ],
            [],
        ]
        _exists, cols, _indexes = await introspect_table(driver, "ks", "tbl")
        assert cols[0].position == 0
        assert cols[0].clustering_order == "ASC"


# ---------------------------------------------------------------------------
# C.2 — diff_schema
# ---------------------------------------------------------------------------


class TestDiffSchemaTableNotExists:
    def test_returns_empty_diff_when_table_missing(self):
        diff = diff_schema("ks", "tbl", [], [], set(), table_exists=False)
        assert diff.table_exists is False
        assert diff.is_empty
        assert not diff.has_unsafe_changes

    def test_no_column_changes_when_table_missing(self):
        model_cols = [_make_model_col("id", "uuid", primary_key=True)]
        diff = diff_schema("ks", "tbl", [], model_cols, set(), table_exists=False)
        # Table-not-exists case — no per-column diffs
        assert diff.column_changes == []
        assert diff.index_changes == []


class TestDiffSchemaAddColumns:
    def test_detects_new_column(self):
        db_cols = [_make_db_col("id", "uuid", kind="partition_key")]
        model_cols = [
            _make_model_col("id", "uuid", primary_key=True),
            _make_model_col("rating", "int"),
        ]
        diff = diff_schema("ks", "tbl", db_cols, model_cols, set(), table_exists=True)
        changes = [c for c in diff.column_changes if c.change_type == "add"]
        assert len(changes) == 1
        assert changes[0].name == "rating"
        assert changes[0].model_type == "int"
        assert not changes[0].unsafe

    def test_no_changes_when_schemas_match(self):
        db_cols = [
            _make_db_col("id", "uuid", kind="partition_key"),
            _make_db_col("name", "text"),
        ]
        model_cols = [
            _make_model_col("id", "uuid", primary_key=True),
            _make_model_col("name", "text"),
        ]
        diff = diff_schema("ks", "tbl", db_cols, model_cols, set(), table_exists=True)
        assert diff.is_empty

    def test_adding_pk_column_is_unsafe(self):
        db_cols = [_make_db_col("id", "uuid", kind="partition_key")]
        model_cols = [
            _make_model_col("id", "uuid", primary_key=True),
            _make_model_col("tenant", "text", primary_key=True),
        ]
        diff = diff_schema("ks", "tbl", db_cols, model_cols, set(), table_exists=True)
        unsafe = [c for c in diff.column_changes if c.unsafe]
        assert len(unsafe) == 1
        assert unsafe[0].name == "tenant"
        assert diff.has_unsafe_changes


class TestDiffSchemaDropColumns:
    def test_detects_dropped_column(self):
        db_cols = [
            _make_db_col("id", "uuid", kind="partition_key"),
            _make_db_col("old_col", "text"),
        ]
        model_cols = [_make_model_col("id", "uuid", primary_key=True)]
        diff = diff_schema("ks", "tbl", db_cols, model_cols, set(), table_exists=True)
        drops = [c for c in diff.column_changes if c.change_type == "drop"]
        assert len(drops) == 1
        assert drops[0].name == "old_col"
        assert drops[0].db_type == "text"
        assert diff.has_destructive_changes

    def test_drop_is_not_marked_unsafe(self):
        db_cols = [
            _make_db_col("id", "uuid", kind="partition_key"),
            _make_db_col("junk", "text"),
        ]
        model_cols = [_make_model_col("id", "uuid", primary_key=True)]
        diff = diff_schema("ks", "tbl", db_cols, model_cols, set(), table_exists=True)
        drop = diff.column_changes[0]
        assert not drop.unsafe  # DROP is destructive but not "impossible"


class TestDiffSchemaTypeChanges:
    def test_safe_widening_not_marked_unsafe(self):
        db_cols = [
            _make_db_col("id", "uuid", kind="partition_key"),
            _make_db_col("score", "int"),
        ]
        model_cols = [
            _make_model_col("id", "uuid", primary_key=True),
            _make_model_col("score", "bigint"),
        ]
        diff = diff_schema("ks", "tbl", db_cols, model_cols, set(), table_exists=True)
        changes = [c for c in diff.column_changes if c.change_type == "type_change"]
        assert len(changes) == 1
        assert changes[0].name == "score"
        assert not changes[0].unsafe

    def test_unsafe_type_change_marked_unsafe(self):
        db_cols = [
            _make_db_col("id", "uuid", kind="partition_key"),
            _make_db_col("score", "text"),
        ]
        model_cols = [
            _make_model_col("id", "uuid", primary_key=True),
            _make_model_col("score", "int"),
        ]
        diff = diff_schema("ks", "tbl", db_cols, model_cols, set(), table_exists=True)
        changes = [c for c in diff.column_changes if c.change_type == "type_change"]
        assert len(changes) == 1
        assert changes[0].unsafe
        assert changes[0].warning


class TestDiffSchemaPkChanges:
    def test_role_change_is_pk_change(self):
        # column was regular, now PK
        db_cols = [
            _make_db_col("id", "uuid", kind="partition_key"),
            _make_db_col("tenant", "text", kind="regular"),
        ]
        model_cols = [
            _make_model_col("id", "uuid", primary_key=True),
            _make_model_col("tenant", "text", primary_key=True),
        ]
        diff = diff_schema("ks", "tbl", db_cols, model_cols, set(), table_exists=True)
        pk_changes = [c for c in diff.column_changes if c.change_type == "pk_change"]
        assert len(pk_changes) == 1
        assert pk_changes[0].name == "tenant"
        assert pk_changes[0].unsafe
        assert diff.has_unsafe_changes


class TestDiffSchemaIndexChanges:
    def test_detects_new_index(self):
        db_cols = [
            _make_db_col("id", "uuid", kind="partition_key"),
            _make_db_col("email", "text"),
        ]
        model_cols = [
            _make_model_col("id", "uuid", primary_key=True),
            _make_model_col("email", "text", index=True, index_name="users_email_idx"),
        ]
        diff = diff_schema("ks", "users", db_cols, model_cols, set(), table_exists=True)
        adds = [c for c in diff.index_changes if c.change_type == "add"]
        assert len(adds) == 1
        assert adds[0].index_name == "users_email_idx"

    def test_detects_dropped_index(self):
        db_cols = [_make_db_col("id", "uuid", kind="partition_key")]
        model_cols = [_make_model_col("id", "uuid", primary_key=True)]
        diff = diff_schema("ks", "tbl", db_cols, model_cols, {"old_idx"}, table_exists=True)
        drops = [c for c in diff.index_changes if c.change_type == "drop"]
        assert len(drops) == 1
        assert drops[0].index_name == "old_idx"
        assert diff.has_destructive_changes

    def test_no_index_changes_when_indexes_match(self):
        db_cols = [
            _make_db_col("id", "uuid", kind="partition_key"),
            _make_db_col("email", "text"),
        ]
        model_cols = [
            _make_model_col("id", "uuid", primary_key=True),
            _make_model_col("email", "text", index=True, index_name="tbl_email_idx"),
        ]
        diff = diff_schema("ks", "tbl", db_cols, model_cols, {"tbl_email_idx"}, table_exists=True)
        assert diff.index_changes == []


# ---------------------------------------------------------------------------
# C.3 — render_migration
# ---------------------------------------------------------------------------


class TestRenderMigration:
    def test_add_column_generates_alter(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        diff.column_changes.append(ColumnChange(name="rating", change_type="add", model_type="int"))
        src = render_migration(diff, "add rating column")
        assert "ForwardMigration" in src
        assert "Migration" in src
        assert 'ALTER TABLE ks.tbl ADD "rating" int' in src
        assert 'ALTER TABLE ks.tbl DROP "rating"' in src

    def test_drop_column_generates_alter_with_comment(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        diff.column_changes.append(ColumnChange(name="old_col", change_type="drop", db_type="text"))
        src = render_migration(diff, "remove old_col")
        assert 'ALTER TABLE ks.tbl DROP "old_col"' in src
        assert "Destructive" in src
        assert "allow_destructive = True" in src

    def test_safe_type_change_generates_alter_type(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        diff.column_changes.append(
            ColumnChange(
                name="score",
                change_type="type_change",
                db_type="int",
                model_type="bigint",
                unsafe=False,
            )
        )
        src = render_migration(diff, "widen score")
        assert 'ALTER TABLE ks.tbl ALTER "score" TYPE bigint' in src

    def test_unsafe_type_change_generates_todo(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        diff.column_changes.append(
            ColumnChange(
                name="score",
                change_type="type_change",
                db_type="text",
                model_type="int",
                unsafe=True,
                warning="Not safe",
            )
        )
        src = render_migration(diff, "change score type")
        assert "TODO" in src
        assert "WARNING" in src
        # Should not generate an ALTER … TYPE statement
        assert 'ALTER TABLE ks.tbl ALTER "score"' not in src

    def test_pk_change_generates_todo(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        diff.column_changes.append(
            ColumnChange(
                name="tenant",
                change_type="pk_change",
                unsafe=True,
                warning="PK changes are not supported",
            )
        )
        src = render_migration(diff, "add tenant pk")
        assert "TODO" in src
        assert "WARNING" in src
        assert "Primary key" in src

    def test_no_changes_generates_pass(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        src = render_migration(diff, "empty")
        assert "pass" in src

    def test_table_not_exists_generates_todo(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=False)
        src = render_migration(diff, "create table")
        assert "TODO" in src
        assert "does not exist" in src

    def test_generated_file_is_importable(self, tmp_path):
        """The rendered source should be valid Python that defines ForwardMigration."""
        import importlib.util

        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        diff.column_changes.append(ColumnChange(name="rating", change_type="add", model_type="int"))
        src = render_migration(diff, "add rating")
        path = tmp_path / "20260101_001_add_rating.py"
        path.write_text(src)

        spec = importlib.util.spec_from_file_location("test_mig", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        assert hasattr(mod, "ForwardMigration")

    def test_index_add_generates_create_index(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        diff.index_changes.append(IndexChange(index_name="tbl_email_idx", change_type="add", column_name="email"))
        src = render_migration(diff, "add email index")
        assert "CREATE INDEX IF NOT EXISTS tbl_email_idx" in src

    def test_index_drop_generates_drop_index(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        diff.index_changes.append(IndexChange(index_name="old_idx", change_type="drop", column_name=""))
        src = render_migration(diff, "remove old index")
        assert "DROP INDEX IF EXISTS ks.old_idx" in src
        assert "allow_destructive = True" in src


# ---------------------------------------------------------------------------
# next_migration_filename
# ---------------------------------------------------------------------------


class TestNextMigrationFilename:
    def test_first_migration_is_001(self, tmp_path):
        name = next_migration_filename(tmp_path, "add rating")
        assert "_001_" in name
        assert name.endswith(".py")

    def test_increments_sequence(self, tmp_path):
        (tmp_path / "20260101_001_first.py").write_text("# m")
        (tmp_path / "20260102_002_second.py").write_text("# m")
        name = next_migration_filename(tmp_path, "third migration")
        assert "_003_" in name

    def test_description_slug_in_filename(self, tmp_path):
        name = next_migration_filename(tmp_path, "Add User Table")
        assert "add_user_table" in name

    def test_special_chars_stripped_from_slug(self, tmp_path):
        name = next_migration_filename(tmp_path, "Add column: foo/bar!")
        assert "/" not in name
        assert "!" not in name
        assert ":" not in name

    def test_nonexistent_dir_returns_001(self, tmp_path):
        name = next_migration_filename(tmp_path / "nonexistent", "test")
        assert "_001_" in name


# ---------------------------------------------------------------------------
# format_diff
# ---------------------------------------------------------------------------


class TestFormatDiff:
    def test_table_not_exists(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=False)
        out = format_diff(diff)
        assert "does not exist" in out

    def test_no_changes(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        out = format_diff(diff)
        assert "No changes detected" in out

    def test_add_shows_plus(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        diff.column_changes.append(ColumnChange(name="rating", change_type="add", model_type="int"))
        out = format_diff(diff)
        assert "[+]" in out
        assert "rating" in out

    def test_drop_shows_minus(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        diff.column_changes.append(ColumnChange(name="old", change_type="drop", db_type="text"))
        out = format_diff(diff)
        assert "[-]" in out

    def test_unsafe_shows_exclamation(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        diff.column_changes.append(
            ColumnChange(
                name="pk",
                change_type="pk_change",
                unsafe=True,
                warning="PK cannot change",
            )
        )
        out = format_diff(diff)
        assert "[!]" in out

    def test_safe_type_change_shows_tilde(self):
        diff = SchemaDiff(keyspace="ks", table="tbl", table_exists=True)
        diff.column_changes.append(
            ColumnChange(
                name="score",
                change_type="type_change",
                db_type="int",
                model_type="bigint",
                unsafe=False,
            )
        )
        out = format_diff(diff)
        assert "[~]" in out


# ---------------------------------------------------------------------------
# CLI parser — new subcommands
# ---------------------------------------------------------------------------


class TestCLIParserNewCommands:
    def test_makemigration_parses_all_flags(self):
        from coodie.migrations.cli import _build_parser

        parser = _build_parser()
        args = parser.parse_args(
            [
                "makemigration",
                "--name",
                "add rating column",
                "--keyspace",
                "test_ks",
                "--module",
                "myapp.models",
                "--migrations-dir",
                "/tmp/migrations",
            ]
        )
        assert args.command == "makemigration"
        assert args.name == "add rating column"
        assert args.keyspace == "test_ks"
        assert args.module == "myapp.models"
        assert args.migrations_dir == "/tmp/migrations"

    def test_makemigration_requires_name(self):
        from coodie.migrations.cli import _build_parser

        parser = _build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["makemigration", "--keyspace", "ks", "--module", "m"])

    def test_makemigration_requires_keyspace(self):
        from coodie.migrations.cli import _build_parser

        parser = _build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["makemigration", "--name", "n", "--module", "m"])

    def test_makemigration_requires_module(self):
        from coodie.migrations.cli import _build_parser

        parser = _build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["makemigration", "--name", "n", "--keyspace", "ks"])

    def test_schema_diff_parses_flags(self):
        from coodie.migrations.cli import _build_parser

        parser = _build_parser()
        args = parser.parse_args(
            [
                "schema-diff",
                "--keyspace",
                "test_ks",
                "--module",
                "myapp.models",
            ]
        )
        assert args.command == "schema-diff"
        assert args.keyspace == "test_ks"
        assert args.module == "myapp.models"

    def test_schema_diff_requires_keyspace(self):
        from coodie.migrations.cli import _build_parser

        parser = _build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["schema-diff", "--module", "m"])

    def test_schema_diff_requires_module(self):
        from coodie.migrations.cli import _build_parser

        parser = _build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["schema-diff", "--keyspace", "ks"])


# ---------------------------------------------------------------------------
# C.5 — Checksum validation in _show_status
# ---------------------------------------------------------------------------


class TestChecksumValidation:
    async def test_status_detects_checksum_mismatch(self, tmp_path, capsys):
        """_show_status should report [CHECKSUM MISMATCH] when a file changed."""
        from coodie.migrations.cli import _show_status

        # Write a migration file to disk
        mig_file = tmp_path / "20260101_001_test.py"
        mig_file.write_text(
            textwrap.dedent("""\
            from coodie.migrations import Migration
            class ForwardMigration(Migration):
                description = "test"
                async def upgrade(self, ctx): pass
        """)
        )

        # Compute the checksum of the *original* content
        from coodie.migrations.base import Migration

        original_checksum = Migration.compute_checksum(mig_file)

        # Tamper with the file
        mig_file.write_text("# tampered\n" + mig_file.read_text())
        tampered_checksum = Migration.compute_checksum(mig_file)
        assert original_checksum != tampered_checksum

        runner = MagicMock()
        runner._migrations_dir = tmp_path
        runner.status = AsyncMock(
            return_value=[
                {
                    "name": "20260101_001_test",
                    "applied": True,
                    "applied_at": "2026-01-01T00:00:00",
                    "description": "test",
                }
            ]
        )
        runner.get_applied = AsyncMock(
            return_value={
                "20260101_001_test": {
                    "checksum": original_checksum,  # stored old checksum
                    "applied_at": "2026-01-01T00:00:00",
                    "description": "test",
                }
            }
        )

        exit_code = await _show_status(runner)
        captured = capsys.readouterr()
        assert "CHECKSUM MISMATCH" in captured.out
        assert exit_code == 1

    async def test_status_ok_when_checksums_match(self, tmp_path, capsys):
        from coodie.migrations.cli import _show_status

        mig_file = tmp_path / "20260101_001_test.py"
        mig_file.write_text(
            textwrap.dedent("""\
            from coodie.migrations import Migration
            class ForwardMigration(Migration):
                description = "test"
                async def upgrade(self, ctx): pass
        """)
        )

        from coodie.migrations.base import Migration

        checksum = Migration.compute_checksum(mig_file)

        runner = MagicMock()
        runner._migrations_dir = tmp_path
        runner.status = AsyncMock(
            return_value=[
                {
                    "name": "20260101_001_test",
                    "applied": True,
                    "applied_at": "2026-01-01T00:00:00",
                    "description": "test",
                }
            ]
        )
        runner.get_applied = AsyncMock(
            return_value={
                "20260101_001_test": {
                    "checksum": checksum,
                    "applied_at": "2026-01-01T00:00:00",
                    "description": "test",
                }
            }
        )

        exit_code = await _show_status(runner)
        captured = capsys.readouterr()
        assert "CHECKSUM MISMATCH" not in captured.out
        assert exit_code == 0
