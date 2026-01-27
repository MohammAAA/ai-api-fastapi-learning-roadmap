'''
Chat Endpoints
Purpose: HTTP handlers (the "View" in MVC).
Why: Thin controller; just handles HTTP, then delegates to service.
'''

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.security.auth import verify_token
from app.services.chat_service import process_chat

router = APIRouter(prefix="/api/v1", tags=["chat"])

@router.post("/chat")
def chat(
    conversation_id: str,
    message: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(verify_token)
):
    """Chat endpoint."""
    result = process_chat(db, conversation_id, message, user_id)
    return result
