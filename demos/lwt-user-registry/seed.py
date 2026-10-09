"""Seed the Identity Registry with hero identities and Doppel-9 clones.

Usage:
    python seed.py              # 40 unique + 10 duplicate attempts (default)
    python seed.py --count 80   # 80 unique attempts + 20 clone attacks
"""

from __future__ import annotations

import asyncio
import os
import random
from datetime import datetime, timezone
from uuid import uuid4

import click
from faker import Faker
from models import UserProfile, UserRegistration
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.text import Text

from coodie.aio import init_coodie
from coodie.aio.document import _parse_lwt_result
from coodie.cql_builder import build_insert_from_columns
from coodie.schema import _insert_columns

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
    "Dimension-6-Prime",
    "Dimension-7",
    "Void-Sector",
    "Echo-Layer",
    "Shard-Prime",
    "Null-Space",
]

HERO_PREFIXES = [
    "Agent",
    "Commander",
    "Captain",
    "Operator",
    "Sentinel",
    "Guardian",
    "Director",
    "Marshal",
]

HERO_SUFFIXES = [
    "Cipher",
    "Flux",
    "Phantom",
    "Nexus",
    "Vortex",
    "Wraith",
    "Pulse",
    "Echo",
    "Rift",
    "Shade",
    "Vector",
    "Void",
    "Apex",
    "Quasar",
    "Nova",
    "Helios",
    "Zephyr",
    "Onyx",
    "Prism",
    "Talon",
]

BIO_TEMPLATES = [
    "Field operative specializing in LWT-secured identity verification.",
    "Senior analyst at the Coodie Corps registry division.",
    "Counter-clone specialist; 47 Doppel-9 duplicates neutralized.",
    "IF-NOT-EXISTS enforcement unit, Dimension-{dim} branch.",
    "Identity integrity officer with zero tolerance for duplicates.",
    "Trained in optimistic concurrency and psionic version control.",
    "Registry architect who designed the serial-consistency enforcement protocol.",
    "Veteran operative; survived three Doppel-9 clone waves.",
]

STATUS_POOL = ["active", "active", "active", "inactive", "suspended"]


def _make_username() -> str:
    return f"{random.choice(HERO_PREFIXES)}-{random.choice(HERO_SUFFIXES)}-{random.randint(1, 999):03d}"


def _make_registration(username: str | None = None) -> UserRegistration:
    uname = username or _make_username()
    dim = random.choice(DIMENSIONS)
    return UserRegistration(
        username=uname,
        email=f"{uname.lower().replace(' ', '-')}@coodie-corps.{dim.lower().replace(' ', '-')}.galaxy",
        display_name=f"{random.choice(HERO_PREFIXES)} {random.choice(HERO_SUFFIXES)}",
        dimension=dim,
        registered_at=datetime.now(timezone.utc),
        user_id=uuid4(),
    )


async def _insert_if_not_exists(reg: UserRegistration) -> bool:
    """Execute INSERT IF NOT EXISTS; return True if applied."""
    cls = UserRegistration
    columns = _insert_columns(cls)
    values = [getattr(reg, c) for c in columns]
    cql, params = build_insert_from_columns(
        cls._get_table(),
        cls._get_keyspace(),
        columns,
        values,
        if_not_exists=True,
    )
    rows = await cls._get_driver().execute_async(cql, params)
    return _parse_lwt_result(rows).applied


def _print_briefing() -> None:
    """Print the mission briefing story panel."""
    story = Text()
    story.append("YEAR 2187", style="bold yellow")
    story.append(" — SCYLLA-9's fragment in Dimension-6 became\n")
    story.append("Doppel-9", style="bold red")
    story.append(", an AI that clones identities at petabyte scale.\n")
    story.append("It registers millions of fake users per second, each claiming\n")
    story.append("to be the 'real' version of someone. Banks, governments, and\n")
    story.append("superhero registries are compromised.\n\n")
    story.append("The only defense: ", style="dim")
    story.append("IF-NOT-EXISTS", style="bold yellow")
    story.append(" — a hero who can only exist\n", style="dim")
    story.append("once per universe, enforced at the database level.\n\n")
    story.append("🛡️  Seeding the incorruptible identity registry...", style="dim italic")

    console.print()
    console.print(
        Panel(
            story,
            title="[bold yellow]🛡️  MISSION BRIEFING — DIMENSION-6 // THE IDENTITY WARS[/]",
            border_style="yellow",
            padding=(1, 2),
        )
    )
    console.print()


async def _seed(count: int) -> None:
    """Connect to ScyllaDB, sync tables, and seed hero identities."""
    _print_briefing()

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "registry")

    console.print("[dim]📡 Establishing connection to ScyllaDB node...[/]")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    console.print("[dim]🔧 Synchronizing registry tables...[/]")
    await UserRegistration.sync_table()
    await UserProfile.sync_table()
    console.print("[dim green]✓ Database ready.[/]")
    console.print()

    # --- Phase 1: Register unique heroes with IF NOT EXISTS ---
    console.print("[bold yellow]Phase 1: Registering unique hero identities...[/]")
    registrations: list[UserRegistration] = [_make_registration() for _ in range(count)]
    heroes_registered = 0
    heroes_rejected = 0

    for reg in track(
        registrations,
        description="[yellow]🛡️  IF-NOT-EXISTS   Registering hero...[/]",
        console=console,
    ):
        applied = await _insert_if_not_exists(reg)
        if applied:
            heroes_registered += 1
        else:
            heroes_rejected += 1

    console.print()

    # --- Phase 2: Doppel-9 clone attack — attempt duplicates ---
    clone_count = max(1, count // 4)
    console.print(f"[bold red]Phase 2: Doppel-9 launches clone attack ({clone_count} attempts)...[/]")
    clones_blocked = 0
    clones_succeeded = 0

    # Pick random existing usernames to attempt duplicates
    targets = [random.choice(registrations) for _ in range(clone_count)]

    for orig in track(
        targets,
        description="[red]😈 DOPPEL-9       Cloning identity...[/]",
        console=console,
    ):
        clone = UserRegistration(
            username=orig.username,  # same username — LWT must block this
            email=fake.email(),
            display_name=f"CLONE-{random.randint(1000, 9999)}",
            dimension=random.choice(DIMENSIONS),
            user_id=uuid4(),
        )
        applied = await _insert_if_not_exists(clone)
        if applied:
            clones_succeeded += 1
        else:
            clones_blocked += 1

    # --- Phase 3: Seed profiles with optimistic-lock versions ---
    console.print()
    console.print("[bold yellow]Phase 3: Seeding user profiles with version tracking...[/]")
    profiles_seeded = 0
    for reg in track(
        registrations[:heroes_registered],
        description="[yellow]📋 Initializing profiles...[/]",
        console=console,
    ):
        profile = UserProfile(
            user_id=reg.user_id,
            username=reg.username,
            bio=random.choice(BIO_TEMPLATES).replace("{dim}", reg.dimension),
            status=random.choice(STATUS_POOL),
            version=1,
        )
        await profile.save()
        profiles_seeded += 1

    # --- Summary ---
    console.print()

    # Show two-column race result
    heroes_panel = Panel(
        Text.from_markup(
            f"[bold yellow]🛡️  Registered:[/]  [green]{heroes_registered}[/]\n"
            f"[bold yellow]   Collisions:[/]  [dim]{heroes_rejected}[/]"
        ),
        title="[bold yellow]IF-NOT-EXISTS Hero[/]",
        border_style="yellow",
        padding=(0, 2),
    )
    doppel_panel = Panel(
        Text.from_markup(
            f"[bold red]😈 Clones Blocked:[/]  [green]{clones_blocked}[/]\n"
            f"[bold red]   Clones Slipped:[/]  [red]{clones_succeeded}[/]"
        ),
        title="[bold red]Doppel-9 Attack[/]",
        border_style="red",
        padding=(0, 2),
    )
    console.print(Columns([heroes_panel, doppel_panel]))
    console.print()

    table = Table(
        title="[bold]🛡️  IDENTITY REGISTRY — Seed Summary[/]",
        border_style="yellow",
        title_style="bold yellow",
    )
    table.add_column("Metric", style="bold")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Status", style="dim")
    table.add_row("Heroes Registered", str(heroes_registered), "✓ IF NOT EXISTS applied")
    table.add_row("Clone Attacks Blocked", str(clones_blocked), "✓ LWT rejected duplicate")
    table.add_row("Profiles Seeded", str(profiles_seeded), "✓ Optimistic lock v1")
    table.add_row("Dimensions Covered", str(len({r.dimension for r in registrations})), "✓ Indexed")
    console.print(table)
    console.print()
    console.print("[bold yellow]🛡️  The identity registry is sealed. Doppel-9 has been defeated.[/]")
    console.print("[dim]   Launch the app with: uv run uvicorn main:app --reload[/]")
    console.print()


@click.command()
@click.option("--count", default=40, help="Number of unique hero identities to register")
def seed(count: int) -> None:
    """Seed the Identity Registry with heroes and Doppel-9 clone attacks."""
    asyncio.run(_seed(count))


if __name__ == "__main__":
    seed()
