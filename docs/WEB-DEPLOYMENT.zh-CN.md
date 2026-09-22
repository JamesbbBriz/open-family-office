# Open Family Office：网站上线与本地使用

## 这次交付的结构

`public/index.html` 是落地页；`public/demo.html` 是互动Demo；`public/downloads/open-family-office-kit.zip` 是落地页的源码下载。外部页面不调用LLM或金融API，不创建用户账户，也不保存服务器端家庭档案。

**公开部署只上传public目录，不上传整个仓库。私人资料绝不能放在public里。**

## 线上让访客 Try

可使用支持静态文件的网站托管。Cloudflare Pages的Direct Upload支持预构建文件目录/ZIP，适用于这套页面。官方说明：
https://developers.cloudflare.com/pages/get-started/direct-upload/

在Cloudflare后台进入Workers & Pages，创建Pages项目并选择上传静态资产。上传网站ZIP内的文件，保证`index.html`处于上传根目录。无需构建命令，无需服务器环境变量，无需数据库。访问托管平台实际返回的URL；本交付没有替你创建站点或提供虚构地址。

已有GitHub仓库也可在Pages设置中选择静态部署来源。由于目录为public，使用Actions部署时必须把artifact路径设为`public`；不要把仓库根目录作为网站目录。官方工作流说明：
https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

落地页源码按钮默认下载同目录中的项目ZIP。确定真实GitHub地址后，在`config/site.json`中填写`repository_url`，格式为`https://github.com/OWNER/open-family-office`，再运行`python scripts/build_site.py`，按钮会变成真实仓库入口。不填写时不会显示虚构仓库地址。

## 本地浏览

解压网站ZIP，双击index.html或demo.html。在允许本地HTML执行脚本的现代浏览器里，样式、图表库和案例数据都已内嵌。iOS文件预览、聊天软件附件预览不一定执行JavaScript；预览无交互不代表文件损坏，可在桌面浏览器打开或访问部署后的网页。

也可在项目根目录运行：

```bash
python -m http.server 8080 --bind 127.0.0.1 --directory public
```

随后在本机浏览器访问`http://127.0.0.1:8080`。该服务只绑定本机，停止终端进程即可关闭。

## 本地真正使用Agent和私人数据

网页Demo不等于Agent runtime。解压完整项目，先运行`python scripts/hh.py demo`验证工具，再让自己的文件型Agent读取AGENTS.md，按照hh-setup等Skills运行。完整工具安装入口是`python scripts/bootstrap.py --all`。可先加`--dry-run`查看将执行的操作。

Python模块名household_cio、hh CLI、hh-* Skills保留兼容。没有把改名当作重写模块的理由。私人JSON、报表、银行单据放在仓库外；生成的私人HTML内嵌财务数据，不能上传到公开站点。

试算器仅在内存中保存输入；关闭/刷新恢复默认。导出JSON由用户主动触发。没有自动上传、跟踪脚本或浏览器持久化。网站托管方仍可能保留常规访问日志；本地Agent使用云模型时也可能向其服务商发送选定资料。

## 修改界面与重建

```bash
npm install --ignore-scripts
npm run build:css
python scripts/build_site.py
python scripts/package_web.py
```

Tailwind构建会编译vendor/daisyui里的MIT源码改编子集，来源与范围见DESIGN-SYSTEM.md。完整daisyUI npm依赖在package.json中声明，交付环境没有验证完整npm安装。无须购买daisyUI Charts：本项目保留Plotly图表并统一主题。

package_web.py重建下载用源码ZIP，不把自己递归包含进去。下载的源码包若没有嵌套的downloads ZIP，重新运行该脚本即可恢复落地页源码下载按钮。
