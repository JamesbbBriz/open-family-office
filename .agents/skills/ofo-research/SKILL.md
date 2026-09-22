---
name: ofo-research
description: Research external data, ownership look-through or liquid-sleeve portfolio methods with explicit assumptions.
license: MIT
compatibility: File-aware agent. Python 3.11+ for deterministic calculations; optional integrations require separate setup.
---

# ofo-research

## Use this when
Research external data, ownership look-through or liquid-sleeve portfolio methods with explicit assumptions.

## Outcome
Use evidence-preserving providers only with permission; keep illiquid household assets separate from liquid research inputs; never silently turn research weights into advice.

## Canonical workflow
- [`agent/workflows/source.md`](../../../agent/workflows/source.md)
- [`agent/workflows/lookthrough.md`](../../../agent/workflows/lookthrough.md)
- [`agent/workflows/optimize.md`](../../../agent/workflows/optimize.md)

## Operating rules
1. Read [`AGENTS.md`](../../../AGENTS.md) before using private data.
2. Work only with files the user explicitly authorizes. Private workspaces live outside this repository.
3. Run documented `ofo` / `python scripts/ofo.py` calculations before stating numerical results.
4. Keep confirmed facts, imported evidence, assumptions and model outputs separate.
5. Do not execute trades, move money, invent missing facts, or present research output as a guaranteed/suitable product recommendation.
6. End with: what changed, what was calculated, what remains unknown, and the next user-controlled choice.
