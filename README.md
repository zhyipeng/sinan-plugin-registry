# Sinan 插件目录

维护插件资料、经审核的版本记录与后续下架信息，不存放插件源码。

当前仅登记官方插件 `tools.json` 的资料，状态为 `pending-release`。GitHub 仓库尚未创建，来源地址为空；没有可安装版本，也没有生成客户端安装索引。内置的应用检索、设置、插件管理不在此目录独立分发。

## 当前维护流程

1. 官方源码位于独立的 `sinan-official-plugins` 仓库。
2. 确定 GitHub 所有者并创建远端后，填写 `source.repository` 的真实 HTTPS 仓库地址。
3. 作者发布平台 ZIP 后，再设计并提交正式版本记录，包含平台、宿主兼容要求、固定 Release/Asset 标识、包大小和 SHA-256。
4. 审核通过后才能纳入可安装索引；不能只因填写源码版本号就视为已发布。

```sh
python3 scripts/check.py
```

当前校验器验证资料登记及 submissions 待审核发布记录，仍拒绝非空 releases，防止在分发协议尚未实现时生成伪可安装记录。目录签名、索引发布、下载和宿主商店均未实现。未来扩展版本协议时需一并升级校验器。


## 发布审核记录 v1

模板工作流可向 `submissions/<plugin-id>/<version>.json` 提交 PR，字段包括 schemaVersion、pluginId、name、version、repository、tag、commit、releaseId、compatibility 和 assets。每个 asset 包含 os、arch、file、sha256、size、assetId、downloadUrl。校验器核对路径、版本、平台、摘要格式及 GitHub 下载地址的对应关系；不联网下载、不执行提交代码，不证明包无恶意行为。

待审核记录不是可安装版本，不自动写入 plugins 的 releases，也不赋予官方身份。当前仍无宿主消费的商店索引或签名发布。目录维护者需核查仓库归属、真实 Release 与资产字节，以及宿主兼容性；将来安装索引协议确定后再人工或经审核的自动流程纳入。
