"""FastAPI article tagging demo showcasing coodie's collection types and mutations."""

from __future__ import annotations

__version__ = "0.1.0"

import os
from collections import Counter
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Article, FrozenTagSnapshot

from coodie.aio import init_coodie

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup: connect to ScyllaDB and sync tables."""
    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "tagmind")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    await Article.sync_table()
    await FrozenTagSnapshot.sync_table()
    yield


app = FastAPI(title="Collections Tags — The Infinite Taxonomy", version="0.1.0", lifespan=lifespan)


# ------------------------------------------------------------------
# JSON API — articles
# ------------------------------------------------------------------


@app.get("/api/articles")
async def api_list_articles() -> list[dict]:
    """List all articles with their collection fields."""
    articles = await Article.find().all()
    return [a.model_dump(mode="json") for a in articles]


@app.get("/api/articles/{article_id}")
async def api_get_article(article_id: UUID) -> dict:
    """Get a single article."""
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article.model_dump(mode="json")


@app.post("/api/articles", status_code=201)
async def api_create_article(
    title: str,
    author: str,
    tags: str = "",
) -> dict:
    """Create a new article. Tags is a comma-separated string."""
    tag_set = {t.strip() for t in tags.split(",") if t.strip()} if tags else set()
    article = Article(title=title, author=author, tags=tag_set)
    await article.save()
    return article.model_dump(mode="json")


async def _collect_tag_counts() -> dict[str, int]:
    """Return a mapping of tag → article count across all articles."""
    articles = await Article.find().all()
    counter: Counter[str] = Counter()
    for a in articles:
        if a.tags:
            counter.update(a.tags)
    return dict(counter)


@app.get("/api/tags")
async def api_list_tags() -> dict:
    """List all unique tags with per-tag article counts."""
    counts = await _collect_tag_counts()
    return {"tags": counts, "total_unique": len(counts)}


# ------------------------------------------------------------------
# JSON API — collection mutations
# ------------------------------------------------------------------


@app.post("/api/articles/{article_id}/tags/add")
async def api_add_tags(article_id: UUID, tags: str) -> dict:
    """Add tags to an article's set<text> using add__ mutation."""
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    new_tags = {t.strip() for t in tags.split(",") if t.strip()}
    await article.update(tags__add=new_tags)
    updated = await Article.find_one(article_id=article_id)
    return {"action": "add__tags", "added": sorted(new_tags), "article": updated.model_dump(mode="json")}


@app.post("/api/articles/{article_id}/tags/remove")
async def api_remove_tags(article_id: UUID, tags: str) -> dict:
    """Remove tags from an article's set<text> using remove__ mutation."""
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    rm_tags = {t.strip() for t in tags.split(",") if t.strip()}
    await article.update(tags__remove=rm_tags)
    updated = await Article.find_one(article_id=article_id)
    return {"action": "remove__tags", "removed": sorted(rm_tags), "article": updated.model_dump(mode="json")}


@app.post("/api/articles/{article_id}/metadata/add")
async def api_add_metadata(article_id: UUID, key: str, value: str) -> dict:
    """Add a key-value pair to an article's map<text,text> using add__ mutation."""
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    await article.update(metadata__add={key: value})
    updated = await Article.find_one(article_id=article_id)
    return {"action": "add__metadata", "key": key, "value": value, "article": updated.model_dump(mode="json")}


@app.post("/api/articles/{article_id}/metadata/remove")
async def api_remove_metadata(article_id: UUID, key: str) -> dict:
    """Remove a key from an article's map using remove__ mutation."""
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    await article.update(metadata__remove={key})
    updated = await Article.find_one(article_id=article_id)
    return {"action": "remove__metadata", "key": key, "article": updated.model_dump(mode="json")}


@app.post("/api/articles/{article_id}/revisions/append")
async def api_append_revision(article_id: UUID, text: str) -> dict:
    """Append a revision to the article's list<text> using append__ mutation."""
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    await article.update(revisions__append=[text])
    updated = await Article.find_one(article_id=article_id)
    return {"action": "append__revisions", "text": text, "article": updated.model_dump(mode="json")}


@app.post("/api/articles/{article_id}/revisions/prepend")
async def api_prepend_revision(article_id: UUID, text: str) -> dict:
    """Prepend a revision to the article's list<text> using prepend__ mutation."""
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    await article.update(revisions__prepend=[text])
    updated = await Article.find_one(article_id=article_id)
    return {"action": "prepend__revisions", "text": text, "article": updated.model_dump(mode="json")}


# ------------------------------------------------------------------
# JSON API — frozen snapshots
# ------------------------------------------------------------------


@app.post("/api/articles/{article_id}/snapshot", status_code=201)
async def api_create_snapshot(article_id: UUID) -> dict:
    """Create a frozen tag snapshot for an article."""
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    snapshot = FrozenTagSnapshot(
        article_id=article.article_id,
        snapshot_at=datetime.now(timezone.utc),
        frozen_tags=set(article.tags) if article.tags else None,
        note=f"Snapshot of {len(article.tags)} tags",
    )
    await snapshot.save()
    return snapshot.model_dump(mode="json")


# ------------------------------------------------------------------
# HTMX UI routes
# ------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def ui_index(request: Request) -> HTMLResponse:
    articles = await Article.find().all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"articles": articles},
    )


@app.get("/ui/articles", response_class=HTMLResponse)
async def ui_list_articles(
    request: Request,
    tags: str = Query(default=""),
) -> HTMLResponse:
    articles = await Article.find().all()
    active_tags = sorted({t.strip() for t in tags.split(",") if t.strip()}) if tags else []
    if active_tags:
        tag_set = set(active_tags)
        articles = [a for a in articles if a.tags and tag_set.issubset(a.tags)]
    return templates.TemplateResponse(
        request=request,
        name="partials/article_list.html",
        context={"articles": articles, "active_tags": active_tags},
    )


@app.get("/ui/tag-cloud", response_class=HTMLResponse)
async def ui_tag_cloud(
    request: Request,
    tags: str = Query(default=""),
) -> HTMLResponse:
    tag_counts = await _collect_tag_counts()
    active_tags = sorted({t.strip() for t in tags.split(",") if t.strip()}) if tags else []
    return templates.TemplateResponse(
        request=request,
        name="partials/tag_cloud.html",
        context={"tag_counts": tag_counts, "active_tags": active_tags},
    )


@app.get("/ui/articles/{article_id}", response_class=HTMLResponse)
async def ui_article_detail(request: Request, article_id: UUID) -> HTMLResponse:
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return templates.TemplateResponse(
        request=request,
        name="partials/article_detail.html",
        context={"article": article},
    )


@app.post("/ui/articles", response_class=HTMLResponse)
async def ui_create_article(
    request: Request,
    title: str = Form(),
    author: str = Form(),
    tags: str = Form(default=""),
) -> HTMLResponse:
    tag_set = {t.strip() for t in tags.split(",") if t.strip()} if tags else set()
    article = Article(title=title, author=author, tags=tag_set)
    await article.save()
    articles = await Article.find().all()
    return templates.TemplateResponse(
        request=request,
        name="partials/article_list.html",
        context={"articles": articles},
    )


@app.post("/ui/articles/{article_id}/tags/add", response_class=HTMLResponse)
async def ui_add_tag(
    request: Request,
    article_id: UUID,
    tag: str = Form(),
) -> HTMLResponse:
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    new_tags = {t.strip() for t in tag.split(",") if t.strip()}
    await article.update(tags__add=new_tags)
    article = await Article.find_one(article_id=article_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/article_detail.html",
        context={"article": article, "flash": f"Added tag(s): {', '.join(sorted(new_tags))}"},
    )


@app.post("/ui/articles/{article_id}/tags/remove", response_class=HTMLResponse)
async def ui_remove_tag(
    request: Request,
    article_id: UUID,
    tag: str = Form(),
) -> HTMLResponse:
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    rm_tags = {t.strip() for t in tag.split(",") if t.strip()}
    await article.update(tags__remove=rm_tags)
    article = await Article.find_one(article_id=article_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/article_detail.html",
        context={"article": article, "flash": f"Removed tag(s): {', '.join(sorted(rm_tags))}"},
    )


@app.post("/ui/articles/{article_id}/metadata/add", response_class=HTMLResponse)
async def ui_add_metadata(
    request: Request,
    article_id: UUID,
    meta_key: str = Form(),
    meta_value: str = Form(),
) -> HTMLResponse:
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    await article.update(metadata__add={meta_key: meta_value})
    article = await Article.find_one(article_id=article_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/article_detail.html",
        context={"article": article, "flash": f"Added metadata: {meta_key}={meta_value}"},
    )


@app.post("/ui/articles/{article_id}/metadata/remove", response_class=HTMLResponse)
async def ui_remove_metadata(
    request: Request,
    article_id: UUID,
    meta_key: str = Form(),
) -> HTMLResponse:
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    await article.update(metadata__remove={meta_key})
    article = await Article.find_one(article_id=article_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/article_detail.html",
        context={"article": article, "flash": f"Removed metadata key: {meta_key}"},
    )


@app.post("/ui/articles/{article_id}/revisions/append", response_class=HTMLResponse)
async def ui_append_revision(
    request: Request,
    article_id: UUID,
    revision: str = Form(),
) -> HTMLResponse:
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    await article.update(revisions__append=[revision])
    article = await Article.find_one(article_id=article_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/article_detail.html",
        context={"article": article, "flash": f"Appended revision: {revision}"},
    )


@app.post("/ui/articles/{article_id}/revisions/prepend", response_class=HTMLResponse)
async def ui_prepend_revision(
    request: Request,
    article_id: UUID,
    revision: str = Form(),
) -> HTMLResponse:
    article = await Article.find_one(article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    await article.update(revisions__prepend=[revision])
    article = await Article.find_one(article_id=article_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/article_detail.html",
        context={"article": article, "flash": f"Prepended revision: {revision}"},
    )
