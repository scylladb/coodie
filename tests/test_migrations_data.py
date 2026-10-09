"""Unit tests for data migration helpers (Phase D — D.1–D.4)."""

from __future__ import annotations

import logging
import re
from unittest.mock import AsyncMock

import pytest

from coodie.migrations.base import _TOKEN_MAX, _TOKEN_MIN, MigrationContext

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_mock_driver(*, pk_columns: list[dict] | None = None, scan_rows: list[dict] | None = None) -> AsyncMock:
    """Build a mock driver for scan_table tests.

    Parameters
    ----------
    pk_columns:
        Rows returned by the ``system_schema.columns`` query (partition key discovery).
    scan_rows:
        Rows returned by each token-range ``SELECT`` query.
    """
    driver = AsyncMock()

    if pk_columns is None:
        pk_columns = [{"column_name": "id", "kind": "partition_key", "position": 0}]
    if scan_rows is None:
        scan_rows = []

    async def _execute_side_effect(cql: str, params: list | None = None, **kwargs):
        if "system_schema.columns" in cql:
            return list(pk_columns)
        if "SELECT * FROM" in cql:
            return list(scan_rows)
        return []

    driver.execute_async.side_effect = _execute_side_effect
    return driver


# ---------------------------------------------------------------------------
# D.1 — scan_table: token-range batched iteration
# ---------------------------------------------------------------------------


class TestScanTable:
    """Tests for ``ctx.scan_table()`` (D.1)."""

    async def test_scan_table_yields_rows(self):
        """scan_table yields rows returned by driver."""
        rows = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        driver = _make_mock_driver(scan_rows=rows)
        ctx = MigrationContext(driver, dry_run=False)

        collected = []
        async for row in ctx.scan_table("ks", "tbl", num_ranges=3):
            collected.append(row)

        # Each of the 3 ranges returns 2 rows → 6 total
        assert len(collected) == 6
        assert all(r["name"] in ("Alice", "Bob") for r in collected)

    async def test_scan_table_uses_token_queries(self):
        """scan_table issues token-range CQL queries."""
        driver = _make_mock_driver()
        ctx = MigrationContext(driver, dry_run=False)

        async for _ in ctx.scan_table("myks", "users", num_ranges=2):
            pass

        # Should have executed 1 PK discovery query + 2 token-range queries
        token_calls = [c for c in driver.execute_async.call_args_list if "SELECT * FROM" in str(c)]
        assert len(token_calls) == 2
        # Verify CQL contains token()
        for call in token_calls:
            cql = call[0][0]
            assert 'token("id")' in cql
            assert "LIMIT" in cql

    async def test_scan_table_composite_pk(self):
        """scan_table handles composite partition keys."""
        pk_cols = [
            {"column_name": "region", "kind": "partition_key", "position": 0},
            {"column_name": "user_id", "kind": "partition_key", "position": 1},
        ]
        driver = _make_mock_driver(pk_columns=pk_cols)
        ctx = MigrationContext(driver, dry_run=False)

        async for _ in ctx.scan_table("ks", "tbl", num_ranges=1):
            pass

        token_calls = [c for c in driver.execute_async.call_args_list if "SELECT * FROM" in str(c)]
        assert len(token_calls) == 1
        cql = token_calls[0][0][0]
        assert 'token("region", "user_id")' in cql

    async def test_scan_table_page_size(self):
        """page_size is reflected in the LIMIT clause."""
        driver = _make_mock_driver()
        ctx = MigrationContext(driver, dry_run=False)

        async for _ in ctx.scan_table("ks", "tbl", page_size=500, num_ranges=1):
            pass

        token_calls = [c for c in driver.execute_async.call_args_list if "SELECT * FROM" in str(c)]
        cql = token_calls[0][0][0]
        assert "LIMIT 500" in cql

    async def test_scan_table_dry_run(self):
        """In dry-run mode, scan_table yields a placeholder and does not call driver."""
        driver = AsyncMock()
        ctx = MigrationContext(driver, dry_run=True)

        collected = []
        async for row in ctx.scan_table("ks", "tbl"):
            collected.append(row)

        assert len(collected) == 1
        assert collected[0] == {"__dry_run__": True}
        driver.execute_async.assert_not_called()
        assert any("dry-run" in cql for cql in ctx.planned_cql)

    async def test_scan_table_records_cql(self):
        """scan_table records executed CQL in planned_cql."""
        driver = _make_mock_driver()
        ctx = MigrationContext(driver, dry_run=False)

        async for _ in ctx.scan_table("ks", "tbl", num_ranges=2):
            pass

        token_cqls = [c for c in ctx.planned_cql if "SELECT * FROM" in c]
        assert len(token_cqls) == 2

    async def test_scan_table_no_pk_raises(self):
        """scan_table raises ValueError if table has no partition key columns."""
        driver = _make_mock_driver(pk_columns=[])
        ctx = MigrationContext(driver, dry_run=False)

        with pytest.raises(ValueError, match="No partition key columns"):
            async for _ in ctx.scan_table("ks", "tbl"):
                pass

    async def test_scan_table_covers_full_token_range(self):
        """Token ranges cover from _TOKEN_MIN to _TOKEN_MAX."""
        driver = _make_mock_driver()
        ctx = MigrationContext(driver, dry_run=False)

        async for _ in ctx.scan_table("ks", "tbl", num_ranges=4):
            pass

        token_calls = [c for c in driver.execute_async.call_args_list if "SELECT * FROM" in str(c)]
        # First range starts at _TOKEN_MIN, last range ends at _TOKEN_MAX
        first_params = token_calls[0][0][1]
        last_params = token_calls[-1][0][1]
        assert first_params[0] == _TOKEN_MIN
        assert last_params[1] == _TOKEN_MAX


# ---------------------------------------------------------------------------
# D.2 — Progress reporting
# ---------------------------------------------------------------------------


class TestScanTableProgress:
    """Tests for progress logging (D.2)."""

    async def test_progress_logged(self, caplog):
        """scan_table logs progress at ~10% intervals."""
        driver = _make_mock_driver()
        ctx = MigrationContext(driver, dry_run=False)

        with caplog.at_level(logging.INFO, logger="coodie"):
            async for _ in ctx.scan_table("ks", "tbl", num_ranges=10):
                pass

        progress_msgs = [r for r in caplog.records if "scan_table" in r.message and "ranges" in r.message]
        # With 10 ranges, log every 1 range (10//10=1) → should have multiple log messages
        assert len(progress_msgs) >= 1
        # Final message should report 100%
        assert "100.0%" in progress_msgs[-1].message

    async def test_progress_includes_last_token(self, caplog):
        """Progress log messages include the last_token value."""
        driver = _make_mock_driver()
        ctx = MigrationContext(driver, dry_run=False)

        with caplog.at_level(logging.INFO, logger="coodie"):
            async for _ in ctx.scan_table("ks", "tbl", num_ranges=5):
                pass

        progress_msgs = [r for r in caplog.records if "last_token=" in r.message]
        assert len(progress_msgs) >= 1


# ---------------------------------------------------------------------------
# D.3 — Resume-from-token
# ---------------------------------------------------------------------------


class TestScanTableResume:
    """Tests for resume-from-token support (D.3)."""

    async def test_resume_skips_processed_ranges(self):
        """resume_token causes ranges with start <= resume_token to be skipped."""
        driver = _make_mock_driver(scan_rows=[{"id": 1}])
        ctx = MigrationContext(driver, dry_run=False)

        # Use 4 ranges, resume from a token past the first range
        range_size = (_TOKEN_MAX - _TOKEN_MIN) // 4
        # resume_token is set to the start of the 2nd range, so first 2 ranges are skipped
        resume_at = _TOKEN_MIN + range_size

        collected = []
        async for row in ctx.scan_table("ks", "tbl", num_ranges=4, resume_token=resume_at):
            collected.append(row)

        # Only ranges whose start > resume_at are processed
        token_calls = [c for c in driver.execute_async.call_args_list if "SELECT * FROM" in str(c)]
        # Ranges: [_TOKEN_MIN, _TOKEN_MIN+range_size, _TOKEN_MIN+2*range_size, _TOKEN_MIN+3*range_size]
        # resume_token = _TOKEN_MIN + range_size → skip ranges starting at _TOKEN_MIN (<=) and _TOKEN_MIN+range_size (<=)
        # Process: ranges starting at _TOKEN_MIN+2*range_size and _TOKEN_MIN+3*range_size
        assert len(token_calls) == 2

    async def test_resume_none_processes_all(self):
        """resume_token=None processes all ranges."""
        driver = _make_mock_driver(scan_rows=[{"id": 1}])
        ctx = MigrationContext(driver, dry_run=False)

        collected = []
        async for row in ctx.scan_table("ks", "tbl", num_ranges=3, resume_token=None):
            collected.append(row)

        token_calls = [c for c in driver.execute_async.call_args_list if "SELECT * FROM" in str(c)]
        assert len(token_calls) == 3

    async def test_resume_past_all_ranges(self):
        """resume_token past all ranges yields nothing."""
        driver = _make_mock_driver(scan_rows=[{"id": 1}])
        ctx = MigrationContext(driver, dry_run=False)

        collected = []
        async for row in ctx.scan_table("ks", "tbl", num_ranges=3, resume_token=_TOKEN_MAX):
            collected.append(row)

        assert len(collected) == 0


# ---------------------------------------------------------------------------
# D.4 — Rate limiting / throttle
# ---------------------------------------------------------------------------


class TestScanTableThrottle:
    """Tests for rate limiting / throttle support (D.4)."""

    async def test_throttle_zero_no_sleep(self, monkeypatch):
        """throttle_seconds=0 does not call asyncio.sleep."""
        import coodie.migrations.base as base_mod

        sleep_calls: list[float] = []

        async def _mock_sleep(seconds: float):
            sleep_calls.append(seconds)

        monkeypatch.setattr(base_mod.asyncio, "sleep", _mock_sleep)

        driver = _make_mock_driver()
        ctx = MigrationContext(driver, dry_run=False)

        async for _ in ctx.scan_table("ks", "tbl", num_ranges=3, throttle_seconds=0.0):
            pass

        assert len(sleep_calls) == 0

    async def test_throttle_positive_sleeps(self, monkeypatch):
        """throttle_seconds > 0 sleeps between each range query."""
        import coodie.migrations.base as base_mod

        sleep_calls: list[float] = []

        async def _mock_sleep(seconds: float):
            sleep_calls.append(seconds)

        monkeypatch.setattr(base_mod.asyncio, "sleep", _mock_sleep)

        driver = _make_mock_driver()
        ctx = MigrationContext(driver, dry_run=False)

        async for _ in ctx.scan_table("ks", "tbl", num_ranges=5, throttle_seconds=0.1):
            pass

        assert len(sleep_calls) == 5
        assert all(s == 0.1 for s in sleep_calls)


# ---------------------------------------------------------------------------
# scan_table paging within a token range (C3)
# ---------------------------------------------------------------------------


def _tok(pk: int) -> int:
    return pk // 2  # every two partitions share a token, like a murmur3 collision


class _FakeTable:
    """In-memory table that answers the CQL shapes ``scan_table`` emits.

    Rows are ``{"pk", "c1", "c2", "v"}`` with ``token(pk) == pk // 2``.
    ``c1`` clusters ascending and ``c2`` descending.
    """

    def __init__(self, rows: list[dict]):
        self.rows = sorted(rows, key=lambda r: (_tok(r["pk"]), r["pk"], r["c1"], -r["c2"]))

    async def execute_async(self, cql: str, params: list | None = None, **kwargs):
        params = list(params or [])
        if "system_schema.columns" in cql:
            return [
                {"column_name": "pk", "kind": "partition_key", "position": 0, "clustering_order": "none"},
                {"column_name": "c1", "kind": "clustering", "position": 0, "clustering_order": "ASC"},
                {"column_name": "c2", "kind": "clustering", "position": 1, "clustering_order": "DESC"},
                {"column_name": "v", "kind": "regular", "position": -1, "clustering_order": "none"},
            ]
        if cql.startswith("SELECT DISTINCT"):
            assert 'token("pk") = token(?)' in cql
            return [{"pk": pk} for pk in dict.fromkeys(r["pk"] for r in self.rows if _tok(r["pk"]) == _tok(params[0]))]
        limit = int(re.search(r"LIMIT (\d+)", cql).group(1))
        if 'token("pk") > token(?)' in cql:
            last, end = params
            hits = [r for r in self.rows if _tok(last) < _tok(r["pk"]) <= end]
        elif 'token("pk") > ?' in cql:
            start, end = params
            hits = [r for r in self.rows if start < _tok(r["pk"]) <= end]
        elif m := re.search(r'AND "(\w+)" ([<>]) \? LIMIT', cql):
            pk, *ck = params
            eqs = ["c1", "c2"][: len(ck) - 1]
            col, op = m.groups()
            assert op == (">" if col == "c1" else "<")
            hits = [
                r
                for r in self.rows
                if r["pk"] == pk
                and all(r[c] == v for c, v in zip(eqs, ck))
                and (r[col] > ck[-1] if op == ">" else r[col] < ck[-1])
            ]
        else:
            assert '"pk" = ? LIMIT' in cql
            hits = [r for r in self.rows if r["pk"] == params[0]]
        return [dict(r) for r in hits[:limit]]


def _key(row: dict) -> tuple:
    return (row["pk"], row["c1"], row["c2"])


class TestScanTablePaging:
    """A token range holding more than ``page_size`` rows must not be truncated."""

    async def _scan(self, rows: list[dict], page_size: int) -> list[dict]:
        ctx = MigrationContext(_FakeTable(rows), dry_run=False)
        return [r async for r in ctx.scan_table("ks", "tbl", page_size=page_size, num_ranges=1)]

    async def test_many_partitions_in_one_range(self):
        rows = [{"pk": pk, "c1": 0, "c2": 0, "v": pk} for pk in range(25)]
        got = await self._scan(rows, page_size=10)
        assert sorted(map(_key, got)) == sorted(map(_key, rows))

    async def test_many_clustering_rows_in_one_partition(self):
        rows = [{"pk": pk, "c1": c1, "c2": c2, "v": 0} for pk in (1, 2, 3) for c1 in range(4) for c2 in range(7)]
        got = await self._scan(rows, page_size=5)
        assert sorted(map(_key, got)) == sorted(map(_key, rows))

    async def test_exact_page_size_multiple(self):
        rows = [{"pk": pk, "c1": 0, "c2": 0, "v": 0} for pk in range(20)]
        got = await self._scan(rows, page_size=10)
        assert sorted(map(_key, got)) == sorted(map(_key, rows))

    async def test_page_ends_on_token_shared_by_two_partitions(self):
        # page 1 ends at pk 4; pk 5 has the same token and must not be skipped
        rows = [{"pk": pk, "c1": c1, "c2": 0, "v": 0} for pk in range(10) for c1 in range(7 if pk == 5 else 1)]
        got = await self._scan(rows, page_size=5)
        assert sorted(map(_key, got)) == sorted(map(_key, rows))
