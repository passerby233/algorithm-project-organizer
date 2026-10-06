# 代码位置与入口

本目录用于指定算法代码的位置。默认把代码放在 [src/](src/)，也可以保留在已有外部仓库，通过 [location.yaml](location.yaml) 指向它。这里只规定位置和入口，不预设训练框架。

## 代码在本项目中

把源代码放入 `code/src/`，然后填写 `location.yaml` 的 `entrypoints`。`path: code/src` 相对**算法项目仓库根目录**解析，不是相对 YAML 所在目录。`train`、`infer`、`eval` 的入口路径再相对代码根目录解析。

例如 `infer: scripts/infer.py` 表示 `code/src/scripts/infer.py`。这里只登记路径；完整命令、参数、环境和工作目录写到 [design.md](../docs/design.md) 与 [delivery.md](../docs/delivery.md)。入口文件尚不存在时保持 `null`。

代码在本仓库时，复现使用本仓库代码的真实 Git SHA；可以在 [assets.yaml](../assets.yaml) 登记本仓库 URL 与固定版本。

## 代码在已有外部仓库中

将共享配置改成：

```yaml
schema_version: 1
mode: external
path: null
repo_asset_id: code-main
entrypoints:
  train: null
  infer: null
  eval: null
```

在 `assets.yaml.repos` 中添加 `code-main`，填写仓库 URL 和真实代码 SHA。每位使用者在本机创建 `code/location.local.yaml`，只覆盖代码位置：

```yaml
path: "C:/project/minimax-h3-distill"
```

Linux/macOS 可写自己的绝对路径，例如 `/work/minimax-h3-distill`。这里的目录名是填写示例，不代表该目录已经存在。`location.local.yaml` 已被 `.gitignore` 排除；共享配置不提交个人机器路径。

## 读取约定

1. 先读 `location.yaml`。`mode` 为 `in_repo` 或 `external`；共享 `path` 为仓库根目录相对路径或 `null`。
2. 本机存在 `location.local.yaml` 时，仅用其中的 `path` 覆盖共享路径；本机文件使用绝对路径，其他字段仍来自共享配置。
3. 确认解析后的目录存在，入口路径与文件名真实可用。路径未填写或不存在时说明缺失，不猜测代码位置。
4. 外部代码需要核对其仓库 URL、实际运行 SHA 和本地改动；项目文档仓库的 SHA 不能代替外部代码的 SHA。

以上约定供使用者和 Agent 读取，不需要新服务。代码目录中的现有 AGENTS.md 与工程约定也应遵守。若此模板只作为现有仓库中的一个子目录使用，调整共享 `path`，并在此说明该算法项目的根目录位置。
