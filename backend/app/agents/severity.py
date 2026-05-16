"""
CityCommand AI — Severity Prediction Agent

Predicts the severity, geographic impact, and time evolution
of a crisis based on:
  - Crisis type and sub-type
  - Credibility confidence score
  - Geographic area (sector, vulnerability index)
  - Signal evidence (temperature, precipitation, etc.)

Output feeds:
  - The Incident Detail screen (severity badge, population, duration)
  - The AI Analysis screen (severity prediction section)
  - The Simulation screen (before-state baseline)

SEVERITY THRESHOLDS
───────────────────
CRITICAL  confidence ≥ 0.85  OR  crisis_type = heat_emergency AND conf ≥ 0.70
HIGH      confidence ≥ 0.65
MEDIUM    confidence ≥ 0.45
LOW       confidence < 0.45

SPREAD RISK
───────────
HIGH    if CRITICAL severity AND vulnerability_score > 0.70
MEDIUM  if HIGH severity OR (MEDIUM AND dense area)
LOW     otherwise
"""

import uuid
from datetime import datetime, timezone
from app.data_store import data_store


# ─────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────
def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _uid(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"


# ─────────────────────────────────────────────────
# Vulnerability Index lookup
# Based on area socio-economic vulnerability
# 0 = resilient, 1 = highly vulnerable
# ─────────────────────────────────────────────────
VULNERABILITY_INDEX: dict[str, float] = {
    "g-10":                 0.58,
    "g10":                  0.58,
    "f-11 katchi abadi":    0.92,
    "f-11":                 0.85,
    "f11":                  0.85,
    "i-9":                  0.75,
    "g-9":                  0.60,
    "f-7":                  0.30,
    "blue area":            0.25,
    "default":              0.55,
}

# ─────────────────────────────────────────────────
# Crisis-type specific parameters
# Tuned for Islamabad urban crisis scenarios
# ─────────────────────────────────────────────────
CRISIS_PARAMS: dict[str, dict] = {
    "urban_flood": {
        "base_radius_m":    1200,
        "base_pop":         8500,
        "base_duration_min": 180,
        "peak_factor":      0.25,    # peak at 25% of duration
        "spread_multiplier": 1.2,
    },
    "heat_emergency": {
        "base_radius_m":    600,
        "base_pop":         3200,
        "base_duration_min": 240,
        "peak_factor":      0.125,   # peak quickly — heat is immediate
        "spread_multiplier": 1.5,
    },
    "infrastructure_failure": {
        "base_radius_m":    400,
        "base_pop":         2000,
        "base_duration_min": 120,
        "peak_factor":      0.30,
        "spread_multiplier": 0.8,
    },
    "traffic_accident": {
        "base_radius_m":    300,
        "base_pop":         500,
        "base_duration_min": 60,
        "peak_factor":      0.20,
        "spread_multiplier": 0.6,
    },
    "fire_emergency": {
        "base_radius_m":    250,
        "base_pop":         1000,
        "base_duration_min": 90,
        "peak_factor":      0.15,
        "spread_multiplier": 1.8,
    },
    "civil_disorder": {
        "base_radius_m":    800,
        "base_pop":         5000,
        "base_duration_min": 180,
        "peak_factor":      0.35,
        "spread_multiplier": 1.1,
    },
    "unknown": {
        "base_radius_m":    500,
        "base_pop":         2000,
        "base_duration_min": 90,
        "peak_factor":      0.30,
        "spread_multiplier": 1.0,
    },
}


def _get_vulnerability(area_text: str) -> float:
    """Look up vulnerability score from area text."""
    lower = (area_text or "").lower()
    for key, score in VULNERABILITY_INDEX.items():
        if key in lower:
            return score
    return VULNERABILITY_INDEX["default"]


def _determine_severity(
    confidence: float,
    crisis_type: str,
    vulnerability: float,
) -> str:
    """
    Map confidence + crisis type + vulnerability to a severity level.
    Heat emergencies in vulnerable areas escalate to CRITICAL more readily.
    """
    if crisis_type == "heat_emergency":
        if confidence >= 0.70 or vulnerability >= 0.85:
            return "CRITICAL"
        if confidence >= 0.50:
            return "HIGH"
        return "MEDIUM"

    if confidence >= 0.85:
        return "CRITICAL"
    if confidence >= 0.65:
        return "HIGH"
    if confidence >= 0.45:
        return "MEDIUM"
    return "LOW"


def _determine_spread_risk(
    severity: str,
    vulnerability: float,
    spread_multiplier: float,
) -> str:
    """Classify spread risk based on severity and vulnerability."""
    if severity == "CRITICAL" and vulnerability > 0.70:
        return "HIGH"
    if severity in ("CRITICAL", "HIGH") and spread_multiplier > 1.0:
        return "MEDIUM"
    return "LOW"


def run(
    workflow_id: str,
    incident_id: str,
    crisis_type: str,
    confidence: float,
    area_text: str,
    signals: list[dict] | None = None,
) -> dict:
    """
    Run the severity prediction agent for a single incident.

    Args:
      workflow_id:   Current pipeline workflow ID
      incident_id:   ID of the incident to predict for
      crisis_type:   Primary crisis type (e.g. "urban_flood")
      confidence:    Credibility confidence score
      area_text:     Location/area string for vulnerability lookup
      signals:       Optional signal list for evidence-based adjustment

    Returns:
      A severity prediction dict that is stored in data_store.severity_predictions
      and returned to the mobile Incident Detail and AI Analysis screens.
    """
    params        = CRISIS_PARAMS.get(crisis_type, CRISIS_PARAMS["unknown"])
    vulnerability = _get_vulnerability(area_text)
    severity      = _determine_severity(confidence, crisis_type, vulnerability)

    # Scale parameters by confidence and vulnerability
    conf_scale = 0.6 + confidence * 0.4       # 0.6–1.0 multiplier
    vuln_scale = 1.0 + vulnerability * 0.3    # 1.0–1.3 multiplier

    radius_m            = int(params["base_radius_m"] * conf_scale * vuln_scale)
    population_affected = int(params["base_pop"] * conf_scale * vuln_scale)
    duration_min        = int(params["base_duration_min"] * conf_scale)
    peak_impact_min     = int(duration_min * params["peak_factor"])
    spread_risk         = _determine_spread_risk(severity, vulnerability, params["spread_multiplier"])

    # Sensor-based adjustments (if available)
    sensor_note = None
    if signals:
        for sig in signals:
            meta = sig.get("metadata") or {}
            if "temp_c" in meta and meta["temp_c"] > 44:
                population_affected = int(population_affected * 1.15)
                sensor_note = f"Temperature anomaly {meta['temp_c']}°C — population risk adjusted +15%"
                break
            if "precipitation_mm" in meta and meta["precipitation_mm"] > 35:
                radius_m = int(radius_m * 1.10)
                sensor_note = f"Precipitation {meta['precipitation_mm']}mm — radius adjusted +10%"
                break

    prediction = {
        "id":                   _uid("sev_"),
        "incident_id":          incident_id,
        "severity":             severity,
        "radius_m":             radius_m,
        "population_affected":  population_affected,
        "duration_min":         duration_min,
        "peak_impact_min":      peak_impact_min,
        "spread_risk":          spread_risk,
        "vulnerability_score":  vulnerability,
        "confidence":           confidence,
        "sensor_note":          sensor_note,
        "params_used": {
            "crisis_type":      crisis_type,
            "conf_scale":       round(conf_scale, 3),
            "vuln_scale":       round(vuln_scale, 3),
            "spread_multiplier": params["spread_multiplier"],
        },
        "created_by_agent":     "SeverityPredictionAgent",
        "created_at":           _now(),
    }

    # Store in data store
    data_store.severity_predictions[incident_id] = prediction

    # Trace entry
    trace = {
        "id":            _uid("trc_"),
        "workflow_id":   workflow_id,
        "incident_id":   incident_id,
        "agent_name":    "SeverityPredictionAgent",
        "step":          f"predict_severity_{crisis_type}",
        "input_summary": (
            f"crisis_type={crisis_type}, confidence={confidence:.2f}, "
            f"area='{area_text}', vulnerability={vulnerability:.2f}"
        ),
        "output_summary": (
            f"Severity: {severity}. Radius: {radius_m:,}m. "
            f"Population: ~{population_affected:,}. "
            f"Duration: {duration_min}min (peak at {peak_impact_min}min). "
            f"Spread risk: {spread_risk}."
            + (f" Sensor note: {sensor_note}" if sensor_note else "")
        ),
        "tool_calls":    [
            "determine_severity()",
            "get_vulnerability()",
            "scale_parameters()",
            "apply_sensor_adjustments()",
        ],
        "fallback_used":         crisis_type == "unknown",
        "human_review_required": severity == "CRITICAL",
        "duration_ms":           48,
        "timestamp":             _now(),
    }
    data_store.traces.append(trace)

    return {**prediction, "trace_id": trace["id"]}
