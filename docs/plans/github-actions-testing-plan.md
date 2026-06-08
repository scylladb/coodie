# GitHub Actions Workflow Testing Plan

> **Goal:** Introduce automated testing for the repository's GitHub Actions
> workflows so that YAML misconfigurations, shell-script logic errors, and
> workflow-integration regressions are caught before they reach the default
> branch. The plan compares every viable tool — `act` CLI, `actionlint`,
> Bats, Python/pytest-based options, and GitHub's Local Action Debugger —
> recommends a layered testing strategy, and provides a phased rollout.

---

## Table of Contents

1. [Current State](#1-current-state)
   - [1.1 Workflow Inventory](#11-workflow-inventory)
   - [1.2 Complexity Assessment](#12-complexity-assessment)
2. [Tool Comparison](#2-tool-comparison)
   - [2.1 actionlint — Static Analysis](#21-actionlint--static-analysis)
   - [2.2 act CLI — Local Workflow Runner](#22-act-cli--local-workflow-runner)
   - [2.3 Bats — Shell Script Unit Testing](#23-bats--shell-script-unit-testing)
   - [2.4 Python / pytest — YAML Validation & Script Testing](#24-python--pytest--yaml-validation--script-testing)
   - [2.5 GitHub Local Action Debugger](#25-github-local-action-debugger)
   - [2.6 workflow_dispatch — Live Smoke Tests](#26-workflow_dispatch--live-smoke-tests)
   - [2.7 Comparison Matrix](#27-comparison-matrix)
3. [Recommended Strategy](#3-recommended-strategy)
4. [Implementation Phases](#4-implementation-phases)
5. [Test Plan](#5-test-plan)
   - [5.1 Static Analysis (actionlint)](#51-static-analysis-actionlint)
   - [5.2 Shell Script Unit Tests (Bats)](#52-shell-script-unit-tests-bats)
   - [5.3 YAML Validation (pytest)](#53-yaml-validation-pytest)
   - [5.4 Live Smoke Tests (workflow_dispatch)](#54-live-smoke-tests-workflow_dispatch)
6. [References](#6-references)

---

## 1. Current State

### 1.1 Workflow Inventory

The repository has 11 GitHub Actions workflow files:

| # | Workflow | File | Trigger(s) | Lines |
|---|---------|------|-----------|-------|
| 1 | CI | `ci.yml` | `push`, `pull_request` | 61 |
| 2 | Unit Tests | `test-unit.yml` | `push`, `pull_request` | 44 |
| 3 | Integration Tests | `test-integration.yml` | `push`, `pull_request` | 52 |
| 4 | Benchmarks | `benchmark.yml` | `push`, `pull_request`, `schedule` | 90 |
| 5 | Docs | `docs.yml` | `push` (master) | 66 |
| 6 | Publish | `publish.yml` | `push` (tags) | 41 |
| 7 | Labels | `labels.yml` | `push` (master, `.github/labels.toml`) | 22 |
| 8 | Issue Manager | `issue-manager.yml` | `issue_comment`, `schedule` | 32 |

**There is no automated testing of any workflow file today.** The only
validation is GitHub's built-in YAML parsing on push and manual smoke
testing.

### 1.2 Complexity Assessment

Legend:
- 🔴 **High** — multi-step shell scripting, conditional logic, API calls
- 🟡 **Medium** — matrix strategies, artifacts, conditional steps
- 🟢 **Low** — simple trigger → single job → marketplace action

| Workflow | Complexity | Testable Shell Logic | Key Risks |
|---------|:----------:|:--------------------:|-----------|
| Self-Healing CI (removed) | 🔴 | Yes (3 shell steps) | Log collection loops, PR comment construction, `workflow_run` trigger |
| Benchmarks | 🟡 | Minimal | Matrix strategy, artifact management, gh-pages deploy |
| Integration Tests | 🟡 | Minimal | Matrix with driver exclusions, service containers |
| Unit Tests | 🟡 | Minimal | Matrix (3 Python versions × 3 OSes) |
| CI | 🟡 | Minimal | Pre-commit, commitlint, semantic-release chain |
| Docs | 🟢 | No | Sphinx build, GitHub Pages deploy |
| Publish | 🟢 | No | PyPI OIDC, artifact upload |
| Labels | 🟢 | No | Single marketplace action |
| Issue Manager | 🟢 | No | Single marketplace action |

---

## 2. Tool Comparison

### 2.1 actionlint — Static Analysis

[actionlint](https://github.com/rhysd/actionlint) is a Go-based static
checker purpose-built for GitHub Actions workflow YAML files.

**What it catches:**
- Invalid YAML structure and unknown workflow keys
- Type errors in `${{ }}` expressions (e.g., accessing `.foo` on a string)
- Unknown action inputs/outputs and missing `required` inputs
- Insecure patterns (untrusted input in `run:` steps)
- Invalid glob patterns, runner labels, and cron expressions
- Shell syntax errors (integrates with `shellcheck`)
- Python syntax errors in `run:` steps (integrates with `pyflakes`)

**Pros:**
- Zero configuration — just run `actionlint` at repo root
- Extremely fast (<1 s for all 11 workflow files)
- Catches the most common workflow errors before push
- Integrates with pre-commit, VS Code, and CI
- No Docker dependency — single static binary

**Cons:**
- Static analysis only — cannot test runtime behavior
- Cannot simulate event payloads or step outputs
- False positives on complex expression patterns (rare)

**Applicability to coodie:** ✅ High — catches YAML and expression errors
across all 11 workflows. Best bang-for-buck as a first step.

### 2.2 act CLI — Local Workflow Runner

[act](https://github.com/nektos/act) is a Go-based CLI that runs GitHub
Actions workflows locally inside Docker containers, simulating the runner
environment.

**What it tests:**
- Full workflow execution with real steps, containers, and artifacts
- Matrix strategies and job dependencies
- Environment variables, secrets (from `.secrets` file), and outputs
- Supports custom event payloads via JSON files (`-e event.json`)

**Pros:**
- Closest to real GitHub Actions behavior without pushing
- Tests the complete orchestration: triggers → jobs → steps → outputs
- Supports most triggers including `push`, `pull_request`, `issue_comment`
- Avoids burning GitHub Actions minutes during development

**Cons:**
- **Requires Docker** — adds CI complexity and ~2 GB image pulls
- **Not 100% fidelity** — some GitHub-specific features are missing:
  - `GITHUB_TOKEN` permissions model is simplified
  - `workflow_run` and `workflow_call` triggers have limited support
  - Marketplace actions with Docker-in-Docker can fail
  - `gh` CLI authentication behaves differently
- **Slow** — each run starts a Docker container (~10-30 s overhead)
- **Event simulation is fragile** — complex events like `issue_comment`
  require hand-crafted JSON payloads that drift from GitHub's actual schema
**Applicability to coodie:** 🔧 Medium — useful for testing simple
workflows (`test-unit.yml`, `ci.yml`) but impractical for complex
workflows that rely on real GitHub API state.

### 2.3 Bats — Shell Script Unit Testing

[Bats](https://github.com/bats-core/bats-core) (Bash Automated Testing
System) is a TAP-compliant testing framework for Bash scripts.

**What it tests:**
- Individual shell functions and scripts extracted from `run:` steps
- Exit codes, stdout/stderr output, and side effects
- Can mock commands (e.g., mock `gh`, `git`, `copilot`) to test logic paths

**Pros:**
- Tests the actual shell logic that is hardest to debug in CI
- Fast — no Docker, no containers, sub-second execution
- Mature ecosystem: `bats-support`, `bats-assert`, `bats-mock` libraries
- Perfect for testing command parsing, permission checks, and fallback logic

**Cons:**
- Requires extracting shell logic from inline `run:` blocks into standalone
  scripts (one-time refactor)
- Tests Bash scripts, not the workflow YAML orchestration itself
- Cannot test GitHub-specific context variables (`${{ github.event.* }}`)
  without mocking

**Applicability to coodie:** ✅ High — workflows with complex shell logic
benefit from extracting steps into testable scripts and testing with Bats
for the highest confidence in the most complex logic.

### 2.4 Python / pytest — YAML Validation & Script Testing

Python and pytest can be used to validate workflow YAML structure and test
helper scripts.

**What it tests:**
- YAML schema validation (are required keys present? are values valid?)
- Cross-workflow consistency (do all workflows use the same checkout action
  version? do all set `cancel-in-progress`?)
- Custom Python scripts called by workflows (if any)

**Available libraries:**
- `pyyaml` / `ruamel.yaml` — parse workflow YAML files
- `jsonschema` — validate against the official GitHub Actions JSON schema
- `pytest` — test framework for assertions
- `subprocess` — call shell scripts and assert on output

**Pros:**
- Leverages the project's existing pytest infrastructure
- Can enforce repository-specific conventions (e.g., "all workflows must
  have a concurrency group," "all checkout actions must use `@v4`")
- Very fast — YAML parsing is near-instant
- No external tool installation — pure Python

**Cons:**
- Does not validate GitHub Actions semantics (expressions, action inputs) —
  `actionlint` is strictly better for that
- Cannot test runtime workflow behavior
- Writing a full schema validator from scratch is wasted effort when
  `actionlint` already does it

**Applicability to coodie:** 🔧 Medium — useful as a complementary layer
for enforcing project-specific conventions that `actionlint` cannot check.
Should not replace `actionlint` for semantic validation.

### 2.5 GitHub Local Action Debugger

[`@github/local-action`](https://github.com/github/local-action) is
GitHub's official tool for locally testing JavaScript/TypeScript custom
Actions.

**Pros:**
- No Docker required — runs with `npx`
- Official, maintained by GitHub

**Cons:**
- **Only works for JS/TS custom Actions** — not for workflow YAML files
- Cannot test `run:` shell steps or composite actions
- Coodie does not have any custom JS/TS Actions

**Applicability to coodie:** ❌ Not applicable — the repository does not
define any custom JavaScript or TypeScript Actions.

### 2.6 workflow_dispatch — Live Smoke Tests

Some workflows support `workflow_dispatch` triggers, enabling
manual testing from the Actions tab.

**What it tests:**
- Full end-to-end behavior in the real GitHub environment
- Real API calls, real `GITHUB_TOKEN`, real PR state

**Pros:**
- Tests the actual production environment — 100% fidelity
- Can be automated via `gh workflow run` in a dedicated test workflow

**Cons:**
- Requires a real PR in the repository
- Consumes GitHub Actions minutes
- Slower than local testing (~30-60 s per run)
- Side effects (pushes force-with-lease, posts comments) require cleanup

**Applicability to coodie:** ✅ High — can be extended to workflows
that support `workflow_dispatch`. Best used as a final validation step,
not for rapid iteration.

### 2.7 Comparison Matrix

| Criterion | actionlint | act CLI | Bats | Python/pytest | Local Action Debugger | workflow_dispatch |
|-----------|:----------:|:-------:|:----:|:-------------:|:---------------------:|:-----------------:|
| **Tests YAML structure** | ✅ | — | — | 🔧 | — | — |
| **Tests expressions** | ✅ | ✅ | — | — | — | ✅ |
| **Tests shell logic** | 🔧 shellcheck | ✅ | ✅ | 🔧 subprocess | — | ✅ |
| **Tests orchestration** | — | ✅ | — | — | — | ✅ |
| **Tests with real GitHub API** | — | — | — | — | — | ✅ |
| **No Docker required** | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Fast feedback (<5 s)** | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Pre-commit compatible** | ✅ | — | ✅ | ✅ | — | — |
| **CI integration** | ✅ | 🔧 | ✅ | ✅ | — | ✅ |
| **Applicable to coodie** | ✅ | 🔧 | ✅ | 🔧 | ❌ | ✅ |

---

## 3. Recommended Strategy

Based on the comparison, the recommended approach is a **three-layer
testing pyramid** for workflows:

```
                  ┌──────────────────────┐
                  │  Live Smoke Tests    │  ← workflow_dispatch on real PRs
                  │  (few, slow, high    │     final validation before merge
                  │   fidelity)          │
                  └──────────┬───────────┘
                             │
                ┌────────────┴────────────┐
                │  Shell Script Unit      │  ← Bats tests for extracted scripts
                │  Tests (many, fast,     │     command parsing, git logic,
                │  focused on logic)      │     fallback paths
                └────────────┬────────────┘
                             │
          ┌──────────────────┴──────────────────┐
          │  Static Analysis + Convention       │  ← actionlint + pytest YAML checks
          │  Checks (all files, instant,        │     run on every PR, pre-commit
          │  catches misconfigurations)          │
          └─────────────────────────────────────┘
```

**Why not `act` CLI as the primary tool?**

While `act` is the most well-known workflow testing tool, it is
**not the best fit** for coodie's most complex workflows:

1. The Docker overhead (~10-30 s startup + ~2 GB image) is disproportionate
   for what are essentially Bash scripts with `gh` CLI calls.
3. The shell logic is better tested by extracting it into scripts and
   using Bats — this is faster, more targeted, and gives clearer
   failure messages.

`act` remains useful for *quick local validation of simple workflows*
(e.g., "does `test-unit.yml` matrix work?"), but it should not be the
primary testing mechanism. Developers can install it optionally.

---

## 4. Implementation Phases

### Phase 1: Static Analysis with actionlint (Priority: High) ✅

**Goal:** Add actionlint to pre-commit and CI so every PR is validated for YAML and expression errors.

| Task | Description |
|---|---|
| 1.1 | Add `actionlint` hook to `.pre-commit-config.yaml` using the [`rhysd/actionlint`](https://github.com/rhysd/actionlint/blob/main/docs/usage.md#pre-commit) pre-commit hook |
| 1.2 | Run `actionlint` locally against all 11 workflows and fix any reported errors |
| 1.3 | Add an `actionlint` step to `ci.yml` (or a new `lint-workflows.yml`) that runs on PRs touching `.github/workflows/` |
| 1.4 | Document actionlint usage in `CONTRIBUTING.md` |
| 1.5 | Verify: `actionlint` passes cleanly on all 11 workflows in CI |

### Phase 2: Shell Script Extraction & Bats Tests (Priority: High) ✅

**Goal:** Extract the complex shell logic from workflows into standalone scripts, test them with Bats, and integrate Bats into the existing pytest suite via a custom pytest plugin.

| Task | Description |
|---|---|
| 2.1 | Create `.github/scripts/` directory for extracted shell scripts |
| 2.2 | Extract complex shell steps from workflows into standalone scripts |
| 2.5 | Update workflow YAML files to source the extracted scripts instead of inline shell |
| 2.6 | Create `tests/workflows/` directory for Bats test files |
| 2.10 | Create `tests/workflows/conftest.py` — a pytest-bats plugin that collects `.bats` files as pytest items, parses individual `@test` blocks, and runs them via `bats`, reporting pass/fail per test case (see [§2.10 Plugin Design](#210-plugin-design) below) |
| 2.11 | Add a CI job that installs `bats-core` and runs all Bats tests via `pytest tests/workflows/` on PRs touching `.github/` |
| 2.12 | Verify: all Bats tests pass locally and in CI via both `bats` directly and `pytest tests/workflows/` |

#### 2.10 Plugin Design

A custom pytest-bats conftest plugin in `tests/workflows/conftest.py`
lets developers run Bats tests with the standard `pytest` command,
getting unified reporting, familiar CLI flags (`-v`, `-k`, `--tb`), and
integration with the existing CI pipeline without a separate Bats job.

```python
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
        # Parse @test "name" { ... } blocks from the file
        content = self.path.read_text()
        for match in re.finditer(r"@test\s+\"([^\"]+)\"", content):
            name = match.group(1)
            yield BatsItem.from_parent(self, name=name)
        # If no @test blocks found, treat the whole file as one item
        if not list(re.finditer(r"@test\s+\"([^\"]+)\"", content)):
            yield BatsItem.from_parent(self, name=self.path.stem)


class BatsItem(pytest.Item):
    """A single @test case from a .bats file."""

    def runtest(self):
        if not shutil.which("bats"):
            pytest.skip("bats is not installed")
        result = subprocess.run(
            ["bats", "--filter", re.escape(self.name), str(self.path)],
            capture_output=True,
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
```

**Key design decisions:**
- **Individual test granularity:** Parses `@test "name"` blocks so each
  Bats test case appears as a separate pytest item (pass/fail/skip per case)
- **`--filter` flag:** Runs only the matching `@test` block per item, so
  failure isolation is accurate
- **`shutil.which("bats")` guard:** Skips gracefully when `bats` is not
  installed (developer machines without it, or CI without the install step)
- **30 s timeout:** Prevents runaway shell scripts from hanging CI
- **Custom `repr_failure`:** Shows Bats stdout/stderr inline in pytest
  output for easy debugging

### Phase 3: Python Convention Checks (Priority: Medium) ✅

**Goal:** Add pytest-based checks that enforce repository-specific workflow conventions that actionlint cannot verify.

| Task | Description |
|---|---|
| 3.1 | Create `tests/test_workflow_conventions.py` |
| 3.2 | Test: all workflows use `actions/checkout@v4` (not `@v3` or unpinned) |
| 3.3 | Test: all multi-job workflows define a `concurrency` group |
| 3.4 | Test: all workflows that use `gh` CLI set `GH_TOKEN` env var |
| 3.5 | Test: no workflow uses `actions/checkout` with `fetch-depth: 1` when `git log`, `git merge-base`, or `git merge` is used in a later step |
| 3.6 | Test: all `schedule` triggers have valid cron expressions |
| 3.7 | Run as part of the existing `pytest` unit test suite (no new CI job needed) |
| 3.8 | Verify: all convention tests pass |

### Phase 4: workflow_dispatch Smoke Tests (Priority: Low)

**Goal:** Document and optionally automate live smoke tests for workflows using `workflow_dispatch` triggers.

| Task | Description |
|---|---|
| 4.1 | Document the manual smoke-test procedure in `CONTRIBUTING.md`: how to trigger via Actions tab, expected results, cleanup steps |
| 4.2 | Create a test PR template (branch `test/workflow-smoke`) with known state for reproducible testing |
| 4.4 | Verify: manual smoke tests pass |

---

## 5. Test Plan

### 5.1 Static Analysis (actionlint)

| Test Case | Phase |
|---|---|
| All 11 workflow files pass `actionlint` with zero errors | 1 |
| Pre-commit hook catches a deliberately introduced YAML error | 1 |
| CI job fails when a PR introduces an invalid workflow expression | 1 |

### 5.2 Shell Script Unit Tests (Bats)

#### `tests/workflows/test_collect_failed_logs.bats`

| Test Case | Phase |
|---|---|
| No failed jobs → empty output | 2 |
| One failed job → logs collected with job name header | 2 |
| Multiple failed jobs → all logs concatenated | 2 |
| API call fails → graceful error handling | 2 |

### 5.3 YAML Validation (pytest)

#### `tests/test_workflow_conventions.py`

| Test Case | Phase |
|---|---|
| All workflows use pinned action versions (`@vN` or `@sha`) | 3 |
| All multi-job workflows have `concurrency` groups | 3 |
| All `run:` steps using `gh` CLI have `GH_TOKEN` in `env:` | 3 |
| All workflows with `git log`, `git merge-base`, or `git merge` use `fetch-depth: 0` | 3 |
| All `schedule` cron expressions are syntactically valid | 3 |

### 5.4 Live Smoke Tests (workflow_dispatch)

| Test Case | Phase |
|---|---|
| Trigger on closed PR → workflow exits with "not open" error | 4 |

---

## 6. References

- [actionlint — Static checker for GitHub Actions](https://github.com/rhysd/actionlint)
- [actionlint pre-commit hook](https://github.com/rhysd/actionlint/blob/main/docs/usage.md#pre-commit)
- [nektos/act — Run GitHub Actions locally](https://github.com/nektos/act)
- [Bats — Bash Automated Testing System](https://github.com/bats-core/bats-core)
- [`@github/local-action` — Local Action Debugger](https://github.com/github/local-action)
- [GitHub Actions workflow syntax reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
