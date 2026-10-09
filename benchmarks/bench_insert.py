"""INSERT benchmarks — coodie vs cqlengine."""

from __future__ import annotations

from uuid import uuid4

import pytest

# ---------------------------------------------------------------------------
# Single INSERT
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="single-insert")
def test_cqlengine_single_insert(benchmark, bench_env):
    from benchmarks.models_cqlengine import CqlProduct

    def _insert():
        CqlProduct.create(id=uuid4(), name="BenchItem", brand="BenchBrand", price=9.99)

    benchmark(_insert)


@pytest.mark.benchmark(group="single-insert")
def test_coodie_single_insert(benchmark, bench_env):
    from benchmarks.models_coodie import CoodieProduct

    def _insert():
        CoodieProduct(id=uuid4(), name="BenchItem", brand="BenchBrand", price=9.99).save()

    benchmark(_insert)


# ---------------------------------------------------------------------------
# INSERT IF NOT EXISTS
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="insert-if-not-exists")
def test_cqlengine_insert_if_not_exists(benchmark, bench_env):
    from benchmarks.models_cqlengine import CqlProduct

    def _insert():
        CqlProduct.if_not_exists().create(id=uuid4(), name="BenchINE", brand="BenchBrand", price=1.0)

    benchmark(_insert)


@pytest.mark.benchmark(group="insert-if-not-exists")
def test_coodie_insert_if_not_exists(benchmark, bench_env):
    from benchmarks.models_coodie import CoodieProduct

    def _insert():
        CoodieProduct(id=uuid4(), name="BenchINE", brand="BenchBrand", price=1.0).insert()

    benchmark(_insert)


# ---------------------------------------------------------------------------
# INSERT with TTL
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="insert-with-ttl")
def test_cqlengine_insert_with_ttl(benchmark, bench_env):
    from benchmarks.models_cqlengine import CqlProduct

    def _insert():
        CqlProduct.ttl(60).create(id=uuid4(), name="BenchTTL", brand="BenchBrand", price=2.0)

    benchmark(_insert)


@pytest.mark.benchmark(group="insert-with-ttl")
def test_coodie_insert_with_ttl(benchmark, bench_env):
    from benchmarks.models_coodie import CoodieProduct

    def _insert():
        CoodieProduct(id=uuid4(), name="BenchTTL", brand="BenchBrand", price=2.0).save(ttl=60)

    benchmark(_insert)
