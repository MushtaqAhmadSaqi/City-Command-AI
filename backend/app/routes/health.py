"""
Health Routes — GET /health/apis

Returns the health status of all mock API integrations.
Supports the dashboard API health indicators.
"""

from fastapi import APIRouter
from app.data_store import data_store

router = APIRouter()


@router.get("/apis")
async def get_api_health():
    """Return health status of all external API integrations."""
    return {
        "success": True,
        "data": list(data_store.api_health.values()),
        "summary": {
            "healthy": sum(1 for a in data_store.api_health.values() if a["status"] == "healthy"),
            "degraded": sum(1 for a in data_store.api_health.values() if a["status"] == "degraded"),
            "down": sum(1 for a in data_store.api_health.values() if a["status"] == "down"),
        }
    }


@router.get("/stats")
async def get_system_stats():
    """Return overall system statistics for the dashboard."""
    return {
        "success": True,
        "data": data_store.get_stats(),
    }
