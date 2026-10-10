"""Seed the Shapeshifter's Archive with polymorphic content.

Usage:
    python seed.py              # 30 mixed content items (default)
    python seed.py --count 100  # 100 items
"""

from __future__ import annotations

import asyncio
import os
import random

import click
from faker import Faker
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.text import Text

from coodie.aio import init_coodie

from models import Article, Content, Podcast, Video

fake = Faker()
console = Console()

# --- Type-specific colour mapping (coral / violet / teal) ---
TYPE_STYLES = {
    "article": {"color": "#f97316", "icon": "📰", "label": "Article"},
    "video": {"color": "#8b5cf6", "icon": "🎬", "label": "Video"},
    "podcast": {"color": "#14b8a6", "icon": "🎙️", "label": "Podcast"},
}

# --- Story-themed data pools ---

ARTICLE_TITLES = [
    "The Quantum Semantics of Distributed Consensus",
    "Why Your ORM Is Secretly a Shapeshifter",
    "10 Things SCYLLA-9 Doesn't Want You to Know",
    "A Field Guide to Interdimensional Content",
    "The Art of Single-Table Inheritance",
    "Polymorphism in the Age of Sentient Databases",
    "Morph-IX Manifesto: All Content Is One",
    "From Blog Post to Black Hole: A Content Journey",
    "Dimensional Collapse and Schema Design",
    "The Discriminator Diaries: Volume XVII",
    "How I Stopped Worrying and Loved the Partition Key",
    "Eventual Consistency: A Love Story",
    "The Topology of Mutable Content Forms",
    "Interdimensional Journalism and the Single Table",
    "Morph-IX's Guide to Content Alchemy",
]

VIDEO_TITLES = [
    "SCYLLA-9 Origins: The nodetool Incident",
    "Shapeshifting Tutorial: Your First Discriminator",
    "Live: Morph-IX Transforms a Podcast Into a Paper",
    "Dimension-11 Travel Vlog (DO NOT WATCH ALONE)",
    "How to Contain Polymorphic Content (Official Guide)",
    "The Making of the Shapeshifter's Archive",
    "Coodie Corps Training: Discriminator Basics",
    "Time-lapse: Article Evolving Into a Video",
    "Morph-IX Unboxing: New Content Forms",
    "WARNING: This Video Was Originally a Meme",
    "ScyllaDB Masterclass: Single-Table Inheritance",
    "Behind the Scenes: The Content Singularity",
]

PODCAST_TITLES = [
    "Ep. 1: The Day Content Became Sentient",
    "Ep. 2: Interview with a Discriminator Column",
    "Ep. 3: Morph-IX Therapy Session (LEAKED)",
    "Ep. 4: Is Your Blog Post Actually a Podcast?",
    "Ep. 5: The Sound of Schema Migration",
    "Ep. 6: Dimensional Rift ASMR",
    "Ep. 7: Debate: Tabs vs Spaces vs Content Types",
    "Ep. 8: The Partition Key Whisperer",
    "Ep. 9: Morph-IX Book Club — 'Being and Nothingness'",
    "Ep. 10: Live Q&A from the Content Singularity",
    "Ep. 11: Why Morph-IX Refuses to Pick a Type",
    "Ep. 12: Season Finale — The Archive Speaks",
]

AUTHORS = [
    "Morph-IX",
    "Agent Cipher",
    "Agent Flux",
    "The Middleware",
    "Captain Jinja",
    "Commander Knit",
    "Dr. Schema",
    "Professor Partition",
    "The Discriminator",
    "Archivist Zero",
]

SUMMARIES = [
    "Content that defies classification. Morph-IX approves.",
    "This piece morphed three times during peer review.",
    "Originally a haiku. Now it's a technical whitepaper.",
    "WARNING: may spontaneously change form when unobserved.",
    "Recovered from the Content Singularity. Handle with care.",
    "Morph-IX claims this is their magnum opus. Again.",
    "Peer-reviewed by sentient database fragments.",
    "Contains trace amounts of interdimensional metadata.",
    "Classified Level-7. Do not read aloud near polymorphic entities.",
    "The last person who edited this became a podcast episode.",
    "Approved for distribution across all 11 dimensions.",
    "Morph-IX insists this content 'transcends type.'",
]

RESOLUTIONS = ["480p", "720p", "1080p", "1440p", "4K"]


def _generate_article() -> Article:
    return Article(
        title=random.choice(ARTICLE_TITLES),
        author=random.choice(AUTHORS),
        summary=random.choice(SUMMARIES),
        published=random.random() < 0.7,
        body=fake.text(max_nb_chars=500),
        word_count=random.randint(200, 5000),
    )


def _generate_video() -> Video:
    return Video(
        title=random.choice(VIDEO_TITLES),
        author=random.choice(AUTHORS),
        summary=random.choice(SUMMARIES),
        published=random.random() < 0.7,
        video_url=f"https://dim-11.stream/v/{fake.uuid4()[:8]}",
        duration_seconds=random.randint(30, 7200),
        resolution=random.choice(RESOLUTIONS),
    )


def _generate_podcast() -> Podcast:
    ep = random.randint(1, 50)
    return Podcast(
        title=random.choice(PODCAST_TITLES),
        author=random.choice(AUTHORS),
        summary=random.choice(SUMMARIES),
        published=random.random() < 0.7,
        audio_url=f"https://morph-ix.audio/ep/{ep:03d}",
        duration_seconds=random.randint(300, 5400),
        episode_number=ep,
    )


GENERATORS = [_generate_article, _generate_video, _generate_podcast]


def _print_briefing() -> None:
    """Print the Morph-IX mission briefing."""
    story = Text()
    story.append("DIMENSION-11", style="bold #f97316")
    story.append(" — SCYLLA-9's fragment became ")
    story.append("Morph-IX", style="bold #8b5cf6")
    story.append(",\n")
    story.append("an AI that can take the form of any content type. It publishes\n")
    story.append("articles that turn into videos mid-sentence, podcasts that become\n")
    story.append("blog posts when you pause them, and memes that evolve into\n")
    story.append("peer-reviewed papers.\n\n")
    story.append("All content is stored in a ")
    story.append("single table", style="bold #14b8a6")
    story.append(" with a ")
    story.append("discriminator column", style="bold #14b8a6")
    story.append(" —\nbecause Morph-IX believes ")
    story.append("all content is one", style="italic")
    story.append(".\n\n")
    story.append("The ")
    story.append("Coodie Corps", style="bold #f97316")
    story.append(" must classify and contain each form before\n")
    story.append("the entire archive collapses into a singularity of\n")
    story.append("undifferentiated content.\n\n")
    story.append("🎭 Initiating polymorphic content scan...", style="dim italic")

    console.print()
    console.print(
        Panel(
            story,
            title="[bold #8b5cf6]🎭 MISSION BRIEFING — DIMENSION-11 // THE SHAPESHIFTER'S ARCHIVE[/]",
            border_style="#8b5cf6",
            padding=(1, 2),
        )
    )
    console.print()


async def _seed(count: int) -> None:
    """Connect to ScyllaDB, sync table, and insert polymorphic content."""
    _print_briefing()

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "cms")

    console.print("[dim]📡 Establishing connection to ScyllaDB node...[/]")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    console.print("[dim]🔧 Synchronizing content table (single-table for all types)...[/]")
    await Content.sync_table()
    await Article.sync_table()
    await Video.sync_table()
    await Podcast.sync_table()
    console.print("[dim green]✓ Database ready.[/]")
    console.print()

    # --- Generate content items ---
    items: list[Content] = []
    for _ in range(count):
        gen = random.choice(GENERATORS)
        items.append(gen())

    # --- Insert with type-coloured progress ---
    counts: dict[str, int] = {"article": 0, "video": 0, "podcast": 0}

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold #8b5cf6]🎭 MORPH-IX[/]"),
        BarColumn(bar_width=40, complete_style="#8b5cf6", finished_style="#14b8a6"),
        MofNCompleteColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Generating content...", total=count)
        for item in items:
            await item.save()
            disc = item.content_type
            if not disc:
                disc = type(item).__name__.lower()
            counts[disc] = counts.get(disc, 0) + 1
            style = TYPE_STYLES.get(disc, TYPE_STYLES["article"])
            progress.update(
                task,
                advance=1,
                description=f'[{style["color"]}]{style["icon"]} {style["label"]}[/] "{item.title[:40]}"',
            )

    # --- Summary table ---
    console.print()
    table = Table(
        title="[bold #8b5cf6]🎭 SHAPESHIFTER'S ARCHIVE — Content Manifest[/]",
        border_style="#8b5cf6",
        title_style="bold #8b5cf6",
    )
    table.add_column("Content Type", style="bold")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Discriminator", style="dim")
    table.add_row(
        "[#f97316]📰 Articles[/]",
        str(counts.get("article", 0)),
        "content_type = 'article'",
    )
    table.add_row(
        "[#8b5cf6]🎬 Videos[/]",
        str(counts.get("video", 0)),
        "content_type = 'video'",
    )
    table.add_row(
        "[#14b8a6]🎙️ Podcasts[/]",
        str(counts.get("podcast", 0)),
        "content_type = 'podcast'",
    )
    table.add_row(
        "[bold]Total[/]",
        f"[bold]{sum(counts.values())}[/]",
        "(single table!)",
    )
    console.print(table)
    console.print()
    console.print("[bold #8b5cf6]🎭 The Shapeshifter's Archive has been sealed. All content forms are classified.[/]")
    console.print("[dim]   Launch the app with: uv run uvicorn main:app --reload[/]")
    console.print()


@click.command()
@click.option("--count", default=30, help="Number of content items to generate")
def seed(count: int) -> None:
    """Seed the Shapeshifter's Archive with polymorphic content."""
    asyncio.run(_seed(count))


if __name__ == "__main__":
    seed()
