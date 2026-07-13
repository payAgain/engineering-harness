# Optional Cursor adapter

Engineering Harness is tool-agnostic. You do **not** need to install anything into `~/.cursor/skills`.

## Recommended usage

1. Attach or open `PROTOCOL.md`
2. Or point the agent at the target project's `harness/PROTOCOL.md` + `AGENTS.md`
3. Keep runtime SSOT in `agents/` and `skills/`

## Optional mirroring

If you want Cursor UI discovery for project roles/procedures, copy (do not move) after init:

```powershell
# from target project root
New-Item -ItemType Directory -Force .cursor\agents, .cursor\skills | Out-Null
Copy-Item agents\* .cursor\agents\ -Force
Get-ChildItem skills\*.md | ForEach-Object {
  $name = $_.BaseName
  New-Item -ItemType Directory -Force ".cursor\skills\$name" | Out-Null
  Copy-Item $_.FullName ".cursor\skills\$name\SKILL.md" -Force
}
```

`agents/` and `skills/` remain the source of truth. Re-copy after role/procedure updates.
