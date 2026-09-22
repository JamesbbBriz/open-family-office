---
name: ofo-overview
description: Explain the household balance sheet, income durability, liquidity and near-term obligations.
license: MIT
compatibility: Any file-aware agent with access to the installed ofo CLI or a source checkout.
---

# ofo-overview

Use this for “where are we now?” questions.

## Run
1. Read AGENTS.md.
2. Run `ofo validate`; stop and surface blocking input errors.
3. Run `ofo overview --format markdown`.
4. Follow snapshot.md, income.md and liquidity.md for interpretation.

## Explain in this order
Spendable liquidity → recurring income/outgoings → dated obligations/runway → net worth composition → concentration/ownership issues → stale evidence.

Do not lead with portfolio returns when the binding household issue is liquidity.

## Finish with
Name the two or three decision-relevant findings and offer **ofo-plan** or **ofo-scenario**.

Canonical workflows:
- [agent/workflows/snapshot.md](../../../agent/workflows/snapshot.md)
- [agent/workflows/income.md](../../../agent/workflows/income.md)
- [agent/workflows/liquidity.md](../../../agent/workflows/liquidity.md)
