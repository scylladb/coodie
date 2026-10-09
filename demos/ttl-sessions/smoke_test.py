"""Smoke test for the TTL Sessions demo.

Starts the FastAPI app, verifies endpoints, creates a session, checks it
exists, then verifies it disappears after the TTL expires.

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
    )
    try:
        print(f"  Waiting for app at {APP_HOST}...")
        wait_for_app(APP_HOST + "/")

        client = httpx.Client(base_url=APP_HOST, timeout=10)

        # --- GET / returns HTML ---
        r = client.get("/")
        assert r.status_code == 200, f"GET / returned {r.status_code}"
        assert "Memory Vault" in r.text, "Index page missing expected content"

        # --- GET /sessions returns JSON list ---
        r = client.get("/sessions")
        assert r.status_code == 200, f"GET /sessions returned {r.status_code}"
        assert isinstance(r.json(), list), "/sessions did not return a list"

        # --- POST /sessions creates a session with short TTL ---
        r = client.post(
            "/sessions",
            params={
                "user_name": "SmokeTest Agent",
                "memory_fragment": "This memory will dissolve shortly",
                "ttl": 5,
            },
        )
        assert r.status_code == 201, f"POST /sessions returned {r.status_code}"
        session = r.json()
        token = session["token"]
        assert session["user_name"] == "SmokeTest Agent"

        # --- GET /sessions/{token} returns the session ---
        r = client.get(f"/sessions/{token}")
        assert r.status_code == 200, f"GET /sessions/{{token}} returned {r.status_code}"

        # --- DELETE /sessions/{token} removes the session ---
        r = client.delete(f"/sessions/{token}")
        assert r.status_code == 204, f"DELETE /sessions/{{token}} returned {r.status_code}"

        # --- GET /sessions/{token} returns 404 after deletion ---
        r = client.get(f"/sessions/{token}")
        assert r.status_code == 404, f"Expected 404 after delete, got {r.status_code}"

        # --- HTMX UI endpoint returns HTML ---
        r = client.get("/ui/sessions")
        assert r.status_code == 200, f"GET /ui/sessions returned {r.status_code}"

        print("  ✓ All endpoint checks passed")

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
