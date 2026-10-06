---
id: null # 复制后填 EXP-001，与文件名一致
owner: null
status: planned # planned / running / done / failed / stopped
started_at: null
finished_at: null
git_sha: null # 实际运行的代码仓库 SHA，通常为完整 40 位
config: null # 固定版本配置的路径或 URI
dlc_job: null # assets.yaml 中的任务 ID；非 DLC 任务使用 job_url
job_url: null
dataset: null # 主要输入/训练数据的资产 ID
evalset: null # 固定评测集的资产 ID
model: null # 输出模型的资产 ID；无模型产物时说明理由
report: null # 原始结果的可访问路径或 URI
---

# Hypothesis — 假设

要验证什么、为什么可能有效、失败会推翻什么判断。明确一个可检验的问题。

# Setup — 设置

- baseline 和比较方案：待填写。
- 唯一/主要变量、超参数与完整配置：待填写。
- 数据与评测版本（引用 assets.yaml）、样本数量：待填写。
- 代码仓库、环境、硬件、随机种子、重复次数：待填写。
- 运行与评测命令、工作目录和任务链接：待填写。

比较条件不一致时说明差异。复杂配置链接到版本化文件。

# Expected Result — 预期与停止条件

实验开始前写明主指标、约束、最小收益阈值、预算和停止条件。说明什么结果会支持继续，什么结果会否定假设。

# Result — 实际结果

| 指标 / 单位 | baseline | 本次结果 | 样本数 / 波动 | 原始证据 |
| --- | --- | --- | --- | --- |
| 待填写 | 待测 | 待测 | 待填写 | 待填写 |

填写失败类型、异常和与预期的差异。运行失败时保留错误日志，不填虚构指标。没有可核验结果时写 UNKNOWN。

# Conclusion — 技术结论

由 Owner 填写或确认：假设得到支持、被否定还是证据不足；结论的适用范围和局限。Agent 草稿标明待确认。

# Next — 下一步

继续、调整、停止或等待什么证据；负责人和下一检查点日期。重要取舍引用 ADR。

# Related — 关联记录

关联问题验收 ID、里程碑 ID、ADR、资产和进展记录。原始日志/报告保存在现有系统，本记录只保存决策所需信息。
