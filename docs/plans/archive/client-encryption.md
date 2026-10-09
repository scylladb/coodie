# Client Encryption (SSL/TLS) Plan

> **Goal:** Document and validate coodie's SSL/TLS support for every driver
> backend — `CassandraDriver` (scylla-driver / cassandra-driver) and
> `AcsyllaDriver` — so that operators can enable client-to-server encryption
> with a single configuration change.  Deliver a user-facing guide, integration
> tests against a real SSL-enabled ScyllaDB instance, and clear recipes for the
> most common cert configurations.

---

## Table of Contents

1. [Feature Gap Analysis](#1-feature-gap-analysis)
   - [1.1 CassandraDriver (scylla-driver / cassandra-driver)](#11-cassandradriver-scylla-driver--cassandra-driver)
   - [1.2 AcsyllaDriver](#12-acsylladriver)
   - [1.3 init_coodie() / init_coodie_async()](#13-init_coodie--init_coodie_async)
2. [Implementation Phases](#2-implementation-phases)
3. [Test Plan](#3-test-plan)
   - [3.1 Integration Tests](#31-integration-tests)
4. [Migration Guide](#4-migration-guide)
5. [References](#5-references)

---

## 1. Feature Gap Analysis

Legend:
- ✅ **Implemented** — working today
- 🔧 **Partial** — infrastructure exists but not fully exposed via public API
- ❌ **Missing** — not yet implemented

### 1.1 CassandraDriver (scylla-driver / cassandra-driver)

| Feature | coodie Equivalent | Status |
|---|---|---|
| Pass `ssl_context` to `Cluster()` | `init_coodie(ssl_context=...)` — first-class parameter | ✅ |
| Pass `ssl_options` to `Cluster()` | `init_coodie(ssl_options=...)` via `**kwargs` | ✅ |
| Bring-your-own SSL session (BYOS) | `init_coodie(session=pre_ssl_session)` | ✅ |
| Mutual TLS (client cert authentication) | SSL context with `load_cert_chain()` | ✅ |
| Documentation for SSL configuration | `docs/source/guide/encryption.md` | ✅ |
| Integration tests for SSL connections | `tests/integration/test_encryption.py` | ✅ |

**Gap summary — CassandraDriver:** All gaps closed ✅

### 1.2 AcsyllaDriver

| Feature | coodie Equivalent | Status |
|---|---|---|
| Pass `ssl_enabled=True` to `acsylla.create_cluster()` | `init_coodie_async(ssl_enabled=True)` — first-class parameter | ✅ |
| Pass PEM cert strings to `create_cluster()` | `init_coodie_async(ssl_trusted_cert=pem_str)` — first-class parameter | ✅ |
| Configure SSL verify flags | `init_coodie_async(ssl_verify_flags=...)` — first-class parameter | ✅ |
| Bring-your-own SSL session (BYOS) | `init_coodie_async(session=pre_ssl_session)` | ✅ |
| Documentation for SSL configuration | `docs/source/guide/encryption.md` | ✅ |
| Integration tests for SSL connections | `tests/integration/test_encryption.py` | ✅ |

**Gap summary — AcsyllaDriver:** All gaps closed ✅

### 1.3 init_coodie() / init_coodie_async()

| Feature | Status | Notes |
|---|---|---|
| `**kwargs` forwarded to `Cluster()` | ✅ | `ssl_context`, `ssl_options`, etc. work today |
| `**kwargs` forwarded to `acsylla.create_cluster()` | ✅ | `ssl_enabled`, `ssl_trusted_cert`, etc. work today |
| Explicit `ssl_context` parameter | ✅ | First-class kwarg on `init_coodie()` |
| Explicit acsylla SSL parameters | ✅ | `ssl_enabled`, `ssl_trusted_cert`, `ssl_cert`, `ssl_private_key`, `ssl_verify_flags` on `init_coodie_async()` |
| SSL validation / helpful error messages | ❌ | Bad SSL config surfaces as a raw driver exception |

**Gap summary — init_coodie():**
- Explicit parameter → ✅ `ssl_context` is now a first-class kwarg on `init_coodie()`; acsylla SSL params on `init_coodie_async()`
- Error messages → out of scope for this plan

---

## 2. Implementation Phases

### Phase 1: Documentation (Priority: High) ✅

**Goal:** Ship a user-facing guide that shows exactly how to enable SSL for every supported driver.

| Task | Description | Status |
|---|---|---|
| 1.1 | Create `docs/source/guide/encryption.md` with CassandraDriver and AcsyllaDriver sections | ✅ |
| 1.2 | Add common recipes: self-signed CA, mutual TLS, disable cert verification (dev/test) | ✅ |
| 1.3 | Add `guide/encryption` to the toctree in `docs/source/index.md` | ✅ |
| 1.4 | Link the encryption guide from `docs/source/guide/drivers.md` | ✅ |

### Phase 2: Integration Tests (Priority: High) ✅

**Goal:** Verify that SSL connections actually work against a real ScyllaDB instance.

| Task | Description | Status |
|---|---|---|
| 2.1 | Add `ssl_certs` session fixture that generates a self-signed CA + server cert using `cryptography`; skip if `cryptography` is not installed | ✅ |
| 2.2 | Add `scylla_ssl_container` fixture that mounts certs and a custom `scylla.yaml` with `client_encryption_options.enabled: true` | ✅ |
| 2.3 | Write `TestSSLCassandraDriver` — sync + async tests verifying `init_coodie(ssl_context=...)` works | ✅ |
| 2.4 | Write `TestSSLAcsyllaDriver` — async test verifying `init_coodie_async(ssl_enabled=True, ssl_trusted_cert=...)` works | ✅ |
| 2.5 | Mark all SSL tests with `@pytest.mark.integration` and add a `ssl` sub-mark | ✅ |

### Phase 3: Explicit ssl_context Parameter (Priority: Low) ✅

**Goal:** Make `ssl_context` a first-class keyword argument on `init_coodie()` so IDEs and type checkers surface it.

| Task | Description | Status |
|---|---|---|
| 3.1 | Add `ssl_context: ssl.SSLContext \| None = None` to `init_coodie()` signature; pass it into `Cluster()` | ✅ |
| 3.2 | Add `ssl_enabled`, `ssl_trusted_cert`, `ssl_cert`, `ssl_private_key`, `ssl_verify_flags` to `init_coodie_async()` for acsylla | ✅ |
| 3.3 | Add type stubs / overloads so mypy doesn't complain | ✅ |
| 3.4 | Unit tests verifying the new parameters reach the driver | ✅ |
| 3.5 | Update `docs/source/guide/encryption.md` to use the new explicit API | ✅ |

---

## 3. Test Plan

### 3.1 Integration Tests

#### `tests/integration/test_encryption.py`

| Test Case | Phase |
|---|---|
| SSL certs fixture generates valid CA + server certificate | 2 |
| ScyllaDB container starts with `client_encryption_options.enabled: true` | 2 |
| `CassandraDriver` sync execute succeeds over SSL (`CERT_NONE` verify) | 2 |
| `CassandraDriver` async execute succeeds over SSL | 2 |
| `CassandraDriver` connection fails when SSL not configured against SSL-only server | 2 |
| `AcsyllaDriver` async execute succeeds over SSL with CA cert | 2 |
| `init_coodie()` correctly forwards `ssl_context` kwarg to `Cluster()` | 2 |
| `init_coodie_async()` correctly forwards `ssl_enabled` kwarg to `acsylla.create_cluster()` | 2 |

---

## 4. Migration Guide

Existing applications that connect to a non-SSL Scylla/Cassandra cluster do not need any changes — coodie passes `**kwargs` directly to the underlying driver, and SSL is opt-in.

To migrate an existing application to SSL:

### cassandra-driver / scylla-driver

```python
import ssl
from coodie.sync import init_coodie

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.load_verify_locations("/path/to/ca.crt")

init_coodie(
    hosts=["node1", "node2"],
    keyspace="my_ks",
    ssl_context=ssl_context,
)
```

### acsylla

```python
from coodie.aio import init_coodie

ca_pem = open("/path/to/ca.crt").read()

await init_coodie(
    hosts=["node1", "node2"],
    keyspace="my_ks",
    driver_type="acsylla",
    ssl_enabled=True,
    ssl_trusted_cert=ca_pem,
)
```

---

## 5. References

- [cassandra-driver SSL docs](https://docs.datastax.com/en/developer/python-driver/3.25/security/)
- [ScyllaDB client encryption options](https://docs.scylladb.com/stable/operating-scylla/security/client-node-encryption.html)
- [acsylla SSL API](https://github.com/acsylla/acsylla#ssl)
- Python [`ssl` module](https://docs.python.org/3/library/ssl.html)
- [cryptography library](https://cryptography.io/en/latest/) — used in test cert generation
