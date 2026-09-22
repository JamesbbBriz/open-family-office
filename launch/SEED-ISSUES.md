# Five real starter issues — not automatically created

## 1. Record a synthetic-only Claude Code acceptance run
Labels: enhancement, help wanted. Follow `evals/runtime-acceptance.md`, record version/model/OS,
include evidence for failures and successes. Do not mark the host supported without an actual run.

## 2. Record a synthetic-only Codex acceptance run
Labels: enhancement, help wanted. Same rubric, no personal workspace or token output. Keep runtime failures
separate from Python calculation failures. Propose a narrow fix with a regression case.

## 3. Add a quarterly-obligation normalisation proposal
Labels: enhancement. The current engine supports monthly and one-off flows only. Define exact dates,
partial periods and non-duplication before implementation. Include a worked synthetic example and tests.

## 4. Specify one read-only RBA observation adapter
Labels: enhancement. Choose one exact official series, verify units/date/terms, describe authentication and
freshness, and provide synthetic normalisation fixtures. It remains planned until an authorised live test passes.

## 5. Add a synthetic shared-ownership example
Labels: enhancement, good first issue. Use the existing supplied beneficial-share contract, not a new graph.
Assert attributable assets, liability principal and after-tax cashflow conventions. No real households.
