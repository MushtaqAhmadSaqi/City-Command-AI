"""
CityCommand AI — In-Memory Data Store

Central state container for the hackathon demo.
All data lives in memory — no database required for MVP.

This singleton holds all signals, incidents, resources, traces,
notifications, audit logs, and API health state. Every route
and service reads/writes through this store.

Design decision: Using a class-based singleton instead of a database
keeps the demo lightweight, fast (<100ms responses), and eliminates
all database setup friction during hackathon judging.
"""

from typing import Dict, List, Any
from datetime import datetime


class DataStore:
    """
    In-memory data store for CityCommand AI.
    
    All collections are simple Python dicts/lists.
    Keys are entity IDs (e.g., "inc_g10_001").
    
    In production, replace with PostgreSQL + PostGIS.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all data to empty state. Used by demo reset."""

        # ── Signal Sources ──
        # Registry of known data sources with credibility weights
        self.signal_sources: Dict[str, Dict[str, Any]] = {}

        # ── Incoming Signals ──
        # Raw and normalized signals from all sources
        self.signals: List[Dict[str, Any]] = []

        # ── Incidents ──
        # Core incident objects keyed by incident ID
        self.incidents: Dict[str, Dict[str, Any]] = {}

        # ── Crisis Classifications ──
        # Primary + alternate classifications per incident
        self.classifications: Dict[str, List[Dict[str, Any]]] = {}

        # ── Severity Predictions ──
        # Severity estimates per incident
        self.severity_predictions: Dict[str, Dict[str, Any]] = {}

        # ── Resources ──
        # Available resource inventory keyed by resource ID
        self.resources: Dict[str, Dict[str, Any]] = {}

        # ── Resource Assignments ──
        # Assignments keyed by incident ID → list of assignments
        self.resource_assignments: Dict[str, List[Dict[str, Any]]] = {}

        # ── Response Actions ──
        # Planned/approved actions per incident
        self.response_actions: Dict[str, List[Dict[str, Any]]] = {}

        # ── Simulations ──
        # Before/after simulation results per incident
        self.simulations: Dict[str, Dict[str, Any]] = {}

        # ── Stakeholder Notifications ──
        # Draft/sent messages keyed by notification ID
        self.notifications: Dict[str, Dict[str, Any]] = {}

        # ── Agent Traces ──
        # Ordered list of agent trace entries (the core judging artifact)
        self.traces: List[Dict[str, Any]] = []

        # ── Audit Logs ──
        # Ordered list of all state change records
        self.audit_logs: List[Dict[str, Any]] = []

        # ── API Health Logs ──
        # Current health status of each mock API
        self.api_health: Dict[str, Dict[str, Any]] = {
            "weather_api": {
                "api_name": "weather_api",
                "status": "healthy",
                "latency_ms": 45,
                "fallback_used": False,
                "error_message": None,
                "last_checked": datetime.utcnow().isoformat() + "Z",
            },
            "traffic_api": {
                "api_name": "traffic_api",
                "status": "healthy",
                "latency_ms": 62,
                "fallback_used": False,
                "error_message": None,
                "last_checked": datetime.utcnow().isoformat() + "Z",
            },
            "social_api": {
                "api_name": "social_api",
                "status": "healthy",
                "latency_ms": 38,
                "fallback_used": False,
                "error_message": None,
                "last_checked": datetime.utcnow().isoformat() + "Z",
            },
            "field_reports_api": {
                "api_name": "field_reports_api",
                "status": "healthy",
                "latency_ms": 55,
                "fallback_used": False,
                "error_message": None,
                "last_checked": datetime.utcnow().isoformat() + "Z",
            },
        }

        # ── False Alarm Records ──
        # Records of corrected/retracted incidents
        self.false_alarm_records: List[Dict[str, Any]] = []

        # ── Demo State ──
        # Tracks whether the demo scenario has been loaded
        self.demo_loaded: bool = False
        self.demo_loaded_at: str | None = None

        # ── Demo Toggles ──
        # Stress-test toggles for judge demonstrations
        self.demo_toggles: Dict[str, bool] = {
            "api_failure": False,        # Simulate traffic API failure
            "duplicate_reports": False,   # Include duplicate signals
            "conflicting_report": True,   # Include water-main field report
            "false_alarm_recovery": False, # Auto-trigger recovery flow
        }

    def get_stats(self) -> Dict[str, Any]:
        """Return summary stats for the dashboard."""
        active_incidents = [
            inc for inc in self.incidents.values()
            if inc.get("status") in ("active", "needs_human_review", "candidate")
        ]
        available_resources = [
            res for res in self.resources.values()
            if res.get("status") == "available"
        ]
        healthy_apis = [
            api for api in self.api_health.values()
            if api.get("status") == "healthy"
        ]

        return {
            "total_signals": len(self.signals),
            "active_incidents": len(active_incidents),
            "total_incidents": len(self.incidents),
            "available_resources": len(available_resources),
            "total_resources": len(self.resources),
            "healthy_apis": len(healthy_apis),
            "total_apis": len(self.api_health),
            "total_traces": len(self.traces),
            "total_audit_logs": len(self.audit_logs),
            "demo_loaded": self.demo_loaded,
        }


# ──────────────────────────────────────────────
# Singleton instance — imported everywhere
# ──────────────────────────────────────────────
data_store = DataStore()
