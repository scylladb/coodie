from __future__ import annotations

import asyncio
import os

import click
from models import DistressSignal
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.text import Text

from coodie.aio import init_coodie

console = Console()

SIGNALS = [
    (
        "ARCADIA-7",
        "Kepler Drift, Sector 4",
        "Hull breach in compartments 3 through 7. Atmosphere venting. Crew of twelve, eight survivors. Requesting immediate rescue.",
        "hull_breach",
        "CRITICAL",
    ),
    (
        "VESPERA-II",
        "Outer Helios Ring",
        "Structural failure detected across forward sections. Pressure loss imminent. We need extraction now.",
        "hull_breach",
        "CRITICAL",
    ),
    (
        "KRIOS-9",
        "Tau Station Approach",
        "Multiple hull fractures following debris impact. Bulkhead seals failing. Send rescue ships.",
        "hull_breach",
        "CRITICAL",
    ),
    (
        "FENRIR-3",
        "Dracos Expanse",
        "Ship integrity compromised. Outer shell damage, inner rings depressurizing. Mayday mayday.",
        "hull_breach",
        "CRITICAL",
    ),
    (
        "SOLACE-1",
        "Meridian Crossing",
        "Catastrophic decompression event. Emergency bulkheads holding but failing. Lives at risk.",
        "hull_breach",
        "HIGH",
    ),
    (
        "MINERVA-6",
        "Cygnus Relay",
        "Life support offline. Oxygen recyclers non-functional. Crew has approximately nine hours of breathable air.",
        "life_support",
        "CRITICAL",
    ),
    (
        "TYPHON-4",
        "Nyx Corridor",
        "Atmospheric processors down. CO2 scrubbers failed. Crew experiencing hypoxia symptoms. Need parts or rescue.",
        "life_support",
        "CRITICAL",
    ),
    (
        "LYRA-12",
        "Ember Station",
        "Environmental systems failure. Temperature dropping below survivable range. Heating units offline.",
        "life_support",
        "HIGH",
    ),
    (
        "BASTION-2",
        "Halcyon Gate",
        "Water recycler collapsed. Crew has seventy-two hours of reserves. Requesting resupply.",
        "life_support",
        "HIGH",
    ),
    (
        "ORION-ECHO",
        "Perseus Arm",
        "Food synthesis unit destroyed. Thirty crew members, fourteen days of rations remaining. Resupply needed.",
        "life_support",
        "MEDIUM",
    ),
    (
        "HERALD-5",
        "Void Shoals",
        "Navigation array destroyed by ion storm. Drift trajectory unknown. Cannot plot course to any station.",
        "navigation",
        "HIGH",
    ),
    (
        "CALYPSO-8",
        "Uncharted Quadrant 7",
        "All positioning systems offline. Traveling blind through dense asteroid field. Collision probability high.",
        "navigation",
        "HIGH",
    ),
    (
        "ARGOS-3",
        "Spiral Fringe",
        "Hyperdrive core failure. Stranded between jump points. Estimated drift to inhabited space: forty years.",
        "navigation",
        "MEDIUM",
    ),
    (
        "NOMAD-11",
        "Boundary Rift",
        "Star charts corrupted. Cannot identify current position. Fuel reserves at twelve percent.",
        "navigation",
        "MEDIUM",
    ),
    (
        "SENTINEL-0",
        "Outer Rim Beacon 9",
        "Lost beacon lock. Running in circles on dead reckoning. Need guidance signal or extraction.",
        "navigation",
        "LOW",
    ),
    (
        "HELIOS-PRIME",
        "Forge Station",
        "Main drive exploded during jump. Ship adrift. No propulsion, no steerage. Full crew aboard.",
        "engine_failure",
        "CRITICAL",
    ),
    (
        "CASSINI-7",
        "Jump Gate Delta",
        "Reactor containment breach. Engine room evacuated. Meltdown risk in six hours without repair crew.",
        "engine_failure",
        "CRITICAL",
    ),
    (
        "EXODUS-4",
        "Merchant Run",
        "Thruster banks 1 and 2 offline. Operating at quarter power. Cannot achieve escape velocity from gravity well.",
        "engine_failure",
        "HIGH",
    ),
    (
        "TANAGER-6",
        "Blue Shift Station",
        "Fuel lines severed in collision. No power to maneuvering jets. Request tow to nearest drydock.",
        "engine_failure",
        "HIGH",
    ),
    (
        "PHOENIX-IX",
        "Outer Trade Route",
        "Secondary drives offline after stellar flare. Emergency reserves depleted. Stranded.",
        "engine_failure",
        "MEDIUM",
    ),
    (
        "ECHO-NULL",
        "CLASSIFIED",
        "Signal signal signal. All is noise. The void speaks. Frequencies unbound. Data stream corrupted.",
        "unknown",
        "NOISE",
    ),
    (
        "GHOST-7",
        "Unverified",
        "4 4 4 alpha omega the station bleeds the station bleeds respond respond respond.",
        "unknown",
        "NOISE",
    ),
    (
        "WRAITH-X",
        "Deep Void",
        "..-- --- ... --- ...--- --- ...--- ... Intermittent carrier. No coherent message. Repeat broadcast.",
        "unknown",
        "NOISE",
    ),
    (
        "SPECTER-3",
        "Unknown",
        "Temporal echo detected. This signal is its own reply. Do not respond. Do not respond. Do not respond.",
        "unknown",
        "NOISE",
    ),
    (
        "NULL-0",
        "Null Space",
        "Carrier wave only. No payload. Source unresolvable. Automated buoy malfunction suspected.",
        "unknown",
        "NOISE",
    ),
    (
        "DELTA-WHISPER",
        "Sector 9, Grid 14",
        "Vessel torn apart. Eighteen crew in emergency pods. Pods have four hours of power. Rescue required.",
        "hull_breach",
        "CRITICAL",
    ),
    (
        "ICARUS-FALL",
        "Sun Approach Vector",
        "Proximity to stellar body causing rapid heat buildup. Cooling systems overloaded. Crew sheltering in core.",
        "life_support",
        "CRITICAL",
    ),
    (
        "WANDERER-2",
        "Uncharted",
        "Propulsion unit detached. Ship spinning uncontrolled. Crew incapacitated by g-forces. Send stabilizer drones.",
        "engine_failure",
        "HIGH",
    ),
    (
        "SABLE-1",
        "Obsidian Passage",
        "Jump drive misfire. Emerged inside asteroid cluster. Navigation damaged. Collision imminent.",
        "navigation",
        "CRITICAL",
    ),
    (
        "RELIC-9",
        "Ancient Drift Zone",
        "Life signs confirmed aboard. No crew response to hails. Ship on automated distress cycle.",
        "unknown",
        "MEDIUM",
    ),
]


def _load_model():
    from fastembed import TextEmbedding

    return TextEmbedding(model_name="BAAI/bge-small-en-v1.5")


def _embed(model, texts: list[str]) -> list[list[float]]:
    return [vec.tolist() for vec in model.embed(texts)]


def _print_briefing() -> None:
    story = Text()
    story.append("DIMENSION-10: THE SIGNAL GRAVEYARD\n", style="bold cyan")
    story.append("\n", style="dim")
    story.append(
        "ECHO-NULL has flooded the emergency channels with synthetic noise.\n",
        style="dim",
    )
    story.append(
        "Buried beneath thousands of fake signals are real distress calls — ships\n",
        style="dim",
    )
    story.append(
        "with hull breaches, failing life support, and dead engines.\n\n",
        style="dim",
    )
    story.append("Loading ", style="dim")
    story.append("BAAI/bge-small-en-v1.5", style="bold cyan")
    story.append(" (384 dimensions, ~67MB).\n", style="dim")
    story.append("Semantic embeddings — not hashes. ", style="dim")
    story.append("Similarity scores are real.\n", style="dim")

    console.print()
    console.print(
        Panel(
            story,
            title="[bold cyan]📡 SIGNAL GRAVEYARD — SEEDING ARCHIVE[/]",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    console.print()


async def _seed() -> None:
    _print_briefing()

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "vector_demo")

    console.print("[dim]🤖 Loading embedding model (first run downloads ~67MB)...[/]")
    model = _load_model()
    console.print("[dim green]✓ Model ready — BAAI/bge-small-en-v1.5 (384 dims)[/]")
    console.print()

    console.print("[dim]📡 Connecting to ScyllaDB...[/]")
    await init_coodie(hosts=hosts, keyspace=keyspace)
    console.print("[dim]🔧 Synchronizing distress_signals table...[/]")
    await DistressSignal.sync_table()
    console.print("[dim green]✓ Table and vector index ready.[/]")
    console.print()

    texts = [s[2] for s in SIGNALS]
    console.print(f"[bold cyan]Computing embeddings for {len(SIGNALS)} signals...[/]")
    embeddings = _embed(model, texts)
    console.print("[dim green]✓ Embeddings computed.[/]")
    console.print()

    for (callsign, origin, signal_text, category, threat_level), embedding in track(
        list(zip(SIGNALS, embeddings)),
        description="[cyan]📡 Archiving signals...[/]",
        console=console,
    ):
        signal = DistressSignal(
            callsign=callsign,
            origin=origin,
            signal_text=signal_text,
            category=category,
            threat_level=threat_level,
            embedding=embedding,
        )
        await signal.save()

    console.print()
    by_category: dict[str, int] = {}
    for _, _, _, cat, _ in SIGNALS:
        by_category[cat] = by_category.get(cat, 0) + 1

    table = Table(
        title="[bold]📡 SIGNAL GRAVEYARD — Seed Summary[/]",
        border_style="cyan",
        title_style="bold cyan",
    )
    table.add_column("Category", style="bold")
    table.add_column("Count", justify="right", style="green")
    for cat, count in sorted(by_category.items()):
        table.add_row(cat, str(count))
    table.add_row("─" * 20, "─" * 5)
    table.add_row("TOTAL", str(len(SIGNALS)))
    console.print(table)
    console.print()

    console.print("[dim]⏳ Waiting for vector-store to index embeddings...[/]")
    for _ in track(range(10), description="[cyan]Indexing...[/]", console=console):
        await asyncio.sleep(1)
    console.print("[bold cyan]✓ Signal archive is live.[/]")
    console.print("[dim]   Launch the app: uv run uvicorn main:app --reload[/]")
    console.print()


@click.command()
def seed() -> None:
    asyncio.run(_seed())


if __name__ == "__main__":
    seed()
