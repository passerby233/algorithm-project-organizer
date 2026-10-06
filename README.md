# algorithm-template

用于**单个小规模算法研发子项目**的模板。把目标、验收口径、下一份证据、关键实验、决策和交付资产保存在同一个 Git 仓库中，使参与者能回答：解决什么问题、做到什么程度、现在卡在哪里、下一步何时得到结果。

本模板参考[项目组织建议](https://chatgpt.com/share/6abf5e14-57a8-83e9-9b48-0de347e3abd0)中的项目仓库方案，实现第一阶段的 **Git + Markdown + YAML**。不包含 DataViewer、Dashboard、大型项目汇总页、Web 服务、自动采集或 Agent 服务。使用时无需安装依赖；Git 和任意文本编辑器即可。Obsidian 可作为编辑器，文档使用标准 Markdown 和相对链接，不依赖插件。

## 先看哪里

| 你想知道什么 | 打开哪个文件 |
| --- | --- |
| 目标、负责人、当前指标、阶段、下一次检查点 | [project.yaml](project.yaml) |
| 为什么做、做什么、什么叫完成 | [docs/problem.md](docs/problem.md) |
| 当前方案、替代方案、实施步骤 | [docs/design.md](docs/design.md) |
| 数据版本、处理流程、分布与质量问题 | [docs/data.md](docs/data.md) |
| 评测口径、baseline、结果与 bad cases | [docs/eval.md](docs/eval.md) |
| 最近发生了什么、阻塞与下一步 | [progress.md](progress.md) |
| 哪些实验支持当前判断 | [experiments/README.md](experiments/README.md) |
| 为什么选择、修改或停止一个方向 | [decisions/README.md](decisions/README.md) |
| 代码、数据、模型、任务在哪里 | [assets.yaml](assets.yaml) |
| 本机代码所在目录、训练/推理/评测入口 | [code/README.md](code/README.md)、[code/location.yaml](code/location.yaml) |
| 最终交付什么、效果和效率如何 | [docs/delivery.md](docs/delivery.md) |
| 蒸馏交付和推理效率表怎么填写 | [MiniMax H3 交付示例](examples/minimax-h3-delivery.md) |
| 如何让 Agent 辅助维护与审核 | [AGENTS.md](AGENTS.md) |

## 10 分钟开始一个项目

### 1. 复制模板

把本目录复制为自己的项目目录。以下示例创建 `camera-control`，目标目录应当尚不存在。

Windows PowerShell：

```powershell
Copy-Item -LiteralPath C:\project\algorithm-template -Destination C:\project\camera-control -Recurse
Set-Location C:\project\camera-control
git init -b main
```

macOS / Linux（在模板的上一级目录执行）：

```bash
cp -R algorithm-template camera-control
cd camera-control
git init -b main
```

上述命令适用于本次生成的不含 `.git` 的模板目录。从托管平台复制时，也可通过组织的模板仓库创建一个新仓库。若给已有算法仓库补齐规范，只复制需要的文件并合并 README、AGENTS.md 和 `.gitignore`，保留已有 Git 历史和项目约定。

算法代码默认放在 `code/src/`，通过 [code/location.yaml](code/location.yaml) 指定代码根目录和入口；保留在另一个仓库时按 [代码位置说明](code/README.md) 填写外部仓库资产和本机目录。这里不预设训练框架。

### 2. 明确目标和验收

先填写 [project.yaml](project.yaml) 中的 `id`、`name`、唯一 `owner`、`deadline`、`goal`、里程碑和 `next_checkpoint`，再填写 [docs/problem.md](docs/problem.md)。

至少明确：业务场景、量化主指标及目标、固定评测集、不能退化的指标、范围外事项、下一次获得证据的期限。尚未测出的数字写 `null`，不要用 `0` 代替未知值。`goal.current` 没有评测证据时也保持 `null`。

在 [docs/eval.md](docs/eval.md) 中约定单位、评测版本、样本数、比较方式和推理效率的测试环境。对不适用的验收项写出理由。先对齐这些内容，再开始优化。

### 3. 登记资源和方案

把代码仓库、数据集和评测集登记到 [assets.yaml](assets.yaml)，在 [docs/data.md](docs/data.md) 中引用对应资产 ID。在 [docs/design.md](docs/design.md) 中说明方案和最小实验，估计的是**何时获得下一份能决定继续或停止的证据**。

修改本 README 顶部的名称和简介，使其成为实际项目入口。`examples/` 是教学材料，可保留参考，不应当作为实际项目证据。

### 4. 保存第一版项目定义

```bash
git add .
git commit -m "docs: define project goal and acceptance"
```

根据组织要求提交评审。仓库发布和远端配置由团队自行安排。本模板不连接任何账号或服务。

项目过程填写示例见 [examples/README.md](examples/README.md)，蒸馏交付示例见 [examples/minimax-h3-delivery.md](examples/minimax-h3-delivery.md)。

## 日常怎么维护

### 开始关键实验

复制 [templates/experiment.md](templates/experiment.md) 为 `experiments/EXP-001.md`，填写 front matter 中的 ID、Owner 和版本信息，正文填写 Hypothesis、Setup、Expected Result。

```powershell
Copy-Item -LiteralPath templates\experiment.md -Destination experiments\EXP-001.md
```

```bash
cp templates/experiment.md experiments/EXP-001.md
```

编号连续递增，文件名与内部 ID 相同。只记录影响技术路线、需要讨论或产生重要资产的实验；普通调试留在训练日志中。运行前写出判定阈值和停止条件，避免看完结果后重新定义成功。

### 实验完成或失败

补齐实际运行的代码 SHA、参数配置、数据/评测集版本、任务和模型资产、原始结果链接。填写 Result、Conclusion、Next；失败和无收益的实验同样保留。

`done` 仅表示实验完成，不表示假设成立或项目达标。需要改变方向时，从 [templates/decision.md](templates/decision.md) 创建 `decisions/ADR-001.md`，由 Owner 确认取舍和下一步。执行任务可用 DLC 或任何其他平台；未使用 DLC 时字段保持 `null`。

### 关键提交或每日/每周检查点

有指标、资产、阻塞或重要判断变化时，更新 `project.yaml` 和关联长期文档，并在 [progress.md](progress.md) 中按顶部格式追加一条记录。稳定阶段每周整理一次即可；关键变化发生时及时记。

每条进展回答：**变化是什么 → 证据在哪里 → 对目标有什么影响 → 谁在何时产出下一份证据**。记录既可手写，也可让现有 Agent 根据 Git 和实验文件起草，再由 Owner 确认。

常用本地查阅命令（`HEAD` 指当前已提交版本，执行前请先提交希望纳入检查的变更）：

```bash
git log --since="7 days ago" --oneline --all
git diff HEAD~1 HEAD -- project.yaml assets.yaml docs experiments decisions progress.md
git rev-parse HEAD
```

`HEAD~1` 需要至少两次提交；只有首次提交时使用 `git show HEAD`。实验的 `git_sha` 填**实际运行的代码版本**，不是事后写报告的提交。代码在外部仓库时，在对应仓库取得 SHA，并登记到 `assets.yaml`。

进展记录可引用已经存在的代码提交，随后将这条记录提交到 Git；不要预填尚未产生的文档提交 SHA。

### 阶段检查与交付

按照 `docs/problem.md` 的验收表逐项检查 `docs/eval.md`、实验记录、原始报告和版本资产。参考 [templates/review.md](templates/review.md) 记录 PASS / FAIL / UNKNOWN，可放在本次进展的评审附件中；无需每次实验单独写一份审核报告。

更新里程碑时填写证据。小项目可以省略不需要的阶段，但要在 `note` 中说明。达到最终验收且交付资料齐全后填写 `docs/delivery.md`，由 Owner 确认关闭。效率评测必须同时说明工况、绝对耗时、加速比、资源、质量与成本口径，可参考 H3 示例；缺测不能写成零成本。若提前停止，保留失败证据、停止决策和可复用资产；停止也可以关闭，但不能记为交付验收通过。

## 字段和状态约定

`project.yaml` 保存**当前状态**；`progress.md` 保存**历史变化**；实验和原始报告保存**证据**；决策保存**取舍**。当前数字只以 `project.yaml` 为准，历史记录保留当时的快照。不要为各位参与者建立重复的项目状态文档。

| 字段 | 约定 |
| --- | --- |
| `schema_version` | 当前为 `1`，方便未来工具读取 |
| `id` / `owner` | 项目 ID 使用小写英文和短横线；一个项目只指定一个最终 Owner |
| `stage` | `definition` 定义 → `baseline` 基线 → `feasibility` 可行性 → `validation` 验证 → `delivery` 交付 → `closed` 关闭 |
| `status` | `unknown` 信息不足；`green` 按计划推进；`yellow` 有风险；`red` 关键路径受阻。颜色不代表已完成 |
| `outcome` | 进行中为 `null`；关闭时为 `delivered` 或 `stopped` |
| `goal.direction` | `maximize` 越大越好，`minimize` 越小越好 |
| `goal.unit` | 写清单位；`ratio` 使用 0–1，`percent` 使用 0–100，延迟可用 `ms`，吞吐可用 `samples/s` |
| `goal.evalset` | `assets.yaml` 中固定评测集的 ID；更换口径后重测 baseline，不直接比较异版本结果 |
| `goal.evidence` | 支持当前指标的相对文件路径或报告链接；原始结果链接应当出现在所引用的实验/评测文档中 |
| `guardrails` | 每项包含 `metric`、`operator`（`>=` / `<=`）、`threshold`、`unit`、`current` 和 `evidence`；口径写在 `docs/eval.md` |
| 里程碑 `status` | `planned` / `in_progress` / `passed` / `failed` / `skipped`；通过要有证据，跳过要有说明 |
| `next_checkpoint` | 一个明确问题、责任人、到期时间和所需证据；它是研发推进的最小单位 |
| `blockers` / `risks` | 每项填写 `id`、`description`、`owner`、`next_action`、`due`；阻塞是已发生的问题，风险是可能发生的问题 |
| `dependencies` | 引用本项目资产 ID 或外部子项目仓库 URL；只记录关联，不创建跨项目管理系统 |
| 日期 / 缺失值 | 日期写为带引号的 `"YYYY-MM-DD"`；更新时间带时区；未知为 `null`，空列表为 `[]`，不适用在正文注明理由 |

项目目标和里程碑的变更要记录原因；已确认的技术决策用新 ADR 修订。进度不填主观百分比，不用提交数、算力使用量或实验数量判断成果。

## 资产怎么写

`assets.yaml` 按 `repos`、`datasets`、`evalsets`、`models`、`dlc_jobs` 分类。同一资产 ID 保持唯一。模板中各分类为空，添加一个真实条目时用列表替换 `[]`，不要重复 YAML 键。

| 分类 | 必填信息 | 常用关联 |
| --- | --- | --- |
| `repos` | `id`、`url`、`git_sha`（尚未冻结可为 `null`） | 代码版本对应实验实际运行的提交 |
| `datasets` / `evalsets` | `id`、`uri`、不可变 `version` | `docs/data.md`、`docs/eval.md` |
| `models` | `id`、`uri`、`version`、来源 `experiment` | 实验 ID、交付模型 |
| `dlc_jobs` | `id`、`url`、`experiment` | 作业地址、对应实验 |

需要的条目还可增加 `owner`、`notes`、样本数、manifest URI 或配置文件位置。数据和模型文件留在既有存储系统；此仓库保存索引、版本和必要说明。用不可变路径、版本号或校验和固定资产，不只写 `latest`。URL 中不保存访问令牌。

## 让 Agent 辅助使用

本模板提供仓库规则和审核格式，不提供名为 `project-agent` 的可执行程序。打开现有 Agent 工具后可直接使用下面的请求。

**审核目标定义：**

> 请遵守 AGENTS.md，检查 project.yaml、docs/problem.md 和 docs/eval.md 是否足以启动项目。逐项指出缺失的目标、固定评测集、基线、验收和下一检查点；只输出建议，不替我修改目标。

**整理进展：**

> 请遵守 AGENTS.md，根据最近 7 天的 Git 记录、experiments 和 assets.yaml，为 progress.md 起草一条带证据的进展。列出建议更新的 project.yaml 字段。不可访问的报告标记 UNKNOWN，技术结论和下一步决策交给 Owner 确认。

**审核交付：**

> 请遵守 AGENTS.md，按 docs/problem.md 的验收标准审核 docs/delivery.md，用 templates/review.md 的格式输出 PASS / FAIL / UNKNOWN，并逐项提供原始证据、版本和缺失信息。不要仅根据文档完整度判断交付达标。

填写表格完整不等于实际验收通过。Agent 的输出是审核建议，Owner 对结论和交付确认负责。

## 目录

```text
algorithm-template/
├── README.md
├── AGENTS.md
├── project.yaml             # 当前状态与阶段检查点
├── assets.yaml              # 代码、数据、评测集、模型、任务索引
├── progress.md              # 带证据的历史进展
├── code/
│   ├── README.md            # 代码目录和本机路径的填写方法
│   ├── location.yaml        # 共享代码位置与入口
│   └── src/.gitkeep         # 默认算法代码目录
├── docs/
│   ├── problem.md           # 问题、范围、验收
│   ├── design.md            # 当前方案与阶段计划
│   ├── data.md              # 数据需求与处理过程
│   ├── eval.md              # 评测口径与结果
│   └── delivery.md          # 功能、效果、效率、过程资产
├── experiments/README.md    # 关键实验记录约定
├── decisions/README.md      # 技术决策记录约定
├── templates/
│   ├── experiment.md
│   ├── decision.md
│   └── review.md
└── examples/
    ├── README.md            # 一条假设到评审的虚构示例
    ├── minimax-h3-delivery.md # 参考用户截图的蒸馏交付示例
    └── assets/H3-infer-eval.png # 示例所引用的原始效率表
```

首次只需填写项目定义和评测口径，其余文档在对应阶段补齐。模板中的空值和填写提示是待办，不代表已完成。
