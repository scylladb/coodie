"""Collection type read/write benchmarks — coodie vs cqlengine."""

from __future__ import annotations

from uuid import uuid4

import pytest

# ---------------------------------------------------------------------------
# Collection field write (list[str])
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="collection-write")
def test_cqlengine_collection_write(benchmark, bench_env):
    from benchmarks.models_cqlengine import CqlProduct

    tags = ["alpha", "beta", "gamma", "delta", "epsilon"]

    def _write():
        CqlProduct.create(id=uuid4(), name="CollWrite", tags=tags)

    benchmark(_write)


@pytest.mark.benchmark(group="collection-write")
def test_coodie_collection_write(benchmark, bench_env):
    from benchmarks.models_coodie import CoodieProduct

    tags = ["alpha", "beta", "gamma", "delta", "epsilon"]

    def _write():
        CoodieProduct(id=uuid4(), name="CollWrite", tags=tags).save()

    benchmark(_write)


# ---------------------------------------------------------------------------
# Collection field read (list[str])
# ---------------------------------------------------------------------------

_COLL_READ_ID = None
_COLL_SEEDED = False


def _seed_collection_row(bench_env):
    global _COLL_READ_ID, _COLL_SEEDED
    if _COLL_SEEDED:
        return
    from benchmarks.models_coodie import CoodieProduct

    _COLL_READ_ID = uuid4()
    CoodieProduct(
        id=_COLL_READ_ID,
        name="CollRead",
        tags=["alpha", "beta", "gamma", "delta", "epsilon"],
    ).save()
    _COLL_SEEDED = True


@pytest.mark.benchmark(group="collection-read")
def test_cqlengine_collection_read(benchmark, bench_env):
    _seed_collection_row(bench_env)
    from benchmarks.models_cqlengine import CqlProduct

    def _read():
        CqlProduct.get(id=_COLL_READ_ID)

    benchmark(_read)


@pytest.mark.benchmark(group="collection-read")
def test_coodie_collection_read(benchmark, bench_env):
    _seed_collection_row(bench_env)
    from benchmarks.models_coodie import CoodieProduct

    def _read():
        CoodieProduct.get(id=_COLL_READ_ID)

    benchmark(_read)


# ---------------------------------------------------------------------------
# Collection round-trip (write + read)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="collection-roundtrip")
def test_cqlengine_collection_roundtrip(benchmark, bench_env):
    from benchmarks.models_cqlengine import CqlProduct

    tags = ["alpha", "beta", "gamma", "delta", "epsilon"]

    def _roundtrip():
        pid = uuid4()
        CqlProduct.create(id=pid, name="CollRT", tags=tags)
        CqlProduct.get(id=pid)

    benchmark(_roundtrip)


@pytest.mark.benchmark(group="collection-roundtrip")
def test_coodie_collection_roundtrip(benchmark, bench_env):
    from benchmarks.models_coodie import CoodieProduct

    tags = ["alpha", "beta", "gamma", "delta", "epsilon"]

    def _roundtrip():
        pid = uuid4()
        CoodieProduct(id=pid, name="CollRT", tags=tags).save()
        CoodieProduct.get(id=pid)

    benchmark(_roundtrip)
