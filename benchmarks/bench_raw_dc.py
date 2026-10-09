"""Raw+DC benchmarks — dataclasses + raw CQL vs coodie vs cqlengine.

Implements the "Raw+DC" pattern: plain Python dataclasses hydrated from raw
CQL queries executed via the cassandra-driver session.  This establishes the
performance floor — the fastest pure-Python path without ORM overhead.

See: https://mkennedy.codes/posts/raw-dc-the-orm-pattern-of-2026/
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from benchmarks.models_raw_dc import RawEvent, RawProduct

# ---------------------------------------------------------------------------
# Helpers — lazily cached prepared statements
# ---------------------------------------------------------------------------

_PREPARED: dict = {}
_PREPARED_READY = False


def _ensure_prepared(cql_session):
    """Lazily cache prepared statements (idempotent)."""
    global _PREPARED_READY
    if _PREPARED_READY:
        return
    _PREPARED.update(
        {
            "insert_product": cql_session.prepare(
                "INSERT INTO bench_ks.bench_products "
                "(id, name, brand, category, price, tags, description) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)"
            ),
            "insert_product_if_not_exists": cql_session.prepare(
                "INSERT INTO bench_ks.bench_products "
                "(id, name, brand, category, price, tags, description) "
                "VALUES (?, ?, ?, ?, ?, ?, ?) IF NOT EXISTS"
            ),
            "insert_product_ttl": cql_session.prepare(
                "INSERT INTO bench_ks.bench_products "
                "(id, name, brand, category, price, tags, description) "
                "VALUES (?, ?, ?, ?, ?, ?, ?) USING TTL ?"
            ),
            "select_product_by_pk": cql_session.prepare(
                "SELECT id, name, brand, category, price, tags, description FROM bench_ks.bench_products WHERE id = ?"
            ),
            "select_products_by_brand": cql_session.prepare(
                "SELECT id, name, brand, category, price, tags, description "
                "FROM bench_ks.bench_products WHERE brand = ?"
            ),
            "select_products_by_brand_limit": cql_session.prepare(
                "SELECT id, name, brand, category, price, tags, description "
                "FROM bench_ks.bench_products WHERE brand = ? LIMIT ?"
            ),
            "count_products_by_brand": cql_session.prepare(
                "SELECT COUNT(*) FROM bench_ks.bench_products WHERE brand = ?"
            ),
            "update_product_price": cql_session.prepare("UPDATE bench_ks.bench_products SET price = ? WHERE id = ?"),
            "update_product_price_if": cql_session.prepare(
                "UPDATE bench_ks.bench_products SET price = ? WHERE id = ? IF brand = ?"
            ),
            "delete_product": cql_session.prepare("DELETE FROM bench_ks.bench_products WHERE id = ?"),
            "insert_event": cql_session.prepare(
                "INSERT INTO bench_ks.bench_events (id, event_type, payload) VALUES (?, ?, ?)"
            ),
        }
    )
    _PREPARED_READY = True


def _row_to_product(row) -> RawProduct:
    """Hydrate a cassandra-driver row (dict) into a RawProduct dataclass.

    The shared ``cql_session`` uses ``dict_factory`` (set by coodie's
    CassandraDriver), so rows arrive as plain dicts.
    """
    return RawProduct(
        id=row["id"],
        name=row["name"],
        brand=row["brand"],
        category=row["category"],
        price=row["price"],
        tags=list(row["tags"]) if row["tags"] else [],
        description=row["description"],
    )


# ---------------------------------------------------------------------------
# Single INSERT
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="single-insert")
def test_raw_dc_single_insert(benchmark, bench_env, cql_session):
    _ensure_prepared(cql_session)
    stmt = _PREPARED["insert_product"]

    def _insert():
        p = RawProduct(id=uuid4(), name="BenchItem", brand="BenchBrand", price=9.99)
        cql_session.execute(stmt, (p.id, p.name, p.brand, p.category, p.price, p.tags, p.description))

    benchmark(_insert)


# ---------------------------------------------------------------------------
# INSERT IF NOT EXISTS
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="insert-if-not-exists")
def test_raw_dc_insert_if_not_exists(benchmark, bench_env, cql_session):
    _ensure_prepared(cql_session)
    stmt = _PREPARED["insert_product_if_not_exists"]

    def _insert():
        p = RawProduct(id=uuid4(), name="BenchINE", brand="BenchBrand", price=1.0)
        cql_session.execute(stmt, (p.id, p.name, p.brand, p.category, p.price, p.tags, p.description))

    benchmark(_insert)


# ---------------------------------------------------------------------------
# INSERT with TTL
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="insert-with-ttl")
def test_raw_dc_insert_with_ttl(benchmark, bench_env, cql_session):
    _ensure_prepared(cql_session)
    stmt = _PREPARED["insert_product_ttl"]

    def _insert():
        p = RawProduct(id=uuid4(), name="BenchTTL", brand="BenchBrand", price=2.0)
        cql_session.execute(stmt, (p.id, p.name, p.brand, p.category, p.price, p.tags, p.description, 60))

    benchmark(_insert)


# ---------------------------------------------------------------------------
# Seed data for read benchmarks
# ---------------------------------------------------------------------------

_SEEDED = False
_SEED_IDS: list = []


def _seed_read_data(cql_session):
    """Insert seed rows for Raw+DC read benchmarks (idempotent)."""
    global _SEEDED
    if _SEEDED:
        return
    _ensure_prepared(cql_session)
    stmt = _PREPARED["insert_product"]
    for i in range(100):
        pid = uuid4()
        _SEED_IDS.append(pid)
        cql_session.execute(
            stmt,
            (pid, f"ReadItem{i}", "ReadBrand", "read_bench", float(i), [], None),
        )
    _SEEDED = True


# ---------------------------------------------------------------------------
# GET by PK
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="get-by-pk")
def test_raw_dc_get_by_pk(benchmark, bench_env, cql_session):
    _seed_read_data(cql_session)
    _ensure_prepared(cql_session)
    stmt = _PREPARED["select_product_by_pk"]
    target_id = _SEED_IDS[0]

    def _get():
        rows = cql_session.execute(stmt, (target_id,))
        _row_to_product(rows.one())

    benchmark(_get)


# ---------------------------------------------------------------------------
# Filter (secondary index)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="filter-secondary-index")
def test_raw_dc_filter_secondary_index(benchmark, bench_env, cql_session):
    _seed_read_data(cql_session)
    _ensure_prepared(cql_session)
    stmt = _PREPARED["select_products_by_brand"]

    def _filter():
        rows = cql_session.execute(stmt, ("ReadBrand",))
        [_row_to_product(r) for r in rows]

    benchmark(_filter)


# ---------------------------------------------------------------------------
# Filter + LIMIT
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="filter-limit")
def test_raw_dc_filter_limit(benchmark, bench_env, cql_session):
    _seed_read_data(cql_session)
    _ensure_prepared(cql_session)
    stmt = _PREPARED["select_products_by_brand_limit"]

    def _filter():
        rows = cql_session.execute(stmt, ("ReadBrand", 10))
        [_row_to_product(r) for r in rows]

    benchmark(_filter)


# ---------------------------------------------------------------------------
# COUNT
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="count")
def test_raw_dc_count(benchmark, bench_env, cql_session):
    _seed_read_data(cql_session)
    _ensure_prepared(cql_session)
    stmt = _PREPARED["count_products_by_brand"]

    def _count():
        rows = cql_session.execute(stmt, ("ReadBrand",))
        rows.one()["count"]

    benchmark(_count)


# ---------------------------------------------------------------------------
# Partial UPDATE
# ---------------------------------------------------------------------------

_UPDATE_SETUP_DONE = False
_UPDATE_ID = None


def _ensure_update_row(cql_session):
    """Create a single row to update repeatedly."""
    global _UPDATE_SETUP_DONE, _UPDATE_ID
    if _UPDATE_SETUP_DONE:
        return
    _ensure_prepared(cql_session)
    _UPDATE_ID = uuid4()
    stmt = _PREPARED["insert_product"]
    cql_session.execute(stmt, (_UPDATE_ID, "UpdateTarget", "UpdateBrand", "general", 1.0, [], None))
    _UPDATE_SETUP_DONE = True


@pytest.mark.benchmark(group="partial-update")
def test_raw_dc_partial_update(benchmark, bench_env, cql_session):
    _ensure_update_row(cql_session)
    stmt = _PREPARED["update_product_price"]

    def _update():
        cql_session.execute(stmt, (42.0, _UPDATE_ID))

    benchmark(_update)


@pytest.mark.benchmark(group="partial-update-fair")
def test_raw_dc_partial_update_fair(benchmark, bench_env, cql_session):
    """Raw+DC baseline for fair partial-update (same as partial-update)."""
    _ensure_update_row(cql_session)
    stmt = _PREPARED["update_product_price"]

    def _update():
        cql_session.execute(stmt, (42.0, _UPDATE_ID))

    benchmark(_update)


# ---------------------------------------------------------------------------
# UPDATE with IF condition (LWT)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="update-if-condition")
def test_raw_dc_update_if_condition(benchmark, bench_env, cql_session):
    _ensure_update_row(cql_session)
    stmt = _PREPARED["update_product_price_if"]

    def _update():
        cql_session.execute(stmt, (99.0, _UPDATE_ID, "UpdateBrand"))

    benchmark(_update)


@pytest.mark.benchmark(group="update-if-condition-fair")
def test_raw_dc_update_if_condition_fair(benchmark, bench_env, cql_session):
    """Raw+DC baseline for fair LWT update (same as update-if-condition)."""
    _ensure_update_row(cql_session)
    stmt = _PREPARED["update_product_price_if"]

    def _update():
        cql_session.execute(stmt, (99.0, _UPDATE_ID, "UpdateBrand"))

    benchmark(_update)


# ---------------------------------------------------------------------------
# Single DELETE
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="single-delete")
def test_raw_dc_single_delete(benchmark, bench_env, cql_session):
    _ensure_prepared(cql_session)
    insert_stmt = _PREPARED["insert_product"]
    delete_stmt = _PREPARED["delete_product"]

    def _delete():
        pid = uuid4()
        cql_session.execute(insert_stmt, (pid, "DelTarget", "Unknown", "general", 0.0, [], None))
        cql_session.execute(delete_stmt, (pid,))

    benchmark(_delete)


# ---------------------------------------------------------------------------
# Bulk DELETE
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="bulk-delete")
def test_raw_dc_bulk_delete(benchmark, bench_env, cql_session):
    _ensure_prepared(cql_session)
    insert_stmt = _PREPARED["insert_product"]
    delete_stmt = _PREPARED["delete_product"]

    def _delete():
        pid = uuid4()
        cql_session.execute(insert_stmt, (pid, "BulkDel", "Unknown", "general", 0.0, [], None))
        cql_session.execute(delete_stmt, (pid,))

    benchmark(_delete)


# ---------------------------------------------------------------------------
# Batch INSERT (10 rows)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="batch-insert-10")
def test_raw_dc_batch_insert_10(benchmark, bench_env, cql_session):
    from cassandra.query import BatchStatement

    _ensure_prepared(cql_session)
    stmt = _PREPARED["insert_event"]

    def _batch():
        batch = BatchStatement()
        for _ in range(10):
            e = RawEvent(id=uuid4(), event_type="click", payload="data")
            batch.add(stmt, (e.id, e.event_type, e.payload))
        cql_session.execute(batch)

    benchmark(_batch)


# ---------------------------------------------------------------------------
# Batch INSERT (100 rows)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="batch-insert-100")
def test_raw_dc_batch_insert_100(benchmark, bench_env, cql_session):
    from cassandra.query import BatchStatement

    _ensure_prepared(cql_session)
    stmt = _PREPARED["insert_event"]

    def _batch():
        batch = BatchStatement()
        for _ in range(100):
            e = RawEvent(id=uuid4(), event_type="click", payload="data")
            batch.add(stmt, (e.id, e.event_type, e.payload))
        cql_session.execute(batch)

    benchmark(_batch)


# ---------------------------------------------------------------------------
# Collection field write (list[str])
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="collection-write")
def test_raw_dc_collection_write(benchmark, bench_env, cql_session):
    _ensure_prepared(cql_session)
    stmt = _PREPARED["insert_product"]
    tags = ["alpha", "beta", "gamma", "delta", "epsilon"]

    def _write():
        p = RawProduct(id=uuid4(), name="CollWrite", tags=tags)
        cql_session.execute(stmt, (p.id, p.name, p.brand, p.category, p.price, p.tags, p.description))

    benchmark(_write)


# ---------------------------------------------------------------------------
# Collection field read (list[str])
# ---------------------------------------------------------------------------

_COLL_READ_ID = None
_COLL_SEEDED = False


def _seed_collection_row(cql_session):
    global _COLL_READ_ID, _COLL_SEEDED
    if _COLL_SEEDED:
        return
    _ensure_prepared(cql_session)
    _COLL_READ_ID = uuid4()
    stmt = _PREPARED["insert_product"]
    cql_session.execute(
        stmt,
        (_COLL_READ_ID, "CollRead", "Unknown", "general", 0.0, ["alpha", "beta", "gamma", "delta", "epsilon"], None),
    )
    _COLL_SEEDED = True


@pytest.mark.benchmark(group="collection-read")
def test_raw_dc_collection_read(benchmark, bench_env, cql_session):
    _seed_collection_row(cql_session)
    stmt = _PREPARED["select_product_by_pk"]

    def _read():
        rows = cql_session.execute(stmt, (_COLL_READ_ID,))
        _row_to_product(rows.one())

    benchmark(_read)


# ---------------------------------------------------------------------------
# Collection round-trip (write + read)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="collection-roundtrip")
def test_raw_dc_collection_roundtrip(benchmark, bench_env, cql_session):
    _ensure_prepared(cql_session)
    insert_stmt = _PREPARED["insert_product"]
    select_stmt = _PREPARED["select_product_by_pk"]
    tags = ["alpha", "beta", "gamma", "delta", "epsilon"]

    def _roundtrip():
        pid = uuid4()
        cql_session.execute(insert_stmt, (pid, "CollRT", "Unknown", "general", 0.0, tags, None))
        rows = cql_session.execute(select_stmt, (pid,))
        _row_to_product(rows.one())

    benchmark(_roundtrip)


# ---------------------------------------------------------------------------
# Model instantiation from dict (no DB — pure serialization overhead)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="model-instantiation")
def test_raw_dc_model_instantiation(benchmark):
    data = {
        "id": uuid4(),
        "name": "InstBench",
        "brand": "BrandX",
        "category": "catA",
        "price": 19.99,
        "tags": ["a", "b", "c"],
        "description": "A benchmark product",
    }

    def _create():
        RawProduct(**data)

    benchmark(_create)


# ---------------------------------------------------------------------------
# Model serialization (model → dict for INSERT — no DB)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="model-serialization")
def test_raw_dc_model_serialization(benchmark):
    from dataclasses import asdict

    doc = RawProduct(
        id=uuid4(),
        name="SerBench",
        brand="BrandX",
        category="catA",
        price=19.99,
        tags=["a", "b", "c"],
        description="A benchmark product",
    )

    def _serialize():
        asdict(doc)

    benchmark(_serialize)
