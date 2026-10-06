"""OCR adapter with a useful error when the system executable is absent."""

from __future__ import annotations

import shutil

import numpy as np


def require_tesseract() -> None:
    if shutil.which("tesseract") is None:
        raise RuntimeError(
            "Tesseract was not found. Install it with `brew install tesseract` "
            "(macOS) or `sudo apt-get install tesseract-ocr` (Ubuntu)."
        )


def recognize(image: np.ndarray, language: str = "eng", psm: int = 6) -> str:
    require_tesseract()
    import pytesseract

    return pytesseract.image_to_string(image, lang=language, config=f"--psm {psm}").strip()
