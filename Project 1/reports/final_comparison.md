# ARIMA, SARIMA, and LightGBM comparison

Same 90 varying-demand series, balanced across stores, categories, and training-volume bands; two development windows and one previously inspected 28-day local test.

| model | development_rmsse | test_rmsse | test_mae | test_rmse |
| --- | --- | --- | --- | --- |
| SARIMA | 0.7213 | 0.6865 | 0.9504 | 1.7022 |
| ARIMA | 0.7225 | 0.6868 | 0.9511 | 1.7012 |
| LightGBM | 0.7276 | 0.6959 | 0.9390 | 1.7125 |

**Lowest development/local-test RMSSE: SARIMA/SARIMA.** LightGBM has the lowest test MAE; ARIMA has the lowest test RMSE. Fixed ARIMA(1,1,1), weekly SARIMA(1,1,1)(1,0,0,7), and a pooled Poisson LightGBM correction use 728 training-target days. LightGBM also uses known calendar features and related series. ARIMA: 270/270 converged; SARIMA: 270/270 converged. Negative statistical forecasts are clipped at zero.

Mean RMSSE is equally weighted across the 90 series, not full M5 WRMSSE. This stratified sample is not a population estimate, orders were not exhaustively tuned, and the reused local test is retrospective rather than a fresh holdout. Earlier full-dataset results remain separate.
