# Validation record — v0.2.0, 2026-09-21

## Executed locally

Core accounting/cash-flow/FX/disposal regression tests; synthetic request/response contract tests for thirteen provider adapters; locally installed NumPy/SciPy/scikit-learn research calculations; a 2,000-path, 120-month fixed-seed synthetic liquid-sleeve simulation; graph/exposure invariants; basic native PDF extraction test; compiled Tailwind 4.1.10 and Plotly.js 3.3.1 report generation.

Chromium rendered the standalone HTML contents at desktop and mobile sizes. Tests switch all five tabs, all thirteen charts, sale scenario, light/dark and Chinese controls. JavaScript errors, external HTTP requests and horizontal overflow are checked. The container blocks file:// navigation by browser policy, so the exact standalone HTML contents were loaded through Playwright set_content. Direct double-click file:// launch was not independently exercised here.

## Not executed / not proved

Complete package-registry installation, clean-OS resolver compatibility, a transitive lockfile, native skfolio/PyPortfolioOpt/yfinance/OpenBB/ofxparse/MCP tool execution, an actual agent or MCP host handshake, live external financial API authentication/results, provider rights/entitlements, production deployment, external CI, a formal security/financial audit or any real investment outcome.

Optional native tests skip explicitly when their packages are absent. Mocked SDK/subprocess tests are contracts, not native results. The public report has no real household records or market history. Monte Carlo parameters and historical return sequences are fictional. Generated research is in-sample/assumption-dependent, not a calibrated forecast.

## Reproduce

```bash
python -m unittest discover -s tests -v
python scripts/build_dashboard.py
python scripts/hh.py demo
python scripts/hh.py doctor
python scripts/release_check.py
```

Browser checks additionally require Playwright and Chromium, neither needed to view the standalone report. Use `python scripts/render_assets.py`. Final measured results are stored in `evals/validation-results.json` and the release test log, not a fabricated hosted-CI badge.

## Recorded test run

123 unit/regression/contract tests were discovered: **119 passed, 4 explicitly skipped, 0 failed**. The skipped groups require native skfolio, PyPortfolioOpt, ofxparse and MCP packages. This number includes synthetic adapter contracts, not thirteen live endpoint successes.

The browser run rendered 13 charts, checked all five mobile views with no horizontal page overflow, reconciled all four cash-curve end values with the Python outputs, exercised JSON export, printing, theme and core language controls, and reported zero JavaScript errors or external HTTP requests. Tests ran on Linux/Python 3.13.5; other operating systems are not claimed validated.
