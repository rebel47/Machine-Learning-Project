# Preprocessing findings

- Aligned 30,490 series across both sales files; overlapping values match exactly.
- Sales contain no missing, negative, or fractional values. Weekly price keys are unique and positive.
- Saved unsigned 16-bit sales, float32 weekly prices, metadata, and calendar in `data/processed/`.
- Feature example: 672 rows and 24 columns. Missing prices remain missing for LightGBM to handle.
- Future-sales mutation check passed for 12 series across the full 28-day horizon.

Calendar and weekly prices are joined through explicit indices. Zero sales remain valid observations; absent events are encoded as no event. Demand lags and rolling windows are shifted at least 28 days for the basic models. The refined model uses only history available at its explicit forecast origin. Category codes use product metadata, without target encoding. Final holdout labels are excluded from training and development.
