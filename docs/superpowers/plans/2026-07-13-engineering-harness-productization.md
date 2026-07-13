# Engineering Harness 产品化 Implementation Plan

> **For agentic workers:** 按任务逐步执行；每完成一块再进入下一块。

**Goal:** 将单体 Markdown 模板拆成可分发的框架仓库：薄 Bootstrap Skill + references + assets + init/audit 脚本。

**Architecture:** Skill 只负责入口与流程路由；详细规则放在 references 渐进读取；assets 提供可复制模板；scripts 负责确定性初始化与审计；目标项目生成物才是运行时 SSOT。

**Tech Stack:** Markdown Skills、PowerShell 脚本、Python 结构测试、Git

---

### Task 1: 仓库骨架与版本元数据

**Files:**
- Create: `README.md`, `VERSION`, `CHANGELOG.md`, `.gitignore`

- [x] 写入版本 `0.1.0`
- [x] 写明三层架构与使用方式

### Task 2: 薄 Bootstrap Skill

**Files:**
- Create: `skills/engineering-harness/SKILL.md`
- Create: `skills/engineering-harness/references/*.md`

- [x] SKILL.md < 200 行
- [x] 支持 init / audit / upgrade / resume / batch
- [x] references 一层深度链接

### Task 3: Assets 模板

**Files:**
- Create: `assets/templates/**`

- [x] 覆盖 Light 最小集与 Standard 扩展集
- [x] 含 AGENTS、current-task、session、skills、agents、scripts stubs

### Task 4: init / audit 脚本

**Files:**
- Create: `scripts/init.ps1`, `scripts/audit.ps1`

- [x] init 按 Light/Standard/Full 复制模板
- [x] audit 检查关键文件与 JSON 合法性
- [x] 写入 `.harness-version`

### Task 5: 结构测试

**Files:**
- Create: `tests/test_structure.py`

- [x] 验证 skill/references/assets/scripts 齐全
- [x] 在临时目录跑 init+audit 冒烟

### Task 6: 回链 worksummary

**Files:**
- Modify: `E:\Work\worksummary\README.md`
- Modify: 用户指南中的递交说明

- [x] 说明正式模板进入框架仓库迁移，旧文件保留为兼容入口
