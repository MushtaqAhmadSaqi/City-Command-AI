/**
 * CityCommand AI — Shared TypeScript Type Definitions
 * These interfaces map directly to the FastAPI Pydantic models.
 */

// ──────────────────────────────────────────────
// Signals
// ──────────────────────────────────────────────
export interface SignalMetadata {
  user_reputation?: number;
  media_attached?: boolean;
  language?: string;
  [key: string]: any;
}

export interface Signal {
  id: string;
  source_id: string;
  source_type: 'social' | 'weather' | 'traffic' | 'field' | 'sensor' | 'calls';
  raw_text: string;
  normalized_text?: string;
  language?: string;
  lat?: number;
  lng?: number;
  location_text?: string;
  timestamp: string;
  metadata?: SignalMetadata;
}

// ──────────────────────────────────────────────
// Incidents & Classifications
// ──────────────────────────────────────────────
export type IncidentStatus = 'candidate' | 'active' | 'verified' | 'reclassified' | 'resolved';
export type SeverityLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface LocationArea {
  area: string;
  lat: number;
  lng: number;
  radius_m: number;
}

export interface AlternateHypothesis {
  type: string;
  confidence: number;
  reason?: string;
}

export interface Classification {
  id: string;
  incident_id: string;
  class_type: string;
  confidence: number;
  is_primary: boolean;
  evidence: string[];
  created_by_agent: string;
}

export interface Incident {
  id: string;
  title: string;
  primary_type: string;
  alternate_hypotheses?: AlternateHypothesis[];
  severity: SeverityLevel;
  confidence: number;
  priority_score: number;
  location?: LocationArea;
  affected_population_estimate?: number;
  expected_duration_min?: number;
  status: IncidentStatus;
}

// ──────────────────────────────────────────────
// Resources
// ──────────────────────────────────────────────
export type ResourceStatus = 'available' | 'assigned' | 'unavailable';

export interface Resource {
  id: string;
  resource_type: string;
  name: string;
  status: ResourceStatus;
  home_lat: number;
  home_lng: number;
  capacity: number;
  metadata?: Record<string, any>;
}

export type AssignmentStatus = 'planned' | 'approved' | 'dispatched' | 'completed';

export interface ResourceAssignment {
  id: string;
  incident_id: string;
  resource_id: string;
  resource_name?: string;
  assigned_units: number;
  eta_min: number;
  priority_reason: string;
  status: AssignmentStatus;
}

// ──────────────────────────────────────────────
// Actions & Simulations
// ──────────────────────────────────────────────
export interface Simulation {
  id: string;
  incident_id: string;
  before_state: Record<string, any>;
  action_plan: string[];
  after_state: Record<string, any>;
  side_effects: string[];
}

// ──────────────────────────────────────────────
// Notifications
// ──────────────────────────────────────────────
export type NotificationStatus = 'draft' | 'approved' | 'sent' | 'retracted';

export interface StakeholderNotification {
  id: string;
  incident_id: string;
  audience: 'public' | 'emergency_services' | 'hospitals' | 'utility' | 'traffic' | 'media' | 'field_team';
  channel: string;
  message: string;
  status: NotificationStatus;
  requires_approval: boolean;
}

// ──────────────────────────────────────────────
// Agent Traces & System Health
// ──────────────────────────────────────────────
export interface AgentTrace {
  id: string;
  workflow_id: string;
  incident_id: string;
  agent_name: string;
  step: string;
  input_summary: string;
  output_summary: string;
  tool_calls: string[];
  fallback_used: boolean;
  timestamp: string;
}

export interface ApiHealth {
  api_name: string;
  status: 'healthy' | 'degraded' | 'down';
  latency_ms: number;
  fallback_used: boolean;
  error_message?: string;
  last_checked: string;
}

// ──────────────────────────────────────────────
// API Responses
// ──────────────────────────────────────────────
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
  timestamp?: string;
  trace_id?: string;
}
