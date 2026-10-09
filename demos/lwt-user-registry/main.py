"""FastAPI LWT User Registry demo showcasing coodie's Lightweight Transactions."""

from __future__ import annotations

__version__ = "0.1.0"

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import UserProfile, UserRegistration

from coodie.aio import init_coodie
from coodie.aio.document import _parse_lwt_result
from coodie.cql_builder import build_insert_from_columns
from coodie.schema import _insert_columns

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup: connect to ScyllaDB and sync tables."""
    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "registry")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    await UserRegistration.sync_table()
    await UserProfile.sync_table()
    yield


app = FastAPI(title="LWT User Registry", version="0.1.0", lifespan=lifespan)


# ------------------------------------------------------------------
# JSON API — registration
# ------------------------------------------------------------------


@app.post("/api/users", status_code=201)
async def api_register_user(
    username: str,
    email: str,
    display_name: str,
    dimension: str,
) -> dict:
    """Register a user with IF NOT EXISTS — returns 409 on duplicate."""
    reg = UserRegistration(
        username=username,
        email=email,
        display_name=display_name,
        dimension=dimension,
    )
    result = await _do_register(reg)
    if not result["applied"]:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "username_taken",
                "existing": result["existing"],
            },
        )
    return {"applied": True, "username": username}


@app.get("/api/users", response_model=list[UserRegistration])
async def api_list_users(
    dimension: str | None = Query(default=None),
) -> list[UserRegistration]:
    """List all registered users (optionally filter by dimension)."""
    qs = UserRegistration.find()
    if dimension:
        qs = qs.filter(dimension=dimension).allow_filtering()
    return await qs.all()


@app.get("/api/users/{username}")
async def api_get_user(username: str) -> dict:
    """Get a single user registration."""
    reg = await UserRegistration.find_one(username=username)
    if reg is None:
        raise HTTPException(status_code=404, detail="User not found")
    return reg.model_dump(mode="json")


@app.delete("/api/users/{username}", status_code=204)
async def api_delete_user(username: str) -> None:
    """Delete a registration with IF EXISTS — no-op if missing."""
    reg = await UserRegistration.find_one(username=username)
    if reg is None:
        raise HTTPException(status_code=404, detail="User not found")
    await reg.delete(if_exists=True)


# ------------------------------------------------------------------
# JSON API — profiles (optimistic locking)
# ------------------------------------------------------------------


@app.get("/api/profiles/{user_id}")
async def api_get_profile(user_id: UUID) -> dict:
    """Get a user profile."""
    profile = await UserProfile.find_one(user_id=user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile.model_dump(mode="json")


@app.put("/api/profiles/{user_id}")
async def api_update_profile(
    user_id: UUID,
    bio: str | None = None,
    status: str | None = None,
    expected_version: int | None = None,
) -> dict:
    """Update a profile with optimistic locking (IF version = expected_version)."""
    profile = await UserProfile.find_one(user_id=user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    updates: dict = {"updated_at": datetime.now(timezone.utc), "version": profile.version + 1}
    if bio is not None:
        updates["bio"] = bio
    if status is not None:
        updates["status"] = status

    if expected_version is not None:
        result = await profile.update(
            if_conditions={"version": expected_version},
            **updates,
        )
        if result and not result.applied:
            raise HTTPException(
                status_code=409,
                detail={"error": "version_conflict", "existing": result.existing},
            )
    else:
        result = await profile.update(if_exists=True, **updates)
        if result and not result.applied:
            raise HTTPException(status_code=404, detail="Profile not found")

    return {"applied": True, "user_id": str(user_id), "version": updates["version"]}


# ------------------------------------------------------------------
# HTMX UI routes
# ------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def ui_index(request: Request) -> HTMLResponse:
    total = len(await UserRegistration.find().all())
    return templates.TemplateResponse("index.html", {"request": request, "total": total})


@app.get("/ui/users", response_class=HTMLResponse)
async def ui_list_users(
    request: Request,
    dimension: str | None = Query(default=None),
) -> HTMLResponse:
    qs = UserRegistration.find()
    if dimension:
        qs = qs.filter(dimension=dimension).allow_filtering()
    users = await qs.all()
    return templates.TemplateResponse(
        "partials/user_list.html",
        {"request": request, "users": users},
    )


@app.post("/ui/register", response_class=HTMLResponse)
async def ui_register(
    request: Request,
    username: str = Form(),
    email: str = Form(),
    display_name: str = Form(),
    dimension: str = Form(),
) -> HTMLResponse:
    reg = UserRegistration(
        username=username,
        email=email,
        display_name=display_name,
        dimension=dimension,
    )
    result = await _do_register(reg)
    users = await UserRegistration.find().all()
    return templates.TemplateResponse(
        "partials/register_result.html",
        {
            "request": request,
            "applied": result["applied"],
            "username": username,
            "existing": result.get("existing"),
            "users": users,
        },
    )


@app.get("/ui/users/{username}", response_class=HTMLResponse)
async def ui_user_detail(request: Request, username: str) -> HTMLResponse:
    reg = await UserRegistration.find_one(username=username)
    if reg is None:
        raise HTTPException(status_code=404, detail="User not found")
    profile = await UserProfile.find_one(user_id=reg.user_id)
    return templates.TemplateResponse(
        "partials/profile.html",
        {"request": request, "reg": reg, "profile": profile},
    )


@app.post("/ui/users/{username}/update-profile", response_class=HTMLResponse)
async def ui_update_profile(
    request: Request,
    username: str,
    bio: str = Form(default=""),
    status: str = Form(default="active"),
    expected_version: int = Form(),
) -> HTMLResponse:
    reg = await UserRegistration.find_one(username=username)
    if reg is None:
        raise HTTPException(status_code=404, detail="User not found")

    profile = await UserProfile.find_one(user_id=reg.user_id)
    applied = False
    conflict_existing = None

    if profile is None:
        # First profile save — no optimistic lock needed
        profile = UserProfile(
            user_id=reg.user_id,
            username=username,
            bio=bio or None,
            status=status,
            version=1,
        )
        await profile.save()
        applied = True
    else:
        result = await profile.update(
            if_conditions={"version": expected_version},
            bio=bio or None,
            status=status,
            updated_at=datetime.now(timezone.utc),
            version=expected_version + 1,
        )
        if result is None or result.applied:
            applied = True
        else:
            conflict_existing = result.existing
            # Reload the current profile so UI shows latest state
            profile = await UserProfile.find_one(user_id=reg.user_id)

    return templates.TemplateResponse(
        "partials/profile.html",
        {
            "request": request,
            "reg": reg,
            "profile": profile,
            "applied": applied,
            "conflict_existing": conflict_existing,
        },
    )


@app.delete("/ui/users/{username}", response_class=HTMLResponse)
async def ui_delete_user(request: Request, username: str) -> HTMLResponse:
    reg = await UserRegistration.find_one(username=username)
    if reg is not None:
        await reg.delete(if_exists=True)
    users = await UserRegistration.find().all()
    return templates.TemplateResponse(
        "partials/user_list.html",
        {"request": request, "users": users},
    )


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


async def _do_register(reg: UserRegistration) -> dict:
    """Execute INSERT IF NOT EXISTS and return a result dict.

    Uses coodie's internal CQL builder to generate the IF NOT EXISTS clause
    and parses the Cassandra LWT ``[applied]`` response column.
    """
    cls = UserRegistration
    columns = _insert_columns(cls)
    values = [getattr(reg, c) for c in columns]
    cql, params = build_insert_from_columns(
        cls._get_table(),
        cls._get_keyspace(),
        columns,
        values,
        if_not_exists=True,
    )
    rows = await cls._get_driver().execute_async(cql, params)
    lwt = _parse_lwt_result(rows)
    existing: dict | None = None
    if lwt.existing:
        # Serialize datetime values for JSON compatibility
        existing = {
            k: v.isoformat() if isinstance(v, datetime) else str(v) if not isinstance(v, (str, int, float, bool)) else v
            for k, v in lwt.existing.items()
        }
    return {"applied": lwt.applied, "existing": existing}
