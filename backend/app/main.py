"""
CityCommand AI — FastAPI Backend Entry Point

This is the main application file for the CityCommand AI backend.
It configures CORS, mounts all route modules, and provides
the global in-memory data store used throughout the demo.

Architecture:
  Mobile App → HTTPS REST → This FastAPI Backend
    → Agent Orchestrator → Services → Data Store
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes import demo, signals, incidents, resources, simulations, notifications, traces, health, recovery
from app.data_store import data_store


# ──────────────────────────────────────────────
# Application Lifespan (startup / shutdown)
# ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize demo data store on startup."""
    print("🚀 CityCommand AI backend starting...")
    print(f"📦 Data store initialized with {len(data_store.incidents)} incidents")
    yield
    print("🛑 CityCommand AI backend shutting down.")


# ──────────────────────────────────────────────
# FastAPI Application
# ──────────────────────────────────────────────
app = FastAPI(
    title="CityCommand AI",
    description="Agentic Crisis Intelligence & Response Orchestrator — Backend API",
    version="1.0.0",
    lifespan=lifespan,
)


# ──────────────────────────────────────────────
# CORS Middleware
# Allow all origins for hackathon demo flexibility.
# In production, restrict to specific domains.
# ──────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# Mount Route Modules
# Each module handles a specific API domain.
# ──────────────────────────────────────────────
app.include_router(health.router,        prefix="/health",        tags=["Health"])
app.include_router(demo.router,          prefix="/demo",          tags=["Demo"])
app.include_router(signals.router,       prefix="/signals",       tags=["Signals"])
app.include_router(incidents.router,     prefix="/incidents",     tags=["Incidents"])
app.include_router(resources.router,     prefix="/resources",     tags=["Resources"])
app.include_router(simulations.router,   prefix="/simulations",   tags=["Simulations"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
app.include_router(traces.router,        prefix="/traces",        tags=["Traces"])
app.include_router(recovery.router,      prefix="/recovery",      tags=["Recovery"])


# ──────────────────────────────────────────────
# Root Endpoint
# ──────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint — API identity and status."""
    return {
        "project": "CityCommand AI",
        "description": "Agentic Crisis Intelligence & Response Orchestrator",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "endpoints": {
            "health": "/health/apis",
            "demo": "/demo/run-scenario",
            "signals": "/signals",
            "incidents": "/incidents",
            "traces": "/traces",
        }
    }
