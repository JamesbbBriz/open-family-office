---
name: ofo-plan
description: Draft an investment policy and compare user-specified allocation targets without picking products.
license: MIT
compatibility: File-aware agent. Python 3.11+ for deterministic calculations; optional integrations require separate setup.
---

# ofo-plan

## Use this when
Draft an investment policy and compare user-specified allocation targets without picking products.

## Outcome
Turn goals, liquidity needs, horizon, constraints and risk capacity into a draft policy, then compare only explicit target allocations.

## Canonical workflow
- [`agent/workflows/policy.md`](../../../agent/workflows/policy.md)
- [`agent/workflows/allocate.md`](../../../agent/workflows/allocate.md)

## Operating rules
1. Read [`AGENTS.md`](../../../AGENTS.md) before using private data.
2. Work only with files the user explicitly authorizes. Private workspaces live outside this repository.
3. Run documented `ofo` / `python scripts/ofo.py` calculations before stating numerical results.
4. Keep confirmed facts, imported evidence, assumptions and model outputs separate.
5. Do not execute trades, move money, invent missing facts, or present research output as a guaranteed/suitable product recommendation.
6. End with: what changed, what was calculated, what remains unknown, and the next user-controlled choice.
