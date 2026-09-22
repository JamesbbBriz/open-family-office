from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any
from .core import InputError

REPO_ROOT = Path(__file__).resolve().parents[2]
MAX_INPUT_BYTES = 10_000_000


def unique_object(pairs: list[tuple[str, Any]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise InputError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path: str | Path) -> dict:
    path = Path(path).expanduser()
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise InputError("Input exceeds 10 MB limit")
    with path.open(encoding="utf-8-sig") as stream:
        data = json.load(stream, object_pairs_hook=unique_object,
                         parse_constant=lambda text: (_ for _ in ()).throw(InputError(f"Invalid JSON constant: {text}")))
    if not isinstance(data, dict):
        raise InputError("Top-level JSON must be an object")
    return data


def outside_repo(path: str | Path) -> Path:
    target = Path(path).expanduser().resolve()
    if target == REPO_ROOT or REPO_ROOT in target.parents:
        raise InputError("Private output must be outside the code repository")
    return target


def write_new(path: str | Path, content: str) -> Path:
    target = outside_repo(path)
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    # Exclusive creation: do not silently replace an existing household or report.
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(target, flags, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        stream.write(content)
    return target
