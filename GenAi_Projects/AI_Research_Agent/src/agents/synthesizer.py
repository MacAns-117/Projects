"""
Synthesizer Agent — cross-references findings from multiple sources.

Takes the formatted summaries from the Searcher and produces a structured
synthesis: key themes, points of consensus, points of disagreement, and
ranked key insights. This is the "reasoning" step before report writing.
"""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from src.config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS


SYNTHESIS_PROMPT = """You are a research synthesis assistant.

You will be given multiple summarized sources from web research. Your job is to:
1. Identify the key themes across the sources.
2. Note where sources agree (consensus).
3. Note where sources disagree or offer different perspectives.
4. Rank the most important insights (top 3-5).

Format your output as follows:

KEY THEMES:
- Theme 1: [description]
- Theme 2: [description]
...

CONSENSUS:
- [What most sources agree on]
...

DISAGREEMENTS / NUANCES:
- [Where sources differ, and why]
...

KEY INSIGHTS (ranked):
1. [Most important insight]
2. [Second most important]
3. [Third most important]
...

Remember: You are synthesizing, not summarizing. Show how the sources relate to each other.

Sources:
{sources}

Synthesis:"""


def create_synthesizer(llm: ChatGroq | None = None):
    """Create a synthesizer chain.

    Args:
        llm: An existing ChatGroq instance (optional — saves init time).

    Returns:
        A runnable chain that takes sources text and returns a synthesis.
    """
    if llm is None:
        llm = ChatGroq(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
        )

    prompt = ChatPromptTemplate.from_template(SYNTHESIS_PROMPT)
    chain = prompt | llm
    return chain


def synthesize(sources_text: str, llm: ChatGroq | None = None) -> str:
    """Synthesize multiple sources into a structured analysis.

    Args:
        sources_text: Formatted string of all source summaries (from Searcher).
        llm: An existing ChatGroq instance (optional).

    Returns:
        Structured synthesis string with Key Themes, Consensus,
        Disagreements, and Key Insights.
    """
    if not sources_text or sources_text == "No sources found.":
        return "No sources available to synthesize."

    chain = create_synthesizer(llm)
    response = chain.invoke({"sources": sources_text})
    return response.content


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    from src.config import validate_config

    print("Testing synthesizer agent...\n")
    validate_config()

    # Simulate sources text (normally comes from Searcher)
    test_sources = """
[Source 1]
Title: LangGraph Introduction
URL: https://example.com/1
Found via query: what is langgraph
Relevance: 0.95
Summary: LangGraph is a framework for building stateful, multi-agent workflows with LLMs. It uses a state machine approach where each node is an agent or function, and edges define the flow of control.

---
[Source 2]
Title: CrewAI vs LangGraph
URL: https://example.com/2
Found via query: langgraph vs crewai
Relevance: 0.88
Summary: CrewAI is role-based and simpler, while LangGraph offers more control over state management and conditional routing. LangGraph is better for complex pipelines; CrewAI is better for quick prototyping.

---
[Source 3]
Title: Multi-Agent Systems in Production
URL: https://example.com/3
Found via query: multi-agent orchestration 2025
Relevance: 0.82
Summary: Production multi-agent systems require robust state management, error handling, and observability. LangGraph's state machine model aligns well with production requirements.
"""

    print("Synthesizing test sources...\n")
    result = synthesize(test_sources)
    print(result)