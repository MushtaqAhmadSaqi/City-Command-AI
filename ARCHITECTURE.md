# CityCommand AI — Architecture

## System Overview

```
┌─────────────────────────────────────────────┐
│          Mobile App (React Native Expo)      │
│  Screens → Services → API Client → Store    │
└──────────────────┬──────────────────────────┘
                   │ HTTPS REST (BASE_URL)
┌──────────────────▼──────────────────────────┐
│          FastAPI Backend                     │
│  Routes → Agent Orchestrator → Services     │
│            ↓                                │
│  Schemas (Pydantic) ← Data Layer (In-mem)   │
│            ↓                                │
│  Seed Data (JSON) + Mock APIs               │
│            ↓                                │
│  Trace Store + Audit Logs                   │
└─────────────────────────────────────────────┘
```

## Mobile App Structure

```
mobile/src/
├── navigation/
│   └── AppNavigator.tsx           # Stack + Tab navigation
├── screens/
│   ├── SplashScreen.tsx           # Brand entry
│   ├── LoginScreen.tsx            # Mock role selection
│   ├── HomeDashboardScreen.tsx    # Command overview
│   ├── IncidentsScreen.tsx        # Map/list view
│   ├── SignalIntakeScreen.tsx     # Signal submission
│   ├── IncidentDetailScreen.tsx   # Full incident context
│   ├── AIAnalysisScreen.tsx       # Classification explanation
│   ├── ResourceAllocationScreen.tsx  # Resource assignments
│   ├── SimulationScreen.tsx       # Before/after impact
│   ├── NotificationScreen.tsx     # Stakeholder messages
│   ├── RecoveryScreen.tsx         # False alarm correction
│   ├── AgentTraceScreen.tsx       # Agent workflow log
│   └── DemoModeScreen.tsx         # Demo controls
├── components/
│   ├── SeverityChip.tsx           # Color-coded severity badge
│   ├── ConfidenceMeter.tsx        # Visual confidence indicator
│   ├── IncidentCard.tsx           # Incident summary card
│   ├── EvidenceList.tsx           # Evidence items list
│   ├── ResourceAssignmentCard.tsx # Resource assignment display
│   ├── SimulationDeltaCard.tsx    # Before/after comparison
│   └── AgentTraceCard.tsx         # Trace entry card
├── services/
│   ├── api.ts                     # API client with BASE_URL
│   └── demoService.ts            # Demo data management
├── store/
│   ├── incidentStore.ts          # Incident state
│   ├── signalStore.ts            # Signal state
│   └── traceStore.ts             # Trace state
└── types/
    └── index.ts                   # Shared TypeScript types
```

## Backend Structure

```
backend/app/
├── main.py                        # FastAPI app entry + CORS
├── routes/
│   ├── signals.py                 # POST/GET /signals
│   ├── incidents.py               # GET /incidents, /incidents/{id}, classify, severity
│   ├── demo.py                    # POST /demo/run-scenario
│   ├── resources.py               # POST /incidents/allocate-resources
│   ├── simulations.py             # POST /incidents/{id}/simulate
│   ├── notifications.py           # POST /notifications/draft, /send-mock
│   ├── traces.py                  # GET /traces
│   └── health.py                  # GET /health/apis
├── agents/
│   ├── signal_intake.py           # Signal Intake Agent
│   ├── signal_cleaning.py         # Signal Cleaning Agent
│   ├── geolocation.py             # Geolocation Agent
│   ├── credibility.py             # Credibility Scoring Agent
│   ├── classification.py          # Crisis Classification Agent
│   ├── severity.py                # Severity Prediction Agent
│   ├── allocation.py              # Resource Allocation Agent
│   ├── simulation.py              # Simulation Agent
│   ├── notification.py            # Stakeholder Notification Agent
│   ├── recovery.py                # False Alarm Recovery Agent
│   └── briefing.py                # Command Center Briefing Agent
├── services/
│   ├── scoring.py                 # Confidence + priority scoring formulas
│   ├── clustering.py              # Duplicate detection
│   ├── route_matrix.py            # Mock route/ETA calculations
│   ├── fallback.py                # Degraded mode handling
│   └── audit.py                   # Audit log service
├── schemas/
│   └── models.py                  # Pydantic models for all entities
├── seed/
│   └── scenario_g10_heat.json     # G-10 flood + heat demo data
└── tests/
    └── (test files)
```

## Agent Pipeline

```
Signal Intake → Signal Cleaning → Geolocation → Credibility Scoring
    → Crisis Classification → Severity Prediction → Resource Allocation
    → Simulation → Stakeholder Notification → Human Review Gate
    → Mock Execution → False Alarm Recovery → Command Center Briefing
```

## Data Pipeline

```
Raw signals
  → normalize text/time/source
  → extract location and confidence
  → cluster duplicates by time + geohash + semantic similarity
  → score credibility and contradiction
  → classify crisis type and alternate hypotheses
  → predict severity/evolution
  → rank incidents
  → allocate constrained resources
  → simulate actions and side effects
  → draft stakeholder messages
  → human approval
  → mock execution
  → trace + audit + recovery logs
```

## Design System

| Token | Value |
|---|---|
| Theme | Dark command-center UI |
| Primary | Deep navy `#0F172A` |
| Accent | Cyan `#06B6D4` |
| Critical | Red `#EF4444` |
| High Warning | Amber `#F59E0B` |
| Confirmed/Safe | Green `#22C55E` |
| Typography | Inter/Roboto, 18-24px headings, 14-16px body |
| Cards | Rounded 16px, subtle border |

## Communication

All mobile ↔ backend communication uses a single `BASE_URL` environment variable. No hardcoded URLs.
