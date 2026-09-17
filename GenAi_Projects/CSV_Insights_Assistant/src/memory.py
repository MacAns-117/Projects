"""Sliding window of past turns. Follow-ups are prepended as text, not a vector store."""

from __future__ import annotations

from collections import deque

from src.config import MEMORY_WINDOW


class ConversationMemory:
    def __init__(self, max_size: int = MEMORY_WINDOW):
        self.history: deque[tuple[str, str]] = deque(maxlen=max_size)
        self.max_size = max_size

    def add_message(self, role: str, content: str) -> None:
        self.history.append((role, content))

    def get_context_string(self) -> str:
        if not self.history:
            return ""
        lines = []
        for role, content in self.history:
            label = "User" if role == "user" else "Assistant"
            lines.append(f"{label}: {content}")
        return "\n".join(lines)

    def get_recent_questions(self, n: int = 1) -> list[str]:
        questions = [c for role, c in self.history if role == "user"]
        return questions[-n:] if questions else []

    def clear(self) -> None:
        self.history.clear()

    def __len__(self) -> int:
        return len(self.history)
