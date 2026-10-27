"""Single place for chunk size, top-k, model names, score floor, reranker."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval. App, API, and eval all read these so README numbers match the code.
DEFAULT_TOP_K = 8
MAX_PDFS = 10
SCORE_FLOOR = 0.22          # cosine-like score = 1 / (1 + chroma_distance)
# If the best retrieved score is below this, treat as no relevant context (OOS gate).
# Tuned on the full arXiv gold set so in-scope Hit@k stays high while OOS returns empty.
MIN_TOP_SCORE = float(os.getenv("RAG_MIN_TOP_SCORE", "0.32"))
# Cross-encoder logit floor after rerank. OOS ~-11; hard in-scope can be ~-6. Default -9.
CE_MIN_SCORE = float(os.getenv("RAG_CE_MIN_SCORE", "-9.0"))
MMR_LAMBDA = 0.5
HYBRID_VECTOR_WEIGHT = 0.6  # rest is BM25

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
LLM_MODEL = "openai/gpt-oss-120b"
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 1024

# Cross-encoder rerank (CPU-friendly MiniLM). Lazy-loaded; fails open to no-rerank.
RERANKER_MODEL = os.getenv(
    "RAG_RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2"
)
RERANK_CANDIDATES = int(os.getenv("RAG_RERANK_CANDIDATES", "20"))
# Env: unset/auto → on iff model loads; "1"/"true" → force on; "0"/"false" → force off.

DEFAULT_DB_PATH = str(ROOT / "chroma_db")
EVAL_DB_PATH = str(ROOT / "chroma_db_eval")
DEFAULT_COLLECTION = "pdf_chunks"

SAMPLE_PDF_DIR = ROOT / "data" / "sample_pdfs"
ARXIV_PDF_DIR = ROOT / "data" / "arxiv_pdfs"
UPLOAD_DIR = ROOT / "data" / "uploaded_pdfs"
GOLD_QA_PATH = ROOT / "eval" / "gold_qa.json"

RETRIEVAL_METHODS = ("similarity", "mmr", "hybrid")

# OpenAI-compatible judge / generation overrides (Groq, llama.cpp, etc.)
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip() or None
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip() or os.getenv("GROQ_API_KEY", "").strip() or None
JUDGE_MODEL = os.getenv("JUDGE_MODEL", os.getenv("LLM_MODEL", LLM_MODEL))
