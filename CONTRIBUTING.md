# Contributing

Start with `python scripts/ofo.py demo`, then `python -m unittest discover -s tests -v`.
Use only fictional or demonstrably redistributable data. Do not attach private statements or paste secrets.

Useful first contributions: a new synthetic household case, a failed edge-case test, clearer onboarding,
a translation, or a narrowly scoped adapter proposal. Keep methodology changes separate from runtime adapters.
One business rule lives in `agent/workflows/` or `agent/methodology/`, not several subtly different host prompts.

For financial changes provide the assumption, worked example, test and failure boundary. An attractive
report is not evidence of correct mathematics. Avoid adding model dependencies to deterministic calculations.
Provider PRs need source terms, provenance, identifier/date/unit behaviour, fixtures and an authorised smoke test.
Do not mark a connector implemented merely because its prompt or specification exists.

Run the test suite and `python scripts/release_check.py`. No external API keys are required for CI.
Describe which checks ran and which did not. Contributions are submitted under this repository's MIT licence.

Public discussion should be constructive and specific. No personal financial advice requests, solicitation,
paid investment promotions or exposure of private financial records. Maintainers can remove unsafe content.
