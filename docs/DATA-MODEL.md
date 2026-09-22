# Data model and supported semantics

The machine contract is `agent/schemas/household.schema.json`; the stricter arithmetic/business checks run with
`python scripts/ofo.py validate <file>`. Currency amounts are decimal strings, not binary floats.

| Object | Meaning | Flat household-model boundary |
|---|---|---|
| Household | Date, currency, records and preferences | One consolidated model |
| Entity | Owner/account context | Labels, not a recursively evaluated ownership graph |
| Asset | Value × supplied beneficial share | Manual current valuation, class and wrapper separated |
| Liability | Positive principal × supplied share | Snapshot debt only, not amortisation |
| Cashflow | Net attributable after-tax amount with dates | Monthly or one-off; not automatic annual/quarterly normalisation |
| FX | Base currency units for one foreign unit | Explicit dated observation, fixed in forecast |
| Evidence | Source identifier and observation date | Provenance register, not proof of truth |
| Policy | User-confirmed target weights and cash reserve | Comparison only, not optimiser or advice |
| Scenario | Named price/cashflow assumptions and equity sales | Deterministic, no probability model |

Asset classes: cash, equity, bond, real_estate, private_business, private_credit, commodity, crypto,
collectible and other. Broad representation does not imply live pricing or specialised analytics for each.
`wrapper` can identify pension, trust or account context without inventing a new economic asset class.
`restriction` is none/locked/pledged. `investable` is explicitly confirmed; the model does not infer legal access.

`ownership_share` is already the household's beneficial share for that record. Do not apply it again to
cashflows: these are explicitly attributable amounts. Business values are equity values only. Aggregate
accounts and their holdings must not coexist as separately counted assets.

## Scenario contract
All fields are required: `id`, `label`, `asset_shocks`, `cashflow_multipliers`, `sales`, `note`.
A shock maps an existing asset id to a fractional value change, e.g. `"-0.20"`. A cashflow multiplier maps
an existing cashflow id to a nonnegative multiple, e.g. `"0.5"`. These are assumptions, not forecasts.
A sale contains `asset_id`, `month` (1–120), `net_proceeds_base`, `stop_cashflow_ids`, `note`.
Only unrestricted private-business equity sales are implemented; attributable after-tax proceeds are required.
There is no automatic related-debt discharge or earn-out modelling. Unknown fields fail rather than being silently ignored.

## Data quality
Missing FX or evidence references, duplicate ids, future valuations, nonfinite decimals, invalid dates,
inconsistent recurrence and unsupported enterprise values fail. Valuations older than 90 days and FX older
than 7 days warn: those thresholds are engineering defaults, not universal market freshness standards.
The runtime does not independently verify sources. A complete schema is not a complete financial understanding.

## v0.2 research extension

Separate JSON inputs in `examples/returns.synthetic.json`, `simulation.synthetic.json`, `ownership.synthetic.json` and `exposures.synthetic.json` define liquid research, simulation, explicit ownership and exposure dimensions. They do not replace or broaden the strict household schema. Never double-count an ownership-consolidated result and the same flat asset. Research cash amounts share the household base currency; all dates and expected parameters are explicit.
