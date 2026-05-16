"""
Demo Routes — POST /demo/run-scenario

Loads the main demo scenario with seed data.
Full implementation in Step 8.
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/run-scenario")
async def run_demo_scenario():
    """Load the G-10 flood + heat emergency demo scenario."""
    # Full implementation in Step 8
    return {
        "success": True,
        "message": "Demo scenario endpoint ready. Full implementation in Step 8.",
    }


@router.post("/reset")
async def reset_demo():
    """Reset all demo data to initial empty state."""
    from app.data_store import data_store
    data_store.reset()
    return {
        "success": True,
        "message": "Demo data reset to empty state.",
    }
