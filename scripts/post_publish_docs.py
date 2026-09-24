#!/usr/bin/env python3
"""Switch user-facing install docs from Git-source installs to PyPI after publication."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
GIT_SPEC = "git+https://github.com/JamesbbBriz/open-family-office.git"

FILES = (
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "docs/QUICKSTART.md",
)


def transform(text: str) -> str:
    # Prefer the shortest uvx form once the package exists on PyPI.
    text = text.replace(f"uvx --from {GIT_SPEC} ofo", "uvx open-family-office")
    # Remaining user-facing install commands can resolve the PyPI project directly.
    text = text.replace(GIT_SPEC, "open-family-office")
    return text


def main() -> int:
    changed = []
    for path in FILES:
        before = path.read_text(encoding="utf-8")
        after = transform(before)
        if before != after:
            path.write_text(after, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())
    if changed:
        print("Updated PyPI install docs:")
        for path in changed:
            print(f"- {path}")
    else:
        print("PyPI install docs already current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
