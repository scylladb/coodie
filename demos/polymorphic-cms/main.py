"""FastAPI Polymorphic CMS demo — single-table inheritance with Discriminator."""

from __future__ import annotations

__version__ = "0.1.0"

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator
from uuid import UUID

from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from coodie.aio import init_coodie

from models import Article, Content, Podcast, Video

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Map discriminator values → subclass for convenience
TYPE_MAP: dict[str, type[Content]] = {
    "article": Article,
    "video": Video,
    "podcast": Podcast,
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup: connect to ScyllaDB and sync the shared content table."""
    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "cms")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    # Sync the base table, then each subclass so subclass-specific columns
    # (e.g. body, video_url, audio_url) are added via ALTER TABLE ADD.
    await Content.sync_table()
    await Article.sync_table()
    await Video.sync_table()
    await Podcast.sync_table()
    yield


app = FastAPI(
    title="Polymorphic CMS — The Shapeshifter's Archive",
    version="0.1.0",
    lifespan=lifespan,
)


# ------------------------------------------------------------------
# JSON API routes
# ------------------------------------------------------------------


@app.get("/content", response_model=list[Content])
async def list_content(
    content_type: str | None = Query(default=None),
    author: str | None = Query(default=None),
) -> list[Content]:
    """List all content, optionally filtered by type or author."""
    if content_type and content_type in TYPE_MAP:
        qs = TYPE_MAP[content_type].find()
    else:
        qs = Content.find()
    if author:
        qs = qs.filter(author=author).allow_filtering()
    return await qs.all()


@app.post("/content/{content_type}", response_model=Content, status_code=201)
async def create_content(content_type: str, item: dict) -> Content:
    """Create content of a given type."""
    cls = TYPE_MAP.get(content_type)
    if cls is None:
        raise HTTPException(status_code=400, detail=f"Unknown type: {content_type}")
    doc = cls(**item)
    await doc.save()
    return doc


@app.get("/content/{content_id}", response_model=Content)
async def get_content(content_id: UUID) -> Content:
    """Get a single content item by ID."""
    item = await Content.find_one(id=content_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return item


@app.delete("/content/{content_id}", status_code=204)
async def delete_content(content_id: UUID) -> None:
    """Delete a content item."""
    item = await Content.find_one(id=content_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Content not found")
    await item.delete()


# ------------------------------------------------------------------
# HTMX UI routes
# ------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def ui_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/ui/content", response_class=HTMLResponse)
async def ui_list_content(
    request: Request,
    content_type: str | None = Query(default=None),
) -> HTMLResponse:
    """List content cards, optionally filtered by type."""
    if content_type and content_type in TYPE_MAP:
        items = await TYPE_MAP[content_type].find().all()
    else:
        items = await Content.find().all()
    return templates.TemplateResponse(
        "partials/content_list.html",
        {"request": request, "items": items},
    )


@app.get("/ui/content/{content_id}", response_class=HTMLResponse)
async def ui_content_detail(request: Request, content_id: UUID) -> HTMLResponse:
    """Show full detail for a single content item."""
    item = await Content.find_one(id=content_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return templates.TemplateResponse(
        "partials/content_detail.html",
        {"request": request, "item": item},
    )


@app.post("/ui/content", response_class=HTMLResponse)
async def ui_create_content(
    request: Request,
    content_type: str = Form(),
    title: str = Form(),
    author: str = Form(),
    summary: str = Form(default=""),
    # Article fields
    body: str = Form(default=""),
    word_count: int = Form(default=0),
    # Video fields
    video_url: str = Form(default=""),
    duration_seconds: int = Form(default=0),
    resolution: str = Form(default="1080p"),
    # Podcast fields
    audio_url: str = Form(default=""),
    episode_number: int = Form(default=0),
) -> HTMLResponse:
    """Create content from the UI form and return the updated list."""
    cls = TYPE_MAP.get(content_type)
    if cls is None:
        raise HTTPException(status_code=400, detail=f"Unknown type: {content_type}")

    kwargs: dict = {
        "title": title,
        "author": author,
        "summary": summary or None,
    }

    if content_type == "article":
        kwargs["body"] = body or None
        kwargs["word_count"] = word_count
    elif content_type == "video":
        kwargs["video_url"] = video_url or None
        kwargs["duration_seconds"] = duration_seconds
        kwargs["resolution"] = resolution
    elif content_type == "podcast":
        kwargs["audio_url"] = audio_url or None
        kwargs["duration_seconds"] = duration_seconds
        kwargs["episode_number"] = episode_number

    doc = cls(**kwargs)
    await doc.save()

    items = await Content.find().all()
    return templates.TemplateResponse(
        "partials/content_list.html",
        {"request": request, "items": items},
    )


@app.delete("/ui/content/{content_id}", response_class=HTMLResponse)
async def ui_delete_content(request: Request, content_id: UUID) -> HTMLResponse:
    """Delete content and return the updated list."""
    item = await Content.find_one(id=content_id)
    if item:
        await item.delete()
    items = await Content.find().all()
    return templates.TemplateResponse(
        "partials/content_list.html",
        {"request": request, "items": items},
    )
