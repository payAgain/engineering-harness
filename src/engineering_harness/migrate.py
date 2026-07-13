"""Migrate legacy Cursor-template harness layouts into tool-agnostic paths."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from engineering_harness import read_version
from engineering_harness.init import copy_template
from engineering_harness.paths import protocol_path


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _copy_tree_files(src_dir: Path, dst_dir: Path, *, force: bool) -> list[str]:
    logs: list[str] = []
    if not src_dir.is_dir():
        return logs
    dst_dir.mkdir(parents=True, exist_ok=True)
    for src in sorted(src_dir.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(src_dir)
        dst = dst_dir / rel
        if dst.exists() and not force:
            logs.append(f"SKIP existing: {dst_dir.name}/{rel.as_posix()}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        logs.append(f"MIGRATE: {src_dir.name}/{rel.as_posix()} -> {dst_dir.name}/{rel.as_posix()}")
    return logs


def detect_legacy_layout(target: Path) -> list[str]:
    """Return human-readable warnings for legacy Cursor SSOT layouts."""
    warnings: list[str] = []
    if (target / ".cursor" / "agents").is_dir() and not (target / "agents").is_dir():
        warnings.append("LEGACY: .cursor/agents present but agents/ missing — run: eh migrate <path>")
    if (target / ".cursor" / "skills").is_dir() and not (target / "skills").is_dir():
        warnings.append("LEGACY: .cursor/skills present but skills/ missing — run: eh migrate <path>")
    if not (target / ".harness-version").exists() and (
        (target / ".cursor" / "agents").is_dir() or (target / "AGENTS.md").exists()
    ):
        warnings.append("LEGACY: harness files without .harness-version — run: eh migrate <path>")
    if (target / "AGENTS.md").exists():
        text = (target / "AGENTS.md").read_text(encoding="utf-8", errors="ignore")
        if ".cursor/agents" in text or ".cursor/skills" in text:
            warnings.append("LEGACY: AGENTS.md still references .cursor/* paths")
    return warnings


def migrate_project(
    target: Path,
    *,
    level: str = "Standard",
    force: bool = False,
) -> list[str]:
    if level not in {"Light", "Standard", "Full"}:
        raise ValueError(f"unsupported level: {level}")

    target = target.resolve()
    if not target.is_dir():
        raise FileNotFoundError(f"target not found: {target}")

    logs: list[str] = []
    timestamp = _now()
    name = target.name

    logs.extend(_copy_tree_files(target / ".cursor" / "agents", target / "agents", force=force))
    logs.extend(_copy_tree_files(target / ".cursor" / "skills", target / "skills", force=force))

    # Standard+ branching + sensors from framework templates (skip if exist unless force)
    if level in {"Standard", "Full"}:
        for source_rel, dest_rel in [
            ("docs/branching.md", "docs/branching.md"),
            ("harness/scripts/branch_check.py", "harness/scripts/branch_check.py"),
            ("harness/scripts/harness_check.py", "harness/scripts/harness_check.py"),
            ("harness/scripts/safe_bash_guard.py", "harness/scripts/safe_bash_guard.py"),
            ("harness/scripts/verify.py", "harness/scripts/verify.py"),
        ]:
            logs.append(
                copy_template(
                    source_rel=source_rel,
                    dest_rel=dest_rel,
                    target=target,
                    project_name=name,
                    level=level,
                    timestamp=timestamp,
                    force=force,
                )
            )

    protocol_dst = target / "harness" / "PROTOCOL.md"
    if protocol_dst.exists() and not force:
        logs.append("SKIP existing: harness/PROTOCOL.md")
    else:
        protocol_dst.parent.mkdir(parents=True, exist_ok=True)
        protocol_dst.write_text(protocol_path().read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        logs.append("WRITE: harness/PROTOCOL.md")

    version_path = target / ".harness-version"
    if version_path.exists() and not force:
        logs.append("SKIP existing: .harness-version")
    else:
        meta = {
            "framework": "engineering-harness",
            "version": read_version(),
            "level": level,
            "layout": "tool-agnostic",
            "cli": "python",
            "migrated_from": "legacy-cursor-template",
            "migrated_at": timestamp,
        }
        version_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        logs.append("WRITE: .harness-version")

    agents_note = target / "agents" / "README-MIGRATE.md"
    if (target / "agents").is_dir() and (not agents_note.exists() or force):
        agents_note.write_text(
            "# Migrated agents\n\n"
            "These files were copied from `.cursor/agents/`.\n"
            "Update `AGENTS.md` reading order to prefer `agents/` over `.cursor/agents/`.\n"
            "`.cursor/*` may remain as an optional IDE adapter only.\n",
            encoding="utf-8",
            newline="\n",
        )
        logs.append("WRITE: agents/README-MIGRATE.md")

    remaining = detect_legacy_layout(target)
    for item in remaining:
        logs.append(f"NOTE: {item}")

    logs.append("MIGRATE DONE")
    logs.append("Next: edit AGENTS.md to reference agents/ and skills/; then eh.cmd branch-new <slug> <path>")
    return logs
