# Awesome-list / directory submission package

Only submit after the relevant distribution surface is actually live. Do not claim registry or PyPI availability before publication succeeds.

## 1. Official MCP Registry

No pull request is required.

The repository already contains:

```text
server.json
.github/workflows/publish.yml
```

The release workflow publishes through GitHub OIDC after PyPI succeeds.

Registry name:

```text
io.github.jamesbbbriz/open-family-office
```

## 2. punkpeye/awesome-mcp-servers

Before submitting, verify the repository's current contribution rules and any required server-quality badge.

Suggested entry:

```markdown
- [Open Family Office](https://github.com/JamesbbBriz/open-family-office) - Read-only local MCP tools for household balance sheets, cash flow, scenarios, ownership look-through and liquid-sleeve research. Python / local-first.
```

Suggested PR title:

```text
Add Open Family Office
```

Suggested PR body:

```text
Adds Open Family Office, an MIT-licensed local-first Python project with a read-only stdio MCP server. The server requires an explicitly authorized OFO_WORKSPACE and does not place trades, move money or perform bank logins.
```

## 3. Agent Skills directories

Open Family Office has portable canonical Skills under:

```text
.agents/skills/
```

For list-style repositories, submit the project or the most self-contained Skill rather than dumping all ten entries.

Recommended first Skill:

```text
ofo-overview
```

Suggested description:

```text
Builds a household-level financial overview across balance sheet, recurring/one-off income and spendable liquidity using deterministic Open Family Office CLI calculations.
```

### List-style bilingual entry

```markdown
| ofo-overview | Household balance sheet, income quality and liquidity review backed by deterministic Open Family Office calculations | Codex / Claude-compatible Agent Skills | [GitHub](https://github.com/JamesbbBriz/open-family-office/tree/main/.agents/skills/ofo-overview) |
```

## 4. Finance / privacy-first tool lists

Suggested description:

```text
Open Family Office — MIT-licensed, local-first family wealth research toolkit covering assets, liabilities, recurring/one-off income, liquidity, ownership, scenarios and a separate liquid investment research sleeve.
```

Use the GitHub repository as the canonical link until the hosted demo is enabled.
