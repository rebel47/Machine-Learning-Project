from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import classification_report, confusion_matrix
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


class SmallCNN(nn.Module):
    def __init__(self, classes: int) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(1),
        )
        self.classifier = nn.Linear(64, classes)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(inputs).flatten(1))


def build_model(name: str, classes: int, pretrained: bool, freeze: bool) -> nn.Module:
    if name == "small_cnn":
        return SmallCNN(classes)
    weights = models.ResNet18_Weights.DEFAULT if pretrained else None
    model = models.resnet18(weights=weights)
    if freeze:
        for parameter in model.parameters():
            parameter.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, classes)
    return model


def run_epoch(model: nn.Module, loader: DataLoader, loss_fn: nn.Module,
              device: torch.device, optimizer=None) -> tuple[float, float]:
    training = optimizer is not None
    model.train(training)
    total_loss = correct = count = 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        if training:
            optimizer.zero_grad()
        with torch.set_grad_enabled(training):
            outputs = model(inputs)
            loss = loss_fn(outputs, targets)
            if training:
                loss.backward()
                optimizer.step()
        total_loss += loss.item() * len(targets)
        correct += (outputs.argmax(1) == targets).sum().item()
        count += len(targets)
    return total_loss / count, correct / count


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a document image classifier.")
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--model", choices=("small_cnn", "resnet18"), default="resnet18")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--freeze-backbone", action="store_true")
    parser.add_argument("--no-pretrained", action="store_true")
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else
                          "mps" if torch.backends.mps.is_available() else "cpu")
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)), transforms.RandomRotation(3),
        transforms.ColorJitter(brightness=0.15, contrast=0.15), transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    eval_transform = transforms.Compose([
        transforms.Resize((224, 224)), transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    train_set = datasets.ImageFolder(args.data / "train", train_transform)
    val_set = datasets.ImageFolder(args.data / "val", eval_transform)
    test_set = datasets.ImageFolder(args.data / "test", eval_transform)
    loaders = {
        "train": DataLoader(train_set, args.batch_size, shuffle=True),
        "val": DataLoader(val_set, args.batch_size),
        "test": DataLoader(test_set, args.batch_size),
    }
    model = build_model(args.model, len(train_set.classes), not args.no_pretrained,
                        args.freeze_backbone).to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=args.lr)
    best_state, best_accuracy = copy.deepcopy(model.state_dict()), -1.0
    print(f"device={device}; classes={train_set.classes}")
    for epoch in range(1, args.epochs + 1):
        train_loss, train_accuracy = run_epoch(model, loaders["train"], loss_fn, device, optimizer)
        val_loss, val_accuracy = run_epoch(model, loaders["val"], loss_fn, device)
        print(f"epoch={epoch} train_loss={train_loss:.4f} train_acc={train_accuracy:.3f} "
              f"val_loss={val_loss:.4f} val_acc={val_accuracy:.3f}")
        if val_accuracy > best_accuracy:
            best_accuracy, best_state = val_accuracy, copy.deepcopy(model.state_dict())
    model.load_state_dict(best_state)
    actual, predicted = [], []
    model.eval()
    with torch.no_grad():
        for inputs, targets in loaders["test"]:
            predicted.extend(model(inputs.to(device)).argmax(1).cpu().numpy())
            actual.extend(targets.numpy())
    print("\nTest classification report:\n",
          classification_report(actual, predicted, target_names=test_set.classes, zero_division=0))
    print("Confusion matrix (rows=true, columns=predicted):\n", confusion_matrix(actual, predicted))
    checkpoint = Path(__file__).parent / "checkpoints" / f"{args.model}.pt"
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"state_dict": model.state_dict(), "classes": train_set.classes,
                "settings": json.loads(json.dumps(vars(args), default=str))}, checkpoint)
    print(f"Saved {checkpoint}")


if __name__ == "__main__":
    main()
