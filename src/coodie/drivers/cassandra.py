from __future__ import annotations

import asyncio
import logging
import warnings
from typing import Any

from coodie.drivers.base import AbstractDriver, _is_ddl

logger = logging.getLogger("coodie")


class CassandraDriver(AbstractDriver):
    """Driver backed by cassandra-driver / scylla-driver."""

    __slots__ = ("_default_keyspace", "_known_tables", "_last_paging_state", "_prepared", "_session")

    def __init__(
        self,
        session: Any,
        default_keyspace: str | None = None,
    ) -> None:
        self._session = session
        self._default_keyspace = default_keyspace
        self._prepared: dict[str, Any] = {}
        self._last_paging_state: bytes | None = None
        self._known_tables: dict[str, frozenset[str]] = {}
        try:
            from cassandra.query import dict_factory  # type: ignore[import-untyped]

            session.row_factory = dict_factory
        except ImportError:
            logger.warning(
                "Could not import cassandra.query.dict_factory; "
                "session will use its default row_factory (rows may not be dicts)"
            )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _prepare(self, cql: str) -> Any:
        if cql not in self._prepared:
            self._prepared[cql] = self._session.prepare(cql)
        return self._prepared[cql]

    @staticmethod
    def _rows_to_dicts(result_set: Any) -> list[dict[str, Any]]:
        if result_set is None:
            return []
        rows = list(result_set)
        if not rows:
            return []
        sample = rows[0]
        if hasattr(sample, "_asdict"):
            return [dict(r._asdict()) for r in rows]
        elif isinstance(sample, dict):
            return rows
        else:
            return [{k: v for k, v in r.__dict__.items() if not k.startswith("_")} for r in rows]

    # ------------------------------------------------------------------
    # Synchronous interface
    # ------------------------------------------------------------------

    def execute(
        self,
        stmt: str,
        params: list[Any],
        consistency: str | None = None,
        timeout: float | None = None,
        fetch_size: int | None = None,
        paging_state: bytes | None = None,
    ) -> list[dict[str, Any]]:
        if not params and _is_ddl(stmt):
            result = self._session.execute(stmt)
            self._last_paging_state = None
            return self._rows_to_dicts(result)
        prepared = self._prepare(stmt)
        bound = prepared.bind(params)
        if consistency is not None:
            from cassandra import ConsistencyLevel  # type: ignore[import-untyped]

            bound.consistency_level = getattr(ConsistencyLevel, consistency)
        if fetch_size is not None:
            bound.fetch_size = fetch_size
        execute_kwargs: dict[str, Any] = {}
        if timeout is not None:
            execute_kwargs["timeout"] = timeout
        if paging_state is not None:
            execute_kwargs["paging_state"] = paging_state
        result = self._session.execute(bound, **execute_kwargs)
        self._last_paging_state = getattr(result, "paging_state", None)
        if fetch_size is not None:
            return self._rows_to_dicts(result.current_rows)
        return self._rows_to_dicts(result)

    def sync_table(
        self,
        table: str,
        keyspace: str,
        cols: list[Any],
        table_options: dict[str, Any] | None = None,
        dry_run: bool = False,
        drop_removed_indexes: bool = False,
    ) -> list[str]:
        cache_key = f"{keyspace}.{table}"
        col_names = frozenset(col.name for col in cols)
        if not dry_run and not drop_removed_indexes and self._known_tables.get(cache_key) == col_names:
            return []  # table already synced this session with same columns

        from coodie.cql_builder import (
            build_alter_table_options,
            build_create_index,
            build_create_table,
            build_create_vector_index,
            build_drop_index,
        )

        planned: list[str] = []

        # 1. CREATE TABLE IF NOT EXISTS
        create_cql = build_create_table(table, keyspace, cols, table_options=table_options)
        planned.append(create_cql)
        if not dry_run:
            self._session.execute(create_cql)

        # 2. Introspect existing columns and add missing ones
        existing = self._get_existing_columns(table, keyspace)
        model_col_names = {col.name for col in cols}
        is_new_table = existing == model_col_names

        if not is_new_table:
            for col in cols:
                if col.name not in existing:
                    alter = f'ALTER TABLE {keyspace}.{table} ADD "{col.name}" {col.cql_type}'
                    planned.append(alter)
                    if not dry_run:
                        self._session.execute(alter)

        # 3. Schema drift detection — warn on DB columns not in model
        drift_cols = existing - model_col_names
        if drift_cols:
            logger.warning(
                "Schema drift detected: columns %s exist in %s.%s but are not defined in the model",
                drift_cols,
                keyspace,
                table,
            )

        # 4. Table option changes
        if table_options:
            current_options = self._get_current_table_options(table, keyspace)
            changed = {}
            for k, v in table_options.items():
                if str(current_options.get(k)) != str(v):
                    changed[k] = v
            if changed:
                alter_cql = build_alter_table_options(table, keyspace, changed)
                planned.append(alter_cql)
                if not dry_run:
                    self._session.execute(alter_cql)

        # 5. Create secondary indexes and vector indexes
        model_indexes: dict[str, Any] = {}
        for col in cols:
            if col.index:
                idx_name = col.index_name or f"{table}_{col.name}_idx"
                model_indexes[idx_name] = col
                index_cql = build_create_index(table, keyspace, col)
                planned.append(index_cql)
                if not dry_run:
                    self._session.execute(index_cql)
            if getattr(col, "vector_index", False):
                idx_name = f"{table}_{col.name}_idx"
                model_indexes[idx_name] = col
                vec_idx_cql = build_create_vector_index(table, keyspace, col)
                planned.append(vec_idx_cql)
                if not dry_run:
                    try:
                        self._session.execute(vec_idx_cql)
                    except Exception as _exc:  # noqa: BLE001 - any failure is inspected for missing SAI support
                        self._warn_if_sai_unsupported(_exc)

        # 6. Drop removed indexes
        if drop_removed_indexes:
            existing_indexes = self._get_existing_indexes(table, keyspace)
            for idx_name in existing_indexes:
                if idx_name not in model_indexes:
                    drop_cql = build_drop_index(idx_name, keyspace)
                    planned.append(drop_cql)
                    if not dry_run:
                        self._session.execute(drop_cql)

        if not dry_run:
            self._known_tables[cache_key] = col_names
            self._warm_prepared_cache(table, keyspace, cols)

        return planned

    def _warn_if_sai_unsupported(self, exc: Exception) -> None:
        """Emit a warning when vector index creation is not supported by the database.

        Raises the original exception unchanged for any other ``InvalidRequest`` error.
        """
        try:
            from cassandra import InvalidRequest  # type: ignore[import-untyped]

            if not isinstance(exc, InvalidRequest):
                raise exc
        except ImportError:
            pass
        _msg = str(exc)
        # Known patterns indicating vector index creation is not supported in this configuration:
        # - "Non-supported custom class": index class not available (older ScyllaDB/Cassandra)
        # - "use tablets": keyspace must be tablets-enabled for vector indexes (newer ScyllaDB).
        #   Full message: "Vector index requires the base table's keyspace to use tablets."
        if (
            "Non-supported custom class" in _msg
            or "use tablets" in _msg
            or "not supported on base tables with tablets" in _msg
        ):
            warnings.warn(
                f"Vector index creation skipped: vector search not supported by this database. {exc}",
                stacklevel=3,
            )
        else:
            raise exc

    def _warm_prepared_cache(self, table: str, keyspace: str, cols: list[Any]) -> None:
        """Pre-prepare SELECT-by-PK and INSERT queries to eliminate cold-start latency."""
        pk_cols = sorted((c for c in cols if c.primary_key), key=lambda c: c.partition_key_index)
        ck_cols = sorted((c for c in cols if c.clustering_key), key=lambda c: c.clustering_key_index)
        key_cols = pk_cols + ck_cols
        if key_cols:
            where_clause = " AND ".join(f'"{c.name}" = ?' for c in key_cols)
            self._prepare(f"SELECT * FROM {keyspace}.{table} WHERE {where_clause}")
        # Counter tables do not support INSERT — only UPDATE … SET col = col + ?.
        is_counter_table = any(getattr(c, "cql_type", None) == "counter" for c in cols)
        if not is_counter_table:
            all_col_names = ", ".join(f'"{c.name}"' for c in cols)
            placeholders = ", ".join("?" * len(cols))
            self._prepare(f"INSERT INTO {keyspace}.{table} ({all_col_names}) VALUES ({placeholders})")

    def _get_existing_columns(self, table: str, keyspace: str) -> set[str]:
        rows = self._session.execute(
            "SELECT column_name FROM system_schema.columns WHERE keyspace_name = %s AND table_name = %s",
            (keyspace, table),
        )
        return {r["column_name"] for r in self._rows_to_dicts(rows)}

    def _get_current_table_options(self, table: str, keyspace: str) -> dict[str, Any]:
        """Introspect current table options from ``system_schema.tables``."""
        rows = self._session.execute(
            "SELECT * FROM system_schema.tables WHERE keyspace_name = %s AND table_name = %s",
            (keyspace, table),
        )
        dicts = self._rows_to_dicts(rows)
        if dicts:
            return dicts[0]
        return {}

    def _get_existing_indexes(self, table: str, keyspace: str) -> set[str]:
        """Introspect existing index names from ``system_schema.indexes``."""
        rows = self._session.execute(
            "SELECT index_name FROM system_schema.indexes WHERE keyspace_name = %s AND table_name = %s",
            (keyspace, table),
        )
        return {r["index_name"] for r in self._rows_to_dicts(rows)}

    # ------------------------------------------------------------------
    # One-row shortcut — bypasses _rows_to_dicts() and list() allocation
    # ------------------------------------------------------------------

    def execute_one(
        self,
        stmt: str,
        params: list[Any],
        consistency: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        prepared = self._prepare(stmt)
        bound = prepared.bind(params)
        if consistency is not None:
            from cassandra import ConsistencyLevel  # type: ignore[import-untyped]

            bound.consistency_level = getattr(ConsistencyLevel, consistency)
        execute_kwargs: dict[str, Any] = {}
        if timeout is not None:
            execute_kwargs["timeout"] = timeout
        result = self._session.execute(bound, **execute_kwargs)
        row = result.one()
        if row is None:
            return None
        if isinstance(row, dict):
            return next(iter(row.values()))
        if hasattr(row, "_asdict"):
            return next(iter(row._asdict().values()))
        return row[0]

    async def execute_one_async(
        self,
        stmt: str,
        params: list[Any],
        consistency: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        prepared = self._prepare(stmt)
        bound = prepared.bind(params)
        if consistency is not None:
            from cassandra import ConsistencyLevel  # type: ignore[import-untyped]

            bound.consistency_level = getattr(ConsistencyLevel, consistency)
        execute_kwargs: dict[str, Any] = {}
        if timeout is not None:
            execute_kwargs["timeout"] = timeout
        future = self._session.execute_async(bound, **execute_kwargs)
        result = await self._wrap_future(future)
        if result is None:
            return None
        # The callback bridge delivers a plain list (not a ResultSet),
        # so we index into it directly instead of using .one().
        if isinstance(result, list):
            row = result[0] if result else None
        else:
            row = result.one()
        if row is None:
            return None
        if isinstance(row, dict):
            return next(iter(row.values()))
        if hasattr(row, "_asdict"):
            return next(iter(row._asdict().values()))
        return row[0]

    def close(self) -> None:
        self._session.cluster.shutdown()

    # ------------------------------------------------------------------
    # Asynchronous interface (asyncio bridge)
    # ------------------------------------------------------------------

    def _wrap_future(self, driver_future: Any) -> asyncio.Future[Any]:
        """Bridge a cassandra-driver ``ResponseFuture`` to an :mod:`asyncio` Future."""
        loop = asyncio.get_running_loop()
        result_future: asyncio.Future[Any] = loop.create_future()

        def on_success(result: Any) -> None:
            loop.call_soon_threadsafe(result_future.set_result, result)

        def on_error(exc: Exception) -> None:
            loop.call_soon_threadsafe(result_future.set_exception, exc)

        driver_future.add_callbacks(on_success, on_error)
        return result_future

    async def execute_async(
        self,
        stmt: str,
        params: list[Any],
        consistency: str | None = None,
        timeout: float | None = None,
        fetch_size: int | None = None,
        paging_state: bytes | None = None,
    ) -> list[dict[str, Any]]:
        if fetch_size is not None:
            # Paginated queries: delegate to the sync execute() via
            # run_in_executor.  The cassandra-driver's async callback
            # mechanism delivers a plain list to add_callbacks, not a
            # ResultSet, so current_rows / paging_state are unavailable.
            # The sync path (session.execute) returns a proper ResultSet.
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(
                None,
                lambda: self.execute(
                    stmt,
                    params,
                    consistency=consistency,
                    timeout=timeout,
                    fetch_size=fetch_size,
                    paging_state=paging_state,
                ),
            )
        prepared = self._prepare(stmt)
        bound = prepared.bind(params)
        if consistency is not None:
            from cassandra import ConsistencyLevel  # type: ignore[import-untyped]

            bound.consistency_level = getattr(ConsistencyLevel, consistency)
        execute_kwargs: dict[str, Any] = {}
        if timeout is not None:
            execute_kwargs["timeout"] = timeout
        future = self._session.execute_async(bound, **execute_kwargs)
        result = await self._wrap_future(future)
        self._last_paging_state = None
        return self._rows_to_dicts(result)

    async def _execute_cql_async(self, cql: str) -> Any:
        """Execute a raw CQL string asynchronously via the callback bridge."""
        future = self._session.execute_async(cql)
        return await self._wrap_future(future)

    async def _execute_bound_async(self, cql: str, params: tuple[Any, ...]) -> Any:
        """Execute a parameterised CQL string asynchronously via the callback bridge."""
        future = self._session.execute_async(cql, params)
        return await self._wrap_future(future)

    async def sync_table_async(
        self,
        table: str,
        keyspace: str,
        cols: list[Any],
        table_options: dict[str, Any] | None = None,
        dry_run: bool = False,
        drop_removed_indexes: bool = False,
    ) -> list[str]:
        cache_key = f"{keyspace}.{table}"
        col_names = frozenset(col.name for col in cols)
        if not dry_run and not drop_removed_indexes and self._known_tables.get(cache_key) == col_names:
            return []  # table already synced this session with same columns

        from coodie.cql_builder import (
            build_alter_table_options,
            build_create_index,
            build_create_table,
            build_create_vector_index,
            build_drop_index,
        )

        planned: list[str] = []

        # 1. CREATE TABLE IF NOT EXISTS
        create_cql = build_create_table(table, keyspace, cols, table_options=table_options)
        planned.append(create_cql)
        if not dry_run:
            await self._execute_cql_async(create_cql)

        # 2. Introspect existing columns and add missing ones
        existing = await self._get_existing_columns_async(table, keyspace)
        model_col_names = {col.name for col in cols}
        is_new_table = existing == model_col_names

        if not is_new_table:
            for col in cols:
                if col.name not in existing:
                    alter = f'ALTER TABLE {keyspace}.{table} ADD "{col.name}" {col.cql_type}'
                    planned.append(alter)
                    if not dry_run:
                        await self._execute_cql_async(alter)

        # 3. Schema drift detection — warn on DB columns not in model
        drift_cols = existing - model_col_names
        if drift_cols:
            logger.warning(
                "Schema drift detected: columns %s exist in %s.%s but are not defined in the model",
                drift_cols,
                keyspace,
                table,
            )

        # 4. Table option changes
        if table_options:
            current_options = await self._get_current_table_options_async(table, keyspace)
            changed = {}
            for k, v in table_options.items():
                if str(current_options.get(k)) != str(v):
                    changed[k] = v
            if changed:
                alter_cql = build_alter_table_options(table, keyspace, changed)
                planned.append(alter_cql)
                if not dry_run:
                    await self._execute_cql_async(alter_cql)

        # 5. Create secondary indexes and vector indexes
        model_indexes: dict[str, Any] = {}
        for col in cols:
            if col.index:
                idx_name = col.index_name or f"{table}_{col.name}_idx"
                model_indexes[idx_name] = col
                index_cql = build_create_index(table, keyspace, col)
                planned.append(index_cql)
                if not dry_run:
                    await self._execute_cql_async(index_cql)
            if getattr(col, "vector_index", False):
                idx_name = f"{table}_{col.name}_idx"
                model_indexes[idx_name] = col
                vec_idx_cql = build_create_vector_index(table, keyspace, col)
                planned.append(vec_idx_cql)
                if not dry_run:
                    try:
                        await self._execute_cql_async(vec_idx_cql)
                    except Exception as _exc:  # noqa: BLE001 - any failure is inspected for missing SAI support
                        self._warn_if_sai_unsupported(_exc)

        # 6. Drop removed indexes
        if drop_removed_indexes:
            existing_indexes = await self._get_existing_indexes_async(table, keyspace)
            for idx_name in existing_indexes:
                if idx_name not in model_indexes:
                    drop_cql = build_drop_index(idx_name, keyspace)
                    planned.append(drop_cql)
                    if not dry_run:
                        await self._execute_cql_async(drop_cql)

        if not dry_run:
            self._known_tables[cache_key] = col_names
            self._warm_prepared_cache(table, keyspace, cols)

        return planned

    async def _get_existing_columns_async(self, table: str, keyspace: str) -> set[str]:
        rows = await self._execute_bound_async(
            "SELECT column_name FROM system_schema.columns WHERE keyspace_name = %s AND table_name = %s",
            (keyspace, table),
        )
        return {r["column_name"] for r in self._rows_to_dicts(rows)}

    async def _get_current_table_options_async(self, table: str, keyspace: str) -> dict[str, Any]:
        """Introspect current table options from ``system_schema.tables``."""
        rows = await self._execute_bound_async(
            "SELECT * FROM system_schema.tables WHERE keyspace_name = %s AND table_name = %s",
            (keyspace, table),
        )
        dicts = self._rows_to_dicts(rows)
        if dicts:
            return dicts[0]
        return {}

    async def _get_existing_indexes_async(self, table: str, keyspace: str) -> set[str]:
        """Introspect existing index names from ``system_schema.indexes``."""
        rows = await self._execute_bound_async(
            "SELECT index_name FROM system_schema.indexes WHERE keyspace_name = %s AND table_name = %s",
            (keyspace, table),
        )
        return {r["index_name"] for r in self._rows_to_dicts(rows)}

    async def close_async(self) -> None:
        self.close()
