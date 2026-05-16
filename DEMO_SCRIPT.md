# 🎤 CityCommand AI - Hackathon Pitch & Demo Script

**Estimated Time**: 4 minutes

## Phase 1: The Hook (0:00 - 0:45)
*(Show the Splash Screen loading into the Home Dashboard)*

**Speaker:**
"Cities today don't suffer from a lack of data; they suffer from a lack of *orchestration*. When a crisis hits, 911 calls, social media, and IoT sensors flood in. But human operators get overwhelmed, leading to delayed dispatch and misallocated resources. 

Meet **CityCommand AI**—a deterministic, multi-agent orchestrator. It doesn't just 'summarize' data. It runs a rigorous 6-stage pipeline to evaluate credibility, predict severity, and physically dispatch fleets in seconds."

---

## Phase 2: The Multi-Node Crisis (0:45 - 1:30)
*(Navigate to the `Demo` tab. Tap `Launch Islamabad Crisis Scenario`.)*

**Speaker:**
"Let me show you a live simulation. We've just injected 5 raw, unstructured signals into the system simultaneously. 
*(Switch to `Dashboard` tab)*
Instantly, the AI has ingested the noise, grouped the signals, and synthesized them into two distinct incidents: A severe heatwave blackout in F-11, and localized urban flooding in G-10."

---

## Phase 3: Explainable AI & Transparency (1:30 - 2:30)
*(Tap on the `F-11 Heat Emergency` incident to open Incident Detail. Tap `AI Analysis`.)*

**Speaker:**
"If an AI is going to dispatch city resources, it must be auditable. Here in the AI Analysis screen, you can see exactly *why* it scored this as CRITICAL. It shows us the specific credibility penalties and the alternate hypotheses it considered.

*(Go back. Tap `Agent Traces`)*
And for true transparency, we record every single execution step on an immutable timeline. Judges, look at this trace: You can see exactly what the `CredibilityScoringAgent` consumed, and its exact output. Nothing is a black box."

---

## Phase 4: Autonomous Dispatch & Simulation (2:30 - 3:30)
*(Go back. Tap `Resource Allocation`)*

**Speaker:**
"Because this is a CRITICAL incident, the `ResourceAllocationAgent` has automatically unlocked the 'City Reserve' fleet. It intelligently dispatched 3 ambulances and 2 traffic police units. But look here—it also generated *Trade-off Notes*, explicitly telling the operator *why* it pulled units from neighboring sectors.

*(Go back. Tap `Simulation`)*
Before authorizing drastic measures, the operator can use the Action Sandbox. If we simulate a 'traffic_reroute', the AI predicts it will improve response times by 15%, but warns us of a side effect: adjacent grid congestion."

---

## Phase 5: Human in the Loop & Recovery (3:30 - 4:00)
*(Go back. Tap `Notifications`)*

**Speaker:**
"The AI is autonomous, but it knows its limits. It drafted 7 different stakeholder messages. Because the Public SMS is sensitive, the AI flagged it with an 'Operator Approval Required' lock. It will not send until a human hits Approve.

*(Go back. Tap `Mark as False Alarm` at the bottom)*
And if this was all a mistake? The `FalseAlarmRecoveryAgent` executes a safe rollback—instantly recalling the fleet, retracting notifications, and logging the teardown for audit.

**Conclusion:** 
"CityCommand AI. Deterministic, transparent, and ready to orchestrate the cities of tomorrow. Thank you."
