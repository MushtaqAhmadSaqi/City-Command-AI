"""
Incident Routes — GET /incidents, GET /incidents/{id}

Incident management endpoints.
Full implementation in Step 10.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def list_incidents():
    """List all incidents. Full implementation in Step 10."""
    from app.data_store import data_store
    return {"success": True, "data": list(data_store.incidents.values())}


@router.get("/{incident_id}")
async def get_incident(incident_id: str):
    """Get incident detail. Full implementation in Step 10."""
    from app.data_store import data_store
    incident = data_store.incidents.get(incident_id)
    if not incident:
        return {"success": False, "error": f"Incident {incident_id} not found"}
    return {"success": True, "data": incident}
