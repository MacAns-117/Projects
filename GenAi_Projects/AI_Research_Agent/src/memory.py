"""
Memory module — conversation history for follow-up questions on research reports.

Maintains a sliding window of past messages so the user can ask
follow-up questions on a completed report.
"""

from __future__ import annotations
from collections import deque
from typing import Optional

from src.config import MEMORY_WINDOW


class ConversationMemory:
    """Manages conversation history with a sliding window."""

    def __init__(self, max_size: int = MEMORY_WINDOW):
        self.history: deque = deque(maxlen=max_size)
        self.max_size = max_size

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.history.append((role, content))

    def get_context_string(self) -> str:
        """Format the conversation history as a context string for the LLM."""
        if not self.history:
            return ""

        lines = []
        for role, content in self.history:
            if role == "user":
                lines.append(f"User: {content}")
            else:
                lines.append(f"Assistant: {content}")

        return "\n".join(lines)

    def get_recent_questions(self, n: int = 1) -> list[str]:
        """Get the last N user questions."""
        questions = [content for role, content in self.history if role == "user"]
        return questions[-n:] if questions else []

    def clear(self) -> None:
        """Clear all conversation history."""
        self.history.clear()

    def __len__(self) -> int:
        return len(self.history)


# Module-level singleton
_global_memory: Optional[ConversationMemory] = None


def get_memory() -> ConversationMemory:
    """Get the global conversation memory instance."""
    global _global_memory
    if _global_memory is None:
        _global_memory = ConversationMemory()
    return _global_memory


def reset_memory() -> None:
    """Reset the global conversation memory."""
    global _global_memory
    _global_memory = None


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    print("Testing memory module...\n")

    mem = ConversationMemory(max_size=5)
    mem.add_message("user", "What are the latest advances in RAG evaluation?")
    mem.add_message("assistant", "## Research Report\n\nSummary: RAG evaluation uses metrics like Hit@K and RAGAS...")

    print("Context string:")
    print(mem.get_context_string())

    print(f"\nRecent questions: {mem.get_recent_questions()}")
    print("\n✓ Memory module test complete.")