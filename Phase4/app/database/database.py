'''
Database Setup
Purpose: Create engine, SessionLocal, Base
Why: Isolates DB infrastructure from business logic.
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Engine
engine = create_engine(settings.DATABASE_URL)

# SessionLocal factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Base for ORM models
Base = declarative_base()
