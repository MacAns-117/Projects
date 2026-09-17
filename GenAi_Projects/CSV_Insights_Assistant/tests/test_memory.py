from src.memory import ConversationMemory


def test_add_and_len():
    mem = ConversationMemory(max_size=5)
    mem.add_message("user", "Hello")
    mem.add_message("assistant", "Hi")
    assert len(mem) == 2


def test_context_string():
    mem = ConversationMemory()
    mem.add_message("user", "What is ADR?")
    mem.add_message("assistant", "Average daily rate.")
    ctx = mem.get_context_string()
    assert "User: What is ADR?" in ctx
    assert "Assistant: Average daily rate." in ctx


def test_empty():
    mem = ConversationMemory()
    assert mem.get_context_string() == ""
    assert mem.get_recent_questions() == []


def test_window():
    mem = ConversationMemory(max_size=3)
    mem.add_message("user", "q1")
    mem.add_message("assistant", "a1")
    mem.add_message("user", "q2")
    mem.add_message("assistant", "a2")
    assert "q1" not in mem.get_context_string()
    assert "q2" in mem.get_context_string()


def test_clear():
    mem = ConversationMemory()
    mem.add_message("user", "x")
    mem.clear()
    assert len(mem) == 0
