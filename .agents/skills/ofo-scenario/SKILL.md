---
name: ofo-scenario
description: Test a job loss, business sale, property shock, major purchase, windfall or other explicit household what-if.
license: MIT
compatibility: Any file-aware agent with access to the installed ofo CLI or a source checkout.
---

# ofo-scenario

Use this for “what happens if…?” questions.

## Run
1. Read AGENTS.md and validate the current household.
2. Translate the user's event into an explicit scenario file; show assumptions before calculating when they are not already confirmed.
3. Run `ofo scenario <scenario.json> --format markdown`.
4. Separate immediate balance-sheet changes from future cash-flow changes.
5. Use Monte Carlo only if the user explicitly asks about a declared liquid investment sleeve.

## Finish with
State the baseline, changed variables, first material consequence and unresolved assumptions. Offer **ofo-dashboard** or **ofo-plan**.

Canonical workflows:
- [agent/workflows/what-if.md](../../../agent/workflows/what-if.md)
- [agent/workflows/simulate.md](../../../agent/workflows/simulate.md)
