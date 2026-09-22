# Dependencies
The complete one-shot installer is `python scripts/bootstrap.py --all`.
The offline accounting commands need only Python. Optional dependencies are lazy-loaded.
`analytics` contains the numerical/chart implementation exercised in this delivery.
`quant`, `market`, `documents`, and `mcp` enable their real external-library bridges.
OpenBB is intentionally in a second environment because it has a broad provider dependency tree.
Version ranges in `pyproject.toml` are NOT a tested universal lockfile. The installer exports the actual resolved versions into `~/.open-family-office/install-*.txt` and runs local tests. OS-specific solver wheels, API entitlements, and future package compatibility are not guaranteed.
Use Python 3.11 or 3.12 for the first complete OpenBB install; the core/analytics were also exercised under 3.13 in this delivery.
