"""API helpers for the real MOEFAS screens (localhost only).

The admin portal calls the gateway through /api (vite proxy). The login sets a session cookie, so the
Playwright request context of the page (page.request) is already authenticated.
Used to read the truth (list, fee components) and to seed data quickly, never to replace a UI check.
"""
from __future__ import annotations

import time

AUTO_PREFIX = "R4-AUTO"          # every scheme the suite creates starts with this, see tools/cleanup_r4_auto.sql
SCHEMES = "api/fas/v1/fas/moe-schemes"
FEE_TYPES = "api/billing/v1/fees/fee-types"

_counter = 0


def post_retry(req, url: str, data, tries: int = 6):
    """POST that waits and retries when the gateway answers 429 (too many requests), then pauses a little so a long run stays under the limit."""
    resp = req.post(url, data=data)
    for attempt in range(tries):
        if resp.status != 429:
            break
        time.sleep(8 + 4 * attempt)
        resp = req.post(url, data=data)
    time.sleep(0.4)
    return resp


def _body(resp):
    body = resp.json()
    return body.get("data") if isinstance(body, dict) and "data" in body else body


def unique_name(tag: str = "") -> str:
    """R4-AUTO-<tag>-<epoch seconds>-<n>. The backend refuses a duplicate scheme name."""
    global _counter
    _counter += 1
    return f"{AUTO_PREFIX}-{tag}-{int(time.time())}-{_counter}".replace("--", "-")


def window(slot: int | None = None) -> dict[str, str]:
    """A period far in the future that does not touch the seed schemes. slot moves to the next free period."""
    global _counter
    _counter += 1
    year = 2100 + 2 * (((int(time.time()) // 60) + _counter + (slot or 0)) % 400)
    return {
        "opens": f"{year}-01-01", "closes": f"{year}-06-30",
        "eff_from": f"{year + 1}-01-01", "eff_to": f"{year + 1}-12-31",
    }


def list_schemes(req, base: str) -> list[dict]:
    items: list[dict] = []
    page_no = 1
    while True:
        resp = req.get(f"{base}{SCHEMES}", params={"PageNumber": page_no, "PageSize": 100})
        assert resp.ok, f"GET moe-schemes returned {resp.status}"
        data = _body(resp)
        items += data["items"]
        if not data["metadata"]["hasNextPage"]:
            break
        page_no += 1
    return [i for i in items if not i.get("isDeleted")]


def get_scheme(req, base: str, scheme_id: str) -> dict:
    resp = req.get(f"{base}{SCHEMES}/{scheme_id}")
    assert resp.ok, f"GET moe-scheme {scheme_id} returned {resp.status}"
    return _body(resp)


def fee_components(req, base: str) -> list[dict]:
    """Active fee components not tied to a school, the same filter the wizard applies. [{id, name, type}]"""
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


def create_scheme(req, base: str, *, name: str, win: dict, component_ids: list[str],
                  status: str = "Draft", pct=(10, 20, 30)) -> tuple[bool, dict, str]:
    """POST a scheme. Returns (ok, data, message). One percentage per level for every component."""
    stages = ["PRIMARY", "SECONDARY", "PRE_UNIVERSITY"]
    subsidies = [{"educationStage": s, "feeComponentId": cid, "subsidyPercentage": p}
                 for cid in component_ids for s, p in zip(stages, pct)]
    payload = {
        "status": status, "name": name, "description": None,
        "openFrom": f"{win['opens']}T00:00:00", "openTo": f"{win['closes']}T23:59:59",
        "effectiveFrom": f"{win['eff_from']}T00:00:00", "effectiveTo": f"{win['eff_to']}T23:59:59",
        "isGhiEnabled": False, "ghiFrom": 0, "ghiTo": 0,
        "isPciEnabled": True, "pciFrom": 0, "pciTo": 1100,
        "incomeOperator": "OR", "nationalities": ["SC"],
        "subsidies": subsidies, "totalBudgetAmount": 1000,
    }
    resp = post_retry(req, f"{base}{SCHEMES}", payload)
    try:
        body = resp.json()
    except Exception:
        return False, {}, f"HTTP {resp.status}"
    ok = bool(resp.ok and body.get("isSuccess", True))
    return ok, (body.get("data") or {}), str(body.get("message") or "") + " " + "; ".join(body.get("errors") or [])


# ====================================================================== SBFAS (school user)
SBFAS = "api/v1/fas/sbfas-schemes"
ME = "api/iam/v1/auth/me"


def sbfas_window(slot: int = 0) -> dict:
    """Far future period for SBFAS schemes. The backend wants Application open from today or later, so use year 2300+."""
    y = 2300 + slot * 4
    return {"opens": f"{y}-01-01", "closes": f"{y}-06-30", "eff_from": f"{y + 1}-01-01", "eff_to": f"{y + 1}-12-31"}


def school_id(req, base: str) -> str:
    body = req.get(f"{base}{ME}").json()
    return (body.get("data") or {}).get("schoolId") or ""


def school_offerings(req, base: str) -> list[dict]:
    """Active grades of the school of the signed-in School user, sorted like the wizard (level code)."""
    sid = school_id(req, base)
    items = req.get(f"{base}api/v1/schools/{sid}/offerings").json()["data"]["items"]
    active = {i["academicLevelId"]: i for i in items if i.get("isActive")}
    import re as _re
    def natural(code: str):
        return [int(t) if t.isdigit() else t.lower() for t in _re.split(r"(\d+)", code)]
    return sorted(active.values(), key=lambda i: natural(i["levelCode"]))


def school_fee_components(req, base: str) -> list[dict]:
    return req.get(f"{base}api/v1/fees/fee-components/by-school?isActive=true").json()["data"]["items"]


def list_sbfas(req, base: str) -> list[dict]:
    out, page = [], 1
    while True:
        body = req.get(f"{base}{SBFAS}?pageNumber={page}&pageSize=50").json()["data"]
        out += body["items"]
        if not body["metadata"].get("hasNextPage"):
            return out
        page += 1


def get_sbfas(req, base: str, scheme_id: str) -> dict:
    return req.get(f"{base}{SBFAS}/{scheme_id}").json()["data"]


def create_sbfas(req, base: str, *, name: str, win: dict, fee_ids: list[str], offerings: list[dict], publish: bool = False, pct: int = 10):
    """POST a SBFAS scheme as the School user. Returns (ok, data, message)."""
    payload = {
        "name": name, "openFrom": win["opens"], "openTo": win["closes"],
        "effectiveFrom": win["eff_from"], "effectiveTo": win["eff_to"], "totalBudgetAmount": 1000,
        "nationalities": ["SC"], "isGhiEnabled": False, "ghiFrom": None, "ghiTo": None,
        "isPciEnabled": True, "pciFrom": 0, "pciTo": 1000, "incomeOperator": None,
        "feeComponents": [{"feeComponentId": f, "items": [{"academicLevelId": o["academicLevelId"], "subsidyPercentage": pct} for o in offerings]} for f in fee_ids],
        "publish": publish,
    }
    resp = post_retry(req, f"{base}{SBFAS}", payload)
    try:
        body = resp.json()
    except Exception:
        return False, {}, f"HTTP {resp.status}"
    ok = bool(resp.ok and body.get("isSuccess", True))
    return ok, (body.get("data") or {}), f"HTTP {resp.status} " + str(body.get("message") or "") + " " + "; ".join(str(e) for e in (body.get("errors") or []))


def delete_sbfas(req, base: str, scheme_id: str) -> bool:
    return req.delete(f"{base}{SBFAS}/{scheme_id}").ok
