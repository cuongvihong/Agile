"""UAT-MOE group: the MOE HQ user prepares data, sets and tracks the MOEFAS budget, creates a MOEFAS scheme.

What the build has (read from the screens and the source):
  * MOEFAS list /moe-hq/moe-fas, wizard /moe-hq/moe-fas/new (General, Eligibility, Subsidy, Review, buttons Discard, Draft, Back, Next, Publish).
  * The budget is the field "Total budget" in the General step. There is no separate "Manage Budget" screen.
  * Statistics and budget tracking are one tab: /moe-hq/moe-fas/<id>?tab=statistics (Total Budget, Used Budget, Remaining Budget).
  * FAS applications of MOE HQ is a read only list.
Where the master describes something else the step is recorded as GAP. Where a step needs the daily job, a tech simulation
or data the master does not define, it is recorded as BLOCKED. Nothing is shown as passed unless it ran and held.

Data created by these cases (the UI cannot delete a MOEFAS scheme): names start with UAT-GAVIN-. Use tools/cleanup_uat_schemes.sql.
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from pages import real_api
from pages.real_schemes import SchemeList, Detail, Wizard
from uat import env
from uat.actors import sign_in_admin, sign_in_parent
from uat.admin_flows import (base, budget_cards, exhausted_scheme, open_moe_statistics, scheme_id_from_response, sidebar,
                             uat_name)
from uat.flows import SANDBOX, open_account_from_home, prepared_charges, resolve_child, wait_home_card

SEEDED = real_api.SEEDED_MOE_SCHEME_ID


def _moe_page(uat):
    page = uat.actor("moe")
    sign_in_admin(page, "moe")
    return page


# ======================================================================= UAT-MOE-01
@pytest.mark.case("UAT-MOE-01")
@pytest.mark.mutating
@pytest.mark.needs_db
def test_uat_moe_01_prepare_ea_school_student_and_publish_fees(uat):
    """Only the parent side result (step 5) can be fully executed. The first four steps are shown on screen and recorded honestly."""
    with prepared_charges(uat, [100.00], balance=0.00) as ids:
        moe = uat.actor("moe")
        uat.blocked("Run the daily sync job (Government API mock, citizen who has just turned 7)",
                    "The daily sync job is a server side scheduled job. The portals have no button or endpoint to start it, so it cannot be driven from the UI. "
                    "Ask the tech team to run it, or use the seeded EA of the child.",
                    "An Active EA is created for the student with balance 0.00")
        sign_in_admin(moe, "moe")

        with uat.step("Log in as MOE HQ User, open School management", "The screen has Create school and lists the schools"):
            sidebar(moe, "School management")
            expect(moe.get_by_role("heading", name="School management")).to_be_visible(timeout=20_000)
            create = moe.get_by_role("button", name=re.compile("Create school", re.I)).or_(moe.get_by_role("link", name=re.compile("Create school", re.I)))
            uat.check("the Create school control is on the screen", create.count() > 0)
            text = moe.locator("main").inner_text()
            uat.check("the list shows MOE school codes and school names", "School name" in text and "MOE school code" in text)
            if "School Test 01" not in text:
                uat.note("School Test 01 of the master is not in the school list (it is not created by this suite).")
        uat.blocked("Create the School and the School User",
                    "The master gives no MOE code, school type, user name or e-mail for 'School Test 01', so the creation forms cannot be filled with the master data.",
                    "A School and a School User exist")

        school = uat.actor("school")
        uat.use("school")
        with uat.step("Log in as the School User", "The School User reaches the school Admin Portal"):
            sign_in_admin(school, "school")
            uat.check("School User is signed in", "/login" not in school.url, school.url)
        uat.blocked("Create the class P1A, enter student.test01 and assign the student to the class",
                    "No class or student of the master exists on this stack and the master gives no values for the class and student forms. "
                    "The student R9 Sandbox Teo (R9-STU-14) already has an EA and is used instead.",
                    "The student is linked to the EA after class assignment")

        uat.use("moe")
        uat.blocked("Create the Fee Publication for School Test 01 and publish it (Tuition fee 100.00 SGD)",
                    "The fee publication needs the school, class and student created in the previous steps. The charge of 100.00 is put in the database instead (prepared data).",
                    "Student Charge is POSTED")

        parent = uat.actor("parent")
        if ids is None:  # UI only mode: no charge of 100.00 can be created, so the parent side is read on what the environment has
            with uat.step("Open the student's Student Charge as the parent", "The parent sees the fees of the child on the child's fee page"):
                sign_in_parent(parent)
                kid = resolve_child(parent, SANDBOX)
                open_account_from_home(parent, kid["name"])
                parent.get_by_role("link", name=f"View billing for {kid['name']}").click()
                expect(parent.get_by_role("heading", name=re.compile(r"fee|charge|outstanding", re.I)).first).to_be_visible(timeout=30_000)
                parent.wait_for_timeout(1_500)
                text = " ".join(parent.locator("main").inner_text().split())
                uat.check("the fee page of the child shows amounts in SGD", bool(re.search(r"\d+\.\d{2}", text)), text[:160])
                uat.note("The charge of 100.00 of the master cannot be created from the portals, so the amount is not compared.")
            uat.conclude()
        with uat.step("Open the student's Student Charge as the parent", "Student Charge of 100.00 is POSTED and visible to the parent"):
            sign_in_parent(parent)
            wait_home_card(parent, SANDBOX["name"], "SGD 0.00")
            open_account_from_home(parent, SANDBOX["name"])
            parent.get_by_role("link", name=f"View billing for {SANDBOX['name']}").click()
            parent.wait_for_function("() => document.querySelector('main')?.innerText.includes('100.00')", timeout=30_000)
            text = " ".join(parent.locator("main").inner_text().split())
            uat.check_all(("the charge of 100.00 is visible to the parent", "100.00" in text, text[:160]),
                          ("the child EA balance is 0.00", "0.00" in text))
    uat.conclude()


# ======================================================================= UAT-MOE-04
@pytest.mark.case("UAT-MOE-04")
@pytest.mark.mutating
def test_uat_moe_04_set_the_moefas_budget(uat):
    page = _moe_page(uat)
    name = uat_name("moe04")
    win = real_api.window()
    wiz = Wizard(page, base())
    with uat.step("Open the MOEFAS screen where the budget is set", "A screen to enter the MOEFAS Budget Amount opens"):
        lst = SchemeList(page, base()).open()
        lst.new_scheme.click()
        expect(wiz.title).to_be_visible(timeout=20_000)
    uat.gap("Open the MOEFAS Manage Budget screen",
            "The build has no separate Manage Budget screen. The budget is the field 'Total budget' in the General step of the scheme wizard, so the steps below use it.",
            "A screen to manage the budget opens")

    with uat.step("Enter the Budget Amount 1000000.00", "The amount is accepted"):
        wiz.fill_general(name, win, budget="1000000.00")
        uat.check("the Total budget field holds 1000000.00", wiz.budget.input_value() in ("1000000.00", "1000000", "1,000,000.00", "1,000,000"), wiz.budget.input_value())

    with uat.step("Finish the wizard and click Draft (save)", "The budget is saved"):
        wiz.go_next()
        wiz.fill_eligibility()
        wiz.go_next()
        chosen = wiz.pick(1)
        for comp in chosen:
            wiz.fill_levels(comp)
        wiz.go_next()
        with page.expect_response(lambda r: "moe-schemes" in r.url and r.request.method == "POST", timeout=30_000) as info:
            wiz.draft_btn.click()
        sid = scheme_id_from_response(info)
        uat.check("the save request succeeded", info.value.ok, f"HTTP {info.value.status}")
        uat.check("the scheme has an id", bool(sid), "no id in the response")
        page.wait_for_timeout(1_500)

    with uat.step("Reopen the budget view of the saved scheme", "The view shows the saved Budget Amount within MOEFAS scope"):
        page.goto(f"{base()}moe-hq/moe-fas/{sid}?tab=statistics", wait_until="domcontentloaded")
        page.wait_for_function("() => /total budget/i.test(document.querySelector('main')?.innerText || '')", timeout=30_000)
        cards = budget_cards(page)
        status, data = real_api.get_moefas_statistics(uat.request("moe"), base(), sid)
        total_api = (data or {}).get("budget", {}).get("total")
        uat.check_all(
            ("the view shows Total Budget 1,000,000", cards["total"] is not None and float(cards["total"]) == 1000000.0, str(cards)),
            ("the saved amount equals the API value", total_api == 1000000, f"HTTP {status}, total {total_api}"),
        )
        uat.note(f"Draft scheme {name} ({sid}) stays in the list. The UI cannot delete a MOEFAS scheme.")
    uat.conclude()


# ======================================================================= UAT-MOE-05
@pytest.mark.case("UAT-MOE-05")
def test_uat_moe_05_track_moefas_statistics_and_budget_usage(uat):
    page = _moe_page(uat)
    status, data = real_api.get_moefas_statistics(uat.request("moe"), base(), SEEDED)
    if status != 200:
        uat.blocked("Open the MOEFAS Subsidy Statistics page", f"The seeded scheme {SEEDED} does not answer (HTTP {status}). Load the R6 seed data.")
        uat.conclude()
    api = data["budget"]
    with uat.step("Open the MOEFAS Subsidy Statistics page", "The statistics of the MOEFAS scheme open"):
        open_moe_statistics(page, SEEDED)
        uat.check_all(("Total Budget is on the page", page.get_by_text("Total Budget").count() > 0),
                      ("Used Budget is on the page", page.get_by_text("Used Budget").count() > 0))

    with uat.step("Check Total Subsidy Amount Granted", "Total granted subsidy is correct for MOEFAS scope"):
        cards = budget_cards(page)
        uat.check_all(("the page shows Used Budget equal to the granted amount of the API", cards["used"] is not None and float(cards["used"]) == float(api["used"]),
                       f"page {cards['used']}, API {api['used']}"),)
    uat.gap("Open the Budget Tracking page",
            "There is no separate Budget Tracking page. Budget and statistics are one tab of the scheme, which is already open.",
            "The tracking page shows Budget Amount and Subsidy Amount Used")

    with uat.step("Read Budget Amount, Subsidy Amount Used and Remaining Budget", "Remaining Budget equals Budget Amount minus Subsidy Amount Used"):
        cards = budget_cards(page)
        ok_all = all(v is not None for v in cards.values())
        uat.check("the page shows total, used and remaining", ok_all, str(cards))
        uat.check("Remaining Budget = Budget Amount - Subsidy Amount Used", cards["remaining"] == cards["total"] - cards["used"], str(cards))
    uat.conclude()


# ======================================================================= UAT-MOE-05-E1
@pytest.mark.case("UAT-MOE-05-E1")
def test_uat_moe_05_e1_budget_is_exhausted_but_grants_continue(uat):
    page = _moe_page(uat)
    found, looked = exhausted_scheme(uat.request("moe"), "moe")
    if found is None:
        if real_api.get_moefas_statistics(uat.request("moe"), base(), SEEDED)[0] == 200:
            open_moe_statistics(page, SEEDED)   # shown in the video: this scheme is not exhausted
        uat.blocked("Open the Budget Tracking page of a scheme whose Subsidy Amount Used reached the Budget Amount",
                    f"No MOEFAS scheme is exhausted ({looked}). Used only grows when the daily allocation job approves grants, and the UI cannot raise it.",
                    "The page shows a budget exhausted warning")
    else:
        with uat.step(f"Open the Budget Tracking page of {found['name']}", "The page shows a budget exhausted warning"):
            open_moe_statistics(page, found["id"])
            warn = page.get_by_text(re.compile(r"out of budget|budget (is )?exhausted|exhausted", re.I))
            uat.check("a budget exhausted warning is shown", warn.count() > 0, f"Used {found['budget']['used']} of {found['budget']['total']}")
    uat.blocked("Let the system grant one more MOEFAS subsidy",
                "The grant is made by the time driven allocation job. R6 already recorded BUG-R6-003: the build blocks a grant above the remaining budget, which is the opposite of 'grants continue'. Expected to FAIL once the job is run.",
                "The extra grant still goes through and is not blocked")
    uat.conclude()


# ======================================================================= UAT-MOE-06
@pytest.mark.case("UAT-MOE-06")
@pytest.mark.mutating
def test_uat_moe_06_create_a_moefas_scheme_and_view_fas_applications(uat):
    page = _moe_page(uat)
    name = uat_name("moe06")
    win = real_api.window()   # the master dates (2028) would collide on the next run because a scheme cannot be deleted from the UI
    wiz = Wizard(page, base())
    with uat.step("Open MOEFAS schemes and create a new scheme", "The wizard opens with the steps General, Eligibility, Subsidy, Review"):
        lst = SchemeList(page, base()).open()
        lst.new_scheme.click()
        expect(wiz.title).to_be_visible(timeout=20_000)
        uat.check("the four steps are shown", wiz.step_labels() == ["General", "Eligibility", "Subsidy", "Review"], str(wiz.step_labels()))

    with uat.step("General step: enter name, Form opens, Form closes, Effective from", "The General step is accepted"):
        wiz.fill_general(name, win)
        wiz.go_next()
        expect(page.get_by_role("heading", level=2, name="Eligibility", exact=True)).to_be_visible(timeout=15_000)
        uat.note(f"Dates used: form {win['opens']} to {win['closes']}, effective {win['eff_from']} (master dates 2028 would clash on a second run).")

    with uat.step("Eligibility step: choose Singapore Citizen and the GHI, PCI bands", "The Eligibility step is accepted"):
        wiz.fill_eligibility()
        wiz.go_next()
        expect(page.get_by_role("heading", level=2, name="Subsidy", exact=True)).to_be_visible(timeout=15_000)

    with uat.step("Subsidy step: Primary 100%, Secondary 70%, Pre-University 50%", "The rate of each level is entered"):
        chosen = wiz.pick(1)
        uat.check("a fee component is available", bool(chosen), "no active fee component of Function 3")
        for comp in chosen:
            wiz.fill_levels(comp, ("100", "70", "50"))
        wiz.go_next()
        expect(page.get_by_role("heading", name="Review", exact=True)).to_be_visible(timeout=15_000)

    with uat.step("Review and click Publish", "The scheme is published"):
        with page.expect_response(lambda r: "moe-schemes" in r.url and r.request.method == "POST", timeout=30_000) as info:
            wiz.publish_btn.click()
        sid = scheme_id_from_response(info)
        uat.check("the publish request succeeded", info.value.ok, f"HTTP {info.value.status}")
        page.wait_for_timeout(1_500)

    with uat.step("Check the scheme list and the scheme is read only", "The list shows the form status and Approved automatically; the scheme cannot be edited"):
        lst = SchemeList(page, base()).open()
        row = lst.row(name)
        expect(row).to_be_visible(timeout=20_000)
        row_text = " ".join(row.inner_text().split())
        actions = lst.actions(name)
        uat.check_all(
            ("the row shows a form status (Upcoming, Open, Active or Closed)", bool(re.search(r"upcoming|open|active|closed|published", row_text, re.I)), row_text),
            ("the scheme can no longer be published or edited", "Publish" not in actions and not any("Edit" in a for a in actions), str(actions)),
        )
        approved = re.search(r"approved automatically", page.locator("main").inner_text(), re.I)
        if not approved:
            uat.gap("The scheme list shows Approved automatically",
                    f"The list columns are {lst.headers()}. The text 'Approved automatically' is not on the list.",
                    "Approved automatically")
        if sid:
            Detail(page, base()).open(sid)
            uat.check("the detail page is read only (no Save, no Publish)", page.get_by_role("button", name=re.compile("^(Save|Publish)$")).count() == 0)

    with uat.step("Open FAS applications", "The list shows applications from all schools, with no Approve or Reject button"):
        sidebar(page, "FAS applications")
        page.wait_for_load_state("networkidle")
        buttons = page.get_by_role("button", name=re.compile(r"^(Approve|Reject)", re.I)).count()
        headers = [" ".join(h.split()) for h in page.locator("main table thead th").all_inner_texts()]
        uat.check_all(
            ("there is no Approve or Reject button", buttons == 0, f"{buttons} found"),
            ("the table has a School column (all schools)", any("school" in h.lower() for h in headers), f"columns: {headers}"),
        )
    uat.conclude()


# ======================================================================= UAT-MOE-06-N1
@pytest.mark.case("UAT-MOE-06-N1")
def test_uat_moe_06_n1_invalid_scheme(uat):
    page = _moe_page(uat)
    name = uat_name("moe06n1")
    win = {"opens": "2028-08-01", "closes": "2028-12-31", "eff_from": "2028-12-31", "eff_to": "2029-12-31"}
    wiz = Wizard(page, base())
    with uat.step("Create a new scheme and enter Form closes 31 Dec 2028 as Effective from", "The wizard accepts the typing"):
        SchemeList(page, base()).open().new_scheme.click()
        expect(wiz.title).to_be_visible(timeout=20_000)
        wiz.fill_general(name, win)

    message = re.compile(r"effective.*after.*(form )?clos", re.I)
    with uat.step("Go to the Review step and click Publish", "The system shows 'Effective from must be after Form closes' and the scheme is not published"):
        wiz.go_next()
        page.wait_for_timeout(1_500)
        shown = page.get_by_text(message)
        if shown.count() == 0:
            expect(page.get_by_role("heading", level=2, name="Eligibility", exact=True)).to_be_visible(timeout=10_000)
            wiz.fill_eligibility()
            wiz.go_next()
            chosen = wiz.pick(1)
            for comp in chosen:
                wiz.fill_levels(comp)
            wiz.go_next()
            wiz.publish_btn.click()
            page.wait_for_timeout(2_000)
            shown = page.get_by_text(message)
        else:
            uat.note("The build shows the error already when Next is pressed in the General step, before the Review step.")
        text = shown.first.inner_text() if shown.count() else ""
        uat.check("the error about Effective from and Form closes is shown", shown.count() > 0, text or "no such message on screen")
        lst = SchemeList(page, base()).open()
        row = lst.row(name)
        in_list = row.count() > 0
        row_text = " ".join(row.first.inner_text().split()) if in_list else ""
        uat.check("the scheme is not published", (not in_list) or not re.search(r"published|active|upcoming|open", row_text, re.I), row_text)
    uat.conclude()
