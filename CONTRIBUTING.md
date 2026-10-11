# Contributing

Contributions are welcome, and they are greatly appreciated! Every little helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs to [our issue page][gh-issues]. If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

coodie could always use more documentation, whether as part of the official coodie docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback [our issue page][gh-issues] on GitHub. If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome 😊

## Get Started!

Ready to contribute? Here's how to set yourself up for local development.

### Prerequisites

- **Python 3.10+**
- **[uv](https://github.com/astral-sh/uv)** (recommended) or pip
- **Docker** (for integration tests)

### Quick Setup

```bash
# Fork & clone
git clone git@github.com:your_name_here/coodie.git
cd coodie

# Install dependencies with uv (recommended)
uv sync --all-extras

# Install bats for workflow shell script tests (optional)
# macOS:  brew install bats-core
# Ubuntu: sudo apt-get install bats
# Or from source: https://bats-core.readthedocs.io/en/stable/installation.html

# Or with pip
pip install -e ".[scylla]"
pip install pytest pytest-cov pytest-asyncio pre-commit

# Install pre-commit hooks
uv run pre-commit install

# Run unit tests (no database needed)
uv run pytest tests/ -v

# Run linters
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/

# Lint GitHub Actions workflows
# (requires actionlint: https://github.com/rhysd/actionlint)
actionlint

# Or run all pre-commit hooks at once (includes actionlint)
uv run pre-commit run --all-files
```

### Running Integration Tests

Integration tests need a running ScyllaDB instance. The test suite uses
[testcontainers](https://github.com/testcontainers/testcontainers-python)
to start one automatically:

```bash
# Run integration tests (starts ScyllaDB via Docker)
uv run pytest tests/ -v -m integration
```

### Creating a Branch

```bash
git checkout -b name-of-your-bugfix-or-feature
```

Now you can make your changes locally.

### Committing

Commit messages must follow [Conventional Commits](https://www.conventionalcommits.org):

```bash
git add .
git commit -m "feat(something): your detailed description of your changes"
git push origin name-of-your-bugfix-or-feature
```

Examples:

- `feat(aio): add TTL support to Document.save()`
- `fix(cql_builder): escape column names with reserved words`
- `docs: update quickstart guide`
- `test(sync): add QuerySet chaining coverage`

We run [`commitlint` on CI](https://github.com/marketplace/actions/commit-linter) to validate commit messages. If you've installed pre-commit hooks, the message will be checked at commit time.

### Submitting a Pull Request

Submit a pull request through the GitHub website or using the GitHub CLI:

```bash
gh pr create --fill
```

## Pull Request Guidelines

We like to have the pull request open as soon as possible, that's a great place to discuss any piece of work, even unfinished. You can use draft pull request if it's still a work in progress. Here are a few guidelines to follow:

1. Include tests for feature or bug fixes.
2. Update the documentation for significant features.
3. Ensure tests are passing on CI.

### Plan-Linking Convention

If your PR implements a phase of a multi-phase plan in `docs/plans/`, you can
link the PR to the plan so the **Plan Phase Continuation** workflow automatically
delegates the next phase to Copilot after merge.

Add one or both of these lines to your PR body:

```
Plan: docs/plans/<plan-name>.md
Phase: N
```

- **`Plan:`** — path to the plan file (case-insensitive, relative to repo root)
- **`Phase:`** — the phase number this PR completes (optional; if omitted the
  workflow detects the completed phase from the plan's own ✅ markers)

**Example PR body:**

```
Implements phase 2 of the UDT support plan.

Plan: docs/plans/udt-support.md
Phase: 2
```

As a fallback the workflow also detects the plan from the **branch name** if
it follows the convention `plan/<plan-name>/phase-N`
(e.g. `plan/udt-support/phase-2`).

When a PR **introduces a new plan file** (adds a `docs/plans/*.md` file), the
workflow treats the merge as the bootstrap trigger and automatically starts
Phase 1 — no explicit `Plan:` line is needed.

## Tips

To run a subset of tests:

```bash
uv run pytest tests/ -k "test_something" -v
```

## Workflow Testing

The repository's GitHub Actions workflows are tested at three levels:

1. **Static Analysis** — [`actionlint`](https://github.com/rhysd/actionlint) runs via pre-commit (which CI also runs) to catch YAML and expression errors.
2. **Shell Script Unit Tests** — Complex shell logic is extracted into `.github/scripts/` and tested with [Bats](https://github.com/bats-core/bats-core). A custom pytest-bats plugin (`tests/workflows/conftest.py`) collects `.bats` files as pytest items, so they run alongside regular Python tests:
   ```bash
   # Direct (requires bats installed)
   bats tests/workflows/

   # Via pytest (the conftest.py plugin runs each @test block as a pytest item;
   # skips gracefully if bats is not installed)
   uv run pytest tests/workflows/ -v
   ```
3. **Convention Checks** — `tests/test_workflow_conventions.py` enforces project-level rules (pinned actions, concurrency groups, `GH_TOKEN`, etc.) via pytest.

### Manual Smoke Tests (workflow_dispatch)

The `Plan Phase Continuation` workflow supports a `workflow_dispatch` trigger
for manual testing:

1. Go to **Actions** → select the workflow → **Run workflow**.
2. Enter the plan file path (e.g. `docs/plans/udt-support.md`) and optionally the completed phase number.
3. Verify the expected comment is posted on the PR.

## Making a new release

Releases are cut by merging a release PR. The
[CI workflow](.github/workflows/ci.yml) uses
[python-semantic-release](https://python-semantic-release.readthedocs.io/)
to analyse [Conventional Commits](https://www.conventionalcommits.org)
and determine whether a version bump is needed:

| Commit prefix | Version bump |
|---|---|
| `fix:` | Patch (`0.0.x`) |
| `feat:` | Minor (`0.x.0`) |
| `feat!:` / `BREAKING CHANGE:` | Major (`x.0.0`) |

On every push to `master` with releasable commits, CI opens (or updates) a
`chore(release): vX.Y.Z` PR from the `release/next` branch containing the
`CHANGELOG.md` entry. Nothing is released until that PR is merged
(rebase or squash), at which point CI will:

1. Push a version tag (e.g. `v1.0.0`).
2. Create a GitHub Release with auto-generated release notes.
3. Build the package with `uv build` (version derived from the tag via `hatch-vcs`).
4. Publish to PyPI using [Trusted Publishing](#setting-up-trusted-publishing-on-pypi) (OIDC).

No manual tagging or PyPI token management is required. The release PR is
opened with the `GH_PAT` secret (fine-grained PAT, Contents + Pull
requests read/write) so CI runs on it; without it `GITHUB_TOKEN` is used and
CI won't trigger on the release PR.

### Setting up Trusted Publishing on PyPI

[Trusted Publishing](https://docs.pypi.org/trusted-publishers/) lets PyPI verify
GitHub Actions runs via OpenID Connect (OIDC), so you never have to create or
rotate a PyPI API token.

**One-time setup steps (done once per PyPI project):**

1. Go to <https://pypi.org> and log in.
2. Open the project page for `coodie`, then go to **Manage → Publishing**.
   - If the project does not exist yet, go to
     <https://pypi.org/manage/account/publishing/> to add a *pending* publisher
     before the first upload.
3. Click **Add a new publisher** and fill in the form:

   | Field | Value |
   |---|---|
   | Owner | `scylladb` |
   | Repository name | `coodie` |
   | Workflow name | `ci.yml` |
   | Environment name | `release` |

4. Click **Add**.

**GitHub repository setup:**

1. In the repository, go to **Settings → Environments** and create an
   environment named **`release`**.
2. Optionally add protection rules (e.g. require a reviewer before the
   publish job runs).

Once this is done, merging the release PR will trigger the release and PyPI publish — no stored
credentials needed.

[gh-issues]: https://github.com/scylladb/coodie/issues
