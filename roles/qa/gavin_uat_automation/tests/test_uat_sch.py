"""UAT-SCH group: the School Admin enters paper applications, creates SBFAS schemes, approves applications, tracks the SBFAS budget.

What the build has (read from the screens and the source):
  * SBFAS schemes /sbfas-schemes: list with row menu (View, Add fee, Publish, Suspend, Reactivate, Delete), wizard
    General, Eligibility, Subsidy, Review with Save draft and Publish, dialog "Add fee component" with the button "Add fee".
  * Statistics and budget are one tab: /sbfas-schemes/<id>?tab=statistics (Total budget, Used budget, Remaining budget).
  * Approval of SBFAS grants is a scheme level tab (Pending allocations), not a drawer per application.
  * The school screens for paper applications (Upload applications, Upload scans, Review application) are checked on screen:
    the case is recorded as GAP only when the screen is really not there.

Data created by these cases: names start with UAT-GAVIN-. Draft schemes are deleted by the API at the end, published ones stay
(use tools/cleanup_uat_schemes.sql).
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from pages import real_api
from pages.real_sbfas import SbfasAddFee, SbfasList, SbfasWizard
from pages.real_schemes import tick
from uat.actors import sign_in_admin
from uat.admin_flows import (base, budget_cards, dump_screen, exhausted_scheme, open_sbfas_statistics, scheme_id_from_response, sidebar,
                             uat_name)


def _school_page(uat):
    page = uat.actor("school")
    sign_in_admin(page, "school")
    return page


def _need_fees(uat, count: int):
    """Active fee components and grades of the school of the School User, read with the session of the browser window."""
    req = uat.request("school")
    fees = real_api.school_fee_components(req, base())
    offerings = real_api.school_offerings(req, base())
    if len(fees) < count or not offerings:
        pytest.skip(f"needs {count} active fee component(s) and at least one active grade at the school; found {len(fees)} fee(s), {len(offerings)} grade(s)")
    return fees, offerings


def _cleanup_draft(uat, sid: str) -> None:
    if sid:
        try:
            real_api.delete_sbfas(uat.request("school"), base(), sid)
        except Exception:  # noqa: BLE001
            pass


def _fill_sbfas_wizard(uat, page, wiz: SbfasWizard, name: str, win: dict, fee_name: str, offerings, *, budget="1000", rates=(100, 80, 60)):
    """General, Eligibility (Singapore Citizen), Subsidy with the master rates for the first grades, then Review."""
    wiz.fill_general(name, win, budget=budget)
    wiz.go_next()
    expect(page.get_by_text("Eligible nationalities")).to_be_visible(timeout=15_000)
    tick(page.locator("#sbfas-nationality-SC"))
    wiz.fill_income_bands()
    wiz.go_next()
    expect(page.get_by_role("heading", name="Active fee components")).to_be_visible(timeout=15_000)
    wiz.pick(fee_name)
    for i, level in enumerate(wiz.levels()):
        wiz.cell(fee_name, level).fill(str(rates[i] if i < len(rates) else rates[-1]))
    wiz.review()


# ======================================================================= UAT-SCH-01 group
def _open_paper_upload_area(uat, page):
    """Open the school's FAS applications and look for the paper upload screens named in the master."""
    sidebar(page, "FAS applications")
    page.wait_for_load_state("networkidle")
    body = page.locator("main").inner_text()
    # The first <nav> is the breadcrumb. The sidebar item 'Record a paper application' sits in the other nav or aside, so read all of them.
    nav = " ".join(" ".join(page.locator("nav, aside").all_inner_texts()).split())
    found = re.search(r"upload (applications|scans)|record a paper application|paper application", body + " " + nav, re.I)
    return found, " ".join(nav.split())[:200]



def _probe_paper_application(uat, page, tag: str) -> str:
    """Open the school menu item 'Record a paper application', search the parent of the dev seed pack by NRIC (read only, nothing is saved) and
    save the controls of the screen in artifacts/probe_<tag>.json. Returns a short text for the note."""
    try:
        sidebar(page, "Record a paper application")
        page.wait_for_load_state("networkidle")
        first = dump_screen(page, f"{tag}_1")
        box = page.get_by_label(re.compile(r"nric|search", re.I)).first
        if box.count() and box.is_enabled():
            box.fill("S8901234H")
            btn = page.get_by_role("button", name=re.compile(r"^search|find|look up", re.I)).first
            if btn.count():
                btn.click()
            else:
                box.press("Enter")
            page.wait_for_timeout(3_000)
        second = dump_screen(page, f"{tag}_2")
        return (f"Screen {first['url']}; fields {[f['label'] or f['id'] for f in first['fields']][:12]}; buttons {first['buttons'][:8]}; "
                f"after the search: {len(second['fields'])} fields, buttons {second['buttons'][:8]}. Controls saved in artifacts/probe_{tag}_1.json and _2.json.")
    except Exception as err:  # noqa: BLE001
        return f"The screen could not be read: {type(err).__name__}: {str(err)[:120]}"


@pytest.mark.case("UAT-SCH-01")
def test_uat_sch_01_enter_a_parents_paper_application(uat):
    page = _school_page(uat)
    with uat.step("Open the school menu FAS applications", "The screen Upload applications is offered"):
        found, nav = _open_paper_upload_area(uat, page)
        uat.check("the school FAS applications screen opens", page.get_by_role("heading").count() > 0)
    if found:
        uat.note(_probe_paper_application(uat, page, "sch01"))
        uat.blocked("Upload scans, enter NRICs, relationship, declaration, Review and submit",
                    f"The build has the school menu item '{found.group(0)}' (search the parent by NRIC, then fill and submit the form). The master describes Upload scans, Review and Save draft instead, so the form is not automated yet. Review it by hand.",
                    "A paper application is submitted with source Paper and status Pending")
    else:
        uat.gap("Open Upload applications, click Upload scans, add paper-form-test01.pdf, click Upload and read",
                f"The school menu has no Upload applications or Upload scans. Menu seen: {nav}",
                "Applicant and child details are prefilled and locked")
        uat.gap("Enter applicant NRIC S0000100A and child NRIC S0000001A, relationship Mother, context, declaration, Review and submit",
                "There is no paper application form for the School User in this build, so nothing can be entered or submitted.",
                "Application submitted for assessment; one application per child with source Paper and status Pending")
    uat.conclude()


@pytest.mark.case("UAT-SCH-01-N1")
def test_uat_sch_01_n1_blocked_when_submitting_a_paper_application(uat):
    page = _school_page(uat)
    with uat.step("Open the school menu FAS applications", "A paper application can be opened on the Review application screen"):
        found, nav = _open_paper_upload_area(uat, page)
        uat.check("the school FAS applications screen opens", page.get_by_role("heading").count() > 0)
    if found:
        uat.note(_probe_paper_application(uat, page, "sch01_n1"))
        uat.blocked("Leave Phone empty; child outside 7 to 16; child with an application; same NRIC for applicant and child",
                    f"The build has the school menu item '{found.group(0)}'. The four blocking rules are not automated yet. Review them by hand.",
                    "A red note at the top states what to fix and no application is created")
    else:
        uat.gap("Leave Phone empty and click Review and submit (and the three other blocking rules)",
                f"There is no Review application screen for paper applications in the school portal. Menu seen: {nav}",
                "Each time a red note at the top of the page states what to fix; no application is created")
    uat.conclude()


@pytest.mark.case("UAT-SCH-01-E1")
def test_uat_sch_01_e1_save_a_draft_when_entry_is_incomplete(uat):
    page = _school_page(uat)
    with uat.step("Open the school menu FAS applications", "The Upload applications list is available"):
        found, nav = _open_paper_upload_area(uat, page)
        uat.check("the school FAS applications screen opens", page.get_by_role("heading").count() > 0)
    if found:
        uat.note(_probe_paper_application(uat, page, "sch01_e1"))
        uat.blocked("Save draft, return to the list, click Continue on the Draft row",
                    f"The build has the school menu item '{found.group(0)}'. The draft flow is not automated yet. Review it by hand.",
                    "A Draft row with Application ID Not submitted, and Continue reopens the entered data")
    else:
        uat.gap("Click Save draft, return to the Upload applications list, click Continue on the Draft row",
                f"There is no paper application entry and no Draft row for the School User in this build. Menu seen: {nav}",
                "The list shows a Draft row with Application ID Not submitted; Continue reopens the data")
    uat.conclude()


# ======================================================================= UAT-SCH-02
@pytest.mark.case("UAT-SCH-02")
@pytest.mark.mutating
def test_uat_sch_02_create_an_sbfas_scheme_and_add_a_fee(uat):
    page = _school_page(uat)
    fees, offerings = _need_fees(uat, 2)
    first, second = fees[0]["name"], fees[1]["name"]
    name = uat_name("tier1")
    win = real_api.sbfas_window(0)
    lst, wiz = SbfasList(page, base()), SbfasWizard(page, base())
    sid = ""
    with uat.step("Open SBFAS schemes and create a new scheme named Tier 1", "The wizard opens with General, Eligibility, Subsidy, Review"):
        lst.open()
        page.get_by_role("link", name=re.compile(r"(new|create).*scheme", re.I)).or_(page.get_by_role("button", name=re.compile(r"(new|create).*scheme", re.I))).first.click()
        expect(wiz.title).to_be_visible(timeout=20_000)
        uat.check("the steps are General, Eligibility, Subsidy, Review", wiz.step_labels() == ["General", "Eligibility", "Subsidy", "Review"], str(wiz.step_labels()))
        uat.note(f"The scheme is named {name} instead of 'Tier 1' so that a second run does not clash.")

    with uat.step("Enter the form period and the effective period, Singapore Citizen, rates P1 100%, P2 80%, P3 60%", "The wizard reaches the Review step"):
        _fill_sbfas_wizard(uat, page, wiz, name, win, first, offerings)
        uat.note("The GHI and PCI bands were left at their defaults: the build does not require them to publish.")

    with uat.step("Review and click Publish", "Tier 1 is published and becomes read only"):
        with page.expect_response(lambda r: "sbfas-schemes" in r.url and r.request.method == "POST", timeout=30_000) as info:
            wiz.publish()
        sid = scheme_id_from_response(info)
        uat.check("the publish request succeeded", info.value.ok, f"HTTP {info.value.status}")
        lst.open()
        lst.search(name)
        row = lst.row(name)
        expect(row).to_be_visible(timeout=20_000)
        actions = lst.actions(name)
        uat.check("the published scheme cannot be published or edited again", "Publish" not in actions and not any("Edit" in a for a in actions), str(actions))

    with uat.step("Check that Add fee is offered only for Active or Upcoming schemes", "Add fee is on the published scheme, not on a draft"):
        uat.check("Add fee is offered for the published scheme", "Add fee" in actions, str(actions))
        draft_name = uat_name("draft")
        _st, ok, data, _msg = real_api.create_sbfas_with_budget(
            uat.request("school"), base(), name=draft_name, win=real_api.sbfas_window(3), fee_ids=[fees[0]["id"]], offerings=offerings, budget=1000, publish=False)
        draft_id = (data or {}).get("id", "")
        try:
            if ok:
                lst.open()
                lst.search(draft_name)
                draft_actions = lst.actions(draft_name)
                uat.check("Add fee is not offered for a draft scheme", "Add fee" not in draft_actions, str(draft_actions))
            else:
                uat.note(f"The draft used to compare could not be created: {_msg}")
        finally:
            _cleanup_draft(uat, draft_id)

    with uat.step("When the scheme is Active or Upcoming click Add fee, choose the new component, enter a value, click Add fee", "The new column is added and the old columns stay read only"):
        lst.open()
        lst.search(name)
        lst.do_action(name, "Add fee")
        dialog = SbfasAddFee(page)
        expect(dialog.dialog).to_be_visible(timeout=15_000)
        options = dialog.options()
        uat.check("the dialog offers the fee that is not in the scheme yet", second in options, str(options))
        uat.check("the fee already in the scheme is not offered again", first not in options, str(options))
        dialog.fee_select.select_option(label=second)
        for level in dialog.level_rows():
            dialog.percentage(level).fill("15")
        dialog.submit.click()
        expect(page.get_by_text("Fee added", exact=False).first).to_be_visible(timeout=20_000)
        updated = next((s for s in real_api_list(uat) if s.get("id") == sid), {})
        uat.check("the scheme now has two fee components", updated.get("feeComponentCount") == 2, str(updated.get("feeComponentCount")))
        uat.note("The master button 'Add to scheme' is called 'Add fee' in the build.")
    uat.blocked("The subsidy applies to the open fees of students already granted the scheme",
                "It needs students who already hold the scheme and have open fees. This suite creates a new scheme, so no student holds it.",
                "The subsidy applies to open fees of students already granted the scheme")
    uat.conclude()


def real_api_list(uat):
    from uat.admin_flows import list_sbfas
    return list_sbfas(uat.request("school"))


# ======================================================================= UAT-SCH-02-N1
@pytest.mark.case("UAT-SCH-02-N1")
@pytest.mark.mutating
def test_uat_sch_02_n1_invalid_sbfas_scheme(uat):
    page = _school_page(uat)
    fees, offerings = _need_fees(uat, 1)
    fee = fees[0]["name"]
    tier1 = uat_name("tier1")
    win = real_api.sbfas_window(1)
    req = uat.request("school")
    _st, ok, data, msg = real_api.create_sbfas_with_budget(
        req, base(), name=tier1, win=win, fee_ids=[fees[0]["id"]], offerings=offerings, budget=1000, publish=True)
    if not ok:
        uat.blocked("The school's Tier 1 scheme is published (setup)", f"The setup scheme could not be published: {msg}")
        uat.conclude()
    lst, wiz = SbfasList(page, base()), SbfasWizard(page, base())

    with uat.step("Create another scheme also named Tier 1 with an overlapping application period", "The wizard reaches the Review step"):
        wiz.open()
        _fill_sbfas_wizard(uat, page, wiz, tier1, win, fee, offerings)

    with uat.step("Click Publish", "The system reports an overlap with an existing scheme and the scheme is not published"):
        wiz.publish()
        page.wait_for_timeout(2_500)
        alerts = [" ".join(t.split()) for t in page.get_by_role("alert").all_inner_texts()]
        shown = " | ".join(a for a in alerts if a) or " ".join(page.locator("main").inner_text().split())[:200]
        lst.open()
        lst.search(tier1)
        count = lst.row(tier1).count()
        uat.check("the second scheme with the same name and period is not created", count == 1, f"{count} scheme(s) named {tier1}")
        if re.search(r"overlap", shown, re.I):
            uat.check("the message names the overlap", True, f"screen said: {shown}")
        else:
            uat.gap("The message names the overlap with the existing scheme",
                    f"The build refuses the second scheme because of the NAME ('{shown}') and has no overlap check: the next step publishes a scheme with "
                    "another name and the same period without any message.")

    with uat.step("Rename it to Tier 2 and Publish again", "The scheme with a different name is published"):
        tier2 = uat_name("tier2")
        wiz.open()
        _fill_sbfas_wizard(uat, page, wiz, tier2, win, fee, offerings)
        with page.expect_response(lambda r: "sbfas-schemes" in r.url and r.request.method == "POST", timeout=30_000) as info:
            wiz.publish()
        uat.check("the publish request succeeded", info.value.ok, f"HTTP {info.value.status}")
        lst.open()
        lst.search(tier2)
        expect(lst.row(tier2)).to_be_visible(timeout=20_000)
        uat.note("Tier 2 is created through a new wizard run with the same period, not by renaming the open form.")
    uat.conclude()


# ======================================================================= UAT-SCH-03
def _pending_area(uat, page):
    sidebar(page, "FAS applications")
    page.wait_for_load_state("networkidle")
    reviews = page.get_by_role("button", name=re.compile(r"^(Review|Reject)", re.I)).count()
    return reviews, " ".join(page.locator("main").inner_text().split())[:200]


@pytest.mark.case("UAT-SCH-03")
def test_uat_sch_03_approve_an_sbfas_application(uat):
    page = _school_page(uat)
    with uat.step("Open FAS applications, Pending tab", "The Pending tab lists applications"):
        reviews, text = _pending_area(uat, page)
        uat.check("the FAS applications screen opens", page.get_by_role("heading").count() > 0)
    uat.blocked("Click Review on the application, check the drawer, choose a tier, Comment Eligible, Confirm approval",
                f"No Pending SBFAS application with the data of the master is available ({reviews} Review button(s) on screen). "
                "Approval cannot be undone from the UI, so this suite never approves a real application. "
                "The build approves grants on the scheme tab Pending allocations, not in a drawer with an ML recommendation.",
                "The application becomes Approved with the tier; Subsidy applied to the student's EA fees; the parent receives an email")
    uat.conclude()


@pytest.mark.case("UAT-SCH-03-N1")
def test_uat_sch_03_n1_reject_an_sbfas_application(uat):
    page = _school_page(uat)
    with uat.step("Open the application in FAS applications", "The application opens"):
        reviews, text = _pending_area(uat, page)
        uat.check("the FAS applications screen opens", page.get_by_role("heading").count() > 0)
    uat.blocked("Click Reject, choose Reason Income above limit, Comment, click Reject application",
                f"No Pending SBFAS application is available ({reviews} Review or Reject button(s) on screen). "
                "A rejection cannot be undone from the UI, so this suite never rejects a real application. "
                "The build rejects on the scheme tab Pending allocations with 'Reject selected' and Remarks.",
                "Reject application stays disabled until Reason and Comment are filled; the application becomes Rejected; the parent is notified by email")
    uat.conclude()


# ======================================================================= UAT-SCH-04
@pytest.mark.case("UAT-SCH-04")
@pytest.mark.mutating
def test_uat_sch_04_set_and_track_the_sbfas_budget(uat):
    page = _school_page(uat)
    fees, offerings = _need_fees(uat, 1)
    name = uat_name("sch04")
    win = real_api.sbfas_window(2)
    lst, wiz = SbfasList(page, base()), SbfasWizard(page, base())
    sid = ""
    try:
        with uat.step("Open the screen where the SBFAS budget is set", "A screen to enter the SBFAS Budget Amount opens"):
            wiz.open()
        uat.gap("Open the SBFAS Manage Budget screen",
                "The build has no separate Manage Budget screen. The budget is the field 'Total budget' in the General step of the SBFAS wizard, so the steps below use it.",
                "A screen to manage the budget opens")

        with uat.step("Enter the Budget Amount 50000.00 and click Save draft", "The budget is saved and tied to the user's school"):
            _fill_sbfas_wizard(uat, page, wiz, name, win, fees[0]["name"], offerings, budget="50000.00")
            with page.expect_response(lambda r: "sbfas-schemes" in r.url and r.request.method == "POST", timeout=30_000) as info:
                wiz.save_draft()
            sid = scheme_id_from_response(info)
            uat.check("the save request succeeded", info.value.ok, f"HTTP {info.value.status}")
            uat.check("the scheme has an id", bool(sid))

        with uat.step("Open the budget tracking of the scheme", "The tracking shows Budget Amount, Subsidy Amount Used and Remaining Budget of the school"):
            open_sbfas_statistics(page, sid)
            cards = budget_cards(page)
            status, data = real_api.get_sbfas_statistics(uat.request("school"), base(), sid)
            api = (data or {}).get("budget", {})
            uat.check_all(
                ("Total budget shows 50,000", cards["total"] is not None and float(cards["total"]) == 50000.0, str(cards)),
                ("Used budget and Remaining budget are shown", cards["used"] is not None and cards["remaining"] is not None, str(cards)),
                ("Remaining = Total - Used", cards["remaining"] == cards["total"] - cards["used"] if None not in cards.values() else False, str(cards)),
                ("the page agrees with the API", api.get("total") == 50000, f"HTTP {status}, {api}"),
            )

        with uat.step("Check that no data of another school appears", "The other school's scheme cannot be opened by this School User"):
            other_status, other_data = real_api.get_sbfas_statistics(uat.request("school"), base(), real_api.SEEDED_OTHER_SCHOOL_SBFAS_SCHEME_ID)
            names = [s.get("name") for s in real_api_list(uat)]
            other_budget = ((other_data or {}).get("budget") or {}) if isinstance(other_data, dict) else {}
            leaked = other_status == 200 and bool(other_budget.get("total") or other_budget.get("used"))
            if other_status == 200 and not leaked:
                uat.note(f"HTTP 200 for the seeded id of another school ({real_api.SEEDED_OTHER_SCHOOL_SBFAS_SCHEME_ID}) but the body holds no budget figure: "
                         f"the id is not a scheme of this environment, so no data is returned. Body: {str(other_data)[:160]}")
            uat.check("no statistics of another school's scheme are returned", other_status in (401, 403, 404) or not leaked,
                      f"HTTP {other_status}, budget {other_budget}")
            uat.check("the list holds only the school's own schemes", real_api.SEEDED_OTHER_SCHOOL_SBFAS_SCHEME_ID not in [s.get("id") for s in real_api_list(uat)], str(names[:5]))
    finally:
        _cleanup_draft(uat, sid)
    uat.conclude()


# ======================================================================= UAT-SCH-04-E1
@pytest.mark.case("UAT-SCH-04-E1")
def test_uat_sch_04_e1_sbfas_budget_is_exhausted_but_grants_continue(uat):
    page = _school_page(uat)
    found, looked = exhausted_scheme(uat.request("school"), "sbfas")
    if found is None:
        if real_api.get_sbfas_statistics(uat.request("school"), base(), real_api.SEEDED_RI_SBFAS_SCHEME_ID)[0] == 200:
            open_sbfas_statistics(page, real_api.SEEDED_RI_SBFAS_SCHEME_ID)   # shown in the video: this scheme is not exhausted
        uat.blocked("Open the Budget Tracking page of a scheme whose Subsidy Amount Used reached the Budget Amount",
                    f"No SBFAS scheme of this school is exhausted ({looked}). Used only grows when grants are approved, and the UI cannot raise it.",
                    "The page shows a budget exhausted warning")
    else:
        with uat.step(f"Open the Budget Tracking page of {found['name']}", "The page shows a budget exhausted warning"):
            open_sbfas_statistics(page, found["id"])
            warn = page.get_by_text(re.compile(r"out of budget|budget (is )?exhausted|exhausted", re.I))
            uat.check("a budget exhausted warning is shown", warn.count() > 0, f"Used {found['budget']['used']} of {found['budget']['total']}")
    uat.blocked("Approve one more SBFAS application",
                "No Pending SBFAS application is available and an approval cannot be undone. R6 recorded that the build refuses a grant above the remaining budget, "
                "which is the opposite of 'grants continue'. Expected to FAIL when it is run with real data.",
                "The application is still approved and the grant is not blocked")
    uat.conclude()
