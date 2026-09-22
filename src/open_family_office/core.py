"""Small, auditable planning engine. No network, recommendations, or execution.

Amounts use Decimal, FX is base-currency units per foreign-currency unit.
The forecast is a cash budget, NOT a full projected balance sheet or return model.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any

ZERO = Decimal("0")
ONE = Decimal("1")
CLASSES = {"cash", "equity", "bond", "real_estate", "private_business", "private_credit", "commodity", "crypto", "collectible", "other"}

class InputError(ValueError):
    """Input is incomplete, ambiguous, or outside the supported model."""


def number(value: Any, label: str = "number") -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise InputError(f"{label}: use a decimal string, not a float or boolean")
    try:
        result = Decimal(value)
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise InputError(f"{label}: invalid decimal") from exc
    if not result.is_finite():
        raise InputError(f"{label}: NaN and Infinity are not allowed")
    return result


def money(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def fraction(value: Any, label: str) -> Decimal:
    result = number(value, label)
    if not ZERO <= result <= ONE:
        raise InputError(f"{label}: must be between 0 and 1")
    return result


def iso(value: Any, label: str) -> date:
    if not isinstance(value, str) or len(value) != 10:
        raise InputError(f"{label}: expected YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise InputError(f"{label}: invalid date") from exc


def required(obj: Any, keys: set[str], label: str) -> None:
    if not isinstance(obj, dict):
        raise InputError(f"{label}: expected an object")
    missing = keys - obj.keys()
    if missing:
        raise InputError(f"{label}: missing {', '.join(sorted(missing))}")


def only(obj: dict, keys: set[str], label: str) -> None:
    extra = obj.keys() - keys
    if extra:
        raise InputError(f"{label}: unsupported fields {', '.join(sorted(extra))}")


def ids(items: Any, label: str) -> set[str]:
    if not isinstance(items, list):
        raise InputError(f"{label}: expected a list")
    found: set[str] = set()
    for item in items:
        required(item, {"id"}, label)
        key = item["id"]
        if not isinstance(key, str) or not key or key in found:
            raise InputError(f"{label}: empty or duplicate id")
        found.add(key)
    return found


def fx_rate(h: dict, currency: str) -> Decimal:
    if currency == h["base_currency"]:
        return ONE
    if currency not in h["fx"]:
        raise InputError(f"Missing FX rate for {currency}; never assume parity")
    rate = number(h["fx"][currency]["base_per_unit"], f"FX {currency}")
    if rate <= ZERO:
        raise InputError("FX rate must be positive")
    return rate


def attributed_value(h: dict, obj: dict) -> Decimal:
    return number(obj["value"]) * fraction(obj["ownership_share"], "ownership_share") * fx_rate(h, obj["currency"])


def accessible(asset: dict) -> bool:
    return asset["restriction"] == "none"


def eligible(asset: dict) -> bool:
    return asset["investable"] and accessible(asset)


def validate(h: dict) -> list[str]:
    top = {"schema_version", "id", "name", "as_of", "base_currency", "synthetic", "entities", "assets", "liabilities", "cashflows", "fx", "evidence", "risk_preferences", "notes"}
    required(h, top, "household")
    only(h, top, "household")
    if h["schema_version"] != "1.0":
        raise InputError("Unsupported schema_version; expected 1.0")
    if type(h["synthetic"]) is not bool:
        raise InputError("synthetic must be boolean")
    if not isinstance(h["base_currency"], str) or len(h["base_currency"]) != 3 or not h["base_currency"].isupper():
        raise InputError("base_currency: use a three-letter uppercase code")
    asof = iso(h["as_of"], "as_of")
    entity_ids = ids(h["entities"], "entities")
    if not entity_ids:
        raise InputError("At least one entity is required")
    evidence_ids = ids(h["evidence"], "evidence")
    for e in h["entities"]:
        required(e, {"id", "label", "type"}, "entity")
        only(e, {"id", "label", "type"}, "entity")
    for e in h["evidence"]:
        required(e, {"id", "kind", "source", "as_of", "note"}, "evidence")
        only(e, {"id", "kind", "source", "as_of", "note"}, "evidence")
        iso(e["as_of"], "evidence.as_of")
        if e["kind"] not in {"synthetic", "user_statement", "document", "official_source", "assumption"}:
            raise InputError("Unsupported evidence kind")
    if not isinstance(h["fx"], dict):
        raise InputError("fx must be an object")
    warnings: list[str] = []
    for curr, observation in h["fx"].items():
        required(observation, {"base_per_unit", "as_of", "evidence_id"}, "fx")
        only(observation, {"base_per_unit", "as_of", "evidence_id"}, "fx")
        if observation["evidence_id"] not in evidence_ids:
            raise InputError("FX evidence does not exist")
        fxdate = iso(observation["as_of"], "fx.as_of")
        if fxdate > asof:
            raise InputError("Future FX observation cannot be used in historical snapshot")
        if (asof - fxdate).days > 7:
            warnings.append(f"FX {curr} is older than 7 days")
        if number(observation["base_per_unit"]) <= ZERO:
            raise InputError("FX must be positive")
        if curr == h["base_currency"] and number(observation["base_per_unit"]) != ONE:
            raise InputError("Base currency FX must equal 1")
    asset_ids = ids(h["assets"], "assets")
    liability_ids = ids(h["liabilities"], "liabilities")
    if asset_ids & liability_ids:
        raise InputError("Asset and liability ids must be distinct")
    common = {"id", "label", "value", "currency", "ownership_share", "owner_id", "valuation_date", "evidence_id"}
    for collection in ("assets", "liabilities"):
        for a in h[collection]:
            extra = {"class", "wrapper", "liquidity_days", "restriction", "investable", "liquidation_haircut", "valuation_basis"} if collection == "assets" else {"type"}
            required(a, common | extra, collection)
            only(a, common | extra, collection)
            if number(a["value"], a["id"]) < ZERO:
                raise InputError("Asset values and debt principal must be non-negative")
            fraction(a["ownership_share"], "ownership_share")
            if a["owner_id"] not in entity_ids or a["evidence_id"] not in evidence_ids:
                raise InputError(f"{a['id']}: missing entity/evidence reference")
            fx_rate(h, a["currency"])
            valued = iso(a["valuation_date"], "valuation_date")
            if valued > asof:
                raise InputError("Future valuation cannot enter current snapshot")
            if (asof - valued).days > 90:
                warnings.append(f"{a['id']}: valuation is older than 90 days")
            if collection == "assets":
                if a["class"] not in CLASSES:
                    raise InputError("Unknown asset class; use other with explicit evidence")
                if a["restriction"] not in {"none", "locked", "pledged"}:
                    raise InputError("restriction must be none, locked or pledged")
                if type(a["investable"]) is not bool:
                    raise InputError("investable must be boolean")
                if type(a["liquidity_days"]) is not int or a["liquidity_days"] < 0:
                    raise InputError("liquidity_days must be a nonnegative integer")
                fraction(a["liquidation_haircut"], "liquidation_haircut")
                if a["class"] == "private_business" and a["valuation_basis"] != "equity":
                    raise InputError("v0.1 requires private business EQUITY value, not enterprise value")
    ids(h["cashflows"], "cashflows")
    flow_fields = {"id", "label", "direction", "category", "recurrence", "nature", "amount", "currency", "start_date", "end_date", "evidence_id", "amount_basis"}
    for f in h["cashflows"]:
        required(f, flow_fields, "cashflow")
        only(f, flow_fields, "cashflow")
        if number(f["amount"], f["id"]) < ZERO:
            raise InputError("Cashflow amount must be positive; use direction")
        if f["direction"] not in {"in", "out"} or f["recurrence"] not in {"monthly", "one_off"}:
            raise InputError("Unsupported direction or recurrence")
        if f["nature"] not in {"stable", "variable", "one_off", "principal_return"}:
            raise InputError("Unsupported cashflow nature")
        if f["recurrence"] == "monthly" and f["nature"] in {"one_off", "principal_return"}:
            raise InputError("One-off receipts/principal returns cannot be recurring income")
        if f["recurrence"] == "one_off" and f["nature"] not in {"one_off", "principal_return"}:
            raise InputError("One-off cashflow must be identified as one_off or principal_return")
        if f["amount_basis"] != "household_net_after_tax":
            raise InputError("Supply attributable after-tax cashflow; tax calculation is not implemented")
        start = iso(f["start_date"], "start_date")
        if f["end_date"] is not None:
            end = iso(f["end_date"], "end_date")
            if end < start:
                raise InputError("Cashflow end_date precedes start_date")
        if f["evidence_id"] not in evidence_ids:
            raise InputError("Cashflow has unknown evidence")
        fx_rate(h, f["currency"])
    required(h["risk_preferences"], {"willingness", "note"}, "risk_preferences")
    only(h["risk_preferences"], {"willingness", "note"}, "risk_preferences")
    if h["risk_preferences"]["willingness"] not in {"unknown", "low", "medium", "high"}:
        raise InputError("Unknown willingness label")
    if h["risk_preferences"]["willingness"] == "unknown":
        warnings.append("Risk willingness has not been elicited; no suitability conclusion")
    return warnings


def snapshot(h: dict) -> dict:
    warnings = validate(h)
    assets_total = sum((attributed_value(h, a) for a in h["assets"]), ZERO)
    debts_total = sum((attributed_value(h, a) for a in h["liabilities"]), ZERO)
    cash = sum((attributed_value(h, a) for a in h["assets"] if a["class"] == "cash" and accessible(a) and a["liquidity_days"] == 0), ZERO)
    liquid7 = sum((attributed_value(h, a) * (ONE - number(a["liquidation_haircut"])) for a in h["assets"] if accessible(a) and a["liquidity_days"] <= 7), ZERO)
    by_class: dict[str, Decimal] = {}
    by_wrapper: dict[str, Decimal] = {}
    for a in h["assets"]:
        by_class[a["class"]] = by_class.get(a["class"], ZERO) + attributed_value(h, a)
        by_wrapper[a["wrapper"]] = by_wrapper.get(a["wrapper"], ZERO) + attributed_value(h, a)
    return {
        "name": h["name"], "as_of": h["as_of"], "currency": h["base_currency"], "synthetic": h["synthetic"],
        "gross_assets": money(assets_total), "liabilities": money(debts_total), "net_worth": money(assets_total - debts_total),
        "spendable_cash": money(cash), "available_within_7_days_after_haircuts": money(liquid7),
        "eligible_allocation_capital": money(sum((attributed_value(h, a) for a in h["assets"] if eligible(a)), ZERO)),
        "asset_classes": {k: money(v) for k, v in sorted(by_class.items())},
        "wrappers": {k: money(v) for k, v in sorted(by_wrapper.items())},
        "warnings": warnings,
        "notes": ["Wrappers are a separate view of the SAME assets: never add them to asset classes.",
                  "Spendable cash excludes securities, locked pensions, pledged balances and future receipts.",
                  "7-day liquidation values use user assumptions, not guaranteed sale proceeds."]
    }


def month_start(asof: date, offset: int) -> date:
    year_month = asof.year * 12 + asof.month - 1 + offset
    return date(year_month // 12, year_month % 12 + 1, 1)


def active(f: dict, month: date) -> bool:
    start = iso(f["start_date"], "start_date").replace(day=1)
    if f["recurrence"] == "one_off":
        return start == month
    end = iso(f["end_date"], "end_date").replace(day=1) if f["end_date"] else None
    return month >= start and (end is None or month <= end)


def validate_scenario(h: dict, scenario: dict | None) -> dict:
    if scenario is None:
        return {"id": "baseline", "label": "Baseline assumptions", "asset_shocks": {}, "cashflow_multipliers": {}, "sales": [], "note": "No return forecast"}
    keys = {"id", "label", "asset_shocks", "cashflow_multipliers", "sales", "note"}
    required(scenario, keys, "scenario")
    only(scenario, keys, "scenario")
    amap = {a["id"]: a for a in h["assets"]}
    fmap = {f["id"]: f for f in h["cashflows"]}
    if not isinstance(scenario["asset_shocks"], dict) or not isinstance(scenario["cashflow_multipliers"], dict) or not isinstance(scenario["sales"], list):
        raise InputError("Scenario shocks/multipliers must be objects and sales must be a list")
    for aid, change in scenario["asset_shocks"].items():
        if aid not in amap or number(change) < -ONE:
            raise InputError("Unknown asset or price shock below -100%")
        if amap[aid]["class"] == "cash":
            raise InputError("Cash price shocks unsupported; model a cash event explicitly")
    for fid, multiplier in scenario["cashflow_multipliers"].items():
        if fid not in fmap or number(multiplier) < ZERO:
            raise InputError("Unknown cashflow or negative multiplier")
    sold: set[str] = set()
    stopped: set[str] = set()
    for sale in scenario["sales"]:
        fields = {"asset_id", "month", "net_proceeds_base", "stop_cashflow_ids", "note"}
        required(sale, fields, "sale")
        only(sale, fields, "sale")
        aid = sale["asset_id"]
        if aid not in amap or aid in sold:
            raise InputError("Unknown or duplicate asset sale")
        if amap[aid]["class"] != "private_business" or not accessible(amap[aid]):
            raise InputError("v0.1 sale bridge supports unrestricted private-business equity only")
        if type(sale["month"]) is not int or not 1 <= sale["month"] <= 120:
            raise InputError("Sale month must be an integer in 1..120")
        if number(sale["net_proceeds_base"]) < ZERO:
            raise InputError("Sale proceeds cannot be negative")
        if not isinstance(sale["stop_cashflow_ids"], list):
            raise InputError("stop_cashflow_ids must be a list")
        for fid in sale["stop_cashflow_ids"]:
            if fid not in fmap or fid in stopped or fmap[fid]["direction"] != "in" or fmap[fid]["recurrence"] != "monthly":
                raise InputError("Sale stop_cashflow_ids must identify unique recurring inflows")
            stopped.add(fid)
        sold.add(aid)
    return scenario


def cashflow(h: dict, months: int = 24, scenario: dict | None = None) -> dict:
    validate(h)
    if type(months) is not int or not 1 <= months <= 120:
        raise InputError("months must be an integer in 1..120")
    scenario = validate_scenario(h, scenario)
    asof = iso(h["as_of"], "as_of")
    balance = number(snapshot(h)["spendable_cash"])
    opening = balance
    rows: list[dict] = []
    stopped: set[str] = set()
    first_shortfall = None
    min_balance = balance
    bridges: list[dict] = []
    amap = {a["id"]: a for a in h["assets"]}
    for offset in range(1, months + 1):
        month = month_start(asof, offset)
        stable = variable = once = principal = out = sales_cash = ZERO
        for sale in scenario["sales"]:
            if sale["month"] == offset:
                sales_cash += number(sale["net_proceeds_base"])
                stopped.update(sale["stop_cashflow_ids"])
                a = amap[sale["asset_id"]]
                disposed = attributed_value(h, a) * (ONE + number(scenario["asset_shocks"].get(a["id"], "0")))
                bridges.append({"month": month.isoformat()[:7], "asset_id": a["id"], "net_cash_received": sale["net_proceeds_base"], "equity_asset_removed": money(disposed), "event_net_worth_delta": money(number(sale["net_proceeds_base"]) - disposed), "note": "Event bridge only; proceeds are attributable after-tax amounts. Not a full future net-worth forecast."})
        for f in h["cashflows"]:
            if f["id"] in stopped or not active(f, month):
                continue
            amount = number(f["amount"]) * fx_rate(h, f["currency"]) * number(scenario["cashflow_multipliers"].get(f["id"], "1"))
            if f["direction"] == "out":
                out += amount
            elif f["nature"] == "principal_return":
                principal += amount
            elif f["recurrence"] == "one_off":
                once += amount
            elif f["nature"] == "stable":
                stable += amount
            else:
                variable += amount
        previous = balance
        balance += stable + variable + once + principal + sales_cash - out
        min_balance = min(min_balance, balance)
        if balance < ZERO and first_shortfall is None:
            first_shortfall = month.isoformat()[:7]
        rows.append({"month": month.isoformat()[:7], "opening_cash": money(previous), "stable_income": money(stable), "variable_income": money(variable), "one_off_receipts": money(once), "principal_return": money(principal), "asset_sale_receipts": money(sales_cash), "outflows": money(out), "closing_cash": money(balance)})
    return {"scenario": scenario["id"], "scenario_label": scenario["label"], "currency": h["base_currency"], "months": months, "opening_cash": money(opening), "ending_cash": money(balance), "minimum_month_end_cash": money(min_balance), "first_shortfall": first_shortfall, "months_table": rows, "event_bridges": bridges,
            "assumptions": ["Monthly budget begins in the next calendar month; current partial month is excluded.", "Negative cash is an UNFUNDED GAP, not an automatic overdraft or borrowing facility.", "No return, interest, inflation, tax, FX evolution or automatic asset liquidation is assumed.", "Debt-service outflows are entered once in cashflows; liabilities are snapshot principal, not deducted again.", "Monthly timing can hide intra-month shortfalls. A budget is not a probability forecast.", "Do not infer a future balance sheet from closing cash; debt amortisation and asset returns are not projected."]}


def stress(h: dict, scenario: dict, months: int = 24) -> dict:
    validate(h)
    scenario = validate_scenario(h, scenario)
    stressed = deepcopy(h)
    for a in stressed["assets"]:
        a["value"] = money(number(a["value"]) * (ONE + number(scenario["asset_shocks"].get(a["id"], "0"))))
    original = snapshot(h)
    shocked = snapshot(stressed)
    return {"scenario": scenario["id"], "label": scenario["label"], "original_snapshot": original, "instant_price_shock_snapshot": shocked, "instant_net_worth_change": money(number(shocked["net_worth"]) - number(original["net_worth"])), "cashflow": cashflow(h, months, scenario), "note": "Price shocks are immediate mark-to-market assumptions, not cash transactions. Future sales appear only in cashflow/event bridges."}


def allocation(h: dict, policy: dict) -> dict:
    validate(h)
    keys = {"id", "status", "targets", "minimum_cash_reserve_base", "note"}
    required(policy, keys, "policy")
    only(policy, keys, "policy")
    if policy["status"] != "user_confirmed":
        raise InputError("Allocation comparison requires user_confirmed targets")
    if not isinstance(policy["targets"], dict):
        raise InputError("Policy targets must be an object")
    weights = {k: fraction(v, k) for k, v in policy["targets"].items()}
    if not weights or any(k not in CLASSES for k in weights) or sum(weights.values(), ZERO) != ONE:
        raise InputError("Target classes must be valid and weights must sum exactly to 1")
    reserve = number(policy["minimum_cash_reserve_base"])
    if reserve < ZERO:
        raise InputError("Cash reserve cannot be negative")
    assets = [a for a in h["assets"] if eligible(a)]
    cash = sum((attributed_value(h, a) for a in assets if a["class"] == "cash" and a["liquidity_days"] == 0), ZERO)
    if reserve > cash:
        raise InputError("Cash reserve exceeds eligible cash; no allocation comparison produced")
    totals: dict[str, Decimal] = {}
    for a in assets:
        totals[a["class"]] = totals.get(a["class"], ZERO) + attributed_value(h, a)
    totals["cash"] = totals.get("cash", ZERO) - reserve
    capital = sum(totals.values(), ZERO)
    if capital <= ZERO:
        raise InputError("No positive residual capital after reserve")
    rows = []
    for c in sorted(set(totals) | set(weights)):
        current = totals.get(c, ZERO)
        target = capital * weights.get(c, ZERO)
        rows.append({"class": c, "current_value": money(current), "target_value": money(target), "difference": money(target - current)})
    return {"currency": h["base_currency"], "policy_id": policy["id"], "reserve_excluded": money(reserve), "residual_capital": money(capital), "comparison": rows, "note": "User-specified target comparison, NOT optimisation, suitability, a trade list, or a recommendation. Locked assets/non-investable assets are excluded. Taxes, costs and tradability are not solved."}
