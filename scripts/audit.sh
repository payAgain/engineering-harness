#!/usr/bin/env bash
# Thin wrapper around the Python CLI.
set -euo pipefail
TARGET="${1:?usage: audit.sh <target>}"
FRAMEWORK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="${FRAMEWORK_ROOT}/src${PYTHONPATH:+:$PYTHONPATH}"
exec python -m engineering_harness audit "$TARGET"
