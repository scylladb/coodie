from __future__ import annotations

from datetime import date, datetime, time as dt_time
from decimal import Decimal
from ipaddress import IPv4Address
from typing import Annotated, Optional
from uuid import UUID

import pytest

from coodie.exceptions import InvalidQueryError
from coodie.fields import (
    Ascii,
    BigInt,
    Double,
    Duration,
    Frozen,
    PrimaryKey,
    SmallInt,
    Time,
    TimeUUID,
    TinyInt,
    VarInt,
    Vector,
    VectorIndex,
)
from coodie.types import CqlDuration, python_type_to_cql_type_str, coerce_row_none_collections


# ---- python_type_to_cql_type_str: basic types ----


@pytest.mark.parametrize(
    "python_type, expected_cql",
    [
        pytest.param(str, "text", id="str-to-text"),
        pytest.param(int, "int", id="int-to-int"),
        pytest.param(float, "float", id="float-to-float"),
        pytest.param(bool, "boolean", id="bool-to-boolean"),
        pytest.param(bytes, "blob", id="bytes-to-blob"),
        pytest.param(UUID, "uuid", id="uuid-to-uuid"),
        pytest.param(datetime, "timestamp", id="datetime-to-timestamp"),
        pytest.param(date, "date", id="date-to-date"),
        pytest.param(Decimal, "decimal", id="decimal-to-decimal"),
        pytest.param(IPv4Address, "inet", id="ipv4-to-inet"),
        pytest.param(dt_time, "time", id="time-to-time"),
        pytest.param(list[str], "list<text>", id="list-str"),
        pytest.param(set[int], "set<int>", id="set-int"),
        pytest.param(dict[str, int], "map<text, int>", id="dict-str-int"),
        pytest.param(frozenset[str], "frozen<set<text>>", id="frozenset-str"),
        pytest.param(frozenset[int], "frozen<set<int>>", id="frozenset-int"),
        pytest.param(Optional[str], "text", id="optional-str"),
        pytest.param(str | None, "text", id="pep604-optional-str"),
        pytest.param(list[int] | None, "list<int>", id="pep604-optional-list"),
        pytest.param(dict[str, int | None], "map<text, int>", id="pep604-optional-nested"),
        pytest.param(Annotated[UUID, PrimaryKey()], "uuid", id="annotated-unwraps"),
    ],
)
def test_python_type_to_cql_type_str(python_type, expected_cql):
    assert python_type_to_cql_type_str(python_type) == expected_cql


# ---- python_type_to_cql_type_str: extended-type markers ----


@pytest.mark.parametrize(
    "annotated_type, expected_cql",
    [
        pytest.param(Annotated[int, BigInt()], "bigint", id="bigint"),
        pytest.param(Annotated[int, SmallInt()], "smallint", id="smallint"),
        pytest.param(Annotated[int, TinyInt()], "tinyint", id="tinyint"),
        pytest.param(Annotated[int, VarInt()], "varint", id="varint"),
        pytest.param(Annotated[float, Double()], "double", id="double"),
        pytest.param(Annotated[str, Ascii()], "ascii", id="ascii"),
        pytest.param(Annotated[UUID, TimeUUID()], "timeuuid", id="timeuuid"),
        pytest.param(Annotated[dt_time, Time()], "time", id="time-marker"),
    ],
)
def test_extended_type_marker(annotated_type, expected_cql):
    assert python_type_to_cql_type_str(annotated_type) == expected_cql


# ---- python_type_to_cql_type_str: frozen types ----


@pytest.mark.parametrize(
    "annotated_type, expected_cql",
    [
        pytest.param(Annotated[list[str], Frozen()], "frozen<list<text>>", id="frozen-list"),
        pytest.param(Annotated[set[int], Frozen()], "frozen<set<int>>", id="frozen-set"),
        pytest.param(
            Annotated[dict[str, int], Frozen()],
            "frozen<map<text, int>>",
            id="frozen-map",
        ),
        pytest.param(
            Annotated[tuple[str, int], Frozen()],
            "frozen<tuple<text, int>>",
            id="frozen-tuple",
        ),
    ],
)
def test_frozen_type(annotated_type, expected_cql):
    assert python_type_to_cql_type_str(annotated_type) == expected_cql


# ---- python_type_to_cql_type_str: frozen + indexed combination ----


def test_frozen_collection_with_index():
    """Frozen collection combined with Indexed should preserve the CQL type string."""
    from coodie.fields import Indexed

    assert python_type_to_cql_type_str(Annotated[list[str], Frozen(), Indexed()]) == "frozen<list<text>>"
    assert python_type_to_cql_type_str(Annotated[set[int], Frozen(), Indexed()]) == "frozen<set<int>>"
    assert python_type_to_cql_type_str(Annotated[dict[str, int], Frozen(), Indexed()]) == "frozen<map<text, int>>"


def test_unsupported_type_raises():
    with pytest.raises(InvalidQueryError):
        python_type_to_cql_type_str(object)


# ---- python_type_to_cql_type_str: UDT (BaseModel subclass) ----


def test_usertype_definition_without_connection():
    """A UserType (BaseModel) subclass and a Document referencing it can be
    defined before any driver is registered, and python_type_to_cql_type_str
    resolves the frozen UDT type string.
    """
    from pydantic import BaseModel

    class Address(BaseModel):
        street: str
        city: str

    class Order(BaseModel):
        id: Annotated[UUID, PrimaryKey()]
        shipping: Address

        class Settings:
            name = "orders"
            keyspace = "test_ks"

    # Class definition did not raise — no connection required
    assert python_type_to_cql_type_str(Address) == "frozen<address>"
    assert python_type_to_cql_type_str(Annotated[Address, Frozen()]) == "frozen<address>"


def test_usertype_custom_type_name():
    """Settings.__type_name__ overrides the derived CQL type name."""
    from pydantic import BaseModel

    class MyAddress(BaseModel):
        street: str

        class Settings:
            __type_name__ = "custom_addr"

    assert python_type_to_cql_type_str(MyAddress) == "frozen<custom_addr>"


def test_no_cqlengine_import():
    import sys

    assert "cassandra.cqlengine" not in sys.modules


def test_marker_with_primary_key():
    """Marker should work alongside other annotations like PrimaryKey."""
    assert python_type_to_cql_type_str(Annotated[int, PrimaryKey(), BigInt()]) == "bigint"


def test_frozen_with_marker():
    """Frozen combined with a type marker should wrap the marker's CQL type."""
    assert python_type_to_cql_type_str(Annotated[UUID, Frozen(), TimeUUID()]) == "frozen<timeuuid>"


# ---- coerce_row_none_collections tests ----


class _FakeDoc:
    """Minimal stand-in with type annotations for coercion tests."""

    tags: list[str]
    labels: set[int]
    meta: dict[str, int]
    name: str
    description: Optional[str]


@pytest.mark.parametrize(
    "field, input_val, expected",
    [
        pytest.param("tags", None, [], id="none-list-to-empty"),
        pytest.param("labels", None, set(), id="none-set-to-empty"),
        pytest.param("meta", None, {}, id="none-dict-to-empty"),
        pytest.param("tags", ["a", "b"], ["a", "b"], id="non-none-unchanged"),
        pytest.param("description", None, None, id="scalar-none-unchanged"),
    ],
)
def test_coerce_row_none_collections(field, input_val, expected):
    row = {field: input_val}
    if field == "tags":
        row.setdefault("name", "x")
    result = coerce_row_none_collections(_FakeDoc, row)
    assert result[field] == expected


def test_coerce_annotated_collection():
    """Collections wrapped in Annotated should also be coerced."""

    class _AnnotatedDoc:
        tags: Annotated[list[str], PrimaryKey()]

    row: dict = {"tags": None}
    result = coerce_row_none_collections(_AnnotatedDoc, row)
    assert result["tags"] == []


def test_coerce_optional_collection():
    """Optional[list[str]] with None should be coerced to empty list."""

    class _OptionalListDoc:
        tags: Optional[list[str]]

    row: dict = {"tags": None}
    result = coerce_row_none_collections(_OptionalListDoc, row)
    assert result["tags"] == []


def test_coerce_pep604_optional_collection():
    """list[str] | None with None should be coerced to empty list."""

    class _Pep604ListDoc:
        tags: list[str] | None

    result = coerce_row_none_collections(_Pep604ListDoc, {"tags": None})
    assert result["tags"] == []


# ---- _collection_fields caching tests ----


def test_collection_fields_cached():
    """_collection_fields should return the same object on repeated calls."""
    from coodie.types import _collection_fields

    result1 = _collection_fields(_FakeDoc)
    result2 = _collection_fields(_FakeDoc)
    assert result1 is result2


def test_collection_fields_detects_collections():
    """_collection_fields should identify all collection-typed fields."""
    from coodie.types import _collection_fields

    fields = _collection_fields(_FakeDoc)
    assert "tags" in fields
    assert "labels" in fields
    assert "meta" in fields
    assert "name" not in fields
    assert "description" not in fields


def test_coerce_skips_absent_keys():
    """coerce_row_none_collections should not add keys absent from the row."""
    row: dict = {"name": "test", "tags": None}
    result = coerce_row_none_collections(_FakeDoc, row)
    assert "labels" not in result
    assert "meta" not in result
    assert result["tags"] == []  # present key with None is still coerced


# ---- CqlDuration dataclass tests ----


def test_cql_duration_defaults():
    d = CqlDuration()
    assert d.months == 0
    assert d.days == 0
    assert d.nanoseconds == 0


def test_cql_duration_custom_values():
    d = CqlDuration(months=1, days=2, nanoseconds=3_000_000_000)
    assert d.months == 1
    assert d.days == 2
    assert d.nanoseconds == 3_000_000_000


def test_cql_duration_immutable():
    d = CqlDuration(months=1)
    with pytest.raises(AttributeError):
        d.months = 2  # type: ignore[misc]


def test_cql_duration_scalar_mapping():
    assert python_type_to_cql_type_str(CqlDuration) == "duration"


def test_duration_marker():
    assert python_type_to_cql_type_str(Annotated[CqlDuration, Duration()]) == "duration"


def test_duration_marker_with_primary_key():
    assert python_type_to_cql_type_str(Annotated[CqlDuration, PrimaryKey(), Duration()]) == "duration"


# ---- Vector type mapping tests ----


def test_vector_marker():
    assert python_type_to_cql_type_str(Annotated[list[float], Vector(dimensions=5)]) == "vector<float, 5>"


def test_vector_marker_different_dimensions():
    assert python_type_to_cql_type_str(Annotated[list[float], Vector(dimensions=128)]) == "vector<float, 128>"


def test_vector_marker_with_primary_key():
    """Vector marker should work alongside PrimaryKey annotation."""
    assert python_type_to_cql_type_str(Annotated[list[float], PrimaryKey(), Vector(dimensions=3)]) == "vector<float, 3>"


def test_vector_marker_with_vector_index():
    """VectorIndex annotation should not affect type mapping."""
    assert (
        python_type_to_cql_type_str(Annotated[list[float], Vector(dimensions=5), VectorIndex()]) == "vector<float, 5>"
    )
