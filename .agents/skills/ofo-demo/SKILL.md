---
name: ofo-demo
description: Try Open Family Office safely with synthetic data before touching private files.
license: MIT
compatibility: Any file-aware agent with access to the installed ofo CLI or a source checkout.
---

# ofo-demo

Use this for a first look or when the user asks what the project can do.

## Run
1. Read AGENTS.md.
2. Run `ofo demo` (source fallback: `python scripts/ofo.py demo`).
3. If the user wants the visual experience, run `ofo demo --open`.
4. Explain that every household number and market series in the demo is synthetic.

## Do not
Do not ask for private data in this skill. Do not describe demo optimizer output as advice or a forecast.

## Finish with
- what the demo actually calculated;
- the difference between household accounting and liquid-sleeve research;
- one next action: **ofo-start** if the user wants to use their own data.

Canonical workflow: [agent/workflows/demo.md](../../../agent/workflows/demo.md)
