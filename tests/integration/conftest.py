"""Integration test fixtures, models, and helpers.

Run with:  pytest -m integration -v
Skipped by default (addopts = "-m 'not integration'").

Use ``--driver-type`` to choose the driver backend:
- ``scylla`` (default) — uses scylla-driver
- ``cassandra`` — uses cassandra-driver
- ``acsylla`` — uses acsylla
- ``python-rs`` — uses python-rs-driver (Rust-based)
"""

from __future__ import annotations

import asyncio
import decimal
import ipaddress
from datetime import date, datetime, timezone
from datetime import time as dt_time
from typing import Annotated
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from pydantic import Field, field_validator

from coodie.aio.document import CounterDocument as AsyncCounterDocument
from coodie.aio.document import Document as AsyncDocument
from coodie.aio.document import MaterializedView as AsyncMaterializedView
from coodie.drivers import _registry, init_coodie
from coodie.fields import (
    Ascii,
    BigInt,
    ClusteringKey,
    Counter,
    Discriminator,
    Double,
    Frozen,
    Indexed,
    PrimaryKey,
    SmallInt,
    Static,
    TimeUUID,
    TinyInt,
    VarInt,
)
from coodie.sync.document import CounterDocument as SyncCounterDocument
from coodie.sync.document import Document as SyncDocument
from coodie.sync.document import MaterializedView as SyncMaterializedView
from tests.conftest import _maybe_await
from tests.conftest_scylla import (  # noqa: F401
    _test_network,
    create_acsylla_session,
    create_cql_session,
    create_python_rs_session,
    scylla_container,
    vector_store_container,
)

# ---------------------------------------------------------------------------
# Session-scoped fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def scylla_session(scylla_container: object, driver_type: str) -> object:  # noqa: F811
    """Return a connected cassandra-driver Session with the test keyspace.

    Skipped when ``--driver-type=acsylla`` or ``--driver-type=python-rs``
    (cassandra-driver may not be installed).
    """
    if driver_type in ("acsylla", "python-rs"):
        yield None
        return

    session, cluster = create_cql_session(scylla_container, "test_ks", tablets=False)
    yield session
    cluster.shutdown()


@pytest.fixture(scope="session")
def scylla_vector_session(scylla_container: object, vector_store_container: object, driver_type: str) -> object:  # noqa: F811
    """Return a cassandra-driver Session with a tablet-enabled ``vector_ks`` keyspace.

    Depends on ``vector_store_container`` so the vector-store service is started
    before vector tests run.  Uses NetworkTopologyStrategy + tablets for vector
    index support on ScyllaDB 6.x+.
    Skipped when ``--driver-type=acsylla`` or ``--driver-type=python-rs``.
    """
    if driver_type in ("acsylla", "python-rs"):
        yield None
        return

    try:
        session, cluster = create_cql_session(scylla_container, "vector_ks")
    except (ImportError, ModuleNotFoundError):
        yield None
        return

    yield session
    cluster.shutdown()


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def coodie_driver(
    scylla_session: object,
    scylla_container: object,  # noqa: F811
    driver_type: str,
) -> object:
    """Register a coodie driver backed by the real ScyllaDB session.

    When ``--driver-type=scylla`` (default) or ``--driver-type=cassandra``
    uses CassandraDriver (both scylla-driver and cassandra-driver expose the
    same ``cassandra`` Python package).
    When ``--driver-type=acsylla`` creates an acsylla session connecting to the
    same container and registers an AcsyllaDriver instead.
    When ``--driver-type=python-rs`` creates a python-rs-driver session and
    registers a PythonRsDriver.
    """
    _registry.clear()
    if driver_type == "acsylla":
        try:
            import acsylla  # type: ignore[import-untyped] # noqa: F401
        except ImportError:
            pytest.skip("acsylla is not installed")

        from coodie.drivers.acsylla import AcsyllaDriver

        acsylla_driver = AcsyllaDriver.connect(
            session_factory=lambda: create_acsylla_session(scylla_container, "test_ks"),
            default_keyspace="test_ks",
        )
        from coodie.drivers import register_driver

        register_driver("default", acsylla_driver, default=True)
        driver = acsylla_driver
    elif driver_type == "python-rs":
        try:
            import scylla  # type: ignore[import-untyped] # noqa: F401
        except ImportError:
            pytest.skip("python-rs-driver is not installed")

        from coodie.drivers.python_rs import PythonRsDriver

        python_rs_driver = PythonRsDriver.connect(
            session_factory=lambda: create_python_rs_session(scylla_container, "test_ks"),
            default_keyspace="test_ks",
        )
        from coodie.drivers import register_driver

        register_driver("default", python_rs_driver, default=True)
        driver = python_rs_driver
    else:
        driver = init_coodie(session=scylla_session, keyspace="test_ks", driver_type=driver_type)
    yield driver
    _registry.clear()
    await driver.close_async()


# ---------------------------------------------------------------------------
# Shared document models
# ---------------------------------------------------------------------------


class SyncProduct(SyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    brand: Annotated[str, Indexed()] = "Unknown"
    category: Annotated[str, Indexed()] = "general"
    price: float = 0.0
    tags: list[str] = Field(default_factory=list)
    description: str | None = None

    @field_validator("tags", mode="before")
    @classmethod
    def _coerce_tags(cls, v: object) -> object:
        return v if v is not None else []

    class Settings:
        name = "it_sync_products"
        keyspace = "test_ks"


class AsyncProduct(AsyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    brand: Annotated[str, Indexed()] = "Unknown"
    category: Annotated[str, Indexed()] = "general"
    price: float = 0.0
    tags: list[str] = Field(default_factory=list)
    description: str | None = None

    @field_validator("tags", mode="before")
    @classmethod
    def _coerce_tags(cls, v: object) -> object:
        return v if v is not None else []

    class Settings:
        name = "it_async_products"
        keyspace = "test_ks"


class SyncReview(SyncDocument):
    product_id: Annotated[UUID, PrimaryKey()]
    created_at: Annotated[datetime, ClusteringKey(order="DESC")] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    author: str
    rating: Annotated[int, Indexed()] = 0

    class Settings:
        name = "it_sync_reviews"
        keyspace = "test_ks"


class AsyncReview(AsyncDocument):
    product_id: Annotated[UUID, PrimaryKey()]
    created_at: Annotated[datetime, ClusteringKey(order="DESC")] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    author: str
    rating: Annotated[int, Indexed()] = 0

    class Settings:
        name = "it_async_reviews"
        keyspace = "test_ks"


class SyncProductsByBrand(SyncMaterializedView):
    """Materialized view on SyncProduct indexed by brand."""

    brand: Annotated[str, PrimaryKey()]
    id: Annotated[UUID, ClusteringKey()] = Field(default_factory=uuid4)
    name: str = ""
    price: float = 0.0

    class Settings:
        name = "it_sync_products_by_brand"
        keyspace = "test_ks"
        __base_table__ = "it_sync_products"


class AsyncProductsByBrand(AsyncMaterializedView):
    """Async materialized view on AsyncProduct indexed by brand."""

    brand: Annotated[str, PrimaryKey()]
    id: Annotated[UUID, ClusteringKey()] = Field(default_factory=uuid4)
    name: str = ""
    price: float = 0.0

    class Settings:
        name = "it_async_products_by_brand"
        keyspace = "test_ks"
        __base_table__ = "it_async_products"


class SyncAllTypes(SyncDocument):
    """One column per supported scalar CQL type + set and dict collections."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    flag: bool = False
    count: int = 0
    score: float = 0.0
    amount: decimal.Decimal = decimal.Decimal("0.0")
    blob_val: bytes = b""
    ts: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    day: date = Field(default_factory=date.today)
    ip4: ipaddress.IPv4Address | None = None
    ip6: ipaddress.IPv6Address | None = None
    tags_set: set[str] = Field(default_factory=set)
    scores_map: dict[str, int] = Field(default_factory=dict)

    @field_validator("tags_set", mode="before")
    @classmethod
    def _coerce_set(cls, v: object) -> object:
        return v if v is not None else set()

    @field_validator("scores_map", mode="before")
    @classmethod
    def _coerce_map(cls, v: object) -> object:
        return v if v is not None else {}

    @field_validator("day", mode="before")
    @classmethod
    def _coerce_day(cls, v: object) -> object:
        if hasattr(v, "date") and callable(v.date):
            return v.date()
        return v

    class Settings:
        name = "it_all_types"
        keyspace = "test_ks"


class AsyncAllTypes(AsyncDocument):
    """Async counterpart of SyncAllTypes."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    flag: bool = False
    count: int = 0
    score: float = 0.0
    amount: decimal.Decimal = decimal.Decimal("0.0")
    blob_val: bytes = b""
    ts: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    day: date = Field(default_factory=date.today)
    ip4: ipaddress.IPv4Address | None = None
    ip6: ipaddress.IPv6Address | None = None
    tags_set: set[str] = Field(default_factory=set)
    scores_map: dict[str, int] = Field(default_factory=dict)

    @field_validator("tags_set", mode="before")
    @classmethod
    def _coerce_set(cls, v: object) -> object:
        return v if v is not None else set()

    @field_validator("scores_map", mode="before")
    @classmethod
    def _coerce_map(cls, v: object) -> object:
        return v if v is not None else {}

    @field_validator("day", mode="before")
    @classmethod
    def _coerce_day(cls, v: object) -> object:
        if hasattr(v, "date") and callable(v.date):
            return v.date()
        return v

    class Settings:
        name = "it_async_all_types"
        keyspace = "test_ks"


class SyncEvent(SyncDocument):
    """Composite partition key + two clustering columns for ordering tests."""

    partition_a: Annotated[str, PrimaryKey(partition_key_index=0)]
    partition_b: Annotated[str, PrimaryKey(partition_key_index=1)]
    seq: Annotated[int, ClusteringKey(order="ASC", clustering_key_index=0)] = 0
    sub: Annotated[int, ClusteringKey(order="DESC", clustering_key_index=1)] = 0
    payload: str = ""

    class Settings:
        name = "it_sync_events"
        keyspace = "test_ks"


class AsyncEvent(AsyncDocument):
    """Async counterpart of SyncEvent."""

    partition_a: Annotated[str, PrimaryKey(partition_key_index=0)]
    partition_b: Annotated[str, PrimaryKey(partition_key_index=1)]
    seq: Annotated[int, ClusteringKey(order="ASC", clustering_key_index=0)] = 0
    sub: Annotated[int, ClusteringKey(order="DESC", clustering_key_index=1)] = 0
    payload: str = ""

    class Settings:
        name = "it_async_events"
        keyspace = "test_ks"


# Microsecond constants for converting CQL time (nanoseconds) → datetime.time
_US_PER_HOUR = 3_600_000_000
_US_PER_MINUTE = 60_000_000
_US_PER_SECOND = 1_000_000

try:
    from cassandra.util import Time as _CqlTime  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover – only needed at integration time
    _CqlTime = None


def _ns_to_time(ns: int) -> dt_time:
    """Convert nanoseconds since midnight to ``datetime.time``."""
    total_us = ns // 1000
    hours, remainder = divmod(total_us, _US_PER_HOUR)
    minutes, remainder = divmod(remainder, _US_PER_MINUTE)
    seconds, microseconds = divmod(remainder, _US_PER_SECOND)
    return dt_time(hours, minutes, seconds, microseconds)


def _coerce_cql_time(v: object) -> object:
    """Coerce cassandra-driver's CQL ``time`` value to ``datetime.time``."""
    if _CqlTime is not None and isinstance(v, _CqlTime):
        return _ns_to_time(v.nanosecond_time)
    if isinstance(v, int):
        return _ns_to_time(v)
    return v


class SyncExtendedTypes(SyncDocument):
    """One column per Phase-1 extended CQL scalar type + frozen collections."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    big_val: Annotated[int, BigInt()] = 0
    small_val: Annotated[int, SmallInt()] = 0
    tiny_val: Annotated[int, TinyInt()] = 0
    var_val: Annotated[int, VarInt()] = 0
    dbl_val: Annotated[float, Double()] = 0.0
    ascii_val: Annotated[str, Ascii()] = ""
    timeuuid_val: Annotated[UUID | None, TimeUUID()] = None
    time_val: dt_time | None = None
    frozen_list: Annotated[list[str], Frozen()] = Field(default_factory=list)
    frozen_set: Annotated[set[int], Frozen()] = Field(default_factory=set)
    frozen_map: Annotated[dict[str, int], Frozen()] = Field(default_factory=dict)

    @field_validator("frozen_list", mode="before")
    @classmethod
    def _coerce_flist(cls, v: object) -> object:
        return v if v is not None else []

    @field_validator("frozen_set", mode="before")
    @classmethod
    def _coerce_fset(cls, v: object) -> object:
        return v if v is not None else set()

    @field_validator("frozen_map", mode="before")
    @classmethod
    def _coerce_fmap(cls, v: object) -> object:
        return v if v is not None else {}

    @field_validator("time_val", mode="before")
    @classmethod
    def _coerce_time(cls, v: object) -> object:
        return _coerce_cql_time(v)

    class Settings:
        name = "it_sync_extended_types"
        keyspace = "test_ks"


class AsyncExtendedTypes(AsyncDocument):
    """Async counterpart of SyncExtendedTypes."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    big_val: Annotated[int, BigInt()] = 0
    small_val: Annotated[int, SmallInt()] = 0
    tiny_val: Annotated[int, TinyInt()] = 0
    var_val: Annotated[int, VarInt()] = 0
    dbl_val: Annotated[float, Double()] = 0.0
    ascii_val: Annotated[str, Ascii()] = ""
    timeuuid_val: Annotated[UUID | None, TimeUUID()] = None
    time_val: dt_time | None = None
    frozen_list: Annotated[list[str], Frozen()] = Field(default_factory=list)
    frozen_set: Annotated[set[int], Frozen()] = Field(default_factory=set)
    frozen_map: Annotated[dict[str, int], Frozen()] = Field(default_factory=dict)

    @field_validator("frozen_list", mode="before")
    @classmethod
    def _coerce_flist(cls, v: object) -> object:
        return v if v is not None else []

    @field_validator("frozen_set", mode="before")
    @classmethod
    def _coerce_fset(cls, v: object) -> object:
        return v if v is not None else set()

    @field_validator("frozen_map", mode="before")
    @classmethod
    def _coerce_fmap(cls, v: object) -> object:
        return v if v is not None else {}

    @field_validator("time_val", mode="before")
    @classmethod
    def _coerce_time(cls, v: object) -> object:
        return _coerce_cql_time(v)

    class Settings:
        name = "it_async_extended_types"
        keyspace = "test_ks"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Minimum Murmur3 token value — used for token-range queries that should match
# every row (TOKEN(pk) > MIN_TOKEN covers the full ring).
MIN_MURMUR3_TOKEN = -(2**63)


async def _retry(fn, retries=5, delay=1):
    """Retry a callable (sync or async) until it returns a truthy result."""
    for attempt in range(retries):
        result = await _maybe_await(fn)
        if result:
            return result
        await asyncio.sleep(delay)
    return await _maybe_await(fn)


# ---------------------------------------------------------------------------
# Variant fixture + model/helper fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(params=["sync", "async"])
def variant(request, driver_type):
    return request.param


@pytest.fixture
def Product(variant):
    if variant == "sync":
        return SyncProduct
    return AsyncProduct


@pytest.fixture
def Review(variant):
    if variant == "sync":
        return SyncReview
    return AsyncReview


@pytest.fixture
def AllTypes(variant):
    if variant == "sync":
        return SyncAllTypes
    return AsyncAllTypes


@pytest.fixture
def Event(variant):
    if variant == "sync":
        return SyncEvent
    return AsyncEvent


@pytest.fixture
def ExtendedTypes(variant):
    if variant == "sync":
        return SyncExtendedTypes
    return AsyncExtendedTypes


@pytest.fixture
def ProductsByBrand(variant):
    if variant == "sync":
        return SyncProductsByBrand
    return AsyncProductsByBrand


@pytest.fixture
def execute_raw_fn(variant):
    if variant == "sync":
        from coodie.sync import execute_raw

        return execute_raw
    from coodie.aio import execute_raw

    return execute_raw


@pytest.fixture
def create_keyspace_fn(variant):
    if variant == "sync":
        from coodie.sync import create_keyspace

        return create_keyspace
    from coodie.aio import create_keyspace

    return create_keyspace


@pytest.fixture
def drop_keyspace_fn(variant):
    if variant == "sync":
        from coodie.sync import drop_keyspace

        return drop_keyspace
    from coodie.aio import drop_keyspace

    return drop_keyspace


@pytest.fixture
def QS(variant):
    """Return the QuerySet class matching the current variant."""
    if variant == "sync":
        from coodie.sync.query import QuerySet

        return QuerySet
    from coodie.aio.query import QuerySet

    return QuerySet


# ---------------------------------------------------------------------------
# Phase A migration-strategy models & fixtures
# ---------------------------------------------------------------------------


class SyncPhaseAProduct(SyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    brand: Annotated[str, Indexed()] = "Unknown"
    price: float = 0.0

    class Settings:
        name = "it_phase_a"
        keyspace = "test_ks"


class AsyncPhaseAProduct(AsyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    brand: Annotated[str, Indexed()] = "Unknown"
    price: float = 0.0

    class Settings:
        name = "it_phase_a"
        keyspace = "test_ks"


class SyncPhaseATTL(SyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""

    class Settings:
        name = "it_phase_a_ttl"
        keyspace = "test_ks"
        __default_ttl__ = 7200


class AsyncPhaseATTL(AsyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""

    class Settings:
        name = "it_phase_a_ttl"
        keyspace = "test_ks"
        __default_ttl__ = 7200


class SyncPhaseADrift(SyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""

    class Settings:
        name = "it_phase_a_drift"
        keyspace = "test_ks"


class AsyncPhaseADrift(AsyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""

    class Settings:
        name = "it_phase_a_drift"
        keyspace = "test_ks"


class SyncPhaseAIndex(SyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""

    class Settings:
        name = "it_phase_a_idx"
        keyspace = "test_ks"


class AsyncPhaseAIndex(AsyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""

    class Settings:
        name = "it_phase_a_idx"
        keyspace = "test_ks"


class SyncPhaseADryRun(SyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""

    class Settings:
        name = "it_phase_a_drytest"
        keyspace = "test_ks"


class AsyncPhaseADryRun(AsyncDocument):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""

    class Settings:
        name = "it_phase_a_drytest"
        keyspace = "test_ks"


@pytest.fixture
def PhaseAProduct(variant):
    if variant == "sync":
        return SyncPhaseAProduct
    return AsyncPhaseAProduct


@pytest.fixture
def PhaseATTL(variant):
    if variant == "sync":
        return SyncPhaseATTL
    return AsyncPhaseATTL


@pytest.fixture
def PhaseADrift(variant):
    if variant == "sync":
        return SyncPhaseADrift
    return AsyncPhaseADrift


@pytest.fixture
def PhaseAIndex(variant):
    if variant == "sync":
        return SyncPhaseAIndex
    return AsyncPhaseAIndex


@pytest.fixture
def PhaseADryRun(variant):
    if variant == "sync":
        return SyncPhaseADryRun
    return AsyncPhaseADryRun


# ---------------------------------------------------------------------------
# Container mutation models
# ---------------------------------------------------------------------------


class SyncContainerDoc(SyncDocument):
    """Document with list, set, and map columns for collection mutation tests."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    items: list[str] = Field(default_factory=list)
    tags: set[str] = Field(default_factory=set)
    meta: dict[str, str] = Field(default_factory=dict)

    @field_validator("items", mode="before")
    @classmethod
    def _coerce_items(cls, v: object) -> object:
        return v if v is not None else []

    @field_validator("tags", mode="before")
    @classmethod
    def _coerce_tags(cls, v: object) -> object:
        return v if v is not None else set()

    @field_validator("meta", mode="before")
    @classmethod
    def _coerce_meta(cls, v: object) -> object:
        return v if v is not None else {}

    class Settings:
        name = "it_sync_container_doc"
        keyspace = "test_ks"


class AsyncContainerDoc(AsyncDocument):
    """Async counterpart of SyncContainerDoc."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    items: list[str] = Field(default_factory=list)
    tags: set[str] = Field(default_factory=set)
    meta: dict[str, str] = Field(default_factory=dict)

    @field_validator("items", mode="before")
    @classmethod
    def _coerce_items(cls, v: object) -> object:
        return v if v is not None else []

    @field_validator("tags", mode="before")
    @classmethod
    def _coerce_tags(cls, v: object) -> object:
        return v if v is not None else set()

    @field_validator("meta", mode="before")
    @classmethod
    def _coerce_meta(cls, v: object) -> object:
        return v if v is not None else {}

    class Settings:
        name = "it_async_container_doc"
        keyspace = "test_ks"


@pytest.fixture
def ContainerDoc(variant):
    if variant == "sync":
        return SyncContainerDoc
    return AsyncContainerDoc


# ---------------------------------------------------------------------------
# Counter column models
# ---------------------------------------------------------------------------


class SyncPageView(SyncCounterDocument):
    """Sync counter document for integration tests."""

    url: Annotated[str, PrimaryKey()]
    view_count: Annotated[int, Counter()] = 0
    unique_visitors: Annotated[int, Counter()] = 0

    @field_validator("view_count", "unique_visitors", mode="before")
    @classmethod
    def _coerce_counter(cls, v: object) -> object:
        return v if v is not None else 0

    class Settings:
        name = "it_sync_page_views"
        keyspace = "test_ks"


class AsyncPageView(AsyncCounterDocument):
    """Async counter document for integration tests."""

    url: Annotated[str, PrimaryKey()]
    view_count: Annotated[int, Counter()] = 0
    unique_visitors: Annotated[int, Counter()] = 0

    @field_validator("view_count", "unique_visitors", mode="before")
    @classmethod
    def _coerce_counter(cls, v: object) -> object:
        return v if v is not None else 0

    class Settings:
        name = "it_async_page_views"
        keyspace = "test_ks"


@pytest.fixture
def PageView(variant):
    if variant == "sync":
        return SyncPageView
    return AsyncPageView


# ---------------------------------------------------------------------------
# Static column models
# ---------------------------------------------------------------------------


class SyncSensorReading(SyncDocument):
    """Document with a static column for sharing data across clustering rows."""

    sensor_id: Annotated[str, PrimaryKey()]
    reading_time: Annotated[str, ClusteringKey()]
    sensor_name: Annotated[str, Static()] = ""
    value: float = 0.0

    class Settings:
        name = "it_sync_sensor_readings"
        keyspace = "test_ks"


class AsyncSensorReading(AsyncDocument):
    """Async counterpart of SyncSensorReading."""

    sensor_id: Annotated[str, PrimaryKey()]
    reading_time: Annotated[str, ClusteringKey()]
    sensor_name: Annotated[str, Static()] = ""
    value: float = 0.0

    class Settings:
        name = "it_async_sensor_readings"
        keyspace = "test_ks"


@pytest.fixture
def SensorReading(variant):
    if variant == "sync":
        return SyncSensorReading
    return AsyncSensorReading


# ---------------------------------------------------------------------------
# Polymorphic models
# ---------------------------------------------------------------------------


class SyncAnimal(SyncDocument):
    """Base polymorphic document using a discriminator column."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""
    animal_type: Annotated[str, Discriminator()] = ""

    class Settings:
        name = "it_sync_animals"
        keyspace = "test_ks"


class SyncCat(SyncAnimal):
    class Settings:
        __discriminator_value__ = "cat"


class SyncDog(SyncAnimal):
    class Settings:
        __discriminator_value__ = "dog"


class AsyncAnimal(AsyncDocument):
    """Async base polymorphic document."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""
    animal_type: Annotated[str, Discriminator()] = ""

    class Settings:
        name = "it_async_animals"
        keyspace = "test_ks"


class AsyncCat(AsyncAnimal):
    class Settings:
        __discriminator_value__ = "cat"


class AsyncDog(AsyncAnimal):
    class Settings:
        __discriminator_value__ = "dog"


@pytest.fixture
def Animal(variant):
    if variant == "sync":
        return SyncAnimal
    return AsyncAnimal


@pytest.fixture
def Cat(variant):
    if variant == "sync":
        return SyncCat
    return AsyncCat


@pytest.fixture
def Dog(variant):
    if variant == "sync":
        return SyncDog
    return AsyncDog


# ---------------------------------------------------------------------------
# TTL / Timestamp test models
# ---------------------------------------------------------------------------


class SyncTTLItem(SyncDocument):
    """Sync document with __default_ttl__ for TTL integration tests."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""
    description: str | None = None

    class Settings:
        name = "it_sync_ttl_items"
        keyspace = "test_ks"
        __default_ttl__ = 2


class AsyncTTLItem(AsyncDocument):
    """Async document with __default_ttl__ for TTL integration tests."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""
    description: str | None = None

    class Settings:
        name = "it_async_ttl_items"
        keyspace = "test_ks"
        __default_ttl__ = 2


@pytest.fixture
def TTLItem(variant):
    if variant == "sync":
        return SyncTTLItem
    return AsyncTTLItem


# ---------------------------------------------------------------------------
# Custom index name models
# ---------------------------------------------------------------------------


class SyncCustomIdxProduct(SyncDocument):
    """Document with a custom-named secondary index."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""
    brand: Annotated[str, Indexed(index_name="my_sync_custom_idx")] = "Unknown"

    class Settings:
        name = "it_sync_custom_idx"
        keyspace = "test_ks"


class AsyncCustomIdxProduct(AsyncDocument):
    """Async counterpart with a custom-named secondary index."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str = ""
    brand: Annotated[str, Indexed(index_name="my_async_custom_idx")] = "Unknown"

    class Settings:
        name = "it_async_custom_idx"
        keyspace = "test_ks"


@pytest.fixture
def CustomIdxProduct(variant):
    if variant == "sync":
        return SyncCustomIdxProduct
    return AsyncCustomIdxProduct
