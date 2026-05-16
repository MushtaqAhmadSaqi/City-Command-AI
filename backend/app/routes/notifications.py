"""
CityCommand AI — Notification Routes

GET   /notifications               List notifications (filter by incident_id)
POST  /notifications/draft         Trigger StakeholderNotificationAgent
PATCH /notifications/{id}/status   Update status (e.g., approve -> sent)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
import uuid

from app.data_store import data_store

router = APIRouter()

def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _uid(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"

# ─────────────────────────────────────────────────
# GET /notifications
# ─────────────────────────────────────────────────
@router.get("")
async def list_notifications(
    incident_id: Optional[str] = Query(None, description="Filter by incident"),
    status:      Optional[str] = Query(None, description="Filter by status")
):
    """List notifications with optional filtering."""
    notifications = list(data_store.notifications.values())

    if incident_id:
        notifications = [n for n in notifications if n.get("incident_id") == incident_id]
    if status:
        notifications = [n for n in notifications if n.get("status") == status]

    # Sort by created_at descending
    notifications.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return {
        "success": True,
        "data":    notifications,
        "timestamp": _now()
    }

# ─────────────────────────────────────────────────
# POST /notifications/draft
# ─────────────────────────────────────────────────
class DraftRequest(BaseModel):
    incident_id: str

@router.post("/draft")
async def draft_notifications(body: DraftRequest):
    """
    Trigger the StakeholderNotificationAgent to draft messages
    for a specific incident.
    """
    if body.incident_id not in data_store.incidents:
        raise HTTPException(status_code=404, detail=f"Incident '{body.incident_id}' not found")

    from app.agents import notification as notification_agent

    wf_id = _uid("wf_")
    result = notification_agent.run(workflow_id=wf_id, incident_id=body.incident_id)

    # Fetch the created notifications to return them
    created_notifs = [data_store.notifications[nid] for nid in result["notification_ids"]]

    return {
        "success": True,
        "data":    created_notifs,
        "message": f"Drafted {len(created_notifs)} notifications.",
        "timestamp": _now(),
        "trace_id":  result["trace_id"]
    }

# ─────────────────────────────────────────────────
# PATCH /notifications/{id}/status
# ─────────────────────────────────────────────────
class StatusUpdate(BaseModel):
    status: str

VALID_STATUSES = {"draft", "approved", "sent", "retracted"}

@router.patch("/{notification_id}/status")
async def update_status(notification_id: str, body: StatusUpdate):
    """Update notification status (e.g., approve and send)."""
    notif = data_store.notifications.get(notification_id)
    if not notif:
        raise HTTPException(status_code=404, detail=f"Notification '{notification_id}' not found")

    if body.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status '{body.status}'")

    old_status = notif["status"]
    notif["status"] = body.status
    if body.status == "sent":
        notif["sent_at"] = _now()

    # Audit log
    data_store.audit_logs.append({
        "id":          _uid("audit_"),
        "entity_type": "notification",
        "entity_id":   notification_id,
        "action":      "status_updated",
        "actor_type":  "human",
        "actor_id":    "operator",
        "before":      {"status": old_status},
        "after":       {"status": body.status},
        "timestamp":   _now(),
    })

    return {
        "success": True,
        "data":    notif,
        "message": f"Status updated: {old_status} -> {body.status}",
        "timestamp": _now()
    }
