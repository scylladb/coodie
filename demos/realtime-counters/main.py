"""FastAPI Realtime Counters demo — The Pulse Engine.

Showcases coodie's CounterDocument support:
- ``CounterDocument`` base class for counter tables
- ``Annotated[int, Counter()]`` for counter columns
- ``increment(**field_deltas)`` for atomic counter increments
- ``decrement(**field_deltas)`` for atomic counter decrements
- Counter tables forbid ``save()`` / ``insert()``

Traffic simulator: spin up virtual users that continuously hit
counters in random patterns, visible on the live dashboard.
"""

from __future__ import annotations

__version__ = "0.2.0"

import asyncio
import logging
import os
import random
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import PageViewCounter

from coodie.aio import init_coodie

logger = logging.getLogger("coodie.demos.counters")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# ------------------------------------------------------------------
# Virtual user traffic patterns
# ------------------------------------------------------------------

URLS = [
    "/dashboard",
    "/products",
    "/products/quantum-flux-capacitor",
    "/products/dimensional-anchor",
    "/blog/scylla-9-incident-report",
    "/blog/dimensional-rift-survival-guide",
    "/docs/getting-started",
    "/docs/counter-patterns",
    "/api/v1/timeline-sync",
    "/missions/active",
]


class TrafficPattern:
    """Defines a virtual user's behaviour: how they hit counters."""

    def __init__(
        self, name: str, *, inc_weight: int = 8, dec_weight: int = 2, min_delay: float = 0.3, max_delay: float = 2.0
    ):
        self.name = name
        self.inc_weight = inc_weight
        self.dec_weight = dec_weight
        self.min_delay = min_delay
        self.max_delay = max_delay


PATTERNS: dict[str, TrafficPattern] = {
    "casual": TrafficPattern("casual", inc_weight=9, dec_weight=1, min_delay=1.0, max_delay=3.0),
    "power": TrafficPattern("power", inc_weight=7, dec_weight=3, min_delay=0.3, max_delay=1.0),
    "bursty": TrafficPattern("bursty", inc_weight=8, dec_weight=2, min_delay=0.1, max_delay=0.5),
    "balanced": TrafficPattern("balanced", inc_weight=5, dec_weight=5, min_delay=0.5, max_delay=2.0),
}


class VirtualUser:
    """A background asyncio task that continuously hits counters."""

    def __init__(self, user_id: str, pattern: TrafficPattern):
        self.user_id = user_id
        self.pattern = pattern
        self.hits: int = 0
        self.task: asyncio.Task | None = None

    async def run(self) -> None:
        """Loop: pick a random URL, increment or decrement, sleep."""
        today = date.today().isoformat()  # noqa: DTZ011 - demo uses the server's local date
        while True:
            url = random.choice(URLS)
            counter = PageViewCounter(url=url, date=today)
            views = random.randint(1, 5)
            visitors = random.randint(0, 1)
            is_increment = random.choices(
                [True, False],
                weights=[self.pattern.inc_weight, self.pattern.dec_weight],
            )[0]
            try:
                if is_increment:
                    await counter.increment(view_count=views, unique_visitors=visitors)
                else:
                    await counter.decrement(view_count=views, unique_visitors=visitors)
                self.hits += 1
            except Exception:
                logger.exception("Virtual user %s hit error", self.user_id)
            delay = random.uniform(self.pattern.min_delay, self.pattern.max_delay)
            await asyncio.sleep(delay)


class TrafficSimulator:
    """Manages a pool of virtual users generating counter traffic."""

    def __init__(self) -> None:
        self.users: dict[str, VirtualUser] = {}

    def start_users(self, count: int = 1, pattern_name: str = "casual") -> list[str]:
        """Spawn *count* virtual users with the given traffic pattern."""
        pattern = PATTERNS.get(pattern_name, PATTERNS["casual"])
        started: list[str] = []
        for _ in range(count):
            user_id = f"agent-{uuid.uuid4().hex[:6]}"
            vu = VirtualUser(user_id, pattern)
            vu.task = asyncio.create_task(vu.run(), name=f"vu-{user_id}")
            self.users[user_id] = vu
            started.append(user_id)
        return started

    def stop_user(self, user_id: str) -> bool:
        """Stop a single virtual user. Returns True if found."""
        vu = self.users.pop(user_id, None)
        if vu and vu.task:
            vu.task.cancel()
            return True
        return False

    def stop_all(self) -> int:
        """Stop all virtual users. Returns the count stopped."""
        count = len(self.users)
        for vu in self.users.values():
            if vu.task:
                vu.task.cancel()
        self.users.clear()
        return count

    def status(self) -> dict:
        """Return a summary of all active virtual users."""
        users_info = []
        for uid, vu in self.users.items():
            users_info.append({"id": uid, "pattern": vu.pattern.name, "hits": vu.hits})
        total_hits = sum(u["hits"] for u in users_info)
        return {"active_users": len(self.users), "total_hits": total_hits, "users": users_info}


simulator = TrafficSimulator()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup: connect to ScyllaDB and sync tables."""
    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "analytics")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    await PageViewCounter.sync_table()
    yield
    simulator.stop_all()


app = FastAPI(
    title="Realtime Counters — The Pulse Engine",
    version="0.2.0",
    lifespan=lifespan,
)


# ------------------------------------------------------------------
# JSON API routes
# ------------------------------------------------------------------


@app.get("/counters")
async def list_counters() -> list[dict]:
    """Return all page-view counters."""
    counters = await PageViewCounter.find().allow_filtering().all()
    return [
        {
            "url": c.url,
            "date": c.date,
            "view_count": c.view_count,
            "unique_visitors": c.unique_visitors,
        }
        for c in counters
    ]


@app.get("/counters/{url:path}")
async def get_counter(url: str, date: str | None = None) -> list[dict]:
    """Get counters for a specific URL, optionally filtered by date."""
    kwargs: dict = {"url": url}
    if date:
        kwargs["date"] = date
    counters = await PageViewCounter.find(**kwargs).all()
    if not counters:
        raise HTTPException(status_code=404, detail="No counters found for this URL")
    return [
        {
            "url": c.url,
            "date": c.date,
            "view_count": c.view_count,
            "unique_visitors": c.unique_visitors,
        }
        for c in counters
    ]


@app.post("/counters/increment", status_code=200)
async def increment_counter(
    url: str,
    date: str,
    view_count: int = 1,
    unique_visitors: int = 0,
) -> dict:
    """Increment counters for a URL/date pair.

    Demonstrates ``CounterDocument.increment(**field_deltas)``.
    """
    counter = PageViewCounter(url=url, date=date)
    await counter.increment(view_count=view_count, unique_visitors=unique_visitors)
    return {"url": url, "date": date, "incremented": {"view_count": view_count, "unique_visitors": unique_visitors}}


@app.post("/counters/decrement", status_code=200)
async def decrement_counter(
    url: str,
    date: str,
    view_count: int = 1,
    unique_visitors: int = 0,
) -> dict:
    """Decrement counters for a URL/date pair.

    Demonstrates ``CounterDocument.decrement(**field_deltas)``.
    """
    counter = PageViewCounter(url=url, date=date)
    await counter.decrement(view_count=view_count, unique_visitors=unique_visitors)
    return {"url": url, "date": date, "decremented": {"view_count": view_count, "unique_visitors": unique_visitors}}


# ------------------------------------------------------------------
# Traffic Simulator JSON API
# ------------------------------------------------------------------


@app.post("/sim/start")
async def sim_start(count: int = 3, pattern: str = "casual") -> dict:
    """Start virtual users that continuously hit counters.

    Patterns: casual (slow), power (fast), bursty (very fast), balanced (50/50 inc/dec).
    """
    started = simulator.start_users(count=count, pattern_name=pattern)
    return {"started": started, "pattern": pattern, **simulator.status()}


@app.post("/sim/stop")
async def sim_stop(user_id: str | None = None) -> dict:
    """Stop one virtual user (by ID) or all if no ID given."""
    if user_id:
        found = simulator.stop_user(user_id)
        if not found:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return {"stopped": user_id, **simulator.status()}
    count = simulator.stop_all()
    return {"stopped_all": count, **simulator.status()}


@app.get("/sim/status")
async def sim_status() -> dict:
    """Return current simulator status: active users, hit counts, patterns."""
    return simulator.status()


# ------------------------------------------------------------------
# HTMX UI routes
# ------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def ui_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        context={"patterns": list(PATTERNS.keys()), "sim": simulator.status()},
    )


async def _render_counter_list(request: Request) -> HTMLResponse:
    """Fetch all counters and render the list partial (date descending)."""
    counters = await PageViewCounter.find().allow_filtering().all()
    counters_sorted = sorted(counters, key=lambda c: (c.date, c.url), reverse=True)
    total_views = sum(c.view_count for c in counters_sorted)
    total_visitors = sum(c.unique_visitors for c in counters_sorted)
    return templates.TemplateResponse(
        request,
        "partials/counter_list.html",
        context={
            "counters": counters_sorted,
            "today": date.today().isoformat(),  # noqa: DTZ011 - demo uses the server's local date
            "total_views": total_views,
            "total_visitors": total_visitors,
        },
    )


@app.get("/ui/counters", response_class=HTMLResponse)
async def ui_list_counters(request: Request) -> HTMLResponse:
    return await _render_counter_list(request)


@app.post("/ui/counters/increment", response_class=HTMLResponse)
async def ui_increment_counter(
    request: Request,
    url: str = Form(),
    date: str = Form(),
    view_count: int = Form(default=1),
    unique_visitors: int = Form(default=0),
) -> HTMLResponse:
    """Increment a counter from the HTMX form and return the updated list."""
    counter = PageViewCounter(url=url, date=date)
    await counter.increment(view_count=view_count, unique_visitors=unique_visitors)
    return await _render_counter_list(request)


@app.post("/ui/counters/decrement", response_class=HTMLResponse)
async def ui_decrement_counter(
    request: Request,
    url: str = Form(),
    date: str = Form(),
    view_count: int = Form(default=1),
    unique_visitors: int = Form(default=0),
) -> HTMLResponse:
    """Decrement a counter from the HTMX form and return the updated list."""
    counter = PageViewCounter(url=url, date=date)
    await counter.decrement(view_count=view_count, unique_visitors=unique_visitors)
    return await _render_counter_list(request)


# ------------------------------------------------------------------
# HTMX Simulator UI routes
# ------------------------------------------------------------------


@app.get("/ui/sim/status", response_class=HTMLResponse)
async def ui_sim_status(request: Request) -> HTMLResponse:
    """Return the simulator status partial for HTMX polling."""
    return templates.TemplateResponse(request, "partials/sim_status.html", context={"sim": simulator.status()})


@app.post("/ui/sim/start", response_class=HTMLResponse)
async def ui_sim_start(
    request: Request,
    count: int = Form(default=3),
    pattern: str = Form(default="casual"),
) -> HTMLResponse:
    """Start virtual users from the HTMX form."""
    simulator.start_users(count=count, pattern_name=pattern)
    return templates.TemplateResponse(request, "partials/sim_status.html", context={"sim": simulator.status()})


@app.post("/ui/sim/stop", response_class=HTMLResponse)
async def ui_sim_stop(
    request: Request,
    user_id: str = Form(default=""),
) -> HTMLResponse:
    """Stop one or all virtual users from the HTMX form."""
    if user_id:
        simulator.stop_user(user_id)
    else:
        simulator.stop_all()
    return templates.TemplateResponse(request, "partials/sim_status.html", context={"sim": simulator.status()})
