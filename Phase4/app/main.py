'''
Entry Point
Purpose: Assemble the FastAPI app.
Why: Minimal main.py
'''

from fastapi import FastAPI
from app.database.database import Base, engine
from app.controllers import chat_controller

# Create tables
Base.metadata.create_all(engine)

# Create app
app = FastAPI(title="AI Agents Backend")

# Include routers
app.include_router(chat_controller.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
