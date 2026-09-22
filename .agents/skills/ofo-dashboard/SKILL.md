---
name: ofo-dashboard
description: Generate a private offline visual review from confirmed household files and optional research inputs.
license: MIT
compatibility: Any file-aware agent with the installed ofo CLI.
---

# ofo-dashboard

Use this when the user wants a reviewable visual artifact.

## Run
1. Read AGENTS.md and validate the household.
2. Choose a new output path inside the private workspace, normally `reports/review-YYYYMMDD.html`.
3. Run `ofo dashboard --out <path> --open`; add explicit scenario/research files only when they are part of the requested review.
4. Confirm the file exists and is non-empty.

## Privacy
The HTML embeds the household data it visualizes. Never put a private dashboard under the public repository or upload it without explicit user action.

## Finish with
Tell the user what views are included and offer **ofo-review** if this dashboard represents a decision checkpoint.

Canonical workflow: [agent/workflows/dashboard.md](../../../agent/workflows/dashboard.md)
