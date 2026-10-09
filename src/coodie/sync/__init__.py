from __future__ import annotations

from typing import Any

from coodie.batch import BatchQuery
from coodie.drivers import init_coodie
from coodie.sync.document import CounterDocument, Document, MaterializedView
from coodie.sync.query import QuerySet


def execute_raw(stmt: str, params: list[Any] | None = None) -> list[dict[str, Any]]:
    """Execute a raw CQL statement synchronously.

    Example::

        from coodie.sync import execute_raw

        rows = execute_raw("SELECT * FROM my_ks.users WHERE id = ?", [some_id])
        for row in rows:
            print(row["name"])
    """
    from coodie.drivers import get_driver

    return get_driver().execute(stmt, params or [])


def create_keyspace(
    keyspace: str,
    replication_factor: int = 1,
    strategy: str = "SimpleStrategy",
    dc_replication_map: dict[str, int] | None = None,
    connection: str | None = None,
) -> None:
    """Create a keyspace if it does not exist (synchronous).

    For ``NetworkTopologyStrategy``, pass *dc_replication_map* as a dict
    mapping data-centre names to replication factors::

        create_keyspace("my_ks", dc_replication_map={"dc1": 3, "dc2": 2})

    For ``SimpleStrategy`` (the default), specify *replication_factor*::

        create_keyspace("my_ks", replication_factor=3)

    Use *connection* to target a named driver registered via
    ``init_coodie(name=...)``.  Defaults to the default driver.
    """
    from coodie.cql_builder import build_create_keyspace
    from coodie.drivers import get_driver

    cql = build_create_keyspace(
        keyspace,
        replication_factor=replication_factor,
        strategy=strategy,
        dc_replication_map=dc_replication_map,
    )
    get_driver(name=connection).execute(cql, [])


def drop_keyspace(
    keyspace: str,
    connection: str | None = None,
) -> None:
    """Drop a keyspace if it exists (synchronous).

    Use *connection* to target a named driver registered via
    ``init_coodie(name=...)``.  Defaults to the default driver.

    Example::

        drop_keyspace("my_ks")
    """
    from coodie.cql_builder import build_drop_keyspace
    from coodie.drivers import get_driver

    cql = build_drop_keyspace(keyspace)
    get_driver(name=connection).execute(cql, [])


__all__ = [
    "BatchQuery",
    "CounterDocument",
    "Document",
    "MaterializedView",
    "QuerySet",
    "create_keyspace",
    "drop_keyspace",
    "execute_raw",
    "init_coodie",
]
