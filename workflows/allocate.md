# Compare an explicit target with accessible capital

Read `AGENTS.md` first. Canonical workflow; do not duplicate its business rules in runtime adapters.


## Inputs
Validated household plus an actually user-confirmed policy. Read `methodology/allocation.md`.

## Procedure
1. Validate that target weights are explicitly user supplied, nonnegative and sum exactly to 1.
2. Set the eligible universe from confirmed investable/restriction fields. A home or locked pension
   does not become tradable because the user wants a different allocation.
3. Protect the explicitly specified cash reserve before the comparison. Insufficient cash blocks it.
4. Run `python scripts/hh.py allocate <household.json> <policy.json>`.
5. Show current versus hypothetical target amounts and the excluded reserve. A negative difference
   is a mathematical gap, not a sale instruction. Costs, taxes, settlement, lot size and market access are unsolved.
6. Discuss whether missing valuation/ownership data makes the comparison incomplete. Never infer
   a missing instrument's expected return from its name or asset-class label.

## Output
A target-comparison memo with the exact supplied assumptions and deterministic output.
Do not label the result optimal, suitable, diversified enough or executable. No trade API exists.

## Broader roadmap
True constrained optimisation, scenario-based private-asset risk and long-horizon goal modelling need
additional validated models. skfolio/PyPortfolioOpt are candidate future dependencies, not integrated features.


## v0.2 extension

This workflow remains user-confirmed policy comparison. Separate `hh-optimize` and `hh-simulate` workflows support research using explicit liquid-sleeve inputs; do not conflate their outputs with suitable household allocations.
