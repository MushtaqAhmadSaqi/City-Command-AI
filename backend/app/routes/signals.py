"""
CityCommand AI — Signal Ingestion Routes

POST /signals        Submit a new signal (citizen/field/social)
GET  /signals        List signals with optional filters
GET  /signals/{id}   Get a single signal by ID

Signals are the raw input to the entire crisis pipeline.
Every submitted signal is normalized, geocoded (best-effort),
and stored. The demo scenario auto-loads 8 signals via the
seed loader; this endpoint allows live submission during judging.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.data_store import data_store
from app.schemas.models import SignalCreate, SourceType

router = APIRouter()


# ─────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────
def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _uid(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"

# Best-effort geocoder for live submissions
_GEO_LOOKUP: dict[str, tuple[float, float]] = {
    "g-10":          (33.6844, 73.0479),
    "g10":           (33.6844, 73.0479),
    "g-9":           (33.6900, 73.0620),
    "g9":            (33.6900, 73.0620),
    "f-11":          (33.6700, 73.0290),
    "f11":           (33.6700, 73.0290),
    "f-7":           (33.7180, 73.0650),
    "f7":            (33.7180, 73.0650),
    "kashmir highway": (33.6900, 73.0490),
    "margalla":      (33.7340, 73.0630),
    "blue area":     (33.7270, 73.0940),
    "i-8":           (33.6630, 73.0780),
    "i8":            (33.6630, 73.0780),
}

def _infer_coords(location_text: str) -> tuple[float | None, float | None]:
    """Best-effort lat/lng from location_text."""
    lower = location_text.lower()
    for key, coords in _GEO_LOOKUP.items():
        if key in lower:
            return coords
    return None, None

def _detect_language(text: str) -> str:
    """Lightweight Roman Urdu / English detection."""
    roman_urdu_markers = ["mein", "hai", "ka", "ki", "ko", "pani", "bhari", "gaadi", "phans", "garam"]
    lower = text.lower()
    if any(marker in lower for marker in roman_urdu_markers):
        return "roman_urdu"
    return "english"

def _normalize_text(raw: str) -> str:
    """Strip extra whitespace, preserve content."""
    return " ".join(raw.strip().split())


# ─────────────────────────────────────────────────
# POST /signals
# ─────────────────────────────────────────────────
@router.post("", status_code=201)
async def submit_signal(body: SignalCreate):
    """
    Submit a new signal to the CityCommand AI system.

    The signal is:
      1. Validated via Pydantic (source_type, raw_text, location_text required)
      2. Normalized (whitespace cleaned, language detected)
      3. Geocoded (best-effort lat/lng from location_text)
      4. Stored in data_store.signals
      5. Audit log entry added

    The mobile Signal Intake screen calls this endpoint for
    live signal submission during the hackathon demo.
    """
    raw_text = body.raw_text.strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="raw_text must not be empty")

    location_text = body.location_text.strip()
    if not location_text:
        raise HTTPException(status_code=400, detail="location_text must not be empty")

    sig_id = _uid("sig_")
    lat, lng = _infer_coords(location_text)
    language  = (body.metadata.language if body.metadata and body.metadata.language
                 else _detect_language(raw_text))

    signal = {
        "id":              sig_id,
        "source_id":       sig_id,
        "source_type":     body.source_type.value,
        "raw_text":        raw_text,
        "normalized_text": _normalize_text(raw_text),
        "language":        language,
        "lat":             lat,
        "lng":             lng,
        "location_text":   location_text,
        "timestamp":       body.timestamp or _now(),
        "metadata":        body.metadata.model_dump() if body.metadata else {},
    }

    data_store.signals.append(signal)

    # Audit log
    data_store.audit_logs.append({
        "id":          _uid("audit_"),
        "entity_type": "signal",
        "entity_id":   sig_id,
        "action":      "signal_submitted",
        "actor_type":  "human",
        "actor_id":    "citizen",
        "before":      None,
        "after":       {
            "source_type":   signal["source_type"],
            "location_text": location_text,
            "language":      language,
            "geocoded":      lat is not None,
        },
        "timestamp": _now(),
    })

    # Trace entry
    data_store.traces.append({
        "id":             _uid("trc_"),
        "workflow_id":    _uid("wf_"),
        "incident_id":    None,
        "agent_name":     "SignalIntakeAgent",
        "step":           "live_signal_received",
        "input_summary":  f"[{signal['source_type']}] {raw_text[:80]}",
        "output_summary":  f"Signal {sig_id} stored. Language={language}. "
                           f"Geocoded={'yes' if lat else 'no (needs review)'}.",
        "tool_calls":     ["normalize_text()", "infer_coords()", "detect_language()"],
        "fallback_used":  lat is None,
        "human_review_required": lat is None,
        "duration_ms":    12,
        "timestamp":      _now(),
    })

    return {
        "success": True,
        "data":    signal,
        "message": (
            "Signal received and geocoded."
            if lat
            else "Signal received. Location could not be geocoded — operator review recommended."
        ),
        "timestamp": _now(),
        "trace_id":  data_store.traces[-1]["id"],
    }


# ─────────────────────────────────────────────────
# GET /signals
# ─────────────────────────────────────────────────
@router.get("")
async def list_signals(
    source_type: Optional[SourceType] = Query(None, description="Filter by source type"),
    limit:       int                  = Query(50,  ge=1, le=200),
    offset:      int                  = Query(0,   ge=0),
):
    """
    List recent signals with optional filtering.

    Query params:
      source_type  — Filter to a specific source (social, weather, traffic, etc.)
      limit        — Max results (default 50, max 200)
      offset       — Pagination offset
    """
    signals = data_store.signals

    if source_type:
        signals = [s for s in signals if s.get("source_type") == source_type.value]

    total   = len(signals)
    paged   = signals[offset : offset + limit]

    return {
        "success": True,
        "data":    paged,
        "meta": {
            "total":  total,
            "limit":  limit,
            "offset": offset,
            "returned": len(paged),
        },
        "timestamp": _now(),
    }


# ─────────────────────────────────────────────────
# GET /signals/{signal_id}
# ─────────────────────────────────────────────────
@router.get("/{signal_id}")
async def get_signal(signal_id: str):
    """Get a single signal by ID."""
    match = next((s for s in data_store.signals if s["id"] == signal_id), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"Signal '{signal_id}' not found")
    return {
        "success": True,
        "data":    match,
        "timestamp": _now(),
    }
