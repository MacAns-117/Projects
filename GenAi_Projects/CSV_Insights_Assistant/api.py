"""FastAPI wrapper. /health, /schema, /ingest, /ask."""

from __future__ import annotations

import io
import sys
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent))

from src.config import LLM_MODEL
from src.data_loader import load_csv_buffer, load_default
from src.orchestrator import create_orchestrator, empty_state
from src.schema import schema_card

app = FastAPI(
    title="CSV Insights Assistant",
    description="LangGraph analytics over one in-memory CSV at a time.",
    version="0.2.0",
)

_df = None
_orchestrator = None
_source_name = None


def _set_df(df, name: str):
    global _df, _orchestrator, _source_name
    _df = df
    _source_name = name
    _orchestrator = create_orchestrator(df)


def _ensure():
    global _df, _orchestrator, _source_name
    if _df is None:
        df = load_default()
        _set_df(df, df.attrs.get("source_name", "hotel_bookings.csv"))


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    intent: str
    data_findings: str = ""
    chart_description: str = ""
    has_chart: bool = False
    source: str = ""


class HealthResponse(BaseModel):
    status: str
    dataset_rows: int
    columns: int
    source: str
    model: str


@app.get("/health", response_model=HealthResponse)
def health():
    try:
        _ensure()
        return HealthResponse(
            status="ok",
            dataset_rows=len(_df),
            columns=len(_df.columns),
            source=_source_name or "",
            model=LLM_MODEL,
        )
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/schema")
def schema():
    try:
        _ensure()
        return {"source": _source_name, "card": schema_card(_df)}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a .csv file")
    try:
        raw = await file.read()
        df = load_csv_buffer(io.BytesIO(raw), filename=file.filename)
        _set_df(df, file.filename)
        return {"source": file.filename, "rows": len(df), "columns": list(df.columns)}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        _ensure()
        result = _orchestrator.invoke(empty_state(request.question))
        findings = result.get("data_findings") or ""
        return AskResponse(
            answer=result.get("final_answer") or "No answer.",
            intent=result.get("intent") or "unknown",
            data_findings=findings[:800],
            chart_description=result.get("chart_description") or "",
            has_chart=result.get("chart_fig") is not None,
            source=_source_name or "",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
