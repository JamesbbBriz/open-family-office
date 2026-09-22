# Explain the full household balance sheet

Read `AGENTS.md` first. Canonical workflow; do not duplicate its business rules in runtime adapters.


## Inputs
A validated model at an explicit date. Read `methodology/balance-sheet.md`.

## Procedure
1. Run `python scripts/hh.py snapshot <household.json> --format markdown`.
2. Explain gross attributable assets, liabilities, net worth, spendable cash and 7-day hypothetical liquidity.
   Keep the denominators visible. Asset-class percentages are based on gross assets, not net worth unless stated.
3. Show wrappers as a second view of the same capital, not additional assets.
4. List restricted or non-investable assets: home, locked pensions, pledged balances and unlisted interests.
5. Flag stale valuations and missing liabilities. The absence of warnings does not validate source truth.
6. Describe exposure concentrations only from confirmed look-through data. An Australian home plus a
   construction business can share a qualitative economic risk; do not invent a 67% effective exposure number.

## Output
A short household snapshot, source/date notes and unresolved issues. Never turn it into buy/hold/sell advice.
A current snapshot says nothing by itself about sustainable spending or a suitable risky-asset percentage.
