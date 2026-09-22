<p align="center"><strong>OPEN FAMILY OFFICE</strong><br>把 Family Office 的方法和工具，开放给愿意掌控自己数据的人。</p>

# Open Family Office

**你的投资组合，不等于你的全部财务生活。** Open Family Office 是一个本地优先、开源的家庭财富研究工具箱，让人和 AI Agent 一起理解家庭的资产、负债、持续与一次性收入、流动性、所有权、目标、情景变化，以及单独声明的流动投资研究组合。

它**不是 SaaS 账户、券商，也不是自动投顾**。项目不会为了“容易用”而砍掉 Ownership Look-through、Monte Carlo、资产配置优化、Provider Adapters、MCP 等硬核能力；真正做减法的是**默认交互层**。

[English](README.md) · [快速开始](docs/QUICKSTART.md) · [Agent UX](docs/AGENT-UX.md) · [数据模型](docs/DATA-MODEL.md) · [集成说明](docs/INTEGRATIONS.md) · [Roadmap](ROADMAP.md)

![Open Family Office](assets/readme/landing.png)

## 30 秒体验

安装了 [uv](https://docs.astral.sh/uv/) 后：

```bash
uvx --from git+https://github.com/JamesbbBriz/open-family-office.git ofo demo --open
```

不需要 clone GitHub、不需要模型账号、不需要 API Key，也不需要输入你的真实家庭资料。Demo 全部使用 synthetic data。

## 安装 CLI

```bash
uv tool install git+https://github.com/JamesbbBriz/open-family-office.git
ofo --version
ofo doctor
```

创建真正属于你的私人工作区：

```bash
ofo init ~/FamilyOffice
cd ~/FamilyOffice
ofo status
```

然后你可以：

- 把这个私人目录直接用 Claude Code / Codex / 其他 file-aware Agent 打开，使用 **ofo-start**；
- 或者自己编辑 `household.json`，完全只用 CLI。

```bash
ofo validate
ofo overview --format markdown
ofo scenario scenarios/job-loss.json
ofo dashboard --out reports/review.html --open
```

进入 workspace 后，CLI 会自动发现 `.ofo/workspace.json`，不需要每次重复输入很长的 household JSON 路径。

![Household research dashboard](assets/readme/overview.png)

## Skill 才是主要的 Agent 使用体验

对普通用户只暴露 10 个有明确目的的 Skill：

| Skill | 用户真正想做的事 |
|---|---|
| **ofo-demo** | 先看看这个项目到底能做什么 |
| **ofo-start** | 建立第一份私人家庭财务模型 |
| **ofo-update** | 加入新的账单、估值或家庭变化 |
| **ofo-overview** | 看清资产负债、收入质量和流动性 |
| **ofo-plan** | 建立 Investment Policy 和配置框架 |
| **ofo-scenario** | 模拟失业、卖公司、房价下跌、大额消费等 |
| **ofo-research** | 主动使用 Provider、穿透分析和量化研究 |
| **ofo-dashboard** | 生成漂亮的私人离线 Dashboard |
| **ofo-review** | 回顾以前的判断、假设和结果 |
| **ofo-doctor** | 检查安装、Skill、Provider 和 MCP |

底层仍然保留细颗粒度 workflow，供 Agent 和开发者组合。

```text
Skill
  ↓
canonical workflow
  ↓
确定性的 ofo CLI / Python 计算
  ↓
Agent 用自然语言解释
```

**Skill 是 UX；MCP 是可选的标准化工具通道。** 不使用 MCP，也可以完整使用这套项目。

## 私人 Workspace

`ofo init` 不只是创建一个 JSON 文件，它会同时把 portable agent kit 安装到你的私人目录：

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

所以 CLI 用户不需要 clone 源码仓库才能使用 Skills。

升级 CLI 之后：

```bash
ofo agent sync
```

没有被你修改过的托管文件会安全升级；你自己改过的 Skill / Workflow 会被标记为 **conflict 并保留原样**，不会被强行覆盖。

## 这套系统关注什么

- 家庭可归属资产与负债；
- 固定持续收入、浮动持续收入、一次性现金流；
- 可使用流动性与锁定/非流动财富；
- 未来大额支出和现金 runway；
- 企业出售等资产替换事件；
- 多成员、多实体的 Ownership Look-through；
- Investment Policy 和大类资产配置约束；
- 显式假设下的 Monte Carlo 和 liquid-sleeve optimization；
- 保留来源信息的只读 Provider adapters；
- 完全离线的 Plotly 家庭财务 Dashboard。

房子、私人企业、锁定养老金不会被偷偷当成“可以每天调仓的股票”。

## 常用 CLI

```bash
ofo validate
ofo overview --format markdown
ofo cashflow --months 36 --format markdown
ofo scenario scenarios/business-sale.json
ofo allocation policy.json
ofo dashboard --out reports/review.html
```

高级研究按需打开：

```bash
ofo providers
ofo fetch rba table --query '{"table":"f01"}' --allow-network --out evidence/rba-f01.json
ofo optimize returns.json --engine scipy --method min_variance
ofo simulate simulation.json
ofo lookthrough ownership.json
```

历史数据、用户观点和模型输出必须分开。优化结果是 research output，不是自动交易指令。

## 可选 MCP

如果你的 Agent host 更喜欢标准 MCP tool calling，可以给已安装 CLI 加 MCP：

```bash
uv tool install --force --with 'mcp>=1.10,<2' git+https://github.com/JamesbbBriz/open-family-office.git
```

进入私人 workspace 后：

```bash
ofo mcp-config
```

生成的是只读 stdio MCP 配置，并且作用范围被限制在这个 workspace。

## 项目结构

```text
src/open_family_office/   可安装的确定性计算引擎 + CLI
agent/workflows/          Canonical financial workflows
agent/methodology/        金融解释规则与方法论
agent/schemas/            结构化家庭数据
.agents/skills/           Canonical portable Skills
.claude/skills/           Claude thin pointers
web/src/                  daisyUI / Tailwind / Plotly 源码
public/                   静态 Landing + synthetic Demo
examples/                 可复现 synthetic fixtures
tests/                    Accounting / Integration / Quant / CLI / Web tests
```

wheel 会把 Demo、模板、Agent Kit 和 Web 资源一并打包，所以正常使用 CLI 不依赖源码 checkout。

## 为什么不是 SaaS

这个项目的目标不是把 Family Office 重新包装成另一个月费软件，而是让愿意折腾、愿意自己掌控数据的人，可以直接使用以前门槛很高的方法和工具；开发者也可以继续提交养老金、税务、国家/地区规则、Provider、Importer、Skill 和量化模块。

开源不是“残缺版 SaaS”，而是一个可以持续组合和扩展的工具基础。

## 边界

Open Family Office 不会替用户下单、转账、登录银行、报税，也不会自动替用户决定具体金融产品。模型和优化结果都依赖输入假设，不能因为数学复杂就被当成确定答案。

MIT License。第三方组件许可见 [THIRD_PARTY.md](THIRD_PARTY.md)。
