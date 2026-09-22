# Release checklist

Run the clean-checkout tests, dashboard builder and `python scripts/release_check.py`. Compare [validation](docs/VALIDATION.md) with any claims in README, release notes, screenshots and CV entries. Optional skipped tests must remain visible; a local run is not a green remote GitHub Actions badge.

Verify every household, return matrix and screenshot in the release is synthetic. Do not include private folders, `.env`, credentials, account statements, venvs, node_modules, user output or paid data. This allowlist checker is a safeguard, not exhaustive PII/security certification.

Check third-party notices, static relative links, metadata and the version. Rebuild `MANIFEST.sha256` after the final changes, excluding the manifest itself, and validate archive extraction. Confirm the standalone report requests no external assets and its displayed values reconcile with core outputs.

Before public use, validate the full native installer, actual agent/MCP host and legitimately authorized providers. Record any failed/unverified service. Keep public announcements factual. Publishing scripts must remain dry-run by default and private-first; creating a public repository requires an explicit human choice.
