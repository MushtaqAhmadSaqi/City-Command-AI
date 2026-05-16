"""
CityCommand AI — Scoring Service

Pure mathematical functions for:
  1. Credibility Confidence Score (9-factor weighted formula)
  2. Priority Score (6-factor formula used for incident ranking)

No side effects — no data_store reads/writes. Called by agents.

CREDIBILITY FORMULA
───────────────────
confidence = clamp(Σ(weight_i × factor_i), 0, 1)

  Factor                  Weight  Range      Description
  ─────────────────────── ──────  ─────────  ──────────────────────────────
  source_credibility      0.25   [0, 1]     Weighted avg of source types
  geo_confidence          0.15   [0, 1]     Location precision score
  urgency                 0.15   [0, 1]     Urgency keywords detected
  signal_velocity         0.10   [0, 1]     Rate of arrival (signals/min)
  corroboration           0.15   [0, 1]     Multi-source agreement
  duplicate_cluster       0.05   [0, 1]     Independent confirmations
  media_attached          0.05   [0, 1]     Images/video present
  contradiction_penalty  -0.05  [-1, 0]    Conflicting evidence detected
  staleness_penalty      -0.05  [-1, 0]    Signal age > threshold

PRIORITY FORMULA
────────────────
priority = (severity_weight × 40) + (confidence × 20) +
           (vulnerability × 20) + (population_ratio × 10) +
           (speed_of_onset × 5) + (resource_availability × 5)

  Range: 0–100, higher = more urgent
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


# ─────────────────────────────────────────────────
# Source credibility lookup table
# Ordered by reliability (higher = more reliable)
# ─────────────────────────────────────────────────
SOURCE_WEIGHTS: dict[str, float] = {
    "sensor":   0.95,   # IoT / environmental sensors
    "weather":  0.92,   # Official weather service
    "field":    0.88,   # Field team reports
    "traffic":  0.82,   # Traffic authority data
    "calls":    0.72,   # Emergency call center
    "social":   0.55,   # Social media / citizen posts
}

SEVERITY_WEIGHTS: dict[str, float] = {
    "CRITICAL": 1.00,
    "HIGH":     0.75,
    "MEDIUM":   0.50,
    "LOW":      0.25,
}


# ─────────────────────────────────────────────────
# Credibility Score Input
# ─────────────────────────────────────────────────
@dataclass
class CredibilityInput:
    """All inputs needed to compute the credibility confidence score."""
    source_types:         list[str]       # e.g. ["social", "traffic", "weather"]
    signal_count:         int             # Total signal count in cluster
    geo_confidence:       float           # 0–1: how precise is the location
    has_urgency:          bool            # Any signal flagged as urgent/critical
    arrival_rate:         float           # Signals per minute (velocity)
    has_media:            bool            # Any signal has image/video
    has_contradiction:    bool            # Conflicting evidence detected
    max_signal_age_min:   float           # Oldest signal age in minutes
    independent_sources:  int             # Count of distinct source_type values
    staleness_threshold:  float = 60.0   # Minutes before staleness penalty kicks in


@dataclass
class CredibilityResult:
    """Output of the credibility scoring formula."""
    confidence:          float
    raw_score:           float
    factors:             dict[str, float]
    weights:             dict[str, float]
    weighted:            dict[str, float]   # factor * weight per dimension
    dominant_penalty:    Optional[str]      # Which penalty hurt most, if any


def score_credibility(inp: CredibilityInput) -> CredibilityResult:
    """
    Compute the 9-factor credibility confidence score.

    Returns a CredibilityResult with full factor breakdown,
    suitable for the AI Analysis screen's score visualization.
    """
    WEIGHTS = {
        "source_credibility":    0.25,
        "geo_confidence":        0.15,
        "urgency":               0.15,
        "signal_velocity":       0.10,
        "corroboration":         0.15,
        "duplicate_cluster":     0.05,
        "media_attached":        0.05,
        "contradiction_penalty": 0.05,
        "staleness_penalty":     0.05,
    }

    # ── Compute each factor ───────────────────────────────────
    # source_credibility: average of all source weights in cluster
    source_creds = [SOURCE_WEIGHTS.get(st, 0.50) for st in inp.source_types]
    source_credibility = sum(source_creds) / len(source_creds) if source_creds else 0.50

    # geo_confidence: direct from input
    geo_confidence = max(0.0, min(1.0, inp.geo_confidence))

    # urgency: presence of urgency indicators
    urgency = 0.90 if inp.has_urgency else 0.55

    # signal_velocity: normalise arrival_rate (cap at 1.0/min = full score)
    signal_velocity = min(inp.arrival_rate / 1.0, 1.0)

    # corroboration: multi-source agreement
    corroboration = min(0.40 + inp.independent_sources * 0.15, 1.0)

    # duplicate_cluster: more signals = stronger cluster (non-duplicates)
    duplicate_cluster = min(inp.signal_count * 0.12, 1.0)

    # media_attached: multimedia evidence
    media_attached = 0.85 if inp.has_media else 0.35

    # contradiction_penalty: conflicting evidence → negative factor
    contradiction_penalty = -0.70 if inp.has_contradiction else 0.0

    # staleness_penalty: old signals reduce confidence
    staleness_penalty = (
        -0.60 if inp.max_signal_age_min > inp.staleness_threshold else 0.0
    )

    factors = {
        "source_credibility":    source_credibility,
        "geo_confidence":        geo_confidence,
        "urgency":               urgency,
        "signal_velocity":       signal_velocity,
        "corroboration":         corroboration,
        "duplicate_cluster":     duplicate_cluster,
        "media_attached":        media_attached,
        "contradiction_penalty": contradiction_penalty,
        "staleness_penalty":     staleness_penalty,
    }

    weighted = {k: round(WEIGHTS[k] * factors[k], 4) for k in WEIGHTS}
    raw_score  = sum(weighted.values())
    confidence = round(max(0.0, min(1.0, raw_score)), 3)

    # Which penalty hurt the most?
    penalties = {k: v for k, v in weighted.items() if v < 0}
    dominant_penalty = min(penalties, key=penalties.get) if penalties else None

    return CredibilityResult(
        confidence=confidence,
        raw_score=round(raw_score, 4),
        factors=factors,
        weights=WEIGHTS,
        weighted=weighted,
        dominant_penalty=dominant_penalty,
    )


# ─────────────────────────────────────────────────
# Priority Score
# ─────────────────────────────────────────────────
@dataclass
class PriorityInput:
    """All inputs needed to compute the priority score."""
    severity:              str    # "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
    confidence:            float  # 0–1
    vulnerability_score:   float  # 0–1 (area social vulnerability index)
    affected_population:   int    # Absolute number
    city_population:       int    # Denominator for population ratio
    speed_of_onset:        float  # 0–1 (1 = instant, 0 = slow build)
    resources_available:   float  # 0–1 (1 = ample, 0 = none)


def score_priority(inp: PriorityInput) -> dict[str, float]:
    """
    Compute the 0–100 priority score for incident ranking.

    Higher score = dispatch first.

    Returns a dict with:
      total_score    — 0–100 final score
      breakdown      — contribution per factor (for AI Analysis screen)
    """
    severity_weight = SEVERITY_WEIGHTS.get(inp.severity.upper(), 0.50)
    pop_ratio       = min(inp.affected_population / max(inp.city_population, 1), 1.0)

    contributions = {
        "severity":               severity_weight       * 40,
        "confidence":             inp.confidence        * 20,
        "vulnerability":          inp.vulnerability_score * 20,
        "population_ratio":       pop_ratio             * 10,
        "speed_of_onset":         inp.speed_of_onset    * 5,
        "resource_availability":  inp.resources_available * 5,
    }

    total = round(sum(contributions.values()), 1)
    total = max(0.0, min(100.0, total))

    return {
        "total_score":  total,
        "severity":     inp.severity,
        "breakdown":    {k: round(v, 2) for k, v in contributions.items()},
    }


# ─────────────────────────────────────────────────
# Classification Rule Engine
# ─────────────────────────────────────────────────

CRISIS_KEYWORDS: dict[str, list[str]] = {
    "urban_flood": [
        "pani", "flood", "water", "bhar", "rain", "submerged",
        "drainage", "inundation", "waterlogging",
    ],
    "heat_emergency": [
        "heat", "garam", "temperature", "heatstroke", "hot",
        "cooling", "power outage", "bijli", "fainting",
    ],
    "infrastructure_failure": [
        "burst", "sewage", "pipe", "main", "infrastructure",
        "collapse", "sewer", "utility",
    ],
    "traffic_accident": [
        "accident", "collision", "crash", "gaadi", "vehicle",
        "overturned", "blocked road",
    ],
    "fire_emergency": [
        "fire", "aag", "smoke", "blaze", "burn", "explosion",
    ],
    "civil_disorder": [
        "protest", "riot", "crowd", "conflict", "violence", "dharna",
    ],
}

CRISIS_SUBTYPES: dict[str, str] = {
    "urban_flood":            "residential_road_flooding",
    "heat_emergency":         "prolonged_power_outage_heat",
    "infrastructure_failure": "water_main_burst",
    "traffic_accident":       "multi_vehicle_collision",
    "fire_emergency":         "structural_fire",
    "civil_disorder":         "public_gathering",
}


@dataclass
class ClassificationResult:
    """Output of the rule-based classification engine."""
    primary_type:          str
    sub_type:              str
    primary_score:         float
    alternate_hypotheses:  list[dict]       # [{type, confidence, reason}]
    human_review_required: bool
    evidence_keywords:     list[str]        # matched keywords for evidence display
    confidence_gap:        float            # primary_score - top_alternate_score


def classify_signals(signals: list[dict], confidence: float) -> ClassificationResult:
    """
    Rule-based crisis classification from signal text.

    Scans all signal text for keyword hits, scores each crisis type,
    then returns primary + alternates. Flags human review if the
    confidence gap between primary and leading alternate is < 0.38.

    This is the function the AI Analysis screen should display.
    """
    all_text = " ".join(
        (s.get("normalized_text") or s.get("raw_text", "")).lower()
        for s in signals
    )

    # Score each crisis type by keyword density
    type_scores: dict[str, float] = {}
    matched_keywords: dict[str, list[str]] = {}
    for crisis_type, keywords in CRISIS_KEYWORDS.items():
        hits = [kw for kw in keywords if kw in all_text]
        score = len(hits) / len(keywords) if keywords else 0.0
        type_scores[crisis_type] = score
        matched_keywords[crisis_type] = hits

    if not any(type_scores.values()):
        # No keyword match — low confidence unknown
        return ClassificationResult(
            primary_type="unknown",
            sub_type="unknown",
            primary_score=0.0,
            alternate_hypotheses=[],
            human_review_required=True,
            evidence_keywords=[],
            confidence_gap=0.0,
        )

    sorted_types = sorted(type_scores.items(), key=lambda x: x[1], reverse=True)
    primary_type, primary_score = sorted_types[0]

    # Build alternates (score > 0.15 and not primary)
    alternates = []
    for crisis_type, score in sorted_types[1:]:
        if score > 0.15:
            alt_conf = round(score * confidence * 0.85, 3)
            alternates.append({
                "type":       crisis_type,
                "confidence": alt_conf,
                "reason":     f"Keyword match ({', '.join(matched_keywords[crisis_type][:3])})",
            })

    top_alt_conf   = alternates[0]["confidence"] if alternates else 0.0
    confidence_gap = round(confidence - top_alt_conf, 3)
    human_review   = confidence_gap < 0.38 and bool(alternates)

    return ClassificationResult(
        primary_type=primary_type,
        sub_type=CRISIS_SUBTYPES.get(primary_type, "general"),
        primary_score=round(primary_score, 3),
        alternate_hypotheses=alternates,
        human_review_required=human_review,
        evidence_keywords=matched_keywords.get(primary_type, []),
        confidence_gap=confidence_gap,
    )
