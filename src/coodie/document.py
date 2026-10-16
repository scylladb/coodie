"""Shared document base classes with explicit ``*_sync`` / ``*_async`` methods.

Use :class:`coodie.sync.Document` or :class:`coodie.aio.Document` (or
``coodie.Document``) as the base of a model. Both are subclasses of
:class:`BaseDocument` and differ only in which twin the un-suffixed names
(``save()``, ``get()``, ...) call.
"""

from __future__ import annotations

import json
import warnings
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import BaseModel

from coodie._modes import _user_stacklevel, check_override, pick, warn_if_blocking
from coodie.cql_builder import (
    build_counter_update,
    build_create_materialized_view,
    build_delete,
    build_drop_materialized_view,
    build_drop_table,
    build_insert_from_columns,
    build_insert_json,
    build_truncate,
    build_update,
    parse_update_kwargs,
)
from coodie.exceptions import DocumentNotFound, InvalidQueryError, MultipleDocumentsFound
from coodie.query import BaseQuerySet, _parse_lwt_result, _snake_case
from coodie.results import LWTResult
from coodie.schema import (
    ColumnDefinition,
    _find_discriminator_column,
    _get_discriminator_value,
    _insert_columns,
    _pk_columns,
    _resolve_polymorphic_base,
    _vector_columns,
    build_schema,
)
from coodie.usertype import extract_udt_classes

if TYPE_CHECKING:
    from typing_extensions import Self

    from coodie.batch import BatchQuery


class BaseDocument(BaseModel):
    """Base class for coodie documents, exposing both sync and async methods."""

    __schema__: ClassVar[list[ColumnDefinition]]
    # Which twin the un-suffixed names call; set by coodie.sync / coodie.aio.
    __coodie_mode__: ClassVar[str] = "sync"
    __queryset_cls__: ClassVar[type[BaseQuerySet]] = BaseQuerySet

    class Settings:
        name: str = ""
        keyspace: str = ""

    model_config = {
        "arbitrary_types_allowed": True,
        "revalidate_instances": "never",
        "use_enum_values": True,
        "populate_by_name": True,
    }

    # ------------------------------------------------------------------
    # Schema / table helpers
    # ------------------------------------------------------------------

    @classmethod
    def _get_table(cls) -> str:
        base = _resolve_polymorphic_base(cls)
        if base is not None and base is not cls:
            return base._get_table()
        settings = getattr(cls, "Settings", None)
        if settings and getattr(settings, "name", None):
            return settings.name
        return _snake_case(cls.__name__)

    @classmethod
    def _get_keyspace(cls) -> str:
        base = _resolve_polymorphic_base(cls)
        if base is not None and base is not cls:
            return base._get_keyspace()
        settings = getattr(cls, "Settings", None)
        if settings and getattr(settings, "keyspace", None):
            return settings.keyspace
        from coodie.drivers import get_driver

        driver = get_driver()
        ks = getattr(driver, "_default_keyspace", None)
        if ks:
            return ks
        raise InvalidQueryError("No keyspace configured")

    @classmethod
    def _get_driver(cls) -> Any:
        from coodie.drivers import get_driver

        settings = getattr(cls, "Settings", None)
        connection = getattr(settings, "connection", None) if settings else None
        return get_driver(name=connection)

    @classmethod
    def _schema(cls) -> list[ColumnDefinition]:
        if not hasattr(cls, "__schema__") or cls.__schema__ is None:
            cls.__schema__ = build_schema(cls)
        return cls.__schema__

    @classmethod
    def _get_table_options(cls) -> dict[str, Any] | None:
        settings = getattr(cls, "Settings", None)
        if settings is None:
            return None
        options: dict[str, Any] = {}
        default_ttl = getattr(settings, "__default_ttl__", None)
        if default_ttl is not None:
            options["default_time_to_live"] = default_ttl
        extra = getattr(settings, "__options__", None)
        if extra:
            options.update(extra)
        return options or None

    @classmethod
    def table_name(cls) -> str:
        """Return the CQL table name for this model."""
        return cls._get_table()

    @classmethod
    def _execute_sync(cls, cql: str, params: list[Any], **kwargs: Any) -> list[dict[str, Any]]:
        warn_if_blocking(cls)
        return cls._get_driver().execute(cql, params, **kwargs)

    @classmethod
    async def _execute_async(cls, cql: str, params: list[Any], **kwargs: Any) -> list[dict[str, Any]]:
        return await cls._get_driver().execute_async(cql, params, **kwargs)

    # ------------------------------------------------------------------
    # Table management
    # ------------------------------------------------------------------

    @classmethod
    def _sync_table_args(cls) -> tuple[Any, ...] | None:
        settings = getattr(cls, "Settings", None)
        if settings and getattr(settings, "__abstract__", False):
            return None
        return (cls._get_table(), cls._get_keyspace(), cls._schema())

    @classmethod
    def sync_table_sync(cls, dry_run: bool = False, drop_removed_indexes: bool = False) -> list[str]:
        """Idempotently create or update the table in the database.

        Args:
            dry_run: When ``True``, return the planned CQL statements without
                executing them.
            drop_removed_indexes: When ``True``, drop secondary indexes that
                exist in the database but are no longer defined in the model.

        Returns:
            List of CQL statements that were (or would be) executed,
            including ``CREATE``/``ALTER TYPE`` for referenced UDTs.
        """
        check_override(cls, "sync_table", "sync")
        args = cls._sync_table_args()
        if args is None:
            return []
        warn_if_blocking(cls)
        driver = cls._get_driver()
        # UDTs live in the table's keyspace and must exist before the table.
        stmts: list[str] = []
        for udt in extract_udt_classes(cls):
            stmts.extend(udt._sync_one(driver, args[1], dry_run))
        stmts.extend(
            driver.sync_table(
                *args,
                table_options=cls._get_table_options(),
                dry_run=dry_run,
                drop_removed_indexes=drop_removed_indexes,
            )
        )
        return stmts

    @classmethod
    async def sync_table_async(cls, dry_run: bool = False, drop_removed_indexes: bool = False) -> list[str]:
        """Async version of :meth:`sync_table_sync`."""
        check_override(cls, "sync_table", "async")
        args = cls._sync_table_args()
        if args is None:
            return []
        driver = cls._get_driver()
        stmts: list[str] = []
        for udt in extract_udt_classes(cls):
            stmts.extend(await udt._sync_one_async(driver, args[1], dry_run))
        stmts.extend(
            await driver.sync_table_async(
                *args,
                table_options=cls._get_table_options(),
                dry_run=dry_run,
                drop_removed_indexes=drop_removed_indexes,
            )
        )
        return stmts

    @classmethod
    def drop_table_sync(cls) -> None:
        """Drop the table for this model."""
        check_override(cls, "drop_table", "sync")
        cls._execute_sync(build_drop_table(cls._get_table(), cls._get_keyspace()), [])

    @classmethod
    async def drop_table_async(cls) -> None:
        """Drop the table for this model."""
        check_override(cls, "drop_table", "async")
        await cls._execute_async(build_drop_table(cls._get_table(), cls._get_keyspace()), [])

    @classmethod
    def truncate_sync(cls) -> None:
        """Truncate (remove all rows from) the table for this model."""
        check_override(cls, "truncate", "sync")
        cls._execute_sync(build_truncate(cls._get_table(), cls._get_keyspace()), [])

    @classmethod
    async def truncate_async(cls) -> None:
        """Truncate (remove all rows from) the table for this model."""
        check_override(cls, "truncate", "async")
        await cls._execute_async(build_truncate(cls._get_table(), cls._get_keyspace()), [])

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    @classmethod
    def create_sync(cls, **kwargs: Any) -> Self:
        """Construct and save a new document in one step."""
        check_override(cls, "create", "sync")
        doc = cls(**kwargs)
        pick(doc, "save", "sync")()
        return doc

    @classmethod
    async def create_async(cls, **kwargs: Any) -> Self:
        """Construct and save a new document in one step."""
        check_override(cls, "create", "async")
        doc = cls(**kwargs)
        await pick(doc, "save", "async")()
        return doc

    def _insert_stmt(self, ttl: int | None, timestamp: int | None, if_not_exists: bool) -> tuple[str, list[Any]]:
        cls = self.__class__
        for vec_name, vec_dims in _vector_columns(cls):
            val = getattr(self, vec_name, None)
            if val is not None and len(val) != vec_dims:
                raise InvalidQueryError(f"Vector field '{vec_name}' expects {vec_dims} dimensions, got {len(val)}")
        columns = _insert_columns(cls)
        values = [getattr(self, c) for c in columns]
        disc_col = _find_discriminator_column(cls)
        disc_val = _get_discriminator_value(cls)
        if disc_col and disc_val:
            values[columns.index(disc_col)] = disc_val
        return build_insert_from_columns(
            cls._get_table(),
            cls._get_keyspace(),
            columns,
            values,
            ttl=ttl,
            if_not_exists=if_not_exists,
            timestamp=timestamp,
        )

    def save_sync(
        self,
        ttl: int | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
        batch: BatchQuery | None = None,
    ) -> None:
        """Insert (upsert) this document."""
        check_override(self.__class__, "save", "sync")
        cql, params = self._insert_stmt(ttl, timestamp, if_not_exists=False)
        if batch is not None:
            batch.add(cql, params)
        else:
            self._execute_sync(cql, params, consistency=consistency, timeout=timeout)

    async def save_async(
        self,
        ttl: int | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
        batch: BatchQuery | None = None,
    ) -> None:
        """Insert (upsert) this document."""
        check_override(self.__class__, "save", "async")
        cql, params = self._insert_stmt(ttl, timestamp, if_not_exists=False)
        if batch is not None:
            batch.add(cql, params)
        else:
            await self._execute_async(cql, params, consistency=consistency, timeout=timeout)

    def _save_json_stmt(self, ttl: int | None, timestamp: int | None) -> tuple[str, list[Any]]:
        cls = self.__class__
        json_string = json.dumps(self.model_dump(mode="json"))
        return build_insert_json(cls._get_table(), cls._get_keyspace(), json_string, ttl=ttl, timestamp=timestamp)

    def save_json_sync(
        self,
        ttl: int | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
    ) -> None:
        """Insert (upsert) this document using ``INSERT INTO … JSON``."""
        check_override(self.__class__, "save_json", "sync")
        cql, params = self._save_json_stmt(ttl, timestamp)
        self._execute_sync(cql, params, consistency=consistency, timeout=timeout)

    async def save_json_async(
        self,
        ttl: int | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
    ) -> None:
        """Insert (upsert) this document using ``INSERT INTO … JSON``."""
        check_override(self.__class__, "save_json", "async")
        cql, params = self._save_json_stmt(ttl, timestamp)
        await self._execute_async(cql, params, consistency=consistency, timeout=timeout)

    def insert_sync(
        self,
        ttl: int | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
        batch: BatchQuery | None = None,
    ) -> LWTResult | None:
        """Insert IF NOT EXISTS (create-only).

        Returns a :class:`~coodie.results.LWTResult` whose ``applied`` is
        ``False`` (with the existing row in ``existing``) when the row was
        already present. Returns ``None`` when added to a *batch*.
        """
        check_override(self.__class__, "insert", "sync")
        cql, params = self._insert_stmt(ttl, timestamp, if_not_exists=True)
        if batch is not None:
            batch.add(cql, params)
            return None
        return _parse_lwt_result(self._execute_sync(cql, params, consistency=consistency, timeout=timeout))

    async def insert_async(
        self,
        ttl: int | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
        batch: BatchQuery | None = None,
    ) -> LWTResult | None:
        """Insert IF NOT EXISTS (create-only). See :meth:`insert_sync`."""
        check_override(self.__class__, "insert", "async")
        cql, params = self._insert_stmt(ttl, timestamp, if_not_exists=True)
        if batch is not None:
            batch.add(cql, params)
            return None
        return _parse_lwt_result(await self._execute_async(cql, params, consistency=consistency, timeout=timeout))

    def _pk_where(self) -> list[tuple[str, str, Any]]:
        return [(c, "=", getattr(self, c)) for c in _pk_columns(self.__class__)]

    def _delete_columns_stmt(
        self,
        column_names: tuple[str, ...],
        timestamp: int | None,
        collection_elements: list[tuple[str, Any]] | None,
    ) -> tuple[str, list[Any]]:
        warnings.warn(
            "delete_columns() nullifies individual column values in-place and bypasses "
            "schema migrations. If you are removing or renaming a column, use "
            "Document.sync_table() for development or `coodie migrate` for production "
            "instead.",
            UserWarning,
            stacklevel=_user_stacklevel(),
        )
        return build_delete(
            self.__class__._get_table(),
            self.__class__._get_keyspace(),
            self._pk_where(),
            columns=list(column_names) if column_names else None,
            timestamp=timestamp,
            collection_elements=collection_elements,
        )

    def delete_columns_sync(
        self,
        *column_names: str,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
        batch: BatchQuery | None = None,
        collection_elements: list[tuple[str, Any]] | None = None,
    ) -> None:
        """Set one or more non-primary-key columns to null for this document.

        Generates ``DELETE col1, col2 FROM table WHERE pk = ?``.

        When *collection_elements* is provided, each ``(column, key_or_index)``
        tuple generates ``DELETE "col"[?] FROM table WHERE pk = ?`` which removes
        a single map entry or list element.

        .. warning::
            This operation nullifies column values in-place and bypasses the
            schema-migration system.  If you are removing or renaming a column,
            use coodie's migration tools instead:
            ``Document.sync_table()`` for development environments, or
            ``coodie migrate`` (the CLI) for production deployments.
        """
        check_override(self.__class__, "delete_columns", "sync")
        cql, params = self._delete_columns_stmt(column_names, timestamp, collection_elements)
        if batch is not None:
            batch.add(cql, params)
        else:
            self._execute_sync(cql, params, consistency=consistency, timeout=timeout)

    async def delete_columns_async(
        self,
        *column_names: str,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
        batch: BatchQuery | None = None,
        collection_elements: list[tuple[str, Any]] | None = None,
    ) -> None:
        """Set one or more non-primary-key columns to null. See :meth:`delete_columns_sync`."""
        check_override(self.__class__, "delete_columns", "async")
        cql, params = self._delete_columns_stmt(column_names, timestamp, collection_elements)
        if batch is not None:
            batch.add(cql, params)
        else:
            await self._execute_async(cql, params, consistency=consistency, timeout=timeout)

    def _delete_stmt(
        self, if_exists: bool, if_conditions: dict[str, Any] | None, timestamp: int | None
    ) -> tuple[str, list[Any]]:
        return build_delete(
            self.__class__._get_table(),
            self.__class__._get_keyspace(),
            self._pk_where(),
            if_exists=if_exists,
            if_conditions=if_conditions,
            timestamp=timestamp,
        )

    def delete_sync(
        self,
        if_exists: bool = False,
        if_conditions: dict[str, Any] | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
        batch: BatchQuery | None = None,
    ) -> LWTResult | None:
        """Delete this document by its primary key.

        When *if_exists* is ``True`` the generated CQL includes ``IF EXISTS``
        and a :class:`~coodie.results.LWTResult` is returned.

        When *if_conditions* is supplied (e.g. ``{"name": "old"}``), the CQL
        includes ``IF name = ?`` and a :class:`~coodie.results.LWTResult` is
        returned.  Operator suffixes like ``col__ne``, ``col__gt``, ``col__in``
        are supported.
        """
        check_override(self.__class__, "delete", "sync")
        cql, params = self._delete_stmt(if_exists, if_conditions, timestamp)
        if batch is not None:
            batch.add(cql, params)
            return None
        rows = self._execute_sync(cql, params, consistency=consistency, timeout=timeout)
        return _parse_lwt_result(rows) if if_exists or if_conditions else None

    async def delete_async(
        self,
        if_exists: bool = False,
        if_conditions: dict[str, Any] | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
        batch: BatchQuery | None = None,
    ) -> LWTResult | None:
        """Delete this document by its primary key. See :meth:`delete_sync`."""
        check_override(self.__class__, "delete", "async")
        cql, params = self._delete_stmt(if_exists, if_conditions, timestamp)
        if batch is not None:
            batch.add(cql, params)
            return None
        rows = await self._execute_async(cql, params, consistency=consistency, timeout=timeout)
        return _parse_lwt_result(rows) if if_exists or if_conditions else None

    def _update_stmt(
        self,
        if_conditions: dict[str, Any] | None,
        if_exists: bool,
        ttl: int | None,
        kwargs: dict[str, Any],
    ) -> tuple[str, list[Any], dict[str, Any]] | None:
        set_data, collection_ops = parse_update_kwargs(kwargs)
        if not set_data and not collection_ops:
            return None
        cql, params = build_update(
            self.__class__._get_table(),
            self.__class__._get_keyspace(),
            set_data=set_data,
            where=self._pk_where(),
            ttl=ttl,
            if_conditions=if_conditions,
            if_exists=if_exists,
            collection_ops=collection_ops or None,
        )
        return cql, params, set_data

    def _after_update(
        self,
        rows: list[dict[str, Any]],
        set_data: dict[str, Any],
        if_conditions: dict[str, Any] | None,
        if_exists: bool,
    ) -> LWTResult | None:
        # Update in-memory model fields for regular set assignments
        for k, v in set_data.items():
            if hasattr(self, k):
                object.__setattr__(self, k, v)
        return _parse_lwt_result(rows) if if_conditions or if_exists else None

    def update_sync(
        self,
        *,
        if_conditions: dict[str, Any] | None = None,
        if_exists: bool = False,
        ttl: int | None = None,
        **kwargs: Any,
    ) -> LWTResult | None:
        """Partial update — sets only the given fields.

        Supports collection operations via ``parse_update_kwargs`` (e.g.
        ``add__``, ``remove__`` prefixed keys).

        When *if_conditions* or *if_exists* is supplied the generated CQL
        includes a lightweight-transaction clause and a
        :class:`~coodie.results.LWTResult` is returned.
        """
        check_override(self.__class__, "update", "sync")
        stmt = self._update_stmt(if_conditions, if_exists, ttl, kwargs)
        if stmt is None:
            return None
        cql, params, set_data = stmt
        return self._after_update(self._execute_sync(cql, params), set_data, if_conditions, if_exists)

    async def update_async(
        self,
        *,
        if_conditions: dict[str, Any] | None = None,
        if_exists: bool = False,
        ttl: int | None = None,
        **kwargs: Any,
    ) -> LWTResult | None:
        """Partial update — sets only the given fields. See :meth:`update_sync`."""
        check_override(self.__class__, "update", "async")
        stmt = self._update_stmt(if_conditions, if_exists, ttl, kwargs)
        if stmt is None:
            return None
        cql, params, set_data = stmt
        return self._after_update(await self._execute_async(cql, params), set_data, if_conditions, if_exists)

    # ------------------------------------------------------------------
    # Query / read operations
    # ------------------------------------------------------------------

    @classmethod
    def find(cls, **kwargs: Any) -> Any:
        """Return a QuerySet filtered by *kwargs*."""
        qs = cls.__queryset_cls__(cls)
        if kwargs:
            qs = qs.filter(**kwargs)
        disc_col = _find_discriminator_column(cls)
        disc_val = _get_discriminator_value(cls)
        if disc_col and disc_val:
            qs = qs.filter(**{disc_col: disc_val})
        return qs

    @classmethod
    def _one(cls, results: list[Any], kwargs: dict[str, Any]) -> Any:
        if len(results) > 1:
            raise MultipleDocumentsFound(f"Expected one {cls.__name__} but found multiple matching {kwargs}")
        return results[0] if results else None

    @classmethod
    def find_one_sync(cls, **kwargs: Any) -> Self | None:
        """Return a single document or None."""
        check_override(cls, "find_one", "sync")
        return cls._one(pick(cls.find(**kwargs).limit(2), "all", "sync")(), kwargs)

    @classmethod
    async def find_one_async(cls, **kwargs: Any) -> Self | None:
        """Return a single document or None."""
        check_override(cls, "find_one", "async")
        return cls._one(await pick(cls.find(**kwargs).limit(2), "all", "async")(), kwargs)

    @classmethod
    def _found(cls, result: Any, kwargs: dict[str, Any]) -> Any:
        if result is None:
            raise DocumentNotFound(f"No {cls.__name__} found matching {kwargs}")
        return result

    @classmethod
    def get_sync(cls, **kwargs: Any) -> Self:
        """Return a single document; raise DocumentNotFound if missing."""
        check_override(cls, "get", "sync")
        return cls._found(pick(cls, "find_one", "sync")(**kwargs), kwargs)

    @classmethod
    async def get_async(cls, **kwargs: Any) -> Self:
        """Return a single document; raise DocumentNotFound if missing."""
        check_override(cls, "get", "async")
        return cls._found(await pick(cls, "find_one", "async")(**kwargs), kwargs)


class BaseCounterDocument(BaseDocument):
    """Counter-column documents. Only increment/decrement are allowed; save/insert raise."""

    def save_sync(self, *args: Any, **kwargs: Any) -> None:
        raise InvalidQueryError("Counter tables do not support save(). Use increment() or decrement() instead.")

    async def save_async(self, *args: Any, **kwargs: Any) -> None:
        raise InvalidQueryError("Counter tables do not support save(). Use increment() or decrement() instead.")

    def insert_sync(self, *args: Any, **kwargs: Any) -> None:
        raise InvalidQueryError("Counter tables do not support insert(). Use increment() or decrement() instead.")

    async def insert_async(self, *args: Any, **kwargs: Any) -> None:
        raise InvalidQueryError("Counter tables do not support insert(). Use increment() or decrement() instead.")

    def _counter_stmt(self, deltas: dict[str, int]) -> tuple[str, list[Any]]:
        return build_counter_update(
            self.__class__._get_table(), self.__class__._get_keyspace(), deltas, self._pk_where()
        )

    def increment_sync(self, **field_deltas: int) -> None:
        """Increment counter columns by the given amounts, e.g. ``increment_sync(view_count=1)``."""
        check_override(self.__class__, "increment", "sync")
        self._execute_sync(*self._counter_stmt(field_deltas))

    async def increment_async(self, **field_deltas: int) -> None:
        """Increment counter columns by the given amounts, e.g. ``await increment_async(view_count=1)``."""
        check_override(self.__class__, "increment", "async")
        await self._execute_async(*self._counter_stmt(field_deltas))

    def decrement_sync(self, **field_deltas: int) -> None:
        """Decrement counter columns by the given amounts, e.g. ``decrement_sync(view_count=1)``."""
        check_override(self.__class__, "decrement", "sync")
        self._execute_sync(*self._counter_stmt({k: -v for k, v in field_deltas.items()}))

    async def decrement_async(self, **field_deltas: int) -> None:
        """Decrement counter columns by the given amounts, e.g. ``await decrement_async(view_count=1)``."""
        check_override(self.__class__, "decrement", "async")
        await self._execute_async(*self._counter_stmt({k: -v for k, v in field_deltas.items()}))


_READ_ONLY = "Materialized views are read-only. Use the base table to write data."


class BaseMaterializedView(BaseDocument):
    """Materialized view documents (read-only).

    Subclasses must define ``Settings`` with:

    * ``__base_table__`` — the base table name (required).
    * ``__view_columns__`` — columns to select (defaults to ``["*"]``).
    * ``__where_clause__`` — the ``WHERE`` clause (defaults to auto-generated
      ``IS NOT NULL`` for all primary-key/clustering columns).
    * ``__clustering_order__`` — optional ``{column: "ASC"|"DESC"}`` dict.

    The view name defaults to the model's table name.
    """

    @classmethod
    def _get_base_table(cls) -> str:
        settings = getattr(cls, "Settings", None)
        base = getattr(settings, "__base_table__", None) if settings else None
        if not base:
            raise InvalidQueryError(f"{cls.__name__}.Settings must define __base_table__")
        return base

    @classmethod
    def _get_view_columns(cls) -> list[str]:
        settings = getattr(cls, "Settings", None)
        return getattr(settings, "__view_columns__", ["*"]) if settings else ["*"]

    @classmethod
    def _get_where_clause(cls) -> str:
        settings = getattr(cls, "Settings", None)
        explicit = getattr(settings, "__where_clause__", None) if settings else None
        if explicit:
            return explicit
        # Auto-generate: all PK + CK columns IS NOT NULL
        schema = cls._schema()
        pk_ck_cols = [c for c in schema if c.primary_key or c.clustering_key]
        return " AND ".join(f'"{c.name}" IS NOT NULL' for c in pk_ck_cols)

    @classmethod
    def _get_clustering_order(cls) -> dict[str, str] | None:
        settings = getattr(cls, "Settings", None)
        return getattr(settings, "__clustering_order__", None) if settings else None

    @classmethod
    def _create_view_stmt(cls) -> str:
        schema = cls._schema()
        pk_cols = sorted([c for c in schema if c.primary_key], key=lambda c: c.partition_key_index)
        ck_cols = sorted([c for c in schema if c.clustering_key], key=lambda c: c.clustering_key_index)
        return build_create_materialized_view(
            view_name=cls._get_table(),
            keyspace=cls._get_keyspace(),
            base_table=cls._get_base_table(),
            columns=cls._get_view_columns(),
            primary_key_columns=[c.name for c in pk_cols],
            clustering_columns=[c.name for c in ck_cols] or None,
            where_clause=cls._get_where_clause(),
            clustering_order=cls._get_clustering_order(),
        )

    @classmethod
    def sync_view_sync(cls) -> None:
        """Create the materialized view in the database."""
        check_override(cls, "sync_view", "sync")
        cls._execute_sync(cls._create_view_stmt(), [])

    @classmethod
    async def sync_view_async(cls) -> None:
        """Create the materialized view in the database."""
        check_override(cls, "sync_view", "async")
        await cls._execute_async(cls._create_view_stmt(), [])

    @classmethod
    def drop_view_sync(cls) -> None:
        """Drop the materialized view."""
        check_override(cls, "drop_view", "sync")
        cls._execute_sync(build_drop_materialized_view(cls._get_table(), cls._get_keyspace()), [])

    @classmethod
    async def drop_view_async(cls) -> None:
        """Drop the materialized view."""
        check_override(cls, "drop_view", "async")
        await cls._execute_async(build_drop_materialized_view(cls._get_table(), cls._get_keyspace()), [])

    def save_sync(self, *args: Any, **kwargs: Any) -> None:
        raise InvalidQueryError(_READ_ONLY)

    async def save_async(self, *args: Any, **kwargs: Any) -> None:
        raise InvalidQueryError(_READ_ONLY)

    def insert_sync(self, *args: Any, **kwargs: Any) -> LWTResult | None:
        raise InvalidQueryError(_READ_ONLY)

    async def insert_async(self, *args: Any, **kwargs: Any) -> LWTResult | None:
        raise InvalidQueryError(_READ_ONLY)

    def delete_sync(self, *args: Any, **kwargs: Any) -> LWTResult | None:
        raise InvalidQueryError(_READ_ONLY)

    async def delete_async(self, *args: Any, **kwargs: Any) -> LWTResult | None:
        raise InvalidQueryError(_READ_ONLY)

    def update_sync(self, *args: Any, **kwargs: Any) -> LWTResult | None:
        raise InvalidQueryError(_READ_ONLY)

    async def update_async(self, *args: Any, **kwargs: Any) -> LWTResult | None:
        raise InvalidQueryError(_READ_ONLY)
