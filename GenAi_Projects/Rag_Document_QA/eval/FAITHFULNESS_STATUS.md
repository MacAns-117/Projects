# Faithfulness eval status

**The faithfulness eval has not been run for this commit.** No paid API calls are made from automation.

Wiring smoke only (27 Oct 2026, IST): llama.cpp `llama-server` build b11922 on CPU, serving Qwen3-0.6B Q8_0, with `LLM_PROVIDER=openai_compatible`. Three `ask()` calls on the arXiv eval corpus and one judge call completed, and the judge returned parseable JSON. No scores were recorded, because a 0.6B model grading its own answers is not a meaningful eval.

Generation and the judge both reuse the app's provider settings (`src/llm.py`), so one set of env vars drives the whole run.

Local llama.cpp / Ollama / LM Studio:

```bash
export LLM_PROVIDER=openai_compatible
export LLM_BASE_URL=http://localhost:8080/v1   # your server
export LLM_MODEL=my-model                      # name the server serves
python -m eval.run_faithfulness
```

Groq (default provider):

```bash
export GROQ_API_KEY=gsk_...                    # judge model defaults to LLM_MODEL / openai/gpt-oss-120b
python -m eval.run_faithfulness
```

Judge-only overrides still win when set: `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `JUDGE_MODEL`.
A Groq key is only ever sent to `api.groq.com`.

The output file records which generator and judge were used. A self-judged run (same local model generating and grading) is weaker evidence than an independent judge; say so if you quote one.

Unit tests cover the judge parsing, OOS short-circuit, summarization, and endpoint resolution with a **mocked** judge (`tests/test_faithfulness.py`, `tests/test_local_llm_wiring.py`).
