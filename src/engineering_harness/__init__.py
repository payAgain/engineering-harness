"""Engineering Harness package."""

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = PACKAGE_ROOT.parents[1]
PACKAGED_RESOURCES = PACKAGE_ROOT / "resources"
FRAMEWORK_ROOT = PACKAGED_RESOURCES if PACKAGED_RESOURCES.is_dir() else SOURCE_ROOT


def read_version() -> str:
    version_file = FRAMEWORK_ROOT / "VERSION"
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    return "0.0.0"
