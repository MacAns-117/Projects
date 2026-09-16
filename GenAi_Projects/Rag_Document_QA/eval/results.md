# Retrieval eval

Index: **132** chunks from the two sample arXiv PDFs. top_k = **8**. 24 questions (22 in-scope, 2 out-of-scope).

Hit@k = at least one retrieved `(source, page)` is in the gold page list. Out-of-scope “refuse” = retrieval returned **no** chunks after the score floor (the LLM is then forced to say it does not know).

| Method | Hit@8 | Hits | OOS refuse |
| --- | ---: | ---: | ---: |
| `similarity` | **59.1%** | 13/22 | 0/2 (0%) |
| `mmr` | **68.2%** | 15/22 | 0/2 (0%) |
| `hybrid` | **77.3%** | 17/22 | 0/2 (0%) |

Hybrid is vector + BM25 on the same chunk list. MMR is Chroma’s `max_marginal_relevance_search`. Similarity is cosine on MiniLM.

Generation (Groq) is **not** in this table — that path needs `GROQ_API_KEY` and is checked only in the live app / `ask()`.
