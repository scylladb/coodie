"""DELETE benchmarks — coodie vs cqlengine."""

from __future__ import annotations

from uuid import uuid4

import pytest

# ---------------------------------------------------------------------------
# Single DELETE
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="single-delete")
def test_cqlengine_single_delete(benchmark, bench_env):
    from benchmarks.models_cqlengine import CqlProduct

    def _delete():
        pid = uuid4()
        obj = CqlProduct.create(id=pid, name="DelTarget")
        obj.delete()

    benchmark(_delete)


@pytest.mark.benchmark(group="single-delete")
def test_coodie_single_delete(benchmark, bench_env):
    from benchmarks.models_coodie import CoodieProduct

    def _delete():
        pid = uuid4()
        doc = CoodieProduct(id=pid, name="DelTarget")
        doc.save()
        doc.delete()

    benchmark(_delete)


# ---------------------------------------------------------------------------
# Bulk DELETE (QuerySet)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="bulk-delete")
def test_cqlengine_bulk_delete(benchmark, bench_env):
    from benchmarks.models_cqlengine import CqlProduct

    def _delete():
        pid = uuid4()
        CqlProduct.create(id=pid, name="BulkDel")
        CqlProduct.objects(id=pid).delete()

    benchmark(_delete)


@pytest.mark.benchmark(group="bulk-delete")
def test_coodie_bulk_delete(benchmark, bench_env):
    from benchmarks.models_coodie import CoodieProduct

    def _delete():
        pid = uuid4()
        CoodieProduct(id=pid, name="BulkDel").save()
        CoodieProduct.find(id=pid).delete()

    benchmark(_delete)
