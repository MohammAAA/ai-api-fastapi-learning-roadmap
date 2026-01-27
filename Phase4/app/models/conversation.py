'''
ORM Models
Purpose: Define database schema
Why: Separates data structure from business logic.
'''

from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone
from app.database.database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    messages = Column(String)  # JSON string
