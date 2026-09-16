from src.chain import SYSTEM_PROMPT


def test_prompt_has_seven_rules_and_dont_know():
    assert "I don't know based on the provided context." in SYSTEM_PROMPT
    for n in range(1, 8):
        assert f"{n}." in SYSTEM_PROMPT
    assert "{context}" in SYSTEM_PROMPT
    assert "{question}" in SYSTEM_PROMPT
