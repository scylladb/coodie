"""Unit tests for coodie vector column support.

Covers:
- Type mapping: ``Vector(dimensions=N)`` → ``vector<float, N>``
- DDL generation: ``build_create_vector_index``
- ANN query builder: ``build_select`` with ``ann_of``
- QuerySet: ``order_by_ann`` for both sync and async variants
- Dimension validation in ``save()``
- ``ColumnDefinition`` defaults for vector fields
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID, uuid4

import pytest
from pydantic import Field

from coodie.cql_builder import _select_cql_cache, build_create_vector_index, build_select
from coodie.exceptions import InvalidQueryError
from coodie.fields import ClusteringKey, Indexed, PrimaryKey, Static, Vector, VectorIndex
from coodie.schema import ColumnDefinition, build_schema
from coodie.types import python_type_to_cql_type_str
from tests.conftest import _maybe_await

# ------------------------------------------------------------------
# Type mapping tests
# ------------------------------------------------------------------


def test_vector_type_mapping():
    ann = Annotated[list[float], Vector(dimensions=384)]
    assert python_type_to_cql_type_str(ann) == "vector<float, 384>"


def test_vector_type_mapping_small():
    ann = Annotated[list[float], Vector(dimensions=16)]
    assert python_type_to_cql_type_str(ann) == "vector<float, 16>"


def test_vector_type_mapping_one_dim():
    ann = Annotated[list[float], Vector(dimensions=1)]
    assert python_type_to_cql_type_str(ann) == "vector<float, 1>"


def test_plain_list_float_still_maps_to_list():
    """Without Vector annotation, list[float] should still emit list<float>."""
    assert python_type_to_cql_type_str(list[float]) == "list<float>"


# ------------------------------------------------------------------
# Schema DDL tests
# ------------------------------------------------------------------


def test_build_schema_vector_column():
    from coodie.sync.document import Document

    class VecModel(Document):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        embedding: Annotated[list[float], Vector(dimensions=8), VectorIndex(similarity_function="COSINE")]

        class Settings:
            name = "vec_model"
            keyspace = "test_ks"

    schema = build_schema(VecModel)
    emb_col = next(c for c in schema if c.name == "embedding")
    assert emb_col.cql_type == "vector<float, 8>"
    assert emb_col.vector_index is True
    assert emb_col.vector_index_options == {"similarity_function": "COSINE"}


def test_build_schema_vector_without_index():
    from coodie.sync.document import Document

    class VecNoIdx(Document):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        embedding: Annotated[list[float], Vector(dimensions=4)]

        class Settings:
            name = "vec_no_idx"
            keyspace = "test_ks"

    schema = build_schema(VecNoIdx)
    emb_col = next(c for c in schema if c.name == "embedding")
    assert emb_col.cql_type == "vector<float, 4>"
    assert emb_col.vector_index is False
    assert emb_col.vector_index_options is None


# ------------------------------------------------------------------
# build_create_vector_index tests
# ------------------------------------------------------------------


def test_build_create_vector_index_with_cosine():
    col = ColumnDefinition(
        name="embedding",
        cql_type="vector<float, 384>",
        vector_index=True,
        vector_index_options={"similarity_function": "COSINE"},
    )
    cql = build_create_vector_index("products", "ks", col)
    assert "CREATE CUSTOM INDEX IF NOT EXISTS" in cql
    assert "products_embedding_idx" in cql
    assert "USING 'vector_index'" in cql
    assert "WITH OPTIONS" in cql
    assert "'similarity_function': 'COSINE'" in cql


def test_build_create_vector_index_with_euclidean():
    col = ColumnDefinition(
        name="vec",
        cql_type="vector<float, 3>",
        vector_index=True,
        vector_index_options={"similarity_function": "EUCLIDEAN"},
    )
    cql = build_create_vector_index("items", "ks", col)
    assert "'similarity_function': 'EUCLIDEAN'" in cql


def test_build_create_vector_index_no_options():
    col = ColumnDefinition(
        name="embedding",
        cql_type="vector<float, 3>",
        vector_index=True,
    )
    cql = build_create_vector_index("products", "ks", col)
    assert "USING 'vector_index'" in cql
    assert "WITH OPTIONS" not in cql


# ------------------------------------------------------------------
# ANN query tests
# ------------------------------------------------------------------


def test_build_select_ann_of():
    _select_cql_cache.clear()
    cql, params = build_select(
        "products",
        "ks",
        ann_of=("embedding", [0.1, 0.2, 0.3]),
        limit=5,
    )
    assert 'ORDER BY "embedding" ANN OF ?' in cql
    assert "LIMIT 5" in cql
    assert params == [[0.1, 0.2, 0.3]]


def test_build_select_ann_with_where():
    _select_cql_cache.clear()
    cql, params = build_select(
        "products",
        "ks",
        where=[("category", "=", "electronics")],
        ann_of=("embedding", [0.1, 0.2]),
        limit=10,
    )
    assert 'WHERE "category" = ?' in cql
    assert 'ORDER BY "embedding" ANN OF ?' in cql
    assert params == ["electronics", [0.1, 0.2]]


def test_build_select_ann_caching():
    _select_cql_cache.clear()
    cql1, p1 = build_select("t", "ks", ann_of=("emb", [0.1, 0.2]), limit=5)
    cql2, p2 = build_select("t", "ks", ann_of=("emb", [0.3, 0.4]), limit=5)
    assert cql1 == cql2
    assert p1 == [[0.1, 0.2]]
    assert p2 == [[0.3, 0.4]]


def test_build_select_no_ann_still_works():
    _select_cql_cache.clear()
    cql, params = build_select("products", "ks", limit=5)
    assert "ANN OF" not in cql
    assert params == []


# ------------------------------------------------------------------
# QuerySet order_by_ann tests
# ------------------------------------------------------------------


@pytest.fixture(params=["sync", "async"])
def variant(request):
    return request.param


@pytest.fixture
def document_cls(variant):
    if variant == "sync":
        from coodie.sync.document import Document

        return Document
    from coodie.aio.document import Document

    return Document


@pytest.fixture
def queryset_cls(variant):
    if variant == "sync":
        from coodie.sync.query import QuerySet

        return QuerySet
    from coodie.aio.query import QuerySet

    return QuerySet


@pytest.fixture
def EmbeddingDoc(document_cls):
    class EmbeddingDoc(document_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        name: str = ""
        embedding: Annotated[list[float], Vector(dimensions=3)] = Field(default_factory=list)

        class Settings:
            name = "embedding_docs"
            keyspace = "test_ks"

    return EmbeddingDoc


def test_order_by_ann_returns_new_queryset(EmbeddingDoc, queryset_cls, registered_mock_driver):
    qs = queryset_cls(EmbeddingDoc)
    qs2 = qs.order_by_ann("embedding", [0.1, 0.2, 0.3])
    assert qs is not qs2
    assert qs2._ann_of_val == ("embedding", [0.1, 0.2, 0.3])


async def test_order_by_ann_generates_correct_cql(EmbeddingDoc, queryset_cls, registered_mock_driver):
    registered_mock_driver.set_return_rows([])
    qs = queryset_cls(EmbeddingDoc).order_by_ann("embedding", [0.1, 0.2, 0.3]).limit(5)
    await _maybe_await(qs.all)
    cql, _ = registered_mock_driver.executed[-1]
    assert 'ORDER BY "embedding" ANN OF ?' in cql
    assert "LIMIT 5" in cql


def test_order_by_ann_does_not_affect_original(EmbeddingDoc, queryset_cls, registered_mock_driver):
    qs = queryset_cls(EmbeddingDoc)
    _ = qs.order_by_ann("embedding", [0.1, 0.2, 0.3])
    assert qs._ann_of_val is None


# ------------------------------------------------------------------
# Dimension validation tests
# ------------------------------------------------------------------


@pytest.fixture
def VecDoc(document_cls):
    class VecDoc(document_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        embedding: Annotated[list[float], Vector(dimensions=3)] = Field(default_factory=list)

        class Settings:
            name = "vec_docs"
            keyspace = "test_ks"

    return VecDoc


async def test_save_validates_vector_dimensions(VecDoc, registered_mock_driver):
    doc = VecDoc(embedding=[0.1, 0.2])
    with pytest.raises(InvalidQueryError, match="expects 3 dimensions, got 2"):
        await _maybe_await(doc.save)


async def test_save_allows_correct_dimensions(VecDoc, registered_mock_driver):
    doc = VecDoc(embedding=[0.1, 0.2, 0.3])
    await _maybe_await(doc.save)
    assert len(registered_mock_driver.executed) == 1


async def test_save_allows_empty_vector(VecDoc, registered_mock_driver):
    """Empty list (len 0) is rejected because 0 != 3."""
    doc = VecDoc(embedding=[])
    with pytest.raises(InvalidQueryError, match="expects 3 dimensions, got 0"):
        await _maybe_await(doc.save)


async def test_save_validates_too_many_dimensions(VecDoc, registered_mock_driver):
    doc = VecDoc(embedding=[0.1, 0.2, 0.3, 0.4])
    with pytest.raises(InvalidQueryError, match="expects 3 dimensions, got 4"):
        await _maybe_await(doc.save)


# ------------------------------------------------------------------
# ColumnDefinition defaults for vector fields
# ------------------------------------------------------------------


def test_column_definition_vector_defaults():
    col = ColumnDefinition(name="emb", cql_type="vector<float, 3>")
    assert col.vector_index is False
    assert col.vector_index_options is None


def test_column_definition_vector_with_options():
    col = ColumnDefinition(
        name="emb",
        cql_type="vector<float, 3>",
        vector_index=True,
        vector_index_options={"similarity_function": "DOT_PRODUCT"},
    )
    assert col.vector_index is True
    assert col.vector_index_options == {"similarity_function": "DOT_PRODUCT"}


# ------------------------------------------------------------------
# New validation tests (from review feedback)
# ------------------------------------------------------------------


def test_vector_invalid_dimensions_zero():
    """Vector dimensions must be > 0."""
    ann = Annotated[list[float], Vector(dimensions=0)]
    with pytest.raises(InvalidQueryError, match="positive integer"):
        python_type_to_cql_type_str(ann)


def test_vector_invalid_dimensions_negative():
    """Vector dimensions must be > 0 — negative dimensions are also rejected."""
    ann = Annotated[list[float], Vector(dimensions=-1)]
    with pytest.raises(InvalidQueryError, match="positive integer"):
        python_type_to_cql_type_str(ann)


def test_vector_invalid_base_type():
    """Vector must wrap list[float]."""
    ann = Annotated[list[int], Vector(dimensions=3)]
    with pytest.raises(InvalidQueryError, match="list\\[float\\]"):
        python_type_to_cql_type_str(ann)


def test_vector_index_on_non_vector_column():
    """VectorIndex on a non-vector column should raise InvalidQueryError."""
    from coodie.sync.document import Document

    class BadModel(Document):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        name: Annotated[str, VectorIndex(similarity_function="COSINE")]

        class Settings:
            name = "bad_model"
            keyspace = "test_ks"

    with pytest.raises(InvalidQueryError, match="VectorIndex can only be applied to vector columns"):
        build_schema(BadModel)


def test_vector_index_combined_with_indexed():
    """VectorIndex and Indexed() on same column should raise InvalidQueryError."""
    from coodie.sync.document import Document

    class BadModel2(Document):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        embedding: Annotated[
            list[float],
            Vector(dimensions=3),
            Indexed(),
            VectorIndex(similarity_function="COSINE"),
        ]

        class Settings:
            name = "bad_model2"
            keyspace = "test_ks"

    with pytest.raises(InvalidQueryError, match="Cannot apply both Indexed.*VectorIndex"):
        build_schema(BadModel2)


def test_vector_index_on_primary_key():
    """VectorIndex on a primary key column should raise InvalidQueryError."""
    from coodie.sync.document import Document

    class BadModel3(Document):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        embedding: Annotated[
            list[float],
            PrimaryKey(partition_key_index=1),
            Vector(dimensions=3),
            VectorIndex(similarity_function="COSINE"),
        ]

        class Settings:
            name = "bad_model3"
            keyspace = "test_ks"

    with pytest.raises(InvalidQueryError, match="VectorIndex cannot be applied to a primary key"):
        build_schema(BadModel3)


def test_vector_index_on_clustering_key():
    """VectorIndex on a clustering key column should raise InvalidQueryError."""
    from coodie.sync.document import Document

    class BadModel4(Document):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        embedding: Annotated[
            list[float],
            ClusteringKey(),
            Vector(dimensions=3),
            VectorIndex(similarity_function="COSINE"),
        ]

        class Settings:
            name = "bad_model4"
            keyspace = "test_ks"

    with pytest.raises(InvalidQueryError, match="VectorIndex cannot be applied to a clustering key"):
        build_schema(BadModel4)


def test_vector_index_on_static_column():
    """VectorIndex on a static column should raise InvalidQueryError."""
    from coodie.sync.document import Document

    class BadModel5(Document):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        embedding: Annotated[
            list[float],
            Static(),
            Vector(dimensions=3),
            VectorIndex(similarity_function="COSINE"),
        ]

        class Settings:
            name = "bad_model5"
            keyspace = "test_ks"

    with pytest.raises(InvalidQueryError, match="VectorIndex cannot be applied to a static"):
        build_schema(BadModel5)


async def test_paged_all_with_ann_executes_query(EmbeddingDoc, queryset_cls, registered_mock_driver):
    """paged_all() combined with order_by_ann() should execute the ANN query and return a PagedResult.

    ScyllaDB ANN queries do not support cursor-based pagination, so paging_state is always None.
    """
    from coodie.results import PagedResult

    registered_mock_driver.set_return_rows([])
    qs = queryset_cls(EmbeddingDoc).order_by_ann("embedding", [0.1, 0.2, 0.3]).limit(5)
    result = await _maybe_await(qs.paged_all)
    assert isinstance(result, PagedResult)
    assert result.paging_state is None
    # Check that the ANN CQL was executed
    cql, _ = registered_mock_driver.executed[-1]
    assert 'ORDER BY "embedding" ANN OF ?' in cql


def test_ann_order_by_cache_key_ignores_order_by():
    """Cache key for ANN queries should not vary with order_by."""
    _select_cql_cache.clear()
    cql1, _ = build_select("t", "ks", ann_of=("emb", [0.1]), order_by=["name"])
    cql2, _ = build_select("t", "ks", ann_of=("emb", [0.2]), order_by=["other"])
    # Same CQL structure, and cache key ignores order_by when ann_of is present.
    assert cql1 == cql2
    assert len(_select_cql_cache) == 1


# ------------------------------------------------------------------
# _warn_if_sai_unsupported() helper tests
# ------------------------------------------------------------------


def _make_invalid_request(msg: str):
    """Return a best-effort InvalidRequest-like exception for testing."""
    try:
        from cassandra import InvalidRequest  # type: ignore[import-untyped]

        exc = InvalidRequest.__new__(InvalidRequest)
        exc.args = (f'code=2200 [Invalid query] message="{msg}"',)
        return exc
    except ImportError:
        return ValueError(msg)


def test_warn_if_sai_unsupported_catches_non_supported_custom_class(recwarn):
    """'Non-supported custom class' pattern emits a warning and does not raise."""
    from coodie.drivers.cassandra import CassandraDriver

    driver = object.__new__(CassandraDriver)
    exc = _make_invalid_request("Non-supported custom class: 'vector_index'")
    driver._warn_if_sai_unsupported(exc)
    assert len(recwarn) == 1
    assert "Vector index creation skipped" in str(recwarn[0].message)


def test_warn_if_sai_unsupported_catches_tablets_required(recwarn):
    """'use tablets' pattern emits a warning and does not raise (ScyllaDB tablets requirement)."""
    from coodie.drivers.cassandra import CassandraDriver

    driver = object.__new__(CassandraDriver)
    exc = _make_invalid_request(
        "Vector index requires the base table's keyspace to use tablets. "
        "Please alter the keyspace to use tablets and try again."
    )
    driver._warn_if_sai_unsupported(exc)
    assert len(recwarn) == 1
    assert "Vector index creation skipped" in str(recwarn[0].message)


def test_warn_if_sai_unsupported_reraises_real_errors():
    """Unrecognised InvalidRequest errors are re-raised."""
    from coodie.drivers.cassandra import CassandraDriver

    driver = object.__new__(CassandraDriver)
    exc = _make_invalid_request("Keyspace 'missing_ks' does not exist")
    with pytest.raises(Exception, match="missing_ks"):
        driver._warn_if_sai_unsupported(exc)
