---
name: ofo-overview
description: Explain the household financial position: balance sheet, income durability and liquidity runway.
license: MIT
compatibility: File-aware agent. Python 3.11+ for deterministic calculations; optional integrations require separate setup.
---

# ofo-overview

## Use this when
Explain the household financial position: balance sheet, income durability and liquidity runway.

## Outcome
Validate first, run deterministic calculations, then summarize net worth, spendable liquidity, recurring income, obligations and material concentration gaps.

## Canonical workflow
- [`agent/workflows/snapshot.md`](../../../agent/workflows/snapshot.md)
- [`agent/workflows/income.md`](../../../agent/workflows/income.md)
- [`agent/workflows/liquidity.md`](../../../agent/workflows/liquidity.md)

## Operating rules
1. Read [`AGENTS.md`](../../../AGENTS.md) before using private data.
2. Work only with files the user explicitly authorizes. Private workspaces live outside this repository.
3. Run documented `ofo` / `python scripts/ofo.py` calculations before stating numerical results.
4. Keep confirmed facts, imported evidence, assumptions and model outputs separate.
5. Do not execute trades, move money, invent missing facts, or present research output as a guaranteed/suitable product recommendation.
6. End with: what changed, what was calculated, what remains unknown, and the next user-controlled choice.
