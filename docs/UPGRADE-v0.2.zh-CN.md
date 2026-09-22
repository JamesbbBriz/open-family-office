# Open Family Office v0.2 升级交付说明

## 直接打开的文件

`public/demo.html` 是完整离线 HTML，包含五个视图、13 张交互图表、四种预计算情景、深浅色模式、核心界面中英文切换，以及 JSON 导出和浏览器打印。所有公开数据都是虚构案例。PNG 截图是实际页面渲染，不是效果图。

最终图表栈是 **Tailwind CSS + Plotly**，不是 React/Recharts。Tailwind 负责布局和界面，Plotly 负责图表。编译后的 CSS 和图表 JavaScript 均内嵌，离线可用。没有为了套用多个库而增加重复图表依赖，也没有把自制 SVG 冒充第三方图表组件。

## 一条命令

建议 Python 3.12、Node.js/npm，从解压后的项目根目录执行：

```bash
python scripts/bootstrap.py --all
```

先查看将执行的步骤：

```bash
python scripts/bootstrap.py --all --dry-run
```

安装主环境 `.venv`、隔离的 `.venv-openbb`，安装数值、量化、行情、文档和 MCP 依赖，编译 Tailwind，生成图表报告，最后运行测试和 doctor。外部服务的 Key 仍由使用者提供。复制 `config/environment.example` 中需要的变量名到你自己的 shell/Agent 设置，不要把真实密钥写回代码库；这个文件不会被自动加载。

本次环境没有包仓库网络，所以没有在这里完成全依赖安装。可运行的本地数值/图表部分与未运行的可选原生 SDK 已在 `docs/VALIDATION.md` 分开记录。安装脚本遇到不兼容或网络错误会停止。没有完整的跨平台传递依赖锁文件；成功安装后会保存本机实际解析版本清单。

## 本次补充

数据：13 个只读适配器，带显式联网许可、密钥缺失检查、请求/响应证据与使用权提示。RBA/ABS/SEC/FRED/OECD/IMF、CoinGecko、Yahoo、OpenBB、Alpha Vantage、Finnhub、MarketData.app、MetalpriceAPI 已有代码入口。

量化：SciPy 最小方差、CVaR、风险平价目标；skfolio 和 PyPortfolioOpt 原生桥接；HRP 与显式输入的 Black–Litterman 入口；有效前沿；相关性 Monte Carlo；所有权 DAG 和多维敞口汇总。

工作流：16 个 Skills，7 个只读 MCP 工具；PDF 文本提取、OFX 导入、标准化基金持仓 CSV；本地 HTML 报告导出。

图表：现金预算曲线、资产构成环形图、持续收入堆叠图、资金来源与去向桑基图、一次性资金图、流动性阶梯、有效前沿、优化目标权重对比、相关性热力图、用户目标与现状对比、模拟分位区间、出售事件瀑布图、压力情景比较。

## 数据与研究边界

接入代码已经写好，不等于已经获得 API 授权或验证每个实时接口。需要 Key 的服务不会绕过身份认证；不能因为 OpenBB 能连接某数据商，就默认获得该数据商的再分发权。金融数据包并未随仓库提供。

房产、企业、私人信贷、养老金可以进入家庭资产负债表，但优化只针对明确的可流动研究部分。指数不能替代一套房的估值，企业出售现金不能全部当作新增财富，归还本金也不等于收入。模拟路径需要显式收益/波动/相关性假设，未做现实概率校准，不含税费和跳跃风险。

Addepar、Wealthfolio、Ghostfolio 是设计参考，而不是需要一并安装的依赖。尚未连接真实银行/券商，不包含自动交易、自动报税、任意 PDF 全自动识别或完整 N-PORT 持仓解析。完整覆盖矩阵见 `docs/INTEGRATIONS.md`。

## 开始用自己的资料

先用虚构案例通过 `python scripts/ofo.py demo` 和 `python scripts/ofo.py doctor`，再用 `AGENTS.md` 让你自己的 Agent 完成访谈。私人 JSON、PDF、OFX、密钥和生成报告全部放在仓库外。HTML 内含资料，切勿把私人报告当成公开 Demo 推送 GitHub。

本次没有创建公开仓库、提交代码、发帖或运行真实交易。`launch/` 中仍有发布材料；README 已升级为实际截图和当前能力，外部发布前按 `RELEASE-CHECKLIST.md` 复核。
