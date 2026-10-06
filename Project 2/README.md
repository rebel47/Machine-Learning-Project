# Project 2 — Document Analysis Crash Course

This folder is a hands-on course made of five small projects. Each project has a
question, a runnable experiment, an explanation of the important ideas, and
exercises. Work through them in order; projects 1, 2, and 5 form one complete OCR
robustness study.

## Course map

| Project | Research question | Main concepts | Typical time |
|---|---|---|---:|
| [01 — Cleanup + OCR](01_document_cleanup_ocr/README.md) | When does preprocessing improve OCR? | pixels, thresholding, morphology, deskewing, OCR stages | 2–3 h |
| [02 — OCR evaluation](02_ocr_evaluation/README.md) | How should recognition errors be measured? | edit distance, CER, WER, micro vs macro averages | 2 h |
| [03 — Classification](03_document_classifier/README.md) | Can visual appearance identify document type? | CNNs, transfer learning, splits, augmentation, F1 | 3–5 h |
| [04 — Retrieval](04_semantic_retrieval/README.md) | Which documents answer a natural-language query? | embeddings, cosine similarity, OCR bottlenecks, CLIP | 3–4 h |
| [05 — Robustness](05_noisy_ocr_experiment/README.md) | Which degradation hurts OCR most? | controlled experiments, noise, ablations, plotting | 3–5 h |

## Setup

Use Python 3.9 or newer. From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Tesseract is a system program, not a Python package:

```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr
```

Only project 3 needs the large deep-learning install:

```bash
python -m pip install -r requirements-deep-learning.txt
```

For Sentence Transformers and CLIP in project 4:

```bash
python -m pip install -r requirements-embeddings.txt
```

## Fast learning path

Run these from `Project 2`:

```bash
python 01_document_cleanup_ocr/run.py --make-demo
python 02_ocr_evaluation/evaluate.py
python 03_document_classifier/make_dataset.py --samples-per-class 20
python 03_document_classifier/train.py --model small_cnn --epochs 2
python 04_semantic_retrieval/retrieve.py "travel reimbursement"
python 05_noisy_ocr_experiment/experiment.py --make-demo --levels 3
python -m unittest discover -s tests -v
```

The first and fifth commands require Tesseract for recognition. Project 2 uses
built-in sample predictions, and project 4 defaults to local TF-IDF, so both run
without external models.

## Concepts you should be able to explain

- **OCR is a pipeline:** text detection finds regions, recognition maps pixels to
  characters, and post-processing applies language or domain knowledge.
- **OCR is not document understanding:** reading `€1,249.00` does not identify it
  as the invoice total. Layout analysis and information extraction are separate.
- **CNN:** local shared filters learn edges, textures, and progressively larger
  patterns. Pooling or strided convolutions reduce spatial resolution.
- **Vision Transformer:** an image is divided into patches, projected into tokens,
  and processed with self-attention. It can connect distant regions directly.
- **Transfer learning:** reuse representations learned on a large dataset, replace
  the task head, then freeze or fine-tune the backbone.
- **Classification / detection / segmentation:** one label per image / boxes around
  objects / one label per pixel.
- **Precision / recall / F1:** correctness of positive predictions / coverage of
  actual positives / their harmonic mean.
- **Splits:** train fits parameters, validation selects settings, test estimates
  final generalization. Never tune repeatedly on the test set.
- **Overfitting:** training performance improves while validation performance
  stalls or worsens. More data, augmentation, regularization, or a smaller model
  can help.

## Recommended study order

If you have one day, complete 01, 02, and 05. If you have two days, add 03 and
04. For every result, write down a hypothesis before running the experiment and
then explain any surprising failure cases. That habit matters more than obtaining
a perfect metric.
