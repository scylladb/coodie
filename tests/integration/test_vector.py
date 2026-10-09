"""Integration tests for vector column support.

Requires a running ScyllaDB instance with vector (SAI) support.

Run with:
    pytest -m integration -v tests/integration/test_vector.py
"""

from __future__ import annotations

import asyncio
import contextlib
from typing import Annotated
from uuid import UUID, uuid4

import pytest
from pydantic import Field

from coodie.aio.document import Document as AsyncDocument
from coodie.exceptions import InvalidQueryError
from coodie.fields import PrimaryKey, Vector, VectorIndex
from coodie.sync.document import Document as SyncDocument
from tests.conftest import _maybe_await

pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio(loop_scope="session"),
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

DIMS = 4  # small dimension count to keep tests fast


class SyncVectorProduct(SyncDocument):
    """Sync document with a vector column for similarity search."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    embedding: Annotated[
        list[float],
        Vector(dimensions=DIMS),
        VectorIndex(similarity_function="COSINE"),
    ] = Field(default_factory=list)

    class Settings:
        name = "it_sync_vector_products"
        keyspace = "vector_ks"  # tablet-enabled keyspace for vector search


class AsyncVectorProduct(AsyncDocument):
    """Async document with a vector column for similarity search."""

    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    embedding: Annotated[
        list[float],
        Vector(dimensions=DIMS),
        VectorIndex(similarity_function="COSINE"),
    ] = Field(default_factory=list)

    class Settings:
        name = "it_async_vector_products"
        keyspace = "vector_ks"  # tablet-enabled keyspace for vector search


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def sai_capable(scylla_vector_session):
    """True if the connected database supports SAI vector indexes.

    Probes by attempting to create a minimal vector table and vector index in
    the tablet-enabled ``vector_ks`` keyspace.  Returns False for drivers that
    don't use a cassandra-driver session (acsylla, python-rs) or when the
    database server doesn't support vector indexes.
    """
    if scylla_vector_session is None:
        return False
    try:
        scylla_vector_session.execute("CREATE TABLE IF NOT EXISTS sai_probe (id uuid PRIMARY KEY, v vector<float, 1>)")
        try:
            scylla_vector_session.execute(
                "CREATE CUSTOM INDEX IF NOT EXISTS sai_probe_idx "
                "ON sai_probe (v) "
                "USING 'vector_index' "
                "WITH OPTIONS = {'similarity_function': 'COSINE'}"
            )
        except Exception:  # noqa: BLE001 - probe: any failure means SAI vector index is unsupported
            return False
        return True
    except Exception:  # noqa: BLE001 - probe: any failure means vector support is unavailable
        return False
    finally:
        with contextlib.suppress(Exception):  # best-effort probe cleanup
            scylla_vector_session.execute("DROP TABLE IF EXISTS sai_probe")


@pytest.fixture(params=["sync", "async"])
def VectorProduct(request, driver_type, sai_capable, scylla_vector_session):
    if not sai_capable:
        pytest.skip("SAI vector indexes not supported by this database/driver")
    if request.param == "sync" and driver_type in ("acsylla", "python-rs"):
        pytest.skip(f"{driver_type} is async-only — sync variant not applicable")
    if request.param == "sync":
        return SyncVectorProduct
    return AsyncVectorProduct


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestVectorIntegration:
    """Integration tests for vector column support against a real ScyllaDB."""

    async def test_sync_table_creates_vector_table(self, coodie_driver, VectorProduct) -> None:
        """sync_table should create the table with the vector column."""
        await _maybe_await(VectorProduct.sync_table)

    async def test_save_and_retrieve_vector(self, coodie_driver, VectorProduct) -> None:
        """Save a document with an embedding and retrieve it by PK."""
        await _maybe_await(VectorProduct.sync_table)
        pid = uuid4()
        vec = [0.1, 0.2, 0.3, 0.4]
        p = VectorProduct(id=pid, name="Widget", embedding=vec)
        await _maybe_await(p.save)

        fetched = await _maybe_await(VectorProduct.find_one, id=pid)
        assert fetched is not None
        assert fetched.id == pid
        # Cassandra drivers may return floats with slight rounding
        assert len(fetched.embedding) == DIMS

    async def test_ann_query_returns_results(self, coodie_driver, VectorProduct) -> None:
        """ANN query should return rows ordered by approximate similarity."""
        await _maybe_await(VectorProduct.sync_table)

        # Insert a few products with known embeddings
        products = [
            VectorProduct(id=uuid4(), name="Alpha", embedding=[1.0, 0.0, 0.0, 0.0]),
            VectorProduct(id=uuid4(), name="Beta", embedding=[0.0, 1.0, 0.0, 0.0]),
            VectorProduct(id=uuid4(), name="Gamma", embedding=[0.0, 0.0, 1.0, 0.0]),
        ]
        for p in products:
            await _maybe_await(p.save)

        # The vector-store sidecar indexes data asynchronously; retry the
        # ANN query a few times so it doesn't fail on a brief indexing lag.
        query_vec = [0.9, 0.1, 0.0, 0.0]
        last_err: Exception | None = None
        for _attempt in range(12):
            try:
                results = await _maybe_await(VectorProduct.find().order_by_ann("embedding", query_vec).limit(3).all)
                break
            except Exception as exc:  # noqa: BLE001 - retry on any indexing-lag error
                last_err = exc
                await asyncio.sleep(5)
        else:
            raise AssertionError(f"ANN query did not succeed after retries: {last_err}") from last_err
        assert len(results) >= 1
        assert all(isinstance(r, VectorProduct) for r in results)

    async def test_dimension_validation_on_save(self, coodie_driver, VectorProduct) -> None:
        """save() should raise InvalidQueryError on dimension mismatch."""
        await _maybe_await(VectorProduct.sync_table)
        p = VectorProduct(id=uuid4(), name="BadVec", embedding=[0.1, 0.2])
        with pytest.raises(InvalidQueryError, match=f"expects {DIMS} dimensions, got 2"):
            await _maybe_await(p.save)

    async def test_sync_table_creates_vector_index(self, coodie_driver, VectorProduct) -> None:
        """sync_table should emit the CREATE CUSTOM INDEX statement."""
        planned = await _maybe_await(VectorProduct.sync_table, dry_run=True)
        idx_statements = [s for s in planned if "USING 'vector_index'" in s]
        assert len(idx_statements) >= 1
        assert "COSINE" in idx_statements[0]
