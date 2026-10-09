"""Phase B migration-framework integration tests.

Exercises the full ``MigrationRunner`` lifecycle against a real ScyllaDB
container: apply, rollback, status, dry-run, state tracking, and
schema-agreement wait.

Every test runs the async path via the ``coodie_driver`` session fixture.
"""

from __future__ import annotations

import contextlib
import textwrap

import pytest

from coodie.migrations.runner import MigrationRunner

pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio(loop_scope="session"),
]


@pytest.fixture()
def migrations_dir(tmp_path):
    """Return a temporary directory for migration files."""
    return tmp_path


def _write_migration(directory, name, *, upgrade_cql, downgrade_cql="", description="test", reversible=True):
    """Create a migration file in *directory*."""
    down_body = f"await ctx.execute({downgrade_cql!r})" if downgrade_cql else "pass"
    rev = "True" if reversible else "False"
    code = textwrap.dedent(f"""\
        from coodie.migrations import Migration

        class ForwardMigration(Migration):
            description = "{description}"
            reversible = {rev}

            async def upgrade(self, ctx):
                await ctx.execute({upgrade_cql!r})

            async def downgrade(self, ctx):
                {down_body}
    """)
    f = directory / f"{name}.py"
    f.write_text(code)
    return f


class TestMigrationPhaseBIntegration:
    """Integration tests for Phase B migration framework."""

    @pytest.fixture(autouse=True)
    async def _cleanup_migration_tables(self, coodie_driver):
        """Drop migration tracking tables before each test."""
        with contextlib.suppress(Exception):  # best-effort cleanup
            await coodie_driver.execute_async('DROP TABLE IF EXISTS test_ks."_coodie_migrations"', [])
        with contextlib.suppress(Exception):  # best-effort cleanup
            await coodie_driver.execute_async('DROP TABLE IF EXISTS test_ks."_coodie_migrations_lock"', [])

    async def test_apply_creates_state_table_and_records_migration(self, coodie_driver, migrations_dir):
        """apply() should create the state table and record applied migrations."""
        _write_migration(
            migrations_dir,
            "20260115_001_add_col",
            upgrade_cql='ALTER TABLE test_ks.it_phase_a ADD "phase_b_test_col" text',
            downgrade_cql='ALTER TABLE test_ks.it_phase_a DROP "phase_b_test_col"',
            description="Add phase_b_test_col",
        )

        # Ensure base table exists
        await coodie_driver.execute_async(
            'CREATE TABLE IF NOT EXISTS test_ks.it_phase_a ("id" uuid PRIMARY KEY, "name" text)', []
        )

        runner = MigrationRunner(coodie_driver, "test_ks", migrations_dir)
        results = await runner.apply()

        assert len(results) == 1
        assert results[0]["name"] == "20260115_001_add_col"
        assert results[0]["description"] == "Add phase_b_test_col"
        assert len(results[0]["planned_cql"]) == 1

        # Verify migration was recorded in the state table
        applied = await runner.get_applied()
        assert "20260115_001_add_col" in applied
        assert applied["20260115_001_add_col"]["description"] == "Add phase_b_test_col"
        assert applied["20260115_001_add_col"]["checksum"]  # non-empty

    async def test_apply_is_idempotent(self, coodie_driver, migrations_dir):
        """Applying the same migration twice should be a no-op the second time."""
        _write_migration(
            migrations_dir,
            "20260115_001_noop",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_idem ("id" uuid PRIMARY KEY)',
            description="Idempotent test",
        )

        runner = MigrationRunner(coodie_driver, "test_ks", migrations_dir)
        results1 = await runner.apply()
        assert len(results1) == 1

        # Second apply — should skip
        results2 = await runner.apply()
        assert len(results2) == 0

    async def test_apply_dry_run_does_not_execute(self, coodie_driver, migrations_dir):
        """dry_run=True should collect CQL but not actually run it or record the migration."""
        _write_migration(
            migrations_dir,
            "20260115_001_dry",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_dryrun ("id" uuid PRIMARY KEY)',
            description="Dry run test",
        )

        runner = MigrationRunner(coodie_driver, "test_ks", migrations_dir)
        results = await runner.apply(dry_run=True)

        assert len(results) == 1
        assert "CREATE TABLE" in results[0]["planned_cql"][0]

        # Verify migration was NOT recorded
        applied = await runner.get_applied()
        assert "20260115_001_dry" not in applied

        # Verify table was NOT created
        rows = await coodie_driver.execute_async(
            "SELECT table_name FROM system_schema.tables WHERE keyspace_name = ? AND table_name = ?",
            ["test_ks", "it_phase_b_dryrun"],
        )
        assert len(rows) == 0

    async def test_apply_with_target(self, coodie_driver, migrations_dir):
        """apply(target=...) should stop after the target migration."""
        _write_migration(
            migrations_dir,
            "20260115_001_first",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_t1 ("id" uuid PRIMARY KEY)',
            description="First",
        )
        _write_migration(
            migrations_dir,
            "20260203_002_second",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_t2 ("id" uuid PRIMARY KEY)',
            description="Second",
        )
        _write_migration(
            migrations_dir,
            "20260301_003_third",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_t3 ("id" uuid PRIMARY KEY)',
            description="Third",
        )

        runner = MigrationRunner(coodie_driver, "test_ks", migrations_dir)
        results = await runner.apply(target="20260203_002")

        assert len(results) == 2
        assert results[0]["name"] == "20260115_001_first"
        assert results[1]["name"] == "20260203_002_second"

        # Third should still be pending
        pending = await runner.pending()
        assert len(pending) == 1
        assert pending[0].name == "20260301_003_third"

    async def test_rollback_removes_migration_record(self, coodie_driver, migrations_dir):
        """rollback() should execute downgrade and remove the state record."""
        _write_migration(
            migrations_dir,
            "20260115_001_roll",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_roll ("id" uuid PRIMARY KEY, "extra" text)',
            downgrade_cql='ALTER TABLE test_ks.it_phase_b_roll DROP "extra"',
            description="Rollback test",
        )

        runner = MigrationRunner(coodie_driver, "test_ks", migrations_dir)
        await runner.apply()

        applied_before = await runner.get_applied()
        assert "20260115_001_roll" in applied_before

        results = await runner.rollback(steps=1)
        assert len(results) == 1
        assert results[0]["name"] == "20260115_001_roll"

        applied_after = await runner.get_applied()
        assert "20260115_001_roll" not in applied_after

    async def test_rollback_dry_run(self, coodie_driver, migrations_dir):
        """rollback(dry_run=True) should not remove the state record."""
        _write_migration(
            migrations_dir,
            "20260115_001_rdry",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_rdry ("id" uuid PRIMARY KEY)',
            downgrade_cql="SELECT * FROM system.local WHERE key = 'local'",
            description="Rollback dry run",
        )

        runner = MigrationRunner(coodie_driver, "test_ks", migrations_dir)
        await runner.apply()

        results = await runner.rollback(steps=1, dry_run=True)
        assert len(results) == 1

        # Migration should still be recorded
        applied = await runner.get_applied()
        assert "20260115_001_rdry" in applied

    async def test_status_shows_applied_and_pending(self, coodie_driver, migrations_dir):
        """status() should show which migrations are applied and which are pending."""
        _write_migration(
            migrations_dir,
            "20260115_001_stat1",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_s1 ("id" uuid PRIMARY KEY)',
            description="Status first",
        )
        _write_migration(
            migrations_dir,
            "20260203_002_stat2",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_s2 ("id" uuid PRIMARY KEY)',
            description="Status second",
        )

        runner = MigrationRunner(coodie_driver, "test_ks", migrations_dir)

        # Apply only the first
        await runner.apply(target="20260115_001")

        statuses = await runner.status()
        assert len(statuses) == 2
        assert statuses[0]["name"] == "20260115_001_stat1"
        assert statuses[0]["applied"] is True
        assert statuses[1]["name"] == "20260203_002_stat2"
        assert statuses[1]["applied"] is False

    async def test_pending_returns_unapplied_migrations(self, coodie_driver, migrations_dir):
        """pending() should return only migrations not yet applied."""
        _write_migration(
            migrations_dir,
            "20260115_001_pend",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_p1 ("id" uuid PRIMARY KEY)',
            description="Pending test",
        )

        runner = MigrationRunner(coodie_driver, "test_ks", migrations_dir)
        pending = await runner.pending()
        assert len(pending) == 1

        await runner.apply()
        pending = await runner.pending()
        assert len(pending) == 0

    async def test_schema_agreement_succeeds_on_single_node(self, coodie_driver, migrations_dir):
        """Schema agreement wait should pass on a single-node cluster."""
        runner = MigrationRunner(coodie_driver, "test_ks", migrations_dir)
        result = await runner._wait_for_schema_agreement(timeout=10.0)
        assert result is True

    async def test_multiple_migrations_ordered(self, coodie_driver, migrations_dir):
        """Multiple migrations should be applied in timestamp order."""
        _write_migration(
            migrations_dir,
            "20260301_003_third",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_m3 ("id" uuid PRIMARY KEY)',
            description="Third",
        )
        _write_migration(
            migrations_dir,
            "20260115_001_first",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_m1 ("id" uuid PRIMARY KEY)',
            description="First",
        )
        _write_migration(
            migrations_dir,
            "20260203_002_second",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_m2 ("id" uuid PRIMARY KEY)',
            description="Second",
        )

        runner = MigrationRunner(coodie_driver, "test_ks", migrations_dir)
        results = await runner.apply()

        assert len(results) == 3
        assert results[0]["name"] == "20260115_001_first"
        assert results[1]["name"] == "20260203_002_second"
        assert results[2]["name"] == "20260301_003_third"

    async def test_checksum_stored_in_state(self, coodie_driver, migrations_dir):
        """Applied migration should have a non-empty SHA-256 checksum."""
        _write_migration(
            migrations_dir,
            "20260115_001_chk",
            upgrade_cql='CREATE TABLE IF NOT EXISTS test_ks.it_phase_b_chk ("id" uuid PRIMARY KEY)',
            description="Checksum test",
        )

        runner = MigrationRunner(coodie_driver, "test_ks", migrations_dir)
        await runner.apply()

        applied = await runner.get_applied()
        checksum = applied["20260115_001_chk"]["checksum"]
        assert isinstance(checksum, str)
        assert len(checksum) == 64  # SHA-256 hex digest
