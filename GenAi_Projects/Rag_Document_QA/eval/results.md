# Retrieval eval

**Run:** 2026-10-27T13:52:50.793327+05:30 (Asia/Calcutta)

Index: **132** chunks from `arxiv_full` (`/workspace/gh/Projects/GenAi_Projects/Rag_Document_QA/data/arxiv_pdfs`). top_k = **8**. 24 questions (22 in-scope, 2 out-of-scope).

Setup: `corpus=arxiv_full; MiniLM embeddings; hybrid weight 0.6; score_floor=0.22; min_top_score=0.32; ce_min_score=-9.0; rerank=cross-encoder/ms-marco-MiniLM-L-6-v2 candidates=20→8; device=cpu`

Hit@k = at least one retrieved `(source, page)` is in the gold page list. MRR = mean reciprocal rank of the first gold-page hit (in-scope only). Out-of-scope “refuse” = retrieval returned **no** chunks after the score floor / min_top_score=0.32 (no-rerank) and, when reranking, the cross-encoder logit floor (see config CE_MIN_SCORE).

| Method | Hit@8 | MRR | Hits | OOS refuse | Rerank |
| --- | ---: | ---: | ---: | ---: | --- |
| `similarity` | **68.2%** | **0.406** | 15/22 | 0/2 (0%) | no |
| `similarity+rerank` | **72.7%** | **0.499** | 16/22 | 2/2 (100%) | yes |
| `mmr` | **68.2%** | **0.411** | 15/22 | 0/2 (0%) | no |
| `mmr+rerank` | **68.2%** | **0.534** | 15/22 | 2/2 (100%) | yes |
| `hybrid` | **77.3%** | **0.412** | 17/22 | 0/2 (0%) | no |
| `hybrid+rerank` | **77.3%** | **0.524** | 17/22 | 2/2 (100%) | yes |

Hybrid is vector + BM25 on the same chunk list. MMR is Chroma’s `max_marginal_relevance_search`. Similarity is cosine on MiniLM. `*+rerank` re-scores the top 20 candidates with `cross-encoder/ms-marco-MiniLM-L-6-v2` and keeps top_k.

Generation faithfulness is a separate script: `python -m eval.run_faithfulness` (needs an OpenAI-compatible endpoint; not run in CI).
