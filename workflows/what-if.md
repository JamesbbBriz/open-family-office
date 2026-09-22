# Compare a changed household circumstance

Read `AGENTS.md` first. Canonical workflow; do not duplicate its business rules in runtime adapters.


## Inputs
A current model and a clearly stated hypothetical event. Read `methodology/scenarios.md`.

## Procedure
1. Translate the event into explicit numerical assumptions and dates. Keep the original unchanged.
   Use the scenario contract documented in `docs/DATA-MODEL.md` and supplied examples.
2. For asset markdowns use `asset_shocks` by known asset id. For changed receipts/outflows use
   `cashflow_multipliers`. Do not infer a joint correlation or probability from the selected shock.
3. A private-business sale uses net attributable after-tax equity proceeds, a settlement month and
   the recurring inflows that stop. Remove the existing equity value in the event bridge.
   Enterprise value, staged earn-outs, household-debt discharge and property sales require explicit extensions.
4. New gifts, inheritances or expenses can be represented in a separate versioned household as dated one-off
   cashflows. They are not monthly income. The scenario must remain conditional until realised.
5. Run baseline and changed paths with identical dates and horizons. Run `stress` for supplied scenario files.
6. Explain current mark-to-market changes separately from future cash events. Do not publish a future
   net-worth forecast: this engine does not model asset returns or debt amortisation.
7. Store the scenario, output and a decision note only in the private workspace. Never silently make it the baseline.

## Output
What changed, what stayed fixed, the cash path, the first gap, any sale bridge, and assumptions driving differences.
In the bundled example a 900,000 sale receipt replaces 600,000 of business equity: the event-only wealth
change is 300,000, not 900,000. Related monthly distributions stop. These are synthetic inputs.
