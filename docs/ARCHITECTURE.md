# Architecture — v0.2

```text
File-aware agent / read-only stdio MCP
                 ↓
Canonical workflows + methodology (one source of truth)
                 ↓
Explicit private household / policy / scenario / research inputs
                 ↓
Decimal accounting core ── separate NumPy/SciPy quant modules
          ↓                       ↓
Cash budget / current state    Liquid-sleeve research / Monte Carlo
          └───────────┬───────────┘
                      ↓
              Standalone Tailwind + Plotly report
```

External sources enter through explicit `fetch` calls into evidence envelopes, not directly into the accounting state. Mapping, identifiers, dates, units and rights require review. The HTTP transport is in the integrations package, not the dependency-free accounting core. The OpenBB worker uses a separate interpreter to reduce dependency collisions. Native libraries are lazy imported so the basic accounting CLI remains usable without them.

Private outputs use the original outside-repository path guard, refuse overwrites and never silently upload. MCP further confines reads to a user-selected JSON workspace. This is a least-privilege design, not a claim of a secure model sandbox. Statements and provider text are untrusted content, never instructions.

`site/dashboard.html`, `.css` and `.js` are the maintainable sources. Compiled Tailwind is checked in; the builder embeds it with Plotly and JSON. Public builds require a synthetic household fixture. Private exports call the same renderer but write outside the repository. Missing optional research inputs render explicit empty states. Currency display follows the household currency; research assumptions must already use that unit.

Ownership graph consolidation is separate from the flat attributable household model. Do not merge both outputs into net worth without reconciling the leaf positions; the graph cannot be counted on top of the same flat assets. Risk dimensions are separate views, not additive exposures. Time-varying ownership, legal beneficial ownership inference and transaction-ledger consolidation remain outside scope.
