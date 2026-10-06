# 02 — OCR Evaluation with CER and WER

## Goal

Measure OCR quality instead of relying on visual impressions.

For a reference sequence of length `N`:

`error rate = (substitutions + deletions + insertions) / N`

CER treats characters as tokens. WER treats whitespace-separated words as
tokens. A rate can exceed 1.0 when a system inserts more tokens than the
reference contains.

## Run

```bash
python 02_ocr_evaluation/evaluate.py
```

This built-in example compares two fictional OCR configurations. For your own
files, give directories containing matching `.txt` filenames:

```bash
python 02_ocr_evaluation/evaluate.py \
  --ground-truth data/ground_truth \
  --predictions raw=outputs/raw clean=outputs/clean \
  --normalize
```

## Reading the output

- **Micro average:** sum all errors and divide by all reference tokens. Long
  documents have more influence.
- **Macro average:** calculate each document's rate and average the rates. Every
  document has equal influence.
- **CER vs WER:** one wrong character may corrupt an entire word, so WER is often
  much higher. CER provides more diagnostic resolution.
- **Normalization:** lowercasing and collapsing whitespace can be appropriate if
  case/layout is irrelevant. State the normalization policy with every result.

## Good evaluation practice

Ground truth should be created independently and checked carefully. Fix the test
set before selecting preprocessing settings. Report sample count, language,
normalization, aggregation, and uncertainty or per-document variation. Inspect
error examples: one number cannot explain the failure mode.

## Exercises

1. Add punctuation removal to normalization. Is that fair for your use case?
2. Construct a case where CER is low but WER is high.
3. Compare micro and macro CER when one page is much longer than the others.
4. Evaluate raw and cleaned text produced by project 1.
