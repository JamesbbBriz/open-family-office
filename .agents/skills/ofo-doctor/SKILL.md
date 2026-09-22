---
name: ofo-doctor
description: Diagnose installation, optional engines, provider readiness, agent-kit state and MCP setup without exposing secrets.
license: MIT
compatibility: Any file-aware agent with the installed ofo CLI.
---

# ofo-doctor

Use this when setup, an optional engine, a provider, Skill discovery or MCP is not working.

## Run
1. Read AGENTS.md.
2. Run `ofo doctor --workspace .` when inside a private workspace.
3. Run `ofo agent status` to detect modified/missing managed Skill files.
4. If Skills are stale, use `ofo agent sync`; never overwrite conflicts.
5. If MCP is requested, run `ofo mcp-config` and explain that MCP is optional and read-only.
6. Never print API key values. Do not make a paid or live provider request just to test configuration.

## Finish with
Return a short table of ready / optional / missing / unverified items and the exact next command needed.

Canonical workflow: [agent/workflows/doctor.md](../../../agent/workflows/doctor.md)
