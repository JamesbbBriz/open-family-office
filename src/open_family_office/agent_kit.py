"""Install and safely update the portable agent kit inside a private workspace."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from . import __version__
from .core import InputError
from .io import outside_repo
from .resources import resource_path

KIT_ITEMS = (
    ("AGENTS.md", "AGENTS.md"),
    ("CLAUDE.md", "CLAUDE.md"),
    ("GEMINI.md", "GEMINI.md"),
    ("agent", "agent"),
    (".agents/skills", ".agents/skills"),
    (".claude/skills", ".claude/skills"),
    (".claude/commands", ".claude/commands"),
)

def _digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _digest_file(path: Path) -> str:
    return _digest_bytes(path.read_bytes())

def _iter_files():
    for source_name, target_name in KIT_ITEMS:
        source = resource_path(source_name)
        if source.is_dir():
            for path in sorted(p for p in source.rglob("*") if p.is_file()):
                rel = Path(target_name) / path.relative_to(source)
                yield path, rel
        else:
            yield source, Path(target_name)

def _manifest_path(root: Path) -> Path:
    return root / ".ofo" / "agent-kit.json"

def _read_manifest(root: Path) -> dict:
    path = _manifest_path(root)
    if not path.is_file():
        return {"version": None, "files": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InputError(f"Invalid agent-kit manifest: {path}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("files", {}), dict):
        raise InputError("Invalid agent-kit manifest structure")
    return data

def _safe_target(root: Path, rel: Path) -> Path:
    if rel.is_absolute() or ".." in rel.parts:
        raise InputError("Agent-kit target must be relative")
    target = root / rel
    resolved_parent = target.parent.resolve()
    if resolved_parent != root and root not in resolved_parent.parents:
        raise InputError(f"Agent-kit path escapes workspace: {rel.as_posix()}")
    return target

def _write_atomic(target: Path, data: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if target.is_symlink():
        raise InputError(f"Refusing to replace symlink: {target}")
    tmp = target.with_name(target.name + ".ofo-tmp")
    if tmp.exists():
        tmp.unlink()
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink()

def sync_agent_kit(workspace: str | Path, *, initial: bool = False) -> dict:
    root = outside_repo(workspace)
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    old = _read_manifest(root)
    old_files = old.get("files", {})
    next_files: dict[str, dict] = {}
    result = {"version": __version__, "installed": [], "updated": [], "unchanged": [], "conflicts": []}

    upstream_paths = set()
    for source, rel in _iter_files():
        rel_text = rel.as_posix()
        upstream_paths.add(rel_text)
        data = source.read_bytes()
        upstream_hash = _digest_bytes(data)
        target = _safe_target(root, rel)
        previous = old_files.get(rel_text, {})
        managed_hash = previous.get("managed_hash") if isinstance(previous, dict) else previous
        current_hash = _digest_file(target) if target.is_file() and not target.is_symlink() else None

        if target.is_symlink():
            result["conflicts"].append(rel_text)
            next_files[rel_text] = {"managed_hash": managed_hash, "upstream_hash": upstream_hash}
            continue
        if current_hash == upstream_hash:
            result["unchanged"].append(rel_text)
            next_files[rel_text] = {"managed_hash": upstream_hash, "upstream_hash": upstream_hash}
            continue
        if current_hash is None:
            _write_atomic(target, data)
            result["installed"].append(rel_text)
            next_files[rel_text] = {"managed_hash": upstream_hash, "upstream_hash": upstream_hash}
            continue
        if not initial and managed_hash and current_hash == managed_hash:
            _write_atomic(target, data)
            result["updated"].append(rel_text)
            next_files[rel_text] = {"managed_hash": upstream_hash, "upstream_hash": upstream_hash}
            continue

        result["conflicts"].append(rel_text)
        next_files[rel_text] = {"managed_hash": managed_hash, "upstream_hash": upstream_hash}

    stale = sorted(set(old_files) - upstream_paths)
    result["stale"] = stale
    manifest = {
        "version": __version__,
        "source": "open-family-office",
        "files": next_files,
        "conflicts": result["conflicts"],
        "stale": stale,
    }
    manifest_path = _manifest_path(root)
    _write_atomic(manifest_path, (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode())
    return result

def agent_kit_status(workspace: str | Path) -> dict:
    root = outside_repo(workspace)
    manifest = _read_manifest(root)
    files = manifest.get("files", {})
    modified, missing = [], []
    for rel_text, entry in files.items():
        target = _safe_target(root, Path(rel_text))
        if not target.is_file() or target.is_symlink():
            missing.append(rel_text)
            continue
        managed_hash = entry.get("managed_hash") if isinstance(entry, dict) else entry
        if managed_hash and _digest_file(target) != managed_hash:
            modified.append(rel_text)
    return {
        "workspace": str(root),
        "installed_version": manifest.get("version"),
        "current_version": __version__,
        "managed_files": len(files),
        "modified": sorted(modified),
        "missing": sorted(missing),
        "conflicts": manifest.get("conflicts", []),
        "stale": manifest.get("stale", []),
    }
