# Machine Learning Project 1

This project trains a lightweight forecasting baseline for the M5 forecasting dataset.

## Data

The project expects the following files in `data/`:

- `calendar.csv`
- `sales_train_validation.csv`
- `sample_submission.csv`
- `sell_prices.csv`

## Run

From the project directory:

```bash
python3 main.py
```

This writes a baseline submission to `data/baseline_submission.csv`.

## Model approach

The forecast uses a simple weekday-based baseline that averages each item/store pair's historical sales by weekday. If a weekday combination is missing, it falls back to the item's overall mean and then the global mean.
