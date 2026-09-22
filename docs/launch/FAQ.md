# FAQ

**Is this a stock recommender?** No. It models household wealth and cash needs; optional investment research uses a separate liquid proxy universe and explicit assumptions.

**Is the dashboard real?** It is a functional standalone HTML with real Tailwind and Plotly. Its public data is synthetic. Scenarios are precomputed; private reports are regenerated using the Python tool.

**Are all data sources connected?** Thirteen adapters have source and contract tests. No live credentials are shipped and no live provider validation is claimed. Native optional libraries need installation and acceptance tests.

**Does one-command setup mean zero configuration?** No. It installs declared packages, builds and tests. Legitimate API keys, account entitlements, input mapping, accepted private data and host permission remain separate.

**Can I publish my report?** It embeds its data. Keep private reports outside public repositories. Local-first is not encryption and does not prevent authorized cloud-agent processing.

**What is not done?** Hosted accounts, automatic bank/broker syncing, transaction execution, general-purpose PDF-to-verified-facts, complete N-PORT parsing, real tax/legal/suitability determinations and end-to-end production hardening.
