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

import logging
import re
import typing
from typing import Any

from pydantic import BaseModel, model_validator

logger = logging.getLogger("coodie")


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
        class name to snake_case (``HTTPAddress`` -> ``http_address``).
        """
        from coodie.types import _udt_type_name

        return _udt_type_name(cls)

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
        from coodie.schema import _cached_type_hints
        from coodie.types import python_type_to_cql_type_str

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
    def sync_type(cls, keyspace: str | None = None, dry_run: bool = False) -> list[str]:
        """Synchronously create or update this UDT in the database.

        Syncs nested UDT dependencies first.  Fields missing from the
        database type are added with ``ALTER TYPE ... ADD``; removed fields
        and type changes are only logged (UDT fields are never dropped or
        altered).

        Returns:
            List of DDL statements that were (or, with ``dry_run``, would be)
            executed.
        """
        from coodie.drivers import get_driver

        driver = get_driver()
        ks = keyspace or cls._get_keyspace()
        stmts: list[str] = []
        for udt in [*_extract_udt_dependencies(cls), cls]:
            stmts.extend(udt._sync_one(driver, ks, dry_run))
        return stmts

    @classmethod
    async def sync_type_async(cls, keyspace: str | None = None, dry_run: bool = False) -> list[str]:
        """Async version of :meth:`sync_type`."""
        from coodie.drivers import get_driver

        driver = get_driver()
        ks = keyspace or cls._get_keyspace()
        stmts: list[str] = []
        for udt in [*_extract_udt_dependencies(cls), cls]:
            stmts.extend(await udt._sync_one_async(driver, ks, dry_run))
        return stmts

    @classmethod
    def _sync_one(cls, driver: Any, keyspace: str, dry_run: bool = False) -> list[str]:
        """Create or extend this UDT only (no dependencies)."""
        from coodie.cql_builder import build_create_type

        rows = driver.execute(_SELECT_TYPE_FIELDS, [keyspace, cls.type_name()])
        if rows:
            stmts = cls._plan_alters(keyspace, rows)
        else:
            stmts = [build_create_type(cls.type_name(), keyspace, cls._get_field_cql_types())]
        if not dry_run:
            for stmt in stmts:
                driver.execute(stmt, [])
        return stmts

    @classmethod
    async def _sync_one_async(cls, driver: Any, keyspace: str, dry_run: bool = False) -> list[str]:
        """Async version of :meth:`_sync_one`."""
        from coodie.cql_builder import build_create_type

        rows = await driver.execute_async(_SELECT_TYPE_FIELDS, [keyspace, cls.type_name()])
        if rows:
            stmts = cls._plan_alters(keyspace, rows)
        else:
            stmts = [build_create_type(cls.type_name(), keyspace, cls._get_field_cql_types())]
        if not dry_run:
            for stmt in stmts:
                await driver.execute_async(stmt, [])
        return stmts

    @classmethod
    def _plan_alters(cls, keyspace: str, rows: list[dict[str, Any]]) -> list[str]:
        """Diff model fields against a ``system_schema.types`` row.

        Returns ``ALTER TYPE ... ADD`` statements for new fields and logs a
        warning for removed fields or changed field types.
        """
        from coodie.cql_builder import build_alter_type_add

        type_name = cls.type_name()
        existing = dict(zip(rows[0]["field_names"] or [], rows[0]["field_types"] or [], strict=False))
        model = dict(cls._get_field_cql_types())
        alters: list[str] = []
        for name, cql_type in model.items():
            if name not in existing:
                alters.append(build_alter_type_add(type_name, keyspace, name, cql_type))
            elif _normalize_cql_type(existing[name]) != _normalize_cql_type(cql_type):
                logger.warning(
                    "UDT %s.%s field %r has type %s in the database but %s in the model; not altering",
                    keyspace,
                    type_name,
                    name,
                    existing[name],
                    cql_type,
                )
        removed = existing.keys() - model.keys()
        if removed:
            logger.warning(
                "Schema drift detected: fields %s exist in UDT %s.%s but are not defined in the model",
                removed,
                keyspace,
                type_name,
            )
        return alters


_SELECT_TYPE_FIELDS = (
    "SELECT field_names, field_types FROM system_schema.types WHERE keyspace_name = ? AND type_name = ?"
)


def _normalize_cql_type(cql_type: str) -> str:
    """Normalize a CQL type string for comparison.

    ponytail: drops ``frozen<`` and every ``>`` instead of parsing, since the
    server may freeze collections inside UDTs; parse properly if it ever
    yields a false match.
    """
    return re.sub(r"\s|frozen<|>", "", cql_type.lower())


def _is_usertype(cls: Any) -> bool:
    """Return ``True`` if *cls* is a ``UserType`` subclass (not ``UserType`` itself)."""
    return isinstance(cls, type) and issubclass(cls, UserType) and cls is not UserType


def _extract_udt_dependencies(udt_cls: type[UserType]) -> list[type[UserType]]:
    """Return UDT dependencies of *udt_cls* in topological (depth-first) order.

    Does **not** include *udt_cls* itself in the result.
    Raises ``InvalidQueryError`` if a circular dependency is detected.
    """
    from coodie.exceptions import InvalidQueryError
    from coodie.schema import _cached_type_hints

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
    from coodie.exceptions import InvalidQueryError
    from coodie.schema import _cached_type_hints

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
