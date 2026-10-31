"""EA activity cases of UAT Master 01: UAT-PAR-03, A1, E1."""
from __future__ import annotations

import re

from core import config
from core.util import norm
from pages import auth, eservice

ACT = config.data("activity")


def test_UAT_PAR_03(uat):
    par = uat.actor("parent")
    child = ACT["child"]
    ctx = {}

    @uat.step(1, "Log in with SingPass", "Home opens")
    def _(s):
        auth.parent_login(par, ACT["persona"])
        uat.map_data(f"Parent with two children with top-ups and payments -> persona {ACT['persona']}; student.test01 / EA-001 -> {child}")
        eservice.go_home(par)
        ctx["card"] = eservice.card_of(par, child)
        s.require(ctx["card"], f"Home shows {child}")
        s.check(len(eservice.home_cards(par)) >= 2, "the parent has two children", len(eservice.home_cards(par)))

    @uat.step(2, "On Home choose the card of one child", "Edu Account Detail of the child", needs=(1,))
    def _(s):
        eservice.open_account(par, child)
        ctx["detail_url"] = par.url
        s.check(child in eservice.main_text(par), "the detail of the child opens", par.url)

    @uat.step(3, "On Edu Account Detail choose to view EA balance activity",
              "Child name and EA code; only this child's wallet entries; top-up as Money in; Description without internal reason; "
              "Back returns to the child", needs=(2,))
    def _(s):
        links = [norm(t) for t in par.locator("main a").all_inner_texts()] + \
                [a for a in par.locator("main a").evaluate_all("els => els.map(e => e.getAttribute('aria-label') || '')")]
        if not any(re.search(r"balance activity|EA activity|transactions", l, re.I) for l in links):
            s.gap("No 'EA balance activity' view. The detail offers 'View invoices and payments' (payments only) and "
                  "'View Top-Up' (top-ups only): no single wallet list.")
        eservice.open_topup_history(par, child)
        txt = eservice.main_text(par)
        s.check(child in txt, "the top-up list shows the child name", txt[:200])
        code = ctx["card"]["code"]
        s.check(code in txt, f"the list shows the EA code {code}", re.findall(r"\b[A-Z]{2,3}-\d{4,}\b", txt)[:4])
        rows = [norm(r) for r in par.locator("main tbody tr").all_inner_texts()]
        s.check(rows and all(child in r for r in rows), "only this child's entries are listed", rows[:3])
        if rows and not any(re.search(r"Money in", r, re.I) for r in rows) and "Money in" not in txt:
            s.gap("Top-ups are not labelled 'Money in'.")
        heads = [norm(h) for h in par.locator("main thead th").all_inner_texts()]
        idx = next((i for i, h in enumerate(heads) if re.search(r"Description|Note", h, re.I)), None)
        if idx is not None:
            notes = [norm(r.locator("td").nth(idx).inner_text()) for r in par.locator("main tbody tr").all()]
            internal = [n for n in notes if re.search(r"UAT|restore|round|internal|seed|test|probe|reason", n, re.I)]
            s.check(not internal, "the Description holds no internal reason", internal[:3] or notes[:3])
        keys = re.findall(r"\b[a-z]+\.[a-z][A-Za-z]+\b", txt[:150])
        s.check(not keys, "the breadcrumb and title show readable text (no untranslated key)", keys or norm(txt[:80]))
        par.get_by_role("button", name="Back").first.click()
        par.wait_for_timeout(1500)
        s.check(par.url.rstrip("/") == ctx["detail_url"].rstrip("/"), "Back returns to the Edu Account Detail of the child", par.url)

    uat.conclude()


def test_UAT_PAR_03_A1(uat):
    par = uat.actor("parent")

    @uat.step(1, "On Home click Recent EA activity of your children", "A list of the recent activity of all children")
    def _(s):
        auth.parent_login(par, ACT["persona"])
        eservice.go_home(par)
        if not re.search(r"Recent EA activity", eservice.main_text(par), re.I):
            s.gap("Home has no 'Recent EA activity of your children'. The closest block is 'Invoices & payments' (payments only).")
        par.get_by_role("link", name=re.compile(r"Recent EA activity|View invoices & payments", re.I)).first.click()
        par.wait_for_timeout(2000)
        s.check(par.locator("main tbody tr").count() > 0, "rows of all children are listed")

    @uat.step(2, "Look at the rows", "Each row has the child name and EA code; a note states the scope is the loaded data", needs=(1,))
    def _(s):
        rows = [norm(r) for r in par.locator("main tbody tr").all_inner_texts() if r.strip()]
        s.check(rows and all(re.search(r"EDU-\d+", r) for r in rows), "each row has the EA code", rows[:3])
        s.check(re.search(r"loaded", eservice.main_text(par), re.I), "a note states the scope is the loaded data")

    @uat.step(3, "Choose the name of one child", "That child's page opens", needs=(1,))
    def _(s):
        link = par.locator("main tbody tr a").first
        s.require(link.count(), "the child name is a link")
        name = norm(link.inner_text())
        link.click()
        par.wait_for_timeout(2000)
        s.check(name in eservice.main_text(par) and re.search(r"/accounts/", par.url), f"the page of {name} opens", par.url)

    uat.conclude()


def test_UAT_PAR_03_E1(uat):
    par = uat.actor("parent")

    @uat.step(1, "Look at the main menu on Home", "No separate Fees and Payments item")
    def _(s):
        auth.parent_login(par, ACT["persona"])
        par.get_by_role("button", name="Open user options").click()
        items = [norm(t) for t in par.locator("header a, header button, [role=menu] a").all_inner_texts() if t.strip()]
        par.keyboard.press("Escape")
        s.check(not any(re.fullmatch(r"Fees (and|&) Payments", i, re.I) for i in items), "no Fees and Payments item", items)

    @uat.step(2, "Open Edu Account Detail and look at the options", "No Invoices and payments item until a list source exists")
    def _(s):
        eservice.go_home(par)
        eservice.open_account(par, ACT["child"])
        has = par.get_by_role("link", name=re.compile(r"invoices and payments", re.I)).count() > 0
        if has:
            eservice.open_invoices(par, ACT["child"])
            rows = eservice.invoice_rows(par)
            s.check(len(rows) > 0, "the Invoices and payments item has its list source (invoices are listed)", f"{len(rows)} row(s)")
            s.note("Future branch of the master: the list source now exists, so showing the item is consistent with the rule.")
        else:
            s.check(True, "no Invoices and payments item")

    uat.conclude()
