"""Vector search benchmarks — coodie ANN queries vs cqlengine list-based fallback.

coodie supports native ``vector<float, N>`` columns with SAI vector indexes
and ``ORDER BY … ANN OF ?`` queries.  cqlengine has no equivalent — the closest
option is a ``list<float>`` column with a full-table scan, demonstrating why
native vector support matters for similarity-search workloads.

Groups:
- ``vector-insert``  — INSERT a row with a 16-dimensional embedding
- ``vector-ann``     — ANN SELECT (coodie) vs full-scan SELECT (cqlengine)
"""

from __future__ import annotations

import random
from uuid import uuid4

import pytest

# Dimension constant matching the model definition in models_coodie.py
DIMS = 16

_skip_reason = "Vector index not available (SAI not supported on this ScyllaDB)"


def _has_vector_index() -> bool:
    """Check if the vector index actually exists in the database."""
    try:
        from coodie.drivers import get_driver

        driver = get_driver()
        rows = driver.execute(
            "SELECT index_name FROM system_schema.indexes "
            "WHERE keyspace_name = 'bench_vector_ks' AND table_name = 'bench_vector_products'",
            [],
        )
        return len(rows) > 0
    except Exception:  # noqa: BLE001
        return False


def _random_vec(dims: int = DIMS) -> list[float]:
    return [random.random() for _ in range(dims)]


# ---------------------------------------------------------------------------
# INSERT benchmarks
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="vector-insert")
def test_coodie_vector_insert(benchmark, bench_env):
    """coodie: INSERT a product with a 16-dim ``vector<float, 16>`` column."""
    if not _has_vector_index():
        pytest.skip(_skip_reason)
    from benchmarks.models_coodie import CoodieVectorProduct

    def _insert():
        CoodieVectorProduct(id=uuid4(), name="BenchVec", embedding=_random_vec()).save()

    benchmark(_insert)


@pytest.mark.benchmark(group="vector-insert")
def test_cqlengine_vector_insert(benchmark, bench_env):
    """cqlengine: INSERT a product with a ``list<float>`` column (no native vector type)."""
    if not _has_vector_index():
        pytest.skip(_skip_reason)
    from benchmarks.models_cqlengine import CqlVectorProduct

    def _insert():
        CqlVectorProduct.create(id=uuid4(), name="BenchVec", embedding=_random_vec())

    benchmark(_insert)


# ---------------------------------------------------------------------------
# SELECT / ANN benchmarks
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="vector-ann")
def test_coodie_ann_select(benchmark, bench_env):
    """coodie: ANN SELECT using ``ORDER BY embedding ANN OF ?``."""
    if not _has_vector_index():
        pytest.skip(_skip_reason)
    from benchmarks.models_coodie import CoodieVectorProduct

    # Seed a few rows so the query has data to return
    for _ in range(5):
        CoodieVectorProduct(id=uuid4(), name="Seed", embedding=_random_vec()).save()

    def _ann():
        qv = _random_vec()
        return CoodieVectorProduct.find().order_by_ann("embedding", qv).limit(5).all()

    benchmark(_ann)


@pytest.mark.benchmark(group="vector-ann")
def test_cqlengine_list_select(benchmark, bench_env):
    """cqlengine: full-table SELECT (no ANN support — returns first N rows)."""
    if not _has_vector_index():
        pytest.skip(_skip_reason)
    from benchmarks.models_cqlengine import CqlVectorProduct

    # Seed a few rows
    for _ in range(5):
        CqlVectorProduct.create(id=uuid4(), name="Seed", embedding=_random_vec())

    def _scan():
        return list(CqlVectorProduct.objects.limit(5))

    benchmark(_scan)
