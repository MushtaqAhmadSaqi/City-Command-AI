"""
Trace Routes — GET /traces

Agent trace endpoints for the judging-critical trace screen.
Full implementation in Step 18.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def list_traces():
    """List all agent traces. Full implementation in Step 18."""
    from app.data_store import data_store
    return {"success": True, "data": data_store.traces}
