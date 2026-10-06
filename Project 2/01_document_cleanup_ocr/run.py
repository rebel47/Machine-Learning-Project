from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2

COURSE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COURSE_ROOT))

from common.ocr import recognize
from common.preprocessing import clean_document, read_image
from common.sample_documents import make_ocr_demo


def process(path: Path, output_root: Path, threshold: str, do_deskew: bool,
            language: str, psm: int) -> None:
    image = read_image(path)
    cleaned, stages, angle = clean_document(image, threshold, do_deskew)
    destination = output_root / "stages" / path.stem
    destination.mkdir(parents=True, exist_ok=True)
    for name, stage in stages.items():
        cv2.imwrite(str(destination / f"{name}.png"), stage)
    raw_text = recognize(image, language, psm)
    clean_text = recognize(cleaned, language, psm)
    raw_dir, clean_dir = output_root / "raw", output_root / "preprocessed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    clean_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / f"{path.stem}.txt").write_text(raw_text, encoding="utf-8")
    (clean_dir / f"{path.stem}.txt").write_text(clean_text, encoding="utf-8")
    print(f"\n{path.name}: deskew angle={angle:.2f}°")
    print("RAW OCR:\n", raw_text)
    print("PREPROCESSED OCR:\n", clean_text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare raw and preprocessed OCR.")
    parser.add_argument("images", nargs="*", type=Path)
    parser.add_argument("--make-demo", action="store_true")
    parser.add_argument("--output", type=Path, default=COURSE_ROOT / "outputs" / "01_cleanup")
    parser.add_argument("--threshold", choices=("otsu", "adaptive"), default="otsu")
    parser.add_argument("--no-deskew", action="store_true")
    parser.add_argument("--language", default="eng")
    parser.add_argument("--psm", type=int, default=6)
    args = parser.parse_args()
    images = list(args.images)
    if args.make_demo:
        images += make_ocr_demo(COURSE_ROOT / "outputs" / "demo_documents")
    if not images:
        parser.error("provide image paths or use --make-demo")
    for image in images:
        process(image, args.output, args.threshold, not args.no_deskew, args.language, args.psm)


if __name__ == "__main__":
    main()
