from pydantic import BaseModel
from typing import Literal, Optional

ApiType = Literal["chat_completions", "responses"]

class BenchmarkRequest(BaseModel):
    prompt: str
    model: str
    api_type: ApiType
    temperature: Optional[float] = None

class BenchmarkResult(BaseModel):
    model: str
    api_type: ApiType
    latency_ms: float
    input_tokens: int
    output_tokens: int
    total_cost_cents: float
