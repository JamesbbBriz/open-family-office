# Quick start

Open Family Office is designed for three different entry levels: **try it**, **install the CLI**, or **clone it to contribute**.

## 1. Try it without installing

With [uv](https://docs.astral.sh/uv/) installed:

```bash
uvx --from git+https://github.com/JamesbbBriz/open-family-office.git ofo demo
```

To open the bundled interactive dashboard as well:

```bash
uvx --from git+https://github.com/JamesbbBriz/open-family-office.git ofo demo --open
```

The demo is synthetic. It does not ask for a model account, API key or household data.

## 2. Install the CLI globally

```bash
uv tool install git+https://github.com/JamesbbBriz/open-family-office.git
ofo --version
ofo doctor
```

If uv warns that its executable directory is not on `PATH`, run `uv tool update-shell` and restart the shell.

A pipx fallback is also possible:

```bash
pipx install git+https://github.com/JamesbbBriz/open-family-office.git
```

## 3. Create your private workspace

Choose a directory outside the public source repository:

```bash
ofo init ~/FamilyOffice
cd ~/FamilyOffice
ofo status
```

`ofo init` creates:

```text
FamilyOffice/
├── household.json
├── PRIVATE.md
├── README.md
├── evidence/
├── imports/
├── scenarios/
├── reports/
├── .ofo/
│   ├── workspace.json
│   └── agent-kit.json
├── .agents/skills/
├── .claude/skills/
├── .claude/commands/
└── agent/
    ├── workflows/
    ├── methodology/
    ├── schemas/
    └── templates/
```

The agent kit is installed automatically. Open **this private workspace** in your file-aware agent and use **ofo-start**.

## 4. The normal CLI path

Once `household.json` is complete:

```bash
ofo validate
ofo overview --format markdown
ofo scenario scenarios/job-loss.json
ofo allocation policy.json
ofo dashboard --out reports/review.html --open
```

Because the CLI discovers the nearest `.ofo/workspace.json`, you do not need to repeat the household path while working inside the workspace.

Legacy expert commands such as `stress` and `compare-allocation` remain available, but they are not the first-run UX.

## 5. Keep Skills current without losing your edits

After upgrading Open Family Office:

```bash
uv tool upgrade open-family-office
cd ~/FamilyOffice
ofo agent sync
ofo agent status
```

Managed files that are still unchanged are updated. A Skill or workflow you edited yourself is reported as a **conflict and left untouched**.

## 6. Optional MCP

MCP is useful when your agent host prefers standard tool calls, but it is not required for normal Skill or CLI use.

Install the MCP dependency into the tool environment:

```bash
uv tool install --force --with 'mcp>=1.10,<2' git+https://github.com/JamesbbBriz/open-family-office.git
```

Then, inside the private workspace:

```bash
ofo mcp-config
```

The generated stdio configuration scopes the server to that workspace. The MCP tools are read-only.

## 7. Advanced research extras

The base CLI intentionally keeps advanced engines optional. A one-shot power-user install can layer additional packages into the uv tool environment:

```bash
uv tool install --force \
  --with 'numpy>=2.1,<3' \
  --with 'pandas>=2.2,<3' \
  --with 'scipy>=1.14,<2' \
  --with 'scikit-learn>=1.5,<2' \
  --with 'pypdf>=5.9,<7' \
  --with 'ofxparse==0.21' \
  --with 'mcp>=1.10,<2' \
  --with 'yfinance>=0.2.60,<1' \
  --with 'skfolio>=0.9,<1' \
  --with 'PyPortfolioOpt>=1.5.6,<2' \
  git+https://github.com/JamesbbBriz/open-family-office.git
```

Check what is actually available:

```bash
ofo doctor
ofo providers
```

Provider code is not a claim of live entitlement or successful authentication.

## 8. Developer checkout

If you want to extend Skills, workflows, providers or quantitative engines:

```bash
git clone https://github.com/JamesbbBriz/open-family-office.git
cd open-family-office
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[analytics,documents]'
python -m unittest discover -s tests -v
```

The source fallback remains `python scripts/ofo.py ...`, but installed users should use `ofo`.
