"""
CityCommand AI — Crisis Classification Agent

Uses the rule-based keyword engine from services/scoring.py
to classify a signal cluster into a crisis type with alternates.

Writes a trace entry with:
  - primary_type and sub_type
  - confidence + gap
  - alternate_hypotheses
  - human_review_required flag
  - matched evidence keywords
"""

from app.services.scoring import classify_signals, ClassificationResult
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
    confidence: float,
) -> dict:
    """
    Run crisis classification for a signal cluster.

    Args:
      workflow_id:  Current pipeline workflow ID
      cluster_key:  e.g. "g10", "f11"
      signals:      List of signal dicts
      confidence:   Credibility confidence score for this cluster

    Returns:
      dict with: primary_type, sub_type, alternate_hypotheses,
                 human_review_required, evidence_keywords, confidence_gap
    """
    result: ClassificationResult = classify_signals(signals, confidence)

    human_review = result.human_review_required

    trace = {
        "id":            _uid("trc_"),
        "workflow_id":   workflow_id,
        "incident_id":   None,
        "agent_name":    "ClassificationAgent",
        "step":          f"classify_{cluster_key}",
        "input_summary": (
            f"{len(signals)} signals, confidence={confidence:.2f}, "
            f"keywords scanned across 6 crisis types"
        ),
        "output_summary": (
            f"PRIMARY: {result.primary_type} (score={result.primary_score:.2f}). "
            f"Sub-type: {result.sub_type}. "
            + (
                f"ALTERNATE: {result.alternate_hypotheses[0]['type']} "
                f"({result.alternate_hypotheses[0]['confidence']:.2f}). "
                if result.alternate_hypotheses else "No alternates. "
            )
            + f"Gap: {result.confidence_gap:.2f}. "
            + ("Human review REQUIRED." if human_review else "Auto-classified.")
        ),
        "tool_calls":    [
            "classify_signals()",
            "score_keyword_density()",
            "check_review_threshold()",
        ],
        "fallback_used":         result.primary_type == "unknown",
        "human_review_required": human_review,
        "duration_ms":           52,
        "timestamp":             _now(),
    }
    data_store.traces.append(trace)

    return {
        "primary_type":          result.primary_type,
        "sub_type":              result.sub_type,
        "primary_score":         result.primary_score,
        "alternate_hypotheses":  result.alternate_hypotheses,
        "human_review_required": human_review,
        "evidence_keywords":     result.evidence_keywords,
        "confidence_gap":        result.confidence_gap,
        "trace_id":              trace["id"],
    }
