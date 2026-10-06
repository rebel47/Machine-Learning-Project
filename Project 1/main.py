from pathlib import Path

from src.forecasting import generate_submission


def main() -> None:
    data_dir = Path(__file__).resolve().parent / "data"
    output_path = data_dir / "baseline_submission.csv"
    generate_submission(data_dir=data_dir, output_path=output_path)
    print(f"Saved baseline forecast to: {output_path}")


if __name__ == "__main__":
    main()
