"""Build hook that bundles canonical project resources into installed wheels.

The source tree remains canonical. Installed CLI users still receive templates,
agent skills/workflows and the offline web UI without needing a Git checkout.
"""
from __future__ import annotations
from pathlib import Path
import shutil
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

ROOT = Path(__file__).resolve().parent
BUNDLE_ITEMS = (
    ("agent", "agent"),
    (".agents/skills", ".agents/skills"),
    (".claude/skills", ".claude/skills"),
    (".claude/commands", ".claude/commands"),
    ("web/src", "web/src"),
    ("web/config", "web/config"),
    ("vendor/licenses", "vendor/licenses"),
    ("examples", "examples"),
    ("AGENTS.md", "AGENTS.md"),
    ("CLAUDE.md", "CLAUDE.md"),
    ("GEMINI.md", "GEMINI.md"),
    ("public/index.html", "public/index.html"),
    ("public/demo.html", "public/demo.html"),
    ("public/.nojekyll", "public/.nojekyll"),
    ("public/_headers", "public/_headers"),
)

class build_py(_build_py):
    def run(self):
        super().run()
        bundle = Path(self.build_lib) / "open_family_office" / "_bundled"
        for source_name, destination_name in BUNDLE_ITEMS:
            source = ROOT / source_name
            if not source.exists():
                raise RuntimeError(f"Required bundle source missing: {source_name}")
            destination = bundle / destination_name
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(
                    source, destination, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.zip"),
                )
            else:
                shutil.copy2(source, destination)

setup(cmdclass={"build_py": build_py})
