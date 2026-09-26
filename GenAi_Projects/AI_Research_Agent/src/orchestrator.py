"""
Orchestrator — LangGraph state machine for the AI Research Agent.

Coordinates the full research pipeline:
  START → Planner → Searcher → Synthesizer → Report Writer → END

Each node produces output that feeds into the next:
- Planner: question (+ optional context) → search queries
- Searcher: queries → sources with summaries
- Synthesizer: sources → structured synthesis
- Report Writer: synthesis + sources (+ optional context) → final research report

Note: this is a linear pipeline (no retry/iteration loops).
"""

from __future__ import annotations

from typing import TypedDict

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

from src.config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from src.agents.planner import plan_searches
from src.agents.searcher import search_and_extract, format_sources_for_synthesis, Source
from src.agents.synthesizer import synthesize
from src.agents.report_writer import write_report


# --- State Definition ---
class ResearchState(TypedDict):
    """State that flows through the LangGraph nodes."""
    question: str
    context: str                 # optional prior conversation for follow-ups
    search_queries: list[str]
    sources: list[Source]
    sources_text: str            # formatted for synthesis/report
    synthesis: str
    final_report: str


# --- Node 1: Planner ---
def create_planner_node(llm: ChatGroq):
    """Create the planner node function."""
    def planner_node(state: ResearchState) -> dict:
        question = state["question"]
        context = state.get("context", "") or ""
        print(f"\n  [Planner] Decomposing question: {question[:60]}...")

        queries = plan_searches(question, llm=llm, context=context)

        print(f"  [Planner] Generated {len(queries)} search queries:")
        for i, q in enumerate(queries, 1):
            print(f"    {i}. {q}")

        return {"search_queries": queries}

    return planner_node


# --- Node 2: Searcher ---
def create_searcher_node(llm: ChatGroq):
    """Create the searcher node function."""
    def searcher_node(state: ResearchState) -> dict:
        queries = state["search_queries"]
        print(f"\n  [Searcher] Executing {len(queries)} searches...")

        sources = search_and_extract(queries, llm=llm)
        sources_text = format_sources_for_synthesis(sources)

        return {
            "sources": sources,
            "sources_text": sources_text,
        }

    return searcher_node


# --- Node 3: Synthesizer ---
def create_synthesizer_node(llm: ChatGroq):
    """Create the synthesizer node function."""
    def synthesizer_node(state: ResearchState) -> dict:
        sources_text = state.get("sources_text", "No sources found.")
        print(f"\n  [Synthesizer] Cross-referencing {len(state.get('sources', []))} sources...")

        synthesis = synthesize(sources_text, llm=llm)

        print(f"  [Synthesizer] Synthesis complete ({len(synthesis)} chars)")
        return {"synthesis": synthesis}

    return synthesizer_node


# --- Node 4: Report Writer ---
def create_report_writer_node(llm: ChatGroq):
    """Create the report writer node function."""
    def report_writer_node(state: ResearchState) -> dict:
        question = state["question"]
        context = state.get("context", "") or ""
        synthesis = state.get("synthesis", "")
        sources_text = state.get("sources_text", "No sources available.")

        print(f"\n  [Report Writer] Generating final report...")

        report = write_report(
            question=question,
            synthesis=synthesis,
            sources_text=sources_text,
            llm=llm,
            context=context,
        )

        print(f"  [Report Writer] Report generated ({len(report)} chars)")
        return {"final_report": report}

    return report_writer_node


# --- Build the Graph ---
def create_orchestrator(llm: ChatGroq | None = None):
    """Create the LangGraph orchestrator for the research agent.

    The graph flow is linear (no retries / MAX_ITERATIONS loop):
      START → Planner → Searcher → Synthesizer → Report Writer → END

    No conditional routing needed — every research question follows
    the same pipeline. The intelligence is in the agents, not the routing.

    Invoke with:
        {"question": "...", "context": "" (optional prior turns), ...}

    Args:
        llm: An existing ChatGroq instance (optional — saves init time).

    Returns:
        Compiled LangGraph ready to invoke with {"question": "...", "context": "..."}
    """
    if llm is None:
        llm = ChatGroq(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
        )

    # Create node functions
    planner = create_planner_node(llm)
    searcher = create_searcher_node(llm)
    synthesizer = create_synthesizer_node(llm)
    report_writer = create_report_writer_node(llm)

    # Build the graph
    workflow = StateGraph(ResearchState)

    # Add nodes
    workflow.add_node("planner", planner)
    workflow.add_node("searcher", searcher)
    workflow.add_node("synthesizer", synthesizer)
    workflow.add_node("report_writer", report_writer)

    # Set entry point
    workflow.set_entry_point("planner")

    # Add linear edges (no conditional routing — research always follows this path)
    workflow.add_edge("planner", "searcher")
    workflow.add_edge("searcher", "synthesizer")
    workflow.add_edge("synthesizer", "report_writer")
    workflow.add_edge("report_writer", END)

    # Compile
    app = workflow.compile()
    return app


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    from src.config import validate_config

    print("=" * 70)
    print("Testing AI Research Agent Orchestrator")
    print("=" * 70)

    validate_config()

    print("\nCreating orchestrator...")
    orchestrator = create_orchestrator()

    question = "What are the latest advances in RAG evaluation?"
    print(f"\nResearch Question: {question}")
    print("=" * 70)

    result = orchestrator.invoke({
        "question": question,
        "context": "",
        "search_queries": [],
        "sources": [],
        "sources_text": "",
        "synthesis": "",
        "final_report": "",
    })

    print("\n" + "=" * 70)
    print("FINAL RESEARCH REPORT")
    print("=" * 70)
    print(result["final_report"])

    print("\n" + "=" * 70)
    print(f"Sources used: {len(result['sources'])}")
    for i, s in enumerate(result["sources"], 1):
        print(f"  [{i}] {s.title} — {s.url}")
    print("=" * 70)
