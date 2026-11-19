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

## 宿主共享剪贴板发行

[剪贴板 0.2.0](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/tools.clipboard-v0.2.0) 与[计算 0.2.0](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/tools.calculator-v0.2.0) 已发布，系统剪贴板统一通过宿主 API 访问，最低宿主版本为 [Sinan v0.2.1](https://github.com/zhyipeng/sinan/releases/tag/v0.2.1)，初始化另检查 `clipboard.v1` 能力。

[三平台 CI](https://github.com/zhyipeng/sinan-official-plugins/actions/runs/43806605442) 无界面测试和构建通过，两个版本各六个目标包的清单、图标、原生架构、大小及 GitHub SHA-256 已核验；登记使用真实 Release/Asset ID，历史记录不变。三平台实机 UI、真实剪贴板、焦点及跨应用输入仍未验收。


## OCR 首次上架

[文字识别 0.1.0](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/tools.ocr-v0.1.0) 已公开，仅登记真实的 macOS arm64 完整包。支持离线中英文提取、主搜索粘图匹配与自动识别、原图预览、页面粘贴和结果复制；最低宿主为 [Sinan v0.3.1](https://github.com/zhyipeng/sinan/releases/tag/v0.3.1)，v0.2.1 不具备新图片接口，v0.3.0 未公开发行。

[插件三平台 CI](https://github.com/zhyipeng/sinan-official-plugins/actions/runs/43830703763) 和[宿主六目标流水线](https://github.com/zhyipeng/sinan/actions/runs/43831907925) 已通过。OCR ZIP 已回下载核对 SHA-256、大小、清单、模型摘要、原生架构、执行位、图标和许可，登记使用真实 Release/Asset ID。其他 OS/架构尚无完整 OCR 资产；真实桌面/WebView、系统剪贴板及权限交互未验收。

## 剪贴板 0.2.1

[剪贴板 0.2.1](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/tools.clipboard-v0.2.1) 已发布并登记三系统 arm64/amd64 六目标包，新增复制成功后自动前移与持久排序、列表图片缩略图及详情等比大图预览。最低宿主仍为 0.2.1，API 1 / UI Bridge 2 不变；历史发行记录保留。

[发布流水线](https://github.com/zhyipeng/sinan-official-plugins/actions/runs/44004573375) 在 macOS runner 上通过全量无界面测试、六目标交叉构建及打包；六个公开 ZIP 已回下载核对 SHA-256、大小、清单、图标、原生架构和执行位，使用真实 Release/Asset ID 登记。没有执行三平台实机 UI、真实系统剪贴板、焦点与自动输入验收。


## OCR 六目标原生发行

[文字识别 0.2.0](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/tools.ocr-v0.2.0) 已登记 macOS、Windows、Linux 的 arm64/amd64 六个真实原生包，最低宿主仍为 0.3.1，保留 0.1.0 发行记录。Windows 含对应目标运行库，Linux 以 Ubuntu 24.04/glibc 2.39 与系统 libstdc++ 为基线；X11/xclip、Wayland/wl-clipboard 的宿主剪贴板依赖不变。

[原生验证](https://github.com/zhyipeng/sinan-official-plugins/actions/runs/44006353531) 在六个真实目标 runner 上完成实际 ZIP 中文/空格路径重定位、11 张合成图每图两次、源文本质量不退化、取消和父进程退出回收。[发布流程](https://github.com/zhyipeng/sinan-official-plugins/actions/runs/44006913968) 仅解析通过验证的 ZIP，复核模型、架构、Windows 无控制台子系统和许可后公开，六个远端包的摘要与公开 SHA256SUMS 一致。ARM/x86 终端样本均可能漏一个点，位置不同，差异已公开在 VALIDATION.json；不把合成图验证当作完美准确率或真实桌面、WebView、输入法及系统剪贴板验收。

## 截图与 OCR 配套发行

[截图 0.1.0](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/tools.screenshot-v0.1.0) 首次上架，[OCR 0.3.0](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/tools.ocr-v0.3.0) 新增跨插件公开图片入口，两者均为三系统 arm64/amd64 六目标原生包，最低宿主 [Sinan 0.4.0](https://github.com/zhyipeng/sinan/releases/tag/v0.4.0)。截图中的 OCR 为可选依赖，缺失时截图和标注照常使用；历史 OCR 0.2.0 及其兼容记录不变。

[宿主六目标发布](https://github.com/zhyipeng/sinan/actions/runs/44070459519)、[截图发布](https://github.com/zhyipeng/sinan-official-plugins/actions/runs/44070601312)、[OCR 六目标原生验证](https://github.com/zhyipeng/sinan-official-plugins/actions/runs/44071389046)及[正式发布](https://github.com/zhyipeng/sinan-official-plugins/actions/runs/44072351423)通过。登记逐项核对实际公开 Release/Asset ID、下载地址、版本、ZIP 原生入口/架构、大小和 SHA-256；旧资产保持不可变。真实桌面/WebView、截图授权、系统剪贴板、焦点与多屏交互尚未验收。

## 截图 0.3.0 上架

[截图 0.3.0](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/tools.screenshot-v0.3.0) 已登记 macOS 和 Windows 各两种架构，最低宿主为 Sinan 0.4.0。支持原生遮罩内框选、标注、输出和 OCR 交接。独立后处理入口已移除，Linux 不再由插件中心提供，已发行的旧版下载文件保留。

四份公开 ZIP 已下载核对大小、SHA-256、清单、图标与原生二进制架构。Windows x64 无界面原生检查通过，ARM64 辅助程序已交叉构建。真实桌面交互待验收。

## 脚本 0.2.0 上架

[脚本 0.2.0](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/tools.script-v0.2.0) 已登记 macOS、Windows、Linux 的 arm64/amd64 六个原生包，最低宿主为 [Sinan 0.6.0](https://github.com/zhyipeng/sinan/releases/tag/v0.6.0)。支持脚本目录扫描、自定义环境和关键字，以及输出页或后台结果通知。macOS 系统通知需要打包应用及系统授权，Linux 需会话 D-Bus 和通知服务。

六个公开 ZIP 已回下载核对大小、SHA-256、清单、图标与原生架构，登记使用实际 Release 和 Asset ID。三平台真实系统通知和输出页交互仍待验收。

## 编码助手 0.1.1

[编码助手 0.1.1](https://github.com/zhyipeng/sinan-official-plugins/releases/tag/tools.encoding-assistant-v0.1.1) 已登记 macOS、Windows、Linux 的 arm64/amd64 六个纯前端包，最低宿主为 [Sinan 0.4.0](https://github.com/zhyipeng/sinan/releases/tag/v0.4.0)。五个工具均在隔离页面离线处理；选图与剪贴板依赖宿主的 UI Bridge 2。

六个公开 ZIP 已回下载核对大小、SHA-256、清单和图标，登记使用实际 Release 和 Asset ID。三端真实 WebView、剪贴板、选图与 Linux X11/Wayland 交互尚未验收。
