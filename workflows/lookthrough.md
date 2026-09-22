# hh-lookthrough

## Goal

Consolidate explicit ownership without double counting.

## Procedure and controls

Collect a user-confirmed acyclic ownership graph with unique node IDs, explicit percentage edges, base-currency leaf values and types. Never infer legal beneficial ownership. Run `python scripts/hh.py lookthrough <file>`. Reject parent-plus-child valuation duplication, cycles, invalid shares or ambiguous roots. Reconcile leaf totals to separately supplied household positions before using the result. For exposure inputs use `python scripts/hh.py exposures <file>`; unknown fractions stay unknown and different dimensions are not additive. State valuation dates and evidence gaps. No synthetic beta, private-asset correlation or automatic property valuation.

## Completion

Return the actual calculation/output location, the methods executed and their limitations. Do not claim installation, live connection or host validation merely because source code exists.
