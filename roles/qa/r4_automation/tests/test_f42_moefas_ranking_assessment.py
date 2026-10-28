"""F4.2 MOEFAS ranking and assessment (TC-010 to TC-043). Source: roles/qa/R4_Test_Cases.xlsx, FS F4 v1.3 section 2.2.

Cases that need new applications (SEED-R4-N1 to N12, N23) cannot run on the prototype and are listed in
data/not_automated.py. The base state has three waiting applications for MOEFAS 2027.
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data import seed
from data.ui_text import EMDASH, LE, TOAST_FORM_CLOSED
from pages.applications_page import ApplicationsPage
from pages.dialogs import CloseFormDialog
from pages.flows import close_form_now, open_hq_list
from pages.schemes_page import SchemesPage

pytestmark = pytest.mark.f42

PRIORITY_TEXT = "{n} of {total} (lowest per capita income first)"


def priority_event(n: int, total: int) -> str:
    return f"Form closed · priority {n} of {total} (lowest per capita income first)"


# ------------------------------------------------------------------ TC-010
def test_tc_010_closing_the_form_ranks_by_lowest_pci(hq):
    """TC-010 Closing the form ranks the waiting applications by lowest PCI first."""
    hq.go("MOEFAS schemes")
    schemes = SchemesPage(hq.page, "MOEFAS schemes")
    form_cell = schemes.cell("MOEFAS 2027", "APPLICATION FORM")
    expect(form_cell).to_contain_text("Open")
    expect(form_cell).to_contain_text("3 waiting")

    schemes.action("MOEFAS 2027", "Close form now (demo)").click()
    dialog = CloseFormDialog(hq.page)
    dialog.expect_open()
    expect(dialog.heading).to_contain_text("Close the application form now?")
    expect(dialog.heading).to_contain_text("DEMO ONLY · MOEFAS 2027")
    expect(dialog.root).to_contain_text("The form closes today. No more MOEFAS applications.")
    expect(dialog.root).to_contain_text(
        "ranks the 3 waiting application(s) by need: lowest per capita income first, "
        "then lowest household income, then earliest submitted.")
    expect(dialog.root).to_contain_text("rules met")
    expect(dialog.root).to_contain_text("approved from 01/01/2027")
    expect(dialog.root).to_contain_text(re.compile(r"the school.s SBFAS if the parent agreed, otherwise rejected"))
    dialog.confirm()
    dialog.expect_closed()
    hq.expect_toast(TOAST_FORM_CLOSED)

    apps = open_hq_list(hq)
    for app_id, n in (("00377", 1), ("00412", 2), ("00410", 3)):
        drawer = apps.open(app_id)
        drawer.expect_history_contains(priority_event(n, 3))
        drawer.close()


# ------------------------------------------------------------------ TC-011
def test_tc_011_priority_is_saved_in_the_decision_block(hq_closed):
    """TC-011 Priority n of N is saved and shown in the Decision block."""
    drawer = hq_closed.open("00377")
    drawer.expect_value("DECISION", "Priority", PRIORITY_TEXT.format(n=1, total=3))


# ------------------------------------------------------------------ TC-012
def test_tc_012_only_waiting_applications_of_the_closing_scheme_are_ranked(hq):
    """TC-012 Only waiting MOEFAS applications of the closing scheme are ranked."""
    apps = open_hq_list(hq)
    decided = ["00390", "00381", "00328", "00301", "00386"]
    before = {}
    for app_id in decided:
        drawer = apps.open(app_id)
        before[app_id] = drawer.history()
        drawer.close()

    close_form_now(hq)
    apps = open_hq_list(hq)
    for app_id in decided:
        drawer = apps.open(app_id)
        assert drawer.history() == before[app_id], f"{app_id} got a new History row"
        drawer.close()

    drawer = apps.open("00390")
    drawer.expect_value("DECISION", "Priority", PRIORITY_TEXT.format(n=1, total=4))
    drawer.close()
    drawer = apps.open("00328")
    drawer.expect_value("DECISION", "Priority", PRIORITY_TEXT.format(n=4, total=4))
    drawer.close()
    apps.expect_row("00398", SCHEME="SBFAS", STATUS="Pending")
    apps.expect_row("00386", SCHEME="SBFAS", STATUS="Approved", TIER="Tier 3")


# ------------------------------------------------------------------ TC-014
def snapshot(apps: ApplicationsPage) -> dict:
    """Row values and History of every application, to compare before and after."""
    data = {}
    for app_id in seed.ALL_IDS:
        values = apps.row_values(app_id)
        drawer = apps.open(app_id)
        data[app_id] = (values, drawer.history())
        drawer.close()
    return data


@pytest.mark.draft
def test_tc_014_closing_a_form_without_waiting_applications_changes_nothing(hq):
    """TC-014 Closing a form with no waiting application changes nothing. ASM-R4-01."""
    close_form_now(hq)
    before = snapshot(open_hq_list(hq))
    hq.go("MOEFAS schemes")
    schemes = SchemesPage(hq.page, "MOEFAS schemes")
    button = schemes.action("MOEFAS 2027", "Close form now (demo)")
    if button.count() == 0:
        pytest.skip("The button is not offered after the assessment (the FS rule of ASM-R4-01), nothing to click")
    button.click()
    dialog = CloseFormDialog(hq.page)
    dialog.expect_open()
    expect(dialog.root).to_contain_text("ranks the 0 waiting application(s)")
    dialog.confirm()
    dialog.expect_closed()
    assert snapshot(open_hq_list(hq)) == before


# ------------------------------------------------------------------ TC-016
def test_tc_016_ranking_follows_pci_and_not_the_submit_time(hq_closed):
    """TC-016 Ranking follows PCI and not the submit time (00410 was submitted first and ranks last)."""
    for app_id, n in (("00410", 3), ("00412", 2), ("00377", 1)):
        drawer = hq_closed.open(app_id)
        drawer.expect_history_contains(priority_event(n, 3))
        drawer.close()


# ------------------------------------------------------------------ TC-021
def test_tc_021_a_passing_application_is_approved_by_the_system(hq_closed):
    """TC-021 A passing application is approved by the system."""
    hq_closed.expect_row("00377", STATUS="Approved", SYSTEM_CHECK="Pass", TIER=EMDASH, ML_RECOMMENDATION=EMDASH)
    drawer = hq_closed.open("00377")
    expect(drawer.row("DECISION", "Result")).to_contain_text("Approved")
    drawer.expect_value("DECISION", "Granted", "MOEFAS (MOEFAS 2027) · from 01/01/2027")
    drawer.expect_value("DECISION", "Priority", PRIORITY_TEXT.format(n=1, total=3))
    expect(drawer.decision("Decided by")).to_have_text(
        re.compile(r"^System \(auto-approved\) · 18/10/2026 \d{2}:\d{2}$"))


# ------------------------------------------------------------------ TC-022
def test_tc_022_history_of_an_automatic_approval(hq_closed):
    """TC-022 History of an automatic approval lists priority, approval and the email."""
    drawer = hq_closed.open("00377")
    assert drawer.history_events() == [
        "Submitted",
        "Waiting for the MOEFAS form to close on 31/12/2026",
        priority_event(1, 3),
        "MOEFAS rules met · approved automatically",
        "Email with result sent to parent",
    ]


# ------------------------------------------------------------------ TC-023
def test_tc_023_effective_from_is_the_scheme_start_when_later(hq_closed):
    """TC-023 Effective from is the scheme Effective from when the scheme starts later."""
    drawer = hq_closed.open("00377")
    granted = drawer.value("DECISION", "Granted")
    expect(granted).to_contain_text("from 01/01/2027")
    expect(granted).not_to_contain_text("18/10/2026")


# ------------------------------------------------------------------ TC-025
def test_tc_025_cards_and_tabs_update_after_the_automatic_decisions(hq):
    """TC-025 Cards and tab counts update after the automatic decisions."""
    apps = open_hq_list(hq)
    apps.expect_cards(seed.HQ_CARDS)
    apps.expect_tabs(seed.HQ_TABS)
    close_form_now(hq)
    apps = open_hq_list(hq)
    apps.expect_cards(seed.HQ_CARDS_AFTER_CLOSE)
    apps.expect_tabs(seed.HQ_TABS_AFTER_CLOSE)


# ------------------------------------------------------------------ TC-026
def test_tc_026_automatic_approval_is_final_and_read_only(hq_closed):
    """TC-026 Automatically approved MOEFAS application is final and read only."""
    drawer = hq_closed.open("00377")
    assert drawer.action_buttons() == []
    expect(drawer.root.locator("input, textarea, select")).to_have_count(0)
    drawer.close()
    hq_closed.expect_row("00377", STATUS="Approved")


# ------------------------------------------------------------------ TC-027
def test_tc_027_both_ghi_and_pci_within_the_limits_pass(hq_closed):
    """TC-027 Both GHI and PCI within the limits pass."""
    drawer = hq_closed.open("00377")
    for label in ("Nationality", "Gross household income", "Per capita income"):
        expect(drawer.row("ELIGIBILITY CHECK", label)).to_contain_text("Pass")
    expect(drawer.value("ELIGIBILITY CHECK", "Gross household income")).to_have_text(
        f"S$ 4,120.00 (limit {LE} S$ 4,200.00)")
    expect(drawer.value("ELIGIBILITY CHECK", "Per capita income")).to_have_text(
        f"S$ 1,030.00 (limit {LE} S$ 1,050.00)")
    hq_closed.expect_row("00377", STATUS="Approved")


# ------------------------------------------------------------------ TC-032
@pytest.mark.known_defect(reason="CMP-33: the drawer shows PCI S$ 1,088.00 for 00412, the exact value is 1,087.50")
def test_tc_032_ghi_and_pci_above_the_limits_fail(hq_closed):
    """TC-032 Both GHI and PCI above the limits fail."""
    for app_id, ghi, pci in (("00412", "4,350.00", "1,087.50"), ("00410", "5,200.00", "1,300.00")):
        drawer = hq_closed.open(app_id)
        expect(drawer.value("ELIGIBILITY CHECK", "Gross household income")).to_contain_text(f"S$ {ghi}")
        expect(drawer.value("ELIGIBILITY CHECK", "Per capita income")).to_contain_text(f"S$ {pci}")
        drawer.expect_history_contains("MOEFAS check: not eligible")
        drawer.expect_history_contains("sent to the school")
        drawer.close()
        hq_closed.expect_row(app_id, SCHEME="SBFAS", STATUS="Pending")


# ------------------------------------------------------------------ TC-034
def test_tc_034_limits_come_from_the_scheme_of_the_application(hq_closed):
    """TC-034 Limits come from the scheme of the application."""
    drawer = hq_closed.open("00377")
    drawer.expect_value("ELIGIBILITY CHECK", "Scheme", "MOEFAS 2027 · effective from 01/01/2027")
    expect(drawer.value("ELIGIBILITY CHECK", "Gross household income")).to_contain_text(f"{LE} S$ 4,200.00")
    expect(drawer.value("ELIGIBILITY CHECK", "Per capita income")).to_contain_text(f"{LE} S$ 1,050.00")
    drawer.close()
    drawer = hq_closed.open("00390")
    drawer.expect_value("ELIGIBILITY CHECK", "Scheme", "MOEFAS 2026 · effective from 01/01/2026")
    expect(drawer.value("ELIGIBILITY CHECK", "Gross household income")).to_contain_text(f"{LE} S$ 4,000.00")
    expect(drawer.value("ELIGIBILITY CHECK", "Per capita income")).to_contain_text(f"{LE} S$ 1,000.00")


# ------------------------------------------------------------------ TC-035
def test_tc_035_fail_with_sbfas_yes_becomes_sbfas_pending(hq_closed):
    """TC-035 Fail with Also consider for SBFAS Yes becomes SBFAS Pending for the school."""
    hq_closed.expect_row("00412", SCHEME="SBFAS", SYSTEM_CHECK=EMDASH, STATUS="Pending",
                         SCHOOL="Bukit View Primary")
    drawer = hq_closed.open("00412")
    drawer.expect_history_contains("Form closed · priority 2 of 3")
    drawer.expect_history_contains("MOEFAS check: not eligible · sent to the school's SBFAS (parent agreed)")


# ------------------------------------------------------------------ TC-036
def test_tc_036_school_sees_the_transferred_application_with_ml_tier(hq):
    """TC-036 The school sees the transferred application with an ML recommendation."""
    close_form_now(hq)
    hq.sign_in_school("BVP-0012")
    hq.go("FAS applications")
    apps = ApplicationsPage(hq.page)
    apps.expect_active_tab("Pending")
    apps.expect_ids(["00412", "00410", "00398"])
    apps.expect_cards({"Pending": "3"})
    for app_id in ("00412", "00410"):
        apps.expect_row(app_id, ML_RECOMMENDATION="Tier 3")
        expect(apps.row_button(app_id)).to_have_text("Review")


# ------------------------------------------------------------------ TC-038
def test_tc_038_transferred_application_is_not_visible_to_other_schools(hq):
    """TC-038 A transferred SBFAS application is not visible to other schools."""
    close_form_now(hq)
    hq.sign_in_school("MRS-0012")
    hq.go("FAS applications")
    apps = ApplicationsPage(hq.page)
    for app_id in ("00412", "00410"):
        apps.do_search(app_id)
        apps.expect_empty()
    apps.do_search("")
    for tab in ("Pending", "All", "Approved", "Rejected"):
        apps.open_tab(tab)
        expect(apps.id_cells.filter(has_text=re.compile("00412|00410|00398|00386"))).to_have_count(0)


# ------------------------------------------------------------------ TC-039
@pytest.mark.draft
@pytest.mark.known_defect(reason="CMP-06: the form badge stays Open after the demo close")
def test_tc_039_scheme_shows_assessed_and_no_waiting_count(hq):
    """TC-039 The scheme shows Assessed and no waiting count after processing. ASM-R4-01."""
    schemes = close_form_now(hq)
    cell = schemes.cell("MOEFAS 2027", "APPLICATION FORM")
    expect(cell).to_contain_text("01/08/2026 – 31/12/2026")
    expect(cell).to_contain_text("Assessed 18/10/2026")
    expect(cell).not_to_contain_text("waiting")
    expect(cell).not_to_contain_text("Open")


# ------------------------------------------------------------------ TC-041
def test_tc_041_earlier_schemes_keep_their_assessed_date(hq_schemes):
    """TC-041 Earlier schemes keep their Assessed date and the new one starts waiting."""
    form_2025 = hq_schemes.cell("MOEFAS 2025", "APPLICATION FORM")
    expect(form_2025).to_contain_text("Closed")
    expect(form_2025).to_contain_text("Assessed 01/01/2025")
    form_2026 = hq_schemes.cell("MOEFAS 2026", "APPLICATION FORM")
    expect(form_2026).to_contain_text("Closed")
    expect(form_2026).to_contain_text("Assessed 01/01/2026")
    form_2027 = hq_schemes.cell("MOEFAS 2027", "APPLICATION FORM")
    expect(form_2027).to_contain_text("Open")
    expect(form_2027).to_contain_text("3 waiting")


# ------------------------------------------------------------------ TC-042
def test_tc_042_moe_hq_has_no_approve_or_reject(hq_apps):
    """TC-042 MOE HQ has no Approve or Reject on any application."""
    for app_id in ("00412", "00398", "00386", "00328"):
        drawer = hq_apps.open(app_id)
        expect(drawer.approve_button).to_have_count(0)
        expect(drawer.reject_button).to_have_count(0)
        drawer.close()
    for app_id in seed.ALL_IDS:
        expect(hq_apps.row_button(app_id)).to_have_text("View")


# ------------------------------------------------------------------ TC-043
def test_tc_043_school_admin_cannot_decide_a_moefas_application(bvp_apps):
    """TC-043 The School Admin cannot decide a MOEFAS application."""
    bvp_apps.open_tab("All")
    bvp_apps.do_search("00412")
    bvp_apps.expect_empty()
    assert "Scheme" not in bvp_apps.filter_names()
    assert "School" not in bvp_apps.filter_names()
