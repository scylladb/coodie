"""Argus-inspired benchmarks — real-world patterns from scylladb/argus.

Patterns covered:
  - get-or-create (exists check + conditional create)
  - Filter by secondary index + all()
  - Composite partition key + clustering read (latest N runs)
  - List/Map collection mutation + save
  - Batch event creation
  - Notification feed (partition read, ordered by clustering key)
  - Status update (read-modify-save)
  - Multi-model fetch (cross-table lookups)
"""

import time
import uuid

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_uuid():
    return uuid.uuid4()


def _make_uuid1():
    return uuid.uuid1()


# ===================================================================
# 1. Get-or-create pattern  (User.get / DoesNotExist / create)
# ===================================================================


def test_cqlengine_get_or_create_user(benchmark, bench_env):
    """cqlengine: get existing user by PK, fall back to create."""
    from benchmarks.models_argus_cqlengine import CqlArgusUser

    uid = _make_uuid()
    CqlArgusUser.create(
        id=uid,
        username=f"user-{uid}",
        email=f"user-{uid}@test.com",
        roles=["ROLE_USER"],
    )

    def _get_or_create():
        try:
            CqlArgusUser.get(id=uid)
        except CqlArgusUser.DoesNotExist:
            CqlArgusUser.create(id=uid, username="fallback", roles=["ROLE_USER"])

    benchmark.group = "argus-get-or-create-user"
    benchmark(_get_or_create)


def test_coodie_get_or_create_user(benchmark, bench_env):
    """coodie: get existing user by PK, fall back to create."""
    from benchmarks.models_argus_coodie import CoodieArgusUser

    uid = _make_uuid()
    user = CoodieArgusUser(
        id=uid,
        username=f"user-{uid}",
        email=f"user-{uid}@test.com",
        roles=["ROLE_USER"],
    )
    user.save()

    def _get_or_create():
        results = CoodieArgusUser.find(id=uid).all()
        if not results:
            new_user = CoodieArgusUser(id=uid, username="fallback", roles=["ROLE_USER"])
            new_user.save()

    benchmark.group = "argus-get-or-create-user"
    benchmark(_get_or_create)


# ===================================================================
# 2. Filter by secondary index (status changes)
# ===================================================================


def test_cqlengine_filter_runs_by_status(benchmark, bench_env):
    """cqlengine: filter test runs by status via secondary index."""
    from benchmarks.models_argus_cqlengine import CqlArgusTestRun

    build = f"bench-job-{_make_uuid()}"
    for i in range(5):
        CqlArgusTestRun.create(
            build_id=build,
            status="passed" if i % 2 == 0 else "failed",
            scylla_version="5.4.0",
        )

    def _filter():
        list(CqlArgusTestRun.filter(build_id=build).all())

    benchmark.group = "argus-filter-runs-by-partition"
    benchmark(_filter)


def test_coodie_filter_runs_by_status(benchmark, bench_env):
    """coodie: filter test runs by partition key (build_id)."""
    from benchmarks.models_argus_coodie import CoodieArgusTestRun

    build = f"bench-job-{_make_uuid()}"
    for i in range(5):
        run = CoodieArgusTestRun(
            build_id=build,
            status="passed" if i % 2 == 0 else "failed",
            scylla_version="5.4.0",
        )
        run.save()

    def _filter():
        CoodieArgusTestRun.find(build_id=build).all()

    benchmark.group = "argus-filter-runs-by-partition"
    benchmark(_filter)


# ===================================================================
# 3. Composite key + limit (latest N runs for a build)
# ===================================================================


def test_cqlengine_latest_runs(benchmark, bench_env):
    """cqlengine: get latest 3 runs for a build (clustering order DESC)."""
    from benchmarks.models_argus_cqlengine import CqlArgusTestRun

    build = f"bench-latest-{_make_uuid()}"
    for _ in range(5):
        CqlArgusTestRun.create(build_id=build, status="passed")

    def _latest():
        list(CqlArgusTestRun.filter(build_id=build).limit(3).all())

    benchmark.group = "argus-latest-runs"
    benchmark(_latest)


def test_coodie_latest_runs(benchmark, bench_env):
    """coodie: get latest 3 runs for a build (clustering order DESC)."""
    from benchmarks.models_argus_coodie import CoodieArgusTestRun

    build = f"bench-latest-{_make_uuid()}"
    for _ in range(5):
        run = CoodieArgusTestRun(build_id=build, status="passed")
        run.save()

    def _latest():
        CoodieArgusTestRun.find(build_id=build).limit(3).all()

    benchmark.group = "argus-latest-runs"
    benchmark(_latest)


# ===================================================================
# 4. List mutation + save (role assignment)
# ===================================================================


def test_cqlengine_list_mutation(benchmark, bench_env):
    """cqlengine: append to list column and save."""
    from benchmarks.models_argus_cqlengine import CqlArgusUser

    uid = _make_uuid()
    CqlArgusUser.create(
        id=uid,
        username="role-test",
        email="role@test.com",
        roles=["ROLE_USER"],
    )

    def _mutate():
        user = CqlArgusUser.get(id=uid)
        if "ROLE_MANAGER" not in user.roles:
            user.roles.append("ROLE_MANAGER")
        user.save()

    benchmark.group = "argus-list-mutation"
    benchmark(_mutate)


def test_coodie_list_mutation(benchmark, bench_env):
    """coodie: modify list field and save."""
    from benchmarks.models_argus_coodie import CoodieArgusUser

    uid = _make_uuid()
    user = CoodieArgusUser(
        id=uid,
        username="role-test",
        email="role@test.com",
        roles=["ROLE_USER"],
    )
    user.save()

    def _mutate():
        results = CoodieArgusUser.find(id=uid).all()
        u = results[0]
        if "ROLE_MANAGER" not in u.roles:
            u.roles.append("ROLE_MANAGER")
        u.save()

    benchmark.group = "argus-list-mutation"
    benchmark(_mutate)


# ===================================================================
# 5. Batch event creation
# ===================================================================


def test_cqlengine_batch_events(benchmark, bench_env):
    """cqlengine: create 10 events in a BatchQuery."""
    from cassandra.cqlengine.query import BatchQuery as CqlBatchQuery

    from benchmarks.models_argus_cqlengine import CqlArgusEvent

    release = _make_uuid()
    run = _make_uuid()

    def _batch():
        with CqlBatchQuery() as b:
            for _ in range(10):
                CqlArgusEvent.batch(b).create(
                    release_id=release,
                    run_id=run,
                    user_id=_make_uuid(),
                    kind="STATUS_CHANGE",
                    body='{"old":"created","new":"running"}',
                )

    benchmark.group = "argus-batch-events"
    benchmark(_batch)


def test_coodie_batch_events(benchmark, bench_env):
    """coodie: create 10 events in a BatchQuery."""
    from benchmarks.models_argus_coodie import CoodieArgusEvent
    from coodie.batch import BatchQuery

    release = _make_uuid()
    run = _make_uuid()

    def _batch():
        with BatchQuery() as b:
            for _ in range(10):
                evt = CoodieArgusEvent(
                    release_id=release,
                    run_id=run,
                    user_id=_make_uuid(),
                    kind="STATUS_CHANGE",
                    body='{"old":"created","new":"running"}',
                )
                evt.save(batch=b)

    benchmark.group = "argus-batch-events"
    benchmark(_batch)


# ===================================================================
# 6. Notification feed (partition scan, time-ordered)
# ===================================================================


def test_cqlengine_notification_feed(benchmark, bench_env):
    """cqlengine: read 10 latest notifications for a user."""
    from benchmarks.models_argus_cqlengine import CqlArgusNotification

    receiver = _make_uuid()
    for _ in range(15):
        CqlArgusNotification.create(
            receiver=receiver,
            sender=_make_uuid(),
            type="MENTION",
            source_type="COMMENT",
            source_id=_make_uuid(),
            title="You were mentioned",
            content="@user mentioned you in a comment",
        )

    def _feed():
        list(CqlArgusNotification.filter(receiver=receiver).limit(10).all())

    benchmark.group = "argus-notification-feed"
    benchmark(_feed)


def test_coodie_notification_feed(benchmark, bench_env):
    """coodie: read 10 latest notifications for a user."""
    from benchmarks.models_argus_coodie import CoodieArgusNotification

    receiver = _make_uuid()
    for _ in range(15):
        n = CoodieArgusNotification(
            receiver=receiver,
            sender=_make_uuid(),
            type="MENTION",
            source_type="COMMENT",
            source_id=_make_uuid(),
            title="You were mentioned",
            content="@user mentioned you in a comment",
        )
        n.save()

    def _feed():
        CoodieArgusNotification.find(receiver=receiver).limit(10).all()

    benchmark.group = "argus-notification-feed"
    benchmark(_feed)


# ===================================================================
# 7. Status update (read-modify-save)
# ===================================================================


def test_cqlengine_status_update(benchmark, bench_env):
    """cqlengine: read a test run, change status, save."""
    from benchmarks.models_argus_cqlengine import CqlArgusTestRun

    build = f"bench-status-{_make_uuid()}"
    CqlArgusTestRun.create(build_id=build, status="created")

    def _update():
        runs = list(CqlArgusTestRun.filter(build_id=build).limit(1).all())
        run = runs[0]
        run.status = "running"
        run.heartbeat = int(time.time())
        run.save()

    benchmark.group = "argus-status-update"
    benchmark(_update)


def test_coodie_status_update(benchmark, bench_env):
    """coodie: read a test run, change status, save."""
    from benchmarks.models_argus_coodie import CoodieArgusTestRun

    build = f"bench-status-{_make_uuid()}"
    run = CoodieArgusTestRun(build_id=build, status="created")
    run.save()

    def _update():
        runs = CoodieArgusTestRun.find(build_id=build).limit(1).all()
        r = runs[0]
        r.status = "running"
        r.heartbeat = int(time.time())
        r.save()

    benchmark.group = "argus-status-update"
    benchmark(_update)


# ===================================================================
# 8. Comment with Map + List (reactions, mentions)
# ===================================================================


def test_cqlengine_comment_with_collections(benchmark, bench_env):
    """cqlengine: create comment with Map reactions and List mentions."""
    from benchmarks.models_argus_cqlengine import CqlArgusComment

    def _create():
        CqlArgusComment.create(
            test_run_id=_make_uuid(),
            user_id=_make_uuid(),
            release_id=_make_uuid(),
            posted_at=int(time.time() * 1000),
            message="This test looks flaky, investigating.",
            mentions=[_make_uuid(), _make_uuid()],
            reactions={"+1": 3, "eyes": 1},
        )

    benchmark.group = "argus-comment-collections"
    benchmark(_create)


def test_coodie_comment_with_collections(benchmark, bench_env):
    """coodie: create comment with Dict reactions and List mentions."""
    from benchmarks.models_argus_coodie import CoodieArgusComment

    def _create():
        c = CoodieArgusComment(
            test_run_id=_make_uuid(),
            user_id=_make_uuid(),
            release_id=_make_uuid(),
            posted_at=int(time.time() * 1000),
            message="This test looks flaky, investigating.",
            mentions=[_make_uuid(), _make_uuid()],
            reactions={"+1": 3, "eyes": 1},
        )
        c.save()

    benchmark.group = "argus-comment-collections"
    benchmark(_create)


# ===================================================================
# 9. Multi-model lookup (test → group → release chain)
# ===================================================================


def test_cqlengine_multi_model_lookup(benchmark, bench_env):
    """cqlengine: chain lookups across user + event (2-model fetch)."""
    from benchmarks.models_argus_cqlengine import CqlArgusEvent, CqlArgusUser

    uid = _make_uuid()
    CqlArgusUser.create(id=uid, username="lookup-test", email="lookup@test.com", roles=["ROLE_USER"])
    eid = _make_uuid()
    CqlArgusEvent.create(
        id=eid,
        user_id=uid,
        kind="STATUS_CHANGE",
        body="test",
    )

    def _lookup():
        event = CqlArgusEvent.get(id=eid)
        CqlArgusUser.get(id=event.user_id)

    benchmark.group = "argus-multi-model-lookup"
    benchmark(_lookup)


def test_coodie_multi_model_lookup(benchmark, bench_env):
    """coodie: chain lookups across user + event (2-model fetch)."""
    from benchmarks.models_argus_coodie import CoodieArgusEvent, CoodieArgusUser

    uid = _make_uuid()
    user = CoodieArgusUser(id=uid, username="lookup-test", email="lookup@test.com", roles=["ROLE_USER"])
    user.save()
    eid = _make_uuid()
    evt = CoodieArgusEvent(
        id=eid,
        user_id=uid,
        kind="STATUS_CHANGE",
        body="test",
    )
    evt.save()

    def _lookup():
        events = CoodieArgusEvent.find(id=eid).all()
        event = events[0]
        CoodieArgusUser.find(id=event.user_id).all()

    benchmark.group = "argus-multi-model-lookup"
    benchmark(_lookup)


# ===================================================================
# 10. Serialization: Argus-scale model instantiation
# ===================================================================


def test_cqlengine_argus_model_instantiation(benchmark):
    """cqlengine: instantiate a large TestRun model (no DB)."""
    try:
        from benchmarks.models_argus_cqlengine import CqlArgusTestRun
    except (ImportError, ModuleNotFoundError):
        pytest.skip("cqlengine not available")

    def _inst():
        CqlArgusTestRun(
            build_id="bench-perf-001",
            id=_make_uuid(),
            release_id=_make_uuid(),
            group_id=_make_uuid(),
            test_id=_make_uuid(),
            assignee=_make_uuid(),
            status="running",
            investigation_status="not_investigated",
            heartbeat=1234567890,
            build_job_url="https://ci.example.com/job/123",
            scylla_version="5.4.0",
        )

    benchmark.group = "argus-model-instantiation"
    benchmark(_inst)


def test_coodie_argus_model_instantiation(benchmark):
    """coodie: instantiate a large TestRun model (no DB)."""
    from benchmarks.models_argus_coodie import CoodieArgusTestRun

    def _inst():
        CoodieArgusTestRun(
            build_id="bench-perf-001",
            id=_make_uuid(),
            release_id=_make_uuid(),
            group_id=_make_uuid(),
            test_id=_make_uuid(),
            assignee=_make_uuid(),
            status="running",
            investigation_status="not_investigated",
            heartbeat=1234567890,
            build_job_url="https://ci.example.com/job/123",
            scylla_version="5.4.0",
        )

    benchmark.group = "argus-model-instantiation"
    benchmark(_inst)
