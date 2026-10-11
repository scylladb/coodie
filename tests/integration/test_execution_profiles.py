"""CassandraDriver on a session whose cluster uses execution profiles (#329)."""

from __future__ import annotations

import pytest

from tests.conftest_scylla import LocalhostTranslator

pytestmark = pytest.mark.integration


@pytest.fixture
def profile_session(scylla_container, scylla_session, driver_type):
    if driver_type in ("acsylla", "python-rs"):
        pytest.skip("cassandra-driver execution profiles only")
    from cassandra import ConsistencyLevel
    from cassandra.cluster import EXEC_PROFILE_DEFAULT, Cluster, ExecutionProfile

    cluster = Cluster(
        ["127.0.0.1"],
        port=int(scylla_container.get_exposed_port(9042)),
        address_translator=LocalhostTranslator(),
        execution_profiles={EXEC_PROFILE_DEFAULT: ExecutionProfile(consistency_level=ConsistencyLevel.ONE)},
    )
    yield cluster.connect()
    cluster.shutdown()


def test_cassandra_driver_on_execution_profile_session(profile_session):
    from coodie.drivers.cassandra import CassandraDriver

    driver = CassandraDriver(session=profile_session, default_keyspace="test_ks")
    driver.execute("CREATE TABLE IF NOT EXISTS test_ks.exec_profiles (id int PRIMARY KEY, name text)", [])
    driver.execute("INSERT INTO test_ks.exec_profiles (id, name) VALUES (?, ?)", [1, "Alice"])

    assert driver.execute("SELECT id, name FROM test_ks.exec_profiles WHERE id = ?", [1]) == [
        {"id": 1, "name": "Alice"}
    ]
    # A failed LWT must report "[applied]": False (named tuples would rename the column)
    rows = driver.execute("UPDATE test_ks.exec_profiles SET name = ? WHERE id = ? IF name = ?", ["Bob", 1, "Carol"])
    assert rows == [{"[applied]": False, "name": "Alice"}]
