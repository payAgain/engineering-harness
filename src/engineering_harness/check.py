"""Harness structure checks and dangerous-command guard."""

from __future__ import annotations

import json
import re
from pathlib import Path

from engineering_harness.paths import (
    DANGEROUS_PATTERNS,
    DELIVERY_DOCUMENTS,
    LIGHT_REQUIRED,
    STANDARD_REQUIRED,
)

GOAL_STATUSES = {"draft", "awaiting_scope_confirmation", "active", "achieved", "accepted", "paused", "blocked", "escalation_required", "cancelled"}


def load_level(root: Path) -> str:
    version_path = root / ".harness-version"
    if not version_path.exists():
        raise FileNotFoundError(".harness-version missing")
    meta = json.loads(version_path.read_text(encoding="utf-8"))
    return str(meta.get("level") or "Standard")


def required_files(level: str, delivery_documents: list[str] | None = None) -> list[str]:
    files = list(LIGHT_REQUIRED)
    if level in {"Standard", "Full"}:
        files.extend(STANDARD_REQUIRED)
    for document_id in delivery_documents or []:
        document = DELIVERY_DOCUMENTS.get(document_id)
        if document:
            files.append(document[1])
    return files


def _frontmatter_value(text: str, key: str) -> str | None:
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", text, re.DOTALL)
    if not match:
        return None
    field = re.search(rf"(?m)^{re.escape(key)}:\s*([^\n#]+)", match.group(1))
    return field.group(1).strip() if field else None


def _normalize_list_item(value: str) -> str:
    return value.strip().strip("\"'").strip()


def _frontmatter_list(text: str, key: str) -> list[str]:
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", text, re.DOTALL)
    if not match:
        return []
    inline = re.search(rf"(?m)^{re.escape(key)}:\s*\[([^]]*)\]\s*$", match.group(1))
    if inline:
        return [_normalize_list_item(item) for item in inline.group(1).split(",") if _normalize_list_item(item)]
    block = re.search(rf"(?ms)^{re.escape(key)}:\s*\n((?:\s{{2}}-\s*[^\n]+\n?)*)", match.group(1))
    if not block:
        return []
    return [_normalize_list_item(item) for item in re.findall(r"(?m)^\s{2}-\s*([^\n#]+)", block.group(1)) if _normalize_list_item(item)]


def _inside_root(root: Path, value: str | None) -> Path | None:
    if not value:
        return None
    root = root.resolve()
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _yaml_scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*([^\n#]+)", text)
    if not match:
        return None
    value = match.group(1).strip()
    return None if value in {"null", "~"} else value.strip('"\'')


def _section(text: str, name: str) -> str:
    match = re.search(rf"(?ms)^{re.escape(name)}:\s*(?:#.*)?\n((?:^[ \t]+.*(?:\n|$)|^\s*$)*)", text)
    return match.group(1) if match else ""


def _yaml_list(section: str, key: str) -> list[str]:
    inline = re.search(rf"(?m)^\s{{2}}{re.escape(key)}:\s*\[([^]]*)\]\s*$", section)
    if inline:
        return [item.strip().strip('"\'') for item in inline.group(1).split(",") if item.strip()]
    block = re.search(rf"(?ms)^\s{{2}}{re.escape(key)}:\s*\n((?:\s{{4}}-\s*[^\n]+\n?)*)", section)
    return re.findall(r"(?m)^\s{4}-\s*([^\n#]+)", block.group(1)) if block else []


def _frontmatter(text: str) -> str:
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", text, re.DOTALL)
    return match.group(1) if match else ""


def _indented_section(text: str, name: str, indent: int) -> str:
    prefix = " " * indent
    child = " " * (indent + 2)
    match = re.search(
        rf"(?ms)^{prefix}{re.escape(name)}:\s*(?:#.*)?\n((?:^{child}.*(?:\n|$)|^\s*$)*)",
        text,
    )
    return match.group(1) if match else ""


def _indented_scalar(section: str, key: str, indent: int) -> str | None:
    match = re.search(rf"(?m)^\s{{{indent}}}{re.escape(key)}:\s*([^\n#]+)", section)
    if not match:
        return None
    value = match.group(1).strip().strip('"\'')
    return None if value in {"null", "~"} else value


def _indented_list(section: str, key: str, indent: int) -> list[str]:
    inline = re.search(rf"(?m)^\s{{{indent}}}{re.escape(key)}:\s*\[([^]]*)\]\s*$", section)
    if inline:
        return [_normalize_list_item(item) for item in inline.group(1).split(",") if _normalize_list_item(item)]
    block = re.search(
        rf"(?ms)^\s{{{indent}}}{re.escape(key)}:\s*\n((?:\s{{{indent + 2}}}-\s*[^\n]+\n?)*)",
        section,
    )
    if not block:
        return []
    return [_normalize_list_item(item) for item in re.findall(rf"(?m)^\s{{{indent + 2}}}-\s*([^\n#]+)", block.group(1)) if _normalize_list_item(item)]


def _test_baseline(text: str) -> tuple[str | None, dict[str, dict[str, object]]]:
    baseline = _indented_section(_frontmatter(text), "test_baseline", 0)
    applicability = _indented_scalar(baseline, "applicability", 2)
    layers: dict[str, dict[str, object]] = {}
    for name in ("unit", "integration"):
        layer = _indented_section(baseline, name, 2)
        layers[name] = {
            "status": _indented_scalar(layer, "status", 4),
            "check_ids": _indented_list(layer, "check_ids", 4),
            "boundaries": _indented_list(layer, "boundaries", 4),
            "exemption_reason": _indented_scalar(layer, "exemption_reason", 4),
        }
    return applicability, layers


def _goal_criteria(text: str) -> tuple[set[str], dict[str, str]]:
    criteria: set[str] = set()
    required: dict[str, str] = {}
    for block in re.split(r"(?m)(?=^\s{2}- id:\s*SC-\d{3,}\s*$)", _section(text, "success_criteria")):
        ident = re.search(r"(?m)^\s{2}- id:\s*(SC-\d{3,})\s*$", block)
        if not ident:
            continue
        criterion_id = ident.group(1)
        criteria.add(criterion_id)
        is_required = re.search(r"(?m)^\s{4}required:\s*true\s*$", block)
        status = re.search(r"(?m)^\s{4}status:\s*([a-z_]+)\s*$", block)
        if is_required:
            required[criterion_id] = status.group(1) if status else ""
    return criteria, required


def _load_goals(root: Path, problems: list[str]) -> dict[str, dict[str, object]]:
    goals: dict[str, dict[str, object]] = {}
    active_by_initiative: dict[str, str] = {}
    for path in sorted((root / "harness" / "goals").glob("G-*.yaml")):
        text = path.read_text(encoding="utf-8")
        goal_id, initiative_id, status = (_yaml_scalar(text, key) for key in ("goal_id", "initiative_id", "status"))
        scope = _section(text, "scope")
        revision_match = re.search(r"(?m)^\s{2}revision:\s*(\d+)\s*$", scope)
        criteria, required = _goal_criteria(text)
        if not goal_id or not re.fullmatch(r"G-\d{3,}", goal_id) or not initiative_id or not re.fullmatch(r"I-\d{3,}", initiative_id):
            problems.append(f"INVALID GOAL: {path.relative_to(root)}: goal_id/initiative_id")
            continue
        if goal_id in goals:
            problems.append(f"DUPLICATE GOAL ID: {goal_id}: {path.relative_to(root)}")
            continue
        if status not in GOAL_STATUSES:
            problems.append(f"INVALID GOAL: {path.relative_to(root)}: status")
        if not revision_match or not criteria:
            problems.append(f"INVALID GOAL: {path.relative_to(root)}: scope revision/success criteria")
        if status == "active" and initiative_id in active_by_initiative:
            problems.append(f"MULTIPLE ACTIVE GOALS: {initiative_id}")
        elif status == "active":
            active_by_initiative[initiative_id] = goal_id
        progress, escalation = _section(text, "progress"), _section(text, "escalation")
        active_build = re.search(r"(?m)^\s{2}active_build_id:\s*([^\n#]+)", progress)
        active_build_id = active_build.group(1).strip().strip('"\'') if active_build and active_build.group(1).strip() not in {"null", "~"} else None
        escalation_match = re.search(r"(?m)^\s{2}required:\s*(true|false)\s*$", escalation)
        goals[goal_id] = {"initiative_id": initiative_id, "status": status, "scope_revision": int(revision_match.group(1)) if revision_match else None, "criteria": criteria, "required_criteria_statuses": required, "active_build_id": active_build_id, "accepted_build_ids": _yaml_list(progress, "accepted_build_ids"), "accepted_commit_shas": _yaml_list(progress, "accepted_commit_shas"), "escalation_required": bool(escalation_match and escalation_match.group(1) == "true")}
    return goals


def _validate_build_authorization(path: Path, data: dict[str, object], goals: dict[str, dict[str, object]], problems: list[str]) -> bool:
    rel = path.name
    authorization = data.get("authorization")
    auth = authorization if isinstance(authorization, dict) else {}
    legacy = data.get("approval")
    if data.get("status") == "approved" and not auth and isinstance(legacy, dict):
        reference, timestamp = legacy.get("reference"), legacy.get("approved_at")
        valid_legacy = all(isinstance(value, str) and value.strip() and not value.startswith("<") for value in (reference, timestamp))
        if not valid_legacy:
            problems.append(f"INVALID BUILD: {rel}: approval reference/time")
            return False
        return True
    reference, timestamp = auth.get("reference"), auth.get("authorized_at")
    valid_common = all(isinstance(value, str) and value.strip() and not value.startswith("<") for value in (reference, timestamp))
    if data.get("status") == "approved" and auth.get("type") == "human-build-approval":
        if not valid_common:
            problems.append(f"INVALID BUILD: {rel}: authorization reference/time")
            return False
        return True
    if data.get("status") != "authorized" or auth.get("type") != "goal-delegation" or not valid_common:
        problems.append(f"INVALID BUILD: {rel}: authorization")
        return False
    goal = goals.get(str(data.get("goal_id") or ""))
    if not goal or goal.get("status") != "active":
        problems.append(f"INVALID GOAL DELEGATION: {rel}: goal missing/not active")
        return False
    if data.get("initiative_id") != goal.get("initiative_id") or data.get("scope_revision") != goal.get("scope_revision") or not isinstance(data.get("scope_revision"), int) or data["scope_revision"] < 1:
        problems.append(f"INVALID GOAL DELEGATION: {rel}: initiative/scope revision mismatch")
        return False
    containment = data.get("containment")
    if not isinstance(containment, dict) or containment.get("status") != "PASS" or not _inside_root(path.parents[2], containment.get("evidence") if isinstance(containment.get("evidence"), str) else None):
        problems.append(f"INVALID GOAL DELEGATION: {rel}: containment")
        return False
    criterion_ids = containment.get("success_criterion_ids")
    if not isinstance(criterion_ids, list) or not criterion_ids or not all(isinstance(item, str) and item in goal["criteria"] for item in criterion_ids):
        problems.append(f"INVALID GOAL DELEGATION: {rel}: success criteria")
        return False
    return True


def _acceptance_test_results(text: str) -> dict[str, str]:
    columns: dict[str, int] = {}
    results: dict[str, str] = {}
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            columns = {}
            continue
        cells = [cell.strip().strip("` ") for cell in line.strip().strip("|").split("|")]
        normalized = [cell.lower() for cell in cells]
        if "layer" in normalized and "result" in normalized:
            columns = {"layer": normalized.index("layer"), "result": normalized.index("result")}
            continue
        if columns and len(cells) > max(columns.values()):
            layer = cells[columns["layer"]].lower()
            if layer in {"unit", "integration"}:
                results[layer] = cells[columns["result"]].lower()
    return results


def _evidenced_requirement_ids(text: str) -> set[str]:
    evidenced: set[str] = set()
    requirement_column: int | None = None
    result_column: int | None = None
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            normalized = [cell.strip("` ").lower() for cell in cells]
            if "requirement ids" in normalized and "result" in normalized:
                requirement_column = normalized.index("requirement ids")
                result_column = normalized.index("result")
                continue
            if requirement_column is not None and result_column is not None:
                if len(cells) > max(requirement_column, result_column):
                    result = cells[result_column].strip("` ").lower()
                    if result == "pass":
                        evidenced.update(
                            re.findall(
                                r"(?<![A-Za-z0-9_-])[A-Z][A-Z0-9_-]*-\d+(?![A-Za-z0-9_-])",
                                cells[requirement_column],
                            )
                        )
                continue
        else:
            requirement_column = None
            result_column = None
        if not re.search(r"(?i)requirement(?:\s+ids?|\s+coverage)?", line):
            continue
        if re.search(r"(?i)\b(fail(?:ed)?|not tested|missing|blocked)\b", line):
            continue
        evidenced.update(re.findall(r"(?<![A-Za-z0-9_-])[A-Z][A-Z0-9_-]*-\d+(?![A-Za-z0-9_-])", line))
    return evidenced


def _valid_goal_acceptance(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    required = ("Requirement coverage", "Criterion evidence", "Build commits", "Observed flows", "Intent reconciliation", "Worktree checkpoint")
    if not all(re.search(rf"(?mi)^#+\s*{re.escape(heading)}\s*$", text) for heading in required):
        return False
    if "<" in "\n".join(line for line in text.splitlines() if any(h.lower() in line.lower() for h in required)):
        return False
    return bool(re.search(r"(?mi)^Unauthorized outward actions:\s*none\s*$", text) and re.search(r"(?m)^- Decision:\s*`accepted`\s*$", text))


def _semantic_problems(root: Path) -> list[str]:
    problems: list[str] = []
    goals = _load_goals(root, problems)
    builds: dict[str, dict[str, object]] = {}
    valid_builds: set[str] = set()
    for path in sorted((root / "harness" / "builds").glob("B-*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"INVALID BUILD: {path.relative_to(root)}: {exc}"); continue
        if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("build_id"), str):
            problems.append(f"INVALID BUILD: {path.relative_to(root)}: schema_version/build_id"); continue
        build_id = str(data["build_id"])
        if build_id in builds:
            problems.append(f"DUPLICATE BUILD ID: {build_id}: {path.relative_to(root)}"); continue
        builds[build_id] = data
        phases = data.get("approved_phase_ids")
        if not isinstance(data.get("initiative_id"), str) or not re.fullmatch(r"I-\d{3,}", str(data["initiative_id"])) or not isinstance(data.get("plan_revision"), int) or data["plan_revision"] < 1 or not isinstance(phases, list) or not phases or not all(isinstance(item, str) and re.fullmatch(r"P-\d{3,}", item) for item in phases):
            problems.append(f"INVALID BUILD: {path.relative_to(root)}: core fields")
        elif _validate_build_authorization(path, data, goals, problems):
            valid_builds.add(build_id)

    for goal_id, goal in goals.items():
        active = goal["active_build_id"]
        if active and (active not in builds or builds[active].get("goal_id") != goal_id):
            problems.append(f"ACTIVE GOAL BUILD MISSING: {goal_id}: {active}")
        accepted_ids, shas = goal["accepted_build_ids"], goal["accepted_commit_shas"]
        if isinstance(accepted_ids, list) and isinstance(shas, list):
            for index, build_id in enumerate(accepted_ids):
                if index >= len(shas) or not re.fullmatch(r"[0-9a-fA-F]{7,64}", shas[index]):
                    problems.append(f"ACCEPTED BUILD WITHOUT SHA: {goal_id}: {build_id}")
        if goal["escalation_required"] and goal["status"] != "escalation_required":
            problems.append(f"INVALID GOAL ESCALATION STATE: {goal_id}")
        if goal["status"] == "accepted":
            if active or any(value != "met" for value in goal["required_criteria_statuses"].values()):
                problems.append(f"GOAL ACCEPTED WITHOUT MET CRITERIA: {goal_id}")
            acceptance = root / "harness" / "goals" / f"{goal_id}-ACCEPTANCE.md"
            if not acceptance.exists():
                problems.append(f"GOAL ACCEPTED WITHOUT EVIDENCE: {goal_id}")
            elif not _valid_goal_acceptance(acceptance):
                problems.append(f"INVALID GOAL ACCEPTANCE: {acceptance.relative_to(root)}")

    for path in (root / "harness" / "tasks").glob("P-*.md"):
        text = path.read_text(encoding="utf-8")
        status = _frontmatter_value(text, "status")
        if status == "blocked":
            fields = ("id", "kind", "reason", "owner", "waiting_for", "revisit_when", "next_action", "created_at")
            if _frontmatter_value(text, "blocker") == "null" or any(not re.search(rf"(?m)^\s{{2}}{field}:\s*\S+", text) for field in fields): problems.append(f"BLOCKED WITHOUT RECOVERY DATA: {path.relative_to(root)}")
            continue
        if status != "accepted": continue
        phase_id, build_id = _frontmatter_value(text, "task_id"), _frontmatter_value(text, "build_id")
        build = builds.get(build_id or "")
        if build_id not in valid_builds or not isinstance(build.get("approved_phase_ids") if build else None, list) or phase_id not in build["approved_phase_ids"]: problems.append(f"ACCEPTED WITHOUT APPROVED BUILD: {path.relative_to(root)}")
        acceptance_rel, verification_rel = _frontmatter_value(text, "acceptance_doc"), _frontmatter_value(text, "verification_evidence")
        applicability, baseline = _test_baseline(text)
        verification_contract = _indented_section(_frontmatter(text), "required_verification", 0)
        required_commands = _indented_list(verification_contract, "commands", 2)
        if not required_commands:
            problems.append(f"REQUIRED VERIFICATION COMMANDS MISSING: {path.relative_to(root)}")
        if applicability not in {"executable", "non-executable"}:
            problems.append(f"TEST BASELINE MISSING: {path.relative_to(root)}")
        for layer_name, layer in baseline.items():
            layer_status = layer["status"]
            if applicability == "executable" and layer_status != "required":
                problems.append(f"INVALID TEST BASELINE EXEMPTION: {path.relative_to(root)}: {layer_name}")
            elif applicability == "non-executable" and layer_status == "exempt":
                reason = str(layer["exemption_reason"] or "").strip()
                if not reason or reason.startswith("<"):
                    problems.append(f"INVALID TEST BASELINE EXEMPTION: {path.relative_to(root)}: {layer_name}")
            elif layer_status not in {"required", "exempt"}:
                problems.append(f"INVALID TEST BASELINE: {path.relative_to(root)}: {layer_name}")
            if layer_status == "required" and not layer["check_ids"]:
                problems.append(f"TEST BASELINE CHECK IDS MISSING: {path.relative_to(root)}: {layer_name}")
            if layer_name == "integration" and layer_status == "required" and (
                not layer["boundaries"] or any(not item or item.startswith("<") for item in layer["boundaries"])
            ):
                problems.append(f"INTEGRATION BOUNDARIES MISSING: {path.relative_to(root)}")
        acceptance = _inside_root(root, acceptance_rel)
        acceptance_text = ""
        if not acceptance or not acceptance.is_file(): problems.append(f"ACCEPTED WITHOUT EVIDENCE: {path.relative_to(root)}")
        else:
            acceptance_text = acceptance.read_text(encoding="utf-8")
            if not re.search(r"(?m)^- Decision:\s*`accepted`\s*$", acceptance_text): problems.append(f"INVALID ACCEPTANCE DECISION: {acceptance_rel}")
            if applicability in {"executable", "non-executable"}:
                if not re.search(r"(?mi)^##\s+Test baseline\s*$", acceptance_text):
                    problems.append(f"ACCEPTANCE TEST BASELINE MISSING: {acceptance_rel}")
                else:
                    test_results = _acceptance_test_results(acceptance_text)
                    for label in ("unit", "integration"):
                        if applicability == "executable" and test_results.get(label) != "pass":
                            problems.append(f"ACCEPTANCE TEST BASELINE INVALID: {acceptance_rel}: {label}")
                    if applicability == "executable" and not re.search(r"(?mi)^- Behavioral assertions verified:\s*`?yes`?\s*$", acceptance_text):
                        problems.append(f"BEHAVIORAL ASSERTIONS NOT VERIFIED: {acceptance_rel}")
                    boundary = re.search(r"(?mi)^- Integration boundaries exercised:\s*`?([^`\n]+)`?\s*$", acceptance_text)
                    if applicability == "executable" and (not boundary or boundary.group(1).strip().lower() in {"", "none", "not-applicable", "n/a"}):
                        problems.append(f"INTEGRATION BOUNDARIES NOT VERIFIED: {acceptance_rel}")
            evidenced_requirements = _evidenced_requirement_ids(acceptance_text)
            missing_requirements = [requirement for requirement in _frontmatter_list(text, "requirement_ids") if requirement not in evidenced_requirements]
            if missing_requirements: problems.append(f"ACCEPTED WITHOUT REQUIREMENT EVIDENCE: {path.relative_to(root)}: {', '.join(missing_requirements)}")
        verification = _inside_root(root, verification_rel)
        if not verification:
            problems.append(f"ACCEPTED WITHOUT PHASE VERIFICATION: {path.relative_to(root)}")
            continue
        try:
            verification_data = json.loads(verification.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"ACCEPTED WITHOUT VALID VERIFICATION: {path.relative_to(root)}: {exc}")
            continue
        if not isinstance(verification_data, dict):
            problems.append(f"ACCEPTED WITHOUT VALID VERIFICATION: {path.relative_to(root)}: root must be an object")
        elif verification_data.get("status") != "PASS" or verification_data.get("phase_id") != phase_id:
            problems.append(f"ACCEPTED WITHOUT VERIFY PASS: {path.relative_to(root)}")
        else:
            results = verification_data.get("results")
            passed_ids = {
                str(item.get("id"))
                for item in results
                if isinstance(results, list) and isinstance(item, dict) and item.get("status") == "PASS" and item.get("id")
            } if isinstance(results, list) else set()
            for check_id in required_commands:
                if check_id not in passed_ids:
                    problems.append(f"REQUIRED VERIFICATION CHECK NOT PASS: {path.relative_to(root)}: {check_id}")
            for layer_name, layer in baseline.items():
                if layer["status"] == "required":
                    for check_id in layer["check_ids"]:
                        if check_id not in passed_ids:
                            problems.append(f"TEST BASELINE CHECK NOT PASS: {path.relative_to(root)}: {layer_name}: {check_id}")
    return problems


def harness_check(root: Path) -> list[str]:
    root = root.resolve(); problems: list[str] = []
    try:
        level = load_level(root)
        meta = json.loads((root / ".harness-version").read_text(encoding="utf-8"))
    except Exception as exc:
        return [str(exc)]
    selected = meta.get("delivery_documents", []) if isinstance(meta, dict) else None
    if not isinstance(selected, list) or any(not isinstance(item, str) or item not in DELIVERY_DOCUMENTS for item in selected):
        problems.append(".harness-version has invalid delivery_documents")
        selected = []
    problems.extend(f"MISSING: {rel}" for rel in required_files(level, selected) if not (root / rel).exists())
    state = root / "harness" / "session" / "session-state.json"
    if state.exists():
        try: json.loads(state.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc: problems.append(f"session-state.json is not valid JSON: {exc}")
    problems.extend(_semantic_problems(root))
    return problems


def guard_command(command: str) -> tuple[bool, str]:
    cmd = (command or "").strip()
    if not cmd: return False, "Usage: safe_bash_guard <command string>"
    for pattern in DANGEROUS_PATTERNS:
        if pattern.lower() in cmd.lower(): return False, f"BLOCKED: dangerous command pattern detected: {pattern}"
    return True, "Command passed safe_bash_guard."
