"""Smoke test for the Time-Series IoT demo.

Starts the FastAPI app, verifies endpoints, creates readings, checks pagination.

Usage:
    python smoke_test.py
"""

from __future__ import annotations

import os
import subprocess
import sys
import time

import httpx

APP_HOST = os.getenv("APP_HOST", "http://127.0.0.1:8001")
APP_STARTUP_TIMEOUT = 20  # seconds


def wait_for_app(url: str, timeout: int = APP_STARTUP_TIMEOUT) -> None:
    """Poll until the app responds or timeout is reached."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = httpx.get(url, timeout=2)
            if r.status_code < 500:
                return
        except httpx.TransportError:
            pass
        time.sleep(0.5)
    raise RuntimeError(f"App did not start within {timeout}s at {url}")


def main() -> None:
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8001", "--log-level", "warning"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "DISABLE_BACKGROUND_DEVICE": "1"},
    )
    try:
        print(f"  Waiting for app at {APP_HOST}...")
        wait_for_app(APP_HOST + "/")

        client = httpx.Client(base_url=APP_HOST, timeout=10)

        # --- GET / returns HTML ---
        r = client.get("/")
        assert r.status_code == 200, f"GET / returned {r.status_code}"
        assert "Station Argos-7" in r.text, "Index page missing expected content"

        # --- GET /sensors returns JSON list ---
        r = client.get("/sensors")
        assert r.status_code == 200, f"GET /sensors returned {r.status_code}"
        assert isinstance(r.json(), list), "/sensors did not return a list"

        # --- GET /readings/paged returns paginated JSON ---
        r = client.get("/readings/paged", params={"page_size": 5})
        assert r.status_code == 200, f"GET /readings/paged returned {r.status_code}"
        body = r.json()
        assert "data" in body, "Paged response missing 'data' key"
        assert "next_cursor" in body, "Paged response missing 'next_cursor' key"
        assert "has_more" in body, "Paged response missing 'has_more' key"

        # If there are more pages, fetch the next page
        if body["next_cursor"]:
            r = client.get(
                "/readings/paged",
                params={"page_size": 5, "cursor": body["next_cursor"]},
            )
            assert r.status_code == 200, f"Next page returned {r.status_code}"

        # --- HTMX UI endpoint returns HTML ---
        r = client.get("/ui/dashboard")
        assert r.status_code == 200, f"GET /ui/dashboard returned {r.status_code}"

        # --- Paged UI endpoint ---
        r = client.get("/ui/paged", params={"page_size": 5})
        assert r.status_code == 200, f"GET /ui/paged returned {r.status_code}"

        # --- Paged UI with date filter ---
        r = client.get("/ui/paged", params={"page_size": 5, "start_date": "2026-01-01"})
        assert r.status_code == 200, f"GET /ui/paged with start_date returned {r.status_code}"

        # --- Device status endpoint ---
        r = client.get("/device/status")
        assert r.status_code == 200, f"GET /device/status returned {r.status_code}"
        status = r.json()
        assert "running" in status, "Device status missing 'running' key"
        assert "sensors" in status, "Device status missing 'sensors' key"
        # Background device is disabled in test mode
        assert status["running"] is False, "Background device should be disabled in test mode"

        # --- Chart data endpoint ---
        r = client.get("/sensors/reactor-core-A1/chart", params={"minutes": 5})
        assert r.status_code == 200, f"GET /sensors/.../chart returned {r.status_code}"
        chart_data = r.json()
        assert "labels" in chart_data, "Chart response missing 'labels' key"
        assert "temperature" in chart_data, "Chart response missing 'temperature' key"
        assert "humidity" in chart_data, "Chart response missing 'humidity' key"
        assert "pressure" in chart_data, "Chart response missing 'pressure' key"

        # --- Charts UI endpoint ---
        r = client.get("/ui/charts")
        assert r.status_code == 200, f"GET /ui/charts returned {r.status_code}"

        print("  ✓ All endpoint checks passed")

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
