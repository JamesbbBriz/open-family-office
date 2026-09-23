# Contributing to Open Family Office

Thanks for helping make Family Office methods more accessible.

Open Family Office combines household accounting, cash-flow modelling, Agent workflows, data adapters and quantitative research. Because the project touches financial decisions, contributions need to be **reproducible, explicit about assumptions and safe with private data**.

## Start here

For a first contribution, look for:

- `good first issue` — narrow, testable tasks;
- `help wanted` — medium-sized design or implementation work.

Before implementing a larger change, comment on the issue with your proposed scope so work does not diverge.

## Never use real household data

Public issues, pull requests, fixtures and screenshots must use only:

- synthetic data created for this project; or
- data that is demonstrably safe and redistributable.

Do **not** commit:

- bank or brokerage statements;
- tax records;
- account identifiers;
- credentials or API keys;
- private Family Office workspaces;
- generated dashboards containing real household data.

See [SECURITY.md](SECURITY.md).

## Development setup

Python 3.12 is the recommended contributor version. CI also verifies Python 3.11 and 3.13.

```bash
git clone https://github.com/JamesbbBriz/open-family-office.git
cd open-family-office

python -m venv .venv

# macOS / Linux
. .venv/bin/activate

# Windows
# .venv\Scripts\activate

python -m pip install -e '.[analytics,documents]'
```

For web work:

```bash
npm ci --ignore-scripts --no-audit --no-fund
```

For all optional/native integrations:

```bash
python scripts/bootstrap.py --all
```

## Repository map

```text
src/open_family_office/   deterministic engine, CLI, integrations and quant tools
agent/workflows/          canonical financial procedures
agent/methodology/        domain interpretation rules
agent/schemas/            structured inputs
.agents/skills/           canonical portable user-facing Skills
.claude/skills/           thin Claude discovery wrappers
web/src/                  daisyUI / Tailwind / Plotly source
public/                   generated static site and synthetic demo
examples/                 synthetic reproducible fixtures
tests/                    accounting, integration, quant, CLI and web tests
```

## Architecture rules

### One source of truth

A business rule belongs in the canonical engine, workflow or methodology layer.

Do not copy slightly different versions of the same financial rule into:

- Claude prompts;
- Codex/Agent Skill wrappers;
- MCP tool descriptions;
- dashboard JavaScript.

Runtime-specific files should point to canonical logic rather than duplicate it.

### Python computes money

Use deterministic code for:

- accounting;
- cash-flow arithmetic;
- ownership consolidation;
- scenario mechanics;
- portfolio math;
- validation.

Agents may interview, plan, explain and summarize, but should not replace available deterministic calculations with mental arithmetic.

### Keep concepts separate

Do not silently collapse:

- net worth into spendable liquidity;
- one-off receipts into recurring income;
- pension/account wrappers into extra asset classes;
- private businesses into tradable securities;
- historical observations into expected returns;
- model output into facts.

## Contribution types

### Financial / accounting logic

A PR changing financial behaviour should include:

1. the assumption or invariant being changed;
2. a worked synthetic example;
3. deterministic tests;
4. the failure boundary / invalid input case;
5. documentation when user-visible behaviour changes.

An attractive chart is not evidence that the mathematics is correct.

### Agent Skills / workflows

User-facing Skills live under `.agents/skills/`.

- Keep Skills task-oriented.
- Put detailed financial procedures in `agent/workflows/`.
- Keep Claude wrappers thin.
- Do not add hidden side effects.
- End Skills with clear user-controlled next steps.

### Provider integrations

Provider PRs should include:

- official source/API documentation;
- identifier, date, unit and currency behaviour;
- licensing / redistribution assumptions;
- required environment-variable names;
- fixture-based contract tests;
- explicit network-off-by-default behaviour;
- a clear statement of what has and has not been live-verified.

Do not mark a provider “working” because a prompt or endpoint sketch exists.

### Quantitative methods

For optimization, simulation or statistical changes include:

- mathematical assumptions;
- constraints;
- deterministic or seeded tests;
- failure cases;
- explanation of what the output does **not** imply.

Do not present optimizer weights or Monte Carlo percentiles as guaranteed outcomes.

### UI / dashboard

For visual changes:

- keep the offline/private-data boundary;
- avoid runtime CDNs unless explicitly justified;
- preserve mobile layout;
- include before/after screenshots when useful;
- run browser arithmetic tests.

## Branches and commits

Suggested branch names:

```text
feat/...
fix/...
docs/...
test/...
chore/...
```

Small, purpose-specific PRs are easier to review than mixed refactors.

Commit messages do not need strict Conventional Commits, but concise prefixes such as `feat:`, `fix:`, `docs:` and `test:` are encouraged.

## Required checks before opening a PR

Run the checks relevant to your change:

```bash
python -m unittest discover -s tests -v
python scripts/ofo.py demo
python scripts/release_check.py
node tests/sandbox.test.cjs
npm run build
```

For documentation-only changes, the full suite will still run in GitHub Actions; you do not need to install every optional native provider locally.

In the PR description, state **which checks you actually ran** and which you did not.

## Pull request process

1. Open a focused PR against `main`.
2. Complete the PR template.
3. Let CI finish.
4. Address review comments and unresolved conversations.
5. Do not merge a red CI run.
6. Prefer squash merge for a clean project history.

`CODEOWNERS` automatically requests the maintainer for external PRs.

The repository currently has one primary maintainer, so it does **not** require one approving review for every PR yet: GitHub does not allow PR authors to approve their own pull requests. Once a second trusted maintainer exists, required approvals should be enabled.

See [docs/MAINTAINERS.md](docs/MAINTAINERS.md).

## Licensing

By submitting a contribution, you agree that it may be distributed under this repository's [MIT License](LICENSE).

## Community conduct

Be specific, evidence-led and respectful. Do not use repository discussions for:

- personalized financial-advice requests;
- investment solicitation;
- paid promotions;
- publishing private financial records.

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
