# Changelog

## 0.5.1
- Added PyPI Trusted Publishing automation using GitHub OIDC and a second `open-family-office` CLI entrypoint while preserving `ofo`.
- Added official MCP Registry `server.json`, package-ownership marker, registry validation in CI, and GitHub OIDC publication after PyPI succeeds.
- Added a prepared GitHub Pages workflow for the synthetic public demo.
- Added cross-file release-version consistency tests and built-wheel smoke coverage for both CLI entrypoints.
- Added a complete GTM launch kit and one-time account/UI setup guide under `docs/launch/`.
- No household accounting, trading, tax or financial-advice behaviour changed in this patch.

## 0.5.0
- Made Open Family Office a standalone installable CLI: the wheel now bundles the synthetic demo, household templates, portable Skills/workflows and offline dashboard resources.
- Added zero-clone trial and global-install paths with `uvx` / `uv tool install`, while keeping `pipx` and source checkouts as alternatives.
- Added workspace discovery so normal commands can run as `ofo overview`, `ofo scenario ...` and `ofo dashboard ...` from a private Family Office directory.
- `ofo init` now creates the private workspace structure and installs the portable agent kit automatically.
- Added `ofo agent install|sync|status` with hash-based safe upgrades: locally edited Skills/workflows are preserved as conflicts rather than overwritten.
- Added `ofo mcp-config` and clarified MCP as an optional, read-only interoperability layer rather than a prerequisite for the Skill/CLI experience.
- Reworked the ten user-facing Skills into task contracts with explicit triggers, deterministic CLI actions, interpretation order, boundaries and next-step handoffs.
- Converted Claude Skill files to thin pointers so the portable `.agents/skills/` definitions remain the single source of truth.
- Added clean-wheel CI that installs the built package into a fresh environment and verifies demo, init, Skill sync, MCP config and private dashboard export outside the source checkout.
- Kept advanced ownership, provider, quant and simulation capability behind progressive disclosure instead of removing it.

## 0.4.0
- Standardized Python package under `src/open_family_office/` and CLI as `ofo`.
- Added a progressive, user-facing 10-skill agent experience with Claude slash-command entrypoints.
- Grouped canonical domain files under `agent/` and website source under `web/`.
- Cleaned maintainer/launch material out of the repository root.
- Fixed release-hygiene CI around editable-install `.egg-info` artifacts and added a web build job.


## v0.3.0 — 2026-09-21

- Public brand changed to Open Family Office; internal Python module and hh-* skills stay compatible.
- Added a standalone landing page and dedicated static demo at public/index.html and public/demo.html.
- Unified daisyUI source-derived components, theme tokens, typography and mobile layouts.
- Added independently tested, client-side 24-month cash-budget playground with business-sale vs windfall behaviour.
- Retained 13 existing research charts and all previous provider/quant/agent tools without claiming new live integrations.
- Added safe source-download packaging and public-only deployment documentation.


## 0.2.0 — 2026-09-21

Added thirteen explicit provider adapters with evidence envelopes and contract tests; optional skfolio, PyPortfolioOpt, yfinance, OpenBB, PDF/OFX and MCP dependency groups; isolated OpenBB worker and a fail-fast setup script. Added locally executable SciPy optimization, a Ledoit–Wolf research frontier, seeded Monte Carlo, ownership consolidation and exposure aggregation. Expanded to sixteen skills and seven read-only MCP tools.

Rebuilt the HTML as a standalone compiled-Tailwind/Plotly dashboard with thirteen charts, five views, four synthetic scenarios, core EN/中文 controls, dark mode and export/print actions. Added private report generation and updated launch screenshots and documentation.

Validation is explicitly split: local numerical/browser execution vs fixture tests vs absent optional native SDK/live-provider tests. There are no live prices or authenticated bank/broker connections in the demo.

## 0.1.0

Initial workflow-first household accounting kit, explicit cash-flow/disposal scenarios, basic offline demo and repository launch material. No live adapters or quantitative optimization were implemented in that release.
