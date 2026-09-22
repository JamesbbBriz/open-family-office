---
name: ofo-plan
description: Draft a household investment policy and compare user-defined allocation targets without selecting products.
license: MIT
compatibility: Any file-aware agent with access to the installed ofo CLI or a source checkout.
---

# ofo-plan

Use this when the user wants a durable allocation framework rather than a one-off market opinion.

## Run
1. Read AGENTS.md and require a valid household overview first.
2. Follow policy.md to separate goals, liquidity reserve, horizon, constraints, risk willingness and risk capacity.
3. Draft policy inputs for user confirmation.
4. Only after confirmation, run `ofo allocation <policy.json> --format markdown`.
5. Keep product/ticker selection outside this skill.

## Finish with
Show reserve capital, investable capital and the consequences of the user-confirmed target mix. Offer **ofo-research** for deeper liquid-sleeve methods or **ofo-scenario** to stress the policy.

Canonical workflows:
- [agent/workflows/policy.md](../../../agent/workflows/policy.md)
- [agent/workflows/allocate.md](../../../agent/workflows/allocate.md)
