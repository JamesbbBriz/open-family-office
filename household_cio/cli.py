from __future__ import annotations
import argparse
import csv
import json
import sys
from copy import deepcopy
from pathlib import Path
from .core import InputError, validate, snapshot, cashflow, stress, allocation
from .io import REPO_ROOT, read_json, outside_repo, write_new
from .reports import markdown


def dump(obj: dict) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Offline household-planning tools; no product recommendations or trading.")
    sub = p.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Create an empty PRIVATE workspace outside this repo")
    init.add_argument("--workspace", required=True)
    for command in ["validate", "snapshot", "cashflow", "stress", "allocate"]:
        sp = sub.add_parser(command)
        sp.add_argument("household")
        sp.add_argument("--format", choices=["json", "markdown"], default="json")
        if command in ["cashflow", "stress"]:
            sp.add_argument("--months", type=int, default=24)
        if command == "stress":
            sp.add_argument("scenario")
        elif command == "cashflow":
            sp.add_argument("--scenario")
        elif command == "allocate":
            sp.add_argument("policy")
    imp = sub.add_parser("import-csv", help="Append explicitly mapped cashflows; never edit original")
    imp.add_argument("csv_path")
    imp.add_argument("--household", required=True)
    imp.add_argument("--out", required=True)
    demo = sub.add_parser("demo", help="Run the bundled synthetic fixture; no API key or model needed")
    demo.add_argument("--out", help="Optional new directory OUTSIDE the repository")
    from .extended_cli import add_commands
    add_commands(sub)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        from .extended_cli import execute
        if execute(args):
            return 0
        if args.command == "init":
            target = outside_repo(args.workspace)
            if target.exists() and any(target.iterdir()):
                raise InputError("Workspace must be new or empty; existing files will not be overwritten")
            template = read_json(REPO_ROOT / "templates/household.json")
            path = write_new(target / "household.json", dump(template))
            write_new(target / ".gitignore", "*\n!.gitignore\n")
            write_new(target / "PRIVATE.md", "PRIVATE WORKSPACE. Not encrypted by this project. Do not upload or commit. Cloud model processing needs explicit consent.\n")
            print(f"Created {path}. Fill required fields with the setup skill; template is intentionally not a completed profile.")
            return 0
        if args.command == "demo":
            h = read_json(REPO_ROOT / "examples/household.synthetic.json")
            s = read_json(REPO_ROOT / "examples/scenarios/business-sale.json")
            baseline = snapshot(h)
            forecast = cashflow(h)
            after = stress(h, s)
            print(markdown(baseline))
            print(f"Baseline 24-month closing cash: {forecast['ending_cash']} {h['base_currency']}")
            print(f"Sale-scenario 24-month closing cash: {after['cashflow']['ending_cash']} {h['base_currency']}")
            print("Synthetic assumptions only. No live data, agent inference, trading or returns forecast.")
            if args.out:
                directory = outside_repo(args.out)
                files = {"snapshot.md": markdown(baseline), "cashflow.md": markdown(forecast), "business-sale.md": markdown(after["cashflow"]), "snapshot.json": dump(baseline)}
                if directory.exists() and any((directory / name).exists() for name in files):
                    raise InputError("Demo output already exists; choose a new directory")
                for name, text in files.items():
                    write_new(directory / name, text)
                print(f"Reports: {directory}")
            return 0
        if args.command == "import-csv":
            h = deepcopy(read_json(args.household))
            validate(h)
            with Path(args.csv_path).expanduser().open(encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream)
                expected = set(read_json(REPO_ROOT / "examples/household.synthetic.json")["cashflows"][0])
                if set(reader.fieldnames or []) != expected or len(reader.fieldnames or []) != len(expected):
                    raise InputError("CSV columns must exactly match templates/cashflows.csv")
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
        h = read_json(args.household)
        if args.command == "validate":
            data = {"valid": True, "warnings": validate(h)}
        elif args.command == "snapshot":
            data = snapshot(h)
        elif args.command == "cashflow":
            data = cashflow(h, args.months, read_json(args.scenario) if args.scenario else None)
        elif args.command == "stress":
            data = stress(h, read_json(args.scenario), args.months)
        else:
            data = allocation(h, read_json(args.policy))
        print(markdown(data) if args.format == "markdown" else dump(data), end="")
        return 0
    except (InputError, OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
