import functools
import re
import typing
from dataclasses import dataclass
from datetime import date, datetime, time as dt_time
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address
from types import UnionType
from typing import Any, Union
from uuid import UUID

from coodie.exceptions import InvalidQueryError
from coodie.fields import (
    Ascii,
    BigInt,
    Double,
    Duration,
    Frozen,
    SmallInt,
    Time,
    TimeUUID,
    TinyInt,
    VarInt,
    Vector,
)
from coodie.schema import _cached_type_hints


@dataclass(frozen=True, slots=True)
class CqlDuration:
    """Represents a CQL ``duration`` value.

    CQL durations have three components that cannot be losslessly represented
    by :class:`datetime.timedelta` because months have variable length.

    Args:
        months: Number of months.
        days: Number of days.
        nanoseconds: Number of nanoseconds.
    """

    months: int = 0
    days: int = 0
    nanoseconds: int = 0


_SCALAR_CQL_TYPES: dict[type, str] = {
    str: "text",
    int: "int",
    float: "float",
    bool: "boolean",
    bytes: "blob",
    UUID: "uuid",
    datetime: "timestamp",
    date: "date",
    dt_time: "time",
    Decimal: "decimal",
    IPv4Address: "inet",
    IPv6Address: "inet",
    CqlDuration: "duration",
}

# Annotation markers that override the CQL type of the base Python type.
_MARKER_CQL_OVERRIDES: dict[type, str] = {
    BigInt: "bigint",
    SmallInt: "smallint",
    TinyInt: "tinyint",
    VarInt: "varint",
    Double: "double",
    Ascii: "ascii",
    TimeUUID: "timeuuid",
    Time: "time",
    Duration: "duration",
}


# ``Optional[X]`` has origin ``typing.Union``; ``X | None`` has ``types.UnionType`` (distinct before 3.14).
_UNION_ORIGINS = (Union, UnionType)


def python_type_to_cql_type_str(annotation: Any) -> str:
    """Map a Python type annotation to its CQL type string."""
    origin = typing.get_origin(annotation)
    args = typing.get_args(annotation)

    # Annotated[X, ...] -> check for type markers, then unwrap to X
    if origin is typing.Annotated:
        has_frozen = False
        cql_override = None
        vec_dims: int | None = None
        for meta in args[1:]:
            if isinstance(meta, Frozen):
                has_frozen = True
            if isinstance(meta, Vector):
                dims = meta.dimensions
                if not isinstance(dims, int) or dims <= 0:
                    raise InvalidQueryError(f"Vector dimensions must be a positive integer, got {dims!r}")
                vec_dims = dims
            override = _MARKER_CQL_OVERRIDES.get(type(meta))
            if override is not None:
                cql_override = override
        if vec_dims is not None:
            base = args[0]
            base_origin = typing.get_origin(base)
            base_args = typing.get_args(base)
            is_float_list = base_origin is list and len(base_args) == 1 and base_args[0] is float
            if not is_float_list:
                raise InvalidQueryError(f"Vector annotation must wrap list[float], got {base!r}")
            return f"vector<float, {vec_dims}>"
        if cql_override is not None:
            return f"frozen<{cql_override}>" if has_frozen else cql_override
        inner = python_type_to_cql_type_str(args[0])
        if has_frozen and not inner.startswith("frozen<"):
            return f"frozen<{inner}>"
        return inner

    # Optional[X] == Union[X, None] -> unwrap to X
    if origin in _UNION_ORIGINS:
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return python_type_to_cql_type_str(non_none[0])
        raise InvalidQueryError(f"Cannot map Union type {annotation} to CQL")

    # list[X] -> list<cql_type>
    if origin is list:
        inner = python_type_to_cql_type_str(args[0]) if args else "text"
        return f"list<{inner}>"

    # set[X] -> set<cql_type>
    if origin is set:
        inner = python_type_to_cql_type_str(args[0]) if args else "text"
        return f"set<{inner}>"

    # frozenset[X] -> frozen<set<cql_type>>
    if origin is frozenset:
        inner = python_type_to_cql_type_str(args[0]) if args else "text"
        return f"frozen<set<{inner}>>"

    # dict[K, V] -> map<k_type, v_type>
    if origin is dict:
        k = python_type_to_cql_type_str(args[0]) if args else "text"
        v = python_type_to_cql_type_str(args[1]) if len(args) > 1 else "text"
        return f"map<{k}, {v}>"

    # tuple[X, Y, ...] -> tuple<x_type, y_type, ...>
    if origin is tuple:
        if args:
            inner = ", ".join(python_type_to_cql_type_str(a) for a in args)
            return f"tuple<{inner}>"
        return "tuple<text>"

    # Scalar lookup
    if annotation in _SCALAR_CQL_TYPES:
        return _SCALAR_CQL_TYPES[annotation]

    # UserType (BaseModel subclass) → frozen<type_name>
    if isinstance(annotation, type) and _is_user_type(annotation):
        return f"frozen<{_udt_type_name(annotation)}>"

    raise InvalidQueryError(f"Cannot map Python type {annotation!r} to a CQL type")


# ------------------------------------------------------------------
# UDT (UserType / BaseModel subclass) helpers
# ------------------------------------------------------------------

_CAMEL_TO_SNAKE_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def _is_user_type(cls: type) -> bool:
    """Return ``True`` if *cls* looks like a UDT (a BaseModel subclass)."""
    try:
        from pydantic import BaseModel
    except ImportError:  # pragma: no cover
        return False
    return isinstance(cls, type) and issubclass(cls, BaseModel) and cls is not BaseModel


def _udt_type_name(cls: type) -> str:
    """Derive the CQL type name for a UserType / BaseModel subclass.

    Uses ``Settings.__type_name__`` if defined, otherwise converts the
    class name to ``lower_snake_case``.
    """
    settings = getattr(cls, "Settings", None)
    if settings is not None:
        custom = getattr(settings, "__type_name__", None)
        if custom:
            return custom
    return _CAMEL_TO_SNAKE_RE.sub("_", cls.__name__).lower()


# Mapping from collection origin types to their empty factory
_COLLECTION_ORIGINS: dict[type, type] = {
    list: list,
    set: set,
    dict: dict,
    tuple: tuple,
    frozenset: frozenset,
}


def _unwrap_annotation(annotation: Any) -> Any:
    """Strip ``Annotated`` and ``Optional`` wrappers from a type annotation."""
    origin = typing.get_origin(annotation)
    args = typing.get_args(annotation)

    if origin is typing.Annotated:
        return _unwrap_annotation(args[0])

    if origin in _UNION_ORIGINS:
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return _unwrap_annotation(non_none[0])

    return annotation


@functools.lru_cache(maxsize=128)
def _collection_fields(cls: type) -> dict[str, type]:
    """Return ``{field_name: factory}`` for fields with collection types."""
    hints = _cached_type_hints(cls)
    result: dict[str, type] = {}
    for name, ann in hints.items():
        base = _unwrap_annotation(ann)
        origin = typing.get_origin(base) or base
        factory = _COLLECTION_ORIGINS.get(origin)  # type: ignore[arg-type]
        if factory is not None:
            result[name] = factory
    return result


def coerce_row_none_collections(doc_cls: type, row: dict[str, Any]) -> dict[str, Any]:
    """Replace ``None`` values for collection-typed fields with empty collections.

    Cassandra returns ``None`` for empty collections (``list``, ``set``, ``map``).
    Pydantic rejects ``None`` for non-optional collection fields, so we coerce
    them to the appropriate empty container *before* constructing the model.
    """
    coll_fields = _collection_fields(doc_cls)
    for key, factory in coll_fields.items():
        if key in row and row[key] is None:
            row[key] = factory()

    return row
