"""Workflow convention tests — enforce repository-specific standards for GitHub Actions.

These tests parse the workflow YAML files in .github/workflows/ and verify
that they follow the project's conventions. They complement actionlint
(which checks GitHub Actions semantics) by enforcing project-level rules.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

WORKFLOWS_DIR = Path(__file__).resolve().parent.parent / ".github" / "workflows"
WORKFLOW_FILES = sorted(WORKFLOWS_DIR.glob("*.yml"))


def _load_workflow(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _iter_steps(workflow: dict):
    """Yield every step dict from every job in the workflow."""
    for job in workflow.get("jobs", {}).values():
        for step in job.get("steps", []):
            yield step


# ---------------------------------------------------------------------------
# 3.2 — All workflows use pinned action versions (@vN or @sha)
# ---------------------------------------------------------------------------

_PINNED_RE = re.compile(r"@(v?\d|[0-9a-f]{40}|release/)")


@pytest.mark.parametrize("workflow_path", WORKFLOW_FILES, ids=[p.name for p in WORKFLOW_FILES])
def test_actions_are_pinned(workflow_path: Path):
    """Every `uses:` reference must be pinned to @vN, a full SHA, or release/ tag."""
    workflow = _load_workflow(workflow_path)
    for step in _iter_steps(workflow):
        uses = step.get("uses", "")
        if uses and "@" in uses:
            assert _PINNED_RE.search(uses), f"{workflow_path.name}: unpinned action {uses!r}"


# ---------------------------------------------------------------------------
# 3.3 — All multi-job workflows define a concurrency group
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("workflow_path", WORKFLOW_FILES, ids=[p.name for p in WORKFLOW_FILES])
def test_multi_job_concurrency(workflow_path: Path):
    """Workflows with >1 job should define a top-level concurrency group.

    Exception: tag-only workflows (e.g. publish) are excluded because
    concurrent tag pushes are rare and should not cancel each other.
    """
    workflow = _load_workflow(workflow_path)
    jobs = workflow.get("jobs", {})
    if len(jobs) <= 1:
        pytest.skip("single-job workflow")

    # Skip tag-only publish workflows
    triggers = workflow.get("on", workflow.get(True, {}))
    if isinstance(triggers, dict):
        push_cfg = triggers.get("push", {})
        if isinstance(push_cfg, dict) and "tags" in push_cfg and "branches" not in push_cfg:
            # Only triggered by tag pushes — no other event types that need concurrency
            other_triggers = {k for k in triggers if k != "push"}
            if not other_triggers:
                pytest.skip("tag-only workflow")

    assert "concurrency" in workflow, f"{workflow_path.name}: multi-job workflow missing top-level concurrency group"


# ---------------------------------------------------------------------------
# 3.4 — All steps using `gh` CLI have GH_TOKEN env var
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("workflow_path", WORKFLOW_FILES, ids=[p.name for p in WORKFLOW_FILES])
def test_gh_cli_has_token(workflow_path: Path):
    """Every step whose `run:` block invokes `gh ` must have GH_TOKEN in env."""
    workflow = _load_workflow(workflow_path)
    for step in _iter_steps(workflow):
        run_block = step.get("run", "")
        if "gh " not in run_block and "gh api" not in run_block:
            continue
        step_env = step.get("env", {}) or {}
        job_env_keys: set[str] = set()
        # Also check job-level env
        for job in workflow.get("jobs", {}).values():
            job_env_keys.update((job.get("env") or {}).keys())
        has_token = "GH_TOKEN" in step_env or "GH_TOKEN" in job_env_keys
        step_name = step.get("name", "(unnamed)")
        assert has_token, f"{workflow_path.name} step {step_name!r}: uses `gh` CLI but has no GH_TOKEN"


# ---------------------------------------------------------------------------
# 3.5 — Workflows with git history commands use fetch-depth: 0
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("workflow_path", WORKFLOW_FILES, ids=[p.name for p in WORKFLOW_FILES])
def test_fetch_depth_for_git_history(workflow_path: Path):
    """If any step uses `git log`, `git merge-base`, or `git merge`, a checkout with fetch-depth: 0 must exist."""
    workflow = _load_workflow(workflow_path)
    steps = list(_iter_steps(workflow))

    needs_history = any(re.search(r"\bgit\s+(log|merge-base|merge)\b", step.get("run", "")) for step in steps)
    if not needs_history:
        pytest.skip("no git history commands found")

    has_full_fetch = any(
        step.get("with", {}).get("fetch-depth") == 0 for step in steps if "actions/checkout" in step.get("uses", "")
    )
    assert has_full_fetch, f"{workflow_path.name}: uses git log/merge commands but no checkout with fetch-depth: 0"


# ---------------------------------------------------------------------------
# 3.6 — All schedule cron expressions are syntactically valid
# ---------------------------------------------------------------------------

# Simple regex: 5 fields separated by spaces, each field contains [0-9*,/-]
_CRON_FIELD = r"[0-9*,/\-LW#?]+"
_CRON_RE = re.compile(rf"^\s*{_CRON_FIELD}(\s+{_CRON_FIELD}){{4}}\s*$")


@pytest.mark.parametrize("workflow_path", WORKFLOW_FILES, ids=[p.name for p in WORKFLOW_FILES])
def test_schedule_cron_valid(workflow_path: Path):
    """All schedule triggers must have syntactically valid 5-field cron expressions."""
    workflow = _load_workflow(workflow_path)
    triggers = workflow.get("on", workflow.get(True, {}))
    if not isinstance(triggers, dict):
        pytest.skip("no structured triggers")
    schedules = triggers.get("schedule", [])
    if not schedules:
        pytest.skip("no schedule trigger")

    for entry in schedules:
        cron = entry.get("cron", "")
        assert _CRON_RE.match(cron), f"{workflow_path.name}: invalid cron expression {cron!r}"


# ---------------------------------------------------------------------------
# 3.7 — Slash-command workflows have per-PR concurrency groups
# ---------------------------------------------------------------------------

_SLASH_COMMAND_WORKFLOWS = [p for p in WORKFLOW_FILES if p.name in ("pr-conflict-detect.yml",)]


@pytest.mark.parametrize("workflow_path", _SLASH_COMMAND_WORKFLOWS, ids=[p.name for p in _SLASH_COMMAND_WORKFLOWS])
def test_slash_command_concurrency(workflow_path: Path):
    """Slash-command and conflict-detection workflows must define a concurrency group
    to prevent overlapping operations on the same PR, even if they have a single job."""
    workflow = _load_workflow(workflow_path)
    assert "concurrency" in workflow, (
        f"{workflow_path.name}: slash-command workflow missing top-level concurrency group"
    )
