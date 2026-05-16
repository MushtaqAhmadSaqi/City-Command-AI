# CityCommand AI — Mobile Screen Checklist

## Design System
| Token | Value |
|---|---|
| Theme | Dark command-center UI |
| Primary | `#0F172A` | Accent | `#06B6D4` | Critical | `#EF4444` | Warning | `#F59E0B` | Safe | `#22C55E` |
| Typography | Inter/Roboto, 18-24px headings, 14-16px body |
| Cards | Rounded 16px, subtle border |

## Screens (13 total)

### 1. SplashScreen (Step 19)
- [ ] Logo, name, tagline, animated pulse, auto-navigate

### 2. LoginScreen (Step 19)
- [ ] Role selection (Operator/Dispatcher/Field/PIO/Admin), local state only

### 3. HomeDashboardScreen (Step 20)
- [ ] Risk score, active incidents, resources, API health, "Run CIRO Demo" CTA
- [ ] Empty state: "No incidents"

### 4. IncidentsScreen (Step 21)
- [ ] Priority cards, severity chips, confidence, filters, tap to detail

### 5. SignalIntakeScreen (Step 21)
- [ ] Text input, source type, location, demo loader, Roman Urdu sample

### 6. IncidentDetailScreen (Step 21)
- [ ] Title, type, severity, confidence, priority, radius, population, duration
- [ ] Evidence, alternates, action buttons, tabs (Overview/Evidence/Actions/Trace)

### 7. AIAnalysisScreen (Step 22)
- [ ] Confidence meter, score breakdown, contradiction panel, alternate hypothesis

### 8. ResourceAllocationScreen (Step 23)
- [ ] Available/assigned resources, ETA, trade-off cards, approve/modify

### 9. SimulationScreen (Step 24)
- [ ] Before/after metrics, delta bars, side effects, cost, risk

### 10. NotificationScreen (Step 25)
- [ ] Audience tabs (7 audiences), draft cards, approve, mock send

### 11. RecoveryScreen (Step 26)
- [ ] Old vs new classification, field evidence, correction message, retract

### 12. AgentTraceScreen (Step 27)
- [ ] Timeline (10+ entries), agent/step/IO/tools/fallback, filters, collapsible

### 13. DemoModeScreen (Step 28)
- [ ] API failure/duplicate/conflict/false alarm toggles, reset, run
