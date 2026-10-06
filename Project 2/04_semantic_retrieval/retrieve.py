from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

COURSE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COURSE_ROOT))

from common.sample_documents import DOCUMENTS, render_document


def make_demo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    extra = {
        "travel_policy": ["TRAVEL POLICY", "Rail and hotel costs can be reimbursed.", "Keep all receipts."],
        "meeting_notes": ["MEETING NOTES", "Model review on Friday.", "Discuss OCR evaluation."],
    }
    for index, (name, lines) in enumerate({**DOCUMENTS, **extra}.items()):
        (root / f"{name}.txt").write_text("\n".join(lines), encoding="utf-8")
        render_document(lines, seed=index).save(root / f"{name}.png")


def rank_tfidf(query: str, texts: list[str]) -> np.ndarray:
    matrix = TfidfVectorizer(ngram_range=(1, 2)).fit_transform(texts + [query])
    return cosine_similarity(matrix[-1], matrix[:-1]).ravel()


def rank_sbert(query: str, texts: list[str]) -> np.ndarray:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as error:
        raise RuntimeError("Install requirements-embeddings.txt for --backend sbert") from error
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts + [query], normalize_embeddings=True)
    return embeddings[:-1] @ embeddings[-1]


def rank_clip(query: str, image_paths: list[Path]) -> np.ndarray:
    try:
        import open_clip
        import torch
    except ImportError as error:
        raise RuntimeError("Install requirements-embeddings.txt for --backend clip") from error
    model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k")
    tokenizer = open_clip.get_tokenizer("ViT-B-32")
    images = torch.stack([preprocess(Image.open(path).convert("RGB")) for path in image_paths])
    with torch.no_grad():
        image_vectors = model.encode_image(images)
        text_vector = model.encode_text(tokenizer([query]))
        image_vectors /= image_vectors.norm(dim=-1, keepdim=True)
        text_vector /= text_vector.norm(dim=-1, keepdim=True)
    return (image_vectors @ text_vector.T).squeeze(1).cpu().numpy()


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve documents by vector similarity.")
    parser.add_argument("query")
    parser.add_argument("--corpus", type=Path, default=Path(__file__).parent / "demo_corpus")
    parser.add_argument("--backend", choices=("tfidf", "sbert", "clip"), default="tfidf")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()
    if not list(args.corpus.glob("*.txt")):
        make_demo(args.corpus)
        print(f"Created demo corpus at {args.corpus}\n")
    text_paths = sorted(args.corpus.glob("*.txt"))
    texts = [path.read_text(encoding="utf-8") for path in text_paths]
    if args.backend == "tfidf":
        scores = rank_tfidf(args.query, texts)
    elif args.backend == "sbert":
        scores = rank_sbert(args.query, texts)
    else:
        image_paths = [path.with_suffix(".png") for path in text_paths]
        missing = [str(path) for path in image_paths if not path.exists()]
        if missing:
            raise FileNotFoundError(f"CLIP needs matching images; missing: {missing}")
        scores = rank_clip(args.query, image_paths)
    print(f"Query: {args.query!r}; backend={args.backend}\n")
    for rank, index in enumerate(np.argsort(scores)[::-1][:args.top_k], 1):
        preview = " ".join(texts[index].split())[:90]
        print(f"{rank}. {text_paths[index].stem:<20} score={scores[index]:.3f}  {preview}")


if __name__ == "__main__":
    main()
