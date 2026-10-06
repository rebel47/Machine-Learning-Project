# 04 — Semantic Document Retrieval

## Goal

Rank documents for a query using vector similarity. This connects OCR output to a
retrieval or RAG system.

## Run

The zero-download baseline uses TF-IDF vectors:

```bash
python 04_semantic_retrieval/retrieve.py "travel reimbursement"
```

After installing `requirements-embeddings.txt`, compare a dense text encoder:

```bash
python 04_semantic_retrieval/retrieve.py "travel reimbursement" --backend sbert
```

To search rendered document images with a text query:

```bash
python 04_semantic_retrieval/retrieve.py "a receipt for coffee" --backend clip
```

The script creates a tiny demo corpus automatically. Use `--corpus path/to/txts`
for your OCR text. Matching `.png` files are needed for CLIP.

## Model ideas

- **TF-IDF** is a sparse lexical representation. It is fast and interpretable but
  usually cannot match synonyms that share no tokens.
- **Dense text embeddings** map sentences into vectors whose geometry captures
  learned semantic similarity. They cost more and inherit model/domain biases.
- **Cosine similarity** is the normalized dot product. It compares direction
  rather than raw vector magnitude.
- **CLIP** maps images and text into a shared space. It may retrieve based on
  visual layout even when OCR is poor, but fine details and exact numbers remain
  difficult.

Text-only retrieval has an OCR bottleneck: missing text cannot be recovered by a
later embedding model. Visual and multimodal representations provide complementary
signals. In production, retrieve candidates and then rerank with a stronger model.

## Evaluation and exercises

Create queries with known relevant documents and report Recall@k or MRR instead
of showing only appealing examples.

1. Query using a synonym absent from the target document. Compare TF-IDF/SBERT.
2. Corrupt OCR text and plot retrieval performance against CER.
3. Build a hybrid score: `alpha * text_similarity + (1-alpha) * image_similarity`.
4. Chunk a long document by page/section. How does chunk size affect retrieval?
