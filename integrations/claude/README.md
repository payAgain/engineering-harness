# Optional Claude Code adapter

Do not require a Claude-specific install for core use.

## Recommended usage

- Paste/attach `PROTOCOL.md`
- Ask Claude Code to read `AGENTS.md`, `current-task.md`, and `harness/session/*`
- Use Claude's Task/subagent mechanism to realize `agents/*.md` roles when forced delegation applies

## Optional project instruction

You may add a short pointer in `CLAUDE.md`:

```markdown
Follow harness/PROTOCOL.md and AGENTS.md.
Role definitions: agents/
Procedures: skills/
```
