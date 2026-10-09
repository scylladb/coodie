# Integration Examples

coodie works with any Python web framework. Below are patterns for the
two most popular choices: **FastAPI** (async) and **Flask** (sync).

## FastAPI (Async)

FastAPI's async-first design pairs naturally with `coodie.aio`. Use the
[lifespan](https://fastapi.tiangolo.com/advanced/events/) context manager
to initialise the driver at startup.

### Project Setup

```bash
pip install fastapi uvicorn coodie
```

### Application

```python
import os
from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator, Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Query
from pydantic import Field

from coodie.aio import Document, init_coodie
from coodie.exceptions import DocumentNotFound
from coodie.fields import ClusteringKey, Indexed, PrimaryKey


# ── Models ──────────────────────────────────────────────────

class Product(Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    brand: Annotated[str, Indexed()]
    category: Annotated[str, Indexed()]
    price: float
    description: Optional[str] = None
    tags: list[str] = Field(default_factory=list)

    class Settings:
        name = "products"


# ── Lifespan ────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "catalog")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    await Product.sync_table()
    yield


app = FastAPI(title="Product Catalog", lifespan=lifespan)


# ── Exception handler ───────────────────────────────────────

@app.exception_handler(DocumentNotFound)
async def not_found_handler(request, exc):
    raise HTTPException(status_code=404, detail=str(exc))


# ── Routes ──────────────────────────────────────────────────

@app.get("/products", response_model=list[Product])
async def list_products(
    category: str | None = Query(default=None),
) -> list[Product]:
    qs = Product.find()
    if category:
        qs = qs.filter(category=category).allow_filtering()
    return await qs.all()


@app.post("/products", response_model=Product, status_code=201)
async def create_product(product: Product) -> Product:
    await product.save()
    return product


@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: UUID) -> Product:
    return await Product.get(id=product_id)


@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: UUID) -> None:
    product = await Product.get(id=product_id)
    await product.delete()
```

### Running

```bash
# Start ScyllaDB
docker run --name scylla -d -p 9042:9042 scylladb/scylla --smp 1

# Create keyspace
docker exec -it scylla cqlsh -e \
  "CREATE KEYSPACE IF NOT EXISTS catalog
   WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"

# Run the app
uvicorn app:app --reload
```

> **Tip:** coodie `Document` classes are valid Pydantic models, so FastAPI can
> use them directly as `response_model` and request bodies — no separate
> schema layer needed.

### Full Demo

A complete FastAPI + HTMX demo lives in the repository under
[`demos/fastapi-catalog/`](https://github.com/scylladb/coodie/tree/master/demos/fastapi-catalog).

---

## Flask (Sync)

Flask's synchronous request handling works with `coodie.sync`. Initialise
the driver once at app creation time.

### Project Setup

```bash
pip install flask coodie
```

### Application

```python
import os
from typing import Annotated, Optional
from uuid import UUID, uuid4

from flask import Flask, jsonify, request, abort
from pydantic import Field

from coodie.sync import Document, init_coodie
from coodie.exceptions import DocumentNotFound
from coodie.fields import Indexed, PrimaryKey


# ── Models ──────────────────────────────────────────────────

class Product(Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    brand: Annotated[str, Indexed()]
    category: Annotated[str, Indexed()]
    price: float
    description: Optional[str] = None
    tags: list[str] = Field(default_factory=list)

    class Settings:
        name = "products"


# ── App factory ─────────────────────────────────────────────

def create_app() -> Flask:
    app = Flask(__name__)

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "catalog")

    init_coodie(hosts=hosts, keyspace=keyspace)
    Product.sync_table()

    # ── Routes ──────────────────────────────────────────

    @app.get("/products")
    def list_products():
        category = request.args.get("category")
        qs = Product.find()
        if category:
            qs = qs.filter(category=category).allow_filtering()
        products = qs.all()
        return jsonify([p.model_dump(mode="json") for p in products])

    @app.post("/products")
    def create_product():
        data = request.get_json()
        product = Product(**data)
        product.save()
        return jsonify(product.model_dump(mode="json")), 201

    @app.get("/products/<uuid:product_id>")
    def get_product(product_id: UUID):
        try:
            product = Product.get(id=product_id)
        except DocumentNotFound:
            abort(404)
        return jsonify(product.model_dump(mode="json"))

    @app.delete("/products/<uuid:product_id>")
    def delete_product(product_id: UUID):
        try:
            product = Product.get(id=product_id)
        except DocumentNotFound:
            abort(404)
        product.delete()
        return "", 204

    return app
```

### Running

```bash
# Start ScyllaDB (same as above)

# Run the app
flask --app app run --reload
```

> **Note:** Since Pydantic models are not directly JSON-serialisable by
> Flask, use `model_dump(mode="json")` to convert documents to
> JSON-friendly dicts.
