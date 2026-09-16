"""
Embeddings module — wraps HuggingFace's all-MiniLM-L6-v2 model.

Converts text chunks into 384-dimensional vectors that capture semantic
meaning. Two texts with similar meaning will have vectors that are close
together in vector space — which is what lets Chroma find "similar"
chunks when the user asks a question.

The model runs locally (no API calls, no API key needed) and is cached
after first load (~3-5 seconds). Subsequent calls reuse the cached
instance.
"""

from __future__ import annotations

from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings


# The model identifier on HuggingFace Hub
# all-MiniLM-L6-v2 = 384 dimensions, ~80MB, trained on 1B+ sentence pairs
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Model kwargs — runs on CPU by default (no GPU needed for this model size)
MODEL_KWARGS = {"device": "cpu"}

# Encode kwargs — normalize embeddings for cosine similarity
ENCODE_KWARGS = {"normalize_embeddings": True}


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """Get a cached HuggingFace embeddings instance.

    The model loads once (~3-5 seconds on first call) and is reused
    for all subsequent calls. This is important because reloading the
    model on every chunk would be catastrophically slow.

    Returns:
        HuggingFaceEmbeddings instance wrapping all-MiniLM-L6-v2.

    Why lru_cache(maxsize=1):
        - First call: loads model from disk (~3-5 sec)
        - All future calls: returns cached instance (instant)
        - maxsize=1 means only one instance is ever cached
    """
    print(f"Loading embedding model: {MODEL_NAME}...")
    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs=MODEL_KWARGS,
        encode_kwargs=ENCODE_KWARGS,
    )
    print("  ✓ Embedding model loaded (384-dim vectors, CPU)")
    return embeddings


def embed_text(text: str) -> list[float]:
    """Embed a single text string into a 384-dim vector.

    Args:
        text: The text to embed.

    Returns:
        A list of 384 floats representing the text's semantic vector.
    """
    embeddings = get_embeddings()
    return embeddings.embed_query(text)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed multiple texts in batch (faster than calling embed_text N times).

    Args:
        texts: List of text strings to embed.

    Returns:
        List of 384-dim vectors, one per input text.
    """
    embeddings = get_embeddings()
    return embeddings.embed_documents(texts)


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    print("Testing embeddings module...\n")

    # Test 1: single text
    vec = embed_text("The cat sat on the mat.")
    print(f"Test 1: embed_text()")
    print(f"  Input: 'The cat sat on the mat.'")
    print(f"  Vector dimensions: {len(vec)}")
    print(f"  First 5 values: {[round(v, 4) for v in vec[:5]]}")
    print(f"  Vector is normalized: {abs(sum(v*v for v in vec) - 1.0) < 0.01}")

    # Test 2: semantic similarity
    texts = [
        "The cat sat on the mat.",
        "A feline rested on a rug.",  # similar meaning, different words
        "The stock market crashed today.",  # completely different
    ]
    print(f"\nTest 2: semantic similarity")
    vectors = embed_texts(texts)

    # Cosine similarity (vectors are already normalized, so dot product = cosine sim)
    def cosine_sim(a, b):
        return sum(x * y for x, y in zip(a, b))

    sim_01 = cosine_sim(vectors[0], vectors[1])
    sim_02 = cosine_sim(vectors[0], vectors[2])
    print(f"  'cat on mat' vs 'feline on rug':  {sim_01:.4f}  (should be high)")
    print(f"  'cat on mat' vs 'stock crashed':   {sim_02:.4f}  (should be low)")
    print(f"\n  → Similar meanings score high, different meanings score low.")
    print(f"  → This is how the retriever finds relevant chunks.")