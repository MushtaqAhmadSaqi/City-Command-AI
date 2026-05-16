"""
Notification Routes — POST /notifications/draft, POST /notifications/send-mock

Stakeholder notification endpoints.
Full implementation in Step 16.
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/draft")
async def draft_notifications():
    """Generate stakeholder message drafts. Full implementation in Step 16."""
    return {"success": True, "message": "Notification draft endpoint ready. Full implementation in Step 16."}


@router.post("/send-mock")
async def send_mock_notification():
    """Mock send an approved notification. Full implementation in Step 16."""
    return {"success": True, "message": "Mock send endpoint ready. Full implementation in Step 16."}
