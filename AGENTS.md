# Skill 维护约定

本仓库是 `algorithm-project-organizer` skill 的源码，入口见 [SKILL.md](SKILL.md)。

- `references/` 是规范和章节结构的唯一来源；整理实际项目时将 skill 源码视为只读，不维护 assets 副本。
- 仅在用户要求修改本 skill 时编辑源码，实际项目文档写入 skill 目录之外的目标项目。
- 修改规范与路由时保持章节标记和规范链接有效；已有项目再次整理时保留用户内容和历史事实。
- 修改初始化工具后验证已有代码接入、从零开始、按需主题、重复调用保护与 skill 目录保护；不通过其他写入方式绕过路径检查。
- 使用 skill-creator 的校验器检查 SKILL.md，并核对内部链接和界面元数据。
