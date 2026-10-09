"""Serialization / deserialization overhead benchmarks — coodie vs cqlengine.

These benchmarks measure pure Python overhead (model construction and
serialization) **without** hitting the database, isolating the ORM layer cost.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

# ---------------------------------------------------------------------------
# Model instantiation from dict (10 fields)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="model-instantiation")
def test_cqlengine_model_instantiation(benchmark):
    try:
        from benchmarks.models_cqlengine import CqlProduct
    except (ImportError, ModuleNotFoundError):
        pytest.skip("cqlengine not available")

    data = {
        "id": uuid4(),
        "name": "InstBench",
        "brand": "BrandX",
        "category": "catA",
        "price": 19.99,
        "tags": ["a", "b", "c"],
        "description": "A benchmark product",
    }

    def _create():
        CqlProduct(**data)

    benchmark(_create)


@pytest.mark.benchmark(group="model-instantiation")
def test_coodie_model_instantiation(benchmark):
    from benchmarks.models_coodie import CoodieProduct

    data = {
        "id": uuid4(),
        "name": "InstBench",
        "brand": "BrandX",
        "category": "catA",
        "price": 19.99,
        "tags": ["a", "b", "c"],
        "description": "A benchmark product",
    }

    def _create():
        CoodieProduct(**data)

    benchmark(_create)


# ---------------------------------------------------------------------------
# Model serialization (model → dict for INSERT)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="model-serialization")
def test_cqlengine_model_serialization(benchmark):
    try:
        from benchmarks.models_cqlengine import CqlProduct
    except (ImportError, ModuleNotFoundError):
        pytest.skip("cqlengine not available")

    obj = CqlProduct(
        id=uuid4(),
        name="SerBench",
        brand="BrandX",
        category="catA",
        price=19.99,
        tags=["a", "b", "c"],
        description="A benchmark product",
    )

    def _serialize():
        # cqlengine serialisation path used during save
        {col.db_field_name: col.to_database(getattr(obj, col.column_name)) for col in obj._columns.values()}

    benchmark(_serialize)


@pytest.mark.benchmark(group="model-serialization")
def test_coodie_model_serialization(benchmark):
    from benchmarks.models_coodie import CoodieProduct

    doc = CoodieProduct(
        id=uuid4(),
        name="SerBench",
        brand="BrandX",
        category="catA",
        price=19.99,
        tags=["a", "b", "c"],
        description="A benchmark product",
    )

    def _serialize():
        doc.model_dump(exclude_none=False)

    benchmark(_serialize)
