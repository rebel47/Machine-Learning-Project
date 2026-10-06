from __future__ import annotations

import argparse
import sys
from pathlib import Path

COURSE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COURSE_ROOT))

from common.metrics import ErrorCounts, cer, wer


SAMPLE = {
    "invoice": {
        "truth": "Invoice 1042\nTotal due EUR 249.00",
        "raw": "lnvoice 1042\nTotaI due EUR 249.OO",
        "clean": "Invoice 1042\nTotal due EUR 249.00",
    },
    "letter": {
        "truth": "Dear Dr. Miller thank you for your letter",
        "raw": "Dear Dr Miller thankyou for your lefter",
        "clean": "Dear Dr. Miller thank you for your letter",
    },
    "receipt": {
        "truth": "Coffee 3.50 Total 3.50",
        "raw": "Cofee 350 Tota 3.50",
        "clean": "Coffee 3.50 Total 3.50",
    },
}


def load_sets(truth_dir: Path, specifications: list[str]) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    truths = {p.stem: p.read_text(encoding="utf-8") for p in sorted(truth_dir.glob("*.txt"))}
    systems: dict[str, dict[str, str]] = {}
    for specification in specifications:
        if "=" not in specification:
            raise ValueError(f"Expected NAME=DIRECTORY, got {specification!r}")
        name, directory = specification.split("=", 1)
        root = Path(directory)
        systems[name] = {
            key: (root / f"{key}.txt").read_text(encoding="utf-8") for key in truths
        }
    return truths, systems


def totals(items: list[ErrorCounts]) -> ErrorCounts:
    return ErrorCounts(sum(x.substitutions for x in items),
                       sum(x.deletions for x in items),
                       sum(x.insertions for x in items),
                       sum(x.reference_length for x in items))


def report(truths: dict[str, str], systems: dict[str, dict[str, str]], normalize: bool) -> None:
    print(f"{'system':<12} {'micro CER':>10} {'macro CER':>10} {'micro WER':>10} {'macro WER':>10}")
    print("-" * 56)
    for system, predictions in systems.items():
        char_scores = [cer(truths[key], predictions[key], normalize) for key in truths]
        word_scores = [wer(truths[key], predictions[key], normalize) for key in truths]
        macro_cer = sum(x.rate for x in char_scores) / len(char_scores)
        macro_wer = sum(x.rate for x in word_scores) / len(word_scores)
        print(f"{system:<12} {totals(char_scores).rate:>10.3f} {macro_cer:>10.3f} "
              f"{totals(word_scores).rate:>10.3f} {macro_wer:>10.3f}")
        chars = totals(char_scores)
        print(f"  character operations: S={chars.substitutions}, D={chars.deletions}, I={chars.insertions}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate CER and WER.")
    parser.add_argument("--ground-truth", type=Path)
    parser.add_argument("--predictions", nargs="*", default=[])
    parser.add_argument("--normalize", action="store_true")
    args = parser.parse_args()
    if args.ground_truth:
        if not args.predictions:
            parser.error("--predictions needs one or more NAME=DIRECTORY values")
        truths, systems = load_sets(args.ground_truth, args.predictions)
    else:
        truths = {key: value["truth"] for key, value in SAMPLE.items()}
        systems = {name: {key: value[name] for key, value in SAMPLE.items()}
                   for name in ("raw", "clean")}
        print("Using built-in teaching example. Pass --ground-truth for your files.\n")
    report(truths, systems, args.normalize)


if __name__ == "__main__":
    main()
