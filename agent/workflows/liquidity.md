# Model whether cash can meet dated obligations

Read `AGENTS.md` first. Canonical workflow; do not duplicate its business rules in runtime adapters.


## Inputs
Validated household model and a user-selected horizon of 1–120 months. Read `methodology/liquidity.md`.

## Procedure
1. Identify existing unrestricted cash. Separately show assets potentially sellable within 7 days after
   explicit haircuts. Do not assume securities will be sold or credit will be extended.
2. Verify living expenses, debt service, school payments, property deposits, tax reserves and capital calls.
   Capital-call dates/amounts are assumptions unless supported by notices. Prevent double counting.
3. Run `python scripts/ofo.py cashflow <household.json> --months 24 --format markdown`.
4. Explain the minimum month-end cash and first unfunded gap. A negative value is a funding shortfall,
   not an approved overdraft. Monthly aggregation can hide intramonth payment stress.
5. Compare at least one explicitly specified adverse-income case with the baseline. Use `stress` or
   a validated scenario file; do not call one deterministic path a probability of ruin.
6. Separate timing, accessibility and valuation risk. A positive net worth cannot fill a cash gap by itself.

## Output
A monthly cash table, sources and assumptions, timing limitations, identified funding gaps and user decisions.
The engine excludes the current partial month and assumes no investment return, FX movement, tax calculation,
inflation or debt amortisation into future net worth. State these limits alongside the results.

## Do not
Declare an optimal emergency fund, select financial products, or promise that a positive path is safe.
