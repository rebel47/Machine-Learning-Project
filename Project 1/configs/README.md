# Comparison configuration

`comparison.json` controls the current ARIMA, weekly SARIMA, and LightGBM
comparison: 90 matched series, 28-day forecasts, 728 training-target days,
fixed statistical orders, and LightGBM parameters. The 90 series are sampled
using only data before the earliest forecast window, across stores, categories,
and volume bands. LightGBM pools all series and uses earlier feature warm-up
history; the statistical models fit the recent 728 observations separately.

`experiment.json` and `selection.json` describe the earlier full-panel study.
Current settings, versions, and sample IDs are recorded in
`reports/results/three_model_manifest.json`.
