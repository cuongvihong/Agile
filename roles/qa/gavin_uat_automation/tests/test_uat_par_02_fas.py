"""UAT-PAR-02 group: the parent applies for FAS online.

What the build has (verified in apps/e-service/src/features/fas-application and on screen):
  /fas-application        My FAS Applications, cards, search, button New Application
  /fas-application/new    ONE form: applicant, beneficiaries (add/remove), family members (add/remove), commitment tick, Submit application
  /fas-application/:id    detail of one application
The master describes a 5 step wizard (Apply for FAS, child lock list, documents, SBFAS tick, context, Save draft, Resume draft,
family code). Those screens do not exist in this build, so the steps that need them are recorded as GAP, with a video of the real
screen. The part of each case that the build can do (fill the form, submit, see the application) is executed for real.
Steps that depend on a time driven job (MOEFAS decision after the form closes) are BLOCKED.

Every run that submits creates real applications with fictional people (NRIC from uat.actors.make_nric). They cannot be deleted from the UI.
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from pages.fas_form_page import FasPages
from uat import env, fasdata
from uat.actors import sign_in_parent

CLIENT_SBFAS = ("Client decision (2026-10-30): there is no tick 'also consider SBFAS'. When an application fails MOEFAS it moves to the school SBFAS "
                "automatically. The tick of the master is out of scope and is not a failure of the build.")

PREFILL_REASON = ("The prefill service of the form answered 502 (GET /api/v1/fas/parent/applications/prefill), so the form opened blank "
                  "with 'Saved details are unavailable'. Applicant details could not be checked as prefilled and read only.")


def go_to_fas(uat, page) -> FasPages:
    """Home -> user menu -> FAS Application -> My FAS Applications."""
    page.get_by_role("button", name="Open user options").click()
    page.get_by_role("link", name="FAS Application").click()
    fas = FasPages(page, env.PARENT_URL)
    expect(page.get_by_role("heading", name="My FAS Applications").first).to_be_visible(timeout=20_000)
    fas._wait_list_loaded()
    return fas


def open_new_application(page, fas: FasPages) -> None:
    fas.new_button.click()
    fas.wait_form_ready()


def fill_typed_form(fas: FasPages, *, children: list, nationality: str = "SC", with_member: bool = True) -> None:
    """The form opens with the children and the spouse of the parent filled from system records and locked. To submit the data of the test
    the children of the records are replaced by blank rows that are filled here; the locked spouse is kept and only its open fields are completed."""
    fas.fill_applicant(fasdata.parent(nationality), fasdata.academic_year())
    fas.use_only_typed_beneficiaries(children)
    if with_member:
        fas.ensure_family_member(fasdata.other_member())
    fas.complete_open_fields()
    fas.tick_commitment()


def fill_and_submit(uat, fas: FasPages, page, *, children=(10,), nationality="SC", with_member=True):
    """Fill the one form and press Submit. Returns the Submission read on the confirmation page."""
    fill_typed_form(fas, children=[fasdata.child(a) for a in children], nationality=nationality, with_member=with_member)
    fas.submit()
    kind, detail = fas.wait_outcome()
    uat.check("the form is accepted", kind == "done", detail if kind != "done" else "")
    return detail


_SEEN_NATIONALITIES: dict[str, str] = {}


def _find_persona(page, wanted: str):
    """Sign in with each Singpass persona and read the nationality of the applicant on the FAS form. Returns the NRIC of the first persona
    whose nationality is `wanted` (the page stays signed in as that persona), or None."""
    from uat.actors import clear_parent_session, persona_options, open_singpass
    open_singpass(page)
    personas = [m.group(1) for m in (re.match(r"(S\d{7}[A-Z])", o) for o in persona_options(page)) if m]
    for nric in dict.fromkeys(personas):
        clear_parent_session(page)
        sign_in_parent(page, nric)
        page.goto(env.PARENT_URL + "/fas-application/new")
        try:
            expect(page.locator("#applicant-nationality")).to_be_visible(timeout=25_000)
            page.wait_for_timeout(1_500)
        except Exception:  # noqa: BLE001
            _SEEN_NATIONALITIES[nric] = "no form"
            continue
        nat = page.locator("#applicant-nationality").input_value()
        _SEEN_NATIONALITIES[nric] = nat
        if nat == wanted:
            return nric
    return None


# ======================================================================= UAT-PAR-02
@pytest.mark.case("UAT-PAR-02")
@pytest.mark.mutating
def test_uat_par_02_submit_online_fas_application(uat):
    page = uat.actor("parent")
    sign_in_parent(page)
    fas = None
    with uat.step("On Home go to Financial assistance and click Apply for FAS", "The application form opens"):
        fas = go_to_fas(uat, page)
        uat.note("Home has no Financial assistance card. The entry is the menu item FAS Application in the user menu, then the button New Application.")
        open_new_application(page, fas)
        uat.check("the form Apply for Financial Assistance is open", "/fas-application/new" in page.url, page.url)

    if fas.prefill_state() != "prefilled":
        uat.blocked("Step 1: choose the relationship and the child, click Continue", PREFILL_REASON, "Parent details are prefilled and read only")
    else:
        with uat.step("Step 1: choose the relationship and the child, click Continue", "Parent details are prefilled and read only"):
            uat.check("applicant name is filled", bool(page.locator("#applicant-fullName").input_value().strip()))
            uat.check("applicant name is read only", page.locator("#applicant-fullName").is_disabled() or page.locator("#applicant-fullName").get_attribute("readonly") is not None)

    with uat.step("Enter the applicant, the child (10 years old) and the family member", "The form accepts valid details"):
        uat.note("The form opens with the children and the spouse of the parent already filled from system records and locked. "
                 "The test replaces the children of the records by one typed child of 10 years and completes the open fields of the spouse.")
        fas.fill_applicant(fasdata.parent(), fasdata.academic_year())
        fas.use_only_typed_beneficiaries([fasdata.child(10)])
        fas.ensure_family_member(fasdata.other_member())
        fas.complete_open_fields()
        uat.check("one beneficiary row is filled", fas.beneficiary_count() == 1, f"{fas.beneficiary_count()} row(s)")
        uat.check("a family member row is filled", fas.family_count() >= 1, f"{fas.family_count()} row(s)")

    with uat.step("Step 2: check members and income, click Continue", "Income comes from Government data, GHI, household size and PCI are shown"):
        text = page.locator("main").inner_text()
        if not re.search(r"\bGHI\b|\bPCI\b|household", text, re.I):
            uat.gap("Income, GHI, household size and PCI are shown from Government data",
                    "The form has no GHI, PCI or household size. The income of the family member comes from the system records (Has income is filled and locked).")

    uat.gap("Step 3: skip documents",
            "The form has no documents upload. There is only the declaration tick.")
    uat.note(CLIENT_SBFAS)
    uat.gap("Step 4: enter context",
            "The form has no context (reason) field.")

    with uat.step("Step 5: review, tick the declaration, click Submit application", "Application submitted, status shown"):
        fas.tick_commitment()
        fas.submit()
        kind, done = fas.wait_outcome()
        uat.check("the confirmation says Application submitted", kind == "done", done if kind != "done" else "")
        if kind != "done":
            uat.conclude()
        uat.check("an application reference is shown", bool(done.code), done.code)
        uat.check("a status is shown", bool(done.status), done.status)
        uat.note(f"Reference {done.code}, status '{done.status}'. Master expects the message 'Application submitted for assessment' and 'Under review, System check Waiting, form close date'.")

    with uat.step("Open My applications", "The application is listed"):
        fas.open_list()
        page.wait_for_timeout(1_000)
        uat.check("the new application is in the list", done.code in page.locator("main").inner_text(), done.code)

    uat.blocked("Open it again after the MOEFAS form closes", "The MOEFAS decision runs when the form closes (time driven job on the server). It cannot be triggered from the UI or waited for in a test run.",
                "Approved MOEFAS from the scheme Effective from, and the parent receives the result email")
    uat.conclude()


# ======================================================================= UAT-PAR-02-N1
@pytest.mark.case("UAT-PAR-02-N1")
def test_uat_par_02_n1_child_is_locked_at_selection(uat):
    page = uat.actor("parent")
    sign_in_parent(page)
    with uat.step("Go to Financial assistance and click Apply for FAS", "The form opens"):
        fas = go_to_fas(uat, page)
        open_new_application(page, fas)

    with uat.step("View the children list at step 1", "Each child is locked with the matching reason, Continue stays disabled"):
        uat.gap("Each child is locked with the matching reason (16 years old, already applied)",
                "The form lists the children of the parent from the system records (fields locked) but does not lock a child with a reason such as "
                "16 years old or already applied. The rules are checked when the form is submitted.")

    with uat.step("Equivalent in the build: submit a child who is 16", "The form refuses the child with the age rule"):
        fill_typed_form(fas, children=[fasdata.child(16)], with_member=True)
        fas.submit()
        page.wait_for_timeout(2_500)
        uat.check("no confirmation page", page.get_by_role("heading", name="Application submitted").count() == 0)
        uat.check("the age rule is shown", page.get_by_text(re.compile(r"at least 7 and younger than 16")).count() > 0)
    uat.conclude()


# ======================================================================= UAT-PAR-02-N2
@pytest.mark.case("UAT-PAR-02-N2")
def test_uat_par_02_n2_no_fas_form_is_open(uat):
    page = uat.actor("parent")
    sign_in_parent(page)
    with uat.step("Open Financial assistance", "My FAS Applications opens"):
        fas = go_to_fas(uat, page)
        uat.check("the list page is open", "/fas-application" in page.url, page.url)

    with uat.step("Click Apply for FAS if it is still enabled", "Apply for FAS is disabled with a note when no form is open"):
        enabled = fas.new_button.is_enabled()
        uat.note(f"New Application is {'enabled' if enabled else 'disabled'}. The build has no code that reads whether a MOEFAS or SBFAS form is open.")
        uat.gap("Apply for FAS is disabled with a note and the children are locked with 'application form is closed' and the next form date",
                "The page never checks the form period. New Application is always available and there is no closed-form note or next form date.")
    uat.conclude()


# ======================================================================= UAT-PAR-02-E1
@pytest.mark.case("UAT-PAR-02-E1")
def test_uat_par_02_e1_save_a_draft_and_return_later(uat):
    page = uat.actor("parent")
    sign_in_parent(page)
    with uat.step("Open the application form and enter some details", "The form accepts partial details"):
        fas = go_to_fas(uat, page)
        open_new_application(page, fas)
        fas.fill_applicant(fasdata.parent(), fasdata.academic_year())

    with uat.step("Click Save draft and exit", "The message 'Draft saved. You can continue later.' appears"):
        draft_buttons = page.get_by_role("button", name=re.compile(r"save draft|draft", re.I))
        if draft_buttons.count() == 0:
            uat.gap("Save draft and exit", "The form has no Save draft button. Buttons on the page: Add beneficiary, Add family member, Submit application.")

    with uat.step("Open Financial assistance again and look for Resume draft", "A Draft card with the saved step and a Resume draft button"):
        page.goto(env.PARENT_URL + "/fas-application")
        page.wait_for_timeout(1_500)
        resume = page.get_by_role("button", name=re.compile(r"resume", re.I))
        if resume.count() == 0:
            uat.gap("Draft card and Resume draft", "My FAS Applications lists only submitted applications. There is no Draft status and no Resume draft button.")
    uat.conclude()


# ======================================================================= UAT-PAR-02-E2
@pytest.mark.case("UAT-PAR-02-E2")
@pytest.mark.mutating
def test_uat_par_02_e2_submit_for_two_children(uat):
    page = uat.actor("parent")
    sign_in_parent(page)
    fas = go_to_fas(uat, page)
    before = set(fas.application_codes())

    with uat.step("Choose both children and go through the form", "The form accepts two beneficiaries"):
        open_new_application(page, fas)
        uat.note("The children of the system records are locked, so two typed children (10 and 8 years old) replace them.")
        fill_typed_form(fas, children=[fasdata.child(10), fasdata.child(8)])
        uat.check("two beneficiary rows", fas.beneficiary_count() == 2, f"{fas.beneficiary_count()} row(s)")

    with uat.step("Click Submit application", "The message Applications submitted appears"):
        fas.submit()
        kind, done = fas.wait_outcome()
        uat.check("a confirmation is shown", kind == "done", done if kind != "done" else "")
        if kind != "done":
            uat.conclude()
        uat.check("a confirmation with a reference is shown", bool(done.code), done.code)

    with uat.step("Open My applications", "Two applications with separate IDs that share one family code FAM-YYYY-NNNNN"):
        fas.open_list()
        page.wait_for_timeout(1_000)
        after = set(fas.application_codes())
        new = after - before
        uat.check("two new applications with separate IDs", len(new) == 2, f"new codes: {sorted(new)}")
        text = page.locator("main").inner_text()
        if not re.search(r"FAM-\d{4}-\d{5}", text):
            first = page.locator("main").get_by_text(sorted(new)[0]).first if new else None
            if first:
                first.click()
                page.wait_for_timeout(1_500)
                text = page.locator("main").inner_text()
        if not re.search(r"FAM-\d{4}-\d{5}", text):
            uat.gap("The two applications share one family code FAM-YYYY-NNNNN", "No family code is shown on the list or on the detail page of the build.")
    uat.conclude()


# ======================================================================= UAT-PAR-02-A1
@pytest.mark.case("UAT-PAR-02-A1")
def test_uat_par_02_a1_fails_moefas_and_moves_to_school_sbfas(uat):
    page = uat.actor("parent")
    sign_in_parent(page)
    go_to_fas(uat, page)
    uat.blocked("Submit the application as in UAT-PAR-02 with household income 8000 per month",
                "Household income comes from the Government API mock. The tester cannot set it to 8000 for one parent.")
    uat.note(CLIENT_SBFAS)
    uat.blocked("After the MOEFAS form closes, open My applications", "The MOEFAS decision is a time driven job on the server. It cannot be triggered from the UI.",
                "SBFAS Pending with the school, timeline shows Sent to school")
    uat.blocked("School Admin approves the Pending SBFAS application", "Depends on the step above.", "Approved SBFAS Tier 1 from Effective from")
    uat.blocked("Parent opens My applications again", "Depends on the step above.", "The parent receives an email")
    uat.conclude()


# ======================================================================= UAT-PAR-02-N3
@pytest.mark.case("UAT-PAR-02-N3")
def test_uat_par_02_n3_fails_moefas_and_sbfas_not_considered(uat):
    page = uat.actor("parent")
    sign_in_parent(page)
    go_to_fas(uat, page)
    uat.note(CLIENT_SBFAS)
    uat.note("The master expects a direct rejection when the tick is cleared. The client removed the tick, so this expectation no longer applies and the case is not counted as a failure of the build.")
    uat.blocked("After the MOEFAS form closes, open My applications", "The MOEFAS decision is a time driven job on the server and the household income of the parent cannot be set.",
                "Rejected with reason 'Not eligible for MOEFAS', and the parent receives an email")
    uat.conclude()


# ======================================================================= UAT-PAR-02-A2
@pytest.mark.case("UAT-PAR-02-A2")
@pytest.mark.mutating
def test_uat_par_02_a2_pr_or_international_student_applies(uat):
    page = uat.actor("parent")
    done = None
    found = _find_persona(page, "PR")
    if found is None:
        uat.blocked("Submit the application for the child (applicant is a Singapore PR)",
                    "The nationality of the applicant comes from the system records and is locked. No Singpass persona is a Singapore PR "
                    f"(nationalities read on the form: {_SEEN_NATIONALITIES}). A PR persona is needed in the Government API mock.",
                    "The application is submitted")
        uat.blocked("Open My applications", "Depends on the step above.", "SBFAS Pending as soon as it is submitted and the timeline shows Sent to school (SBFAS)")
        uat.conclude()
    page.goto(env.PARENT_URL + "/")
    page.wait_for_timeout(1_500)
    fas = go_to_fas(uat, page)
    with uat.step("Submit the application for the child (applicant is a Singapore PR)", "The application is submitted"):
        open_new_application(page, fas)
        done = fill_and_submit(uat, fas, page, nationality="PR")
        uat.check("a reference is shown", bool(done.code), done.code)

    with uat.step("Open My applications", "SBFAS Pending as soon as it is submitted and the timeline shows Sent to school (SBFAS)"):
        fas.open_list()
        page.wait_for_timeout(1_000)
        card = next((c for c in fas.card_texts() if done.code in c), "")
        uat.check("the application is in the list", bool(card), done.code)
        page.locator("main").get_by_text(done.code).first.click()
        page.wait_for_timeout(1_500)
        text = " ".join(page.locator("main").inner_text().split())
        uat.check("the application goes straight to the school (SBFAS)", bool(re.search(r"SBFAS|school", text, re.I)), text[:260])

    uat.blocked("School Admin approves the application and chooses the tier", "A School Admin can approve only an allocation of a published SBFAS scheme that has pending allocations. "
                "The new application is not guaranteed to reach that list without the allocation job.", "The school approves and chooses the tier")
    uat.conclude()


# ======================================================================= UAT-PAR-02-N4
@pytest.mark.case("UAT-PAR-02-N4")
def test_uat_par_02_n4_school_rejects_sbfas(uat):
    page = uat.actor("parent")
    sign_in_parent(page)
    go_to_fas(uat, page)
    uat.blocked("School Admin chooses Reject with a Reason and a Comment", "Needs a Pending SBFAS application of a PR child at the school. None can be created on demand (see UAT-PAR-02-A2). "
                "The school screen rejects selected allocations with Remarks only (no Reason list).", "The application is Rejected")
    uat.blocked("Parent opens My applications", "Depends on the step above.", "Timeline shows the reason and the comment, and the parent receives an email")
    uat.conclude()
