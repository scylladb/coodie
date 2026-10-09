"""Seed the analytics database with synthetic page-view traffic.

Usage:
    python seed.py                      # 200 increments across 10 pages
    python seed.py --count 500          # 500 increments
    python seed.py --pages 20           # spread across 20 pages
"""

from __future__ import annotations

import asyncio
import os
import random

import click
from models import PageViewCounter
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.text import Text

from coodie.aio import init_coodie

console = Console()

# --- Story-themed data pools ---

PAGES = [
    "/dashboard",
    "/products",
    "/products/quantum-flux-capacitor",
    "/products/dimensional-anchor",
    "/products/timeline-compass",
    "/blog/scylla-9-incident-report",
    "/blog/dimensional-rift-survival-guide",
    "/blog/coodie-corps-recruitment",
    "/docs/getting-started",
    "/docs/counter-patterns",
    "/docs/migration-playbook",
    "/api/v1/timeline-sync",
    "/api/v1/agent-registry",
    "/about",
    "/contact",
    "/login",
    "/settings",
    "/analytics",
    "/missions/active",
    "/missions/archived",
]

DATES = [
    "2026-03-01",
    "2026-03-02",
    "2026-03-03",
    "2026-02-28",
    "2026-02-27",
]


def _print_briefing(count: int, num_pages: int) -> None:
    """Print the mission briefing story panel."""
    story = Text()
    story.append("DIMENSION-7", style="bold magenta")
    story.append(" — In the command center of the Coodie Corps,\n")
    story.append("PULSE", style="bold red")
    story.append(", the analytics engine, tracks every agent's\n")
    story.append("movement across the interdimensional network.\n")
    story.append("Every page hit is a counter increment — ")
    story.append("atomic", style="bold yellow")
    story.append(", ")
    story.append("distributed", style="bold yellow")
    story.append(",\n")
    story.append("and ")
    story.append("conflict-free", style="bold yellow")
    story.append(".\n\n")
    story.append("Generating ", style="dim")
    story.append(f"{count}", style="bold green")
    story.append(" page-view events across ", style="dim")
    story.append(f"{num_pages}", style="bold green")
    story.append(" endpoints. 📊", style="dim")

    console.print()
    console.print(
        Panel(
            story,
            title="[bold magenta]📊 MISSION BRIEFING — DIMENSION-7 // THE PULSE ENGINE[/]",
            border_style="magenta",
            padding=(1, 2),
        )
    )
    console.print()


async def _seed(count: int, num_pages: int) -> None:
    """Connect to ScyllaDB, sync tables, and generate page-view increments."""
    _print_briefing(count, num_pages)

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "analytics")

    console.print("[dim]📡 Establishing connection to ScyllaDB node...[/]")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    console.print("[dim]🔧 Synchronizing counter tables...[/]")
    await PageViewCounter.sync_table()
    console.print("[dim green]✓ Database ready.[/]")
    console.print()

    pages = random.sample(PAGES, min(num_pages, len(PAGES)))
    stats: dict[str, dict[str, int]] = {}

    for i in track(
        range(count),
        description="[magenta]📊 PULSE  Generating page-view traffic... [/]",
        console=console,
    ):
        url = random.choice(pages)
        date = random.choice(DATES)

        counter = PageViewCounter(url=url, date=date)
        views = random.randint(1, 5)
        visitors = random.randint(0, 1)
        await counter.increment(view_count=views, unique_visitors=visitors)

        key = f"{url}|{date}"
        if key not in stats:
            stats[key] = {"views": 0, "visitors": 0}
        stats[key]["views"] += views
        stats[key]["visitors"] += visitors

    # --- Summary table ---
    console.print()
    table = Table(
        title="[bold]📊 PULSE — Traffic Generation Summary[/]",
        border_style="magenta",
        title_style="bold magenta",
    )
    table.add_column("URL", style="cyan", max_width=40)
    table.add_column("Date", style="dim")
    table.add_column("Views", justify="right", style="green")
    table.add_column("Visitors", justify="right", style="yellow")

    for key in sorted(stats.keys())[:15]:
        url, date = key.split("|")
        table.add_row(url, date, str(stats[key]["views"]), str(stats[key]["visitors"]))
    if len(stats) > 15:
        table.add_row("...", "...", "...", "...")

    console.print(table)
    console.print()

    total_views = sum(s["views"] for s in stats.values())
    total_visitors = sum(s["visitors"] for s in stats.values())
    console.print(
        f"[bold magenta]📊 {count} increments applied — {total_views} views, {total_visitors} visitors across {len(stats)} URL/date combos.[/]"
    )
    console.print("[dim]   Launch the app with: uv run uvicorn main:app --reload[/]")
    console.print()


@click.command()
@click.option("--count", default=200, help="Number of page-view events to generate")
@click.option("--pages", "num_pages", default=10, help="Number of distinct pages to spread traffic across")
def seed(count: int, num_pages: int) -> None:
    """Generate synthetic page-view traffic for the analytics dashboard."""
    asyncio.run(_seed(count, num_pages))


if __name__ == "__main__":
    seed()
