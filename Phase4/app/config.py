''' 
This file holds configuration & settings
Purpose: Centralize environment variables and app settings.
Why: Keeps config in one place, makes it easy to switch between dev/prod.
'''

from pydantic_settings import BaseSettings
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent #BASE_DIR = Phase4/
# print (BASE_DIR)


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/data/test.db" # This ensures the path works regardless of where we run the app from.
    
    # OpenAI
    OPENAI_API_KEY: str

    # Gemini
    GEMINI_API_KEY: str
    
    # Security
    VALID_TOKENS: dict = {
        "Token123": "user1",
        secrets.token_urlsafe(): "user2"
    }
    
    # Environment
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
