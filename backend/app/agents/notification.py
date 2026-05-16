"""
CityCommand AI — Stakeholder Notification Agent

Drafts targeted messages for 7 distinct audiences based on
incident details and resource assignments.

AUDIENCES & CHANNELS
────────────────────
public              SMS Broadcast
emergency_services  Radio/CAD
hospitals           Email/Portal
utility             Email
traffic             Smart Signs/App
media               Press Release
field_team          Push Notification

APPROVAL LOGIC
──────────────
Public and Media notifications ALWAYS require human approval.
Other notifications require approval IF incident confidence < 0.85
OR if there are alternate hypotheses flagged for human review.
"""

import uuid
from datetime import datetime, timezone
from app.data_store import data_store

def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _uid(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"

_AUDIENCES = [
    ("public",             "SMS Broadcast"),
    ("emergency_services", "Radio/CAD"),
    ("hospitals",          "Email/Portal"),
    ("utility",            "Email"),
    ("traffic",            "Smart Signs/App"),
    ("media",              "Press Release"),
    ("field_team",         "Push Notification"),
]

def _generate_message(audience: str, incident: dict, assignments: list[dict]) -> str:
    """Generate a targeted message based on audience and incident type."""
    title    = incident.get("title", "Unknown Incident")
    area     = incident.get("location", {}).get("area", "Unknown Area")
    severity = incident.get("severity", "MEDIUM")
    c_type   = incident.get("primary_type", "unknown")

    # Gather resource info
    ambulances = [a for a in assignments if a["resource_type"] == "ambulance"]
    pumps      = [a for a in assignments if a["resource_type"] == "drainage_pump"]
    police     = [a for a in assignments if a["resource_type"] == "traffic_police"]

    if audience == "public":
        if c_type == "urban_flood":
            return f"⚠️ FLOOD ALERT: {area}. Avoid travel in this area. Emergency teams deployed. Stay tuned for updates. — CityCommand AI"
        elif c_type == "heat_emergency":
            return f"⚠️ HEAT ALERT: {area}. Extreme temperatures. Stay hydrated and indoors. Cooling centers being deployed. — CityCommand AI"
        else:
            return f"⚠️ EMERGENCY ALERT: {title} in {area}. Please avoid the area. — CityCommand AI"

    elif audience == "emergency_services":
        units = f"{len(ambulances)}x Amb, {len(pumps)}x Pump, {len(police)}x Police"
        return f"DISPATCH: {title} at {area}. Severity: {severity}. Units assigned: {units}. Coordinate with field team on ground."

    elif audience == "hospitals":
        if c_type in ["heat_emergency", "traffic_accident", "fire_emergency"]:
            return f"MEDICAL ALERT: {title} at {area}. Expect incoming casualties/patients. {len(ambulances)} ambulances dispatched. Prepare intake protocols."
        return f"ADVISORY: {title} at {area}. Maintain normal operations, no mass casualties expected at this time."

    elif audience == "utility":
        if c_type == "urban_flood":
            return f"UTILITY NOTICE: Flooding reported at {area}. Possible water-main involvement or electrical hazard. Dispatch inspection crew."
        elif c_type == "heat_emergency":
            return f"UTILITY NOTICE: Heat emergency at {area}. Monitor grid load and report any localized outages."
        return f"UTILITY ADVISORY: {title} at {area}. Monitor infrastructure in vicinity."

    elif audience == "traffic":
        return f"TRAFFIC MGMT: {title} at {area}. Divert traffic away from incident zone. Update variable message signs."

    elif audience == "media":
        return f"FOR IMMEDIATE RELEASE: CityCommand AI is responding to {title} in {area}. Severity is {severity}. Emergency response is underway. Public advised to avoid the area. Official update to follow."

    elif audience == "field_team":
        return f"FIELD DISPATCH: Deploy to {area} for {title}. Report situational update every 15 mins. Establish perimeter."

    return f"Notification regarding {title}."

def run(workflow_id: str, incident_id: str) -> dict:
    """
    Draft notifications for an incident.

    Args:
      workflow_id: Current pipeline workflow ID
      incident_id: Incident to notify about

    Returns:
      Dict with created notification IDs and trace ID.
    """
    incident = data_store.incidents.get(incident_id)
    if not incident:
        raise ValueError(f"Incident {incident_id} not found")

    assignments = data_store.resource_assignments.get(incident_id, [])

    # Determine base approval requirement
    confidence = incident.get("confidence", 0.5)
    human_review_flag = incident.get("human_review_required", False)
    base_requires_approval = (confidence < 0.85) or human_review_flag

    created_ids = []
    drafts_created = 0

    for audience, channel in _AUDIENCES:
        # Public and media ALWAYS require approval
        requires_approval = base_requires_approval or audience in ("public", "media")

        message = _generate_message(audience, incident, assignments)

        notif = {
            "id":                _uid("msg_"),
            "incident_id":       incident_id,
            "audience":          audience,
            "channel":           channel,
            "message":           message,
            "status":            "draft",
            "requires_approval": requires_approval,
            "sent_at":           None,
            "created_by_agent":  "StakeholderNotificationAgent",
            "created_at":        _now(),
        }
        data_store.notifications[notif["id"]] = notif
        created_ids.append(notif["id"])
        drafts_created += 1

    # Trace
    trace = {
        "id":            _uid("trc_"),
        "workflow_id":   workflow_id,
        "incident_id":   incident_id,
        "agent_name":    "StakeholderNotificationAgent",
        "step":          "draft_all_notifications",
        "input_summary": f"Incident {incident_id}, {len(assignments)} assignments",
        "output_summary": f"Created {drafts_created} draft messages across 7 audiences. "
                          f"Public/Media require approval. Base approval: {base_requires_approval}.",
        "tool_calls":    ["draft_message_per_audience()", "check_approval_required()"],
        "fallback_used": False,
        "human_review_required": True, # Always true because public/media need approval
        "duration_ms":   42,
        "timestamp":     _now(),
    }
    data_store.traces.append(trace)

    return {
        "notification_ids": created_ids,
        "trace_id": trace["id"]
    }
