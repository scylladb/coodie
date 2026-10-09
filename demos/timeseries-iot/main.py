"""FastAPI IoT Sensor Dashboard — Station Argos-7.

Showcases coodie's time-series capabilities:
- **Time-bucketed partitions** — ``(sensor_id, date_bucket)`` composite PK
- **ClusteringKey(order="DESC")** — newest readings first within each partition
- **per_partition_limit()** — latest N readings per sensor in one query
- **paged_all()** — cursor-based pagination across large result sets
- **Background device** — continuously generates new sensor telemetry for ALL sensors
- **Real-time dashboard** — auto-updates as new data arrives
- **Live charts** — Chart.js line charts with auto-refreshing time-series data
- **Infinite scroll** — scroll-triggered pagination with date filtering
"""

from __future__ import annotations

__version__ = "0.3.0"

import asyncio
import base64
import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import SensorReading
from seed import _generate_reading

from coodie.aio import init_coodie
from coodie.results import PagedResult

logger = logging.getLogger("coodie")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# --- Background device configuration ---
DEVICE_INTERVAL = float(os.getenv("DEVICE_INTERVAL", "3"))  # seconds between readings


def _utc_today() -> date:
    """Return today's date in UTC (matches the date_bucket written by the background device)."""
    return datetime.now(timezone.utc).date()


DEVICE_SENSORS: list[str] = []  # populated at startup from DB or defaults
_bg_task: asyncio.Task[None] | None = None

_DEFAULT_SENSORS = [
    "reactor-core-A1",
    "coolant-loop-B2",
    "exhaust-vent-C3",
    "cryo-chamber-D4",
    "engine-bay-E5",
]


def _generate_live_reading(sensor_id: str) -> dict:
    """Generate a single sensor reading with realistic-ish values."""
    return _generate_reading(sensor_id, datetime.now(timezone.utc))


async def _background_device_loop() -> None:
    """Continuously generate new sensor readings for ALL sensors each cycle."""
    # Wait briefly for startup to complete
    await asyncio.sleep(2)

    # Discover existing sensors or use defaults; cache the result
    await _ensure_sensors_loaded()

    logger.info("Background device started — %d sensors, interval=%ss", len(DEVICE_SENSORS), DEVICE_INTERVAL)
    while True:
        try:
            # Generate a new reading for EVERY sensor each cycle
            for sensor_id in DEVICE_SENSORS:
                data = _generate_live_reading(sensor_id)
                reading = SensorReading(**data)
                await reading.save()
        except asyncio.CancelledError:
            logger.info("Background device stopped")
            return
        except Exception:
            logger.exception("Background device error")
        await asyncio.sleep(DEVICE_INTERVAL)


async def _ensure_sensors_loaded() -> list[str]:
    """Return cached sensor list, discovering from DB once if needed.

    Populates ``DEVICE_SENSORS`` on the first call and reuses the cache
    afterwards — avoids the ``ALLOW FILTERING`` full-table scan on every
    dashboard refresh.
    """
    if DEVICE_SENSORS:
        return DEVICE_SENSORS

    today = _utc_today()
    sensor_ids: set[str] = set()
    for day_offset in range(3):
        bucket = today - timedelta(days=day_offset)
        readings = await SensorReading.find(date_bucket=bucket).per_partition_limit(1).allow_filtering().all()
        for r in readings:
            sensor_ids.add(r.sensor_id)

    sensors = sorted(sensor_ids) if sensor_ids else list(_DEFAULT_SENSORS)
    DEVICE_SENSORS.clear()
    DEVICE_SENSORS.extend(sensors)
    return DEVICE_SENSORS


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup: connect to ScyllaDB, sync tables, and start background device."""
    global _bg_task

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "iot")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    await SensorReading.sync_table()

    # Start the background device unless explicitly disabled
    if os.getenv("DISABLE_BACKGROUND_DEVICE", "").lower() not in ("1", "true", "yes"):
        _bg_task = asyncio.create_task(_background_device_loop())

    yield

    # Shutdown: cancel the background device
    if _bg_task and not _bg_task.done():
        _bg_task.cancel()
        try:
            await _bg_task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="IoT Sensor Dashboard — Station Argos-7",
    version=__version__,
    lifespan=lifespan,
)


# ------------------------------------------------------------------
# JSON API routes
# ------------------------------------------------------------------


@app.get("/sensors")
async def list_sensors() -> list[str]:
    """Return distinct sensor IDs found in the data."""
    return await _ensure_sensors_loaded()


@app.get("/sensors/{sensor_id}/latest")
async def get_latest_readings(
    sensor_id: str,
    days: int = Query(default=1, ge=1, le=30),
    limit: int = Query(default=5, ge=1, le=100),
) -> list[SensorReading]:
    """Get the latest readings for a sensor using per_partition_limit().

    Demonstrates ``per_partition_limit(n)`` — returns at most ``limit``
    rows from each daily partition for the given sensor.
    """
    today = _utc_today()
    all_readings: list[SensorReading] = []
    for day_offset in range(days):
        bucket = today - timedelta(days=day_offset)
        readings = await SensorReading.find(sensor_id=sensor_id, date_bucket=bucket).per_partition_limit(limit).all()
        all_readings.extend(readings)
    return all_readings


@app.get("/readings/paged")
async def get_paged_readings(
    sensor_id: str | None = Query(default=None),
    bucket: date | None = Query(default=None),  # noqa: B008 - FastAPI dependency declaration
    start_date: date | None = Query(default=None),  # noqa: B008 - FastAPI dependency declaration
    page_size: int = Query(default=10, ge=1, le=100),
    cursor: str | None = Query(default=None),
) -> dict:
    """Paginated reading list using paged_all().

    Demonstrates ``paged_all()`` — returns a ``PagedResult`` with a
    ``paging_state`` cursor that can be passed back to fetch the next page.

    If ``start_date`` is given, queries partitions from that date forward to today.
    """
    if start_date and not bucket:
        # Query across date range: collect from start_date to today (max 30 days).
        # Uses offset-based cursors (the offset is encoded in the cursor).
        today = _utc_today()
        max_range = timedelta(days=30)
        if today - start_date > max_range:
            start_date = today - max_range

        offset = 0
        if cursor:
            try:
                offset = int(base64.urlsafe_b64decode(cursor.encode()).decode())
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid cursor")

        # Collect readings across all date partitions in the range
        all_readings: list[SensorReading] = []
        current = start_date
        while current <= today:
            qs = SensorReading.find(date_bucket=current)
            if sensor_id:
                qs = qs.filter(sensor_id=sensor_id)
            readings = await qs.allow_filtering().all()
            all_readings.extend(readings)
            current += timedelta(days=1)

        # Apply offset-based pagination
        page_data = all_readings[offset : offset + page_size]
        has_more = len(all_readings) > offset + page_size
        next_cursor = None
        if has_more:
            next_cursor = base64.urlsafe_b64encode(str(offset + page_size).encode()).decode()

        return {
            "data": [r.model_dump(mode="json") for r in page_data],
            "next_cursor": next_cursor,
            "has_more": has_more,
        }

    qs = SensorReading.find()
    if sensor_id:
        qs = qs.filter(sensor_id=sensor_id)
    if bucket:
        qs = qs.filter(date_bucket=bucket)

    qs = qs.fetch_size(page_size).allow_filtering()
    if cursor:
        try:
            paging_bytes = base64.urlsafe_b64decode(cursor.encode())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid cursor")
        qs = qs.page(paging_bytes)

    result: PagedResult = await qs.paged_all()
    next_cursor = None
    if result.paging_state:
        next_cursor = base64.urlsafe_b64encode(result.paging_state).decode()

    return {
        "data": [r.model_dump(mode="json") for r in result.data],
        "next_cursor": next_cursor,
        "has_more": result.paging_state is not None,
    }


@app.get("/device/status")
async def device_status() -> dict:
    """Return the background device status."""
    return {
        "running": _bg_task is not None and not _bg_task.done(),
        "sensors": DEVICE_SENSORS,
        "interval_seconds": DEVICE_INTERVAL,
    }


@app.get("/sensors/{sensor_id}/chart")
async def get_chart_data(
    sensor_id: str,
    minutes: int = Query(default=5, ge=1, le=60),
) -> dict:
    """Return recent time-series data for a sensor, formatted for Chart.js.

    Returns the last ``minutes`` of readings with timestamps and metric values
    as separate arrays suitable for Chart.js line charts.
    """
    today = _utc_today()
    readings: list[SensorReading] = []

    # Query today's partition first; only query yesterday if the time window spans midnight
    day_readings = await SensorReading.find(sensor_id=sensor_id, date_bucket=today).per_partition_limit(200).all()
    readings.extend(day_readings)

    # If the requested window extends past midnight, also query yesterday
    cutoff = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).replace(tzinfo=None)
    if cutoff.date() < today:
        yesterday = today - timedelta(days=1)
        day_readings = (
            await SensorReading.find(sensor_id=sensor_id, date_bucket=yesterday).per_partition_limit(200).all()
        )
        readings.extend(day_readings)

    # Filter to the requested time window
    recent = [r for r in readings if r.ts and r.ts >= cutoff]
    # Sort chronologically (oldest first) for chart display
    recent.sort(key=lambda r: r.ts)

    return {
        "sensor_id": sensor_id,
        "labels": [r.ts.strftime("%H:%M:%S") for r in recent],
        "temperature": [round(r.temperature, 2) for r in recent],
        "humidity": [round(r.humidity, 1) for r in recent],
        "pressure": [round(r.pressure, 1) for r in recent],
        "battery_pct": [r.battery_pct for r in recent],
        "count": len(recent),
    }


# ------------------------------------------------------------------
# HTMX UI routes
# ------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def ui_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@app.get("/ui/dashboard", response_class=HTMLResponse)
async def ui_dashboard(request: Request) -> HTMLResponse:
    """Return the sensor dashboard partial with latest readings per sensor."""
    today = _utc_today()
    sensors: dict[str, list[SensorReading]] = {}

    sensor_ids = await _ensure_sensors_loaded()

    # Get latest 5 readings per sensor (today's partition)
    for sid in sensor_ids:
        readings = await SensorReading.find(sensor_id=sid, date_bucket=today).per_partition_limit(5).all()
        if not readings:
            # Try yesterday if no data today
            yesterday = today - timedelta(days=1)
            readings = await SensorReading.find(sensor_id=sid, date_bucket=yesterday).per_partition_limit(5).all()
        sensors[sid] = readings

    device_active = _bg_task is not None and not _bg_task.done()
    return templates.TemplateResponse(
        request,
        "partials/dashboard.html",
        context={"sensors": sensors, "device_active": device_active},
    )


@app.get("/ui/sensor/{sensor_id}", response_class=HTMLResponse)
async def ui_sensor_detail(
    request: Request,
    sensor_id: str,
    days: int = Query(default=3, ge=1, le=7),
) -> HTMLResponse:
    """Return paginated reading history for a single sensor."""
    today = _utc_today()
    readings: list[SensorReading] = []
    for day_offset in range(days):
        bucket = today - timedelta(days=day_offset)
        day_readings = await SensorReading.find(sensor_id=sensor_id, date_bucket=bucket).per_partition_limit(20).all()
        readings.extend(day_readings)

    return templates.TemplateResponse(
        request,
        "partials/sensor_detail.html",
        context={"sensor_id": sensor_id, "readings": readings, "days": days},
    )


@app.get("/ui/paged", response_class=HTMLResponse)
async def ui_paged_readings(
    request: Request,
    page_size: int = Query(default=15, ge=1, le=50),
    cursor: str | None = Query(default=None),
    start_date: date | None = Query(default=None),  # noqa: B008 - FastAPI dependency declaration
    sensor_id: str | None = Query(default=None),
) -> HTMLResponse:
    """Return a page of readings using paged_all() for HTMX infinite scroll.

    Supports filtering by ``start_date`` and ``sensor_id``.
    """
    qs = SensorReading.find()

    if sensor_id:
        qs = qs.filter(sensor_id=sensor_id)
    if start_date:
        # Filter to the specific start_date partition; for multi-day range,
        # use the JSON API at /readings/paged?start_date=...
        qs = qs.filter(date_bucket=start_date)

    qs = qs.fetch_size(page_size).allow_filtering()
    if cursor:
        try:
            paging_bytes = base64.urlsafe_b64decode(cursor.encode())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid cursor")
        qs = qs.page(paging_bytes)

    result: PagedResult = await qs.paged_all()
    next_cursor = None
    if result.paging_state:
        next_cursor = base64.urlsafe_b64encode(result.paging_state).decode()

    return templates.TemplateResponse(
        request,
        "partials/paged_readings.html",
        context={
            "readings": result.data,
            "next_cursor": next_cursor,
            "page_size": page_size,
            "start_date": start_date.isoformat() if start_date else "",
            "sensor_id": sensor_id or "",
        },
    )


@app.get("/ui/charts", response_class=HTMLResponse)
async def ui_charts(request: Request) -> HTMLResponse:
    """Return the live charts partial with sensor list for Chart.js."""
    sensor_ids = await _ensure_sensors_loaded()
    device_active = _bg_task is not None and not _bg_task.done()
    return templates.TemplateResponse(
        request,
        "partials/charts.html",
        context={"sensor_ids": sensor_ids, "device_active": device_active},
    )
