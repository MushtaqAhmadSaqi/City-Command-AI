"""
CityCommand AI — Recovery Routes

POST /recovery/{incident_id}/false-alarm
Triggers the False Alarm Recovery Agent to roll back resources
and retract notifications for a mistakenly flagged incident.
"""

import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from app.data_store import data_store

router = APIRouter()

def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _uid(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"

class FalseAlarmRequest(BaseModel):
    reason: str = "Operator confirmed false alarm"

@router.post("/{incident_id}/false-alarm")
async def trigger_false_alarm_recovery(incident_id: str, body: FalseAlarmRequest):
    """
    Trigger the False Alarm Recovery Agent.
    Releases all assigned resources, retracts pending notifications,
    and marks the incident as resolved.
    """
    if incident_id not in data_store.incidents:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found")

    from app.agents import recovery as recovery_agent

    wf_id = _uid("wf_")
    
    try:
        result = recovery_agent.run(
            workflow_id=wf_id, 
            incident_id=incident_id, 
            reason_details=body.reason
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "success": True,
        "data":    result,
        "message": "False alarm recovery complete. Resources released.",
        "timestamp": _now(),
        "trace_id":  result["trace_id"]
    }
