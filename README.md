# Sinan Plugin Registry

Sinan 插件中心登记目录。负责维护插件资料、版本记录与审核机制。

## 核心职责
- **插件审核**：规范化插件发布与维护流程。
- **版本管理**：维护经审核的版本发布记录。

## 贡献方式
提交 Pull Request 至 `submissions/` 目录，通过自动化校验与人工审核后纳入登记。

资料可选 `icon` 字段为内嵌图片 data URL（SVG、PNG、JPEG 的 base64），解码后最多 64 KiB；SVG 使用静态基础形状，不含样式、脚本及外部引用。宿主校验后用于商店展示，不请求远程图片；无图标时显示插件名首字。新增字段要求支持图标的新版宿主。

## 已登记插件

- JSON 工具（`tools.json` 0.4.3）：纯前端 JSON 编辑工具，提供 macOS / Windows / Linux 的 ARM64 / AMD64 六目标包。
- 剪贴板（`tools.clipboard` 0.1.1）：文本/图片历史、本机持久化及自动粘贴，提供 macOS / Windows / Linux 的 ARM64 / AMD64 六目标包；Linux X11 需要 xclip / xdotool，Wayland 需要 wl-clipboard 且只支持手动粘贴。需要包含插件热键与系统输入接口的新版司南（本体源码 750cf22 或更新）；宿主开发构建仍使用 0.1.0 版本号，早期同版本号构建不兼容，不能仅据最低版本号判断功能具备。

- 翻译（`tools.translate` 0.3.0）：MyMemory、Google 免费网页接口和全局共享 LLM，支持命名配置选择与快捷复制，提供三平台 ARM64/AMD64 六目标包。需要包含共享 LLM 窄桥与 `llm` 权限的新宿主（[源码 d594882 或更新](https://github.com/zhyipeng/sinan/commit/d594882c5561f6e1f1b0d583efb1c1e34659b461)）；早期同为 0.1.0 的宿主不兼容。平台 CI 构建与无界面检查通过，真实桌面交互及真实 LLM 未验收。[发行包](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/v0.3.0)。

- 日历（`tools.calendar` 0.1.2）：只读月历、农历、生肖、传统节日与二十四节气，中国大陆放假/补班数据覆盖 2004–2027 年，未收录年份明确提示。提供 macOS / Windows / Linux 的 ARM64 / AMD64 六目标包；需要三平台隔离 UI、桥 2 与图标能力（[宿主源码 0bf8cc9 或更新](https://github.com/zhyipeng/sinan/commit/0bf8cc9138bbfbd964cbd4bffb2a1da46f638adb)）。三平台 CI 测试与构建通过，实机 UI 未验收。[发行包](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/v0.1.2)。

## 插件独立版本与标签

同仓库内不同插件可使用相同的 `version`。新版本的 `tag` 使用 `<plugin-id>-v<version>`（例如 `tools.calendar-v0.1.0`），与该记录的 pluginId/version 精确对应；继续兼容历史 `v<version>`。版本唯一性仍按单个插件检查，既有标签、发行资产与登记记录不改写。

新增格式需先更新司南宿主：旧宿主可能拒绝包含新标签的整个目录并回退缓存。文件名、下载 URL 与标签绑定、真实 Release/Asset ID、大小及 SHA-256 校验保持不变。不得只为标签迁移重新登记已存在的同插件同版本。桌面宿主自身的发布标签不受影响。

验证：`python3 scripts/check.py` 与 `python3 -m unittest discover -s scripts/tests`（Windows 使用 `python -X utf8`，测试命令对应为 `python -X utf8 -m unittest discover -s scripts/tests`）。


## 统一图标更新与计算首次上架

已登记 JSON 工具 0.4.4、剪贴板 0.1.2、翻译 0.3.1、日历 0.1.3，以及首次上架的计算 0.1.0。五个插件统一浅色圆角底板与蓝色线条图标，每个版本均对应真实的三系统 arm64/amd64 六目标发行资产；旧发行记录保留。

计算支持主搜索即时计算、结果复制、多行稿纸和本地历史。Linux 复制依赖 X11 的 xclip 或 Wayland 的 wl-copy；缺少依赖时明确报错。[计算发行包](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/tools.calculator-v0.1.0)。

[三平台 CI](https://github.com/zhyipeng/sinan-official-plugins/actions/runs/43799988731) 无界面测试与构建通过，30 个包的版本、图标、原生架构、大小与 SHA-256 已核验；真实桌面/WebView/剪贴板交互仍未验收。新发行标签需支持独立发布标签的宿主（源码 c518ca5 或更新），相同开发版本号 0.1.0 不构成兼容证明。
