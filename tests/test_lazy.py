"""Tests for coodie.lazy.LazyDocument."""

from typing import Annotated
from uuid import UUID, uuid4

import pytest
from pydantic import Field

from coodie.fields import PrimaryKey
from coodie.lazy import LazyDocument


def _make_doc_cls(base_cls):
    class SimpleDoc(base_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        name: str = ""
        rating: int = 0

        class Settings:
            name = "simple_docs"
            keyspace = "test_ks"

    return SimpleDoc


def _make_collection_doc_cls(base_cls):
    class CollDoc(base_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        tags: list[str] = Field(default_factory=list)

        class Settings:
            name = "coll_docs"
            keyspace = "test_ks"

    return CollDoc


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
def SimpleDoc(document_cls):
    return _make_doc_cls(document_cls)


@pytest.fixture
def CollDoc(document_cls):
    return _make_collection_doc_cls(document_cls)


# ------------------------------------------------------------------
# Construction
# ------------------------------------------------------------------


def test_lazy_document_no_parse_on_init(SimpleDoc):
    raw = {"id": uuid4(), "name": "Alice", "rating": 5}
    lazy = LazyDocument(SimpleDoc, raw)
    assert lazy._parsed is None


def test_lazy_document_repr_before_parse(SimpleDoc):
    lazy = LazyDocument(SimpleDoc, {"id": uuid4(), "name": "A", "rating": 1})
    r = repr(lazy)
    assert "parsed=False" in r
    assert "SimpleDoc" in r


# ------------------------------------------------------------------
# Field access triggers parsing
# ------------------------------------------------------------------


def test_lazy_document_field_access(SimpleDoc):
    pid = uuid4()
    lazy = LazyDocument(SimpleDoc, {"id": pid, "name": "Bob", "rating": 10})
    assert lazy._parsed is None
    assert lazy.name == "Bob"
    assert lazy._parsed is not None
    assert lazy.id == pid
    assert lazy.rating == 10


def test_lazy_document_repr_after_parse(SimpleDoc):
    lazy = LazyDocument(SimpleDoc, {"id": uuid4(), "name": "C", "rating": 3})
    _ = lazy.name  # trigger parse
    r = repr(lazy)
    assert "LazyDocument(" in r
    assert "parsed=False" not in r


# ------------------------------------------------------------------
# Collection coercion
# ------------------------------------------------------------------


def test_lazy_document_none_collection_coerced(CollDoc):
    pid = uuid4()
    lazy = LazyDocument(CollDoc, {"id": pid, "tags": None})
    assert lazy.tags == []


def test_lazy_document_collection_preserved(CollDoc):
    pid = uuid4()
    lazy = LazyDocument(CollDoc, {"id": pid, "tags": ["a", "b"]})
    assert lazy.tags == ["a", "b"]


# ------------------------------------------------------------------
# Equality
# ------------------------------------------------------------------


def test_lazy_document_eq_with_lazy(SimpleDoc):
    pid = uuid4()
    a = LazyDocument(SimpleDoc, {"id": pid, "name": "X", "rating": 1})
    b = LazyDocument(SimpleDoc, {"id": pid, "name": "X", "rating": 1})
    assert a == b


def test_lazy_document_eq_with_doc(SimpleDoc):
    pid = uuid4()
    lazy = LazyDocument(SimpleDoc, {"id": pid, "name": "X", "rating": 1})
    doc = SimpleDoc(id=pid, name="X", rating=1)
    assert lazy == doc


# ------------------------------------------------------------------
# _resolve caches
# ------------------------------------------------------------------


def test_lazy_document_resolve_caches(SimpleDoc):
    lazy = LazyDocument(SimpleDoc, {"id": uuid4(), "name": "D", "rating": 2})
    doc1 = lazy._resolve()
    doc2 = lazy._resolve()
    assert doc1 is doc2
