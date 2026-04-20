from __future__ import annotations

import warnings
from typing import Any, ClassVar, TYPE_CHECKING

from pydantic import BaseModel

from coodie.cql_builder import (
    build_insert_from_columns,
    build_insert_json,
    build_delete,
    build_update,
    build_counter_update,
    build_drop_table,
    build_truncate,
    build_create_materialized_view,
    build_drop_materialized_view,
    parse_update_kwargs,
)
from coodie.exceptions import (
    DocumentNotFound,
    MultipleDocumentsFound,
    InvalidQueryError,
)
from coodie.results import LWTResult
from coodie.schema import (
    build_schema,
    ColumnDefinition,
    _find_discriminator_column,
    _get_discriminator_value,
    _insert_columns,
    _pk_columns,
    _resolve_polymorphic_base,
    _vector_columns,
)
from coodie.aio.query import QuerySet
from coodie.sync.query import _snake_case

if TYPE_CHECKING:
    from coodie.batch import AsyncBatchQuery


class Document(BaseModel):
    """Base class for asynchronous coodie documents."""

    __schema__: ClassVar[list[ColumnDefinition]]

    class Settings:
        name: str = ""
        keyspace: str = ""

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
        from coodie.exceptions import InvalidQueryError

        raise InvalidQueryError("No keyspace configured")

    @classmethod
    def _get_driver(cls) -> Any:
        from coodie.drivers import get_driver

        settings = getattr(cls, "Settings", None)
        connection = getattr(settings, "connection", None) if settings else None
        return get_driver(name=connection)

    @classmethod
    def _schema(cls) -> list[ColumnDefinition]:
        if "__schema__" not in cls.__dict__ or cls.__schema__ is None:
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
    async def sync_table(
        cls,
        dry_run: bool = False,
        drop_removed_indexes: bool = False,
    ) -> list[str]:
        """Idempotently create or update the table in the database.

        Args:
            dry_run: When ``True``, return the planned CQL statements without
                executing them.
            drop_removed_indexes: When ``True``, drop secondary indexes that
                exist in the database but are no longer defined in the model.

        Returns:
            List of CQL statements that were (or would be) executed.
        """
        settings = getattr(cls, "Settings", None)
        if settings and getattr(settings, "__abstract__", False):
            return []
        schema = cls._schema()
        return await cls._get_driver().sync_table_async(
            cls._get_table(),
            cls._get_keyspace(),
            schema,
            table_options=cls._get_table_options(),
            dry_run=dry_run,
            drop_removed_indexes=drop_removed_indexes,
        )

    @classmethod
    def table_name(cls) -> str:
        """Return the CQL table name for this model."""
        return cls._get_table()

    @classmethod
    async def drop_table(cls) -> None:
        """Drop the table for this model."""
        cql = build_drop_table(cls._get_table(), cls._get_keyspace())
        await cls._get_driver().execute_async(cql, [])

    @classmethod
    async def truncate(cls) -> None:
        """Truncate (remove all rows from) the table for this model."""
        cql = build_truncate(cls._get_table(), cls._get_keyspace())
        await cls._get_driver().execute_async(cql, [])

    @classmethod
    async def create(cls, **kwargs: Any) -> Document:
        """Construct and save a new document in one step."""
        doc = cls(**kwargs)
        await doc.save()
        return doc

    # ------------------------------------------------------------------
    # Write operations (all async)
    # ------------------------------------------------------------------

    async def save(
        self,
        ttl: int | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
        batch: AsyncBatchQuery | None = None,
    ) -> None:
        """Insert (upsert) this document."""
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
        cql, params = build_insert_from_columns(
            cls._get_table(),
            cls._get_keyspace(),
            columns,
            values,
            ttl=ttl,
            timestamp=timestamp,
        )
        if batch is not None:
            batch.add(cql, params)
        else:
            await cls._get_driver().execute_async(cql, params, consistency=consistency, timeout=timeout)

    async def save_json(
        self,
        ttl: int | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
    ) -> None:
        """Insert (upsert) this document using ``INSERT INTO … JSON``."""
        import json

        cls = self.__class__
        json_string = json.dumps(self.model_dump(mode="json"))
        cql, params = build_insert_json(
            cls._get_table(),
            cls._get_keyspace(),
            json_string,
            ttl=ttl,
            timestamp=timestamp,
        )
        await cls._get_driver().execute_async(cql, params, consistency=consistency, timeout=timeout)

    async def insert(
        self,
        ttl: int | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
        batch: AsyncBatchQuery | None = None,
    ) -> None:
        """Insert IF NOT EXISTS (create-only)."""
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
        cql, params = build_insert_from_columns(
            cls._get_table(),
            cls._get_keyspace(),
            columns,
            values,
            ttl=ttl,
            if_not_exists=True,
            timestamp=timestamp,
        )
        if batch is not None:
            batch.add(cql, params)
        else:
            await cls._get_driver().execute_async(cql, params, consistency=consistency, timeout=timeout)

    async def delete_columns(
        self,
        *column_names: str,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
        batch: AsyncBatchQuery | None = None,
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
        warnings.warn(
            "delete_columns() nullifies individual column values in-place and bypasses "
            "schema migrations. If you are removing or renaming a column, use "
            "Document.sync_table() for development or `coodie migrate` for production "
            "instead.",
            UserWarning,
            stacklevel=2,
        )
        pk_names = _pk_columns(self.__class__)
        where = [(c, "=", getattr(self, c)) for c in pk_names]
        cql, params = build_delete(
            self.__class__._get_table(),
            self.__class__._get_keyspace(),
            where,
            columns=list(column_names) if column_names else None,
            timestamp=timestamp,
            collection_elements=collection_elements,
        )
        if batch is not None:
            batch.add(cql, params)
        else:
            await self.__class__._get_driver().execute_async(cql, params, consistency=consistency, timeout=timeout)

    async def delete(
        self,
        if_exists: bool = False,
        if_conditions: dict[str, Any] | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
        batch: AsyncBatchQuery | None = None,
    ) -> LWTResult | None:
        """Delete this document by its primary key.

        When *if_exists* is ``True`` the generated CQL includes ``IF EXISTS``
        and a :class:`~coodie.results.LWTResult` is returned.

        When *if_conditions* is supplied (e.g. ``{"name": "old"}``), the CQL
        includes ``IF name = ?`` and a :class:`~coodie.results.LWTResult` is
        returned.  Operator suffixes like ``col__ne``, ``col__gt``, ``col__in``
        are supported.
        """

        pk_names = _pk_columns(self.__class__)
        where = [(c, "=", getattr(self, c)) for c in pk_names]
        cql, params = build_delete(
            self.__class__._get_table(),
            self.__class__._get_keyspace(),
            where,
            if_exists=if_exists,
            if_conditions=if_conditions,
            timestamp=timestamp,
        )
        if batch is not None:
            batch.add(cql, params)
            return None

        rows = await self.__class__._get_driver().execute_async(cql, params, consistency=consistency, timeout=timeout)
        if if_exists or if_conditions:
            return _parse_lwt_result(rows)
        return None

    async def update(
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
        set_data, collection_ops = parse_update_kwargs(kwargs)

        if not set_data and not collection_ops:
            return None

        pk_names = _pk_columns(self.__class__)
        where = [(c, "=", getattr(self, c)) for c in pk_names]

        cql, params = build_update(
            self.__class__._get_table(),
            self.__class__._get_keyspace(),
            set_data=set_data,
            where=where,
            ttl=ttl,
            if_conditions=if_conditions,
            if_exists=if_exists,
            collection_ops=collection_ops or None,
        )
        rows = await self.__class__._get_driver().execute_async(cql, params)

        # Update in-memory model fields for regular set assignments
        for k, v in set_data.items():
            if hasattr(self, k):
                object.__setattr__(self, k, v)

        if if_conditions or if_exists:
            return _parse_lwt_result(rows)
        return None

    # ------------------------------------------------------------------
    # Query / read operations
    # ------------------------------------------------------------------

    @classmethod
    def find(cls, **kwargs: Any) -> QuerySet:
        """Return an async QuerySet filtered by *kwargs*."""
        qs = QuerySet(cls)
        if kwargs:
            qs = qs.filter(**kwargs)
        disc_col = _find_discriminator_column(cls)
        disc_val = _get_discriminator_value(cls)
        if disc_col and disc_val:
            qs = qs.filter(**{disc_col: disc_val})
        return qs

    @classmethod
    async def find_one(cls, **kwargs: Any) -> Document | None:
        """Return a single document or None."""
        results = await cls.find(**kwargs).limit(2).all()
        if len(results) > 1:
            raise MultipleDocumentsFound(f"Expected one {cls.__name__} but found multiple matching {kwargs}")
        return results[0] if results else None

    @classmethod
    async def get(cls, **kwargs: Any) -> Document:
        """Return a single document; raise DocumentNotFound if missing."""
        result = await cls.find_one(**kwargs)
        if result is None:
            raise DocumentNotFound(f"No {cls.__name__} found matching {kwargs}")
        return result

    model_config = {
        "arbitrary_types_allowed": True,
        "revalidate_instances": "never",
        "use_enum_values": True,
        "populate_by_name": True,
    }


class CounterDocument(Document):
    """Base class for asynchronous counter-column documents.

    Counter tables only support increment/decrement operations.
    ``save()`` and ``insert()`` are forbidden.
    """

    async def save(  # noqa: ARG002
        self,
        ttl: int | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
    ) -> None:
        raise InvalidQueryError("Counter tables do not support save(). Use increment() or decrement() instead.")

    async def insert(  # noqa: ARG002
        self,
        ttl: int | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
    ) -> None:
        raise InvalidQueryError("Counter tables do not support insert(). Use increment() or decrement() instead.")

    async def _counter_update(self, deltas: dict[str, int]) -> None:
        """Execute a counter UPDATE with the given deltas."""
        pk_names = _pk_columns(self.__class__)
        where = [(c, "=", getattr(self, c)) for c in pk_names]
        cql, params = build_counter_update(
            self.__class__._get_table(),
            self.__class__._get_keyspace(),
            deltas,
            where,
        )
        await self.__class__._get_driver().execute_async(cql, params)

    async def increment(self, **field_deltas: int) -> None:
        """Increment counter columns by the given amounts.

        Example::

            await page_view.increment(view_count=1, unique_visitors=1)
        """
        await self._counter_update(field_deltas)

    async def decrement(self, **field_deltas: int) -> None:
        """Decrement counter columns by the given amounts.

        Example::

            await page_view.decrement(view_count=1)
        """
        negated = {k: -v for k, v in field_deltas.items()}
        await self._counter_update(negated)


def _parse_lwt_result(rows: list[dict[str, Any]]) -> LWTResult:
    """Parse the result of a LWT operation into a :class:`LWTResult`."""
    if not rows:
        return LWTResult(applied=True)
    row = rows[0]
    applied = row.get("[applied]", True)
    existing = {k: v for k, v in row.items() if k != "[applied]"} or None
    return LWTResult(applied=applied, existing=existing)


class MaterializedView(Document):
    """Base class for asynchronous materialized view documents (read-only).

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
    async def sync_view(cls) -> None:
        """Create the materialized view in the database."""
        schema = cls._schema()
        pk_cols = sorted(
            [c for c in schema if c.primary_key],
            key=lambda c: c.partition_key_index,
        )
        ck_cols = sorted(
            [c for c in schema if c.clustering_key],
            key=lambda c: c.clustering_key_index,
        )
        cql = build_create_materialized_view(
            view_name=cls._get_table(),
            keyspace=cls._get_keyspace(),
            base_table=cls._get_base_table(),
            columns=cls._get_view_columns(),
            primary_key_columns=[c.name for c in pk_cols],
            clustering_columns=[c.name for c in ck_cols] or None,
            where_clause=cls._get_where_clause(),
            clustering_order=cls._get_clustering_order(),
        )
        await cls._get_driver().execute_async(cql, [])

    @classmethod
    async def drop_view(cls) -> None:
        """Drop the materialized view."""
        cql = build_drop_materialized_view(cls._get_table(), cls._get_keyspace())
        await cls._get_driver().execute_async(cql, [])

    async def save(self, **kwargs: Any) -> None:  # type: ignore[override]
        raise InvalidQueryError("Materialized views are read-only. Use the base table to write data.")

    async def insert(self, **kwargs: Any) -> None:  # type: ignore[override]
        raise InvalidQueryError("Materialized views are read-only. Use the base table to write data.")

    async def delete(self, **kwargs: Any) -> LWTResult | None:  # type: ignore[override]
        raise InvalidQueryError("Materialized views are read-only. Use the base table to write data.")

    async def update(self, **kwargs: Any) -> LWTResult | None:  # type: ignore[override]
        raise InvalidQueryError("Materialized views are read-only. Use the base table to write data.")
