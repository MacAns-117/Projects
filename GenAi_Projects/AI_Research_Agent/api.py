"""
FastAPI wrapper for the AI Research Agent.

Exposes the multi-agent orchestrator as a REST API:

    GET  /health   → {"status": "ok", "model": "..."}
    POST /research → {"question": "..."} → {"report": "...", "sources": [...]}

Auth: send header X-API-Token matching RESEARCH_API_TOKEN.
If RESEARCH_API_TOKEN is unset, requests are allowed only when RESEARCH_DEV=1;
otherwise the API returns 503.

Run with:
    uvicorn api:app --host 127.0.0.1 --port 8000 --reload
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

# Ensure src/ is importable
sys.path.insert(0, str(Path(__file__).parent))

from src.config import validate_config, LLM_MODEL
from src.orchestrator import create_orchestrator

logger = logging.getLogger(__name__)


# --- Request/Response Models ---
class ResearchRequest(BaseModel):
    question: str


class SourceInfo(BaseModel):
    title: str
    url: str
    summary_preview: str


class ResearchResponse(BaseModel):
    report: str
    sources: list[SourceInfo]
    num_sources: int


class HealthResponse(BaseModel):
    status: str
    model: str


def require_api_token(x_api_token: str | None = Header(default=None, alias="X-API-Token")) -> None:
    """Require X-API-Token unless local RESEARCH_DEV=1 with no token configured."""
    expected = os.environ.get("RESEARCH_API_TOKEN", "").strip()
    if not expected:
        if os.environ.get("RESEARCH_DEV") == "1":
            return
        raise HTTPException(
            status_code=503,
            detail="API token not configured. Set RESEARCH_API_TOKEN or RESEARCH_DEV=1 for local use.",
        )
    if not x_api_token or x_api_token != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API token")


# --- App Initialization ---
app = FastAPI(
    title="AI Research Agent API",
    description="Multi-agent LangGraph system for automated web research",
    version="1.0.0",
)

_orchestrator = None


def _ensure_loaded():
    global _orchestrator
    if _orchestrator is None:
        validate_config()
        _orchestrator = create_orchestrator()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check if the API is running."""
    try:
        _ensure_loaded()
        return HealthResponse(status="ok", model=LLM_MODEL)
    except Exception:
        logger.exception("Health check failed")
        raise HTTPException(status_code=503, detail="Service not ready")


@app.post("/research", response_model=ResearchResponse, dependencies=[Depends(require_api_token)])
async def research(request: ResearchRequest):
    """Run a research query and get a structured report.

    This runs the full pipeline: Planner → Searcher → Synthesizer → Report Writer.
    Takes 2-4 minutes to complete.
    """
    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        _ensure_loaded()

        result = await asyncio.to_thread(
            _orchestrator.invoke,
            {
                "question": request.question,
                "context": "",
                "search_queries": [],
                "sources": [],
                "sources_text": "",
                "synthesis": "",
                "final_report": "",
            },
        )

        # Format sources for response
        sources_list = [
            SourceInfo(
                title=s.title,
                url=s.url,
                summary_preview=s.summary[:200] + "..." if len(s.summary) > 200 else s.summary
            )
            for s in result.get("sources", [])
        ]

        return ResearchResponse(
            report=result.get("final_report", "Error: Could not generate report."),
            sources=sources_list,
            num_sources=len(sources_list),
        )

    except HTTPException:
        raise
    except Exception:
        logger.exception("Research failed")
        raise HTTPException(status_code=500, detail="Research failed due to an internal error.")


if __name__ == "__main__":
    import uvicorn
    print("Starting AI Research Agent API...")
    print("Docs available at: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
