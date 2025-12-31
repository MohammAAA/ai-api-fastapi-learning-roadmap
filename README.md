# ai-api-fastapi-learning-roadmap

AI Agent Developer learning roadmap with **hands-on** projects covering HTTP/REST, FastAPI, LLM API integration (OpenAI/Gemini), streaming, memory, RAG, auth, persistence, and deployment.

---

## Why this repo exists

This repo is a structured, project-driven path to go from “I can call an AI API” to “I can ship and deploy an AI-powered backend service.” It emphasizes measurable tradeoffs (latency + cost), clean API design, and production-minded practices (logging, error handling, auth, DB).

---

## Roadmap (phases)

### Phase 0 — Foundation Sprint
**Goal:** First API call + understand the ecosystem.

**Deliverables**
- `Phase0-FoundationSprint/src/simple_openai_call.py` — minimal OpenAI call.
- `Phase0-FoundationSprint/src/api_exploration.py` — compare models, measure latency, estimate cost, print a comparison table.

### Phase 1 — REST + FastAPI fundamentals
**Goal:** Build a real API server and understand HTTP.

**Deliverables**
- `Phase1-Rest-FastApi-Fundamentals/src/main.py` — FastAPI starter server + routes.
- `Phase1-Rest-FastApi-Fundamentals/src/calculator_api.py` — Simple Math API Server
- `Phase1-Rest-FastApi-Fundamentals/tests/test_calculator.py` — 10+ scenarios
- `Phase1-Rest-FastApi-Fundamentals/docs/rest_concepts.md` — methods, status codes, request/response structure

### Phase 2 — Integrate OpenAI/Gemini
**Goal:** Build real AI-powered services with auth/environment management, rate limits, and error handling.

**Deliverables**
- `Phase2-Integrate_AiModel/src/config.py` — environment management via `.env`
- `Phase2-Integrate_AiModel/src/assistant_api.py` — `POST /ask` assistant endpoint
- `Phase2-Integrate_AiModel/tests/test_assistant.py` — includes error cases
- `Phase2-Integrate_AiModel/docs/cost_analysis.md` — spend + per-question cost notes

### Phase 3 — Advanced patterns
**Goal:** Streaming, memory/history, RAG.

**Deliverables**
- Streaming endpoint (`/ask-streaming`)
- Conversation memory endpoint (`/chat`)
- RAG endpoints: `POST /upload`, `POST /query`

### Phase 4 — Production hardening
**Goal:** Auth, DB integration, deployment.

**Deliverables**
- Auth protection (HTTP Bearer) for sensitive endpoints
- Persistence (SQLite for learning; Postgres for production)
- Deployed service (Render/Railway/Replit)

### Phase 5 — Capstone (2–3 weeks)
**Goal:** One polished, resume-worthy project.

**Recommended capstone**
- Professional AI Pair Programmer (file upload + analysis + streaming + history + cost tracking)

---

## Repo structure

To be finalized

---

## Prerequisites

- Python 3.11+
- An OpenAI API key (and optionally a Gemini API key)
- Basic CLI comfort (running scripts, installing packages)

---

## Setup (Ubuntu/macOS/Windows)
### 1) Install dependencies (Ubutnu)

Start minimal (Phase 0):
- Install Anaconda: (https://www.anaconda.com/docs/getting-started/anaconda/install)
```bash
pip install openai==2.14.0 requests==2.32.5 python-dotenv==1.2.1 tabulate==0.9.0
```
Later (Phase 1+):
```bash
pip install fastapi uvicorn
```
### 2) Create virtual environment
```bash
conda create -n AI-Agents python=3.13
conda activate AI-Agents
```

### 3) Configure environment variables

Create `.env` (never commit it):

```bash
cp .env.example .env
```

.env.example:
```python
OPENAI_API_KEY=sk-your_key_here
GEMINI_API_KEY=your_key_here
```
`python-dotenv` can load .env values into environment variables using `load_dotenv()`.

### Phase 0: Quick start
#### Run the first OpenAI call
```bash
python -m Phase0.src.simple_openai_call
```
Expected: prints the assistant message.

##### Run model exploration
```bash
python -m Phase0.src.api_exploration --prompt "Say hello in Egyptian Arabic."
```
