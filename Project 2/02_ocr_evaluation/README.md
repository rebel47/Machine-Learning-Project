# 02 — OCR Evaluation with CER and WER

## What you will learn

You will implement Levenshtein edit distance, recover substitution/deletion/
insertion counts, and calculate Character Error Rate (CER) and Word Error Rate
(WER) for several preprocessing configurations.

```text
error rate = (substitutions + deletions + insertions) / reference length
```

## Folder contents

```text
data/imageTextN.png    OCR input image
data/ground_truth.txt  independent reference transcription
data/source.txt        image source information
output/                OCR predictions and metrics.csv
README.md              concepts and exercises
project.ipynb          implementation and guided experiment
```

Open `project.ipynb` in Jupyter and run top to bottom. Tesseract must be installed.

## Core ideas

- A **substitution** changes a token, a **deletion** loses one, and an
  **insertion** adds one.
- CER treats characters as tokens; WER splits text into words. A single wrong
  character may make a whole word wrong, so WER is often larger.
- A rate can exceed 1.0 if the recognizer inserts more tokens than the reference
  contains.
- **Micro averaging** pools all errors and tokens, so long pages matter more.
  **Macro averaging** averages page rates, so every page has equal weight.
- Normalization choices—case, punctuation, and whitespace—change the metric.
  Always report them.

Ground truth must be checked carefully and kept separate from model development.
Do not tune preprocessing repeatedly on the final test pages.

## Check your understanding

1. Create a sentence with low CER but high WER.
2. Disable lowercase/whitespace normalization. Why does the result change?
3. Add a punctuation-removal rule. Is that fair for every application?
4. Add a second, much longer page and compare micro with macro CER.
5. Inspect the edit counts—not just the final rate. Which error dominates?

## Completion criterion

You are finished when `output/metrics.csv` compares raw, Otsu, and adaptive OCR,
and you can derive CER from the stored edit counts.
