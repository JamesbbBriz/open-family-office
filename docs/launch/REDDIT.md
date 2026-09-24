# Reddit launch drafts

Do not cross-post the same wording into many communities on the same day. Adapt to each community's rules and be explicit that you are the author.

## r/opensource style

### Title

```text
I built an open-source, local-first “family office” toolkit that models the household around the portfolio
```

### Body

I’m the author of Open Family Office.

I originally approached this from an asset-management background. What bothered me about many portfolio tools is that they can be very detailed about securities while treating the rest of a household almost as an afterthought.

For example:

- a primary home increases net worth but may not help near-term liquidity;
- a private business can be both a large asset and a source of recurring income;
- selling that business should remove the asset and may stop future distributions;
- pension/super wrappers should not double-count the investments inside them;
- risk tolerance and actual financial capacity are different.

I built those ideas into a local-first Python toolkit with an offline dashboard, portable Agent Skills and an optional read-only MCP server.

There are no bank logins, no trading, and the public demo is synthetic.

Repo:
https://github.com/JamesbbBriz/open-family-office

Try without cloning:

```bash
uvx --from git+https://github.com/JamesbbBriz/open-family-office.git ofo demo --open
```

I’d value criticism of the data model and the boundary between “personal finance” and “family-office-style” modelling.

## r/SideProject style

### Title

```text
Open Family Office — I’m trying to make family-office methods usable as an open-source local toolkit
```

### Body

I built this partly as a bridge between my finance background and AI/software work.

The core idea is that portfolio allocation should sit inside a larger household model: assets, liabilities, recurring/one-off income, liquidity, ownership, goals and scenarios.

Instead of making the LLM responsible for calculations, the project uses deterministic Python and gives agents a small set of task-oriented Skills.

It is early, MIT licensed, and designed so users can keep the actual household workspace separate from the public code repository.

GitHub:
https://github.com/JamesbbBriz/open-family-office

I’m looking for feedback more than promotion — especially from people who have built planning, accounting, wealth-tech or local-first software.
