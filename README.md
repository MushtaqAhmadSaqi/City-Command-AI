# CityCommand AI 🌐 🚁

**Intelligent Crisis Orchestration & Resource Allocation Platform**

CityCommand AI is a deterministic, multi-agent AI pipeline built for municipal emergency response. It ingests raw, unstructured signals (social media, IoT sensors, field reports), triangulates credibility, classifies the threat, and autonomously coordinates a city-wide fleet response while keeping human operators in the loop for critical decision gating.

## 🏆 Key Features for Judging

- **Multi-Agent Orchestrator**: A 6-stage autonomous pipeline (Intake → Scoring → Classification → Severity → Dispatch → Notification).
- **Explainable AI (XAI)**: Full transparency via the Agent Trace Screen. See exactly *why* a resource was dispatched and the trade-offs the AI considered.
- **Deterministic Evaluation**: Re-run the same inputs, get the same outputs. Essential for reliable municipal software.
- **False Alarm Recovery**: Native rollback agent that instantly tears down a resolved/false incident and frees up tied resources.

---

## 🏗 System Architecture

The platform is a decoupled monorepo:

### 1. Backend (`/backend`)
- **Framework**: FastAPI (Python 3.10+)
- **Core Engine**: Pure functional Python orchestration (no heavy LangChain wrappers to ensure determinism).
- **State**: In-memory `data_store.py` (simulating a high-throughput Redis/Postgres cluster) pre-seeded with Islamabad GIS and fleet data.

### 2. Frontend (`/mobile`)
- **Framework**: React Native (Expo)
- **Styling**: NativeWind (Tailwind CSS for React Native)
- **State Management**: Zustand (React hooks-based atomic state)

---

## 🐳 Quick Start (Docker - Recommended)

The easiest way to run the entire stack is using Docker. No local Python or Node installation is required.

1. Ensure Docker is running.
2. Run the following command from the project root:
```bash
docker-compose up --build
```

**Access the Platform:**
- **Frontend Dashboard**: [http://localhost:8081](http://localhost:8081)
- **Backend API (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

**Load Demo Data:**
To trigger the demo scenario and populate the dashboard:
```bash
curl -X POST http://localhost:8000/demo/run-scenario
```

---

## 🚀 Manual Start (Local Demo)

### Terminal 1: Boot the Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # (or venv\Scripts\activate on Windows)
pip install -r requirements.txt
uvicorn app.main:app --reload
```
*The API will be live at `http://localhost:8000`*

### Terminal 2: Boot the Mobile App
```bash
cd mobile
npm install
npx expo start
```
*Press `a` to run on Android emulator or `i` for iOS simulator.*

---

## 💻 Tech Stack
* **Python** (FastAPI, Pydantic)
* **TypeScript** (React Native, Expo, Zustand)
* **TailwindCSS** (NativeWind)

*Built by MushtaqAhmadSaqi for the AI Hackathon.*