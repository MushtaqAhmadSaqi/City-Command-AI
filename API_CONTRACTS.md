# CityCommand AI — API Contracts

## Base URL

All endpoints are relative to `BASE_URL` (e.g., `http://localhost:8000`).

---

## Endpoints

### 1. POST /signals
**Purpose:** Submit a citizen/social/field signal.  
**Auth:** citizen / operator  
**Request Body:**
```json
{
  "source_type": "social_post",
  "raw_text": "G-10 mein pani bhar gaya hai, gaariyan phans gayi hain",
  "location_text": "G-10 Islamabad",
  "timestamp": "2026-05-16T18:05:00Z",
  "metadata": {
    "user_reputation": 0.62,
    "media_attached": false,
    "language": "roman_urdu"
  }
}
```
**Response:** `201` Created signal object  
**Errors:** `400` missing text/location

---

### 2. GET /signals
**Purpose:** List recent signals.  
**Auth:** operator  
**Query Params:** `?limit=50&source_type=social_post`  
**Response:** `200` Array of signal objects

---

### 3. POST /demo/run-scenario
**Purpose:** Load main demo scenario data (G-10 flood + heat emergency).  
**Auth:** operator  
**Request Body:**
```json
{
  "scenario_id": "g10_heat_demo"
}
```
**Response:** `200` Created incidents + traces + signals  
**Errors:** `404` scenario not found

---

### 4. GET /incidents
**Purpose:** Get incident summaries.  
**Auth:** operator  
**Query Params:** `?status=active&severity=HIGH`  
**Response:** `200` Array of incident summary objects

---

### 5. GET /incidents/{id}
**Purpose:** Get full incident detail.  
**Auth:** operator  
**Response:** `200` Full incident object with classifications, severity, evidence, actions  
**Errors:** `404` incident not found

---

### 6. POST /incidents/{id}/classify
**Purpose:** Run crisis classification on an incident.  
**Auth:** operator  
**Request Body:**
```json
{
  "use_llm": false,
  "include_alternate_hypotheses": true,
  "human_review_required_if_conflict": true
}
```
**Response:** `200` Classification result with primary + alternates  
**Errors:** `422` insufficient signals

---

### 7. POST /incidents/{id}/predict-severity
**Purpose:** Run severity prediction.  
**Auth:** operator  
**Request Body:**
```json
{
  "include_spread_risk": true
}
```
**Response:** `200` Severity prediction object  
**Errors:** `422` missing location

---

### 8. POST /incidents/allocate-resources
**Purpose:** Allocate resources across multiple incidents.  
**Auth:** dispatcher / operator  
**Request Body:**
```json
{
  "incident_ids": ["inc_g10_001", "inc_heat_001"]
}
```
**Response:** `200` Assignment plan with ETAs and trade-offs  
**Errors:** `409` no resources available

---

### 9. POST /incidents/{id}/simulate
**Purpose:** Simulate response actions for an incident.  
**Auth:** operator  
**Request Body:**
```json
{
  "actions": ["traffic_reroute", "emergency_dispatch", "public_alert"]
}
```
**Response:** `200` Simulation result with before/after state  
**Errors:** `400` invalid action type

---

### 10. POST /notifications/draft
**Purpose:** Generate stakeholder notification drafts.  
**Auth:** operator  
**Request Body:**
```json
{
  "incident_id": "inc_g10_001",
  "audiences": ["public", "emergency_services", "hospitals", "utility", "traffic", "media", "field_team"]
}
```
**Response:** `200` Array of draft message objects  
**Errors:** `409` confidence too low for public notification

---

### 11. POST /notifications/send-mock
**Purpose:** Mock send an approved notification.  
**Auth:** operator / admin  
**Request Body:**
```json
{
  "notification_id": "msg_001"
}
```
**Response:** `200` Send status  
**Errors:** `403` approval not given

---

### 12. POST /alerts/{id}/retract
**Purpose:** Retract or correct a previously sent alert.  
**Auth:** operator / admin  
**Request Body:**
```json
{
  "reason": "Field verification confirmed water-main burst, not flooding"
}
```
**Response:** `200` Recovery record  
**Errors:** `404` alert not found

---

### 13. GET /traces
**Purpose:** Get agent trace entries.  
**Auth:** operator  
**Query Params:** `?incident_id=inc_g10_001&agent_name=Classification`  
**Response:** `200` Array of trace objects

---

### 14. GET /health/apis
**Purpose:** Check health status of all mock APIs.  
**Auth:** operator  
**Response:** `200` Array of API health objects

---

### 15. POST /field-reports
**Purpose:** Submit a field verification report.  
**Auth:** field_team  
**Request Body:**
```json
{
  "incident_id": "inc_g10_001",
  "finding": "water_main_burst_confirmed",
  "evidence": "Visible pipe rupture at service lane, no rainfall accumulation",
  "confidence": 0.92
}
```
**Response:** `200` Updated incident  
**Errors:** `404` incident not found

---

### 16. POST /recovery/false-alarm
**Purpose:** Run false alarm recovery flow.  
**Auth:** operator  
**Request Body:**
```json
{
  "incident_id": "inc_g10_001",
  "new_classification": "infrastructure_failure",
  "sub_type": "water_main_burst",
  "reason": "Field team confirmed pipe burst only",
  "retract_public_alert": true
}
```
**Response:** `200` Reclassified incident + recovery record  
**Errors:** `422` no field evidence submitted

---

## Common Response Envelope

```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2026-05-16T18:30:00Z",
  "trace_id": "trace_xxx"
}
```
