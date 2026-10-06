# 技术决策

只记录对目标、方案、评测口径、资源投入或继续/停止有影响的取舍。普通实现细节不需要单独写 ADR。

复制 [决策模板](../templates/decision.md) 为 `ADR-001.md`，编号递增，内部 ID 与文件名一致。

每条至少写清：问题、备选方案、证据、选择理由、影响与下一步。关联实验 ID、资产或代码版本；证据无法访问时说明限制。

状态为 `proposed` / `accepted` / `rejected` / `superseded`。Agent 可以起草 `proposed` 的建议，Owner 确认后填写 `accepted_by` 和日期。已接受记录保留原始判断；替代时新增 ADR 并填写 `supersedes`，在原记录注明替代链接及状态，不重写过去的理由。

讨论改变目标或验收标准时，解释变更原因，随后更新 [project.yaml](../project.yaml) 和 [问题定义](../docs/problem.md)。不要通过降低阈值将原有失败结果改写成成功。

本目录初始没有决策。最终交付在 [delivery.md](../docs/delivery.md) 引用影响结果的关键 ADR 即可。
