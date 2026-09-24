# Show HN submission

## Title

```text
Show HN: Open Family Office – local-first family wealth research for AI agents
```

## Body

I studied Asset Management rather than Computer Science, and while moving deeper into AI engineering I kept coming back to one problem: most personal-finance tools model the portfolio, not the household around it.

A household may own a home, a private business, super/pension, cash and public securities. Its income may be stable, variable or a one-off liquidity event. Those things affect liquidity and risk capacity even when they are not tradable portfolio positions.

So I built Open Family Office, an MIT-licensed local-first toolkit that models:

- assets and liabilities;
- recurring vs one-off income;
- spendable liquidity and cash runway;
- ownership look-through;
- life-event / stress scenarios;
- a separately declared liquid investment sleeve;
- optional Monte Carlo and optimization research.

The architecture is intentionally split: deterministic Python does the financial arithmetic; Agent Skills guide the workflow; MCP is an optional read-only interoperability layer.

You can try the synthetic demo without cloning or entering private data:

```bash
uvx --from git+https://github.com/JamesbbBriz/open-family-office.git ofo demo --open
```

Repo:
https://github.com/JamesbbBriz/open-family-office

The part I am most interested in feedback on is where the boundary should sit between a household model and a portfolio model. What would you expect a useful personal “family office” to understand that ordinary portfolio software usually misses?

## Posting notes

- Submit from the project author account.
- Do not coordinate votes.
- Be present for the first few hours and answer technical questions directly.
- If PyPI and the hosted demo are live, replace the Git install command with the PyPI install path and add the demo link.
