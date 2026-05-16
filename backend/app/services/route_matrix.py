"""
CityCommand AI — Mock Route Matrix Service

Provides travel time (ETA) estimates between resource home
locations and incident centroids.

In production: replaced by a real routing API (OSRM, Google Maps, etc.)
For the hackathon demo: deterministic lookup table + formula so
ETAs are realistic and consistent across runs.

Average speed assumptions (Islamabad urban traffic):
  - Normal:    35 km/h → ~1.7 min/km
  - Congested: 12 km/h → ~5.0 min/km
  - Emergency: 55 km/h → ~1.1 min/km (with siren)
"""

import math

# ─────────────────────────────────────────────────
# Hardcoded ETAs for known resource → incident pairs
# Format: (resource_id, incident_location_key) → eta_min
# ─────────────────────────────────────────────────
_ETA_TABLE: dict[tuple[str, str], int] = {
    ("res_pump_01",  "g10"): 12,
    ("res_pump_02",  "g10"): 18,
    ("res_cop_01",   "g10"):  8,
    ("res_cop_02",   "g10"): 11,
    ("res_amb_01",   "g10"): 14,
    ("res_amb_02",   "g10"): 16,
    ("res_cool_01",  "g10"): 22,
    ("res_water_01", "g10"): 25,

    ("res_pump_01",  "f11"): 20,
    ("res_pump_02",  "f11"): 26,
    ("res_cop_01",   "f11"): 15,
    ("res_cop_02",   "f11"): 18,
    ("res_amb_01",   "f11"): 14,
    ("res_amb_02",   "f11"): 16,
    ("res_cool_01",  "f11"): 19,
    ("res_water_01", "f11"): 22,
}

# Location → geohash key mapping
_LOCATION_KEY_MAP: dict[str, str] = {
    "g-10": "g10", "g10": "g10",
    "kashmir": "g10",
    "f-11": "f11", "f11": "f11",
    "katchi": "f11",
}

def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Haversine formula for distance in km."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dlng / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_eta(
    resource_id: str,
    resource_lat: float,
    resource_lng: float,
    incident_lat: float,
    incident_lng: float,
    incident_area: str = "",
    emergency_mode: bool = True,
) -> int:
    """
    Return ETA in minutes from resource home to incident centroid.

    Lookup order:
      1. Hardcoded table (most accurate for demo)
      2. Haversine distance / emergency speed formula
    """
    # Match incident area to location key
    lower_area = incident_area.lower()
    loc_key    = None
    for k, v in _LOCATION_KEY_MAP.items():
        if k in lower_area:
            loc_key = v
            break

    # Try hardcoded lookup first
    if loc_key:
        table_eta = _ETA_TABLE.get((resource_id, loc_key))
        if table_eta:
            return table_eta

    # Fallback: haversine + speed formula
    dist_km     = _haversine_km(resource_lat, resource_lng, incident_lat, incident_lng)
    speed_kmh   = 55.0 if emergency_mode else 35.0
    eta_minutes = int(math.ceil(dist_km / speed_kmh * 60))
    return max(eta_minutes, 3)   # Minimum 3 minutes
