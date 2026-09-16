"""Single place for chunk size, top-k, model names, score floor."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval. App, API, and eval all read these so README numbers match the code.
DEFAULT_TOP_K = 8
MAX_PDFS = 10
SCORE_FLOOR = 0.22          # cosine-like score = 1 / (1 + chroma_distance)
MMR_LAMBDA = 0.5
HYBRID_VECTOR_WEIGHT = 0.6  # rest is BM25

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
LLM_MODEL = "openai/gpt-oss-120b"
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 1024

DEFAULT_DB_PATH = str(ROOT / "chroma_db")
EVAL_DB_PATH = str(ROOT / "chroma_db_eval")
DEFAULT_COLLECTION = "pdf_chunks"

SAMPLE_PDF_DIR = ROOT / "data" / "sample_pdfs"
UPLOAD_DIR = ROOT / "data" / "uploaded_pdfs"
GOLD_QA_PATH = ROOT / "eval" / "gold_qa.json"

RETRIEVAL_METHODS = ("similarity", "mmr", "hybrid")
