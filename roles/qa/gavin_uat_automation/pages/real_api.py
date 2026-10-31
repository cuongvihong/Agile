"""API helpers for R6 FAS Budget & Statistics on localhost Qatest (http://localhost:5173)."""
from __future__ import annotations

import re
import time

AUTO_PREFIX = "R6-AUTO"
MOE_SCHEMES = "api/fas/v1/fas/moe-schemes"
MOE_HQ_SCHEME_STATS = "api/fas/v1/fas/moehq/schemes/{id}/statistics"
MOE_HQ_SCHEME_PENDING = "api/fas/v1/fas/moehq/schemes/{id}/pending-allocations"
MOE_HQ_SCHEME_PREVIEW = "api/fas/v1/fas/moehq/schemes/{id}/allocations/preview"
MOE_HQ_SCHEME_CONFIRM = "api/fas/v1/fas/moehq/schemes/{id}/allocations/confirm"
MOE_HQ_SCHEME_REJECT = "api/fas/v1/fas/moehq/schemes/{id}/allocations/reject"

SBFAS_SCHEMES = "api/v1/fas/sbfas-schemes"
SCHOOL_SCHEME_STATS = "api/v1/fas/school/schemes/{id}/statistics"
SCHOOL_SCHEME_PENDING = "api/v1/fas/school/schemes/{id}/pending-allocations"
SCHOOL_SCHEME_PREVIEW = "api/v1/fas/school/schemes/{id}/allocations/preview"
SCHOOL_SCHEME_CONFIRM = "api/v1/fas/school/schemes/{id}/allocations/confirm"
SCHOOL_SCHEME_REJECT = "api/v1/fas/school/schemes/{id}/allocations/reject"

FEE_TYPES = "api/billing/v1/fees/fee-types"
ME = "api/iam/v1/auth/me"

SEEDED_MOE_SCHEME_ID = "MOE-SCH-2026"
SEEDED_MOEFAS_SCHEME_ID = SEEDED_MOE_SCHEME_ID
SEEDED_RI_SBFAS_SCHEME_ID = "SBFAS-SCH-RI-2026"
SEEDED_RPS_SBFAS_SCHEME_ID = "SBFAS-SCH-RPS-2026"
SEEDED_OTHER_SCHOOL_SBFAS_SCHEME_ID = SEEDED_RPS_SBFAS_SCHEME_ID

_counter = 0


def post_retry(req, url: str, data, tries: int = 6):
    resp = req.post(url, data=data)
    for attempt in range(tries):
        if resp.status != 429:
            break
        time.sleep(8 + 4 * attempt)
        resp = req.post(url, data=data)
    time.sleep(0.3)
    return resp


def _body(resp):
    body = resp.json()
    return body.get("data") if isinstance(body, dict) and "data" in body else body


def unique_name(tag: str = "") -> str:
    global _counter
    _counter += 1
    return f"{AUTO_PREFIX}-{tag}-{int(time.time())}-{_counter}".replace("--", "-")


def window(slot: int | None = None) -> dict[str, str]:
    global _counter
    _counter += 1
    year = 3600 + 4 * (((int(time.time() * 1000) % 900) + _counter * 13 + (slot or 0) * 7) % 1200)
    return {
        "opens": f"{year}-01-01",
        "closes": f"{year}-06-30",
        "eff_from": f"{year + 1}-01-01",
        "eff_to": f"{year + 1}-12-31",
    }


def sbfas_window(slot: int = 0) -> dict[str, str]:
    global _counter
    _counter += 1
    y = 2700 + ((slot + _counter + int(time.time()) % 50) * 4)
    return {
        "opens": f"{y}-01-01",
        "closes": f"{y}-06-30",
        "eff_from": f"{y + 1}-01-01",
        "eff_to": f"{y + 1}-12-31",
    }


def fee_components(req, base: str) -> list[dict]:
    types: list[dict] = []
    page_no = 1
    while True:
        resp = req.get(f"{base}{FEE_TYPES}/table", params={"PageNumber": page_no, "PageSize": 100, "IsActive": "true"})
        assert resp.ok, f"GET fee-types returned {resp.status}"
        data = _body(resp)
        types += data["items"]
        if not data["metadata"]["hasNextPage"]:
            break
        page_no += 1
    out = []
    for t in types:
        detail = _body(req.get(f"{base}{FEE_TYPES}/{t['id']}"))
        for c in detail.get("feeComponents") or []:
            if c.get("isActive") and c.get("school") is None:
                out.append({"id": c["id"], "name": c["name"], "type": t["name"]})
    return out


def create_moe_scheme_with_budget(
    req,
    base: str,
    *,
    name: str,
    win: dict,
    component_ids: list[str],
    budget,
    status: str = "Draft",
    pct=(10, 20, 30),
):
    stages = ["PRIMARY", "SECONDARY", "PRE_UNIVERSITY"]
    subsidies = [
        {"educationStage": s, "feeComponentId": cid, "subsidyPercentage": p}
        for cid in component_ids
        for s, p in zip(stages, pct)
    ]
    payload = {
        "status": status,
        "name": name,
        "description": "R6 budget test scheme",
        "openFrom": f"{win['opens']}T00:00:00",
        "openTo": f"{win['closes']}T23:59:59",
        "effectiveFrom": f"{win['eff_from']}T00:00:00",
        "effectiveTo": f"{win['eff_to']}T23:59:59",
        "isGhiEnabled": True,
        "ghiFrom": 0,
        "ghiTo": 4000,
        "isPciEnabled": True,
        "pciFrom": 0,
        "pciTo": 1100,
        "incomeOperator": "OR",
        "nationalities": ["SC"],
        "subsidies": subsidies,
        "totalBudgetAmount": budget,
    }
    resp = post_retry(req, f"{base}{MOE_SCHEMES}", payload)
    try:
        body = resp.json()
    except Exception:
        return resp.status, False, {}, f"HTTP {resp.status}"
    ok = bool(resp.ok and body.get("isSuccess", True))
    msg = str(body.get("message") or "") + " " + "; ".join(str(e) for e in (body.get("errors") or []))
    return resp.status, ok, (body.get("data") or {}), msg.strip()


def school_id(req, base: str) -> str:
    body = req.get(f"{base}{ME}").json()
    return (body.get("data") or {}).get("schoolId") or ""


def school_offerings(req, base: str) -> list[dict]:
    sid = school_id(req, base)
    items = req.get(f"{base}api/v1/schools/{sid}/offerings").json()["data"]["items"]
    active = {i["academicLevelId"]: i for i in items if i.get("isActive")}

    def natural(code: str):
        return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", code)]

    return sorted(active.values(), key=lambda i: natural(i["levelCode"]))


def school_fee_components(req, base: str) -> list[dict]:
    return req.get(f"{base}api/v1/fees/fee-components/by-school?isActive=true").json()["data"]["items"]


def create_sbfas_with_budget(
    req,
    base: str,
    *,
    name: str,
    win: dict,
    fee_ids: list[str],
    offerings: list[dict],
    budget,
    publish: bool = False,
    pct: int = 10,
):
    payload = {
        "name": name,
        "openFrom": win["opens"],
        "openTo": win["closes"],
        "effectiveFrom": win["eff_from"],
        "effectiveTo": win["eff_to"],
        "totalBudgetAmount": budget,
        "nationalities": ["SC"],
        "isGhiEnabled": False,
        "ghiFrom": None,
        "ghiTo": None,
        "isPciEnabled": True,
        "pciFrom": 0,
        "pciTo": 1000,
        "incomeOperator": None,
        "feeComponents": [
            {
                "feeComponentId": f,
                "items": [{"academicLevelId": o["academicLevelId"], "subsidyPercentage": pct} for o in offerings],
            }
            for f in fee_ids
        ],
        "publish": publish,
    }
    resp = post_retry(req, f"{base}{SBFAS_SCHEMES}", payload)
    try:
        body = resp.json()
    except Exception:
        return resp.status, False, {}, f"HTTP {resp.status}"
    ok = bool(resp.ok and body.get("isSuccess", True))
    msg = f"HTTP {resp.status} " + str(body.get("message") or "") + " " + "; ".join(str(e) for e in (body.get("errors") or []))
    return resp.status, ok, (body.get("data") or {}), msg.strip()


def delete_sbfas(req, base: str, scheme_id: str) -> bool:
    return req.delete(f"{base}{SBFAS_SCHEMES}/{scheme_id}").ok


def moefas_window(slot: int = 0) -> dict[str, str]:
    return window(slot)


def create_moefas_with_budget(
    req,
    base: str,
    *,
    name: str,
    win: dict,
    fee_ids: list[str],
    offerings: list[dict] | None = None,
    budget,
    publish: bool = False,
):
    return create_moe_scheme_with_budget(
        req,
        base,
        name=name,
        win=win,
        component_ids=fee_ids,
        budget=budget,
        status="Published" if publish else "Draft",
    )


def delete_moefas(req, base: str, scheme_id: str) -> bool:
    return req.delete(f"{base}{MOE_SCHEMES}/{scheme_id}").ok


def get_moefas_statistics(req, base: str, scheme_id: str):
    resp = req.get(f"{base}{MOE_HQ_SCHEME_STATS.format(id=scheme_id)}")
    try:
        data = _body(resp)
    except Exception:
        data = {}
    return resp.status, data


def get_sbfas_statistics(req, base: str, scheme_id: str):
    resp = req.get(f"{base}{SCHOOL_SCHEME_STATS.format(id=scheme_id)}")
    try:
        data = _body(resp)
    except Exception:
        data = {}
    return resp.status, data

