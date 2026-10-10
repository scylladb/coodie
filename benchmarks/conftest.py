"""Shared fixtures for coodie vs cqlengine vs raw-dc benchmarks.

Provides a ScyllaDB testcontainer, cqlengine connection setup, coodie
driver registration, and raw CQL + dataclass (Raw+DC) prepared statements.
All benchmark files share these session-scoped fixtures so the database
container is started only once.

Use ``--driver-type`` to choose the coodie driver backend:

- ``scylla``   (default) — CassandraDriver backed by scylla-driver
- ``cassandra`` — CassandraDriver backed by cassandra-driver
- ``acsylla``  — AcsyllaDriver backed by the async-native acsylla library
- ``python-rs`` — PythonRsDriver backed by the Rust-based python-rs-driver

The **cqlengine** side always uses cassandra-driver / scylla-driver regardless
of ``--driver-type`` (cqlengine has no acsylla backend).

The **Raw+DC** side uses the same cassandra-driver session directly, executing
hand-written CQL and hydrating plain Python ``dataclasses``.
"""

from __future__ import annotations

import asyncio
import gc
import logging
import os
from typing import Any
from uuid import uuid4

import pytest

from tests.conftest_scylla import (  # noqa: F401
    _test_network,
    create_acsylla_session,
    create_cql_session,
    create_python_rs_session,
    scylla_container,
    vector_store_container,
)

# ---------------------------------------------------------------------------
# CLI option
# ---------------------------------------------------------------------------


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--driver-type",
        default="scylla",
        choices=["scylla", "cassandra", "acsylla", "python-rs"],
        help="Coodie driver backend for benchmarks (default: scylla)",
    )


def pytest_configure(config: pytest.Config) -> None:
    # Instruction counts measure a single call; GC runs triggered by earlier
    # allocations would land in it at random (CODSPEED_ENV is set by CI).
    if os.environ.get("CODSPEED_ENV"):
        gc.disable()


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    # Benchmarks that never touch the database run under CodSpeed instruction counting.
    for item in items:
        if "scylla_container" not in item.fixturenames:
            item.add_marker(pytest.mark.in_memory)


@pytest.fixture(scope="session")
def driver_type(request: pytest.FixtureRequest) -> str:
    return request.config.getoption("--driver-type")


# ---------------------------------------------------------------------------
# Raw cassandra-driver session (used by cqlengine and coodie when not acsylla)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def cql_session(scylla_container: Any):  # noqa: F811
    """Return a cassandra-driver ``Session`` connected to the bench keyspace."""
    try:
        session, cluster = create_cql_session(scylla_container, "bench_ks", tablets=False)
    except (ImportError, ModuleNotFoundError):
        pytest.skip("cassandra-driver not available")
    session.set_keyspace("bench_ks")
    yield session
    cluster.shutdown()


# ---------------------------------------------------------------------------
# cqlengine setup
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def cqlengine_connection(cql_session: Any):
    """Register cqlengine connection and sync tables."""
    try:
        from cassandra.cqlengine import connection as cql_conn
        from cassandra.cqlengine.management import sync_table
    except ImportError:
        pytest.skip("cqlengine not available (install cassandra-driver or scylla-driver)")

    cql_conn.register_connection("bench", session=cql_session)
    cql_conn.set_default_connection("bench")

    from benchmarks.models_argus_cqlengine import (
        CqlArgusComment,
        CqlArgusEvent,
        CqlArgusNotification,
        CqlArgusTestRun,
        CqlArgusUser,
    )
    from benchmarks.models_cqlengine import CqlEvent, CqlProduct, CqlReview, CqlVectorProduct

    sync_table(CqlProduct, keyspaces=["bench_ks"])
    sync_table(CqlReview, keyspaces=["bench_ks"])
    sync_table(CqlEvent, keyspaces=["bench_ks"])
    sync_table(CqlVectorProduct, keyspaces=["bench_ks"])
    sync_table(CqlArgusUser, keyspaces=["bench_ks"])
    sync_table(CqlArgusTestRun, keyspaces=["bench_ks"])
    sync_table(CqlArgusEvent, keyspaces=["bench_ks"])
    sync_table(CqlArgusNotification, keyspaces=["bench_ks"])
    sync_table(CqlArgusComment, keyspaces=["bench_ks"])
    yield
    cql_conn.unregister_connection("bench")


# ---------------------------------------------------------------------------
# coodie driver setup
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def coodie_connection(cql_session: Any, scylla_container: Any, vector_store_container: Any, driver_type: str):  # noqa: F811
    """Register a coodie driver — backend chosen by ``--driver-type``.

    * ``scylla`` / ``cassandra`` — CassandraDriver sharing the cql_session
    * ``acsylla`` — AcsyllaDriver with its own async-native session
    * ``python-rs`` — PythonRsDriver with a Rust-backed async session

    Depends on ``vector_store_container`` so the vector-store service is started
    before benchmarks that exercise vector search (e.g. ``test_coodie_ann_select``).
    """
    from coodie.drivers import _registry, init_coodie, register_driver

    _registry.clear()

    # Create a tablet-enabled keyspace for vector benchmarks (required by
    # vector_index on ScyllaDB 6.x+).
    try:
        _vec_session, _vec_cluster = create_cql_session(scylla_container, "bench_vector_ks")
        _vec_cluster.shutdown()
    except Exception as exc:  # noqa: BLE001
        logging.getLogger(__name__).warning("Could not create bench_vector_ks with tablets (%s)", exc)

    if driver_type == "acsylla":
        try:
            import acsylla  # type: ignore[import-untyped] # noqa: F401
        except ImportError:
            pytest.skip("acsylla is not installed")

        from coodie.drivers.acsylla import AcsyllaDriver

        loop = asyncio.new_event_loop()
        session = loop.run_until_complete(create_acsylla_session(scylla_container, "bench_ks"))
        driver = AcsyllaDriver(session=session, default_keyspace="bench_ks", loop=loop)
        register_driver("default", driver, default=True)
    elif driver_type == "python-rs":
        try:
            import scylla  # type: ignore[import-untyped] # noqa: F401
        except ImportError:
            pytest.skip("python-rs-driver is not installed")

        from coodie.drivers.python_rs import PythonRsDriver

        loop = asyncio.new_event_loop()
        session = loop.run_until_complete(create_python_rs_session(scylla_container, "bench_ks"))
        driver = PythonRsDriver(session=session, default_keyspace="bench_ks", loop=loop)
        register_driver("default", driver, default=True)
    else:
        driver = init_coodie(session=cql_session, keyspace="bench_ks", driver_type=driver_type)

    from benchmarks.models_argus_coodie import (
        CoodieArgusComment,
        CoodieArgusEvent,
        CoodieArgusNotification,
        CoodieArgusTestRun,
        CoodieArgusUser,
    )
    from benchmarks.models_coodie import CoodieEvent, CoodieProduct, CoodieReview, CoodieVectorProduct

    CoodieProduct.sync_table()
    CoodieReview.sync_table()
    CoodieEvent.sync_table()
    CoodieVectorProduct.sync_table()
    CoodieArgusUser.sync_table()
    CoodieArgusTestRun.sync_table()
    CoodieArgusEvent.sync_table()
    CoodieArgusNotification.sync_table()
    CoodieArgusComment.sync_table()
    yield driver
    _registry.clear()


# ---------------------------------------------------------------------------
# Combined setup (ensures both sides are ready)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def bench_env(cqlengine_connection: Any, coodie_connection: Any):
    """Ensure cqlengine and coodie are fully initialised.

    Raw+DC benchmarks prepare their own CQL statements lazily via the
    ``cql_session`` fixture — no separate setup fixture is needed.
    """
    yield


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_uuid():
    """Return a new random UUID."""
    return uuid4()
