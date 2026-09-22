"""Locate canonical resources in a source checkout or bundled copies in an installed wheel."""
from __future__ import annotations
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
BUNDLE_ROOT = PACKAGE_ROOT / "_bundled"
_SOURCE_CANDIDATE = PACKAGE_ROOT.parents[1]
SOURCE_ROOT = (
    _SOURCE_CANDIDATE
    if (_SOURCE_CANDIDATE / "pyproject.toml").is_file()
    and (_SOURCE_CANDIDATE / "agent").is_dir()
    else None
)

def resource_path(relative: str | Path) -> Path:
    relative = Path(relative)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Resource path must be relative")
    if SOURCE_ROOT is not None:
        candidate = SOURCE_ROOT / relative
        if candidate.exists():
            return candidate
    bundled = BUNDLE_ROOT / relative
    if bundled.exists():
        return bundled
    raise FileNotFoundError(f"Open Family Office resource is not installed: {relative.as_posix()}")

def source_checkout() -> Path | None:
    return SOURCE_ROOT

def public_page(name: str = "demo.html") -> Path:
    if name not in {"index.html", "demo.html"}:
        raise ValueError("Unknown public page")
    return resource_path(Path("public") / name)
