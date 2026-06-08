"""Shared ScyllaDB testcontainer fixtures.

Import these into integration test or benchmark conftest.py files to avoid
duplicating the container setup, address translator, and session creation.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import pytest


class LocalhostTranslator:
    """Translate any discovered host address to 127.0.0.1.

    When ScyllaDB runs in Docker, system.local advertises the container-internal
    IP (e.g. 172.17.0.3) as the broadcast RPC address.  The cassandra-driver
    replaces its host-table entry for the contact point with that internal IP and
    then tries to reconnect there — which fails on a CI runner.

    By translating every address back to 127.0.0.1 the driver always reaches the
    node through the mapped host port, regardless of what Scylla advertises.
    """

    def translate(self, addr: str) -> str:
        return "127.0.0.1"


@pytest.fixture(scope="session")
def _test_network():
    """Shared Docker network so ScyllaDB and vector-store can find each other by hostname."""
    try:
        from testcontainers.core.network import Network  # type: ignore[import-untyped]
    except ImportError:
        yield None
        return

    with Network() as network:
        yield network


def _start_scylla(image: str, base_cmd: str, ready_log: str, network: Any) -> Any:
    """Start a ScyllaDB container, falling back if ``--experimental-features`` is rejected.

    On ScyllaDB 2025.x+ vector-search is GA and the experimental flag is
    invalid.  The image uses supervisord, so the container stays "running"
    even after scylla crashes — we detect the failure from the container logs.
    """
    from testcontainers.core.container import DockerContainer  # type: ignore[import-untyped]
    from testcontainers.core.waiting_utils import wait_for_logs  # type: ignore[import-untyped]

    vector_store_uri = "--vector-store-primary-uri=http://vector-store:6080"
    error_signature = "the argument ('vector-search') for option '--experimental-features' is invalid"

    cmd_with_flag = f"{base_cmd} {vector_store_uri} --experimental-features=vector-search"
    cmd_without_flag = f"{base_cmd} {vector_store_uri}"

    container = DockerContainer(image).with_command(cmd_with_flag).with_exposed_ports(9042)
    if network is not None:
        container = container.with_network(network).with_network_aliases("scylla")
    container.start()

    # Give supervisord time to attempt scylla startup and potentially fail.
    time.sleep(10)
    logs = container.get_wrapped_container().logs().decode("utf-8", errors="replace")
    if error_signature in logs:
        logging.info("Container rejected --experimental-features=vector-search; retrying without it")
        container.stop()
        container = DockerContainer(image).with_command(cmd_without_flag).with_exposed_ports(9042)
        if network is not None:
            container = container.with_network(network).with_network_aliases("scylla")
        container.start()

    wait_for_logs(container, ready_log, timeout=120)
    return container


@pytest.fixture(scope="session")
def scylla_container(_test_network):
    """Start a ScyllaDB container once for the entire test session.

    Uses DockerContainer directly to avoid ScyllaContainer._connect(), which
    calls get_cluster() with the container's internal Docker IP but the mapped
    host port — an incorrect combination that causes NoHostAvailable on GHA.

    Tries ``--experimental-features=vector-search`` first (required on older
    ScyllaDB images).  If the container crashes because the flag is no longer
    valid (vector-search became GA in 2025.x), restarts without it.

    The container joins ``_test_network`` with alias ``scylla`` so that the
    vector-store sidecar can reach it, and is configured with
    ``--vector-store-primary-uri`` pointing at the ``vector-store`` alias.
    """
    try:
        from testcontainers.core.container import DockerContainer  # type: ignore[import-untyped]  # noqa: F401
    except ImportError as exc:
        pytest.skip(f"testcontainers not installed: {exc}")

    image = "scylladb/scylla:2025.4.5"
    base_cmd = "--smp 1 --memory 512M --developer-mode 1 --skip-wait-for-gossip-to-settle=0"
    ready_log = "Starting listening for CQL clients"

    container = _start_scylla(image, base_cmd, ready_log, _test_network)
    try:
        yield container
    finally:
        container.stop()


@pytest.fixture(scope="session")
def vector_store_container(scylla_container, _test_network):
    """Start the vector-store sidecar on the shared Docker network.

    The sidecar connects to ScyllaDB via the ``scylla`` network alias.
    ScyllaDB already has ``--vector-store-primary-uri=http://vector-store:6080``
    so ANN queries are routed to this container once it is healthy.
    """
    try:
        from testcontainers.core.container import DockerContainer  # type: ignore[import-untyped]
        from testcontainers.core.waiting_utils import wait_for_logs  # type: ignore[import-untyped]
    except ImportError as exc:
        pytest.skip(f"testcontainers not installed: {exc}")

    container = (
        DockerContainer("scylladb/vector-store:latest")
        .with_env("VECTOR_STORE_SCYLLADB_URI", "scylla:9042")
        .with_env("VECTOR_STORE_URI", "0.0.0.0:6080")
        .with_exposed_ports(6080)
    )
    if _test_network is not None:
        container = container.with_network(_test_network).with_network_aliases("vector-store")
    container.start()
    try:
        wait_for_logs(container, "listening", timeout=120)
        yield container
    finally:
        container.stop()


def create_cql_session(scylla_container: Any, keyspace: str, *, tablets: bool = True) -> Any:
    """Create a cassandra-driver Session connected to the given keyspace.

    Handles the retry loop for container startup and creates the keyspace
    if it doesn't exist.

    Args:
        scylla_container: The testcontainer running ScyllaDB.
        keyspace: The keyspace name to create and connect to.
        tablets: If ``True`` (default), create the keyspace with
            ``NetworkTopologyStrategy + tablets = {'enabled': true}``, which is
            required by ``vector_index`` on ScyllaDB 6.x+.  Falls back to
            ``SimpleStrategy`` when tablets are not supported by the server.
            Pass ``False`` to always use ``SimpleStrategy``.

    Returns:
        ``(session, cluster)`` so the caller can shut down the cluster.
    """
    from cassandra.cluster import Cluster, NoHostAvailable  # type: ignore[import-untyped]

    port = int(scylla_container.get_exposed_port(9042))
    cluster = Cluster(
        ["127.0.0.1"],
        port=port,
        connect_timeout=10,
        address_translator=LocalhostTranslator(),
    )

    for attempt in range(10):
        try:
            session = cluster.connect()
            break
        except NoHostAvailable:
            if attempt == 9:
                raise
            time.sleep(2)

    if tablets:
        # Discover the datacenter name (required for NetworkTopologyStrategy).
        # The column is called "data_center" in Cassandra/ScyllaDB.
        row = session.execute("SELECT data_center FROM system.local").one()
        dc = getattr(row, "data_center", "datacenter1") if row else "datacenter1"
        # Try NTS + tablets; fall back to SimpleStrategy on older ScyllaDB.
        try:
            session.execute(
                f"CREATE KEYSPACE IF NOT EXISTS {keyspace} "
                f"WITH replication = {{'class': 'NetworkTopologyStrategy', '{dc}': 1}} "
                f"AND tablets = {{'enabled': true}}"
            )
        except Exception as exc:  # noqa: BLE001
            logging.warning("Tablets not available (%s); creating %s without tablets", exc, keyspace)
            session.execute(
                f"CREATE KEYSPACE IF NOT EXISTS {keyspace} "
                "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}"
            )
    else:
        session.execute(
            f"CREATE KEYSPACE IF NOT EXISTS {keyspace} "
            "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}"
        )

    session.set_keyspace(keyspace)
    return session, cluster


async def create_acsylla_session(scylla_container: Any, keyspace: str) -> Any:
    """Create an acsylla session connected to the given keyspace.

    Creates the keyspace if it doesn't exist, then returns a session with
    the keyspace already set.
    """
    import acsylla  # type: ignore[import-untyped]

    container_info = scylla_container.get_wrapped_container()
    container_info.reload()
    networks = container_info.attrs["NetworkSettings"]["Networks"]
    container_ip = next(iter(networks.values()))["IPAddress"]

    cluster = acsylla.create_cluster([container_ip], port=9042)
    session = await cluster.create_session()
    await session.execute(
        acsylla.create_statement(
            f"CREATE KEYSPACE IF NOT EXISTS {keyspace} "
            "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}",
            parameters=0,
        )
    )
    await session.close()
    return await cluster.create_session(keyspace=keyspace)


async def create_python_rs_session(scylla_container: Any, keyspace: str) -> Any:
    """Create a python-rs-driver session connected to the given keyspace.

    Creates the keyspace if it doesn't exist via a temporary session,
    then returns a new session.  Uses the container's internal IP since
    python-rs-driver does not need an address translator.
    """
    from scylla.session_builder import SessionBuilder  # type: ignore[import-untyped]

    container_info = scylla_container.get_wrapped_container()
    container_info.reload()
    networks = container_info.attrs["NetworkSettings"]["Networks"]
    container_ip = next(iter(networks.values()))["IPAddress"]

    builder = SessionBuilder().contact_points(((container_ip, 9042),))
    session = await builder.connect()

    # Create keyspace via raw CQL (USE keyspace is not supported)
    await session.execute(
        f"CREATE KEYSPACE IF NOT EXISTS {keyspace} "
        "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}",
        None,
    )
    return session
