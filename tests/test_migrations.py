"""Unit tests for the coodie.migrations module (Phase B)."""

from __future__ import annotations

import textwrap
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from coodie.exceptions import MigrationError
from coodie.migrations.base import Migration, MigrationContext
from coodie.migrations.runner import (
    MigrationInfo,
    MigrationRunner,
    _load_migration_class,
    discover_migrations,
)

# ---------------------------------------------------------------------------
# Migration base class tests
# ---------------------------------------------------------------------------


class TestMigration:
    def test_default_attributes(self):
        m = Migration()
        assert m.description == ""
        assert m.allow_destructive is False
        assert m.reversible is True

    async def test_upgrade_raises_not_implemented(self):
        m = Migration()
        ctx = MigrationContext(driver=None, dry_run=True)
        with pytest.raises(NotImplementedError, match="upgrade"):
            await m.upgrade(ctx)

    async def test_downgrade_raises_not_implemented(self):
        m = Migration()
        ctx = MigrationContext(driver=None, dry_run=True)
        with pytest.raises(NotImplementedError, match="downgrade"):
            await m.downgrade(ctx)

    def test_compute_checksum(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("hello")
        checksum = Migration.compute_checksum(f)
        assert isinstance(checksum, str)
        assert len(checksum) == 64  # SHA-256

    def test_checksum_changes_with_content(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("hello")
        c1 = Migration.compute_checksum(f)
        f.write_text("world")
        c2 = Migration.compute_checksum(f)
        assert c1 != c2


# ---------------------------------------------------------------------------
# MigrationContext tests
# ---------------------------------------------------------------------------


class TestMigrationContext:
    async def test_dry_run_does_not_call_driver(self):
        driver = AsyncMock()
        ctx = MigrationContext(driver, dry_run=True)
        result = await ctx.execute("CREATE TABLE test (id int PRIMARY KEY)")
        assert result == []
        driver.execute_async.assert_not_called()
        assert ctx.planned_cql == ["CREATE TABLE test (id int PRIMARY KEY)"]

    async def test_execute_calls_driver(self):
        driver = AsyncMock()
        driver.execute_async.return_value = [{"count": 1}]
        ctx = MigrationContext(driver, dry_run=False)
        result = await ctx.execute("SELECT count(*) FROM test", [])
        assert result == [{"count": 1}]
        driver.execute_async.assert_called_once_with("SELECT count(*) FROM test", [])

    async def test_planned_cql_records_all_statements(self):
        driver = AsyncMock()
        driver.execute_async.return_value = []
        ctx = MigrationContext(driver, dry_run=False)
        await ctx.execute("stmt1")
        await ctx.execute("stmt2")
        assert ctx.planned_cql == ["stmt1", "stmt2"]

    async def test_execute_default_params(self):
        driver = AsyncMock()
        driver.execute_async.return_value = []
        ctx = MigrationContext(driver, dry_run=False)
        await ctx.execute("stmt1")
        driver.execute_async.assert_called_once_with("stmt1", [])


# ---------------------------------------------------------------------------
# Migration discovery tests
# ---------------------------------------------------------------------------


class TestDiscoverMigrations:
    def test_empty_directory(self, tmp_path):
        result = discover_migrations(tmp_path)
        assert result == []

    def test_nonexistent_directory(self, tmp_path):
        result = discover_migrations(tmp_path / "nonexistent")
        assert result == []

    def test_discovers_valid_files(self, tmp_path):
        (tmp_path / "20260115_001_add_column.py").write_text("# migration")
        (tmp_path / "20260203_002_drop_index.py").write_text("# migration")
        result = discover_migrations(tmp_path)
        assert len(result) == 2
        assert result[0].name == "20260115_001_add_column"
        assert result[1].name == "20260203_002_drop_index"

    def test_ignores_non_matching_files(self, tmp_path):
        (tmp_path / "20260115_001_add_column.py").write_text("# migration")
        (tmp_path / "README.md").write_text("# readme")
        (tmp_path / "__init__.py").write_text("")
        (tmp_path / "helper.py").write_text("# helper")
        result = discover_migrations(tmp_path)
        assert len(result) == 1

    def test_sorted_by_timestamp(self, tmp_path):
        (tmp_path / "20260203_002_second.py").write_text("# migration")
        (tmp_path / "20260115_001_first.py").write_text("# migration")
        (tmp_path / "20260301_003_third.py").write_text("# migration")
        result = discover_migrations(tmp_path)
        assert [m.name for m in result] == [
            "20260115_001_first",
            "20260203_002_second",
            "20260301_003_third",
        ]

    def test_ignores_directories(self, tmp_path):
        (tmp_path / "20260115_001_add_column.py").write_text("# migration")
        (tmp_path / "20260203_002_subdir").mkdir()
        result = discover_migrations(tmp_path)
        assert len(result) == 1

    def test_migration_info_repr(self, tmp_path):
        info = MigrationInfo(name="test", path=tmp_path / "test.py", sort_key="20260115_001")
        assert "test" in repr(info)


# ---------------------------------------------------------------------------
# Migration file loading tests
# ---------------------------------------------------------------------------


class TestLoadMigrationClass:
    def test_loads_valid_migration(self, tmp_path):
        code = textwrap.dedent("""\
            from coodie.migrations import Migration

            class ForwardMigration(Migration):
                description = "Add rating column"

                async def upgrade(self, ctx):
                    await ctx.execute('ALTER TABLE test ADD "rating" int')

                async def downgrade(self, ctx):
                    await ctx.execute('ALTER TABLE test DROP "rating"')
        """)
        f = tmp_path / "20260115_001_add_rating.py"
        f.write_text(code)
        info = MigrationInfo(name="20260115_001_add_rating", path=f, sort_key="20260115_001")
        m = _load_migration_class(info)
        assert isinstance(m, Migration)
        assert m.description == "Add rating column"

    def test_missing_forward_migration_class(self, tmp_path):
        f = tmp_path / "20260115_001_bad.py"
        f.write_text("# no ForwardMigration here\nx = 1\n")
        info = MigrationInfo(name="20260115_001_bad", path=f, sort_key="20260115_001")
        with pytest.raises(ImportError, match="ForwardMigration"):
            _load_migration_class(info)

    def test_forward_migration_not_subclass(self, tmp_path):
        code = textwrap.dedent("""\
            class ForwardMigration:
                pass
        """)
        f = tmp_path / "20260115_001_bad.py"
        f.write_text(code)
        info = MigrationInfo(name="20260115_001_bad", path=f, sort_key="20260115_001")
        with pytest.raises(ImportError, match="subclass"):
            _load_migration_class(info)


# ---------------------------------------------------------------------------
# MigrationRunner tests (with mock driver)
# ---------------------------------------------------------------------------


def _make_mock_driver() -> AsyncMock:
    """Build a mock driver that records CQL calls and returns sensible defaults."""
    driver = AsyncMock()
    driver.execute_async.return_value = []
    return driver


def _write_migration(directory: Path, name: str, *, description: str = "test", reversible: bool = True) -> Path:
    """Create a minimal migration file in *directory*."""
    rev = "True" if reversible else "False"
    code = textwrap.dedent(f"""\
        from coodie.migrations import Migration

        class ForwardMigration(Migration):
            description = "{description}"
            reversible = {rev}

            async def upgrade(self, ctx):
                await ctx.execute('ALTER TABLE ks.tbl ADD "col" int')

            async def downgrade(self, ctx):
                await ctx.execute('ALTER TABLE ks.tbl DROP "col"')
    """)
    f = directory / f"{name}.py"
    f.write_text(code)
    return f


class TestMigrationRunnerState:
    """Tests for state tracking (B.3)."""

    async def test_ensure_state_table(self, tmp_path):
        driver = _make_mock_driver()
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        await runner._ensure_state_table()
        cql = driver.execute_async.call_args[0][0]
        assert "CREATE TABLE IF NOT EXISTS" in cql
        assert "_coodie_migrations" in cql

    async def test_get_applied_empty(self, tmp_path):
        driver = _make_mock_driver()
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        result = await runner.get_applied()
        assert result == {}

    async def test_record_applied(self, tmp_path):
        driver = _make_mock_driver()
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        await runner._record_applied("20260115_001_test", "Test migration", "abc123")
        call_args = driver.execute_async.call_args
        assert "INSERT INTO" in call_args[0][0]
        assert "20260115_001_test" in call_args[0][1]

    async def test_remove_applied(self, tmp_path):
        driver = _make_mock_driver()
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        await runner._remove_applied("20260115_001_test")
        call_args = driver.execute_async.call_args
        assert "DELETE FROM" in call_args[0][0]


class TestMigrationRunnerPending:
    """Tests for pending migration detection (B.2)."""

    async def test_all_pending_when_none_applied(self, tmp_path):
        driver = _make_mock_driver()
        _write_migration(tmp_path, "20260115_001_first")
        _write_migration(tmp_path, "20260203_002_second")
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        pending = await runner.pending()
        assert len(pending) == 2
        assert pending[0].name == "20260115_001_first"

    async def test_excludes_applied(self, tmp_path):
        driver = _make_mock_driver()
        # Simulate that the first migration is already applied
        driver.execute_async.return_value = [
            {"migration_name": "20260115_001_first", "applied_at": None, "description": "", "checksum": ""}
        ]
        _write_migration(tmp_path, "20260115_001_first")
        _write_migration(tmp_path, "20260203_002_second")
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        # get_applied will use the mocked return
        pending = await runner.pending()
        assert len(pending) == 1
        assert pending[0].name == "20260203_002_second"


class TestMigrationRunnerApply:
    """Tests for migration application (B.4)."""

    async def test_apply_runs_upgrade(self, tmp_path):
        driver = _make_mock_driver()
        # First call (ensure_state_table) and second (get_applied) return empty
        _write_migration(tmp_path, "20260115_001_add_col", description="Add column")
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        results = await runner.apply(dry_run=True)
        assert len(results) == 1
        assert results[0]["name"] == "20260115_001_add_col"
        assert results[0]["description"] == "Add column"
        assert len(results[0]["planned_cql"]) == 1
        assert "ALTER TABLE" in results[0]["planned_cql"][0]

    async def test_apply_dry_run_does_not_record(self, tmp_path):
        driver = _make_mock_driver()
        _write_migration(tmp_path, "20260115_001_add_col")
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        await runner.apply(dry_run=True)
        # In dry_run, we should not call INSERT to record the migration
        for call in driver.execute_async.call_args_list:
            cql = call[0][0]
            assert "INSERT INTO" not in cql or "_coodie_migrations" not in cql or "IF NOT EXISTS" in cql

    async def test_apply_with_target(self, tmp_path):
        driver = _make_mock_driver()
        _write_migration(tmp_path, "20260115_001_first")
        _write_migration(tmp_path, "20260203_002_second")
        _write_migration(tmp_path, "20260301_003_third")
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        results = await runner.apply(dry_run=True, target="20260203_002")
        assert len(results) == 2  # applies first and second, stops after target

    async def test_apply_no_pending(self, tmp_path):
        driver = _make_mock_driver()
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        results = await runner.apply(dry_run=True)
        assert results == []


class TestMigrationRunnerRollback:
    """Tests for migration rollback (B.4)."""

    async def test_rollback_runs_downgrade(self, tmp_path):
        driver = _make_mock_driver()
        _write_migration(tmp_path, "20260115_001_add_col", description="Add column")
        # Simulate that the migration is applied
        driver.execute_async.return_value = [
            {"migration_name": "20260115_001_add_col", "applied_at": None, "description": "Add column", "checksum": "x"}
        ]
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        results = await runner.rollback(steps=1, dry_run=True)
        assert len(results) == 1
        assert results[0]["name"] == "20260115_001_add_col"
        assert "DROP" in results[0]["planned_cql"][0]

    async def test_rollback_irreversible_raises(self, tmp_path):
        driver = _make_mock_driver()
        _write_migration(tmp_path, "20260115_001_add_col", reversible=False)
        driver.execute_async.return_value = [
            {"migration_name": "20260115_001_add_col", "applied_at": None, "description": "", "checksum": ""}
        ]
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        with pytest.raises(MigrationError, match="not reversible"):
            await runner.rollback(steps=1, dry_run=True)

    async def test_rollback_no_applied(self, tmp_path):
        driver = _make_mock_driver()
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        results = await runner.rollback(dry_run=True)
        assert results == []


class TestMigrationRunnerStatus:
    """Tests for status reporting (B.4)."""

    async def test_status_shows_all_migrations(self, tmp_path):
        driver = _make_mock_driver()
        _write_migration(tmp_path, "20260115_001_first")
        _write_migration(tmp_path, "20260203_002_second")
        # First migration is applied
        driver.execute_async.return_value = [
            {
                "migration_name": "20260115_001_first",
                "applied_at": "2026-01-15T00:00:00",
                "description": "test",
                "checksum": "x",
            }
        ]
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        statuses = await runner.status()
        assert len(statuses) == 2
        assert statuses[0]["name"] == "20260115_001_first"
        assert statuses[0]["applied"] is True
        assert statuses[1]["name"] == "20260203_002_second"
        assert statuses[1]["applied"] is False


class TestMigrationRunnerLock:
    """Tests for LWT-based lock (B.5)."""

    async def test_acquire_lock(self, tmp_path):
        driver = _make_mock_driver()
        # LWT INSERT returns [{"[applied]": True}] on success
        driver.execute_async.return_value = [{"[applied]": True}]
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        result = await runner._acquire_lock()
        assert result is True

    async def test_acquire_lock_fails(self, tmp_path):
        driver = _make_mock_driver()
        # LWT INSERT returns [{"[applied]": False}] when lock is held
        driver.execute_async.return_value = [{"[applied]": False}]
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        result = await runner._acquire_lock()
        assert result is False

    async def test_release_lock(self, tmp_path):
        driver = _make_mock_driver()
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        await runner._release_lock()
        call_args = driver.execute_async.call_args
        assert "DELETE FROM" in call_args[0][0]
        assert "_coodie_migrations_lock" in call_args[0][0]


class TestSchemaAgreement:
    """Tests for schema agreement wait (B.6)."""

    async def test_agreement_single_node(self, tmp_path):
        driver = _make_mock_driver()
        # local schema version
        driver.execute_async.side_effect = [
            [{"schema_version": "abc-123"}],  # system.local
            [],  # system.peers (no peers = single node)
        ]
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        result = await runner._wait_for_schema_agreement(timeout=5.0)
        assert result is True

    async def test_agreement_multi_node_agreed(self, tmp_path):
        driver = _make_mock_driver()
        driver.execute_async.side_effect = [
            [{"schema_version": "abc-123"}],  # system.local
            [{"schema_version": "abc-123"}, {"schema_version": "abc-123"}],  # system.peers
        ]
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        result = await runner._wait_for_schema_agreement(timeout=5.0)
        assert result is True

    async def test_agreement_timeout(self, tmp_path):
        driver = _make_mock_driver()
        # Always return disagreeing versions
        driver.execute_async.side_effect = lambda *a, **kw: (
            [{"schema_version": "abc"}] if "local" in a[0] else [{"schema_version": "def"}]
        )
        runner = MigrationRunner(driver, "test_ks", tmp_path)
        result = await runner._wait_for_schema_agreement(timeout=1.0)
        assert result is False
