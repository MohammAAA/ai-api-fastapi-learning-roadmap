from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from openai import OpenAI
import os
import secrets # to generate random token string

security = HTTPBearer() # When attached with Depends(security), FastAPI will automatically check the Authorization header and parse the bearer credentials.
app = FastAPI()
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
valid_tokens = {secrets.token_urlsafe(): "user1",
                secrets.token_urlsafe(): "user2"
                }  # Simple example, This is an in-memory token map, so it resets when the app restarts and is not production ready, just for learning.

print(f"valid tokens are: {valid_tokens}")

@app.post("/ask")
async def ask(question: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    # The argument (credentials) extracts the bearer token from the Authorization header using the dependency (security), and stores it as an HTTPAuthCredential object.

    if credentials.credentials not in valid_tokens:     # Checks whether this token exists as a key in the valid_tokens dictionary.
        # If the token is missing, the caller is considered unauthenticated/unauthorized.
        raise HTTPException(status_code=401, detail="Invalid token")
    # else, proceed with the question
    prompt = question
    response = client_openai.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=1.0,
        max_output_tokens=600
    )
    return {
        "current_user": valid_tokens[credentials.credentials],
        "answer": response.output_text,
        "tokens": response.usage.total_tokens,
        "model": response.model
    }
