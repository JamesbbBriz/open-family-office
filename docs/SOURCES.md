# Source and design references

Checked/read on 2026-09-21. These references explain specific design choices; they do not certify the
software, provide upstream endorsements or imply that an integration is implemented.

## Agent packaging and inspiration
- AI Job Search README: https://github.com/MadsLorentzen/ai-job-search
  Workflow-oriented local repo, profile onboarding and an explicit warning about private data in public forks.
- AI Job Search AGENTS.md: https://github.com/MadsLorentzen/ai-job-search/blob/master/AGENTS.md
  Single-canonical-specification / thin-pointer design. No source code or artwork from that repository is copied here.
- Agent Skills specification: https://agentskills.io/specification
  SKILL.md with required name/description frontmatter and optional referenced resources.
- Codex skill documentation: https://developers.openai.com/codex/skills/
  Repository `.agents/skills`, explicit `$` invocation and file-based skill discovery.
- Claude Code skills: https://code.claude.com/docs/en/skills
  Project `.claude/skills` and slash-command invocation. Runtime acceptance remains separately untested.

## Financial source candidates, not bundled adapters
- RBA tables: https://www.rba.gov.au/statistics/tables/
- ABS Data API guide: https://www.abs.gov.au/statistics/application-programming-interfaces-apis/data-api-user-guide
- SEC EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- FRED API: https://fred.stlouisfed.org/docs/api/fred/

## Publishing and product boundary
- GitHub social preview: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview
  Recommended preview 1280×640 and under 1 MB; included preview is rendered from the bundled synthetic social-card HTML.
- GitHub CLI repo creation: https://cli.github.com/manual/gh_repo_create
  Used by the operator-run publishing helper. No GitHub write was performed to build this release.
- Show HN guidance: https://news.ycombinator.com/showhn.html
  A project should be tryable, not merely an announcement/landing page. The offline demo supports that.
- ASIC RG 255: https://asic.gov.au/regulatory-resources/find-a-document/regulatory-guides/rg-255-providing-digital-financial-product-advice-to-retail-clients/
  Digital financial-product advice needs substantive scoping. A disclaimer or local-first/open-source label
  is not a legal exemption. This kit excludes product recommendations and execution, but does not claim legal clearance.

## Build-supply-chain references
CI action references were read through the GitHub connector:
`actions/checkout` tag v4 resolved to `11d5960a326750d5838078e36cf38b85af677262`;
`actions/setup-python` tag v5 resolved to `a26af69be951a213d495a4c3e4e4022e16d87065`.
Pinning is not a guarantee of security; review dependency updates. Remote CI has not run in this delivery environment.
