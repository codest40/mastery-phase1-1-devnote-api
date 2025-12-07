# error.py

from datetime import datetime
import os
import time
import platform

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_env
from db import get_db
import crud


# ---------------------
# ROUTER SETUP
# ---------------------
err_router = APIRouter(tags=["Error Metrics"])


# ---------------------
# GLOBAL ERROR STORAGE
# ---------------------
error_metrics = {
    "count": 0,
    "last_error_type": None,
    "last_error_time": None,
}


# ---------------------
# MIDDLEWARE – TRACK FAILED REQUESTS
# ---------------------
async def error_tracking_middleware(request: Request, call_next):
    """
    Middleware to log failed responses and exceptions globally.
    """
    try:
        response = await call_next(request)

        if response.status_code >= 400:
            error_metrics["count"] += 1
            error_metrics["last_error_type"] = (
                f"HTTP {response.status_code}"
            )
            error_metrics["last_error_time"] = (
                datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            )

        return response

    except Exception as exc:  # noqa: B902
        error_metrics["count"] += 1
        error_metrics["last_error_type"] = type(exc).__name__
        error_metrics["last_error_time"] = (
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        )
        raise exc


# ---------------------
# GLOBAL EXCEPTION HANDLER
# ---------------------
async def global_exception_handler(request: Request, exc: Exception):
    """
    Handles all unhandled exceptions.
    """
    error_metrics["count"] += 1
    error_metrics["last_error_type"] = type(exc).__name__
    error_metrics["last_error_time"] = (
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    )

    print(f"⚠️ Error occurred: {exc}")

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# ---------------------
# DASHBOARD STATS ENDPOINT
# ---------------------
@err_router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """
    Returns backend system stats for the dashboard.
    """
    start = time.perf_counter()

    # Try to get total notes safely
    try:
        notes = await crud.list_notes(db)
        total_notes = len(notes) if isinstance(notes, list) else 0
    except Exception as exc:  # noqa: B902
        total_notes = -1
        error_metrics["count"] += 1
        error_metrics["last_error_type"] = type(exc).__name__
        error_metrics["last_error_time"] = (
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        )

    # Calculate latency
    latency_ms = round((time.perf_counter() - start) * 1000, 2)

    # Prepare environment info
    env = get_env() or os.getenv("ENV", "development")

    return {
        "total_notes": total_notes,
        "latency_ms": latency_ms,
        "error_count": error_metrics["count"],
        "last_error_type": error_metrics["last_error_type"],
        "last_error_time": error_metrics["last_error_time"],
        "environment": env,
        "platform": platform.system(),
    }


# ---------------------
# TEST ROUTE – INTENTIONAL FAILURE
# ---------------------
@err_router.get("/trigger-error")
async def trigger_error():
    """
    Intentional endpoint to simulate backend error for testing.
    """
    raise ValueError("Simulated backend failure")
