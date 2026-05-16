"""
CityCommand AI — Demo Scenario Route

POST /demo/run-scenario
  The "big red button" for the hackathon demo.
  Loads seed signals + resources, then runs the full
  deterministic agent pipeline to produce:
    • 2 incidents (G-10 flooding, F-11 heat emergency)
    • Classifications with alternate hypotheses
    • Severity predictions
    • Resource allocations with trade-off notes
    • Simulation before/after states
    • Stakeholder notification drafts (7 audiences)
    • 12+ agent trace entries
    • Audit log

POST /demo/reset
  Wipes the data store back to empty state.

GET /demo/status
  Returns whether the demo has been loaded.
"""

import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException

from app.data_store import data_store
from app.services.seed_loader import load_seed_scenario

router = APIRouter()


# ─────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────
def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _uid(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"

def _trace(
    workflow_id: str,
    incident_id: str | None,
    agent_name: str,
    step: str,
    input_summary: str,
    output_summary: str,
    tool_calls: list[str] | None = None,
    fallback_used: bool = False,
    human_review_required: bool = False,
    duration_ms: int = 0,
):
    entry = {
        "id": _uid("trc_"),
        "workflow_id": workflow_id,
        "incident_id": incident_id,
        "agent_name": agent_name,
        "step": step,
        "input_summary": input_summary,
        "output_summary": output_summary,
        "tool_calls": tool_calls or [],
        "fallback_used": fallback_used,
        "human_review_required": human_review_required,
        "duration_ms": duration_ms,
        "timestamp": _now(),
    }
    data_store.traces.append(entry)
    return entry


# ─────────────────────────────────────────────────
# POST /demo/run-scenario
# ─────────────────────────────────────────────────
@router.post("/run-scenario")
async def run_demo_scenario():
    """
    Load and run the full G-10 Flood + F-11 Heat Emergency demo.

    This is the single endpoint that powers the entire 3-5 minute
    hackathon demo. It deterministically produces every data object
    the mobile app needs to display.
    """

    # Prevent double-loading without a reset
    if data_store.demo_loaded:
        raise HTTPException(
            status_code=409,
            detail="Demo already loaded. Call POST /demo/reset first."
        )

    workflow_id = _uid("wf_")

    # ── Step 1: Signal Intake Agent ───────────────────────
    seed_result = load_seed_scenario()
    _trace(
        workflow_id, None,
        "SignalIntakeAgent", "ingest_seed_signals",
        "Pulling signals from scenario G-10 / Heat seed file",
        f"Loaded {seed_result['signals_loaded']} signals from 4 source types "
        f"({seed_result['resources_loaded']} resources registered)",
        tool_calls=["seed_loader.load_seed_scenario()", "data_store.signals.append()"],
        duration_ms=38,
    )

    # ── Step 2: Signal Cleaning Agent ─────────────────────
    flood_signal_ids = [s["id"] for s in data_store.signals if "g-10" in (s.get("location_text","")).lower() or "g10" in (s.get("location_text","")).lower() or "kashmir" in (s.get("location_text","")).lower()]
    heat_signal_ids  = [s["id"] for s in data_store.signals if "f-11" in (s.get("location_text","")).lower() or "f11" in (s.get("location_text","")).lower()]

    _trace(
        workflow_id, None,
        "SignalCleaningAgent", "normalize_and_cluster",
        f"{seed_result['signals_loaded']} raw signals received",
        f"Normalized text, stripped PII, translated Roman Urdu. "
        f"Clustered into 2 geographic groups: G-10 ({len(flood_signal_ids)} signals), "
        f"F-11 ({len(heat_signal_ids)} signals). No spam detected.",
        tool_calls=["normalize_text()", "cluster_by_geohash()", "detect_duplicates()"],
        duration_ms=52,
    )

    # ── Step 3: Geolocation Agent ─────────────────────────
    _trace(
        workflow_id, None,
        "GeolocationAgent", "extract_coordinates",
        "2 signal clusters: G-10 Islamabad, F-11 Katchi Abadi",
        "G-10 centroid: (33.6844, 73.0479) • F-11 centroid: (33.6700, 73.0290). "
        "Both centroids have geo_confidence > 0.82.",
        tool_calls=["infer_coords_from_text()", "validate_within_city_bounds()"],
        duration_ms=29,
    )

    # ── Step 4: Create Incidents ───────────────────────────
    flood_inc_id = _uid("inc_")
    heat_inc_id  = _uid("inc_")
    now = _now()

    flood_incident = {
        "id":           flood_inc_id,
        "title":        "G-10 Probable Urban Flooding",
        "primary_type": "urban_flood",
        "sub_type":     "residential_road_flooding",
        "alternate_hypotheses": [
            {"type": "water_main_burst", "confidence": 0.41, "reason": "Localized inundation pattern + sewage smell reported"},
        ],
        "severity":     "HIGH",
        "confidence":   0.78,
        "priority_score": 87.4,
        "location": {
            "area":     "G-10, Islamabad",
            "lat":      33.6844,
            "lng":      73.0479,
            "radius_m": 1200,
        },
        "affected_population_estimate": 8500,
        "expected_duration_min": 180,
        "peak_impact_min": 45,
        "status":       "needs_human_review",
        "human_review_required": True,
        "signal_ids":   flood_signal_ids,
        "created_at":   now,
        "updated_at":   now,
    }
    heat_incident = {
        "id":           heat_inc_id,
        "title":        "F-11 Critical Heat Emergency",
        "primary_type": "heat_emergency",
        "sub_type":     "prolonged_power_outage_heat",
        "alternate_hypotheses": [],
        "severity":     "CRITICAL",
        "confidence":   0.91,
        "priority_score": 92.1,
        "location": {
            "area":     "F-11 Katchi Abadi, Islamabad",
            "lat":      33.6700,
            "lng":      73.0290,
            "radius_m": 600,
        },
        "affected_population_estimate": 3200,
        "expected_duration_min": 240,
        "peak_impact_min": 30,
        "status":       "active",
        "human_review_required": False,
        "signal_ids":   heat_signal_ids,
        "created_at":   now,
        "updated_at":   now,
    }
    data_store.incidents[flood_inc_id] = flood_incident
    data_store.incidents[heat_inc_id]  = heat_incident

    # ── Step 5: Credibility Scoring Agent ─────────────────
    _trace(
        workflow_id, flood_inc_id,
        "CredibilityScoringAgent", "score_g10_cluster",
        f"5 signals for G-10 cluster (social×2, traffic×1, weather×1, calls×1)",
        "Confidence: 0.78 | Factors: source_credibility=0.72, geo=0.85, "
        "velocity=0.80, corroboration=0.90, media_attached=0.60, "
        "contradiction_penalty=−0.15 (sewage smell conflicts with rain hypothesis). "
        "Alternate hypothesis flagged: water_main_burst (0.41).",
        tool_calls=["score_credibility()", "detect_contradiction()", "flag_alternate_hypothesis()"],
        human_review_required=True,
        duration_ms=71,
    )
    _trace(
        workflow_id, heat_inc_id,
        "CredibilityScoringAgent", "score_f11_cluster",
        f"3 signals for F-11 cluster (social×1, calls×1, sensor×1)",
        "Confidence: 0.91 | Factors: source_credibility=0.85, geo=0.90, "
        "urgency=0.95, corroboration=0.88, sensor_temp=46.5°C (anomaly confirmed). "
        "No contradictions detected. High vulnerability area (katchi abadi).",
        tool_calls=["score_credibility()", "check_vulnerability_index()"],
        duration_ms=55,
    )

    # ── Step 6: Crisis Classification Agent ───────────────
    _trace(
        workflow_id, flood_inc_id,
        "ClassificationAgent", "classify_g10",
        "Input: 5 corroborated signals, geo_cluster=G-10, confidence=0.78",
        "PRIMARY: urban_flood (0.78). ALTERNATE: water_main_burst (0.41). "
        "Human review REQUIRED due to conflicting inundation pattern. "
        "Rule: if |primary_conf − alternate_conf| < 0.40, flag for review.",
        tool_calls=["classify_crisis_type()", "generate_alternate_hypotheses()", "check_review_threshold()"],
        fallback_used=False,
        human_review_required=True,
        duration_ms=88,
    )
    _trace(
        workflow_id, heat_inc_id,
        "ClassificationAgent", "classify_f11",
        "Input: 3 corroborated signals, sensor_temp=46.5°C, power_outage=True",
        "PRIMARY: heat_emergency (0.91). No credible alternate. "
        "Classified as CRITICAL without human review (confidence > 0.85 threshold).",
        tool_calls=["classify_crisis_type()", "check_auto_escalate_threshold()"],
        duration_ms=62,
    )

    # ── Step 7: Severity Prediction Agent ─────────────────
    data_store.severity_predictions[flood_inc_id] = {
        "id": _uid("sev_"), "incident_id": flood_inc_id,
        "severity": "HIGH", "radius_m": 1200,
        "population_affected": 8500, "duration_min": 180,
        "peak_impact_min": 45, "spread_risk": "MEDIUM",
        "vulnerability_score": 0.62, "confidence": 0.78,
        "created_by_agent": "SeverityPredictionAgent", "created_at": now,
    }
    data_store.severity_predictions[heat_inc_id] = {
        "id": _uid("sev_"), "incident_id": heat_inc_id,
        "severity": "CRITICAL", "radius_m": 600,
        "population_affected": 3200, "duration_min": 240,
        "peak_impact_min": 30, "spread_risk": "HIGH",
        "vulnerability_score": 0.91, "confidence": 0.91,
        "created_by_agent": "SeverityPredictionAgent", "created_at": now,
    }
    _trace(
        workflow_id, None,
        "SeverityPredictionAgent", "predict_both_incidents",
        "Both incidents classified; running severity models",
        "G-10: HIGH severity, 8,500 people, 180 min, spread_risk=MEDIUM. "
        "F-11: CRITICAL severity, 3,200 people, 240 min, spread_risk=HIGH (katchi abadi vulnerability=0.91). "
        "F-11 ranked #1 by priority despite smaller footprint (vulnerability × severity).",
        tool_calls=["predict_severity()", "estimate_population()", "score_vulnerability()"],
        duration_ms=94,
    )

    # ── Step 8: Resource Allocation Agent ─────────────────
    assignments = [
        {"id": _uid("asgn_"), "incident_id": flood_inc_id,
         "resource_id": "res_pump_01", "resource_name": "High Capacity Pump Alpha",
         "resource_type": "drainage_pump", "assigned_units": 1, "eta_min": 12,
         "priority_reason": "Primary drainage for 1,200m flood radius",
         "trade_off_note": None, "status": "planned", "created_at": now},
        {"id": _uid("asgn_"), "incident_id": flood_inc_id,
         "resource_id": "res_pump_02", "resource_name": "Standard Pump Beta",
         "resource_type": "drainage_pump", "assigned_units": 1, "eta_min": 18,
         "priority_reason": "Secondary drainage support",
         "trade_off_note": None, "status": "planned", "created_at": now},
        {"id": _uid("asgn_"), "incident_id": flood_inc_id,
         "resource_id": "res_cop_01", "resource_name": "Traffic Squad Alpha",
         "resource_type": "traffic_police", "assigned_units": 4, "eta_min": 8,
         "priority_reason": "Reroute blocked Kashmir Highway",
         "trade_off_note": None, "status": "planned", "created_at": now},
        {"id": _uid("asgn_"), "incident_id": heat_inc_id,
         "resource_id": "res_amb_01", "resource_name": "Ambulance Unit 1 (ALS)",
         "resource_type": "ambulance", "assigned_units": 1, "eta_min": 14,
         "priority_reason": "Multiple heatstroke cases require ALS response",
         "trade_off_note": "ALS unit diverted from G-10 standby — G-10 covered by BLS if needed",
         "status": "planned", "created_at": now},
        {"id": _uid("asgn_"), "incident_id": heat_inc_id,
         "resource_id": "res_amb_02", "resource_name": "Ambulance Unit 2 (BLS)",
         "resource_type": "ambulance", "assigned_units": 1, "eta_min": 16,
         "priority_reason": "BLS unit for secondary heat cases",
         "trade_off_note": None, "status": "planned", "created_at": now},
        {"id": _uid("asgn_"), "incident_id": heat_inc_id,
         "resource_id": "res_cool_01", "resource_name": "Mobile Cooling Tent Unit",
         "resource_type": "cooling_center", "assigned_units": 1, "eta_min": 22,
         "priority_reason": "Immediate cooling for 50+ vulnerable residents",
         "trade_off_note": None, "status": "planned", "created_at": now},
        {"id": _uid("asgn_"), "incident_id": heat_inc_id,
         "resource_id": "res_water_01", "resource_name": "Emergency Water Supply Bowser",
         "resource_type": "water_bowser", "assigned_units": 1, "eta_min": 25,
         "priority_reason": "Critical hydration for 6-hour water shortage",
         "trade_off_note": None, "status": "planned", "created_at": now},
    ]
    for asgn in assignments:
        iid = asgn["incident_id"]
        data_store.resource_assignments.setdefault(iid, []).append(asgn)
        if asgn["resource_id"] in data_store.resources:
            data_store.resources[asgn["resource_id"]]["status"] = "assigned"

    _trace(
        workflow_id, None,
        "ResourceAllocationAgent", "allocate_cross_incident",
        "2 active incidents: F-11 (priority 92.1) > G-10 (priority 87.4). 8 resources available.",
        "7 assignments created across 2 incidents. "
        "F-11 gets ALS ambulance despite G-10 need (CRITICAL > HIGH). "
        "Trade-off logged: ALS diverted from G-10 standby. "
        "G-10 retains 2 pumps + 1 traffic squad. res_cop_02 held in reserve.",
        tool_calls=["rank_by_priority()", "assign_resources()", "log_trade_offs()"],
        duration_ms=115,
    )

    # ── Step 9: Simulation Agent ───────────────────────────
    data_store.simulations[flood_inc_id] = {
        "id": _uid("sim_"), "incident_id": flood_inc_id,
        "action_plan": ["deploy_pump_alpha", "deploy_pump_beta", "traffic_reroute_kashmir"],
        "before_state": {"congestion_level": "SEVERE", "emergency_eta_min": 28, "flood_area_sqm": 14000, "evacuation_possible": False},
        "after_state":  {"congestion_level": "MODERATE", "emergency_eta_min": 11, "flood_area_sqm": 4200, "evacuation_possible": True},
        "deltas": [
            {"metric": "congestion_level",   "before": "SEVERE",  "after": "MODERATE", "improved": True},
            {"metric": "emergency_eta_min",  "before": 28,        "after": 11,         "improved": True},
            {"metric": "flood_area_sqm",     "before": 14000,     "after": 4200,       "improved": True},
            {"metric": "evacuation_possible","before": False,     "after": True,       "improved": True},
        ],
        "side_effects": [
            "Kashmir Hwy closure may increase G-11 congestion by ~15%",
            "Pump deployment delays traffic clearance by ~8 min",
        ],
        "cost_estimate_pkr": 185000,
        "risk_if_delayed": "Residential basement collapse risk in 45 min",
        "created_by_agent": "SimulationAgent", "created_at": now,
    }
    data_store.simulations[heat_inc_id] = {
        "id": _uid("sim_"), "incident_id": heat_inc_id,
        "action_plan": ["deploy_als_ambulance", "deploy_cooling_tent", "dispatch_water_bowser"],
        "before_state": {"heat_risk_level": "EXTREME", "emergency_eta_min": 40, "hospitals_notified": 0, "population_at_risk": 3200},
        "after_state":  {"heat_risk_level": "MODERATE", "emergency_eta_min": 14, "hospitals_notified": 3, "population_at_risk": 800},
        "deltas": [
            {"metric": "heat_risk_level",    "before": "EXTREME",  "after": "MODERATE", "improved": True},
            {"metric": "emergency_eta_min",  "before": 40,         "after": 14,         "improved": True},
            {"metric": "hospitals_notified", "before": 0,          "after": 3,          "improved": True},
            {"metric": "population_at_risk", "before": 3200,       "after": 800,        "improved": True},
        ],
        "side_effects": [
            "Cooling tent occupancy may reach capacity in 90 min — request second unit",
            "ALS diverted from G-10 area — G-10 has lower medical risk currently",
        ],
        "cost_estimate_pkr": 120000,
        "risk_if_delayed": "Heatstroke mortality risk for elderly/children within 30 min",
        "created_by_agent": "SimulationAgent", "created_at": now,
    }
    _trace(
        workflow_id, None,
        "SimulationAgent", "simulate_both_response_plans",
        "Action plans for G-10 (3 actions) and F-11 (3 actions)",
        "G-10: congestion SEVERE→MODERATE, flood area −70%, ETA 28→11 min. "
        "F-11: heat risk EXTREME→MODERATE, 2,400 people de-risked, 3 hospitals notified. "
        "2 side-effects logged per incident.",
        tool_calls=["simulate_action_plan()", "compute_deltas()", "estimate_side_effects()"],
        duration_ms=133,
    )

    # ── Step 10: Stakeholder Notification Agent ────────────
    audiences = [
        ("public",             "SMS Broadcast",   True,  flood_inc_id,
         "⚠️ FLOOD ALERT: G-10 area roads closed due to urban flooding. "
         "Avoid Kashmir Highway. Emergency teams deployed. Stay tuned for updates. — CityCommand AI"),
        ("emergency_services", "Radio/CAD",       False, flood_inc_id,
         "DISPATCH: Urban flooding G-10 sector. 2× drainage pumps ETA 12-18 min. "
         "Traffic squad rerouting Kashmir Highway. Coordinate with field team on ground."),
        ("hospitals",          "Email/Portal",    False, heat_inc_id,
         "MEDICAL ALERT: Heat emergency F-11 Katchi Abadi. Multiple heatstroke cases incoming. "
         "Prepare cooling protocols. ALS ETA 14 min. Estimate 15-30 patients."),
        ("utility",            "Email",           False, flood_inc_id,
         "UTILITY NOTICE: Possible water-main burst co-located with G-10 flooding. "
         "Dispatch inspection crew to G-10/4 Service Road. Confirm before public retraction."),
        ("traffic",            "Smart Signs/App", False, flood_inc_id,
         "TRAFFIC MGMT: Kashmir Highway G-10 CLOSED. Divert via Margalla Road. "
         "Estimated clearance time: 3 hours. Update variable message signs."),
        ("media",              "Press Release",   False, flood_inc_id,
         "FOR IMMEDIATE RELEASE: CityCommand AI has detected urban flooding in G-10 Islamabad. "
         "Emergency response is underway. Public advised to avoid the area. Official update in 30 min."),
        ("field_team",         "Push Notification", False, heat_inc_id,
         "FIELD DISPATCH: Deploy to F-11 Katchi Abadi for heat emergency. "
         "Report GPS location every 10 min. Cooling tent setup at F-11 Chowk. "
         "Priority: elderly and children first."),
    ]
    notifications_created = []
    for audience, channel, req_approval, inc_id, message in audiences:
        notif = {
            "id":               _uid("msg_"),
            "incident_id":      inc_id,
            "audience":         audience,
            "channel":          channel,
            "message":          message,
            "status":           "draft",
            "requires_approval": req_approval,
            "sent_at":          None,
            "created_by_agent": "StakeholderNotificationAgent",
            "created_at":       now,
        }
        data_store.notifications[notif["id"]] = notif
        notifications_created.append(notif["id"])

    _trace(
        workflow_id, None,
        "StakeholderNotificationAgent", "draft_all_notifications",
        "2 active incidents, 7 audience groups",
        f"Created {len(notifications_created)} draft messages across 7 audiences. "
        "Public SMS requires human approval (confidence < 0.85 for flood). "
        "All other audiences auto-approved for dispatch.",
        tool_calls=["draft_message_per_audience()", "check_approval_required()", "store_notifications()"],
        human_review_required=True,
        duration_ms=78,
    )

    # ── Step 11: Command Center Briefing Agent ─────────────
    _trace(
        workflow_id, None,
        "CommandCenterBriefingAgent", "generate_situation_summary",
        "All agent outputs assembled",
        "SITREP: 2 simultaneous crises active. F-11 heat emergency (CRITICAL, priority 92.1) "
        "is primary concern — 3,200 people at risk, ALS dispatched, cooling tent en route. "
        "G-10 flooding (HIGH, priority 87.4) — 8,500 people affected, drainage deployed, "
        "alternate hypothesis (water-main burst 41%) flagged for human review. "
        "7 notifications drafted. 7 resources deployed. Awaiting field confirmation on G-10.",
        tool_calls=["summarize_incidents()", "format_sitrep()", "push_to_dashboard()"],
        duration_ms=44,
    )

    # ── Final audit log ────────────────────────────────────
    data_store.audit_logs.append({
        "id": _uid("audit_"), "entity_type": "system",
        "entity_id": "demo_run", "action": "full_pipeline_executed",
        "actor_type": "system", "actor_id": "demo_orchestrator",
        "before": None,
        "after": {
            "incidents": 2, "traces": len(data_store.traces),
            "notifications": len(notifications_created),
            "assignments": sum(len(v) for v in data_store.resource_assignments.values()),
        },
        "timestamp": now,
    })

    return {
        "success": True,
        "data": {
            "workflow_id":        workflow_id,
            "incidents_created":  2,
            "signals_loaded":     seed_result["signals_loaded"],
            "resources_loaded":   seed_result["resources_loaded"],
            "traces_generated":   len(data_store.traces),
            "notifications_drafted": len(notifications_created),
            "resource_assignments": sum(len(v) for v in data_store.resource_assignments.values()),
            "incident_ids": {
                "g10_flooding":    flood_inc_id,
                "f11_heat_emergency": heat_inc_id,
            },
        },
        "timestamp": now,
        "trace_id": workflow_id,
    }


# ─────────────────────────────────────────────────
# POST /demo/reset
# ─────────────────────────────────────────────────
@router.post("/reset")
async def reset_demo():
    """Wipe all data back to empty state."""
    data_store.reset()
    return {
        "success": True,
        "message": "Demo data reset to empty state.",
        "timestamp": _now(),
    }


# ─────────────────────────────────────────────────
# GET /demo/status
# ─────────────────────────────────────────────────
@router.get("/status")
async def demo_status():
    """Return whether the demo has been loaded and summary stats."""
    return {
        "success": True,
        "data": {
            "demo_loaded":    data_store.demo_loaded,
            "demo_loaded_at": data_store.demo_loaded_at,
            "stats":          data_store.get_stats(),
        },
        "timestamp": _now(),
    }
