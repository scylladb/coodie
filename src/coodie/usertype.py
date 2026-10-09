"""User-Defined Type (UDT) support for coodie.

Provides a ``UserType(BaseModel)`` base class for declaring Cassandra/ScyllaDB
UDTs using standard Pydantic type annotations.

Example::

    from coodie.usertype import UserType

    class Address(UserType):
        street: str
        city: str
        zipcode: int

        class Settings:
            __type_name__ = "address"   # optional — defaults to snake_case
            keyspace = "my_ks"
"""

from __future__ import annotations

import functools
import re
import typing
from typing import Any

from pydantic import BaseModel, model_validator

_SNAKE_RE1 = re.compile(r"(.)([A-Z][a-z]+)")
_SNAKE_RE2 = re.compile(r"([a-z0-9])([A-Z])")


@functools.lru_cache(maxsize=128)
def _snake_case(name: str) -> str:
    """Convert CamelCase class name to snake_case."""
    s1 = _SNAKE_RE1.sub(r"\1_\2", name)
    return _SNAKE_RE2.sub(r"\1_\2", s1).lower()


class UserType(BaseModel):
    """Base class for Cassandra/ScyllaDB User-Defined Types.

    Subclass this with standard Pydantic field annotations to define a UDT::

        class Address(UserType):
            street: str
            city: str
            zipcode: int
    """

    class Settings:
        __type_name__: str = ""
        keyspace: str = ""

    @model_validator(mode="before")
    @classmethod
    def _coerce_namedtuple(cls, v: Any) -> Any:
        """Convert a cassandra-driver namedtuple UDT value to a dict.

        When reading UDT columns back from the database, the cassandra-driver
        returns namedtuples rather than model instances.  This validator
        converts them to plain dicts so Pydantic can validate them normally.
        """
        if hasattr(v, "_asdict"):
            return v._asdict()
        return v

    @classmethod
    def type_name(cls) -> str:
        """Return the CQL type name for this UDT.

        Uses ``Settings.__type_name__`` if set, otherwise converts the
        class name to snake_case.
        """
        settings = getattr(cls, "Settings", None)
        if settings:
            override = getattr(settings, "__type_name__", None)
            if override:
                return override
        return _snake_case(cls.__name__)

    @classmethod
    def _get_keyspace(cls) -> str:
        """Return the keyspace from Settings or the default driver keyspace."""
        settings = getattr(cls, "Settings", None)
        if settings and getattr(settings, "keyspace", None):
            return settings.keyspace
        from coodie.drivers import get_driver

        driver = get_driver()
        ks = getattr(driver, "_default_keyspace", None)
        if ks:
            return ks
        from coodie.exceptions import InvalidQueryError

        raise InvalidQueryError("No keyspace configured")

    @classmethod
    def _get_field_cql_types(cls) -> list[tuple[str, str]]:
        """Return ``[(field_name, cql_type_str), ...]`` for this UDT's fields."""
        from coodie.types import python_type_to_cql_type_str
        from coodie.schema import _cached_type_hints

        hints = _cached_type_hints(cls)
        result: list[tuple[str, str]] = []
        for name, annotation in hints.items():
            if name.startswith("_") or name == "Settings":
                continue
            origin = typing.get_origin(annotation)
            if origin is typing.ClassVar:
                continue
            result.append((name, python_type_to_cql_type_str(annotation)))
        return result

    @classmethod
    def sync_type(cls, keyspace: str | None = None) -> list[str]:
        """Synchronously create or update this UDT in the database.

        Recursively syncs any nested UDT dependencies first.

        Returns:
            List of CQL statements that were executed.
        """
        from coodie.drivers import get_driver

        driver = get_driver()
        ks = keyspace or cls._get_keyspace()

        stmts: list[str] = []

        # Recursively sync nested UDT dependencies
        for dep in _extract_udt_dependencies(cls):
            if dep is not cls:
                stmts.extend(dep.sync_type(keyspace=ks))

        # Build and execute CREATE TYPE
        fields = cls._get_field_cql_types()
        from coodie.cql_builder import build_create_type

        create_stmt = build_create_type(cls.type_name(), ks, fields)
        driver.execute(create_stmt, [])
        stmts.append(create_stmt)

        return stmts

    @classmethod
    async def sync_type_async(cls, keyspace: str | None = None) -> list[str]:
        """Asynchronously create or update this UDT in the database.

        Recursively syncs any nested UDT dependencies first.

        Returns:
            List of CQL statements that were executed.
        """
        from coodie.drivers import get_driver

        driver = get_driver()
        ks = keyspace or cls._get_keyspace()

        stmts: list[str] = []

        # Recursively sync nested UDT dependencies
        for dep in _extract_udt_dependencies(cls):
            if dep is not cls:
                stmts.extend(await dep.sync_type_async(keyspace=ks))

        # Build and execute CREATE TYPE
        fields = cls._get_field_cql_types()
        from coodie.cql_builder import build_create_type

        create_stmt = build_create_type(cls.type_name(), ks, fields)
        await driver.execute_async(create_stmt, [])
        stmts.append(create_stmt)

        return stmts


def _is_usertype(cls: Any) -> bool:
    """Return ``True`` if *cls* is a ``UserType`` subclass (not ``UserType`` itself)."""
    return isinstance(cls, type) and issubclass(cls, UserType) and cls is not UserType


def _extract_udt_dependencies(udt_cls: type[UserType]) -> list[type[UserType]]:
    """Return UDT dependencies of *udt_cls* in topological (depth-first) order.

    Does **not** include *udt_cls* itself in the result.
    Raises ``InvalidQueryError`` if a circular dependency is detected.
    """
    from coodie.schema import _cached_type_hints
    from coodie.exceptions import InvalidQueryError

    result: list[type[UserType]] = []
    visited: set[type] = set()
    in_stack: set[type] = set()

    def _visit(cls: type[UserType]) -> None:
        if cls in visited:
            return
        if cls in in_stack:
            raise InvalidQueryError(f"Circular UDT dependency detected involving {cls.__name__}")
        in_stack.add(cls)

        # Scan fields for nested UserType references
        hints = _cached_type_hints(cls)
        for name, annotation in hints.items():
            if name.startswith("_") or name == "Settings":
                continue
            for dep in _find_udt_types_in_annotation(annotation):
                _visit(dep)

        in_stack.discard(cls)
        visited.add(cls)
        result.append(cls)

    # Scan the target class's fields
    hints = _cached_type_hints(udt_cls)
    for name, annotation in hints.items():
        if name.startswith("_") or name == "Settings":
            continue
        for dep in _find_udt_types_in_annotation(annotation):
            _visit(dep)

    return result


def _find_udt_types_in_annotation(annotation: Any) -> list[type[UserType]]:
    """Extract all ``UserType`` subclasses referenced in a type annotation."""
    from coodie.types import _UNION_ORIGINS

    if _is_usertype(annotation):
        return [annotation]

    origin = typing.get_origin(annotation)
    args = typing.get_args(annotation)

    if origin is typing.Annotated and args:
        return _find_udt_types_in_annotation(args[0])

    if origin in _UNION_ORIGINS and args:
        result: list[type[UserType]] = []
        for arg in args:
            if arg is not type(None):
                result.extend(_find_udt_types_in_annotation(arg))
        return result

    if origin in (list, set, dict, tuple, frozenset) and args:
        result = []
        for arg in args:
            result.extend(_find_udt_types_in_annotation(arg))
        return result

    return []


def extract_udt_classes(doc_cls: type) -> list[type[UserType]]:
    """Return all ``UserType`` subclasses used by a Document, topologically sorted.

    Scans the Document's type hints for UDT references (direct fields,
    inside collections, nested UDTs) and returns them in dependency order
    suitable for sequential ``sync_type()`` calls.
    """
    from coodie.schema import _cached_type_hints
    from coodie.exceptions import InvalidQueryError

    all_udts: list[type[UserType]] = []
    seen: set[type] = set()
    visited: set[type] = set()
    in_stack: set[type] = set()

    def _visit(cls: type[UserType]) -> None:
        if cls in visited:
            return
        if cls in in_stack:
            raise InvalidQueryError(f"Circular UDT dependency detected involving {cls.__name__}")
        in_stack.add(cls)

        hints = _cached_type_hints(cls)
        for name, annotation in hints.items():
            if name.startswith("_") or name == "Settings":
                continue
            for dep in _find_udt_types_in_annotation(annotation):
                _visit(dep)

        in_stack.discard(cls)
        visited.add(cls)
        if cls not in seen:
            all_udts.append(cls)
            seen.add(cls)

    hints = _cached_type_hints(doc_cls)
    for name, annotation in hints.items():
        if name.startswith("_") or name == "Settings":
            continue
        for udt_cls in _find_udt_types_in_annotation(annotation):
            _visit(udt_cls)

    return all_udts
