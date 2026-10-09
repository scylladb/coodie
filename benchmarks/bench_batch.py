"""Batch operation benchmarks — coodie vs cqlengine."""

from __future__ import annotations

from uuid import uuid4

import pytest

# ---------------------------------------------------------------------------
# Batch INSERT (10 rows)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="batch-insert-10")
def test_cqlengine_batch_insert_10(benchmark, bench_env):
    from cassandra.cqlengine.query import BatchQuery as CqlBatch

    from benchmarks.models_cqlengine import CqlEvent

    def _batch():
        with CqlBatch() as batch:
            for _ in range(10):
                CqlEvent.batch(batch).create(id=uuid4(), event_type="click", payload="data")

    benchmark(_batch)


@pytest.mark.benchmark(group="batch-insert-10")
def test_coodie_batch_insert_10(benchmark, bench_env):
    from benchmarks.models_coodie import CoodieEvent
    from coodie.batch import BatchQuery

    def _batch():
        with BatchQuery() as batch:
            for _ in range(10):
                CoodieEvent(id=uuid4(), event_type="click", payload="data").save(batch=batch)

    benchmark(_batch)


# ---------------------------------------------------------------------------
# Batch INSERT (100 rows)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="batch-insert-100")
def test_cqlengine_batch_insert_100(benchmark, bench_env):
    from cassandra.cqlengine.query import BatchQuery as CqlBatch

    from benchmarks.models_cqlengine import CqlEvent

    def _batch():
        with CqlBatch() as batch:
            for _ in range(100):
                CqlEvent.batch(batch).create(id=uuid4(), event_type="click", payload="data")

    benchmark(_batch)


@pytest.mark.benchmark(group="batch-insert-100")
def test_coodie_batch_insert_100(benchmark, bench_env):
    from benchmarks.models_coodie import CoodieEvent
    from coodie.batch import BatchQuery

    def _batch():
        with BatchQuery() as batch:
            for _ in range(100):
                CoodieEvent(id=uuid4(), event_type="click", payload="data").save(batch=batch)

    benchmark(_batch)
