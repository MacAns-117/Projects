# AI Research Agent

Multi-agent research pipeline (Planner → Searcher → Synthesizer → Report Writer) built with LangGraph, Groq, and Tavily. Surfaces: Streamlit UI and a FastAPI wrapper.

**Pipeline note:** the graph is strictly linear — there is no `MAX_ITERATIONS` retry loop.

## Setup

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: set GROQ_API_KEY and TAVILY_API_KEY (and RESEARCH_API_TOKEN for the API)
```

Never commit a real `.env`.

## Streamlit UI

```bash
streamlit run app.py
```

Conversation memory is passed into the orchestrator as `context` so follow-ups can resolve prior turns. Use **Clear Conversation** in the sidebar to reset.

## FastAPI

Bind to localhost by default. Auth via header `X-API-Token` matching `RESEARCH_API_TOKEN`.

- If `RESEARCH_API_TOKEN` is unset: allow only when `RESEARCH_DEV=1`, else **503**.
- Wrong/missing token → **401**.

```bash
# Local dev without a token:
RESEARCH_DEV=1 uvicorn api:app --host 127.0.0.1 --port 8000

# Or with a token:
# RESEARCH_API_TOKEN=secret uvicorn api:app --host 127.0.0.1 --port 8000
# curl -H "X-API-Token: secret" -H "Content-Type: application/json" \
#   -d '{"question":"..."}' http://127.0.0.1:8000/research
```

Docs: http://127.0.0.1:8000/docs

## Tests

```bash
pytest tests/ -q
# or: RESEARCH_DEV=1 pytest tests/ -q
```

## Eval (paid / costly)

Live eval runs the full pipeline on 15 gold questions (~100+ API calls, 30–60 min). **Skip unless you accept Groq+Tavily cost.**

```bash
# Smoke scorer without keys:
python -m eval.run_eval --mock

# Live (requires GROQ_API_KEY + TAVILY_API_KEY):
# python -m eval.run_eval
```

## Dependency notes

`pip-audit` may report LangChain/LangGraph advisory packages. Do not bump LangChain majors casually — review GHSA/CVE text and pin carefully when upgrading.
