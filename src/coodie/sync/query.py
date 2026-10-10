"""Synchronous QuerySet.

Un-suffixed terminal methods (``all()``, ``count()``, ...) run synchronously.
The explicit ``*_sync`` / ``*_async`` methods from
:class:`~coodie.query.BaseQuerySet` are always available too.
"""

from __future__ import annotations

from coodie._modes import pick, sync_alias
from coodie.query import BaseQuerySet, _parse_lwt_result, _snake_case

__all__ = ["QuerySet", "_parse_lwt_result", "_snake_case"]


class QuerySet(BaseQuerySet):
    """Synchronous chainable query builder (``*_async`` methods are available too)."""

    __slots__ = ()
    __coodie_mode__ = "sync"

    all = sync_alias(BaseQuerySet.all_sync)
    paged_all = sync_alias(BaseQuerySet.paged_all_sync)
    first = sync_alias(BaseQuerySet.first_sync)
    count = sync_alias(BaseQuerySet.count_sync)
    aggregate = sync_alias(BaseQuerySet.aggregate_sync)
    sum = sync_alias(BaseQuerySet.sum_sync)
    avg = sync_alias(BaseQuerySet.avg_sync)
    min = sync_alias(BaseQuerySet.min_sync)
    max = sync_alias(BaseQuerySet.max_sync)
    json = sync_alias(BaseQuerySet.json_sync)
    writetime = sync_alias(BaseQuerySet.writetime_sync)
    column_ttl = sync_alias(BaseQuerySet.column_ttl_sync)
    delete = sync_alias(BaseQuerySet.delete_sync)
    create = sync_alias(BaseQuerySet.create_sync)
    update = sync_alias(BaseQuerySet.update_sync)

    def __len__(self) -> int:
        return pick(self, "count", "sync")()
