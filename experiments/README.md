# 关键实验

实验记录用来验证假设和支持决策，不是每天的工作流水账。普通调试的全部细节留在日志、训练平台或实验追踪工具中。

## 什么时候创建记录

- 会影响技术路线、继续或停止的实验。
- 需要进入技术讨论 / 周会的实验。
- 产生重要模型、数据或交付候选资产的实验。

失败、无收益和中止的关键实验也保留。

## 怎么写

复制 [实验模板](../templates/experiment.md) 为 `EXP-001.md`，后续编号递增。内部 `id` 与文件名一致，每个实验指定一个 Owner。

开始前填写 Hypothesis、Setup、Expected Result；结束后补齐 Result、Conclusion、Next 和真实版本证据。Owner 负责技术结论，Agent 可以根据可核验的日志补齐事实并起草建议。

状态为 `planned` / `running` / `done` / `failed` / `stopped`。`failed` 表示运行未能完成，`done` 可以得到无收益或否定假设的结果，不等于项目验收通过。

front matter 中 `dataset`、`evalset`、`model` 引用 [assets.yaml](../assets.yaml) 中的 ID；`git_sha` 对应实际运行的代码，`config` 指向能复现运行的固定配置。多个数据集写在 Setup 中，所有版本都需登记。未使用的任务或模型字段保持 `null` 并说明理由。

## 结束后的关联更新

- 新资产登记到 `assets.yaml`。
- 影响当前目标的结果更新到 `project.yaml`，保留证据路径。
- 关键变化写入 [progress.md](../progress.md)。
- 改变技术方向时创建 [决策记录](../decisions/README.md)。
- 当前方案或评测口径变化时更新对应长期文档。

本目录初始没有实验。创建第一条记录后，可直接通过文件列表和 Git 历史查看，无需再维护一份手工实验数据库。
