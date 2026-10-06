"""Generate small synthetic documents so every lab has a reproducible start."""

from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


DOCUMENTS = {
    "invoice": ["INVOICE #1042", "Total due: EUR 249.00", "Payment terms: 14 days"],
    "letter": ["Dear Dr. Miller,", "Thank you for your recent letter.", "Sincerely, Ada"],
    "receipt": ["CORNER MARKET", "Coffee     3.50", "TOTAL      3.50"],
    "form": ["REGISTRATION FORM", "Name: Alex Morgan", "Member ID: 1734"],
}


def font(size: int = 30) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def render_document(lines: list[str], seed: int = 0, size: tuple[int, int] = (900, 600)) -> Image.Image:
    rng = random.Random(seed)
    image = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((35, 35, size[0] - 35, size[1] - 35), outline=(190, 190, 190), width=2)
    y = 85
    for index, line in enumerate(lines):
        text_font = font(38 if index == 0 else 29)
        draw.text((75 + rng.randint(-3, 3), y), line, fill="black", font=text_font)
        y += 90 if index == 0 else 62
    return image


def make_ocr_demo(output_dir: Path) -> list[Path]:
    image_dir, truth_dir = output_dir / "images", output_dir / "ground_truth"
    image_dir.mkdir(parents=True, exist_ok=True)
    truth_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for index, (kind, lines) in enumerate(DOCUMENTS.items()):
        path = image_dir / f"{kind}.png"
        render_document(lines, seed=index).save(path)
        (truth_dir / f"{kind}.txt").write_text("\n".join(lines), encoding="utf-8")
        paths.append(path)
    return paths
