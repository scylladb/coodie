"""Asynchronous QuerySet.

Un-suffixed terminal methods (``all()``, ``count()``, ...) run asynchronously.
The explicit ``*_sync`` / ``*_async`` methods from
:class:`~coodie.query.BaseQuerySet` are always available too.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from coodie._modes import async_alias
from coodie.query import BaseQuerySet, _parse_lwt_result, _snake_case

if TYPE_CHECKING:
    from coodie.aio.document import Document
    from coodie.lazy import LazyDocument

__all__ = ["QuerySet", "_parse_lwt_result", "_snake_case"]


class QuerySet(BaseQuerySet):
    """Asynchronous chainable query builder (``*_sync`` methods are available too)."""

    __slots__ = ()
    __coodie_mode__ = "async"

    paged_all = async_alias(BaseQuerySet.paged_all_async)
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

    # Stubbed for type checkers, so results are typed as documents (not Any).
    if TYPE_CHECKING:

        async def all(self, *, lazy: bool = False) -> list[Document] | list[LazyDocument] | list[tuple[Any, ...]]: ...
        async def first(self) -> Document | None: ...

    else:
        all = async_alias(BaseQuerySet.all_async)
        first = async_alias(BaseQuerySet.first_async)
