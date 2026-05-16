"""
CityCommand AI — Pydantic Models

All request/response models for the FastAPI backend.
These map 1-to-1 with the TypeScript interfaces in mobile/src/types/index.ts.

Organized into groups matching the agent pipeline:
  Signals → Incidents → Classification → Severity →
  Resources → Actions → Simulations → Notifications →
  Traces → Audit → Recovery → Health
"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal, Optional
from datetime import datetime
from enum import Enum


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class SourceType(str, Enum):
    social   = "social"
    weather  = "weather"
    traffic  = "traffic"
    field    = "field"
    sensor   = "sensor"
    calls    = "calls"

class SeverityLevel(str, Enum):
    LOW      = "LOW"
    MEDIUM   = "MEDIUM"
    HIGH     = "HIGH"
    CRITICAL = "CRITICAL"

class IncidentStatus(str, Enum):
    candidate           = "candidate"
    active              = "active"
    needs_human_review  = "needs_human_review"
    verified            = "verified"
    reclassified        = "reclassified"
    resolved            = "resolved"

class ResourceStatus(str, Enum):
    available   = "available"
    assigned    = "assigned"
    unavailable = "unavailable"

class AssignmentStatus(str, Enum):
    planned    = "planned"
    approved   = "approved"
    dispatched = "dispatched"
    completed  = "completed"

class NotificationStatus(str, Enum):
    draft     = "draft"
    approved  = "approved"
    sent      = "sent"
    retracted = "retracted"

class ApiStatus(str, Enum):
    healthy  = "healthy"
    degraded = "degraded"
    down     = "down"


# ──────────────────────────────────────────────
# Signals
# ──────────────────────────────────────────────

class SignalMetadata(BaseModel):
    user_reputation: Optional[float] = Field(None, ge=0.0, le=1.0)
    media_attached:  Optional[bool]  = False
    language:        Optional[str]   = None
    urgency:         Optional[str]   = None
    caller_type:     Optional[str]   = None
    sensor_id:       Optional[str]   = None
    precipitation_mm: Optional[float] = None
    temp_c:          Optional[float] = None
    humidity_percent: Optional[float] = None
    confidence:      Optional[float] = None

class SignalCreate(BaseModel):
    source_type:   SourceType
    raw_text:      str
    location_text: str
    timestamp:     Optional[str] = None
    metadata:      Optional[SignalMetadata] = None

class Signal(BaseModel):
    id:               str
    source_id:        Optional[str] = None
    source_type:      SourceType
    raw_text:         str
    normalized_text:  Optional[str] = None
    language:         Optional[str] = None
    lat:              Optional[float] = None
    lng:              Optional[float] = None
    location_text:    Optional[str] = None
    timestamp:        str
    metadata:         Optional[SignalMetadata] = None


# ──────────────────────────────────────────────
# Incidents & Classifications
# ──────────────────────────────────────────────

class LocationArea(BaseModel):
    area:     str
    lat:      float
    lng:      float
    radius_m: float

class AlternateHypothesis(BaseModel):
    type:       str
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason:     Optional[str] = None

class ConfidenceFactors(BaseModel):
    source_credibility:    float = 0.0
    geo_confidence:        float = 0.0
    urgency:               float = 0.0
    signal_velocity:       float = 0.0
    corroboration:         float = 0.0
    duplicate_cluster:     float = 0.0
    media_attached:        float = 0.0
    contradiction_penalty: float = 0.0
    staleness_penalty:     float = 0.0

class Classification(BaseModel):
    id:                str
    incident_id:       str
    class_type:        str
    sub_type:          Optional[str] = None
    confidence:        float
    confidence_factors: Optional[ConfidenceFactors] = None
    is_primary:        bool
    evidence:          List[str] = []
    alternate_hypotheses: List[AlternateHypothesis] = []
    human_review_required: bool = False
    created_by_agent:  str
    created_at:        str

class Incident(BaseModel):
    id:                          str
    title:                       str
    primary_type:                str
    sub_type:                    Optional[str] = None
    alternate_hypotheses:        List[AlternateHypothesis] = []
    severity:                    SeverityLevel
    confidence:                  float
    priority_score:              float
    location:                    Optional[LocationArea] = None
    affected_population_estimate: Optional[int] = None
    expected_duration_min:       Optional[int] = None
    peak_impact_min:             Optional[int] = None
    status:                      IncidentStatus
    human_review_required:       bool = False
    signal_ids:                  List[str] = []
    created_at:                  str
    updated_at:                  str


# ──────────────────────────────────────────────
# Severity Predictions
# ──────────────────────────────────────────────

class SeverityPrediction(BaseModel):
    id:                       str
    incident_id:              str
    severity:                 SeverityLevel
    radius_m:                 float
    population_affected:      int
    duration_min:             int
    peak_impact_min:          int
    spread_risk:              Optional[str] = None
    vulnerability_score:      Optional[float] = None
    confidence:               float
    created_by_agent:         str
    created_at:               str


# ──────────────────────────────────────────────
# Resources
# ──────────────────────────────────────────────

class Resource(BaseModel):
    id:            str
    resource_type: str
    name:          str
    status:        ResourceStatus
    home_lat:      float
    home_lng:      float
    capacity:      int
    metadata:      Optional[Dict[str, Any]] = None

class ResourceAssignment(BaseModel):
    id:              str
    incident_id:     str
    resource_id:     str
    resource_name:   Optional[str] = None
    resource_type:   Optional[str] = None
    assigned_units:  int
    eta_min:         int
    priority_reason: str
    trade_off_note:  Optional[str] = None
    status:          AssignmentStatus
    created_at:      str


# ──────────────────────────────────────────────
# Response Actions
# ──────────────────────────────────────────────

class ResponseAction(BaseModel):
    id:          str
    incident_id: str
    action_type: str
    description: str
    status:      Literal["planned", "approved", "rejected", "executed"]
    actor:       Optional[str] = None
    created_at:  str


# ──────────────────────────────────────────────
# Simulations
# ──────────────────────────────────────────────

class SimulationState(BaseModel):
    congestion_level: Optional[str] = None
    emergency_eta_min: Optional[int] = None
    evacuation_possible: Optional[bool] = None
    flood_area_sqm: Optional[float] = None
    heat_risk_level: Optional[str] = None
    hospitals_notified: Optional[int] = None
    population_at_risk: Optional[int] = None

class SimulationDelta(BaseModel):
    metric:   str
    before:   Any
    after:    Any
    improved: bool

class Simulation(BaseModel):
    id:           str
    incident_id:  str
    action_plan:  List[str]
    before_state: SimulationState
    after_state:  SimulationState
    deltas:       List[SimulationDelta] = []
    side_effects: List[str] = []
    cost_estimate_pkr: Optional[int] = None
    risk_if_delayed: Optional[str] = None
    created_by_agent: str
    created_at:   str


# ──────────────────────────────────────────────
# Stakeholder Notifications
# ──────────────────────────────────────────────

class StakeholderNotification(BaseModel):
    id:                str
    incident_id:       str
    audience:          Literal["public", "emergency_services", "hospitals", "utility", "traffic", "media", "field_team"]
    channel:           str
    message:           str
    status:            NotificationStatus
    requires_approval: bool
    sent_at:           Optional[str] = None
    created_by_agent:  str
    created_at:        str


# ──────────────────────────────────────────────
# Agent Traces
# ──────────────────────────────────────────────

class AgentTrace(BaseModel):
    id:             str
    workflow_id:    str
    incident_id:    Optional[str] = None
    agent_name:     str
    step:           str
    input_summary:  str
    output_summary: str
    tool_calls:     List[str] = []
    fallback_used:  bool = False
    human_review_required: bool = False
    duration_ms:    Optional[int] = None
    timestamp:      str


# ──────────────────────────────────────────────
# Audit Logs
# ──────────────────────────────────────────────

class AuditLog(BaseModel):
    id:          str
    entity_type: str
    entity_id:   str
    action:      str
    actor_type:  Literal["human", "agent", "system"]
    actor_id:    Optional[str] = None
    before:      Optional[Dict[str, Any]] = None
    after:       Optional[Dict[str, Any]] = None
    timestamp:   str


# ──────────────────────────────────────────────
# API Health
# ──────────────────────────────────────────────

class ApiHealth(BaseModel):
    api_name:      str
    status:        ApiStatus
    latency_ms:    int
    fallback_used: bool
    error_message: Optional[str] = None
    last_checked:  str


# ──────────────────────────────────────────────
# False Alarm Records
# ──────────────────────────────────────────────

class FalseAlarmRecord(BaseModel):
    id:                    str
    incident_id:           str
    original_classification: str
    new_classification:    str
    reason:                str
    field_evidence:        Optional[str] = None
    retraction_message:    Optional[str] = None
    alert_retracted:       bool = False
    created_by:            str
    created_at:            str


# ──────────────────────────────────────────────
# Common API Response Envelope
# ──────────────────────────────────────────────

class ApiResponse(BaseModel):
    success:    bool
    data:       Optional[Any] = None
    message:    Optional[str] = None
    error:      Optional[str] = None
    timestamp:  str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    trace_id:   Optional[str] = None
