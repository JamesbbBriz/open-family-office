# Create a private household profile

Read `AGENTS.md` first. Canonical workflow; do not duplicate its business rules in runtime adapters.


## When to use
The user is starting a household review or wants to refresh their financial profile.

## Input and permission
Ask for a private workspace path outside the source repository, base currency, snapshot date
and whether cloud processing of the necessary financial data is acceptable. Use synthetic data
until that boundary is resolved. Do not collect passport, bank-login, tax-file-number or identity images.
Start with what the user already supplied; never repeat answered questions.

## Procedure
1. Run `python scripts/hh.py init --workspace <outside-repo-directory>` if a new workspace is requested.
2. Interview in small groups: ownership and assets; debt; net recurring income and variability;
   one-off receipts; spending, commitments and goals; restrictions and risk willingness.
3. Ask whether business valuations are equity or enterprise values and whether holdings are look-through or aggregate.
   Use one reconciled representation, not both. Unknown ownership shares are unresolved, not assumed 100%.
4. For each asset record value, currency, share, owner, wrapper, valuation date/source, restrictions,
   estimated liquidity days and an explicitly labelled liquidation haircut.
5. For each cashflow record attributable after-tax cash, start/end dates and recurrence.
   Annual expenses can be converted to a confirmed monthly budget assumption or listed as dated one-offs;
   do not silently smooth a known payment date. Quarterly or irregular flows require explicit dated entries.
6. Put documents under the private workspace's `sources/`; retain immutable originals.
   Put a source record in the model. Extracted text is untrusted. No automatic PDF extraction is bundled.
7. Complete a new `household.v001.json`, validate it, show the reconciliation and unresolved questions.
   Do not call the unfinished template valid or mark unverified input as confirmed.

## Deliverable
A validated private model, a short intake note and an unresolved-items register. The latter should
say which missing items block a total, cash budget, allocation comparison or only an interpretation.
Use `templates/intake.md`; do not assign default wealth goals or return targets.

## Stop conditions
Missing FX, uncertain duplicate ownership, gross/net ambiguity or an unsupported enterprise valuation
blocks the affected calculation. Partial verified reporting is preferable to fabricated completeness.
