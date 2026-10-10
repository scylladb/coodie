from __future__ import annotations

import pytest

from coodie.cql_builder import (
    _insert_cql_cache,
    _select_cql_cache,
    build_batch,
    build_count,
    build_counter_update,
    build_create_index,
    build_create_keyspace,
    build_create_materialized_view,
    build_create_table,
    build_delete,
    build_drop_keyspace,
    build_drop_materialized_view,
    build_drop_table,
    build_insert,
    build_insert_from_columns,
    build_insert_json,
    build_select,
    build_select_column_ttl,
    build_select_json,
    build_select_writetime,
    build_update,
    build_where_clause,
    parse_filter_kwargs,
    parse_update_kwargs,
    quote_ident,
    schema_name,
)
from coodie.schema import ColumnDefinition


def make_col(**kwargs):  # type: ignore[no-untyped-def]
    defaults = {"name": "x", "cql_type": "text"}
    defaults.update(kwargs)
    return ColumnDefinition(**defaults)


def test_create_keyspace_default():
    cql = build_create_keyspace("ks")
    assert "CREATE KEYSPACE IF NOT EXISTS ks" in cql
    assert "SimpleStrategy" in cql
    assert "'replication_factor': '1'" in cql


def test_create_keyspace_custom():
    cql = build_create_keyspace("ks", replication_factor=3, strategy="NetworkTopologyStrategy")
    assert "NetworkTopologyStrategy" in cql
    assert "'replication_factor': '3'" in cql


def test_create_table_simple():
    cols = [
        make_col(name="id", cql_type="uuid", primary_key=True),
        make_col(name="name", cql_type="text"),
    ]
    cql = build_create_table("products", "ks", cols)
    assert "CREATE TABLE IF NOT EXISTS ks.products" in cql
    assert '"id" uuid' in cql
    assert '"name" text' in cql
    assert 'PRIMARY KEY ("id")' in cql


def test_create_table_composite_pk():
    cols = [
        make_col(name="product_id", cql_type="uuid", primary_key=True, partition_key_index=0),
        make_col(name="category", cql_type="text", primary_key=True, partition_key_index=1),
    ]
    cql = build_create_table("products", "ks", cols)
    assert 'PRIMARY KEY (("product_id", "category"))' in cql


def test_create_table_with_clustering():
    cols = [
        make_col(name="product_id", cql_type="uuid", primary_key=True),
        make_col(
            name="created_at",
            cql_type="timestamp",
            clustering_key=True,
            clustering_order="DESC",
        ),
    ]
    cql = build_create_table("reviews", "ks", cols)
    assert '"created_at"' in cql
    assert "WITH CLUSTERING ORDER BY" in cql


def test_create_table_no_pk_raises():
    cols = [make_col(name="name", cql_type="text")]
    with pytest.raises(ValueError):
        build_create_table("t", "ks", cols)


def test_create_table_with_static_column():
    cols = [
        make_col(name="sensor_id", cql_type="text", primary_key=True),
        make_col(name="reading_time", cql_type="text", clustering_key=True),
        make_col(name="sensor_name", cql_type="text", static=True),
        make_col(name="value", cql_type="float"),
    ]
    cql = build_create_table("sensor_readings", "ks", cols)
    assert '"sensor_name" text STATIC' in cql
    assert '"value" float' in cql
    # Non-static columns should not have STATIC keyword
    assert '"value" float STATIC' not in cql
    assert '"sensor_id" text STATIC' not in cql


def test_create_index():
    col = make_col(name="brand", cql_type="text", index=True)
    cql = build_create_index("products", "ks", col)
    assert "CREATE INDEX IF NOT EXISTS" in cql
    assert 'ON ks.products ("brand")' in cql


def test_drop_table():
    cql = build_drop_table("products", "ks")
    assert cql == "DROP TABLE IF EXISTS ks.products"


@pytest.mark.parametrize(
    "kwargs, expected_triple",
    [
        pytest.param({"name": "Alice"}, ("name", "=", "Alice"), id="eq"),
        pytest.param({"rating__gte": 4}, ("rating", ">=", 4), id="gte"),
        pytest.param({"price__lt": 100}, ("price", "<", 100), id="lt"),
        pytest.param({"id__in": [1, 2, 3]}, ("id", "IN", [1, 2, 3]), id="in"),
        pytest.param({"name__like": "Al%"}, ("name", "LIKE", "Al%"), id="like"),
        pytest.param({"status__ne": "deleted"}, ("status", "!=", "deleted"), id="ne"),
        pytest.param({"tags__contains": "x"}, ("tags", "CONTAINS", "x"), id="contains"),
        pytest.param({"meta__contains_key": "k"}, ("meta", "CONTAINS KEY", "k"), id="contains_key"),
    ],
)
def test_parse_filter_kwargs(kwargs, expected_triple):
    result = parse_filter_kwargs(kwargs)
    assert expected_triple in result


def test_build_where_clause_empty():
    clause, params = build_where_clause([])
    assert clause == ""
    assert params == []


def test_build_where_clause_eq():
    clause, params = build_where_clause([("name", "=", "Alice")])
    assert clause == 'WHERE "name" = ?'
    assert params == ["Alice"]


def test_build_where_clause_in():
    clause, params = build_where_clause([("id", "IN", [1, 2])])
    assert "IN (?, ?)" in clause
    assert params == [1, 2]


def test_build_select_simple():
    cql, params = build_select("products", "ks")
    assert cql == "SELECT * FROM ks.products"
    assert params == []


def test_build_select_with_where():
    cql, params = build_select("products", "ks", where=[("name", "=", "Alice")])
    assert 'WHERE "name" = ?' in cql
    assert params == ["Alice"]


def test_build_select_with_limit():
    cql, _params = build_select("products", "ks", limit=10)
    assert "LIMIT 10" in cql


def test_build_select_order_by_desc():
    cql, _ = build_select("products", "ks", order_by=["-created_at"])
    assert '"created_at" DESC' in cql


def test_build_select_allow_filtering():
    cql, _ = build_select("products", "ks", allow_filtering=True)
    assert "ALLOW FILTERING" in cql


def test_build_select_per_partition_limit():
    cql, _ = build_select("products", "ks", per_partition_limit=5)
    assert "PER PARTITION LIMIT 5" in cql


def test_build_select_with_columns():
    cql, _ = build_select("products", "ks", columns=["id", "name"])
    assert 'SELECT "id", "name" FROM ks.products' == cql


def test_build_select_like_filter():
    cql, params = build_select("products", "ks", where=[("name", "LIKE", "Al%")])
    assert '"name" LIKE ?' in cql
    assert params == ["Al%"]


def test_build_count():
    cql, params = build_count("products", "ks")
    assert "SELECT COUNT(*)" in cql
    assert params == []


def test_build_insert():
    cql, params = build_insert("products", "ks", {"id": "1", "name": "X"})
    assert "INSERT INTO ks.products" in cql
    assert "VALUES (?, ?)" in cql
    assert params == ["1", "X"]


def test_build_insert_if_not_exists():
    cql, _ = build_insert("products", "ks", {"id": "1"}, if_not_exists=True)
    assert "IF NOT EXISTS" in cql


# -- build_insert_from_columns (Phase 3: Task 3.6 + 3.8) ---------------------


def test_build_insert_from_columns():
    cols = ("id", "name")
    vals = ["1", "X"]
    cql, params = build_insert_from_columns("products", "ks", cols, vals)
    assert "INSERT INTO ks.products" in cql
    assert "VALUES (?, ?)" in cql
    assert params == ["1", "X"]


def test_build_insert_from_columns_if_not_exists():
    cols = ("id",)
    vals = ["1"]
    cql, _ = build_insert_from_columns("products", "ks", cols, vals, if_not_exists=True)
    assert "IF NOT EXISTS" in cql


def test_build_insert_from_columns_with_ttl():
    cols = ("id",)
    vals = ["1"]
    cql, _ = build_insert_from_columns("products", "ks", cols, vals, ttl=60)
    assert "USING TTL 60" in cql


def test_build_insert_from_columns_caching():
    """Second call with same shape returns identical CQL (cache hit)."""
    _insert_cql_cache.clear()
    cols = ("id", "name")
    cql1, _ = build_insert_from_columns("products", "ks", cols, ["1", "A"])
    cql2, _ = build_insert_from_columns("products", "ks", cols, ["2", "B"])
    # Both produce the same CQL template (values differ, CQL doesn't)
    assert cql1 == cql2
    assert len(_insert_cql_cache) == 1


def test_build_insert_from_columns_cache_separate_for_if_not_exists():
    """save() and insert() (IF NOT EXISTS) produce distinct cache entries."""
    _insert_cql_cache.clear()
    cols = ("id",)
    cql_save, _ = build_insert_from_columns("t", "ks", cols, ["1"])
    cql_ins, _ = build_insert_from_columns("t", "ks", cols, ["1"], if_not_exists=True)
    assert cql_save != cql_ins
    assert len(_insert_cql_cache) == 2


# -- build_select CQL caching (Phase 3: Task 3.8) ----------------------------


def test_build_select_cql_caching():
    """Repeated build_select with same shape returns cached CQL."""
    _select_cql_cache.clear()
    cql1, p1 = build_select("t", "ks", where=[("id", "=", "a")])
    cql2, p2 = build_select("t", "ks", where=[("id", "=", "b")])
    assert cql1 == cql2
    assert p1 == ["a"]
    assert p2 == ["b"]
    assert len(_select_cql_cache) == 1


def test_build_select_cache_varies_by_shape():
    """Different WHERE shapes produce distinct cache entries."""
    _select_cql_cache.clear()
    cql1, _ = build_select("t", "ks", where=[("id", "=", "a")])
    cql2, _ = build_select("t", "ks", where=[("id", "=", "a"), ("name", "=", "b")])
    assert cql1 != cql2
    assert len(_select_cql_cache) == 2


def test_build_select_cache_varies_by_in_length():
    """IN clause with different value counts produces distinct CQL."""
    _select_cql_cache.clear()
    cql1, p1 = build_select("t", "ks", where=[("id", "IN", [1, 2])])
    cql2, p2 = build_select("t", "ks", where=[("id", "IN", [1, 2, 3])])
    assert "IN (?, ?)" in cql1
    assert "IN (?, ?, ?)" in cql2
    assert p1 == [1, 2]
    assert p2 == [1, 2, 3]


@pytest.mark.parametrize(
    "builder, extra_kwargs, expected_fragment",
    [
        pytest.param("insert", {"ttl": 60}, "USING TTL 60", id="insert-ttl"),
        pytest.param(
            "insert",
            {"timestamp": 1234567890},
            "USING TIMESTAMP 1234567890",
            id="insert-ts",
        ),
        pytest.param(
            "insert",
            {"ttl": 60, "timestamp": 1234567890},
            "USING TTL 60 AND TIMESTAMP 1234567890",
            id="insert-ttl-ts",
        ),
        pytest.param("update", {"ttl": 300}, "USING TTL 300", id="update-ttl"),
        pytest.param(
            "update",
            {"timestamp": 1234567890},
            "USING TIMESTAMP 1234567890",
            id="update-ts",
        ),
        pytest.param(
            "update",
            {"ttl": 60, "timestamp": 1234567890},
            "USING TTL 60 AND TIMESTAMP 1234567890",
            id="update-ttl-ts",
        ),
        pytest.param(
            "delete",
            {"timestamp": 1234567890},
            "USING TIMESTAMP 1234567890",
            id="delete-ts",
        ),
    ],
)
def test_using_clause(builder, extra_kwargs, expected_fragment):
    if builder == "insert":
        cql, _ = build_insert("products", "ks", {"id": "1"}, **extra_kwargs)
    elif builder == "update":
        cql, _ = build_update(
            "products",
            "ks",
            set_data={"name": "Y"},
            where=[("id", "=", "1")],
            **extra_kwargs,
        )
    else:
        cql, _ = build_delete("products", "ks", [("id", "=", "1")], **extra_kwargs)
    assert expected_fragment in cql


def test_build_update():
    cql, params = build_update(
        "products",
        "ks",
        set_data={"name": "Y"},
        where=[("id", "=", "1")],
    )
    assert "UPDATE ks.products" in cql
    assert 'SET "name" = ?' in cql
    assert 'WHERE "id" = ?' in cql
    assert params == ["Y", "1"]


def test_build_update_with_if_exists():
    cql, params = build_update(
        "products",
        "ks",
        set_data={"name": "Y"},
        where=[("id", "=", "1")],
        if_exists=True,
    )
    assert "IF EXISTS" in cql
    assert params == ["Y", "1"]


def test_build_update_if_exists_takes_precedence_over_if_conditions():
    cql, params = build_update(
        "products",
        "ks",
        set_data={"name": "Y"},
        where=[("id", "=", "1")],
        if_conditions={"name": "X"},
        if_exists=True,
    )
    assert "IF EXISTS" in cql
    assert 'IF "name"' not in cql
    assert params == ["Y", "1"]


def test_build_delete():
    cql, params = build_delete("products", "ks", [("id", "=", "1")])
    assert "DELETE FROM ks.products" in cql
    assert params == ["1"]


def test_build_delete_if_exists():
    cql, params = build_delete("products", "ks", [("id", "=", "1")], if_exists=True)
    assert "DELETE FROM ks.products" in cql
    assert "IF EXISTS" in cql
    assert params == ["1"]


def test_build_batch():
    stmts = [
        ("INSERT INTO ks.t (id) VALUES (?)", ["1"]),
        ("INSERT INTO ks.t (id) VALUES (?)", ["2"]),
    ]
    cql, params = build_batch(stmts)
    assert "BEGIN BATCH" in cql
    assert "APPLY BATCH" in cql
    assert params == ["1", "2"]


def test_build_counter_update_single():
    cql, params = build_counter_update(
        "page_views",
        "ks",
        deltas={"view_count": 1},
        where=[("url", "=", "/home")],
    )
    assert "UPDATE ks.page_views" in cql
    assert '"view_count" = "view_count" + ?' in cql
    assert 'WHERE "url" = ?' in cql
    assert params == [1, "/home"]


def test_build_counter_update_multiple():
    cql, params = build_counter_update(
        "page_views",
        "ks",
        deltas={"view_count": 5, "unique_visitors": 1},
        where=[("url", "=", "/home")],
    )
    assert '"view_count" = "view_count" + ?' in cql
    assert '"unique_visitors" = "unique_visitors" + ?' in cql
    assert params == [5, 1, "/home"]


def test_build_counter_update_decrement():
    cql, params = build_counter_update(
        "page_views",
        "ks",
        deltas={"view_count": -1},
        where=[("url", "=", "/home")],
    )
    assert '"view_count" = "view_count" + ?' in cql
    assert params == [-1, "/home"]


# --- Phase 3: Partial Update API ---


def test_parse_update_kwargs_regular():
    set_data, ops = parse_update_kwargs({"name": "Y", "price": 10})
    assert set_data == {"name": "Y", "price": 10}
    assert ops == []


def test_parse_update_kwargs_collection_ops():
    set_data, ops = parse_update_kwargs({"tags__add": {"new"}, "items__remove": ["old"], "name": "X"})
    assert set_data == {"name": "X"}
    assert ("tags", "add", {"new"}) in ops
    assert ("items", "remove", ["old"]) in ops


def test_parse_update_kwargs_append_prepend():
    set_data, ops = parse_update_kwargs({"items__append": ["z"], "items__prepend": ["a"]})
    assert set_data == {}
    assert ("items", "append", ["z"]) in ops
    assert ("items", "prepend", ["a"]) in ops


def test_parse_update_kwargs_map_update():
    set_data, ops = parse_update_kwargs({"meta__update": {"k": "v"}})
    assert set_data == {}
    assert ("meta", "update", {"k": "v"}) in ops


def test_build_update_map_update():
    cql, params = build_update(
        "products",
        "ks",
        set_data={},
        where=[("id", "=", "1")],
        collection_ops=[("meta", "update", {"k": "v"})],
    )
    assert '"meta" = "meta" + ?' in cql
    assert params == [{"k": "v"}, "1"]


def test_build_update_map_remove():
    cql, params = build_update(
        "products",
        "ks",
        set_data={},
        where=[("id", "=", "1")],
        collection_ops=[("meta", "remove", {"k"})],
    )
    assert '"meta" = "meta" - ?' in cql
    assert params == [{"k"}, "1"]


def test_build_update_list_remove():
    cql, params = build_update(
        "products",
        "ks",
        set_data={},
        where=[("id", "=", "1")],
        collection_ops=[("items", "remove", ["old"])],
    )
    assert '"items" = "items" - ?' in cql
    assert params == [["old"], "1"]


def test_build_update_with_if_conditions():
    cql, params = build_update(
        "products",
        "ks",
        set_data={"name": "Y"},
        where=[("id", "=", "1")],
        if_conditions={"name": "X"},
    )
    assert 'IF "name" = ?' in cql
    assert params == ["Y", "1", "X"]


@pytest.mark.parametrize(
    "op_key, op_name, value, expected_fragment, expected_params",
    [
        pytest.param(
            "tags",
            "add",
            {"new_tag"},
            '"tags" = "tags" + ?',
            [{"new_tag"}, "1"],
            id="set-add",
        ),
        pytest.param(
            "tags",
            "remove",
            {"old_tag"},
            '"tags" = "tags" - ?',
            [{"old_tag"}, "1"],
            id="set-remove",
        ),
        pytest.param(
            "items",
            "append",
            ["z"],
            '"items" = "items" + ?',
            [["z"], "1"],
            id="list-append",
        ),
        pytest.param(
            "items",
            "prepend",
            ["a"],
            '"items" = ? + "items"',
            [["a"], "1"],
            id="list-prepend",
        ),
    ],
)
def test_build_update_collection_op(op_key, op_name, value, expected_fragment, expected_params):
    cql, params = build_update(
        "products",
        "ks",
        set_data={},
        where=[("id", "=", "1")],
        collection_ops=[(op_key, op_name, value)],
    )
    assert expected_fragment in cql
    assert params == expected_params


def test_build_update_mixed_set_and_collection_ops():
    cql, params = build_update(
        "products",
        "ks",
        set_data={"name": "Y"},
        where=[("id", "=", "1")],
        collection_ops=[("tags", "add", {"new"})],
    )
    assert '"name" = ?' in cql
    assert '"tags" = "tags" + ?' in cql
    assert params == ["Y", {"new"}, "1"]


# ------------------------------------------------------------------
# Phase 8: build_create_table with table_options
# ------------------------------------------------------------------


def test_create_table_with_default_ttl():
    cols = [
        make_col(name="id", cql_type="uuid", primary_key=True),
        make_col(name="name", cql_type="text"),
    ]
    cql = build_create_table("products", "ks", cols, table_options={"default_time_to_live": 86400})
    assert "WITH default_time_to_live = 86400" in cql


def test_create_table_with_multiple_options():
    cols = [
        make_col(name="id", cql_type="uuid", primary_key=True),
    ]
    cql = build_create_table(
        "products",
        "ks",
        cols,
        table_options={"default_time_to_live": 3600, "gc_grace_seconds": 864000},
    )
    assert "default_time_to_live = 3600" in cql
    assert "gc_grace_seconds = 864000" in cql
    assert " AND " in cql


def test_create_table_with_string_option():
    cols = [
        make_col(name="id", cql_type="uuid", primary_key=True),
    ]
    cql = build_create_table("products", "ks", cols, table_options={"comment": "my table"})
    assert "comment = 'my table'" in cql


def test_create_table_with_clustering_and_options():
    cols = [
        make_col(name="id", cql_type="uuid", primary_key=True),
        make_col(
            name="created_at",
            cql_type="timestamp",
            clustering_key=True,
            clustering_order="DESC",
        ),
    ]
    cql = build_create_table("reviews", "ks", cols, table_options={"default_time_to_live": 3600})
    assert "WITH CLUSTERING ORDER BY" in cql
    assert "default_time_to_live = 3600" in cql
    assert " AND " in cql


def test_create_table_no_options():
    cols = [
        make_col(name="id", cql_type="uuid", primary_key=True),
    ]
    cql = build_create_table("products", "ks", cols, table_options=None)
    assert "default_time_to_live" not in cql
    assert "gc_grace_seconds" not in cql


# ------------------------------------------------------------------
# Phase 10: Token-range query support
# ------------------------------------------------------------------


@pytest.mark.parametrize(
    "kwargs, expected_triple",
    [
        pytest.param({"id__token__gt": 100}, ("id", "TOKEN >", 100), id="token-gt"),
        pytest.param({"id__token__gte": 100}, ("id", "TOKEN >=", 100), id="token-gte"),
        pytest.param({"id__token__lt": 200}, ("id", "TOKEN <", 200), id="token-lt"),
        pytest.param({"id__token__lte": 200}, ("id", "TOKEN <=", 200), id="token-lte"),
    ],
)
def test_parse_filter_kwargs_token(kwargs, expected_triple):
    result = parse_filter_kwargs(kwargs)
    assert result == [expected_triple]


def test_parse_filter_kwargs_token_range():
    result = parse_filter_kwargs({"id__token__gt": 100, "id__token__lte": 200})
    assert ("id", "TOKEN >", 100) in result
    assert ("id", "TOKEN <=", 200) in result


def test_build_where_clause_token():
    clause, params = build_where_clause([("id", "TOKEN >", 100)])
    assert clause == 'WHERE TOKEN("id") > ?'
    assert params == [100]


def test_build_where_clause_token_range():
    clause, params = build_where_clause([("id", "TOKEN >", 100), ("id", "TOKEN <=", 200)])
    assert 'TOKEN("id") > ?' in clause
    assert 'TOKEN("id") <= ?' in clause
    assert params == [100, 200]


def test_build_select_with_token_filter():
    cql, params = build_select(
        "products",
        "ks",
        where=[("id", "TOKEN >", 100), ("id", "TOKEN <=", 200)],
        allow_filtering=True,
    )
    assert 'TOKEN("id") > ?' in cql
    assert 'TOKEN("id") <= ?' in cql
    assert params == [100, 200]
    assert "ALLOW FILTERING" in cql


def test_parse_filter_kwargs_mixed_token_and_regular():
    result = parse_filter_kwargs({"id__token__gt": 100, "name": "Alice"})
    assert ("id", "TOKEN >", 100) in result
    assert ("name", "=", "Alice") in result


# ------------------------------------------------------------------
# Phase 12: Materialized Views
# ------------------------------------------------------------------


def test_build_create_materialized_view_simple():
    cql = build_create_materialized_view(
        view_name="products_by_brand",
        keyspace="ks",
        base_table="products",
        columns=["*"],
        primary_key_columns=["brand"],
        clustering_columns=["id"],
        where_clause='"brand" IS NOT NULL AND "id" IS NOT NULL',
    )
    assert "CREATE MATERIALIZED VIEW IF NOT EXISTS ks.products_by_brand" in cql
    assert "AS SELECT * FROM ks.products" in cql
    assert '"brand" IS NOT NULL AND "id" IS NOT NULL' in cql
    assert 'PRIMARY KEY ("brand", "id")' in cql


def test_build_create_materialized_view_specific_columns():
    cql = build_create_materialized_view(
        view_name="products_by_brand",
        keyspace="ks",
        base_table="products",
        columns=["id", "name", "brand"],
        primary_key_columns=["brand"],
        clustering_columns=["id"],
        where_clause='"brand" IS NOT NULL AND "id" IS NOT NULL',
    )
    assert 'SELECT "id", "name", "brand" FROM ks.products' in cql


def test_build_create_materialized_view_composite_pk():
    cql = build_create_materialized_view(
        view_name="mv_test",
        keyspace="ks",
        base_table="base",
        columns=["*"],
        primary_key_columns=["a", "b"],
        where_clause='"a" IS NOT NULL AND "b" IS NOT NULL',
    )
    assert 'PRIMARY KEY (("a", "b"))' in cql


def test_build_create_materialized_view_no_clustering():
    cql = build_create_materialized_view(
        view_name="mv_test",
        keyspace="ks",
        base_table="base",
        columns=["*"],
        primary_key_columns=["id"],
        where_clause='"id" IS NOT NULL',
    )
    assert 'PRIMARY KEY ("id")' in cql


def test_build_create_materialized_view_with_clustering_order():
    cql = build_create_materialized_view(
        view_name="products_by_brand",
        keyspace="ks",
        base_table="products",
        columns=["*"],
        primary_key_columns=["brand"],
        clustering_columns=["created_at"],
        where_clause='"brand" IS NOT NULL AND "created_at" IS NOT NULL',
        clustering_order={"created_at": "DESC"},
    )
    assert "WITH CLUSTERING ORDER BY" in cql
    assert '"created_at" DESC' in cql


def test_build_drop_materialized_view():
    cql = build_drop_materialized_view("products_by_brand", "ks")
    assert cql == "DROP MATERIALIZED VIEW IF EXISTS ks.products_by_brand"


# ------------------------------------------------------------------
# Phase 13: Keyspace Management
# ------------------------------------------------------------------


def test_build_create_keyspace_network_topology():
    cql = build_create_keyspace("ks", dc_replication_map={"dc1": 3, "dc2": 2})
    assert "CREATE KEYSPACE IF NOT EXISTS ks" in cql
    assert "NetworkTopologyStrategy" in cql
    assert "'dc1': '3'" in cql
    assert "'dc2': '2'" in cql


def test_build_create_keyspace_network_topology_single_dc():
    cql = build_create_keyspace("ks", dc_replication_map={"us-east": 3})
    assert "NetworkTopologyStrategy" in cql
    assert "'us-east': '3'" in cql


def test_build_create_keyspace_network_topology_overrides_strategy():
    cql = build_create_keyspace("ks", strategy="SimpleStrategy", dc_replication_map={"dc1": 3})
    assert "NetworkTopologyStrategy" in cql
    assert "SimpleStrategy" not in cql


def test_build_drop_keyspace():
    cql = build_drop_keyspace("my_ks")
    assert cql == "DROP KEYSPACE IF EXISTS my_ks"


# ------------------------------------------------------------------
# Phase A: Migration Strategy — Enhanced sync_table helpers
# ------------------------------------------------------------------


@pytest.mark.parametrize(
    "stored, expected",
    [
        ("users_email_idx", "ks.users_email_idx"),
        ("ByEmail", 'ks."ByEmail"'),
        ("By-Email", 'ks."By-Email"'),
        ("order", 'ks."order"'),
    ],
)
def test_build_drop_index(stored, expected):
    from coodie.cql_builder import build_drop_index

    assert build_drop_index(stored, "ks") == f"DROP INDEX IF EXISTS {expected}"


def test_build_alter_table_options_single():
    from coodie.cql_builder import build_alter_table_options

    cql = build_alter_table_options("products", "ks", {"default_time_to_live": 3600})
    assert cql == "ALTER TABLE ks.products WITH default_time_to_live = 3600"


def test_build_alter_table_options_multiple():
    from coodie.cql_builder import build_alter_table_options

    cql = build_alter_table_options("products", "ks", {"default_time_to_live": 3600, "gc_grace_seconds": 864000})
    assert "ALTER TABLE ks.products WITH" in cql
    assert "default_time_to_live = 3600" in cql
    assert "gc_grace_seconds = 864000" in cql
    assert " AND " in cql


def test_build_alter_table_options_string_value():
    from coodie.cql_builder import build_alter_table_options

    cql = build_alter_table_options("products", "ks", {"comment": "my table"})
    assert cql == "ALTER TABLE ks.products WITH comment = 'my table'"


# -- Phase 1: build_truncate -------------------------------------------------


def test_build_truncate():
    from coodie.cql_builder import build_truncate

    cql = build_truncate("products", "ks")
    assert cql == "TRUNCATE TABLE ks.products"


# ---- build_create_custom_index tests ----


def test_build_create_custom_index_basic():
    from coodie.cql_builder import build_create_custom_index

    col = make_col(name="embedding", cql_type="vector<float, 5>", vector_index=True)
    cql = build_create_custom_index("products", "ks", col)
    assert "CREATE CUSTOM INDEX IF NOT EXISTS products_embedding_idx" in cql
    assert 'ON ks.products ("embedding")' in cql
    assert "USING 'org.apache.cassandra.index.sai.StorageAttachedIndex'" in cql


def test_build_create_custom_index_with_options():
    from coodie.cql_builder import build_create_custom_index

    col = make_col(
        name="embedding",
        cql_type="vector<float, 5>",
        vector_index=True,
        vector_index_name="my_ann_idx",
    )
    cql = build_create_custom_index(
        "products",
        "ks",
        col,
        options={"similarity_function": "cosine"},
    )
    assert "CREATE CUSTOM INDEX IF NOT EXISTS my_ann_idx" in cql
    assert 'ON ks.products ("embedding")' in cql
    assert "WITH OPTIONS = {'similarity_function': 'cosine'}" in cql


def test_build_create_custom_index_custom_class():
    from coodie.cql_builder import build_create_custom_index

    col = make_col(name="text_col", cql_type="text", vector_index=True)
    cql = build_create_custom_index(
        "docs",
        "ks",
        col,
        index_class="com.example.CustomIndex",
    )
    assert "USING 'com.example.CustomIndex'" in cql


# ---- build_select with ann_of tests ----


def test_build_select_ann_of():
    cql, params = build_select(
        "products",
        "ks",
        ann_of=("embedding", [0.1, 0.2, 0.3]),
        limit=5,
    )
    assert 'ORDER BY "embedding" ANN OF ?' in cql
    assert "LIMIT 5" in cql
    assert [0.1, 0.2, 0.3] in params


def test_build_select_ann_of_with_where():
    cql, params = build_select(
        "products",
        "ks",
        where=[("category", "=", "electronics")],
        ann_of=("embedding", [0.1, 0.2]),
        limit=10,
    )
    assert 'WHERE "category" = ?' in cql
    assert 'ORDER BY "embedding" ANN OF ?' in cql
    assert params == ["electronics", [0.1, 0.2]]


def test_build_select_ann_overrides_order_by():
    """When ann_of is provided, regular order_by should be ignored."""
    cql, _params = build_select(
        "products",
        "ks",
        order_by=["name"],
        ann_of=("embedding", [0.5, 0.5]),
    )
    assert 'ORDER BY "embedding" ANN OF ?' in cql
    assert '"name" ASC' not in cql


# ---- build_create_table with vector column ----


def test_create_table_with_vector_column():
    cols = [
        make_col(name="id", cql_type="uuid", primary_key=True),
        make_col(name="embedding", cql_type="vector<float, 5>"),
    ]
    cql = build_create_table("products", "ks", cols)
    assert '"embedding" vector<float, 5>' in cql


# ---- build_create_table with duration column ----


def test_create_table_with_duration_column():
    cols = [
        make_col(name="id", cql_type="uuid", primary_key=True),
        make_col(name="ttl_duration", cql_type="duration"),
    ]
    cql = build_create_table("events", "ks", cols)
    assert '"ttl_duration" duration' in cql


# ---- build_insert_json (Phase 5) ----


def test_build_insert_json_basic():
    cql, params = build_insert_json("users", "ks", '{"id": "1", "name": "Alice"}')
    assert cql == "INSERT INTO ks.users JSON ?"
    assert params == ['{"id": "1", "name": "Alice"}']


def test_build_insert_json_if_not_exists():
    cql, _ = build_insert_json("users", "ks", "{}", if_not_exists=True)
    assert "IF NOT EXISTS" in cql


def test_build_insert_json_with_ttl():
    cql, _ = build_insert_json("users", "ks", "{}", ttl=300)
    assert "USING TTL 300" in cql


def test_build_insert_json_with_timestamp():
    cql, _ = build_insert_json("users", "ks", "{}", timestamp=1234567890)
    assert "USING TIMESTAMP 1234567890" in cql


# ---- build_select_json (Phase 5) ----


def test_build_select_json_basic():
    cql, params = build_select_json("users", "ks")
    assert cql == "SELECT JSON * FROM ks.users"
    assert params == []


def test_build_select_json_with_where():
    where = [("id", "=", "1")]
    cql, params = build_select_json("users", "ks", where=where)
    assert "SELECT JSON * FROM ks.users" in cql
    assert 'WHERE "id" = ?' in cql
    assert params == ["1"]


def test_build_select_json_with_limit():
    cql, _ = build_select_json("users", "ks", limit=10)
    assert "LIMIT 10" in cql


def test_build_select_json_allow_filtering():
    cql, _ = build_select_json("users", "ks", allow_filtering=True)
    assert "ALLOW FILTERING" in cql


# ---- build_select_writetime (Phase 5) ----


def test_build_select_writetime_basic():
    cql, params = build_select_writetime("users", "ks", "name")
    assert cql == 'SELECT WRITETIME("name") FROM ks.users'
    assert params == []


def test_build_select_writetime_with_where():
    where = [("id", "=", "1")]
    cql, params = build_select_writetime("users", "ks", "name", where=where)
    assert 'SELECT WRITETIME("name") FROM ks.users' in cql
    assert 'WHERE "id" = ?' in cql
    assert params == ["1"]


def test_build_select_writetime_allow_filtering():
    cql, _ = build_select_writetime("users", "ks", "name", allow_filtering=True)
    assert "ALLOW FILTERING" in cql


# ---- build_select_column_ttl (Phase 5) ----


def test_build_select_column_ttl_basic():
    cql, params = build_select_column_ttl("users", "ks", "name")
    assert cql == 'SELECT TTL("name") FROM ks.users'
    assert params == []


def test_build_select_column_ttl_with_where():
    where = [("id", "=", "1")]
    cql, params = build_select_column_ttl("users", "ks", "name", where=where)
    assert 'SELECT TTL("name") FROM ks.users' in cql
    assert 'WHERE "id" = ?' in cql
    assert params == ["1"]


def test_build_select_column_ttl_allow_filtering():
    cql, _ = build_select_column_ttl("users", "ks", "name", allow_filtering=True)
    assert "ALLOW FILTERING" in cql


# ---- identifier quoting (#298) ----


@pytest.mark.parametrize(
    ("name", "quoted", "stored"),
    [
        ("users", "users", "users"),
        ("MyTable", "MyTable", "mytable"),
        ('"MyTable"', '"MyTable"', "MyTable"),
        ("order", '"order"', "order"),
        ("Order", '"order"', "order"),
        ("my-table", '"my-table"', "my-table"),
        ('"a""b"', '"a""b"', 'a"b'),
    ],
)
def test_quote_ident_and_schema_name(name, quoted, stored):
    assert quote_ident(name) == quoted
    assert schema_name(name) == stored
    assert schema_name(quoted) == stored


def test_identifier_quoting_in_generated_cql():
    cols = [make_col(name="id", cql_type="uuid", primary_key=True)]
    assert build_create_table("order", "ks", cols).startswith('CREATE TABLE IF NOT EXISTS ks."order" (')
    assert build_create_table('"MyTable"', "ks", cols).startswith('CREATE TABLE IF NOT EXISTS ks."MyTable" (')
    cql, _ = build_select("order", "select", where=[("id", "=", 1)])
    assert cql.startswith('SELECT * FROM "select"."order" WHERE')
    idx = make_col(name="email", cql_type="text", index=True)
    assert (
        build_create_index('"MyTable"', "ks", idx)
        == 'CREATE INDEX IF NOT EXISTS MyTable_email_idx ON ks."MyTable" ("email")'
    )
