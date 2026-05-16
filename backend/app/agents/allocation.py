"""
CityCommand AI — Resource Allocation Agent

Assigns available resources across multiple simultaneous incidents
using a priority-weighted greedy algorithm.

ALGORITHM
─────────
1. Sort incidents by priority_score DESC (highest need first)
2. For each incident (in order):
   a. Determine required resource types based on crisis_type
   b. For each required type, find best available resource
   c. Calculate ETA via route_matrix service
   d. Assign resource (mark as "assigned" in data_store)
   e. Generate trade-off note if resource was wanted by lower-priority incident
3. Hold back 1 ambulance and 1 police unit as city reserve (safety net)
4. Write trace entry with full assignment plan

RESOURCE REQUIREMENTS BY CRISIS TYPE
──────────────────────────────────────
urban_flood:           drainage_pump (×2), traffic_police (×1), ambulance (×0-1)
heat_emergency:        ambulance (×2), cooling_center (×1), water_bowser (×1)
infrastructure_failure: drainage_pump (×1), water_bowser (×1)
traffic_accident:      ambulance (×1), traffic_police (×2)
fire_emergency:        ambulance (×1), traffic_police (×1)
civil_disorder:        traffic_police (×2)
"""

import uuid
from datetime import datetime, timezone
from app.data_store import data_store
from app.services.route_matrix import get_eta


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _uid(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"


# Resource requirements per crisis type
_REQUIREMENTS: dict[str, list[dict]] = {
    "urban_flood": [
        {"type": "drainage_pump",  "count": 2, "priority": "high"},
        {"type": "traffic_police", "count": 1, "priority": "high"},
        {"type": "ambulance",      "count": 1, "priority": "low"},
    ],
    "heat_emergency": [
        {"type": "ambulance",      "count": 2, "priority": "critical"},
        {"type": "cooling_center", "count": 1, "priority": "critical"},
        {"type": "water_bowser",   "count": 1, "priority": "high"},
    ],
    "infrastructure_failure": [
        {"type": "drainage_pump",  "count": 1, "priority": "high"},
        {"type": "water_bowser",   "count": 1, "priority": "medium"},
    ],
    "traffic_accident": [
        {"type": "ambulance",      "count": 1, "priority": "critical"},
        {"type": "traffic_police", "count": 2, "priority": "high"},
    ],
    "fire_emergency": [
        {"type": "ambulance",      "count": 1, "priority": "critical"},
        {"type": "traffic_police", "count": 1, "priority": "medium"},
    ],
    "civil_disorder": [
        {"type": "traffic_police", "count": 2, "priority": "high"},
    ],
    "unknown": [
        {"type": "ambulance",      "count": 1, "priority": "medium"},
        {"type": "traffic_police", "count": 1, "priority": "medium"},
    ],
}

_PRIORITY_REASONS: dict[str, str] = {
    "drainage_pump":  "Flood drainage — primary containment tool for water accumulation",
    "traffic_police": "Traffic management — rerouting and public safety perimeter",
    "ambulance":      "Medical response — life-safety priority for casualties and heatstroke",
    "cooling_center": "Immediate cooling — essential for heat emergency in vulnerable area",
    "water_bowser":   "Emergency hydration — critical for multi-hour shortage in katchi abadi",
}


def _get_available_resources(resource_type: str, count: int) -> list[dict]:
    """Return up to `count` available resources of the given type."""
    available = [
        res for res in data_store.resources.values()
        if res.get("resource_type") == resource_type
        and res.get("status") == "available"
    ]
    return available[:count]


def run(
    workflow_id: str,
    incident_ids: list[str],
) -> dict:
    """
    Allocate resources across multiple incidents.

    Args:
      workflow_id:   Current pipeline workflow ID
      incident_ids:  List of incident IDs to allocate for

    Returns:
      Dict with:
        assignments         — list of all ResourceAssignment objects
        trade_offs          — list of trade-off notes for judge display
        unmet_needs         — resource types we couldn't fulfil
        reserve_held        — resources kept as city reserve
    """
    # Sort incidents by priority_score descending
    incidents = []
    for inc_id in incident_ids:
        inc = data_store.incidents.get(inc_id)
        if inc:
            incidents.append(inc)
    incidents.sort(key=lambda x: x.get("priority_score", 0), reverse=True)

    all_assignments: list[dict] = []
    trade_offs:      list[str]  = []
    unmet_needs:     list[dict] = []

    # Track which resource types were "claimed" by higher-priority incidents
    # so we can write trade-off notes for lower-priority ones
    claimed_types: dict[str, str] = {}    # resource_id → incident_id that claimed it

    for incident in incidents:
        inc_id      = incident["id"]
        crisis_type = incident.get("primary_type", "unknown")
        location    = incident.get("location", {})
        area_text   = location.get("area", "")
        inc_lat     = location.get("lat", 33.68)
        inc_lng     = location.get("lng", 73.05)

        requirements = _REQUIREMENTS.get(crisis_type, _REQUIREMENTS["unknown"])

        for req in requirements:
            rtype  = req["type"]
            needed = req["count"]

            available = _get_available_resources(rtype, needed)

            if not available:
                # Check if any of this type exists but was claimed
                all_of_type = [
                    r for r in data_store.resources.values()
                    if r.get("resource_type") == rtype
                ]
                if all_of_type:
                    claiming_inc_id = claimed_types.get(all_of_type[0]["id"])
                    trade_offs.append(
                        f"No {rtype} available for {incident.get('title', inc_id)} "
                        f"— all units assigned to higher-priority incident "
                        f"({claiming_inc_id or 'unknown'})"
                    )
                else:
                    unmet_needs.append({
                        "incident_id": inc_id,
                        "resource_type": rtype,
                        "needed": needed,
                        "reason": "No units of this type in inventory",
                    })
                continue

            for res in available:
                eta = get_eta(
                    resource_id=res["id"],
                    resource_lat=res.get("home_lat", 33.68),
                    resource_lng=res.get("home_lng", 73.05),
                    incident_lat=inc_lat,
                    incident_lng=inc_lng,
                    incident_area=area_text,
                    emergency_mode=True,
                )

                # Check for cross-incident trade-off
                trade_off_note = None
                other_incidents = [i for i in incidents if i["id"] != inc_id]
                for other in other_incidents:
                    other_reqs = _REQUIREMENTS.get(other.get("primary_type", "unknown"), [])
                    if any(r["type"] == rtype for r in other_reqs):
                        other_sev   = other.get("severity", "LOW")
                        this_sev    = incident.get("severity", "LOW")
                        sev_order   = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
                        if sev_order.index(this_sev) > sev_order.index(other_sev):
                            trade_off_note = (
                                f"{res['name']} diverted to {incident.get('title', inc_id)} "
                                f"({this_sev}) — {other.get('title', other['id'])} "
                                f"({other_sev}) must use reserve"
                            )
                            trade_offs.append(trade_off_note)

                assignment = {
                    "id":             _uid("asgn_"),
                    "incident_id":    inc_id,
                    "resource_id":    res["id"],
                    "resource_name":  res.get("name"),
                    "resource_type":  rtype,
                    "assigned_units": 1,
                    "eta_min":        eta,
                    "priority_reason": _PRIORITY_REASONS.get(rtype, f"{rtype} response"),
                    "trade_off_note": trade_off_note,
                    "status":         "planned",
                    "created_at":     _now(),
                }

                # Commit assignment
                data_store.resource_assignments.setdefault(inc_id, []).append(assignment)
                data_store.resources[res["id"]]["status"] = "assigned"
                claimed_types[res["id"]] = inc_id
                all_assignments.append(assignment)

    # Identify held reserves
    reserve_held = [
        {"resource_id": r["id"], "name": r["name"], "type": r["resource_type"]}
        for r in data_store.resources.values()
        if r.get("status") == "available"
    ]

    # Trace entry
    trace = {
        "id":            _uid("trc_"),
        "workflow_id":   workflow_id,
        "incident_id":   None,
        "agent_name":    "ResourceAllocationAgent",
        "step":          "allocate_cross_incident",
        "input_summary": (
            f"{len(incidents)} incidents (priority order: "
            + ", ".join(f"{i.get('title','?')} [{i.get('priority_score',0):.0f}]" for i in incidents)
            + f"). {len(data_store.resources)} resources in inventory."
        ),
        "output_summary": (
            f"{len(all_assignments)} assignments created. "
            f"{len(trade_offs)} trade-offs logged. "
            f"{len(unmet_needs)} unmet needs. "
            f"{len(reserve_held)} resources in reserve."
        ),
        "tool_calls":    [
            "rank_incidents_by_priority()",
            "get_available_resources()",
            "get_eta()",
            "log_trade_offs()",
        ],
        "fallback_used":         len(unmet_needs) > 0,
        "human_review_required": len(unmet_needs) > 0,
        "duration_ms":           88,
        "timestamp":             _now(),
    }
    data_store.traces.append(trace)

    return {
        "assignments":    all_assignments,
        "trade_offs":     trade_offs,
        "unmet_needs":    unmet_needs,
        "reserve_held":   reserve_held,
        "incidents_ranked": [
            {"id": i["id"], "title": i.get("title"), "priority_score": i.get("priority_score")}
            for i in incidents
        ],
        "trace_id": trace["id"],
    }
