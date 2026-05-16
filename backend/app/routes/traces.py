"""
CityCommand AI — Trace and Audit Log Routes

GET /traces                 List agent traces (filters: incident_id, workflow_id, agent_name)
GET /traces/audit-logs      List system audit logs (filters: entity_type, entity_id)

These endpoints directly power the "Agent Trace Screen",
a critical requirement for the hackathon judging.
"""

from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, timezone

from app.data_store import data_store

router = APIRouter()

def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# ─────────────────────────────────────────────────
# GET /traces
# ─────────────────────────────────────────────────
@router.get("")
async def list_traces(
    incident_id: Optional[str] = Query(None, description="Filter by incident ID"),
    workflow_id: Optional[str] = Query(None, description="Filter by workflow ID"),
    agent_name:  Optional[str] = Query(None, description="Filter by agent name"),
):
    """
    List agent execution traces.
    Returns the deterministic agent reasoning steps for the judging screen.
    """
    traces = data_store.traces

    if incident_id:
        traces = [t for t in traces if t.get("incident_id") == incident_id]
    if workflow_id:
        traces = [t for t in traces if t.get("workflow_id") == workflow_id]
    if agent_name:
        traces = [t for t in traces if t.get("agent_name") == agent_name]

    # Sort newest first
    traces = sorted(traces, key=lambda x: x.get("timestamp", ""), reverse=True)

    return {
        "success": True,
        "data":    traces,
        "count":   len(traces),
        "timestamp": _now()
    }

# ─────────────────────────────────────────────────
# GET /traces/audit-logs
# ─────────────────────────────────────────────────
@router.get("/audit-logs")
async def list_audit_logs(
    entity_type: Optional[str] = Query(None, description="Filter by entity type (e.g., incident, resource)"),
    entity_id:   Optional[str] = Query(None, description="Filter by specific entity ID"),
):
    """
    List system audit logs.
    Shows the history of manual operator overrides and critical system state changes.
    """
    logs = data_store.audit_logs

    if entity_type:
        logs = [l for l in logs if l.get("entity_type") == entity_type]
    if entity_id:
        logs = [l for l in logs if l.get("entity_id") == entity_id]

    # Sort newest first
    logs = sorted(logs, key=lambda x: x.get("timestamp", ""), reverse=True)

    return {
        "success": True,
        "data":    logs,
        "count":   len(logs),
        "timestamp": _now()
    }

