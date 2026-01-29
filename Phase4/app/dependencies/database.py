'''
DB Session Dependency
Purpose: Provide session to endpoints (the get_db function).
Why: Clean dependency injection for FastAPI.
'''
from app.database.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()