# Notebook workflow

1. Explore sales, prices, calendar effects, and sparse demand.
2. Align histories, build safe features, and choose 90 matched series.
3. Fit ARIMA, weekly SARIMA, and pooled LightGBM on common forecast windows.
4. Compare errors and convergence, plot forecasts, and write `final_comparison.md`.

Code is split into small notebook cells. The additional local-test comparison is
retrospective because that window was inspected in the earlier full-panel study.
