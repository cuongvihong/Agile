"""Parent FAS cases of UAT Master 01: UAT-PAR-02, N1, N2, E1, E2, A1, N3, A2, N4."""
from __future__ import annotations

import re

from conftest import active_children
from core import config
from core.util import norm, state_get
from fas_helpers import (SUBMITTED_MSG, find_pending_allocation, fill_form, keep_only, my_codes, open_application,
                         open_form, remember_app)
from pages import admin, auth, eservice

FAS = config.data("fas")


def _home_has_fa(page) -> bool:
    eservice.go_home(page)
    return bool(re.search(r"Financial assistance|Apply for FAS", eservice.main_text(page), re.I))


def test_UAT_PAR_02(uat):
    par = uat.actor("parent")
    ctx = {}

    @uat.step(1, "On Home go to Financial assistance and click Apply for FAS", "The application opens")
    def _(s):
        auth.parent_login(par, FAS["persona"])
        uat.map_data(f"Singapore Citizen parent with a 10 year old child -> persona {FAS['persona']}, child {FAS['child']}")
        if not _home_has_fa(par):
            s.same_function("Home has no Financial assistance block. FAS is reached through the user menu 'FAS Application' "
                            "then 'New Application'.")
        ctx["before"] = my_codes(par)
        open_form(par)
        s.check("/fas-application/new" in par.url, "the application form opens", par.url)

    @uat.step(2, "Step 1: choose the relationship and the child, click Continue", "Parent details are prefilled and read only", needs=(1,))
    def _(s):
        s.same_function("The build has one page form (Applicant, Beneficiary, Family member details), not a 5 step wizard with Continue.")
        for label in ("Full name *", "NRIC / FIN *", "Date of birth *"):
            st = eservice.readonly_state(par, label)
            s.check(st["value"] and st["readonly"], f"applicant '{label.rstrip(' *')}' is prefilled and read only", st)
        bens = keep_only(par, [FAS["child"]])
        s.require(bens == [FAS["child"]], f"only {FAS['child']} stays as beneficiary", bens)
        par.get_by_label("Relationship to beneficiary *").select_option(label=FAS["relationship"])

    @uat.step(3, "Step 2: check members and income, click Continue",
              "Income comes from Government data and GHI, household size and PCI are shown", needs=(1,))
    def _(s):
        txt = eservice.main_text(par)
        found = {k: bool(re.search(p, txt, re.I)) for k, p in
                 (("GHI", r"GHI|Gross Household Income"), ("PCI", r"PCI|Per Capita Income"), ("household size", r"household size|members count"))}
        if not all(found.values()):
            s.gap(f"The form does not show the income from Government data before submission: {found}. "
                  "GHI, PCI and the member count appear only on the application detail after submission.")
        s.check(par.get_by_text("Family member details").count() > 0, "the household members are listed")

    @uat.step(4, "Step 3: skip documents, keep the tick to also consider SBFAS, click Continue", "The step is passed", needs=(1,))
    def _(s):
        s.note("Client confirmed 30/10/2026: no 'also consider SBFAS' tick; a failed MOEFAS goes to the school SBFAS automatically.")
        s.check(par.get_by_text(re.compile(r"also consider SBFAS", re.I)).count() == 0, "no SBFAS tick (agreed 30/10/2026)")

    @uat.step(5, "Step 4: enter context (Household income reduced), click Continue", "The context is kept", needs=(1,))
    def _(s):
        ctx_field = par.locator("main textarea:not([readonly]):not([disabled])")
        if ctx_field.count() == 0:
            s.gap("The form has no field for the context of the application (only Employment status).")
        else:
            ctx_field.first.fill(FAS["context"])
            s.check(ctx_field.first.input_value() == FAS["context"], "the context is entered")

    @uat.step(6, "Step 5: review, tick the declaration, click Submit application",
              f"The message '{SUBMITTED_MSG}' appears", needs=(2,))
    def _(s):
        filled = fill_form(par, FAS["relationship"], FAS["phone"], FAS["email"])
        s.note(f"Filled: {filled}")
        s.check(filled.get("declaration"), "the declaration is ticked")
        txt = eservice.submit_application(par)
        errs = eservice.validation_messages(par)
        s.check(SUBMITTED_MSG.lower() in (txt + " " + admin.toast_text(par)).lower(), f"the message '{SUBMITTED_MSG}' appears",
                f"{txt[:200]} | messages {errs}")
        new = [c for c in my_codes(par) if c not in ctx["before"]]
        s.require(len(new) == 1, "one new application is listed", new)
        ctx["code"] = new[0]
        remember_app(new[0], "par02")

    @uat.step(7, "Open My applications", "Under review, System check Waiting and the form close date", needs=(6,))
    def _(s):
        card = next((c for c in eservice.my_fas_cards(par) if c["code"] == ctx["code"]), {"status": ""})
        s.check(re.search(r"under review", card["status"], re.I), "the status is Under review", card["status"])
        detail = open_application(par, ctx["code"])
        s.check(re.search(r"System check\W+Waiting", detail, re.I), "System check is Waiting", detail[:300])
        s.check(re.search(r"close|closing", detail, re.I) and re.search(r"\d{1,2}/\d{1,2}/\d{4}|\w{3} \d{1,2}, \d{4}", detail),
                "the form close date is shown", detail[:300])

    @uat.step(8, "Open it again after the MOEFAS form closes", "Approved MOEFAS from the scheme Effective from; the parent receives the result email")
    def _(s):
        s.blocked("The MOEFAS decision is made by a time driven job after the form close date. It cannot be triggered here; "
                  "rerun this step after the close date of the open MOEFAS scheme. The e-mail must be checked in the mailbox.")

    uat.conclude()


def test_UAT_PAR_02_N1(uat, discovery):
    par = uat.actor("parent")
    ctx = {}

    @uat.step(1, "Go to Financial assistance and click Apply for FAS", "The form opens")
    def _(s):
        fam = next((f for f in discovery if any((c.get("age") or 0) >= 16 for c in f["children"]) and active_children(f)), None) \
            or next((f for f in discovery if active_children(f)), None)
        if not fam:
            s.blocked("No persona has a child of 16 or a child with an application under review.")
        ctx["fam"] = fam
        ctx["locked"] = sorted(active_children(fam) | {c["name"] for c in fam["children"] if (c.get("age") or 0) >= 16})
        uat.map_data(f"student.test16 / student.test03 -> persona {fam['persona']}, children to be locked: {ctx['locked']}")
        auth.parent_login(par, fam["persona"])
        ctx["before"] = my_codes(par)
        ctx["bens"] = open_form(par)
        s.check("/fas-application/new" in par.url, "the form opens")

    @uat.step(2, "View the children list at step 1", "Each child is locked with the matching reason; Continue stays disabled", needs=(1,))
    def _(s):
        for name in ctx["locked"]:
            if name not in ctx["bens"]:
                s.check(True, f"{name} is not offered (cannot be selected)")
                continue
            sec = norm(eservice.beneficiary_section(par, name).inner_text())
            s.check(re.search(r"already|existing application|under review|16|not eligible|locked", sec, re.I),
                    f"{name} is locked with a reason", sec[:200])
        keep_only(par, [n for n in ctx["locked"] if n in ctx["bens"]])
        if not eservice.beneficiary_names(par):
            s.note("No locked child left on the form.")
            return
        btn = par.get_by_role("button", name="Submit application")
        if btn.is_disabled():
            s.check(True, "submission stays disabled while no child can be selected")
            return
        fill_form(par, FAS["relationship"], FAS["phone"], FAS["email"])
        txt = eservice.submit_application(par)
        new = [c for c in my_codes(par) if c not in ctx["before"]]
        s.check(not new, "no application is created for a locked child",
                f"new application(s) {new}; screen: {txt[:200]}; messages {eservice.validation_messages(par)}")

    uat.conclude()


def test_UAT_PAR_02_N2(uat):
    hq = uat.actor("moe")

    @uat.step(1, "Open Financial assistance (no MOEFAS or SBFAS form is open today)", "The page opens")
    def _(s):
        auth.admin_login(hq, "hq")
        admin.moefas_list(hq)
        open_now = [n for n, st in admin.moefas_scheme_names_with_status(hq) if st == "Application open"]
        if open_now:
            s.blocked(f"A MOEFAS form is open today ({open_now}). The case needs a date outside every form period; "
                      "rerun it when no form is open.")

    @uat.step(2, "Click Apply for FAS if it is still enabled", "Apply for FAS is disabled with a note; children locked with the next form date", needs=(1,))
    def _(s):
        par = uat.actor("parent")
        auth.parent_login(par, FAS["persona"])
        eservice.open_my_fas(par)
        btn = par.get_by_role("button", name="New Application")
        s.check(btn.is_disabled(), "Apply for FAS (New Application) is disabled", f"enabled={not btn.is_disabled()}")
        s.check(re.search(r"closed|next form|not open", eservice.main_text(par), re.I), "a note says the form is closed",
                eservice.main_text(par)[:200])

    uat.conclude()


def test_UAT_PAR_02_E1(uat):
    par = uat.actor("parent")

    @uat.step(1, "Go to step 4 and enter context", "The context is entered")
    def _(s):
        auth.parent_login(par, FAS["persona"])
        open_form(par)
        area = par.locator("main textarea:not([readonly]):not([disabled])")
        if area.count() == 0:
            s.gap("The form has no field for the context.")
        else:
            area.first.fill(FAS["context"])

    @uat.step(2, "Click Save draft and exit", "The message 'Draft saved. You can continue later.' appears")
    def _(s):
        b = par.get_by_role("button", name=re.compile(r"Save draft", re.I))
        if b.count() == 0:
            buttons = [norm(t) for t in par.locator("main button").all_inner_texts()]
            s.gap(f"The form has no Save draft and exit button. Buttons: {buttons}", stop=True)
        b.first.click()
        par.wait_for_timeout(1500)
        s.check("Draft saved. You can continue later." in eservice.main_text(par) + admin.toast_text(par), "the draft message appears")

    @uat.step(3, "Open Financial assistance again", "The Draft card shows status Draft and the saved step")
    def _(s):
        eservice.open_my_fas(par)
        cards = eservice.my_fas_cards(par)
        if not any(re.search(r"draft", c["status"], re.I) for c in cards):
            s.gap(f"My FAS Applications shows no Draft card. Statuses: {[c['status'] for c in cards]}")

    @uat.step(4, "Click Resume draft", "Step 4 opens with the context kept")
    def _(s):
        if par.get_by_role("button", name=re.compile(r"Resume draft", re.I)).count() == 0:
            s.gap("There is no Resume draft button.")

    uat.conclude()


def test_UAT_PAR_02_E2(uat, discovery):
    par = uat.actor("parent")
    ctx = {}

    @uat.step(1, "Choose both children at step 1", "Both children are selected")
    def _(s):
        for fam in discovery:
            free = [c["name"] for c in fam["children"] if c["name"] not in active_children(fam)
                    and 7 <= (c.get("age") or 0) < 16 and re.search(r"Citizen", c.get("citizenship", ""), re.I)]
            if len(free) >= 2 and fam["persona"] != FAS["persona"]:
                ctx["fam"], ctx["kids"] = fam, free[:2]
                break
        if not ctx:
            s.blocked("No persona has two Singapore Citizen children aged 7 to 15 without an application.")
        uat.map_data(f"student.test01 + student.test04 -> persona {ctx['fam']['persona']}, {ctx['kids']}")
        auth.parent_login(par, ctx["fam"]["persona"])
        ctx["before"] = my_codes(par)
        open_form(par)
        bens = keep_only(par, ctx["kids"])
        s.check(sorted(bens) == sorted(ctx["kids"]), "both children are on the application", bens)

    @uat.step(2, "Go through every step and click Submit application", "The message 'Applications submitted' appears", needs=(1,))
    def _(s):
        fill_form(par, FAS["relationship"], FAS["phone"], FAS["email"])
        txt = eservice.submit_application(par)
        s.check("Applications submitted" in txt + admin.toast_text(par), "the message 'Applications submitted' appears", txt[:200])
        ctx["new"] = [c for c in my_codes(par) if c not in ctx["before"]]
        for c in ctx["new"]:
            remember_app(c, "par02e2")
        s.require(ctx["new"], "the submission is listed", ctx["new"])

    @uat.step(3, "Open My applications", "Two separate Application IDs sharing one family code FAM-YYYY-NNNNN", needs=(2,))
    def _(s):
        s.check(len(ctx["new"]) == 2, "two separate applications (one per child)", ctx["new"])
        fam_codes = set()
        for c in ctx["new"]:
            fam_codes.update(re.findall(r"FAM-\d{4}-\d{5}", open_application(par, c)))
        s.check(len(fam_codes) == 1, "the applications share one family code FAM-YYYY-NNNNN", sorted(fam_codes))

    uat.conclude()


def test_UAT_PAR_02_A1(uat):
    @uat.step(1, "Submit the application as in UAT-PAR-02 with household income 8000 per month", "Submitted")
    def _(s):
        s.blocked("Household income comes from the Government API mock; it cannot be set to 8000 for a parent from the UI.")

    @uat.step(2, "After the MOEFAS form closes, open My applications", "SBFAS Pending with the school; timeline shows Sent to school")
    def _(s):
        s.blocked("The MOEFAS decision is a time driven job after the form close date.")

    @uat.step(3, "School Admin approves the Pending SBFAS application", "Approved SBFAS Tier 1 from Effective from", needs=(2,))
    def _(s):
        pass

    @uat.step(4, "Parent opens My applications again", "Approved SBFAS Tier 1; the parent receives an e-mail", needs=(3,))
    def _(s):
        pass

    uat.conclude()


def test_UAT_PAR_02_N3(uat):
    par = uat.actor("parent")

    @uat.step(1, "Submit the application and clear the SBFAS tick at step 3", "The tick can be cleared")
    def _(s):
        auth.parent_login(par, FAS["persona"])
        open_form(par)
        has_tick = par.get_by_text(re.compile(r"also consider SBFAS", re.I)).count() > 0
        s.note(f"SBFAS tick on the form: {has_tick}")
        s.blocked("Client confirmed 30/10/2026 that the form has no 'also consider SBFAS' tick: a failed MOEFAS always goes "
                  "to the school SBFAS. The precondition of this case no longer exists; BA should retire or rewrite it.")

    @uat.step(2, "After the MOEFAS form closes, open My applications", "Rejected with reason Not eligible for MOEFAS; e-mail")
    def _(s):
        s.blocked("Time driven MOEFAS decision; household income 8000 cannot be set.")

    uat.conclude()


def _pr_child(discovery, skip: set) -> tuple[dict, str] | None:
    for fam in discovery:
        for c in fam["children"]:
            if re.search(r"Permanent|\bPR\b", c.get("citizenship", ""), re.I) and c["name"] not in active_children(fam) \
                    and c["name"] not in skip:
                return fam, c["name"]
    return None


def _submit_pr(uat, s, par, discovery, kind: str, skip: set) -> dict:
    hit = _pr_child(discovery, skip)
    if not hit:
        s.blocked("No Singapore PR child without an application exists under the Singpass test personas "
                  f"({len(discovery)} scanned). student.pr01 must be seeded.")
    fam, child = hit
    uat.map_data(f"student.pr01 -> {child} of persona {fam['persona']}")
    auth.parent_login(par, fam["persona"])
    before = my_codes(par)
    open_form(par)
    keep_only(par, [child])
    fill_form(par, FAS["relationship"], FAS["phone"], FAS["email"])
    txt = eservice.submit_application(par)
    new = [c for c in my_codes(par) if c not in before]
    s.require(new, "the application is submitted", txt[:200])
    remember_app(new[0], kind)
    return {"fam": fam, "child": child, "code": new[0]}


def test_UAT_PAR_02_A2(uat, discovery):
    par = uat.actor("parent")
    ctx = {}

    @uat.step(1, "Submit the application for the child (Singapore PR)", "The application is submitted")
    def _(s):
        ctx.update(_submit_pr(uat, s, par, discovery, "pr", set()))

    @uat.step(2, "Open My applications", "SBFAS Pending as soon as it is submitted; timeline shows Sent to school (SBFAS)", needs=(1,))
    def _(s):
        card = next((c for c in eservice.my_fas_cards(par) if c["code"] == ctx["code"]), {})
        s.check(re.search(r"SBFAS|school", card.get("status", ""), re.I), "the status is SBFAS Pending", card)
        detail = open_application(par, ctx["code"])
        s.check(re.search(r"Sent to school", detail, re.I), "the timeline shows Sent to school (SBFAS)", detail[:300])

    @uat.step(3, "School Admin approves the application", "The school approves the application and chooses the tier", needs=(1,))
    def _(s):
        sch = uat.actor("school")
        auth.admin_login(sch, "school")
        hit = find_pending_allocation(sch, [ctx["code"]])
        if not hit:
            s.check(False, "the school sees the application as a pending SBFAS allocation", f"{ctx['code']} not found in any SBFAS scheme")
            return
        admin.select_allocation(sch, hit[1])
        txt = admin.approve_selected(sch)
        s.check(re.search(r"approved|confirmed|success", txt, re.I), "the approval is confirmed", txt[:300])
        if not re.search(r"tier", txt, re.I):
            s.gap("The approval does not let the school choose the tier (it confirms the allocation of the scheme).")

    uat.conclude()


def test_UAT_PAR_02_N4(uat, discovery):
    par = uat.actor("parent")
    ctx = {}

    @uat.step(1, "School Admin chooses Reject with a Reason (Not eligible nationality) and a Comment", "The application is rejected")
    def _(s):
        ctx.update(_submit_pr(uat, s, par, discovery, "pr_reject", set(state_get("created_apps_pr", []) or [])))
        sch = uat.actor("school")
        auth.admin_login(sch, "school")
        hit = find_pending_allocation(sch, [ctx["code"]])
        s.require(hit, "the PR application is a pending SBFAS allocation of the school", ctx["code"])
        admin.select_allocation(sch, hit[1])
        dlg = admin.open_reject_dialog(sch)
        if dlg.locator("select").count() == 0:
            s.gap("The reject dialog has no Reason list (only Remarks).")
        else:
            opts = [o.strip() for o in dlg.locator("select option").all_inner_texts()]
            pick = next((o for o in opts if "national" in o.lower()), opts[1] if len(opts) > 1 else None)
            if pick:
                dlg.locator("select").first.select_option(label=pick)
        dlg.locator("textarea").first.fill("Not eligible nationality - UAT master 01")
        dlg.get_by_role("button", name=re.compile(r"reject", re.I)).last.click()
        admin.settle(sch, 2000)

    @uat.step(2, "Parent opens My applications", "Rejected; the timeline shows the reason and the comment; e-mail", needs=(1,))
    def _(s):
        uat.actor("parent")
        detail = open_application(par, ctx["code"])
        s.check(re.search(r"reject|not approved", detail, re.I), "the application is Rejected", detail[:200])
        s.check("Not eligible nationality" in detail, "the reason and the comment are shown", detail[:400])

    uat.conclude()
