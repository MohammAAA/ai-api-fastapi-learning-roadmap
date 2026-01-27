'''Chat Business Logic
Purpose: Core chat logic (separated from controller).
Why: Business logic separated from HTTP layer (easy to test and reuse).
'''

import json
from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.services.openai_service import get_ai_response

def get_or_create_conversation(db: Session, conversation_id: str, user_id: str) -> Conversation:
    """Fetch or create conversation."""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        conv = Conversation(id=conversation_id, user_id=user_id, messages=json.dumps([]))
        db.add(conv)
        db.commit()
        db.refresh(conv)
    return conv

def append_user_message(messages_json: str, user_message: dict) -> str:
    """Append user message to conversation."""
    messages = json.loads(messages_json or "[]")
    if isinstance(messages, dict):
        messages = [messages]
    messages.append(user_message)
    return json.dumps(messages)

def process_chat(db: Session, conversation_id: str, message: str, user_id: str):
    """Full chat processing."""
    user_msg = {"role": "user", "message": message}
    
    # Get or create conversation
    conv = get_or_create_conversation(db, conversation_id, user_id)
    
    # Append user message
    conv.messages = append_user_message(conv.messages, user_msg)
    
    # Get AI response
    stored_messages = json.loads(conv.messages)
    ai_response_text = get_ai_response(json.dumps(stored_messages))
    
    # Append AI response
    ai_msg = {"role": "assistant", "message": ai_response_text}
    stored_messages.append(ai_msg)
    conv.messages = json.dumps(stored_messages)
    
    db.commit()
    
    return {
        "conversation_id": conv.id,
        "user_id": conv.user_id,
        "created_at": conv.created_at,
        "history": stored_messages,
        "response": ai_response_text
    }
