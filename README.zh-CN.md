# Open Family Office

**不是“AI选股”，而是本地优先的家庭资产管理研究工作区。** 它把家庭资产、负债、持续/一次性收入、流动性需求、所有权、情景变化和单独声明的可投资流动资产放在同一个框架里。

[English](README.md) · [快速开始](docs/QUICKSTART.md) · [Agent 使用体验](docs/AGENT-UX.md) · [数据模型](docs/DATA-MODEL.md)

![Open Family Office](assets/readme/landing.png)

## 30 秒体验

```bash
git clone https://github.com/JamesbbBriz/open-family-office.git
cd open-family-office
python scripts/ofo.py demo
```

也可以直接打开 `public/index.html` 和 `public/demo.html`。演示使用虚构家庭数据，不需要 API Key、模型账号或网络。

## Skill 使用路径

```text
ofo-demo
   ↓
ofo-start → ofo-overview → ofo-plan
                 ↓             ↓
            ofo-scenario   ofo-research
                 ↓             ↓
              ofo-dashboard → ofo-review

已有家庭资料：ofo-update
环境/依赖问题：ofo-doctor
```

Claude Code 可以直接使用 `/ofo-start`、`/ofo-overview` 等命令；其他文件型 Agent 读取 `.agents/skills/ofo-*/SKILL.md`。真正的金融业务流程只维护在 `agent/workflows/`，不同 Agent 的入口只做薄适配。

## 关键原则

- Python 负责金额与量化计算，Agent 负责访谈、编排和解释。
- 用户确认事实、原始证据、外部数据、假设和模型输出必须分开。
- 房产、私人企业、锁定养老金不会被偷偷当成可日交易资产。
- 网络访问默认关闭；外部数据先进入 evidence，再经确认写入家庭模型。
- 私人资料和生成的私人 HTML 必须放在仓库外。
- 不自动交易、不转账、不登录银行、不替用户选择具体金融产品。

## 目录

```text
src/open_family_office/   确定性引擎、数据适配器、量化、报表
agent/                     业务流程、方法论、schema、模板
.agents/skills/            通用 Agent Skills
.claude/                   Claude Skills 与命令入口
web/src/                   网站源码
public/                    静态发布产物
examples/                  虚构案例
tests/                     自动测试
```

安装后 CLI 使用 `ofo`：

```bash
python -m pip install -e '.[analytics,documents]'
ofo doctor
ofo overview /path/to/household.json
ofo stress /path/to/household.json /path/to/scenario.json
```

更多内容见 [快速开始](docs/QUICKSTART.md) 和 [Agent 使用体验](docs/AGENT-UX.md)。
