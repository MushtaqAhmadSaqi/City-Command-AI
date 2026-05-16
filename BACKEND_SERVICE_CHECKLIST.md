# CityCommand AI — Backend Service Checklist

## Services (13 total)

### 1. SignalService
- [ ] Accept raw signals from forms and mock APIs
- [ ] Store in incoming_signals collection
- [ ] Return structured signal objects

### 2. IncidentService
- [ ] Create/update incidents from signal clusters
- [ ] Manage incident lifecycle (candidate → active → verified → reclassified → resolved)
- [ ] Return incident summaries and details

### 3. AgentOrchestrator
- [ ] Run deterministic agent pipeline in sequence
- [ ] Create trace entries for each agent step
- [ ] Handle fallback when agents fail
- [ ] Pipeline: Intake → Clean → Geo → Credibility → Classify → Severity → Allocate → Simulate → Notify → Review → Recovery

### 4. CredibilityScoringService
- [ ] Score using: source_credibility, geo_confidence, urgency, velocity, corroboration, duplicates, media, contradiction, staleness
- [ ] Return factor breakdown + final confidence

### 5. ClassificationService
- [ ] Classify crisis type (flood, heat, accident, infrastructure, outage, disorder, disease)
- [ ] Generate alternate hypotheses
- [ ] Flag human review if conflict exists
- [ ] Fallback to rule-based if LLM unavailable

### 6. SeverityPredictionService
- [ ] Estimate: severity level, radius, population, duration, peak impact, spread risk
- [ ] Include uncertainty ranges
- [ ] Conservative estimates when data missing

### 7. ResourceAllocationService
- [ ] Accept multiple incidents + resource inventory
- [ ] Calculate priority-weighted assignments
- [ ] Include ETA and trade-off explanations
- [ ] Handle resource scarcity and reserves

### 8. SimulationService
- [ ] Accept action plan + before state
- [ ] Calculate after state with deltas
- [ ] Generate side effects list
- [ ] Support: reroute, dispatch, alert, ticket, advisory

### 9. NotificationService
- [ ] Generate drafts for 7 audiences: public, emergency, hospitals, utility, traffic, media, field
- [ ] Apply CAP-like fields (hazard, area, severity, certainty, instruction)
- [ ] Public messages require approval
- [ ] Disable public if confidence < threshold

### 10. RecoveryService
- [ ] Accept field verification evidence
- [ ] Reclassify incident
- [ ] Create false_alarm_record
- [ ] Generate retraction/correction message
- [ ] Update audit log

### 11. TraceService
- [ ] Store agent trace entries
- [ ] Query by incident, workflow, agent
- [ ] Return timeline-ordered traces

### 12. ApiHealthService
- [ ] Track mock API status (healthy/degraded/down)
- [ ] Log latency and fallback usage
- [ ] Support demo toggle for API failures

### 13. AuditService
- [ ] Log all state changes with actor, entity, before/after
- [ ] Support human/agent/system actor types
- [ ] Query by entity or actor

## Agents (11 total)

| # | Agent | Status |
|---|---|---|
| 1 | Signal Intake Agent | [ ] |
| 2 | Signal Cleaning Agent | [ ] |
| 3 | Geolocation Agent | [ ] |
| 4 | Credibility Scoring Agent | [ ] |
| 5 | Crisis Classification Agent | [ ] |
| 6 | Severity Prediction Agent | [ ] |
| 7 | Resource Allocation Agent | [ ] |
| 8 | Simulation Agent | [ ] |
| 9 | Stakeholder Notification Agent | [ ] |
| 10 | False Alarm Recovery Agent | [ ] |
| 11 | Command Center Briefing Agent | [ ] |

## Data Models (16 tables)

| # | Model | Status |
|---|---|---|
| 1 | users | [ ] |
| 2 | roles | [ ] |
| 3 | signal_sources | [ ] |
| 4 | incoming_signals | [ ] |
| 5 | incidents | [ ] |
| 6 | crisis_classifications | [ ] |
| 7 | severity_predictions | [ ] |
| 8 | resources | [ ] |
| 9 | resource_assignments | [ ] |
| 10 | response_actions | [ ] |
| 11 | simulations | [ ] |
| 12 | stakeholder_notifications | [ ] |
| 13 | agent_traces | [ ] |
| 14 | audit_logs | [ ] |
| 15 | api_health_logs | [ ] |
| 16 | false_alarm_records | [ ] |
