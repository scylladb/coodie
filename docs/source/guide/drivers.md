# Drivers & Initialization

coodie talks to Cassandra and ScyllaDB through a pluggable driver layer.
You initialize the connection with `init_coodie()`, and coodie takes
care of the rest.

## Quick Start

The simplest way to connect — point at your cluster and go:

```python
from coodie.sync import init_coodie

driver = init_coodie(
    hosts=["127.0.0.1"],
    keyspace="my_keyspace",
)
```

For async applications:

```python
from coodie.aio import init_coodie

driver = await init_coodie(
    hosts=["127.0.0.1"],
    keyspace="my_keyspace",
)
```

## Supported Drivers

coodie ships with three driver implementations:

| Driver | Backend | Protocol | Best For |
|--------|---------|----------|----------|
| `CassandraDriver` | `cassandra-driver` or `scylla-driver` | CQL native protocol | General use, sync and async |
| `AcsyllaDriver` | `acsylla` | CQL native protocol (Cython) | High-performance async workloads |
| `PythonRsDriver` | `python-rs-driver` | CQL native protocol (Rust, via PyO3) | Experimental Rust-backed async driver |

### scylla-driver (Default)

The default `driver_type="scylla"` uses `scylla-driver` (a fork of
`cassandra-driver` optimized for ScyllaDB, fully compatible with
Cassandra):

```python
init_coodie(
    hosts=["node1", "node2", "node3"],
    keyspace="my_ks",
    driver_type="scylla",  # default — can be omitted
)
```

Install:

```bash
pip install scylla-driver
```

### cassandra-driver

If you prefer the DataStax `cassandra-driver`:

```python
init_coodie(
    hosts=["node1", "node2"],
    keyspace="my_ks",
    driver_type="cassandra",
)
```

Install:

```bash
pip install cassandra-driver
```

```{note}
`driver_type="scylla"` and `driver_type="cassandra"` both use the
`CassandraDriver` class internally. The only difference is which Python
package provides the `cassandra` module. Both work with Cassandra and
ScyllaDB clusters.
```

### acsylla (Async)

For maximum async performance, use `acsylla` — a Cython-based ScyllaDB
driver. It works with both `coodie.aio.init_coodie()` and
`coodie.sync.init_coodie()` (see [Sync Bridge](#sync-bridge)):

```python
from coodie.aio import init_coodie

driver = await init_coodie(
    hosts=["node1", "node2"],
    keyspace="my_ks",
    driver_type="acsylla",
)
```

Install:

```bash
pip install acsylla
```

Extra keyword arguments are forwarded to `acsylla.create_cluster(hosts, **kwargs)`.

### python-rs-driver (Async, Experimental)

[python-rs-driver](https://github.com/scylladb-zpp-2025-python-rs-driver/python-rs-driver)
wraps the Rust [scylla-rust-driver](https://github.com/scylladb/scylla-rust-driver)
via PyO3. It is async-native and, like acsylla, works from both the sync
and async APIs through the [Sync Bridge](#sync-bridge):

```python
from coodie.aio import init_coodie

driver = await init_coodie(
    hosts=["node1", "node2"],
    keyspace="my_ks",
    driver_type="python-rs",
    port=9042,  # optional; applied to every contact point
)
```

Extra keyword arguments are forwarded to `SessionBuilder(**kwargs)`,
except `port`, which coodie applies to each host when building the
contact points.

Install: python-rs-driver is **not published on PyPI** and is built from
source, so you need a Rust toolchain (`cargo`). Its Python package is
named `scylla`. Install it from Git, then coodie:

```bash
pip install "scylla @ git+https://github.com/scylladb-zpp-2025-python-rs-driver/python-rs-driver"
pip install coodie
```

Inside a coodie checkout, the `python-rs` extra resolves the same Git
source through `[tool.uv.sources]`:

```bash
uv pip install -e ".[python-rs]"
```

```{note}
Only Linux is exercised in coodie's CI for python-rs-driver. macOS and
Windows builds need a working Rust toolchain and are untested. Per-query
`consistency` and `timeout` are currently ignored by `PythonRsDriver`,
and python-rs-driver does not expose SSL/TLS or authentication options
to Python yet.
```

(sync-bridge)=

## Sync Bridge

acsylla and python-rs-driver only offer an async API, and their sessions
are bound to the event loop they were created on. coodie bridges them to
the sync API like this:

1. With `hosts=`, `init_coodie()` / `init_coodie_async()` start a
   dedicated event loop in a daemon thread (`coodie-acsylla-sync` or
   `coodie-python-rs-sync`). They create the session **on that loop**,
   and block until it is connected.
2. Sync calls (`execute`, `sync_table`, `close`) submit the coroutine to
   the background loop with `asyncio.run_coroutine_threadsafe()` and block
   on the result. This works from any thread, including one that already
   runs an event loop (for example pytest-asyncio or an ASGI handler).
3. Async calls (`execute_async`, `sync_table_async`, `close_async`) are
   also dispatched to the background loop, and the caller awaits the result
   without blocking its own loop.

So plain sync code can use acsylla:

```python
from coodie.sync import Document, init_coodie

init_coodie(hosts=["127.0.0.1"], keyspace="my_ks", driver_type="acsylla")

class Product(Document):
    ...

Product.sync_table()  # runs on the background loop, blocks until done
```

The same driver also serves `coodie.aio` documents.

```{warning}
The bridge needs the session to be created on the background loop. If you
pass your own session via `session=`, async calls run directly on your
loop, but sync calls may hang. `AcsyllaDriver` emits a `UserWarning` in
this case. To get a sync-capable driver, pass `hosts=` or use
`AcsyllaDriver.connect()` / `PythonRsDriver.connect()` with a session
factory.
```

`CassandraDriver` (scylla/cassandra) needs no bridge: its sync calls use
the driver's blocking API, and its async calls wrap the driver's
`execute_async()` futures.

## init_coodie() Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hosts` | `list[str] \| None` | `None` | Contact points for the cluster |
| `session` | `Any \| None` | `None` | Pre-created driver session (BYOS) |
| `keyspace` | `str \| None` | `None` | Default keyspace |
| `driver_type` | `str` | `"scylla"` | `"scylla"`, `"cassandra"`, `"acsylla"`, or `"python-rs"` |
| `name` | `str` | `"default"` | Name for multi-driver setups |
| `ssl_context` | `ssl.SSLContext \| None` | `None` | TLS context (scylla/cassandra only) |
| `lazy` | `bool` | `False` | Connect on first use (scylla/cassandra only) |
| `compression` | `str \| bool \| None` | `None` | Passed to `Cluster()` (scylla/cassandra only, ignored when `lazy=True`) |
| `speculative_execution_policy` | `Any \| None` | `None` | Passed to `Cluster()` (scylla/cassandra only, ignored when `lazy=True`) |
| `**kwargs` | | | Passed to `Cluster()` (scylla/cassandra), `acsylla.create_cluster()` (acsylla), or `SessionBuilder()` (python-rs, except `port`) |

`init_coodie_async()` takes the same parameters, except that `lazy`,
`compression`, and `speculative_execution_policy` go through `**kwargs`.
It adds the acsylla TLS options `ssl_enabled`, `ssl_trusted_cert`,
`ssl_cert`, `ssl_private_key`, and `ssl_verify_flags` (see {doc}`encryption`).

If you pass `hosts`, coodie creates the cluster and session for you. If
you pass `session`, coodie wraps your existing session and ignores
`hosts` and `**kwargs`. acsylla and python-rs need one of the two.
scylla/cassandra fall back to `["127.0.0.1"]` when neither is given.

## Bring Your Own Session (BYOS)

Already have a configured session? Pass it directly:

```python
from cassandra.cluster import Cluster

cluster = Cluster(
    ["node1", "node2"],
    protocol_version=4,
    # ... any other cluster options
)
session = cluster.connect("my_keyspace")

from coodie.sync import init_coodie
driver = init_coodie(session=session, keyspace="my_keyspace")
```

This is useful when you need fine-grained control over connection
pooling, load balancing policies, or authentication.

## Named Drivers (Multi-Cluster)

For applications that talk to multiple clusters, register each with a
unique name:

```python
from coodie.sync import init_coodie

init_coodie(hosts=["analytics-cluster"], keyspace="analytics", name="analytics")
init_coodie(hosts=["production-cluster"], keyspace="prod", name="prod")
```

Retrieve a specific driver by name:

```python
from coodie.drivers import get_driver

analytics_driver = get_driver("analytics")
prod_driver = get_driver("prod")
```

The first driver registered (or the one registered with the default
name `"default"`) is used when no name is specified.

## Low-Level Driver API

The `AbstractDriver` base class defines the driver interface:

```python
from coodie.drivers import get_driver

driver = get_driver()

# Sync
rows = driver.execute("SELECT * FROM users WHERE id = ?", [user_id])

# Async
rows = await driver.execute_async("SELECT * FROM users WHERE id = ?", [user_id])
```

### register_driver()

Register a custom driver implementation:

```python
from coodie.drivers import register_driver

register_driver("my_driver", my_driver_instance, default=True)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Unique name for the driver |
| `driver` | `AbstractDriver` | Driver instance |
| `default` | `bool` | Set as the default driver (default: `False`) |

## Extra Cluster Options

Any extra keyword arguments to `init_coodie()` are forwarded to the
underlying driver's cluster or session builder (`Cluster()` for
scylla/cassandra):

```python
init_coodie(
    hosts=["node1"],
    keyspace="my_ks",
    port=19042,
    connect_timeout=30,
)
```

This includes SSL/TLS options such as `ssl_context` for
cassandra-driver/scylla-driver and `ssl_enabled` for acsylla.
See {doc}`encryption` for full examples.

## What's Next?

- {doc}`encryption` — SSL/TLS encryption for client-to-server connections
- {doc}`sync-vs-async` — choosing between sync and async APIs
- {doc}`lwt` — conditional writes with IF NOT EXISTS / IF EXISTS
- {doc}`batch-operations` — batch multiple statements into one round-trip
- {doc}`exceptions` — error handling patterns
