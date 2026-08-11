"""Seed the Argus-Prime test tracker with synthetic CI/CD data.

Usage:
    python seed.py                          # 5 users, 20 test runs, 100 events (interactive)
    python seed.py --no-interactive         # non-interactive / CI mode
    python seed.py --users 10               # 10 users
    python seed.py --runs 50                # 50 test runs
    python seed.py --events 200             # 200 events
    python seed.py --batch-size 25          # 25 events per batch

Demonstrates:
  - Batch event ingestion (logged + unlogged batches)
  - Prepared-statement caching (automatic via coodie drivers)
  - Partition-scoped queries (events by run_id + kind, notifications by receiver)
"""

from __future__ import annotations

import os
import random
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid1, uuid4

import click
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeRemainingColumn
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from coodie.sync import BatchQuery, init_coodie

from models import Event, Notification, TestRun, User

console = Console()

STATUS_STYLE = {
    "passed": "bold green",
    "failed": "bold red",
    "running": "bold yellow",
    "aborted": "bold magenta",
    "created": "dim",
    "not_run": "dim",
}
SEV_STYLE = {
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "critical": "bold red",
}

# ── Themed data pools ─────────────────────────────────────────────────

USERNAMES = [
    "argus-admin",
    "ci-watcher",
    "sct-runner",
    "nightly-bot",
    "release-mgr",
    "qa-lead",
    "perf-tester",
    "scylla-dev",
    "oss-contrib",
    "infra-ops",
]

BUILD_PREFIXES = [
    "scylla-enterprise",
    "scylla-oss",
    "scylla-manager",
    "scylla-operator",
    "scylla-monitoring",
    "python-driver",
    "gocql",
    "java-driver",
    "rust-driver",
    "coodie",
]

SCYLLA_VERSIONS = [
    "6.0.0",
    "6.0.1",
    "6.1.0-rc1",
    "5.4.3",
    "5.4.2",
    "2025.1.0",
    "2025.1.1",
    "2025.2.0-dev",
]

STATUSES = ["created", "running", "passed", "failed", "aborted", "not_run"]
INVESTIGATION_STATUSES = ["not_investigated", "investigated", "in_progress", "ignored"]

EVENT_KINDS = ["error", "warning", "info", "status_change", "heartbeat", "nemesis"]

EVENT_BODIES = {
    "error": [
        "Timeout waiting for cluster to stabilize after nemesis",
        "Node restart failed — CQL port unreachable after 120s",
        "OOM killer terminated scylla process on node-3",
        "Assertion failure in compaction_manager::run()",
        "Schema disagreement detected across 3/5 nodes",
    ],
    "warning": [
        "Compaction backlog exceeds 100 GB on node-2",
        "Latency p99 exceeded 500 ms threshold",
        "Gossip heartbeat delayed by 30s for node-4",
        "Disk usage at 85% on /var/lib/scylla",
        "Repair job taking longer than expected (>2h)",
    ],
    "info": [
        "Test run started — provisioning 5-node cluster",
        "Nemesis cycle #3 completed — all nodes recovered",
        "Snapshot taken before upgrade step",
        "Rolling restart completed in 4m 32s",
        "Final validation queries passed — 0 data loss",
    ],
    "status_change": [
        "Status changed: created → running",
        "Status changed: running → passed",
        "Status changed: running → failed",
        "Status changed: failed → not_investigated",
        "Status changed: not_investigated → investigated",
    ],
    "heartbeat": [
        "Heartbeat #1 — cluster healthy, 5/5 nodes UN",
        "Heartbeat #2 — load balanced, avg CPU 45%",
        "Heartbeat #3 — compactions on schedule",
        "Heartbeat #4 — all seeds reachable",
        "Heartbeat #5 — no schema changes detected",
    ],
    "nemesis": [
        "Nemesis: DecommissionMonkey targeting node-2",
        "Nemesis: ChaosMonkey killed scylla on node-4",
        "Nemesis: NetworkPartitionMonkey isolating node-1",
        "Nemesis: RollingRestartMonkey restarting all nodes",
        "Nemesis: CorruptDataMonkey corrupting sstable on node-3",
    ],
}

NOTIFICATION_TYPES = [
    "test_run_started",
    "test_run_passed",
    "test_run_failed",
    "assignment_change",
    "comment_mention",
    "investigation_required",
]

SEVERITY_LEVELS = ["info", "warning", "error", "critical"]


def _chunks(lst: list, size: int) -> list[list]:
    """Split a list into chunks of a given size."""
    return [lst[i : i + size] for i in range(0, len(lst), size)]


# ── Interactive helpers ───────────────────────────────────────────────


def _pause(interactive: bool, prompt: str = "Press [bold green]ENTER[/] to continue...") -> None:
    """Pause for the user to read, if running interactively."""
    if not interactive:
        return
    console.print()
    console.print(Padding(f"  [dim]▶  {prompt}[/]", (0, 0)))
    input()


def _explain(title: str, body: str, *, color: str = "green") -> None:
    """Print a themed explanation panel."""
    console.print(
        Panel(
            Text.from_markup(body),
            title=f"[bold {color}]{title}[/]",
            border_style=color,
            padding=(1, 3),
        )
    )


# ── Data generators ───────────────────────────────────────────────────


def _generate_users(count: int) -> list[dict]:
    """Generate N user records."""
    users = []
    for i in range(count):
        username = USERNAMES[i % len(USERNAMES)]
        if i >= len(USERNAMES):
            username = f"{username}-{i}"
        uid = uuid4()
        users.append(
            {
                "id": uid,
                "username": username,
                "full_name": f"{username.replace('-', ' ').title()}",
                "email": f"{username}@scylladb.com",
                "registration_date": datetime.now(timezone.utc) - timedelta(days=random.randint(30, 365)),
                "roles": random.sample(["admin", "viewer", "operator", "tester"], k=random.randint(1, 3)),
            }
        )
    return users


def _generate_test_runs(count: int, user_ids: list[UUID]) -> list[dict]:
    """Generate N test run records across different builds."""
    runs = []
    for i in range(count):
        prefix = random.choice(BUILD_PREFIXES)
        build_num = random.randint(1000, 9999)
        build_id = f"{prefix}/nightly/{build_num}"
        start = datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 720))
        duration_minutes = random.randint(10, 480)
        status = random.choice(STATUSES)
        end = start + timedelta(minutes=duration_minutes) if status in ("passed", "failed", "aborted") else None

        runs.append(
            {
                "build_id": build_id,
                "start_time": start,
                "id": uuid4(),
                "release_id": uuid4() if random.random() > 0.3 else None,
                "assignee": random.choice(user_ids) if random.random() > 0.4 else None,
                "status": status,
                "investigation_status": random.choice(INVESTIGATION_STATUSES)
                if status == "failed"
                else "not_investigated",
                "heartbeat": random.randint(0, 50),
                "end_time": end,
                "build_job_url": f"https://jenkins.scylladb.com/job/{prefix}/{build_num}",
                "scylla_version": random.choice(SCYLLA_VERSIONS),
                "tags": random.sample(
                    ["nightly", "release", "perf", "longevity", "upgrade", "rolling"], k=random.randint(0, 3)
                ),
            }
        )
    return runs


def _generate_events(count: int, run_ids: list[UUID], user_ids: list[UUID]) -> list[dict]:
    """Generate N event records spread across runs and kinds."""
    events = []
    for _ in range(count):
        kind = random.choice(EVENT_KINDS)
        body = random.choice(EVENT_BODIES[kind])
        events.append(
            {
                "run_id": random.choice(run_ids),
                "kind": kind,
                "created_at": datetime.now(timezone.utc) - timedelta(minutes=random.randint(1, 10000)),
                "id": uuid4(),
                "user_id": random.choice(user_ids) if random.random() > 0.5 else None,
                "body": body,
                "severity": random.choice(SEVERITY_LEVELS),
                "metadata": {"source": random.choice(["sct", "monitor", "nemesis", "manual"])},
            }
        )
    return events


def _generate_notifications(user_ids: list[UUID], run_ids: list[UUID], count_per_user: int) -> list[dict]:
    """Generate notifications for each user."""
    notifications = []
    for uid in user_ids:
        for _ in range(count_per_user):
            ntype = random.choice(NOTIFICATION_TYPES)
            notifications.append(
                {
                    "receiver": uid,
                    "id": uuid1(),
                    "type": ntype,
                    "state": random.choice([0, 1]),  # 0 = unread, 1 = read
                    "sender": random.choice(user_ids),
                    "source_type": "test_run",
                    "source_id": random.choice(run_ids),
                    "title": f"{ntype.replace('_', ' ').title()}",
                    "content": f"Notification: {ntype} for run {random.choice(run_ids)}",
                }
            )
    return notifications


# ── Story panel ───────────────────────────────────────────────────────


def _print_briefing(num_users: int, num_runs: int, num_events: int) -> None:
    """Print the mission briefing story panel."""
    story = Text()
    story.append("DIMENSION-13", style="bold green")
    story.append(" — SCYLLA-9's fragment merged with a\n")
    story.append("test-automation AI to become ")
    story.append("ARGUS-PRIME", style="bold green")
    story.append(", a thousand-eyed\n")
    story.append("entity that observes every CI/CD pipeline in every universe.\n\n")
    story.append("It tracks test runs with ")
    story.append("composite partition keys", style="bold cyan")
    story.append(" so precise\nthat it can distinguish two test failures\n")
    story.append("that happened one Planck-time apart.\n\n")
    story.append("ARGUS-PRIME has declared that all software must achieve\n")
    story.append("100% test coverage", style="bold red")
    story.append(" or face dimensional annihilation.\n\n")
    story.append("This demo walks you through how ", style="dim")
    story.append("coodie", style="bold white")
    story.append(" stores and queries\nthat surveillance data in ScyllaDB — step by step.", style="dim")

    stats = Text()
    stats.append(f"  Operatives  : {num_users}\n", style="dim cyan")
    stats.append(f"  Test Runs   : {num_runs}\n", style="dim cyan")
    stats.append(f"  Events      : {num_events}\n", style="dim cyan")
    stats.append("  Keyspace    : argus\n", style="dim cyan")

    console.print()
    console.print(
        Panel(
            story,
            title="[bold green]🐙  MISSION BRIEFING — DIMENSION-13 // THE PANOPTICON PROTOCOL[/]",
            border_style="green",
            padding=(1, 3),
        )
    )
    console.print(
        Panel(
            stats,
            title="[bold cyan]OPERATION PARAMETERS[/]",
            border_style="cyan",
            padding=(0, 1),
        )
    )
    console.print()


# ── Ingestion phases ──────────────────────────────────────────────────


def _ingest_users(users: list[dict], interactive: bool) -> None:
    """Insert users one-by-one (typically small count)."""
    _explain(
        "🔵  PHASE 1 — User Registration",
        (
            "[bold]What coodie is doing:[/]\n"
            "  Each [bold cyan]User[/] is saved with [cyan]Document.save()[/] — one INSERT per record.\n"
            "  Under the hood the driver prepares the CQL INSERT once and caches it;\n"
            "  every subsequent call reuses that [bold]PreparedStatement[/] (zero re-prepare overhead).\n\n"
            "[bold]Table layout:[/]\n"
            "  Partition key  → [cyan]id[/]  (UUID — one partition per user)\n"
            "  Secondary indexes on [cyan]username[/], [cyan]email[/], [cyan]api_token[/]\n"
            "    → lets ARGUS-PRIME find any operative by token in O(1)"
        ),
        color="cyan",
    )
    _pause(interactive)
    console.print(Rule("[bold cyan]registering operatives[/]", style="cyan"))
    for u in users:
        User(**u).save()
        console.print(
            f"  [cyan]👁[/]  [bold]{u['username']:<18}[/]  "
            f"[dim]{u['email']:<32}[/]  "
            f"[[{', '.join(f'[bold cyan]{r}[/]' for r in u['roles'])}]]"
        )
    console.print()


def _ingest_test_runs(runs: list[dict], batch_size: int, interactive: bool) -> int:
    """Batch-insert test runs using LOGGED batches."""
    _explain(
        "🟢  PHASE 2 — Test Run Ingestion  ▸  LOGGED Batches",
        (
            "[bold]What coodie is doing:[/]\n"
            "  Test runs are written via [cyan]BatchQuery(logged=True)[/].\n"
            "  A [bold]LOGGED batch[/] in Cassandra/ScyllaDB is [bold green]atomic[/] — either every row in\n"
            "  the batch is persisted or none are.  The coordinator writes a batch log\n"
            "  to two nodes before applying, so partial failures are impossible.\n\n"
            "[bold]Table layout:[/]\n"
            "  Partition key  → [cyan]build_id[/]  (e.g. 'scylla-oss/nightly/4271')\n"
            "  Clustering key → [cyan]start_time DESC[/]\n"
            "    → 'latest run for build X' hits [bold]exactly one partition[/],\n"
            "      and the most recent run is returned first with no ORDER BY needed.\n\n"
            "[bold]Why batch size matters:[/]\n"
            f"  Each batch holds up to [bold]{batch_size}[/] rows.  Smaller batches mean lower\n"
            "  coordinator memory pressure; larger batches reduce round-trips."
        ),
        color="green",
    )
    _pause(interactive)
    console.print(Rule("[bold green]ingesting test runs via LOGGED batches[/]", style="green"))

    batches = _chunks(runs, batch_size)
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40, complete_style="green", finished_style="bold green"),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        overall = progress.add_task("[bold green]🐙 Test Runs", total=len(runs))
        for i, batch in enumerate(batches, start=1):
            with BatchQuery(logged=True) as bq:
                for row in batch:
                    TestRun(**row).save(batch=bq)
            progress.advance(overall, len(batch))
            progress.console.print(
                f"  [green]✓ LOGGED  batch #{i:03d}[/]  "
                f"[dim]({len(batch)} rows)[/]  [dim green]atomic commit — no partial writes[/]"
            )

    console.print()
    return len(runs)


def _ingest_events(events: list[dict], batch_size: int, interactive: bool) -> int:
    """Batch-insert events using UNLOGGED batches."""
    _explain(
        "🔴  PHASE 3 — Event Storm  ▸  UNLOGGED Batches",
        (
            "[bold]What coodie is doing:[/]\n"
            "  Events are written via [cyan]BatchQuery(logged=False)[/].\n"
            "  An [bold]UNLOGGED batch[/] skips the batch log entirely — [bold green]maximum throughput[/],\n"
            "  but without atomicity guarantees.  Perfect for high-volume event streams\n"
            "  where losing a handful of events is acceptable.\n\n"
            "[bold]Table layout — Compound Partition Key:[/]\n"
            "  Partition key  → [cyan](run_id, kind)[/]  ← two columns form a single partition\n"
            "  Clustering key → [cyan]created_at DESC[/]\n"
            "    → query 'all errors for run X' is a [bold]single-partition scan[/]:\n"
            "      [cyan]Event.find(run_id=..., kind='error').all()[/]\n"
            "    → ARGUS-PRIME can retrieve every error in a run without touching\n"
            "      any other partition — near-zero latency regardless of cluster size.\n\n"
            "[bold]Prepared-statement cache at work:[/]\n"
            "  The INSERT for events is prepared once and reused for every row in\n"
            "  every batch.  coodie's driver holds a per-session LRU cache keyed\n"
            "  on the CQL string — you never call session.prepare() manually."
        ),
        color="red",
    )
    _pause(interactive)
    console.print(Rule("[bold red]unleashing event storm via UNLOGGED batches[/]", style="red"))

    batches = _chunks(events, batch_size)
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40, complete_style="red", finished_style="bold red"),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        overall = progress.add_task("[bold red]⚡ Events", total=len(events))
        for i, batch in enumerate(batches, start=1):
            with BatchQuery(logged=False) as bq:
                for row in batch:
                    Event(**row).save(batch=bq)
            progress.advance(overall, len(batch))
            progress.console.print(
                f"  [red]✓ UNLOGGED batch #{i:03d}[/]  "
                f"[dim]({len(batch)} rows)[/]  [dim red]best-effort — max throughput[/]"
            )

    console.print()
    return len(events)


def _ingest_notifications(notifications: list[dict], batch_size: int, interactive: bool) -> int:
    """Batch-insert notifications using UNLOGGED batches with TimeUUID clustering."""
    _explain(
        "🟢  PHASE 4 — Notification Feed  ▸  TimeUUID Clustering",
        (
            "[bold]What coodie is doing:[/]\n"
            "  Notifications are written via [cyan]BatchQuery(logged=False)[/] — same\n"
            "  unlogged pattern as events, prioritising throughput over atomicity.\n\n"
            "[bold]Table layout — TimeUUID Clustering:[/]\n"
            "  Partition key  → [cyan]receiver[/]  (UUID of the user)\n"
            "  Clustering key → [cyan]id DESC[/]  where [cyan]id[/] is a [bold cyan]timeuuid[/]\n\n"
            "  [bold]Why timeuuid instead of a plain timestamp?[/]\n"
            "  A standard [cyan]timestamp[/] has millisecond resolution — two notifications\n"
            "  arriving in the same millisecond would collide and one would be lost.\n"
            "  [cyan]timeuuid[/] (UUID version 1) embeds a 100-nanosecond clock tick plus a\n"
            "  unique node identifier, making every ID globally unique [bold]and[/] sortable.\n"
            "  Ordering by [cyan]id DESC[/] therefore gives a perfect chronological feed\n"
            "  — newest notifications first — at no extra cost."
        ),
        color="green",
    )
    _pause(interactive)
    console.print(Rule("[bold green]broadcasting notifications — TimeUUID ordering[/]", style="green"))

    batches = _chunks(notifications, batch_size)
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40, complete_style="green", finished_style="bold green"),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        overall = progress.add_task("[bold green]🔔 Notifications", total=len(notifications))
        for i, batch in enumerate(batches, start=1):
            with BatchQuery(logged=False) as bq:
                for row in batch:
                    Notification(**row).save(batch=bq)
            progress.advance(overall, len(batch))
            progress.console.print(
                f"  [green]✓ UNLOGGED batch #{i:03d}[/]  "
                f"[dim]({len(batch)} rows)[/]  [dim green]timeuuid — sub-ms ordering[/]"
            )

    console.print()
    return len(notifications)


# ── Partition-scoped query demos ──────────────────────────────────────


def _demo_partition_queries(runs: list[dict], user_ids: list[UUID], interactive: bool) -> None:
    """Demonstrate partition-scoped queries after ingestion."""
    _explain(
        "🔎  PHASE 5 — Partition-Scoped Queries",
        (
            "[bold]What coodie is doing:[/]\n"
            "  Now that data is in ScyllaDB, ARGUS-PRIME issues three targeted reads.\n"
            "  Each query hits [bold]exactly one partition[/] — the most efficient access\n"
            "  pattern in Cassandra/ScyllaDB because the coordinator can route the\n"
            "  request to a single replica without a scatter-gather fan-out.\n\n"
            "[bold]Query 1 — TestRun by build_id (partition key)[/]\n"
            "  [cyan]TestRun.find(build_id=...).all()[/]\n"
            "  Retrieves all runs for one build, newest first (clustering order).\n\n"
            "[bold]Query 2 — Event by compound partition (run_id, kind)[/]\n"
            "  [cyan]Event.find(run_id=..., kind='error').all()[/]\n"
            "  All error events for one run — single partition because both\n"
            "  partition key columns are supplied.\n\n"
            "[bold]Query 3 — Notification by receiver (partition key)[/]\n"
            "  [cyan]Notification.find(receiver=...).all()[/]\n"
            "  All notifications for one user, newest first (timeuuid DESC).\n\n"
            "  In every case coodie reuses the same [bold]cached PreparedStatement[/] that\n"
            "  was first compiled during ingestion — no re-prepare round-trip."
        ),
        color="yellow",
    )
    _pause(interactive)
    console.print(Rule("[bold yellow]querying the Panopticon[/]", style="yellow"))

    # ── Query 1: TestRun by build_id ──────────────────────────────────
    sample_build = runs[0]["build_id"]
    console.print(f"\n  [bold cyan]▶ TestRun.find(build_id={sample_build!r}).all()[/]")
    results = list(TestRun.find(build_id=sample_build).all())
    console.print(f"  [dim]→ {len(results)} run(s) returned — ordered by start_time DESC[/]")

    run_table = Table(box=None, padding=(0, 2), show_header=True, header_style="bold green")
    run_table.add_column("Run ID", style="dim")
    run_table.add_column("Status")
    run_table.add_column("ScyllaDB version", style="cyan")
    run_table.add_column("Start time", style="dim")
    for run in results[:5]:
        sty = STATUS_STYLE.get(run.status, "")
        run_table.add_row(
            str(run.id)[:16] + "…",
            f"[{sty}]{run.status}[/]",
            run.scylla_version or "—",
            run.start_time.strftime("%Y-%m-%d %H:%M") if run.start_time else "—",
        )
    console.print(Padding(run_table, (0, 4)))

    _pause(interactive, "Press [bold green]ENTER[/] for the next query...")

    # ── Query 2: Event by compound partition ──────────────────────────
    sample_run_id = runs[0]["id"]
    sample_kind = "error"
    console.print(f"\n  [bold cyan]▶ Event.find(run_id={str(sample_run_id)[:8]}…, kind='error').all()[/]")
    event_results = list(Event.find(run_id=sample_run_id, kind=sample_kind).all())
    console.print(f"  [dim]→ {len(event_results)} error event(s) — ordered by created_at DESC[/]")

    ev_table = Table(box=None, padding=(0, 2), show_header=True, header_style="bold red")
    ev_table.add_column("Severity")
    ev_table.add_column("Body", no_wrap=False, max_width=60)
    ev_table.add_column("Source", style="dim")
    for ev in event_results[:5]:
        sty = SEV_STYLE.get(ev.severity, "")
        ev_table.add_row(
            f"[{sty}]{ev.severity}[/]",
            ev.body[:60],
            ev.metadata.get("source", "—"),
        )
    console.print(Padding(ev_table, (0, 4)))

    _pause(interactive, "Press [bold green]ENTER[/] for the last query...")

    # ── Query 3: Notification by receiver ────────────────────────────
    sample_receiver = user_ids[0]
    console.print(f"\n  [bold cyan]▶ Notification.find(receiver={str(sample_receiver)[:8]}…).all()[/]")
    notif_results = list(Notification.find(receiver=sample_receiver).all())
    console.print(f"  [dim]→ {len(notif_results)} notification(s) — timeuuid DESC (newest first)[/]")

    n_table = Table(box=None, padding=(0, 2), show_header=True, header_style="bold green")
    n_table.add_column("Type", style="cyan")
    n_table.add_column("Title")
    n_table.add_column("State", style="dim")
    for n in notif_results[:5]:
        state_label = "[green]read[/]" if n.state else "[yellow]unread[/]"
        n_table.add_row(n.type, n.title, state_label)
    console.print(Padding(n_table, (0, 4)))

    console.print()


# ── Final dashboard ───────────────────────────────────────────────────


def _print_dashboard(users: list[dict], runs: list[dict], events: list[dict]) -> None:
    """Render a live surveillance dashboard summarising everything ARGUS-PRIME saw."""
    console.print()
    console.print(Rule("[bold green]🐙  ARGUS-PRIME  //  PANOPTICON DASHBOARD[/]", style="green"))
    console.print()

    # ── Operatives panel ─────────────────────────────────────────────
    op_table = Table(
        title="[bold cyan]👁  REGISTERED OPERATIVES[/]",
        border_style="cyan",
        title_style="bold cyan",
        show_lines=False,
        padding=(0, 1),
    )
    op_table.add_column("Username", style="bold")
    op_table.add_column("Email", style="dim")
    op_table.add_column("Roles", style="cyan")
    for u in users:
        op_table.add_row(u["username"], u["email"], ", ".join(u["roles"]))

    # ── Test-run status breakdown ─────────────────────────────────────
    status_counts: dict[str, int] = {}
    for r in runs:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1

    status_table = Table(
        title="[bold green]📊  TEST RUN STATUS[/]",
        border_style="green",
        title_style="bold green",
        show_lines=False,
        padding=(0, 1),
    )
    status_table.add_column("Status")
    status_table.add_column("Count", justify="right")
    status_table.add_column("Bar")
    total_runs = len(runs)
    for status in STATUSES:
        count = status_counts.get(status, 0)
        pct = count / total_runs if total_runs else 0
        bar = "█" * int(pct * 20)
        sty = STATUS_STYLE.get(status, "dim")
        status_table.add_row(
            f"[{sty}]{status}[/]",
            f"[{sty}]{count}[/]",
            f"[{sty}]{bar}[/]",
        )

    # ── Event kind breakdown ──────────────────────────────────────────
    kind_counts: dict[str, int] = {}
    for e in events:
        kind_counts[e["kind"]] = kind_counts.get(e["kind"], 0) + 1

    kind_table = Table(
        title="[bold red]⚡  EVENT STORM ANALYSIS[/]",
        border_style="red",
        title_style="bold red",
        show_lines=False,
        padding=(0, 1),
    )
    kind_table.add_column("Kind")
    kind_table.add_column("Count", justify="right")
    kind_table.add_column("Bar")
    total_events = len(events)
    kind_style = {
        "error": "bold red",
        "warning": "yellow",
        "info": "cyan",
        "status_change": "green",
        "heartbeat": "dim green",
        "nemesis": "bold magenta",
    }
    for kind in EVENT_KINDS:
        count = kind_counts.get(kind, 0)
        pct = count / total_events if total_events else 0
        bar = "█" * int(pct * 20)
        sty = kind_style.get(kind, "")
        kind_table.add_row(
            f"[{sty}]{kind}[/]",
            f"[{sty}]{count}[/]",
            f"[{sty}]{bar}[/]",
        )

    # ── Recent runs table (live data from ScyllaDB) ───────────────────
    live_runs = list(TestRun.find().allow_filtering().limit(8).all())
    live_table = Table(
        title="[bold green]🔴  LIVE — RECENT TEST RUNS  (read from ScyllaDB)[/]",
        border_style="green",
        title_style="bold green",
        show_lines=True,
        padding=(0, 1),
    )
    live_table.add_column("Build", style="bold", no_wrap=True)
    live_table.add_column("Status")
    live_table.add_column("ScyllaDB", style="cyan")
    live_table.add_column("Tags", style="dim")
    live_table.add_column("Started")
    for r in live_runs:
        sty = STATUS_STYLE.get(r.status, "")
        tags_str = ", ".join(r.tags[:3]) if r.tags else "—"
        live_table.add_row(
            r.build_id,
            f"[{sty}]{r.status}[/]",
            r.scylla_version or "—",
            tags_str,
            r.start_time.strftime("%m-%d %H:%M") if r.start_time else "—",
        )

    console.print(Padding(op_table, (0, 2)))
    console.print()
    console.print(Columns([Padding(status_table, (0, 1)), Padding(kind_table, (0, 1))]))
    console.print()
    console.print(Padding(live_table, (0, 2)))
    console.print()


# ── Ingestion summary ─────────────────────────────────────────────────


def _print_summary(
    user_count: int,
    run_count: int,
    event_count: int,
    notif_count: int,
    batch_size: int,
) -> None:
    """Print a summary table of the ingestion results."""
    table = Table(
        title="[bold green]🐙  ARGUS-PRIME — Ingestion Complete[/]",
        border_style="green",
        title_style="bold green",
        show_lines=False,
        padding=(0, 2),
    )
    table.add_column("Model", style="bold")
    table.add_column("Records", justify="right", style="bold green")
    table.add_column("Method", style="dim")
    table.add_column("Partition key", style="cyan")
    table.add_column("Clustering key", style="dim cyan")
    table.add_row("User", str(user_count), "Individual saves", "id", "—")
    table.add_row("TestRun", str(run_count), "LOGGED batch", "build_id", "start_time DESC")
    table.add_row("Event", str(event_count), "UNLOGGED batch", "(run_id, kind)", "created_at DESC")
    table.add_row("Notification", str(notif_count), "UNLOGGED batch", "receiver", "timeuuid DESC")
    table.add_section()
    total = user_count + run_count + event_count + notif_count
    table.add_row("[bold]TOTAL[/]", f"[bold green]{total:,}[/]", f"batch_size={batch_size}", "", "")
    console.print(Padding(table, (0, 2)))
    console.print()

    verdict = Text()
    verdict.append("THE PANOPTICON PROTOCOL", style="bold green")
    verdict.append(" IS ACTIVE.\n", style="green")
    verdict.append(f"{total:,} records ingested. ", style="dim green")
    verdict.append("All dimensions are under surveillance. ", style="dim green")
    verdict.append("ARGUS-PRIME is satisfied.", style="bold green")
    console.print(Align(verdict, align="center"))
    console.print()
    console.print(Rule(style="green"))
    console.print()


# ── Main seed function ────────────────────────────────────────────────


def _seed(num_users: int, num_runs: int, num_events: int, batch_size: int, interactive: bool) -> None:
    """Connect to ScyllaDB, sync tables, and run the full ingestion pipeline."""
    _print_briefing(num_users, num_runs, num_events)
    _pause(interactive, "Press [bold green]ENTER[/] to begin the Panopticon Protocol...")

    hosts = os.getenv("SCYLLA_HOSTS", "127.0.0.1").split(",")
    keyspace = os.getenv("SCYLLA_KEYSPACE", "argus")

    console.print(Rule("[bold green]connecting to ScyllaDB[/]", style="green"))
    console.print(f"  [dim]hosts = {hosts}  |  keyspace = {keyspace!r}[/]")
    console.print()

    _explain(
        "🔌  Connection & Schema Sync",
        (
            "[bold]init_coodie()[/] establishes a cluster connection using the underlying\n"
            "Cassandra/ScyllaDB driver.  It creates a single [cyan]Session[/] object that is\n"
            "reused for the entire program — connection pooling is handled automatically.\n\n"
            "[bold]Document.sync_table()[/] inspects the Pydantic model and issues the\n"
            "appropriate [cyan]CREATE TABLE IF NOT EXISTS[/] (and [cyan]CREATE INDEX[/]) statements.\n"
            "It is idempotent — safe to run on every startup, it only modifies the\n"
            "schema when something is actually missing."
        ),
        color="green",
    )
    _pause(interactive)

    init_coodie(hosts=hosts, keyspace=keyspace)
    console.print("  [dim green]✓ cluster connection established[/]")
    User.sync_table()
    TestRun.sync_table()
    Event.sync_table()
    Notification.sync_table()
    console.print("  [dim green]✓ all 4 tables synchronised — ARGUS-PRIME is online[/]")
    console.print()

    # Generate data
    users = _generate_users(num_users)
    user_ids = [u["id"] for u in users]
    runs = _generate_test_runs(num_runs, user_ids)
    run_ids = [r["id"] for r in runs]
    events = _generate_events(num_events, run_ids, user_ids)
    notifications_per_user = max(1, num_events // (num_users * 2))
    notifications = _generate_notifications(user_ids, run_ids, notifications_per_user)

    # Ingest — each phase explains itself and pauses
    _ingest_users(users, interactive)
    run_count = _ingest_test_runs(runs, batch_size, interactive)
    event_count = _ingest_events(events, batch_size, interactive)
    notif_count = _ingest_notifications(notifications, batch_size, interactive)

    # Query demo
    _demo_partition_queries(runs, user_ids, interactive)

    # Visual dashboard (reads live data back from ScyllaDB)
    _explain(
        "📺  LIVE DASHBOARD — reading back from ScyllaDB",
        (
            "All data has been written to ScyllaDB.  The dashboard below is built\n"
            "entirely from [bold cyan]live queries[/] — not from in-memory lists.\n\n"
            "This demonstrates the [bold]full round-trip[/]: write with coodie, read with coodie,\n"
            "display with [cyan]rich[/] — exactly what a real ARGUS-PRIME surveillance node does."
        ),
        color="magenta",
    )
    _pause(interactive, "Press [bold green]ENTER[/] to open the Panopticon Dashboard...")
    _print_dashboard(users, runs, events)

    # Ingestion summary
    _print_summary(num_users, run_count, event_count, notif_count, batch_size)


@click.command()
@click.option("--users", default=5, show_default=True, help="Number of users to create")
@click.option("--runs", default=20, show_default=True, help="Number of test runs to create")
@click.option("--events", default=100, show_default=True, help="Number of events to ingest")
@click.option("--batch-size", default=25, show_default=True, help="Records per batch")
@click.option(
    "--interactive/--no-interactive",
    default=True,
    show_default=True,
    help="Pause between phases for explanation (disable for CI/scripted runs)",
)
def seed(users: int, runs: int, events: int, batch_size: int, interactive: bool) -> None:
    """Seed the Argus-Prime test tracker with synthetic CI/CD data.

    Run with --interactive (default) to walk through each phase with
    explanations and pauses.  Use --no-interactive for CI / automation.
    """
    _seed(users, runs, events, batch_size, interactive)


if __name__ == "__main__":
    seed()
