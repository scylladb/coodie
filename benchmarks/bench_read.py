"""SELECT / query benchmarks — coodie vs cqlengine."""

from __future__ import annotations

from uuid import uuid4

import pytest

# ---------------------------------------------------------------------------
# Seed data (module-level, populated once per session)
# ---------------------------------------------------------------------------

_SEEDED = False
_SEED_IDS: list = []


def _seed_data(bench_env):
    """Insert seed rows for read benchmarks (idempotent)."""
    global _SEEDED
    if _SEEDED:
        return
    from benchmarks.models_coodie import CoodieProduct

    for i in range(100):
        pid = uuid4()
        _SEED_IDS.append(pid)
        CoodieProduct(
            id=pid,
            name=f"ReadItem{i}",
            brand="ReadBrand",
            category="read_bench",
            price=float(i),
        ).save()
    _SEEDED = True


# ---------------------------------------------------------------------------
# GET by PK
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="get-by-pk")
def test_cqlengine_get_by_pk(benchmark, bench_env):
    _seed_data(bench_env)
    from benchmarks.models_cqlengine import CqlProduct

    target_id = _SEED_IDS[0]

    def _get():
        CqlProduct.get(id=target_id)

    benchmark(_get)


@pytest.mark.benchmark(group="get-by-pk")
def test_coodie_get_by_pk(benchmark, bench_env):
    _seed_data(bench_env)
    from benchmarks.models_coodie import CoodieProduct

    target_id = _SEED_IDS[0]

    def _get():
        CoodieProduct.get(id=target_id)

    benchmark(_get)


# ---------------------------------------------------------------------------
# Filter (secondary index)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="filter-secondary-index")
def test_cqlengine_filter_secondary_index(benchmark, bench_env):
    _seed_data(bench_env)
    from benchmarks.models_cqlengine import CqlProduct

    def _filter():
        list(CqlProduct.objects.filter(brand="ReadBrand"))

    benchmark(_filter)


@pytest.mark.benchmark(group="filter-secondary-index")
def test_coodie_filter_secondary_index(benchmark, bench_env):
    _seed_data(bench_env)
    from benchmarks.models_coodie import CoodieProduct

    def _filter():
        CoodieProduct.find(brand="ReadBrand").allow_filtering().all()

    benchmark(_filter)


# ---------------------------------------------------------------------------
# Filter + LIMIT
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="filter-limit")
def test_cqlengine_filter_limit(benchmark, bench_env):
    _seed_data(bench_env)
    from benchmarks.models_cqlengine import CqlProduct

    def _filter():
        list(CqlProduct.objects.filter(brand="ReadBrand").limit(10))

    benchmark(_filter)


@pytest.mark.benchmark(group="filter-limit")
def test_coodie_filter_limit(benchmark, bench_env):
    _seed_data(bench_env)
    from benchmarks.models_coodie import CoodieProduct

    def _filter():
        CoodieProduct.find(brand="ReadBrand").allow_filtering().limit(10).all()

    benchmark(_filter)


# ---------------------------------------------------------------------------
# COUNT
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="count")
def test_cqlengine_count(benchmark, bench_env):
    _seed_data(bench_env)
    from benchmarks.models_cqlengine import CqlProduct

    def _count():
        CqlProduct.objects.filter(brand="ReadBrand").count()

    benchmark(_count)


@pytest.mark.benchmark(group="count")
def test_coodie_count(benchmark, bench_env):
    _seed_data(bench_env)
    from benchmarks.models_coodie import CoodieProduct

    def _count():
        CoodieProduct.find(brand="ReadBrand").allow_filtering().count()

    benchmark(_count)
