"""Shared pytest fixtures."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def sample_search_results():
    """Mock search results for testing."""
    return {
        "answer": "LangGraph is a framework for multi-agent workflows.",
        "results": [
            {"title": "LangGraph Docs", "url": "https://example.com/1", "content": "LangGraph builds stateful graphs.", "score": 0.95},
            {"title": "LangChain Blog", "url": "https://example.com/2", "content": "LangGraph vs CrewAI.", "score": 0.88},
        ],
        "query": "what is langgraph"
    }


@pytest.fixture
def sample_sources_text():
    """Mock formatted sources for synthesizer testing."""
    return """
[Source 1]
Title: LangGraph Docs
URL: https://example.com/1
Found via query: what is langgraph
Relevance: 0.95
Summary: LangGraph is a framework for building stateful, multi-agent workflows.

---
[Source 2]
Title: LangChain Blog
URL: https://example.com/2
Found via query: langgraph vs crewai
Relevance: 0.88
Summary: CrewAI is role-based, LangGraph offers more control over state.
"""