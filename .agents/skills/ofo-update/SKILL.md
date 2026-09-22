---
name: ofo-update
description: Add new statements, valuations, cash-flow changes or household facts without losing history.
license: MIT
compatibility: Any file-aware agent with access to the installed ofo CLI or a source checkout.
---

# ofo-update

Use this when an existing household receives new evidence or circumstances change.

## Run
1. Read AGENTS.md and run `ofo status`.
2. Keep the original source file unchanged in the private workspace.
3. Follow import.md to map new evidence into a proposed model update.
4. Show material changes before activating them.
5. Write a new model version; never silently overwrite source evidence.
6. Run `ofo validate` and then `ofo overview --format markdown`.

## Finish with
List changed facts, stale/unresolved items, and offer **ofo-scenario** if the change affects future plans or **ofo-dashboard** for a refreshed review.

Canonical workflows:
- [agent/workflows/import.md](../../../agent/workflows/import.md)
- [agent/workflows/snapshot.md](../../../agent/workflows/snapshot.md)
