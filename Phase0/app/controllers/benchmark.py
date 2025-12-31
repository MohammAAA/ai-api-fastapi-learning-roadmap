from fastapi import APIRouter
from app.schemas.benchmark import BenchmarkRequest, BenchmarkResult
from app.services.openai_benchmark import run_once

router = APIRouter(prefix="/benchmark", tags=["benchmark"])

@router.post("/run", response_model=BenchmarkResult)
def benchmark(req: BenchmarkRequest):
    return run_once(req.prompt, req.model, req.api_type, req.temperature)
