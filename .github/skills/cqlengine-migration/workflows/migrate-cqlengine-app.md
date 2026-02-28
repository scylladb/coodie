# Workflow: Migrate a cqlengine Application to coodie

A phased process for converting a full cqlengine application to coodie. Each
phase has entry criteria, numbered steps, and exit criteria.

---

## Phase 1: Preparation & Inventory

**Entry criteria:** You have access to the cqlengine codebase and a working
test suite (or at least a way to run the application).

1. **Find all cqlengine imports** — search for `cassandra.cqlengine` across the
   codebase:
   ```
   grep -rn "cassandra\.cqlengine" src/ --include="*.py"
   ```
2. **List all models** — find every `class X(Model):` definition:
   ```
   grep -rn "class.*Model\b" src/ --include="*.py"
   ```
3. **List all UDTs** — find every `class X(UserType):` definition:
   ```
   grep -rn "class.*UserType\b" src/ --include="*.py"
   ```
4. **Identify connection setup** — find `connection.setup()` calls.
5. **Identify batch usage** — find `BatchQuery` imports and usage.
6. **Check for unsupported features** — review each model for:
   - Static columns (`static=True`)
   - Token-range queries (`__token`)
   - Custom management scripts
   - Per-model `__connection__`
   - Counter columns
7. **Create a migration tracking document** — list every model/UDT with status
   (pending / in-progress / done / verified).

**Exit criteria:** You have a complete inventory of models, UDTs, queries, and
potential blockers. No code changes yet.

---

## Phase 2: Dependencies & Setup

**Entry criteria:** Inventory complete from Phase 1.

1. **Add coodie to dependencies:**
   ```bash
   uv add coodie  # or pip install coodie
   ```
2. **Verify coodie imports work:**
   ```python
   from coodie.sync import Document, init_coodie
   from coodie.fields import PrimaryKey, ClusteringKey, Indexed
   ```
3. **Set up a test database** — ensure you have a Cassandra/ScyllaDB instance
   for testing (local Docker or CI container).
4. **Create a feature branch** for the migration.

**Exit criteria:** coodie is installed, imports work, test database is available.

---

## Phase 3: Model Conversion (one at a time)

**Entry criteria:** Dependencies installed from Phase 2.

For each model (start with the simplest, work up to the most complex):

1. **Convert the model class** using the [type-mapping reference](../references/type-mapping.md):
   - Change base class: `Model` → `Document`
   - Convert all column definitions to type annotations
   - Convert key/index annotations
   - Move table metadata to `Settings` inner class
   - Set correct defaults for optional fields

2. **Convert any UDTs** that this model depends on:
   - Change base class: `cqlengine.UserType` → `coodie.usertype.UserType`
   - Convert fields to type annotations
   - Remove `columns.UserDefinedType()` wrappers

3. **Verify the model compiles:**
   ```bash
   python -c "from myapp.models import ConvertedModel"
   ```

4. **Run `sync_table()`** against the test database:
   ```python
   ConvertedModel.sync_table()
   ```

5. **Run existing tests** for this model — fix any failures.

6. **Commit** the converted model with a descriptive message:
   ```
   refactor(models): migrate Product from cqlengine to coodie
   ```

7. **Repeat** for the next model.

**Exit criteria:** All models compile, `sync_table()` succeeds, existing model
tests pass.

---

## Phase 4: Query & CRUD Conversion

**Entry criteria:** All models converted from Phase 3.

For each module that queries models:

1. **Replace query patterns** using the [checklist](../references/checklist.md):
   - `.objects.filter()` → `.find()`
   - `.objects.get()` → `.get()`
   - `.objects.all()` → `.find().all()`
   - `.create()` → `Model(**kw).save()` or `.create()`

2. **Replace batch operations:**
   - `Model.batch(b).create()` → `Model(...).save(batch=batch)`

3. **Replace exception handling:**
   - `except Model.DoesNotExist` → `except DocumentNotFound`

4. **Replace connection setup:**
   - `connection.setup()` → `init_coodie()`

5. **Replace sync_table calls:**
   - `management.sync_table(M)` → `M.sync_table()`

6. **Run tests** for this module.

7. **Commit** the query conversion:
   ```
   refactor(queries): migrate Product queries from cqlengine to coodie
   ```

**Exit criteria:** All queries use coodie API, no `.objects` references remain,
tests pass.

---

## Phase 5: Verification & Cleanup

**Entry criteria:** All models and queries converted from Phases 3–4.

1. **Search for remaining cqlengine references:**
   ```bash
   grep -rn "cassandra\.cqlengine" src/ --include="*.py"
   grep -rn "\.objects\." src/ --include="*.py"
   grep -rn "from cassandra" src/ --include="*.py"
   ```

2. **Remove cqlengine dependency:**
   ```bash
   uv remove cassandra-driver  # if fully migrated
   ```

3. **Run the full test suite** — all tests must pass.

4. **Smoke test CRUD** against a real database:
   - Create a record
   - Read it back
   - Update a field
   - Delete it
   - Verify with `sync_table()`

5. **Review the gotchas list** — check that none of the issues in
   [gotchas.md](../references/gotchas.md) remain in the codebase.

6. **Final commit:**
   ```
   refactor: complete cqlengine to coodie migration
   ```

**Exit criteria:** Zero `cassandra.cqlengine` imports remain. Full test suite
passes. CRUD smoke test succeeds on a real database.
