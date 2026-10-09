"""pytest-bats plugin — collect and run .bats files as pytest items."""

from __future__ import annotations

import re
import shutil
import subprocess

import pytest


def pytest_collect_file(parent, file_path):
    """Collect .bats files as pytest test modules."""
    if file_path.suffix == ".bats" and file_path.name.startswith("test_"):
        return BatsFile.from_parent(parent, path=file_path)


class BatsFile(pytest.File):
    """A .bats file containing one or more @test blocks."""

    def collect(self):
        content = self.path.read_text(encoding="utf-8")
        tests_found = False
        for match in re.finditer(r"@test\s+\"([^\"]+)\"", content):
            tests_found = True
            name = match.group(1)
            yield BatsItem.from_parent(self, name=name)
        # If no @test blocks found, treat the whole file as one item
        if not tests_found:
            yield BatsItem.from_parent(self, name=self.path.stem)


class BatsItem(pytest.Item):
    """A single @test case from a .bats file."""

    def runtest(self):
        if not shutil.which("bats"):
            pytest.skip("bats is not installed")
        result = subprocess.run(
            ["bats", "--filter", re.escape(self.name), str(self.path)],
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            raise BatsTestFailure(result.stdout, result.stderr)

    def repr_failure(self, excinfo, style=None):
        if isinstance(excinfo.value, BatsTestFailure):
            return f"Bats test failed: {self.name}\n{excinfo.value}"
        return super().repr_failure(excinfo, style)

    def reportinfo(self):
        return self.path, None, f"bats: {self.name}"


class BatsTestFailure(Exception):
    """Raised when a bats test case fails."""

    def __init__(self, stdout: str, stderr: str):
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        parts = []
        if self.stdout.strip():
            parts.append(f"stdout:\n{self.stdout}")
        if self.stderr.strip():
            parts.append(f"stderr:\n{self.stderr}")
        return "\n".join(parts) or "(no output)"
