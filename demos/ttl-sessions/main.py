"""FastAPI TTL Sessions demo — The Memory Thief.

Showcases coodie's TTL support:
- ``__default_ttl__`` on a model's Settings class (table-level default)
- ``ttl=`` on individual ``save()`` calls (per-record override)
- Data literally disappears as the TTL expires
"""

from __future__ import annotations

__version__ = "0.1.0"

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Session

from coodie.aio import init_coodie

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup: connect to ScyllaDB and sync tables."""
    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "ephemera")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    await Session.sync_table()
    yield


app = FastAPI(title="TTL Sessions — The Memory Thief", version="0.1.0", lifespan=lifespan)


# ------------------------------------------------------------------
# JSON API routes
# ------------------------------------------------------------------


@app.get("/sessions", response_model=list[Session])
async def list_sessions() -> list[Session]:
    """Return all currently-alive sessions (expired rows are gone automatically)."""
    return await Session.find().allow_filtering().all()


@app.post("/sessions", response_model=Session, status_code=201)
async def create_session(
    user_name: str,
    memory_fragment: str,
    ttl: int = 300,
) -> Session:
    """Create a new session with the given TTL (seconds).

    Demonstrates ``save(ttl=...)`` to override the model's ``__default_ttl__``.
    """
    session = Session(
        user_name=user_name,
        memory_fragment=memory_fragment,
        ttl_seconds=ttl,
    )
    await session.save(ttl=ttl)
    return session


@app.get("/sessions/{token}", response_model=Session)
async def get_session(token: UUID) -> Session:
    """Fetch a single session by token — returns 404 if TTL has expired."""
    session = await Session.find_one(token=token)
    if session is None:
        raise HTTPException(status_code=404, detail="Session expired or not found")
    return session


@app.delete("/sessions/{token}", status_code=204)
async def delete_session(token: UUID) -> None:
    """Manually delete a session before its TTL expires."""
    session = await Session.find_one(token=token)
    if session:
        await session.delete()


# ------------------------------------------------------------------
# HTMX UI routes
# ------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def ui_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/ui/sessions", response_class=HTMLResponse)
async def ui_list_sessions(request: Request) -> HTMLResponse:
    sessions = await Session.find().allow_filtering().all()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    return templates.TemplateResponse(
        "partials/session_list.html",
        {"request": request, "sessions": sessions, "now": now},
    )


@app.post("/ui/sessions", response_class=HTMLResponse)
async def ui_create_session(
    request: Request,
    user_name: str = Form(),
    memory_fragment: str = Form(),
    ttl: int = Form(default=30),
) -> HTMLResponse:
    """Create a session from the HTMX form and return the updated list."""
    session = Session(
        user_name=user_name,
        memory_fragment=memory_fragment,
        ttl_seconds=ttl,
    )
    await session.save(ttl=ttl)
    sessions = await Session.find().allow_filtering().all()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    return templates.TemplateResponse(
        "partials/session_list.html",
        {"request": request, "sessions": sessions, "now": now},
    )


@app.delete("/ui/sessions/{token}", response_class=HTMLResponse)
async def ui_delete_session(request: Request, token: UUID) -> HTMLResponse:
    """Delete a session and return the updated list."""
    session = await Session.find_one(token=token)
    if session:
        await session.delete()
    sessions = await Session.find().allow_filtering().all()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    return templates.TemplateResponse(
        "partials/session_list.html",
        {"request": request, "sessions": sessions, "now": now},
    )
