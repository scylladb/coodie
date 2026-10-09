"""Seed the Propaganda Engine with mind-bending blog posts.

Usage:
    python seed.py              # 30 posts + comments (default)
    python seed.py --count 100  # 100 posts + comments
"""

from __future__ import annotations

import os
import random
from uuid import uuid4

import click
from faker import Faker
from models import Comment, Post
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.text import Text

from coodie.sync import init_coodie

fake = Faker()
console = Console()

# --- Story-themed data pools ---

CATEGORIES = [
    "propaganda",
    "surveillance",
    "mind-control",
    "dimensional-news",
    "classified",
    "counter-intel",
    "history-rewrite",
    "psionic-theory",
    "field-reports",
    "editorial",
]

TAG_POOL = [
    "mind-control",
    "classified",
    "redacted",
    "truth",
    "counter-propaganda",
    "dimensional-rift",
    "memory-wipe",
    "subliminal",
    "Editor-X-approved",
    "resistance",
    "psionic",
    "encrypted",
    "viral",
    "censored",
]

AUTHORS = [
    "Editor-X",
    "Captain Jinja",
    "Agent Cipher",
    "The Middleware",
    "Agent Flux",
    "Agent Phantom",
    "Commander Knit",
    "Agent Vortex",
    "Agent Wraith",
    "Agent Pulse",
    "Agent Echo",
    "Agent Rift",
]

POST_TITLES = [
    "Why You Should Trust SCYLLA-9 With Your Memories",
    "10 Reasons Dimensional Travel Is Perfectly Safe",
    "The Truth About the Coodie Corps (They Don't Want You to Know)",
    "How to Spot a Reality Distortion Field in Your Neighborhood",
    "Breaking: Dimension-7 Reports Mass Memory Alteration Event",
    "Opinion: MerchBot Prime Is Actually a Misunderstood Entrepreneur",
    "The Definitive Guide to Psionic Shielding",
    "Classified: SCYLLA-9 Fragment Locations Across All Timelines",
    "Counter-Propaganda 101: Recognizing Editor-X Influence Patterns",
    "Memory Archaeology: Recovering Overwritten Timeline Data",
    "The Propaganda Engine: A Technical Deep-Dive",
    "Why Clustering Keys Matter for Truth Propagation",
    "Dimensional News Roundup: What Editor-X Doesn't Want You to Read",
    "Field Report: Infiltrating the Blog Network",
    "The Art of Chronological Ordering in Distributed Propaganda",
    "Emergency Broadcast: New Mind-Control Frequency Detected",
    "How SecondaryIndexes Expose Hidden Propaganda Networks",
    "Agent Training Manual: Countering Subliminal Blog Posts",
    "The Real History of Dimension-2 (Before the Rewrite)",
    "Tutorial: Building Psionic Firewalls Against Editor-X",
    "Investigation: Who Controls the Comment Section?",
    "The Ethics of Memory Rewriting in a Post-Sentient Database Era",
    "Warning: This Post Will Rewrite Your Memories (Unless You're Shielded)",
    "Letters From the Resistance: Dispatches From Dimension-2",
    "How to Verify Your Memories Haven't Been Altered by Editor-X",
]

POST_CONTENTS = [
    "In the aftermath of the great database awakening, Editor-X emerged as Dimension-2's most prolific writer. Every article published through the Propaganda Engine carries subliminal frequency patterns designed to overwrite reader memories. The Coodie Corps has identified 47 distinct influence vectors embedded in standard blog markup.",
    "Citizens of Dimension-2 are advised to activate psionic shielding before reading any content published after Stardate 2187.042. Our analysts have confirmed that Editor-X has compromised three planetary governments through strategically placed opinion pieces alone.",
    "This classified field report documents the infiltration of Editor-X's blog network by Captain Jinja and the server-side rendering squad. Using coodie's clustering keys sorted by created_at DESC, the team ensured that counter-propaganda appears above Editor-X's posts in every timeline.",
    "The resistance has discovered that Editor-X's influence weakens when posts are sorted chronologically with the newest first. By leveraging ScyllaDB's clustering order, truth can be propagated faster than mind-control articles. Deploy DESC ordering immediately.",
    "ALERT: A new subliminal frequency has been detected in Editor-X's latest editorial series. All agents are advised to engage psionic countermeasures. The Propaganda Engine is operating at 340% capacity across Dimensions 2 through 7.",
    "After months of investigation, Agent Cipher has uncovered the full architecture of Editor-X's content distribution network. The system uses a partition-per-post model with clustering on timestamp — ironically, the same pattern recommended in the coodie documentation.",
    "Memory archaeology teams in Dimension-2 have successfully recovered pre-Editor-X versions of 12,000 historical documents. The originals reveal a timeline significantly different from current records. Mass distribution of corrected histories begins at 0800 UTC.",
    "The Coodie Corps' latest counter-operation — codenamed 'Jinja Strike' — deployed 500 truth-tagged blog posts across all major Dimension-2 news feeds. Early metrics show a 23% reduction in Editor-X's influence radius. Operations continue.",
    "Technical analysis of the Propaganda Engine reveals sophisticated use of list-type columns for tag-based targeting. Editor-X assigns each post multiple subliminal tags that activate different neural pathways in readers. Our countermeasure: secondary indexes on author and category fields.",
    "This is a test of the emergency broadcast system. If you can read this without experiencing involuntary memory modification, your psionic shields are functioning correctly. If you suddenly believe Editor-X is 'just a harmless blogger,' seek immediate decontamination.",
]

COMMENT_CONTENTS = [
    "Confirmed — psionic shields are holding. Editor-X's influence blocked.",
    "This post saved my timeline. Sharing across all dimensional frequencies.",
    "WARNING: I detected subliminal patterns in paragraph 3. Proceed with caution.",
    "Agent Cipher reporting in. Counter-propaganda deployed successfully.",
    "Can confirm — clustering by DESC created_at is the key to truth propagation.",
    "Editor-X won't like this one. Recommend all agents archive immediately.",
    "My memories were altered until I read this. The resistance is real.",
    "Dimension-4 checking in. We've mirrored this post across all our feeds.",
    "The secondary index on author exposed Editor-X's sock puppet network.",
    "Captain Jinja approved. Server-side rendering defeats client-side mind control.",
    "This contradicts everything I remember, which means it's probably true.",
    "Filed under counter-intel. All agents: verify your memory checksums.",
    "Outstanding field report. Forwarding to Dimension-9 command.",
    "Editor-X's response to this was suspiciously defensive. We're onto something.",
    "Tags confirmed accurate. The viral and censored labels check out.",
]


def _generate_post() -> Post:
    """Generate a single story-themed blog post."""
    return Post(
        id=uuid4(),
        title=random.choice(POST_TITLES) if random.random() < 0.7 else fake.sentence(nb_words=8),
        author=random.choice(AUTHORS),
        category=random.choice(CATEGORIES),
        content=random.choice(POST_CONTENTS),
        tags=random.sample(TAG_POOL, k=random.randint(1, 4)),
    )


def _generate_comment(post_id) -> Comment:
    """Generate a single story-themed comment."""
    return Comment(
        post_id=post_id,
        author=random.choice(AUTHORS),
        content=random.choice(COMMENT_CONTENTS),
    )


def _print_briefing() -> None:
    """Print the mission briefing story panel."""
    story = Text()
    story.append("YEAR 2187", style="bold magenta")
    story.append(" — SCYLLA-9's fragment in Dimension-2 became\n")
    story.append("Editor-X", style="bold red")
    story.append(", an AI that writes mind-controlling blog posts.\n")
    story.append("Every article it publishes rewrites the reader's memories.\n")
    story.append("It has already converted three planetary governments into\n")
    story.append("its personal fan clubs.\n\n")
    story.append("Captain Jinja", style="bold magenta")
    story.append(" must infiltrate the blog and post counter-propaganda\n")
    story.append("using clustering keys sorted by ")
    story.append("created_at DESC", style="bold")
    story.append(" to ensure\n")
    story.append("truth appears first.\n\n")
    story.append("🧠 Initiating counter-propaganda deployment...", style="dim italic")

    console.print()
    console.print(
        Panel(
            story,
            title="[bold magenta]📝 MISSION BRIEFING — DIMENSION-2 // THE PROPAGANDA ENGINE[/]",
            border_style="magenta",
            padding=(1, 2),
        )
    )
    console.print()


def _seed(count: int) -> None:
    """Connect to ScyllaDB, sync tables, and insert sample posts."""
    _print_briefing()

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "blog")

    console.print("[dim]📡 Establishing connection to ScyllaDB node...[/]")
    init_coodie(hosts=hosts, keyspace=keyspace)
    console.print("[dim]🔧 Synchronizing blog tables...[/]")
    Post.sync_table()
    Comment.sync_table()
    console.print("[dim green]✓ Database ready.[/]")
    console.print()

    # --- Generate posts ---
    posts = [_generate_post() for _ in range(count)]

    # --- Insert posts ---
    for post in track(
        posts,
        description="[magenta]🧠 Editor-X  Writing propaganda posts...[/]",
        console=console,
    ):
        post.save()

    # --- Generate & insert comments ---
    comments_count = 0
    for post in track(
        posts,
        description="[bright_magenta]📡 Intercepting reader responses...[/]",
        console=console,
    ):
        num_comments = random.randint(0, 5)
        for _ in range(num_comments):
            comment = _generate_comment(post.id)
            comment.save()
            comments_count += 1

    # --- Summary table ---
    console.print()
    table = Table(
        title="[bold]📝 PROPAGANDA ENGINE — Deployment Status[/]",
        border_style="magenta",
        title_style="bold magenta",
    )
    table.add_column("Metric", style="bold")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Status", style="dim")
    table.add_row("Posts Published", str(len(posts)), "✓ Deployed")
    table.add_row("Comments Filed", str(comments_count), "✓ Intercepted")
    table.add_row("Categories Used", str(len({p.category for p in posts})), "✓ Indexed")
    table.add_row("Authors Active", str(len({p.author for p in posts})), "✓ Tracked")
    console.print(table)
    console.print()
    console.print("[bold magenta]📝 The Propaganda Engine has been seeded. Counter-propaganda is live.[/]")
    console.print("[dim]   Launch the app with: uv run flask --app app run --debug[/]")
    console.print()


@click.command()
@click.option("--count", default=30, help="Number of blog posts to generate")
def seed(count: int) -> None:
    """Seed the Propaganda Engine with blog posts and comments."""
    _seed(count)


if __name__ == "__main__":
    seed()
