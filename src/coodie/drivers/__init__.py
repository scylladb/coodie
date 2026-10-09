from __future__ import annotations

import ssl as _ssl
from typing import Any

from coodie.drivers.base import AbstractDriver
from coodie.drivers.lazy import LazyDriver
from coodie.exceptions import ConfigurationError

_registry: dict[str, AbstractDriver] = {}
_default_driver_name: str | None = None


def _python_rs_contact_points(hosts: list[str], port: str | int | None) -> tuple[str | tuple[str, int], ...]:
    if port is None:
        return tuple(hosts)
    return tuple((host, int(port)) for host in hosts)


def _build_python_rs_session_builder(session_builder_cls: Any, hosts: list[str], kwargs: dict[str, Any]) -> Any:
    """Build a python-rs SessionBuilder via fluent API.

    Extracts optional ``port`` from ``kwargs``, forwards remaining kwargs to
    ``SessionBuilder(...)``, then applies normalized contact points.
    """
    builder_kwargs = dict(kwargs)
    port = builder_kwargs.pop("port", None)
    builder = session_builder_cls(**builder_kwargs)
    builder = builder.contact_points(_python_rs_contact_points(hosts, port))
    return builder


def register_driver(
    name: str,
    driver: AbstractDriver,
    default: bool = False,
) -> None:
    global _default_driver_name
    _registry[name] = driver
    if default or _default_driver_name is None:
        _default_driver_name = name


def get_driver(name: str | None = None) -> AbstractDriver:
    target = name or _default_driver_name
    if target is None or target not in _registry:
        raise ConfigurationError("No coodie driver registered. Call init_coodie() first.")
    return _registry[target]


def init_coodie(
    hosts: list[str] | None = None,
    session: Any | None = None,
    keyspace: str | None = None,
    driver_type: str = "scylla",
    name: str = "default",
    ssl_context: _ssl.SSLContext | None = None,
    lazy: bool = False,
    compression: str | bool | None = None,
    speculative_execution_policy: Any | None = None,
    **kwargs: Any,
) -> AbstractDriver:
    """Create a driver, register it under *name*, and make it the default.

    This is the synchronous entry point (re-exported as
    ``coodie.sync.init_coodie``).  It can be called from plain sync code;
    for ``driver_type="acsylla"`` and ``"python-rs"`` with ``hosts=``, the
    session is created on a dedicated background event loop, so the returned
    driver supports both the sync and async APIs (the "sync bridge").

    Args:
        hosts: Contact points.  For ``"scylla"``/``"cassandra"`` defaults to
            ``["127.0.0.1"]`` when neither *hosts* nor *session* is given.
            For ``"acsylla"`` and ``"python-rs"`` either *hosts* or
            *session* is required.
        session: Pre-created driver session to wrap (bring your own
            session).  When given, *hosts* and ``**kwargs`` are ignored.
            An acsylla session passed here is not on the background loop:
            ``AcsyllaDriver`` emits a ``UserWarning`` and sync calls may hang.
        keyspace: Default keyspace.  Also passed to ``Cluster.connect()``
            (scylla/cassandra) and ``create_session()`` (acsylla).
        driver_type: ``"scylla"`` (default), ``"cassandra"``, ``"acsylla"``
            or ``"python-rs"``.  ``"scylla"`` and ``"cassandra"`` both use
            ``CassandraDriver``; they differ only in which package provides
            the ``cassandra`` module.
        name: Registry name, used with ``get_driver(name)`` for multi-cluster
            setups.  The new driver always becomes the default.
        ssl_context: ``ssl.SSLContext`` forwarded to ``Cluster()``.
            scylla/cassandra only.
        lazy: When ``True`` (and no *session*), return a ``LazyDriver`` that
            connects on first use.  scylla/cassandra only.  *compression*
            and *speculative_execution_policy* are not applied in lazy mode;
            pass them via ``**kwargs`` instead.
        compression: Forwarded to ``Cluster(compression=...)``.
            scylla/cassandra only, non-lazy.
        speculative_execution_policy: Forwarded to
            ``Cluster(speculative_execution_policy=...)``.  scylla/cassandra
            only, non-lazy.
        **kwargs: Extra connection options, used only when coodie creates the
            session: ``Cluster(hosts, **kwargs)`` for scylla/cassandra,
            ``acsylla.create_cluster(hosts, **kwargs)`` for acsylla, and
            ``SessionBuilder(**kwargs)`` for python-rs (where ``port`` is
            popped and applied to every contact point instead).

    Returns:
        The registered driver.

    Raises:
        ConfigurationError: Unknown *driver_type*, or acsylla/python-rs
            without *hosts* or *session*.
        ImportError: The selected driver package is not installed.
    """
    if driver_type == "acsylla":
        from coodie.drivers.acsylla import AcsyllaDriver

        if session is None and hosts is not None:
            driver: AbstractDriver = AcsyllaDriver.connect_sync(hosts, keyspace=keyspace, **kwargs)
        elif session is None:
            raise ConfigurationError(
                "AcsyllaDriver requires hosts or a pre-created acsylla session. "
                "Pass hosts= or session=, or use init_coodie_async() with hosts."
            )
        else:
            driver = AcsyllaDriver(session=session, default_keyspace=keyspace)
    elif driver_type == "python-rs":
        from coodie.drivers.python_rs import PythonRsDriver

        if session is None and hosts is not None:
            try:
                from scylla import SessionBuilder  # type: ignore[import-untyped]
            except ImportError as exc:
                raise ImportError(
                    "python-rs-driver is required for PythonRsDriver. "
                    "Build from source: https://github.com/scylladb-zpp-2025-python-rs-driver/python-rs-driver"
                ) from exc

            async def _make_session() -> Any:
                builder = _build_python_rs_session_builder(SessionBuilder, hosts, kwargs)
                return await builder.connect()

            driver = PythonRsDriver.connect(
                session_factory=_make_session,
                default_keyspace=keyspace,
            )
        elif session is None:
            raise ConfigurationError(
                "PythonRsDriver requires a pre-created python-rs-driver session or hosts. Pass session= or hosts=."
            )
        else:
            driver = PythonRsDriver(session=session, default_keyspace=keyspace)
    elif driver_type in ("scylla", "cassandra"):
        if lazy and session is None:
            from coodie.drivers.lazy import LazyDriver

            driver = LazyDriver(hosts=hosts, keyspace=keyspace, ssl_context=ssl_context, kwargs=kwargs)
        else:
            from coodie.drivers.cassandra import CassandraDriver

            if session is None:
                try:
                    from cassandra.cluster import Cluster  # type: ignore[import-untyped]
                except ImportError as exc:
                    raise ImportError(
                        "cassandra-driver (or scylla-driver) is required for CassandraDriver. "
                        "Install it with: pip install scylla-driver"
                    ) from exc
                if ssl_context is not None:
                    kwargs["ssl_context"] = ssl_context
                if compression is not None:
                    kwargs["compression"] = compression
                if speculative_execution_policy is not None:
                    kwargs["speculative_execution_policy"] = speculative_execution_policy
                cluster = Cluster(hosts or ["127.0.0.1"], **kwargs)
                session = cluster.connect(keyspace)

            driver = CassandraDriver(session=session, default_keyspace=keyspace)
    else:
        raise ConfigurationError(
            f"Unknown driver_type={driver_type!r}. Supported: 'scylla', 'cassandra', 'acsylla', 'python-rs'."
        )

    register_driver(name, driver, default=True)
    return driver


async def init_coodie_async(
    hosts: list[str] | None = None,
    session: Any | None = None,
    keyspace: str | None = None,
    driver_type: str = "scylla",
    name: str = "default",
    ssl_context: _ssl.SSLContext | None = None,
    ssl_enabled: bool | None = None,
    ssl_trusted_cert: str | None = None,
    ssl_cert: str | None = None,
    ssl_private_key: str | None = None,
    ssl_verify_flags: int | None = None,
    **kwargs: Any,
) -> AbstractDriver:
    """Async variant of :func:`init_coodie` (re-exported as ``coodie.aio.init_coodie``).

    Use it from inside a running event loop.  For ``"acsylla"`` and
    ``"python-rs"`` with ``hosts=``, the session is created on a dedicated
    background loop (same as :func:`init_coodie`), so the driver works from
    both sync and async code.  With ``session=``, the driver runs the async
    API directly on the caller's loop.  Every other case
    (``"scylla"``/``"cassandra"``) delegates to :func:`init_coodie`, which
    connects synchronously.

    Args:
        hosts: Contact points.  See :func:`init_coodie`.
        session: Pre-created driver session to wrap.  When given, *hosts*
            and ``**kwargs`` are ignored.
        keyspace: Default keyspace.
        driver_type: ``"scylla"`` (default), ``"cassandra"``, ``"acsylla"``
            or ``"python-rs"``.
        name: Registry name.  The new driver always becomes the default.
        ssl_context: ``ssl.SSLContext`` for scylla/cassandra.
        ssl_enabled: acsylla only (with *hosts*); forwarded to
            ``acsylla.create_cluster()``.
        ssl_trusted_cert: acsylla only (with *hosts*); PEM CA certificate.
        ssl_cert: acsylla only (with *hosts*); PEM client certificate.
        ssl_private_key: acsylla only (with *hosts*); PEM client key.
        ssl_verify_flags: acsylla only (with *hosts*); certificate
            verification flags.
        **kwargs: Extra connection options, as in :func:`init_coodie`.  For
            scylla/cassandra they are passed through to :func:`init_coodie`,
            so ``lazy``, ``compression`` and ``speculative_execution_policy``
            can be given here too.

    Returns:
        The registered driver.

    Raises:
        ConfigurationError: Unknown *driver_type*, or acsylla/python-rs
            without *hosts* or *session*.
        ImportError: The selected driver package is not installed.
    """
    if driver_type == "acsylla" and session is None and hosts is not None:
        try:
            import acsylla  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError("acsylla is required for AcsyllaDriver. Install it with: pip install acsylla") from exc
        from coodie.drivers.acsylla import AcsyllaDriver

        if ssl_enabled is not None:
            kwargs["ssl_enabled"] = ssl_enabled
        if ssl_trusted_cert is not None:
            kwargs["ssl_trusted_cert"] = ssl_trusted_cert
        if ssl_cert is not None:
            kwargs["ssl_cert"] = ssl_cert
        if ssl_private_key is not None:
            kwargs["ssl_private_key"] = ssl_private_key
        if ssl_verify_flags is not None:
            kwargs["ssl_verify_flags"] = ssl_verify_flags

        async def _make_session() -> Any:
            cluster = acsylla.create_cluster(hosts, **kwargs)
            return await cluster.create_session(keyspace=keyspace)

        driver: AbstractDriver = AcsyllaDriver.connect(
            session_factory=_make_session,
            default_keyspace=keyspace,
        )
        register_driver(name, driver, default=True)
        return driver

    if driver_type == "acsylla":
        from coodie.drivers.acsylla import AcsyllaDriver

        if session is None:
            raise ConfigurationError(
                "AcsyllaDriver requires a pre-created acsylla session. "
                "Pass session= or use init_coodie_async() with hosts."
            )
        driver = AcsyllaDriver(session=session, default_keyspace=keyspace)
        register_driver(name, driver, default=True)
        return driver

    if driver_type == "python-rs" and session is None and hosts is not None:
        try:
            from scylla import SessionBuilder  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError(
                "python-rs-driver is required for PythonRsDriver. "
                "Build from source: https://github.com/scylladb-zpp-2025-python-rs-driver/python-rs-driver"
            ) from exc
        from coodie.drivers.python_rs import PythonRsDriver

        async def _make_python_rs_session() -> Any:
            builder = _build_python_rs_session_builder(SessionBuilder, hosts, kwargs)
            return await builder.connect()

        driver = PythonRsDriver.connect(
            session_factory=_make_python_rs_session,
            default_keyspace=keyspace,
        )
        register_driver(name, driver, default=True)
        return driver

    if driver_type == "python-rs":
        from coodie.drivers.python_rs import PythonRsDriver

        if session is None:
            raise ConfigurationError(
                "PythonRsDriver requires a pre-created python-rs-driver session. "
                "Pass session= or use init_coodie_async() with hosts."
            )
        driver = PythonRsDriver(session=session, default_keyspace=keyspace)
        register_driver(name, driver, default=True)
        return driver

    return init_coodie(
        hosts=hosts,
        session=session,
        keyspace=keyspace,
        driver_type=driver_type,
        name=name,
        ssl_context=ssl_context,
        **kwargs,
    )


__all__ = [
    "AbstractDriver",
    "LazyDriver",
    "get_driver",
    "init_coodie",
    "init_coodie_async",
    "register_driver",
]
