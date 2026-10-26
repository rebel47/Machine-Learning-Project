# Final evaluation

Model frozen from development folds: **lightgbm_refined**. Final local holdout: 2016-04-25–2016-05-22 (`d_1914`–`d_1941`).

| model | wrmsse | mae | rmse | bias |
| --- | --- | --- | --- | --- |
| seasonal_naive | 0.8697 | 1.2440 | 2.6769 | -0.1062 |
| weekday_mean | 0.7417 | 1.0830 | 2.2630 | -0.0608 |
| lightgbm_refined | 0.7147 | 1.0473 | 2.1532 | -0.0855 |

Selected-model WRMSSE improvement over the strongest holdout baseline: **3.65%** (negative means worse). This holdout was not used to reselect the model. Largest store-level absolute MAE: CA_3 (1.366 units); this is influenced by sales volume. Mean horizon MAE is 0.984 in days 1–7 and 1.047 in days 22–28. Segment tables and forecast plots are saved.

WRMSSE aggregates all 12 M5 hierarchy levels, trims leading zero demand for scales, and uses revenue from the 28 training days before each cutoff. Zero-weight, zero-scale series contribute zero; positive-weight undefined scales raise an error. Definition: [M5 accuracy paper](https://doi.org/10.1016/j.ijforecast.2021.11.013).

Retrained the selected method through `d_1941` and exported `data/submissions/forecast_submission.csv` with 60,980 template-aligned rows and 28 finite nonnegative forecasts. Final evaluation-horizon actuals are unavailable locally. These are local backtest results, not a Kaggle leaderboard score or measured inventory savings.
