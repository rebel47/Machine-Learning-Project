# Comparison configuration

`comparison.json` selects all 30,490 series for ARIMA, weekly SARIMA, and
LightGBM across three 28-day forecast windows. Statistical models use 728 daily
observations per series. LightGBM pools every series and samples target dates
every 13 days, with earlier observations available for feature warm-up.

The statistical fits run on eight CPU workers with 256-series checkpoints.
Checkpoint identities include estimator code, input fingerprints, parameters,
and package versions. Constant histories receive exact constant forecasts.

`experiment.json` and `selection.json` describe the earlier full-panel study.
Completed full-panel settings, versions, and the series-identity hash are recorded
in `reports/results/full_panel_manifest.json`. Earlier 90-series results retain
the `three_model_` prefix; current full-panel results use `full_panel_`.
