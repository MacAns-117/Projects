import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.chunker import Chunk


@pytest.fixture
def tiny_chunks():
    return [
        Chunk("alpha.pdf", 1, "The Transformer encoder has N = 6 identical layers.", 0),
        Chunk("alpha.pdf", 3, "d_model is 512 in the base Transformer.", 0),
        Chunk("beta.pdf", 1, "RAG-Sequence uses one retrieved document for the whole target.", 0),
        Chunk("beta.pdf", 6, "RAG-Sequence scores 44.5 EM on Natural Questions.", 0),
    ]
