"""Tests for planner and memory (no LLM calls required)."""
import pytest
from unittest.mock import patch, MagicMock

from src.agents.planner import plan_searches
from src.memory import ConversationMemory


class TestPlanner:
    @patch('src.agents.planner.create_planner')
    def test_plan_searches(self, mock_create):
        """Test that planner returns a list of queries."""
        # Mock the LLM response
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = MagicMock(content='["query 1", "query 2", "query 3"]')
        mock_create.return_value = mock_chain

        queries = plan_searches("What is RAG?")
        assert len(queries) == 3
        assert "query 1" in queries

    @patch('src.agents.planner.create_planner')
    def test_plan_searches_fallback(self, mock_create):
        """Test fallback parsing if JSON fails."""
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = MagicMock(content='query one\nquery two\nquery three')
        mock_create.return_value = mock_chain

        queries = plan_searches("What is RAG?")
        assert len(queries) >= 1

    @patch('src.agents.planner.create_planner')
    def test_plan_searches_empty_falls_back_to_question(self, mock_create):
        """If the LLM returns unusable output, fall back to [question]."""
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = MagicMock(content='[]')
        mock_create.return_value = mock_chain

        question = "What is RAG evaluation?"
        queries = plan_searches(question)
        assert queries == [question]


class TestMemory:
    def test_add_and_retrieve(self):
        mem = ConversationMemory(max_size=5)
        mem.add_message("user", "Hello")
        assert len(mem) == 1

    def test_sliding_window(self):
        mem = ConversationMemory(max_size=2)
        mem.add_message("user", "q1")
        mem.add_message("assistant", "a1")
        mem.add_message("user", "q2")
        assert len(mem) == 2
        context = mem.get_context_string()
        assert "q1" not in context
        assert "q2" in context

    def test_clear(self):
        mem = ConversationMemory()
        mem.add_message("user", "test")
        mem.clear()
        assert len(mem) == 0
