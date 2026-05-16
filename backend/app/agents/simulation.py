"""
CityCommand AI — Simulation Agent

Simulates the before/after impact of an action plan on an incident.
Takes a list of response actions and computes:
  - Before state (current crisis metrics)
  - After state (projected metrics post-response)
  - Per-metric deltas with improved/worsened flags
  - Side effects (unintended consequences)
  - Cost estimate (PKR)
  - Risk if delayed (text description)

SUPPORTED ACTIONS
─────────────────
traffic_reroute         Close congested road, redirect via alternate routes
emergency_dispatch      Send emergency units to incident site
public_alert            Broadcast public warning message
deploy_pump             Activate drainage pumps at flood site
cooling_station         Open mobile cooling tent for heat victims
water_supply            Deploy water bowser for emergency hydration
utility_inspection      Send utility crew to inspect infrastructure
field_verification      Deploy field team to verify and report back

ACTION EFFECTS MODEL
────────────────────
Each action contributes delta improvements to a set of metrics.
Deltas are additive — multiple actions combine for greater effect.
Side effects are drawn from a predefined impact matrix.
"""

import uuid
from datetime import datetime, timezone
from app.data_store import data_store


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _uid(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"


# ─────────────────────────────────────────────────
# Action effect definitions
# Each action → dict of metric improvements + side_effects
# ─────────────────────────────────────────────────
_ACTION_EFFECTS: dict[str, dict] = {
    "traffic_reroute": {
        "congestion_reduction":     0.55,   # fraction reduction
        "emergency_eta_reduction":  0.60,
        "evacuation_improvement":   0.30,
        "cost_pkr":                 15_000,
        "side_effects": [
            "Alternate routes may experience 15–20% congestion increase",
            "Rerouting takes ~8 min to propagate across signal network",
        ],
    },
    "emergency_dispatch": {
        "emergency_eta_reduction":  0.70,
        "medical_response_boost":   0.80,
        "cost_pkr":                 40_000,
        "side_effects": [
            "Adjacent sectors temporarily lose ambulance standby coverage",
        ],
    },
    "public_alert": {
        "evacuation_improvement":   0.50,
        "population_at_risk_reduction": 0.25,
        "cost_pkr":                 2_000,
        "side_effects": [
            "Alert may cause panic — traffic may spike temporarily",
            "Requires human approval before broadcast",
        ],
    },
    "deploy_pump": {
        "flood_area_reduction":     0.65,
        "congestion_reduction":     0.20,
        "evacuation_improvement":   0.40,
        "cost_pkr":                 75_000,
        "side_effects": [
            "Pump deployment vehicle occupies one lane during setup (~8 min)",
            "Drainage may overflow at downstream junction if not cleared",
        ],
    },
    "cooling_station": {
        "heat_risk_reduction":      0.55,
        "population_at_risk_reduction": 0.45,
        "hospitals_notified_add":   2,
        "cost_pkr":                 35_000,
        "side_effects": [
            "Cooling tent capacity: 50 persons — may fill within 90 min",
            "Second unit request recommended if population > 500",
        ],
    },
    "water_supply": {
        "heat_risk_reduction":      0.25,
        "population_at_risk_reduction": 0.20,
        "cost_pkr":                 18_000,
        "side_effects": [
            "Bowser refill needed every 4 hours — coordinate with utility",
        ],
    },
    "utility_inspection": {
        "flood_area_reduction":     0.10,
        "cost_pkr":                 8_000,
        "side_effects": [
            "Inspection crew may need road closure at service lane",
        ],
    },
    "field_verification": {
        "cost_pkr":                 5_000,
        "side_effects": [
            "Field report may trigger reclassification (alternate hypothesis confirmed)",
            "Adds ~20 min before classification update propagates",
        ],
    },
}

# ─────────────────────────────────────────────────
# Before-state templates by crisis type
# ─────────────────────────────────────────────────
_BEFORE_STATE_TEMPLATES: dict[str, dict] = {
    "urban_flood": {
        "congestion_level":      "SEVERE",
        "congestion_score":      0.90,
        "emergency_eta_min":     28,
        "flood_area_sqm":        14_000,
        "evacuation_possible":   False,
        "population_at_risk":    8_500,
        "hospitals_notified":    0,
        "heat_risk_level":       None,
    },
    "heat_emergency": {
        "congestion_level":      "MODERATE",
        "congestion_score":      0.45,
        "emergency_eta_min":     40,
        "flood_area_sqm":        None,
        "evacuation_possible":   True,
        "population_at_risk":    3_200,
        "hospitals_notified":    0,
        "heat_risk_level":       "EXTREME",
        "heat_risk_score":       0.95,
    },
    "infrastructure_failure": {
        "congestion_level":      "HIGH",
        "congestion_score":      0.65,
        "emergency_eta_min":     22,
        "flood_area_sqm":        5_000,
        "evacuation_possible":   True,
        "population_at_risk":    2_000,
        "hospitals_notified":    0,
        "heat_risk_level":       None,
    },
    "unknown": {
        "congestion_level":      "MODERATE",
        "congestion_score":      0.50,
        "emergency_eta_min":     20,
        "flood_area_sqm":        None,
        "evacuation_possible":   True,
        "population_at_risk":    1_000,
        "hospitals_notified":    0,
        "heat_risk_level":       None,
    },
}

_CONGESTION_LABELS = ["CLEAR", "LOW", "MODERATE", "HIGH", "SEVERE"]


def _score_to_label(score: float) -> str:
    idx = min(int(score * (len(_CONGESTION_LABELS) - 1)), len(_CONGESTION_LABELS) - 1)
    return _CONGESTION_LABELS[idx]


def _compute_after_state(
    before: dict, actions: list[str]
) -> tuple[dict, list[dict], list[str], int]:
    """
    Apply all action effects to the before state.
    Returns: (after_state, deltas, side_effects, total_cost_pkr)
    """
    after = {**before}
    all_side_effects: list[str] = []
    total_cost       = 0

    # Aggregate all deltas from actions
    congestion_red    = 0.0
    eta_red           = 0.0
    evac_boost        = 0.0
    flood_red         = 0.0
    heat_red          = 0.0
    pop_risk_red      = 0.0
    hosp_add          = 0
    med_boost         = 0.0

    for action in actions:
        fx = _ACTION_EFFECTS.get(action, {})
        congestion_red   += fx.get("congestion_reduction",          0.0)
        eta_red          += fx.get("emergency_eta_reduction",       0.0)
        evac_boost       += fx.get("evacuation_improvement",        0.0)
        flood_red        += fx.get("flood_area_reduction",          0.0)
        heat_red         += fx.get("heat_risk_reduction",           0.0)
        pop_risk_red     += fx.get("population_at_risk_reduction",  0.0)
        hosp_add         += fx.get("hospitals_notified_add",        0)
        med_boost        += fx.get("medical_response_boost",        0.0)
        total_cost       += fx.get("cost_pkr",                      0)
        all_side_effects += fx.get("side_effects",                  [])

    # Cap reductions at 90% (nothing goes to zero)
    congestion_red  = min(congestion_red,  0.90)
    eta_red         = min(eta_red,         0.90)
    flood_red       = min(flood_red,       0.90)
    heat_red        = min(heat_red,        0.90)
    pop_risk_red    = min(pop_risk_red,    0.80)
    evac_boost      = min(evac_boost,      1.00)

    # Apply to after state
    before_cong_score = before.get("congestion_score", 0.5)
    after_cong_score  = max(0.05, before_cong_score * (1 - congestion_red))
    after["congestion_score"] = round(after_cong_score, 2)
    after["congestion_level"] = _score_to_label(after_cong_score)

    before_eta = before.get("emergency_eta_min", 20)
    after["emergency_eta_min"] = max(3, int(before_eta * (1 - eta_red)))

    if before.get("flood_area_sqm") is not None:
        after["flood_area_sqm"] = max(0, int(before["flood_area_sqm"] * (1 - flood_red)))

    if before.get("heat_risk_level") is not None:
        before_heat = before.get("heat_risk_score", 0.9)
        after_heat  = max(0.1, before_heat * (1 - heat_red))
        after["heat_risk_score"] = round(after_heat, 2)
        heat_labels = ["LOW", "MODERATE", "HIGH", "EXTREME"]
        after["heat_risk_level"] = heat_labels[min(int(after_heat * 3.99), 3)]

    before_pop = before.get("population_at_risk", 1000)
    after["population_at_risk"] = max(50, int(before_pop * (1 - pop_risk_red)))

    after["hospitals_notified"] = before.get("hospitals_notified", 0) + hosp_add

    if evac_boost > 0:
        after["evacuation_possible"] = True

    # Build deltas list
    deltas: list[dict] = []
    metric_labels = {
        "congestion_level":    "Congestion Level",
        "emergency_eta_min":   "Emergency ETA (min)",
        "flood_area_sqm":      "Flood Area (m²)",
        "population_at_risk":  "Population at Risk",
        "hospitals_notified":  "Hospitals Notified",
        "heat_risk_level":     "Heat Risk Level",
        "evacuation_possible": "Evacuation Possible",
    }
    for key, label in metric_labels.items():
        b_val = before.get(key)
        a_val = after.get(key)
        if b_val is None and a_val is None:
            continue
        # Determine if improved (lower is better for most numeric metrics)
        if isinstance(b_val, bool):
            improved = a_val and not b_val
        elif isinstance(b_val, (int, float)) and key not in ("hospitals_notified",):
            improved = a_val < b_val
        else:
            improved = a_val != b_val
        deltas.append({
            "metric":   label,
            "key":      key,
            "before":   b_val,
            "after":    a_val,
            "improved": improved,
        })

    return after, deltas, list(dict.fromkeys(all_side_effects)), total_cost


def run(
    workflow_id: str,
    incident_id: str,
    actions: list[str],
) -> dict:
    """
    Run the simulation agent for a single incident.

    Args:
      workflow_id:  Current pipeline workflow ID
      incident_id:  ID of the incident to simulate
      actions:      List of action strings (e.g. ["deploy_pump", "traffic_reroute"])

    Returns:
      A simulation dict stored in data_store.simulations[incident_id]
    """
    incident    = data_store.incidents.get(incident_id, {})
    crisis_type = incident.get("primary_type", "unknown")

    # Get or build before state
    existing_sim = data_store.simulations.get(incident_id)
    if existing_sim:
        before_state = existing_sim.get("before_state", {})
    else:
        before_state = dict(
            _BEFORE_STATE_TEMPLATES.get(crisis_type, _BEFORE_STATE_TEMPLATES["unknown"])
        )

    after_state, deltas, side_effects, total_cost = _compute_after_state(before_state, actions)

    # Risk if delayed — based on peak_impact_min
    sev_pred      = data_store.severity_predictions.get(incident_id, {})
    peak_min      = sev_pred.get("peak_impact_min", 30)
    severity      = incident.get("severity", "MEDIUM")
    risk_messages = {
        "CRITICAL": f"Inaction risk: CRITICAL deterioration in {peak_min} min — life-safety threshold",
        "HIGH":     f"Delayed response increases affected population by est. 30% within {peak_min} min",
        "MEDIUM":   f"Situation stable for ~{peak_min * 2} min but escalation risk remains",
        "LOW":      "Low urgency — monitor and reassess in 60 min",
    }
    risk_if_delayed = risk_messages.get(severity, risk_messages["MEDIUM"])

    simulation = {
        "id":                _uid("sim_"),
        "incident_id":       incident_id,
        "action_plan":       actions,
        "before_state":      before_state,
        "after_state":       after_state,
        "deltas":            deltas,
        "side_effects":      side_effects,
        "cost_estimate_pkr": total_cost,
        "risk_if_delayed":   risk_if_delayed,
        "created_by_agent":  "SimulationAgent",
        "created_at":        _now(),
    }
    data_store.simulations[incident_id] = simulation

    # Improvements count for trace summary
    improved = sum(1 for d in deltas if d["improved"])
    worsened = sum(1 for d in deltas if not d["improved"] and d["before"] != d["after"])

    trace = {
        "id":            _uid("trc_"),
        "workflow_id":   workflow_id,
        "incident_id":   incident_id,
        "agent_name":    "SimulationAgent",
        "step":          f"simulate_{crisis_type}_response",
        "input_summary": (
            f"Actions: {actions}. "
            f"Crisis: {crisis_type}, Severity: {severity}."
        ),
        "output_summary": (
            f"{len(deltas)} metrics simulated: {improved} improved, {worsened} worsened. "
            f"{len(side_effects)} side effects identified. "
            f"Cost estimate: PKR {total_cost:,}. "
            f"Risk if delayed: {risk_if_delayed[:60]}..."
        ),
        "tool_calls":    [
            "compute_after_state()",
            "apply_action_effects()",
            "compute_deltas()",
            "estimate_side_effects()",
        ],
        "fallback_used":         crisis_type == "unknown",
        "human_review_required": False,
        "duration_ms":           95,
        "timestamp":             _now(),
    }
    data_store.traces.append(trace)

    return {**simulation, "trace_id": trace["id"]}
