"""Engineering Harness package."""

from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[2]


def read_version() -> str:
    version_file = FRAMEWORK_ROOT / "VERSION"
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    return "0.0.0"
