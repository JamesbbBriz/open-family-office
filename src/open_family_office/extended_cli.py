"""Advanced CLI commands; lazy imports keep the common path lightweight."""
from __future__ import annotations
import importlib.metadata
import importlib.util
import json
import os
import platform
import sys
import webbrowser
from pathlib import Path
from . import __version__
from .core import InputError
from .io import read_json, write_new

def add_commands(sub):
    doctor = sub.add_parser("doctor", help="Report installation and optional integration readiness without exposing secrets")
    doctor.add_argument("--workspace")
    sub.add_parser("providers", help="List implemented provider capabilities and verification status")

    fetch = sub.add_parser("fetch", help="Explicit read-only external retrieval into an evidence envelope")
    fetch.add_argument("provider")
    fetch.add_argument("capability")
    fetch.add_argument("--query", required=True)
    fetch.add_argument("--allow-network", action="store_true")
    fetch.add_argument("--out")

    for name in ("optimize", "simulate", "lookthrough", "exposures", "extract-pdf", "import-ofx", "import-holdings"):
        command = sub.add_parser(name)
        command.add_argument("input")
        command.add_argument("--out")
        if name == "optimize":
            command.add_argument("--engine", choices=["scipy", "skfolio", "pypfopt"], default="scipy")
            command.add_argument(
                "--method",
                choices=["min_variance", "risk_parity", "cvar", "hrp", "black_litterman"],
                default="min_variance",
            )

    mcp = sub.add_parser("mcp", help="Start the read-only stdio MCP server")
    mcp.add_argument("--workspace", help="Private workspace; otherwise OFO_WORKSPACE is required")

    dashboard = sub.add_parser("dashboard", help="Export a private standalone HTML dashboard")
    dashboard.add_argument("input", nargs="?", help="Household JSON; defaults to workspace/household.json")
    dashboard.add_argument("--workspace")
    dashboard.add_argument("--out", required=True)
    dashboard.add_argument("--scenario", action="append", default=[])
    dashboard.add_argument("--returns")
    dashboard.add_argument("--simulation")
    dashboard.add_argument("--policy")
    dashboard.add_argument("--open", action="store_true", help="Open the exported HTML after writing it")

def execute(args):
    command = args.command

    if command in ("providers", "doctor"):
        from .integrations.registry import providers
        data = {"providers": providers()}
        if command == "doctor":
            packages = {
                "plotly": "plotly",
                "numpy": "numpy",
                "pandas": "pandas",
                "scipy": "scipy",
                "scikit-learn": "sklearn",
                "skfolio": "skfolio",
                "PyPortfolioOpt": "pypfopt",
                "mcp": "mcp",
                "pypdf": "pypdf",
                "ofxparse": "ofxparse",
                "yfinance": "yfinance",
            }
            data = {
                "open_family_office": __version__,
                "python": platform.python_version(),
                "executable": sys.executable,
                "dependencies": {},
                "providers": providers(),
                "network": "off until explicitly requested",
                "openbb_process": "configured" if os.environ.get("OPENBB_PYTHON") else "not configured",
            }
            for package, module in packages.items():
                try:
                    version = importlib.metadata.version(package)
                except importlib.metadata.PackageNotFoundError:
                    version = None
                data["dependencies"][package] = {
                    "installed": importlib.util.find_spec(module) is not None,
                    "version": version,
                }
            if getattr(args, "workspace", None):
                from .cli import find_workspace
                from .agent_kit import agent_kit_status
                root = find_workspace(args.workspace)
                data["workspace"] = agent_kit_status(root)

    elif command == "fetch":
        from .integrations.providers import fetch
        data = fetch(args.provider, args.capability, json.loads(args.query), allow_network=args.allow_network)

    elif command == "optimize":
        from .quant.allocation import optimize
        data = optimize(read_json(args.input), args.engine, args.method)

    elif command == "simulate":
        from .quant.simulation import simulate
        data = simulate(read_json(args.input))

    elif command == "lookthrough":
        from .quant.ownership import consolidate
        data = consolidate(read_json(args.input))

    elif command == "exposures":
        from .quant.ownership import exposures
        data = exposures(read_json(args.input)["positions"])

    elif command in ("extract-pdf", "import-ofx", "import-holdings"):
        from .integrations.documents import extract_pdf, import_ofx, holdings_csv
        data = {
            "extract-pdf": extract_pdf,
            "import-ofx": import_ofx,
            "import-holdings": holdings_csv,
        }[command](args.input)

    elif command == "mcp":
        if args.workspace:
            from .cli import find_workspace
            os.environ["OFO_WORKSPACE"] = str(find_workspace(args.workspace))
        from .integrations.mcp_server import main
        main()
        return True

    elif command == "dashboard":
        from .cli import household_path
        from .dashboard import export_dashboard
        household = read_json(household_path(args.input, args.workspace))
        output = export_dashboard(
            household,
            Path(args.out),
            [read_json(path) for path in args.scenario],
            returns=read_json(args.returns) if args.returns else None,
            simulation=read_json(args.simulation) if args.simulation else None,
            policy=read_json(args.policy) if args.policy else None,
        )
        print(output)
        if args.open:
            webbrowser.open(Path(output).resolve().as_uri())
        return True

    else:
        return False

    text = json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if getattr(args, "out", None):
        print(write_new(args.out, text))
    else:
        print(text, end="")
    return True
