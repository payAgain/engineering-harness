# Engineering Harness Productization Spec

> 日期：2026-07-13  
> 状态：v0.2.0 — 通用 Agent 框架（非 IDE Skill 安装）

## 目标

提供任意 coding agent 都可使用的工程护栏框架：

1. 框架仓库负责分发与版本
2. `PROTOCOL.md` 作为通用调用入口
3. 目标项目 `agents/` + `skills/` + `harness/` 作为运行时 SSOT

## 明确不做

- 不把框架安装到 Cursor / Claude / 其他 IDE 的全局 skills 目录
- 不以 `.cursor/**` 作为运行时事实源
- 不把框架绑定到单一厂商 Agent API

## 已完成

### v0.1.0
- 从单体模板拆出 assets / scripts / tests

### v0.2.0
- 主入口改为 `PROTOCOL.md`
- 目标路径改为中立 `agents/`、`skills/*.md`
- 调度语义改为 “separate role instance”
- `integrations/*` 仅作可选适配说明
- init 同步写入项目内 `harness/PROTOCOL.md`
- 测试覆盖：无 `.cursor` 运行时依赖；init/audit 冒烟通过

## 使用

```text
1. pwsh -File scripts/init.ps1 -TargetPath <project> -Level Standard
2. Give any agent: PROTOCOL.md
3. pwsh -File scripts/audit.ps1 -TargetPath <project>
```

## 后续（可选）

- 纯 POSIX 的 init/audit 实现（减少对 PowerShell 的依赖）
- upgrade 迁移
- Spec Kit Feature Spec 层融合
