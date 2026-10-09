"""Views for the Hivemind Kanban task board."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from cassandra_models import TaskCounter, TaskEvent
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

# Default board ID (single-board demo)
DEFAULT_BOARD_ID = UUID("00000000-0000-0000-0000-000000000001")

STATUS_FLOW = {
    "todo": "in_progress",
    "in_progress": "done",
    "done": "todo",
}


def _get_counter(board_id: UUID, status: str) -> int:
    """Get the counter value for a board+status, returning 0 if not found."""
    try:
        counter = TaskCounter.find_one(board_id=board_id, status=status)
        if counter is not None:
            return counter.count
    except (ValueError, ConnectionError, OSError):
        pass
    return 0


def board(request: HttpRequest) -> HttpResponse:
    """Render the Kanban board with tasks grouped by status."""
    board_id = DEFAULT_BOARD_ID
    tasks = TaskEvent.find(board_id=board_id).all()

    columns = {
        "todo": [],
        "in_progress": [],
        "done": [],
    }
    for task in tasks:
        if task.status in columns:
            columns[task.status].append(task)

    # Get counter values
    counters = {}
    for status in columns:
        counters[status] = _get_counter(board_id, status)

    total_tasks = sum(counters.values())

    return render(
        request,
        "tasks/board.html",
        {
            "columns": columns,
            "counters": counters,
            "total_tasks": total_tasks,
            "board_id": board_id,
        },
    )


def task_create(request: HttpRequest) -> HttpResponse:
    """Create a new task event."""
    if request.method == "POST":
        board_id = DEFAULT_BOARD_ID
        sprint_raw = request.POST.get("sprint", "1")
        try:
            sprint = max(1, int(sprint_raw))
        except (ValueError, TypeError):
            sprint = 1
        task = TaskEvent(
            board_id=board_id,
            title=request.POST.get("title", "Untitled Task"),
            description=request.POST.get("description", ""),
            assignee=request.POST.get("assignee", ""),
            priority=request.POST.get("priority", "medium"),
            sprint=sprint,
            status="todo",
        )
        task.save()

        # Increment counter
        counter = TaskCounter(board_id=board_id, status="todo")
        counter.increment(count=1)

    return redirect("board")


def task_move(request: HttpRequest, board_id: str, created_at: str) -> HttpResponse:
    """Move a task to the next status column."""
    if request.method == "POST":
        bid = UUID(board_id)
        ts = datetime.fromisoformat(created_at)
        task = TaskEvent.find_one(board_id=bid, created_at=ts)
        if task is not None:
            old_status = task.status
            new_status = STATUS_FLOW.get(old_status, "todo")

            # Delete old task and create new one with updated status
            task.delete()
            new_task = TaskEvent(
                board_id=task.board_id,
                id=task.id,
                title=task.title,
                description=task.description,
                status=new_status,
                assignee=task.assignee,
                priority=task.priority,
                sprint=task.sprint,
            )
            new_task.save()

            # Update counters
            old_counter = TaskCounter(board_id=bid, status=old_status)
            old_counter.decrement(count=1)
            new_counter = TaskCounter(board_id=bid, status=new_status)
            new_counter.increment(count=1)

    return redirect("board")


def task_delete(request: HttpRequest, board_id: str, created_at: str) -> HttpResponse:
    """Delete a task event."""
    if request.method == "POST":
        bid = UUID(board_id)
        ts = datetime.fromisoformat(created_at)
        task = TaskEvent.find_one(board_id=bid, created_at=ts)
        if task is not None:
            # Decrement counter
            counter = TaskCounter(board_id=bid, status=task.status)
            counter.decrement(count=1)
            task.delete()

    return redirect("board")
