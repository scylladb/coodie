"""Smoke test for the argus-tracker demo.

Runs ``seed.py --users 2 --runs 5 --events 10`` and verifies:
  - exit code is 0
  - stdout mentions the expected model names

Usage:
    python smoke_test.py
"""

from __future__ import annotations

import subprocess
import sys


def main() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "seed.py",
            "--users",
            "2",
            "--runs",
            "5",
            "--events",
            "10",
            "--no-interactive",
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"seed.py exited with {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    for expected in ["User", "TestRun", "Event", "Notification", "PANOPTICON PROTOCOL"]:
        assert expected in result.stdout, f"Expected '{expected}' in output:\n{result.stdout}"
    print("  ✓ All checks passed — ARGUS-PRIME is satisfied")


if __name__ == "__main__":
    main()
