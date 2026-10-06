from __future__ import annotations

from pathlib import Path

import pandas as pd


DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
HORIZON_DAYS = 28


def load_data(data_dir: str | Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the M5 sales, calendar, and submission tables."""
    data_path = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
    sales = pd.read_csv(data_path / "sales_train_validation.csv")
    calendar = pd.read_csv(data_path / "calendar.csv")
    submission = pd.read_csv(data_path / "sample_submission.csv")
    return sales, calendar, submission


def build_baseline_forecast(sales: pd.DataFrame, calendar: pd.DataFrame, submission: pd.DataFrame) -> pd.DataFrame:
    """Create a simple weekday-based sales baseline for the next 28 days.

    The logic uses each item/store pair's average historical sales for its weekday,
    with a fallback to the item's overall mean for missing combinations.
    """
    if sales.empty or calendar.empty or submission.empty:
        raise ValueError("Input tables must not be empty.")

    sales_long = sales.melt(
        id_vars=["id", "item_id", "dept_id", "cat_id", "store_id", "state_id"],
        var_name="d",
        value_name="sales",
    )
    sales_long = sales_long.merge(calendar[["d", "weekday"]], on="d", how="left")

    item_store_mean = sales_long.groupby(["item_id", "store_id"], as_index=False)["sales"].mean()
    item_store_mean = item_store_mean.rename(columns={"sales": "item_store_mean"})

    weekday_means = (
        sales_long.groupby(["item_id", "store_id", "weekday"], as_index=False)["sales"]
        .mean()
        .rename(columns={"sales": "weekday_mean_sales"})
    )

    global_mean = float(sales_long["sales"].mean())

    submission_with_meta = submission.merge(
        sales[["id", "item_id", "store_id"]], on="id", how="left"
    )

    future_days = [f"d_{day}" for day in range(1914, 1914 + HORIZON_DAYS)]
    future_calendar = calendar[calendar["d"].isin(future_days)][["d", "weekday"]].copy()
    future_calendar = future_calendar.sort_values("d").reset_index(drop=True)
    future_map = dict(zip(future_calendar["d"], future_calendar["weekday"]))

    result = submission_with_meta.copy()

    for offset, future_day in enumerate(future_days, start=1):
        weekday = future_map.get(future_day, "Sunday")

        day_lookup = weekday_means[weekday_means["weekday"] == weekday][["item_id", "store_id", "weekday_mean_sales"]]
        merged = result[["id", "item_id", "store_id"]].merge(
            day_lookup,
            on=["item_id", "store_id"],
            how="left",
        )
        merged = merged.merge(item_store_mean, on=["item_id", "store_id"], how="left")

        forecast = merged["weekday_mean_sales"].fillna(merged["item_store_mean"]).fillna(global_mean)
        result[f"F{offset}"] = forecast.clip(lower=0).round(4)

    return result[["id", *[f"F{day}" for day in range(1, HORIZON_DAYS + 1)]]]


def generate_submission(data_dir: str | Path | None = None, output_path: str | Path | None = None) -> pd.DataFrame:
    """Generate a forecast submission file based on the weekday baseline."""
    sales, calendar, submission = load_data(data_dir)
    forecast = build_baseline_forecast(sales, calendar, submission)

    if output_path is None:
        output_path = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
        output_path = output_path / "baseline_submission.csv"
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    forecast.to_csv(output_path, index=False)
    return forecast


if __name__ == "__main__":
    generate_submission()
