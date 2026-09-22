# Classify income durability and one-off capital

Read `AGENTS.md` first. Canonical workflow; do not duplicate its business rules in runtime adapters.


## Inputs
Cashflows plus selected evidence about employment, business distributions, rent, pensions or asset sales.
Read `methodology/income.md`. Run `cashflow` for numeric totals; do not estimate missing net tax amounts.

## Procedure
1. For every inflow distinguish recurring fixed, recurring variable, one-off capital and principal return.
   Label gross revenue, net operating income, household distributions and personal after-tax receipts separately.
2. Describe durability: contractual basis, end date, variable component, concentration, vacancy/default risk,
   business reinvestment needs, and evidence supporting the description. Recurring does not mean guaranteed.
3. Separate investment distributions from returns of capital. A fund paying 10% does not establish a 10% return.
4. Show the next 12 monthly receipts and identified income dependencies. Do not extrapolate an exit, inheritance,
   bonus or asset disposal into perpetual annual income.
5. Identify correlated pressure qualitatively: job income, company distributions and owned property may
   fall together. Use a scenario to illustrate a user-supplied shock, not a fabricated beta.
6. A pending event belongs in a conditional scenario, not today's spendable cash. Do not probability-weight
   the amount into guaranteed reserves.

## Output
A register using `templates/income-register.md`: amount/date/source, recurrence, economic nature,
uncertainty, dependencies and information gaps. Distinguish modelling judgement from confirmed facts.

## Boundary
This is a structured review of income evidence, not credit underwriting or a certified sustainability rating.
