# One-time actions that require account / repository settings access

Everything that can live in code is already represented by repository files. These are the remaining clicks that cannot be completed by the current repository connection.

## A. GitHub repository About

Repository home → About → gear icon.

### Description

```text
Local-first open-source family wealth research for people and AI agents: cash flow, asset allocation, scenarios, ownership look-through and more.
```

### Website

After Pages is live:

```text
https://jamesbbbriz.github.io/open-family-office/
```

### Topics

```text
family-office
family-finance
wealth-management
personal-finance
asset-allocation
financial-planning
portfolio-management
fintech
ai-agents
agent-skills
agentic-ai
local-first
python
mcp
monte-carlo
risk-management
open-source
open-source-finance
```

## B. Social preview

Repository → Settings → General → Social preview.

Upload:

```text
assets/social-preview.png
```

## C. Protect main

Repository → Settings → Rules → Rulesets → New branch ruleset.

Use:

```text
Name: Protect main
Enforcement: Active
Target: main
```

Enable:

- Require a pull request before merging
- Require conversation resolution
- Require status checks before merging
- Block force pushes
- Block deletions

Required checks:

```text
Python 3.11
Python 3.12
Python 3.13
Wheel smoke
Web
```

Keep required approvals at **0** while there is only one primary maintainer. Once a second trusted maintainer exists, change to 1 approval and require Code Owner review.

## D. GitHub Pages

Repository → Settings → Pages.

Set:

```text
Source: GitHub Actions
```

Then:

```text
Actions → Deploy Demo to GitHub Pages → Run workflow
```

Expected URL:

```text
https://jamesbbbriz.github.io/open-family-office/
```

## E. GitHub Discussions

Repository → Settings → General → Features → Discussions.

Enable Discussions.

Recommended categories:

- Announcements
- General
- Ideas
- Q&A
- Show and tell

Ready-to-post material is in [GITHUB-DISCUSSIONS.md](GITHUB-DISCUSSIONS.md).

## F. PyPI pending Trusted Publisher

Sign in:

```text
https://pypi.org/manage/account/publishing/
```

Create pending publisher:

```text
PyPI project name: open-family-office
GitHub owner: JamesbbBriz
Repository: open-family-office
Workflow: publish.yml
Environment: pypi
```

Then publish the already-prepared Draft Release:

```text
GitHub → Releases → Open Family Office v0.5.1 → Edit → Publish release
```

The release event automatically runs `Publish PyPI + MCP Registry`: PyPI is published first, then the MCP Registry metadata.

If the draft is not visible for any reason, `Actions → Publish PyPI + MCP Registry → Run workflow` remains the fallback.

No PyPI token or MCP registry secret is required.

## G. External posts

These platforms require the author's own account/session and are not writable through the current tools:

- Hacker News / Show HN
- LinkedIn
- X
- Reddit
- Product Hunt

Final copy is already in this launch directory.
