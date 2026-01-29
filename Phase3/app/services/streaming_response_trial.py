import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI, RateLimitError, OpenAI

app = FastAPI()
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/ask-streaming")
async def ask_streaming(question: str):
    def generate():
        response = client_openai.responses.create(
            model="gpt-4o-mini",
            input=question,
            stream=True
        )
        for chunk in response:
             # Responses streaming emits different event types; we want text deltas.
            if chunk.type == "response.output_text.delta":
                yield chunk.delta  # send only the newly generated text
            elif chunk.type == "response.completed":
                break
    
    # SSE (server-sent-events (event-stream)) is usually best for browser streaming; use text/plain if we prefer raw chunks.
    return StreamingResponse(generate(), media_type="text/event-stream")
