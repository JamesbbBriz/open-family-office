---
name: ofo-start
description: Create or complete a private family-office workspace and produce the first verified household view.
license: MIT
compatibility: Any file-aware agent with access to the installed ofo CLI or a source checkout.
---

# ofo-start

Use this for a new household or an incomplete workspace.

## Run
1. Read AGENTS.md.
2. Run `ofo status`. If there is no workspace, create one with `ofo init <user-approved-path>`.
3. Follow setup.md to gather only the minimum facts needed for the first useful model.
4. Preserve supplied files under the private workspace; do not rewrite evidence.
5. Validate with `ofo validate`.
6. When valid, run `ofo overview --format markdown`.

## Interview order
Household/base currency → assets/debt → recurring income/outgoings → dated obligations → restrictions/liquidity → goals. Leave unknowns explicit.

## Finish with
Summarize what is confirmed, what is still unknown, and offer at most two next skills: usually **ofo-overview** or **ofo-plan**.

Canonical workflows:
- [agent/workflows/setup.md](../../../agent/workflows/setup.md)
- [agent/workflows/import.md](../../../agent/workflows/import.md)
- [agent/workflows/snapshot.md](../../../agent/workflows/snapshot.md)
