from __future__ import annotations
import argparse
import csv
import json
import os
import shlex
import sys
import webbrowser
from copy import deepcopy
from pathlib import Path
from . import __version__
from .core import InputError, validate, snapshot, cashflow, stress, allocation
from .io import read_json, outside_repo, write_new
from .reports import markdown
from .resources import resource_path, public_page

def dump(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + "\n"

def _workspace_marker(root: Path) -> Path:
    return root / ".ofo" / "workspace.json"

def find_workspace(value: str | Path | None = None) -> Path:
    if value:
        root = outside_repo(value)
        if not root.is_dir():
            raise InputError(f"Workspace does not exist: {root}")
        return root
    env = os.environ.get("OFO_WORKSPACE")
    if env:
        return find_workspace(env)
    cwd = Path.cwd().resolve()
    for candidate in (cwd, *cwd.parents):
        if _workspace_marker(candidate).is_file():
            return outside_repo(candidate)
    raise InputError("No Open Family Office workspace found. Run 'ofo init PATH', cd into it, or pass --workspace PATH.")

def household_path(explicit: str | Path | None, workspace: str | Path | None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    return find_workspace(workspace) / "household.json"

def _add_workspace(sp):
    sp.add_argument("--workspace", help="Private workspace. Defaults to OFO_WORKSPACE or the nearest .ofo/workspace.json.")

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ofo",
        description="Open Family Office — local-first household wealth research for people and AI agents.",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a private workspace and install the portable agent kit")
    init.add_argument("workspace", help="New or empty directory outside the code installation")
    init.add_argument("--no-agent", action="store_true", help="Create only the data workspace")

    status = sub.add_parser("status", help="Show workspace and agent-kit readiness without printing private balances")
    _add_workspace(status)

    for command in ["validate", "snapshot", "cashflow", "overview"]:
        sp = sub.add_parser(command)
        sp.add_argument("household", nargs="?", help="Household JSON. Defaults to workspace/household.json")
        _add_workspace(sp)
        sp.add_argument("--format", choices=["json", "markdown"], default="json")
        if command in ["cashflow", "overview"]:
            sp.add_argument("--months", type=int, default=24)
        if command == "cashflow":
            sp.add_argument("--scenario")

    scenario = sub.add_parser("scenario", help="Run an explicit household scenario against the current workspace")
    scenario.add_argument("scenario")
    scenario.add_argument("--household")
    _add_workspace(scenario)
    scenario.add_argument("--months", type=int, default=24)
    scenario.add_argument("--format", choices=["json", "markdown"], default="markdown")

    compare = sub.add_parser("allocation", help="Compare a user-confirmed allocation policy with the household")
    compare.add_argument("policy")
    compare.add_argument("--household")
    _add_workspace(compare)
    compare.add_argument("--format", choices=["json", "markdown"], default="markdown")

    legacy_stress = sub.add_parser("stress", help=argparse.SUPPRESS)
    legacy_stress.add_argument("household")
    legacy_stress.add_argument("scenario")
    legacy_stress.add_argument("--months", type=int, default=24)
    legacy_stress.add_argument("--format", choices=["json", "markdown"], default="json")
    legacy_compare = sub.add_parser("compare-allocation", help=argparse.SUPPRESS)
    legacy_compare.add_argument("household")
    legacy_compare.add_argument("policy")
    legacy_compare.add_argument("--format", choices=["json", "markdown"], default="json")

    imp = sub.add_parser("import-csv", help="Append explicitly mapped cashflows to a new household file")
    imp.add_argument("csv_path")
    imp.add_argument("--household")
    _add_workspace(imp)
    imp.add_argument("--out", required=True)

    demo = sub.add_parser("demo", help="Run the bundled synthetic fixture; no API key or model required")
    demo.add_argument("--out", help="Optional new report directory outside the code installation")
    demo.add_argument("--open", action="store_true", help="Open the bundled interactive demo in your browser")

    agent = sub.add_parser("agent", help="Install, sync or inspect the workspace agent kit")
    agent_sub = agent.add_subparsers(dest="agent_action", required=True)
    for action in ("install", "sync", "status"):
        asp = agent_sub.add_parser(action)
        _add_workspace(asp)

    mcp_config = sub.add_parser("mcp-config", help="Print a read-only stdio MCP configuration for this workspace")
    _add_workspace(mcp_config)
    mcp_config.add_argument("--format", choices=["json", "command"], default="json")

    from .extended_cli import add_commands
    add_commands(sub)
    return p

def _init_workspace(path: str, with_agent: bool = True) -> Path:
    target = outside_repo(path)
    if target.exists() and any(target.iterdir()):
        raise InputError("Workspace must be new or empty; existing files will not be overwritten")
    target.mkdir(parents=True, exist_ok=True, mode=0o700)
    template = read_json(resource_path("agent/templates/household.json"))
    write_new(target / "household.json", dump(template))
    write_new(target / ".gitignore", "*\n!.gitignore\n")
    write_new(
        target / "PRIVATE.md",
        "PRIVATE WORKSPACE. Open Family Office does not encrypt this folder. "
        "Do not upload or commit it. Cloud model processing needs explicit consent.\n",
    )
    write_new(
        target / "README.md",
        "# My Open Family Office\n\n"
        "This is a private data workspace, not the public source repository.\n\n"
        "1. Open this folder in your file-aware AI agent and use the ofo-start skill.\n"
        "2. Or edit household.json manually, then run ofo validate and ofo overview.\n"
        "3. Run ofo scenario scenario.json for explicit what-if analysis.\n"
        "4. Run ofo dashboard --out reports/review.html for a private offline review page.\n",
    )
    for directory in ("evidence", "imports", "scenarios", "reports", ".ofo"):
        (target / directory).mkdir(parents=True, exist_ok=True, mode=0o700)
    write_new(
        _workspace_marker(target),
        dump({"format": 1, "open_family_office_version": __version__, "household": "household.json"}),
    )
    if with_agent:
        from .agent_kit import sync_agent_kit
        sync_agent_kit(target, initial=True)
    return target

def _status(root: Path) -> dict:
    household = root / "household.json"
    state = "missing"
    warnings = []
    if household.is_file():
        try:
            warnings = validate(read_json(household))
            state = "ready"
        except (InputError, OSError, ValueError, KeyError, TypeError) as exc:
            state = "needs_setup"
            warnings = [str(exc)]
    from .agent_kit import agent_kit_status
    return {
        "version": __version__,
        "workspace": str(root),
        "household": state,
        "warnings": warnings,
        "agent_kit": agent_kit_status(root),
        "network": "off by default",
    }

def _mcp_config(root: Path, fmt: str) -> str:
    command = sys.executable
    args = ["-m", "open_family_office.cli", "mcp"]
    if fmt == "command":
        prefix = f'OFO_WORKSPACE={shlex.quote(str(root))} ' if os.name != "nt" else f'set OFO_WORKSPACE={root} && '
        return prefix + " ".join(shlex.quote(v) for v in [command, *args]) + "\n"
    return dump({
        "mcpServers": {
            "open-family-office": {
                "command": command,
                "args": args,
                "env": {"OFO_WORKSPACE": str(root)},
            }
        }
    })

def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        from .extended_cli import execute
        if execute(args):
            return 0

        if args.command == "init":
            target = _init_workspace(args.workspace, with_agent=not args.no_agent)
            print(f"Created private workspace: {target}")
            print("Next: cd into it, open it in your file-aware agent, and use the ofo-start skill.")
            print("CLI-only path: edit household.json, then run 'ofo validate' and 'ofo overview'.")
            return 0

        if args.command == "status":
            print(dump(_status(find_workspace(args.workspace))), end="")
            return 0

        if args.command == "agent":
            root = find_workspace(args.workspace)
            from .agent_kit import sync_agent_kit, agent_kit_status
            if args.agent_action == "status":
                data = agent_kit_status(root)
            else:
                data = sync_agent_kit(root, initial=args.agent_action == "install")
            print(dump(data), end="")
            return 0

        if args.command == "mcp-config":
            print(_mcp_config(find_workspace(args.workspace), args.format), end="")
            return 0

        if args.command == "demo":
            h = read_json(resource_path("examples/household.synthetic.json"))
            s = read_json(resource_path("examples/scenarios/business-sale.json"))
            baseline = snapshot(h)
            forecast = cashflow(h)
            after = stress(h, s)
            print(markdown(baseline))
            print(f"Baseline 24-month closing cash: {forecast['ending_cash']} {h['base_currency']}")
            print(f"Sale-scenario 24-month closing cash: {after['cashflow']['ending_cash']} {h['base_currency']}")
            print("Synthetic assumptions only. No live data, agent inference, trading or returns forecast.")
            if args.out:
                directory = outside_repo(args.out)
                files = {
                    "snapshot.md": markdown(baseline),
                    "cashflow.md": markdown(forecast),
                    "business-sale.md": markdown(after["cashflow"]),
                    "snapshot.json": dump(baseline),
                }
                if directory.exists() and any((directory / name).exists() for name in files):
                    raise InputError("Demo output already exists; choose a new directory")
                for name, text in files.items():
                    write_new(directory / name, text)
                print(f"Reports: {directory}")
            if args.open:
                webbrowser.open(public_page("demo.html").as_uri())
            return 0

        if args.command == "import-csv":
            source = household_path(args.household, args.workspace)
            h = deepcopy(read_json(source))
            validate(h)
            with Path(args.csv_path).expanduser().open(encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream)
                expected = set(read_json(resource_path("examples/household.synthetic.json"))["cashflows"][0])
                if set(reader.fieldnames or []) != expected or len(reader.fieldnames or []) != len(expected):
                    raise InputError("CSV columns must exactly match the bundled cashflow template")
                rows = list(reader)
            if not rows:
                raise InputError("CSV contains no data rows")
            for row in rows:
                if None in row or any(v is None for v in row.values()):
                    raise InputError("Malformed CSV row")
                row["end_date"] = row["end_date"] or None
                h["cashflows"].append(row)
            validate(h)
            print(write_new(args.out, dump(h)))
            return 0

        if args.command == "scenario":
            h = read_json(household_path(args.household, args.workspace))
            data = stress(h, read_json(args.scenario), args.months)
        elif args.command == "allocation":
            h = read_json(household_path(args.household, args.workspace))
            data = allocation(h, read_json(args.policy))
        elif args.command == "stress":
            h = read_json(args.household)
            data = stress(h, read_json(args.scenario), args.months)
        elif args.command == "compare-allocation":
            h = read_json(args.household)
            data = allocation(h, read_json(args.policy))
        else:
            h = read_json(household_path(args.household, args.workspace))
            if args.command == "validate":
                data = {"valid": True, "warnings": validate(h)}
            elif args.command == "snapshot":
                data = snapshot(h)
            elif args.command == "cashflow":
                data = cashflow(h, args.months, read_json(args.scenario) if args.scenario else None)
            elif args.command == "overview":
                data = {"snapshot": snapshot(h), "cashflow": cashflow(h, args.months), "months": args.months}
            else:
                raise InputError(f"Unknown command: {args.command}")

        print(markdown(data) if args.format == "markdown" else dump(data), end="")
        return 0
    except (InputError, OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
