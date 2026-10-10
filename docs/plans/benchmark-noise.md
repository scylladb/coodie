# Benchmark Noise — Stable Regression Signal on Shared Runners

> **Goal:** Stop benchmark alerts from firing on GitHub runner noise
> ([#315](https://github.com/scylladb/coodie/issues/315)) by measuring what
> runner hardware can't distort: CPU instruction counts for in-memory
> benchmarks, and a same-job master-vs-PR ratio for database benchmarks.

---

## Table of Contents

1. [Problem](#1-problem)
2. [Approach](#2-approach)
3. [Implementation Phases](#3-implementation-phases)
4. [Trade-offs](#4-trade-offs)
5. [References](#5-references)

---

## 1. Problem

`.github/workflows/benchmark.yml` compares each run with the single previous
run stored on `gh-pages`. Sub-µs benchmarks swing up to **1.91×** between runs
of unrelated commits. The two driver jobs of the same commit often disagree,
too (e.g. `9ecca5d`: 851k vs 1.17M iter/s for `test_coodie_udt_instantiation`).
The likely cause is the runner: each job gets a fresh VM, and the hardware
under it varies (CPU model, frequency, noisy neighbours).

[#322](https://github.com/scylladb/coodie/pull/322) is the stop-gap. It charts
`1/min` instead of `1/mean`, logs the runner CPU model, and raises the alert
threshold to 200%. The margin is thin: the observed spread is 1.91×, close to the
2× threshold. Pinning to one CPU (`taskset`) only fixes core migration, which is
the smallest noise source here.

## 2. Approach

The 96 benchmarks split into two kinds:

| Kind | Count | Selection | Measurement |
|---|---|---|---|
| In-memory (instantiation, serialization, DDL generation) | 16 | `-m in_memory`, set automatically for tests that don't use `scylla_container` | CPU instruction counts under stock Valgrind (callgrind), base `src/` and PR `src/` measured in the **same job** |
| Database (insert, read, update, batch, schema, …) | 80 | `-m "not in_memory"` | Wall time, base commit and PR run in the **same job**, compared as a `min` ratio |

## 3. Implementation Phases

### Phase 1: Instruction Counts for In-Memory Benchmarks (Priority: High) ✅ Done

**Goal:** Deterministic PR-vs-master signal for the 16 in-memory benchmarks, with no benchmark code changes and no external service.

| Task | Description |
|---|---|
| 1.1 | Add `pytest-codspeed` to the `dev` dependency group. It speaks the `pytest-benchmark` API, and with `CODSPEED_ENV` set it issues callgrind start/stop/dump client requests around each benchmark, so stock Valgrind writes one profile per benchmark |
| 1.2 | `benchmarks/conftest.py`: mark tests that don't use `scylla_container` with `in_memory`; register the marker in `pyproject.toml` |
| 1.3 | Add `.github/workflows/instruction-counts.yml` (PRs only): `git worktree add base <base sha>`, then run the PR's `benchmarks/` under `valgrind --tool=callgrind --instr-atstart=no` twice, with `-o pythonpath=base/src` and with `src`. `PYTHONHASHSEED=0` makes the counts repeat exactly |
| 1.4 | `.github/scripts/compare-instructions.py`: read the `totals:` per benchmark, print a Markdown table to the job summary, fail on growth over +5% (CI noise floor with GC disabled: ≤1.2%). `benchmarks/conftest.py` disables GC when `CODSPEED_ENV` is set, since GC timing otherwise skews single-call counts by up to ~6% |

CodSpeed's hosted service needs an org admin to install its GitHub app, so this phase skips it and drives callgrind directly.

### Phase 2: Same-Job Base-vs-PR Comparison for Database Benchmarks (Priority: High)

**Goal:** Cancel runner hardware differences for the 80 database benchmarks by running the base commit and the PR on the same VM.

| Task | Description |
|---|---|
| 2.1 | In the PR path of `benchmark.yml`, `git worktree add base ${{ github.event.pull_request.base.sha }}` (as in Phase 1) and run the PR's `pytest benchmarks/ -m "not in_memory" -o pythonpath=base/src` with `--benchmark-storage=file://$RUNNER_TEMP/bench --benchmark-save=base` |
| 2.2 | Run the PR checkout with the same storage and `--benchmark-compare=0001 --benchmark-compare-fail=min:25%` (no custom compare script) |
| 2.3 | Post the comparison table to the job summary; keep the job non-blocking until the threshold is tuned on a few PRs |

### Phase 3: Retire Single-Run Alerts (Priority: Medium)

**Goal:** Phases 1–2 own the PR verdict; `github-action-benchmark` only keeps the master trend chart.

| Task | Description |
|---|---|
| 3.1 | Set `comment-on-alert: false` in `benchmark.yml`; keep `auto-push` on master for the gh-pages chart |
| 3.2 | Keep the in-memory benchmarks in the gh-pages chart for trend only. Their PR verdict comes from Phase 1 |
| 3.3 | Document in `benchmarks/README.md` where to read each signal |

### Phase 4: Database Benchmarks Under Instruction Counting (Priority: Low)

**Goal:** Find out whether callgrind gives stable counts for the database path. Only coodie's client-side instructions would count.

| Task | Description |
|---|---|
| 4.1 | Experimental `workflow_dispatch` job running a few database benchmarks under callgrind (as in Phase 1) with the Scylla testcontainer |
| 4.2 | Compare count variance across 5 runs; adopt if it stays under 1%. Driver I/O threads and event-loop polling may add noise |

## 4. Trade-offs

- Phase 1 leans on pytest-codspeed's callgrind client requests (one dump per benchmark, named by test URI). If a pytest-codspeed release changes that, the compare script finds no results and fails loudly.
- No history for instruction counts; each PR is compared with its base only.
- Instruction counts don't capture cache or memory effects. That's acceptable for pure-Python model code, and Phase 2 keeps a wall-time signal on the database path.
- Phase 2 roughly doubles the labeled PR benchmark job time.

## 5. References

- [#315 — Benchmark alerts fire on runner noise](https://github.com/scylladb/coodie/issues/315)
- [#322 — stop-gap: min-based ops, 200% threshold](https://github.com/scylladb/coodie/pull/322)
- [Valgrind callgrind manual](https://valgrind.org/docs/manual/cl-manual.html)
- [CodSpeed Python docs](https://codspeed.io/docs/benchmarks/python)
- [CodSpeed GitHub Actions integration](https://codspeed.io/docs/integrations/ci/github-actions)
- [CodSpeed: benchmarks in CI without noise](https://codspeed.io/blog/benchmarks-in-ci-without-noise)
- [pythonspeed: consistent benchmarking in CI](https://pythonspeed.com/articles/consistent-benchmarking-in-ci)
- [Quansight: GitHub Actions for benchmarks](https://labs.quansight.org/blog/github-actions-benchmarks)
- [scikit-image `asv continuous` in CI](https://github.com/raybellwaves/scikit-image/blob/main/benchmarks/README_CI.md)
