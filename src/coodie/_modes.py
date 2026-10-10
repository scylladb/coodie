"""Plumbing shared by the sync and async APIs.

Every I/O method exists as an explicit ``<name>_sync`` / ``<name>_async`` twin
on the shared base classes. ``coodie.sync`` and ``coodie.aio`` add the
un-suffixed ``<name>`` as an alias for one of the twins (the class's default
mode).
"""

from __future__ import annotations

import asyncio
import contextvars
import functools
import os
import sys
import types
import warnings
from collections.abc import Callable
from typing import Any, TypeVar

from coodie.exceptions import BlockingCallWarning

F = TypeVar("F", bound=Callable[..., Any])

_PKG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "")

# True while a coodie alias (e.g. ``save()``) is running its twin, so the twin
# knows it was not called directly.
_via_alias: contextvars.ContextVar[bool] = contextvars.ContextVar("coodie_via_alias", default=False)


def _user_stacklevel() -> int:
    """``stacklevel`` for a warning raised by the caller, pointing at the first frame outside coodie."""
    frame = sys._getframe(1)
    level = 1
    while frame.f_back is not None and frame.f_code.co_filename.startswith(_PKG_DIR):
        frame = frame.f_back
        level += 1
    return level


_LIBRARY_MODULES = ("coodie.", "pydantic.", "builtins")


@functools.lru_cache(maxsize=4096)
def _is_user_defined(cls: type, name: str) -> bool:
    """True when the class that provides *name* on *cls* is the user's, not coodie's."""
    for klass in cls.__mro__:
        if name in klass.__dict__:
            return not klass.__module__.startswith(_LIBRARY_MODULES)
    return False


def _alias(twin: F, *, is_async: bool) -> F:
    name = twin.__name__
    is_classmethod = isinstance(twin, types.MethodType)
    func: Any = twin.__func__ if is_classmethod else twin  # type: ignore[attr-defined]

    if is_async:

        @functools.wraps(func)
        async def alias(self: Any, *args: Any, **kwargs: Any) -> Any:
            token = _via_alias.set(True)
            try:
                return await getattr(self, name)(*args, **kwargs)
            finally:
                _via_alias.reset(token)

    else:

        @functools.wraps(func)
        def alias(self: Any, *args: Any, **kwargs: Any) -> Any:
            token = _via_alias.set(True)
            try:
                return getattr(self, name)(*args, **kwargs)
            finally:
                _via_alias.reset(token)

    alias.__name__ = alias.__qualname__ = name.rsplit("_", 1)[0]
    return classmethod(alias) if is_classmethod else alias  # type: ignore[return-value]


def sync_alias(twin: F) -> F:
    """Un-suffixed alias that delegates to the ``*_sync`` twin through ``self``, so overrides apply."""
    return _alias(twin, is_async=False)


def async_alias(twin: F) -> F:
    """Un-suffixed alias that delegates to the ``*_async`` twin through ``self``, so overrides apply."""
    return _alias(twin, is_async=True)


def pick(obj: Any, name: str, mode: str) -> Any:
    """Bound method coodie uses internally to run *name* in *mode*.

    If the model overrides the un-suffixed alias and *mode* is its default
    mode, the override is used, matching how ``create()`` called ``save()``
    before the explicit twins existed.
    """
    cls = obj if isinstance(obj, type) else type(obj)
    if mode == getattr(cls, "__coodie_mode__", None) and _is_user_defined(cls, name):
        return getattr(obj, name)
    return getattr(obj, f"{name}_{mode}")


def warn_if_blocking(cls: type) -> None:
    """Warn when a blocking query runs inside an event loop on an async-default model.

    Called once per executed statement, so a composite call like ``get_sync()``
    warns once. Sync-default models never warn (unchanged behaviour).
    """
    if getattr(cls, "__coodie_mode__", None) != "async":
        return
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    warnings.warn(
        f"Synchronous {cls.__name__} query inside a running event loop blocks it; use the *_async method instead.",
        BlockingCallWarning,
        stacklevel=_user_stacklevel(),
    )


def check_override(cls: type, name: str, mode: str) -> None:
    """Warn when a twin is called directly while the model overrides the un-suffixed alias.

    The direct call would skip that override. Code that only uses the
    un-suffixed names never triggers this.
    """
    if _via_alias.get() or not _is_user_defined(cls, name) or _is_user_defined(cls, f"{name}_{mode}"):
        return
    override = getattr(cls, name)
    if sys._getframe(2).f_code is getattr(getattr(override, "__func__", override), "__code__", None):
        return  # the override itself delegating to the twin
    warnings.warn(
        f"{cls.__name__} overrides {name}() but {name}_{mode}() was called directly, which skips that "
        f"override. Override {name}_sync() and {name}_async() instead.",
        UserWarning,
        stacklevel=_user_stacklevel(),
    )
