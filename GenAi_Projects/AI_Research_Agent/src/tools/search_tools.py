"""
Search tools — Tavily-based web search for the research agent.

Wraps the Tavily API to provide clean, structured search results.
The agent calls these tools to find information on the web.
"""

from __future__ import annotations
from typing import TypedDict, List
from tavily import TavilyClient

from src.config import TAVILY_API_KEY, MAX_SEARCH_RESULTS, SEARCH_DEPTH, INCLUDE_ANSWER

# Module-level lazy singleton — reuse one client across searches
_tavily_client: TavilyClient | None = None


def _get_tavily_client() -> TavilyClient:
    """Return a shared TavilyClient instance."""
    global _tavily_client
    if _tavily_client is None:
        if not TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY not set in environment.")
        _tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    return _tavily_client


class SearchResult(TypedDict):
    """Structured search result returned by search_web."""
    title: str
    url: str
    content: str
    score: float


def search_web(query: str, max_results: int = MAX_SEARCH_RESULTS) -> dict:
    """Search the web using Tavily and return structured results.

    Use this tool when you need to find information on the web.
    Returns titles, URLs, content snippets, and relevance scores.

    Args:
        query: The search query (natural language).
        max_results: Max number of results to return (default 5).

    Returns:
        Dictionary with:
        - "answer": Quick AI-generated answer (if INCLUDE_ANSWER is True)
        - "results": List of SearchResult dicts
        - "query": The original query

    Raises:
        ValueError: If TAVILY_API_KEY is not set.
        RuntimeError: If the Tavily API call fails.
    """
    client = _get_tavily_client()

    try:
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth=SEARCH_DEPTH,
            include_answer=INCLUDE_ANSWER,
        )
    except Exception as e:
        raise RuntimeError(f"Tavily search failed: {str(e)}")

    # Format the results
    results: List[SearchResult] = []
    for r in response.get("results", []):
        results.append(SearchResult(
            title=r.get("title", ""),
            url=r.get("url", ""),
            content=r.get("content", ""),
            score=r.get("score", 0.0),
        ))

    return {
        "answer": response.get("answer", ""),
        "results": results,
        "query": query,
    }


def format_search_results(search_data: dict) -> str:
    """Format search results as a readable string for the LLM context.

    Args:
        search_data: The dict returned by search_web().

    Returns:
        Formatted string with numbered sources, titles, URLs, and snippets.
    """
    if not search_data or not search_data.get("results"):
        return "No search results found."

    parts = []
    if search_data.get("answer"):
        parts.append(f"Quick Answer: {search_data['answer']}\n")

    for i, r in enumerate(search_data["results"], 1):
        parts.append(
            f"[{i}] {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:500]}...\n"
            f"Relevance: {r['score']:.2f}\n"
        )

    return "\n".join(parts)


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    from src.config import validate_config

    print("Testing search_tools...\n")
    validate_config()

    query = "What is LangGraph?"
    print(f"Searching: {query}\n")

    data = search_web(query, max_results=3)
    print(f"Quick Answer: {data['answer']}\n")
    print(f"Found {len(data['results'])} results:\n")
    print(format_search_results(data))
