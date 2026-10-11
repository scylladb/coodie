# Benchmarks

coodie includes a comprehensive benchmark suite that compares performance
against **cqlengine** (from cassandra-driver / scylla-driver) across common ORM
operations.

## What Is Benchmarked

| File | Operations |
|---|---|
| `bench_insert.py` | Single INSERT, INSERT IF NOT EXISTS, INSERT with TTL |
| `bench_read.py` | GET by PK, filter by secondary index, filter + LIMIT, COUNT |
| `bench_update.py` | Partial UPDATE, UPDATE with IF condition (LWT) |
| `bench_delete.py` | Single DELETE, bulk DELETE via QuerySet |
| `bench_batch.py` | Batch INSERT (10 rows), batch INSERT (100 rows) |
| `bench_schema.py` | `sync_table` create, `sync_table` idempotent no-op |
| `bench_collections.py` | Collection field write/read/round-trip |
| `bench_udt.py` | UDT serialization, instantiation, nested UDT, DDL generation |
| `bench_serialization.py` | Model instantiation and serialization (no DB) |

## Running Locally

Benchmarks require **Docker** (ScyllaDB runs in a container via
[testcontainers](https://testcontainers-python.readthedocs.io/)).

```bash
# Install dependencies
uv sync --all-groups

# Run all benchmarks with the default scylla driver
pytest benchmarks/ -v --benchmark-enable --benchmark-sort=mean

# Choose a driver: scylla | cassandra | acsylla
pytest benchmarks/ -v --benchmark-enable --driver-type=acsylla

# Save results and compare later
pytest benchmarks/ --benchmark-enable --benchmark-save=baseline
pytest benchmarks/ --benchmark-enable --benchmark-compare=0001_baseline
```

See `benchmarks/README.md` for the full set of options.

## CI Integration

The **Benchmarks** workflow (`.github/workflows/benchmark.yml`) runs
automatically on:

* Every push to `master`
* Pull requests labeled **`benchmark`**
* Weekly schedule (Monday 06:00 UTC)

Each run benchmarks both the **scylla** and **acsylla** drivers.

### Trend Tracking with github-action-benchmark

Results are published to the `gh-pages` branch using
[github-action-benchmark](https://github.com/benchmark-action/github-action-benchmark).
This provides:

* **Historical trend charts** — viewable on the repository's GitHub Pages site:
  * [scylla driver benchmarks](https://scylladb.github.io/coodie/benchmarks/scylla/)
  * [acsylla driver benchmarks](https://scylladb.github.io/coodie/benchmarks/acsylla/)
  * [instruction counts](https://scylladb.github.io/coodie/benchmarks/instructions/):
    CPU instructions per call for the in-memory `test_coodie_*` benchmarks,
    from the Instruction Counts workflow. These barely change between runner
    VMs, so they show real trends better than the wall-time charts. A PR, or a
    master push, fails when any count grows more than 5%, and PRs get a comment
    with the overview.
  * [all benchmarks overview](https://scylladb.github.io/coodie/benchmarks/)
* **Regression alerts** — when a benchmark regresses beyond 150% of its
  previous value, an alert comment is posted on the commit or pull request.
* **Workflow summary** — every CI run includes a benchmark summary in the
  GitHub Actions job summary.

On pushes to `master`, results are automatically pushed to the `gh-pages` branch.
On pull requests the action compares against the stored baseline and reports
regressions without modifying the `gh-pages` branch.

### Running Benchmarks on a Pull Request

Add the **`benchmark`** label to the pull request. The workflow will run and
post results in the job summary. If a regression is detected, a comment is
left on the PR.
