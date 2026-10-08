# 03 — Document Classification and Transfer Learning

## What you will learn

You will generate a small labeled dataset of invoices, letters, receipts, and
forms; train a compact CNN; then prepare a pretrained ResNet-18 for the same task.
The notebook covers data splitting, augmentation, cross-entropy, overfitting,
precision/recall/F1, and confusion matrices.

## Folder contents

```text
data/imageTextN.png  real document image for inspection
data/source.txt      image source information
data/generated/      labeled train/validation/test images made by the notebook
output/              model checkpoint, learning curves, and confusion matrix
project.ipynb        complete guided experiment
```

Install the optional deep-learning dependencies, then open the notebook:

```bash
python -m pip install -r requirements-deep-learning.txt
jupyter lab
```

## Core ideas

- A **convolution** applies shared local filters across the image. Early layers
  learn edges/textures; later layers combine them into larger patterns.
- **Pooling** or strided convolution reduces spatial size and increases the
  receptive field.
- **Transfer learning** reuses visual features learned on a large dataset.
  Freezing the backbone is cheaper and often safer with little data; fine-tuning
  adapts it more strongly but can overfit.
- **Cross-entropy** penalizes low probability on the correct class.
- **Augmentation** changes only training images to simulate plausible variation.
- Precision measures positive-prediction correctness; recall measures coverage;
  F1 is their harmonic mean.

The generated dataset teaches the workflow but cannot support a real scientific
claim. Real projects should use varied sources such as RVL-CDIP and split by
template/customer to avoid near-duplicate leakage.

## Check your understanding

1. Compare the small CNN with frozen and fine-tuned ResNet-18.
2. Remove augmentation and observe the train/validation gap.
3. Make one class rare. Compare accuracy with macro F1.
4. Explain every cell in the confusion matrix.
5. Why should the test split be used only after model choices are complete?

## Completion criterion

You are finished when you can explain the full training/evaluation loop and can
diagnose whether a performance gap is underfitting, overfitting, or data leakage.
