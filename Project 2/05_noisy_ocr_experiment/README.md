# 05 — Noisy and Historical-Document OCR Experiment

## Research question

**Which document degradations hurt OCR most, and when does preprocessing help?**

This project turns the earlier lessons into a small controlled experiment. It
applies blur, Gaussian noise, rotation, low contrast, and occlusion at increasing
severity, then measures raw and preprocessed OCR with CER.

## Run

```bash
python 05_noisy_ocr_experiment/experiment.py --make-demo --levels 4
```

Results are saved under `outputs/05_robustness/` as degraded images, `results.csv`,
and `cer_plot.png`. Use real data with matching basenames:

```text
my_data/
├── images/page_01.png
└── ground_truth/page_01.txt
```

```bash
python 05_noisy_ocr_experiment/experiment.py --data my_data
```

## Experimental design

- **Independent variables:** degradation type/severity and preprocessing on/off.
- **Dependent variable:** CER.
- **Controls:** same source pages, OCR engine/configuration, random seed, and
  evaluation normalization.
- **Ablation:** compare raw OCR with exactly one preprocessing pipeline.

Synthetic degradation is useful because severity and ground truth are controlled,
but it is not identical to real historical damage. Validate conclusions on real
scans. Average results over multiple pages and seeds, and show variation—not only
the mean.

## How to interpret results

Look for curves and interactions, not merely the best row. Deskewing should target
rotation; thresholding may restore moderate low contrast; neither can reconstruct
text hidden by occlusion. At high noise, binarization may amplify artifacts.
Unexpected outcomes are valuable: inspect saved images and OCR text, then refine
the hypothesis.

## Extensions

1. Add stains, JPEG compression, bleed-through, and nonuniform illumination.
2. Run several random seeds and add confidence intervals.
3. Compare Tesseract with EasyOCR or a vision-language model.
4. Break CER down by digits, punctuation, and alphabetic characters.
5. Test combinations of degradations, while noting the larger experiment matrix.

## Research-style summary template

“We evaluated OCR on _n_ documents under five controlled degradations and _k_
severity levels. Rotation/blur caused the largest CER increase. Preprocessing
helped under ___ but hurt under ___, likely because ___. The key limitation is
that synthetic corruption does not reproduce the full distribution of historical
scans.”
