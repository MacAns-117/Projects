import json

from src.config import DEFAULT_TOP_K, GOLD_QA_PATH, LLM_MODEL, MAX_PDFS


def test_gold_file_shape():
    gold = json.loads(GOLD_QA_PATH.read_text(encoding="utf-8"))
    qs = gold["questions"]
    assert len(qs) == 24
    assert sum(1 for q in qs if q["out_of_scope"]) == 2
    for q in qs:
        assert q["question"]
        if not q["out_of_scope"]:
            assert q["gold_pages"]


def test_config_matches_readme_numbers():
    assert DEFAULT_TOP_K == 8
    assert MAX_PDFS == 10
    assert LLM_MODEL == "openai/gpt-oss-120b"
