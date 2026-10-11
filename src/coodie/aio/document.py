"""Asynchronous documents.

Un-suffixed methods (``save()``, ``get()``, ...) run asynchronously. Every model
also has the explicit ``*_sync`` / ``*_async`` methods from
:class:`~coodie.document.BaseDocument`, so the same class and instance can be
used from both sync and async code.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from coodie._modes import async_alias
from coodie.aio.query import QuerySet
from coodie.document import BaseCounterDocument, BaseDocument, BaseMaterializedView
from coodie.query import _parse_lwt_result

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["CounterDocument", "Document", "MaterializedView", "_parse_lwt_result"]


class Document(BaseDocument):
    """Base class for asynchronous coodie documents (``*_sync`` methods are available too)."""

    __coodie_mode__ = "async"
    __queryset_cls__ = QuerySet

    sync_table = async_alias(BaseDocument.sync_table_async)
    drop_table = async_alias(BaseDocument.drop_table_async)
    truncate = async_alias(BaseDocument.truncate_async)
    save = async_alias(BaseDocument.save_async)
    save_json = async_alias(BaseDocument.save_json_async)
    insert = async_alias(BaseDocument.insert_async)
    delete_columns = async_alias(BaseDocument.delete_columns_async)
    delete = async_alias(BaseDocument.delete_async)
    update = async_alias(BaseDocument.update_async)

    # Aliases that return the model are stubbed for type checkers, so they
    # return the subclass rather than BaseDocument.
    if TYPE_CHECKING:

        @classmethod
        async def create(cls, **kwargs: Any) -> Self: ...
        @classmethod
        async def find_one(cls, **kwargs: Any) -> Self | None: ...
        @classmethod
        async def get(cls, **kwargs: Any) -> Self: ...

    else:
        create = async_alias(BaseDocument.create_async)
        find_one = async_alias(BaseDocument.find_one_async)
        get = async_alias(BaseDocument.get_async)

    @classmethod
    def find(cls, **kwargs: Any) -> QuerySet:
        """Return a QuerySet filtered by *kwargs*."""
        return super().find(**kwargs)


class CounterDocument(BaseCounterDocument, Document):
    """Base class for asynchronous counter-column documents.

    Counter tables only support increment/decrement operations.
    ``save()`` and ``insert()`` are forbidden.
    """

    increment = async_alias(BaseCounterDocument.increment_async)
    decrement = async_alias(BaseCounterDocument.decrement_async)


class MaterializedView(BaseMaterializedView, Document):
    """Base class for asynchronous materialized view documents (read-only).

    See :class:`~coodie.document.BaseMaterializedView` for the ``Settings`` it needs.
    """

    sync_view = async_alias(BaseMaterializedView.sync_view_async)
    drop_view = async_alias(BaseMaterializedView.drop_view_async)
