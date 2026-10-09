"""Seed the IoT sensor network with synthetic telemetry data.

Usage:
    python seed.py                          # 5 sensors, 3 days, 50 readings/day
    python seed.py --sensors 10             # 10 sensors
    python seed.py --days 7                 # 7 days of data
    python seed.py --readings-per-day 100   # 100 readings per sensor per day
"""

from __future__ import annotations

import asyncio
import os
import random
from datetime import datetime, timedelta, timezone

import click
from models import SensorReading
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.text import Text

from coodie.aio import init_coodie

console = Console()

# --- Themed sensor data pools ---

SENSOR_NAMES = [
    "reactor-core-A1",
    "coolant-loop-B2",
    "exhaust-vent-C3",
    "cryo-chamber-D4",
    "engine-bay-E5",
    "cargo-hold-F6",
    "bridge-console-G7",
    "med-bay-H8",
    "airlock-sector-I9",
    "lab-module-J10",
    "comm-array-K11",
    "nav-beacon-L12",
]

LOCATIONS = {
    "reactor-core-A1": "Deck 1 — Reactor Core",
    "coolant-loop-B2": "Deck 1 — Coolant System",
    "exhaust-vent-C3": "Deck 2 — Exhaust Array",
    "cryo-chamber-D4": "Deck 3 — Cryo Bay",
    "engine-bay-E5": "Deck 1 — Engine Bay",
    "cargo-hold-F6": "Deck 4 — Cargo Hold",
    "bridge-console-G7": "Deck 5 — Bridge",
    "med-bay-H8": "Deck 3 — Medical Bay",
    "airlock-sector-I9": "Deck 2 — Airlock",
    "lab-module-J10": "Deck 3 — Science Lab",
    "comm-array-K11": "Deck 5 — Comms Array",
    "nav-beacon-L12": "Deck 5 — Navigation",
}


def _generate_reading(sensor_id: str, ts: datetime) -> dict:
    """Generate a single sensor reading with realistic-ish values."""
    base_temp = {"reactor": 85.0, "coolant": 15.0, "cryo": -40.0, "engine": 70.0}
    temp_base = 22.0
    for prefix, base in base_temp.items():
        if sensor_id.startswith(prefix):
            temp_base = base
            break

    return {
        "sensor_id": sensor_id,
        "date_bucket": ts.date(),
        "ts": ts,
        "temperature": round(temp_base + random.gauss(0, 3.0), 2),
        "humidity": round(max(0, min(100, 45.0 + random.gauss(0, 10.0))), 2),
        "pressure": round(1013.25 + random.gauss(0, 5.0), 2),
        "battery_pct": max(0, min(100, int(95 + random.gauss(0, 5)))),
    }


def _print_briefing(num_sensors: int, days: int, rpd: int) -> None:
    """Print the mission briefing story panel."""
    story = Text()
    story.append("STATION ARGOS-7", style="bold cyan")
    story.append(" — Deep in the Scylla Nebula,\n")
    story.append("the station's ", style="dim")
    story.append(f"{num_sensors}", style="bold yellow")
    story.append(" environmental sensors", style="dim")
    story.append(" relay critical\ntelemetry to Central Command.\n\n")
    story.append("Each sensor transmits ")
    story.append(f"~{rpd} readings/day", style="bold yellow")
    story.append(f" across {days} days", style="bold yellow")
    story.append(",\n")
    story.append("bucketed by date into compact partitions.\n")
    story.append("The newest readings surface first — ")
    story.append("DESC clustering", style="bold cyan")
    story.append(" ensures\nthe crew always sees the most recent data.\n\n")
    story.append("Total readings: ", style="dim")
    story.append(f"{num_sensors * days * rpd:,}", style="bold green")

    console.print()
    console.print(
        Panel(
            story,
            title="[bold cyan]📡 MISSION BRIEFING — STATION ARGOS-7 // SENSOR GRID[/]",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    console.print()


async def _seed(num_sensors: int, days: int, rpd: int) -> None:
    """Connect to ScyllaDB, sync tables, and insert sensor readings."""
    _print_briefing(num_sensors, days, rpd)

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "iot")

    console.print("[dim]📡 Establishing uplink to ScyllaDB node...[/]")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    console.print("[dim]🔧 Synchronizing sensor tables...[/]")
    await SensorReading.sync_table()
    console.print("[dim green]✓ Database ready.[/]")
    console.print()

    sensors = SENSOR_NAMES[:num_sensors]
    today = datetime.now(timezone.utc).date()
    total = 0

    for sensor_id in sensors:
        location = LOCATIONS.get(sensor_id, "Unknown Deck")
        items = []
        for day_offset in range(days):
            bucket_date = today - timedelta(days=days - 1 - day_offset)
            for _ in range(rpd):
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                ts = datetime(
                    bucket_date.year,
                    bucket_date.month,
                    bucket_date.day,
                    hour,
                    minute,
                    second,
                    tzinfo=timezone.utc,
                )
                items.append(_generate_reading(sensor_id, ts))

        for data in track(
            items,
            description=f"[cyan]📡 {sensor_id:<22} ({location})[/]",
            console=console,
        ):
            reading = SensorReading(**data)
            await reading.save()
            total += 1

    # --- Summary table ---
    console.print()
    table = Table(
        title="[bold]📡 STATION ARGOS-7 — Sensor Grid Status[/]",
        border_style="cyan",
        title_style="bold cyan",
    )
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right", style="green")
    table.add_column("Note", style="dim")
    table.add_row("Sensors Online", str(len(sensors)), "✓ Transmitting")
    table.add_row("Days of Data", str(days), "✓ Time-bucketed partitions")
    table.add_row("Readings/Sensor/Day", str(rpd), "✓ ClusteringKey DESC")
    table.add_row("Total Readings", f"{total:,}", "✓ Stored in ScyllaDB")
    table.add_row(
        "Partitions Created",
        str(len(sensors) * days),
        "✓ (sensor_id, date_bucket)",
    )
    console.print(table)
    console.print()
    console.print(f"[bold cyan]📡 {total:,} readings transmitted. Station Argos-7 sensors nominal.[/]")
    console.print("[dim]   Launch the dashboard with: uv run uvicorn main:app --reload[/]")
    console.print()


@click.command()
@click.option("--sensors", default=5, help="Number of sensors to simulate")
@click.option("--days", default=3, help="Number of days of historical data")
@click.option("--readings-per-day", "rpd", default=50, help="Readings per sensor per day")
def seed(sensors: int, days: int, rpd: int) -> None:
    """Seed Station Argos-7 with synthetic sensor telemetry."""
    asyncio.run(_seed(sensors, days, rpd))


if __name__ == "__main__":
    seed()
