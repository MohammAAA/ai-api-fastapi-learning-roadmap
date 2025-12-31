import time
from openai import OpenAI
from app.data.models_info import pricing_reference
from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def _prices_for(model: str) -> tuple[float, float]:
    # cents-per-token from your pricing_reference
    if model == "gpt-4o-mini":
        m = pricing_reference["models"]["gpt-4o-mini"]
    elif model == "gpt-4.1-nano":
        m = pricing_reference["models"]["gpt-4-nano"]
    else:
        raise ValueError(f"Unknown model for pricing: {model}")
    return m["input_token_price"], m["output_token_price"]

def run_once(prompt: str, model: str, api_type: str, temperature: float | None = None):
    # lazy import, this is to avoid circular import:
    # where 2 files are trying to import from each other at the same time
    from scripts.api_exploration import print_response
    start = time.perf_counter()

    if api_type == "chat_completions":
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        latency_ms = (time.perf_counter() - start) * 1000
        input_tokens = resp.usage.prompt_tokens
        output_tokens = resp.usage.completion_tokens
        response_preview = resp.choices[0].message.content
        print_response(
            model = model,
            response = response_preview
        )

    elif api_type == "responses":
        resp = client.responses.create(
            model=model,
            input=prompt,
            temperature=temperature,
        )
        latency_ms = (time.perf_counter() - start) * 1000
        input_tokens = resp.usage.input_tokens
        output_tokens = resp.usage.output_tokens
        response_preview = resp.output_text
        print_response(
            model = model,
            response = response_preview
        )

    else:
        raise ValueError("api_type must be chat_completions or responses")

    in_price, out_price = _prices_for(model)
    total_cost_cents = input_tokens * in_price + output_tokens * out_price

    return {
        "model": model,
        "api_type": api_type,
        "latency_ms": latency_ms,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_cost_cents": total_cost_cents,
    }
