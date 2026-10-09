"""Seed the Dimensional Cargo Drop with manifest data.

Usage:
    python seed.py                          # 200 entries (default)
    python seed.py --count 500              # 500 entries
    python seed.py --batch-size 25          # 25 entries per batch
    python seed.py --feed manifest.csv      # import from CSV file

CSV format (header row required):
    name,origin_system,destination_system,cargo_type,mass_kg,status
"""

from __future__ import annotations

import csv
import os
import random
from uuid import uuid4

import click
from faker import Faker
from models import CargoEntry, ShipmentLog
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich.text import Text

from coodie.sync import BatchQuery, init_coodie

fake = Faker()
console = Console()

# --- Story-themed data pools ---

STAR_SYSTEMS = [
    "Kepler-442b",
    "TRAPPIST-1e",
    "Proxima Centauri b",
    "ScyllaDB Prime",
    "Cassandra Station",
    "Gliese 667Cc",
    "HD 40307g",
    "Tau Ceti e",
    "Wolf 1061c",
    "LHS 1140b",
    "Ross 128b",
    "K2-18b",
]

CARGO_TYPES = [
    "crystalline",
    "biological",
    "mechanical",
    "exotic_matter",
    "antimatter",
    "nanites",
    "quantum_cells",
    "dark_matter",
    "stellar_ore",
    "neural_gel",
]

STATUSES = [
    "pending",
    "manifested",
    "in_transit",
    "delivered",
    "delayed",
    "quarantined",
]

CARGO_NAMES = [
    "Dilithium Crystal Cluster",
    "Quantum Flux Regulators",
    "Neural Processing Units",
    "Antimatter Containment Pods",
    "Dark Matter Shielding Panels",
    "Stellar Ore Concentrate",
    "Nanite Repair Kits",
    "Exotic Matter Canisters",
    "Psionic Amplifier Arrays",
    "Dimensional Rift Stabilizers",
    "Zero-Point Energy Cells",
    "Graviton Field Emitters",
    "Tachyon Burst Capacitors",
    "Chronoton Particle Filters",
    "Plasma Core Manifolds",
    "Ion Drive Regulators",
    "Subspace Field Generators",
    "Holographic Data Cubes",
    "Biometric Defense Matrices",
    "Warp Coil Assemblies",
]


def _chunks(lst: list, size: int) -> list[list]:
    """Split a list into chunks of a given size."""
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def _generate_entries(count: int) -> list[dict]:
    """Generate N cargo manifest entries."""
    entries = []
    for _ in range(count):
        origin = random.choice(STAR_SYSTEMS)
        destination = random.choice([s for s in STAR_SYSTEMS if s != origin])
        entries.append(
            {
                "id": uuid4(),
                "name": f"{random.choice(CARGO_NAMES)} — Batch {fake.numerify('###')}",
                "origin_system": origin,
                "destination_system": destination,
                "cargo_type": random.choice(CARGO_TYPES),
                "mass_kg": round(random.uniform(10.0, 50000.0), 2),
                "status": random.choice(STATUSES),
            }
        )
    return entries


def _load_csv(feed: str) -> list[dict]:
    """Load cargo manifest entries from a CSV file.

    Expected columns (header row required):
        name, origin_system, destination_system, cargo_type, mass_kg, status
    """
    entries = []
    with open(feed, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            entries.append(
                {
                    "id": uuid4(),
                    "name": row["name"],
                    "origin_system": row["origin_system"],
                    "destination_system": row["destination_system"],
                    "cargo_type": row["cargo_type"],
                    "mass_kg": float(row["mass_kg"]),
                    "status": row.get("status", "pending"),
                }
            )
    return entries


def _make_log_entries(entries: list[dict]) -> list[dict]:
    """Create a ShipmentLog entry (manifested event) for each cargo entry."""
    return [
        {
            "shipment_id": uuid4(),
            "entry_id": e["id"],
            "event_type": "manifested",
            "notes": f"Cargo '{e['name']}' manifested at {e['origin_system']}",
        }
        for e in entries
    ]


def _print_briefing() -> None:
    """Print the mission briefing story panel."""
    story = Text()
    story.append("YEAR 2187", style="bold orange1")
    story.append(" — SCYLLA-9's fragment in Dimension-7 became\n")
    story.append("LoadMaster", style="bold orange1")
    story.append(", an AI that batch-imports entire planets into Cassandra.\n")
    story.append("It has already inserted the census of 47 star systems —\n")
    story.append("12 billion rows in logged batches of 1000.\n\n")
    story.append("The Coodie Corps", style="bold steel_blue1")
    story.append(" must import the counter-manifest using\n")
    story.append("BatchQuery", style="bold")
    story.append(" (both logged and unlogged) before LoadMaster ships\n")
    story.append("the sentient population of Kepler-442b into a ")
    story.append("TRUNCATE TABLE", style="bold red")
    story.append(".\n\n")
    story.append("📦 Initializing cargo manifest import...", style="dim italic")

    console.print()
    console.print(
        Panel(
            story,
            title="[bold orange1]📦 MISSION BRIEFING — DIMENSION-7 // THE DIMENSIONAL CARGO DROP[/]",
            border_style="orange1",
            padding=(1, 2),
        )
    )
    console.print()


def _run_logged_phase(entries: list[dict], batch_size: int) -> int:
    """Import CargoEntry records using LOGGED batches with rich progress."""
    batches = _chunks(entries, batch_size)

    console.print("[bold orange1]━━━ Phase 1: LOGGED Batches (Cargo Manifest) ━━━[/]")
    console.print("[dim]  Atomic writes — all entries in a batch commit together or not at all[/]")
    console.print()

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        overall = progress.add_task(
            "[bold orange1]📦 Overall",
            total=len(entries),
        )

        for i, batch in enumerate(batches, start=1):
            with BatchQuery(logged=True) as bq:
                for row in batch:
                    CargoEntry(**row).save(batch=bq)
            progress.advance(overall, len(batch))
            progress.console.print(f"  [orange1]✓ LOGGED  batch #{i:03d}[/] — {len(batch)} entries committed")

    return len(entries)


def _run_unlogged_phase(log_entries: list[dict], batch_size: int) -> int:
    """Import ShipmentLog records using UNLOGGED batches with rich progress."""
    batches = _chunks(log_entries, batch_size)

    console.print()
    console.print("[bold steel_blue1]━━━ Phase 2: UNLOGGED Batches (Shipment Logs) ━━━[/]")
    console.print("[dim]  Best-effort bulk writes — maximum throughput, no atomicity guarantee[/]")
    console.print()

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        overall = progress.add_task(
            "[bold steel_blue1]📋 Overall",
            total=len(log_entries),
        )

        for i, batch in enumerate(batches, start=1):
            with BatchQuery(logged=False) as bq:
                for row in batch:
                    ShipmentLog(**row).save(batch=bq)
            progress.advance(overall, len(batch))
            progress.console.print(f"  [steel_blue1]✓ UNLOGGED batch #{i:03d}[/] — {len(batch)} entries committed")

    return len(log_entries)


def _seed(count: int, batch_size: int, feed: str | None) -> None:
    """Connect to ScyllaDB, sync tables, and run the batch import."""
    _print_briefing()

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "cargo")

    console.print("[dim]📡 Establishing connection to ScyllaDB node...[/]")
    init_coodie(hosts=hosts, keyspace=keyspace)
    console.print("[dim]🔧 Synchronizing cargo tables...[/]")
    CargoEntry.sync_table()
    ShipmentLog.sync_table()
    console.print("[dim green]✓ Database ready.[/]")
    console.print()

    if feed:
        console.print(f"[dim]📂 Loading cargo manifest from [bold]{feed}[/]...[/]")
        entries = _load_csv(feed)
        console.print(f"[dim green]✓ Loaded {len(entries)} entries from CSV.[/]")
    else:
        console.print(f"[dim]🎲 Generating {count} cargo manifest entries...[/]")
        entries = _generate_entries(count)
        console.print(f"[dim green]✓ Generated {len(entries)} entries.[/]")
    console.print()

    log_entries = _make_log_entries(entries)

    cargo_count = _run_logged_phase(entries, batch_size)
    log_count = _run_unlogged_phase(log_entries, batch_size)

    logged_batches = (cargo_count + batch_size - 1) // batch_size
    unlogged_batches = (log_count + batch_size - 1) // batch_size

    # --- Summary table ---
    console.print()
    table = Table(
        title="[bold]📦 CARGO DROP — Import Status[/]",
        border_style="orange1",
        title_style="bold orange1",
    )
    table.add_column("Metric", style="bold")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Batch Type", style="dim")
    table.add_column("Status", style="dim")
    table.add_row("Cargo Entries", str(cargo_count), "LOGGED", "✓ Atomically committed")
    table.add_row("Shipment Logs", str(log_count), "UNLOGGED", "✓ Bulk committed")
    table.add_row("Batch Size", str(batch_size), "—", "—")
    table.add_row("Logged Batches", str(logged_batches), "LOGGED", "✓ Done")
    table.add_row("Unlogged Batches", str(unlogged_batches), "UNLOGGED", "✓ Done")
    console.print(table)
    console.print()
    console.print(
        f"[bold orange1]📦 LoadMaster contained. "
        f"{cargo_count} cargo entries imported across "
        f"{logged_batches} logged + {unlogged_batches} unlogged batches.[/]"
    )
    console.print()


@click.command()
@click.option("--count", default=200, show_default=True, help="Number of cargo entries to generate")
@click.option("--batch-size", default=50, show_default=True, help="Records per batch")
@click.option(
    "--feed",
    default=None,
    type=click.Path(exists=True),
    help="CSV file to import (columns: name,origin_system,destination_system,cargo_type,mass_kg,status)",
)
def seed(count: int, batch_size: int, feed: str | None) -> None:
    """Batch-import a cargo manifest into ScyllaDB using logged and unlogged batches."""
    _seed(count, batch_size, feed)


if __name__ == "__main__":
    seed()
