"""MOE HQ cases of UAT Master 01: UAT-MOE-01, 04, 05, 05-E1, 06, 06-N1."""
from __future__ import annotations

import re
from datetime import date

from core import config
from core.util import money, norm, state_set
from pages import admin, auth, eservice


def _shift(iso: str, years: int) -> str:
    d = date.fromisoformat(iso)
    return d.replace(year=d.year + years).isoformat()


def test_UAT_MOE_01(uat):
    hq = uat.actor("moe")

    @uat.step(1, "Run the daily sync job (Government API mock has a citizen who has just turned 7)",
              "An Active EA is created for the student with balance 0.00")
    def _(s):
        s.blocked("The daily sync job is a server side scheduled job. Neither portal has a control to start it. "
                  "The tech team must run it and give the NRIC of the new seven year old.")

    @uat.step(2, "Log in to the Admin Portal as MOE HQ User, create a School and a School User",
              "The school and the school user are created")
    def _(s):
        auth.admin_login(hq, "hq")
        admin.goto(hq, "/school-management", "School management")
        s.check(hq.get_by_role("button", name=re.compile("Create school")).count() > 0 or
                hq.get_by_text("Create school").count() > 0, "the Create school control is on School management")
        admin.goto(hq, "/school-user-management")
        s.check("School" in admin.main_text(hq), "the School Users screen opens", admin.main_text(hq)[:120])
        s.blocked("Master data 'School Test 01' has no MOE school code, school type, user name or e-mail, "
                  "so the creation forms cannot be filled with master values.")

    @uat.step(3, "Log in as the School User, create class P1A, enter student.test01 and assign the student",
              "The student is linked to the EA after class assignment")
    def _(s):
        sch = uat.actor("school")
        auth.admin_login(sch, "school")
        admin.goto(sch, "/class-management")
        s.check(re.search(r"Class", admin.main_text(sch)), "the Classes screen opens")
        admin.goto(sch, "/student-management")
        s.check(re.search(r"Student", admin.main_text(sch)), "the Students screen opens")
        s.blocked("student.test01 comes from the daily sync job of step 1, which cannot run here.")

    @uat.step(4, "Log in as MOE HQ User, create a Fee Publication for that school and publish it (Tuition fee 100.00)",
              "Student Charge is POSTED", page=hq)
    def _(s):
        uat.actor("moe")
        admin.goto(hq, "/fee-batches", "Fee publication batches")
        rows = admin.table_rows(hq)
        s.check(len(rows) > 0, "the Fee publication batches list opens with batches", f"{len(rows)} row(s)")
        s.blocked("The fee publication must target School Test 01 and student.test01, which do not exist (steps 1 to 3).")

    @uat.step(5, "Open the student's Student Charge as the parent",
              "Student Charge is POSTED and visible to the parent")
    def _(s):
        par = uat.actor("parent")
        persona, child = config.data("pay", "persona"), config.data("pay", "child")
        uat.map_data(f"student.test01 -> {child} (persona {persona}), the EA used by the payment cases")
        auth.parent_login(par, persona)
        eservice.open_account(par, child)
        eservice.open_pay(par, child)
        charges = eservice.all_charges(par)
        s.check(len(charges) > 0, "the parent sees the charges of the child", f"{len(charges)} charge(s)")
        statuses = sorted({c["status"] for c in charges})
        s.note(f"Status labels shown to the parent: {statuses}")
        s.blocked("The charge of master student.test01 (Tuition fee 100.00 from step 4) cannot exist. "
                  "Visibility of published charges to the parent was checked on the mapped child.")

    uat.conclude()


def test_UAT_MOE_04(uat):
    hq = uat.actor("moe")
    mf = config.data("moefas")
    name = f"UAT-M01-MOE04-{config.RUN_TAG}"

    @uat.step(1, "Open the MOEFAS Manage Budget screen", "A screen to manage the MOEFAS budget opens")
    def _(s):
        auth.admin_login(hq, "hq")
        admin.moefas_list(hq)
        txt = admin.main_text(hq)
        has_manage = re.search(r"Manage Budget", txt, re.I) or hq.get_by_role("link", name=re.compile("budget", re.I)).count()
        if not has_manage:
            s.same_function("No Manage Budget screen. The budget is the field 'Total budget (S$)' of the General step "
                            "of the MOEFAS scheme wizard (New scheme).")
        admin.moefas_new(hq)
        s.check(hq.locator("#moefas-create-total-budget").count() == 1, "the Total budget field is offered")

    @uat.step(2, "Enter the Budget Amount 1000000.00", "The amount is accepted", needs=(1,))
    def _(s):
        y = 100 * (int(config.RUN_TAG[-3:]) % 30 + 30)  # far future period, never collides with real schemes
        admin.moefas_general(hq, name, _shift(mf["form_opens"], y), _shift(mf["form_closes"], y),
                             _shift(mf["effective_from"], y), "1000000.00")
        s.check(hq.locator("#moefas-create-total-budget").input_value() in ("1000000.00", "1000000"),
                "the Total budget field holds 1000000.00", hq.locator("#moefas-create-total-budget").input_value())
        uat.map_data(f"Scheme for the budget: {name}, dates moved {y} years ahead (a draft that does not touch real periods)")

    @uat.step(3, "Click Save", "The budget is saved", needs=(2,))
    def _(s):
        admin.click_button(hq, "Draft")
        txt = admin.main_text(hq) + " " + admin.toast_text(hq)
        if "Complete all required fields" in txt and "/new" in hq.url:
            # the draft needs the other steps too: fill them with the MOE-06 master values
            admin.wizard_next(hq)
            admin.moefas_eligibility(hq, "Singapore Citizen", mf["ghi_to"], mf["pci_to"])
            admin.wizard_next(hq)
            comp = admin.moefas_pick_fee_component(hq)
            admin.moefas_rates(hq, comp, mf["rates"])
            admin.click_button(hq, "Draft")
            txt = admin.main_text(hq) + " " + admin.toast_text(hq)
        s.check(re.search(r"drafted|saved", txt, re.I) or "/new" not in hq.url, "the save is confirmed", txt[:200])

    @uat.step(4, "Reopen the budget view", "The view shows the saved Budget Amount within MOEFAS scope", needs=(3,))
    def _(s):
        admin.open_moefas_scheme(hq, name)
        nums = admin.budget_numbers(admin.main_text(hq))
        s.check(nums["total"] == money("S$ 1000000.00"), "the saved Total budget is 1,000,000.00", nums)
        s.check(re.search(r"MOE", admin.main_text(hq)), "the view is the MOEFAS scheme of MOE HQ")

    uat.conclude()


def _active_moefas(hq) -> str | None:
    admin.moefas_list(hq)
    for nm, st in admin.moefas_scheme_names_with_status(hq):
        if st in ("Application open", "Effective", "Application closed"):
            return nm
    return None


def test_UAT_MOE_05(uat):
    hq = uat.actor("moe")
    scheme = {}

    @uat.step(1, "Open the MOEFAS Subsidy Statistics page", "The statistics of the MOEFAS scheme open")
    def _(s):
        auth.admin_login(hq, "hq")
        nm = _active_moefas(hq)
        if not nm:
            s.blocked("No MOEFAS scheme is open or effective, so no subsidy has been granted (setup 2 of the master).")
        scheme["name"] = nm
        uat.map_data(f"MOEFAS scheme with grants: {nm}")
        admin.open_moefas_scheme(hq, nm)
        admin.click_tab(hq, r"Budget KPIs")
        s.same_function("The statistics are the tab 'Budget KPIs & Statistics' of the scheme, not a separate page.")
        s.check("Used Budget" in admin.main_text(hq) or "Used budget" in admin.main_text(hq), "the statistics show Used Budget")

    @uat.step(2, "Check Total Subsidy Amount Granted", "Total granted subsidy is correct for MOEFAS scope", needs=(1,))
    def _(s):
        stats = admin.budget_numbers(admin.main_text(hq))
        admin.click_tab(hq, r"Scheme Details")
        details = admin.budget_numbers(admin.main_text(hq))
        s.check(stats["used"] is not None, "the statistics show the granted amount (Used Budget)", stats)
        s.check(stats["used"] == details["used"], "the granted amount is the same on the statistics and on the scheme details",
                f"statistics {stats['used']}, details {details['used']}")
        if not re.search(r"Total Subsidy Amount Granted", admin.main_text(hq), re.I):
            s.same_function("The label is 'Used Budget', not 'Total Subsidy Amount Granted'.")

    @uat.step(3, "Open the Budget Tracking page",
              "Shows Budget Amount and Subsidy Amount Used; Remaining = Budget Amount - Subsidy Amount Used", needs=(1,))
    def _(s):
        admin.click_tab(hq, r"Budget KPIs")
        n = admin.budget_numbers(admin.main_text(hq))
        s.same_function("No separate Budget Tracking page. Budget tracking is the same 'Budget KPIs & Statistics' tab.")
        s.check(n["total"] is not None and n["used"] is not None, "Budget Amount and Subsidy Amount Used are shown", n)
        if n["total"] is not None and n["used"] is not None and n["remaining"] is not None:
            s.check(n["remaining"] == n["total"] - n["used"], "Remaining Budget = Budget Amount - Subsidy Amount Used", n)

    uat.conclude()


def test_UAT_MOE_05_E1(uat):
    hq = uat.actor("moe")

    @uat.step(1, "Open the Budget Tracking page (Subsidy Amount Used >= Budget Amount)", "The page shows a budget exhausted warning")
    def _(s):
        auth.admin_login(hq, "hq")
        admin.moefas_list(hq)
        found = None
        for nm, st in admin.moefas_scheme_names_with_status(hq):
            if st == "Draft":
                continue
            admin.open_moefas_scheme(hq, nm)
            admin.click_tab(hq, r"Budget KPIs")
            n = admin.budget_numbers(admin.main_text(hq))
            if n["total"] is not None and n["used"] is not None and n["used"] >= n["total"]:
                found = (nm, n)
                break
        if not found:
            s.blocked("No MOEFAS scheme has Subsidy Amount Used >= Budget Amount. Used grows only when the allocation "
                      "job grants subsidies, which cannot be triggered from the UI.")
        uat.map_data(f"Exhausted scheme: {found[0]}")
        txt = admin.main_text(hq)
        s.check(re.search(r"exhaust|insufficient|over budget|budget (is )?(used up|depleted)|no remaining", txt, re.I),
                "a budget exhausted warning is shown", txt[:300])

    @uat.step(2, "Let the system grant one more MOEFAS subsidy", "The extra grant still goes through and is not blocked")
    def _(s):
        s.blocked("A MOEFAS grant is made by the time driven allocation job after the form closes. It cannot be triggered here.")

    uat.conclude()


def _publish_moefas(hq, s, mf, name, years):
    admin.moefas_new(hq)
    admin.moefas_general(hq, name, _shift(mf["form_opens"], years), _shift(mf["form_closes"], years),
                         _shift(mf["effective_from"], years), mf["budget"])
    admin.wizard_next(hq)
    admin.moefas_eligibility(hq, "Singapore Citizen", mf["ghi_to"], mf["pci_to"])
    admin.wizard_next(hq)
    comp = admin.moefas_pick_fee_component(hq)
    admin.moefas_rates(hq, comp, mf["rates"])
    admin.wizard_next(hq)
    review = admin.review_text(hq)
    admin.click_button(hq, "Publish")
    return comp, review, admin.main_text(hq) + " " + admin.toast_text(hq)


def test_UAT_MOE_06(uat):
    hq = uat.actor("moe")
    mf = config.data("moefas")
    ctx = {"name": f"{mf['name']} UAT-{config.RUN_TAG}"}

    @uat.step(1, "Open MOEFAS schemes and create a new scheme", "The wizard opens")
    def _(s):
        auth.admin_login(hq, "hq")
        admin.moefas_list(hq)
        hq.get_by_role("link", name="New scheme").click()
        hq.locator("#moefas-create-name").wait_for()
        txt = admin.main_text(hq)
        s.check(all(w in txt.upper() for w in ("GENERAL", "ELIGIBILITY", "SUBSIDY", "REVIEW")),
                "the wizard has General, Eligibility, Subsidy, Review")

    @uat.step(2, "General step: enter name, Form opens, Form closes, Effective from",
              "1 Aug 2028 to 31 Dec 2028, Effective from 1 Jan 2029 accepted", needs=(1,))
    def _(s):
        admin.moefas_general(hq, ctx["name"], mf["form_opens"], mf["form_closes"], mf["effective_from"], mf["budget"])
        uat.map_data(f"Name 'MOEFAS 2028' -> '{ctx['name']}' (unique per run). Budget not in master -> {mf['budget']}")
        admin.wizard_next(hq)
        s.check("Eligibility" in admin.main_text(hq) and hq.locator("#moefas-create-ghi-to").count() == 1,
                "the General step is accepted and Eligibility opens", admin.main_text(hq)[:200])

    @uat.step(3, "Eligibility step: choose nationality Singapore Citizen and GHI, PCI bands", "Eligibility accepted", needs=(2,))
    def _(s):
        admin.moefas_eligibility(hq, "Singapore Citizen", mf["ghi_to"], mf["pci_to"])
        uat.map_data(f"GHI and PCI bands not in master -> GHI <= {mf['ghi_to']}, PCI <= {mf['pci_to']}")
        admin.wizard_next(hq)
        s.check("Subsidy per level" in admin.main_text(hq), "the Subsidy step opens")

    @uat.step(4, "Subsidy step: Primary 100%, Secondary 70%, Pre-University 50%", "Rates accepted", needs=(3,))
    def _(s):
        comp = admin.moefas_pick_fee_component(hq)
        ctx["component"] = comp
        uat.map_data(f"Fee component of the scheme: {comp} (an Active fee component, setup 2)")
        admin.moefas_rates(hq, comp, mf["rates"])
        admin.wizard_next(hq)
        rev = admin.review_text(hq)
        s.check("Review" in rev and all(f"{v}%" in rev for v in mf["rates"].values()),
                "the Review shows the three rates", rev[-400:])

    @uat.step(5, "Review and Publish", "The scheme is published and becomes read only", needs=(4,))
    def _(s):
        admin.click_button(hq, "Publish")
        txt = admin.main_text(hq) + " " + admin.toast_text(hq)
        if re.search(r"overlap", txt, re.I) and "/new" in hq.url:
            s.note(f"Publish refused because an earlier run published the same period: {txt[:200]}. "
                   "Republishing 100 years later to test the rest of the case.")
            ctx["name"] = f"{mf['name']} UAT-{config.RUN_TAG}-B"
            _, _, txt = _publish_moefas(hq, s, mf, ctx["name"], 100)
            uat.map_data(f"Dates moved 100 years ahead after the overlap refusal: scheme {ctx['name']}")
        admin.moefas_list(hq)
        row = next((r for r in admin.moefas_rows(hq) if ctx["name"] in r), "")
        s.require(row, "the scheme is in the MOEFAS list", txt[:200])
        s.check(re.search(r"Published|Upcoming|Application open", row), "the list shows the scheme as published", row)
        acts = admin.row_actions(hq, f"Actions for {ctx['name']}")
        s.check(not any(re.search(r"Edit|Publish|Delete", a) for a in acts), "the published scheme cannot be edited or published again", acts)
        state_set("moe06_scheme", ctx["name"])

    @uat.step(6, "The scheme list shows the form status label and Approved automatically",
              "Form status label and 'Approved automatically' are shown", needs=(5,))
    def _(s):
        row = next((r for r in admin.moefas_rows(hq) if ctx["name"] in r), "")
        s.check(re.search(r"Upcoming|Application open|Application closed|Published|Effective|Closed", row), "the row shows a form status label", row)
        admin.open_moefas_scheme(hq, ctx["name"])
        detail = admin.main_text(hq)
        s.check(hq.get_by_role("button", name=re.compile(r"^(Save|Publish|Edit)$")).count() == 0, "the scheme detail is read only")
        if not re.search(r"Approved automatically", row + " " + detail, re.I):
            s.gap("The text 'Approved automatically' is on neither the scheme list nor the scheme detail.")

    @uat.step(7, "Open FAS applications", "Applications from all schools are listed, with no Approve or Reject button")
    def _(s):
        admin.hq_fas_applications(hq)
        heads = admin.table_headers(hq)
        s.check("School" in heads, "the list has a School column", heads)
        rows = admin.table_rows(hq)
        schools = set()
        idx = heads.index("School") if "School" in heads else None
        if idx is not None:
            for r in hq.locator("main tbody tr").all():
                cells = r.locator("td").all_inner_texts()
                if len(cells) > idx:
                    schools.add(norm(cells[idx]))
        s.note(f"Schools in the list: {sorted(schools)}")
        s.check(len(rows) > 0, "applications are listed", f"{len(rows)} row(s)")
        n_buttons = hq.get_by_role("button", name=re.compile(r"^(Approve|Reject)", re.I)).count()
        s.check(n_buttons == 0, "there is no Approve or Reject button", f"{n_buttons} found")

    uat.conclude()


def test_UAT_MOE_06_N1(uat):
    hq = uat.actor("moe")
    mf = config.data("moefas")
    name = f"UAT-M01-MOE06N1-{config.RUN_TAG}"

    @uat.step(1, "Create a new scheme and enter the Form closes date (31 Dec 2028) as Effective from", "The wizard takes the values")
    def _(s):
        auth.admin_login(hq, "hq")
        admin.moefas_new(hq)
        admin.moefas_general(hq, name, mf["form_opens"], "2028-12-31", "2028-12-31", "1000")
        s.check(hq.locator("#moefas-create-effective-from").input_value() == "2028-12-31", "Effective from holds 31 Dec 2028")

    @uat.step(2, "Go to the Review step and click Publish",
              "The system shows 'Effective from must be after Form closes' and the scheme is not published", needs=(1,))
    def _(s):
        admin.wizard_next(hq)
        txt = admin.main_text(hq)
        msg_ok = re.search(r"effective.{0,30}(must be|should be).{0,10}after.{0,20}form clos", txt, re.I)
        if "/new" in hq.url and hq.locator("#moefas-create-ghi-to").count():
            # the wizard let it through: try to finish and publish
            admin.moefas_eligibility(hq, "Singapore Citizen", mf["ghi_to"], mf["pci_to"])
            admin.wizard_next(hq)
            comp = admin.moefas_pick_fee_component(hq)
            admin.moefas_rates(hq, comp, mf["rates"])
            admin.wizard_next(hq)
            admin.click_button(hq, "Publish")
            txt = admin.main_text(hq) + " " + admin.toast_text(hq)
            msg_ok = re.search(r"effective.{0,30}after.{0,20}form clos", txt, re.I)
        s.check(msg_ok, "the message says Effective from must be after Form closes", txt[:300])
        admin.moefas_list(hq)
        s.check(not any(name in r for r in admin.moefas_rows(hq)), "the scheme is not published (not in the list)")

    uat.conclude()
