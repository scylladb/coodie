<div align="center">

<img src="docs/images/logo.png" alt="coodie logo" width="200">

# coodie

**The modern Pydantic-based ODM for Cassandra & ScyllaDB**

*Cassandra + Beanie (hoodie) = **coodie** 🧥*

[![CI Status](https://img.shields.io/github/actions/workflow/status/scylladb/coodie/ci.yml?branch=master&label=CI&logo=github&style=for-the-badge)](https://github.com/scylladb/coodie/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/github/actions/workflow/status/scylladb/coodie/docs.yml?branch=master&label=Docs&logo=github&style=for-the-badge)](https://scylladb.github.io/coodie/)
[![Coverage](https://img.shields.io/codecov/c/github/scylladb/coodie.svg?logo=codecov&logoColor=fff&style=for-the-badge)](https://codecov.io/gh/scylladb/coodie)
[![PyPI](https://img.shields.io/pypi/v/coodie.svg?logo=python&logoColor=fff&style=for-the-badge)](https://pypi.org/project/coodie/)
[![Downloads](https://img.shields.io/pypi/dm/coodie.svg?logo=pypi&logoColor=fff&style=for-the-badge)](https://pypi.org/project/coodie/)
[![Python](https://img.shields.io/pypi/pyversions/coodie.svg?style=for-the-badge&logo=python&logoColor=fff)](https://pypi.org/project/coodie/)
[![License](https://img.shields.io/pypi/l/coodie.svg?style=for-the-badge)](https://github.com/scylladb/coodie/blob/master/LICENSE)

<p>
<a href="https://scylladb.github.io/coodie/">📖 Documentation</a> •
<a href="#-quick-start">🚀 Quick Start</a> •
<a href="https://github.com/scylladb/coodie/blob/master/CONTRIBUTING.md">🤝 Contributing</a> •
<a href="https://github.com/scylladb/coodie/blob/master/CHANGELOG.md">📋 Changelog</a>
</p>

</div>

---

<!-- start-tagline -->
Define your data models as Python classes, and coodie handles schema synchronization,
serialization, and query building — with both **sync** and **async** APIs.
<!-- end-tagline -->

## ✨ Feature Highlights

<!-- start-features -->
<table>
<tr>
<td width="50%">

🧬 **Pydantic v2 Models** — full type-checking & validation\
⚡ **Sync & Async** — `coodie.sync` for blocking, `coodie.aio` for asyncio\
🔗 **Chainable QuerySet** — `.filter()` · `.limit()` · `.order_by()`

</td>
<td width="50%">

🔄 **Automatic Schema Sync** — `sync_table()` creates & evolves tables\
🏗️ **Batch & LWT** — `BatchQuery` + `if_not_exists()` support\
🎯 **Multi-Driver** — scylla-driver · cassandra-driver · acsylla\
🔍 **Vector Search** — `Vector(dimensions=N)` + `order_by_ann()` for ANN queries

</td>
</tr>
</table>
<!-- end-features -->

## 🔍 How Does coodie Compare?

<!-- start-comparison -->
| Feature | **coodie** | **beanie** | **cqlengine** |
|---|:---:|:---:|:---:|
| **Database** | Cassandra / ScyllaDB | MongoDB | Cassandra |
| **Schema Definition** | Pydantic v2 `BaseModel` | Pydantic v2 `BaseModel` | Custom `columns.*` classes |
| **Type Hints** | ✅ Native `Annotated[]` | ✅ Native Pydantic | ❌ No type hints |
| **Async Support** | ✅ First-class | ✅ First-class | ❌ Sync only |
| **Sync Support** | ✅ `coodie.sync` | ❌ Async only | ✅ Sync only |
| **Query API** | Chainable `QuerySet` | Chainable `FindMany` | Chainable `QuerySet` |
| **Schema Migration** | ✅ `sync_table()` | ❌ Manual | ✅ `sync_table()` |
| **LWT (Compare-and-Set)** | ✅ `if_not_exists()` | N/A | ✅ `iff()` |
| **Batch Operations** | ✅ `BatchQuery` | ❌ | ✅ `BatchQuery` |
| **Counter Columns** | ✅ `Counter()` | ❌ | ✅ `columns.Counter` |
| **User-Defined Types** | ✅ `UserType` | ❌ | ✅ `UserType` |
| **TTL Support** | ✅ Per-save TTL | ❌ | ✅ Per-save TTL |
| **Pagination** | ✅ Token-based `PagedResult` | ✅ Cursor-based | ❌ Manual |
| **Multiple Drivers** | ✅ 3 drivers | motor only | cassandra-driver only |
| **Polymorphic Models** | ✅ `Discriminator` | ❌ | ❌ |
| **Vector Search (ANN)** | ✅ `Vector()` + `order_by_ann()` | ❌ | ❌ |
| **Python Version** | 3.10+ | 3.8+ | 3.6+ |
<!-- end-comparison -->

## 📦 Installation

<!-- start-installation -->
```bash
pip install coodie
```

Choose a driver extra for your cluster:

```bash
pip install "coodie[scylla]"      # ScyllaDB / Cassandra (recommended)
pip install "coodie[cassandra]"   # Cassandra via cassandra-driver
pip install "coodie[acsylla]"     # Async-native via acsylla
```
<!-- end-installation -->

## 🚀 Quick Start

<!-- start-quickstart -->
**1. Start a local ScyllaDB** (or use an existing cluster):

```bash
docker run --name scylla -d -p 9042:9042 scylladb/scylla --smp 1

# Wait for it to be ready (~30s), then create a keyspace
docker exec -it scylla cqlsh -e \
  "CREATE KEYSPACE IF NOT EXISTS my_ks
   WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
```

**2. Install coodie:**

```bash
pip install "coodie[scylla]"
```

**3. Write your first script:**

```python
from coodie.sync import Document, init_coodie
from coodie.fields import PrimaryKey
from pydantic import Field
from typing import Annotated
from uuid import UUID, uuid4

# Connect
init_coodie(hosts=["127.0.0.1"], keyspace="my_ks")

# Define a model
class User(Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    name: str
    email: str

    class Settings:
        name = "users"

# Sync schema & insert
User.sync_table()
user = User(name="Alice", email="alice@example.com")
user.save()

# Query
print(User.find(name="Alice").allow_filtering().all())
```

> 💡 **Async?** Just swap `coodie.sync` for `coodie.aio` and add `await` — that's it!
<!-- end-quickstart -->

## 📖 Usage

<details>
<summary><b>Define a Document</b></summary>

```python
from typing import Annotated
from uuid import UUID, uuid4
from pydantic import Field
from coodie import Document, PrimaryKey, ClusteringKey, Indexed

class Product(Document):
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    category: Annotated[str, ClusteringKey()] = "general"
    name: str
    brand: Annotated[str, Indexed()] = "Unknown"
    price: float = 0.0

    class Settings:
        name = "products"      # table name (defaults to snake_case class name)
        keyspace = "my_ks"
```

</details>

<details>
<summary><b>Async API</b> — <code>coodie</code> / <code>coodie.aio</code></summary>

```python
import asyncio
from coodie import init_coodie
# Product defined above — same field definitions, using coodie.aio.Document

async def main():
    await init_coodie(hosts=["127.0.0.1"], keyspace="my_ks")
    await Product.sync_table()

    p = Product(name="Gadget", brand="Acme", price=9.99)
    await p.save()

    results = await Product.find(brand="Acme").limit(10).all()
    for product in results:
        print(product.name, product.price)

    gadget = await Product.get(id=p.id)
    await gadget.delete()

asyncio.run(main())
```

</details>

<details>
<summary><b>Sync API</b> — <code>coodie.sync</code></summary>

```python
from coodie.sync import Document, init_coodie

class Product(Document):
    ...  # same field definitions

init_coodie(hosts=["127.0.0.1"], keyspace="my_ks")
Product.sync_table()

p = Product(name="Widget", price=4.99)
p.save()

results = Product.find(brand="Acme").allow_filtering().all()
one = Product.find_one(name="Widget")
```

</details>

<details>
<summary><b>QuerySet Chaining</b></summary>

```python
# Filter, sort, and limit
products = (
    await Product.find()
    .filter(brand="Acme")
    .order_by("price")
    .limit(20)
    .all()
)

# Count
n = await Product.find(brand="Acme").allow_filtering().count()

# Async iteration
async for p in Product.find(brand="Acme"):
    print(p)

# Delete matching rows
await Product.find(brand="Discontinued").allow_filtering().delete()
```

</details>

<details>
<summary><b>Field Annotations Reference</b></summary>

| Annotation | Purpose |
|---|---|
| `PrimaryKey(partition_key_index=0)` | Partition key column (composite keys via index) |
| `ClusteringKey(order="ASC", clustering_key_index=0)` | Clustering column |
| `Indexed(index_name=None)` | Secondary index |
| `Counter()` | Counter column |
| `Discriminator()` | Polymorphic model discriminator |
| `Vector(dimensions=N)` | Vector column — maps `list[float]` to `vector<float, N>` |
| `VectorIndex(similarity_function="COSINE")` | SAI vector index for ANN queries |

</details>

<details>
<summary><b>Vector Search (ANN)</b></summary>

coodie supports ScyllaDB's `vector<float, N>` column type and ANN similarity search via `VectorIndex`.

```python
class ProductEmbedding(Document):
    product_id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    embedding: Annotated[
        list[float],
        Vector(dimensions=384),
        VectorIndex(similarity_function="COSINE"),
    ]
    ...

results = await ProductEmbedding.find().order_by_ann("embedding", query_vector).limit(10).all()
```

> 📖 **Full guide:** [Vector Search (ANN)](docs/source/guide/vector-search.md)

</details>

## 📚 Learn More

| Resource | Link |
|---|---|
| 📖 **Full Documentation** | [scylladb.github.io/coodie](https://scylladb.github.io/coodie/) |
| 🚀 **Quick Start Guide** | [Installation & Quickstart](https://scylladb.github.io/coodie/quickstart.html) |
| 📊 **Benchmark History** | [Performance Trends](https://scylladb.github.io/coodie/benchmarks/) |
| 🎮 **Demo Apps** | [demos/](demos/README.md) — FastAPI, Flask, Django & CLI examples |
| 🔄 **Migrating from cqlengine** | [Migration Guide](https://scylladb.github.io/coodie/migration/from-cqlengine.html) |
| 🤝 **Contributing** | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 📋 **Changelog** | [CHANGELOG.md](CHANGELOG.md) |
| 🐛 **Bug Reports** | [GitHub Issues](https://github.com/scylladb/coodie/issues) |

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="http://fruch.github.io/"><img src="https://avatars.githubusercontent.com/u/340979?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Israel Fruchter</b></sub></a><br /><a href="https://github.com/scylladb/coodie/commits?author=fruch" title="Code">💻</a> <a href="#ideas-fruch" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/scylladb/coodie/commits?author=fruch" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[browniebroke/cookiecutter-pypackage](https://github.com/browniebroke/cookiecutter-pypackage)
project template.
