# 01 — Document Cleanup and OCR

## Goal

Observe how image preprocessing changes both pixels and recognized text. The
pipeline is deliberately explicit:

`color image → grayscale → denoise → binarize → deskew → Tesseract`

## Run

From the `Project 2` directory:

```bash
python 01_document_cleanup_ocr/run.py --make-demo
```

Or process your own page:

```bash
python 01_document_cleanup_ocr/run.py path/to/page.jpg --threshold adaptive
```

Outputs include every intermediate image under `outputs/01_cleanup/stages` and
method-specific text under `raw` and `preprocessed`. Try `--no-deskew`,
`--threshold otsu`, and `--threshold adaptive`.

Evaluate the demo outputs in project 2:

```bash
python 02_ocr_evaluation/evaluate.py \
  --ground-truth outputs/demo_documents/ground_truth \
  --predictions raw=outputs/01_cleanup/raw clean=outputs/01_cleanup/preprocessed \
  --normalize
```

## What each operation does

- **Grayscale** reduces three color channels to intensity. Text recognition
  usually needs contrast more than color.
- **Denoising** suppresses isolated pixel variation, but too much blurs thin
  strokes and punctuation.
- **Binarization** separates foreground from background. Otsu chooses one global
  threshold; adaptive thresholding chooses a local threshold and often handles
  uneven lighting better.
- **Deskewing** estimates the dominant orientation of foreground pixels and
  rotates the page. Large layout elements can confuse this simple estimator.
- **Perspective correction** maps a photographed quadrilateral to a rectangle.
  `common.preprocessing.four_point_transform` implements it when corners are known.

## Questions and exercises

1. Photograph a page under uneven light. Which threshold works best, and why?
2. Increase denoising. Which characters disappear first?
3. Compare `--psm 6` (one text block) with `--psm 3` (automatic layout).
4. Find one case where preprocessing makes OCR worse. Keep it as a failure case.

## Explain it in an interview

“Preprocessing changes the input distribution seen by the recognizer. It can
remove nuisance variation such as skew and background texture, but aggressive
thresholding can remove dots, accents, and thin strokes. Therefore I compare OCR
before and after preprocessing with CER/WER rather than judging the image by eye.”
