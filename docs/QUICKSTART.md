# Run the source checkout

## Preview: no installation

Open `public/demo.html` in a browser that executes JavaScript. It is a standalone synthetic report, approximately 5 MB uncompressed. No CDN or API calls are needed. Asset data, code and the Plotly bundle are inside the file. Existing screenshot images are actual renders, not concept art.

## Complete setup

Use Python 3.12 for the widest expected optional-package compatibility, and Node.js 20+ with npm. Python 3.11+ is required by this project. From the source root:

```bash
python scripts/bootstrap.py --all --dry-run
python scripts/bootstrap.py --all
```

The first command changes nothing. The second creates `.venv`, installs `.[all]`, installs OpenBB into `.venv-openbb`, builds CSS, generates the HTML and runs tests. It contacts package registries, not financial data providers. The isolated OpenBB interpreter uses your invoking Python version; unsupported Python/OS combinations may fail. Full resolution was not executed in the delivery environment. Successful resolved versions are recorded outside the repo in `~/.open-family-office/install-core.txt` and `install-openbb.txt`.

Use `.venv/bin/python` on macOS/Linux or `.venv\Scripts\python.exe` on Windows for every subsequent Python command. The examples below use `python` for readability after you activate that environment.

```bash
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python scripts/hh.py doctor
python scripts/hh.py demo
python scripts/hh.py providers
```

`doctor` reports missing dependencies and environment-variable names, never their values. Keys are read from your shell/agent environment; `config/environment.example` is a reference, not an automatically sourced `.env` file. Set `OPENBB_PYTHON` to the absolute interpreter path printed by bootstrap.

## Smaller setup

```bash
python scripts/bootstrap.py --without-ui-build
# Or a dependency-free accounting run:
python scripts/hh.py demo
```

The smaller install enables numerical analytics and reuses checked-in compiled CSS. The prebuilt HTML never requires Python merely to view it. The full test suite requires analytics dependencies; optional native tests explicitly skip when their packages are missing.

## Run the research tools

```bash
python scripts/hh.py optimize examples/returns.synthetic.json --engine scipy --method min_variance
python scripts/hh.py optimize examples/returns.synthetic.json --engine scipy --method cvar
python scripts/hh.py optimize examples/returns.synthetic.json --engine scipy --method risk_parity
python scripts/hh.py simulate examples/simulation.synthetic.json
python scripts/hh.py lookthrough examples/ownership.synthetic.json
python scripts/hh.py exposures examples/exposures.synthetic.json
```

After their extras are installed, `--engine skfolio` supports minimum variance, CVaR and risk parity. `--engine pypfopt` additionally supports HRP (uncapped wrapper) and Black–Litterman (requires explicit prior returns, absolute views and confidences). Unsupported engine/method combinations stop with an error; there is no silent fallback pretending to use another library.

## Explicit retrieval example

```bash
python scripts/hh.py fetch rba table --query '{"table":"f01"}' --allow-network --out "$HOME/hh-private/rba-f01.json"
```

Create the parent private folder first. Omitting `--allow-network` refuses retrieval. A returned evidence envelope is not an approved household valuation: check instrument identity, units, date and use rights before mapping it. Some provider responses require additional normalization; this is not an automatic end-to-end price-to-allocation feed.

## Private dashboard export

Keep private inputs outside this source checkout. The command refuses to overwrite an existing output file:

```bash
python scripts/hh.py dashboard "$HOME/hh-private/household.json"   --policy "$HOME/hh-private/policy.json"   --scenario "$HOME/hh-private/scenario.json"   --returns "$HOME/hh-private/liquid-returns.json"   --simulation "$HOME/hh-private/simulation.json"   --out "$HOME/hh-private/dashboard-001.html"
```

Only household and output are required; absent optional research inputs produce empty states, not invented values. All monetary research inputs must use the household base currency. No automatic FX conversion is performed inside an optimizer or Monte Carlo input. Changing family assumptions requires regeneration; the HTML selects already-computed scenarios.

## Agent / MCP

Read `AGENTS.md`, then invoke portable skills in your chosen host. Discovery syntax varies by host/version. See `config/mcp.example.json` for a read-only stdio server, using the installed interpreter and an explicit private `HH_WORKSPACE`. Its seven tools read only JSON inside that folder, no live APIs, no writes, no orders. Paths containing spaces must be passed as separate argument values. Native host handshakes were not run in this delivery.
