# Notebook checks

The current notebooks check raw schemas and unique keys, overlapping sales,
array alignment, future-sales leakage, the matched 90-series sample, hand-computed
RMSSE, identical forecast horizons, saved-prediction metrics, and finite
nonnegative forecasts. Statistical convergence warnings are recorded explicitly.

No separate Python test files are required. The earlier full-panel WRMSSE and
submission results remain separate from this matched-sample comparison.
