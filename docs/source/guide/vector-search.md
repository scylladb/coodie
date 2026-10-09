# Vector Search (ANN)

coodie supports ScyllaDB's `vector<float, N>` column type and the
`vector_index` custom index for Approximate Nearest-Neighbor (ANN)
similarity search.

## Defining a Vector Column

Use `Vector(dimensions=N)` to annotate a `list[float]` field and
`VectorIndex(similarity_function=...)` to attach an ANN index to it:

```python
from typing import Annotated
from uuid import UUID, uuid4
from pydantic import Field
from coodie.aio import Document, init_coodie
from coodie.fields import PrimaryKey, Vector, VectorIndex

class ProductEmbedding(Document):
    product_id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    embedding: Annotated[
        list[float],
        Vector(dimensions=384),
        VectorIndex(similarity_function="COSINE"),
    ]

    class Settings:
        name = "product_embeddings"
        keyspace = "my_ks"
```

To override the generated index name (`<table>_<column>_idx`), pass
`index_name`, just like `Indexed(index_name=...)`:
`VectorIndex(similarity_function="COSINE", index_name="product_ann_idx")`.

For **sync** usage replace `coodie.aio` with `coodie.sync`.

## Syncing the Table

`sync_table()` creates the `vector<float, 384>` column and the
vector index in one call:

```python
await ProductEmbedding.sync_table()
# sync: ProductEmbedding.sync_table()
```

Generated CQL:

```sql
CREATE TABLE IF NOT EXISTS my_ks.product_embeddings (
    product_id uuid PRIMARY KEY,
    name text,
    embedding vector<float, 384>
);

CREATE CUSTOM INDEX ON my_ks.product_embeddings (embedding)
USING 'vector_index'
WITH OPTIONS = {'similarity_function': 'COSINE'};
```

## Inserting Documents

coodie validates that the vector length matches `dimensions` on `save()`:

```python
p = ProductEmbedding(
    product_id=uuid4(),
    name="Widget",
    embedding=[0.1] * 384,   # must have exactly 384 floats
)
await p.save()
# sync: p.save()
```

## Running an ANN Query

Use `.order_by_ann(column, query_vector)` on a `QuerySet` to emit
a `ORDER BY … ANN OF ?` clause:

```python
query_vector = [0.1] * 384

results = await (
    ProductEmbedding.find()
    .order_by_ann("embedding", query_vector)
    .limit(10)
    .all()
)
# sync: ProductEmbedding.find().order_by_ann("embedding", query_vector).limit(10).all()
```

Generated CQL:

```sql
SELECT * FROM my_ks.product_embeddings
ORDER BY embedding ANN OF ?
LIMIT 10;
```

## Pagination

ScyllaDB ANN queries do not support cursor-based pagination
(paging state). Calling `paged_all()` on an ANN query always returns
a single page with `paging_state=None`. Use `.limit(N)` to control
the number of results.

```python
result = await (
    ProductEmbedding.find()
    .order_by_ann("embedding", query_vector)
    .limit(10)
    .paged_all()
)
# result.paging_state is always None for ANN queries
```

## Validation Rules

coodie enforces the following constraints at schema-build time:

| Constraint | Error |
|---|---|
| `Vector(dimensions=0)` or negative | `dimensions must be a positive integer` |
| `Annotated[list[int], Vector(...)]` | `must wrap list[float]` |
| `VectorIndex` on a non-vector column | `can only be applied to vector columns` |
| `VectorIndex` + `Indexed()` on the same column | `Cannot apply both Indexed() and VectorIndex()` |
| `VectorIndex` on a primary key column | `cannot be applied to a primary key column` |
| `VectorIndex` on a clustering key column | `cannot be applied to a clustering key column` |
| `VectorIndex` on a static column | `cannot be applied to a static column` |

## ScyllaDB Requirements

- **ScyllaDB 6.x+**: requires a tablet-enabled keyspace
  (`NetworkTopologyStrategy` + `tablets = {'enabled': true}`).
  Use `scylladb/scylla-nightly:latest` for development.
- **Older ScyllaDB / Cassandra**: `sync_table()` emits a warning and
  skips the index creation instead of raising, so non-vector workloads
  are unaffected.

## Similarity Functions

| Function | Description |
|---|---|
| `COSINE` | Cosine similarity (default). Measures angle between vectors. |
| `EUCLIDEAN` | Euclidean (L2) distance. Smaller distance = more similar. |
| `DOT_PRODUCT` | Dot product similarity. Vectors should be normalized for meaningful results. |
