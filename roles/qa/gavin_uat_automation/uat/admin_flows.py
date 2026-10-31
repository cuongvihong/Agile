"""Reusable pieces of the Admin Portal UAT cases (MOE HQ and School users)."""
from __future__ import annotations

import re
import time
from decimal import Decimal

from playwright.sync_api import Page

from pages import real_api
from uat import env

MONEY = r"(?:SGD|S\$|\$)?\s*([\d,]+(?:\.\d+)?)"


def uat_name(tag: str) -> str:
    """A name that is easy to find (and to clean up) in the scheme lists."""
    return f"UAT-GAVIN-{tag}-{int(time.time())}"


def base() -> str:
    return env.ADMIN_URL + "/"


def to_dec(text: str | None) -> Decimal | None:
    if not text:
        return None
    m = re.search(r"([\d,]+(?:\.\d+)?)", text)
    return Decimal(m.group(1).replace(",", "")) if m else None


def read_amount(page: Page, label: str) -> Decimal | None:
    """The money value that follows a label such as 'Total Budget' on the statistics tab."""
    text = page.locator("main").inner_text()
    m = re.search(rf"{label}\D{{0,80}}?([\d,]+(?:\.\d+)?)", text, re.I)
    return Decimal(m.group(1).replace(",", "")) if m else None


def budget_cards(page: Page) -> dict[str, Decimal | None]:
    return {
        "total": read_amount(page, "Total budget"),
        "used": read_amount(page, "Used budget"),
        "remaining": read_amount(page, "Remaining budget"),
    }


def wait_statistics(page: Page, timeout: int = 30_000) -> None:
    page.wait_for_function(
        "() => /total budget/i.test(document.querySelector('main')?.innerText || '')", timeout=timeout)


def _open_statistics(page: Page, target: str, user: str, password: str) -> None:
    """Open a statistics tab by its address. The hosted portal can answer a full reload with the login page after a moment, so wait for either
    the statistics or the login page, sign in again when it is the login page, and reopen."""
    from pages import real_login
    for _ in range(3):
        page.goto(target, wait_until="domcontentloaded")
        try:
            page.wait_for_function(
                "() => /total budget/i.test(document.querySelector('main')?.innerText || '') || location.pathname.includes('/login')",
                timeout=25_000)
        except Exception:  # noqa: BLE001
            pass
        if "/login" in page.url:
            real_login.sign_in(page, env.ADMIN_URL, user, password)
            continue
        if re.search(r"total budget", page.locator("main").inner_text(), re.I):
            return
    wait_statistics(page)


def open_moe_statistics(page: Page, scheme_id: str) -> None:
    _open_statistics(page, f"{base()}moe-hq/moe-fas/{scheme_id}?tab=statistics", env.HQ_USER, env.HQ_PASS)


def open_sbfas_statistics(page: Page, scheme_id: str) -> None:
    _open_statistics(page, f"{base()}sbfas-schemes/{scheme_id}?tab=statistics", env.SCHOOL_USER, env.SCHOOL_PASS)


def sidebar(page: Page, name: str) -> None:
    """Open a screen from the left menu, the way a user does."""
    link = page.get_by_role("link", name=re.compile(rf"^{re.escape(name)}$", re.I)).first
    link.click()
    page.wait_for_load_state("domcontentloaded")


def list_moe_schemes(req) -> list[dict]:
    items, page_no = [], 1
    while True:
        resp = req.get(f"{base()}{real_api.MOE_SCHEMES}", params={"PageNumber": page_no, "PageSize": 100})
        if not resp.ok:
            return items
        body = resp.json()
        data = body.get("data") if isinstance(body, dict) and "data" in body else body
        items += data.get("items", [])
        if not (data.get("metadata") or {}).get("hasNextPage"):
            return [i for i in items if not i.get("isDeleted")]
        page_no += 1


def list_sbfas(req) -> list[dict]:
    items, page_no = [], 1
    while True:
        resp = req.get(f"{base()}{real_api.SBFAS_SCHEMES}?pageNumber={page_no}&pageSize=50")
        if not resp.ok:
            return items
        data = resp.json().get("data") or {}
        items += data.get("items", [])
        if not (data.get("metadata") or {}).get("hasNextPage"):
            return items
        page_no += 1


def exhausted_scheme(req, kind: str) -> tuple[dict | None, str]:
    """Look for a scheme whose used amount reached its total budget. Returns (scheme, what was looked at)."""
    schemes = list_moe_schemes(req) if kind == "moe" else list_sbfas(req)
    stat = real_api.get_moefas_statistics if kind == "moe" else real_api.get_sbfas_statistics
    looked = 0
    for s in schemes[:40]:
        sid = s.get("id")
        if not sid:
            continue
        status, data = stat(req, base(), sid)
        looked += 1
        b = (data or {}).get("budget") or {}
        if status == 200 and b.get("total") and b.get("used") is not None and b["used"] >= b["total"]:
            return {"id": sid, "name": s.get("name"), "budget": b}, f"{looked} schemes checked"
    return None, f"{looked} schemes checked, none has Used >= Total"


def scheme_id_from_response(info) -> str:
    """Id of the scheme from the POST response caught while pressing Draft or Publish."""
    try:
        body = info.value.json()
        data = body.get("data") if isinstance(body, dict) and "data" in body else body
        if isinstance(data, dict):
            return str(data.get("id") or "")
        return ""
    except Exception:  # noqa: BLE001
        return ""


def dump_screen(page: Page, tag: str) -> dict:
    """Read the controls of the open screen (headings, labelled fields, buttons, links) and save them in artifacts/probe_<tag>.json.
    Used for screens that are reviewed by hand until their controls are known, so that the next version of the suite can drive them."""
    import json
    info = page.evaluate("""() => {
      const t = e => (e.innerText || e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80);
      const label = e => { const l = e.id && document.querySelector(`label[for='${e.id}']`); return l ? t(l) : (e.getAttribute('aria-label') || e.placeholder || ''); };
      return {
        url: location.href,
        headings: [...document.querySelectorAll('main h1, main h2, main h3')].map(t),
        fields: [...document.querySelectorAll('main input, main select, main textarea')].map(e => ({tag: e.tagName, type: e.type, id: e.id, name: e.name,
                 label: label(e), required: e.required || e.getAttribute('aria-required') === 'true', value: e.type === 'password' ? '' : (e.value || '').slice(0, 40),
                 disabled: e.disabled, readonly: e.readOnly, options: e.tagName === 'SELECT' ? [...e.options].map(o => o.value).join('|') : undefined})),
        buttons: [...document.querySelectorAll('main button, main [role=button]')].map(t).filter(Boolean),
        links: [...document.querySelectorAll('main a')].map(t).filter(Boolean).slice(0, 30),
        text: t(document.querySelector('main') || document.body).slice(0, 80) && (document.querySelector('main')?.innerText || '').slice(0, 1500),
      };
    }""")
    out = env.ARTIFACTS / f"probe_{tag}.json"
    try:
        out.write_text(json.dumps(info, indent=1, ensure_ascii=False), encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    return info
