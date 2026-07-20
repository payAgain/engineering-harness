"""Setuptools hooks for bundling framework runtime resources."""

from pathlib import Path
import shutil

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


ROOT = Path(__file__).resolve().parent


class build_py(_build_py):
    """Copy protocol and templates into the installed package."""

    def run(self) -> None:
        super().run()
        resources = Path(self.build_lib) / "engineering_harness" / "resources"
        if resources.exists():
            shutil.rmtree(resources)
        resources.mkdir(parents=True)
        shutil.copy2(ROOT / "VERSION", resources / "VERSION")
        shutil.copy2(ROOT / "PROTOCOL.md", resources / "PROTOCOL.md")
        shutil.copytree(
            ROOT / "protocol" / "references",
            resources / "protocol" / "references",
            dirs_exist_ok=True,
        )
        shutil.copytree(
            ROOT / "assets" / "templates",
            resources / "assets" / "templates",
            dirs_exist_ok=True,
        )


setup(cmdclass={"build_py": build_py})
