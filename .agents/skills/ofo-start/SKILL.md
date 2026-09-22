---
name: ofo-start
description: Set up a new private family-office workspace and guide first-time onboarding.
license: MIT
compatibility: File-aware agent. Python 3.11+ for deterministic calculations; optional integrations require separate setup.
---

# ofo-start

## Use this when
Set up a new private family-office workspace and guide first-time onboarding.

## Outcome
Create a private workspace outside the repository, gather only user-authorized facts, validate them, and produce the first snapshot.

## Canonical workflow
- [`agent/workflows/setup.md`](../../../agent/workflows/setup.md)
- [`agent/workflows/import.md`](../../../agent/workflows/import.md)
- [`agent/workflows/snapshot.md`](../../../agent/workflows/snapshot.md)

## Operating rules
1. Read [`AGENTS.md`](../../../AGENTS.md) before using private data.
2. Work only with files the user explicitly authorizes. Private workspaces live outside this repository.
3. Run documented `ofo` / `python scripts/ofo.py` calculations before stating numerical results.
4. Keep confirmed facts, imported evidence, assumptions and model outputs separate.
5. Do not execute trades, move money, invent missing facts, or present research output as a guaranteed/suitable product recommendation.
6. End with: what changed, what was calculated, what remains unknown, and the next user-controlled choice.
