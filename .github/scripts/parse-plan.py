#!/usr/bin/env python3
"""parse-plan.py — Parse a plan markdown file and output phase structure as JSON.

Usage:
    python .github/scripts/parse-plan.py --plan-file docs/plans/udt-support.md
    python .github/scripts/parse-plan.py --plan-file docs/plans/udt-support.md --completed-phase 2

Output JSON:
    {
        "phases": [
            {
                "number": 1,
                "title": "Core Workflow Scaffold",
                "complete": true
            },
            ...
        ],
        "next_phase": {
            "number": 2,
            "title": "...",
            "content": "..."
        },
        "all_complete": false,
        "completed_phase": 1
    }
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Matches: ### Phase N: Title, ### Phase N — Title, ### Phase N – Title
# Also matches letter phases: ### Phase A: Title, ### Phase B — Title, etc.
# The title may contain ✅ at the end if the phase is marked complete.
PHASE_HEADER_RE = re.compile(
    r"^### Phase (\d+|[A-Za-z])\s*(?:[:\u2014\u2013\-]\s*)?(.+?)\s*$",
    re.MULTILINE,
)

CHECKMARK = "\u2705"  # ✅


def _strip_code_blocks(text: str) -> str:
    """Remove fenced code block content to avoid false matches."""
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def _task_rows_all_complete(content: str) -> bool:
    """Return True if a Status-column table exists and all task rows contain ✅."""
    lines = content.splitlines()
    in_table = False
    has_status_col = False
    status_col_idx = -1
    task_rows: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_table = False
            has_status_col = False
            status_col_idx = -1
            continue

        # Split inner cells (strip leading/trailing empty cells from | delimiters)
        parts = [p.strip() for p in stripped.split("|")[1:-1]]
        if not parts:
            continue

        # Detect table header row (contains a "status" column)
        lower_parts = [p.lower() for p in parts]
        if not in_table and ("status" in lower_parts or "check" in lower_parts):
            in_table = True
            has_status_col = True
            for i, h in enumerate(lower_parts):
                if h in ("status", "check"):
                    status_col_idx = i
                    break
            continue

        # Skip separator rows (e.g. |---|---|---|)
        if all(re.match(r"^[-:]+$", p) for p in parts if p):
            continue

        # Collect status cell from task data rows
        if in_table and has_status_col and status_col_idx >= 0 and status_col_idx < len(parts):
            task_rows.append(parts[status_col_idx])

    if not task_rows:
        return False
    return all(CHECKMARK in cell for cell in task_rows)


def _checkboxes_all_complete(content: str) -> bool:
    """Return True if the content has checkboxes and all are checked [x].

    Only matches actual list checkboxes at the start of a line (optionally
    indented), not checkbox syntax inside code spans or table cells.
    """
    checkboxes = re.findall(r"^[ \t]*-[ \t]+\[(.)\]", content, re.MULTILINE)
    if not checkboxes:
        return False
    return all(c.lower() == "x" for c in checkboxes)


def _is_phase_complete(header_line: str, content: str) -> bool:
    """Determine whether a phase is complete.

    Priority order:
    1. ✅ in the phase header line → complete
    2. All task rows in a Status-column table contain ✅ → complete
    3. All checkboxes in the content are [x] → complete
    4. Otherwise → incomplete
    """
    if CHECKMARK in header_line:
        return True
    if _task_rows_all_complete(content):
        return True
    return bool(_checkboxes_all_complete(content))


def parse_phases(text: str) -> list[dict]:
    """Parse all phases from plan markdown text.

    Returns a list of phase dicts with keys: number, title, complete, content.
    """
    phases = []
    # Strip fenced code blocks before matching phase headers to avoid
    # picking up example phase headers inside code fences.
    stripped = _strip_code_blocks(text)
    matches = list(PHASE_HEADER_RE.finditer(stripped))

    for i, match in enumerate(matches):
        raw_number = match.group(1)
        number: int | str = int(raw_number) if raw_number.isdigit() else raw_number.upper()
        raw_title = match.group(2).strip()
        # Remove status markers from the title for display
        clean_title = raw_title.replace(CHECKMARK, "").strip()

        # Content: from end of this header line to start of next phase header.
        # Use the original (un-stripped) text so code blocks are included in
        # the content sent to the delegation prompt.
        content_start = match.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(stripped)
        content = stripped[content_start:content_end].strip()

        complete = _is_phase_complete(match.group(0), content)

        phases.append(
            {
                "number": number,
                "title": clean_title,
                "complete": complete,
                "content": content,
            }
        )

    return phases


def find_next_phase(phases: list[dict], completed_phase: str) -> dict | None:
    """Find the next incomplete phase.

    If completed_phase is a digit string or a single letter, find that phase
    in the list by its number/label and return the first incomplete phase after
    it.  If the completed phase is not found and completed_phase is a digit,
    fall back to numeric comparison (p["number"] > completed_phase_int) so that
    specifying a phase number higher than any in the list returns None.
    If completed_phase is "auto" or empty, return the first incomplete phase
    overall.
    """
    if completed_phase and completed_phase != "auto":
        comp_val: int | str = int(completed_phase) if completed_phase.isdigit() else completed_phase.upper()
        comp_idx = next((i for i, p in enumerate(phases) if p["number"] == comp_val), -1)
        if comp_idx >= 0:
            # Found the completed phase: look for incomplete phases after it.
            candidates = [p for p in phases[comp_idx + 1 :] if not p["complete"]]
        elif completed_phase.isdigit():
            # Phase number not found; fall back to numeric comparison so that
            # a completed_phase value beyond the last phase returns None.
            min_number = int(completed_phase) + 1
            candidates = [
                p for p in phases if isinstance(p["number"], int) and p["number"] >= min_number and not p["complete"]
            ]
        else:
            # Letter phase not found → treat as past the end of the plan.
            candidates = []
    else:
        candidates = [p for p in phases if not p["complete"]]
    return candidates[0] if candidates else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a plan markdown file and output JSON phase structure.")
    parser.add_argument("--plan-file", required=True, help="Path to the plan markdown file")
    parser.add_argument(
        "--completed-phase",
        default="auto",
        help='Completed phase number (integer) or "auto" to detect from plan (default: auto)',
    )
    args = parser.parse_args()

    plan_path = Path(args.plan_file)
    if not plan_path.exists():
        print(json.dumps({"error": f"Plan file not found: {args.plan_file}"}), flush=True)
        sys.exit(1)

    text = plan_path.read_text(encoding="utf-8")
    phases = parse_phases(text)
    next_phase = find_next_phase(phases, args.completed_phase)
    all_complete = bool(phases) and all(p["complete"] for p in phases)

    # Determine the output completed_phase value
    if args.completed_phase.isdigit():
        completed_phase_out: int | str = int(args.completed_phase)
    elif args.completed_phase != "auto":
        # Letter-based completed phase (e.g. "A", "B")
        completed_phase_out = args.completed_phase.upper()
    elif phases:
        completed_phase_nums = [p["number"] for p in phases if p["complete"]]
        completed_phase_out = max(completed_phase_nums) if completed_phase_nums else 0
    else:
        completed_phase_out = 0

    result = {
        "phases": [
            {
                "number": p["number"],
                "title": p["title"],
                "complete": p["complete"],
            }
            for p in phases
        ],
        "next_phase": (
            {
                "number": next_phase["number"],
                "title": next_phase["title"],
                "content": next_phase["content"],
            }
            if next_phase
            else None
        ),
        "all_complete": all_complete,
        "completed_phase": completed_phase_out,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
