# Retail Sales Forecasting: ARIMA, SARIMA, and LightGBM

A retail time series study using M5 sales data to compare statistical forecasting
with machine learning over a 28-day horizon.

## Model summary

| Model | Specification | Approach |
| --- | --- | --- |
| ARIMA | ARIMA(1,1,1) | Models each series without an explicit seasonal component. |
| SARIMA | SARIMA(1,1,1)(1,0,0,7) | Adds a weekly seasonal component to each series. |
| LightGBM | 200 trees, 31 leaves, learning rate 0.05 | Uses calendar and lag features to correct a recent weekday-average forecast. |

ARIMA and SARIMA each fit all 30,490 series using 728 recent daily observations.
LightGBM learns across all 30,490 series using temporally sampled training targets.

## Evaluation

All three models forecast **30,490 product/store series** for **28 days**.
Two development windows precede the local test, **2016-04-25 to 2016-05-22**.
The previously inspected local test makes this a retrospective comparison.
MAE/RMSE cover every series; mean RMSSE covers 30,490 series with defined training scales.
182,669/182,760 optimized statistical fits converged;
180 constant-history windows receive exact constant forecasts.

| Model | Development RMSSE | Local-test RMSSE | Local-test MAE | Local-test RMSE |
| --- | --- | --- | --- | --- |
| SARIMA | 0.7356 | 0.7613 | 1.0538 | 2.2030 |
| ARIMA | 0.7360 | 0.7617 | 1.0570 | 2.2181 |
| LightGBM | 0.7377 | 0.7595 | 1.0473 | 2.1532 |

## Comparison graphs

### Model scores

![ARIMA, SARIMA, and LightGBM scores](reports/figures/comparison_01_three_models.png)

### Error across the forecast horizon

![MAE by forecast day](reports/figures/comparison_02_horizon.png)

### Representative forecasts

Examples from low-, medium-, and high-volume series selected using training data.

![Actual sales and three-model forecasts](reports/figures/comparison_03_forecasts.png)

## Final comparison

**LightGBM** has the lowest local-test mean RMSSE, MAE, and RMSE. **SARIMA** has the lowest average development RMSSE.
These scores and graphs cover all **30,490 series**, using fixed model settings
and common forecast windows.
