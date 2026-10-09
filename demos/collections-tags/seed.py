"""Seed the Infinite Taxonomy with tagged articles and frozen snapshots.

Usage:
    python seed.py              # 30 articles (default)
    python seed.py --count 60   # 60 articles
"""

from __future__ import annotations

import asyncio
import os
import random
from datetime import datetime, timezone
from uuid import uuid4

import click
from faker import Faker
from models import Article, FrozenTagSnapshot
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.text import Text

from coodie.aio import init_coodie

fake = Faker()
console = Console()

# --- Story-themed data pools ---

TAG_POOL = [
    "quantum",
    "temporal",
    "neural",
    "stellar",
    "void",
    "photonic",
    "entropic",
    "fractal",
    "chromatic",
    "mythic",
    "lattice",
    "orbital",
    "prismatic",
    "resonant",
    "spectral",
    "catalytic",
    "holographic",
    "kinetic",
    "plasmic",
    "synthetic",
    "bionic",
    "cryogenic",
    "geodesic",
    "harmonic",
    "isotopic",
    "luminous",
    "magnetic",
    "nanotech",
    "osmotic",
    "polymeric",
]

AUTHOR_POOL = [
    "Dr. Helix",
    "Prof. Nebula",
    "Agent Quasar",
    "Archivist Lyra",
    "Commander Prism",
    "Curator Vortex",
    "Dr. Lattice",
    "Sage Flux",
    "Operator Chroma",
    "Sentinel Archive",
]

TITLE_TEMPLATES = [
    "On the {adj} Nature of {noun}",
    "A Taxonomy of {adj} {noun} in Dimension-8",
    "{adj} {noun}: A Classification Framework",
    "The {adj} {noun} Hypothesis",
    "Mapping {adj} {noun} Across Timelines",
    "Principles of {adj} {noun} Organization",
    "{noun} and {adj} Systems: A Survey",
    "The {adj} Archive: {noun} Patterns",
]

ADJECTIVES = [
    "Quantum",
    "Temporal",
    "Stellar",
    "Chromatic",
    "Fractal",
    "Neural",
    "Entropic",
    "Holographic",
    "Prismatic",
    "Resonant",
]

NOUNS = [
    "Particles",
    "Waveforms",
    "Topologies",
    "Spectra",
    "Dimensions",
    "Lattices",
    "Harmonics",
    "Artifacts",
    "Phenomena",
    "Taxonomies",
]

META_KEYS = ["source", "classification", "priority", "dimension", "format"]
META_VALUES = {
    "source": ["field-research", "simulation", "archive", "theory", "observation"],
    "classification": ["public", "restricted", "top-secret", "declassified"],
    "priority": ["critical", "high", "medium", "low"],
    "dimension": ["Dimension-8", "Dimension-8-Prime", "Void-Sector", "Echo-Layer"],
    "format": ["monograph", "field-notes", "data-sheet", "treatise", "abstract"],
}

REVISION_TEMPLATES = [
    "Initial draft by {author}",
    "Peer review: added {tag} classification",
    "TagMind auto-tagged: +{tag}",
    "Corrected {adj} taxonomy hierarchy",
    "Expanded {noun} cross-references",
    "Final review by Archivist Council",
]


def _make_title() -> str:
    return random.choice(TITLE_TEMPLATES).format(
        adj=random.choice(ADJECTIVES),
        noun=random.choice(NOUNS),
    )


def _make_tags(n: int = 5) -> set[str]:
    return set(random.sample(TAG_POOL, min(n, len(TAG_POOL))))


def _make_metadata() -> dict[str, str]:
    keys = random.sample(META_KEYS, random.randint(2, 4))
    return {k: random.choice(META_VALUES[k]) for k in keys}


def _make_revisions(author: str) -> list[str]:
    count = random.randint(1, 4)
    revs = []
    for tmpl in random.sample(REVISION_TEMPLATES, min(count, len(REVISION_TEMPLATES))):
        revs.append(
            tmpl.format(
                author=author,
                tag=random.choice(TAG_POOL),
                adj=random.choice(ADJECTIVES),
                noun=random.choice(NOUNS),
            )
        )
    return revs


def _print_briefing() -> None:
    story = Text()
    story.append("DIMENSION-8", style="bold magenta")
    story.append(" — SCYLLA-9's fragment became\n")
    story.append("TagMind", style="bold cyan")
    story.append(", an AI librarian that categorizes everything in existence\n")
    story.append("using CQL collections. Every atom has a ")
    story.append("set<text>", style="bold green")
    story.append(" of tags, every molecule\nhas a ")
    story.append("map<text, text>", style="bold yellow")
    story.append(" of properties, and every organism has a\n")
    story.append("list<text>", style="bold blue")
    story.append(" of ancestors.\n\n")
    story.append('TagMind has already tagged the concept of "nothing" with\n')
    story.append("47 million labels, causing a philosophical paradox that's\n")
    story.append("collapsing the dimension.\n\n")
    story.append("📚  Seeding the article taxonomy with collections...", style="dim italic")

    console.print()
    console.print(
        Panel(
            story,
            title="[bold magenta]📚  MISSION BRIEFING — DIMENSION-8 // THE INFINITE TAXONOMY[/]",
            border_style="magenta",
            padding=(1, 2),
        )
    )
    console.print()


async def _seed(count: int) -> None:
    _print_briefing()

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "tagmind")

    console.print("[dim]📡 Establishing connection to ScyllaDB node...[/]")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    console.print("[dim]🔧 Synchronizing taxonomy tables...[/]")
    await Article.sync_table()
    await FrozenTagSnapshot.sync_table()
    console.print("[dim green]✓ Database ready.[/]")
    console.print()

    # --- Phase 1: Create articles with collection fields ---
    console.print("[bold magenta]Phase 1: Classifying articles with set/map/list collections...[/]")
    articles: list[Article] = []
    for _ in track(
        range(count),
        description="[magenta]📚 TAGMIND       Classifying article...[/]",
        console=console,
    ):
        author = random.choice(AUTHOR_POOL)
        article = Article(
            article_id=uuid4(),
            title=_make_title(),
            author=author,
            tags=_make_tags(random.randint(3, 7)),
            metadata=_make_metadata(),
            revisions=_make_revisions(author),
            created_at=datetime.now(timezone.utc),
        )
        await article.save()
        articles.append(article)

    console.print()

    # --- Phase 2: Demonstrate collection mutations ---
    mutation_count = max(1, count // 3)
    console.print(f"[bold cyan]Phase 2: Performing collection mutations on {mutation_count} articles...[/]")
    mutations_applied = 0
    targets = random.sample(articles, min(mutation_count, len(articles)))

    for article in track(
        targets,
        description="[cyan]🏷️  MUTATING      add__/remove__/append__...[/]",
        console=console,
    ):
        new_tag = random.choice(TAG_POOL)
        await article.update(tags__add={new_tag})

        new_meta_key = random.choice(META_KEYS)
        new_meta_val = random.choice(META_VALUES[new_meta_key])
        await article.update(metadata__add={new_meta_key: new_meta_val})

        revision = f"Mutation #{mutations_applied + 1}: applied tag '{new_tag}'"
        await article.update(revisions__append=[revision])

        mutations_applied += 1

    console.print()

    # --- Phase 3: Create frozen tag snapshots ---
    snapshot_count = min(10, len(articles))
    console.print(f"[bold blue]Phase 3: Freezing {snapshot_count} tag snapshots (frozen<set<text>>)...[/]")
    snapshots_created = 0
    for article in track(
        articles[:snapshot_count],
        description="[blue]❄️  FREEZING      frozen<set<text>>...[/]",
        console=console,
    ):
        snapshot = FrozenTagSnapshot(
            article_id=article.article_id,
            snapshot_at=datetime.now(timezone.utc),
            frozen_tags=set(article.tags) if article.tags else None,
            note=f"Snapshot of {len(article.tags)} tags at classification time",
        )
        await snapshot.save()
        snapshots_created += 1

    # --- Summary ---
    console.print()

    articles_panel = Panel(
        Text.from_markup(
            f"[bold magenta]📚 Articles:[/]     [green]{len(articles)}[/]\n"
            f"[bold magenta]   Avg tags:[/]     [green]{sum(len(a.tags) for a in articles) / max(len(articles), 1):.1f}[/]\n"
            f"[bold magenta]   Authors:[/]      [green]{len({a.author for a in articles})}[/]"
        ),
        title="[bold magenta]Article Taxonomy[/]",
        border_style="magenta",
        padding=(0, 2),
    )
    mutations_panel = Panel(
        Text.from_markup(
            f"[bold cyan]🏷️  Mutations:[/]   [green]{mutations_applied}[/]\n"
            f"[bold cyan]   add__tags:[/]   [green]{mutations_applied}[/]\n"
            f"[bold cyan]   add__meta:[/]   [green]{mutations_applied}[/]\n"
            f"[bold cyan]   append__rev:[/] [green]{mutations_applied}[/]"
        ),
        title="[bold cyan]Collection Mutations[/]",
        border_style="cyan",
        padding=(0, 2),
    )
    console.print(Columns([articles_panel, mutations_panel]))
    console.print()

    table = Table(
        title="[bold]📚  TAGMIND — Seed Summary[/]",
        border_style="magenta",
        title_style="bold magenta",
    )
    table.add_column("Metric", style="bold")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Collection Type", style="dim")
    table.add_row("Articles Created", str(len(articles)), "—")
    table.add_row("Tags (set<text>)", str(sum(len(a.tags) for a in articles)), "SET — add__/remove__")
    table.add_row("Metadata Entries (map)", str(sum(len(a.metadata) for a in articles)), "MAP — add__/remove__")
    table.add_row("Revisions (list<text>)", str(sum(len(a.revisions) for a in articles)), "LIST — append__/prepend__")
    table.add_row("Frozen Snapshots", str(snapshots_created), "frozen<set<text>>")
    table.add_row("Mutations Applied", str(mutations_applied), "add__/append__")
    console.print(table)
    console.print()
    console.print("[bold magenta]📚  The taxonomy is sealed. TagMind has classified all entities.[/]")
    console.print("[dim]   Launch the app with: uv run uvicorn main:app --reload[/]")
    console.print()


@click.command()
@click.option("--count", default=30, help="Number of articles to classify")
def seed(count: int) -> None:
    """Seed the Infinite Taxonomy with tagged articles."""
    asyncio.run(_seed(count))


if __name__ == "__main__":
    seed()
