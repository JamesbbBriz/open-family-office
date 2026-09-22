---
name: ofo-review
description: Review a past financial decision or scenario and record what changed.
license: MIT
compatibility: File-aware agent. Python 3.11+ for deterministic calculations; optional integrations require separate setup.
---

# ofo-review

## Use this when
Review a past financial decision or scenario and record what changed.

## Outcome
Compare the original assumptions with actual outcomes and new evidence, then create a concise decision record without rewriting history.

## Canonical workflow
- [`agent/workflows/review.md`](../../../agent/workflows/review.md)

## Operating rules
1. Read [`AGENTS.md`](../../../AGENTS.md) before using private data.
2. Work only with files the user explicitly authorizes. Private workspaces live outside this repository.
3. Run documented `ofo` / `python scripts/ofo.py` calculations before stating numerical results.
4. Keep confirmed facts, imported evidence, assumptions and model outputs separate.
5. Do not execute trades, move money, invent missing facts, or present research output as a guaranteed/suitable product recommendation.
6. End with: what changed, what was calculated, what remains unknown, and the next user-controlled choice.
