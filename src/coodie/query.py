"""Shared query builder with explicit ``*_sync`` / ``*_async`` terminal methods.

:class:`coodie.sync.QuerySet` and :class:`coodie.aio.QuerySet` subclass
:class:`BaseQuerySet` and add the un-suffixed terminal names (``all()``,
``count()``, ...) as aliases for their default mode.
"""

from __future__ import annotations

import functools
import re
from collections.abc import AsyncIterator, Iterator
from typing import TYPE_CHECKING, Any, ClassVar

from coodie._modes import check_override, pick, warn_if_blocking
from coodie.cql_builder import (
    build_aggregate,
    build_count,
    build_delete,
    build_insert,
    build_select,
    build_select_column_ttl,
    build_select_json,
    build_select_writetime,
    build_update,
    parse_filter_kwargs,
    parse_update_kwargs,
)
from coodie.drivers import get_driver as _get_driver_impl
from coodie.lazy import LazyDocument
from coodie.results import LWTResult, PagedResult
from coodie.schema import (
    _build_subclass_map,
    _find_discriminator_column,
    _resolve_polymorphic_base,
)
from coodie.types import _collection_fields

if TYPE_CHECKING:
    from typing_extensions import Self

    from coodie.document import BaseDocument


class BaseQuerySet:
    """Chainable query builder with explicit ``*_sync`` / ``*_async`` terminal methods."""

    __slots__ = (
        "_allow_filtering_val",
        "_ann_of_val",
        "_cast_val",
        "_consistency_val",
        "_defer_val",
        "_distinct_val",
        "_doc_cls",
        "_fetch_size_val",
        "_group_by_val",
        "_if_exists_val",
        "_if_not_exists_val",
        "_limit_val",
        "_only_val",
        "_order_by_val",
        "_paging_state_val",
        "_per_partition_limit_val",
        "_select_token_val",
        "_timeout_val",
        "_timestamp_val",
        "_ttl_val",
        "_validate_val",
        "_values_list_val",
        "_where",
    )

    # Which twin the un-suffixed names call; set by coodie.sync / coodie.aio.
    __coodie_mode__: ClassVar[str] = "sync"

    def __init__(
        self,
        doc_cls: type[BaseDocument],
        *,
        where: list[tuple[str, str, Any]] | None = None,
        limit_val: int | None = None,
        order_by_val: list[str] | None = None,
        allow_filtering_val: bool = False,
        if_not_exists_val: bool = False,
        if_exists_val: bool = False,
        ttl_val: int | None = None,
        timestamp_val: int | None = None,
        consistency_val: str | None = None,
        timeout_val: float | None = None,
        only_val: list[str] | None = None,
        defer_val: list[str] | None = None,
        values_list_val: list[str] | None = None,
        per_partition_limit_val: int | None = None,
        fetch_size_val: int | None = None,
        paging_state_val: bytes | None = None,
        distinct_val: bool = False,
        group_by_val: list[str] | None = None,
        select_token_val: list[str] | None = None,
        cast_val: list[tuple[str, str]] | None = None,
        ann_of_val: tuple[str, list[float]] | None = None,
        validate_val: bool | None = None,
    ) -> None:
        self._doc_cls = doc_cls
        self._where: list[tuple[str, str, Any]] = where or []
        self._limit_val = limit_val
        self._order_by_val: list[str] = order_by_val or []
        self._allow_filtering_val = allow_filtering_val
        self._if_not_exists_val = if_not_exists_val
        self._if_exists_val = if_exists_val
        self._ttl_val = ttl_val
        self._timestamp_val = timestamp_val
        self._consistency_val = consistency_val
        self._timeout_val = timeout_val
        self._only_val = only_val
        self._defer_val = defer_val
        self._values_list_val = values_list_val
        self._per_partition_limit_val = per_partition_limit_val
        self._fetch_size_val = fetch_size_val
        self._paging_state_val = paging_state_val
        self._distinct_val = distinct_val
        self._group_by_val: list[str] = group_by_val or []
        self._select_token_val = select_token_val
        self._cast_val = cast_val
        self._ann_of_val: tuple[str, list[float]] | None = ann_of_val
        self._validate_val = validate_val

    # ------------------------------------------------------------------
    # Internal: clone with overrides
    # ------------------------------------------------------------------

    def _clone(self, **overrides: Any) -> Self:
        new = object.__new__(type(self))
        new._doc_cls = self._doc_cls
        new._where = self._where
        new._limit_val = self._limit_val
        new._order_by_val = self._order_by_val
        new._allow_filtering_val = self._allow_filtering_val
        new._if_not_exists_val = self._if_not_exists_val
        new._if_exists_val = self._if_exists_val
        new._ttl_val = self._ttl_val
        new._timestamp_val = self._timestamp_val
        new._consistency_val = self._consistency_val
        new._timeout_val = self._timeout_val
        new._only_val = self._only_val
        new._defer_val = self._defer_val
        new._values_list_val = self._values_list_val
        new._per_partition_limit_val = self._per_partition_limit_val
        new._fetch_size_val = self._fetch_size_val
        new._paging_state_val = self._paging_state_val
        new._distinct_val = self._distinct_val
        new._group_by_val = self._group_by_val
        new._select_token_val = self._select_token_val
        new._cast_val = self._cast_val
        new._ann_of_val = self._ann_of_val
        new._validate_val = self._validate_val
        for key, val in overrides.items():
            setattr(new, f"_{key}", val)
        return new

    # ------------------------------------------------------------------
    # Chainable builder methods
    # ------------------------------------------------------------------

    def filter(self, **kwargs: Any) -> Self:
        triples = parse_filter_kwargs(kwargs)
        return self._clone(where=self._where + triples)

    def limit(self, n: int) -> Self:
        return self._clone(limit_val=n)

    def order_by(self, *cols: str) -> Self:
        return self._clone(order_by_val=list(cols))

    def order_by_ann(self, column: str, vector: list[float]) -> Self:
        """Order results by approximate nearest neighbor (ANN) similarity.

        Generates ``ORDER BY "column" ANN OF ?`` in the CQL query.

        Args:
            column: The vector column name.
            vector: The query vector to compare against.
        """
        return self._clone(ann_of_val=(column, vector))

    def allow_filtering(self) -> Self:
        return self._clone(allow_filtering_val=True)

    def if_not_exists(self) -> Self:
        return self._clone(if_not_exists_val=True)

    def if_exists(self) -> Self:
        return self._clone(if_exists_val=True)

    def ttl(self, seconds: int) -> Self:
        return self._clone(ttl_val=seconds)

    def timestamp(self, ts: int) -> Self:
        return self._clone(timestamp_val=ts)

    def consistency(self, level: str) -> Self:
        return self._clone(consistency_val=level)

    def timeout(self, seconds: float) -> Self:
        return self._clone(timeout_val=seconds)

    def using(
        self,
        *,
        ttl: int | None = None,
        timestamp: int | None = None,
        consistency: str | None = None,
        timeout: float | None = None,
    ) -> Self:
        overrides: dict[str, Any] = {}
        if ttl is not None:
            overrides["ttl_val"] = ttl
        if timestamp is not None:
            overrides["timestamp_val"] = timestamp
        if consistency is not None:
            overrides["consistency_val"] = consistency
        if timeout is not None:
            overrides["timeout_val"] = timeout
        return self._clone(**overrides)

    def only(self, *columns: str) -> Self:
        return self._clone(only_val=list(columns))

    def defer(self, *columns: str) -> Self:
        return self._clone(defer_val=list(columns))

    def values_list(self, *columns: str) -> Self:
        return self._clone(values_list_val=list(columns))

    def per_partition_limit(self, n: int) -> Self:
        return self._clone(per_partition_limit_val=n)

    def fetch_size(self, n: int) -> Self:
        return self._clone(fetch_size_val=n)

    def page(self, paging_state: bytes | None) -> Self:
        return self._clone(paging_state_val=paging_state)

    def distinct(self) -> Self:
        return self._clone(distinct_val=True)

    def group_by(self, *cols: str) -> Self:
        return self._clone(group_by_val=list(cols))

    def select_token(self, *cols: str) -> Self:
        return self._clone(select_token_val=list(cols))

    def cast(self, column: str, cql_type: str) -> Self:
        existing = list(self._cast_val) if self._cast_val else []
        existing.append((column, cql_type))
        return self._clone(cast_val=existing)

    def is_not_null(self, column: str) -> Self:
        return self._clone(where=self._where + [(column, "ISNULL", False)])

    def is_null(self, column: str) -> Self:
        return self._clone(where=self._where + [(column, "ISNULL", True)])

    def validate(self, enabled: bool = True) -> Self:
        """Enable or disable Pydantic validation when hydrating rows.

        By default, rows from the database are hydrated using
        ``model_construct()`` which skips validation for speed.
        Call ``.validate()`` to switch to ``model_validate()`` which
        performs full type coercion and runs custom validators — useful
        when driver-returned types may not match model field types exactly.
        """
        return self._clone(validate_val=enabled)

    # ------------------------------------------------------------------
    # Terminal methods
    # ------------------------------------------------------------------

    def _get_driver(self) -> Any:
        return _get_driver_impl()

    def _table(self) -> str:
        return self._doc_cls._get_table()

    def _keyspace(self) -> str:
        return self._doc_cls._get_keyspace()

    def _resolve_columns(self) -> list[str] | None:
        if self._only_val:
            return self._only_val
        if self._defer_val:
            all_cols = list(self._doc_cls.model_fields.keys())
            return [c for c in all_cols if c not in self._defer_val]
        return None

    def _execute_sync(self, cql: str, params: list[Any], **kwargs: Any) -> list[dict[str, Any]]:
        warn_if_blocking(self._doc_cls)
        return self._get_driver().execute(cql, params, **kwargs)

    async def _execute_async(self, cql: str, params: list[Any], **kwargs: Any) -> list[dict[str, Any]]:
        return await self._get_driver().execute_async(cql, params, **kwargs)

    def _execute_one_sync(self, cql: str, params: list[Any]) -> Any:
        warn_if_blocking(self._doc_cls)
        return self._get_driver().execute_one(cql, params, consistency=self._consistency_val, timeout=self._timeout_val)

    async def _execute_one_async(self, cql: str, params: list[Any]) -> Any:
        return await self._get_driver().execute_one_async(
            cql, params, consistency=self._consistency_val, timeout=self._timeout_val
        )

    def _cl(self) -> dict[str, Any]:
        return {"consistency": self._consistency_val, "timeout": self._timeout_val}

    def _select_stmt(self) -> tuple[str, list[Any]]:
        return build_select(
            self._table(),
            self._keyspace(),
            columns=self._resolve_columns(),
            where=self._where or None,
            limit=self._limit_val,
            order_by=self._order_by_val or None,
            allow_filtering=self._allow_filtering_val,
            per_partition_limit=self._per_partition_limit_val,
            distinct=self._distinct_val,
            group_by=self._group_by_val or None,
            select_token=self._select_token_val,
            cast=self._cast_val,
            ann_of=self._ann_of_val,
        )

    def _rows_to_result(
        self, rows: list[dict[str, Any]], lazy: bool
    ) -> list[Any] | list[LazyDocument] | list[tuple[Any, ...]]:
        if self._values_list_val is not None:
            vl_cols = self._values_list_val
            return [tuple(row.get(c) for c in vl_cols) for row in rows]
        if lazy:
            doc_cls = self._doc_cls
            return [LazyDocument(doc_cls, row) for row in rows]
        return self._rows_to_docs(rows)

    def all_sync(self, *, lazy: bool = False) -> list[Any] | list[LazyDocument] | list[tuple[Any, ...]]:
        """Execute the query and return all matching documents."""
        check_override(type(self), "all", "sync")
        return self._rows_to_result(self._execute_sync(*self._select_stmt(), **self._cl()), lazy)

    async def all_async(self, *, lazy: bool = False) -> list[Any] | list[LazyDocument] | list[tuple[Any, ...]]:
        """Execute the query and return all matching documents."""
        check_override(type(self), "all", "async")
        return self._rows_to_result(await self._execute_async(*self._select_stmt(), **self._cl()), lazy)

    def _rows_to_docs(self, rows: list[dict[str, Any]]) -> list[Any]:
        doc_cls = self._doc_cls
        disc_col = _find_discriminator_column(doc_cls)
        if disc_col is not None:
            base = _resolve_polymorphic_base(doc_cls) or doc_cls
            subclass_map = _build_subclass_map(base)
            result = []
            for row in rows:
                disc_value = row.get(disc_col)
                target_cls = subclass_map.get(disc_value, doc_cls)
                coll = _collection_fields(target_cls)
                if coll:
                    for key, factory in coll.items():
                        if key in row and row[key] is None:
                            row[key] = factory()
                known = target_cls.model_fields
                filtered = {k: v for k, v in row.items() if k in known}
                result.append(target_cls.model_validate(filtered))
            return result
        # Fast non-polymorphic path
        coll = _collection_fields(doc_cls)
        # Determine whether to use model_construct (fast) or model_validate
        # (safe).  When validate_val is None (the default), auto-detect
        # based on the driver's needs_row_validation flag.
        if self._validate_val is None:
            use_construct = not getattr(self._get_driver(), "needs_row_validation", False)
        else:
            use_construct = not self._validate_val
        if use_construct:
            # model_construct() fast path — skip Pydantic validation
            construct = doc_cls.model_construct
            if not rows:
                return []
            # All rows from the same CQL query share identical column sets,
            # so we compute _fields_set once and reuse across the batch.
            fields = set(rows[0].keys())
            if not coll:
                return [construct(_fields_set=fields, **row) for row in rows]
            # Collection factories replace None→empty container in-place;
            # they do not add/remove keys, so _fields_set stays correct.
            result = []
            for row in rows:
                for key, factory in coll.items():
                    if key in row and row[key] is None:
                        row[key] = factory()
                result.append(construct(_fields_set=fields, **row))
            return result
        # Default path — model_validate() with full type coercion
        validate = doc_cls.model_validate
        if not coll:
            return [validate(row) for row in rows]
        result = []
        for row in rows:
            for key, factory in coll.items():
                if key in row and row[key] is None:
                    row[key] = factory()
            result.append(validate(row))
        return result

    def _paged_stmt(self) -> tuple[str, list[Any]]:
        return build_select(
            self._table(),
            self._keyspace(),
            where=self._where or None,
            limit=self._limit_val,
            order_by=self._order_by_val or None,
            allow_filtering=self._allow_filtering_val,
            ann_of=self._ann_of_val,
        )

    def _paged_kwargs(self) -> dict[str, Any]:
        return {**self._cl(), "fetch_size": self._fetch_size_val, "paging_state": self._paging_state_val}

    def paged_all_sync(self) -> PagedResult:
        """Execute query returning a :class:`PagedResult` with documents and paging state.

        When combined with :meth:`order_by_ann`, ScyllaDB ANN queries do not support
        cursor-based pagination and will always return a single page with
        ``paging_state=None``.  Use :meth:`limit` to control the number of results.
        """
        check_override(type(self), "paged_all", "sync")
        rows = self._execute_sync(*self._paged_stmt(), **self._paged_kwargs())
        paging_state = getattr(self._get_driver(), "_last_paging_state", None)
        return PagedResult(data=self._rows_to_docs(rows), paging_state=paging_state)

    async def paged_all_async(self) -> PagedResult:
        """Execute query returning a :class:`PagedResult`. See :meth:`paged_all_sync`."""
        check_override(type(self), "paged_all", "async")
        rows = await self._execute_async(*self._paged_stmt(), **self._paged_kwargs())
        paging_state = getattr(self._get_driver(), "_last_paging_state", None)
        return PagedResult(data=self._rows_to_docs(rows), paging_state=paging_state)

    def first_sync(self) -> Any:
        """Return the first matching document or None."""
        check_override(type(self), "first", "sync")
        results = pick(self.limit(1), "all", "sync")()
        return results[0] if results else None

    async def first_async(self) -> Any:
        """Return the first matching document or None."""
        check_override(type(self), "first", "async")
        results = await pick(self.limit(1), "all", "async")()
        return results[0] if results else None

    def _count_stmt(self) -> tuple[str, list[Any]]:
        return build_count(
            self._table(), self._keyspace(), where=self._where or None, allow_filtering=self._allow_filtering_val
        )

    def count_sync(self) -> int:
        """Return the number of matching rows."""
        check_override(type(self), "count", "sync")
        val = self._execute_one_sync(*self._count_stmt())
        return int(val) if val is not None else 0

    async def count_async(self) -> int:
        """Return the number of matching rows."""
        check_override(type(self), "count", "async")
        val = await self._execute_one_async(*self._count_stmt())
        return int(val) if val is not None else 0

    def _aggregate_stmt(self, func: str, column: str) -> tuple[str, list[Any]]:
        return build_aggregate(
            self._table(),
            self._keyspace(),
            func,
            column,
            where=self._where or None,
            allow_filtering=self._allow_filtering_val,
        )

    @staticmethod
    def _parse_aggregates(funcs: dict[str, str]) -> list[tuple[str, str, str]]:
        parsed = []
        for name, expr in funcs.items():
            func, _, col = expr.partition("(")
            parsed.append((name, func.strip(), col.rstrip(")").strip()))
        return parsed

    def aggregate_sync(self, **funcs: str) -> dict[str, Any]:
        """Execute one or more aggregate functions.

        Each keyword argument maps a result name to a ``"func(column)"``
        expression.  Example::

            result = qs.aggregate_sync(total="sum(price)", avg_price="avg(price)")
            # result == {"total": 150.0, "avg_price": 30.0}
        """
        check_override(type(self), "aggregate", "sync")
        return {
            name: self._execute_one_sync(*self._aggregate_stmt(func, col))
            for name, func, col in self._parse_aggregates(funcs)
        }

    async def aggregate_async(self, **funcs: str) -> dict[str, Any]:
        """Execute one or more aggregate functions. See :meth:`aggregate_sync`."""
        check_override(type(self), "aggregate", "async")
        return {
            name: await self._execute_one_async(*self._aggregate_stmt(func, col))
            for name, func, col in self._parse_aggregates(funcs)
        }

    def sum_sync(self, column: str) -> Any:
        check_override(type(self), "sum", "sync")
        return self._execute_one_sync(*self._aggregate_stmt("SUM", column))

    async def sum_async(self, column: str) -> Any:
        check_override(type(self), "sum", "async")
        return await self._execute_one_async(*self._aggregate_stmt("SUM", column))

    def avg_sync(self, column: str) -> Any:
        check_override(type(self), "avg", "sync")
        return self._execute_one_sync(*self._aggregate_stmt("AVG", column))

    async def avg_async(self, column: str) -> Any:
        check_override(type(self), "avg", "async")
        return await self._execute_one_async(*self._aggregate_stmt("AVG", column))

    def min_sync(self, column: str) -> Any:
        check_override(type(self), "min", "sync")
        return self._execute_one_sync(*self._aggregate_stmt("MIN", column))

    async def min_async(self, column: str) -> Any:
        check_override(type(self), "min", "async")
        return await self._execute_one_async(*self._aggregate_stmt("MIN", column))

    def max_sync(self, column: str) -> Any:
        check_override(type(self), "max", "sync")
        return self._execute_one_sync(*self._aggregate_stmt("MAX", column))

    async def max_async(self, column: str) -> Any:
        check_override(type(self), "max", "async")
        return await self._execute_one_async(*self._aggregate_stmt("MAX", column))

    def _json_stmt(self) -> tuple[str, list[Any]]:
        return build_select_json(
            self._table(),
            self._keyspace(),
            where=self._where or None,
            limit=self._limit_val,
            allow_filtering=self._allow_filtering_val,
        )

    def json_sync(self) -> list[str]:
        """Execute ``SELECT JSON * FROM …`` and return a list of JSON strings."""
        check_override(type(self), "json", "sync")
        return [row.get("[json]", "") for row in self._execute_sync(*self._json_stmt(), **self._cl())]

    async def json_async(self) -> list[str]:
        """Execute ``SELECT JSON * FROM …`` and return a list of JSON strings."""
        check_override(type(self), "json", "async")
        return [row.get("[json]", "") for row in await self._execute_async(*self._json_stmt(), **self._cl())]

    def _column_fn_stmt(self, builder: Any, column: str) -> tuple[str, list[Any]]:
        return builder(
            self._table(),
            self._keyspace(),
            column,
            where=self._where or None,
            allow_filtering=self._allow_filtering_val,
        )

    @staticmethod
    def _scalar(rows: list[dict[str, Any]]) -> Any:
        return next(iter(rows[0].values())) if rows else None

    def writetime_sync(self, column: str) -> Any:
        """Execute ``SELECT WRITETIME("col") FROM …`` and return the scalar result."""
        check_override(type(self), "writetime", "sync")
        return self._scalar(self._execute_sync(*self._column_fn_stmt(build_select_writetime, column), **self._cl()))

    async def writetime_async(self, column: str) -> Any:
        """Execute ``SELECT WRITETIME("col") FROM …`` and return the scalar result."""
        check_override(type(self), "writetime", "async")
        stmt = self._column_fn_stmt(build_select_writetime, column)
        return self._scalar(await self._execute_async(*stmt, **self._cl()))

    def column_ttl_sync(self, column: str) -> Any:
        """Execute ``SELECT TTL("col") FROM …`` and return the scalar result."""
        check_override(type(self), "column_ttl", "sync")
        return self._scalar(self._execute_sync(*self._column_fn_stmt(build_select_column_ttl, column), **self._cl()))

    async def column_ttl_async(self, column: str) -> Any:
        """Execute ``SELECT TTL("col") FROM …`` and return the scalar result."""
        check_override(type(self), "column_ttl", "async")
        stmt = self._column_fn_stmt(build_select_column_ttl, column)
        return self._scalar(await self._execute_async(*stmt, **self._cl()))

    def _delete_stmt(self, if_conditions: dict[str, Any] | None) -> tuple[str, list[Any]]:
        return build_delete(
            self._table(),
            self._keyspace(),
            self._where,
            timestamp=self._timestamp_val,
            if_exists=self._if_exists_val,
            if_conditions=if_conditions,
        )

    def delete_sync(self, if_conditions: dict[str, Any] | None = None) -> LWTResult | None:
        """Delete all matching rows."""
        check_override(type(self), "delete", "sync")
        rows = self._execute_sync(*self._delete_stmt(if_conditions), **self._cl())
        return _parse_lwt_result(rows) if self._if_exists_val or if_conditions else None

    async def delete_async(self, if_conditions: dict[str, Any] | None = None) -> LWTResult | None:
        """Delete all matching rows."""
        check_override(type(self), "delete", "async")
        rows = await self._execute_async(*self._delete_stmt(if_conditions), **self._cl())
        return _parse_lwt_result(rows) if self._if_exists_val or if_conditions else None

    def _create_stmt(self, data: dict[str, Any]) -> tuple[str, list[Any]]:
        return build_insert(
            self._table(),
            self._keyspace(),
            data,
            if_not_exists=self._if_not_exists_val,
            ttl=self._ttl_val,
            timestamp=self._timestamp_val,
        )

    def create_sync(self, **kwargs: Any) -> LWTResult | None:
        """Insert a new document. Respects ``if_not_exists()``, ``ttl()``, and ``timestamp()`` chain modifiers."""
        check_override(type(self), "create", "sync")
        rows = self._execute_sync(*self._create_stmt(kwargs))
        return _parse_lwt_result(rows) if self._if_not_exists_val else None

    async def create_async(self, **kwargs: Any) -> LWTResult | None:
        """Insert a new document. Respects ``if_not_exists()``, ``ttl()``, and ``timestamp()`` chain modifiers."""
        check_override(type(self), "create", "async")
        rows = await self._execute_async(*self._create_stmt(kwargs))
        return _parse_lwt_result(rows) if self._if_not_exists_val else None

    def _update_stmt(
        self, ttl: int | None, if_conditions: dict[str, Any] | None, kwargs: dict[str, Any]
    ) -> tuple[str, list[Any]] | None:
        set_data, collection_ops = parse_update_kwargs(kwargs)
        if not set_data and not collection_ops:
            return None
        return build_update(
            self._table(),
            self._keyspace(),
            set_data,
            self._where,
            ttl=ttl if ttl is not None else self._ttl_val,
            if_conditions=if_conditions,
            collection_ops=collection_ops or None,
        )

    def update_sync(
        self,
        ttl: int | None = None,
        if_conditions: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> LWTResult | None:
        """Bulk UPDATE matching rows. TTL may be provided as a parameter or via the ``ttl()`` chain modifier.

        Returns a :class:`~coodie.results.LWTResult` when *if_conditions* is given, else ``None``.
        """
        check_override(type(self), "update", "sync")
        stmt = self._update_stmt(ttl, if_conditions, kwargs)
        if stmt is None:
            return None
        rows = self._execute_sync(*stmt)
        return _parse_lwt_result(rows) if if_conditions else None

    async def update_async(
        self,
        ttl: int | None = None,
        if_conditions: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> LWTResult | None:
        """Bulk UPDATE matching rows. See :meth:`update_sync`."""
        check_override(type(self), "update", "async")
        stmt = self._update_stmt(ttl, if_conditions, kwargs)
        if stmt is None:
            return None
        rows = await self._execute_async(*stmt)
        return _parse_lwt_result(rows) if if_conditions else None

    def __iter__(self) -> Iterator[Any]:
        return iter(pick(self, "all", "sync")())

    async def __aiter__(self) -> AsyncIterator[Any]:
        for doc in await pick(self, "all", "async")():
            yield doc


def _parse_lwt_result(rows: list[dict[str, Any]]) -> LWTResult:
    """Parse the result of a LWT operation into a :class:`LWTResult`."""
    if not rows:
        return LWTResult(applied=True)
    row = rows[0]
    applied = row.get("[applied]", True)
    existing = None if applied else ({k: v for k, v in row.items() if k != "[applied]"} or None)
    return LWTResult(applied=applied, existing=existing)


_SNAKE_RE1 = re.compile(r"(.)([A-Z][a-z]+)")
_SNAKE_RE2 = re.compile(r"([a-z0-9])([A-Z])")


@functools.lru_cache(maxsize=128)
def _snake_case(name: str) -> str:
    s1 = _SNAKE_RE1.sub(r"\1_\2", name)
    return _SNAKE_RE2.sub(r"\1_\2", s1).lower()
