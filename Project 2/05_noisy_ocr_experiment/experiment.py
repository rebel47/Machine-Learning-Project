from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

COURSE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COURSE_ROOT))

from common.degradation import apply_degradation
from common.metrics import cer
from common.ocr import recognize
from common.preprocessing import clean_document, read_image
from common.sample_documents import make_ocr_demo


DEGRADATIONS = ("blur", "noise", "rotation", "low_contrast", "occlusion")


def plot_results(rows: list[dict], destination: Path) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
    for axis, method in zip(axes, ("raw", "preprocessed")):
        for kind in DEGRADATIONS:
            subset = [row for row in rows if row["method"] == method and row["degradation"] == kind]
            levels = sorted({float(row["severity"]) for row in subset})
            means = [np.mean([float(row["cer"]) for row in subset if float(row["severity"]) == level])
                     for level in levels]
            axis.plot(levels, means, marker="o", label=kind)
        axis.set(title=method.title(), xlabel="Severity", ylabel="Mean CER", ylim=(0, None))
        axis.grid(alpha=0.3)
    axes[1].legend(fontsize=8)
    figure.tight_layout()
    figure.savefig(destination, dpi=150)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure OCR robustness under degradation.")
    parser.add_argument("--data", type=Path)
    parser.add_argument("--make-demo", action="store_true")
    parser.add_argument("--output", type=Path, default=COURSE_ROOT / "outputs" / "05_robustness")
    parser.add_argument("--levels", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--language", default="eng")
    parser.add_argument("--psm", type=int, default=6)
    args = parser.parse_args()
    if args.levels < 1:
        parser.error("--levels must be at least 1")
    data = args.data
    if args.make_demo:
        data = COURSE_ROOT / "05_noisy_ocr_experiment" / "demo_data"
        make_ocr_demo(data)
    if data is None:
        parser.error("provide --data or use --make-demo")
    supported = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}
    image_paths = sorted(path for path in (data / "images").iterdir()
                         if path.is_file() and path.suffix.lower() in supported)
    if not image_paths:
        parser.error(f"no images found in {data / 'images'}")
    args.output.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    severities = np.linspace(0.2, 1.0, args.levels)
    for image_index, image_path in enumerate(image_paths):
        truth_path = data / "ground_truth" / f"{image_path.stem}.txt"
        if not truth_path.exists():
            raise FileNotFoundError(f"Missing ground truth: {truth_path}")
        truth = truth_path.read_text(encoding="utf-8")
        image = read_image(image_path)
        for kind in DEGRADATIONS:
            for severity in severities:
                damaged = apply_degradation(image, kind, float(severity), args.seed + image_index)
                name = f"{image_path.stem}_{kind}_{severity:.2f}"
                cv2.imwrite(str(args.output / f"{name}.png"), damaged)
                cleaned, _, _ = clean_document(damaged)
                for method, candidate in (("raw", damaged), ("preprocessed", cleaned)):
                    hypothesis = recognize(candidate, args.language, args.psm)
                    score = cer(truth, hypothesis, normalize=True)
                    rows.append({"document": image_path.stem, "degradation": kind,
                                 "severity": f"{severity:.2f}", "method": method,
                                 "cer": f"{score.rate:.6f}", "ocr_text": hypothesis})
                print(f"finished {name}")
    csv_path = args.output / "results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    plot_results(rows, args.output / "cer_plot.png")
    print(f"\nSaved {len(rows)} measurements to {csv_path}")


if __name__ == "__main__":
    main()
