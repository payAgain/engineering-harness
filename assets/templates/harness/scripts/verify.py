#!/usr/bin/env python3
"""Run configured project checks and write machine-readable verification evidence."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PLACEHOLDERS = {
    "",
    "<fill-build-command>",
    "<fill-test-command>",
    "<fill-lint-command-or-na>",
    "n/a",
    "na",
}


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _load_config(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("verification.json schema_version must be 1")
    checks = data.get("checks")
    if not isinstance(checks, list) or not checks:
        raise ValueError("verification.json checks must be a non-empty list")
    return data


def _configured(command: object) -> bool:
    return isinstance(command, str) and command.strip().lower() not in PLACEHOLDERS


def _write_evidence(path: Path, evidence: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run project verification contract")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--evidence", type=Path, default=None)
    parser.add_argument("--phase", default=None, help="Phase ID recorded in evidence")
    args = parser.parse_args()

    root = args.root.resolve()
    config_path = (args.config or root / "harness" / "verification.json").resolve()
    evidence_path = (args.evidence or root / "harness" / "evidence" / "verification-latest.json").resolve()
    started_at = _now()
    results: list[dict[str, Any]] = []
    final_status = "PASS"

    print("=== HARNESS ===")
    check = Path(__file__).with_name("harness_check.py")
    harness_proc = subprocess.run([sys.executable, str(check), "--root", str(root)], check=False)
    if harness_proc.returncode != 0:
        final_status = "FAIL"
        results.append({"id": "harness", "status": "FAIL", "exit_code": harness_proc.returncode})
    else:
        results.append({"id": "harness", "status": "PASS", "exit_code": 0})

    if final_status != "FAIL":
        try:
            config = _load_config(config_path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            final_status = "INCOMPLETE"
            results.append({"id": "configuration", "status": "INCOMPLETE", "message": str(exc)})
        else:
            seen: set[str] = set()
            for index, item in enumerate(config["checks"]):
                if not isinstance(item, dict):
                    final_status = "INCOMPLETE"
                    results.append({"id": f"check-{index + 1}", "status": "INCOMPLETE", "message": "check must be an object"})
                    continue

                check_id = str(item.get("id") or "").strip()
                required = item.get("required") is True
                command = item.get("command")
                if not check_id or check_id in seen:
                    final_status = "INCOMPLETE"
                    results.append({"id": check_id or f"check-{index + 1}", "status": "INCOMPLETE", "message": "check id must be unique and non-empty"})
                    continue
                seen.add(check_id)

                if not _configured(command):
                    status = "INCOMPLETE" if required else "NOT_APPLICABLE"
                    if required:
                        final_status = "INCOMPLETE"
                    results.append({"id": check_id, "required": required, "status": status, "command": command})
                    print(f"=== {check_id.upper()} [{status}] ===")
                    continue

                cwd_value = item.get("cwd", ".")
                cwd = (root / str(cwd_value)).resolve()
                print(f"=== {check_id.upper()} ===")
                print(f"$ {command}")
                try:
                    proc = subprocess.run(str(command), cwd=str(cwd), shell=True, check=False)
                except OSError as exc:
                    proc_result = {"id": check_id, "required": required, "status": "FAIL", "command": command, "cwd": str(cwd), "message": str(exc)}
                    if required:
                        final_status = "FAIL"
                else:
                    status = "PASS" if proc.returncode == 0 else "FAIL"
                    proc_result = {"id": check_id, "required": required, "status": status, "command": command, "cwd": str(cwd), "exit_code": proc.returncode}
                    if required and proc.returncode != 0:
                        final_status = "FAIL"
                results.append(proc_result)

    evidence = {
        "schema_version": 1,
        "status": final_status,
        "started_at": started_at,
        "finished_at": _now(),
        "project_root": str(root),
        "phase_id": args.phase,
        "config": str(config_path),
        "results": results,
    }
    try:
        _write_evidence(evidence_path, evidence)
        print(f"Evidence: {evidence_path}")
    except OSError as exc:
        print(f"VERIFY FAIL [EVIDENCE]: {exc}")
        return 1

    print(f"VERIFY {final_status}")
    return 0 if final_status == "PASS" else 2 if final_status == "INCOMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
