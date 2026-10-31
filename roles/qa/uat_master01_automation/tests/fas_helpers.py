"""Shared steps of the FAS cases (online application by the parent, school decision)."""
from __future__ import annotations

import re

from core import config
from core.util import state_append
from pages import admin, eservice

SUBMITTED_MSG = "Application submitted for assessment"


def open_form(page) -> list[str]:
    eservice.open_my_fas(page)
    eservice.open_new_application(page)
    return eservice.beneficiary_names(page)


def keep_only(page, keep: list[str]) -> list[str]:
    for name in list(eservice.beneficiary_names(page)):
        if name not in keep:
            eservice.remove_beneficiary(page, name)
    return eservice.beneficiary_names(page)


def fill_form(page, relationship: str, phone: str, email: str) -> dict:
    """Fill the fields the parent must type; returns what was filled."""
    done = {}
    rel = page.get_by_label("Relationship to beneficiary *")
    if rel.count():
        rel.first.select_option(label=relationship)
        done["relationship"] = relationship
    for label, value in (("Phone number *", phone), ("Email address *", email)):
        loc = page.get_by_label(label)
        if loc.count() and not loc.first.evaluate("e => e.readOnly || e.disabled"):
            loc.first.fill(value)
            done[label] = value
    done["selects"] = eservice.fill_empty_required_selects(page)
    for i in range(page.locator("main input[type=radio]").count()):
        r = page.locator("main input[type=radio]").nth(i)
        name = r.get_attribute("name") or ""
        if name and not r.is_disabled() and page.locator(f'main input[type=radio][name="{name}"]:checked').count() == 0:
            r.check()
    decl = page.get_by_label(re.compile(r"I agree to the declaration"))
    if decl.count():
        decl.first.check()
        done["declaration"] = True
    return done


def my_codes(page) -> list[str]:
    page.goto(config.PARENT_URL + "/fas-application")
    page.get_by_text("My FAS Applications").first.wait_for()
    page.wait_for_timeout(1500)
    return [c["code"] for c in eservice.my_fas_cards(page)]


def open_application(page, code: str) -> str:
    page.goto(config.PARENT_URL + "/fas-application")
    page.get_by_text(code).first.wait_for()
    page.get_by_text(code, exact=True).first.click()
    page.get_by_text(f"Application: {code}").first.wait_for(timeout=20000)
    page.wait_for_timeout(1000)
    return eservice.main_text(page)


def remember_app(code: str, kind: str) -> None:
    state_append("created_apps", code)
    state_append(f"created_apps_{kind}", code)


# ---- school side: find and decide pending allocations of applications created by this run ----

def find_pending_allocation(sch, codes: list[str]) -> tuple[str, str] | None:
    """(scheme name, app code) of a pending allocation of the school. Only codes of this run unless allowed."""
    admin.sbfas_list(sch)
    names = []
    for r in admin.sbfas_rows(sch):
        m = re.match(r"(.+?)\s+SBF-\d+", r)
        if m:
            names.append(m.group(1).strip())
    for nm in names:
        try:
            admin.open_sbfas_scheme(sch, nm)
            admin.click_tab(sch, r"Pending allocations")
        except Exception:
            continue
        for row in admin.pending_allocation_rows(sch):
            m = re.search(r"APP-[A-Z0-9-]+", row)
            if not m:
                continue
            if m.group(0) in codes or (config.ALLOW_FOREIGN_APPS and not codes):
                return nm, m.group(0)
    return None
