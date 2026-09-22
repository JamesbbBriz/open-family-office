# ofo-dashboard

## Goal

Build an evidence-aware private financial dashboard.

## Procedure and controls

Run doctor for analytics and Plotly availability. Require the household file; optional policy, scenario, liquid-return and simulation JSON must be reviewed separately. All monetary research inputs share the household base currency. Run `python scripts/ofo.py dashboard <household> --out <outside-repo/report-new.html>` and add `--policy`, repeatable `--scenario`, `--returns`, `--simulation` only for existing approved files. Refuse overwrite and inside-repo output. Missing research inputs stay empty. Explain the distinction between present balance sheet, future cash budget and investment simulation. Check the report in a browser; disclose that private data is embedded and must not be published. Precomputed scenario switching is not a real-time financial calculation engine.

## Completion

Return the actual calculation/output location, the methods executed and their limitations. Do not claim installation, live connection or host validation merely because source code exists.
