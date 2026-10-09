"""Seed the catalog with products and reviews after migrations are applied.

Usage:
    python seed.py              # 50 products (default)
    python seed.py --count 200  # 200 products
"""

from __future__ import annotations

import asyncio
import os
import random
from uuid import UUID, uuid4

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

MANUFACTURERS = [
    "Temporal Industries",
    "Rift Corp",
    "Nexus Labs",
    "Void Works",
    "Dimension-7 Supply",
    "MerchBot Prime",
    "Quantum Foundry",
    "Starlight Mfg",
    "Echo Dynamics",
    "Cascade Systems",
]

CATEGORIES = [
    "gadgets",
    "navigation",
    "containment",
    "temporal",
    "energy",
    "stealth",
    "computing",
    "biotech",
    "psionic",
    "weapons",
]

TAG_POOL = [
    "clearance",
    "new-arrival",
    "top-rated",
    "limited-edition",
    "prototype",
    "banned-in-dim-3",
    "MerchBot-certified",
    "hazardous",
    "sentient",
]

PRODUCT_NAMES = [
    "Quantum Entanglement Mouse",
    "Gravity Inversion Boots",
    "Chrono-Displacement Watch",
    "Neural Interface Headband",
    "Dimensional Rift Compass",
    "Void-Walker Cloak",
    "Singularity Containment Flask",
    "Phase-Shift Keyboard",
    "Holographic Memory Crystal",
    "Dark Energy Lantern",
    "Probability Manipulation Dice",
    "Psychic Amplification Ring",
    "Nano-Swarm Defense Matrix",
    "Reality Anchor Pendant",
    "Sentient Navigation Orb",
    "Plasma Forge Gauntlets",
    "Molecular Disassembler Pen",
    "Zero-Point Energy Cell",
    "Chaos Theory Calculator",
    "Shadow Frequency Tuner",
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
]

REVIEW_SNIPPETS = [
    "Performed as expected during field deployment — solid build quality.",
    "WARNING: Reality distortion field expanding. Recommend upgrade.",
    "Artifact stable under standard containment. No dimensional leakage.",
    "Anomalous energy signature detected. Cross-reference with SCYLLA-9.",
    "Confirmed sentient. Responds to verbal commands.",
    "Safe for transport when wrapped in void-silk.",
    "Temporal echo detected — may exist in two timelines simultaneously.",
    "No anomalies detected. Recommend downgrade from Class-5.",
    "CRITICAL: Containment breach at 0347 UTC.",
    "Excellent value for interdimensional missions.",
]


def _generate_product(*, featured: bool = False) -> Product:
    """Generate a single story-themed product."""
    return Product(
        id=uuid4(),
        name=random.choice(PRODUCT_NAMES) if random.random() < 0.7 else fake.catch_phrase() + " Device",
        manufacturer=random.choice(MANUFACTURERS),
        category=random.choice(CATEGORIES),
        price=round(random.uniform(49.99, 9999.99), 2),
        description=fake.sentence(nb_words=12),
        tags=random.sample(TAG_POOL, k=random.randint(1, 3)),
        featured=featured,
    )


def _generate_review(product_id: UUID) -> Review:
    """Generate a single review for a product."""
    return Review(
        product_id=product_id,
        author=random.choice(AGENT_CALLSIGNS),
        rating=random.randint(1, 5),
        content=random.choice(REVIEW_SNIPPETS),
    )


def _print_briefing() -> None:
    """Print the mission briefing story panel."""
    story = Text()
    story.append("SCHEMA MIGRATION FRAMEWORK DEMO\n\n", style="bold cyan")
    story.append("The coodie migration runner manages schema evolution\n")
    story.append("through versioned migration files.  Each migration is\n")
    story.append("tracked in the ")
    story.append("_coodie_migrations", style="bold")
    story.append(" table with checksums.\n\n")
    story.append("⚡ Seeding the migrated schema with sample data...", style="dim italic")

    console.print()
    console.print(
        Panel(
            story,
            title="[bold cyan]⚡ SCHEMA MIGRATIONS — CATALOG SEED[/]",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    console.print()


async def _seed(count: int) -> None:
    """Connect to ScyllaDB and insert sample products + reviews."""
    _print_briefing()

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "migrations_demo")

    console.print("[dim]📡 Connecting to ScyllaDB...[/]")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    console.print("[dim green]✓ Connected.[/]")
    console.print()

    # --- Generate products (20% featured) ---
    products = []
    for i in range(count):
        featured = i < max(1, count // 5)
        products.append(_generate_product(featured=featured))

    # --- Insert products ---
    for product in track(
        products,
        description="[cyan]⚡ Inserting products...[/]",
        console=console,
    ):
        await product.save()

    # --- Generate & insert reviews ---
    reviews_count = 0
    for product in track(
        products,
        description="[magenta]📡 Adding reviews...[/]",
        console=console,
    ):
        for _ in range(random.randint(0, 5)):
            review = _generate_review(product.id)
            await review.save()
            reviews_count += 1

    # --- Summary table ---
    console.print()
    table = Table(
        title="[bold]⚡ CATALOG — Seed Summary[/]",
        border_style="cyan",
        title_style="bold cyan",
    )
    table.add_column("Metric", style="bold")
    table.add_column("Count", justify="right", style="green")
    table.add_row("Products", str(len(products)))
    table.add_row("  Featured", str(sum(1 for p in products if p.featured)))
    table.add_row("Reviews", str(reviews_count))
    console.print(table)
    console.print()
    console.print("[bold cyan]✓ Seed complete. Run the app with: uv run uvicorn main:app --reload[/]")
    console.print()


@click.command()
@click.option("--count", default=50, help="Number of products to generate")
def seed(count: int) -> None:
    """Seed the catalog with products and reviews."""
    asyncio.run(_seed(count))


if __name__ == "__main__":
    seed()
