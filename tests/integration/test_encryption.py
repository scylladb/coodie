"""Integration tests for SSL/TLS client encryption.

These tests spin up a ScyllaDB container with ``client_encryption_options``
enabled, generate a self-signed server certificate via the ``cryptography``
library, and verify that both ``CassandraDriver`` and ``AcsyllaDriver`` can
connect successfully over TLS.

Requirements:
- ``cryptography`` (available when scylla-driver / cassandra-driver is installed)
- ``testcontainers``
- Docker

Run with::

    pytest -m integration tests/integration/test_encryption.py -v
"""

from __future__ import annotations

import ipaddress
import ssl
import time
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio

from tests.conftest_scylla import LocalhostTranslator

# ---------------------------------------------------------------------------
# Cert-generation helper
# ---------------------------------------------------------------------------


def _generate_certs(cert_dir: Path) -> dict[str, Path]:
    """Generate a self-signed CA + server certificate using ``cryptography``.

    Returns a dict with keys ``ca_cert``, ``server_cert``, ``server_key``.
    Raises ``ImportError`` when ``cryptography`` is not installed.
    """
    import datetime

    from cryptography import x509  # type: ignore[import-untyped]
    from cryptography.hazmat.primitives import hashes, serialization  # type: ignore[import-untyped]
    from cryptography.hazmat.primitives.asymmetric import rsa  # type: ignore[import-untyped]
    from cryptography.x509.oid import NameOID  # type: ignore[import-untyped]

    now = datetime.datetime.now(datetime.timezone.utc)
    expiry = now + datetime.timedelta(days=365)

    # --- CA ----------------------------------------------------------------
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "coodie-test-ca")])
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(ca_name)
        .issuer_name(ca_name)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(expiry)
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(ca_key, hashes.SHA256())
    )

    ca_cert_path = cert_dir / "ca.crt"
    ca_cert_path.write_bytes(ca_cert.public_bytes(serialization.Encoding.PEM))

    # --- Server cert -------------------------------------------------------
    server_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    server_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
    server_cert = (
        x509.CertificateBuilder()
        .subject_name(server_name)
        .issuer_name(ca_name)
        .public_key(server_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(expiry)
        .add_extension(
            x509.SubjectAlternativeName(
                [
                    x509.DNSName("localhost"),
                    x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                ]
            ),
            critical=False,
        )
        .sign(ca_key, hashes.SHA256())
    )

    server_cert_path = cert_dir / "server.crt"
    server_key_path = cert_dir / "server.key"
    server_cert_path.write_bytes(server_cert.public_bytes(serialization.Encoding.PEM))
    server_key_path.write_bytes(
        server_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

    return {
        "ca_cert": ca_cert_path,
        "server_cert": server_cert_path,
        "server_key": server_key_path,
    }


# ---------------------------------------------------------------------------
# Session-scoped fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def ssl_certs(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    """Generate a self-signed CA + server certificate pair.

    Skips the test session if ``cryptography`` is not installed.
    """
    try:
        import cryptography  # type: ignore[import-untyped]  # noqa: F401
    except ImportError:
        pytest.skip("cryptography is not installed — skipping SSL tests")

    cert_dir = tmp_path_factory.mktemp("ssl_certs")
    return _generate_certs(cert_dir)


@pytest.fixture(scope="session")
def scylla_ssl_container(ssl_certs: dict[str, Path]) -> Any:
    """Start a ScyllaDB container with TLS enabled.

    Mounts the generated certificates and a custom ``scylla.yaml`` that enables
    ``client_encryption_options``.
    """
    try:
        from testcontainers.core.container import DockerContainer  # type: ignore[import-untyped]
        from testcontainers.core.waiting_utils import wait_for_logs  # type: ignore[import-untyped]
    except ImportError:
        pytest.skip("testcontainers is not installed — skipping SSL tests")

    cert_dir = ssl_certs["ca_cert"].parent

    # Write a scylla.yaml fragment that enables client encryption
    scylla_yaml = cert_dir / "scylla.yaml"
    scylla_yaml.write_text(
        "client_encryption_options:\n"
        "  enabled: true\n"
        "  certificate: /certs/server.crt\n"
        "  keyfile: /certs/server.key\n"
        "  require_client_auth: false\n"
    )

    with (
        DockerContainer("scylladb/scylla:2025.4.5")
        .with_command(
            "--smp 1 --memory 512M --developer-mode 1 "
            "--skip-wait-for-gossip-to-settle=0 "
            "--options-file /certs/scylla.yaml"
        )
        .with_volume_mapping(str(cert_dir), "/certs", "ro")
        .with_exposed_ports(9042) as container
    ):
        wait_for_logs(container, "Starting listening for CQL clients", timeout=120)
        yield container


@pytest.fixture(scope="session")
def ssl_session(scylla_ssl_container: Any, ssl_certs: dict[str, Path]) -> Any:
    """Return a cassandra-driver Session connected over TLS."""
    from cassandra.cluster import Cluster, NoHostAvailable  # type: ignore[import-untyped]

    port = int(scylla_ssl_container.get_exposed_port(9042))

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    cluster = Cluster(
        ["127.0.0.1"],
        port=port,
        ssl_context=ctx,
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

    session.execute(
        "CREATE KEYSPACE IF NOT EXISTS ssl_ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}"
    )
    yield session
    cluster.shutdown()


# ---------------------------------------------------------------------------
# CassandraDriver SSL tests (sync + async)
# ---------------------------------------------------------------------------


@pytest.mark.integration
@pytest.mark.ssl
class TestSSLCassandraDriver:
    """Verify that CassandraDriver works over a TLS-encrypted connection."""

    def test_sync_execute_over_ssl(self, ssl_session: Any) -> None:
        """execute() returns rows when the session was created with an SSLContext."""
        from typing import Annotated
        from uuid import UUID, uuid4

        from pydantic import Field

        from coodie.drivers import _registry, register_driver
        from coodie.drivers.cassandra import CassandraDriver
        from coodie.fields import PrimaryKey
        from coodie.sync.document import Document as SyncDocument

        class SSLProduct(SyncDocument):
            id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
            name: str = ""

            class Settings:
                name = "ssl_products"
                keyspace = "ssl_ks"

        _registry.clear()
        driver = CassandraDriver(session=ssl_session, default_keyspace="ssl_ks")
        register_driver("default", driver, default=True)

        try:
            SSLProduct.sync_table()
            doc = SSLProduct(name="encrypted-widget")
            doc.save()
            found = SSLProduct.find_one(id=doc.id)
            assert found is not None
            assert found.name == "encrypted-widget"
        finally:
            _registry.clear()

    @pytest.mark.asyncio
    async def test_async_execute_over_ssl(self, ssl_session: Any) -> None:
        """execute_async() returns rows when the session was created with an SSLContext."""
        from typing import Annotated
        from uuid import UUID, uuid4

        from pydantic import Field

        from coodie.aio.document import Document as AsyncDocument
        from coodie.drivers import _registry, register_driver
        from coodie.drivers.cassandra import CassandraDriver
        from coodie.fields import PrimaryKey

        class SSLAsyncProduct(AsyncDocument):
            id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
            name: str = ""

            class Settings:
                name = "ssl_async_products"
                keyspace = "ssl_ks"

        _registry.clear()
        driver = CassandraDriver(session=ssl_session, default_keyspace="ssl_ks")
        register_driver("default", driver, default=True)

        try:
            await SSLAsyncProduct.sync_table()
            doc = SSLAsyncProduct(name="async-encrypted-widget")
            await doc.save()
            found = await SSLAsyncProduct.find_one(id=doc.id)
            assert found is not None
            assert found.name == "async-encrypted-widget"
        finally:
            _registry.clear()

    def test_init_coodie_ssl_context_kwarg(self, scylla_ssl_container: Any) -> None:
        """init_coodie() forwards ssl_context kwarg to the underlying Cluster."""
        from coodie.drivers import _registry
        from coodie.sync import init_coodie

        port = int(scylla_ssl_container.get_exposed_port(9042))

        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        _registry.clear()
        try:
            driver = init_coodie(
                hosts=["127.0.0.1"],
                keyspace="ssl_ks",
                port=port,
                ssl_context=ctx,
                address_translator=LocalhostTranslator(),
            )
            rows = driver.execute("SELECT release_version FROM system.local", [])
            assert rows, "Expected at least one row from system.local"
        finally:
            _registry.clear()


# ---------------------------------------------------------------------------
# AcsyllaDriver SSL tests (async)
# ---------------------------------------------------------------------------


@pytest.mark.integration
@pytest.mark.ssl
class TestSSLAcsyllaDriver:
    """Verify that AcsyllaDriver works over a TLS-encrypted connection."""

    @pytest_asyncio.fixture(scope="class")
    async def acsylla_ssl_session(self, scylla_ssl_container: Any, ssl_certs: dict[str, Path]) -> Any:
        """Return an acsylla session connected over TLS."""
        try:
            import acsylla  # type: ignore[import-untyped]
        except ImportError:
            pytest.skip("acsylla is not installed")

        container_info = scylla_ssl_container.get_wrapped_container()
        container_info.reload()
        networks = container_info.attrs["NetworkSettings"]["Networks"]
        container_ip = next(iter(networks.values()))["IPAddress"]

        ca_pem = ssl_certs["ca_cert"].read_text()

        cluster = acsylla.create_cluster(
            [container_ip],
            port=9042,
            ssl_enabled=True,
            ssl_verify_flags=acsylla.CassSSLVerifyFlags.CASS_SSL_VERIFY_NONE,
            ssl_trusted_cert=ca_pem,
        )
        session = await cluster.create_session()
        await session.execute(
            acsylla.create_statement(
                "CREATE KEYSPACE IF NOT EXISTS ssl_ks "
                "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}",
                parameters=0,
            )
        )
        await session.close()
        session = await cluster.create_session(keyspace="ssl_ks")
        yield session
        await session.close()

    @pytest.mark.asyncio
    async def test_async_execute_over_ssl(self, acsylla_ssl_session: Any) -> None:
        """AcsyllaDriver.execute_async() returns rows over a TLS connection."""
        import asyncio
        from typing import Annotated
        from uuid import UUID, uuid4

        from pydantic import Field

        from coodie.aio.document import Document as AsyncDocument
        from coodie.drivers import _registry, register_driver
        from coodie.drivers.acsylla import AcsyllaDriver
        from coodie.fields import PrimaryKey

        class SSLAcsyllaProduct(AsyncDocument):
            id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
            name: str = ""

            class Settings:
                name = "ssl_acsylla_products"
                keyspace = "ssl_ks"

        _registry.clear()
        loop = asyncio.get_running_loop()
        driver = AcsyllaDriver(session=acsylla_ssl_session, default_keyspace="ssl_ks", loop=loop)
        register_driver("default", driver, default=True)

        try:
            await SSLAcsyllaProduct.sync_table()
            doc = SSLAcsyllaProduct(name="acsylla-encrypted-widget")
            await doc.save()
            found = await SSLAcsyllaProduct.find_one(id=doc.id)
            assert found is not None
            assert found.name == "acsylla-encrypted-widget"
        finally:
            _registry.clear()

    @pytest.mark.asyncio
    async def test_init_coodie_async_ssl_kwargs(self, scylla_ssl_container: Any, ssl_certs: dict[str, Path]) -> None:
        """init_coodie_async() forwards ssl_enabled / ssl_trusted_cert to acsylla.create_cluster()."""
        try:
            import acsylla  # type: ignore[import-untyped]  # noqa: F401
        except ImportError:
            pytest.skip("acsylla is not installed")

        from coodie.aio import init_coodie
        from coodie.drivers import _registry

        container_info = scylla_ssl_container.get_wrapped_container()
        container_info.reload()
        networks = container_info.attrs["NetworkSettings"]["Networks"]
        container_ip = next(iter(networks.values()))["IPAddress"]

        ca_pem = ssl_certs["ca_cert"].read_text()

        _registry.clear()
        try:
            driver = await init_coodie(
                hosts=[container_ip],
                keyspace="ssl_ks",
                driver_type="acsylla",
                ssl_enabled=True,
                ssl_verify_flags=0,  # CASS_SSL_VERIFY_NONE
                ssl_trusted_cert=ca_pem,
            )
            rows = await driver.execute_async("SELECT release_version FROM system.local", [])
            assert rows, "Expected at least one row from system.local"
        finally:
            _registry.clear()
