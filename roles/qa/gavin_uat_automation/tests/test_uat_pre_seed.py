"""PRECONDITION cases. They run first in every UAT run and create the data the UAT cases need (top-up and fees of the seeded students).
Each case has its own video, banner and screenshots, so the way the data was created is evidence.

The data is created through the API of the Admin portal (the same calls the screens make) and read back on the screens:
Top-Up History, the campaign list, the fee batch list and the e-Service pay screen of the parent.
UAT_SEED=0 skips them, UAT_SEED=plan only reads (no data is created). Run alone:  run_uat.cmd seed
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import Page

from data import seed_plan as plan
from uat import env
from pages.billing_page import BillingPage
from uat.actors import sign_in_admin, sign_in_parent
from uat.seed import MODE, RUN_CAMPAIGN, Seeder, SeedError

pytestmark = pytest.mark.precondition


def _gate():
    if MODE == "0":
        pytest.skip("UAT_SEED=0: preconditions are skipped.")


def _search(page: Page, text: str) -> bool:
    """Type the text in the search box of the list (if there is one) and say whether the text is on the screen."""
    box = page.locator("input[type=search]:not([role=combobox]), input[placeholder*='earch' i]:not([role=combobox])").first
    try:
        if box.count():
            box.fill(text)
            box.press("Enter")
            page.wait_for_timeout(1500)
    except Exception:  # noqa: BLE001
        pass
    return text.lower() in _text(page).lower()


def _pick_first_school(page: Page) -> str:
    """The fee components page lists the components of ONE school: open the School selector and take the first option. Returns its text, or '' when there is no selector."""
    try:
        combo = page.get_by_role("combobox").first
        if not combo.count():
            return ""
        combo.click()
        page.wait_for_timeout(800)
        opt = page.get_by_role("option").first
        if not opt.count():
            page.keyboard.press("Escape")
            return ""
        label = " ".join(opt.inner_text().split())
        opt.click()
        page.wait_for_timeout(2000)
        return label
    except Exception:  # noqa: BLE001
        return ""


def _ready(page: Page) -> None:
    page.wait_for_load_state("domcontentloaded")
    page.locator("main, body").first.wait_for(timeout=30_000)
    page.wait_for_timeout(2000)


def _text(page: Page) -> str:
    return (page.locator("main").first.inner_text() if page.locator("main").count() else page.locator("body").inner_text())


def _money(v) -> str:
    return "n/a" if v is None else f"{float(v):.2f}"


@pytest.mark.case("UAT-PRE-01")
@pytest.mark.mutating
def test_uat_pre_01_topup_data(uat):
    _gate()
    page = uat.actor("moe")
    sign_in_admin(page, "moe")
    seeder = Seeder(uat.request("moe"))

    with uat.step("Sign in as MOE HQ and open Education Account Top-Up Management", "The screen has the tabs Individual Top-Up, Bulk Top-up and Top-Up History"):
        page.goto(env.ADMIN_URL + "/top-up?tab=individual")
        page.get_by_text("Education Account Top-Up Management").first.wait_for(timeout=30_000)
        uat.check("the three tabs are on the screen", all(t in _text(page) for t in ("Individual Top-Up", "Bulk Top-up", "Top-Up History")))

    accounts = {}
    with uat.step("Find the EA of each seeded student", "Each student is found with a wallet and a balance"):
        for t in plan.TOPUPS:
            s = plan.STUDENTS[t["key"]]
            try:
                box = page.get_by_label(re.compile("Search Account by", re.I)).or_(page.locator("input[type=text]").first)
                box.first.fill(s["nric"])
                page.get_by_role("button", name=re.compile(r"^Search$", re.I)).first.click()
                page.wait_for_timeout(1500)
            except Exception:  # noqa: BLE001
                uat.note(f"The search box of the screen was not driven for {s['name']}; the account was read through the API.")
            accounts[t["key"]] = seeder.account(t["key"])
            uat.check(f"{s['name']} ({s['nric']}) has a wallet", bool(accounts[t["key"]]["walletId"]),
                      f"wallet {accounts[t['key']]['walletCode']}, balance SGD {_money(accounts[t['key']]['balance'])}")
    if MODE == "plan":
        uat.note("UAT_SEED=plan: nothing is created.")
        uat.conclude()
        return

    results = {}
    with uat.step("Top up each EA with SGD 20 and read it back in Top-Up History", "Top-Up History shows each top-up as Success"):
        for t in plan.TOPUPS:
            r = seeder.ensure_topup(accounts[t["key"]], t["amount"])
            results[t["key"]] = r
            if r["created"]:
                uat.check(f"{plan.STUDENTS[t['key']]['name']}: balance grew by {t['amount']}",
                          r["after"] is not None and r["before"] is not None and abs(float(r["after"]) - float(r["before"]) - t["amount"]) < 0.005,
                          f"SGD {_money(r['before'])} to {_money(r['after'])}, reference {r['ref']}")
            else:
                uat.note(f"{plan.STUDENTS[t['key']]['name']}: this top-up was created in an earlier run ({r['ref']}); nothing was added.")
        for key in plan.RESTORE_EA:
            r = seeder.restore_ea(key, plan.EA_TARGET)
            if r is None:
                continue
            name = plan.STUDENTS[key]["name"]
            if r["created"]:
                uat.check(f"{name}: the EA is back to SGD {plan.EA_TARGET:.2f} for round {plan.ROUND}", abs(float(r["after"]) - plan.EA_TARGET) < 0.005,
                          f"SGD {r['before']:.2f} to {r['after']:.2f} in {r['parts']} top-up(s)")
            else:
                uat.note(f"{name}: the EA is SGD {r['before']:.2f}, no restore top-up was needed for round {plan.ROUND}.")
        for t in plan.TOPUPS:
            s_ = plan.STUDENTS[t["key"]]
            # The history has many rows after several rounds, so look the student up with the Search box (NRIC) instead of reading the first page.
            page.goto(env.ADMIN_URL + "/top-up?tab=history")
            _ready(page)
            try:
                box = page.get_by_label("Search", exact=True).first
                box.fill(s_["nric"])
                page.get_by_role("button", name=re.compile(r"^Search$", re.I)).first.click()
                page.wait_for_timeout(2500)
            except Exception:  # noqa: BLE001
                uat.note(f"The search box of Top-Up History was not driven for {s_['name']}; the first page was read.")
            text = _text(page)
            uat.check(f"Top-Up History shows {s_['name']} with ${t['amount']}.00", s_["name"] in text and f"${t['amount']}.00" in text)

    with uat.step("Create the bulk top-up campaign and read it back in the list", "The campaign is in the list as Active"):
        for c in plan.CAMPAIGNS:
            r = seeder.ensure_campaign(c)
            page.goto(env.ADMIN_URL + "/top-up?tab=campaigns")
            _ready(page)
            uat.check(f"campaign {c['name']} is in the list", _search(page, c["name"]),
                      ("created now" if r["created"] else "it existed already") + ("; executed" if r.get("executed") else "; not executed"))
    uat.conclude()


@pytest.mark.case("UAT-PRE-02")
@pytest.mark.mutating
def test_uat_pre_02_fee_data(uat):
    _gate()
    page = uat.actor("moe")
    sign_in_admin(page, "moe")
    seeder = Seeder(uat.request("moe"))

    with uat.step("Sign in as MOE HQ and open the fee components", "The list of fee components opens"):
        page.goto(env.ADMIN_URL + "/fee-management/components")
        _ready(page)
        uat.check("the fee type MISC exists", bool(seeder.fee_type_id()))
    if MODE == "plan":
        uat.note("UAT_SEED=plan: nothing is created.")
        uat.conclude()
        return

    comp = {}
    with uat.step("Create the fee components with their rates", "Each component exists with its price"):
        for c in plan.COMPONENTS:
            comp[c["name"]] = seeder.ensure_component(c)
            uat.check(f"component {c['name']} (SGD {c['price']:.2f}) exists", bool(comp[c["name"]]["id"]), "created now" if comp[c["name"]]["created"] else "it existed already")
        page.goto(env.ADMIN_URL + "/fee-management/components")
        _ready(page)
        school = _pick_first_school(page)
        for c in plan.COMPONENTS:
            shown = _search(page, c["name"])
            if shown:
                uat.check(f"the list shows {c['name']}", True)
            else:
                # The component exists on the server (checked above). The page lists one school at a time, so a component of another scope may not be in this school's list.
                uat.note(f"{c['name']} was not on the screen for school '{school or 'none chosen'}'. The server list holds it (see the checks above).")

    pubs = {}
    with uat.step("Publish a fee batch for the chosen students and wait until it is Completed", "Each batch is Completed and created one charge per chosen student"):
        for c in plan.COMPONENTS:
            r = seeder.ensure_publication(c, comp[c["name"]]["id"])
            pubs[c["name"]] = r
            uat.check(f"batch {r['title']} is Completed", str(r.get("status", "")).upper() == "COMPLETED",
                      f"created {r.get('charges')} charge(s), failed {r.get('failed')}, skipped {r.get('skipped')}" + ("" if r["created"] else "; it was published in an earlier run"))
        page.goto(env.ADMIN_URL + "/fee-batches")
        _ready(page)
        for c in plan.COMPONENTS:
            uat.check(f"the batch list shows {pubs[c['name']]['title']}", _search(page, pubs[c["name"]]["title"]))

    with uat.step("Sign in as the parent and see the charge to pay", "The pay screen of the child lists the charge with its name and amount"):
        parent = uat.actor("parent")
        first = plan.COMPONENTS[0]
        key = first["students"][0]
        s = plan.STUDENTS[key]
        sign_in_parent(parent, s["parent"])
        parent.goto(f"{env.PARENT_URL}/accounts/{s['code']}/pay")
        parent.get_by_text("Pay education charges").first.wait_for(timeout=30_000)
        parent.wait_for_timeout(2000)
        pay = BillingPage(parent, env.PARENT_URL)
        pay.wait_ready()
        listed = [c for c in pay.read_all_charges() if first["name"].lower() in c.description.lower()]  # the list has 10 charges a page
        seen = bool(listed)
        text = (listed[0].description + " " + str(listed[0].net)) if listed else ""
        if seen or pubs[first["name"]]["created"]:
            uat.check(f"{s['name']} sees {first['name']}", seen)
        else:
            # Published in an earlier run of this round, and a payment case may have paid it since: not a seed defect (step 3 shows the batch Completed).
            uat.note(f"{s['name']} no longer lists {first['name']}: the charge was published in an earlier run and has been paid or is held since.")
        if not seen:
            uat.conclude()
            return
        # The charge row shows the amount without the SGD prefix (the summary cards above it have the prefix), so look for the number on the row of the charge.
        uat.check(f"the amount is SGD {first['price']:.2f}", float(listed[0].net) == float(first["price"]), f"{listed[0].description}: {listed[0].net}")
    uat.conclude()


# ======================================================================= UAT-PRE-03
@pytest.mark.case("UAT-PRE-03")
@pytest.mark.mutating
def test_uat_pre_03_fas_data(uat):
    """FAS data for the UAT cases that need an application and an approved FAS (R6 budget, R10 parent application, R5 paper form).

    Why the real scheme: a second MOEFAS scheme cannot be created (the API refuses overlapping form or effective periods, and the real scheme
    covers 01/01/2026 to 11/30/2026 for the form and 12/01/2026 to 12/31/2027 for the effect). Why the approval waits: HQ can confirm allocations
    only from the scheme Effective from date. The application is created now, the approval is done by the first run on or after that date.
    """
    import datetime as dt

    from uat.seed import remember_fas, state

    _gate()
    f = plan.FAS
    kids = [plan.STUDENTS[k] for k in f["children"]]
    page = uat.actor("moe")
    sign_in_admin(page, "moe")
    hq = Seeder(uat.request("moe"))
    scheme: dict = {}

    with uat.step("Sign in as MOE HQ and open the MOEFAS scheme and its budget (R6)", "The scheme is listed with its form dates, effective dates and budget"):
        page.goto(env.ADMIN_URL + "/moe-hq/moe-fas")
        _ready(page)
        scheme = hq.moe_scheme() or {}
        uat.check("a real MOEFAS scheme exists", bool(scheme.get("id")))
        uat.check(f"the screen lists {scheme.get('name')}", str(scheme.get("name", "")) in _text(page))
        if not state().get("fas", {}).get("application"):  # the form has to be open only to submit; later runs only approve
            uat.check("the form of the scheme is open today (parents can apply)", bool(scheme.get("form_open")),
                      f"form {scheme.get('open_from')} to {scheme.get('open_to')}, status {scheme.get('status')}")
        uat.note(f"Budget of the scheme: total {_money(scheme.get('total'))}, used {_money(scheme.get('used'))}, remaining {_money(scheme.get('remaining'))}. "
                 f"Effective from {scheme.get('effective_from')} to {scheme.get('effective_to')}.")
    if not float(scheme.get("total") or 0) > 0:
        uat.blocked("The scheme has a budget that covers the approved applications",
                    "The total budget of the scheme is 0, so every confirm is skipped with INSUFFICIENT_BUDGET. Existing schemes are view only in the Admin portal: "
                    "the budget has to be set by Dev or BA (a new scheme is not possible while the periods overlap).", "Remaining budget is at least the amount of the allocations")
    if MODE == "plan":
        uat.note("UAT_SEED=plan: nothing is created.")
        uat.conclude()
        return

    parent = uat.actor("parent")
    sign_in_parent(parent, f["parent"])
    ps = Seeder(uat.request("parent"), base=env.PARENT_URL)
    app: dict = {}
    with uat.step("Sign in as the parent and apply for FAS for Ethan and Leo (R10)", "The application is submitted and listed with a reference"):
        parent.goto(env.PARENT_URL + "/fas-application")
        parent.get_by_text("My FAS Applications").first.wait_for(timeout=30_000)
        parent.wait_for_timeout(1500)
        app = ps.ensure_fas_application()
        if app.get("error"):
            uat.check("the application was accepted", False, f"HTTP {app.get('http')}: {app.get('message')}")
        else:
            uat.check("the application has a reference", bool(app.get("code")), f"{app.get('code')}" + (" (created now)" if app.get("created") else " (it existed already)"))
            if app.get("created"):
                uat.note(f"Matched {app.get('matched')}, GHI {_money(app.get('ghi'))}, PCI {_money(app.get('pci'))}. "
                         f"Allocations: {app.get('allocations')}")
            parent.goto(env.PARENT_URL + "/fas-application")
            parent.get_by_text("My FAS Applications").first.wait_for(timeout=30_000)
            parent.wait_for_timeout(2500)
            uat.check("My FAS Applications lists the new application", str(app.get("code")) in _text(parent), str(app.get("code")))

    ours: list = []
    with uat.step("MOE HQ sees the pending allocations of the new application", "One pending allocation per child is in the scheme"):
        if not app.get("code") or not scheme.get("id"):
            uat.check("the application and the scheme are known", False, "see the steps above")
        else:
            pend = hq.moe_pending(scheme["id"])
            ours = [i for i in pend["items"] if str(i.get("applicationCode")) == str(app["code"])]
            confirmed = state().get("fas", {}).get("confirmed")
            if confirmed and not ours:
                uat.note("The allocations were confirmed in an earlier run, so they are no longer pending.")
            else:
                uat.check(f"{len(kids)} pending allocations belong to {app['code']}", len(ours) == len(kids),
                          f"found {len(ours)}: {[(i.get('beneficiaryName'), i.get('allocatedAmount')) for i in ours]}")
            page.goto(env.ADMIN_URL + "/moe-hq/fas-applications")
            _ready(page)
            uat.check(f"the HQ application list shows {app['code']}", _search(page, str(app["code"])))

    approved = False
    title4, exp4 = "MOE HQ confirms the allocations (from the scheme Effective from date)", "The allocations are approved and the budget is used"
    eff = scheme.get("effective_from")
    today = dt.date.today()
    done_before = state().get("fas", {}).get("confirmed")
    why = None
    if not done_before:
        if not ours:
            why = "There are no pending allocations of this application to confirm."
        elif eff and today < eff:
            why = (f"The scheme is effective from {eff}. HQ can confirm only from that day (NOT_EFFECTIVE before). "
                   f"Run UAT-PRE-03 again on or after {eff}: the approval is done then, by this same step.")
    if why:
        uat.blocked(title4, why, exp4)
    else:
        with uat.step(title4, exp4):
            if done_before:
                approved = True
                uat.note(f"Confirmed in an earlier run: {done_before}")
            else:
                ids = [i["allocationId"] for i in ours]
                pre = hq.moe_confirm(scheme["id"], ids, preview_only=True)
                items = (pre["data"] or {}).get("items") or []
                uat.note(f"Preview: {[(i.get('allocationId'), i.get('predictedOutcome'), i.get('reason')) for i in items]}; fits budget {(pre['data'] or {}).get('fitsBudget')}")
                res = hq.moe_confirm(scheme["id"], ids)
                results = (res["data"] or {}).get("results") or []
                ok = [r for r in results if str(r.get("outcome", "")).upper() != "SKIPPED"]
                uat.check("the confirm answered", res["http"] in (200, 201), f"HTTP {res['http']}")
                uat.check(f"{len(ids)} allocations were approved", len(ok) == len(ids),
                          f"{[(r.get('allocationId'), r.get('outcome'), r.get('reason'), r.get('amount')) for r in results]}")
                approved = True
                remember_fas("confirmed", {"at": dt.datetime.now().isoformat(timespec="seconds"), "ids": ids})

    title5, exp5 = "Parent opens the application and sees the approved FAS", "The application shows Approved"
    if not approved:
        uat.blocked(title5, "The allocations are not approved yet (see the step above).", exp5)
    else:
        with uat.step(title5, exp5):
            parent.goto(env.PARENT_URL + "/fas-application")
            parent.get_by_text("My FAS Applications").first.wait_for(timeout=30_000)
            parent.wait_for_timeout(2500)
            parent.get_by_text(str(app.get("code"))).first.click()
            parent.wait_for_timeout(2500)
            uat.check("the application shows Approved", bool(re.search(r"approved", _text(parent), re.I)), " ".join(_text(parent).split())[:240])

    uat.blocked("School records a paper application (R5)",
                "Not automated. Every student with a free slot already has an application or an approved FAS, and the school paper form screen is not driven by this suite yet. "
                "Record one by hand in the school Admin screen Record a paper application for a child who has no application (sheet Don FAS of the data catalog).",
                "The paper application is stored in the same list")
    uat.conclude()


@pytest.mark.case("UAT-PRE-04")
@pytest.mark.mutating
def test_uat_pre_04_school_b_and_its_user(uat):
    _gate()
    page = uat.actor("moe")
    sign_in_admin(page, "moe")
    seeder = Seeder(uat.request("moe"))

    with uat.step("Sign in as MOE HQ and open School management", "School management lists the schools"):
        page.goto(env.ADMIN_URL + "/school-management")
        _ready(page)
        uat.check("School management is open", "chool" in _text(page), _text(page)[:120])
    if MODE == "plan":
        uat.note("UAT_SEED=plan: nothing is created.")
        uat.conclude()
        return

    with uat.step("Create School B (MOE school code, School name, School type)", "School B exists with its MOE school code"):
        sch = seeder.ensure_school(plan.SCHOOL_B)
        uat.check(f"School {plan.SCHOOL_B['moe_code']} ({plan.SCHOOL_B['name']}) exists", bool(sch.get("id")), "created now" if sch["created"] else "it existed already")
        page.goto(env.ADMIN_URL + "/school-management")
        _ready(page)
        if _search(page, plan.SCHOOL_B["moe_code"]):
            uat.check("the list shows School B", True)
        else:
            uat.note("School B exists on the server (checked above) but was not found by the search box of the list on screen.")

    with uat.step("Create the school user of School B (NRIC, First name, Last name, Email, MOE school code)", "The school user exists and belongs to School B"):
        usr = seeder.ensure_school_user(plan.SCHOOL_B_USER)
        uat.check(f"the school user {plan.SCHOOL_B_USER['email']} exists", bool(usr.get("id")), "created now" if usr["created"] else "it existed already")
        uat.note("The password of the school user is not recorded. Open the user detail in Admin, School Users to see how the user logs in.")
    uat.conclude()
