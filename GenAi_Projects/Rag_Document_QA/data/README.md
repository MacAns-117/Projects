# Data

## `sample_pdfs/` (shipped)

Two public arXiv PDFs used for the retrieval eval. They are **not** a resume.

| File | Paper |
| --- | --- |
| `attention_is_all_you_need.pdf` | Vaswani et al., *Attention Is All You Need*, [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) |
| `rag_lewis_2020.pdf` | Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, [arXiv:2005.11401](https://arxiv.org/abs/2005.11401) |

Re-download:

```bash
curl -L -o data/sample_pdfs/attention_is_all_you_need.pdf https://arxiv.org/pdf/1706.03762.pdf
curl -L -o data/sample_pdfs/rag_lewis_2020.pdf https://arxiv.org/pdf/2005.11401.pdf
```

## `uploaded_pdfs/`

Runtime dumps from the Streamlit uploader. Gitignored.
