# Your Personalized AI APIs + FastAPI Learning Strategy
## Backend Engineer → AI Agent Developer (12-16 weeks)

---

## PHASE 0: Foundation Sprint (1-2 weeks)
### Goal: Get your first API call working + understand the ecosystem

#### 1.1 Quick Wins (Day 1-2)
**What you'll do:**
- [ ] Install Python 3.11+ (you have basic Python, so skip tutorials)
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Install: `pip install openai requests python-dotenv`
- [ ] Read (15 min): https://platform.openai.com/docs/quickstart (just the code, not all theory)
- [ ] Get API key: https://platform.openai.com/account/api-keys

**First hands-on code (10 min task):**
```python
# simple_openai_call.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",  # cheaper for learning
    messages=[{"role": "user", "content": "Say hello"}]
)
print(response.choices[0].message.content)
```

**Why this works for you:**
- No FastAPI yet, no REST concepts yet
- Just "function call → get output" (like C function call you're familiar with)
- You see the API works
- Builds confidence

#### 1.2 Understand What You Just Did (Day 2-3)
**Reading (non-linear, focus on YOUR questions):**

| Document | Why | How Long | What to Focus On |
|----------|-----|----------|-----------------|
| [OpenAI API Overview](https://platform.openai.com/docs/overview) | Understand their service model | 10 min | Models, pricing, rate limits |
| [OpenAI Models Documentation](https://platform.openai.com/docs/models) | Know what models exist and costs | 15 min | gpt-4o-mini vs gpt-4o (price/quality tradeoff) |
| [OpenAI Chat Completions](https://platform.openai.com/docs/api-reference/chat/create) | Know parameters you can use | 20 min | temperature, max_tokens, system role |
| [Gemini API Overview](https://ai.google.dev/docs) | Compare alternative | 10 min | Free tier limits, models available |
| [REST API Fundamentals](https://restfulapi.net/) (read only first 3 sections) | Understand HTTP (REST is HTTP) | 15 min | What's a GET, POST, status codes |

**Do NOT read:**
- Full FastAPI documentation yet (too much)
- Authentication deep dives yet
- Advanced API patterns yet

#### 1.3 Checkpoint 1: Theory + Quick Hands-On
**Your task (complete by end of Day 3):**
```
Create: api_exploration.py that:
1. Calls OpenAI API with different models (gpt-4o-mini, gpt-3.5-turbo)
2. Measures response time for each
3. Prints cost per 1000 tokens (use pricing from docs)
4. Adds temperature=0.5 and observe difference in responses
5. Prints a comparison table
```

**Why:**
- Practical understanding of model tradeoffs
- You'll reference this later
- Adds to portfolio (shows you understand cost optimization)

---

## PHASE 1: REST + FastAPI Fundamentals (2-3 weeks)
### Goal: Build a real API server, understand HTTP, deploy your first API

#### 2.1 REST API Concepts (Self-paced: 3 days)
**You need to understand:**
1. **HTTP Methods**: GET (read), POST (create), PUT (update), DELETE (remove)
2. **Status Codes**: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 500 Server Error
3. **Request/Response**: Headers, Body (JSON), Path parameters, Query parameters
4. **Statelessness**: Each request independent (unlike C sockets where you hold state)

**How to learn (YOUR way - mixing reading + trying):**
```
Day 1: Read
- https://restfulapi.net/http-methods/
- https://restfulapi.net/http-status-codes/
- https://restfulapi.net/json-vs-xml/ (just JSON, skip XML)
(Total: 30 min, don't memorize, just understand concepts)

Day 2: Hands-on REST testing
- Install: pip install requests httpie
- Use curl/Postman to test real APIs
  Example: curl https://api.example.com/users (public API)
- Write Python script that makes GET, POST requests
- See headers, status codes in action

Day 3: Summarize
- Create: rest_concepts.md
  - Document 5 HTTP methods with real examples
  - Document 3 status codes with when to use
  - Document request/response structure
```

#### 2.2 FastAPI Basics (3-4 days)
**Install & First Server:**
```
pip install fastapi uvicorn
```

**Micro-progression (do in order):**

**Day 1: Hello World**
```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```
Then:
```bash
uvicorn main:app --reload
# Open browser: http://localhost:8000
# Auto docs: http://localhost:8000/docs
```

**Your aha moment:** FastAPI auto-generates API documentation! (Swagger UI at /docs)

**Day 2: Add POST, understand request bodies**
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return {"created": item.name, "price": item.price}
```
Test with:
```bash
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Book","price":10.5}'
```

**Day 3: Understand routing, parameters, Pydantic validation**
Read: https://fastapi.tiangolo.com/tutorial/first-steps/ (sections 1-5 only)

**Why FastAPI for you:**
- Automatic validation (Pydantic) catches errors like C type checking
- Auto-documentation (no manual work)
- Modern Python (async support)
- Used in production AI services

#### 2.3 Checkpoint 2: Build Your First API
**Project: Simple Math API Server**

Requirements:
```
1. GET /health → returns {"status": "ok"}
2. POST /calculate
   Input: {"operation": "add|subtract|multiply", "a": float, "b": float}
   Output: {"result": float, "operation": string}
3. GET /history → returns list of last 10 calculations
   (store in memory, using list)
4. Add request logging (print request time, path, response status)
```

**Deliverables:**
- `calculator_api.py` (your API code)
- `test_calculator.py` (test 10+ scenarios with requests library)
- `README.md` with:
  - How to run
  - API documentation (endpoints, inputs, outputs)
  - Lessons learned

**Evaluation rubric (self-assess):**
- [ ] API runs without errors
- [ ] All endpoints work (test with curl or Python requests)
- [ ] Input validation works (try invalid input, see proper error)
- [ ] Code is readable (comments, variable names)
- [ ] README is clear enough someone else could use it

---

## PHASE 2: Integrate OpenAI/Gemini APIs (2-3 weeks)
### Goal: Build real AI-powered services, understand authentication, rate limiting, error handling

#### 3.1 Authentication & Environment Management (1-2 days)
**Problem**: Don't want API keys in your code

**Solution:**
```python
# .env
OPENAI_API_KEY=sk-xxxxx
GEMINI_API_KEY=yyyy

# config.py
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
```

Read: https://python-dotenv.readthedocs.io/ (just the basic section)

**Gemini setup** (compare to OpenAI):
- Get key: https://aistudio.google.com/app/apikeys
- Install: `pip install google-generativeai`
- Understand: https://ai.google.dev/tutorials/python_quickstart

**Compare OpenAI vs Gemini** (15 min):
| Aspect | OpenAI | Gemini |
|--------|--------|--------|
| Free tier | $5 credit | 60 req/min |
| Cost | Higher | Competitive |
| Models | GPT-4, 4o-mini | Gemini 2.0 Flash |
| Community | Larger | Growing |
| For you | Start here | Backup option |

#### 3.2 Build AI-Powered Apps (Iterative)

**Week 1: Text-Based AI Agent**

Project: **Personal Assistant API**
```
POST /ask
Input: {"question": string, "context": string (optional)}
Output: {"answer": string, "model": string, "tokens_used": int}

Features:
1. Send question to OpenAI
2. Track tokens (understand costs)
3. Handle errors gracefully (rate limits, API errors)
4. Log all requests for debugging
```

**Implementation guide:**
```python
from fastapi import FastAPI, HTTPException
from openai import OpenAI, RateLimitError
import logging

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/ask")
async def ask_question(question: str, context: str = None):
    try:
        prompt = f"{context}\n\nQuestion: {question}" if context else question
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return {
            "answer": response.choices[0].message.content,
            "tokens": response.usage.total_tokens,
            "model": response.model
        }
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except Exception as e:
        logging.error(f"API error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

**Why this structure:**
- Error handling (important in production)
- Logging (debug real issues)
- Cost tracking (understand API economics)

**Your checkpoint deliverables:**
- `assistant_api.py`
- `test_assistant.py` (test error cases too)
- `cost_analysis.md` (how much did you spend, per question cost)

---

**Week 2: Build a Practical Daily Agent**

Choose ONE (based on your profession):

**Option A: Code Review Assistant**
```
POST /review-code
Input: {"code": string, "language": string, "focus": "performance|security|style"}
Output: {"review": string, "issues": list, "improvements": list}

Practical: Analyze your own code snippets
```

**Option B: Professional Summary Generator**
```
POST /summarize
Input: {"content": string, "format": "bullet|paragraph|table"}
Output: {"summary": string, "key_points": list}

Practical: Summarize technical articles, papers, documentation
```

**Option C: Code Snippet Search + Explanation**
```
GET /explain?language=python&concept=async
Output: {"explanation": string, "code_example": string, "when_to_use": string}

Practical: Learning tool for yourself
```

**Implementation timeline:**
- Day 1-2: Design API schema (inputs/outputs)
- Day 3: Implement with OpenAI
- Day 4: Test with real use cases
- Day 5: Add Gemini as fallback
- Day 6: Optimize (caching, cost)
- Day 7: Documentation + deployment draft

---

## PHASE 3: Advanced Patterns (3-4 weeks)
### Goal: Build production-ready agents, understand RAG, streaming, memory

#### 4.1 Streaming & Real-time Responses (1 week)
**Problem**: Long responses take time. User waits. Bad UX.
**Solution**: Stream responses as they're generated

```python
from fastapi.responses import StreamingResponse

@app.post("/ask-streaming")
async def ask_streaming(question: str):
    def generate():
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}],
            stream=True
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    return StreamingResponse(generate(), media_type="text/plain")
```

**Test with curl:**
```bash
curl http://localhost:8000/ask-streaming?question="Explain async"
```

#### 4.2 Implement Memory/History (1-2 weeks)

**Problem**: Each request forgets previous context
**Solution**: Store conversation history

```python
from datetime import datetime

conversations: dict = {}  # In-memory; use database in production

@app.post("/chat")
async def chat(conversation_id: str, message: str):
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    
    # Build message history
    history = conversations[conversation_id]
    history.append({"role": "user", "content": message})
    
    # Send to API with history
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history
    )
    
    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})
    
    return {
        "response": assistant_message,
        "conversation_id": conversation_id,
        "turn": len(history) // 2
    }
```

**Real use case:** Build a personal productivity assistant that remembers your projects, preferences, past questions

#### 4.3 Vector Databases & RAG (1-2 weeks)

**Your background advantage**: You understand embeddings + vector databases conceptually

**Project: Personal Knowledge Base Query**
```
1. Upload technical documents (PDFs, markdown)
2. System splits into chunks, creates embeddings (OpenAI API)
3. Store in vector DB (Pinecone free tier or Qdrant local)
4. User asks question → search relevant chunks → ask LLM with context

POST /upload
Input: document file

POST /query
Input: {"question": string}
Output: {"answer": string, "sources": list}
```

**Implementation:**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Pseudo-code (you'll flesh this out)
documents = load_pdf("myfile.pdf")
chunks = split_text(documents, chunk_size=500)
embeddings = OpenAIEmbeddings()
vector_store = PineconeVectorStore.from_documents(chunks, embeddings)

# Later: query
results = vector_store.similarity_search("what is async?", k=3)
prompt = f"Answer based on: {results}\n\nQuestion: {question}"
response = client.chat.completions.create(...)
```

---

## PHASE 4: Production Hardening (2-3 weeks)
### Goal: Deploy real service, learn DevOps basics, make portfolio-ready

#### 5.1 Authentication & Authorization
**Real problem**: Your API should be secure

```python
from fastapi.security import HTTPBearer, HTTPAuthCredential
import secrets

security = HTTPBearer()
valid_tokens = {secrets.token_urlsafe(): "user1"}  # Simple example

@app.post("/ask")
async def ask(question: str, credentials: HTTPAuthCredential = Depends(security)):
    if credentials.credentials not in valid_tokens:
        raise HTTPException(status_code=401, detail="Invalid token")
    # ... your logic
```

Read: https://fastapi.tiangolo.com/tutorial/security/ (sections 1-3)

#### 5.2 Database Integration
**Move from in-memory to real database**

```python
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import Session

# SQLite for learning, PostgreSQL for production
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = Column(String)  # JSON serialized

# Now store persistent conversations
```

#### 5.3 Deployment
**Deploy to free tier:**
- **Option 1**: Render.com (free, simple)
- **Option 2**: Railway.app (free tier)
- **Option 3**: Replit (super simple)

```bash
# Simple: just push to GitHub, connect to Render
# Render auto-deploys on push
```

**Why this matters for job market:**
- "Deployed to production" on resume = real experience
- Shows you understand full stack
- Hiring managers see real URLs they can test

---

## PHASE 5: Capstone Project (2-3 weeks)
### Build ONE polished, resume-worthy project

**Recommendation for you: Professional AI Pair Programmer**

**Scope:**
```
1. User uploads code file
2. System analyzes for:
   - Code style issues
   - Performance problems
   - Security vulnerabilities
   - Refactoring opportunities
3. Generates detailed report + fixes

Features:
- Support multiple languages (Python, C, Go)
- Streaming analysis (long files)
- Persistent history
- Cost tracking
- Deployed live
```

**Why this project:**
- Shows full-stack skills (API, DB, RAG-like retrieval, LLM)
- Directly useful in your job search (can analyze real code)
- Impressive for interviews ("I built an AI pair programmer")
- Extensible (add more languages, metrics, etc.)

**Deliverables for portfolio:**
```
1. GitHub repo with:
   - Clean code structure
   - Comprehensive README
   - Requirements.txt
   - Example usage docs
   - Architecture diagram

2. Deployed live URL (works in browser/CLI)

3. Demo video (5 min):
   - Show the problem
   - Show your solution
   - Show deployment
   - Discuss what you learned

4. Blog post (2-3 pages):
   - Problem statement
   - Technical approach
   - Challenges faced
   - Future improvements
```

---

## Learning Resources by Phase

### Essential Reading (in order)
1. **REST API**: https://restfulapi.net/
2. **FastAPI Basics**: https://fastapi.tiangolo.com/tutorial/
3. **OpenAI API**: https://platform.openai.com/docs/api-reference
4. **Gemini API**: https://ai.google.dev/
5. **Python AsyncIO** (when you hit streaming): https://docs.python.org/3/library/asyncio.html

### Tools You'll Use
```
Development:
- VSCode + Python extension
- Postman (API testing)
- Git (version control)

APIs:
- OpenAI platform
- Gemini API
- Pinecone (vector DB free tier)

Deployment:
- Render.com
- GitHub
```

### Communities
- **OpenAI Community**: https://community.openai.com/
- **FastAPI Discord**: (active, responsive)
- **LangChain Community**: (if you use LangChain)
- **HackerNews**: Lurk for insights

---

## Your Weekly Checkpoint Format

Each week, you'll submit:
```
## Week X Checkpoint

### Completed Tasks
- [ ] Task 1
- [ ] Task 2

### Code Quality
- Lines: XXX
- Functions: Y
- Tests: Z

### Learning Insights
- What you learned
- What confused you
- Questions for next checkpoint

### Deliverables
- Code link (GitHub)
- Working API URL (if deployed)
- Test results

### Self-Assessment
- [ ] Code works
- [ ] Tests pass
- [ ] Documentation clear
- [ ] Ready for code review
```

---

## Timeline Summary

| Phase | Duration | Output |
|-------|----------|--------|
| Phase 0 | 1-2 weeks | First API call, understand ecosystem |
| Phase 1 | 2-3 weeks | Working FastAPI server, REST fundamentals |
| Phase 2 | 2-3 weeks | OpenAI/Gemini integration, practical agents |
| Phase 3 | 3-4 weeks | Streaming, memory, RAG, advanced patterns |
| Phase 4 | 2-3 weeks | Auth, database, deployment, production hardening |
| Phase 5 | 2-3 weeks | Capstone project, portfolio-ready |
| **Total** | **12-18 weeks** | **Production-grade AI service** |

---

## Your Competitive Edge

**Most candidates:**
- Take online course, get certificate
- Never deploy anything
- No real projects on resume

**You will:**
1. Build real projects (5+ of them)
2. Deploy live (hiring managers test it)
3. Show understanding of full stack (API, auth, database, deployment)
4. Demonstrate cost optimization (important for LLM apps)
5. Have code on GitHub (proof of skills)

**Job interview scenario:**
- Interviewer asks: "Show us something you built with AI APIs"
- You: Share URL to deployed service, explain architecture, show code
- You win.

---

## How to Proceed

1. **Start immediately**: Begin Phase 0, do the "simple_openai_call.py" today
2. **Follow the checkpoint format**: After each phase, share your work
3. **Ask questions**: When stuck, ask—don't go down rabbit holes
4. **Adjust pace**: If something takes longer, that's fine—learn deeply
5. **Build real projects**: Don't skip to next phase without working code

You have a 12-16 week runway to transform from "someone who knows APIs exist" to "engineer who ships AI products."

Let's start.
