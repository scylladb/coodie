from __future__ import annotations

__version__ = "0.1.0"

import math
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import DistressSignal

from coodie.aio import init_coodie

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

_model = None


def _get_model():
    global _model
    if _model is None:
        from fastembed import TextEmbedding

        _model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return _model


def _embed(text: str) -> list[float]:
    return next(iter(_get_model().embed([text]))).tolist()


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "vector_demo")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    await DistressSignal.sync_table()
    _get_model()
    yield


app = FastAPI(title="Signal Graveyard", version="0.1.0", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def ui_index(request: Request) -> HTMLResponse:
    total = await DistressSignal.find().count()
    return templates.TemplateResponse(request, "index.html", {"total": total})


@app.post("/ui/search", response_class=HTMLResponse)
async def ui_search(
    request: Request,
    query: str = Form(default=""),
    limit: int = Form(default=10),
) -> HTMLResponse:
    if not query.strip():
        return templates.TemplateResponse(
            request,
            "partials/results.html",
            {"results": [], "query": ""},
        )

    query_embedding = _embed(query)
    signals = await DistressSignal.find().order_by_ann("embedding", query_embedding).limit(limit).all()

    results = []
    for s in signals:
        score = _cosine_similarity(query_embedding, s.embedding)
        results.append({"signal": s, "score": score})

    return templates.TemplateResponse(
        request,
        "partials/results.html",
        {"results": results, "query": query},
    )


@app.get("/ui/browse", response_class=HTMLResponse)
async def ui_browse(request: Request) -> HTMLResponse:
    signals = await DistressSignal.find().limit(50).all()
    return templates.TemplateResponse(
        request,
        "partials/browse.html",
        {"signals": signals},
    )
