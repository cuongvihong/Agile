"""Fixtures of the UAT Master 01 suite.

  uat        one UatRun per test, named after the test function (test_UAT_PAR_01_N3 -> UAT-PAR-01-N3)
  discovery  scan of every Singpass test persona (children, age, citizenship, FAS applications),
             cached for the day in artifacts/discovery.json. Only built when a case asks for it.
"""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from core import config as C  # noqa: E402
from core.recorder import UatRun  # noqa: E402
from pages import auth, eservice  # noqa: E402


def _master() -> dict:
    try:
        return json.loads(C.MASTER_JSON.read_text(encoding="utf-8"))
    except Exception:
        return {}


MASTER = _master()


def pytest_addoption(parser):
    parser.addoption("--uat-case", action="store", default="", help="Comma separated case ids, * allowed (UAT-PAR-01*)")


def _case_id(nodename: str) -> str:
    name = re.sub(r"\[.*\]$", "", nodename)
    return name.replace("test_", "", 1).replace("_", "-")


def pytest_collection_modifyitems(session, config, items):
    wanted = [w.strip() for w in config.getoption("--uat-case").split(",") if w.strip()]
    if not wanted:
        return
    keep, drop = [], []
    for it in items:
        cid = _case_id(it.name)
        if any(re.fullmatch(w.replace("*", ".*"), cid) for w in wanted):
            keep.append(it)
        else:
            drop.append(it)
    if drop:
        config.hook.pytest_deselected(items=drop)
    items[:] = keep


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch(headless=not C.HEADED, slow_mo=C.SLOW_MO_MS)
        yield b
        b.close()


@pytest.fixture()
def uat(request, browser):
    cid = _case_id(request.node.name)
    run = UatRun(cid, browser, MASTER.get(cid, {"title": cid}))
    yield run
    # a test that crashed before conclude() still closes its windows and saves what it has
    if run.actors:
        try:
            run._close()
        except Exception:
            pass


# ---- persona discovery ------------------------------------------------------------------

def _age(dob_text: str) -> int | None:
    try:
        d = datetime.strptime(dob_text, "%b %d, %Y").date()
    except Exception:
        return None
    t = date.today()
    return t.year - d.year - ((t.month, t.day) < (d.month, d.day))


def _scan(browser) -> list[dict]:
    ctx = browser.new_context(viewport=C.VIEWPORT)
    page = ctx.new_page()
    page.set_default_timeout(20000)
    families = []
    try:
        auth.open_parent_login(page)
        personas = auth.persona_options(page)
        for label in personas:
            nric = label.split(" ")[0]
            fam = {"persona": nric, "label": label, "children": [], "applications": [], "error": ""}
            try:
                ctx.clear_cookies()
                auth.parent_login(page, nric)
                eservice.go_home(page)
                for c in eservice.home_cards(page):
                    page.goto(C.PARENT_URL + c["href"])
                    page.get_by_text("EA BALANCE").first.wait_for()
                    info = eservice.account_info(page)
                    fam["children"].append({**{k: c[k] for k in ("name", "href", "code", "status")},
                                            "balance": str(c["balance"]) if c["balance"] is not None else None,
                                            "dob": info["dob"], "age": _age(info["dob"]),
                                            "citizenship": info["citizenship"]})
                page.goto(C.PARENT_URL + "/fas-application")
                page.get_by_text("My FAS Applications").first.wait_for()
                page.wait_for_timeout(1500)
                fam["applications"] = eservice.my_fas_cards(page)
                auth.parent_logout(page)
            except Exception as e:
                fam["error"] = f"{type(e).__name__}: {str(e)[:200]}"
            families.append(fam)
    finally:
        ctx.close()
    return families


@pytest.fixture(scope="session")
def discovery(browser):
    if C.DISCOVERY_JSON.exists():
        try:
            cached = json.loads(C.DISCOVERY_JSON.read_text(encoding="utf-8"))
            if cached.get("date") == date.today().isoformat() and cached.get("eservice") == C.PARENT_URL:
                return cached["families"]
        except Exception:
            pass
    if not C.ALLOW_DISCOVERY:
        return []
    fams = _scan(browser)
    C.DISCOVERY_JSON.write_text(json.dumps({"date": date.today().isoformat(), "eservice": C.PARENT_URL,
                                                 "scanned_at": time.strftime("%H:%M:%S"), "families": fams},
                                                indent=2, ensure_ascii=False), encoding="utf-8")
    return fams


ACTIVE_APP = re.compile(r"PENDING|REVIEW|SUBMITTED|APPROVED|Under review|Pending|Approved", re.I)


def active_children(fam: dict) -> set[str]:
    """Children that already have an application that is not withdrawn or rejected."""
    names = set()
    for a in fam.get("applications", []):
        if ACTIVE_APP.search(a.get("status", "")) and not re.search(r"WITHDRAWN|REJECT|NOT_APPROVED|Not approved", a.get("status", ""), re.I):
            names.update(a.get("beneficiaries", []))
    return names
