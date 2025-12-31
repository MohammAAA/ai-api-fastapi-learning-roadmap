from fastapi import FastAPI
from app.routers import benchmark

app = FastAPI(title="AI API Learning Roadmap")
app.include_router(benchmark.router)

@app.get("/health")
def health():
    return {"status": "ok"}
