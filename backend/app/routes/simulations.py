"""
CityCommand AI — Simulation Routes

POST /simulations/run              Run simulation for an incident
GET  /simulations/{incident_id}    Get existing simulation result
GET  /simulations/actions          List all supported action types
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from app.data_store import data_store

router = APIRouter()

SUPPORTED_ACTIONS = [
    "traffic_reroute", "emergency_dispatch", "public_alert",
    "deploy_pump", "cooling_station", "water_supply",
    "utility_inspection", "field_verification",
]

def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ─────────────────────────────────────────────────
# GET /simulations/actions
# ─────────────────────────────────────────────────
@router.get("/actions")
async def list_actions():
    """List all supported simulation action types."""
    return {
        "success": True,
        "data":    SUPPORTED_ACTIONS,
        "timestamp": _now(),
    }


# ─────────────────────────────────────────────────
# POST /simulations/run
# ─────────────────────────────────────────────────
class SimulationRequest(BaseModel):
    incident_id: str
    actions:     list[str]

@router.post("/run")
async def run_simulation(body: SimulationRequest):
    """
    Run the SimulationAgent for a specific incident and action plan.

    Computes before/after state, per-metric deltas, side effects,
    cost estimate, and risk-if-delayed message.
    """
    incident = data_store.incidents.get(body.incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{body.incident_id}' not found")

    invalid = [a for a in body.actions if a not in SUPPORTED_ACTIONS]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported action types: {invalid}. Supported: {SUPPORTED_ACTIONS}"
        )

    from app.agents import simulation as simulation_agent
    import uuid

    wf_id  = f"wf_{uuid.uuid4().hex[:8]}"
    result = simulation_agent.run(
        workflow_id=wf_id,
        incident_id=body.incident_id,
        actions=body.actions,
    )

    return {
        "success":   True,
        "data":      result,
        "timestamp": _now(),
        "trace_id":  result.get("trace_id"),
    }


# ─────────────────────────────────────────────────
# GET /simulations/{incident_id}
# ─────────────────────────────────────────────────
@router.get("/{incident_id}")
async def get_simulation(incident_id: str):
    """Get the most recent simulation result for an incident."""
    simulation = data_store.simulations.get(incident_id)
    if not simulation:
        raise HTTPException(
            status_code=404,
            detail=f"No simulation found for incident '{incident_id}'. Run POST /simulations/run first."
        )
    return {
        "success":   True,
        "data":      simulation,
        "timestamp": _now(),
    }
