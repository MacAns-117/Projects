"""Retrieve + prompt + generate. Citations in the prompt are [1], [2], … matching retrieve_with_context."""

from __future__ import annotations

from dataclasses import dataclass

from langchain_chroma import Chroma

from src.config import CE_MIN_SCORE, DEFAULT_DB_PATH, DEFAULT_TOP_K, MIN_TOP_SCORE, SCORE_FLOOR
from src.retriever import RetrievedChunk, retrieve_with_context

SYSTEM_PROMPT = """You are a helpful assistant that answers questions using ONLY the context provided below.

Rules:
1. Use ONLY the information in the context to answer the question.
2. Look through ALL numbered chunks, not just the first one.
3. If the context does not contain the answer, or the question is unrelated to the documents (geography, people, events never mentioned), say exactly: "I don't know based on the provided context."
4. Cite sources with [N] matching the numbers in the context. Example: "The Transformer uses self-attention [1]."
5. If several chunks support a claim, cite them all: "N = 6 encoder layers [1][2]."
6. Do not use knowledge outside the context. Do not guess.
7. Keep answers short. No preamble.

Context:
{context}

Question: {question}

Answer:"""

REFUSAL = "I don't know based on the provided context."


@dataclass
class RAGAnswer:
    question: str
    answer: str
    citations: list[RetrievedChunk]
    context_string: str
    method: str
    reranked: bool = False


def ask(
    question: str,
    vectorstore: Chroma | None = None,
    db_path: str | None = None,
    top_k: int = DEFAULT_TOP_K,
    method: str = "hybrid",
    score_floor: float = SCORE_FLOOR,
    use_reranker: bool | None = None,
    min_top_score: float | None = MIN_TOP_SCORE,
    ce_min_score: float | None = CE_MIN_SCORE,
) -> RAGAnswer:
    if vectorstore is None and db_path is None:
        db_path = DEFAULT_DB_PATH

    from src.reranker import should_rerank

    do_rerank = should_rerank(use_reranker)

    citations, context_string = retrieve_with_context(
        question,
        vectorstore=vectorstore,
        db_path=db_path,
        top_k=top_k,
        method=method,
        score_floor=score_floor,
        use_reranker=do_rerank,
        min_top_score=min_top_score,
        ce_min_score=ce_min_score,
    )

    if not citations:
        return RAGAnswer(
            question=question,
            answer=REFUSAL,
            citations=[],
            context_string="No relevant context found.",
            method=method,
            reranked=False,
        )

    from src.llm import generate_answer

    prompt = SYSTEM_PROMPT.format(context=context_string, question=question)
    answer = generate_answer(prompt)
    return RAGAnswer(
        question=question,
        answer=answer,
        citations=citations,
        context_string=context_string,
        method=method,
        reranked=do_rerank and any("+rerank" in (c.method or "") for c in citations),
    )
