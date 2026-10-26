# Modeling findings

Compared five methods on two rolling 28-day development folds, using all 30,490 series.
Selected **lightgbm_refined** by mean development WRMSSE; improvement over the strongest baseline is **7.59%**.

| model | mean_wrmsse | std_wrmsse | mean_mae | mean_seconds |
| --- | --- | --- | --- | --- |
| lightgbm_refined | 0.6458 | 0.0349 | 1.0323 | 69.4499 |
| weekday_mean | 0.6988 | 0.0481 | 1.0601 | 0.1479 |
| lightgbm_demand | 0.7908 | 0.0179 | 1.0829 | 23.4321 |
| lightgbm_prices | 0.7917 | 0.0234 | 1.0828 | 23.9138 |
| seasonal_naive | 0.9059 | 0.0239 | 1.2215 | 0.0025 |

Basic ML uses 364 days of targets; refined ML uses 728 days and learns a multiplicative correction to an 8-week weekday baseline available at the forecast origin. Targets are sampled every 13 days so weekdays rotate; every series is represented. All demand inputs respect the forecast origin. The price variant assumes target-week prices are known. Settings were fixed before final-holdout evaluation; one refinement followed initial development underperformance; original scores are preserved in `reports/results/initial_development_scores.csv`. No broad hyperparameter search was performed. Gain importance is descriptive.
