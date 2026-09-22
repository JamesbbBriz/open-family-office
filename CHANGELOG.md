# Changelog

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
