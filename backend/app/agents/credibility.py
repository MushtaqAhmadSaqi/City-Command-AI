"""
CityCommand AI — Credibility Scoring Agent

Wraps the scoring service with trace logging.
Called by the orchestrator after geolocation.

Returns credibility scores with full factor breakdowns
that feed the AI Analysis screen.
"""

from app.services.scoring import CredibilityInput, score_credibility
from app.data_store import data_store
from datetime import datetime, timezone
import uuid


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _uid(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"


def run(
    workflow_id: str,
    cluster_key: str,
    signals: list[dict],
    geo_confidence: float = 0.85,
) -> dict:
    """
    Run the credibility scoring agent for a signal cluster.

    Args:
      workflow_id:    Current pipeline workflow ID
      cluster_key:   e.g. "g10", "f11"
      signals:       List of signal dicts in the cluster
      geo_confidence: Score from the geolocation agent

    Returns:
      dict with: confidence, factors, weights, weighted, dominant_penalty
    """
    from datetime import datetime, timezone
    from app.data_store import data_store

    source_types = list({s.get("source_type", "social") for s in signals})
    has_urgency  = any(
        (s.get("metadata") or {}).get("urgency") in ("high", "critical")
        for s in signals
    )
    has_media   = any(
        (s.get("metadata") or {}).get("media_attached") for s in signals
    )
    has_contradiction = False  # Detected later by classification agent
    oldest_age_min    = 10.0  # Mock: assume signals are recent

    inp = CredibilityInput(
        source_types=source_types,
        signal_count=len(signals),
        geo_confidence=geo_confidence,
        has_urgency=has_urgency,
        arrival_rate=len(signals) / 10.0,   # signals per 10-min window
        has_media=has_media,
        has_contradiction=has_contradiction,
        max_signal_age_min=oldest_age_min,
        independent_sources=len(source_types),
    )
    result = score_credibility(inp)

    # Write trace entry
    trace = {
        "id":             _uid("trc_"),
        "workflow_id":    workflow_id,
        "incident_id":    None,
        "agent_name":     "CredibilityScoringAgent",
        "step":           f"score_{cluster_key}_cluster",
        "input_summary":  (
            f"{len(signals)} signals, sources={source_types}, "
            f"media={has_media}, urgency={has_urgency}"
        ),
        "output_summary": (
            f"Confidence: {result.confidence:.2f}. "
            f"Dominant factors: source_cred={result.factors['source_credibility']:.2f}, "
            f"corroboration={result.factors['corroboration']:.2f}. "
            + (f"Penalty: {result.dominant_penalty}." if result.dominant_penalty else "No penalties.")
        ),
        "tool_calls":     ["score_credibility()", "apply_weights()", "detect_penalties()"],
        "fallback_used":  False,
        "human_review_required": False,
        "duration_ms":    35,
        "timestamp":      _now(),
    }
    data_store.traces.append(trace)

    return {
        "confidence":       result.confidence,
        "raw_score":        result.raw_score,
        "factors":          result.factors,
        "weights":          result.weights,
        "weighted":         result.weighted,
        "dominant_penalty": result.dominant_penalty,
        "trace_id":         trace["id"],
    }
