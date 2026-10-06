"""Small, explicit OpenCV preprocessing operations for document images."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import cv2
import numpy as np


def read_image(path: Path | str) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return image


def to_grayscale(image: np.ndarray) -> np.ndarray:
    return image if image.ndim == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def denoise(gray: np.ndarray) -> np.ndarray:
    """Remove small noise while preserving character edges."""
    return cv2.bilateralFilter(gray, d=7, sigmaColor=35, sigmaSpace=35)


def binarize(gray: np.ndarray, method: str = "otsu") -> np.ndarray:
    if method == "otsu":
        return cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    if method == "adaptive":
        return cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 31, 15,
        )
    raise ValueError("method must be 'otsu' or 'adaptive'")


def estimate_skew(binary: np.ndarray) -> float:
    """Estimate text skew in degrees from foreground pixel coordinates."""
    foreground = np.column_stack(np.where(binary < 128))
    if len(foreground) < 20:
        return 0.0
    angle = cv2.minAreaRect(foreground[:, ::-1].astype(np.float32))[-1]
    return -(90 + angle) if angle < -45 else -angle


def rotate(image: np.ndarray, angle: float) -> np.ndarray:
    height, width = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1.0)
    return cv2.warpAffine(
        image, matrix, (width, height), flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT, borderValue=255,
    )


def deskew(binary: np.ndarray) -> tuple[np.ndarray, float]:
    angle = estimate_skew(binary)
    return rotate(binary, angle), angle


def clean_document(
    image: np.ndarray, threshold: str = "otsu", do_deskew: bool = True
) -> tuple[np.ndarray, Dict[str, np.ndarray], float]:
    """Return final image, intermediate stages, and applied deskew angle."""
    gray = to_grayscale(image)
    smooth = denoise(gray)
    binary = binarize(smooth, threshold)
    final, angle = deskew(binary) if do_deskew else (binary, 0.0)
    stages = {"01_gray": gray, "02_denoised": smooth, "03_binary": binary,
              "04_deskewed": final}
    return final, stages, angle


def four_point_transform(image: np.ndarray, points: np.ndarray) -> np.ndarray:
    """Rectify a page from four corner points in any order."""
    pts = np.asarray(points, dtype=np.float32)
    if pts.shape != (4, 2):
        raise ValueError("points must have shape (4, 2)")
    ordered = np.zeros((4, 2), dtype=np.float32)
    sums, diffs = pts.sum(axis=1), np.diff(pts, axis=1).ravel()
    ordered[0], ordered[2] = pts[np.argmin(sums)], pts[np.argmax(sums)]
    ordered[1], ordered[3] = pts[np.argmin(diffs)], pts[np.argmax(diffs)]
    top_left, top_right, bottom_right, bottom_left = ordered
    width = int(max(np.linalg.norm(bottom_right - bottom_left),
                    np.linalg.norm(top_right - top_left)))
    height = int(max(np.linalg.norm(top_right - bottom_right),
                     np.linalg.norm(top_left - bottom_left)))
    destination = np.array(
        [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
        dtype=np.float32,
    )
    matrix = cv2.getPerspectiveTransform(ordered, destination)
    return cv2.warpPerspective(image, matrix, (width, height))
