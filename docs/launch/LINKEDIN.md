# LinkedIn launch post

## Main post

I studied Asset Management, but I’ve been moving deeper into AI engineering.

So I built the project that connects the two.

Most portfolio tools begin with:

> What do you own?

A Family Office has to ask a much wider set of questions:

> What do you own?
> What do you owe?
> Where does income come from?
> How durable is that income?
> What is actually liquid?
> What future obligations matter?
> What are you exposed to through property, private businesses and wrappers?
> What changes if a business is sold, someone stops working, or a major purchase happens?

That became **Open Family Office** — an MIT-licensed, local-first open-source toolkit for household wealth research.

It combines:

- household balance-sheet and cash-flow modelling;
- recurring vs one-off income;
- liquidity and runway;
- ownership look-through;
- scenario analysis;
- a separately declared liquid investment sleeve;
- optional quantitative research;
- portable Agent Skills;
- optional read-only MCP.

The implementation principle is simple:

```text
User intent
   ↓
Agent Skill
   ↓
Canonical workflow
   ↓
Deterministic Python
   ↓
Plain-language explanation
```

The AI is not supposed to “mentally calculate” the money.

The project is also deliberately not a broker, bank login automation tool, or autonomous adviser.

Repository:
https://github.com/JamesbbBriz/open-family-office

Synthetic demo:

```bash
uvx --from git+https://github.com/JamesbbBriz/open-family-office.git ofo demo --open
```

I’m especially interested in feedback from people working in wealth management, financial planning, fintech and agent tooling: what important household-level concept do portfolio products usually fail to model?

## Suggested media

Use `assets/social-preview.png` as the first image.

Optional second image: `assets/readme/overview.png`.
