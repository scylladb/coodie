"""LazyDocument — defers Pydantic parsing until field access."""

from __future__ import annotations

from typing import Any


class LazyDocument:
    """Proxy that defers Pydantic ``model_validate()`` until a field is accessed.

    Returned by ``QuerySet.all(lazy=True)``.  The raw row dict from the
    database is stored and only parsed into a full Document on first
    attribute access, giving near-zero construction cost for rows that are
    never inspected (common in exists-checks, pagination cursors and
    status dashboards).
    """

    __slots__ = ("_doc_cls", "_parsed", "_raw_data")

    def __init__(self, doc_cls: type, raw_data: dict[str, Any]) -> None:
        self._doc_cls = doc_cls
        self._raw_data = raw_data
        self._parsed: Any = None

    # ------------------------------------------------------------------

    def _resolve(self) -> Any:
        """Force parsing and return the full Document instance."""
        parsed = self._parsed
        if parsed is None:
            from coodie.types import _collection_fields

            coll = _collection_fields(self._doc_cls)
            if coll:
                raw = self._raw_data
                for key, factory in coll.items():
                    if key in raw and raw[key] is None:
                        raw[key] = factory()
            parsed = self._doc_cls.model_validate(self._raw_data)
            self._parsed = parsed
        return parsed

    def __getattr__(self, name: str) -> Any:
        return getattr(self._resolve(), name)

    def __repr__(self) -> str:
        if self._parsed is not None:
            return f"LazyDocument({self._parsed!r})"
        return f"LazyDocument({self._doc_cls.__name__}, parsed=False)"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LazyDocument):
            return self._resolve() == other._resolve()
        return self._resolve() == other
