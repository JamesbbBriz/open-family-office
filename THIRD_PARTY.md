# Third-party components and acknowledgments

Project-authored code, workflows and documentation are MIT licensed under `LICENSE`. That license does not replace third-party notices or grant financial-data use rights.

## Bundled in the standalone HTML

- Plotly.js 3.3.1, supplied by installed plotly.py 6.5.2. Its upstream bundle copyright/license headers remain in the embedded script. See `vendor/licenses/plotly-js-MIT.txt` and the copied Plotly distribution notices.
- Compiled Tailwind CSS 4.1.10 utilities, theme/preflight output. The upstream license is copied to `vendor/licenses/tailwindcss-LICENSE.txt`.

The HTML uses system fonts, not bundled font files. It has no CDN dependencies. The full Plotly bundle includes its upstream internal dependency notices; retain them when minifying or redistributing. `THIRD_PARTY_NOTICES.txt` is a plain-text redistribution companion.

## Installed separately, not vendored

NumPy, pandas, SciPy, scikit-learn, skfolio, PyPortfolioOpt, yfinance, pypdf, ofxparse, MCP Python SDK and OpenBB are declared as dependency groups or a separate environment. Their own licenses and transitive dependencies apply when installed. Pinning a package or installing OpenBB does not grant exchange/provider data licenses, brokerage access or resale rights.

## Design references, not copied products

MadsLorentzen/ai-job-search informed profile-first, thin-pointer workflows. Wealthfolio/Ghostfolio informed product and data-provider considerations. Addepar informed entity/position modeling concepts. Their application code and data collections are not included. This project is independent and not endorsed by those maintainers or service providers.

## daisyUI MIT source-derived subset (v0.3 UI)

Button, card, badge and input source patterns are modified from saadeghi/daisyui. Copyright (c) 2020 Pouya Saadeghi. Full notice: vendor/licenses/daisyui-MIT.txt. Upstream blob references: vendor/daisyui/README.md. This is not the separately sold daisyUI Charts pack.
