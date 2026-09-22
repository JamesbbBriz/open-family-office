# Quick start

## 1. Try synthetic data first

```bash
python scripts/ofo.py demo
```

No installation, network or model account is required for this demo.

## 2. Install the local tools

Python 3.12 is the recommended development version.

```bash
python -m venv .venv
# macOS/Linux
. .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -e '.[analytics,documents]'
ofo doctor
```

For all optional engines and integrations:

```bash
python scripts/bootstrap.py --all
```

## 3. Agent-first onboarding

For Claude Code, open the repository and run:

```text
/ofo-start
```

For other file-aware agents, ask it to use `.agents/skills/ofo-start/SKILL.md`. The skill creates a private workspace **outside the repository**, gathers only authorized facts and runs deterministic validation before producing the first overview.

Recommended next steps:

```text
ofo-overview → ofo-plan → ofo-scenario → ofo-dashboard
```

Use `ofo-update` when new statements or valuations arrive; use `ofo-research` only when external evidence or liquid-sleeve research is actually needed.

## 4. CLI examples

```bash
ofo validate ~/ofo-private/household.json
ofo overview ~/ofo-private/household.json
ofo cashflow ~/ofo-private/household.json --months 24 --format markdown
ofo stress ~/ofo-private/household.json ~/ofo-private/scenario.json --months 24
ofo compare-allocation ~/ofo-private/household.json ~/ofo-private/policy.json
```

Research tools:

```bash
ofo optimize examples/returns.synthetic.json --engine scipy --method min_variance
ofo simulate examples/simulation.synthetic.json
ofo lookthrough examples/ownership.synthetic.json
```

Provider retrieval is explicit and opt-in:

```bash
ofo providers
ofo fetch rba table --query '{"table":"f01"}' --allow-network --out ~/ofo-private/rba-f01.json
```

## 5. Export a private dashboard

```bash
ofo dashboard ~/ofo-private/household.json --out ~/ofo-private/dashboard-001.html
```

The HTML embeds private data. Do not place private exports under `public/` or commit them to GitHub.
