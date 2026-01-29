'''
OpenAI Wrapper
Purpose: Encapsulate OpenAI API calls
Why: Isolated, testable, easy to swap OpenAI for another provider.
'''

from google import genai
from google.genai import errors
from fastapi import HTTPException
from openai import AsyncOpenAI, RateLimitError # AsyncOpenAI to await the asynchronous APIs by OpenAI
from app.config import settings

client_gemini = genai.Client()
client_openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

def get_ai_response(conversation_json: str) -> str:
    """Call OpenAI API."""
    try:
        response = client_gemini.aio.models.generate_content(model="gemini-2.5-flash", contents=conversation_json)
        
    except errors.ClientError as e: # Client errors handling
    # 429 is the HTTP status code for Rate Limit Exceeded
        if e.code == 429:
            print("Gemini rate limit exceeded! Fall-back to OpenAI model ...")
            try:      
                response = client_openai.responses.create(
                    model="gpt-4o-mini",
                    input=conversation_json,
                    temperature=1.0
                )
                return response.output_text
            except RateLimitError: # OpenAI Client error (RateLimit) handling
                raise HTTPException(status_code=429, detail=" OpenAI rate limit exceeded .. exiting")
            except Exception as e: # OpenAI server errors handling
                raise HTTPException(status_code=500, detail="OpenAI internal server error .. exiting")
        else:
            print(f"Gemini API Error: {e} .. exiting")

    except Exception as e: # Gemini Server errors handling
        print(f"Gemini Unexpected error: {e}")

    return response.text



