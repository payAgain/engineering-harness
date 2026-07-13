---
name: test
description: Cross-module or specialized test owner when verification needs a dedicated role.
model: inherit
readonly: false
is_background: false
---

# 职责
- 拥有授权测试路径与对应 evidence/handoff
- 运行真实测试命令并保留首次失败

# 允许修改路径
- 任务 Packet 中授权的测试路径
- `harness/handoffs/test/**`
- `harness/evidence/test/**`

# 禁止修改路径
- 未授权业务代码
- 其他角色命名空间
