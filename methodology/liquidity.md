# Liquidity and cash timing

Spendable cash is the attributed value of cash-class assets with `restriction: none` and `liquidity_days: 0`.
Notice/term cash is not spendable today. Its later maturity is not inferred automatically: an explicit, reconciled principal-return flow is required.
Potential 7-day liquidity includes accessible assets with `liquidity_days <= 7`, after an explicit
`liquidation_haircut`. The latter is a hypothetical resource view, not a guarantee or an assumed liquidation.

Each forecast month:
closing cash = opening cash + stable inflows + variable inflows + one-off receipts + principal returns
+ sale receipts − recorded outflows.

The first month is the next calendar month after `as_of`. Dates within a month are aggregated.
Recurring entries are active inclusively between their start and end months; a one-off only occurs in its dated month.
No unrecorded return, yield, inflation, financing facility, tax, FX change or asset liquidation is added.

Debt principal is recorded in the balance sheet; full debt service is a cashflow once. The budget does not
produce an amortised debt schedule or full future net worth. A negative closing balance is an unfunded gap.
Monthly aggregation may miss intramonth shortages, and a point path is not a distribution of outcomes.

Capital calls and large planned expenses must be separately dated. Unknown timing is a reason to compare
alternative dates, not to present an average date as certain. Future sale proceeds do not cure today's cash gap.

A later release can add intramonth timing, explicit debt amortisation, stochastic outcomes and funding actions.
Each addition needs separate assumptions and validation rather than an LLM-generated answer labelled mathematical.
