"""
CityCommand AI — Incident Routes

GET  /incidents                    List all incidents (filterable, sorted by priority)
GET  /incidents/{id}               Full incident detail
POST /incidents/{id}/classify      Run classification agent on an incident
POST /incidents/{id}/predict-severity  Run severity prediction on an incident
PATCH /incidents/{id}/status       Update incident status (operator action)
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.data_store import data_store

router = APIRouter()


# ─────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────
def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _uid(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"

def _trace(workflow_id, incident_id, agent_name, step,
           input_summary, output_summary, tool_calls=None,
           fallback_used=False, human_review_required=False, duration_ms=0):
    entry = {
        "id": _uid("trc_"), "workflow_id": workflow_id,
        "incident_id": incident_id, "agent_name": agent_name,
        "step": step, "input_summary": input_summary,
        "output_summary": output_summary,
        "tool_calls": tool_calls or [], "fallback_used": fallback_used,
        "human_review_required": human_review_required,
        "duration_ms": duration_ms, "timestamp": _now(),
    }
    data_store.traces.append(entry)
    return entry


# ─────────────────────────────────────────────────
# GET /incidents
# ─────────────────────────────────────────────────
@router.get("")
async def list_incidents(
    status:   Optional[str] = Query(None, description="Filter by status"),
    severity: Optional[str] = Query(None, description="Filter by severity level"),
    limit:    int           = Query(50, ge=1, le=200),
    offset:   int           = Query(0, ge=0),
):
    """
    Return incidents sorted by priority_score descending.
    Enriches each incident with:
      - signal_count
      - assignment_count
      - has_simulation
      - notification_count
    """
    incidents = list(data_store.incidents.values())

    if status:
        incidents = [i for i in incidents if i.get("status") == status]
    if severity:
        incidents = [i for i in incidents if i.get("severity") == severity.upper()]

    # Sort by priority descending
    incidents.sort(key=lambda i: i.get("priority_score", 0), reverse=True)

    # Enrich with counts for the mobile list cards
    enriched = []
    for inc in incidents[offset: offset + limit]:
        inc_id = inc["id"]
        enriched.append({
            **inc,
            "signal_count":       len(inc.get("signal_ids", [])),
            "assignment_count":   len(data_store.resource_assignments.get(inc_id, [])),
            "has_simulation":     inc_id in data_store.simulations,
            "notification_count": sum(
                1 for n in data_store.notifications.values()
                if n.get("incident_id") == inc_id
            ),
        })

    return {
        "success": True,
        "data":    enriched,
        "meta": {
            "total":   len(list(data_store.incidents.values())),
            "filtered": len(incidents),
            "limit":   limit,
            "offset":  offset,
            "returned": len(enriched),
        },
        "timestamp": _now(),
    }


# ─────────────────────────────────────────────────
# GET /incidents/{incident_id}
# ─────────────────────────────────────────────────
@router.get("/{incident_id}")
async def get_incident(incident_id: str):
    """
    Full incident detail — everything the Incident Detail screen needs.

    Returns the base incident enriched with:
      - signals        (full signal objects)
      - severity_prediction
      - resource_assignments
      - simulation
      - notifications  (draft/sent messages)
      - traces         (agent trace entries for this incident)
    """
    incident = data_store.incidents.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found")

    # Attach related entities
    signals = [
        s for s in data_store.signals
        if s["id"] in incident.get("signal_ids", [])
    ]
    assignments = data_store.resource_assignments.get(incident_id, [])
    severity_pred = data_store.severity_predictions.get(incident_id)
    simulation    = data_store.simulations.get(incident_id)
    notifications = [
        n for n in data_store.notifications.values()
        if n.get("incident_id") == incident_id
    ]
    traces = [
        t for t in data_store.traces
        if t.get("incident_id") == incident_id
    ]

    return {
        "success": True,
        "data": {
            **incident,
            "signals":             signals,
            "severity_prediction": severity_pred,
            "resource_assignments": assignments,
            "simulation":          simulation,
            "notifications":       notifications,
            "traces":              traces,
            "signal_count":        len(signals),
            "assignment_count":    len(assignments),
        },
        "timestamp": _now(),
    }


# ─────────────────────────────────────────────────
# POST /incidents/{incident_id}/classify
# ─────────────────────────────────────────────────
class ClassifyRequest(BaseModel):
    use_llm:                       bool = False
    include_alternate_hypotheses:  bool = True
    human_review_required_if_conflict: bool = True

@router.post("/{incident_id}/classify")
async def classify_incident(incident_id: str, body: ClassifyRequest):
    """
    Run or re-run crisis classification on an incident.
    Uses deterministic rule-based logic (no LLM required for demo).
    """
    incident = data_store.incidents.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found")

    signal_count = len(incident.get("signal_ids", []))
    if signal_count < 1:
        raise HTTPException(status_code=422, detail="Insufficient signals for classification")

    wf_id = _uid("wf_")
    primary_type  = incident.get("primary_type", "unknown")
    confidence    = incident.get("confidence", 0.5)
    alt_hyp       = incident.get("alternate_hypotheses", [])
    human_review  = (
        body.human_review_required_if_conflict
        and len(alt_hyp) > 0
        and alt_hyp[0].get("confidence", 0) > 0.35
    )

    classification = {
        "id":             _uid("cls_"),
        "incident_id":    incident_id,
        "class_type":     primary_type,
        "sub_type":       incident.get("sub_type"),
        "confidence":     confidence,
        "confidence_factors": {
            "source_credibility":    round(confidence * 0.90, 2),
            "geo_confidence":        round(confidence * 1.08, 2),
            "urgency":               0.88,
            "signal_velocity":       0.75,
            "corroboration":         round(confidence * 1.15, 2),
            "duplicate_cluster":     0.10,
            "media_attached":        0.60,
            "contradiction_penalty": -0.15 if alt_hyp else 0.0,
            "staleness_penalty":     -0.05,
        },
        "is_primary":              True,
        "evidence":                [s["normalized_text"][:100] for s in data_store.signals
                                    if s["id"] in incident.get("signal_ids", [])][:3],
        "alternate_hypotheses":    alt_hyp,
        "human_review_required":   human_review,
        "created_by_agent":        "ClassificationAgent",
        "created_at":              _now(),
    }

    # Store classification under incident_id
    data_store.classifications.setdefault(incident_id, [])
    data_store.classifications[incident_id].append(classification)

    # Update incident human_review_required
    data_store.incidents[incident_id]["human_review_required"] = human_review
    data_store.incidents[incident_id]["updated_at"] = _now()

    _trace(
        wf_id, incident_id,
        "ClassificationAgent", "reclassify_on_demand",
        f"Re-classification requested. use_llm={body.use_llm}. Signals: {signal_count}",
        f"PRIMARY: {primary_type} ({confidence:.2f}). "
        + (f"ALTERNATE: {alt_hyp[0]['type']} ({alt_hyp[0]['confidence']:.2f}). "
           if alt_hyp else "No alternates. ")
        + f"Human review {'REQUIRED' if human_review else 'not required'}.",
        tool_calls=["classify_crisis_type()", "check_review_threshold()"],
        human_review_required=human_review,
        duration_ms=66,
    )

    return {
        "success": True,
        "data":    classification,
        "timestamp": _now(),
        "trace_id":  data_store.traces[-1]["id"],
    }


# ─────────────────────────────────────────────────
# POST /incidents/{incident_id}/predict-severity
# ─────────────────────────────────────────────────
class SeverityRequest(BaseModel):
    include_spread_risk: bool = True

@router.post("/{incident_id}/predict-severity")
async def predict_severity(incident_id: str, body: SeverityRequest):
    """
    Run or re-run severity prediction on an incident.
    Returns the full SeverityPrediction object.
    """
    incident = data_store.incidents.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found")

    if not incident.get("location"):
        raise HTTPException(status_code=422, detail="Missing location — cannot predict severity")

    existing = data_store.severity_predictions.get(incident_id)
    if existing:
        return {
            "success": True,
            "data":    existing,
            "message": "Returning existing severity prediction.",
            "timestamp": _now(),
        }

    # Derive severity from incident data
    severity_map = {"CRITICAL": "CRITICAL", "HIGH": "HIGH", "MEDIUM": "MEDIUM", "LOW": "LOW"}
    severity = severity_map.get(incident.get("severity", "MEDIUM"), "MEDIUM")

    prediction = {
        "id":                  _uid("sev_"),
        "incident_id":         incident_id,
        "severity":            severity,
        "radius_m":            incident["location"].get("radius_m", 500),
        "population_affected": incident.get("affected_population_estimate", 0),
        "duration_min":        incident.get("expected_duration_min", 60),
        "peak_impact_min":     incident.get("peak_impact_min", 30),
        "spread_risk":         "HIGH" if severity == "CRITICAL" else "MEDIUM",
        "vulnerability_score": 0.91 if "katchi" in incident.get("location", {}).get("area", "").lower() else 0.62,
        "confidence":          incident.get("confidence", 0.7),
        "created_by_agent":    "SeverityPredictionAgent",
        "created_at":          _now(),
    }
    data_store.severity_predictions[incident_id] = prediction

    wf_id = _uid("wf_")
    _trace(
        wf_id, incident_id,
        "SeverityPredictionAgent", "predict_on_demand",
        f"Severity prediction requested. include_spread_risk={body.include_spread_risk}",
        f"Severity: {severity}. Radius: {prediction['radius_m']}m. "
        f"Population: {prediction['population_affected']}. "
        f"Spread risk: {prediction['spread_risk']}.",
        tool_calls=["predict_severity()", "estimate_population()", "score_vulnerability()"],
        duration_ms=55,
    )

    return {
        "success": True,
        "data":    prediction,
        "timestamp": _now(),
        "trace_id":  data_store.traces[-1]["id"],
    }


# ─────────────────────────────────────────────────
# PATCH /incidents/{incident_id}/status
# ─────────────────────────────────────────────────
class StatusUpdate(BaseModel):
    status: str
    actor:  Optional[str] = "operator"

VALID_STATUSES = {"candidate", "active", "needs_human_review", "verified", "reclassified", "resolved"}

@router.patch("/{incident_id}/status")
async def update_incident_status(incident_id: str, body: StatusUpdate):
    """Update an incident's status. Used for operator approve/verify actions."""
    incident = data_store.incidents.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found")

    if body.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status '{body.status}'")

    old_status = incident.get("status")
    data_store.incidents[incident_id]["status"] = body.status
    data_store.incidents[incident_id]["updated_at"] = _now()

    data_store.audit_logs.append({
        "id":          _uid("audit_"),
        "entity_type": "incident",
        "entity_id":   incident_id,
        "action":      "status_updated",
        "actor_type":  "human",
        "actor_id":    body.actor,
        "before":      {"status": old_status},
        "after":       {"status": body.status},
        "timestamp":   _now(),
    })

    return {
        "success": True,
        "data":    data_store.incidents[incident_id],
        "message": f"Status updated: {old_status} → {body.status}",
        "timestamp": _now(),
    }
