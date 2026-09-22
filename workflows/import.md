# Import and reconcile records without inventing facts

Read `AGENTS.md` first. Canonical workflow; do not duplicate its business rules in runtime adapters.


## Inputs
A private workspace, source files explicitly selected by the user, snapshot date and existing model.
No automatic mailbox or bank access. No source folder is read merely because it exists.

## Procedure
1. Preserve the original. Identify document date, owner/account, currency, gross/net basis and coverage.
2. Build a proposed mapping to `schemas/household.schema.json`. Transactions and balances are different.
   A transfer between two owned accounts is not new household income. Loan proceeds are not investment return.
3. Identify duplicates: account totals versus positions, property in a trust versus personally reported value,
   company equity versus company-owned assets, pension total versus its holdings.
4. Cashflow CSV imports use exactly the header in `templates/cashflows.csv`. They append to a new model:
   `python scripts/hh.py import-csv <csv> --household <old.json> --out <new-private.json>`.
   Add real evidence references before importing. Duplicate IDs and bad references must fail.
5. For other records the agent may draft JSON from the selected evidence, but extraction remains reviewed,
   not an advertised automated importer. Mark unreadable values unknown; never infer digits from totals alone.
6. Reconcile source subtotals to the model and present each adjustment. Run `validate`, then `snapshot`.
   Leave the original model unchanged until the user adopts the new version.

## Output
`import-review.md`: sources; mapped fields; exceptions; duplicate removals; before/after reconciliation;
exact validation command and result. Keep it private. Do not quote sensitive account numbers in issues.

## Failure behaviour
Reject an ambiguous CSV header rather than guessing. Encoding/format errors get specific messages.
A broken field does not justify replacing the entire model or resetting the workspace.


## v0.2 extension

Local PDF text and OFX tools exist: `extract-pdf`, `import-ofx`, and normalized `import-holdings`. Text/transactions are evidence drafts, not approved facts or recurring-income classifications. Review and map explicitly; OCR and arbitrary PDF accuracy are not claimed.
