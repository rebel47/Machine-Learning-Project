from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

from PIL import ImageEnhance

COURSE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COURSE_ROOT))

from common.sample_documents import DOCUMENTS, render_document


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a teaching document dataset.")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--samples-per-class", type=int, default=40)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    counts = {"train": 0.70, "val": 0.15, "test": 0.15}
    boundaries = (counts["train"], counts["train"] + counts["val"])
    for class_index, (kind, base_lines) in enumerate(DOCUMENTS.items()):
        for index in range(args.samples_per_class):
            ratio = index / args.samples_per_class
            split = "train" if ratio < boundaries[0] else "val" if ratio < boundaries[1] else "test"
            lines = list(base_lines)
            lines[-1] = f"{lines[-1]} {1000 + index}"
            image = render_document(lines, seed=args.seed + class_index * 1000 + index)
            image = image.rotate(rng.uniform(-2.5, 2.5), fillcolor="white")
            image = ImageEnhance.Contrast(image).enhance(rng.uniform(0.75, 1.15))
            destination = args.output / split / kind
            destination.mkdir(parents=True, exist_ok=True)
            image.save(destination / f"{kind}_{index:03d}.png")
    print(f"Created {len(DOCUMENTS) * args.samples_per_class} images under {args.output}")


if __name__ == "__main__":
    main()
