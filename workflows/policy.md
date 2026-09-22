# Draft an investment policy for user review

Read `AGENTS.md` first. Canonical workflow; do not duplicate its business rules in runtime adapters.


## Inputs
Confirmed profile, snapshot, income review, liquidity analysis and expressed preferences.
Use `templates/investment-policy.md`; the output is always DRAFT until adopted by the user.

## Procedure
1. Record purpose, time horizons, obligations, base currency and assets in scope.
2. Separate emotional willingness to accept losses, financial ability to fund obligations, and the return
   required by stated goals. A goal gap is not permission to take more risk.
3. Specify reserves, restrictions, excluded assets, ownership constraints and concentration questions.
4. Leave numerical return targets, security choices and strategic weights unfilled unless the user supplied
   them explicitly as assumptions. Do not generate an apparently personalised recommended allocation.
5. Define review triggers: income change, sale/large receipt, new debt, capital call, relocation or changed goals.
6. Record decision authority and review cadence. Define what requires a new decision rather than an autonomous action.
7. Present contradictions. For example, a large near-term goal plus locked wealth may be inconsistent with available cash.
   Offer a comparison of user-defined alternatives, not an unsupported suitability verdict.

## Output
Private `policy.v001.md` with status, assumptions, open decisions and evidence. Optional machine-readable
policy has `status: user_confirmed` only after actual adoption and includes user-specified weights and reserve.
The example policy percentages are synthetic software fixtures, not suggested allocations.
