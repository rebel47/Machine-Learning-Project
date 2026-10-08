# 05 — Noisy and Historical-Document OCR Experiment

## Research question

**Which types of document degradation hurt OCR most, and when does preprocessing
help?**

You will add controlled blur, noise, rotation, low contrast, and occlusion to a
real text image. For every degradation and severity, the notebook compares raw
OCR with an Otsu/deskew preprocessing pipeline using CER.

## Folder contents

```text
data/imageTextN.png    clean source image
data/ground_truth.txt  reference transcription
data/source.txt        image source information
output/degraded/       generated corrupted images
output/results.csv     measurements
output/cer_plot.png    robustness curves
project.ipynb          complete research-style experiment
```

Open `project.ipynb` in Jupyter and run top to bottom. Tesseract must be installed.

## Experimental design

- **Independent variables:** degradation type, severity, and preprocessing.
- **Dependent variable:** normalized CER.
- **Controls:** source page, OCR settings, random seed, and normalization.
- **Ablation:** raw OCR versus exactly one fixed preprocessing pipeline.

Synthetic damage offers controlled severity and perfect ground truth, but it does
not reproduce all properties of historical scans. A sound conclusion must be
validated on multiple real pages and random seeds, with uncertainty—not only a
mean curve.

Deskewing should target rotation; thresholding may recover moderate low contrast;
neither can reconstruct occluded text. At high noise, binarization may amplify
artifacts. Inspect the saved images and OCR text whenever a number surprises you.

## Check your understanding

1. Predict the most damaging degradation before running the notebook.
2. Explain one case where preprocessing makes the result worse.
3. Add JPEG compression, stains, or bleed-through.
4. Repeat across random seeds and add error bars.
5. Break CER down into digits, punctuation, and alphabetic characters.

## Completion criterion

You are finished when you can summarize the method, result, limitation, and next
experiment in four sentences, supported by `results.csv` and `cer_plot.png`.
