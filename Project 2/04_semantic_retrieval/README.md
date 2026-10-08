# 04 — Semantic Document Retrieval

## What you will learn

You will turn a small document collection into vectors, rank it for a query with
cosine similarity, compare lexical TF-IDF with dense embeddings, and evaluate
retrieval with Recall@k and reciprocal rank.

## Folder contents

```text
data/documents/*.txt  small searchable corpus
data/imageTextN.png   example source document image
data/source.txt       image source information
output/               rankings.csv and similarity plot
project.ipynb         complete guided experiment
```

The TF-IDF lesson works with the base environment. For Sentence Transformers:

```bash
python -m pip install -r requirements-embeddings.txt
```

## Core ideas

- **TF-IDF** produces sparse lexical vectors. It is fast and interpretable but
  usually misses synonyms that share no words.
- **Dense embeddings** learn a vector space where semantically related text may
  be close even without exact token overlap.
- **Cosine similarity** compares vector direction: the dot product after length
  normalization.
- **Recall@k** asks whether a relevant result appears in the first `k` items.
  **Reciprocal rank** rewards putting the first relevant result near the top.

OCR is a retrieval bottleneck: an embedding model cannot recover text OCR omitted.
Image encoders such as CLIP can preserve layout/visual evidence, but may miss exact
numbers. Real systems often combine lexical, dense, and visual scores, then rerank.

## Check your understanding

1. Query with a synonym not present in the target text. Compare both backends.
2. Remove important words from one document to simulate OCR loss.
3. Change unigram TF-IDF to `(1, 2)` n-grams. What improves or worsens?
4. Add five labeled queries and calculate mean reciprocal rank.
5. Explain why high cosine similarity is not a calibrated probability.

## Completion criterion

You are finished when `output/rankings.csv` exists and you can explain one query
where lexical and semantic retrieval rank documents differently.
