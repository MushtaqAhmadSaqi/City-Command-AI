"""
Resource Routes — POST /resources/allocate

Resource allocation endpoints.
Full implementation in Step 14.
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/allocate")
async def allocate_resources():
    """Allocate resources across incidents. Full implementation in Step 14."""
    return {"success": True, "message": "Resource allocation endpoint ready. Full implementation in Step 14."}


@router.get("")
async def list_resources():
    """List all resources."""
    from app.data_store import data_store
    return {"success": True, "data": list(data_store.resources.values())}
