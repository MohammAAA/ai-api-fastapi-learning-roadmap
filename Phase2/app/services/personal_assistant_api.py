from fastapi import FastAPI, HTTPException
from openai import OpenAI, RateLimitError
import os
import logging
from app.core.file_logging_config import setup_logging
from app.core.csv_logging_config import setup_csv_logging


setup_logging() # initialize the logging configuration
setup_csv_logging("logs/assistant_prompts.csv")

txt_logger = logging.getLogger("appLoger.file")
csv_logger = logging.getLogger("appLoger.csv")
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/ask")
async def ask_question(question: str, context: str = None):
    try:
        prompt = f"{context}\n\nQuestion: {question}" if context else question
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
            temperature=1.0,
            max_output_tokens=600
        )
        txt_logger.info(
            "prompt & response:",
            extra={"extra_data": {
                "prompt": prompt,
                "response": response.output_text,
                "tokens": response.usage.total_tokens,
                "model": response.model,
            }}
        ) # This will be logged to the .txt file
        csv_logger.info(
            "prompt_row",
            extra={
                "prompt": prompt,
                "response": response.output_text,
                "model": response.model,
                "totalTokens": response.usage.total_tokens
            }
        ) # This will be logged to the .csv file
        return {
            "answer": response.output_text,
            "tokens": response.usage.total_tokens,
            "model": response.model
        }
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except Exception as e:
        logging.error(f"API error: {e}") # Internal loggings for debugging purposes, the user does not have access to it.
        raise HTTPException(status_code=500, detail="Internal server error")
