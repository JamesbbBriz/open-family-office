# Target comparison is not optimisation

This release implements only a deterministic comparison with **user-confirmed** weights.

Eligible capital consists of assets explicitly marked investable and unrestricted. Deduct the user's specified
cash reserve from eligible cash, not from an inaccessible account. The remaining eligible values define the
comparison denominator. Target amounts = residual eligible capital × supplied weight; differences = target − current.
Weights must sum exactly to 1. An insufficient reserve or no residual capital blocks the calculation.

Home equity, locked pensions and pledged balances are still shown in the full household snapshot. They are
not silently made available to implement a target. An eligible but illiquid asset can still make a mathematical
target infeasible to implement; the output is not a rebalance order or a transaction plan.

No expected-return estimator, covariance estimator, optimiser, Black–Litterman model, portfolio backtest,
tax-lot selector or trade execution is bundled. Unsupported data must not be invented to make a solver run.
The synthetic policy exists to test arithmetic, not to recommend 60/30/10 or any other weights.

Risk willingness is the user's stated preference. Financial capacity requires evidence about cashflows,
obligations, leverage, dependants and horizon. Required return comes from goal assumptions. None is a
substitute for the others. A shortfall can imply revisiting a goal rather than taking additional market risk.
