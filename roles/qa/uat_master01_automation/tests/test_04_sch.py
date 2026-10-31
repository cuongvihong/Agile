"""School cases of UAT Master 01: UAT-SCH-01, 01-N1, 01-E1, 02, 02-N1, 03, 03-N1, 04, 04-E1."""
from __future__ import annotations

import re
from decimal import Decimal

from core import config
from core.util import norm, state_get, state_set
from fas_helpers import find_pending_allocation
from pages import admin, auth

SCH = config.data("school")
SB = config.data("sbfas")


# ---- paper application ------------------------------------------------------------------

def _paper_lookup(uat, s, page) -> bool:
    """Opens 'Record a paper application' and looks up the parent. True when the form loads."""
    err = admin.paper_find_parent(page, SCH["parent_nric"])
    uat.map_data(f"Applicant S0000100A / child S0000001A -> parent {SCH['parent_nric']} / child {SCH['child_nric']} of the school")
    if err:
        api = [e for e in uat.actors["school"]["api_errors"] if "prefill" in e or "parent" in e]
        s.check(False, "the parent and child details load", f"dialog says: {err[:220]}; API: {api[-2:]}")
        return False
    return True


def test_UAT_SCH_01(uat):
    sch = uat.actor("school")
    ctx = {}

    @uat.step(1, "Open Upload applications, click Upload scans, add the PDF, click Upload and read", "The scan is uploaded and read")
    def _(s):
        auth.admin_login(sch, "school")
        nav = sch.get_by_role("link", name=re.compile(r"Upload applications", re.I))
        if nav.count() == 0:
            s.same_function("No 'Upload applications' menu. The school menu has 'Record a paper application'.")
        admin.goto(sch, "/fas-applications/physical/new")
        files = sch.locator("input[type=file]")
        if files.count() == 0 and sch.get_by_text(re.compile(r"Upload scans", re.I)).count() == 0:
            s.gap("The paper application screen has no Upload scans / file upload, so the PDF cannot be uploaded and read.")
        elif files.count():
            files.first.set_input_files(str(config.ROOT / SCH["paper_file"]))
            s.check(True, "the PDF scan is attached", SCH["paper_file"])

    @uat.step(2, "Enter the applicant's NRIC and the child's NRIC", "Applicant and child details are prefilled and locked; income from Government data, GHI and PCI shown")
    def _(s):
        ok = _paper_lookup(uat, s, sch)
        if not ok:
            return
        txt = admin.main_text(sch)
        s.check(re.search(r"GHI|Gross household income", txt, re.I) and re.search(r"PCI|Per capita", txt, re.I),
                "GHI and PCI from Government data are shown", txt[:300])
        ro = sch.locator("main input[readonly], main input:disabled")
        s.check(ro.count() > 0, "applicant and child details are locked", f"{ro.count()} locked field(s)")
        ctx["ok"] = True

    @uat.step(3, "Choose the relationship, declare other members, enter context, tick the declaration", "The form accepts the entry", needs=(2,))
    def _(s):
        rel = sch.get_by_label(re.compile(r"Relationship", re.I))
        if rel.count():
            rel.first.select_option(label=SCH["relationship"])
        phone = sch.get_by_label(re.compile(r"Phone", re.I))
        if phone.count():
            phone.first.fill(SCH["phone"])
        area = sch.locator("main textarea:not([readonly]):not([disabled])")
        if area.count():
            area.first.fill(SCH["context"])
        else:
            s.gap("No field for the context.")
        decl = sch.get_by_label(re.compile(r"declar", re.I))
        s.check(decl.count() > 0, "a declaration tick is offered")
        if decl.count():
            decl.first.check()

    @uat.step(4, "Click Review and submit", "The Review before submitting screen opens", needs=(3,))
    def _(s):
        b = sch.get_by_role("button", name=re.compile(r"Review and submit", re.I))
        if b.count() == 0:
            s.same_function("No 'Review and submit' button; the form is submitted directly.")
            return
        b.first.click()
        admin.settle(sch, 1500)
        s.check(re.search(r"Review before submitting", admin.main_text(sch), re.I), "the Review before submitting screen opens")

    @uat.step(5, "Check the Review screen, then click Confirm and submit", "The message 'Application submitted for assessment' appears", needs=(3,))
    def _(s):
        b = sch.get_by_role("button", name=re.compile(r"Confirm and submit|Submit", re.I))
        s.require(b.count() > 0, "a submit button is offered")
        b.last.click()
        admin.settle(sch, 2500)
        txt = admin.main_text(sch) + " " + admin.toast_text(sch)
        s.check("Application submitted for assessment" in txt, "the message 'Application submitted for assessment' appears", txt[:200])

    @uat.step(6, "Open the Upload applications list", "One application per child, source Paper, status Pending; the draft is removed", needs=(5,))
    def _(s):
        admin.school_fas_applications(sch)
        rows = admin.table_rows(sch)
        s.check(any(re.search(r"Paper", r, re.I) and re.search(r"Pending", r, re.I) for r in rows),
                "a row with source Paper and status Pending is listed", rows[:3])

    uat.conclude()


def test_UAT_SCH_01_N1(uat):
    sch = uat.actor("school")

    @uat.step(1, "Open a paper application on the Review application screen", "The form is open")
    def _(s):
        auth.admin_login(sch, "school")
        if admin.paper_find_parent(sch, SCH["parent_nric"]):
            s.blocked("Blocked by UAT-SCH-01: the parent lookup of 'Record a paper application' fails, so no paper application can be opened.")

    rules = [
        (2, "Leave Phone number empty and click Review and submit", "phone"),
        (3, f"Enter a child outside the 7 to 16 age range ({SCH['child_over_age_nric']}) and click Review and submit", "age"),
        (4, "Enter a child who already has an application this year and click Review and submit", "dup"),
        (5, "Enter the same NRIC for applicant and child and click Review and submit", "same"),
    ]
    for n, title, kind in rules:
        @uat.step(n, title, "A red note at the top states what to fix; no application is created", needs=(1,))
        def _(s, kind=kind):
            child_field = sch.get_by_label(re.compile(r"Child.*NRIC|Beneficiary.*NRIC", re.I))
            if kind in ("age", "dup", "same") and child_field.count() == 0:
                s.gap("The paper form loads the children from the parent lookup; a child NRIC cannot be entered.")
                return
            if kind == "phone":
                sch.get_by_label(re.compile(r"Phone", re.I)).first.fill("")
            elif kind == "age":
                child_field.first.fill(SCH["child_over_age_nric"])
            elif kind == "dup":
                child_field.first.fill(SCH["child_nric"])
            else:
                child_field.first.fill(SCH["parent_nric"])
            sch.get_by_role("button", name=re.compile(r"Review and submit|Submit", re.I)).first.click()
            admin.settle(sch, 1500)
            top = norm(" ".join(sch.locator("[role=alert]").all_inner_texts()))
            s.check(top, "a note states what to fix", top[:200])
            s.check("submitted" not in admin.main_text(sch).lower(), "no application is created")

    uat.conclude()


def test_UAT_SCH_01_E1(uat):
    sch = uat.actor("school")

    @uat.step(1, "Click Save draft", "The draft is saved")
    def _(s):
        auth.admin_login(sch, "school")
        if admin.paper_find_parent(sch, SCH["parent_nric"]):
            s.blocked("Blocked by UAT-SCH-01: the parent lookup fails, so no paper application can be partly entered.")
        b = sch.get_by_role("button", name=re.compile(r"Save draft", re.I))
        if b.count() == 0:
            s.gap("The paper application form has no Save draft button.", stop=True)
        b.first.click()
        admin.settle(sch, 1500)

    @uat.step(2, "Return to the Upload applications list", "A Draft row with Application ID 'Not submitted'", needs=(1,))
    def _(s):
        admin.school_fas_applications(sch)
        rows = admin.table_rows(sch)
        s.check(any("Draft" in r and "Not submitted" in r for r in rows), "the list shows a Draft row 'Not submitted'", rows[:3])

    @uat.step(3, "Click Continue on the Draft row", "The entered data is reopened", needs=(2,))
    def _(s):
        sch.locator("main tbody tr", has_text="Draft").get_by_role("button", name=re.compile("Continue")).first.click()
        admin.settle(sch, 1500)
        s.check(SCH["parent_nric"][-4:] in admin.main_text(sch), "the draft reopens with the applicant")

    uat.conclude()


# ---- SBFAS schemes ------------------------------------------------------------------------

def _create_sbfas(sch, name: str, publish: bool = True) -> tuple[str, str]:
    admin.sbfas_new(sch)
    admin.sbfas_general(sch, name, SB["open_from"], SB["open_to"], SB["effective_from"], SB["effective_to"], SB["budget"])
    admin.click_button(sch, "Next")
    admin.sbfas_eligibility(sch, SB["ghi_to"], SB["pci_to"])
    admin.click_button(sch, "Next")
    comp = admin.sbfas_pick_component(sch)
    admin.sbfas_rates(sch, SB["rates"])
    admin.click_button(sch, "Review")
    review = admin.main_text(sch)
    admin.click_button(sch, "Publish" if publish else "Save draft")
    return comp, review + " || " + admin.main_text(sch) + " " + admin.toast_text(sch)


def test_UAT_SCH_02(uat):
    sch = uat.actor("school")
    name = f"{SB['name']} UAT-{config.RUN_TAG}"
    ctx = {}

    @uat.step(1, "Open SBFAS schemes and create a new scheme named Tier 1", "The wizard opens")
    def _(s):
        auth.admin_login(sch, "school")
        admin.sbfas_list(sch)
        sch.get_by_role("button", name="New scheme").click()
        sch.locator("#sbfas-name").wait_for()
        uat.map_data(f"Name 'Tier 1' -> '{name}' (unique per run)")
        s.check(all(w in admin.main_text(sch) for w in ("General", "Eligibility", "Subsidy", "Review")), "the wizard steps are shown")

    @uat.step(2, "Enter the form period and the effective period", "The General step is accepted", needs=(1,))
    def _(s):
        admin.sbfas_general(sch, name, SB["open_from"], SB["open_to"], SB["effective_from"], SB["effective_to"], SB["budget"])
        uat.map_data(f"Periods not in master -> form {SB['open_from']}..{SB['open_to']}, effective {SB['effective_from']}..{SB['effective_to']}")
        admin.click_button(sch, "Next")
        s.check(sch.locator("#sbfas-nationality-SC").count() == 1, "the Eligibility step opens")

    @uat.step(3, "Choose nationality and GHI, PCI bands", "Eligibility accepted", needs=(2,))
    def _(s):
        admin.sbfas_eligibility(sch, SB["ghi_to"], SB["pci_to"])
        admin.click_button(sch, "Next")
        s.check("Subsidy percentages" in admin.main_text(sch), "the Subsidy step opens")

    @uat.step(4, "Enter the subsidy rate for each level (P1 100%, P2 80%, P3 60%)", "Rates accepted", needs=(3,))
    def _(s):
        ctx["component"] = admin.sbfas_pick_component(sch)
        labels = admin.sbfas_rates(sch, SB["rates"])
        uat.map_data(f"Fee component of Tier 1: {ctx['component']}; grades {labels}")
        admin.click_button(sch, "Review")
        rev = admin.main_text(sch)
        s.check(all(f"{r}%" in rev for r in SB["rates"]), "the Review shows 100%, 80% and 60%", rev[-300:])
        if SB["effective_to"] and SB["effective_to"] not in rev:
            s.check(False, "the Review keeps the Effective to that was entered", rev[:300])

    @uat.step(5, "Review and Publish", "Tier 1 is published and becomes read only", needs=(4,))
    def _(s):
        admin.click_button(sch, "Publish")
        admin.sbfas_list(sch, name)
        row = next((r for r in admin.sbfas_rows(sch) if name in r), "")
        s.require(row, "the scheme is in the list", admin.toast_text(sch))
        s.check(re.search(r"Published|Upcoming|Application open|Active", row), "the scheme is published", row)
        acts = admin.sbfas_actions(sch, name)
        ctx["acts"] = acts
        s.check(not any(a in ("Edit", "Publish", "Delete") for a in acts), "the published scheme is read only", acts)
        state_set("sch02_scheme", name)

    @uat.step(6, "When the scheme is Active, click Add fee, choose the new component, enter a value, click Add to scheme",
              "Add fee only on Active or Upcoming schemes; new column added, old columns read only; subsidy applies to open fees of granted students",
              needs=(5,))
    def _(s):
        s.check("Add fee" in ctx["acts"], "Add fee is offered on the Upcoming or Active scheme", ctx["acts"])
        draft = f"UAT-M01-DRAFT-{config.RUN_TAG}"
        _create_sbfas(sch, draft, publish=False)
        admin.sbfas_list(sch, draft)
        d_acts = admin.sbfas_actions(sch, draft) if any(draft in r for r in admin.sbfas_rows(sch)) else []
        s.check(d_acts and "Add fee" not in d_acts, "Add fee is not offered on a Draft scheme", d_acts)
        if "Delete" in d_acts:
            sch.get_by_role("button", name=f"Actions — {draft}").click()
            sch.get_by_role("menuitem", name="Delete").click()
            dl = admin.dialog(sch)
            if dl.count():
                dl.get_by_role("button", name=re.compile(r"Delete|Confirm", re.I)).last.click()
            admin.settle(sch)
        admin.open_sbfas_scheme(sch, name)
        sch.get_by_role("button", name="Add fee component").click()
        dlg = admin.dialog(sch)
        opts = [o.strip() for o in dlg.locator("select option").all_inner_texts() if o.strip() and o.strip() != "Choose a fee"]
        new_comp = next((o for o in opts if o != ctx["component"]), None)
        s.require(new_comp, "a component that is not yet in the scheme is offered", opts[:5])
        uat.map_data(f"New fee component 'Activity fee' -> '{new_comp}'")
        dlg.locator("select").first.select_option(label=new_comp)
        for i in range(dlg.locator("input[type=number]").count()):
            dlg.locator("input[type=number]").nth(i).fill("50")
        dlg.get_by_role("button", name="Add fee", exact=True).click()
        admin.settle(sch, 2000)
        detail = admin.main_text(sch)
        s.check(new_comp in detail, "the new column is added to the subsidy table", detail[-400:])
        s.check(sch.locator("main input[type=number]:not([disabled])").count() == 0, "the old columns are read only")
        s.note("Expected 4 (subsidy applied to open fees of students already granted) needs a student granted this new scheme: "
               "not possible right after publishing. Check it on a scheme with grants.")

    uat.conclude()


def test_UAT_SCH_02_N1(uat):
    sch = uat.actor("school")
    ctx = {}

    @uat.step(1, "Create another scheme also named Tier 1 with an application period overlapping the old Tier 1", "The wizard takes the data")
    def _(s):
        auth.admin_login(sch, "school")
        base = state_get("sch02_scheme")
        admin.sbfas_list(sch, base or "")
        if not base or not any(base in r for r in admin.sbfas_rows(sch)):
            base = f"{SB['name']} UAT-{config.RUN_TAG}-N1"
            _create_sbfas(sch, base, publish=True)
            s.note(f"UAT-SCH-02 did not run in this session: published '{base}' first as the existing Tier 1.")
        ctx["base"] = base
        uat.map_data(f"Tier 1 -> '{base}' (same name, same period)")
        s.check(True, "the existing Tier 1 is published", base)

    @uat.step(2, "Click Publish", "Reports an overlap with an existing scheme and cannot be published", needs=(1,))
    def _(s):
        _, txt = _create_sbfas(sch, ctx["base"], publish=True)
        s.check(re.search(r"overlap", txt, re.I), "the message reports an overlap with an existing scheme", txt[-250:])
        admin.sbfas_list(sch, ctx["base"])
        same = [r for r in admin.sbfas_rows(sch) if ctx["base"] in r]
        s.check(len(same) == 1, "the second scheme is not published", f"{len(same)} scheme(s) named {ctx['base']}")

    @uat.step(3, "Rename it to Tier 2 and Publish again", "The second attempt with a different name can be published", needs=(1,))
    def _(s):
        tier2 = ctx["base"].replace(SB["name"], "Tier 2", 1)
        _, txt = _create_sbfas(sch, tier2, publish=True)
        admin.sbfas_list(sch, tier2)
        s.check(any(tier2 in r for r in admin.sbfas_rows(sch)), "Tier 2 is published", txt[-200:])

    uat.conclude()


def _approval_target(uat, s, sch) -> tuple[str, str]:
    codes = state_get("created_apps", []) or []
    hit = find_pending_allocation(sch, codes)
    if not hit:
        s.blocked("No pending SBFAS allocation of an application created by this run exists "
                  f"(apps of this run: {codes}). A decision cannot be undone, so the suite does not touch other testers' "
                  "applications (UAT_ALLOW_FOREIGN_APPS=1 allows it). A Pending SBFAS application comes from a PR child "
                  "(UAT-PAR-02-A2) or from the MOEFAS decision job.")
    uat.map_data(f"Pending SBFAS application -> {hit[1]} on scheme {hit[0]}")
    return hit


def test_UAT_SCH_03(uat):
    sch = uat.actor("school")

    @uat.step(1, "Open FAS applications, Pending tab", "Pending applications are listed")
    def _(s):
        auth.admin_login(sch, "school")
        admin.school_fas_applications(sch)
        if sch.get_by_role("tab", name=re.compile("Pending")).count() == 0:
            opts = " ".join(sch.locator("main select").first.locator("option").all_inner_texts())
            if "Pending School Review" in opts:
                s.same_function("No Pending tab; the Status filter has 'Pending School Review'.")
            else:
                s.gap("No Pending tab and no Pending filter.")

    @uat.step(2, "Click Review on the application", "A review drawer opens")
    def _(s):
        if sch.get_by_role("button", name=re.compile(r"^Review$")).count() == 0:
            s.gap("The FAS applications list has no Review button or drawer; 'View details' opens a read only page "
                  "and approval is on the SBFAS scheme tab 'Pending allocations'.")

    @uat.step(3, "Check income, context and the ML recommendation in the drawer",
              "Income, context and the ML recommended tier (preselected) are shown")
    def _(s):
        rows = sch.locator("main tbody tr")
        if rows.count() == 0:
            s.blocked("No application in the school list to open.")
        rows.first.get_by_role("button", name=re.compile("View details")).click()
        admin.settle(sch, 1500)
        txt = admin.main_text(sch)
        s.check(re.search(r"Gross Household Income|GHI", txt) and re.search(r"Per Capita Income|PCI", txt), "income is shown", txt[:200])
        if not re.search(r"recommend", txt, re.I):
            s.gap("No ML recommendation (recommended tier) is shown.")
        if not re.search(r"context", txt, re.I):
            s.gap("The context of the application is not shown.")

    @uat.step(4, "Choose a tier, enter Comment 'Eligible', click Confirm approval",
              "Approved with the tier and the scheme Effective from; 'Subsidy applied to the student's EA fees'; e-mail; read only")
    def _(s):
        scheme, code = _approval_target(uat, s, sch)
        admin.open_sbfas_scheme(sch, scheme)
        admin.click_tab(sch, r"Pending allocations")
        admin.select_allocation(sch, code)
        txt = admin.approve_selected(sch)
        s.check(re.search(r"approved|confirmed|success", txt, re.I), "the application is approved", txt[:300])
        s.check("Subsidy applied to the student's EA fees" in txt, "the message 'Subsidy applied to the student's EA fees' appears", txt[:300])
        if not re.search(r"tier", txt, re.I):
            s.gap("No tier choice and no Comment on approval.")
        admin.click_tab(sch, r"Pending allocations")
        s.check(not any(code in r for r in admin.pending_allocation_rows(sch)), "the application is no longer pending (read only)")
        s.note("The parent e-mail must be checked in the mailbox.")

    uat.conclude()


def test_UAT_SCH_03_N1(uat):
    sch = uat.actor("school")
    ctx = {}

    @uat.step(1, "Open the application in FAS applications", "The application opens")
    def _(s):
        auth.admin_login(sch, "school")
        ctx["scheme"], ctx["code"] = _approval_target(uat, s, sch)
        admin.open_sbfas_scheme(sch, ctx["scheme"])
        admin.click_tab(sch, r"Pending allocations")
        s.require(admin.select_allocation(sch, ctx["code"]), "the pending application is selected")

    @uat.step(2, "Click Reject", "The reject form opens", needs=(1,))
    def _(s):
        ctx["dlg"] = admin.open_reject_dialog(sch)
        s.check(ctx["dlg"].is_visible(), "the reject dialog opens")

    @uat.step(3, "Choose a Reason (Income above limit) and enter a Comment",
              "The Reject application button stays disabled until both Reason and Comment are filled", needs=(2,))
    def _(s):
        dlg = ctx["dlg"]
        btn = dlg.get_by_role("button", name=re.compile(r"reject", re.I)).last
        s.check(btn.is_disabled(), "the reject button is disabled while nothing is filled")
        if dlg.locator("select").count() == 0:
            s.gap("No Reason list in the reject dialog (Remarks only).")
        else:
            opts = [o.strip() for o in dlg.locator("select option").all_inner_texts()]
            pick = next((o for o in opts if "income" in o.lower()), opts[-1])
            dlg.locator("select").first.select_option(label=pick)
            s.check(btn.is_disabled(), "the reject button stays disabled with only the Reason")
        dlg.locator("textarea").first.fill("Income above the Tier 1 limit")
        s.check(btn.is_enabled(), "the reject button is enabled when filled")

    @uat.step(4, "Click Reject application",
              "Rejected; 'Application rejected. Parent notified by email'; the parent receives an e-mail with the reason", needs=(3,))
    def _(s):
        ctx["dlg"].get_by_role("button", name=re.compile(r"reject", re.I)).last.click()
        admin.settle(sch, 2000)
        txt = admin.main_text(sch) + " " + admin.toast_text(sch)
        s.check("Application rejected. Parent notified by email" in txt, "the message 'Application rejected. Parent notified by email' appears", txt[:300])
        s.check(not any(ctx["code"] in r for r in admin.pending_allocation_rows(sch)), "the application is no longer pending")

    uat.conclude()


def test_UAT_SCH_04(uat):
    sch = uat.actor("school")
    name = f"UAT-M01-SCH04-{config.RUN_TAG}"

    @uat.step(1, "Open the SBFAS Manage Budget screen", "The budget screen opens")
    def _(s):
        auth.admin_login(sch, "school")
        admin.sbfas_list(sch)
        if not re.search(r"Manage Budget", admin.main_text(sch), re.I):
            s.same_function("No SBFAS Manage Budget screen; the budget is 'Total budget' in the General step of the SBFAS scheme wizard.")
        admin.sbfas_new(sch)
        s.check(sch.locator("#sbfas-budget").count() == 1, "the Total budget field is offered")

    @uat.step(2, "Enter the Budget Amount 50000.00 and click Save", "The budget is saved and tied to the user's school", needs=(1,))
    def _(s):
        _, txt = _create_sbfas(sch, name, publish=False)
        admin.sbfas_list(sch, name)
        s.require(any(name in r for r in admin.sbfas_rows(sch)), "the scheme with the budget is saved in the school list", txt[-200:])

    @uat.step(3, "Open the Budget Tracking page", "Budget Amount, Subsidy Amount Used and Remaining Budget of the school; no other school's data", needs=(2,))
    def _(s):
        admin.open_sbfas_scheme(sch, name)
        admin.click_tab(sch, r"Budget and statistics")
        s.same_function("No separate Budget Tracking page; it is the tab 'Budget and statistics' of the scheme.")
        n = admin.budget_numbers(admin.main_text(sch))
        s.check(n["total"] == Decimal("50000.00"), "the saved Budget Amount is 50,000.00", n)
        if None not in n.values():
            s.check(n["remaining"] == n["total"] - n["used"], "Remaining Budget = Budget Amount - Subsidy Amount Used", n)
        hq = uat.actor("moe")
        auth.admin_login(hq, "hq")
        others = [x for x in admin.school_names(hq) if x and "Rosyth" not in x]
        uat.actor("school")
        txt = admin.main_text(sch)
        leaked = [x for x in others if x in txt]
        s.check(not leaked, "no data of another school appears", leaked)

    uat.conclude()


def test_UAT_SCH_04_E1(uat):
    sch = uat.actor("school")

    @uat.step(1, "Open the Budget Tracking page (Subsidy Amount Used >= Budget Amount)", "A budget exhausted warning is shown")
    def _(s):
        auth.admin_login(sch, "school")
        admin.sbfas_list(sch)
        names = [m.group(1).strip() for r in admin.sbfas_rows(sch) for m in [re.match(r"(.+?)\s+SBF-\d+", r)] if m]
        hit = None
        for nm in names:
            admin.open_sbfas_scheme(sch, nm)
            admin.click_tab(sch, r"Budget and statistics")
            n = admin.budget_numbers(admin.main_text(sch))
            if n["total"] is not None and n["used"] is not None and n["total"] > 0 and n["used"] >= n["total"]:
                hit = nm
                break
        if not hit:
            s.blocked(f"No SBFAS scheme of the school has Subsidy Amount Used >= Budget Amount ({len(names)} checked). "
                      "Used grows only with approved grants.")
        uat.map_data(f"Exhausted SBFAS scheme -> {hit}")
        txt = admin.main_text(sch)
        s.check(re.search(r"exhaust|insufficient|over budget|no remaining", txt, re.I), "a budget exhausted warning is shown", txt[:300])

    @uat.step(2, "Approve one more SBFAS application", "The application is still approved and the grant is not blocked", needs=(1,))
    def _(s):
        scheme, code = _approval_target(uat, s, sch)
        admin.open_sbfas_scheme(sch, scheme)
        admin.click_tab(sch, r"Pending allocations")
        admin.select_allocation(sch, code)
        txt = admin.approve_selected(sch)
        s.check(re.search(r"approved|confirmed|success", txt, re.I) and not re.search(r"insufficient|exceed", txt, re.I),
                "the grant goes through", txt[:300])

    uat.conclude()
