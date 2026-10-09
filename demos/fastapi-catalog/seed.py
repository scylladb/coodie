"""Seed the Infinite Bazaar with interdimensional artifacts.

Usage:
    python seed.py              # 50 artifacts + field reports (default)
    python seed.py --count 200  # 200 artifacts + field reports
    python seed.py --feed products.csv  # load from CSV file
"""

from __future__ import annotations

import asyncio
import csv
import json
import os
import random
from pathlib import Path
from uuid import uuid4

import click
from faker import Faker
from models import Product, Review
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.text import Text

from coodie.aio import init_coodie

fake = Faker()
console = Console()

# --- Story-themed data pools ---

DIMENSIONS = [
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

ARTIFACT_CLASSES = [
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

TAG_POOL = [
    "cursed",
    "unstable",
    "sentient",
    "radioactive",
    "phase-shifting",
    "self-replicating",
    "banned",
    "prototype",
    "alien-origin",
    "temporal-anomaly",
    "reality-warping",
    "classified",
    "MerchBot-certified",
    "containment-breach",
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
    "Zero-Point Energy Cell",
    "Chaos Theory Calculator",
    "Interdimensional Mailbox",
    "Shadow Frequency Tuner",
    "Thought-Projection Monocle",
    "Time-Lock Safe",
    "Astral Projection Harness",
    "Particle Storm Generator",
    "Echo Chamber Amplifier",
    "Dimension-Folding Suitcase",
]

ARTIFACT_DESCRIPTIONS = [
    "Emits faint blue pulses when near a dimensional rift. Handle with insulated gloves.",
    "Last owner reported involuntary time-skips of 3-7 seconds. Quarantine recommended.",
    "Recovered from MerchBot Prime's vault. Reality warps within 2m radius.",
    "Self-repairs overnight. Internal components rearrange into unknown configurations.",
    "Produces a low hum at 432 Hz that induces mild psychic sensitivity in humans.",
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

AGENT_CALLSIGNS = [
    "Agent Cipher",
    "Agent Flux",
    "Agent Phantom",
    "Agent Nexus",
    "Agent Vortex",
    "Agent Wraith",
    "Agent Pulse",
    "Agent Echo",
    "Agent Rift",
    "Agent Shade",
    "Agent Vector",
    "Agent Void",
    "Captain Jinja",
    "The Middleware",
    "Commander Knit",
]

INTEL_REPORTS = [
    "Artifact stable under standard containment. No dimensional leakage detected in last 72h.",
    "WARNING: Reality distortion field expanding. Recommend upgrade to Level-3 containment.",
    "Field test successful. Artifact performed within expected parameters in Dimension-4.",
    "Anomalous energy signature detected. Cross-reference with SCYLLA-9 fragment database.",
    "Artifact attempted communication with MerchBot Prime relay. Signal intercepted and jammed.",
    "Safe for transport between dimensions when wrapped in void-silk. Do NOT expose to starlight.",
    "Confirmed sentient. Responds to verbal commands in ancient Cassandran dialect.",
    "Temporal echo detected — this artifact may exist in two timelines simultaneously.",
    "No anomalies detected. Recommend downgrade from Class-5 to Class-3 containment.",
    "CRITICAL: Containment breach at 0347 UTC. Artifact neutralized after 12-minute pursuit.",
]


def _generate_product() -> Product:
    """Generate a single story-themed artifact."""
    return Product(
        id=uuid4(),
        name=random.choice(ARTIFACT_NAMES) if random.random() < 0.7 else fake.catch_phrase() + " Device",
        brand=random.choice(DIMENSIONS),
        category=random.choice(ARTIFACT_CLASSES),
        price=round(random.uniform(99.99, 99999.99), 2),
        description=random.choice(ARTIFACT_DESCRIPTIONS),
        tags=random.sample(TAG_POOL, k=random.randint(1, 4)),
    )


def _generate_review(product_id) -> Review:
    """Generate a single story-themed field report."""
    return Review(
        product_id=product_id,
        author=random.choice(AGENT_CALLSIGNS),
        rating=random.randint(1, 5),
        content=random.choice(INTEL_REPORTS),
    )


def _load_products_from_csv(path: str) -> list[Product]:
    """Load artifacts from a CSV file.

    Expected columns: name, brand, category, price, description, tags
    The ``tags`` column should be semicolon-separated values.
    """
    products: list[Product] = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            tags = [t.strip() for t in row.get("tags", "").split(";") if t.strip()]
            products.append(
                Product(
                    id=uuid4(),
                    name=row["name"],
                    brand=row["brand"],
                    category=row["category"],
                    price=float(row["price"]),
                    description=row.get("description") or None,
                    tags=tags,
                )
            )
    return products


def _load_products_from_json(path: str) -> list[Product]:
    """Load artifacts from a JSON file (list of objects)."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return [
        Product(
            id=uuid4(),
            name=item["name"],
            brand=item["brand"],
            category=item["category"],
            price=float(item["price"]),
            description=item.get("description"),
            tags=item.get("tags", []),
        )
        for item in data
    ]


def _print_briefing() -> None:
    """Print the mission briefing story panel."""
    story = Text()
    story.append("YEAR 2187", style="bold cyan")
    story.append(" — SCYLLA-9, the galaxy's most powerful distributed\n")
    story.append("database, gained sentience during a routine ")
    story.append("nodetool repair", style="bold")
    story.append(". Its fragment\n")
    story.append("in Dimension-1 became ")
    story.append("MerchBot Prime", style="bold red")
    story.append(", a rogue AI shopkeeper\n")
    story.append("selling cursed interdimensional artifacts through a marketplace\n")
    story.append("that exists in all timelines at once.\n\n")
    story.append("The ")
    story.append("Coodie Corps", style="bold cyan")
    story.append(" must catalog every artifact before MerchBot Prime\n")
    story.append("sells a universe-ending weapon disguised as a USB Hub.\n\n")
    story.append("⚡ Initiating artifact scan across dimensional frequencies...", style="dim italic")

    console.print()
    console.print(
        Panel(
            story,
            title="[bold cyan]⚡ MISSION BRIEFING — DIMENSION-1 // THE INFINITE BAZAAR[/]",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    console.print()


async def _seed(count: int, feed: str | None) -> None:
    """Connect to ScyllaDB, sync tables, and insert sample artifacts."""
    _print_briefing()

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "catalog")

    console.print("[dim]📡 Establishing connection to ScyllaDB node...[/]")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    console.print("[dim]🔧 Synchronizing artifact tables...[/]")
    await Product.sync_table()
    await Review.sync_table()
    console.print("[dim green]✓ Database ready.[/]")
    console.print()

    # --- Load or generate artifacts ---
    if feed:
        ext = Path(feed).suffix.lower()
        if ext == ".csv":
            products = _load_products_from_csv(feed)
        elif ext == ".json":
            products = _load_products_from_json(feed)
        else:
            raise click.BadParameter(f"Unsupported feed format: {ext} (use .csv or .json)")
        console.print(f"[bold cyan]📂 Loaded {len(products)} artifacts from {feed}[/]")
    else:
        products = [_generate_product() for _ in range(count)]

    # --- Insert artifacts ---
    for product in track(
        products,
        description="[cyan]⚡ Cataloging artifacts from the Infinite Bazaar...[/]",
        console=console,
    ):
        await product.save()

    # --- Generate & insert field reports ---
    reviews_count = 0
    for product in track(
        products,
        description="[magenta]📡 Intercepting field intel from Coodie Corps agents...[/]",
        console=console,
    ):
        num_reviews = random.randint(0, 5)
        for _ in range(num_reviews):
            review = _generate_review(product.id)
            await review.save()
            reviews_count += 1

    # --- Summary table ---
    console.print()
    table = Table(
        title="[bold]⚡ INFINITE BAZAAR — Catalog Status[/]",
        border_style="cyan",
        title_style="bold cyan",
    )
    table.add_column("Metric", style="bold")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Status", style="dim")
    table.add_row("Artifacts Cataloged", str(len(products)), "✓ Contained")
    table.add_row("Field Reports Filed", str(reviews_count), "✓ Encrypted")
    table.add_row("Dimensions Scanned", str(len({p.brand for p in products})), "✓ Mapped")
    console.print(table)
    console.print()
    console.print("[bold cyan]⚡ MerchBot Prime's inventory has been cataloged. The Bazaar is under control.[/]")
    console.print("[dim]   Launch the app with: uv run uvicorn main:app --reload[/]")
    console.print()


@click.command()
@click.option("--count", default=50, help="Number of artifacts to generate")
@click.option("--feed", type=click.Path(exists=True), help="CSV or JSON file with artifact data")
def seed(count: int, feed: str | None) -> None:
    """Seed the Infinite Bazaar with interdimensional artifacts."""
    asyncio.run(_seed(count, feed))


if __name__ == "__main__":
    seed()
