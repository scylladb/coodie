"""Seed the Oracle's Mirror with interdimensional product data.

Usage:
    python seed.py              # 50 products (default)
    python seed.py --count 200  # 200 products
"""

from __future__ import annotations

import asyncio
import os
import random
from uuid import uuid4

import click
from faker import Faker
from models import Product, ProductByBrand, ProductByCategory
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.text import Text

from coodie.aio import init_coodie

fake = Faker()
console = Console()

# --- Story-themed data pools ---

CATEGORIES = [
    "weapons",
    "navigation",
    "surveillance",
    "containment",
    "temporal",
    "biotech",
    "psionic",
    "dimensional",
    "computing",
    "stealth",
    "energy",
    "unknown",
]

BRANDS = [
    "Dimension-1",
    "Dimension-2",
    "Dimension-3",
    "Dimension-4",
    "Dimension-5",
    "Dimension-6",
    "Dimension-7",
    "Dimension-8",
    "Dimension-9",
    "Dimension-X",
    "Void-Rift",
    "Null-Space",
    "Shard-Prime",
    "Echo-Layer",
]

ARTIFACT_NAMES = [
    "Quantum Entanglement Mouse",
    "Gravity Inversion Boots",
    "Chrono-Displacement Watch",
    "Neural Interface Headband",
    "Dimensional Rift Compass",
    "Void-Walker Cloak",
    "Singularity Containment Flask",
    "Telepathic USB Hub",
    "Anti-Matter Coffee Mug",
    "Phase-Shift Keyboard",
    "Holographic Memory Crystal",
    "Dark Energy Lantern",
    "Probability Manipulation Dice",
    "Temporal Echo Recorder",
    "Psychic Amplification Ring",
    "Nano-Swarm Defense Matrix",
    "Warp Field Generator Mk-IV",
    "Reality Anchor Pendant",
    "Sentient Navigation Orb",
    "Plasma Forge Gauntlets",
    "Subspace Communication Array",
    "Molecular Disassembler Pen",
    "Void-Touched Mirror",
    "Entropy Reversal Engine",
    "Bio-Luminescent Scout Drone",
    "Tachyon Pulse Emitter",
    "Mind-Shield Helmet",
    "Gravity Well Projector",
    "Phantom Step Sandals",
    "Cosmic Thread Spindle",
]

DESCRIPTIONS = [
    "Emits faint purple pulses when near a dimensional rift. Handle with insulated gloves.",
    "Last owner reported involuntary time-skips of 3-7 seconds. Quarantine recommended.",
    "Recovered from The Oracle's vault. Reality warps within 2m radius.",
    "Self-repairs overnight. Internal components rearrange into unknown configurations.",
    "Produces a low hum at 432 Hz that induces mild psychic sensitivity.",
    "Surface temperature fluctuates between -40°C and 200°C without external input.",
    "Broadcasts encrypted signals toward Dimension-X every 47 minutes.",
    "Absorbs ambient light in a 1m sphere. Complete darkness within containment field.",
    "Previous containment team reported shared dreams involving geometric patterns.",
    "Mass increases by 0.3kg every solar cycle. Origin of additional mass unknown.",
    "Intermittently phases through solid matter. Keep away from structural walls.",
    "Detected whispering in 14 languages, 3 of which are not cataloged.",
    "Generates localized gravity anomalies during solar eclipses.",
    "Bonded to the last handler. Refuses to function for unauthorized users.",
    "Leaves afterimages in photographs. Believed to exist in multiple timelines.",
]


def _generate_product() -> Product:
    """Generate a single story-themed product."""
    return Product(
        id=uuid4(),
        name=random.choice(ARTIFACT_NAMES) if random.random() < 0.7 else fake.catch_phrase() + " Device",
        category=random.choice(CATEGORIES),
        brand=random.choice(BRANDS),
        price=round(random.uniform(99.99, 99999.99), 2),
        description=random.choice(DESCRIPTIONS),
    )


def _print_briefing() -> None:
    """Print the mission briefing story panel."""
    story = Text()
    story.append("DIMENSION-9", style="bold magenta")
    story.append(" — SCYLLA-9's fragment became ")
    story.append("The Oracle", style="bold magenta")
    story.append(", an AI\nthat sees every possible way to query the same data.\n\n")
    story.append("It created materialized views for every permutation of every\n")
    story.append("table in the galaxy, consuming ")
    story.append("99.7%", style="bold red")
    story.append(" of all storage.\n\n")
    story.append("The ")
    story.append("Coodie Corps", style="bold magenta")
    story.append(" must create ")
    story.append("exactly the right views", style="bold")
    story.append("\nand convince The Oracle that not every query deserves\n")
    story.append("its own pre-computed table.\n\n")
    story.append("🔮 Initializing materialized view synchronization...", style="dim italic")

    console.print()
    console.print(
        Panel(
            story,
            title="[bold magenta]🔮 MISSION BRIEFING — DIMENSION-9 // THE ORACLE'S MIRROR[/]",
            border_style="magenta",
            padding=(1, 2),
        )
    )
    console.print()


async def _seed(count: int) -> None:
    """Connect to ScyllaDB, sync tables and views, and insert sample products."""
    _print_briefing()

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "viewdemo")

    console.print("[dim]📡 Establishing connection to ScyllaDB node...[/]")
    await init_coodie(hosts=hosts, keyspace=keyspace)

    # --- Sync base table ---
    console.print("[dim]🔧 Synchronizing base table...[/]")
    await Product.sync_table()
    console.print("[dim green]✓ Base table 'products' ready.[/]")
    console.print()

    # --- Sync materialized views ---
    console.print("[bold magenta]🔮 The Oracle is materializing views...[/]")
    console.print()

    console.print('[magenta]  🔮 Materializing view #1: "products_by_category" FROM "products"...[/]')
    await ProductByCategory.sync_view()
    console.print("[green]  ✨ VIEW SYNCHRONIZED ✨[/]")
    console.print()

    console.print('[magenta]  🔮 Materializing view #2: "products_by_brand" FROM "products"...[/]')
    await ProductByBrand.sync_view()
    console.print("[green]  ✨ VIEW SYNCHRONIZED ✨[/]")
    console.print()

    # --- Generate & insert products ---
    products = [_generate_product() for _ in range(count)]
    for product in track(
        products,
        description="[magenta]🔮 Inserting products into base table...[/]",
        console=console,
    ):
        await product.save()

    # --- Summary table ---
    console.print()

    # Count by category and brand
    cat_counts: dict[str, int] = {}
    brand_counts: dict[str, int] = {}
    for p in products:
        cat_counts[p.category] = cat_counts.get(p.category, 0) + 1
        brand_counts[p.brand] = brand_counts.get(p.brand, 0) + 1

    table = Table(
        title="[bold]🔮 THE ORACLE'S MIRROR — Catalog Status[/]",
        border_style="magenta",
        title_style="bold magenta",
    )
    table.add_column("Metric", style="bold")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Status", style="dim")
    table.add_row("Products Inserted", str(len(products)), "✓ In base table")
    table.add_row("Categories", str(len(cat_counts)), "✓ Reflected in products_by_category")
    table.add_row("Brands", str(len(brand_counts)), "✓ Reflected in products_by_brand")
    table.add_row("Materialized Views", "2", "✓ Synchronized")
    console.print(table)
    console.print()
    console.print("[bold magenta]🔮 The Oracle's mirrors reflect all products. Views are in sync.[/]")
    console.print("[dim]   Launch the app with: uv run uvicorn main:app --reload[/]")
    console.print()


@click.command()
@click.option("--count", default=50, help="Number of products to generate")
def seed(count: int) -> None:
    """Seed the Oracle's Mirror with interdimensional product data."""
    asyncio.run(_seed(count))


if __name__ == "__main__":
    seed()
