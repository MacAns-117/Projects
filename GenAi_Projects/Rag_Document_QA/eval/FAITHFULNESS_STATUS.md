# Faithfulness eval status

**Not run against a live LLM for this commit** (no paid API calls from automation; no local llama.cpp server was attached on the box).

To run yourself against any OpenAI-compatible endpoint:

```bash
export OPENAI_BASE_URL=http://127.0.0.1:8080/v1   # or https://api.groq.com/openai/v1
export OPENAI_API_KEY=local                        # or your Groq key
export JUDGE_MODEL=local-model                     # or openai/gpt-oss-120b
python -m eval.run_faithfulness
```

Unit tests cover the judge parsing, OOS short-circuit, and summarization with a **mocked** judge (`tests/test_faithfulness.py`).
