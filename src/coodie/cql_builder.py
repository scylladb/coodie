from __future__ import annotations

import functools
import re
from typing import Any

from coodie.schema import ColumnDefinition

_UNQUOTED_IDENT_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
try:
    # scylla-driver / cassandra-driver keep this list in step with the server; use theirs when installed.
    from cassandra.metadata import cql_keywords_reserved as _RESERVED_KEYWORDS
except ImportError:  # acsylla / python-rs expose none; fall back to the CQL reserved words
    _RESERVED_KEYWORDS = frozenset(
        "add allow alter and apply asc authorize batch begin by columnfamily create delete desc describe "  # noqa: SIM905
        "drop entries execute from full grant if in index infinity insert into is keyspace limit materialized "
        "mbean mbeans modify nan norecursive not null of on or order primary rename replace revoke schema "
        "select set table to token truncate unlogged unset update use using view where with".split()
    )


def _is_quoted(name: str) -> bool:
    return len(name) > 1 and name[0] == name[-1] == '"'


@functools.lru_cache(maxsize=1024)
def quote_ident(name: str) -> str:
    """Return a keyspace/table/type/index name ready to embed in CQL.

    Follows CQL rules: unquoted names are case-insensitive (folded to
    lowercase), so plain names are returned unchanged and only reserved
    words or names with other characters get quoted.  Wrap a name in
    double quotes (e.g. ``Settings.name = '"MyTable"'``) to make it
    case-sensitive; already-quoted names are returned as-is.
    """
    if _is_quoted(name):
        return name
    if _UNQUOTED_IDENT_RE.fullmatch(name) and name.lower() not in _RESERVED_KEYWORDS:
        return name
    return '"' + name.lower().replace('"', '""') + '"'


def schema_name(name: str) -> str:
    """Return *name* as stored in ``system_schema`` (lowercased unless quoted)."""
    if _is_quoted(name):
        return name[1:-1].replace('""', '"')
    return name.lower()


@functools.lru_cache(maxsize=1024)
def qualified_name(keyspace: str, name: str) -> str:
    """Return ``keyspace.name`` with both parts passed through :func:`quote_ident`."""
    return f"{quote_ident(keyspace)}.{quote_ident(name)}"


def build_create_keyspace(
    keyspace: str,
    replication_factor: int = 1,
    strategy: str = "SimpleStrategy",
    dc_replication_map: dict[str, int] | None = None,
) -> str:
    if dc_replication_map is not None:
        strategy = "NetworkTopologyStrategy"
        dc_parts = ", ".join(f"'{dc}': '{rf}'" for dc, rf in dc_replication_map.items())
        return f"CREATE KEYSPACE IF NOT EXISTS {quote_ident(keyspace)} WITH replication = {{'class': '{strategy}', {dc_parts}}}"
    return (
        f"CREATE KEYSPACE IF NOT EXISTS {quote_ident(keyspace)} "
        f"WITH replication = {{'class': '{strategy}', "
        f"'replication_factor': '{replication_factor}'}}"
    )


def build_drop_keyspace(keyspace: str) -> str:
    return f"DROP KEYSPACE IF EXISTS {quote_ident(keyspace)}"


def build_create_table(
    table: str,
    keyspace: str,
    cols: list[ColumnDefinition],
    table_options: dict[str, Any] | None = None,
) -> str:
    col_defs = []
    for col in cols:
        col_def = f'"{col.name}" {col.cql_type}'
        if col.static:
            col_def += " STATIC"
        col_defs.append(col_def)

    # Partition key columns (ordered by partition_key_index)
    pk_cols = [c for c in cols if c.primary_key]
    pk_cols.sort(key=lambda c: c.partition_key_index)

    # Clustering key columns (ordered by clustering_key_index)
    ck_cols = [c for c in cols if c.clustering_key]
    ck_cols.sort(key=lambda c: c.clustering_key_index)

    if not pk_cols:
        raise ValueError(f"Table {table} has no primary key columns")

    if len(pk_cols) == 1:
        pk_str = f'"{pk_cols[0].name}"'
    else:
        pk_str = "(" + ", ".join(f'"{c.name}"' for c in pk_cols) + ")"

    if ck_cols:
        primary_key = f"PRIMARY KEY ({pk_str}, " + ", ".join(f'"{c.name}"' for c in ck_cols) + ")"
    else:
        primary_key = f"PRIMARY KEY ({pk_str})"

    col_defs_str = ", ".join(col_defs)

    clustering_order_parts = []
    if any(c.clustering_order != "ASC" for c in ck_cols):
        clustering_order_parts = [f'"{c.name}" {c.clustering_order}' for c in ck_cols]

    with_parts: list[str] = []
    if clustering_order_parts:
        with_parts.append("CLUSTERING ORDER BY (" + ", ".join(clustering_order_parts) + ")")
    if table_options:
        for k, v in table_options.items():
            if isinstance(v, str):
                with_parts.append(f"{k} = '{v}'")
            else:
                with_parts.append(f"{k} = {v}")

    with_clause = ""
    if with_parts:
        with_clause = " WITH " + " AND ".join(with_parts)

    return f"CREATE TABLE IF NOT EXISTS {qualified_name(keyspace, table)} ({col_defs_str}, {primary_key}){with_clause}"


def build_create_index(
    table: str,
    keyspace: str,
    col: ColumnDefinition,
) -> str:
    index_name = col.index_name or f"{schema_name(table)}_{col.name}_idx"
    return f'CREATE INDEX IF NOT EXISTS {quote_ident(index_name)} ON {qualified_name(keyspace, table)} ("{col.name}")'


def build_create_custom_index(
    table: str,
    keyspace: str,
    col: ColumnDefinition,
    index_class: str = "org.apache.cassandra.index.sai.StorageAttachedIndex",
    options: dict[str, str] | None = None,
) -> str:
    index_name = col.vector_index_name or f"{schema_name(table)}_{col.name}_idx"
    cql = f"CREATE CUSTOM INDEX IF NOT EXISTS {quote_ident(index_name)} ON {qualified_name(keyspace, table)} (\"{col.name}\") USING '{index_class}'"
    if options:
        opts_str = ", ".join(f"'{k}': '{v}'" for k, v in options.items())
        cql += f" WITH OPTIONS = {{{opts_str}}}"
    return cql


def build_create_vector_index(
    table: str,
    keyspace: str,
    col: ColumnDefinition,
) -> str:
    """Build a ``CREATE CUSTOM INDEX`` for a vector column using ``'vector_index'``."""
    return build_create_custom_index(table, keyspace, col, index_class="vector_index", options=col.vector_index_options)


def build_drop_index(index_name: str, keyspace: str) -> str:
    """*index_name* is as stored in ``system_schema``, so its case is kept."""
    if index_name != index_name.lower():
        index_name = '"' + index_name.replace('"', '""') + '"'
    return f"DROP INDEX IF EXISTS {qualified_name(keyspace, index_name)}"


def build_alter_table_options(
    table: str,
    keyspace: str,
    options: dict[str, Any],
) -> str:
    parts = []
    for k, v in options.items():
        if isinstance(v, str):
            parts.append(f"{k} = '{v}'")
        else:
            parts.append(f"{k} = {v}")
    return f"ALTER TABLE {qualified_name(keyspace, table)} WITH " + " AND ".join(parts)


def build_truncate(table: str, keyspace: str) -> str:
    return f"TRUNCATE TABLE {qualified_name(keyspace, table)}"


def build_drop_table(table: str, keyspace: str) -> str:
    return f"DROP TABLE IF EXISTS {qualified_name(keyspace, table)}"


def build_create_materialized_view(
    view_name: str,
    keyspace: str,
    base_table: str,
    columns: list[str],
    primary_key_columns: list[str],
    clustering_columns: list[str] | None = None,
    where_clause: str | None = None,
    clustering_order: dict[str, str] | None = None,
) -> str:
    cols_str = ", ".join(c if c == "*" else f'"{c}"' for c in columns)

    if len(primary_key_columns) == 1:
        pk_str = f'"{primary_key_columns[0]}"'
    else:
        pk_str = "(" + ", ".join(f'"{c}"' for c in primary_key_columns) + ")"

    if clustering_columns:
        key_str = f"PRIMARY KEY ({pk_str}, " + ", ".join(f'"{c}"' for c in clustering_columns) + ")"
    else:
        key_str = f"PRIMARY KEY ({pk_str})"

    cql = (
        f"CREATE MATERIALIZED VIEW IF NOT EXISTS {qualified_name(keyspace, view_name)} "
        f"AS SELECT {cols_str} FROM {qualified_name(keyspace, base_table)}"
    )

    if where_clause:
        cql += f" WHERE {where_clause}"

    cql += f" {key_str}"

    with_parts: list[str] = []
    if clustering_order:
        order_parts = [f'"{c}" {d}' for c, d in clustering_order.items()]
        with_parts.append("CLUSTERING ORDER BY (" + ", ".join(order_parts) + ")")

    if with_parts:
        cql += " WITH " + " AND ".join(with_parts)

    return cql


def build_drop_materialized_view(view_name: str, keyspace: str) -> str:
    return f"DROP MATERIALIZED VIEW IF EXISTS {qualified_name(keyspace, view_name)}"


def parse_filter_kwargs(
    kwargs: dict[str, Any],
) -> list[tuple[str, str, Any]]:
    operators = {
        "gt": ">",
        "gte": ">=",
        "lt": "<",
        "lte": "<=",
        "in": "IN",
        "contains": "CONTAINS",
        "contains_key": "CONTAINS KEY",
        "like": "LIKE",
        "ne": "!=",
        "isnull": "ISNULL",
    }
    token_operators = {
        "token__gt": "TOKEN >",
        "token__gte": "TOKEN >=",
        "token__lt": "TOKEN <",
        "token__lte": "TOKEN <=",
    }
    result = []
    for key, value in kwargs.items():
        parts2 = key.rsplit("__", 2)
        if len(parts2) == 3:
            col, mid, op = parts2
            token_key = f"{mid}__{op}"
            if token_key in token_operators:
                result.append((col, token_operators[token_key], value))
                continue
        parts = key.rsplit("__", 1)
        if len(parts) == 2 and parts[1] in operators:
            col, op_key = parts
            result.append((col, operators[op_key], value))
        else:
            result.append((key, "=", value))
    return result


def build_where_clause(
    filter_triples: list[tuple[str, str, Any]],
) -> tuple[str, list[Any]]:
    if not filter_triples:
        return "", []
    parts = []
    params: list[Any] = []
    for col, op, value in filter_triples:
        if op == "ISNULL":
            if value:
                parts.append(f'"{col}" IS NULL')
            else:
                parts.append(f'"{col}" IS NOT NULL')
        elif op.startswith("TOKEN "):
            actual_op = op[len("TOKEN ") :]
            parts.append(f'TOKEN("{col}") {actual_op} ?')
            params.append(value)
        elif op == "IN":
            placeholders = ", ".join("?" * len(value))
            parts.append(f'"{col}" IN ({placeholders})')
            params.extend(value)
        else:
            parts.append(f'"{col}" {op} ?')
            params.append(value)
    return "WHERE " + " AND ".join(parts), params


# ---------------------------------------------------------------------------
# Shared helpers for CQL template caching
# ---------------------------------------------------------------------------


def _where_to_shape(where: list[tuple[str, str, Any]]) -> tuple:
    """Convert WHERE triples into a hashable shape tuple (excludes values)."""
    parts = []
    for col, op, value in where:
        if op == "IN":
            parts.append((col, op, len(value)))
        elif op == "ISNULL":
            parts.append((col, op, value))
        else:
            parts.append((col, op))
    return tuple(parts)


def _extract_where_params(where: list[tuple[str, str, Any]], params: list[Any]) -> None:
    """Append bind-parameter values from WHERE triples into *params*."""
    for _col, op, value in where:
        if op == "ISNULL":
            pass  # IS [NOT] NULL has no params
        elif op == "IN":
            params.extend(value)
        else:
            params.append(value)


_select_cql_cache: dict[tuple, str] = {}


def build_select(
    table: str,
    keyspace: str,
    columns: list[str] | None = None,
    where: list[tuple[str, str, Any]] | None = None,
    limit: int | None = None,
    order_by: list[str] | None = None,
    allow_filtering: bool = False,
    per_partition_limit: int | None = None,
    distinct: bool = False,
    group_by: list[str] | None = None,
    select_token: list[str] | None = None,
    cast: list[tuple[str, str]] | None = None,
    ann_of: tuple[str, list[float]] | None = None,
) -> tuple[str, list[Any]]:
    # Build the cache key from the query *shape* (excludes actual values).
    where_shape = _where_to_shape(where) if where else ()
    cache_key = (
        table,
        keyspace,
        tuple(columns) if columns else None,
        where_shape,
        limit,
        None if ann_of else (tuple(order_by) if order_by else None),
        allow_filtering,
        per_partition_limit,
        distinct,
        tuple(group_by) if group_by else None,
        tuple(select_token) if select_token else None,
        tuple(cast) if cast else None,
        ann_of[0] if ann_of else None,
    )

    params: list[Any] = []
    if where:
        _extract_where_params(where, params)

    # ANN vector param is appended after WHERE params.
    if ann_of is not None:
        params.append(ann_of[1])

    cached_cql = _select_cql_cache.get(cache_key)
    if cached_cql is not None:
        return cached_cql, params

    cols_str = ", ".join(f'"{c}"' for c in columns) if columns else "*"

    if cast:
        cast_parts = [f'CAST("{c}" AS {t})' for c, t in cast]
        cols_str += ", " + ", ".join(cast_parts)

    if select_token:
        token_cols = ", ".join(f'"{c}"' for c in select_token)
        cols_str += f", TOKEN({token_cols})"

    keyword = "SELECT DISTINCT" if distinct else "SELECT"
    cql = f"{keyword} {cols_str} FROM {qualified_name(keyspace, table)}"

    if where:
        clause, _wp = build_where_clause(where)
        if clause:
            cql += " " + clause

    if group_by:
        gb_parts = ", ".join(f'"{c}"' for c in group_by)
        cql += f" GROUP BY {gb_parts}"

    if ann_of is not None:
        cql += f' ORDER BY "{ann_of[0]}" ANN OF ?'
    elif order_by:
        order_parts = []
        for col in order_by:
            if col.startswith("-"):
                order_parts.append(f'"{col[1:]}" DESC')
            else:
                order_parts.append(f'"{col}" ASC')
        cql += " ORDER BY " + ", ".join(order_parts)

    if per_partition_limit is not None:
        cql += f" PER PARTITION LIMIT {per_partition_limit}"

    if limit is not None:
        cql += f" LIMIT {limit}"

    if allow_filtering:
        cql += " ALLOW FILTERING"

    _select_cql_cache[cache_key] = cql
    return cql, params


# Cache for COUNT CQL templates keyed by query shape.
_count_cql_cache: dict[tuple, str] = {}


def build_count(
    table: str,
    keyspace: str,
    where: list[tuple[str, str, Any]] | None = None,
    allow_filtering: bool = False,
) -> tuple[str, list[Any]]:
    where_shape = _where_to_shape(where) if where else ()
    cache_key = (table, keyspace, where_shape, allow_filtering)

    params: list[Any] = []
    if where:
        _extract_where_params(where, params)

    cached_cql = _count_cql_cache.get(cache_key)
    if cached_cql is not None:
        return cached_cql, params

    cql = f"SELECT COUNT(*) FROM {qualified_name(keyspace, table)}"

    if where:
        clause, _wp = build_where_clause(where)
        if clause:
            cql += " " + clause

    if allow_filtering:
        cql += " ALLOW FILTERING"

    _count_cql_cache[cache_key] = cql
    return cql, params


# Cache for aggregate CQL templates keyed by query shape.
_aggregate_cql_cache: dict[tuple, str] = {}


def build_aggregate(
    table: str,
    keyspace: str,
    func: str,
    column: str,
    where: list[tuple[str, str, Any]] | None = None,
    allow_filtering: bool = False,
) -> tuple[str, list[Any]]:
    where_shape = _where_to_shape(where) if where else ()
    cache_key = (table, keyspace, func.upper(), column, where_shape, allow_filtering)

    params: list[Any] = []
    if where:
        _extract_where_params(where, params)

    cached_cql = _aggregate_cql_cache.get(cache_key)
    if cached_cql is not None:
        return cached_cql, params

    cql = f'SELECT {func.upper()}("{column}") FROM {qualified_name(keyspace, table)}'

    if where:
        clause, _wp = build_where_clause(where)
        if clause:
            cql += " " + clause

    if allow_filtering:
        cql += " ALLOW FILTERING"

    _aggregate_cql_cache[cache_key] = cql
    return cql, params


def _build_using_clause(
    ttl: int | None = None,
    timestamp: int | None = None,
) -> str:
    parts: list[str] = []
    if ttl is not None:
        parts.append(f"TTL {ttl}")
    if timestamp is not None:
        parts.append(f"TIMESTAMP {timestamp}")
    if not parts:
        return ""
    return " USING " + " AND ".join(parts)


def build_insert(
    table: str,
    keyspace: str,
    data: dict[str, Any],
    ttl: int | None = None,
    if_not_exists: bool = False,
    timestamp: int | None = None,
) -> tuple[str, list[Any]]:
    cols = list(data.keys())
    vals = list(data.values())
    cols_str = ", ".join(f'"{c}"' for c in cols)
    placeholders = ", ".join("?" * len(cols))
    cql = f"INSERT INTO {qualified_name(keyspace, table)} ({cols_str}) VALUES ({placeholders})"
    if if_not_exists:
        cql += " IF NOT EXISTS"
    cql += _build_using_clause(ttl=ttl, timestamp=timestamp)
    return cql, vals


_insert_cql_cache: dict[tuple, str] = {}


def build_insert_from_columns(
    table: str,
    keyspace: str,
    columns: tuple[str, ...],
    values: list[Any],
    ttl: int | None = None,
    if_not_exists: bool = False,
    timestamp: int | None = None,
) -> tuple[str, list[Any]]:
    cache_key = (table, keyspace, columns, if_not_exists)
    base_cql = _insert_cql_cache.get(cache_key)
    if base_cql is None:
        cols_str = ", ".join(f'"{c}"' for c in columns)
        placeholders = ", ".join("?" * len(columns))
        base_cql = f"INSERT INTO {qualified_name(keyspace, table)} ({cols_str}) VALUES ({placeholders})"
        if if_not_exists:
            base_cql += " IF NOT EXISTS"
        _insert_cql_cache[cache_key] = base_cql
    cql = base_cql + _build_using_clause(ttl=ttl, timestamp=timestamp)
    return cql, values


def build_insert_json(
    table: str,
    keyspace: str,
    json_string: str,
    ttl: int | None = None,
    if_not_exists: bool = False,
    timestamp: int | None = None,
) -> tuple[str, list[Any]]:
    """Build an ``INSERT INTO … JSON ?`` CQL statement.

    The *json_string* is bound as a positional parameter so the driver
    handles escaping.
    """
    cql = f"INSERT INTO {qualified_name(keyspace, table)} JSON ?"
    if if_not_exists:
        cql += " IF NOT EXISTS"
    cql += _build_using_clause(ttl=ttl, timestamp=timestamp)
    return cql, [json_string]


def build_select_json(
    table: str,
    keyspace: str,
    where: list[tuple[str, str, Any]] | None = None,
    limit: int | None = None,
    allow_filtering: bool = False,
) -> tuple[str, list[Any]]:
    """Build a ``SELECT JSON * FROM …`` CQL statement.

    Returns rows where each row is a dict with a single ``"[json]"`` key
    containing the JSON string representation of the row.
    """
    cql = f"SELECT JSON * FROM {qualified_name(keyspace, table)}"
    params: list[Any] = []

    if where:
        clause, where_params = build_where_clause(where)
        if clause:
            cql += " " + clause
            params.extend(where_params)

    if limit is not None:
        cql += f" LIMIT {limit}"

    if allow_filtering:
        cql += " ALLOW FILTERING"

    return cql, params


def build_select_writetime(
    table: str,
    keyspace: str,
    column: str,
    where: list[tuple[str, str, Any]] | None = None,
    allow_filtering: bool = False,
) -> tuple[str, list[Any]]:
    """Build a ``SELECT WRITETIME("col") FROM …`` CQL statement."""
    cql = f'SELECT WRITETIME("{column}") FROM {qualified_name(keyspace, table)}'
    params: list[Any] = []

    if where:
        clause, where_params = build_where_clause(where)
        if clause:
            cql += " " + clause
            params.extend(where_params)

    if allow_filtering:
        cql += " ALLOW FILTERING"

    return cql, params


def build_select_column_ttl(
    table: str,
    keyspace: str,
    column: str,
    where: list[tuple[str, str, Any]] | None = None,
    allow_filtering: bool = False,
) -> tuple[str, list[Any]]:
    """Build a ``SELECT TTL("col") FROM …`` CQL statement."""
    cql = f'SELECT TTL("{column}") FROM {qualified_name(keyspace, table)}'
    params: list[Any] = []

    if where:
        clause, where_params = build_where_clause(where)
        if clause:
            cql += " " + clause
            params.extend(where_params)

    if allow_filtering:
        cql += " ALLOW FILTERING"

    return cql, params


def parse_update_kwargs(
    kwargs: dict[str, Any],
) -> tuple[dict[str, Any], list[tuple[str, str, Any]]]:
    """Parse update kwargs into regular set data and collection operations.

    Returns ``(set_data, collection_ops)`` where *collection_ops* is a list of
    ``(column, operator, value)`` tuples.  Supported operators: ``add``,
    ``remove``, ``append``, ``prepend``, ``update`` (alias for ``add``),
    ``put`` (map element set), ``setindex`` (list element set by index).

    For ``put`` and ``setindex`` the *value* must be a ``(key_or_index, val)``
    tuple which generates ``"col"[?] = ?``.
    """
    collection_operators = {"add", "remove", "append", "prepend", "update", "put", "setindex"}
    set_data: dict[str, Any] = {}
    collection_ops: list[tuple[str, str, Any]] = []
    for key, value in kwargs.items():
        parts = key.rsplit("__", 1)
        if len(parts) == 2 and parts[1] in collection_operators:
            col, op = parts
            collection_ops.append((col, op, value))
        else:
            set_data[key] = value
    return set_data, collection_ops


# Cache for UPDATE CQL templates keyed by query shape.
_update_cql_cache: dict[tuple, str] = {}

_IF_OPS: dict[str, str] = {"ne": "!=", "gt": ">", "lt": "<", "gte": ">=", "lte": "<=", "in": "IN"}


def _parse_if_conditions(
    conditions: dict[str, Any],
) -> tuple[str, list[Any]]:
    """Parse an ``if_conditions`` dict into a CQL ``IF`` clause and parameter list.

    Keys may use Django-style operator suffixes: ``col__ne`` (``!=``),
    ``col__gt`` (``>``), ``col__lt`` (``<``), ``col__gte`` (``>=``),
    ``col__lte`` (``<=``), ``col__in`` (``IN``).  Plain keys default to ``=``.
    """
    parts: list[str] = []
    params: list[Any] = []
    for key, value in conditions.items():
        pieces = key.rsplit("__", 1)
        if len(pieces) == 2 and pieces[1] in _IF_OPS:
            col, op_key = pieces
            op = _IF_OPS[op_key]
            if op == "IN":
                placeholders = ", ".join("?" * len(value))
                parts.append(f'"{col}" IN ({placeholders})')
                params.extend(value)
            else:
                parts.append(f'"{col}" {op} ?')
                params.append(value)
        else:
            parts.append(f'"{key}" = ?')
            params.append(value)
    return " IF " + " AND ".join(parts), params


def build_update(
    table: str,
    keyspace: str,
    set_data: dict[str, Any],
    where: list[tuple[str, str, Any]],
    ttl: int | None = None,
    if_conditions: dict[str, Any] | None = None,
    collection_ops: list[tuple[str, str, Any]] | None = None,
    if_exists: bool = False,
    timestamp: int | None = None,
) -> tuple[str, list[Any]]:
    # Build cache key from query shape (column names + ops, not values).
    set_cols = tuple(set_data.keys())
    col_ops_shape = tuple((col, op) for col, op, _v in collection_ops) if collection_ops else ()
    where_shape = _where_to_shape(where) if where else ()
    if_cond_cols = tuple(if_conditions.keys()) if if_conditions else ()
    cache_key = (
        table,
        keyspace,
        set_cols,
        col_ops_shape,
        where_shape,
        ttl,
        if_cond_cols,
        if_exists,
        timestamp,
    )

    # Extract params (always needed regardless of cache hit).
    params: list[Any] = list(set_data.values())
    if collection_ops:
        for _col, _op, value in collection_ops:
            if _op in ("put", "setindex"):
                k, v = value
                params.extend([k, v])
            else:
                params.append(value)
    _extract_where_params(where, params)
    if if_conditions and not if_exists:
        _, cond_params_pre = _parse_if_conditions(if_conditions)
        params.extend(cond_params_pre)

    cached_cql = _update_cql_cache.get(cache_key)
    if cached_cql is not None:
        return cached_cql, params

    set_parts = [f'"{k}" = ?' for k in set_data]

    if collection_ops:
        for col, op, _value in collection_ops:
            if op in ("add", "append", "update"):
                set_parts.append(f'"{col}" = "{col}" + ?')
            elif op == "prepend":
                set_parts.append(f'"{col}" = ? + "{col}"')
            elif op == "remove":
                set_parts.append(f'"{col}" = "{col}" - ?')
            elif op in ("put", "setindex"):
                set_parts.append(f'"{col}"[?] = ?')

    cql = f"UPDATE {qualified_name(keyspace, table)}"
    cql += _build_using_clause(ttl=ttl, timestamp=timestamp)
    cql += " SET " + ", ".join(set_parts)

    clause, _wp = build_where_clause(where)
    cql += " " + clause

    if if_exists:
        cql += " IF EXISTS"
    elif if_conditions:
        cond_clause, _ = _parse_if_conditions(if_conditions)
        cql += cond_clause

    _update_cql_cache[cache_key] = cql
    return cql, params


# Cache for DELETE CQL templates keyed by query shape.
_delete_cql_cache: dict[tuple, str] = {}


def build_delete(
    table: str,
    keyspace: str,
    where: list[tuple[str, str, Any]],
    columns: list[str] | None = None,
    if_exists: bool = False,
    timestamp: int | None = None,
    if_conditions: dict[str, Any] | None = None,
    collection_elements: list[tuple[str, Any]] | None = None,
) -> tuple[str, list[Any]]:
    where_shape = _where_to_shape(where) if where else ()
    col_elem_shape = tuple((col, type(k).__name__) for col, k in collection_elements) if collection_elements else ()
    cache_key = (
        table,
        keyspace,
        tuple(columns) if columns else None,
        where_shape,
        col_elem_shape,
        if_exists,
        tuple(if_conditions.keys()) if if_conditions else (),
        timestamp,
    )

    params: list[Any] = []
    delete_parts: list[str] = []

    if columns:
        delete_parts.extend(f'"{c}"' for c in columns)
    if collection_elements:
        for col, key_or_idx in collection_elements:
            delete_parts.append(f'"{col}"[?]')
            params.append(key_or_idx)

    cached_cql = _delete_cql_cache.get(cache_key)
    if cached_cql is not None:
        _extract_where_params(where, params)
        if if_conditions and not if_exists:
            params.extend(if_conditions.values())
        return cached_cql, params

    cols_str = ", ".join(delete_parts) if delete_parts else ""
    cql = f"DELETE {cols_str} FROM {qualified_name(keyspace, table)}".replace("DELETE  FROM", "DELETE FROM")
    cql += _build_using_clause(timestamp=timestamp)

    clause, where_params = build_where_clause(where)
    cql += " " + clause
    params.extend(where_params)

    if if_exists:
        cql += " IF EXISTS"
    elif if_conditions:
        cond_clause, cond_params = _parse_if_conditions(if_conditions)
        cql += cond_clause
        params.extend(cond_params)

    _delete_cql_cache[cache_key] = cql
    return cql, params


def build_counter_update(
    table: str,
    keyspace: str,
    deltas: dict[str, int],
    where: list[tuple[str, str, Any]],
) -> tuple[str, list[Any]]:
    """Build an UPDATE statement for counter columns."""
    set_parts = [f'"{k}" = "{k}" + ?' for k in deltas]
    params: list[Any] = list(deltas.values())

    cql = f"UPDATE {qualified_name(keyspace, table)} SET " + ", ".join(set_parts)

    clause, where_params = build_where_clause(where)
    cql += " " + clause
    params.extend(where_params)

    return cql, params


def build_create_type(
    type_name: str,
    keyspace: str,
    fields: list[tuple[str, str]],
) -> str:
    """Build a ``CREATE TYPE IF NOT EXISTS`` CQL statement."""
    field_defs = ", ".join(f'"{name}" {cql_type}' for name, cql_type in fields)
    return f"CREATE TYPE IF NOT EXISTS {qualified_name(keyspace, type_name)} ({field_defs})"


def build_drop_type(type_name: str, keyspace: str) -> str:
    return f"DROP TYPE IF EXISTS {qualified_name(keyspace, type_name)}"


def build_alter_type_add(
    type_name: str,
    keyspace: str,
    field_name: str,
    cql_type: str,
) -> str:
    return f'ALTER TYPE {qualified_name(keyspace, type_name)} ADD "{field_name}" {cql_type}'


def build_batch(
    statements: list[tuple[str, list[Any]]],
    logged: bool = True,
    batch_type: str | None = None,
    timestamp: int | None = None,
) -> tuple[str, list[Any]]:
    if batch_type is not None:
        bt = batch_type.upper()
    else:
        bt = "" if logged else "UNLOGGED"
    all_params: list[Any] = []
    stmt_lines = []
    for stmt, p in statements:
        stmt_lines.append(stmt + ";")
        all_params.extend(p)
    inner = "\n  ".join(stmt_lines)
    prefix = f"BEGIN {bt} BATCH" if bt else "BEGIN BATCH"
    if timestamp is not None:
        prefix += f" USING TIMESTAMP {timestamp}"
    cql = f"{prefix}\n  {inner}\nAPPLY BATCH"
    return cql, all_params
