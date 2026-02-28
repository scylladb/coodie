# Migration Checklist: cqlengine → coodie

Use this checklist when converting a cqlengine application to coodie. Work
through items in order — models first, then queries, then infrastructure.

## Pre-Migration

- [ ] **Inventory models:** List all `cassandra.cqlengine.models.Model` subclasses
- [ ] **Inventory UDTs:** List all `cassandra.cqlengine.usertype.UserType` subclasses
- [ ] **Inventory queries:** Search for `Model.objects`, `BatchQuery`, `connection.setup`
- [ ] **Check feature gaps:** Review unsupported features and plan workarounds
- [ ] **Set up coodie:** Add `coodie` to project dependencies, ensure tests run

## Phase 1: Model Conversion (per model)

- [ ] **Change base class:** `Model` → `Document`
- [ ] **Update imports:** `cassandra.cqlengine` → `coodie.sync` / `coodie.aio` + `coodie.fields`
- [ ] **Convert column types:** `columns.*` → Python type annotations with `Annotated` markers
  - See [type-mapping.md](type-mapping.md) for the full mapping table
- [ ] **Convert key definitions:**
  - `primary_key=True` → `Annotated[T, PrimaryKey()]`
  - `partition_key=True` → `PrimaryKey(partition_key_index=N)` for composite keys
  - `clustering_order="DESC"` → `ClusteringKey(order="DESC")`
  - `index=True` → `Annotated[T, Indexed()]`
- [ ] **Convert column options:**
  - `required=True` → no default (field is required)
  - `required=False` / no required → `Optional[T] = None`
  - `default=value` → `field: T = value`
  - `default=callable` → `Field(default_factory=callable)`
- [ ] **Move table metadata to `Settings`:**
  - `__table_name__` → `Settings.name`
  - `__keyspace__` → `Settings.keyspace`
  - `__default_ttl__` → `Settings.__default_ttl__`
  - `__options__` → `Settings.__options__`
- [ ] **Convert collection defaults:**
  - `columns.List(T, default=[])` → `list[T] = Field(default_factory=list)`
  - `columns.Set(T, default=set())` → `set[T] = Field(default_factory=set)`
  - `columns.Map(K, V)` → `dict[K, V] = Field(default_factory=dict)`
- [ ] **Verify model imports and compiles** — `python -c "from myapp.models import Product"`

## Phase 2: UDT Conversion (per UDT)

- [ ] **Change base class:** `cqlengine.UserType` → `coodie.usertype.UserType`
- [ ] **Convert fields:** `columns.*` → Python type annotations
- [ ] **Move type name:** `__type_name__` → `Settings.__type_name__`
- [ ] **Remove wrappers:** `columns.UserDefinedType(Addr)` → plain `Addr` annotation
- [ ] **Update sync calls:** `management.sync_type("ks", Addr)` → `Addr.sync_type()`

## Phase 3: Query & CRUD Conversion

- [ ] **Replace query entry points:**
  - `M.objects.all()` → `M.find().all()`
  - `M.objects.filter(k=v)` → `M.find(k=v).all()`
  - `M.objects.get(pk=v)` → `M.get(pk=v)`
  - `M.objects.filter(pk=v).first()` → `M.find_one(pk=v)`
  - `M.objects.count()` → `M.find().count()`
- [ ] **Replace create calls:**
  - `M.create(**kw)` → `M(**kw).save()` or `M.create(**kw)`
- [ ] **Replace update patterns:**
  - `obj.field = val; obj.save()` → `obj.update(field=val)`
  - `M.objects.filter().update(f=v)` → `M.find().update(f=v)`
- [ ] **Replace delete patterns:**
  - `M.objects.filter().delete()` → `M.find().delete()`
- [ ] **Replace LWT operations:**
  - `M.if_not_exists().create()` → `M(...).insert()`
- [ ] **Replace TTL usage:**
  - `M.ttl(N).create()` → `M(...).save(ttl=N)`
- [ ] **Replace exception handling:**
  - `except M.DoesNotExist` → `except DocumentNotFound`
  - `except M.MultipleObjectsReturned` → `except MultipleDocumentsReturned`

## Phase 4: Batch & Connection Conversion

- [ ] **Replace connection setup:**
  - `connection.setup([hosts], "ks")` → `init_coodie(hosts=[hosts], keyspace="ks")`
- [ ] **Replace batch operations:**
  - `with BatchQuery() as b: M.batch(b).create()` → `with BatchQuery() as batch: M(...).save(batch=batch)`
- [ ] **Replace sync_table calls:**
  - `management.sync_table(M)` → `M.sync_table()`

## Phase 5: Async Migration (if applicable)

- [ ] **Change imports:** `coodie.sync` → `coodie.aio`
- [ ] **Add `await`** to all terminal methods: `save()`, `delete()`, `get()`, `find().all()`, `find_one()`, `count()`, `sync_table()`, `insert()`, `update()`
- [ ] **Replace `BatchQuery`** with `AsyncBatchQuery` and use `async with`
- [ ] **Replace `init_coodie`** with `await init_coodie()`

## Post-Migration Verification

- [ ] **Run test suite** — all existing tests pass
- [ ] **Search for leftover cqlengine imports:** `grep -r "cassandra.cqlengine" src/`
- [ ] **Search for leftover `.objects`:** `grep -r "\.objects\." src/`
- [ ] **Search for leftover `columns.`:** `grep -r "columns\." src/ --include="*.py"`
- [ ] **Search for leftover dunders:** `grep -r "__table_name__\|__keyspace__" src/ --include="*.py"` (should only be in `Settings`)
- [ ] **Smoke test CRUD:** Create, read, update, delete with a test database
- [ ] **Check schema:** `M.sync_table()` creates the expected table
