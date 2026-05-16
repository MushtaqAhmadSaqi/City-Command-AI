"""
CityCommand AI — Resource Routes

GET  /resources                     List all resources with status
GET  /resources/{id}                Single resource detail
POST /resources/allocate            Allocate resources across incidents
GET  /resources/assignments/{inc_id} Get assignments for one incident
POST /resources/{id}/release        Release a resource back to available
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.data_store import data_store

router = APIRouter()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _uid(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"


# ─────────────────────────────────────────────────
# GET /resources
# ─────────────────────────────────────────────────
@router.get("")
async def list_resources(
    status:        Optional[str] = Query(None, description="Filter by status: available | assigned | unavailable"),
    resource_type: Optional[str] = Query(None, description="Filter by resource type"),
):
    """List all resources with optional filters. Enriches with current assignment info."""
    resources = list(data_store.resources.values())

    if status:
        resources = [r for r in resources if r.get("status") == status]
    if resource_type:
        resources = [r for r in resources if r.get("resource_type") == resource_type]

    # Enrich with current assignment (if any)
    enriched = []
    for res in resources:
        assignment = None
        for inc_id, assignments in data_store.resource_assignments.items():
            match = next((a for a in assignments if a["resource_id"] == res["id"]), None)
            if match:
                assignment = {"incident_id": inc_id, "eta_min": match["eta_min"], "status": match["status"]}
                break
        enriched.append({**res, "current_assignment": assignment})

    return {
        "success": True,
        "data":    enriched,
        "meta": {
            "total":     len(list(data_store.resources.values())),
            "available": sum(1 for r in data_store.resources.values() if r.get("status") == "available"),
            "assigned":  sum(1 for r in data_store.resources.values() if r.get("status") == "assigned"),
        },
        "timestamp": _now(),
    }


# ─────────────────────────────────────────────────
# GET /resources/{resource_id}
# ─────────────────────────────────────────────────
@router.get("/{resource_id}")
async def get_resource(resource_id: str):
    """Get single resource detail."""
    res = data_store.resources.get(resource_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Resource '{resource_id}' not found")
    return {"success": True, "data": res, "timestamp": _now()}


# ─────────────────────────────────────────────────
# POST /resources/allocate
# ─────────────────────────────────────────────────
class AllocateRequest(BaseModel):
    incident_ids: list[str]

@router.post("/allocate")
async def allocate_resources(body: AllocateRequest):
    """
    Allocate available resources across one or more incidents.

    Uses the ResourceAllocationAgent which:
      - Ranks incidents by priority_score
      - Assigns resources per crisis-type requirements
      - Calculates ETAs via route_matrix
      - Logs trade-off notes where a higher-priority incident takes a resource
      - Holds back reserves for city safety net
    """
    if not body.incident_ids:
        raise HTTPException(status_code=400, detail="incident_ids must not be empty")

    # Validate all incident IDs exist
    missing = [iid for iid in body.incident_ids if iid not in data_store.incidents]
    if missing:
        raise HTTPException(status_code=404, detail=f"Incidents not found: {missing}")

    # Check if any resources are actually available
    available_count = sum(1 for r in data_store.resources.values() if r.get("status") == "available")
    if available_count == 0:
        raise HTTPException(
            status_code=409,
            detail="No resources available. All units are assigned. Release resources first."
        )

    from app.agents import allocation as allocation_agent
    wf_id  = _uid("wf_")
    result = allocation_agent.run(workflow_id=wf_id, incident_ids=body.incident_ids)

    return {
        "success": True,
        "data":    result,
        "message": (
            f"{len(result['assignments'])} assignments created across "
            f"{len(body.incident_ids)} incidents."
        ),
        "timestamp": _now(),
        "trace_id":  result.get("trace_id"),
    }


# ─────────────────────────────────────────────────
# GET /resources/assignments/{incident_id}
# ─────────────────────────────────────────────────
@router.get("/assignments/{incident_id}")
async def get_assignments_for_incident(incident_id: str):
    """Get all resource assignments for a specific incident."""
    if incident_id not in data_store.incidents:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found")

    assignments = data_store.resource_assignments.get(incident_id, [])
    return {
        "success":     True,
        "data":        assignments,
        "incident_id": incident_id,
        "count":       len(assignments),
        "timestamp":   _now(),
    }


# ─────────────────────────────────────────────────
# POST /resources/{resource_id}/release
# ─────────────────────────────────────────────────
@router.post("/{resource_id}/release")
async def release_resource(resource_id: str):
    """Release an assigned resource back to available status."""
    res = data_store.resources.get(resource_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Resource '{resource_id}' not found")
    if res.get("status") == "available":
        return {"success": True, "message": f"Resource '{resource_id}' is already available.", "timestamp": _now()}

    old_status = res["status"]
    data_store.resources[resource_id]["status"] = "available"

    # Remove from all assignment lists
    for inc_id in list(data_store.resource_assignments.keys()):
        data_store.resource_assignments[inc_id] = [
            a for a in data_store.resource_assignments[inc_id]
            if a["resource_id"] != resource_id
        ]

    data_store.audit_logs.append({
        "id": _uid("audit_"), "entity_type": "resource", "entity_id": resource_id,
        "action": "released", "actor_type": "human", "actor_id": "operator",
        "before": {"status": old_status}, "after": {"status": "available"},
        "timestamp": _now(),
    })

    return {
        "success": True,
        "data":    data_store.resources[resource_id],
        "message": f"Resource '{resource_id}' released to available.",
        "timestamp": _now(),
    }
