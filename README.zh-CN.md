<p align="center">
  <img src="assets/readme/logo-family4.png" width="300" alt="Open Family Office 四口之家 Logo">
</p>

<h1 align="center">Open Family Office</h1>

<p align="center"><em>把 Family Office 的方法和工具，开放给愿意掌控自己数据的人。</em></p>

<p align="center">
  <a href="https://github.com/JamesbbBriz/open-family-office/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/JamesbbBriz/open-family-office/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <img alt="Version" src="https://img.shields.io/badge/version-v0.5.1-2f824d">
  <img alt="Python" src="https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white">
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-2f824d"></a>
  <img alt="Local-first" src="https://img.shields.io/badge/local--first-yes-3b7f5b">
  <img alt="Agent Skills" src="https://img.shields.io/badge/agent%20skills-10-4c8c68">
  <img alt="MCP Optional" src="https://img.shields.io/badge/MCP-optional-d3a84a">
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="docs/QUICKSTART.md">快速开始</a> ·
  <a href="docs/AGENT-UX.md">Agent UX</a> ·
  <a href="docs/DATA-MODEL.md">数据模型</a> ·
  <a href="docs/INTEGRATIONS.md">集成说明</a> ·
  <a href="ROADMAP.md">Roadmap</a>
</p>

---

**你的投资组合，不等于你的全部财务生活。** Open Family Office 是一个本地优先、开源的家庭财富研究工具箱，让人和 AI Agent 一起理解资产、负债、持续与一次性收入、流动性、所有权、目标、情景变化，以及单独声明的流动投资研究组合。

它**不是 SaaS 账户、券商，也不是自动投顾**。Ownership Look-through、Monte Carlo、资产配置优化、Provider Adapters 和可选 MCP 等高级能力都保留，但默认使用体验保持简单、任务导向。

## 30 秒体验

安装了 [uv](https://docs.astral.sh/uv/) 后：

```bash
uvx --from git+https://github.com/JamesbbBriz/open-family-office.git ofo demo --open
```

Synthetic Demo 不需要 API Key、模型账号、联网请求，也不需要输入真实家庭资料。

## 安装一次，数据留在自己手里

```bash
uv tool install git+https://github.com/JamesbbBriz/open-family-office.git

ofo init ~/FamilyOffice
cd ~/FamilyOffice

ofo status
ofo overview --format markdown
ofo dashboard --out reports/review.html --open
```

`ofo init` 会建立私人 workspace，并把 portable agent kit 一起装进去。之后可以直接把这个文件夹用 Claude Code / Codex / 其他 file-aware Agent 打开并使用 **ofo-start**，也可以完全只用 CLI。

## 看的是整个家庭，不只是 Portfolio

<table>
  <tr>
    <td width="50%"><img src="assets/readme/overview.png" alt="Open Family Office 家庭总览"></td>
    <td width="50%"><img src="assets/readme/scenarios.png" alt="Open Family Office 情景分析"></td>
  </tr>
  <tr>
    <td align="center"><sub><b>家庭总览</b> — 净资产、可用流动性、资产结构和现金 runway。</sub></td>
    <td align="center"><sub><b>情景实验室</b> — 卖公司、收入中断和显式压力假设。</sub></td>
  </tr>
</table>

系统刻意把这些概念分开：

- **净资产** vs. **真正可动用的流动性**；
- **持续收入** vs. **一次性到账**；
- **当前资产负债表** vs. **未来现金预算**；
- **非流动家庭财富** vs. **流动投资研究**；
- **事实与证据** vs. **假设与模型输出**。

房子、私人企业、锁定养老金不会被偷偷当成“可以每天调仓的股票”。

## Skill 才是主要的 Agent 使用体验

| Skill | 用户真正想做的事 |
|---|---|
| **ofo-demo** | 先看看项目能做什么 |
| **ofo-start** | 建立第一份私人家庭财务模型 |
| **ofo-update** | 加入新账单、估值或家庭变化 |
| **ofo-overview** | 看清资产负债、收入质量和流动性 |
| **ofo-plan** | 建立 Investment Policy 和配置框架 |
| **ofo-scenario** | 模拟失业、卖公司、房价下跌、大额消费等 |
| **ofo-research** | 主动使用 Provider、穿透分析和量化研究 |
| **ofo-dashboard** | 生成私人离线 Dashboard |
| **ofo-review** | 回顾以前的判断、假设和结果 |
| **ofo-doctor** | 检查安装、Skill、Provider 和 MCP |

```text
用户意图
   ↓
目的明确的 Skill
   ↓
Canonical financial workflow
   ↓
确定性的 ofo CLI / Python
   ↓
Agent 用自然语言解释
```

**Skill 是 UX，Workflow 是金融业务实现，CLI 是确定性执行核心，MCP 是可选工具通道。**

升级 CLI 后：

```bash
ofo agent sync
```

没有被修改过的托管 Skill / Workflow 会安全升级；你自己改过的文件会被标记为 conflict 并**保留原样**。

## 私人 Workspace

```text
FamilyOffice/
├── household.json
├── evidence/
├── imports/
├── scenarios/
├── reports/
├── .ofo/
├── .agents/skills/
├── .claude/skills/
├── .claude/commands/
└── agent/
    ├── workflows/
    ├── methodology/
    ├── schemas/
    └── templates/
```

进入 workspace 后，CLI 会自动发现最近的 `.ofo/workspace.json`：

```bash
ofo validate
ofo overview
ofo scenario scenarios/business-sale.json
ofo allocation policy.json
ofo dashboard --out reports/review.html
```

Local-first 不等于自动加密，也不等于模型一定在本地运行。你明确允许云端 Agent 读取的文件仍可能发送给模型服务；私人 HTML Dashboard 本身也会嵌入数据。详见 [SECURITY.md](SECURITY.md)。

<details>
<summary><b>高级研究能力</b></summary>

### Household Engine

- 家庭可归属资产与负债；
- 固定持续、浮动持续和一次性现金流；
- 可使用流动性与锁定 / 非流动财富；
- 未来大额支出和现金 runway；
- 企业出售等资产替换事件；
- Ownership Look-through 与 Exposure；
- Investment Policy 和配置约束。

### Quant Research

```bash
ofo optimize returns.json --engine scipy --method min_variance
ofo simulate simulation.json
ofo lookthrough ownership.json
```

可选引擎包括 SciPy、skfolio 和 PyPortfolioOpt。量化结果始终依赖输入数据和假设，不会因为数学复杂就自动变成确定答案。

### Provider Layer

当前适配器覆盖 SEC EDGAR、FRED、RBA、ABS、OECD、IMF、CoinGecko、Yahoo/yfinance、OpenBB、Alpha Vantage、Finnhub、MarketData.app 和 MetalpriceAPI。

外部数据获取必须显式开启：

```bash
ofo providers
ofo fetch rba table \
  --query '{"table":"f01"}' \
  --allow-network \
  --out evidence/rba-f01.json
```

写了 Adapter 不代表已经拥有对应实时服务的授权或成功认证。

### 可选 MCP

MCP 不是使用项目的前提。需要标准 Tool Calling 时：

```bash
uv tool install --force \
  --with 'mcp>=1.10,<2' \
  git+https://github.com/JamesbbBriz/open-family-office.git

ofo mcp-config
```

stdio MCP 只读，并被限制在明确授权的 workspace 中。

</details>

## 项目结构

```text
src/open_family_office/   可安装的确定性引擎 + CLI
agent/workflows/          Canonical financial workflows
agent/methodology/        金融解释规则
agent/schemas/            结构化家庭数据
.agents/skills/           Canonical portable Skills
.claude/skills/           Claude thin pointers
web/src/                  daisyUI / Tailwind / Plotly 源码
public/                   Landing + synthetic Demo
examples/                 可复现 synthetic fixtures
tests/                    Accounting / Integration / Quant / CLI / Web tests
```

安装后的 wheel 已经包含 Demo、模板、Agent Kit 和离线 Web 资源，正常 CLI 用户不需要 clone 源码仓库。

## 参与开发

```bash
git clone https://github.com/JamesbbBriz/open-family-office.git
cd open-family-office

python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[analytics,documents]'

python -m unittest discover -s tests -v
node tests/sandbox.test.cjs
python scripts/release_check.py
```

很适合贡献的方向包括：不同国家/地区的养老金与税务模型、Importer、Provider fixture、家庭财务边界案例、Skill 改进、无障碍体验和可复现量化方法。

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 项目边界

Open Family Office 不会替用户下单、转账、登录银行、报税，也不会自动替用户决定具体金融产品。它是一个研究和决策支持工具；高级模型的价值取决于输入与假设本身。

MIT License。第三方组件许可见 [THIRD_PARTY.md](THIRD_PARTY.md)。
