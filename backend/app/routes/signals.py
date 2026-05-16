"""
Signal Routes — POST /signals, GET /signals

Signal ingestion endpoints for citizen/social/field data.
Full implementation in Step 9.
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def submit_signal():
    """Submit a new signal. Full implementation in Step 9."""
    return {"success": True, "message": "Signal endpoint ready. Full implementation in Step 9."}


@router.get("")
async def list_signals():
    """List recent signals. Full implementation in Step 9."""
    from app.data_store import data_store
    return {"success": True, "data": data_store.signals}
