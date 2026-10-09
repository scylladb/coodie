"""Smoke test for the batch-importer demo.

Runs ``seed.py --count 10`` and verifies:
  - exit code is 0
  - stdout reports the expected import count

Usage:
    python smoke_test.py
"""

from __future__ import annotations

import subprocess
import sys


def main() -> None:
    result = subprocess.run(
        [sys.executable, "seed.py", "--count", "10"],
        capture_output=True,
        check=False,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"seed.py exited with {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "10" in result.stdout, f"Expected entry count '10' in output:\n{result.stdout}"
    print("  ✓ All checks passed")


if __name__ == "__main__":
    main()
