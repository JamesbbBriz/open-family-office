# Balance-sheet conventions

The snapshot is a **current, attributable, point-in-time economic view**. It is not legal ownership advice.

For each asset: attributable base value = supplied value × supplied ownership share × base-per-unit FX.
Debt uses the same convention. Net worth = total attributable assets − total attributable debt.
An asset value is a level, not an expected return. A stale appraisal is not a tradable price.

An account/pension/trust is a wrapper. Record either its aggregate value or its underlying holdings,
never both. When holdings are available, their asset classes remain equity, debt, cash etc.
The wrapper report is a parallel view, not another amount to add to gross assets.

A private business must be entered at **equity value** in the flat household model. An enterprise valuation needs an
explicit equity bridge outside this engine. Do not add company cash/property to an equity valuation
that already includes them, or subtract company debt a second time.

Ownership is deliberately shallow. `owner_id` labels a legal/account context; `ownership_share` is the
user-supplied beneficial share already attributed to this household. The engine does not multiply chains,
resolve cross-holdings or consolidate intercompany claims. Such records require reviewed net attribution first.
Do not advertise an Addepar-style ownership graph as implemented.

Future employment/business receipts are planning cashflows. No human-capital asset is capitalised into
current net worth. Home equity and locked retirement wealth may be valuable without being deployable capital.
Non-investable and restricted flags are distinct: users confirm them rather than the model inferring legal access.

See `docs/DATA-MODEL.md` for actual field names. See `tests/test_core.py` for arithmetic invariants.
