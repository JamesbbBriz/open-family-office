"""Build the offline Tailwind + Plotly dashboard from source or an installed wheel."""
from __future__ import annotations
import json
import re
from pathlib import Path
from . import __version__
from .core import snapshot, cashflow, stress, allocation, validate, active, fx_rate, number, month_start, iso
from .io import read_json, write_new
from .resources import resource_path, source_checkout
from .integrations.registry import providers

def _canonicalize(value):
    if isinstance(value, float):
        return round(value, 5)
    if isinstance(value, list):
        return [_canonicalize(v) for v in value]
    if isinstance(value, dict):
        return {k: _canonicalize(v) for k, v in value.items()}
    return value

def payload(h, scenarios=None, returns=None, simulation=None, policy=None):
    validate(h)
    cases = {
        "baseline": {
            "label": "Baseline",
            "snapshot": snapshot(h),
            "forecast": cashflow(h),
            "change": "0",
            "explanation": "Current assets and dated cash budget; not a future balance sheet.",
            "asset_shocks": {},
        }
    }
    for scenario in scenarios or []:
        result = stress(h, scenario)
        cases[scenario["id"]] = {
            "label": scenario["label"],
            "snapshot": result["instant_price_shock_snapshot"],
            "forecast": result["cashflow"],
            "change": result["instant_net_worth_change"],
            "explanation": scenario["note"],
            "asset_shocks": scenario["asset_shocks"],
        }
    for key, case in cases.items():
        scenario = next((s for s in (scenarios or []) if s["id"] == key), None)
        case["one_off_outflows"] = {}
        for i, row in enumerate(case["forecast"]["months_table"], 1):
            month = month_start(iso(h["as_of"], "as_of"), i)
            total = sum(
                (
                    number(flow["amount"])
                    * fx_rate(h, flow["currency"])
                    * number((scenario or {}).get("cashflow_multipliers", {}).get(flow["id"], "1"))
                    for flow in h["cashflows"]
                    if flow["direction"] == "out"
                    and flow["recurrence"] == "one_off"
                    and active(flow, month)
                ),
                number("0"),
            )
            case["one_off_outflows"][row["month"]] = float(total)

    quant = None
    if returns:
        import numpy as np
        from .quant.allocation import optimize, frontier
        quant = {
            "frontier": frontier(returns),
            "optimizers": {m: optimize(returns, "scipy", m) for m in ["min_variance", "risk_parity", "cvar"]},
            "correlation": np.corrcoef(np.asarray(returns["returns"]), rowvar=False).tolist(),
            "assets": returns["assets"],
            "synthetic": returns.get("synthetic", False),
        }

    sim = None
    if simulation:
        from .quant.simulation import simulate
        sim = simulate(simulation)

    compare = allocation(h, policy) if policy else None
    regular = sum(
        (
            number(flow["amount"]) * fx_rate(h, flow["currency"])
            for flow in h["cashflows"]
            if flow["direction"] == "out" and flow["recurrence"] == "monthly"
        ),
        number("0"),
    )
    return _canonicalize(
        {
            "version": __version__,
            "household": h,
            "cases": cases,
            "quant": quant,
            "simulation": sim,
            "allocation": compare,
            "reserve": float(compare["reserve_excluded"]) if compare else 0,
            "regular_monthly_outflows": float(regular),
            "providers": providers(),
            "disclosure": "Source data and chart scripts are embedded. No external network calls are required by this HTML.",
        }
    )

def render(data):
    from plotly.offline import get_plotlyjs
    root = resource_path("web/src")
    template = (root / "dashboard.html").read_text(encoding="utf-8")
    values = {
        "__TAILWIND_CSS__": (root / "tailwind.generated.css").read_text(encoding="utf-8"),
        "__APP_CSS__": (root / "dashboard.css").read_text(encoding="utf-8"),
        "__SHARED_CSS__": (root / "shared.css").read_text(encoding="utf-8"),
        "__SANDBOX_MATH__": (root / "sandbox.js").read_text(encoding="utf-8"),
        "__DASHBOARD_DATA__": json.dumps(data, ensure_ascii=True, allow_nan=False)
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"),
        "__PLOTLY_JS__": get_plotlyjs().replace("</script", "<\\/script"),
        "__APP_JS__": (root / "dashboard.js").read_text(encoding="utf-8"),
    }
    content = re.sub("|".join(map(re.escape, values)), lambda m: values[m.group(0)], template)
    licenses = resource_path("vendor/licenses")
    notice = "\n".join(p.read_text(encoding="utf-8") for p in sorted(licenses.glob("*.txt")))
    return content + "\n<!-- THIRD PARTY LICENSES\n" + notice.replace("--", "- -") + "\n-->\n"

def export_dashboard(h, out, scenarios=None, returns=None, simulation=None, policy=None):
    return write_new(out, render(payload(h, scenarios, returns, simulation, policy)))

def build_public_demo() -> Path:
    root = source_checkout()
    if root is None:
        raise RuntimeError("Rebuilding public/demo.html requires a source checkout")
    h = read_json(resource_path("examples/household.synthetic.json"))
    if h.get("synthetic") is not True:
        raise ValueError("Public build requires an explicitly synthetic fixture")
    scenarios_dir = resource_path("examples/scenarios")
    scenarios = [read_json(p) for p in sorted(scenarios_dir.glob("*.json"))]
    data = payload(
        h,
        scenarios,
        read_json(resource_path("examples/returns.synthetic.json")),
        read_json(resource_path("examples/simulation.synthetic.json")),
        read_json(resource_path("examples/policy.synthetic.json")),
    )
    target = root / "public/demo.html"
    target.write_text(render(data), encoding="utf-8")
    (root / "examples/dashboard-data.synthetic.json").write_text(
        json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    return target
