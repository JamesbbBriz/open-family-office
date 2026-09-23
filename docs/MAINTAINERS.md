# Maintainer guide

This document describes the review and merge policy for Open Family Office.

## Current maintainer model

The repository is currently maintained primarily by **@JamesbbBriz**.

`.github/CODEOWNERS` assigns the repository to the maintainer so external pull requests automatically request review.

## Main-branch ruleset

The repository should protect the default branch with a GitHub Ruleset targeting `main`.

Recommended settings:

### Pull requests

- **Require a pull request before merging:** ON
- **Required approvals:** 0 for now
- **Require review from Code Owners:** OFF for now
- **Require conversation resolution before merging:** ON

Why zero approvals? GitHub does not let a pull-request author approve their own PR. With only one primary maintainer, requiring one approval would block maintainer-authored PRs unless an administrative bypass is used.

When a second trusted maintainer is added:

- set required approvals to **1**;
- enable **Require review from Code Owners**;
- enable dismissal of stale approvals when the diff changes materially.

### Required status checks

Require these checks from the `CI` workflow:

- `Python 3.11`
- `Python 3.12`
- `Python 3.13`
- `Wheel smoke`
- `Web`

The optional-native integration job is intentionally manual and should not block normal pull requests.

### History / destructive changes

Recommended:

- **Block force pushes:** ON
- **Block branch deletion:** ON
- **Require linear history:** optional; squash merging already keeps `main` clean

## Merge policy

Preferred merge method: **Squash and merge**.

Before merge:

1. CI is green.
2. Review conversations are resolved.
3. Financial assumptions and failure boundaries are documented when relevant.
4. No real household data is present.
5. Generated web artifacts are reproducible.
6. Provider claims match actual validation status.

Do not bypass failing checks just because a PR is documentation-adjacent; documentation and generated artifacts are covered by repository hygiene tests.

## Review priorities

Review in this order:

1. privacy / credentials / unintended network or write side effects;
2. accounting and financial invariants;
3. deterministic tests and failure handling;
4. Agent workflow consistency;
5. provider provenance and licensing;
6. UX and documentation.

## External contributors

Anyone may open an issue or PR. CODEOWNERS requests the maintainer automatically.

Use:

- `good first issue` for narrow, self-contained tasks;
- `help wanted` for larger community work.

Do not assign write access merely to make approvals easier. Add collaborators only after repeated trusted contributions.

## Release policy

Public releases should:

- correspond to a version in `pyproject.toml`;
- include clear install instructions;
- state validation status honestly;
- avoid claims of live integrations that were not tested;
- keep release assets synthetic / redistributable.

## Security

Sensitive vulnerabilities and private financial data must not be posted in a public issue.

See [SECURITY.md](../SECURITY.md).
