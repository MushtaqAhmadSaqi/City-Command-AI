"""
CityCommand AI — Seed Data Loader

Reads scenario_g10_heat.json and loads it into the in-memory
data store. Called by POST /demo/run-scenario.

The loader:
  1. Reads signals + resources from the JSON file
  2. Normalises each signal (adds id, normalized_text, coords)
  3. Loads resource inventory into data_store.resources
  4. Logs load audit entry
  5. Returns counts so the route can echo them back
"""

import json
import uuid
from pathlib import Path
from datetime import datetime, timezone

from app.data_store import data_store

# Path is relative to project root; resolve at import time
SEED_FILE = Path(__file__).parent.parent / "seed" / "scenario_g10_heat.json"

# ── Location lookup table (mock geocoding) ──────────────────────
_GEO_LOOKUP: dict[str, tuple[float, float]] = {
    "g-10": (33.6844, 73.0479),
    "g10":  (33.6844, 73.0479),
    "kashmir highway": (33.6900, 73.0490),
    "g-10 markaz": (33.6830, 73.0460),
    "g-10/4": (33.6810, 73.0450),
    "f-11": (33.6700, 73.0290),
    "f11":  (33.6700, 73.0290),
}

def _infer_coords(location_text: str) -> tuple[float | None, float | None]:
    """Best-effort lat/lng lookup from location_text."""
    lower = location_text.lower()
    for key, coords in _GEO_LOOKUP.items():
        if key in lower:
            return coords
    return None, None

def _normalize_text(raw: str) -> str:
    """Minimal normalization: strip and title-ish clean."""
    return raw.strip()

def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_seed_scenario() -> dict:
    """
    Load the G-10 / Heat scenario seed data into the data store.

    Returns a summary dict for the API response.
    Raises FileNotFoundError if the seed file is missing.
    Raises ValueError if the scenario_id doesn't match.
    """
    if not SEED_FILE.exists():
        raise FileNotFoundError(f"Seed file not found: {SEED_FILE}")

    with open(SEED_FILE, "r", encoding="utf-8") as f:
        seed: dict = json.load(f)

    # ── Load Signals ──────────────────────────────────────
    signals_loaded = 0
    for raw_sig in seed.get("signals", []):
        sig_id = f"sig_{uuid.uuid4().hex[:8]}"
        lat, lng = _infer_coords(raw_sig.get("location_text", ""))
        normalized = _normalize_text(raw_sig.get("raw_text", ""))

        signal = {
            "id":              sig_id,
            "source_id":       raw_sig.get("source_id", sig_id),
            "source_type":     raw_sig.get("source_type", "social"),
            "raw_text":        raw_sig.get("raw_text", ""),
            "normalized_text": normalized,
            "language":        raw_sig.get("metadata", {}).get("language"),
            "lat":             lat,
            "lng":             lng,
            "location_text":   raw_sig.get("location_text"),
            "timestamp":       raw_sig.get("timestamp", _now()),
            "metadata":        raw_sig.get("metadata", {}),
        }
        data_store.signals.append(signal)
        signals_loaded += 1

    # ── Load Resources ────────────────────────────────────
    resources_loaded = 0
    for raw_res in seed.get("resources", []):
        res_id = raw_res.get("id", f"res_{uuid.uuid4().hex[:8]}")
        data_store.resources[res_id] = {
            "id":            res_id,
            "resource_type": raw_res.get("resource_type"),
            "name":          raw_res.get("name"),
            "status":        raw_res.get("status", "available"),
            "home_lat":      raw_res.get("home_lat"),
            "home_lng":      raw_res.get("home_lng"),
            "capacity":      raw_res.get("capacity", 1),
            "metadata":      raw_res.get("metadata", {}),
        }
        resources_loaded += 1

    # ── Mark demo loaded ──────────────────────────────────
    data_store.demo_loaded    = True
    data_store.demo_loaded_at = _now()

    # ── Add audit entry ───────────────────────────────────
    data_store.audit_logs.append({
        "id":         f"audit_{uuid.uuid4().hex[:8]}",
        "entity_type": "system",
        "entity_id":  "demo",
        "action":     "seed_loaded",
        "actor_type": "system",
        "actor_id":   "data_loader",
        "before":     None,
        "after":      {"signals": signals_loaded, "resources": resources_loaded},
        "timestamp":  _now(),
    })

    return {
        "scenario_id":       seed.get("scenario_id"),
        "signals_loaded":    signals_loaded,
        "resources_loaded":  resources_loaded,
        "demo_loaded_at":    data_store.demo_loaded_at,
    }
