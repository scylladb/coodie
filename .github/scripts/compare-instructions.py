"""Compare per-benchmark instruction counts from two callgrind output dirs.

pytest-codspeed, run under ``valgrind --tool=callgrind --instr-atstart=no``
with ``CODSPEED_ENV`` set, dumps one callgrind file per benchmark, named by
its ``desc: Trigger: Client Request: <test uri>`` line.

Usage: compare-instructions.py BASE_DIR HEAD_DIR [--fail-pct N]
Prints a Markdown table; exits 1 if any benchmark grew by more than N%.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TRIGGER_RE = re.compile(r"^desc: Trigger: Client Request: (.+::.+)$", re.MULTILINE)
TOTALS_RE = re.compile(r"^totals: (\d+)$", re.MULTILINE)


def read_counts(out_dir: Path) -> dict[str, int]:
    counts = {}
    for f in out_dir.glob("cg.*"):
        text = f.read_text()
        trigger, totals = TRIGGER_RE.search(text), TOTALS_RE.search(text)
        if trigger and totals:
            counts[trigger.group(1)] = int(totals.group(1))
    return counts


def compare(base: dict[str, int], head: dict[str, int], fail_pct: float) -> tuple[str, bool]:
    rows = ["| Benchmark | base | PR | change |", "|---|---:|---:|---:|"]
    failed = False
    for name in sorted(base.keys() | head.keys()):
        b, h = base.get(name), head.get(name)
        if b is None or h is None:
            rows.append(f"| `{name}` | {b or '—'} | {h or '—'} | new/removed |")
            continue
        pct = (h - b) / b * 100
        mark = ""
        if pct > fail_pct:
            failed, mark = True, " 🔴"
        elif pct < -fail_pct:
            mark = " 🟢"
        rows.append(f"| `{name}` | {b:,} | {h:,} | {pct:+.1f}%{mark} |")
    return "\n".join(rows), failed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=Path)
    parser.add_argument("head_dir", type=Path)
    parser.add_argument("--fail-pct", type=float, default=5.0)
    args = parser.parse_args()
    base, head = read_counts(args.base_dir), read_counts(args.head_dir)
    if not base or not head:
        print(f"No callgrind results found (base: {len(base)}, PR: {len(head)})")
        return 1
    table, failed = compare(base, head, args.fail_pct)
    print(f"### Instruction counts (CPU instructions per call, fail above +{args.fail_pct:g}%)\n\n{table}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
