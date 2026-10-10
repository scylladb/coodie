# 🎭 coodie Polymorphic CMS Demo — The Shapeshifter's Archive

> *Dimension-11: The Shapeshifter's Archive* — Classify polymorphic content
> before Morph-IX collapses the entire archive into a singularity of
> undifferentiated content.

A runnable demo app showcasing **coodie**'s **single-table inheritance** via the
`Discriminator` column. Three content types — `Article`, `Video`, and `Podcast`
— share a single Cassandra table, with coodie automatically routing queries
based on the `content_type` discriminator value.

Built with [FastAPI](https://fastapi.tiangolo.com/) and [HTMX](https://htmx.org/).

## Quick Start

```bash
cd demos/polymorphic-cms
make run
```

This single command starts ScyllaDB, creates the keyspace, seeds 30 mixed
content items, and launches the FastAPI app.

## Prerequisites

* Python ≥ 3.10
* [uv](https://docs.astral.sh/uv/) (recommended) or pip
* Docker & Docker Compose (for ScyllaDB)

## Step-by-Step

### 1. Start ScyllaDB and create keyspace

```bash
make db-up
```

### 2. Seed sample data

```bash
make seed                       # 30 items (default)
uv run python seed.py --count 100   # custom count
```

### 3. Run the app

```bash
uv run uvicorn main:app --reload
```

The API will be available at <http://127.0.0.1:8000>.
Interactive docs at <http://127.0.0.1:8000/docs>.
**HTMX UI** at <http://127.0.0.1:8000/> — browse, create, and filter
polymorphic content.

## How It Works — Single-Table Inheritance

All three content types live in **one Cassandra table** (`contents`):

```python
from coodie.aio import Document
from coodie.fields import Discriminator, Indexed, PrimaryKey

class Content(Document):
    """Base content — single table for all types."""
    id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
    content_type: Annotated[str, Discriminator()] = ""
    title: str
    author: Annotated[str, Indexed()]
    # ... shared fields ...

    class Settings:
        name = "contents"
        keyspace = "cms"

class Article(Content):
    body: Optional[str] = None
    word_count: int = 0

    class Settings:
        __discriminator_value__ = "article"

class Video(Content):
    video_url: Optional[str] = None
    duration_seconds: int = 0
    resolution: str = "1080p"

    class Settings:
        __discriminator_value__ = "video"

class Podcast(Content):
    audio_url: Optional[str] = None
    duration_seconds: int = 0
    episode_number: int = 0

    class Settings:
        __discriminator_value__ = "podcast"
```

**Key points:**
- The `Discriminator()` marker on `content_type` tells coodie this is a
  polymorphic hierarchy.
- Each subclass sets `__discriminator_value__` in its `Settings`.
- `Article.find()` automatically adds `WHERE content_type = 'article'`.
- `Content.find()` returns all types — coodie routes each row to the
  correct subclass.

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `SCYLLA_HOSTS` | `127.0.0.1` | Comma-separated ScyllaDB contact points |
| `SCYLLA_KEYSPACE` | `cms` | Keyspace to use |

## Makefile Targets

| Target | Description |
|---|---|
| `make db-up` | Start ScyllaDB and create the `cms` keyspace |
| `make db-down` | Stop ScyllaDB |
| `make seed` | Seed 30 polymorphic content items (depends on `db-up`) |
| `make run` | Install deps, seed data, and start the app |
| `make clean` | Stop DB and remove data volumes |

## Seed Script

The `seed.py` script generates realistic sample data with colorful
[rich](https://rich.readthedocs.io/) progress output themed around
Morph-IX's shapeshifting archive.

```bash
# Generate 100 mixed content items
uv run python seed.py --count 100
```

Each type gets its own colour in the progress display:
- 📰 **Articles** — coral (`#f97316`)
- 🎬 **Videos** — violet (`#8b5cf6`)
- 🎙️ **Podcasts** — teal (`#14b8a6`)

## Example API Requests

### List all content

```bash
curl http://127.0.0.1:8000/content
```

### Filter by type

```bash
curl "http://127.0.0.1:8000/content?content_type=article"
curl "http://127.0.0.1:8000/content?content_type=video"
curl "http://127.0.0.1:8000/content?content_type=podcast"
```

### Create an article

```bash
curl -X POST http://127.0.0.1:8000/content/article \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Art of Polymorphism",
    "author": "Morph-IX",
    "summary": "All content is one.",
    "body": "A treatise on single-table inheritance...",
    "word_count": 1500
  }'
```

### Create a video

```bash
curl -X POST http://127.0.0.1:8000/content/video \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Shapeshifting 101",
    "author": "Dr. Schema",
    "video_url": "https://dim-11.stream/v/abc123",
    "duration_seconds": 600,
    "resolution": "1080p"
  }'
```

### Create a podcast

```bash
curl -X POST http://127.0.0.1:8000/content/podcast \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ep. 1: The Day Content Became Sentient",
    "author": "The Discriminator",
    "audio_url": "https://morph-ix.audio/ep/001",
    "duration_seconds": 1800,
    "episode_number": 1
  }'
```

### Get a content item by ID

```bash
curl http://127.0.0.1:8000/content/<content-id>
```

### Delete content

```bash
curl -X DELETE http://127.0.0.1:8000/content/<content-id>
```

## Cleanup

```bash
make clean
```
