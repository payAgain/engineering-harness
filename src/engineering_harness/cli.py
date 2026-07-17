"""CLI entrypoint: eh / python -m engineering_harness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from engineering_harness import FRAMEWORK_ROOT, read_version
from engineering_harness.audit import audit_project
from engineering_harness.branch import current_branch, ensure_working_branch, evaluate_branch
from engineering_harness.check import guard_command, harness_check, load_level
from engineering_harness.init import init_project


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="eh",
        description="Engineering Harness CLI (Windows-first, tool-agnostic).",
    )
    parser.add_argument("--version", action="store_true", help="Print framework version and exit")

    sub = parser.add_subparsers(dest="action")

    init_p = sub.add_parser("init", help="Initialize harness files into a target project")
    init_p.add_argument("target", type=Path, help="Target project directory")
    init_p.add_argument(
        "--level",
        choices=["Light", "Standard", "Full"],
        default="Standard",
        help="Harness depth (default: Standard)",
    )
    init_p.add_argument("--name", default="", help="Project name override")
    init_p.add_argument(
        "--docs",
        default="none",
        help="Delivery documents: none, recommended, all, or comma-separated document IDs",
    )
    init_p.add_argument("--force", action="store_true", help="Overwrite existing generated files")

    audit_p = sub.add_parser("audit", help="Audit an initialized project")
    audit_p.add_argument("target", type=Path, help="Target project directory")

    check_p = sub.add_parser("check", help="Run harness_check against a project")
    check_p.add_argument("target", type=Path, nargs="?", default=Path("."), help="Project root")

    guard_p = sub.add_parser("guard", help="Check a shell command for dangerous patterns")
    guard_p.add_argument(
        "shell_command",
        nargs=argparse.REMAINDER,
        help="Command string after optional --",
    )

    branch_p = sub.add_parser("branch-check", help="Fail if on protected main/master for implementation work")
    branch_p.add_argument("target", type=Path, nargs="?", default=Path("."), help="Project root")
    branch_p.add_argument(
        "--allow-protected",
        action="store_true",
        help="Allow main/master (docs/governance exception only)",
    )

    ensure_p = sub.add_parser("branch-new", help="Create and checkout a working branch (GitHub Flow)")
    ensure_p.add_argument("name", help="Slug or full branch name (e.g. login-api or feat/login-api)")
    ensure_p.add_argument("target", type=Path, nargs="?", default=Path("."), help="Project root")
    ensure_p.add_argument("--prefix", default="feat", help="Prefix when name has no slash (default: feat)")

    sub.add_parser("doctor", help="Show framework paths and Python runtime info")
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(read_version())
        return 0

    if not args.action:
        parser.print_help()
        return 2

    if args.action == "doctor":
        print(f"framework_root={FRAMEWORK_ROOT}")
        print(f"version={read_version()}")
        print(f"python={sys.executable}")
        print(f"protocol={FRAMEWORK_ROOT / 'PROTOCOL.md'}")
        return 0

    if args.action == "init":
        logs = init_project(
            args.target,
            level=args.level,
            project_name=(args.name or None),
            force=args.force,
            delivery_documents=args.docs,
        )
        for line in logs:
            print(line)
        print("")
        print("INIT DONE")
        print(f"Target: {args.target.resolve()}")
        print(f"Level: {args.level}")
        print(f"Framework: {read_version()}")
        print(f"Delivery documents: {args.docs}")
        print("Give any agent: <project>/harness/PROTOCOL.md (or framework PROTOCOL.md)")
        print("Branching: GitHub Flow — do not develop on main; use feat/* etc.")
        print(f"Next: python -m engineering_harness audit {args.target.resolve()}")
        return 0

    if args.action == "audit":
        code, lines = audit_project(args.target)
        for line in lines:
            print(line)
        return code

    if args.action == "check":
        root = args.target.resolve()
        problems = harness_check(root)
        if problems:
            for item in problems:
                print(item)
            print("HARNESS_CHECK FAIL")
            return 1
        print(f"HARNESS_CHECK PASS (level={load_level(root)}, layout=tool-agnostic)")
        return 0

    if args.action == "guard":
        parts = list(args.shell_command)
        if parts and parts[0] == "--":
            parts = parts[1:]
        command = " ".join(parts).strip()
        ok, message = guard_command(command)
        print(message)
        if not command:
            return 2
        return 0 if ok else 1

    if args.action == "branch-check":
        root = args.target.resolve()
        branch = current_branch(root)
        code, message = evaluate_branch(branch, allow_protected=args.allow_protected)
        print(message)
        if branch:
            print(f"current_branch={branch}")
        return code

    if args.action == "branch-new":
        root = args.target.resolve()
        code, lines = ensure_working_branch(root, args.name, prefix=args.prefix)
        for line in lines:
            print(line)
        return code

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
