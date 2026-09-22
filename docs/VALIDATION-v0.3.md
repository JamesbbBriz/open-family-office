# Open Family Office v0.3 validation — 2026-09-21

## What was actually exercised

- Python regression suite: 131 tests, 127 passed, 4 explicitly skipped; no failures. The skips remain native skfolio, PyPortfolioOpt, OFX and MCP dependencies that are not installed here.
- Browser cash arithmetic: 31 Node assertions passed. These check one-off receipts, inclusive business-income stop dates, cent reconciliation, expense escalation, funding gaps and invalid input rejection.
- Browser rendering/interaction: 71 checks passed using Chromium and Playwright, including all 14 chart areas, six views, four original household cases, custom cash calculation, reset, JSON export, language/theme, print hooks and 320/390/768px widths.
- No console/script errors or external resource requests were recorded in that browser run. The browser context was set offline; scripts, styles and data were embedded in each HTML.
- A separately started local HTTP server returned byte-identical index.html and demo.html, verified with Python urllib.

## Important test boundary

This environment's managed Chromium blocks direct file:// and localhost navigation with ERR_BLOCKED_BY_ADMINISTRATOR. To render and test, Playwright loaded the **exact built HTML bytes** using page.set_content into fresh, offline browser contexts. That tests rendering and interactions without network, not navigation through a publicly deployed site. Relative link targets were checked against packaged files; a public URL and Safari/iOS native file-preview flow were not tested.

The output is constructed as two standalone documents suitable for local HTML viewing or static hosting, but deployment itself has not occurred. No domain or repository was registered.

## Unchanged backend limits

This is a UI/name/packaging update, not evidence that optional dependencies or remote providers became operational. Full npm/pip resolver runs, native optional SDK execution, all live financial APIs and actual Agent/MCP host integration remain unverified. The daisyUI UI uses an attributed, modified upstream MIT component source subset compiled with an available Tailwind compiler, not a silently simulated full npm installation.

## Reproduce

```bash
python -m unittest discover -s tests -v
node tests/sandbox.test.cjs
python scripts/release_check.py
# Development environment with Playwright and Chromium:
python tests/browser_smoke.py
```

Browser assertions and limits are recorded in web-validation-v0.3.json. Screenshots in assets/ are browser renders of synthetic examples, not concept mockups. Receipt defaults and computed sample amounts are demonstrations, not user records.
