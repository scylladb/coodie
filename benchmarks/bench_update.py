"""UPDATE benchmarks — coodie vs cqlengine."""

from __future__ import annotations

from uuid import uuid4

import pytest

# ---------------------------------------------------------------------------
# Setup helpers
# ---------------------------------------------------------------------------

_SETUP_DONE = False
_UPDATE_ID = None


def _ensure_row(bench_env):
    """Create a single row to update repeatedly."""
    global _SETUP_DONE, _UPDATE_ID
    if _SETUP_DONE:
        return
    from benchmarks.models_coodie import CoodieProduct

    _UPDATE_ID = uuid4()
    CoodieProduct(id=_UPDATE_ID, name="UpdateTarget", brand="UpdateBrand", price=1.0).save()
    _SETUP_DONE = True


# ---------------------------------------------------------------------------
# Partial UPDATE (read-modify-write — legacy pattern)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="partial-update")
def test_cqlengine_partial_update(benchmark, bench_env):
    _ensure_row(bench_env)
    from benchmarks.models_cqlengine import CqlProduct

    def _update():
        CqlProduct.objects(id=_UPDATE_ID).update(price=42.0)

    benchmark(_update)


@pytest.mark.benchmark(group="partial-update")
def test_coodie_partial_update(benchmark, bench_env):
    _ensure_row(bench_env)
    from benchmarks.models_coodie import CoodieProduct

    def _update():
        doc = CoodieProduct.get(id=_UPDATE_ID)
        doc.update(price=42.0)

    benchmark(_update)


# ---------------------------------------------------------------------------
# Partial UPDATE — fair 1-roundtrip comparison via QuerySet.update()
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="partial-update-fair")
def test_cqlengine_partial_update_fair(benchmark, bench_env):
    _ensure_row(bench_env)
    from benchmarks.models_cqlengine import CqlProduct

    def _update():
        CqlProduct.objects(id=_UPDATE_ID).update(price=42.0)

    benchmark(_update)


@pytest.mark.benchmark(group="partial-update-fair")
def test_coodie_partial_update_fair(benchmark, bench_env):
    """coodie: single-roundtrip UPDATE via QuerySet.update()."""
    _ensure_row(bench_env)
    from benchmarks.models_coodie import CoodieProduct

    def _update():
        CoodieProduct.find(id=_UPDATE_ID).update(price=42.0)

    benchmark(_update)


# ---------------------------------------------------------------------------
# UPDATE with IF condition (LWT)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="update-if-condition")
def test_cqlengine_update_if_condition(benchmark, bench_env):
    _ensure_row(bench_env)
    from benchmarks.models_cqlengine import CqlProduct

    def _update():
        CqlProduct.objects(id=_UPDATE_ID).iff(brand="UpdateBrand").update(price=99.0)

    benchmark(_update)


@pytest.mark.benchmark(group="update-if-condition")
def test_coodie_update_if_condition(benchmark, bench_env):
    _ensure_row(bench_env)
    from benchmarks.models_coodie import CoodieProduct

    def _update():
        doc = CoodieProduct.get(id=_UPDATE_ID)
        doc.update(if_conditions={"brand": "UpdateBrand"}, price=99.0)

    benchmark(_update)


# ---------------------------------------------------------------------------
# UPDATE with IF condition — fair 1-roundtrip via QuerySet.update()
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="update-if-condition-fair")
def test_cqlengine_update_if_condition_fair(benchmark, bench_env):
    _ensure_row(bench_env)
    from benchmarks.models_cqlengine import CqlProduct

    def _update():
        CqlProduct.objects(id=_UPDATE_ID).iff(brand="UpdateBrand").update(price=99.0)

    benchmark(_update)


@pytest.mark.benchmark(group="update-if-condition-fair")
def test_coodie_update_if_condition_fair(benchmark, bench_env):
    """coodie: single-roundtrip LWT UPDATE via QuerySet.update()."""
    _ensure_row(bench_env)
    from benchmarks.models_coodie import CoodieProduct

    def _update():
        CoodieProduct.find(id=_UPDATE_ID).update(
            if_conditions={"brand": "UpdateBrand"},
            price=99.0,
        )

    benchmark(_update)
