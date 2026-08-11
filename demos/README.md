# coodie Demo Suite

> A collection of standalone demo applications showcasing **coodie** — the
> Pydantic-native Cassandra/ScyllaDB ORM — across different frameworks and
> Cassandra features.

## Quick Start

Every demo is self-contained. Pick one, `cd` into its folder, and run:

```bash
make run
```

This single command starts ScyllaDB (via Docker Compose), creates the keyspace,
seeds sample data, and launches the app.

## Prerequisites

* Python ≥ 3.10
* [uv](https://docs.astral.sh/uv/) (recommended) or pip
* Docker & Docker Compose (for ScyllaDB)

## Demos

| Demo | Framework | Features Shown | Directory |
|---|---|---|---|
| 🛒 Product Catalog | FastAPI + HTMX | Async CRUD, secondary indexes, clustering order, Jinja2 templates, seed data | [`fastapi-catalog/`](fastapi-catalog/) |
| 📝 Blog | Flask + Jinja2 | Sync CRUD, clustering keys (newest-first), secondary indexes, tags (list field), seed data | [`flask-blog/`](flask-blog/) |
| 🐝 Task Board | Django | Sync API, dual-database pattern, counter columns, Kanban UI | [`django-taskboard/`](django-taskboard/) |
| 🔮 Materialized Views | FastAPI + HTMX | `MaterializedView`, `sync_view()`, read-only queries, auto-updating views | [`materialized-views/`](materialized-views/) |
| 📊 Realtime Counters | FastAPI + HTMX | `CounterDocument`, `increment()`, `decrement()`, live analytics dashboard | [`realtime-counters/`](realtime-counters/) |
| 🔧 Schema Migrations | FastAPI | `coodie migrate` CLI, apply/rollback/dry-run, `_coodie_migrations` state tracking, migration file authoring | [`schema-migrations/`](schema-migrations/) |
| 🐙 Argus Test Tracker | CLI | Composite PK + clustering, compound partition keys, TimeUUID notifications, batch ingestion, prepared-statement caching, partition-scoped queries | [`argus-tracker/`](argus-tracker/) |

## Shared Infrastructure

All demos share a single ScyllaDB container defined in
[`docker-compose.yml`](docker-compose.yml). Each demo's `Makefile` references
this shared file via `../docker-compose.yml`.

### Standard Makefile Targets

| Target | Description |
|---|---|
| `make db-up` | Start ScyllaDB and create the demo's keyspace |
| `make db-down` | Stop ScyllaDB |
| `make seed` | Seed sample data (depends on `db-up`) |
| `make run` | Install deps, seed data, and start the app |
| `make clean` | Stop DB and remove data volumes |

## Adding a New Demo

1. Create a folder under `demos/<name>/`
2. Add `pyproject.toml`, `README.md`, `Makefile`, `models.py`, `seed.py`
3. Follow the Makefile convention above
4. Update this README's demo table
