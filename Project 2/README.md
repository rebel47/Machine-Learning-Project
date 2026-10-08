# Project 2 — Self-Learning Document Analysis Course

This course contains five independent, notebook-first projects. You can copy any
project folder elsewhere and it will still contain its lesson, input data, code,
and output location.

## Standard structure

Every project contains:

```text
project_name/
├── data/       # input images, text, and source information
├── output/     # generated images, metrics, plots, and models
├── README.md   # lesson goals, theory, instructions, and exercises
└── project.ipynb # executable lesson with explanations beside the code
```

There is intentionally no shared `common` package and no test folder. Important
functions are written inside the notebook where they are introduced. Repetition
is useful here: each module remains understandable on its own.

## Learning path

| Order | Module | What you will build |
|---:|---|---|
| 1 | [Document cleanup + OCR](01_document_cleanup_ocr/README.md) | A visible preprocessing pipeline and raw/clean OCR comparison |
| 2 | [OCR evaluation](02_ocr_evaluation/README.md) | CER/WER from edit distance, including error counts |
| 3 | [Document classifier](03_document_classifier/README.md) | Synthetic data, a CNN baseline, and ResNet transfer learning |
| 4 | [Semantic retrieval](04_semantic_retrieval/README.md) | TF-IDF and dense-embedding document search |
| 5 | [Noisy OCR experiment](05_noisy_ocr_experiment/README.md) | A controlled OCR robustness study with plots |

## Setup

From `Project 2`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

Open the notebook inside the project you want to study and run cells from top to
bottom. Projects 1, 2, and 5 also need Tesseract:

```bash
brew install tesseract                 # macOS
sudo apt-get install tesseract-ocr     # Ubuntu/Debian
```

Project 3 has an optional deep-learning install:

```bash
python -m pip install -r requirements-deep-learning.txt
```

Project 4's neural embedding extensions use:

```bash
python -m pip install -r requirements-embeddings.txt
```

## How to study

For each notebook: predict what a cell will do, run it, describe the output in
your own words, change one parameter, and record why the result changed. Finish
the exercises in the README before moving on. The goal is not only working code;
it is being able to explain the experiment and its limitations.
