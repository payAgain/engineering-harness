"""Black-box smoke test for the built wheel consumer experience."""

from __future__ import annotations

import glob
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import venv


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="eh-wheel-consumer-") as tmp:
        root = Path(tmp)
        wheel_dir = root / "wheel"
        wheel_dir.mkdir()
        subprocess.run(
            [sys.executable, "-m", "pip", "wheel", ".", "--no-deps", "-w", str(wheel_dir)],
            cwd=repository,
            check=True,
        )
        wheels = glob.glob(str(wheel_dir / "*.whl"))
        if len(wheels) != 1:
            raise RuntimeError(f"expected one wheel, found {wheels}")

        environment = root / "venv"
        venv.EnvBuilder(with_pip=True).create(environment)
        scripts = environment / ("Scripts" if os.name == "nt" else "bin")
        python = scripts / ("python.exe" if os.name == "nt" else "python")
        eh = scripts / ("eh.exe" if os.name == "nt" else "eh")
        subprocess.run([str(python), "-m", "pip", "install", "--no-deps", wheels[0]], check=True)

        version = subprocess.run([str(eh), "--version"], check=True, capture_output=True, text=True)
        expected = (repository / "VERSION").read_text(encoding="utf-8").strip()
        if version.stdout.strip() != expected:
            raise RuntimeError(f"installed version {version.stdout.strip()!r} != {expected!r}")

        target = root / "generated"
        subprocess.run([str(eh), "doctor"], cwd=root, check=True)
        subprocess.run(
            [str(eh), "init", str(target), "--level", "Standard", "--name", "wheel-consumer"],
            cwd=root,
            check=True,
        )
        subprocess.run([str(eh), "audit", str(target)], cwd=root, check=True)

        protocol = target / "harness" / "PROTOCOL.md"
        packet = target / "harness" / "tasks" / "_PACKET.template.md"
        if not protocol.is_file() or not packet.is_file():
            raise RuntimeError("installed wheel did not generate packaged protocol/templates")

    print("WHEEL CONSUMER PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
