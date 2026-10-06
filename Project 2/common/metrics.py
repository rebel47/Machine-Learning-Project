"""Transparent OCR metrics, including edit-operation counts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Sequence, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ErrorCounts:
    substitutions: int
    deletions: int
    insertions: int
    reference_length: int

    @property
    def errors(self) -> int:
        return self.substitutions + self.deletions + self.insertions

    @property
    def rate(self) -> float:
        if self.reference_length == 0:
            return 0.0 if self.errors == 0 else 1.0
        return self.errors / self.reference_length


def edit_counts(reference: Sequence[T], hypothesis: Sequence[T]) -> ErrorCounts:
    """Levenshtein distance with a deterministic S/D/I traceback."""
    rows, cols = len(reference) + 1, len(hypothesis) + 1
    cost = [[0] * cols for _ in range(rows)]
    operation = [[""] * cols for _ in range(rows)]
    for i in range(1, rows):
        cost[i][0], operation[i][0] = i, "D"
    for j in range(1, cols):
        cost[0][j], operation[0][j] = j, "I"
    for i in range(1, rows):
        for j in range(1, cols):
            if reference[i - 1] == hypothesis[j - 1]:
                cost[i][j], operation[i][j] = cost[i - 1][j - 1], "M"
            else:
                choices = [
                    (cost[i - 1][j - 1] + 1, "S"),
                    (cost[i - 1][j] + 1, "D"),
                    (cost[i][j - 1] + 1, "I"),
                ]
                cost[i][j], operation[i][j] = min(choices, key=lambda x: x[0])
    substitutions = deletions = insertions = 0
    i, j = len(reference), len(hypothesis)
    while i or j:
        op = operation[i][j]
        if op in ("M", "S"):
            substitutions += op == "S"
            i, j = i - 1, j - 1
        elif op == "D":
            deletions += 1
            i -= 1
        else:
            insertions += 1
            j -= 1
    return ErrorCounts(substitutions, deletions, insertions, len(reference))


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def cer(reference: str, hypothesis: str, normalize: bool = False) -> ErrorCounts:
    if normalize:
        reference, hypothesis = normalize_text(reference), normalize_text(hypothesis)
    return edit_counts(list(reference), list(hypothesis))


def wer(reference: str, hypothesis: str, normalize: bool = False) -> ErrorCounts:
    if normalize:
        reference, hypothesis = normalize_text(reference), normalize_text(hypothesis)
    return edit_counts(reference.split(), hypothesis.split())
