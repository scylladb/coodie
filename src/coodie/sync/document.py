"""Synchronous documents.

Un-suffixed methods (``save()``, ``get()``, ...) run synchronously. Every model
also has the explicit ``*_sync`` / ``*_async`` methods from
:class:`~coodie.document.BaseDocument`, so the same class and instance can be
used from both sync and async code.
"""

from __future__ import annotations

from typing import Any

from coodie._modes import sync_alias
from coodie.document import BaseCounterDocument, BaseDocument, BaseMaterializedView
from coodie.query import _parse_lwt_result
from coodie.sync.query import QuerySet

__all__ = ["CounterDocument", "Document", "MaterializedView", "_parse_lwt_result"]


class Document(BaseDocument):
    """Base class for synchronous coodie documents (``*_async`` methods are available too)."""

    __coodie_mode__ = "sync"
    __queryset_cls__ = QuerySet

    sync_table = sync_alias(BaseDocument.sync_table_sync)
    drop_table = sync_alias(BaseDocument.drop_table_sync)
    truncate = sync_alias(BaseDocument.truncate_sync)
    create = sync_alias(BaseDocument.create_sync)
    save = sync_alias(BaseDocument.save_sync)
    save_json = sync_alias(BaseDocument.save_json_sync)
    insert = sync_alias(BaseDocument.insert_sync)
    delete_columns = sync_alias(BaseDocument.delete_columns_sync)
    delete = sync_alias(BaseDocument.delete_sync)
    update = sync_alias(BaseDocument.update_sync)
    find_one = sync_alias(BaseDocument.find_one_sync)
    get = sync_alias(BaseDocument.get_sync)

    @classmethod
    def find(cls, **kwargs: Any) -> QuerySet:
        """Return a QuerySet filtered by *kwargs*."""
        return super().find(**kwargs)


class CounterDocument(BaseCounterDocument, Document):
    """Base class for synchronous counter-column documents.

    Counter tables only support increment/decrement operations.
    ``save()`` and ``insert()`` are forbidden.
    """

    increment = sync_alias(BaseCounterDocument.increment_sync)
    decrement = sync_alias(BaseCounterDocument.decrement_sync)


class MaterializedView(BaseMaterializedView, Document):
    """Base class for synchronous materialized view documents (read-only).

    See :class:`~coodie.document.BaseMaterializedView` for the ``Settings`` it needs.
    """

    sync_view = sync_alias(BaseMaterializedView.sync_view_sync)
    drop_view = sync_alias(BaseMaterializedView.drop_view_sync)
