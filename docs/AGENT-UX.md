# Agent experience

Open Family Office keeps **user-facing skills small** and **financial workflows granular**. Users should not need to know the internal workflow graph.

## Recommended journey

1. **`ofo-demo`** — try synthetic data with zero setup.
2. **`ofo-start`** — create a private workspace outside the repository and build the first verified household model.
3. **`ofo-overview`** — answer “where are we now?” with balance sheet, income durability and liquidity.
4. **`ofo-plan`** — draft an investment policy and compare user-specified allocation targets.
5. **`ofo-scenario`** — test a sale, job loss, property shock, purchase or other change.
6. **`ofo-dashboard`** — export a private, offline review page.
7. **`ofo-update`** and **`ofo-review`** — keep the model current and preserve decision history.

Use **`ofo-research`** when external evidence, ownership look-through or liquid-sleeve optimization is explicitly needed. Use **`ofo-doctor`** when setup or provider readiness is the problem.

## UX principles

- **Progressive disclosure:** first-run users see 8–10 purposeful skills, not every internal calculation primitive.
- **Deterministic money:** Python owns calculations; the agent owns interview, synthesis and explanation.
- **Evidence before inference:** imported/provider data is staged and reviewed before becoming an active household fact.
- **Private by placement:** real family files live outside the public repository.
- **No hidden side effects:** no trading, transfers, login automation or silent network calls.
- **Explicit handoffs:** each skill ends with one or two sensible next skills, never a wall of commands.

## Internal workflow map

```text
ofo-start      -> setup -> import -> snapshot
ofo-update     -> import -> snapshot
ofo-overview   -> snapshot + income + liquidity
ofo-plan       -> policy + allocate
ofo-scenario   -> what-if (+ simulate when explicitly requested)
ofo-research   -> source / lookthrough / optimize
ofo-dashboard  -> dashboard
ofo-review     -> review
ofo-doctor     -> doctor
ofo-demo       -> demo
```

The files under `agent/workflows/` remain the canonical domain procedures. `.agents/skills/`, `.claude/skills/` and `.claude/commands/` are runtime entrypoints only.
