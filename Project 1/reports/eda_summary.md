# EDA findings

Analyzed 30,490 series through `d_1913`; the final local holdout is excluded.

- 68.20% of daily sales are zero. The largest 20% of series contribute 70.3% of units.
- Average demand is highest on Saturday and lowest on Wednesday; detrended lag-7 correlation is 0.70.
- Store/category demand and representative series show why one aggregate forecast is insufficient.
- Price analysis uses 92 deterministic high-volume, median, and price-varying series plus representative examples, over the last training year; it is not a random population estimate.
- Only 1.18% of consecutive observed weekly prices change. In 30 eligible sampled series, median price/sales Spearman correlation is 0.04; this is not a population estimate or causal effect. Event and SNAP comparisons are also observational.

Use weekday/calendar features, lagged demand, and intermittency features. Compare prices as an explicit ablation assuming target-week prices are known. Full-history zero rates describe the data; they are not model inputs. Nine charts are in `reports/figures/`.
