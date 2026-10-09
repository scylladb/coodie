"""Integration test for ``MigrationContext.scan_table`` paging."""

from __future__ import annotations

import pytest

from coodie.migrations.base import MigrationContext

pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio(loop_scope="session"),
]


async def test_scan_table_pages_within_token_range(coodie_driver):
    """scan_table must return every row even when a range or partition exceeds page_size.

    Composite partition key, a static column, a static-only partition, mixed
    clustering order and case-sensitive / reserved column names.
    """
    await coodie_driver.execute_async("DROP TABLE IF EXISTS test_ks.it_scan_paging", [])
    await coodie_driver.execute_async(
        'CREATE TABLE test_ks.it_scan_paging (pk int, "Pk2" int, "order" int, c2 int, s int static, v int,'
        ' PRIMARY KEY ((pk, "Pk2"), "order", c2)) WITH CLUSTERING ORDER BY ("order" ASC, c2 DESC)',
        [],
    )
    expected = {(pk, 0, c1, c2) for pk in range(12) for c1 in range(3) for c2 in range(4)}
    for pk, pk2, c1, c2 in expected:
        await coodie_driver.execute_async(
            'INSERT INTO test_ks.it_scan_paging (pk, "Pk2", "order", c2, s, v) VALUES (?, ?, ?, ?, 1, 0)',
            [pk, pk2, c1, c2],
        )
    await coodie_driver.execute_async('INSERT INTO test_ks.it_scan_paging (pk, "Pk2", s) VALUES (99, 0, 1)', [])
    expected.add((99, 0, None, None))

    ctx = MigrationContext(coodie_driver)
    got = [
        (r["pk"], r["Pk2"], r["order"], r["c2"])
        async for r in ctx.scan_table("test_ks", "it_scan_paging", page_size=5, num_ranges=2)
    ]
    assert len(got) == len(expected)
    assert set(got) == expected
