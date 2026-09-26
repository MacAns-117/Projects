"""
Report Writer Agent — generates a structured research report.

Takes the synthesis and original sources, and produces a polished
report with sections (Summary, Key Findings, Sources) and inline
citations. This is the final output the user sees.
"""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from src.config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS


REPORT_PROMPT = """You are a research report writer.

You will be given:
1. The user's original question.
2. A synthesis of findings from multiple web sources.
3. The list of sources with URLs.
4. Optional prior conversation context (for follow-up questions).

Write a structured research report in Markdown format with the following sections:

## Summary
(A 2-3 sentence overview of the findings.)

## Key Findings
(Bullet points with inline citations like [1], [2]. Reference sources by their number.)

## Detailed Analysis
(2-3 paragraphs explaining the findings in more detail, with citations.)

## Confidence Assessment
(State whether the findings are High, Medium, or Low confidence based on source agreement and quality.)

## Sources
(List the sources as numbered references with URLs.)

Guidelines:
- Cite sources using [1], [2], etc. matching the source numbers.
- Be factual — do not add information not in the synthesis.
- If sources disagree, mention both perspectives.
- Keep the report under 800 words.
- If prior context is present, acknowledge follow-ups briefly in the Summary.

Prior conversation context (may be empty):
{context}

User's question: {question}

Synthesis:
{synthesis}

Sources:
{sources}

Report:"""


def create_report_writer(llm: ChatGroq | None = None):
    """Create a report writer chain.

    Args:
        llm: An existing ChatGroq instance (optional — saves init time).

    Returns:
        A runnable chain that takes question, synthesis, and sources.
    """
    if llm is None:
        llm = ChatGroq(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
        )

    prompt = ChatPromptTemplate.from_template(REPORT_PROMPT)
    chain = prompt | llm
    return chain


def write_report(
    question: str,
    synthesis: str,
    sources_text: str,
    llm: ChatGroq | None = None,
    context: str = "",
) -> str:
    """Generate a structured research report.

    Args:
        question: The user's original research question.
        synthesis: The structured synthesis from the Synthesizer agent.
        sources_text: Formatted source list with URLs (from Searcher).
        llm: An existing ChatGroq instance (optional).
        context: Optional prior conversation context for follow-ups.

    Returns:
        Markdown-formatted research report string.
    """
    if not synthesis or synthesis == "No sources available to synthesize.":
        return "## Summary\n\nUnable to generate a report — no sources were found for this query."

    chain = create_report_writer(llm)
    response = chain.invoke({
        "question": question,
        "synthesis": synthesis,
        "sources": sources_text,
        "context": context or "(none)",
    })
    return response.content


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    from src.config import validate_config

    print("Testing report_writer agent...\n")
    validate_config()

    # Simulate inputs
    test_question = "What are the latest advances in RAG evaluation?"
    test_synthesis = """KEY THEMES:
- Theme 1: RAG evaluation requires multiple metrics (retrieval + generation).
- Theme 2: RAGAS is the dominant framework but has limitations.

CONSENSUS:
- Most sources agree that Hit@K is the standard retrieval metric.
- RAGAS faithfulness scoring is widely adopted but expensive to run.

DISAGREEMENTS:
- Some sources argue RAGAS is too strict; others say it's necessary.

KEY INSIGHTS (ranked):
1. Hybrid retrieval (BM25 + vector) improves Hit@K by 15-20%.
2. Faithfulness scoring requires LLM calls, making it expensive at scale.
3. There is no single "best" metric — evaluation should be task-specific."""

    test_sources = """[Source 1]
Title: RAGAS Framework
URL: https://example.com/ragas

[Source 2]
Title: RAG Evaluation Benchmarks
URL: https://example.com/benchmarks

[Source 3]
Title: Hybrid Retrieval Analysis
URL: https://example.com/hybrid"""

    print("Writing report...\n")
    report = write_report(test_question, test_synthesis, test_sources)
    print(report)
