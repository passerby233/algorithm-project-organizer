# algorithm-project-organizer

这是一个算法项目整理 skill 仓库。让 Agent 将研发对话、实验结果和关键产出整理成项目文档，支持已有代码项目接入、从零建档和持续更新。

整理内容包括问题定义、算法方案与任务计划、数据说明、评测要求与报告、算法交付、事实进展节点及实际实验记录。

首次使用请先阅读 [SKILL.md](SKILL.md)，了解各类文档的职责、产出位置、整理流程和增量更新规则；各主题的具体填写要求通过其中的规范链接查看。

## 安装（以 Codex 为例）

| 场景 | 安装位置 |
| --- | --- |
| 在一个现有项目中使用或与团队共享 | `<项目根目录>/.agents/skills/algorithm-project-organizer/` |
| 个人在多个项目中使用 | `~/.agents/skills/algorithm-project-organizer/` |

在 Codex 中发送以下指令，即可让 Agent 安装：

```text
使用 $skill-installer，从 https://github.com/passerby233/algorithm-template 安装这个 skill。
仓库根目录包含 SKILL.md，安装名称为 algorithm-project-organizer，
目标目录为当前项目的 .agents/skills/algorithm-project-organizer/。
```

个人跨项目使用时，将目标目录改为 `~/.agents/skills/algorithm-project-organizer/`。安装后若未显示，重启 Codex。安装与发现规则见 [Codex 官方文档](https://learn.chatgpt.com/docs/build-skills)；其他 Agent 按各自的 skill 安装规则使用。

## 使用示例

需要判断一段内容应写入哪个文件时，查看 [SKILL.md 的内容分流定义](SKILL.md#内容分流)。

**已有代码项目：** 在项目中讨论完需求或方案后调用。

```text
使用 $algorithm-project-organizer，整理本次问题定义、方案讨论和数据要求，更新当前项目文档。
```

**从零开始：** 先整理需求和方案，再逐步补充研发产出。

```text
使用 $algorithm-project-organizer，在当前工作区新建“图像修复”项目，整理我们刚才讨论的目标和算法方案，尚无代码。
```

**持续更新：** 实验、评测或交付有产出后再次调用。

```text
使用 $algorithm-project-organizer，结合本次对话和 outputs/eval-report.html，更新已有评测文档，并记录实际结果带来的决策和进展。
```

已有项目的文档默认写入 `<项目根目录>/docs/`；新项目默认建立在 `<工作区>/algorithm-projects/<项目名>/`，文档同样放在其 `docs/` 中。后续调用复用原文档目录，按需补充相关内容。

本仓库的 `references/` 保存填写规范，实际项目内容写入用户项目。
