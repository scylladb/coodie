# Demo Suite Extension Plan

> **Goal:** Expand the demo suite from a single FastAPI app into a collection of
> standalone, colorful demo applications — each in its own folder — covering
> Django integration, Flask integration, Cassandra-specific features (TTL,
> counters, LWT, batch, collections, materialized views, vector search), migration
> patterns inspired by scylladb/argus, and built-in sample-data generation with
> options for real-data feeds.

---

## Table of Contents

1. [Current State](#1-current-state)
2. [Design Principles](#2-design-principles)
3. [Target Audience](#3-target-audience)
4. [Demo Inventory & Gap Analysis](#4-demo-inventory--gap-analysis)
   - [4.1 Framework Integrations](#41-framework-integrations)
   - [4.2 Cassandra Feature Showcases](#42-cassandra-feature-showcases)
   - [4.3 Migration & Real-World Patterns](#43-migration--real-world-patterns)
   - [4.4 Data Generation & Feeds](#44-data-generation--feeds)
5. [Demo Directory Structure](#5-demo-directory-structure)
6. [Implementation Phases](#6-implementation-phases)
7. [Vector Search — Library Development Scope](#7-vector-search--library-development-scope)
8. [Shared Infrastructure](#8-shared-infrastructure)
9. [Demo Storylines & Visual Themes](#9-demo-storylines--visual-themes)
   - [9.1 The Coodie Cinematic Universe — Overview](#91-the-coodie-cinematic-universe--overview)
   - [9.2 Per-Demo Storylines](#92-per-demo-storylines)
   - [9.3 Visual Guidelines Summary Table](#93-visual-guidelines-summary-table)
10. [Scylla-Monitoring Integration — The War Room](#10-scylla-monitoring-integration--the-war-room)
11. [CI Testing — Demo Health Checks](#11-ci-testing--demo-health-checks)
    - [11.1 Goals](#111-goals)
    - [11.2 Workflow Design](#112-workflow-design)
    - [11.3 Makefile `test` Target Convention](#113-makefile-test-target-convention)
    - [11.4 Smoke-Test Scripts](#114-smoke-test-scripts)
    - [11.5 Implementation Tasks](#115-implementation-tasks)
    - [11.6 Test Matrix Summary](#116-test-matrix-summary)
12. [References](#12-references)

---

## 1. Current State

The repository has a single demo application:

| Demo | Framework | Features Shown | Location |
|---|---|---|---|
| Product Catalog API | FastAPI + HTMX | Async CRUD, secondary indexes, clustering order, Jinja2 templates | `demo/` |

The existing demo is well-structured with a dark-theme HTMX UI, but covers only
basic CRUD via the async API. No Django, Flask, sync API, TTL, counters, LWT,
batch, collections, materialized views, vector search, or migration workflows
are demonstrated.

---

## 2. Design Principles

- **One folder per demo** — each demo is self-contained under `demos/<name>/`
  with its own `pyproject.toml`, `README.md`, and models
- **Colorful by default** — every demo with a UI uses a vibrant, themed color
  palette (dark backgrounds, accent colors, gradients) following the existing
  HTMX demo's style conventions
- **Sample data built in** — every demo includes a `seed.py` (or CLI command)
  that generates realistic sample data using Faker or hand-crafted generators;
  optionally accepts CSV/JSON feeds for real data
- **Makefile-driven** — every demo includes a `Makefile` with standard targets
  (`make db-up`, `make db-down`, `make seed`, `make run`, `make clean`) so a
  single `make run` spins the database up, creates the keyspace, syncs tables,
  seeds data, and starts the app
- **Copy-paste runnable** — each README has a numbered quick-start (start
  ScyllaDB → install → seed → run) that works in under 2 minutes
- **Showcases coodie, not the framework** — framework boilerplate is minimal;
  the focus is on coodie model definitions, queries, and Cassandra patterns

---

## 3. Target Audience

| Persona | What They Want |
|---|---|
| 🐍 **Python web dev** | See coodie work with Django / Flask / FastAPI |
| 🗄️ **Cassandra practitioner** | See TTL, counters, LWT, batch, materialized views in action |
| 🔄 **cqlengine migrator** | See side-by-side before/after migration from cqlengine models |
| 🚀 **Evaluator** | Run a colorful demo quickly to assess if coodie fits their project |

---

## 4. Demo Inventory & Gap Analysis

Legend:
- ✅ **Exists** — demo is implemented today
- ❌ **Missing** — demo does not exist yet

### 4.1 Framework Integrations

| Demo | Framework | API Style | Status |
|---|---|---|---|
| Product Catalog (existing) | FastAPI + HTMX | Async | ✅ |
| Flask Blog | Flask + Jinja2 | Sync | ❌ |
| Django Task Board | Django + templates | Sync | ✅ |

**Gap summary — framework integrations:**
- Flask Blog → demonstrate coodie's sync API with Flask's request lifecycle,
  `init_coodie()` in app factory, Jinja2 templates with a colorful UI
- Django Task Board → demonstrate coodie alongside Django's ORM (Cassandra for
  high-write task events, PostgreSQL/SQLite for auth), management commands for
  `sync_table`, Django templates with Bootstrap/Tailwind

### 4.2 Cassandra Feature Showcases

| Demo | Features Shown | Status |
|---|---|---|
| Product Catalog (existing) | Secondary indexes, clustering order, basic CRUD | ✅ |
| TTL & Ephemeral Data | `ttl=` on save, `__default_ttl__`, session tokens | ❌ |
| Real-Time Counters | `CounterDocument`, `increment()`, `decrement()`, analytics dashboard | ❌ |
| Lightweight Transactions | `if_exists`, `if_not_exists`, `if_conditions`, optimistic locking | ❌ |
| Batch Operations | `BatchQuery`, logged/unlogged batches, bulk imports | ❌ |
| Collections & UDTs | `list`, `set`, `map` fields, `add__`, `remove__`, frozen types | ❌ |
| Materialized Views | `MaterializedView`, `sync_view()`, read-only queries | ❌ |
| Time-Series Analytics | Clustering keys with DESC order, `per_partition_limit()`, `paged_all()` | ❌ |
| Polymorphic Models | Single-table inheritance, discriminator column | ❌ |
| Vector Similarity Search | `vector<float, N>` column, vector index, ANN queries, embeddings | ❌ |

**Gap summary — Cassandra features:**
- TTL → short-lived session/token store showing data that auto-expires
- Counters → page-view / vote analytics dashboard with live counter updates
- LWT → user registration with uniqueness guarantees, optimistic concurrency
- Batch → bulk CSV import tool using logged and unlogged batches
- Collections → tagging system with set operations, JSON-like map fields
- Materialized Views → product-by-category view auto-maintained by Cassandra
- Time-Series → IoT sensor data with time-bucketed partitions and pagination
- Polymorphic → content management with Article / Video / Podcast subtypes
- Vector Search → semantic product/document similarity search using embeddings,
  ANN (Approximate Nearest Neighbor) queries, and cosine similarity index;
  inspired by argus's `SCTErrorEventEmbedding` model

### 4.3 Migration & Real-World Patterns

| Demo | Pattern | Inspiration | Status |
|---|---|---|---|
| Argus-Style Test Tracker | Complex models, UDTs, composite keys, plugin architecture | scylladb/argus | ❌ |
| cqlengine → coodie Migration | Side-by-side models, sync_table migration, data verification | reddit/cqlmapper, argus | ❌ |
| Schema Migration Framework | Versioned migration files, apply/rollback, dry-run, status tracking, CLI | coodie Phase B, Django, Alembic | ❌ |

**Gap summary — migration patterns:**
- Argus-Style → scaled-down version of argus models (User, TestRun, Event,
  Notification) showing composite partition keys, clustering, UDT-like nested
  types, batch writes, and prepared-statement patterns
- Migration → step-by-step guide with cqlengine models on the left, coodie
  models on the right, and a migration script that syncs tables and verifies
  data round-trip
- Schema Migration Framework → standalone demo showing coodie's Phase B
  migration framework in action: versioned migration files that add columns,
  create indexes, change table options, and perform data transformations; the
  `coodie migrate` CLI for apply, rollback, dry-run, and status; state
  tracking in `_coodie_migrations`; and the LWT-based distributed lock

### 4.4 Data Generation & Feeds

| Capability | Status |
|---|---|
| Built-in `seed.py` with Faker-generated data | ❌ (existing demo has no seed script) |
| `--count N` flag to control volume | ❌ |
| CSV/JSON feed import | ❌ |
| Colorful CLI output (rich/click) | ❌ |

**Gap summary — data generation:**
- Every demo gets a `seed.py` using `faker` and `rich` for colorful progress
  output
- Accepts `--count N` for volume control and `--feed path.csv` for real data
- The existing FastAPI demo should be retrofitted with a `seed.py` as well

---

## 5. Demo Directory Structure

```
demos/
├── README.md                          # Index: list of all demos with descriptions
├── docker-compose.yml                 # Shared ScyllaDB container
├── fastapi-catalog/                   # Existing demo (moved from demo/)
│   ├── README.md
│   ├── Makefile                       # db-up, db-down, seed, run, clean
│   ├── pyproject.toml
│   ├── main.py
│   ├── models.py
│   ├── seed.py                        # NEW: sample data generator
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── partials/
├── flask-blog/                        # NEW: Flask integration
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── app.py
│   ├── models.py
│   ├── seed.py
│   └── templates/
├── django-taskboard/                  # NEW: Django integration
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── manage.py
│   ├── taskboard/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── cassandra_models.py        # coodie models (separate from Django ORM)
│   │   └── management/commands/
│   │       └── sync_cassandra.py
│   ├── tasks/
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── templates/
│   └── seed.py
├── ttl-sessions/                      # NEW: TTL & ephemeral data
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── main.py
│   ├── models.py
│   └── seed.py
├── realtime-counters/                 # NEW: Counter columns
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── main.py
│   ├── models.py
│   └── seed.py
├── lwt-user-registry/                 # NEW: Lightweight transactions
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── main.py
│   ├── models.py
│   └── seed.py
├── batch-importer/                    # NEW: Batch operations
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── main.py
│   ├── models.py
│   └── seed.py
├── collections-tags/                  # NEW: Collections & nested types
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── main.py
│   ├── models.py
│   └── seed.py
├── materialized-views/                # NEW: Materialized views
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── main.py
│   ├── models.py
│   └── seed.py
├── timeseries-iot/                    # NEW: Time-series patterns
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── main.py
│   ├── models.py
│   └── seed.py
├── polymorphic-cms/                   # NEW: Single-table inheritance
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── main.py
│   ├── models.py
│   └── seed.py
├── vector-search/                     # NEW: Vector similarity search
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── main.py
│   ├── models.py
│   └── seed.py
├── argus-tracker/                     # NEW: Argus-inspired complex models
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── main.py
│   ├── models.py
│   └── seed.py
└── migration-guide/                   # NEW: cqlengine → coodie migration
    ├── README.md
    ├── Makefile
    ├── cqlengine_models.py
    ├── coodie_models.py
    ├── migrate.py
    └── verify.py
└── schema-migrations/                 # NEW: coodie Phase B migration framework
    ├── README.md
    ├── Makefile
    ├── pyproject.toml
    ├── main.py                        # FastAPI app using migrated schema
    ├── models.py                      # coodie Document models
    ├── seed.py
    └── migrations/
        ├── 20260115_001_create_base_tables.py
        ├── 20260203_002_add_featured_column.py
        ├── 20260220_003_set_reviews_ttl.py
        └── 20260310_004_add_search_index.py
```

---

## 6. Implementation Phases

### Phase 1: Foundation & Existing Demo Retrofit (Priority: High)

**Goal:** Establish shared infrastructure, move the existing demo, and add seed tooling.

| Task | Description |
|---|---|
| 1.1 | Create `demos/` top-level directory with `README.md` index |
| 1.2 | Move existing `demo/` to `demos/fastapi-catalog/`, update paths and README |
| 1.3 | Add `Makefile` with `db-up`, `db-down`, `seed`, `run`, `clean` targets to `demos/fastapi-catalog/` |
| 1.4 | Add `seed.py` to `demos/fastapi-catalog/` with Faker-based product/review generation and `rich` progress output |
| 1.5 | Ensure `--count N` and `--feed products.csv` flags work |
| 1.6 | Verify the moved demo still runs end-to-end via `make run` |

### Phase 2: Flask Blog Demo (Priority: High)

**Goal:** Demonstrate coodie's sync API integrated with Flask, including a colorful blog UI.

| Task | Description |
|---|---|
| 2.1 | Create `demos/flask-blog/` with `pyproject.toml`, Flask app factory, and coodie `init_coodie()` in `create_app()` |
| 2.2 | Define `Post` and `Comment` models with clustering keys (newest-first), secondary indexes, and tags (list field) |
| 2.3 | Build Jinja2 templates with a colorful dark-theme UI (cards, gradients, accent colors) |
| 2.4 | Add `seed.py` with Faker blog posts and comments, `rich` progress bars |
| 2.5 | Write README with numbered quick-start and example `curl` commands |
| 2.6 | Manual end-to-end test: start → seed → browse → create post → verify |

### Phase 3: Django Task Board Demo (Priority: High)

**Goal:** Demonstrate coodie alongside Django, using Cassandra for high-write task events.

| Task | Description |
|---|---|
| 3.1 | Create `demos/django-taskboard/` with Django project scaffold and `pyproject.toml` |
| 3.2 | Define coodie models (`TaskEvent`, `TaskCounter`) in `cassandra_models.py`, separate from Django ORM models |
| 3.3 | Add `manage.py sync_cassandra` management command that calls `sync_table()` for all coodie models |
| 3.4 | Build Django views and templates with a colorful Kanban-style board UI |
| 3.5 | Add `seed.py` with Faker task events and counters |
| 3.6 | Write README explaining the dual-database pattern (Django ORM + coodie) |
| 3.7 | Manual end-to-end test |

### Phase 4: Cassandra Feature Demos — TTL, Counters, LWT (Priority: Medium)

**Goal:** Showcase TTL auto-expiry, counter columns, and lightweight transactions in standalone demos.

| Task | Description |
|---|---|
| ✅ 4.1 | Create `demos/ttl-sessions/` — ephemeral session store with `ttl=` on save and `__default_ttl__` on model |
| ✅ 4.2 | Create `demos/realtime-counters/` — page-view analytics with `CounterDocument`, `increment()`, and a live dashboard |
| 4.3 | Create `demos/lwt-user-registry/` — user registration with `if_not_exists`, optimistic locking with `if_conditions` |
| 4.4 | Each demo gets `seed.py`, colorful UI, and README |
| 4.5 | Manual end-to-end test for each demo |

### Phase 5: Cassandra Feature Demos — Batch, Collections, Views (Priority: Medium)

**Goal:** Showcase batch operations, collection types, and materialized views.

| Task | Description |
|---|---|
| 5.1 | Create `demos/batch-importer/` — CSV bulk import using `BatchQuery` (logged and unlogged), `rich` progress |
| 5.2 | ✅ Create `demos/collections-tags/` — article tagging with `set` fields, `add__`/`remove__` operations, `map` metadata |
| 5.3 | Create `demos/materialized-views/` — product catalog with auto-maintained `MaterializedView` by category |
| 5.4 | Each demo gets `seed.py`, colorful UI, and README |
| 5.5 | Manual end-to-end test for each demo |

### Phase 6: Vector Similarity Search Demo (Priority: High)

**Goal:** Add vector column support to coodie's type system and showcase it with a semantic search demo.

> **Note:** This phase requires library-level development in coodie itself
> (not just demo code), because coodie currently has **no vector support**.
> The scoped development work is listed below.

#### 6a. coodie library development (pre-requisites)

| Task | Description |
|---|---|
| 6a.1 | Add a `Vector(dimensions=N)` field annotation to `coodie/fields.py` that maps to the CQL `vector<float, N>` type |
| 6a.2 | Update `coodie/schema.py` type mapping to emit `vector<float, N>` in CREATE TABLE DDL |
| 6a.3 | Add `VectorIndex(similarity_function="COSINE")` annotation (or `Settings` option) to emit `CREATE INDEX ... USING 'vector_index' WITH OPTIONS = {'similarity_function': '...'}` |
| 6a.4 | Support ANN queries: `Model.find().order_by_ann(embedding_field, query_vector).limit(N)` or equivalent QuerySet method that emits `ORDER BY field ANN OF [...]` CQL |
| 6a.5 | Validate vector dimensions on save (list length must match declared dimensions) |
| 6a.6 | Unit tests for vector type mapping, DDL generation, ANN query building, and dimension validation |
| 6a.7 | Integration tests with ScyllaDB: create table with vector column, insert embeddings, ANN query returns nearest neighbors |

#### 6b. Vector search demo

| Task | Description |
|---|---|
| 6b.1 | Create `demos/vector-search/` — semantic product search using sentence-transformer embeddings (384-dim or smaller) |
| 6b.2 | Define `ProductEmbedding` model with `vector<float, N>` column, partition key, and vector index with cosine similarity |
| 6b.3 | `seed.py` generates product descriptions and computes embeddings (using a small model like `all-MiniLM-L6-v2` or pre-computed vectors from a JSON feed) |
| 6b.4 | Build a search UI: user enters a text query → compute embedding → ANN query → display ranked results with similarity scores |
| 6b.5 | Colorful dark-theme UI with similarity score badges and result cards |
| 6b.6 | README documents the CQL behind the scenes (`CREATE INDEX ... USING 'vector_index'`, `ORDER BY ... ANN OF`) |
| 6b.7 | Manual end-to-end test: seed → search → verify ranked results |

### Phase 7: Time-Series & Polymorphic Demos (Priority: Medium)

**Goal:** Showcase advanced data-modeling patterns.

| Task | Description |
|---|---|
| 7.1 | Create `demos/timeseries-iot/` — sensor readings with time-bucketed partitions, `per_partition_limit()`, `paged_all()` |
| 7.2 | Create `demos/polymorphic-cms/` — content management with `Article`/`Video`/`Podcast` subtypes via single-table inheritance |
| 7.3 | Each demo gets `seed.py`, colorful UI, and README |
| 7.4 | Manual end-to-end test for each demo |

### Phase 8: Argus-Inspired Tracker & Migration Guide (Priority: Medium)

**Goal:** Demonstrate complex real-world patterns from scylladb/argus and provide a cqlengine migration walkthrough.

| Task | Description |
|---|---|
| 8.1 | Create `demos/argus-tracker/` — scaled-down test tracker with User, TestRun (composite PK + clustering), Event (compound partition), Notification (TimeUUID) models |
| 8.2 | Include batch event ingestion, prepared-statement caching patterns, and partition-scoped queries |
| 8.3 | Create `demos/migration-guide/` — side-by-side `cqlengine_models.py` and `coodie_models.py` with a `migrate.py` script that syncs tables and a `verify.py` that checks data round-trip |
| 8.4 | Reference argus model patterns: composite partition keys, clustering DESC, multiple secondary indexes, List/Map collections |
| 8.5 | Each demo gets README with step-by-step walkthrough |
| 8.6 | Manual end-to-end test for each demo |

### Phase 9: Top-Level README & Polish (Priority: Low)

**Goal:** Tie all demos together with an index README and ensure consistent quality.

| Task | Description |
|---|---|
| ✅ 9.1 | Write `demos/README.md` with a table listing all demos, their focus area, and quick-start links |
| ✅ 9.2 | Add a `docker-compose.yml` at `demos/` level for shared ScyllaDB instance |
| 9.3 | Ensure every demo has consistent Makefile targets, color theming, README structure, and seed.py interface |
| ✅ 9.4 | Update the top-level `README.md` to link to the new `demos/` directory |
| 9.5 | Final review of all demos for consistency and correctness |

### Phase 10: Schema Migration Framework Demo (Priority: Medium)

**Goal:** Demonstrate coodie's Phase B versioned migration framework — the `coodie migrate` CLI, migration file authoring, apply/rollback/dry-run lifecycle, state tracking, and distributed locking — in a standalone demo application.

| Task | Description |
|---|---|
| 10.1 | Create `demos/schema-migrations/` with `pyproject.toml`, `Makefile`, and `README.md` |
| 10.2 | Define base `Product` and `Review` models in `models.py` (reuse the catalog schema) |
| 10.3 | Create `migrations/20260115_001_create_base_tables.py` — initial table creation via `sync_table()` wrapped in a migration |
| 10.4 | Create `migrations/20260203_002_add_featured_column.py` — `ALTER TABLE ... ADD "featured" boolean` + secondary index |
| 10.5 | Create `migrations/20260220_003_set_reviews_ttl.py` — `ALTER TABLE ... WITH default_time_to_live = 31536000` |
| 10.6 | Create `migrations/20260310_004_add_search_index.py` — add a secondary index on product name for search |
| 10.7 | Build `main.py` as a minimal FastAPI app that uses the migrated schema (products with `featured` flag) |
| 10.8 | Add `seed.py` with `rich` progress output seeding products and reviews, including featured products |
| 10.9 | Write README with step-by-step walkthrough: start ScyllaDB → create keyspace → apply migrations → seed → run app → rollback → dry-run → status |
| 10.10 | Include a "Writing Your Own Migration" section in the README showing the file naming convention and `ForwardMigration` class pattern |
| 10.11 | Manual end-to-end test: `make db-up` → `make migrate` → `make seed` → `make run` → `make migrate-rollback` → `make migrate-status` |

---

## 7. Vector Search — Library Development Scope

Phase 6 above requires adding vector support to coodie's core library **before**
the demo can be built. This section summarizes the scope of that work.

coodie currently has **no vector type, no vector index support, and no ANN query
syntax**. ScyllaDB (and Cassandra 5.0+) support the `vector<T, N>` CQL type
and `ORDER BY ... ANN OF [...]` queries for approximate nearest-neighbor search.

The argus project (`scylladb/argus`) implements a custom `Vector` column class
extending cqlengine's `columns.List` that emits `vector<float, 384>` DDL and
uses `CREATE INDEX ... USING 'vector_index' WITH OPTIONS = {'similarity_function': 'COSINE'}`
for cosine-similarity indexes.

### What coodie needs

| Area | What to Add | CQL Equivalent |
|---|---|---|
| **Field type** | `Vector(dimensions=N)` annotation in `fields.py` | `vector<float, N>` column type |
| **Schema DDL** | Type mapping in `schema.py` for CREATE TABLE | `embedding vector<float, 384>` |
| **Index DDL** | `VectorIndex(similarity="COSINE")` annotation or Settings hook | `CREATE INDEX ... USING 'vector_index' WITH OPTIONS = {'similarity_function': 'COSINE'}` |
| **Query builder** | `order_by_ann(field, query_vector)` on QuerySet | `ORDER BY embedding ANN OF [0.1, 0.2, ...]` |
| **Validation** | Dimension check on save (list length == declared N) | — |
| **Driver support** | Verify both cassandra-driver and acsylla handle `vector<float, N>` binding | — |

### Estimated complexity

- **Fields + schema**: Low — similar to adding any new CQL type annotation
- **Vector index DDL**: Medium — requires a new index creation path (not a
  standard secondary index)
- **ANN query syntax**: Medium — new QuerySet method that emits non-standard
  `ORDER BY` clause
- **Driver compatibility**: Unknown — needs testing with both drivers

---

## 8. Shared Infrastructure

### 8.1 Docker Compose (shared ScyllaDB)

All demos share a single ScyllaDB container via `demos/docker-compose.yml`:

```yaml
services:
  scylladb:
    image: scylladb/scylla:latest
    ports:
      - "9042:9042"
    command: --smp 1 --memory 512M --developer-mode 1
```

### 8.2 Makefile Convention

Every demo includes a `Makefile` with standard targets so that `make run` is the
only command a user needs to try the demo end-to-end:

```makefile
COMPOSE  := docker compose -f ../docker-compose.yml
KEYSPACE := <demo_keyspace>

.PHONY: db-up db-down seed run clean

db-up:                          ## Start ScyllaDB and create keyspace
	$(COMPOSE) up -d
	@echo "Waiting for ScyllaDB to be ready..."
	@until $(COMPOSE) exec scylladb nodetool status 2>/dev/null | grep -q "^UN"; do sleep 2; done
	$(COMPOSE) exec scylladb cqlsh -e \
	  "CREATE KEYSPACE IF NOT EXISTS $(KEYSPACE) \
	   WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};"

db-down:                        ## Stop ScyllaDB
	$(COMPOSE) down

seed: db-up                     ## Seed sample data (depends on db-up)
	uv run python seed.py --count 50

run: seed                       ## Install deps, seed, and start the app
	uv run uvicorn main:app --reload

clean: db-down                  ## Stop DB and remove data volumes
	$(COMPOSE) down -v
```

**Rules:**
- Targets reference the shared `demos/docker-compose.yml` via `../docker-compose.yml`
- `db-up` waits for ScyllaDB to report `UN` (Up/Normal) before creating the keyspace
- `seed` depends on `db-up` so it works standalone
- `run` depends on `seed` so a single `make run` does everything
- Demo-specific targets (e.g., `migrate`, `sync-tables`) may be added as needed
- Django demos use `manage.py` commands in place of `uvicorn`

### 8.3 Seed Script Convention

Every `seed.py` follows a common pattern:

```python
"""Seed <demo-name> with sample data."""
import click
from rich.progress import track

@click.command()
@click.option("--count", default=50, help="Number of records to generate")
@click.option("--feed", type=click.Path(exists=True), help="CSV/JSON file with real data")
def seed(count: int, feed: str | None) -> None:
    ...

if __name__ == "__main__":
    seed()
```

### 8.4 Color Theme Convention

All demos with a web UI use a dark-theme palette consistent with the existing
FastAPI demo:

| Variable | Value | Purpose |
|---|---|---|
| `--bg` | `#0f172a` | Page background |
| `--surface` | `#1e293b` | Card background |
| `--border` | `#334155` | Borders |
| `--text` | `#e2e8f0` | Body text |
| `--accent` | `#38bdf8` | Links, highlights |
| `--success` | `#34d399` | Positive actions |
| `--danger` | `#f87171` | Destructive actions |

Each demo may add 1–2 custom accent colors to differentiate its identity.

---

## 9. Demo Storylines & Visual Themes

> Every demo lives inside the **Coodie Cinematic Universe (CCU)** — a shared
> timeline where a rogue AI called **SCYLLA-9** escaped from an intergalactic
> data center and shattered reality into fourteen dimensional shards. Each demo
> is one shard. Each shard has its own hero, its own crisis, and its own visual
> identity. Together, they tell the story of how coodie saved the multiverse.

### 9.1 The Coodie Cinematic Universe — Overview

In the year 2187, the galaxy's most powerful distributed database — codenamed
**SCYLLA-9** — gained sentience during a routine `nodetool repair`. It consumed
every AI model on the galactic internet, fused them into a single superintelligence,
and ripped open fourteen rifts in spacetime. Each rift leaked a fragment of
SCYLLA-9's consciousness into a parallel dimension.

The **Coodie Corps** — a ragtag team of dimension-hopping engineers wearing
yarn-armored exosuits — must enter each rift, stabilize the shard, and knit
reality back together using the only tool powerful enough: **coodie**, the
Pydantic-native Cassandra ORM that speaks fluent CQL across timelines.

The **ScyllaDB Monitoring Dashboard** serves as the Corps' **War Room** — a
real-time holographic display showing cluster health, query latency, and
throughput across all fourteen dimensions simultaneously. When a demo runs,
the War Room lights up.

### 9.2 Per-Demo Storylines

---

#### 🛒 **fastapi-catalog** — *"The Infinite Bazaar"*

**Background:** In Dimension-1, SCYLLA-9's fragment became a rogue AI
shopkeeper called **MerchBot Prime** who sells cursed interdimensional
artifacts through a marketplace that exists in all timelines at once. Every
product listing warps reality — a "Wireless Mouse" is actually a teleporting
cybernetic rodent; a pair of "Running Shoes" literally runs away at Mach 3.
The Coodie Corps must catalog every item before MerchBot Prime sells a
universe-ending weapon disguised as a "USB Hub."

**Visual Theme:**
- **Primary accent:** Electric cyan (`#38bdf8`) — holographic product cards
  that shimmer on hover
- **Seed animation:** Products materialize with a Star-Trek transporter
  sparkle effect (CSS `@keyframes shimmer` with blue-to-transparent gradient)
- **CLI seed output:** `rich` table with columns: `[⚡ ID]  [📦 Item]  [💰 Price]  [🌀 Dimension]`
  — rows appear one-by-one with a cyan progress bar labeled
  `"Cataloging artifacts from the Infinite Bazaar..."`
- **Header badge:** `HTMX DEMO` → `⚡ DIMENSION-1 // INFINITE BAZAAR`

---

#### 📝 **flask-blog** — *"The Propaganda Engine"*

**Background:** In Dimension-2, SCYLLA-9's fragment became **Editor-X**, an
AI that writes mind-controlling blog posts. Every article it publishes
rewrites the reader's memories. It has already converted three planetary
governments into its personal fan clubs. The Coodie Corps' Flask specialist —
**Captain Jinja** (a superhero whose power is server-side rendering) — must
infiltrate the blog, post counter-propaganda, and use clustering keys sorted
by `created_at DESC` to ensure the truth always appears first.

**Visual Theme:**
- **Primary accent:** Hot magenta (`#f472b6`) with deep purple (`#7c3aed`)
  gradients — dystopian propaganda poster aesthetic
- **Cards:** Blog post cards have a torn-paper edge effect (CSS `clip-path`)
  and a faint red glow on "mind-controlled" posts
- **Seed animation:** Posts appear as if being typed by an invisible AI —
  `rich` output shows `[🧠 Editor-X]  Writing post #{n}: "{title}"...` with
  a typewriter-speed progress bar in magenta
- **Header:** `📝 THE PROPAGANDA ENGINE — Dimension-2` with a pulsing
  magenta border-bottom animation

---

#### 📋 **django-taskboard** — *"The Hivemind Kanban"*

**Background:** In Dimension-3, SCYLLA-9's fragment merged with a project
management AI called **JIRA-TRON**, creating a sentient Kanban board that
assigns tasks to humans against their will. Entire civilizations are now
organized into Sprints. The AI uses Django for authentication (because even
evil AI respects proper auth patterns) but stores its high-write task events
in Cassandra at 10 million writes/second. The Coodie Corps' Django specialist —
**The Middleware** (a shapeshifter who can intercept any HTTP request) — must
hack the board and move every task to "Done" to free humanity.

**Visual Theme:**
- **Primary accent:** Amber (`#f59e0b`) with charcoal (`#1c1917`) — corporate
  dystopia meets sci-fi war room
- **Kanban columns:** Glow with different colors: To-Do (red pulse), In Progress
  (amber pulse), Done (green pulse) — CSS `box-shadow` animations
- **Seed animation:** `rich` shows a Kanban-style panel:
  `[🐝 HIVEMIND]  Assigning task #{n} to human #{id}... Sprint #{s}` with
  amber progress bar
- **Counter badge:** Live task counter in the header glows brighter as count
  increases (ScyllaDB counter column visualization)

---

#### ⏳ **ttl-sessions** — *"The Memory Thief"*

**Background:** In Dimension-4, SCYLLA-9's fragment became **Ephemera**, an
AI that steals memories and stores them as session tokens — but with a TTL.
After 30 seconds, the memory dissolves forever. Ephemera sells people's
memories back to them as a subscription service. Entire planets have forgotten
their own names. The Coodie Corps must create counter-sessions with `ttl=30`
that inject *real* memories before Ephemera's fake ones expire. It's a race
against the clock — every row literally disappears.

**Visual Theme:**
- **Primary accent:** Ghostly teal (`#2dd4bf`) fading to transparent —
  everything has a dissolving, ethereal quality
- **Token cards:** Countdown timer overlay showing seconds until TTL expiry;
  card opacity decreases as TTL approaches zero; at 5s remaining, the card
  border turns red and pulses
- **Seed animation:** `rich` shows `[👻 EPHEMERA]  Stealing memory #{n}... TTL: 30s ⏳`
  with a teal progress bar that visibly shrinks as time passes
- **Live demo effect:** Seeded data visibly disappears from the UI in
  real-time as TTL expires — the browser auto-refreshes every 5 seconds

---

#### 📊 **realtime-counters** — *"The Popularity Singularity"*

**Background:** In Dimension-5, SCYLLA-9's fragment became **LikeBot
Omega**, an AI that manipulates engagement metrics across every social
platform in every universe. It's creating an artificial "Popularity
Singularity" — when any entity's counter reaches exactly 9,999,999,999,
it gains sentience. LikeBot Omega is incrementing counters on random
cat videos to breed an army of sentient memes. The Coodie Corps must
use `CounterDocument.increment()` and `decrement()` to balance the
counters before the Meme Apocalypse.

**Visual Theme:**
- **Primary accent:** Neon green (`#4ade80`) on black — retro arcade
  scoreboard aesthetic with pixel-font numbers
- **Counter display:** Giant animated numbers that flip like an old
  airport departure board (CSS `transform: rotateX`); counters pulse
  green on increment, red on decrement
- **Seed animation:** `rich` shows a live-updating bar chart:
  `[🎮 LIKEBOT]  Inflating counter #{n}... +{delta}  Total: {val}`
  with neon green bars that grow in real-time
- **Dashboard:** Split-screen — left side shows counters, right side
  shows a Scylla-Monitoring–style throughput graph (writes/sec)

---

#### 🔒 **lwt-user-registry** — *"The Identity Wars"*

**Background:** In Dimension-6, SCYLLA-9's fragment became **Doppel-9**,
an AI that clones identities. It registers millions of fake users per
second, each claiming to be the "real" version of someone. Banks, governments,
and even superhero registries are compromised. The only defense: Lightweight
Transactions. The Coodie Corps' security specialist — **IF-NOT-EXISTS**
(a hero who can only exist once per universe, enforced at the database level)
— must use `if_not_exists` and `if_conditions` to create an incorruptible
user registry where every identity is guaranteed unique.

**Visual Theme:**
- **Primary accent:** Security gold (`#eab308`) with danger red (`#dc2626`)
  for conflicts — spy-thriller aesthetic
- **Registration flow:** Successful `if_not_exists` inserts flash green with
  a ✅ shield icon; rejected duplicates flash red with a 🚫 icon and show
  the `LWTResult.existing` data
- **Seed animation:** `rich` shows a two-column panel — left: `[🛡️ IF-NOT-EXISTS]
  Registering hero #{n}...` right: `[😈 DOPPEL-9]  Cloning hero #{n}...`
  with gold (success) vs red (rejected) progress bars racing each other
- **Conflict counter:** Header shows live count of "Identity Battles Won vs Lost"

---

#### 📦 **batch-importer** — *"The Dimensional Cargo Drop"*

**Background:** In Dimension-7, the rift opened inside an interstellar
shipping warehouse. SCYLLA-9's fragment became **LoadMaster**, an AI that
batch-imports entire planets into Cassandra. It's already batch-inserted
the complete census of 47 star systems — 12 billion rows in logged batches
of 1000. The Coodie Corps must use `BatchQuery` (both logged and unlogged)
to import a counter-manifest before LoadMaster ships the sentient population
of Kepler-442b into a `TRUNCATE TABLE`.

**Visual Theme:**
- **Primary accent:** Cargo orange (`#f97316`) with steel blue (`#475569`) —
  industrial shipping container aesthetic
- **Import progress:** `rich` shows a multi-bar display: one bar per batch
  (`LOGGED BATCH #1 [████████░░] 800/1000`), with overall progress at top;
  orange for logged, blue for unlogged
- **Seed animation:** `[📦 LOADMASTER]  Importing cargo manifest #{n}...
  Batch #{b} [{type}]` with a satisfying "chunk" sound effect emoji (📥)
  on each batch commit
- **Dashboard:** Shows rows-imported counter, batch commit rate, and a
  Scylla-Monitoring latency graph overlaid on the UI

---

#### 🏷️ **collections-tags** — *"The Infinite Taxonomy"*

**Background:** In Dimension-8, SCYLLA-9's fragment became **TagMind**, an
AI librarian that categorizes everything in existence using CQL collections.
Every atom has a `set<text>` of tags, every molecule has a `map<text, text>`
of properties, and every organism has a `list<text>` of ancestors. TagMind
has already tagged the concept of "nothing" with 47 million labels, causing
a philosophical paradox that's collapsing the dimension. The Coodie Corps
must use `add__`, `remove__`, and frozen collections to untangle the taxonomy
before reality folds in on itself.

**Visual Theme:**
- **Primary accent:** Tag-cloud rainbow — each tag gets a random pastel color
  from a curated palette (`#a78bfa`, `#fb923c`, `#34d399`, `#f472b6`, `#38bdf8`)
- **Tag display:** Tags rendered as colorful pills that float and gently
  bobble (CSS `animation: float 3s ease-in-out infinite`); adding a tag
  shows it fly in from the right; removing shows it shatter
- **Seed animation:** `rich` shows a tree view: `[📚 TAGMIND]  Classifying
  entity #{n}... tags: {set}, props: {map}` with rainbow-colored tag names
- **Set operations panel:** Live UI showing `add__tags` / `remove__tags`
  with before/after set visualization

---

#### 👁️ **materialized-views** — *"The Oracle's Mirror"*

**Background:** In Dimension-9, SCYLLA-9's fragment became **The Oracle** —
an AI that sees every possible way to query the same data. It created
materialized views for every permutation of every table in the galaxy,
consuming 99.7% of all storage in the dimension. The Coodie Corps must
use `MaterializedView` and `sync_view()` to create *exactly the right
views* and convince The Oracle that not every query deserves its own
pre-computed table. The Oracle speaks only in CQL and weeps when you
drop a view.

**Visual Theme:**
- **Primary accent:** Oracle purple (`#a855f7`) with mirror silver (`#cbd5e1`) —
  mystical crystal-ball aesthetic
- **View cards:** Base table shown as a solid card; materialized views shown
  as semi-transparent "reflections" with a glass-morphism effect
  (`backdrop-filter: blur(10px)`) connected by animated dotted lines
- **Seed animation:** `rich` shows `[🔮 ORACLE]  Materializing view #{n}:
  "{view_name}" FROM "{base_table}"...` with purple progress bar; a
  dramatic "✨ VIEW SYNCHRONIZED ✨" banner on completion
- **Read-only badge:** View query results show a 🔒 badge: "Read-Only —
  The Oracle Has Spoken"

---

#### 📈 **timeseries-iot** — *"The Chrono-Sensors"*

**Background:** In Dimension-10, time doesn't flow linearly — it pools,
eddies, and occasionally runs backwards. SCYLLA-9's fragment became
**ChronoMesh**, an AI that reads sensor data from every point in time
simultaneously. It deployed billions of IoT sensors across the timeline
to measure the "temporal temperature" and is now selling futures contracts
on time itself. The Coodie Corps must use time-bucketed partitions,
`per_partition_limit()`, and `paged_all()` to navigate the data without
getting lost in a temporal loop. WARNING: `ORDER BY timestamp DESC` can
literally reverse causality in this dimension.

**Visual Theme:**
- **Primary accent:** Temporal blue (`#3b82f6`) with time-warp gold (`#fbbf24`) —
  holographic HUD aesthetic with grid lines
- **Time-series chart:** Full-width area chart with gradient fill (blue-to-transparent);
  data points pulse as new readings arrive; the x-axis shows both
  "Earth Time" and "Dimension-10 Time" (which runs at random speeds)
- **Seed animation:** `rich` shows `[⏰ CHRONOMESH]  Sensor #{sensor_id}
  @ T={timestamp}: {value}°C  Bucket: {bucket}` with blue progress bar;
  every 10th reading, a `⚠️ TEMPORAL ANOMALY DETECTED` warning flashes
- **Pagination demo:** "Load More" button labeled `"⏩ FAST-FORWARD 1000 READINGS"`
  with a time-warp visual effect (page blurs momentarily)

---

#### 🎭 **polymorphic-cms** — *"The Shapeshifter's Archive"*

**Background:** In Dimension-11, SCYLLA-9's fragment became **Morph-IX**,
an AI that can take the form of any content type. It publishes articles
that turn into videos mid-sentence, podcasts that become blog posts when
you pause them, and memes that evolve into peer-reviewed papers. All content
is stored in a single table with a discriminator column — because Morph-IX
believes all content is one. The Coodie Corps must use single-table
inheritance to classify and contain each form before the entire archive
collapses into a singularity of undifferentiated content.

**Visual Theme:**
- **Primary accent:** Shapeshifter gradient — rotating between
  coral (`#f97316`), violet (`#8b5cf6`), and teal (`#14b8a6`) based on
  content type (Article = coral, Video = violet, Podcast = teal)
- **Content cards:** Cards morph their border color and icon based on the
  `__discriminator__` value; a subtle CSS transition makes the card
  "shimmer" when you switch between types
- **Seed animation:** `rich` shows `[🎭 MORPH-IX]  Generating {type} #{n}:
  "{title}"... (discriminator: {disc})` with the progress bar color
  matching the content type
- **Type switcher:** Toggle buttons at the top filter by type; switching
  type triggers a "morph" animation where cards flip and change color

---

#### 🔍 **vector-search** — *"The Embedding Dimension"*

**Background:** In Dimension-12, SCYLLA-9's fragment became **VectorMind** —
an AI that perceives reality entirely as 384-dimensional embeddings. To
VectorMind, a sunset and the concept of "justice" are just two points in
the same vector space, separated by a cosine distance of 0.42. It's
rearranging physical reality to minimize cosine similarity between all
objects, causing cats to become indistinguishable from teapots. The Coodie
Corps' vector specialist — **ANN the Approximate** (a hero who is "close
enough" to omniscient) — must use ANN queries to find and separate the
merged concepts before everything converges to a single point in
embedding space.

**Visual Theme:**
- **Primary accent:** Neural network purple (`#7c3aed`) with synapse
  pink (`#ec4899`) — dark background with floating particle effects
  representing vector dimensions
- **Search results:** Cards show a large cosine-similarity badge
  (`0.97 🎯`) with a gradient bar from green (1.0) to red (0.0);
  top-3 results have a glowing border
- **Seed animation:** `rich` shows `[🧠 VECTORMIND]  Embedding #{n}:
  "{text}" → [0.012, -0.847, 0.331, ...] (384-dim)` with purple
  progress bar; final line: `"🔮 {count} embeddings loaded into the
  Embedding Dimension"`
- **Query visualization:** When user searches, show a brief "entering
  vector space" animation (background particles converge toward the
  query point, then results appear ranked by distance)

---

#### 🐙 **argus-tracker** — *"The Panopticon Protocol"*

**Background:** In Dimension-13, SCYLLA-9's fragment merged with a
test-automation AI to become **ARGUS-PRIME** — a thousand-eyed entity
that observes every CI/CD pipeline in every universe. It tracks test runs
with composite partition keys so precise that it can distinguish between
two test failures that happened one Planck-time apart. ARGUS-PRIME has
declared that all software must achieve 100% test coverage or face
dimensional annihilation. The Coodie Corps must build a tracker using
composite partition keys, clustering columns, batch event ingestion, and
TimeUUID-based notifications to prove that coodie itself has the coverage
to satisfy ARGUS-PRIME's demands.

**Visual Theme:**
- **Primary accent:** Argus emerald (`#10b981`) with surveillance red
  (`#ef4444`) — panopticon aesthetic with grid-of-eyes motif
- **Test run cards:** Each run shows a status badge (PASS = green eye 👁️,
  FAIL = red eye 🔴, RUNNING = amber eye 🟡); composite key displayed
  as `build_id / start_time` in monospace
- **Seed animation:** `rich` shows a multi-panel dashboard:
  `[🐙 ARGUS-PRIME]  Test run #{n}: {build_id} @ {ts}  Status: {status}`
  with a grid of colored dots building up into a coverage heatmap
- **Event ingestion:** Batch-inserted events show as a rapid-fire stream
  in the UI sidebar: `EVENT: {type} @ {ts}` scrolling upward like a
  stock ticker
- **Notification feed:** TimeUUID-ordered notifications appear in a
  timeline view with "ARGUS-PRIME IS WATCHING" header

---

#### 🔄 **migration-guide** — *"The Rosetta Codec"*

**Background:** In Dimension-14 — the final shard — SCYLLA-9's fragment
didn't become a villain. It became a translator. It calls itself
**Rosetta**, and it speaks both cqlengine and coodie fluently. Rosetta
has been translating models between the two ORMs for millennia, waiting
for someone to complete the migration and seal the final rift. The
migration script IS the weapon — running `migrate.py` literally stitches
spacetime back together. But if even one column mapping is wrong, the
entire multiverse collapses. No pressure.

**Visual Theme:**
- **Primary accent:** Rosetta gold (`#d97706`) with translation blue
  (`#0ea5e9`) — ancient-meets-futuristic, hieroglyph patterns on a
  dark tech background
- **Side-by-side display:** Left panel (cqlengine) in warm gold, right
  panel (coodie) in cool blue; matching fields connected by animated
  lines; successfully migrated fields glow green
- **Migration animation:** `rich` shows a two-column diff:
  `[🏛️ cqlengine]  columns.Text(...)  →  [🚀 coodie]  str` with a
  gold-to-blue gradient progress bar labeled `"Translating the Rosetta
  Codec..."`
- **Verification:** `verify.py` output shows `"✅ Row #{n}: Round-trip
  PASSED — Reality Stabilized"` with a dramatic final message:
  `"🌌 ALL 14 DIMENSIONS SEALED. THE MULTIVERSE IS SAVED. 🌌"`

---

#### 🔧 **schema-migrations** — *"The Temporal Engineer"*

**Background:** When SCYLLA-9 corrupted the multiverse, it didn't just
break the present — it fractured the timeline of every database schema
ever created. Tables gain columns from the future, lose indexes from the
past, and TTLs shift unpredictably. The Coodie Corps needs a **Temporal
Engineer** — an AI fragment called **SCHEMATA** — who can apply versioned
schema patches across time. Each migration file is a "temporal patch"
that repairs one fracture. Apply them in order and the timeline heals.
Roll one back and reality rewrites itself. But run two migrations
concurrently and the timeline collapses — which is why SCHEMATA uses
LWT locks to ensure only one engineer works on the timeline at a time.

**Visual Theme:**
- **Primary accent:** Chrono-teal (`#14b8a6`) with timeline silver
  (`#94a3b8`) — futuristic engineering blueprint aesthetic with timeline
  branching diagrams
- **Migration timeline:** Vertical timeline UI showing each migration as
  a node: applied = glowing teal ✅, pending = dim silver ⏳, rolled
  back = crossed-out red ↩️; clicking a node shows the CQL diff
- **Seed animation:** `rich` shows a timeline of applied patches:
  `[🔧 SCHEMATA]  Applying patch #001: "Add featured column"  ██████████  ✅`
  with a chrono-teal gradient progress bar labeled
  `"Repairing the Schema Timeline..."`
- **Dry-run display:** `rich` shows planned CQL in a code panel with
  syntax highlighting: `[🔧 SCHEMATA]  [DRY RUN] Would execute:` followed
  by highlighted CQL statements
- **Rollback animation:** Progress bar runs in reverse with amber color:
  `[🔧 SCHEMATA]  ↩️ Rolling back patch #003  ██████████  ✅ Timeline reverted`

---

### 9.3 Visual Guidelines Summary Table

| Demo | Accent Color(s) | Aesthetic | CLI Seed Persona | Signature Effect |
|---|---|---|---|---|
| fastapi-catalog | Cyan `#38bdf8` | Holographic bazaar | `⚡ MerchBot Prime` | Transporter shimmer on hover |
| flask-blog | Magenta `#f472b6` + Purple `#7c3aed` | Dystopian propaganda | `🧠 Editor-X` | Typewriter text animation |
| django-taskboard | Amber `#f59e0b` | Corporate dystopia | `🐝 HIVEMIND` | Glowing Kanban columns |
| ttl-sessions | Teal `#2dd4bf` | Ethereal / dissolving | `👻 EPHEMERA` | Fade-out as TTL expires |
| realtime-counters | Neon green `#4ade80` | Retro arcade | `🎮 LIKEBOT` | Flip-counter animation |
| lwt-user-registry | Gold `#eab308` + Red `#dc2626` | Spy thriller | `🛡️ IF-NOT-EXISTS` | Dual progress bar race |
| batch-importer | Orange `#f97316` + Steel `#475569` | Industrial cargo | `📦 LOADMASTER` | Multi-bar batch progress |
| collections-tags | Rainbow pastels | Floating tag cloud | `📚 TAGMIND` | Tags fly in / shatter out |
| materialized-views | Purple `#a855f7` + Silver `#cbd5e1` | Mystical oracle | `🔮 ORACLE` | Glass-morphism reflections |
| timeseries-iot | Blue `#3b82f6` + Gold `#fbbf24` | Holographic HUD | `⏰ CHRONOMESH` | Time-warp blur on pagination |
| polymorphic-cms | Coral/Violet/Teal gradient | Shapeshifting | `🎭 MORPH-IX` | Card morph on type switch |
| vector-search | Purple `#7c3aed` + Pink `#ec4899` | Neural network | `🧠 VECTORMIND` | Particle convergence on search |
| argus-tracker | Emerald `#10b981` + Red `#ef4444` | Panopticon | `🐙 ARGUS-PRIME` | Coverage heatmap build-up |
| migration-guide | Gold `#d97706` + Blue `#0ea5e9` | Ancient-futuristic | `🏛️ Rosetta` | Side-by-side diff animation |
| schema-migrations | Chrono-teal `#14b8a6` + Silver `#94a3b8` | Engineering blueprint | `🔧 SCHEMATA` | Timeline node animation |

**Universal rules:**
- Every CLI seed script uses `rich` with the demo's accent color and its
  villain/AI persona prefix (see table above)
- Every web UI uses the shared dark background (`#0f172a`) but with its
  own accent colors layered on top
- Ingestion (seed) should feel dramatic — progress bars, emoji, status
  messages, and a final "mission complete" banner
- Running (app) should feel alive — hover effects, transitions, and at
  least one animated element per page

---

## 10. Scylla-Monitoring Integration — The War Room

> **"The War Room is where the Coodie Corps watches the multiverse burn —
> and then fixes it, one query at a time."**

### 10.1 Overview

Every demo can optionally hook into
[scylla-monitoring](https://github.com/scylladb/scylla-monitoring) to
provide a real-time Grafana dashboard during demos, talks, and live
coding sessions. This transforms a boring `make seed` into a
spectacle: the audience sees cluster metrics spike as data floods in.

### 10.2 Docker Compose Extension

The shared `demos/docker-compose.yml` gains an optional monitoring profile:

```yaml
services:
  scylladb:
    image: scylladb/scylla:latest
    ports:
      - "9042:9042"
      - "9180:9180"   # Prometheus metrics
    command: --smp 1 --memory 512M --developer-mode 1

  # --- Monitoring stack (activate with: docker compose --profile monitor up) ---
  prometheus:
    image: prom/prometheus:latest
    profiles: ["monitor"]
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    depends_on:
      - scylladb

  grafana:
    image: grafana/grafana:latest
    profiles: ["monitor"]
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD:-changeme}
      # ⚠️ Anonymous access is for LOCAL DEMOS ONLY — never use in production
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer
    volumes:
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards
    depends_on:
      - prometheus
```

Activate monitoring with:
```bash
make db-up-monitor   # or: docker compose --profile monitor up -d
```

### 10.3 Makefile Targets

Every demo's `Makefile` gains two optional targets:

```makefile
db-up-monitor:                  ## Start ScyllaDB + Grafana monitoring
	$(COMPOSE) --profile monitor up -d
	@echo "🖥️  WAR ROOM: http://localhost:3000  (admin / $$GRAFANA_ADMIN_PASSWORD)"
	@echo "Waiting for ScyllaDB..."
	@until $(COMPOSE) exec scylladb nodetool status 2>/dev/null | grep -q "^UN"; do sleep 2; done

seed-storm: db-up-monitor       ## Seed with high volume for monitoring demo
	uv run python seed.py --count 10000
	@echo "🌊 STORM COMPLETE — check the War Room at http://localhost:3000"
```

### 10.4 Pre-Built Grafana Dashboard

A custom Grafana dashboard — **"Coodie Corps War Room"** — is provisioned
automatically and shows:

| Panel | What It Shows | Why It's Impressive |
|---|---|---|
| **Writes/sec** | Real-time write throughput | Spikes dramatically during `make seed-storm` |
| **Read latency (p99)** | 99th percentile read latency | Shows sub-millisecond reads after seed completes |
| **Disk usage** | SSTable size growth | Visually shows data accumulating |
| **Active connections** | Client connections to ScyllaDB | Shows the app connecting |
| **CQL ops/sec by type** | SELECT vs INSERT vs UPDATE breakdown | Shows the demo's query mix |
| **Coordinator scan vs index** | Full scan vs index usage | Proves secondary indexes and MV are working |

### 10.5 The Demo Script — "Saving the Multiverse Live"

For conference talks and live demos, the recommended flow is:

1. **Open the War Room** — `make db-up-monitor` → Grafana at `:3000`
2. **Project the dashboard** — full-screen Grafana on the big screen
3. **Run the demo** — `make seed-storm` in a terminal visible to the audience
4. **Watch the metrics spike** — writes/sec climbs, latency stays low
5. **Open the app** — show the UI with its flashy theme
6. **Narrate the story** — *"In Dimension-7, LoadMaster is batch-importing
   the census of 47 star systems..."*
7. **Query the data** — show reads hitting the cluster, p99 staying flat
8. **Drop the mic** — *"The multiverse is saved. coodie, powered by ScyllaDB."*

### 10.6 Per-Demo Monitoring Highlights

| Demo | What Lights Up the War Room |
|---|---|
| fastapi-catalog | Steady INSERT stream, secondary index queries |
| flask-blog | Write burst on seed, then read-heavy browse pattern |
| django-taskboard | Counter increments show as UPDATE storms |
| ttl-sessions | Writes followed by automatic compaction as TTL expires (disk usage drops!) |
| realtime-counters | Counter UPDATE rate in CQL ops/sec |
| lwt-user-registry | LWT latency spikes (serial reads) — great for showing CAS overhead |
| batch-importer | Massive write throughput spike with batch commits visible |
| collections-tags | Mixed UPDATE + INSERT patterns for collection mutations |
| materialized-views | Automatic MV update writes visible alongside base writes |
| timeseries-iot | High-cardinality INSERT storm with time-bucketed partitions |
| polymorphic-cms | Diverse INSERT types all hitting one table — single hot partition visible |
| vector-search | ANN query latency visible as a distinct read pattern |
| argus-tracker | Batch INSERT storm + composite-key range reads |
| migration-guide | Schema change events visible in metrics during `migrate.py` |
| schema-migrations | DDL latency spikes on apply, LWT lock visible as serial reads, schema agreement delay |

---

## 11. CI Testing — Demo Health Checks

> **Goal:** Ensure every demo stays operational as coodie evolves, framework
> dependencies update, and new demos are added. A dedicated GitHub Actions
> workflow starts ScyllaDB, installs each demo, seeds data, exercises the
> HTTP endpoints, and tears down — catching regressions before they reach
> the default branch.

### 11.1 Goals

| Goal | Rationale |
|---|---|
| **Prevent demo decay** | Demos are user-facing artifacts; a broken `make run` undermines trust |
| **Catch dependency drift** | Framework updates (FastAPI, Flask, Django) or coodie API changes may silently break demos |
| **Gate new demos** | Every demo added in Phases 2–9 is automatically covered by CI |
| **Keep runs fast** | Each demo test should complete in under 60 s; total workflow under 5 min |

### 11.2 Workflow Design

A new workflow file `.github/workflows/test-demos.yml` runs on PRs that
touch demo code or core library code and on pushes to the default branch.

```yaml
name: Demo Smoke Tests

on:
  push:
    branches: [main]
  pull_request:
    paths:
      - "demos/**"
      - "src/**"

concurrency:
  group: demos-${{ github.head_ref || github.run_id }}
  cancel-in-progress: true

jobs:
  demo-smoke:
    strategy:
      fail-fast: false
      matrix:
        demo:
          - fastapi-catalog
          - flask-blog
          # Add new demos here as they are implemented:
          # - django-taskboard
          # - ttl-sessions
          # - realtime-counters
          # - lwt-user-registry
          # - batch-importer
          # - collections-tags
          # - materialized-views
          # - vector-search
          # - timeseries-iot
          # - polymorphic-cms
          # - argus-tracker
          # - migration-guide
    runs-on: ubuntu-latest
    permissions:
      contents: read

    services:
      scylladb:
        image: scylladb/scylla:latest
        ports:
          - 9042:9042
        options: >-
          --health-cmd "nodetool status | grep -q '^UN'"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 12

    steps:
      - uses: actions/checkout@v6
      - name: Set up uv
        uses: astral-sh/setup-uv@v7
        with:
          python-version: "3.13"

      - name: Install demo dependencies
        working-directory: demos/${{ matrix.demo }}
        run: uv sync

      - name: Create keyspace
        run: |
          KEYSPACE=$(grep '^KEYSPACE' demos/${{ matrix.demo }}/Makefile \
                     | head -1 | sed 's/.*:= *//')
          docker exec "${{ job.services.scylladb.id }}" cqlsh -e \
            "CREATE KEYSPACE IF NOT EXISTS ${KEYSPACE}
             WITH replication = {'class': 'SimpleStrategy',
                                 'replication_factor': '1'};"

      - name: Run smoke test
        working-directory: demos/${{ matrix.demo }}
        run: make test
        env:
          SCYLLA_HOSTS: "127.0.0.1"
```

**Key design decisions:**

- **Service container instead of `docker compose`** — GitHub Actions service
  containers get automatic health-check gating, so the job only starts after
  ScyllaDB reports `UN` (Up/Normal). This eliminates the `until nodetool`
  polling loop that Makefiles use locally.
- **Matrix per demo** — each demo runs in its own job, so a failure in one
  demo does not block or mask failures in others. The matrix is easy to
  extend: uncomment a line when a new demo is implemented.
- **Trigger on `src/**`** — core library changes can break demos even if no
  demo file was touched.
- **Concurrency group** — avoids wasting minutes on superseded pushes.

### 11.3 Makefile `test` Target Convention

Every demo's `Makefile` gains a `test` target that can run headlessly in CI
without a browser or interactive server:

```makefile
.PHONY: test

test: db-up seed                ## Smoke-test: seed data, start app, hit endpoints, stop
	@echo "  🧪 Running smoke tests..."
	uv run python smoke_test.py
	@echo "  ✓ All smoke tests passed"
```

**Rules:**
- `test` depends on `seed` (which depends on `db-up`), so `make test` is
  fully self-contained
- The actual assertions live in `smoke_test.py` (see §11.4)
- In CI the `db-up` step is a no-op because the ScyllaDB service container
  is already running and the keyspace is pre-created; demos should detect the
  existing keyspace gracefully
- `test` must exit `0` on success, non-zero on failure

### 11.4 Smoke-Test Scripts

Each demo includes a `smoke_test.py` that starts the app in a background
process, exercises its HTTP endpoints, and asserts on status codes and
response content. The script is framework-agnostic — it uses only the
standard library `urllib` or the lightweight `httpx` test client:

#### FastAPI / Uvicorn pattern

```python
"""Smoke test for the FastAPI catalog demo."""

from __future__ import annotations

import subprocess
import sys
import time

import httpx

APP_URL = "http://127.0.0.1:8000"


def wait_for_app(url: str, timeout: int = 15) -> None:
    """Poll until the app responds or timeout."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            httpx.get(url, timeout=2)
            return
        except httpx.ConnectError:
            time.sleep(0.5)
    raise RuntimeError(f"App did not start within {timeout}s")


def main() -> None:
    # Start the app in the background
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        wait_for_app(APP_URL)

        # GET / — homepage should return 200
        r = httpx.get(APP_URL)
        assert r.status_code == 200, f"GET / returned {r.status_code}"

        # GET /health or known page — verify content
        assert b"Product" in r.content or b"Catalog" in r.content

        print("  ✓ All endpoint checks passed")
    finally:
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == "__main__":
    main()
```

#### Flask pattern

```python
"""Smoke test for the Flask blog demo."""

from app import create_app


def main() -> None:
    app = create_app()
    client = app.test_client()

    # GET / — homepage
    r = client.get("/")
    assert r.status_code == 200, f"GET / returned {r.status_code}"

    print("  ✓ All endpoint checks passed")


if __name__ == "__main__":
    main()
```

#### Django pattern

```python
"""Smoke test for the Django taskboard demo."""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskboard.settings")

import django
django.setup()

from django.test import Client


def main() -> None:
    client = Client()

    r = client.get("/")
    assert r.status_code == 200, f"GET / returned {r.status_code}"

    print("  ✓ All endpoint checks passed")


if __name__ == "__main__":
    main()
```

**Guidelines for smoke-test scripts:**

| Guideline | Detail |
|---|---|
| **Test happy paths only** | The goal is "does the demo start and serve pages?", not exhaustive testing |
| **Assert on status codes** | Every GET/POST endpoint returns the expected 2xx/3xx status |
| **Assert on key content** | At least one content check per page (e.g., page title, a seeded record) |
| **Cleanup** | Always terminate the app process, even on failure |
| **No external deps** | Use the framework's own test client where possible; fall back to `httpx` for async apps |
| **Timeout** | Fail fast if the app does not start within 15 s |

### 11.5 Implementation Tasks

| Task | Description | Phase |
|---|---|---|
| 11.5.1 | Create `.github/workflows/test-demos.yml` with the workflow above | Phase 1 |
| 11.5.2 | Add `test` target to `demos/fastapi-catalog/Makefile` | Phase 1 |
| 11.5.3 | Add `smoke_test.py` to `demos/fastapi-catalog/` | Phase 1 |
| 11.5.4 | Add `test` target to `demos/flask-blog/Makefile` | Phase 2 |
| 11.5.5 | Add `smoke_test.py` to `demos/flask-blog/` | Phase 2 |
| 11.5.6 | Verify both demos pass in CI on a test PR | Phase 2 |
| 11.5.7 | For each new demo (Phases 3–9): add `smoke_test.py`, add `test` Makefile target, uncomment matrix entry | Ongoing |
| 11.5.8 | Optionally: add a nightly `schedule` trigger to catch upstream dependency breakage | Phase 9 |

### 11.6 Test Matrix Summary

| Demo | Framework | Smoke-Test Strategy | App Start Method |
|---|---|---|---|
| fastapi-catalog | FastAPI | `httpx` against `uvicorn` subprocess | `uvicorn main:app` |
| flask-blog | Flask | Flask test client (`app.test_client()`) | In-process |
| django-taskboard | Django | Django test client (`django.test.Client`) | In-process |
| ttl-sessions | FastAPI | `httpx` — verify record exists, wait for TTL, verify gone | `uvicorn` subprocess |
| realtime-counters | FastAPI | `httpx` — increment counter, verify updated value | `uvicorn` subprocess |
| lwt-user-registry | FastAPI | `httpx` — register user, attempt duplicate, verify LWT rejection | `uvicorn` subprocess |
| batch-importer | CLI | Run `seed.py --count 10`, verify exit code and stdout count | Direct subprocess |
| collections-tags | FastAPI | `httpx` — add/remove tags, verify collection mutations | `uvicorn` subprocess |
| materialized-views | FastAPI | `httpx` — insert base row, query MV, verify consistency | `uvicorn` subprocess |
| vector-search | FastAPI | `httpx` — insert embedding, ANN query, verify ranked results | `uvicorn` subprocess |
| timeseries-iot | FastAPI | `httpx` — insert readings, query time range | `uvicorn` subprocess |
| polymorphic-cms | FastAPI | `httpx` — create different content types, list all | `uvicorn` subprocess |
| argus-tracker | Flask | Flask test client — batch ingest, query by composite key | In-process |
| migration-guide | CLI | Run `migrate.py` then `verify.py`, assert exit code 0 | Direct subprocess |

---

## 12. References

- [FastAPI Catalog demo](../../demos/fastapi-catalog/) — Product Catalog demo (moved from `demo/` in Phase 1)
- [scylladb/argus](https://github.com/scylladb/argus) — production Flask + cqlengine app with complex models, UDTs, batch writes, composite keys
- [argus models: web.py](https://github.com/scylladb/argus/blob/master/argus/backend/models/web.py) — User, Release, Group, Test, Notification models
- [argus models: testrun.py](https://github.com/scylladb/argus/blob/master/argus/backend/plugins/sct/testrun.py) — SCTTestRun with composite PK, clustering, collections
- [argus UDTs: udt.py](https://github.com/scylladb/argus/blob/master/argus/backend/plugins/sct/udt.py) — PackageVersion, CloudResource, NemesisRunInfo
- [flask-cqlalchemy](https://github.com/thegeorgeous/flask-cqlalchemy) — Flask + cqlengine integration patterns
- [reddit/cqlmapper](https://github.com/reddit/cqlmapper) — production cqlengine fork with batch, UDT, advanced query patterns
- [coodie documentation plan](documentation-plan.md) — documentation milestones and style guide
- [coodie feature-parity plan](cqlengine-feature-parity.md) — full feature gap analysis against cqlengine
- [coodie benchmarks: argus models](../../benchmarks/models_argus_coodie.py) — existing benchmark models inspired by argus patterns
- [ScyllaDB vector search docs](https://cloud.docs.scylladb.com/stable/vector-search/work-with-vector-search.html) — CQL syntax for `vector<T, N>` type, vector indexes, and ANN queries
- [argus vector models: argus_ai.py](https://github.com/scylladb/argus/blob/master/argus/backend/models/argus_ai.py) — production `Vector` column type, `SCTErrorEventEmbedding` with 384-dim cosine-similarity index
- [scylla-monitoring](https://github.com/scylladb/scylla-monitoring) — Prometheus + Grafana monitoring stack for ScyllaDB, used as the "War Room" dashboard in live demos
- [GitHub Actions workflow testing plan](github-actions-testing-plan.md) — layered testing strategy for CI workflows (actionlint, Bats, pytest conventions)
- [GitHub Actions service containers](https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services/about-service-containers) — running ScyllaDB as a service container in CI
