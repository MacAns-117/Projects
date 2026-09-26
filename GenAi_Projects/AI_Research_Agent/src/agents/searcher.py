"""
Searcher Agent — executes web searches and extracts content.

Takes a list of search queries (from the Planner), runs each via Tavily,
extracts full page content from top results, and summarizes each source.
Returns a structured list of findings ready for synthesis.
"""

from __future__ import annotations

from dataclasses import dataclass

from langchain_groq import ChatGroq

from src.config import MAX_SEARCH_RESULTS, MAX_SOURCES
from src.tools.search_tools import search_web
from src.tools.extract_tools import extract_page_content
from src.tools.summarize_tools import summarize_text


@dataclass
class Source:
    """A single research source with summary."""
    title: str
    url: str
    query: str           # The search query that found this source
    snippet: str          # Short snippet from search results
    summary: str          # LLM-generated summary of full page content
    relevance: float      # Tavily relevance score (0-1)


def search_and_extract(
    queries: list[str],
    llm: ChatGroq | None = None,
    max_per_query: int = MAX_SEARCH_RESULTS,
    max_sources: int = MAX_SOURCES,
) -> list[Source]:
    """Execute searches and extract/summarize content from results.

    For each query:
    1. Search via Tavily
    2. Take the top result(s)
    3. Extract full page content
    4. Summarize the content
    5. Package as a Source object

    Args:
        queries: List of search query strings (from the Planner).
        llm: An existing ChatGroq instance (optional — saves init time).
        max_per_query: Max search results per query.
        max_sources: Max total sources to collect.

    Returns:
        List of Source objects with summaries.
    """
    sources: list[Source] = []

    for i, query in enumerate(queries, 1):
        print(f"  [Search {i}/{len(queries)}] Query: {query[:60]}...")

        try:
            # Step 1: Search
            search_data = search_web(query, max_results=max_per_query)
            results = search_data.get("results", [])

            if not results:
                print(f"    No results found.")
                continue

            # Take top 2 results per query to stay within max_sources
            top_results = results[:2]

            for r in top_results:
                if len(sources) >= max_sources:
                    print(f"    Reached max sources ({max_sources}). Stopping.")
                    return sources

                url = r.get("url", "")
                title = r.get("title", "")
                snippet = r.get("content", "")
                score = r.get("score", 0.0)

                print(f"    Extracting: {title[:50]}...")

                # Step 2: Extract full page content (structured result)
                extract = extract_page_content(url)

                # Step 3: Summarize
                if not extract.ok:
                    # Fall back to the search snippet if extraction fails
                    summary = f"(Extraction failed) Search snippet: {snippet[:500]}"
                else:
                    print(f"    Summarizing {len(extract.content)} chars...")
                    summary = summarize_text(extract.content, llm=llm)

                # Step 4: Package
                sources.append(Source(
                    title=title,
                    url=url,
                    query=query,
                    snippet=snippet[:300],
                    summary=summary,
                    relevance=score,
                ))
                print(f"    ✓ Source added (relevance: {score:.2f})")

        except Exception as e:
            print(f"    ✗ Search failed for query '{query}': {e}")
            continue

    print(f"  Collected {len(sources)} sources total.")
    return sources


def format_sources_for_synthesis(sources: list[Source]) -> str:
    """Format all sources as a context string for the synthesizer agent.

    Args:
        sources: List of Source objects.

    Returns:
        Formatted string with numbered sources, titles, URLs, and summaries.
    """
    if not sources:
        return "No sources found."

    parts = []
    for i, s in enumerate(sources, 1):
        parts.append(
            f"[Source {i}]\n"
            f"Title: {s.title}\n"
            f"URL: {s.url}\n"
            f"Found via query: {s.query}\n"
            f"Relevance: {s.relevance:.2f}\n"
            f"Summary: {s.summary}\n"
        )

    return "\n---\n".join(parts)


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    from src.config import validate_config

    print("Testing searcher agent...\n")
    validate_config()

    # Use queries from a simple test plan
    test_queries = [
        "what is langgraph multi-agent orchestration",
        "langgraph vs crewai comparison 2025",
    ]

    print(f"\nExecuting {len(test_queries)} searches...\n")
    sources = search_and_extract(test_queries, max_sources=4)

    print(f"\n{'='*60}")
    print(f"Collected {len(sources)} sources:\n")
    print(format_sources_for_synthesis(sources))
