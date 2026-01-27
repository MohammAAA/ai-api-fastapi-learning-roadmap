'''
OpenAI Wrapper
Purpose: Encapsulate OpenAI API calls
Why: Isolated, testable, easy to swap OpenAI for another provider.
'''

from openai import OpenAI
from app.config import settings

client_openai = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_ai_response(conversation_json: str) -> str:
    """Call OpenAI API."""
    response = client_openai.responses.create(
        model="gpt-4o-mini",
        input=conversation_json,
        temperature=1.0
    )
    return response.output_text
