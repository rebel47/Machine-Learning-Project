# 03 — Document Classification with Transfer Learning

## Goal

Classify an entire page as an invoice, letter, receipt, or form. This is visual
classification: the model can exploit layout, typography, and texture without
understanding every word.

## Prepare and run

Install `requirements-deep-learning.txt`, then create a small synthetic dataset:

```bash
python 03_document_classifier/make_dataset.py --samples-per-class 40
python 03_document_classifier/train.py --model small_cnn --epochs 5
```

The small CNN is a quick CPU baseline. The main transfer-learning experiment is:

```bash
# Train only the new classification head
python 03_document_classifier/train.py --model resnet18 --freeze-backbone --epochs 3

# Fine-tune the whole pretrained network with a smaller learning rate
python 03_document_classifier/train.py --model resnet18 --epochs 3 --lr 0.0001
```

Pretrained weights are downloaded once by Torchvision. Add `--no-pretrained` to
study training from scratch.

## What to learn

- A **convolution** uses the same local filter at every position. Weight sharing
  makes it efficient and translation-aware.
- Early CNN layers learn edges and textures; deeper layers combine them into more
  task-specific patterns.
- **Transfer learning** starts from useful generic visual features. Freezing the
  backbone reduces compute and overfitting; fine-tuning adapts features but needs
  more data and a careful learning rate.
- **Cross-entropy** penalizes low predicted probability for the correct class.
- **Augmentation** creates plausible variation only in the training split. Here it
  includes small rotations and color changes.

## Evaluation

Accuracy can hide failure on a rare class. Inspect per-class precision, recall,
F1, and the confusion matrix. A high train score with a weaker validation score
suggests overfitting. The held-out test split should be used only after model and
hyperparameter choices are finished.

The generated data is intentionally easy and is for learning mechanics, not for a
scientific claim. Replace it with RVL-CDIP or your own labeled pages for a serious
experiment, and split by source/customer so near-duplicate templates cannot leak
across splits.

## Exercises

1. Compare frozen, fine-tuned, and randomly initialized ResNet-18.
2. Remove augmentation and plot the train/validation gap.
3. Make one class rare. Compare accuracy with macro F1.
4. Inspect confident mistakes and propose a data-centric fix.
