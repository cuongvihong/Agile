"""F4.15 Review and publish (TC-214 to TC-230). Source: FS F4 v1.3 section 6.5 and 7.3.
TC-218 and TC-230 need the F4 build. The overlap cases (TC-219 to TC-225) use their own dates where the
dates of the case contradict the rule "Effective from must be after Form closes" (see docs/COVERAGE.md)."""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data import ui_text as T
from data.ui_text import ENDASH
from pages.flows import build_moefas, build_sbfas, publish
from pages.schemes_page import SchemesPage, SchemeWizard

pytestmark = pytest.mark.f415

OVERLAP = re.compile(r"The period overlaps with ")
DEC_2027 = re.compile(r"31/12/2027|31 Dec 2027")


def try_publish(wizard: SchemeWizard) -> None:
    """Open the review and press Publish when the dialog offers it. A blocked publish may stop at either step."""
    wizard.go_step(3)
    wizard.view_button.click()
    page = wizard.page
    try:
        expect(page.locator(".modal")).to_be_visible(timeout=3000)
    except AssertionError:
        return
    button = page.get_by_role("button", name="Publish", exact=True)
    if button.count():
        button.click()


def expect_message(page, pattern) -> None:
    expect(page.get_by_text(pattern).first).to_be_visible()


def leave_wizard(page, wizard: SchemeWizard) -> None:
    if page.locator(".modal").count():
        page.locator(".modal").get_by_role("button", name=T.TIMES, exact=True).click()
    wizard.cancel_button.click()


def test_tc_214_view_opens_the_review_with_general_eligibility_and_subsidy(hq_schemes):
    """TC-214 View opens the review with General, Eligibility and Subsidy (School fee as fixed amounts)."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Probe 2028")
    wizard.go_step(3)
    wizard.value_type.select_option(label="Fixed amount (S$)")
    wizard.add_component("School fee")
    for level, value in (("Primary", "100"), ("Secondary", "70"), ("Pre-University", "50")):
        wizard.cell_input(level, 0).fill(value)
    dialog = wizard.open_review()
    expect(dialog.title).to_have_text("Review scheme before publishing")
    assert [s.split(" (")[0] for s in dialog.sub_labels()] == ["1 · GENERAL", "2 · ELIGIBILITY",
                                                              "3 · SUBSIDY BY LEVEL"]
    expected = {
        "Scheme name": "QA Probe 2028", "Scheme type": "MOEFAS",
        "Application form": "01/08/2027 " + ENDASH + " 31/12/2027",
        "Assessment": "Automatic, after the form closes on 31/12/2027",
        "Effective from": "01/01/2028", "Effective to": "No end date",
        "Nationality": "Singapore Citizen", "Household income band (GHI)": "Not used",
        "Per capita income band (PCI)": "S$ 0 " + ENDASH + " 1,100",
        "Match rule": "Any selected income band is met",
    }
    for label, text in expected.items():
        expect(dialog.value(label)).to_have_text(text)
    for number in ("100", "70", "50"):
        expect(dialog.table).to_contain_text(number)
    expect(dialog.back_to_edit).to_be_visible()
    expect(dialog.publish_button).to_be_visible()


def test_tc_215_publish_makes_the_scheme_view_only_and_adds_an_upcoming_row(hq, hq_schemes):
    """TC-215 Publish makes the scheme view only and adds an Upcoming row."""
    publish(hq, build_moefas(hq_schemes, "QA Probe 2028"))
    cell = lambda column: hq_schemes.cell("QA Probe 2028", column)        # noqa: E731
    expect(cell("SCHEME")).to_contain_text("Approved automatically")
    expect(cell("ELIGIBILITY")).to_have_text("Singapore Citizen · PCI ≤ S$ 1,100.00")
    expect(cell("APPLICATION FORM")).to_contain_text("01/08/2027 " + ENDASH + " 31/12/2027")
    expect(cell("APPLICATION FORM")).to_contain_text("Not open yet")
    expect(cell("EFFECTIVE TO")).to_have_text("No end date")
    expect(cell("STATUS")).to_have_text("Upcoming")
    assert hq_schemes.actions("QA Probe 2028") == ["View", "Add fee"]
    expect(hq_schemes.card_value("Upcoming")).to_have_text("2")


def test_tc_216_back_to_edit_returns_to_the_wizard_with_the_values_kept(hq_schemes):
    """TC-216 Back to edit returns to the wizard with the values kept."""
    wizard = build_moefas(hq_schemes, "QA Probe 2028")
    dialog = wizard.open_review()
    dialog.back_to_edit.click()
    dialog.expect_closed()
    wizard.go_step(1)
    expect(wizard.name_input).to_have_value("QA Probe 2028")
    wizard.go_step(3)
    assert wizard.component_columns() == ["SCHOOL FEE"]
    expect(wizard.cell_input("Primary", 0)).to_have_value("100")
    wizard.cancel_button.click()
    assert hq_schemes.names() == ["MOEFAS 2027", "MOEFAS 2026", "MOEFAS 2025"]


def test_tc_217_a_scheme_with_errors_cannot_be_published(hq_schemes):
    """TC-217 A scheme with errors cannot be published."""
    wizard = hq_schemes.new_scheme()
    wizard.go_step(3)
    wizard.view_button.click()
    expect(wizard.page.get_by_role("button", name="Publish", exact=True)).to_have_count(0)
    expect(wizard.page.get_by_text(T.ERR_NAME).first).to_be_visible()
    expect(wizard.page.get_by_text("Add at least one fee component.").first).to_be_visible()
    assert wizard.has_warning(1) and wizard.has_warning(3)
    leave_wizard(wizard.page, wizard)
    assert hq_schemes.names() == ["MOEFAS 2027", "MOEFAS 2026", "MOEFAS 2025"]


def test_tc_219_a_moefas_scheme_overlapping_the_effective_period_is_blocked(hq, hq_schemes):
    """TC-219 A MOEFAS scheme overlapping the effective period of another is blocked.
    Scheme B has its own form dates before its Effective from, because the form dates of the case come after it."""
    publish(hq, build_moefas(hq_schemes, "QA Test 2028", eff_to="31/12/2028"))
    wizard = build_moefas(hq_schemes, "QA Test B", form_opens="01/03/2027", form_closes="30/04/2027",
                          eff_from="01/06/2028")
    try_publish(wizard)
    expect_message(wizard.page, "The period overlaps with QA Test 2028 (01/01/2028 " + ENDASH + " 31/12/2028). "
                   "Change Effective from / Effective to.")
    leave_wizard(wizard.page, wizard)
    assert "QA Test B" not in hq_schemes.names()


def test_tc_220_a_moefas_form_period_overlapping_another_form_period_is_blocked(hq, hq_schemes):
    """TC-220 A MOEFAS form period overlapping another form period is blocked."""
    publish(hq, build_moefas(hq_schemes, "QA Test 2028", eff_to="31/12/2028"))
    wizard = build_moefas(hq_schemes, "QA Test C", form_opens="01/12/2027", form_closes="31/01/2028",
                          eff_from="01/01/2029", eff_to="31/12/2029")
    try_publish(wizard)
    expect_message(wizard.page, "The application form period overlaps with QA Test 2028 (01/08/2027 " + ENDASH +
                   " 31/12/2027). Change Form opens / Form closes.")


def test_tc_221_periods_that_touch_without_overlapping_are_allowed(hq, hq_schemes):
    """TC-221 Periods that touch without overlapping are allowed, a start inside the earlier period is blocked."""
    publish(hq, build_moefas(hq_schemes, "QA Test 2028", eff_to="31/12/2028"))
    publish(hq, build_moefas(hq_schemes, "QA Test D", form_opens="01/08/2028", form_closes="31/12/2028",
                             eff_from="01/01/2029"))
    assert "QA Test D" in hq_schemes.names()
    wizard = build_moefas(hq_schemes, "QA Test E", form_opens="01/03/2028", form_closes="30/04/2028",
                          eff_from="31/12/2028")
    try_publish(wizard)
    expect_message(wizard.page, OVERLAP)


def test_tc_222_sbfas_with_the_same_name_and_an_overlapping_period_is_blocked(bvp_schemes):
    """TC-222 SBFAS with the same name and an overlapping period is blocked."""
    wizard = build_sbfas(bvp_schemes, "Tier 1", form_opens="01/08/2026", form_closes="31/12/2026",
                         eff_from="01/01/2027")
    try_publish(wizard)
    expect_message(wizard.page, "The period overlaps with Tier 1 (01/01/2027 – no end date). "
                   "Change Effective from / Effective to.")


def test_tc_223_sbfas_with_a_different_name_in_the_same_period_is_allowed(bvp, bvp_schemes):
    """TC-223 SBFAS with a different name in the same period is allowed."""
    publish(bvp, build_sbfas(bvp_schemes, "Tier 4", form_opens="01/08/2026", form_closes="31/12/2026",
                             eff_from="01/01/2027"))
    assert "Tier 4" in bvp_schemes.names()


def test_tc_224_the_same_sbfas_name_in_another_school_is_allowed(mrs):
    """TC-224 The same SBFAS name in another school is allowed."""
    mrs.go("SBFAS schemes")
    schemes = SchemesPage(mrs.page, "SBFAS schemes")
    publish(mrs, build_sbfas(schemes, "Tier 1", form_opens="01/08/2026", form_closes="31/12/2026",
                             eff_from="01/01/2027", grades=("S1", "S2", "S3", "S4")))
    assert schemes.names().count("Tier 1") >= 1


def test_tc_225_a_draft_with_overlapping_dates_fails_only_at_publish(hq, hq_schemes):
    """TC-225 A draft with overlapping dates can be saved and fails only at Publish."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Overlap")
    wizard.set_dates(form_opens="01/01/2026", form_closes="31/03/2026", eff_from="01/06/2026")
    wizard.save_draft()
    hq.expect_toast(T.TOAST_DRAFT)
    assert "QA Overlap" in hq_schemes.names()
    hq_schemes.action("QA Overlap", "Edit").click()
    reopened = SchemeWizard(hq.page)
    reopened.go_step(3)
    reopened.add_component("School fee")
    for level, value in (("Primary", "100"), ("Secondary", "70"), ("Pre-University", "50")):
        reopened.cell_input(level, 0).fill(value)
    try_publish(reopened)
    expect_message(reopened.page, OVERLAP)


def test_tc_226_publishing_sets_the_effective_to_of_an_earlier_scheme_with_no_end_date(hq, hq_schemes):
    """TC-226 Publishing sets the Effective to of an earlier scheme with no end date."""
    wizard = build_moefas(hq_schemes, "QA Probe 2028")
    dialog = wizard.open_review()
    expect(dialog.blue_note).to_have_text("MOEFAS 2027 has no end date. Publishing sets its Effective to 31/12/2027, "
                                          "the day before this scheme starts.")
    dialog.publish_button.click()
    dialog.expect_closed()
    expect(hq_schemes.cell("MOEFAS 2027", "EFFECTIVE TO")).to_have_text(DEC_2027)


def test_tc_227_an_earlier_scheme_that_already_has_an_end_date_is_left_unchanged(hq, hq_schemes):
    """TC-227 An earlier scheme that already has an end date is left unchanged."""
    publish(hq, build_moefas(hq_schemes, "QA Probe 2028"))
    wizard = build_moefas(hq_schemes, "QA Probe 2029", form_opens="01/08/2028", form_closes="31/12/2028",
                          eff_from="01/01/2029")
    dialog = wizard.open_review()
    expect(dialog.blue_note).to_contain_text("QA Probe 2028 has no end date")
    expect(dialog.blue_note).not_to_contain_text("MOEFAS 2026")
    dialog.publish_button.click()
    dialog.expect_closed()
    expect(hq_schemes.cell("MOEFAS 2026", "EFFECTIVE TO")).to_have_text(re.compile(r"31/12/2026|31 Dec 2026"))


def test_tc_228_an_earlier_sbfas_scheme_of_the_same_name_gets_the_day_before_as_effective_to(bvp, bvp_schemes):
    """TC-228 An earlier SBFAS scheme of the same name gets the day before as Effective to."""
    wizard = build_sbfas(bvp_schemes, "Tier 1", eff_from="01/01/2028")
    dialog = wizard.open_review()
    expect(dialog.blue_note).to_contain_text("Tier 1 has no end date")
    expect(dialog.blue_note).to_contain_text("31/12/2027")
    dialog.publish_button.click()
    dialog.expect_closed()
    bvp.expect_toast(T.TOAST_PUBLISHED)
    expect(bvp_schemes.cell("Tier 1", "STATUS", index=0)).to_have_text("Upcoming")
    expect(bvp_schemes.cell("Tier 1", "EFFECTIVE TO", index=1)).to_have_text(DEC_2027)


def test_tc_229_published_rows_offer_view_and_add_fee_and_no_edit(hq_schemes):
    """TC-229 Published rows offer View and Add fee and no Edit. View is read only."""
    for name in hq_schemes.names():
        assert "Edit" not in hq_schemes.actions(name)
    dialog = hq_schemes.open_view("MOEFAS 2026")
    expect(dialog.title).to_have_text("MOEFAS 2026")
    expect(dialog.subtitle).to_contain_text("Active · view-only")
    assert [s.split(" (")[0] for s in dialog.sub_labels()] == ["1 · GENERAL", "2 · ELIGIBILITY",
                                                              "3 · SUBSIDY BY LEVEL"]
    expect(dialog.footer_close).to_be_visible()
    expect(dialog.publish_button).to_have_count(0)
    expect(dialog.back_to_edit).to_have_count(0)
