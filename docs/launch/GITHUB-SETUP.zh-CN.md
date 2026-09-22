> v0.2 发布范围以 README 和 docs/VALIDATION.md 为准。适配器源码与样例测试不等于真实 API 已验证；不要对外宣称未执行的原生 SDK、宿主或在线接入结果。

# GitHub 仓库装修与发布操作单

项目工作名：**Open Family Office**。建议仓库名：`open-family-office`。这是工作名，不代表商标或域名已查验/注册。
首版源代码、文档和虚构样例采用 MIT；公开发布前由维护者确认许可和归属。

## 1. 发布前先验收，不先堆 Badge

运行演示、全部测试和发布检查；阅读 `SECURITY.md` 与 `RELEASE-CHECKLIST.md`。
核对公开目录只有虚构家庭数据。真实账单、私人工作区和既有 Git 历史都不应出现在公开包。

先把命令里的 `YOUR_GITHUB_OWNER` 替换成你的真实 GitHub 用户名或组织名。
发布脚本默认只预览，并且真正创建时默认私有：

```bash
python scripts/publish.py --repo YOUR_GITHUB_OWNER/open-family-office
python scripts/publish.py --repo YOUR_GITHUB_OWNER/open-family-office --publish
```

第二条会实际创建私有仓库，需要你本机已安装并登录 GitHub CLI，且已配置 Git 提交姓名/邮箱。
若明确选择直接公开，使用下面这一条代替第二条，不要对已经创建的同名仓库重复运行：

```bash
python scripts/publish.py --repo YOUR_GITHUB_OWNER/open-family-office --publish --public
```

脚本只处理新仓库，将允许发布的文件复制到全新临时 Git 仓库后推送，不带入任何旧历史。
它会设置描述、Topics、模板标记和 Discussions；不会发社交帖子、开推广 Issue 或部署网站。
本次交付没有实际执行任何创建/推送动作。GitHub CLI 的正式命令见 `docs/SOURCES.md`。

## 2. About 区域直接使用

Description：

> Household-first agent workflows for wealth, income durability, liquidity and multi-asset scenarios. Local-first. No trading.

Topics（聚焦真实能力，不加无关热门关键词）：

`agent-skills`, `asset-management`, `personal-finance`, `cash-flow`, `financial-planning`, `local-first`, `python`, `fintech`

Website：只有实际部署并验收演示后再填真实网址，未部署就留空。
仓库类型：Template repository。真实用户资料必须放在仓库外，模板标记本身不提供隐私保护。

## 3. 首页内容顺序

已有 `README.md` 和 `README.zh-CN.md`：定位 → 实际演示截图 → 一条可运行命令 → 三个家庭问题 →
已实现/未实现 → 工作流 → 企业出售例子 → 隐私 → 贡献 → 许可/出处。

不要把 20 个技术名词放在第一屏。不要显示不存在的 CI 结果、机构客户、收益率、下载量或社区人数。
远程 CI 真正跑过以后才添加指向本仓库真实工作流的状态 Badge。

## 4. Social preview 和截图

设置页的 Social preview 上传 `assets/social-preview.png`，不要只使用个人头像。
`assets/demo.png` 是实际虚构演示页面截图，`assets/business-sale.png` 展示出售企业场景。
GitHub 官方建议社交预览 1280×640、文件小于 1 MB；本包按此尺寸提供。
截图有明确的 SYNTHETIC 标记，不用真实家庭数据做传播。

## 5. Discussions、Issues 与首个 Release

Discussions 开 General、Ideas 和 Show and tell 三类即可。将 `launch/DISCUSSION-WELCOME.md` 作为欢迎帖草稿。
先核实私密漏洞报告入口，再邀请用户报告敏感安全问题，不把私人账单引导进公开 Issue。

Issue 模板已提供。`launch/SEED-ISSUES.md` 有五个真实任务；按真实优先级手动创建，不制造虚假活跃度。
`launch/RELEASE-NOTES.md` 是 v0.2.0 发布说明草稿。远程 CI 和演示验收后再建标签/Release。
不要在仓库尚未发布时发“已上线”的宣传文案。

## 6. 演示托管

首轮不需要后端：`public/demo.html` 本身是离线可交互的预计算演示。
公开托管时只部署 `public/demo.html` 和需要的公开静态素材，不把整个开发目录或私人 workspace 部署出去。
GitHub Pages 可作为低维护候选；使用当前官方设置流程并核实实际网址。这里只是发布选择，不代表已部署。
页面没有上传入口、账户或金融 API，因此它不能冒充 Hosted 产品。

## 7. 个人 GitHub 求职展示

将该仓库 Pin 到个人主页。个人简介连接 Asset Management 与 AI Engineering，不必围绕转行困难写文案。
用 `launch/CV-PROJECT.md` 的真实工程事实描述项目；推广数据只有实际发生后才能写。

## 完成定义

一个陌生人能在 30 秒内说清项目用途；能用虚构数据试用；能找到一条运行命令；
能看到计算假设和未实现功能；知道如何提交不包含隐私的反馈。满足这些比装饰性 Badge 更重要。

## v0.3更名和网站入口

产品名Open Family Office，仓库slug建议open-family-office。首页先放assets/landing-preview.png，再放assets/dashboard-preview.png。网站链接必须填实际部署返回的地址，不使用猜测域名。静态部署仅上传public/。落地页自带Try demo、Use locally和源码下载入口，未设置真实仓库URL时不伪造GitHub链接。
