# Launch drafts — publish only after the repository is actually public

Replace `REPO_URL` and `DEMO_URL` with verified live destinations. Omit DEMO_URL when no public demo is hosted.
Do not claim real host acceptance, integrations, users or performance that has not been measured.

## LinkedIn — founder / applied-AI angle

I studied Asset Management, and I've been building AI workflows.

The project I wanted to build wasn't another “which stock should I buy?” chatbot.
It started with a different question: what does the household's whole financial picture look like?

A home, a private business, retirement assets, a mortgage and uncertain income don't fit neatly into a ticker list.
A business sale is a good example: cash comes in, but an existing asset disappears and ongoing distributions may stop.

I'm sharing Open Family Office, an open-source workflow kit for that kind of analysis.
The agent structures the interview and evidence. Small Python tools handle the arithmetic.
The current release includes cash budgets, disposal scenarios, numerical research and a 13-chart offline dashboard. All public inputs and return histories are synthetic.

There is no trading, bank sync or claim of an optimal portfolio. The numerical demo runs without an API key.

I'd value feedback on one question: which real household situation does this model fail to represent clearly?
Please use fictional numbers rather than sharing personal statements.

Repository: REPO_URL

## X — single post

A business sale creates cash, but it can also remove an asset and recurring income.

I built Open Family Office: open-source agent workflows for household wealth, cash flow and explicit scenarios.
No stock picks. The synthetic Python demo needs no API key.

REPO_URL

## X — optional 4-part thread

1/ A portfolio list isn't a household balance sheet. Your home, debt, pension, business and future payments
can matter more than which stocks you hold. That's the starting point for Open Family Office.

2/ The first demo sells a fictional business. It receives the net cash, removes the old equity value and stops
its distributions. Those three changes belong in one scenario — not three unrelated reports.

3/ It's mostly workflow instructions, methodology and templates, with a small deterministic Python layer.
The agent explains; it doesn't invent prices, calculate tax or place trades. Private files stay outside the code repo.
Cloud-model processing still needs an explicit privacy decision.

4/ v0.2 adds numerical research, 13 adapter implementations and an interactive offline dashboard. Adapter contract tests are not live-provider validation. Optional native SDK and host acceptance remain explicit gates. No hosted product is shipped.
I'm looking for reproducible edge cases and honest modelling criticism, not personal financial records.
REPO_URL

## Show HN

Title: Show HN: Open Family Office – agent workflows for household cash-flow scenarios

I built a local-first workflow kit around household balance sheets rather than stock selection.
It handles manual multi-asset records, dated obligations, recurring versus one-off receipts, and explicit scenarios.

The example I find most useful is selling a private business: sale cash replaces equity value and dependent
income stops. The underlying calculation is small Python code you can inspect and run without an API key.

The interactive demo switches between precomputed synthetic cases. Agent skills handle interviewing and
interpretation in a user-provided host. The report now includes separately scoped numerical research. This is an early release: no bank sync, live prices or trading in the demo; optional SDK/live-service acceptance is documented honestly.

Run: `python scripts/hh.py demo`
Repository: REPO_URL
Public demo, only when deployed and verified: DEMO_URL

I'd especially appreciate criticism of the household model and its failure cases. Please use synthetic data.

## Technical community / Reddit-style draft

Title: I built a household cash-flow workflow for coding agents — looking for modelling edge cases

I'm the author. This is a self-promotion/feedback post, so I'll keep the scope concrete.
The project models assets, debt, dated payments and recurring/one-off receipts, with a tiny deterministic Python engine.
It is not a trading bot or an investment-product recommender.

The part I'd like feedback on is the business-sale bridge: stop the relevant income, remove existing equity,
and add net sale cash without counting the same wealth twice. A synthetic example and tests are included.

No signup or financial document upload is needed to try the demo. REPO_URL
Which edge case would you use to break this model?

Only use this draft where current community rules permit it. Do not paste it into unrelated communities.

## 中文短帖

我做了一个开源的家庭资产管理 Agent 工作流，名字叫 Open Family Office。

它不回答“明天买哪只股票”，而是先看整个家庭：资产、负债、收入来源、未来付款和现金能否接得上。
例如卖掉一家企业，不能只把出售款加进去，还要移除原企业资产，并考虑经营收入停止后的影响。

目前包含 Skills、方法论、Python 计算、量化研究及 13 张交互图表。公开演示全部是虚构数据，
打开离线 HTML 不需要 API Key，也不会连接银行。13 个数据源适配器有代码与样例测试，但真实 API 授权、
部分原生 SDK 和宿主端到端仍待验证；没有 Hosted 服务或自动交易。

目前最想收集的不是私人账单，而是“你认为这个模型遗漏了哪类家庭财务情况”的反馈。
仓库：REPO_URL
