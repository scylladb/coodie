# Installation

## Requirements

- **Python 3.10** or later

## Install coodie

The package is published on [PyPI](https://pypi.org/project/coodie/) and can
be installed with `pip` (or any equivalent):

```bash
pip install coodie
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add coodie
```

## Driver Extras

coodie itself is driver-agnostic. Install the driver extra that matches your
cluster:

```bash
# ScyllaDB / Cassandra via scylla-driver (recommended)
pip install "coodie[scylla]"

# Cassandra via cassandra-driver
pip install "coodie[cassandra]"

# Async-native driver via acsylla
pip install "coodie[acsylla]"
```

The experimental Rust-based python-rs-driver is not on PyPI, so the
`python-rs` extra cannot pull it from there. Build it from Git first
(needs a Rust toolchain), then install coodie:

```bash
pip install "scylla @ git+https://github.com/scylladb-zpp-2025-python-rs-driver/python-rs-driver"
pip install coodie
```

See {doc}`guide/drivers` for details.

You need **at least one** driver installed to connect to a database.

## Verify the Installation

```python
import coodie
print(coodie.__version__)
```

## What's Next?

Head to the {doc}`quickstart` to connect to a cluster and run your first query.
