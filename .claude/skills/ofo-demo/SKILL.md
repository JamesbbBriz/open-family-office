---
name: ofo-demo
description: Try Open Family Office safely with synthetic data before touching private files.
license: MIT
compatibility: File-aware agent. Python 3.11+ for deterministic calculations; optional integrations require separate setup.
---

# ofo-demo

## Use this when
Try Open Family Office safely with synthetic data before touching private files.

## Outcome
Run the bundled synthetic demo, explain the outputs, and show the next safe step.

## Canonical workflow
- [`agent/workflows/demo.md`](../../../agent/workflows/demo.md)

## Operating rules
1. Read [`AGENTS.md`](../../../AGENTS.md) before using private data.
2. Work only with files the user explicitly authorizes. Private workspaces live outside this repository.
3. Run documented `ofo` / `python scripts/ofo.py` calculations before stating numerical results.
4. Keep confirmed facts, imported evidence, assumptions and model outputs separate.
5. Do not execute trades, move money, invent missing facts, or present research output as a guaranteed/suitable product recommendation.
6. End with: what changed, what was calculated, what remains unknown, and the next user-controlled choice.
