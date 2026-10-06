# 填写示例：相机可控性优化

本页是虚构的项目过程演练。交付文档另见 [MiniMax H3 蒸馏示例](minimax-h3-delivery.md)，该示例使用用户提供的效率截图，并明确区分截图数字、推导和未提供的信息。

**以下所有人物、日期、指标和 URI 都是虚构教学材料。没有运行训练或评测，不存在可供验收的真实资产。** 示例展示一条“问题 → 假设 → 结果 → 决策 → 下一检查点”的链路，不能作为实际项目证据。

这是填写片段，不是另一套可运行项目。示例中的路径表示将模板复制到真实项目后应创建的位置；完整字段保留自根目录的空模板。

## 1. 定义目标

在 `docs/problem.md` 中写清：

> 在固定的 500 条 camera-eval-v1 中，提升相机运动指令通过率。baseline 为 360/500（72%），交付目标为至少 450/500（90%）。不新增相机指令类型。质量通过率不得低于 98%，同环境推理 p50 不得超过 2100 ms。最小实验的继续条件是提升至少 5 个百分点，且质量与效率约束均满足。

还需要分别定义业务场景测试、关键 case 和可复现交付的要求，填满问题模板中的验收表。评测规则、人评方法、输入、硬件和计时方式写入 `docs/eval.md`。

`project.yaml` 的相关字段示意：

```yaml
schema_version: 1
id: camera-control
name: "相机可控性优化（虚构示例）"
owner: example-owner
stage: feasibility
status: yellow
outcome: null
updated_at: "2026-10-05T15:30:00+08:00"
deadline: "2026-10-16"
goal:
  metric: camera_control_pass_rate
  direction: maximize
  unit: ratio
  baseline: 0.72
  target: 0.90
  current: 0.84
  evalset: camera-eval-v1
  evidence:
    - experiments/EXP-001.md
guardrails:
  - metric: quality_pass_rate
    operator: ">="
    threshold: 0.98
    unit: ratio
    current: 0.99
    evidence:
      - experiments/EXP-001.md
  - metric: inference_p50
    operator: "<="
    threshold: 2100
    unit: ms
    current: 2050
    evidence:
      - experiments/EXP-001.md
workstreams:
  - model
  - eval
dependencies:
  - camera-train-v1
  - camera-eval-v1
next_checkpoint:
  question: "最小实验收益在固定困难样例和多随机种子下是否保持？"
  owner: example-owner
  due: "2026-10-08"
  evidence_required: "EXP-002 的同口径报告、失败类型分析和继续/停止判断"
blockers: []
risks:
  - id: R1
    description: "单次实验不能判断结果是否稳定"
    owner: example-owner
    next_action: "补做多随机种子验证"
    due: "2026-10-08"
```

示例片段省略了 `milestones`；实际使用时保留模板中的里程碑，并填写责任人、截止日、验收条件和证据。颜色表达推进风险，不表示距目标完成了多少百分比。

## 2. 登记资产

`assets.yaml` 的字段形状如下。真实项目请用实际可访问的仓库、不可变资产 URI 和完整代码 SHA 替换；`example://` 地址没有实际内容。

```yaml
schema_version: 1
repos:
  - id: code-main
    url: "https://git.example.invalid/algorithms/camera-control"
    git_sha: null # 教学材料无实际代码提交，不能伪造 SHA
    owner: example-owner
datasets:
  - id: camera-train-v1
    uri: "example://datasets/camera-train/v1/manifest.json"
    version: v1
    notes: "虚构的独立训练集，与评测集隔离"
evalsets:
  - id: camera-eval-v1
    uri: "example://datasets/camera-eval/v1/manifest.json"
    version: v1
    notes: "虚构的固定 500 条样例"
models:
  - id: camera-model-v1
    uri: "example://models/camera/v1"
    version: v1
    experiment: EXP-001
dlc_jobs: [] # 本例没有真实作业；使用 DLC 时添加真实 ID 与 URL
```

`docs/data.md` 解释训练与评测集划分、数据处理代码和质量检查，`docs/design.md` 解释 condition dropout 的方案和验证顺序。

## 3. 记录关键实验

从实验模板创建 `experiments/EXP-001.md`，相关内容示意：

```yaml
---
id: EXP-001
owner: example-owner
status: done
started_at: "2026-10-04"
finished_at: "2026-10-05"
git_sha: null
config: "example://configs/dropout-v1.yaml"
dlc_job: null
job_url: null
dataset: camera-train-v1
evalset: camera-eval-v1
model: camera-model-v1
report: "example://reports/EXP-001"
---
```

`done` 在这里仅演示实验结束状态，不表示本教学案例执行过真实实验。正文示意：

| 部分 | 怎么填写 |
| --- | --- |
| Hypothesis | 增加 camera condition dropout 可以改善轨迹泛化 |
| Setup | 同一模型、训练集、固定评测集和推理参数，仅比较 dropout=0 与 0.1；配置、代码与种子应固定 |
| Expected Result | 主指标提升至少 5 个百分点，质量通过率 ≥98%，推理 p50 ≤2100 ms；不满足则停止或重新分析 |
| Result | 虚构结果：360/500 → 420/500，即 72% → 84%；质量 99%；p50 2050 ms |
| Conclusion | 有正向信号，尚未达到 90% 交付目标；只有单次结果，不能断言收益稳定 |
| Next | 补做困难样例与多随机种子验证；example-owner 于 10 月 8 日提供 EXP-002 |

真实实验还要有原始逐样本结果、代码 SHA、模型版本和效率测试条件。补不齐这些证据时不能通过可复现性审核。

## 4. 确认决策

从决策模板创建 `decisions/ADR-001.md`，初始为 `proposed`：

> 选择继续小规模复验，暂不扩大训练。依据是 EXP-001 的初步收益超过可行性阈值，但尚未达到最终目标，稳定性证据也不足。备选方案是直接扩大训练或停止该方法。下一步复验不成立则停止方向，成立后再决定验证投入。

由 Owner 确认后填写 `accepted_by`、日期并设为 `accepted`。未经确认的 Agent 建议不能直接变成已接受决策。

## 5. 更新进展

在 `progress.md` 中追加检查点，同时更新 `project.yaml`：

> **2026-10-05 — 可行性信号待复验（虚构）**  
> 主指标 72% → 84%（camera-eval-v1，提升 12 个百分点）。关联 EXP-001；原始结果 URI 应记录在实验中。当前离交付目标还差 6 个百分点。单次结果稳定性未知，因此状态为 yellow。下一份证据是 10 月 8 日由 example-owner 提供困难样例与多随机种子报告；继续条件见实验开始前约定的阈值。技术取舍待 ADR-001 确认。

实际记录还要补充相关代码提交，记录提交只引用已经存在的 SHA。不要使用该段虚构文字作为真实周报。

## 6. 审核与交付

即使把虚构数字当作演练输入，84% 仍未达到 90% 的交付阈值；一次实验结束也不能把项目关闭为 `delivered`。

对本教学材料执行真实审核时，所有效果和可复现性判断都应为 **UNKNOWN**，因为不存在真实评测报告、代码和模型。这个例子说明填写完整和取得证据是两件事。

真实项目最终需在 `docs/delivery.md` 中交付功能说明、量化效果、推理效率、固定版本资产、复现命令和已知限制，逐项核验验收表，并由 Owner 确认。若验证失败而停止，通过 ADR 记录原因，关闭结果为 `stopped`，保留有用资产和失败结论。
