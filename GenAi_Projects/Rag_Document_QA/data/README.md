# Data

## `sample_pdfs/` (shipped — tiny synthetic fixtures)

Two short multi-page PDFs used by **unit tests** (`tests/test_loader.py`). They contain the key phrases the loader checks for (`Attention` / `Vaswani`, `Retrieval-Augmented`) but are **not** the full arXiv articles.

| File | Role |
| --- | --- |
| `attention_is_all_you_need.pdf` | 12-page synthetic fixture (Attention / Vaswani on page 1) |
| `rag_lewis_2020.pdf` | 16-page synthetic fixture (Retrieval-Augmented on page 1) |

The published Hit@8 numbers in `eval/results.md` were measured on the **full** public arXiv PDFs. To reproduce that eval locally, replace the fixtures with:

```bash
curl -L -o data/sample_pdfs/attention_is_all_you_need.pdf https://arxiv.org/pdf/1706.03762.pdf
curl -L -o data/sample_pdfs/rag_lewis_2020.pdf https://arxiv.org/pdf/2005.11401.pdf
python -m eval.run_eval
```

Papers: Vaswani et al., *Attention Is All You Need*, [arXiv:1706.03762](https://arxiv.org/abs/1706.03762); Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, [arXiv:2005.11401](https://arxiv.org/abs/2005.11401).

## `uploaded_pdfs/`

Runtime dumps from the Streamlit uploader. Gitignored.
