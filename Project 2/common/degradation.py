"""Controlled synthetic degradation operators."""

from __future__ import annotations

import cv2
import numpy as np


def apply_degradation(image: np.ndarray, kind: str, severity: float, seed: int = 42) -> np.ndarray:
    severity = float(np.clip(severity, 0.0, 1.0))
    rng = np.random.default_rng(seed)
    if kind == "blur":
        kernel = 1 + 2 * max(1, round(severity * 4))
        return cv2.GaussianBlur(image, (kernel, kernel), 0)
    if kind == "noise":
        noise = rng.normal(0, 45 * severity, image.shape)
        return np.clip(image.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    if kind == "rotation":
        from .preprocessing import rotate
        return rotate(image, 12 * severity)
    if kind == "low_contrast":
        return np.clip(128 + (image.astype(np.float32) - 128) * (1 - 0.8 * severity), 0, 255).astype(np.uint8)
    if kind == "occlusion":
        result = image.copy()
        height, width = result.shape[:2]
        box_width = max(1, int(width * 0.45 * severity))
        cv2.rectangle(result, (width // 3, height // 3),
                      (min(width - 1, width // 3 + box_width), height // 3 + 45),
                      (235, 235, 235), -1)
        return result
    raise ValueError(f"Unknown degradation: {kind}")
