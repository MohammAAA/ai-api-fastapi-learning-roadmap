'''
Authentication Logic
Purpose: Handle token validation
Why: Centralizes auth logic, reusable across endpoints.
'''

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from app.config import settings

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify bearer token and return user_id."""
    token = credentials.credentials
    if token not in settings.VALID_TOKENS:
        raise HTTPException(status_code=401, detail="Invalid token")
    return settings.VALID_TOKENS[token]
