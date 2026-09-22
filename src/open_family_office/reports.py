from __future__ import annotations
import json
from decimal import Decimal
from typing import Any


def amount(v: str) -> str:
    return f"{Decimal(v):,.2f}"


def markdown(data: dict) -> str:
    if "gross_assets" in data:
        lines = [f"# Household snapshot — {data['name']}", "", f"As of {data['as_of']} · {data['currency']} · {'SYNTHETIC DEMO' if data['synthetic'] else 'PRIVATE DATA'}", "", "| Measure | Amount |", "|---|---:|"]
        for key in ["gross_assets", "liabilities", "net_worth", "spendable_cash", "available_within_7_days_after_haircuts", "eligible_allocation_capital"]:
            lines.append(f"| {key.replace('_', ' ').capitalize()} | {amount(data[key])} |")
        lines += ["", "## Asset classes (gross attributable asset values)", "", "| Class | Amount |", "|---|---:|"]
        lines += [f"| {k} | {amount(v)} |" for k, v in data["asset_classes"].items()]
        lines += ["", "## Notes"] + [f"- {n}" for n in data["notes"]]
        lines += ["", "## Data-quality flags"] + ([f"- {n}" for n in data["warnings"]] or ["No configured data-quality flags. This does not establish suitability or accuracy of supplied evidence."])
        return "\n".join(lines) + "\n"
    if "months_table" in data:
        lines = [f"# Cash budget — {data['scenario_label']}", "", f"Currency: {data['currency']} · Months: {data['months']}", "", f"Opening cash: {amount(data['opening_cash'])}", f"Ending cash: {amount(data['ending_cash'])}", f"Minimum month-end cash: {amount(data['minimum_month_end_cash'])}", f"First unfunded gap: {data['first_shortfall'] or 'None in this modelled period'}", "", "| Month | Stable | Variable | One-off / principal / sales | Outflows | Closing cash |", "|---|---:|---:|---:|---:|---:|"]
        for r in data["months_table"]:
            one = sum(Decimal(r[k]) for k in ["one_off_receipts", "principal_return", "asset_sale_receipts"])
            lines.append(f"| {r['month']} | {amount(r['stable_income'])} | {amount(r['variable_income'])} | {one:,.2f} | {amount(r['outflows'])} | {amount(r['closing_cash'])} |")
        for bridge in data["event_bridges"]:
            lines += ["", f"## Sale bridge — {bridge['asset_id']} ({bridge['month']})", f"Cash received: {amount(bridge['net_cash_received'])}; equity asset removed: {amount(bridge['equity_asset_removed'])}; event-only net-worth change: {amount(bridge['event_net_worth_delta'])}.", bridge["note"]]
        lines += ["", "## Assumptions"] + [f"- {n}" for n in data["assumptions"]]
        return "\n".join(lines) + "\n"
    return "# Model output\n\n```json\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n```\n"
