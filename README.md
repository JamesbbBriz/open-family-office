<p align="center"><strong>OPEN FAMILY OFFICE</strong><br>Local-first family wealth research for AI agents.</p>

# Open Family Office

**Your portfolio is not your whole financial life.** Open Family Office models the household around the portfolio: assets, debt, recurring and one-off income, liquidity needs, ownership, scenarios and a separately declared liquid investment sleeve.

[中文](README.zh-CN.md) · [Quick start](docs/QUICKSTART.md) · [Agent experience](docs/AGENT-UX.md) · [Data model](docs/DATA-MODEL.md) · [Integrations](docs/INTEGRATIONS.md) · [Roadmap](ROADMAP.md)

![Open Family Office](assets/readme/landing.png)

## Try it in 30 seconds

No API key, model account or network call is needed for the synthetic demo.

```bash
git clone https://github.com/JamesbbBriz/open-family-office.git
cd open-family-office
python scripts/ofo.py demo
```

Or open `public/index.html` and `public/demo.html` directly. The bundled dashboard is static and self-contained.

![Household research dashboard](assets/readme/overview.png)

## The user experience

The project exposes a small set of **purposeful skills**, while keeping detailed financial procedures internal.

```text
ofo-demo
   ↓
ofo-start → ofo-overview → ofo-plan
                 ↓             ↓
            ofo-scenario   ofo-research
                 ↓             ↓
              ofo-dashboard → ofo-review

Existing household: ofo-update
Setup problem:      ofo-doctor
```

For Claude Code the same entrypoints are available as `/ofo-demo`, `/ofo-start`, `/ofo-overview`, etc. Other file-aware agents can load `.agents/skills/ofo-*/SKILL.md`. Canonical domain logic lives under `agent/workflows/`; runtime files are thin entrypoints.

## What it understands

- household balance sheet and attributable ownership
- recurring fixed vs variable vs one-off cash flows
- spendable liquidity versus locked/illiquid wealth
- business-sale and other event bridges
- future obligations and cash runway
- household investment policy constraints
- explicit ownership look-through and exposure dimensions
- liquid-sleeve optimization and Monte Carlo research with explicit assumptions
- evidence-preserving read-only provider adapters
- offline private dashboards

The research boundary is deliberate: a home, private company or locked pension is **not** silently converted into a tradable ticker.

## CLI

Install locally:

```bash
python -m pip install -e '.[analytics,documents]'
ofo doctor
ofo demo
```

Common deterministic commands:

```bash
ofo validate /path/to/household.json
ofo overview /path/to/household.json
ofo stress /path/to/household.json /path/to/scenario.json
ofo compare-allocation /path/to/household.json /path/to/policy.json
ofo optimize examples/returns.synthetic.json --engine scipy --method min_variance
ofo simulate examples/simulation.synthetic.json
```

Optional setup for quant engines, documents, market adapters and MCP is documented in [Quick start](docs/QUICKSTART.md).

## Architecture

```text
src/open_family_office/   deterministic engine, integrations, quant, reports
agent/workflows/          canonical financial procedures
agent/methodology/        domain rules and interpretation guidance
agent/schemas/            structured household inputs
agent/templates/          starter private-workspace templates
.agents/skills/           portable user-facing skill entrypoints
.claude/skills/           Claude project skills
.claude/commands/         Claude slash-command entrypoints
web/src/                  landing/dashboard source
public/                   generated static website
examples/                 synthetic reproducible fixtures
tests/                    accounting, integration, quant and web tests
```

See [Agent experience](docs/AGENT-UX.md) for the skill design.

## Data and provider layer

Adapters exist for SEC EDGAR, FRED, RBA, ABS, OECD, IMF, CoinGecko, Yahoo/yfinance, OpenBB, Alpha Vantage, Finnhub, MarketData.app and MetalpriceAPI. Network access is off by default. Adapter source code is **not** a claim that every live provider or entitlement has been validated.

External evidence is stored with source metadata and must be reviewed before it becomes an active household fact.

## Privacy boundary

Real household JSON, statements, credentials and private reports belong **outside this public repository**. The tools reject private outputs inside the code repository and avoid silently overwriting existing files. Generated HTML embeds its data; publishing a private report publishes that data.

Cloud agent runtimes may receive files you explicitly allow them to read. Local-first does not mean local inference or encryption. See [SECURITY.md](SECURITY.md).

## Not a broker or autonomous adviser

Open Family Office does not place trades, move money, log into banks, file tax returns or choose financial products for the user. Optimizer weights and simulations are research outputs conditional on supplied assumptions.

## Development

```bash
python -m pip install -e '.[analytics,documents]'
python -m unittest discover -s tests -v
node tests/sandbox.test.cjs
python scripts/release_check.py
```

Optional full setup:

```bash
python scripts/bootstrap.py --all
```

MIT licensed. Third-party components retain their own notices in [THIRD_PARTY.md](THIRD_PARTY.md). Contributions are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).
