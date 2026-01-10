from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from google import genai
from google.genai import errors
from openai import OpenAI, RateLimitError
import logging
import os
from app.core.csv_logging_config import setup_csv_logging
from app.schemas.request_parameters import FocusOptions, CodeReviewRequest

# Initialize the logger configs
setup_csv_logging("logs/Code_review_assistant_logs.csv")
csv_logger = logging.getLogger("appLoger.csv")

app = FastAPI()
client_gemini = genai.Client()
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post ("/review-code")
async def code_reviewer(file: UploadFile = File(), language: str = Form(), focus: str = Form()):
    try:
        # Read the raw code content
        code_bytes = await file.read()
        code_text = code_bytes.decode("utf-8")
        prompt = f"you are an experienced {language} developer and architect with 15+ years of experience. Perform comprehensive code review for the following {language} code, provide more focus on the {focus} \n\n {code_text}"
        response = client_gemini.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        csv_logger.info(
            "prompt_row",
            extra={
                "prompt": prompt,
                "response": response.text,
                "model": "gemini-2.5-flash",
                "totalTokens": response.usage_metadata.total_token_count
            }
        ) # This will be logged to the .csv file
        return {
            "answer": response.text,
            "tokens": response.usage_metadata.total_token_count,
            "model": "gemini-2.5-flash"
        }
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid file encoding. Please upload UTF-8 text.")
    except errors.ClientError as e: # Client errors handling
    # 429 is the HTTP status code for Rate Limit Exceeded
        if e.code == 429:
            print("Gemini rate limit exceeded! Fall-back to OpenAI model ...")
            try:
                
                response_openai = client_openai.responses.create(
                    model="gpt-4o-mini",
                    input=prompt,
                    temperature=1.0,
                )
                csv_logger.info(
                    "prompt_row",
                    extra={
                        "prompt": prompt,
                        "response": response_openai.output_text,
                        "model": response_openai.model,
                        "totalTokens": response_openai.usage.total_tokens
                    }
                ) # This will be logged to the .csv file
                return {
                    "answer": response_openai.output_text,
                    "tokens": response_openai.usage.total_tokens,
                    "model": response_openai.model
                }
            except RateLimitError: # Gemini Client error (RateLimit) handling
                raise HTTPException(status_code=429, detail=" OpenAI rate limit exceeded .. exiting")
            except Exception as e: # OpenAI server errors handling
                logging.error(f"API error: {e}") # Internal loggings for debugging purposes, the user does not have access to it.
                raise HTTPException(status_code=500, detail="OpenAI internal server error .. exiting")
        else:
            print(f"Gemini API Error: {e} .. exiting")

    except Exception as e: # Gemini Server errors handling
        print(f"Gemini Unexpected error: {e}")



""" Problem: JSON is fragile for raw code because of quotes, newlines, and tabs.
Solution: Change our endpoint to accept the code as a file upload..
This way, the client sends the file content as-is (binary/text stream) and FastAPI handles it safely without any JSON parsing issues.
"""

