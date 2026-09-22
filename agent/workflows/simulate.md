# ofo-simulate

## Goal

Simulate explicitly supplied liquid-sleeve assumptions.

## Procedure and controls

Require `scope=liquid_sleeve`, initial capital, asset weights, annual drift/volatility, a valid correlation matrix, net monthly cash flows, horizon, path count and seed. Document whether input cash flows came from household budgeting or a separate hypothetical assumption. Match base currency. Run `python scripts/ofo.py simulate <file>`. Show percentiles and funding gaps with methodology: correlated lognormal returns, monthly frictionless rebalancing, month-end cash flows, no tax/fees/jumps. Depletion is not an automatically funded overdraft. Model frequencies are conditional outputs, not calibrated real-world probabilities. Do not integrate a home's or private company's paper value into liquid capital.

## Completion

Return the actual calculation/output location, the methods executed and their limitations. Do not claim installation, live connection or host validation merely because source code exists.
