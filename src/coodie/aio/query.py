"""Asynchronous QuerySet.

Un-suffixed terminal methods (``all()``, ``count()``, ...) run asynchronously.
The explicit ``*_sync`` / ``*_async`` methods from
:class:`~coodie.query.BaseQuerySet` are always available too.
"""

from __future__ import annotations

from coodie._modes import async_alias
from coodie.query import BaseQuerySet, _parse_lwt_result, _snake_case

__all__ = ["QuerySet", "_parse_lwt_result", "_snake_case"]


class QuerySet(BaseQuerySet):
    """Asynchronous chainable query builder (``*_sync`` methods are available too)."""

    __slots__ = ()
    __coodie_mode__ = "async"

    all = async_alias(BaseQuerySet.all_async)
    paged_all = async_alias(BaseQuerySet.paged_all_async)
    first = async_alias(BaseQuerySet.first_async)
    count = async_alias(BaseQuerySet.count_async)
    aggregate = async_alias(BaseQuerySet.aggregate_async)
    sum = async_alias(BaseQuerySet.sum_async)
    avg = async_alias(BaseQuerySet.avg_async)
    min = async_alias(BaseQuerySet.min_async)
    max = async_alias(BaseQuerySet.max_async)
    json = async_alias(BaseQuerySet.json_async)
    writetime = async_alias(BaseQuerySet.writetime_async)
    column_ttl = async_alias(BaseQuerySet.column_ttl_async)
    delete = async_alias(BaseQuerySet.delete_async)
    create = async_alias(BaseQuerySet.create_async)
    update = async_alias(BaseQuerySet.update_async)
