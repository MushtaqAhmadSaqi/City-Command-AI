---
title: "CityCommand AI - Antigravity Readable Build Specification"
project: "CityCommand AI"
product: "Agentic Crisis Intelligence & Response Orchestrator"
source_document: "CityCommand_AI_CIRO_Comprehensive_Product_Report(1).docx"
version: "1.0"
date: "2026-05-16"
intended_reader: "Google Antigravity / AI coding agent"
format: "Markdown / GitHub Flavored Markdown"
---

# ANTIGRAVITY READ ME FIRST

This file is the clean Markdown version of the CityCommand AI product report. Treat it as the source of truth for planning and implementation.

## Primary instruction for Antigravity

Analyze this file first, then create a step-by-step implementation roadmap before writing code. Build the project in controlled increments. After each step, update `IMPLEMENTATION_PROGRESS.md` and wait for the user instruction `NEXT STEP` before continuing.

## Required build behavior

- Build a mobile-first hackathon prototype for CityCommand AI.
- Use React Native Expo + TypeScript for the mobile app.
- Use FastAPI + Python for the backend.
- Use mock/demo data first; avoid fragile live API dependencies.
- Use deterministic backend logic first; keep optional LLM/Gemini usage isolated.
- All apps must communicate with the backend through `BASE_URL` only.
- Preserve the document's MVP scope, demo flow, agent pipeline, API design, UX screens, and judging proof points.
- Do not redesign the product unless a change is required for implementation correctness.
- Maintain a clear implementation log and mark every completed phase.

## Recommended first action

Create these project-control files before implementation:

1. `IMPLEMENTATION_PROGRESS.md`
2. `ROADMAP.md`
3. `ARCHITECTURE.md`
4. `API_CONTRACTS.md`
5. `MOBILE_SCREEN_CHECKLIST.md`
6. `BACKEND_SERVICE_CHECKLIST.md`

---

# SOURCE DOCUMENT CONTENT

**CityCommand AI**

**Agentic Crisis Intelligence & Response Orchestrator**

Comprehensive Product, Technical, UX, Backend, API, Demo, and Implementation Report

Prepared for: Google Antigravity Hackathon Team

Version: 1.0 | Date: May 16, 2026

| **Document Purpose**  | **What this file gives your team**                                                                               |
|-----------------------|------------------------------------------------------------------------------------------------------------------|
| Product strategy      | Clear product vision, winning positioning, personas, goals, MVP scope, and acceptance criteria.                  |
| Engineering blueprint | Practical architecture, agents, APIs, database schema, mock data, fallback logic, and build order.               |
| UX direction          | Mobile-first screens, design system, interaction flows, empty states, and AI coder notes.                        |
| Hackathon execution   | Day-by-day plan, demo scenario, stress tests, demo script, judging answers, README plan, and vibe-coder prompts. |

**Core pitch: CityCommand AI turns fragmented city crisis signals into verified incidents, prioritized response actions, simulated outcomes, stakeholder messages, and auditable Antigravity agent traces.**

# Table of Contents

1. Executive Summary

2. Product Vision

3. PRD - Product Requirements Document

4. TRD - Technical Requirements Document

5. Google Antigravity Multi-Agent Architecture

6. UI/UX Design Specification

7. App Flow, User Flow, and System Flow

8. Backend Schema, Database, and Data Contracts

9. API Design

10. Implementation Plan for MVP and Hackathon Demo

11. Vibe Coder / AI Coder Build Requirements

12. Demo Video Script

13. Judging Strategy

14. Risks, Limitations, Safety, and Governance

15. Final Recommended MVP

Appendix A. Scoring Models and Decision Logic

Appendix B. Mock Dataset and Demo Scenario Pack

Appendix C. Stress Tests and QA Plan

Appendix D. README Template

Appendix E. Glossary

Appendix F. Research Sources and References

# Research-Grounded Design Basis

This report uses official and high-quality sources for current platform capabilities and emergency-management design logic. The most important constraint is that public information positions Google Antigravity primarily as an agent-first development platform and IDE, not as a confirmed production emergency-response runtime. Therefore, this product plan uses Antigravity deeply for build orchestration, multi-agent workflow design, verification artifacts, traceability, and demo proof, while recommending a deployable backend agent runtime using Google ADK or a custom FastAPI orchestrator.

| **Source area**                  | **Design implication for CityCommand AI**                                                                                                                                                |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Google Antigravity               | Use Antigravity as the visible agentic development, orchestration, browser/terminal verification, and artifact-generation workspace. Show logs and artifacts to prove agentic execution. |
| Google ADK                       | Use ADK or a custom orchestrator for deployable multi-agent runtime patterns, tool use, workflow agents, and Cloud Run deployment.                                                       |
| FEMA NIMS / EOC                  | Model the product around multi-agency coordination, command-center handoff, structured roles, and auditable decision records.                                                            |
| OASIS CAP                        | Structure public alerts around hazard type, affected area, severity, certainty, urgency, instruction, and cancellation/correction.                                                       |
| NIST AI RMF                      | Use risk management, human review, audit logs, fallback behavior, and safe use boundaries for high-impact AI decisions.                                                                  |
| WHO heat-health action           | Treat heat emergencies as multi-sector response problems involving health, water, power, transport, vulnerable groups, and public messaging.                                             |
| FHWA Traffic Incident Management | Design rerouting and road incident response as coordinated multi-disciplinary actions with before/after impact simulation.                                                               |
| World Bank urban flood risk      | Include hazard exposure, drainage/low-lying areas, vulnerability layers, and intervention evaluation in flood response.                                                                  |

# 1. Executive Summary

## One-line pitch

**CityCommand AI is a mobile-first agentic command system that transforms noisy multi-source crisis signals into verified incidents, prioritized resource allocations, simulated response actions, safe stakeholder messages, and auditable Antigravity agent traces.**

## The problem

Cities receive signals from social posts, weather systems, traffic maps, citizen complaints, emergency calls, sensors, field teams, and historical vulnerability data. These sources are often fragmented across departments and dashboards. The operational problem is not only detecting a flood, heat emergency, accident, outage, or infrastructure failure. The deeper problem is converting incomplete, noisy, conflicting signals into coordinated action quickly enough to reduce harm.

## The solution

CityCommand AI creates an end-to-end crisis intelligence loop: ingest signals, clean them, geolocate them, score credibility, classify crisis type, predict severity, prioritize incidents, allocate constrained resources, simulate response actions, generate stakeholder-specific messages, support human approval, and recover from false positives or wrong classifications.

## Why it matters

Urban flooding, heatwaves, road blockages, accidents, infrastructure failures, public disorder, disease clusters, and power outages can cascade. A flood can block roads, delay ambulances, overload hospitals, spread misinformation, and create secondary congestion. A heat emergency can strain hospitals, water services, power systems, and public transport. CityCommand AI helps a command center see the whole system instead of isolated alerts.

## Why it can win the hackathon

- It directly satisfies the challenge requirement for multi-source ingestion, crisis detection, action planning, simulation, outcome visualization, and agentic workflow.

- It demonstrates Google Antigravity deeply through multi-agent build orchestration, traceable agent workflows, verification artifacts, and a visible Agent Trace screen.

- It handles two simultaneous incidents, so judges see prioritization and resource trade-offs, not only a single alert.

- It includes misinformation/conflict handling, duplicate merging, degraded-mode fallback, and false alarm recovery.

- It is mobile-first, which meets the mandatory prototype requirement and keeps the demo clear.

## MVP scope

The recommended MVP is a polished mobile app and FastAPI backend in demo mode. The main scenario is probable urban flooding in G-10/George Town, supported by social posts, heavy rainfall, and traffic congestion, while one field report suggests a broken water main. Simultaneously, a heat emergency is reported in a nearby low-income neighborhood. The system allocates limited rescue, traffic, medical, utility, and water resources; simulates rerouting, dispatch, alerting, and tickets; and then demonstrates recovery if field verification confirms the water-main hypothesis.

# 2. Product Vision

## Name options

| **Option**           | **Why it works**                                                                                                                            |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| CityCommand AI       | Strong, direct, command-center oriented, easy to remember, and broad enough for flood, heat, traffic, utilities, health, and public safety. |
| CrisisGrid AI        | Emphasizes citywide networked intelligence and multi-crisis coordination.                                                                   |
| UrbanShield AgentOps | Security and resilience oriented, but slightly less civic and more defense-sounding.                                                        |
| SignalRescue AI      | Highlights signal-to-response transformation, but narrower than full command orchestration.                                                 |
| CivicPulse Command   | Good civic intelligence feel, but less direct for emergency response.                                                                       |

**Selected name: CityCommand AI - Agentic Crisis Intelligence & Response System.**

## Mission

Help city response teams detect, verify, prioritize, coordinate, simulate, and communicate localized crises before fragmented signals become delayed response.

## Target users

| **User**                   | **Primary need**                                           | **What they see in the app**                                                                 |
|----------------------------|------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| Command center operator    | Understand what is happening and what to do first.         | Priority-ranked incidents, confidence, evidence, resources, simulation, messages, approvals. |
| Emergency dispatcher       | Assign limited teams efficiently.                          | Resource availability, ETA, constraints, assignment justification.                           |
| Traffic authority          | Reduce congestion and preserve emergency access.           | Reroute recommendation, before/after congestion, side effects.                               |
| Utility provider           | Verify water, power, drainage, or infrastructure failures. | Utility tickets, field evidence, reclassification notices.                                   |
| Hospital coordinator       | Prepare for surge or access disruption.                    | Hospital advisories, expected cases, arrival windows, access risk.                           |
| Field verification team    | Confirm, correct, or downgrade incidents.                  | Field report form, task location, required evidence, status update.                          |
| Public information officer | Send safe, accurate messages.                              | Audience-specific drafts, certainty labels, correction/retraction flow.                      |

## Differentiation

CityCommand AI is more than a normal dashboard because it does not only display incidents. It runs an auditable agentic decision pipeline. The core differentiators are:

- Specialized agents with explicit inputs, outputs, tools, decision logic, and failure behavior.

- Confidence and priority scores that are decomposed into understandable factors.

- Multi-crisis coordination with limited resources and transparent trade-offs.

- Before/after simulation for traffic, dispatch, alerts, tickets, and resource cost.

- Human-in-the-loop safety for public alerts and high-impact decisions.

- False positive and wrong-classification recovery as a first-class feature.

- Antigravity artifacts and trace logs that make the agentic workflow visible to judges.

## Product positioning statement

For city command centers that struggle with fragmented crisis signals, CityCommand AI is an agentic response orchestrator that fuses multi-source data, classifies emerging crises, allocates constrained resources, simulates response impact, and safely coordinates stakeholders. Unlike a map dashboard, CityCommand AI gives explainable, auditable, and recoverable decisions.

# 3. PRD - Product Requirements Document

## Product overview

CityCommand AI is a mobile-first crisis intelligence and response coordination system. It is designed for hackathon delivery as a working prototype with mock APIs and synthetic data, while preserving a realistic architecture that could scale to production with real integrations.

## Goals

| **Goal**               | **Description**                                                                           | **MVP evidence**                                                                             |
|------------------------|-------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| Multi-source detection | Fuse at least three sources per scenario.                                                 | Social posts + weather + traffic + field report + vulnerability layer.                       |
| Agentic reasoning      | Demonstrate multi-agent interaction and decision traceability.                            | Agent Trace screen with inputs, outputs, tools, confidence, and fallback.                    |
| Crisis classification  | Identify type, location, severity, confidence, affected population, and likely evolution. | G-10 urban flooding with alternate water-main hypothesis; heat emergency as second incident. |
| Resource optimization  | Allocate constrained city resources across competing incidents.                           | Rescue/police to flood, medical/water support to heat zone, reserve ambulance decision.      |
| Impact simulation      | Show before/after state and side effects.                                                 | Congestion index, ETA improvement, public alert side-effect warning.                         |
| Recovery               | Correct false alarms or wrong classifications.                                            | Flood alert retracted and reclassified as water-main burst after field verification.         |

## Non-goals

- Do not connect to real emergency dispatch systems during hackathon.

- Do not send real public emergency alerts.

- Do not scrape private social media or use sensitive citizen data.

- Do not claim certified emergency prediction accuracy.

- Do not automate life-safety decisions without human approval.

- Do not build a large ML training pipeline; use deterministic logic plus optional LLM explanations.

## Personas and user stories

| **Persona**                | **User story**                                                                               | **Acceptance expectation**                                                                  |
|----------------------------|----------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Operator                   | As an operator, I want incidents ranked by priority so I can decide what needs action first. | Dashboard shows priority score, severity, confidence, and recommended next action.          |
| Operator                   | As an operator, I want to see why AI classified an incident as flooding.                     | AI analysis screen shows evidence, contradictions, and score breakdown.                     |
| Dispatcher                 | As a dispatcher, I want resource recommendations with constraints and ETAs.                  | Allocation screen shows each resource, ETA, scarcity, and reason.                           |
| Traffic authority          | As a traffic authority user, I want to simulate reroutes before approving them.              | Simulation screen shows congestion before/after and side effects.                           |
| Public information officer | As a communicator, I want safe messages for different audiences.                             | Notification screen shows public, hospital, utility, traffic, media, and field-team drafts. |
| Field verifier             | As a field team member, I want to correct an incident if AI was wrong.                       | Recovery screen reclassifies incident, retracts alert, and updates logs.                    |

## Core product features

| **Feature**               | **Practical detail**                                                                                                                                    |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| Signal intake             | Accept social/citizen text, weather, traffic, field reports, emergency-call frequency, sensors, and vulnerability layers.                               |
| Signal normalization      | Clean informal language, normalize time, detect language, extract location, remove duplicates, and preserve uncertainty.                                |
| Credibility scoring       | Score source credibility, geolocation confidence, urgency language, mention velocity, contradiction, duplicates, staleness, and official corroboration. |
| Crisis classification     | Classify flood, heatwave, accident, infrastructure failure, power outage, public disorder, or disease cluster.                                          |
| Severity prediction       | Estimate affected radius, population, duration, peak impact, spread risk, uncertainty range, and likely evolution.                                      |
| Resource allocation       | Allocate ambulances, police, rescue teams, shelters, generators, water tankers, drones, hospitals, utility teams, and field teams.                      |
| Multi-crisis coordination | Handle two or more incidents competing for limited resources and show the trade-off.                                                                    |
| Simulation                | Show before state, response action, after state, ETA improvement, congestion effect, resource cost, and side effects.                                   |
| Stakeholder notification  | Generate tailored messages for public, emergency services, hospitals, utilities, traffic, media, and field teams.                                       |
| False alarm recovery      | Verify, correct, retract, update logs, notify stakeholders, and preserve audit trail.                                                                   |
| Robustness                | Handle API downtime, stale data, missing location, duplicates, rate limits, conflicting sources, and low-confidence reports.                            |
| Agent traces              | Show step-by-step agent workflow from signal fusion to final action.                                                                                    |

## MVP features

- Mobile app with demo role login.

- Dashboard with two active incidents and API health.

- Signal intake form plus one-click demo scenario loader.

- Incident list and incident detail screen.

- AI analysis screen with evidence, confidence, and alternate hypothesis.

- Resource allocation screen for two simultaneous incidents.

- Action simulation screen with before/after metrics.

- Stakeholder notification drafts with human approval.

- False alarm recovery screen.

- Agent trace/log screen.

- Backend seed data and mock APIs.

- README, screenshots, and demo video script.

## Advanced features after MVP

- Real traffic and route matrix integration.

- Real push notifications via Firebase Cloud Messaging.

- PostGIS geospatial queries and polygon-based affected zones.

- Optional web command dashboard.

- Role-based auth and audit permissions.

- Real sensor ingestion and public complaint systems.

- Disease cluster model with verification-only public messaging.

- Historical vulnerability maps from city planning, hospitals, shelters, drainage, and census layers.

- Offline-first mobile field verification.

## Functional requirements

| **ID** | **Functional requirement**                                                                                                                                 |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-01  | System shall ingest at least three signal sources per incident in the main demo.                                                                           |
| FR-02  | System shall normalize informal English/Roman Urdu/Urdu-style text into structured signals.                                                                |
| FR-03  | System shall extract or infer location and assign a geolocation confidence score.                                                                          |
| FR-04  | System shall cluster duplicate reports into one incident candidate.                                                                                        |
| FR-05  | System shall classify crisis type with primary and alternate hypotheses.                                                                                   |
| FR-06  | System shall calculate confidence score using source credibility, geolocation, urgency, velocity, contradiction, duplicates, staleness, and corroboration. |
| FR-07  | System shall calculate severity, affected radius, population estimate, duration, peak impact, and spread risk.                                             |
| FR-08  | System shall rank incidents by priority and show why.                                                                                                      |
| FR-09  | System shall allocate constrained resources across at least two simultaneous incidents.                                                                    |
| FR-10  | System shall show trade-off explanations for resource allocation.                                                                                          |
| FR-11  | System shall simulate traffic reroute, emergency dispatch, utility ticket, hospital advisory, and public alert outcomes.                                   |
| FR-12  | System shall generate tailored stakeholder messages.                                                                                                       |
| FR-13  | System shall require human approval before sending public alert or retraction.                                                                             |
| FR-14  | System shall support false alarm correction and reclassification.                                                                                          |
| FR-15  | System shall record agent traces, audit logs, and API health/fallback logs.                                                                                |

## Non-functional requirements

| **Category**   | **Requirement**                                     | **MVP target**                                     |
|----------------|-----------------------------------------------------|----------------------------------------------------|
| Latency        | Pipeline should feel real-time in demo.             | Under 5 seconds with mock data.                    |
| Reliability    | API failures should not crash the app.              | Fallback to cached/mock data and lower confidence. |
| Explainability | Every score must have evidence.                     | Score breakdown shown on AI analysis screen.       |
| Safety         | High-impact actions require review.                 | Public alerts and retractions need approval.       |
| Privacy        | Avoid personal data.                                | Synthetic demo data and area-level location.       |
| Scalability    | Architecture should support queued ingestion later. | Monolith now, service boundaries documented.       |
| Accessibility  | Readable under pressure.                            | High contrast, clear labels, large tap targets.    |
| Auditability   | All decisions recorded.                             | Trace and audit logs visible in app.               |

## Success metrics

| **Metric**                 | **Hackathon target**                                  |
|----------------------------|-------------------------------------------------------|
| Signal sources fused       | 4+ in the main demo.                                  |
| Simultaneous incidents     | At least 2.                                           |
| Agent traces               | 10+ visible trace entries.                            |
| Response actions simulated | At least 4.                                           |
| Stakeholder messages       | At least 6 audiences.                                 |
| Fallback scenarios         | At least 2: API failure and conflicting field report. |
| False alarm recovery       | One complete correction/retraction flow.              |
| Demo length                | 3-5 minutes.                                          |
| Mobile app                 | Working prototype mandatory.                          |

## Acceptance criteria

1.  A user can run the main demo scenario from the mobile dashboard.

2.  The system creates G-10 probable flooding and a separate heat emergency incident.

3.  The G-10 incident shows urban flooding as primary and water-main burst as alternate hypothesis.

4.  Confidence, severity, affected population, expected duration, and priority are displayed.

5.  The system allocates limited resources across both incidents and explains trade-offs.

6.  The system simulates reroute, dispatch, hospital advisory, utility ticket, and public alert.

7.  The system drafts stakeholder messages but requires approval for public alert.

8.  The field report correction changes G-10 from flood to water-main infrastructure failure.

9.  The system retracts/corrects the public flood alert and updates utility ticket.

10. Agent trace and audit screens show what each agent did.

# 4. TRD - Technical Requirements Document

## Recommended architecture

Mobile App (React Native Expo)

| HTTPS REST

Backend API (FastAPI Python)

| internal service calls

Agent Orchestrator (Google ADK or custom deterministic orchestrator)

| reads/writes

Database (PostgreSQL + PostGIS in production, SQLite/JSON for MVP)

| optional

Cache / Queue (Redis or in-memory demo queue)

| mock integrations

Weather, Traffic, Social, Field Reports, Vulnerability, Resources

## Recommended tech stack

| **Layer**     | **Recommendation**                                        | **Reason**                                                                                     |
|---------------|-----------------------------------------------------------|------------------------------------------------------------------------------------------------|
| Mobile app    | React Native Expo + TypeScript                            | Fastest path to cross-platform mobile prototype and matches mandatory mobile requirement.      |
| UI styling    | NativeWind or custom design tokens                        | Fast dark command-center UI with consistent spacing and colors.                                |
| Backend       | FastAPI Python                                            | Clear REST APIs, easy Pydantic schemas, simple agent integration.                              |
| Agent runtime | Google ADK or custom Python orchestrator                  | ADK aligns with Google agent ecosystem; custom orchestrator is safest if ADK setup takes time. |
| LLM           | Gemini API where available                                | Aligned with Google ecosystem; use optional for summarization/message generation.              |
| Database      | SQLite for demo; PostgreSQL + PostGIS for production path | SQLite is quick; PostGIS supports geospatial incident queries.                                 |
| Maps/traffic  | Mock first; optional Google Maps Routes API               | Routes API supports Compute Routes and Compute Route Matrix for distances/travel times.        |
| Notifications | Mock first; optional Firebase Cloud Messaging             | FCM provides cross-platform app messaging; use mock in demo unless time allows.                |
| Hosting       | Cloud Run, Render, Railway, or local tunnel               | Simple backend deployment for judges.                                                          |

## Mobile app architecture

mobile/src/

navigation/

AppNavigator.tsx

screens/

SplashScreen.tsx

LoginScreen.tsx

HomeDashboardScreen.tsx

IncidentsScreen.tsx

SignalIntakeScreen.tsx

IncidentDetailScreen.tsx

AIAnalysisScreen.tsx

ResourceAllocationScreen.tsx

SimulationScreen.tsx

NotificationScreen.tsx

RecoveryScreen.tsx

AgentTraceScreen.tsx

DemoModeScreen.tsx

components/

SeverityChip.tsx

ConfidenceMeter.tsx

IncidentCard.tsx

EvidenceList.tsx

ResourceAssignmentCard.tsx

SimulationDeltaCard.tsx

AgentTraceCard.tsx

services/

api.ts

demoService.ts

store/

incidentStore.ts

signalStore.ts

traceStore.ts

types/

index.ts

## Backend architecture

backend/app/

main.py

routes/

signals.py

incidents.py

demo.py

resources.py

simulations.py

notifications.py

traces.py

health.py

agents/

signal_intake.py

signal_cleaning.py

geolocation.py

credibility.py

classification.py

severity.py

allocation.py

simulation.py

notification.py

recovery.py

briefing.py

services/

scoring.py

clustering.py

route_matrix.py

fallback.py

audit.py

schemas/

models.py

seed/

scenario_g10_heat.json

tests/

## Data pipeline

Raw signals

-\> normalize text/time/source

-\> extract location and confidence

-\> cluster duplicates by time + geohash + semantic similarity

-\> score credibility and contradiction

-\> classify crisis type and alternate hypotheses

-\> predict severity/evolution

-\> rank incidents

-\> allocate constrained resources

-\> simulate actions and side effects

-\> draft stakeholder messages

-\> human approval

-\> mock execution

-\> trace + audit + recovery logs

## Security and privacy

- Use JWT/Firebase Auth for production; mock role selection for hackathon.

- Separate roles: operator, dispatcher, field_team, public_info, admin, viewer.

- Do not store real names, phone numbers, exact addresses, or sensitive emergency-call audio in MVP.

- Hash citizen IDs if user accounts are simulated.

- Public alerts should reference areas, not individuals.

- All high-impact public actions require human approval and audit logs.

- Store API keys in environment variables only.

- Rate-limit public signal submission and sanitize all text input.

## Scalability path

The MVP can be a single FastAPI backend with in-memory demo data. For a production-like path, split the backend into signal ingestion, agent orchestration, incident intelligence, resource allocation, simulation, notification, and trace services. Add a message queue for incoming signals and an event stream for live dashboard updates.

## Cost and latency planning

| **Component**   | **MVP cost**               | **Latency expectation**              | **Production note**                                        |
|-----------------|----------------------------|--------------------------------------|------------------------------------------------------------|
| Mock APIs       | \$0                        | \<100 ms                             | Replace with real integrations later.                      |
| FastAPI backend | Free/low                   | \<300 ms for deterministic endpoints | Deploy on Cloud Run or equivalent.                         |
| LLM calls       | Quota-dependent            | 1-3 seconds                          | Use only for summaries/messages, not every screen refresh. |
| Routes API      | Billed if live             | Higher if traffic-aware              | Use only on simulation or allocation refresh.              |
| FCM             | No direct FCM service cost | Seconds-level delivery               | Use mock send for demo safety.                             |
| PostGIS         | Low if small DB            | Fast with indexes                    | Needed for real polygon/radius search.                     |

## Fallback logic

| **Failure**              | **Fallback behavior**                            | **User-visible effect**                            |
|--------------------------|--------------------------------------------------|----------------------------------------------------|
| Weather API down         | Use cached weather and reduce confidence.        | Banner: Weather source degraded.                   |
| Traffic API down         | Use historical/mock congestion baseline.         | Simulation marked estimated.                       |
| Missing location         | Infer from text or ask for manual location.      | Geo confidence low; no public alert.               |
| Duplicate reports        | Merge into cluster but preserve source count.    | Incident evidence shows duplicate cluster.         |
| Conflicting field report | Create alternate hypothesis and require review.  | Conflict panel shown.                              |
| LLM failure              | Use rule-based classifier and template messages. | Trace shows fallback.                              |
| Rate limit               | Batch signals and queue analysis.                | Dashboard says delayed processing.                 |
| Stale data               | Penalize source score.                           | Confidence explanation includes staleness penalty. |

# 5. Google Antigravity Multi-Agent Architecture

## Confirmed platform usage

Google Antigravity should be treated as the agent-first development and orchestration surface for the hackathon project. Official Google material describes Antigravity as a platform where agents can autonomously plan, execute, and verify tasks across the editor, terminal, and browser, with a Manager Surface and reviewable Artifacts such as plans, screenshots, walkthroughs, and recordings. The product demo should visibly connect CityCommand AI decisions to Antigravity-style traces and artifacts.

## Safe design assumption

Because public sources do not confirm Antigravity as a production emergency-response runtime API, the recommended implementation is: use Antigravity for coding, planning, verification, artifact generation, and demo trace proof; use Google ADK or a custom FastAPI orchestrator for the actual backend agent workflow.

## Agent workflow

Signal Intake Agent

-\> Signal Cleaning Agent

-\> Geolocation Agent

-\> Credibility Scoring Agent

-\> Crisis Classification Agent

-\> Severity Prediction Agent

-\> Resource Allocation Agent

-\> Simulation Agent

-\> Stakeholder Notification Agent

-\> Human Review Gate

-\> Mock Execution

-\> False Alarm Recovery Agent

-\> Command Center Briefing Agent

## Agent catalog

| **Agent**                      | **Purpose**                                    | **Input**                                         | **Output**                                           | **Tools/APIs**                           | **Failure behavior**                                          |
|--------------------------------|------------------------------------------------|---------------------------------------------------|------------------------------------------------------|------------------------------------------|---------------------------------------------------------------|
| Signal Intake Agent            | Collect raw signals from forms and mock APIs.  | Raw social/weather/traffic/field/call data.       | Structured signal list.                              | Mock APIs, forms, seed JSON.             | If source fails, mark API degraded and continue.              |
| Signal Cleaning Agent          | Normalize noisy text and remove spam.          | Raw signals.                                      | Cleaned signals with language/time/source metadata.  | Text rules, optional LLM.                | Keep uncertain text with low confidence rather than deleting. |
| Geolocation Agent              | Extract and validate area/location.            | Clean text and metadata.                          | lat/lng, area, radius, geo confidence.               | Gazetteer, Maps mock, geocoder later.    | Ask for manual location or field verification.                |
| Credibility Scoring Agent      | Score reliability and misinformation risk.     | Signals and source metadata.                      | Credibility factors and final confidence.            | Scoring service, velocity model.         | No public alert if confidence is low.                         |
| Crisis Classification Agent    | Classify crisis type and alternate hypotheses. | Signal cluster and scores.                        | Primary class, confidence, alternates.               | Rules + Gemini/LLM optional.             | Fallback to rule-based classifier.                            |
| Severity Prediction Agent      | Estimate impact and evolution.                 | Classification, location, vulnerability, traffic. | Severity, radius, population, duration, spread risk. | Mock vulnerability layer, formulas.      | Use conservative ranges if data missing.                      |
| Resource Allocation Agent      | Assign limited resources across incidents.     | Incidents and resource inventory.                 | Assignments with ETA and trade-offs.                 | Route matrix mock, optimization formula. | Suggest reserves or alternatives if unavailable.              |
| Simulation Agent               | Estimate response impact.                      | Action plan and before state.                     | After state, deltas, side effects.                   | Mock traffic/dispatch model.             | Show qualitative simulation if numerical model fails.         |
| Stakeholder Notification Agent | Draft tailored messages.                       | Incident and action plan.                         | Message drafts by audience.                          | Templates + LLM optional.                | Public drafts disabled if low confidence.                     |
| False Alarm Recovery Agent     | Correct and retract wrong alerts.              | Verification evidence.                            | Reclassification, correction, audit log.             | Recovery service, notification mock.     | Escalate to human if correction is high impact.               |
| Command Center Briefing Agent  | Summarize current situation.                   | Full incident state.                              | Executive briefing.                                  | LLM or template.                         | Use deterministic template if LLM unavailable.                |

## Example Antigravity-style trace

{

"trace_id": "trace_0007",

"workflow_id": "wf_demo_g10_heat_001",

"agent_name": "Crisis Classification Agent",

"step": "classify_cluster",

"input_summary": "8 reports, heavy rainfall alert, congestion spike, one conflicting field report",

"decision": {

"primary_type": "urban_flooding",

"confidence": 0.78,

"alternate_hypothesis": "broken_water_main",

"alternate_confidence": 0.41

},

"reasoning_summary": "Social velocity, rainfall, and traffic blockage support flooding; field report introduces water-main uncertainty.",

"tool_calls": \["mock_weather_api", "mock_traffic_api", "gazetteer_lookup"\],

"fallback_used": false,

"human_review_required": true

}

## What judges should see

- Antigravity Manager Surface screenshot with multiple build agents/tasks.

- Antigravity Artifacts folder: task plan, implementation plan, screenshots, test logs, browser recordings.

- In-app Agent Trace screen showing CityCommand pipeline decisions.

- README section explaining where Antigravity was used and what artifacts prove it.

- Demo narration that explicitly says Antigravity is central to agent planning, coding, verification, and trace proof.

# 6. UI/UX Design Specification

## Design principles

- Mobile-first command clarity: show incident, severity, confidence, priority, next action, and human approval status first.

- Explainable AI: every classification and score must have evidence, not only a percentage.

- Safe interaction: public messages and resource dispatch remain draft/approval actions in demo.

- Fast scanning: color + text labels, short cards, prominent status chips.

- Traceable decisions: every screen should link to trace logs or evidence.

- Stress-test ready: demo toggles should let judges see API failure, duplicate reports, false alarm, and conflict handling.

## Visual system

| **Design token** | **Recommendation**                                           |
|------------------|--------------------------------------------------------------|
| Theme            | Dark command-center UI with high contrast cards.             |
| Primary color    | Deep navy / \#0F172A.                                        |
| Accent color     | Cyan / \#06B6D4 for AI and traces.                           |
| Critical         | Red / \#EF4444 with label CRITICAL.                          |
| High warning     | Amber / \#F59E0B with label HIGH.                            |
| Confirmed/safe   | Green / \#22C55E with label CONFIRMED or SENT.               |
| Typography       | Inter or Roboto; 18-24px headings, 14-16px body, bold chips. |
| Cards            | Rounded 16px, subtle border, compact evidence rows.          |
| Maps             | Dark map placeholder with incident rings and route overlays. |

## Mobile screen specification

| **Screen**                | **Purpose**                | **Main components**                                                  | **User actions**                  | **Empty/error state**              | **AI coder notes**                        |
|---------------------------|----------------------------|----------------------------------------------------------------------|-----------------------------------|------------------------------------|-------------------------------------------|
| Splash                    | Brand entry                | Logo, product name, tagline, animated map pulse.                     | Auto navigate.                    | No state.                          | Keep clean and premium.                   |
| Mock login                | Role selection             | Operator, Dispatcher, Field Team, Public Info, Admin.                | Choose role.                      | No role selected.                  | Use local state; no real auth required.   |
| Home dashboard            | Command overview           | Risk score, active incidents, resources, API health, trace status.   | Run demo, open incident.          | No incidents.                      | Big CTA: Run CIRO Demo Scenario.          |
| Live incidents            | Map/list view              | Map markers, priority cards, filters.                                | Tap marker/card.                  | Map unavailable.                   | Fallback to list-only mode.               |
| Signal intake             | Add or trigger signals     | Text input, source type, location, demo signal loader.               | Submit signal.                    | Missing location warning.          | Include Roman Urdu sample.                |
| Incident detail           | Full incident context      | Type, severity, confidence, population, duration, evidence, actions. | Run analysis, allocate, simulate. | Insufficient evidence.             | Tabs: Overview, Evidence, Actions, Trace. |
| AI analysis               | Explain classification     | Confidence meter, score breakdown, contradiction panel.              | Accept/request verification.      | Low confidence.                    | Show alternate hypothesis clearly.        |
| Resource allocation       | Show constrained decisions | Available resources, assignments, ETA, trade-off cards.              | Approve/modify.                   | Resource shortage.                 | Explain why each resource goes where.     |
| Action simulation         | Before/after impact        | Congestion, ETA, side effects, cost, risk.                           | Run simulation.                   | Simulation unavailable.            | Use animated bars.                        |
| Stakeholder notifications | Draft messages             | Audience tabs, messages, approve/send mock.                          | Approve, edit, send.              | Public disabled if low confidence. | Use CAP-like fields.                      |
| Recovery                  | Correct false alarm        | Old vs new classification, field evidence, correction message.       | Retract/reclassify.               | No prior alert.                    | Critical judge screen.                    |
| Agent trace               | Prove agentic workflow     | Timeline, agent, step, input/output, tools, fallback.                | Filter/open details.              | No trace yet.                      | Show 10+ entries.                         |
| Settings/demo             | Control scenarios          | API failure, duplicate, conflict, false alarm toggles.               | Reset/run.                        | None.                              | Use for judge stress tests.               |

## Optional web dashboard

If time remains, build a simple web admin dashboard after mobile completion. The web version should reuse backend APIs and show a large map, incident table, resources board, simulation lab, agent trace timeline, and audit log. Do not prioritize web over mobile because the challenge explicitly makes the mobile app mandatory.

# 7. App Flow, User Flow, and System Flow

## Citizen/city signal flow

User submits report or mock source sends signal

-\> Signal Intake Agent stores raw signal

-\> Signal Cleaning Agent normalizes language/time/source

-\> Geolocation Agent extracts area and confidence

-\> Credibility Agent scores urgency/source/staleness

-\> Cluster engine checks duplicates

-\> Incident candidate is created or updated

-\> Dashboard shows new/updated incident

## Command center operator flow

Open app -\> select Operator role -\> run demo scenario

-\> View dashboard -\> open highest-priority incident

-\> Review AI analysis and evidence

-\> Accept classification or request field verification

-\> Run allocation -\> run simulation -\> review messages

-\> Approve mock response -\> monitor traces and recovery updates

## Multi-signal detection flow for G-10

Social posts: "G-10 mein pani bhar gaya hai, gaariyan phans gayi hain"

Weather: heavy rainfall alert

Traffic: congestion spike

Field report: possible water-main burst

-\> Cluster: G-10/George Town within 30 min window

-\> Classification: primary urban flooding, alternate water-main burst

-\> Confidence: flood 78%, water-main 41%

-\> Human review required because conflicting field report exists

## Multi-crisis allocation flow

Incident A: G-10 probable flooding, high traffic impact

Incident B: Heat emergency, high vulnerable-population risk

Resources: limited rescue teams, police, medical outreach, water tanker, utility team

-\> Priority calculation

-\> G-10 receives rescue teams + traffic police + utility verification

-\> Heat zone receives medical outreach + water tanker

-\> Ambulance remains in reserve because injury reports are low confidence

## False alarm recovery flow

Field verification confirms water-main burst only

-\> Recovery Agent compares field evidence with original classification

-\> Incident reclassified: urban_flooding -\> infrastructure_failure/water_main_burst

-\> Severity downgraded

-\> Public flood alert corrected/retracted

-\> Utility provider ticket escalated

-\> Trace and audit logs updated

## API failure fallback flow

Traffic API fails mid-response

-\> API Health Agent marks traffic source degraded

-\> System uses cached/mock congestion baseline

-\> Confidence reduced and fallback noted

-\> Simulation labeled estimated

-\> Operator sees degraded-mode banner

# 8. Backend Schema, Database, and Data Contracts

## Database approach

Use SQLite or in-memory JSON for a fast hackathon demo. Design the schema as if it can migrate to PostgreSQL + PostGIS. PostGIS is recommended for production because it extends PostgreSQL with spatial storage, indexing, and querying support, which is essential for incident radius, affected-zone, route, and vulnerability-layer queries.

### users

| **Field**  | **Type**  | **Description**         | **Example**          |
|------------|-----------|-------------------------|----------------------|
| id         | UUID      | Unique user id.         | usr_001              |
| name       | TEXT      | Display name.           | Command Operator     |
| email      | TEXT      | User email.             | operator@demo.city   |
| role_id    | UUID      | References roles table. | role_operator        |
| created_at | TIMESTAMP | Creation time.          | 2026-05-16T18:00:00Z |

### roles

| **Field**   | **Type** | **Description**  | **Example**                           |
|-------------|----------|------------------|---------------------------------------|
| id          | UUID     | Role id.         | role_operator                         |
| name        | TEXT     | Role name.       | operator                              |
| permissions | JSONB    | Allowed actions. | \["approve_alert", "run_simulation"\] |

### signal_sources

| **Field**        | **Type** | **Description**                            | **Example**      |
|------------------|----------|--------------------------------------------|------------------|
| id               | UUID     | Source id.                                 | src_weather      |
| name             | TEXT     | Source name.                               | Mock Weather API |
| source_type      | TEXT     | social/weather/traffic/field/sensor/calls. | weather          |
| base_credibility | FLOAT    | Starting reliability weight.               | 0.88             |
| is_mock          | BOOLEAN  | Whether source is simulated.               | true             |

### incoming_signals

| **Field**       | **Type**  | **Description**           | **Example**                  |
|-----------------|-----------|---------------------------|------------------------------|
| id              | UUID      | Signal id.                | sig_001                      |
| source_id       | UUID      | References signal source. | src_social                   |
| raw_text        | TEXT      | Original text.            | G-10 mein pani bhar gaya hai |
| normalized_text | TEXT      | Cleaned text.             | Water accumulation in G-10   |
| language        | TEXT      | Detected language.        | roman_urdu                   |
| lat/lng         | FLOAT     | Coordinates if known.     | 33.6844, 73.0479             |
| location_text   | TEXT      | Human-readable place.     | G-10 Islamabad               |
| timestamp       | TIMESTAMP | Signal time.              | 2026-05-16T18:05:00Z         |
| metadata        | JSONB     | Source-specific metadata. | {"media_attached": false}    |

### incidents

| **Field**           | **Type** | **Description**                                  | **Example**                     |
|---------------------|----------|--------------------------------------------------|---------------------------------|
| id                  | UUID     | Incident id.                                     | inc_g10_001                     |
| title               | TEXT     | Human-readable title.                            | Probable urban flooding in G-10 |
| status              | TEXT     | candidate/active/verified/reclassified/resolved. | active                          |
| primary_type        | TEXT     | Crisis type.                                     | urban_flooding                  |
| severity            | TEXT     | LOW/MEDIUM/HIGH/CRITICAL.                        | HIGH                            |
| priority_score      | FLOAT    | Rank ordering score.                             | 86                              |
| confidence          | FLOAT    | Final confidence.                                | 0.78                            |
| lat/lng             | FLOAT    | Incident centroid.                               | 33.6844, 73.0479                |
| radius_m            | INT      | Affected radius.                                 | 1200                            |
| affected_population | INT      | Population estimate.                             | 18500                           |

### crisis_classifications

| **Field**        | **Type** | **Description**            | **Example**                              |
|------------------|----------|----------------------------|------------------------------------------|
| id               | UUID     | Classification id.         | cls_001                                  |
| incident_id      | UUID     | Incident reference.        | inc_g10_001                              |
| class_type       | TEXT     | Crisis type.               | urban_flooding                           |
| confidence       | FLOAT    | Classification confidence. | 0.78                                     |
| is_primary       | BOOLEAN  | Primary or alternate.      | true                                     |
| evidence         | JSONB    | Evidence list.             | \["rain", "traffic", "social velocity"\] |
| created_by_agent | TEXT     | Agent name.                | Crisis Classification Agent              |

### severity_predictions

| **Field**             | **Type**  | **Description**      | **Example**                             |
|-----------------------|-----------|----------------------|-----------------------------------------|
| id                    | UUID      | Prediction id.       | sev_001                                 |
| incident_id           | UUID      | Incident reference.  | inc_g10_001                             |
| severity_level        | TEXT      | Severity label.      | HIGH                                    |
| affected_radius_m     | INT       | Radius.              | 1200                                    |
| population_estimate   | INT       | Affected population. | 18500                                   |
| expected_duration_min | INT       | Duration.            | 180                                     |
| peak_impact_time      | TIMESTAMP | Predicted peak.      | 2026-05-16T19:00:00Z                    |
| spread_risk           | FLOAT     | Risk of expansion.   | 0.62                                    |
| uncertainty_range     | JSONB     | Min/max range.       | {"duration_min":120,"duration_max":240} |

### resources

| **Field**         | **Type** | **Description**                 | **Example**                   |
|-------------------|----------|---------------------------------|-------------------------------|
| id                | UUID     | Resource id.                    | res_rescue_a                  |
| resource_type     | TEXT     | Resource category.              | rescue_team                   |
| name              | TEXT     | Resource label.                 | Rescue Team A                 |
| status            | TEXT     | available/assigned/unavailable. | available                     |
| home_lat/home_lng | FLOAT    | Base location.                  | 33.6901, 73.0302              |
| capacity          | INT      | Units/capacity.                 | 1                             |
| metadata          | JSONB    | Skills/equipment.               | {"skills":\["water_rescue"\]} |

### resource_assignments

| **Field**       | **Type** | **Description**                        | **Example**                            |
|-----------------|----------|----------------------------------------|----------------------------------------|
| id              | UUID     | Assignment id.                         | asg_001                                |
| incident_id     | UUID     | Incident reference.                    | inc_g10_001                            |
| resource_id     | UUID     | Resource reference.                    | res_rescue_a                           |
| assigned_units  | INT      | Number assigned.                       | 1                                      |
| eta_min         | INT      | Estimated arrival.                     | 13                                     |
| priority_reason | TEXT     | Why assigned.                          | Vehicles stranded and traffic blockage |
| status          | TEXT     | planned/approved/dispatched/completed. | planned                                |

### response_actions

| **Field**         | **Type** | **Description**                         | **Example**                                  |
|-------------------|----------|-----------------------------------------|----------------------------------------------|
| id                | UUID     | Action id.                              | act_001                                      |
| incident_id       | UUID     | Incident reference.                     | inc_g10_001                                  |
| action_type       | TEXT     | reroute/dispatch/alert/ticket/advisory. | traffic_reroute                              |
| description       | TEXT     | Action summary.                         | Redirect traffic away from underpass         |
| status            | TEXT     | draft/approved/simulated/executed.      | draft                                        |
| requires_approval | BOOLEAN  | Human approval needed.                  | true                                         |
| payload           | JSONB    | Action parameters.                      | {"alternate_routes":\["Service Road West"\]} |

### simulations

| **Field**    | **Type** | **Description**            | **Example**                 |
|--------------|----------|----------------------------|-----------------------------|
| id           | UUID     | Simulation id.             | sim_001                     |
| incident_id  | UUID     | Incident reference.        | inc_g10_001                 |
| before_state | JSONB    | Pre-action metrics.        | {"congestion":88}           |
| action_plan  | JSONB    | Actions simulated.         | \["reroute","dispatch"\]    |
| after_state  | JSONB    | Post-action metrics.       | {"congestion":64}           |
| side_effects | JSONB    | Possible negative effects. | \["side-route congestion"\] |

### stakeholder_notifications

| **Field**         | **Type** | **Description**                | **Example**                      |
|-------------------|----------|--------------------------------|----------------------------------|
| id                | UUID     | Message id.                    | msg_001                          |
| incident_id       | UUID     | Incident reference.            | inc_g10_001                      |
| audience          | TEXT     | Target audience.               | public                           |
| channel           | TEXT     | mock_push/sms/email/dashboard. | mock_push                        |
| message           | TEXT     | Draft message.                 | Avoid low-lying roads near G-10. |
| status            | TEXT     | draft/approved/sent/retracted. | draft                            |
| requires_approval | BOOLEAN  | Approval flag.                 | true                             |

### agent_traces

| **Field**      | **Type** | **Description**     | **Example**                 |
|----------------|----------|---------------------|-----------------------------|
| id             | UUID     | Trace id.           | trace_001                   |
| workflow_id    | TEXT     | Workflow id.        | wf_demo_001                 |
| incident_id    | UUID     | Incident reference. | inc_g10_001                 |
| agent_name     | TEXT     | Agent name.         | Credibility Scoring Agent   |
| step           | TEXT     | Agent step.         | score_cluster               |
| input_summary  | TEXT     | Inputs summarized.  | 6 posts + weather + traffic |
| output_summary | TEXT     | Output summarized.  | confidence 0.78             |
| tool_calls     | JSONB    | Tools/APIs used.    | \["mock_weather_api"\]      |
| fallback_used  | BOOLEAN  | Fallback flag.      | false                       |

### audit_logs

| **Field**   | **Type** | **Description**     | **Example**                 |
|-------------|----------|---------------------|-----------------------------|
| id          | UUID     | Log id.             | audit_001                   |
| actor_type  | TEXT     | human/agent/system. | agent                       |
| actor_id    | TEXT     | Actor name/id.      | Recovery Agent              |
| action      | TEXT     | Action performed.   | incident_reclassified       |
| entity_type | TEXT     | Entity changed.     | incident                    |
| entity_id   | UUID     | Entity id.          | inc_g10_001                 |
| before      | JSONB    | Previous state.     | {"type":"urban_flooding"}   |
| after       | JSONB    | New state.          | {"type":"water_main_burst"} |

### api_health_logs

| **Field**     | **Type** | **Description**        | **Example** |
|---------------|----------|------------------------|-------------|
| id            | UUID     | Health log id.         | api_001     |
| api_name      | TEXT     | API checked.           | traffic_api |
| status        | TEXT     | healthy/degraded/down. | down        |
| latency_ms    | INT      | Latency.               | 0           |
| fallback_used | BOOLEAN  | Fallback flag.         | true        |
| error_message | TEXT     | Error reason.          | timeout     |

### false_alarm_records

| **Field**                | **Type** | **Description**     | **Example**                          |
|--------------------------|----------|---------------------|--------------------------------------|
| id                       | UUID     | Record id.          | fa_001                               |
| incident_id              | UUID     | Incident reference. | inc_g10_001                          |
| original_classification  | TEXT     | Old class.          | urban_flooding                       |
| corrected_classification | TEXT     | New class.          | water_main_burst                     |
| reason                   | TEXT     | Why corrected.      | Field team confirmed pipe burst only |
| retraction_sent          | BOOLEAN  | Retraction status.  | true                                 |

## Sample JSON contracts

### Signal input

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

### Incident object

{

"id": "inc_g10_001",

"title": "Probable urban flooding in G-10",

"primary_type": "urban_flooding",

"alternate_hypotheses": \[{"type":"water_main_burst","confidence":0.41}\],

"severity": "HIGH",

"confidence": 0.78,

"priority_score": 86,

"location": {"area":"G-10 Islamabad","lat":33.6844,"lng":73.0479,"radius_m":1200},

"affected_population_estimate": 18500,

"expected_duration_min": 180,

"status": "needs_human_review"

}

# 9. API Design

| **Method** | **URL**                          | **Purpose**                           | **Request**                | **Response**           | **Errors**                 | **Auth**            |
|------------|----------------------------------|---------------------------------------|----------------------------|------------------------|----------------------------|---------------------|
| POST       | /signals                         | Submit a citizen/social/field signal. | Signal JSON.               | Created signal.        | 400 missing text/location. | citizen/operator    |
| GET        | /signals                         | List recent signals.                  | filters.                   | Signal list.           | None.                      | operator            |
| POST       | /demo/run-scenario               | Load main demo data.                  | scenario_id.               | Incidents + traces.    | 404 scenario missing.      | operator            |
| GET        | /incidents                       | Get incidents.                        | filters.                   | Incident summaries.    | None.                      | operator            |
| GET        | /incidents/{id}                  | Get incident detail.                  | none.                      | Full incident.         | 404 not found.             | operator            |
| POST       | /incidents/{id}/classify         | Run classification.                   | config.                    | Classification result. | 422 insufficient signals.  | operator            |
| POST       | /incidents/{id}/predict-severity | Run severity prediction.              | config.                    | Prediction result.     | 422 missing location.      | operator            |
| POST       | /incidents/allocate-resources    | Allocate across multiple incidents.   | incident_ids.              | Assignment plan.       | 409 no resources.          | dispatcher/operator |
| POST       | /incidents/{id}/simulate         | Simulate response actions.            | action list.               | Simulation result.     | 400 invalid action.        | operator            |
| POST       | /notifications/draft             | Generate stakeholder messages.        | incident_id + audiences.   | Drafts.                | 409 low confidence.        | operator            |
| POST       | /notifications/send-mock         | Mock send approved message.           | notification_id.           | Send status.           | 403 approval missing.      | operator/admin      |
| POST       | /alerts/{id}/retract             | Retract/correct alert.                | reason.                    | Recovery record.       | 404 alert not found.       | operator/admin      |
| GET        | /traces                          | Get agent traces.                     | incident/workflow filters. | Trace list.            | None.                      | operator            |
| GET        | /health/apis                     | Check API health.                     | none.                      | Health list.           | None.                      | operator            |
| POST       | /field-reports                   | Submit field verification.            | incident + finding.        | Updated incident.      | 404 incident missing.      | field_team          |
| POST       | /recovery/false-alarm            | Run recovery flow.                    | incident + correction.     | Reclassified incident. | 422 no evidence.           | operator            |

## Example classify endpoint

### Request

POST /incidents/inc_g10_001/classify

{

"use_llm": true,

"include_alternate_hypotheses": true,

"human_review_required_if_conflict": true

}

### Response

{

"incident_id": "inc_g10_001",

"primary_classification": {"type":"urban_flooding","confidence":0.78},

"alternate_hypotheses": \[

{"type":"water_main_burst","confidence":0.41,"reason":"Field report indicates localized pipe burst."}

\],

"evidence": \["6 social reports within 12 minutes", "Heavy rainfall alert", "Traffic congestion spike", "Field report conflict"\],

"human_review_required": true

}

# 10. Implementation Plan for MVP and Hackathon Demo

## Build strategy

Do not start with complex AI. Start with a beautiful demo loop and deterministic backend. Then add optional LLM summarization. The winning hackathon prototype must be reliable, explainable, and easy to demonstrate. Mock APIs are acceptable and recommended by the challenge guidelines when real data is hard or sensitive.

## MVP build order

11. Create monorepo, mobile app, backend app, shared TypeScript/Pydantic types, and seed scenario JSON.

12. Build dashboard, incident list, and incident detail with mock data.

13. Add backend endpoints for demo scenario, incidents, signals, and traces.

14. Implement deterministic agent pipeline with trace creation.

15. Implement confidence scoring and classification with alternate hypothesis.

16. Implement severity prediction and priority scoring.

17. Implement resource allocation across two incidents.

18. Implement simulation output and stakeholder message drafts.

19. Implement false alarm recovery and retraction flow.

20. Polish mobile UI, demo toggles, README, and demo video.

## What to mock vs what to integrate

| **System piece** | **MVP decision**                                   | **Future/live version**                                   |
|------------------|----------------------------------------------------|-----------------------------------------------------------|
| Weather          | Mock heavy rainfall and heat index JSON.           | Weather API or official meteorological alert feed.        |
| Traffic/maps     | Mock congestion index and route ETA.               | Google Routes API Compute Routes/Route Matrix.            |
| Social posts     | Synthetic posts in English/Roman Urdu.             | Public complaint channels or approved public social APIs. |
| Emergency calls  | Mock frequency counts only.                        | Aggregated dispatch counts, no call audio.                |
| Vulnerability    | Seeded low-income/elderly/hospital/drainage layer. | GIS/census/health/shelter datasets.                       |
| Notifications    | Mock send and status update.                       | Firebase Cloud Messaging or SMS gateway with governance.  |
| Agent runtime    | Custom deterministic orchestrator.                 | Google ADK multi-agent runtime plus tools.                |
| Database         | SQLite/in-memory JSON.                             | PostgreSQL + PostGIS.                                     |

## Day-by-day build plan

| **Day** | **Target**              | **Deliverable**                                                              |
|---------|-------------------------|------------------------------------------------------------------------------|
| Day 1   | Foundation              | Repo, backend shell, Expo app, core types, seed scenario.                    |
| Day 2   | Mobile shell            | Dashboard, incident list/detail, navigation, dark UI.                        |
| Day 3   | Agent pipeline          | Signal intake, cleaning, geolocation, credibility, classification, traces.   |
| Day 4   | Crisis intelligence     | Severity, priority, multi-crisis allocation, trade-off explanations.         |
| Day 5   | Simulation and messages | Before/after simulation, notifications, mock send, API failure fallback.     |
| Day 6   | Recovery and polish     | False alarm flow, audit logs, demo settings, UI improvements.                |
| Day 7   | Demo readiness          | README, screenshots, Antigravity artifacts, 3-5 minute video, judge answers. |

## Testing plan

| **Test category** | **Tests**                                                                                                      |
|-------------------|----------------------------------------------------------------------------------------------------------------|
| Unit tests        | Confidence scoring, priority scoring, duplicate merge, classification fallback, resource allocation.           |
| API tests         | Submit signal, run scenario, get incidents, classify, allocate, simulate, draft messages, recover.             |
| UI tests          | Dashboard loads, incident detail opens, trace screen displays, recovery flow changes status.                   |
| Demo tests        | Complete entire story in 3-5 minutes without manual data editing.                                              |
| Stress tests      | API failure, duplicate reports, conflicting field report, low-confidence disease cluster, reroute side effect. |

# 11. Vibe Coder / AI Coder Build Requirements

## Exact modules to generate

| **Area**      | **Files/components**                                                                        |
|---------------|---------------------------------------------------------------------------------------------|
| Dashboard     | HomeDashboardScreen.tsx, RiskSummaryCard.tsx, ApiHealthBanner.tsx                           |
| Incidents     | IncidentsScreen.tsx, IncidentCard.tsx, IncidentDetailScreen.tsx, EvidenceList.tsx           |
| Signals       | SignalIntakeScreen.tsx, SignalList.tsx, DemoSignalLoader.tsx                                |
| AI analysis   | AIAnalysisScreen.tsx, ConfidenceMeter.tsx, ScoreBreakdown.tsx, AlternateHypothesisPanel.tsx |
| Resources     | ResourceAllocationScreen.tsx, ResourceCard.tsx, AssignmentExplanation.tsx                   |
| Simulation    | SimulationScreen.tsx, BeforeAfterPanel.tsx, CongestionDelta.tsx, SideEffectsCard.tsx        |
| Notifications | NotificationScreen.tsx, MessageDraftCard.tsx, ApprovalBar.tsx                               |
| Recovery      | RecoveryScreen.tsx, CorrectionPanel.tsx, RetractionMessageCard.tsx                          |
| Traces        | AgentTraceScreen.tsx, TraceTimeline.tsx, TraceDetailModal.tsx                               |
| Demo settings | DemoModeScreen.tsx, ScenarioToggle.tsx, ResetDemoButton.tsx                                 |

## Backend services

- SignalService

- IncidentService

- AgentOrchestrator

- CredibilityScoringService

- ClassificationService

- SeverityPredictionService

- ResourceAllocationService

- SimulationService

- NotificationService

- RecoveryService

- TraceService

- ApiHealthService

- AuditService

## Seed/mock data checklist

- 6 social posts for G-10 flood in English/Roman Urdu.

- 1 heavy rainfall weather alert.

- 1 traffic congestion spike near G-10.

- 1 field report indicating possible water-main burst.

- 3 heat emergency reports in nearby vulnerable neighborhood.

- 1 heat index reading and low-income vulnerability layer.

- Resource inventory: rescue teams, police units, ambulance, water tanker, medical outreach, utility team, drone, generator.

- Duplicate reports and stale reports for testing.

- API failure response for traffic API.

- False alarm recovery confirmation.

## Ready-to-copy coding prompts

### Prompt 1: Generate project structure

Create a monorepo named citycommand-ai with two apps: mobile using React Native Expo TypeScript and backend using FastAPI Python. Add folders for screens, components, services, store, types, mock data, backend routes, backend agents, backend services, schemas, seed data, and tests. Create a README with setup instructions. Do not implement business logic yet.

### Prompt 2: Build mobile dashboard

Build the React Native Expo mobile dashboard for CityCommand AI. Use a dark command-center style. Add a HomeDashboardScreen with risk summary, active incidents count, available resources, API health, and a large Run CIRO Demo Scenario button. Add bottom tabs: Dashboard, Incidents, Signals, Resources, Traces.

### Prompt 3: Build incident detail screen

Build IncidentDetailScreen for CityCommand AI. It must show title, crisis type, severity chip, confidence meter, priority score, affected radius, affected population, expected duration, evidence list, alternate hypotheses, and action buttons: Run AI Analysis, Allocate Resources, Simulate Response, Draft Notifications, Recovery Flow.

### Prompt 4: Build backend schema

In the FastAPI backend, define Pydantic models and SQL-ready schema objects for Users, Roles, SignalSources, IncomingSignals, Incidents, CrisisClassifications, SeverityPredictions, ConfidenceScores, Resources, ResourceAssignments, ResponseActions, Simulations, StakeholderNotifications, AgentTraces, AuditLogs, ApiHealthLogs, and FalseAlarmRecords.

### Prompt 5: Build mock signal ingestion API

Create FastAPI routes for POST /signals, GET /signals, POST /demo/run-scenario, and GET /incidents. The demo scenario should load social posts, weather alert, traffic congestion spike, field report conflict, heat emergency signals, resource inventory, vulnerability data, and initial agent trace records.

### Prompt 6: Build agent trace screen

Build AgentTraceScreen in React Native. Show a timeline of agent logs with agent name, step, input summary, output summary, confidence, tool calls, fallback used, and human review required. Add filters by agent name and incident. Use collapsible cards and highlight fallback events.

### Prompt 7: Build resource allocation simulation

Implement backend ResourceAllocationService that accepts multiple incidents and limited resources. Calculate priority score using severity, vulnerability, urgency, travel time, and resource scarcity. Assign resources to G-10 flood and heat emergency. Return trade-off explanations. Build ResourceAllocationScreen to display available resources, assigned resources, ETA, and why each assignment was made.

### Prompt 8: Build stakeholder notification module

Implement NotificationService that generates stakeholder-specific draft messages for public citizens, emergency services, hospitals, utility companies, traffic authority, transport authority, media/command center, and field verification teams. Public messages must require human approval. Build NotificationScreen with audience tabs, draft cards, edit button, approve button, and mock send button.

### Prompt 9: Build false alarm recovery flow

Implement RecoveryService and RecoveryScreen. The flow should accept field verification that G-10 is a water-main burst rather than urban flooding. Reclassify the incident, downgrade severity, create a false_alarm_record, generate a public correction/retraction message, notify the utility provider, and append audit logs and agent traces.

### Prompt 10: Polish UI and prepare demo mode

Polish the CityCommand AI mobile UI for a hackathon demo. Add loading states, empty states, degraded API banners, animated confidence meters, before/after simulation cards, and a demo settings screen with toggles for API failure, duplicate reports, conflicting field report, false alarm recovery, and reset demo. Ensure the complete demo can be completed in 3-5 minutes.

# 12. Demo Video Script

## Target length

3-5 minutes. The demo should be scripted tightly. Do not wander through all screens. Show the end-to-end story and the Antigravity trace proof.

| **Time**  | **Scene**                 | **Narration / action**                                                                                                                                      |
|-----------|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0:00-0:20 | Opening hook              | Cities do not lack signals. They lack coordinated, real-time decisions. Show rapid montage: citizen report, rain alert, traffic spike, field report.        |
| 0:20-0:40 | Product intro             | This is CityCommand AI, an agentic crisis intelligence and response system built for the Google Antigravity Hackathon. Show dashboard.                      |
| 0:40-1:10 | Multi-source input        | Trigger demo scenario: G-10 flooding posts, heavy rainfall, traffic spike, field report conflict, heat emergency.                                           |
| 1:10-1:45 | Agentic detection         | Show agents cleaning, geolocating, scoring credibility, merging duplicates, classifying flood with water-main alternate hypothesis.                         |
| 1:45-2:15 | Multi-crisis coordination | Show second heat emergency and explain competing resource constraints.                                                                                      |
| 2:15-2:50 | Resource allocation       | Rescue and traffic units to G-10; medical outreach and water tanker to heat zone; ambulance held in reserve.                                                |
| 2:50-3:25 | Simulation                | Show reroute and dispatch before/after: congestion improves, ETA improves, side-effect warning appears.                                                     |
| 3:25-3:50 | Notifications             | Show stakeholder messages: public, hospital, traffic, utility, field team. Public alert needs approval.                                                     |
| 3:50-4:30 | Recovery                  | Field verification confirms water-main burst. System reclassifies, retracts flood alert, notifies utility, updates audit log.                               |
| 4:30-5:00 | Closing                   | CityCommand AI is not a dashboard; it is an auditable agentic response orchestrator: detect, classify, prioritize, allocate, simulate, notify, and recover. |

## Required demo proof points

- Mobile app is working.

- At least three signal sources are shown.

- Two simultaneous crises are detected.

- Agent traces are visible.

- Resource trade-offs are explained.

- Simulation changes system state.

- False alarm recovery is demonstrated.

- Antigravity usage is shown through artifacts or screenshots.

# 13. Judging Strategy

## Scoring alignment

| **Criteria**                  | **Weight** | **How CityCommand AI maximizes score**                                                                                      |
|-------------------------------|------------|-----------------------------------------------------------------------------------------------------------------------------|
| Antigravity integration       | 20-25%     | Show Antigravity Manager Surface, Artifacts, traces, task plans, screenshots, browser recordings, and in-app trace mapping. |
| Crisis detection and severity | 20-25%     | Multi-source fusion, confidence scoring, alternate hypotheses, affected population, duration, spread risk.                  |
| Resource optimization         | 20%        | Two incidents compete for limited resources with ETA and trade-off explanation.                                             |
| Simulation and coordination   | 15%        | Before/after impact, stakeholder messages, tickets, reroutes, side effects.                                                 |
| Robustness/scalability/cost   | 10%        | Fallbacks, caching, mock-to-live pathway, cost/latency notes, API health logs.                                              |
| Innovation and UX             | 10%        | Mobile-first command UX, trace transparency, recovery flow, demo toggles.                                                   |

## What to emphasize

- This system transforms signals into decisions, not just markers on a map.

- The agent workflow is modular, traceable, and recoverable.

- The prototype handles conflict, duplicates, and API failure.

- Human review is built into public alerting and high-impact actions.

- The demo is city-realistic: flood + heat + traffic + utility conflict + limited resources.

## Strong judge Q&A

| **Judge question**                 | **Strong answer**                                                                                                                                                                                      |
|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Is this just a dashboard?          | No. The dashboard is the surface. The core is a multi-agent pipeline that ingests, verifies, classifies, prioritizes, allocates, simulates, communicates, and recovers.                                |
| How is Antigravity central?        | We use Antigravity for agentic build orchestration, planning, browser/terminal verification, artifacts, and we mirror the runtime agent decisions in app traces.                                       |
| How do you prevent misinformation? | We score source credibility, geo confidence, mention velocity, duplication, contradiction, staleness, and official corroboration. Low-confidence events trigger field verification, not public alerts. |
| What happens if an API fails?      | The system enters degraded mode, uses cached/mock fallback, lowers confidence, and logs the fallback in the trace.                                                                                     |
| Why not fully automate dispatch?   | Because this is a high-impact public safety context. The system recommends and simulates, but humans approve external actions.                                                                         |
| Why is this feasible?              | The MVP uses mock APIs, deterministic scoring, seed scenarios, and a focused mobile demo while preserving a production path.                                                                           |

# 14. Risks, Limitations, Safety, and Governance

## Risk register

| **Risk**                     | **Impact**                                | **Mitigation**                                                                         |
|------------------------------|-------------------------------------------|----------------------------------------------------------------------------------------|
| False public alert           | Can cause panic, congestion, or distrust. | Human approval, certainty labels, staged messages, retraction flow.                    |
| Misinformation/social rumor  | Wrong classification or wasted resources. | Credibility scoring, duplicate clustering, official corroboration, field verification. |
| False negative/missed event  | Delayed response.                         | Low-confidence monitoring queue and escalation if signal velocity grows.               |
| Biased vulnerability scoring | Could stigmatize communities.             | Use vulnerability only to prioritize support; show explanation; avoid punitive labels. |
| Privacy leakage              | Sensitive citizen/location exposure.      | Synthetic demo data, hashing, area-level public display, minimal storage.              |
| Overreliance on AI           | Operators may accept bad recommendations. | Evidence panels, uncertainty ranges, approval gates, audit trail.                      |
| API outage                   | Reduced situational awareness.            | Cached data, alternate mock source, confidence reduction, degraded banner.             |
| Model hallucination          | Unsafe message or wrong facts.            | Template-bounded generation, deterministic checks, human review.                       |
| Hackathon overbuild          | Incomplete prototype.                     | Build demo loop first; delay real integrations.                                        |

## Safe alerting policy

- Public alert must state the affected area clearly.

- Public alert must avoid unverified casualty claims.

- Public alert must use certainty wording: possible, probable, confirmed.

- Public alert must give simple safe action, such as avoid low-lying roads, use alternate routes, stay hydrated, check on vulnerable neighbors, or follow official instructions.

- Public alert must not create unnecessary evacuation pressure unless confirmed by authority.

- Public alert must be reversible through correction/retraction workflow.

- Public alert must require human approval.

## MVP limitations

- Synthetic data only.

- No certified emergency dispatch integration.

- No real public alert channel.

- Severity predictions are heuristic.

- Traffic and route impacts are simulated.

- Field verification is mocked.

- No formal validation with emergency-management professionals yet.

# 15. Final Recommended MVP

## Exact version to build

**Build CityCommand AI as a polished mobile-first demo with a FastAPI backend, mock APIs, deterministic multi-agent orchestration, visible agent traces, and a complete two-crisis scenario. This version is realistic, judge-friendly, feasible in limited time, and directly aligned with the challenge scoring criteria.**

## Must-have features

- Mobile app with role-based demo login.

- Dashboard with active incidents, resource status, and API health.

- Signal intake and demo scenario trigger.

- G-10 probable urban flooding incident with water-main conflict.

- Nearby heat emergency incident with vulnerability context.

- Confidence and severity breakdown.

- Multi-crisis resource allocation with trade-offs.

- Action simulation with before/after outcomes.

- Stakeholder notification drafts and approval controls.

- False alarm recovery and retraction/correction.

- Agent trace screen.

- README and demo video.

## Features to delay

- Full web dashboard.

- Real social media ingestion.

- Real public alerting.

- Complex machine learning training.

- Production-grade RBAC.

- Real emergency-call integration.

- Advanced GIS maps and polygon editing.

- Disease cluster analytics beyond low-confidence verification demo.

## Most impressive judge moments

21. Press Run CIRO Demo and show multiple sources entering the system.

22. Open Agent Trace and show each agent decision.

23. Show urban flood classification with water-main alternate hypothesis.

24. Show heat emergency competing for resources.

25. Show resource allocation with a clear why-this-resource explanation.

26. Run simulation and show before/after metrics.

27. Approve public message draft safely.

28. Trigger field verification and show false alarm recovery.

## Final recommendation

Do not try to build everything real. Build one excellent end-to-end story. The winning version is not the one with the most live APIs; it is the one that proves agentic crisis reasoning, coordination, simulation, safety, and recovery in a way judges can understand in five minutes.

# Appendix A. Scoring Models and Decision Logic

## Confidence scoring formula

final_confidence =

0.20 \* source_credibility

\+ 0.16 \* geolocation_confidence

\+ 0.14 \* urgency_language

\+ 0.14 \* mention_velocity

\+ 0.16 \* official_corroboration

\+ 0.08 \* duplicate_consistency

\+ 0.06 \* media_or_sensor_support

\- 0.10 \* contradiction_level

\- 0.06 \* staleness_penalty

Use this as an explainable heuristic. In the UI, do not show only final confidence. Show the factors so judges understand how the system reasoned.

## Priority scoring formula

priority_score = normalize(

0.28 \* severity_score

\+ 0.22 \* vulnerable_population_score

\+ 0.18 \* urgency_score

\+ 0.12 \* spread_risk

\+ 0.10 \* infrastructure_criticality

\+ 0.10 \* response_time_sensitivity

)

resource_assignment_score = priority_score / (travel_time_minutes + scarcity_penalty)

## Severity levels

| **Level** | **Example meaning**                                                              | **Default action**                                        |
|-----------|----------------------------------------------------------------------------------|-----------------------------------------------------------|
| LOW       | Low confidence or minor localized issue.                                         | Monitor; no public alert.                                 |
| MEDIUM    | Localized impact with moderate corroboration.                                    | Notify field team; prepare resources.                     |
| HIGH      | Clear multi-source impact or vulnerable population risk.                         | Allocate resources, simulate action, draft alerts.        |
| CRITICAL  | Confirmed life-safety threat, severe infrastructure disruption, or rapid spread. | Immediate human escalation and multi-agency coordination. |

# Appendix B. Mock Dataset and Demo Scenario Pack

## Main demo signals

| **Signal** | **Source**     | **Content**                                                 | **Expected use**                       |
|------------|----------------|-------------------------------------------------------------|----------------------------------------|
| S1         | Social         | G-10 mein pani bhar gaya hai, gaariyan phans gayi hain.     | Flood evidence, urgency, location.     |
| S2         | Social         | Flash flood near George Town underpass, traffic stuck.      | Flood evidence, alias matching.        |
| S3         | Weather        | Heavy rainfall alert: 38 mm in last hour.                   | Official corroboration.                |
| S4         | Traffic        | Congestion index 88 near G-10, average speed down 62%.      | Traffic impact.                        |
| S5         | Field report   | Water appears from broken main near service lane.           | Alternate hypothesis.                  |
| S6         | Citizen/health | Elderly residents fainting due to heat in low-income block. | Heat emergency evidence.               |
| S7         | Weather/heat   | Heat index 43 C, humidity high.                             | Heat severity.                         |
| S8         | Vulnerability  | High elderly density, low tree cover, limited water access. | Heat priority and resource allocation. |

## Resource inventory

| **Resource**          | **Quantity** | **Availability** | **Best use**                     |
|-----------------------|--------------|------------------|----------------------------------|
| Rescue teams          | 2            | Available        | G-10 vehicle/water rescue.       |
| Police traffic units  | 2            | Available        | Road closure and rerouting.      |
| Ambulance             | 1            | Reserve          | Use if injury signal confirmed.  |
| Medical outreach team | 1            | Available        | Heat emergency.                  |
| Water tanker          | 1            | Available        | Heat emergency support.          |
| Utility repair team   | 1            | Available        | Water-main verification/repair.  |
| Drone                 | 1            | Available        | Area scan if needed.             |
| Generator             | 1            | Available        | Power outage or shelter support. |

# Appendix C. Stress Tests and QA Plan

| **Stress test**                                                  | **Expected behavior**                                               |
|------------------------------------------------------------------|---------------------------------------------------------------------|
| Two crises within 30 minutes compete for resources.              | Priority ranking and allocation trade-off explanation.              |
| Social media indicates flooding but official sensor unavailable. | Confidence remains moderate; field verification requested.          |
| Traffic API fails mid-response.                                  | Fallback to cached congestion baseline; confidence reduced.         |
| Public alert causes evacuation congestion risk.                  | Simulation flags side effect; recommends staged alerting.           |
| False alarm confirmed.                                           | Reclassification, correction message, utility ticket, audit update. |
| Duplicate reports from multiple users.                           | Cluster and merge; preserve count and evidence.                     |
| Low-confidence disease cluster signal.                           | No public alert; health verification task generated.                |
| Rerouting increases congestion near hospital.                    | Simulation flags hospital access risk and suggests alternate route. |

# Appendix D. README Template

\# CityCommand AI

\## Overview

CityCommand AI is a mobile-first agentic crisis intelligence and response orchestrator.

\## Architecture

Mobile App -\> FastAPI Backend -\> Agent Orchestrator -\> Mock APIs -\> Trace/Audit Store

\## Antigravity Usage

\- Manager Surface used to coordinate build agents.

\- Artifacts include task plan, implementation plan, screenshots, browser recordings, and test logs.

\- In-app Agent Trace screen mirrors the multi-agent workflow.

\## Setup

1. cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload

2. cd mobile && npm install && npx expo start

\## Demo Scenario

Run the G-10 flood + heat emergency scenario from the dashboard.

\## Assumptions

Mock data only. No real emergency dispatch or public alerts.

\## Privacy and Safety

Synthetic data, human approval for public alerts, correction/retraction workflow.

\## Limitations

Heuristic scoring, simulated APIs, no production GIS validation.

# Appendix E. Glossary

| **Term**             | **Meaning**                                                                                                               |
|----------------------|---------------------------------------------------------------------------------------------------------------------------|
| Agentic system       | A system where specialized AI/software agents plan, process, decide, and execute tasks through a workflow.                |
| Antigravity Artifact | A reviewable output such as plan, screenshot, walkthrough, or recording produced during agentic development/verification. |
| Confidence score     | Estimated reliability of the classification based on source, location, corroboration, contradiction, and staleness.       |
| Priority score       | Ranking score that determines which incident receives constrained resources first.                                        |
| CAP                  | Common Alerting Protocol: standard format for all-hazard public warnings.                                                 |
| NIMS                 | National Incident Management System: framework for multi-agency emergency coordination.                                   |
| Degraded mode        | System state when a source/API fails and fallback data is used.                                                           |
| False positive       | System detects a crisis that is later corrected or downgraded.                                                            |
| False negative       | System initially misses a crisis or underestimates it.                                                                    |

# Appendix F. Research Sources and References

The following sources should be cited in the README and presentation. Use them to justify platform choices, safety logic, alerting format, traffic coordination, heat response, flood response, and AI governance.

Google Developers Blog. (2025, November 20). Build with Google Antigravity, our new agentic development platform. https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/

Google Antigravity. (2025, November 18). Introducing Google Antigravity. https://antigravity.google/blog/introducing-google-antigravity

Google Codelabs. (n.d.). Getting Started with Google Antigravity. https://codelabs.developers.google.com/getting-started-google-antigravity

Google Cloud. (2025, July 2). Build multi-agentic systems using Google ADK. https://cloud.google.com/blog/products/ai-machine-learning/build-multi-agentic-systems-using-google-adk

Agent Development Kit. (n.d.). ADK documentation. https://adk.dev/

Google Cloud. (n.d.). Quickstart: Build and deploy an AI agent to Cloud Run using ADK. https://docs.cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-adk-service

Firebase. (n.d.). Firebase Cloud Messaging documentation. https://firebase.google.com/docs/cloud-messaging

Firebase. (n.d.). Message types and payload limits. https://firebase.google.com/docs/cloud-messaging/customize-messages/set-message-type

Google Maps Platform. (n.d.). Routes API documentation. https://developers.google.com/maps/documentation/routes

Google Maps Platform. (n.d.). Routes API traffic-aware routing. https://developers.google.com/maps/documentation/routes/config_trade_offs

FEMA. (2025). National Incident Management System. https://www.fema.gov/emergency-managers/nims

FEMA. (2025). National Response Framework. https://www.fema.gov/emergency-managers/national-preparedness/frameworks/response

OASIS Open. (2010). Common Alerting Protocol v1.2. https://www.oasis-open.org/standard/cap/

NIST. (2023). Artificial Intelligence Risk Management Framework. https://www.nist.gov/itl/ai-risk-management-framework

NIST. (2024). Generative AI Profile for the AI Risk Management Framework. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

FHWA. (2025). Traffic Incident Management. https://ops.fhwa.dot.gov/tim/

WHO. (2026). Heat and health. https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health

WHO Europe. (n.d.). Planning heat-health action. https://www.who.int/europe/health-topics/climate-change/planning-heat-health-action

WMO. (n.d.). Early Warnings for All. https://wmo.int/activities/early-warnings-all

NOAA National Weather Service. (n.d.). Turn Around Don't Drown. https://www.weather.gov/safety/flood-turn-around-dont-drown

World Bank. (2023). Urban Flood Risk Handbook. https://openknowledge.worldbank.org/entities/publication/c967c64d-a12f-407c-801b-3887755e6ddf

PostGIS. (n.d.). PostGIS documentation. https://postgis.net/

Expo. (2026). Create your first app. https://docs.expo.dev/tutorial/create-your-first-app/
