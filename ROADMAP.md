# CityCommand AI — Roadmap

## Vision
CityCommand AI transforms fragmented city crisis signals into verified incidents, prioritized resource allocations, simulated response actions, safe stakeholder messages, and auditable agent traces.

## Architecture
```
Mobile App (React Native Expo + TypeScript)
       │ HTTPS REST
Backend API (FastAPI Python)
       │ internal service calls
Agent Orchestrator (Custom deterministic)
       │ reads/writes
Data Layer (In-memory + SQLite for MVP)
       │ mock integrations
Mock APIs (Weather, Traffic, Social, Field, Vulnerability)
```

## Build Phases

### Phase 1: Foundation (Steps 1–4)
- Document analysis and roadmap
- Monorepo structure
- FastAPI backend shell
- React Native Expo mobile shell

### Phase 2: Data & Contracts (Steps 5–7)
- TypeScript + Pydantic type contracts
- Seed scenario JSON (G-10 flood + heat emergency)
- Backend Pydantic models and data layer

### Phase 3: Backend Core (Steps 8–13)
- Demo scenario endpoint
- Signal ingestion endpoints
- Incident endpoints
- Agent orchestrator
- Credibility + classification
- Severity + priority scoring

### Phase 4: Backend Advanced (Steps 14–18)
- Resource allocation service
- Simulation service
- Notification draft service
- False alarm recovery service
- Agent trace + audit log system

### Phase 5: Mobile UI (Steps 19–27)
- Navigation, splash, login
- Dashboard
- Incident list + detail
- AI analysis
- Resource allocation
- Simulation
- Notifications
- Recovery
- Agent traces

### Phase 6: Integration & Polish (Steps 28–30)
- Demo mode + backend connection
- Loading/error states
- Final testing + README + demo artifacts

## Demo Scenario
1. Run CIRO Demo → multi-source signals enter system
2. System classifies G-10 flooding (primary) + water-main burst (alternate)
3. Second incident: heat emergency in nearby low-income area
4. Resources allocated across both incidents with trade-offs
5. Simulation shows before/after impact
6. Stakeholder messages drafted, public alert requires approval
7. Field verification triggers false alarm recovery → reclassify to water-main burst
8. Agent traces visible throughout

## Success Metrics
- 4+ signal sources fused
- 2+ simultaneous incidents
- 10+ agent trace entries
- 4+ response actions simulated
- 6+ stakeholder audiences
- 2+ fallback scenarios
- 1 complete false alarm recovery
- 3–5 minute demo
