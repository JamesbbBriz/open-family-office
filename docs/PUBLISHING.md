# Publishing and distribution

Open Family Office has three public distribution surfaces:

1. **PyPI** for the installable Python package and CLI.
2. **Official MCP Registry** for discovery by MCP-compatible clients.
3. **GitHub Pages** for the synthetic public demo.

The repository contains the automation for all three. Only the account-level setup that cannot be expressed in repository files is manual.

## 1. PyPI Trusted Publishing

Workflow:

```text
.github/workflows/publish.yml
```

The workflow builds a wheel and source distribution, checks metadata, smoke-tests the installed CLI, validates `server.json`, publishes to PyPI through OIDC, waits for PyPI propagation, then publishes MCP metadata through GitHub OIDC.

No long-lived PyPI API token is required.

### One-time PyPI setup

Sign in to PyPI and create a **pending Trusted Publisher** for a new project.

Use these exact values:

| Field | Value |
|---|---|
| PyPI project name | `open-family-office` |
| GitHub owner | `JamesbbBriz` |
| Repository | `open-family-office` |
| Workflow | `publish.yml` |
| Environment | `pypi` |

PyPI page:

```text
https://pypi.org/manage/account/publishing/
```

A pending publisher does not reserve the package name until the first successful upload.

### First publish

v0.5.1 is prepared as a **Draft GitHub Release**. After the pending PyPI Trusted Publisher exists:

```text
GitHub → Releases → Open Family Office v0.5.1 → Edit → Publish release
```

Publishing the draft automatically triggers `Publish PyPI + MCP Registry`.

The workflow-dispatch button remains available as an operator fallback, but the normal release path is to publish the prepared GitHub Release.

### Release invariant

These versions must stay identical:

- `pyproject.toml`
- `src/open_family_office/__init__.py`
- `package.json`
- top-level `server.json`
- `server.json.packages[0].version`

`tests/test_release_metadata.py` enforces this.

## 2. Official MCP Registry

The MCP identity is:

```text
io.github.jamesbbbriz/open-family-office
```

Registry metadata:

```text
server.json
```

The registry package points at the PyPI distribution and uses `uvx`.

Conceptually, clients run:

```bash
OFO_WORKSPACE=/absolute/private/path \
uvx --with 'mcp>=1.10,<2' open-family-office mcp
```

The MCP server is read-only and requires the user to explicitly choose a private workspace.

PyPI ownership verification is carried by this hidden README marker:

```text
mcp-name: io.github.jamesbbbriz/open-family-office
```

The publishing workflow authenticates to the official MCP Registry with GitHub Actions OIDC; no MCP registry secret is stored.

## 3. GitHub Pages demo

Prepared workflow:

```text
.github/workflows/pages.yml
```

The deployment uploads the already-generated `public/` directory. CI separately verifies that rebuilding the site produces no uncommitted differences.

### One-time Pages setup

On GitHub:

```text
Settings → Pages → Build and deployment → Source → GitHub Actions
```

Then run:

```text
Actions → Deploy Demo to GitHub Pages → Run workflow
```

After the first successful deployment, changes under `public/**` deploy automatically from `main`.

Expected default URL:

```text
https://jamesbbbriz.github.io/open-family-office/
```

Do not add a custom domain until the domain is owned and configured.

## Release checklist

Before creating a future GitHub Release:

1. update all version-bearing files;
2. run `python -m unittest discover -s tests -v`;
3. run `python scripts/release_check.py`;
4. make sure `server.json` validates;
5. merge through green CI;
6. create a GitHub Release tagged exactly `v<version>`.

The release event then handles PyPI and MCP publication.

## Security model

- PyPI uses short-lived OIDC credentials.
- MCP Registry uses GitHub OIDC.
- Pages uses GitHub's Pages OIDC deployment flow.
- No publishing API tokens belong in the repository.
- Publishing workflows are intentionally separate from pull-request CI.
