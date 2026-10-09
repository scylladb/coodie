"""DDL / sync_table benchmarks — coodie vs cqlengine."""

import uuid

import pytest

# ---------------------------------------------------------------------------
# sync_table — create (first call)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="sync-table-create")
def test_cqlengine_sync_table_create(benchmark, bench_env):
    from cassandra.cqlengine import columns
    from cassandra.cqlengine.management import sync_table
    from cassandra.cqlengine.models import Model

    class CqlTempSchema(Model):
        __table_name__ = f"bench_temp_cql_{uuid.uuid4().hex[:8]}"
        __keyspace__ = "bench_ks"
        id = columns.UUID(primary_key=True, default=uuid.uuid4)
        name = columns.Text()

    def _sync():
        sync_table(CqlTempSchema, keyspaces=["bench_ks"])

    benchmark(_sync)


@pytest.mark.benchmark(group="sync-table-create")
def test_coodie_sync_table_create(benchmark, bench_env):
    from typing import Annotated

    from pydantic import Field

    from coodie.fields import PrimaryKey
    from coodie.sync.document import Document

    table_name = f"bench_temp_coodie_{uuid.uuid4().hex[:8]}"

    class CoodieTempSchema(Document):
        id: Annotated[uuid.UUID, PrimaryKey()] = Field(default_factory=uuid.uuid4)
        name: str = ""

        class Settings:
            name = table_name
            keyspace = "bench_ks"

    def _sync():
        CoodieTempSchema.sync_table()

    benchmark(_sync)


# ---------------------------------------------------------------------------
# sync_table — idempotent (no-op, 2nd call)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="sync-table-noop")
def test_cqlengine_sync_table_noop(benchmark, bench_env):
    from cassandra.cqlengine.management import sync_table

    from benchmarks.models_cqlengine import CqlProduct

    def _sync():
        sync_table(CqlProduct, keyspaces=["bench_ks"])

    benchmark(_sync)


@pytest.mark.benchmark(group="sync-table-noop")
def test_coodie_sync_table_noop(benchmark, bench_env):
    from benchmarks.models_coodie import CoodieProduct

    def _sync():
        CoodieProduct.sync_table()

    benchmark(_sync)
