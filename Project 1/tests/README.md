# Notebook checks

The current notebooks check raw schemas and unique keys, overlapping sales,
array alignment, future-sales leakage, inclusion of all 30,490 series,
hand-computed RMSSE, identical forecast horizons, checkpoint row ordering,
saved-prediction metrics, and finite nonnegative forecasts. Constant histories
and optimizer convergence are reported separately. Undefined RMSSE scales are
excluded only from that metric, with coverage reported; MAE/RMSE use every series.

No separate Python test files are required. The earlier full-panel WRMSSE and
submission results remain separate from the current full-panel comparison.
