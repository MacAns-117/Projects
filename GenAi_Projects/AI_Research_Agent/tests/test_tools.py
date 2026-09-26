"""Tests for search_tools, summarize_tools, and extract_tools."""
import pytest
from unittest.mock import patch, MagicMock

from src.tools.search_tools import format_search_results
from src.tools.summarize_tools import summarize_text
from src.tools.extract_tools import extract_page_content, _validate_url, ExtractResult


class TestSearchTools:
    def test_format_search_results(self, sample_search_results):
        """Test formatting search results."""
        formatted = format_search_results(sample_search_results)
        assert "LangGraph Docs" in formatted
        assert "https://example.com/1" in formatted
        assert "Quick Answer" in formatted

    def test_format_empty_results(self):
        """Test formatting empty results."""
        empty = {"answer": "", "results": [], "query": "test"}
        assert format_search_results(empty) == "No search results found."


class TestSummarizeTools:
    def test_summarize_empty_text(self):
        """Summarizing empty text returns a fallback message."""
        result = summarize_text("")
        assert "No substantial text" in result

    def test_summarize_short_text(self):
        """Summarizing very short text returns a fallback message."""
        result = summarize_text("Hi.")
        assert "No substantial text" in result


class TestExtractTools:
    def test_reject_non_http_scheme(self):
        with pytest.raises(ValueError, match="Unsupported URL scheme"):
            _validate_url("file:///etc/passwd")

    def test_reject_ftp_scheme(self):
        with pytest.raises(ValueError, match="Unsupported URL scheme"):
            _validate_url("ftp://example.com/file")

    def test_reject_localhost(self):
        with pytest.raises(ValueError, match="Blocked"):
            _validate_url("http://localhost/admin")

    def test_reject_loopback_ip(self):
        with pytest.raises(ValueError, match="Blocked"):
            _validate_url("http://127.0.0.1/")

    def test_reject_private_10(self):
        with pytest.raises(ValueError, match="Blocked"):
            _validate_url("http://10.0.0.1/")

    def test_reject_link_local(self):
        with pytest.raises(ValueError, match="Blocked"):
            _validate_url("http://169.254.169.254/latest/meta-data/")

    def test_extract_returns_structured_failure_for_bad_url(self):
        result = extract_page_content("http://127.0.0.1/")
        assert isinstance(result, ExtractResult)
        assert result.ok is False
        assert result.error
        assert result.content == ""
