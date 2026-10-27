"""Tests for planner and memory (no LLM calls required)."""
from unittest.mock import MagicMock, patch

from src.agents.planner import parse_query_list, plan_searches
from src.memory import ConversationMemory


class TestParseQueryList:
    def test_valid_three(self):
        out = parse_query_list('["a", "b", "c"]')
        assert out == ["a", "b", "c"]

    def test_code_fenced_json(self):
        raw = '```json\n["one", "two", "three", "four"]\n```'
        assert parse_query_list(raw) == ["one", "two", "three", "four"]

    def test_string_reply_is_rejected(self):
        # Must NOT become a list of characters.
        assert parse_query_list('"LangGraph vs CrewAI"') is None

    def test_too_few(self):
        assert parse_query_list('["only", "two"]') is None

    def test_too_many(self):
        assert parse_query_list('["a","b","c","d","e","f"]') is None

    def test_non_string_items(self):
        assert parse_query_list('[1, 2, 3]') is None
        assert parse_query_list('[{"q": "x"}, "b", "c"]') is None

    def test_empty_string_item(self):
        assert parse_query_list('["ok", "", "also"]') is None

    def test_garbage(self):
        assert parse_query_list("not json at all") is None
        assert parse_query_list("") is None
        assert parse_query_list('{"queries": ["a","b","c"]}') is None


class TestPlanner:
    @patch("src.agents.planner.create_planner")
    def test_plan_searches(self, mock_create):
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = MagicMock(
            content='["query 1", "query 2", "query 3"]'
        )
        mock_create.return_value = mock_chain

        queries = plan_searches("What is RAG?")
        assert len(queries) == 3
        assert "query 1" in queries

    @patch("src.agents.planner.create_planner")
    def test_fenced_reply(self, mock_create):
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = MagicMock(
            content='```json\n["alpha", "beta", "gamma"]\n```'
        )
        mock_create.return_value = mock_chain
        assert plan_searches("q") == ["alpha", "beta", "gamma"]

    @patch("src.agents.planner.create_planner")
    def test_string_reply_falls_back_after_retry(self, mock_create):
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = MagicMock(content='"LangGraph vs CrewAI"')
        mock_create.return_value = mock_chain
        question = "What is RAG?"
        queries = plan_searches(question)
        assert queries == [question]
        assert mock_chain.invoke.call_count == 2

    @patch("src.agents.planner.create_planner")
    def test_retry_then_success(self, mock_create):
        mock_chain = MagicMock()
        mock_chain.invoke.side_effect = [
            MagicMock(content="garbage"),
            MagicMock(content='["a", "b", "c"]'),
        ]
        mock_create.return_value = mock_chain
        assert plan_searches("q") == ["a", "b", "c"]
        assert mock_chain.invoke.call_count == 2

    @patch("src.agents.planner.create_planner")
    def test_newline_text_falls_back_to_question(self, mock_create):
        """Non-JSON line lists are no longer accepted — fall back to [question]."""
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = MagicMock(
            content="query one\nquery two\nquery three"
        )
        mock_create.return_value = mock_chain
        question = "What is RAG?"
        assert plan_searches(question) == [question]

    @patch("src.agents.planner.create_planner")
    def test_empty_list_falls_back_to_question(self, mock_create):
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = MagicMock(content="[]")
        mock_create.return_value = mock_chain
        question = "What is RAG evaluation?"
        assert plan_searches(question) == [question]


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
