# Agent experience

Open Family Office keeps the hard financial machinery and hides unnecessary complexity from first-run users.

**Skills are the UX. Workflows are the domain implementation. CLI/MCP are execution channels.**

## Why this split exists

The project is not trying to become a hosted SaaS dashboard. It is an open toolkit that should be useful to:

- a curious household that likes to self-host and experiment;
- an AI-agent user who wants natural-language access to deterministic finance tools;
- a developer who wants to add a pension model, provider, jurisdiction, importer or quant method.

Those users need different levels of detail without maintaining three different products.

## User-facing skill graph

```text
ofo-demo
   ↓
ofo-start
   ↓
ofo-overview ───────→ ofo-plan
   │                    │
   ├──→ ofo-scenario    └──→ ofo-research
   │          │                  │
   └──────────┴──────────→ ofo-dashboard
                                ↓
                           ofo-review

Existing-data change: ofo-update
Setup/debugging:      ofo-doctor
```

The user should not need to know the names of internal primitives such as `snapshot`, `liquidity`, `lookthrough` or `cvar` until they deliberately go deeper.

## Skill contract

Every Skill must define:

1. **Trigger** — when this Skill should be selected.
2. **Outcome** — what useful state or artifact should exist afterward.
3. **Deterministic action** — which `ofo` command/tool must be run before numerical claims.
4. **Interpretation order** — what the agent should explain first.
5. **Boundary** — what this Skill must not do.
6. **Handoff** — no more than two sensible next Skills.

This avoids “prompt prose that still lets the model improvise the whole workflow.”

## Canonical mapping

| Skill | Internal workflows | Main deterministic entrypoint |
|---|---|---|
| `ofo-demo` | demo | `ofo demo` |
| `ofo-start` | setup → import → snapshot | `ofo init`, `ofo validate`, `ofo overview` |
| `ofo-update` | import → snapshot | `ofo validate`, `ofo overview` |
| `ofo-overview` | snapshot + income + liquidity | `ofo overview` |
| `ofo-plan` | policy + allocate | `ofo allocation` |
| `ofo-scenario` | what-if (+ simulate) | `ofo scenario`, optional `ofo simulate` |
| `ofo-research` | source / lookthrough / optimize | `ofo providers`, `ofo fetch`, `ofo optimize` |
| `ofo-dashboard` | dashboard | `ofo dashboard` |
| `ofo-review` | review | deterministic reruns as needed |
| `ofo-doctor` | doctor | `ofo doctor`, `ofo agent status`, `ofo mcp-config` |

## Portable agent kit

`ofo init` installs the agent kit into the **private workspace**, not only the public source checkout:

- `.agents/skills/` — canonical portable user Skills;
- `.claude/skills/` — thin Claude discovery wrappers;
- `.claude/commands/` — slash-command entrypoints;
- `agent/workflows/` — canonical financial procedures;
- `agent/methodology/`, `schemas/`, `templates/` — domain support files;
- `AGENTS.md` — operating contract.

That means an installed CLI user can open the private folder directly in a file-aware agent without cloning the source repository.

## Upgrades and customization

Open source users should be allowed to fork and edit Skills locally.

`ofo agent sync` therefore uses a managed-file manifest:

- unchanged managed file → safe to upgrade;
- missing managed file → restore;
- locally modified file → **conflict, preserve user version**;
- file removed upstream → mark stale, do not silently delete.

This makes the agent kit upgradeable without treating user customization as corruption.

## CLI versus MCP

MCP is useful, but it is not the product's only interaction model.

- **CLI** is the deterministic, inspectable core.
- **Skills** provide task-level natural-language UX.
- **MCP** exposes a small read-only subset of tools to compatible hosts.

A user can get the full household workflow without MCP. When MCP is enabled, it should reduce plumbing, not introduce new financial authority.

## Progressive disclosure

### Level 0 — no install
`ofo demo` via `uvx`.

### Level 1 — household workflow
`init → overview → scenario → dashboard`.

### Level 2 — planning
policy, allocation framework, recurring review.

### Level 3 — research
provider evidence, ownership look-through, Monte Carlo, optimization.

### Level 4 — contributor
new Skills, workflows, jurisdictions, providers, importers and quant engines.

The capability remains broad; only the default surface is small.
