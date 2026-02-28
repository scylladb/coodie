---
name: cqlengine-migration
description: >-
  Guides migration of Python codebases from cassandra.cqlengine (or other
  Cassandra ORM/ODM libraries) to coodie. Use when converting cqlengine
  models, queries, batch operations, UDTs, or connection setup to coodie,
  or when identifying gotchas and breaking changes during ORM migration.
---

# cqlengine → coodie Migration

Systematically migrate a cqlengine (or other Cassandra ORM) application to coodie
using phased, verifiable steps.

> **Pre-requisite:** Follow [setup-environment.md](../setup-environment.md)
> for environment bootstrapping and commit conventions.

## Essential Principles

<essential_principles>

<principle name="models-first-queries-last">
**Migrate model definitions before touching any query or CRUD code.**

Models are the foundation — every query, save, and batch operation depends on
the model class compiling correctly with Pydantic v2. Converting queries while
models still use `columns.*` produces cascading errors that are hard to debug.
Always get models green (importable, no validation errors) before changing any
runtime code.
</principle>

<principle name="one-model-at-a-time">
**Convert and test one model at a time; never batch-convert an entire module.**

cqlengine models often have subtle interactions (shared keyspace, cross-model
queries, batch operations spanning models). Converting one model, running the
existing test suite, and verifying parity before moving to the next prevents
compound errors and makes `git bisect` useful.
</principle>

<principle name="pydantic-defaults-differ">
**Fields without a default are required in coodie (Pydantic v2), unlike cqlengine.**

In cqlengine, `columns.Text()` without `required=True` is optional — it
defaults to `None` and Cassandra stores a null. In coodie, a bare `name: str`
is **required** and Pydantic raises `ValidationError` if omitted. Always audit
every field: if it was optional in cqlengine, add `= None` or
`Optional[T] = None`.
</principle>

<principle name="settings-not-dunders">
**Table metadata moves from class-level dunders to an inner `Settings` class.**

cqlengine uses `__table_name__`, `__keyspace__`, `__default_ttl__`,
`__options__`, etc. as class attributes. coodie moves them all into a nested
`Settings` class. Forgetting this causes table-not-found or wrong-keyspace
errors at runtime.
</principle>

<principle name="async-is-same-model">
**The model definition is identical for sync and async — only the import changes.**

`from coodie.sync import Document` vs `from coodie.aio import Document`.
All terminal methods (`save()`, `get()`, `find().all()`, etc.) become
`await`-able in async mode. Do not create separate model classes for
sync/async.
</principle>

</essential_principles>

## When to Use

- Converting `cassandra.cqlengine` models/queries to coodie
- Migrating from another Cassandra ORM (e.g. cqlengine forks, custom abstractions)
- Identifying breaking changes and gotchas before starting migration
- Reviewing a migration PR for completeness
- Estimating effort for migrating an existing cqlengine codebase

## When NOT to Use

- **Schema evolution** (adding/dropping columns in production) — use the coodie
  migration system (see `docs/plans/migration-strategy.md`)
- **Writing new coodie models from scratch** — use the coodie documentation
  guides directly (`docs/source/guide/`)
- **Performance tuning** — use the `benchmarks` skill
- **Test refactoring** — use the `test-refactoring` skill

## Migration Decision Tree

```
What are you migrating?
│
├─ A cqlengine Model class?
│  └─ Phase 1: Convert model (see type-mapping reference)
│     Then Phase 2: Convert queries
│
├─ Connection setup / session management?
│  └─ Phase 1: Replace connection.setup() → init_coodie()
│
├─ Batch operations?
│  └─ Phase 2: Convert BatchQuery usage
│
├─ User-Defined Types?
│  └─ Phase 1: Convert UserType + sync_type() calls
│
├─ Custom management / sync_table calls?
│  └─ Phase 1: Replace management.sync_table(M) → M.sync_table()
│
└─ Entire application?
   └─ Follow the full workflow: workflows/migrate-cqlengine-app.md
```

## Transformation Quick Reference

### Imports

| cqlengine | coodie |
|-----------|--------|
| `from cassandra.cqlengine.models import Model` | `from coodie.sync import Document` or `from coodie.aio import Document` |
| `from cassandra.cqlengine import columns` | `from typing import Annotated` + `from coodie.fields import ...` |
| `from cassandra.cqlengine import connection` | `from coodie.sync import init_coodie` or `from coodie.aio import init_coodie` |
| `from cassandra.cqlengine.management import sync_table` | _(not needed — use `Document.sync_table()`)_ |
| `from cassandra.cqlengine.query import BatchQuery` | `from coodie.sync import BatchQuery` or `from coodie.aio import AsyncBatchQuery` |
| `from cassandra.cqlengine.usertype import UserType` | `from coodie.usertype import UserType` |

### Model Class

| cqlengine | coodie |
|-----------|--------|
| `class M(Model):` | `class M(Document):` |
| `__table_name__ = "t"` | `class Settings: name = "t"` |
| `__keyspace__ = "ks"` | `class Settings: keyspace = "ks"` |
| `__default_ttl__ = 3600` | `class Settings: __default_ttl__ = 3600` |
| `__options__ = {...}` | `class Settings: __options__ = {...}` |

### CRUD Operations

| cqlengine | coodie (sync) | coodie (async) |
|-----------|---------------|----------------|
| `M.create(**kw)` | `M(**kw).save()` _or_ `M.create(**kw)` | `await M(**kw).save()` _or_ `await M.create(**kw)` |
| `M.objects.all()` | `M.find().all()` | `await M.find().all()` |
| `M.objects.filter(k=v)` | `M.find(k=v).all()` | `await M.find(k=v).all()` |
| `M.objects.get(pk=v)` | `M.get(pk=v)` | `await M.get(pk=v)` |
| `M.objects.filter(pk=v).first()` | `M.find_one(pk=v)` | `await M.find_one(pk=v)` |
| `M.objects.count()` | `M.find().count()` | `await M.find().count()` |
| `M.objects.filter().limit(n)` | `M.find().limit(n).all()` | `await M.find().limit(n).all()` |
| `M.objects.order_by("-col")` | `M.find().order_by("-col").all()` | `await M.find().order_by("-col").all()` |
| `M.objects.allow_filtering()` | `M.find().allow_filtering().all()` | `await M.find().allow_filtering().all()` |
| `obj.field = val; obj.save()` | `obj.update(field=val)` | `await obj.update(field=val)` |
| `obj.delete()` | `obj.delete()` | `await obj.delete()` |
| `M.objects.filter().update(f=v)` | `M.find().update(f=v)` | `await M.find().update(f=v)` |
| `M.objects.filter().delete()` | `M.find().delete()` | `await M.find().delete()` |

### Exception Mapping

| cqlengine | coodie |
|-----------|--------|
| `Model.DoesNotExist` | `coodie.exceptions.DocumentNotFound` |
| `Model.MultipleObjectsReturned` | `coodie.exceptions.MultipleDocumentsReturned` |

## Gotchas Quick Reference

The most common migration pitfalls. Full details in [gotchas.md](references/gotchas.md).

| # | Gotcha | Impact | Fix |
|---|--------|--------|-----|
| 1 | No `Model.objects` attribute | `AttributeError` at runtime | Replace `.objects.filter()` → `.find()` |
| 2 | Fields without defaults are **required** | `ValidationError` on instantiation | Add `= None` / `Optional[T] = None` for optional fields |
| 3 | `__table_name__` as class attribute ignored | Table created with wrong name | Move to `class Settings: name = "..."` |
| 4 | `columns.Text()` → `str` (not `Optional[str]`) | Required vs optional mismatch | Audit every field's optionality |
| 5 | `Model.create()` vs `Model().save()` | API difference | coodie supports both — `create()` is a classmethod |
| 6 | `sync_table(M)` function call | `NameError` — no management module | Use `M.sync_table()` class method |
| 7 | `connection.setup()` signature differs | Connection fails | Use `init_coodie(hosts=[...], keyspace="...")` |
| 8 | Batch API difference | Wrong batch context usage | Use `obj.save(batch=batch)`, not `Model.batch(b).create()` |
| 9 | `DoesNotExist` exception class moved | Uncaught exceptions | Import `DocumentNotFound` from `coodie.exceptions` |
| 10 | `default=callable` → `Field(default_factory=callable)` | Pydantic shares mutable default | Use `Field(default_factory=...)` for callables |
| 11 | Collections need `Field(default_factory=...)` | Pydantic validation error | `list[str] = Field(default_factory=list)` |
| 12 | `columns.UserDefinedType(Addr)` wrapper removed | Unnecessary wrapper | Use the UDT class directly as type annotation |
| 13 | Counter columns require `CounterDocument` | Cannot mix counter/non-counter | Inherit from `CounterDocument`, use `increment()`/`decrement()` |
| 14 | `clustering_order` on column → `ClusteringKey(order=)` | Wrong CQL generated | Use `Annotated[T, ClusteringKey(order="DESC")]` |
| 15 | `partition_key=True` → `PrimaryKey(partition_key_index=N)` | Composite partition key wrong | Use index parameter for multi-column partition keys |

## Reference Index

| File | Content |
|------|---------|
| [type-mapping.md](references/type-mapping.md) | Complete cqlengine column → coodie type mapping table |
| [gotchas.md](references/gotchas.md) | Comprehensive gotchas with examples and fixes |
| [checklist.md](references/checklist.md) | Step-by-step migration checklist |

| Workflow | Purpose |
|----------|---------|
| [migrate-cqlengine-app.md](workflows/migrate-cqlengine-app.md) | 5-phase process for migrating a full cqlengine application |

## Success Criteria

A well-migrated codebase:

- [ ] No imports from `cassandra.cqlengine` remain
- [ ] All models inherit from `Document` (not `Model`)
- [ ] All field types use Python type annotations (no `columns.*`)
- [ ] Table metadata is in `Settings` inner class (no `__table_name__` dunders)
- [ ] All queries use `.find()` / `.get()` / `.find_one()` (no `.objects`)
- [ ] All optional fields have explicit defaults (`= None` or `Optional[T] = None`)
- [ ] Connection setup uses `init_coodie()` (not `connection.setup()`)
- [ ] Batch operations use `obj.save(batch=batch)` pattern
- [ ] UDTs use plain type annotations (no `columns.UserDefinedType()` wrapper)
- [ ] Existing test suite passes against coodie
