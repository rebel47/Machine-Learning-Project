# 01 — Document Cleanup and OCR

## What you will learn

You will turn a scanned text image into grayscale, remove noise, create a binary
image, estimate skew, and compare Tesseract OCR before and after preprocessing.
Every stage is displayed before it is saved, so you can connect the code to the
pixel-level result.

## Folder contents

```text
data/imageTextN.png    real text image from the OpenCV sample repository
data/ground_truth.txt  manual reference transcription
data/source.txt        download URL and license note
output/                generated stage images and OCR text
project.ipynb          complete executable lesson
```

## Start the lesson

From the `Project 2` folder, activate the environment and launch Jupyter:

```bash
source .venv/bin/activate
jupyter lab
```

Open `01_document_cleanup_ocr/project.ipynb` and run cells in order.

## Core ideas

- **Grayscale** reduces RGB color to one intensity channel. Printed OCR usually
  depends more on foreground/background contrast than color.
- **Denoising** removes small intensity changes. Too much smoothing also removes
  thin strokes, punctuation, and accents.
- **Binarization** assigns pixels to foreground or background. Otsu finds one
  global threshold; adaptive thresholding handles uneven local illumination.
- **Deskewing** estimates the dominant text angle and rotates the page back.
- **OCR** is normally detection → recognition → post-processing. Tesseract's page
  segmentation mode tells it what layout to expect.

Preprocessing is not automatically helpful. A visually clean thresholded image
may have lost information needed by the recognizer. Compare text with CER/WER in
project 2 rather than judging only by appearance.

## Check your understanding

1. Why can adaptive thresholding outperform Otsu under uneven lighting?
2. What character features might disappear after aggressive denoising?
3. Change Tesseract from page segmentation mode 6 to 3. What changes?
4. Rotate the input by 5 degrees and verify whether deskewing recovers it.
5. Find a preprocessing setting that makes OCR worse and explain why.

## Completion criterion

You are finished when `output/` contains the intermediate images and both OCR
texts, and you can explain why each transformation might help or hurt.
