# Forecast comparison configuration

`tuning.json` defines the current ARIMA/SARIMA candidate grid, screening strata,
and CPU settings. Screening uses development data and population weights.
Each family's strongest alternative is confirmed against its original setting
on all 30,490 series in both development windows. Final settings are selected
separately for regular and intermittent demand using groups fixed from the
90 days before the first development origin (regular: at least 80% selling days).

`comparison.json` defines the common 28-day windows, the original statistical
settings, and unchanged pooled LightGBM settings. `experiment.json` describes
the earlier LightGBM study. Statistical batches use eight CPU workers and
resumable checkpoints identified by estimator code, inputs, settings, and versions.

`reports/results/tuning_selection.json` freezes development-only selection;
`tuned_manifest.json` records provenance. Current results use `tuned_` and
`tuning_` prefixes. Earlier full-panel results use `full_panel_`; the older
90-series experiment uses `three_model_`.

Alternative SARIMA candidates difference observations before conditional fitting,
then restore forecasts to sales units. The original SARIMA benchmark retains its
full state-space fit. Unchanged ARIMA caches retain recorded provenance.
