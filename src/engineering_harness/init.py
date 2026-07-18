"""Initialize harness files into a target project."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from engineering_harness import read_version
from engineering_harness.paths import (
    DELIVERY_DOCUMENTS,
    DOCUMENT_PRESETS,
    HUMAN_MAINTAINED_FILES,
    LIGHT_FILES,
    STANDARD_DIRS,
    STANDARD_FILES,
    protocol_path,
    templates_root,
)


APPROVAL_POLICY = """# Approval Policy

- commit on working branches (`feat/*` etc.): required after verified work; agent-executed
- tag / push / release / update protected `main|master`: explicit one-time human authorization
- migrate / destructive reset: explicit one-time human authorization
- G4 without commit SHA: not allowed (must-commit); waiver only with explicit one-time approval
"""


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _render(content: str, *, project_name: str, level: str, timestamp: str) -> str:
    return (
        content.replace("{{PROJECT_NAME}}", project_name)
        .replace("{{HARNESS_LEVEL}}", level)
        .replace("{{TIMESTAMP}}", timestamp)
        .replace("{{BUILD_CMD}}", "<fill-build-command>")
        .replace("{{TEST_CMD}}", "<fill-test-command>")
        .replace("{{LINT_CMD}}", "<fill-lint-command-or-NA>")
    )


def copy_template(
    *,
    source_rel: str,
    dest_rel: str,
    target: Path,
    project_name: str,
    level: str,
    timestamp: str,
    force: bool,
) -> str:
    src = templates_root() / Path(source_rel)
    dst = target / Path(dest_rel)
    if dst.exists() and dest_rel in HUMAN_MAINTAINED_FILES:
        return f"PRESERVE human-maintained: {dest_rel}"
    if dst.exists() and not force:
        return f"SKIP existing: {dest_rel}"
    if not src.exists():
        raise FileNotFoundError(f"template missing: {src}")
    text = _render(src.read_text(encoding="utf-8"), project_name=project_name, level=level, timestamp=timestamp)
    _write_text(dst, text)
    return f"WRITE: {dest_rel}"


def resolve_delivery_documents(selection: str) -> list[str]:
    value = selection.strip()
    if not value:
        raise ValueError("delivery document selection cannot be empty; use 'none' explicitly")
    if value in DOCUMENT_PRESETS:
        return list(DOCUMENT_PRESETS[value])
    document_ids = [item.strip() for item in value.split(",") if item.strip()]
    if not document_ids:
        raise ValueError("delivery document selection cannot be empty; use 'none' explicitly")
    unknown = sorted(set(document_ids) - DELIVERY_DOCUMENTS.keys())
    if unknown:
        choices = ", ".join(DELIVERY_DOCUMENTS)
        raise ValueError(f"unknown delivery document(s): {', '.join(unknown)}; choose from: {choices}")
    return list(dict.fromkeys(document_ids))


def init_project(
    target: Path,
    *,
    level: str = "Standard",
    project_name: str | None = None,
    force: bool = False,
    delivery_documents: str | None = None,
) -> list[str]:
    if level not in {"Light", "Standard", "Full"}:
        raise ValueError(f"unsupported level: {level}")

    target = target.resolve()
    version_path = target / ".harness-version"
    if delivery_documents is None:
        if not version_path.is_file():
            raise ValueError("--docs is required on first init; use 'none' to confirm no delivery documents")
        try:
            existing_meta = json.loads(version_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot preserve delivery documents from .harness-version: {exc}") from exc
        if not isinstance(existing_meta, dict):
            raise ValueError("cannot preserve delivery documents: .harness-version root must be an object")
        existing_documents = existing_meta.get("delivery_documents")
        if not isinstance(existing_documents, list) or not all(
            isinstance(item, str) and item in DELIVERY_DOCUMENTS for item in existing_documents
        ):
            raise ValueError("cannot preserve invalid delivery_documents from .harness-version")
        selected_documents = list(dict.fromkeys(existing_documents))
    else:
        selected_documents = resolve_delivery_documents(delivery_documents)

    target.mkdir(parents=True, exist_ok=True)
    name = project_name or target.name
    timestamp = _now()
    logs: list[str] = []

    for source_rel, dest_rel in LIGHT_FILES:
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
        _write_text(protocol_dst, protocol_path().read_text(encoding="utf-8"))
        logs.append("WRITE: harness/PROTOCOL.md")

    if level in {"Standard", "Full"}:
        for source_rel, dest_rel in STANDARD_FILES:
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
        for rel in STANDARD_DIRS:
            path = target / rel
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                logs.append(f"DIR: {rel}")

    for document_id in selected_documents:
        source_rel, dest_rel = DELIVERY_DOCUMENTS[document_id]
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

    if level == "Full":
        policy = target / "docs" / "approval-policy.md"
        if policy.exists() and not force:
            logs.append("SKIP existing: docs/approval-policy.md")
        else:
            _write_text(policy, APPROVAL_POLICY)
            logs.append("WRITE: docs/approval-policy.md")

    meta = {
        "framework": "engineering-harness",
        "version": read_version(),
        "level": level,
        "layout": "tool-agnostic",
        "cli": "python",
        "delivery_documents": selected_documents,
        "initialized_at": timestamp,
    }
    _write_text(target / ".harness-version", json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    logs.append("WRITE: .harness-version")
    return logs
