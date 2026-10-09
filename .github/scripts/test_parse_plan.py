"""Unit tests for .github/scripts/parse-plan.py."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent.parent / ".github" / "scripts" / "parse-plan.py"
PLANS_DIR = Path(__file__).resolve().parent.parent.parent / "docs" / "plans"


def run_parser(plan_file: str, completed_phase: str = "auto") -> dict:
    """Run parse-plan.py as a subprocess and return the parsed JSON output."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--plan-file", plan_file, "--completed-phase", completed_phase],
        capture_output=True,
        check=False,
        text=True,
    )
    assert result.returncode == 0, f"parse-plan.py failed: {result.stderr}"
    return json.loads(result.stdout)


# ---------------------------------------------------------------------------
# Import the module directly for unit-level testing
# ---------------------------------------------------------------------------

_spec = importlib.util.spec_from_file_location("parse_plan", str(SCRIPT))
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]

parse_phases = _mod.parse_phases
find_next_phase = _mod.find_next_phase
_task_rows_all_complete = _mod._task_rows_all_complete
_checkboxes_all_complete = _mod._checkboxes_all_complete


# ---------------------------------------------------------------------------
# Phase header parsing
# ---------------------------------------------------------------------------


def test_phase_with_checkmark_in_header_is_complete():
    text = "### Phase 1: Core Workflow Scaffold ✅\n\nSome content."
    phases = parse_phases(text)
    assert len(phases) == 1
    assert phases[0]["number"] == 1
    assert phases[0]["title"] == "Core Workflow Scaffold"
    assert phases[0]["complete"] is True


def test_phase_with_priority_tag_is_incomplete():
    text = "### Phase 2: Title (Priority: High)\n\nSome content."
    phases = parse_phases(text)
    assert len(phases) == 1
    assert phases[0]["number"] == 2
    assert phases[0]["complete"] is False


def test_phase_with_dash_separator_is_parsed():
    text = "### Phase 1 — Quick wins\n\nSome content."
    phases = parse_phases(text)
    assert len(phases) == 1
    assert phases[0]["number"] == 1
    assert phases[0]["title"] == "Quick wins"


def test_phase_with_em_dash_separator_is_parsed():
    # Em dash (U+2014)
    text = "### Phase 3 \u2014 Some Title\n\nContent."
    phases = parse_phases(text)
    assert len(phases) == 1
    assert phases[0]["title"] == "Some Title"


def test_no_phases_returns_empty_list():
    text = "# Just a plan\n\nNo phase headers here."
    phases = parse_phases(text)
    assert phases == []


def test_multiple_phases_all_with_checkmarks():
    text = textwrap.dedent("""\
        ### Phase 1: Alpha ✅

        Content for 1.

        ### Phase 2: Beta ✅

        Content for 2.
    """)
    phases = parse_phases(text)
    assert len(phases) == 2
    assert all(p["complete"] for p in phases)


def test_multiple_phases_first_complete_second_not():
    text = textwrap.dedent("""\
        ### Phase 1: Alpha ✅

        Content for 1.

        ### Phase 2: Beta (Priority: High)

        Content for 2.
    """)
    phases = parse_phases(text)
    assert phases[0]["complete"] is True
    assert phases[1]["complete"] is False


# ---------------------------------------------------------------------------
# Letter-based phase header parsing (e.g., Phase A, Phase B)
# ---------------------------------------------------------------------------


def test_letter_phase_parsed_correctly():
    text = "### Phase A: Foundation (Tier 1)\n\nSome content."
    phases = parse_phases(text)
    assert len(phases) == 1
    assert phases[0]["number"] == "A"
    assert phases[0]["title"] == "Foundation (Tier 1)"
    assert phases[0]["complete"] is False


def test_letter_phase_with_checkmark_is_complete():
    text = "### Phase B: Core Framework ✅\n\nSome content."
    phases = parse_phases(text)
    assert len(phases) == 1
    assert phases[0]["number"] == "B"
    assert phases[0]["title"] == "Core Framework"
    assert phases[0]["complete"] is True


def test_letter_phases_multiple_with_status_table():
    text = textwrap.dedent("""\
        ### Phase A: Enhanced sync_table (Tier 1)

        | Task | Description | Status |
        |---|---|---|
        | A.1 | Dry-run mode | ✅ Done |
        | A.2 | Drift warnings | ✅ Done |

        ### Phase B: Migration Core (Tier 2)

        | Task | Description | Status |
        |---|---|---|
        | B.1 | Migration base class | ✅ Done |
        | B.2 | File discovery | ✅ Done |

        ### Phase C: Auto-Generation

        | Task | Description | Priority |
        |---|---|---|
        | C.1 | Schema introspection | High |
        | C.2 | Diff engine | High |
    """)
    phases = parse_phases(text)
    assert len(phases) == 3
    assert phases[0]["number"] == "A"
    assert phases[0]["complete"] is True
    assert phases[1]["number"] == "B"
    assert phases[1]["complete"] is True
    assert phases[2]["number"] == "C"
    assert phases[2]["complete"] is False


def test_letter_phases_lowercase_normalized_to_uppercase():
    text = "### Phase a: Some Phase ✅\n\nContent."
    phases = parse_phases(text)
    assert phases[0]["number"] == "A"


# ---------------------------------------------------------------------------
# Task table completion detection
# ---------------------------------------------------------------------------


def test_all_tasks_complete_when_all_have_checkmark():
    content = textwrap.dedent("""\
        **Goal:** Do the thing.

        | Task | Description | Status |
        |---|---|---|
        | 1.1 | First task | ✅ |
        | 1.2 | Second task | ✅ |
    """)
    assert _task_rows_all_complete(content) is True


def test_tasks_incomplete_when_any_lacks_checkmark():
    content = textwrap.dedent("""\
        | Task | Description | Status |
        |---|---|---|
        | 1.1 | First task | ✅ |
        | 1.2 | Second task | ❌ |
    """)
    assert _task_rows_all_complete(content) is False


def test_no_status_column_returns_false():
    content = textwrap.dedent("""\
        | Task | Description |
        |---|---|
        | 1.1 | First task |
        | 1.2 | Second task |
    """)
    assert _task_rows_all_complete(content) is False


def test_phase_complete_via_task_table():
    text = textwrap.dedent("""\
        ### Phase 1: Core Module (Priority: High)

        **Goal:** Build it.

        | Task | Description | Status |
        |---|---|---|
        | 1.1 | Task one | ✅ |
        | 1.2 | Task two | ✅ |
    """)
    phases = parse_phases(text)
    assert phases[0]["complete"] is True


def test_phase_incomplete_via_task_table_mixed():
    text = textwrap.dedent("""\
        ### Phase 1: Core Module (Priority: High)

        | Task | Description | Status |
        |---|---|---|
        | 1.1 | Task one | ✅ |
        | 1.2 | Task two | ❌ |
    """)
    phases = parse_phases(text)
    assert phases[0]["complete"] is False


# ---------------------------------------------------------------------------
# Checkbox completion detection
# ---------------------------------------------------------------------------


def test_checkboxes_all_complete():
    content = "- [x] Task 1\n- [x] Task 2\n- [x] Task 3\n"
    assert _checkboxes_all_complete(content) is True


def test_checkboxes_partially_complete():
    content = "- [x] Task 1\n- [ ] Task 2\n"
    assert _checkboxes_all_complete(content) is False


def test_no_checkboxes_returns_false():
    content = "No checkboxes here."
    assert _checkboxes_all_complete(content) is False


def test_phase_complete_via_checkboxes():
    text = textwrap.dedent("""\
        ### Phase 1: Foundation (Core Docs)

        - [x] README overhaul
        - [x] Installation guide
        - [x] Quickstart guide
    """)
    phases = parse_phases(text)
    assert phases[0]["complete"] is True


def test_phase_incomplete_via_checkboxes_mixed():
    text = textwrap.dedent("""\
        ### Phase 1: Foundation (Core Docs)

        - [x] README overhaul
        - [ ] Installation guide
    """)
    phases = parse_phases(text)
    assert phases[0]["complete"] is False


# ---------------------------------------------------------------------------
# find_next_phase
# ---------------------------------------------------------------------------


def _make_phases(statuses: list[bool]) -> list[dict]:
    return [{"number": i + 1, "title": f"Phase {i + 1}", "complete": s} for i, s in enumerate(statuses)]


def _make_letter_phases(labels: list[str], statuses: list[bool]) -> list[dict]:
    return [{"number": lbl.upper(), "title": f"Phase {lbl}", "complete": s} for lbl, s in zip(labels, statuses)]


def test_find_next_phase_auto_returns_first_incomplete():
    phases = _make_phases([True, True, False, False])
    result = find_next_phase(phases, "auto")
    assert result is not None
    assert result["number"] == 3


def test_find_next_phase_with_completed_number_skips_before():
    phases = _make_phases([True, False, False])
    # completed_phase=1, so skip phase 1; next incomplete is phase 2
    result = find_next_phase(phases, "1")
    assert result is not None
    assert result["number"] == 2


def test_find_next_phase_all_complete_returns_none():
    phases = _make_phases([True, True, True])
    assert find_next_phase(phases, "auto") is None


def test_find_next_phase_empty_phases_returns_none():
    assert find_next_phase([], "auto") is None


def test_find_next_phase_completed_phase_beyond_all_returns_none():
    phases = _make_phases([True, False])
    # completed_phase=5 means skip all phases ≤5; no phases > 5 exist
    result = find_next_phase(phases, "5")
    assert result is None


def test_find_next_phase_letter_completed_skips_before():
    phases = _make_letter_phases(["A", "B", "C"], [True, False, False])
    result = find_next_phase(phases, "A")
    assert result is not None
    assert result["number"] == "B"


def test_find_next_phase_letter_completed_returns_next_incomplete():
    phases = _make_letter_phases(["A", "B", "C", "D"], [True, True, False, False])
    result = find_next_phase(phases, "B")
    assert result is not None
    assert result["number"] == "C"


def test_find_next_phase_letter_beyond_all_returns_none():
    phases = _make_letter_phases(["A", "B"], [True, True])
    result = find_next_phase(phases, "B")
    assert result is None


def test_find_next_phase_unknown_letter_returns_none():
    phases = _make_letter_phases(["A", "B", "C"], [True, False, False])
    # Phase "Z" is not in the list → treated as past the end
    result = find_next_phase(phases, "Z")
    assert result is None


# ---------------------------------------------------------------------------
# all_complete flag
# ---------------------------------------------------------------------------


def test_all_complete_true_when_all_phases_done():
    text = textwrap.dedent("""\
        ### Phase 1: Alpha ✅

        Content.

        ### Phase 2: Beta ✅

        Content.
    """)
    phases = parse_phases(text)
    all_complete = bool(phases) and all(p["complete"] for p in phases)
    assert all_complete is True


def test_all_complete_false_when_any_phase_incomplete():
    text = textwrap.dedent("""\
        ### Phase 1: Alpha ✅

        Content.

        ### Phase 2: Beta (Priority: High)

        Content.
    """)
    phases = parse_phases(text)
    all_complete = bool(phases) and all(p["complete"] for p in phases)
    assert all_complete is False


# ---------------------------------------------------------------------------
# Phase content extraction
# ---------------------------------------------------------------------------


def test_phase_content_is_extracted():
    text = textwrap.dedent("""\
        ### Phase 1: Alpha ✅

        **Goal:** Do something.

        | Task | Description | Status |
        |---|---|---|
        | 1.1 | A task | ✅ |

        ### Phase 2: Beta (Priority: High)

        **Goal:** Do another thing.
    """)
    phases = parse_phases(text)
    assert "Goal: Do something" in phases[0]["content"] or "**Goal:**" in phases[0]["content"]
    assert "| 1.1 |" in phases[0]["content"]
    # Phase 2 content should NOT appear in phase 1's content
    assert "Do another thing" not in phases[0]["content"]


# ---------------------------------------------------------------------------
# Real plan files (integration)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "plan_name,expected_all_complete",
    [
        ("documentation-plan.md", True),
        ("udt-support.md", False),
    ],
)
def test_real_plan_all_complete(plan_name: str, expected_all_complete: bool):
    plan_file = PLANS_DIR / plan_name
    if not plan_file.exists():
        pytest.skip(f"{plan_name} not found")

    data = run_parser(str(plan_file))
    assert data["all_complete"] == expected_all_complete


def test_real_plan_udt_support_has_incomplete_phases():
    plan_file = PLANS_DIR / "udt-support.md"
    if not plan_file.exists():
        pytest.skip("udt-support.md not found")

    data = run_parser(str(plan_file))
    assert data["next_phase"] is not None
    assert data["next_phase"]["number"] == 5
    assert len(data["phases"]) == 7


def test_real_plan_documentation_all_phases_complete_via_checkboxes():
    plan_file = PLANS_DIR / "documentation-plan.md"
    if not plan_file.exists():
        pytest.skip("documentation-plan.md not found")

    data = run_parser(str(plan_file))
    assert data["all_complete"] is True
    assert len(data["phases"]) == 6


def test_plan_file_not_found_returns_nonzero():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--plan-file", "docs/plans/nonexistent.md"],
        capture_output=True,
        check=False,
        text=True,
    )
    assert result.returncode != 0


def test_completed_phase_argument_skips_phases():
    plan_file = PLANS_DIR / "udt-support.md"
    if not plan_file.exists():
        pytest.skip("udt-support.md not found")

    data = run_parser(str(plan_file), completed_phase="2")
    # Phases 1–2 are skipped by caller; phases 3 and 4 are marked ✅ in the
    # plan, so the first incomplete phase after phase 2 is phase 5.
    assert data["next_phase"] is not None
    assert data["next_phase"]["number"] == 5


def test_real_plan_migration_strategy_letter_phases():
    plan_file = PLANS_DIR / "migration-strategy.md"
    if not plan_file.exists():
        pytest.skip("migration-strategy.md not found")

    data = run_parser(str(plan_file))
    # Phases A and B have all Status=✅ Done rows → detected as complete
    assert len(data["phases"]) == 4
    assert data["phases"][0]["number"] == "A"
    assert data["phases"][0]["complete"] is True
    assert data["phases"][1]["number"] == "B"
    assert data["phases"][1]["complete"] is True
    assert data["phases"][2]["number"] == "C"
    assert data["phases"][2]["complete"] is False
    # Next phase to delegate is Phase C
    assert data["next_phase"] is not None
    assert data["next_phase"]["number"] == "C"
    assert data["all_complete"] is False


def test_real_plan_migration_strategy_letter_completed_phase_arg():
    plan_file = PLANS_DIR / "migration-strategy.md"
    if not plan_file.exists():
        pytest.skip("migration-strategy.md not found")

    data = run_parser(str(plan_file), completed_phase="B")
    # Caller says Phase B is done; next incomplete phase should be C (D is already done)
    assert data["next_phase"] is not None
    assert data["next_phase"]["number"] == "C"
