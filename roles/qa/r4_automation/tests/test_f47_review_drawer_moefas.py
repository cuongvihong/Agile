"""F4.7 Review drawer, MOEFAS (TC-102 to TC-113). Source: FS F4 v1.3 section 4.
TC-108 is Block (no BA rule, ASM-R4-19) and is listed in data/not_automated.py."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data.ui_text import MIDDOT

pytestmark = pytest.mark.f47

WAITING_NOTE = ("Waiting for the MOEFAS 2027 form to close on 31/12/2026. The system then ranks all applications "
                "by need (lowest per capita income first) and assesses them in that order. The check below is "
                "indicative.")
BOTTOM_NOTE = ("MOEFAS is decided automatically after the form closes: Pass → approved from Effective from, "
               "Fail → the school's SBFAS (if the parent agreed) or rejected.")


# ------------------------------------------------------------- MOEFAS, MOE HQ
def test_tc_102_pending_moefas_drawer_shows_header_and_waiting_note(hq_apps):
    """TC-102 Pending MOEFAS drawer shows the header and the waiting note."""
    drawer = hq_apps.open("00377")
    expect(drawer.eyebrow).to_have_text("MOEFAS REVIEW")
    expect(drawer.title).to_have_text("APP-2026-00377")
    expect(drawer.subtitle).to_have_text(f"Nur Aisyah {MIDDOT} Meridian Secondary")
    expect(drawer.blue_note).to_have_text(WAITING_NOTE)


@pytest.mark.draft
def test_tc_103_eligibility_rows_show_values_limits_and_pass_or_fail(hq_apps):
    """TC-103 Eligibility check rows show scheme, level, nationality, GHI and PCI with Pass or Fail. ASM-R4-17."""
    drawer = hq_apps.open("00377")
    S = "ELIGIBILITY CHECK"
    drawer.expect_value(S, "Scheme", f"MOEFAS 2027 {MIDDOT} effective from 01/01/2027")
    drawer.expect_value(S, "Level", f"Secondary {MIDDOT} S3")
    drawer.expect_value(S, "Nationality", "Singapore Citizen")
    drawer.expect_value(S, "Gross household income", "S$ 4,120.00 (limit ≤ S$ 4,200.00)")
    drawer.expect_value(S, "Per capita income", "S$ 1,030.00 (limit ≤ S$ 1,050.00)")
    for label in ("Nationality", "Gross household income", "Per capita income"):
        expect(drawer.badge(S, label)).to_have_text("Pass")
    expect(drawer.yellow_note).to_have_text(BOTTOM_NOTE)
    drawer.close()
    second = hq_apps.open("00412")
    second.expect_value(S, "Level", f"Primary {MIDDOT} P3")
    expect(second.value(S, "Gross household income")).to_contain_text("S$ 4,350.00 (limit ≤ S$ 4,200.00)")
    expect(second.badge(S, "Gross household income")).to_have_text("Fail")
    expect(second.badge(S, "Per capita income")).to_have_text("Fail")
    expect(second.value(S, "Per capita income")).to_contain_text("(limit ≤ S$ 1,050.00)")


@pytest.mark.draft
@pytest.mark.known_defect(reason="CMP-33: the prototype rounds PCI to S$ 1,088.00 and adds '4% over' (ASM-R4-17)")
def test_tc_103_pci_shows_two_decimals_and_no_extra_text(hq_apps):
    """TC-103 (PCI part) 4,350 divided by 4 shows S$ 1,087.50. ASM-R4-17."""
    drawer = hq_apps.open("00412")
    drawer.expect_value("ELIGIBILITY CHECK", "Per capita income", "S$ 1,087.50 (limit ≤ S$ 1,050.00)")


def test_tc_104_household_context_and_documents_for_moefas(hq_apps):
    """TC-104 Household and income, context and documents are shown for MOEFAS."""
    drawer = hq_apps.open("00377")
    H = "HOUSEHOLD AND INCOME"
    drawer.expect_value(H, "Gross household income", "S$ 4,120.00 / month")
    drawer.expect_value(H, "Household size", "4")
    drawer.expect_value(H, "Per capita income", "S$ 1,030.00")
    drawer.expect_value(H, "Income source", "API")
    expect(drawer.section("CONTEXT")).to_contain_text("My working hours were cut in June")
    expect(drawer.section("DOCUMENTS")).to_contain_text("payslips_2026.pdf")
    expect(drawer.section("DOCUMENTS").get_by_role("button", name="View")).to_be_visible()
    drawer.close()
    empty = hq_apps.open("00390")
    expect(empty.section("CONTEXT")).to_contain_text("No context given.")
    expect(empty.section("DOCUMENTS")).to_contain_text("No documents.")


def test_tc_105_moefas_drawer_has_no_student_parent_or_ml_block(hq_apps):
    """TC-105 MOEFAS drawer has no student, parent or ML block."""
    drawer = hq_apps.open("00412")
    expect(drawer.title).to_have_text("APP-2026-00412")
    assert drawer.section_names() == ["ELIGIBILITY CHECK", "HOUSEHOLD AND INCOME", "CONTEXT", "DOCUMENTS", "HISTORY"]


def test_tc_106_approved_moefas_drawer_shows_granted_priority_and_decided_by(hq_apps):
    """TC-106 Approved MOEFAS drawer shows Granted, Priority and Decided by."""
    drawer = hq_apps.open("00390")
    D = "DECISION"
    drawer.expect_value(D, "Result", "Approved")
    drawer.expect_value(D, "Granted", f"MOEFAS (MOEFAS 2026) {MIDDOT} from 01/01/2026")
    drawer.expect_value(D, "Priority", "1 of 4 (lowest per capita income first)")
    drawer.expect_value(D, "Decided by", f"System (auto-approved) {MIDDOT} 01/01/2026 00:05")


@pytest.mark.draft
def test_tc_107_rejected_moefas_drawer_shows_reason_and_system_as_decider(hq_apps):
    """TC-107 Rejected MOEFAS drawer shows the reason and the system as decider. ASM-R4-11."""
    drawer = hq_apps.open("00328")
    D = "DECISION"
    drawer.expect_value(D, "Result", "Rejected")
    drawer.expect_value(D, "Priority", "4 of 4 (lowest per capita income first)")
    drawer.expect_value(D, "Reason", "Not eligible for MOEFAS")
    drawer.expect_value(D, "Comment", "GHI and PCI both above MOEFAS limits.")
    expect(drawer.value(D, "Decided by")).to_contain_text("System")
    expect(drawer.row(D, "Granted")).to_have_count(0)


def test_tc_109_decision_block_is_not_shown_while_pending(hq_apps):
    """TC-109 Decision block is not shown while the application is pending."""
    drawer = hq_apps.open("00412")
    expect(drawer.title).to_have_text("APP-2026-00412")
    assert "DECISION" not in drawer.section_names()


# ------------------------------------------------------------ open and close
def test_tc_110_drawer_closes_with_the_x_button(hq_apps):
    """TC-110 Drawer closes with the X button and the list keeps its tab, filters and search."""
    hq_apps.set_filter("Status", "Pending")
    hq_apps.do_search("aisha")
    drawer = hq_apps.open("00412")
    drawer.close()
    hq_apps.expect_active_tab("All")
    expect(hq_apps.search).to_have_value("aisha")
    expect(hq_apps.filter("Status").locator("option:checked")).to_have_text("Pending")
    hq_apps.expect_ids(["00412"])


def test_tc_111_drawer_closes_when_clicking_outside(hq_apps):
    """TC-111 Drawer closes when the user clicks outside it. No data is changed."""
    drawer = hq_apps.open("00412")
    drawer.close_by_overlay()
    hq_apps.expect_ids(["00377", "00412", "00410", "00398", "00390", "00386", "00328", "00381", "00301"])
    hq_apps.expect_row("00412", STATUS="Pending")


def test_tc_112_reopening_shows_the_data_of_the_clicked_row(hq_apps):
    """TC-112 Reopening the drawer shows the data of the clicked row."""
    first = hq_apps.open("00412")
    expect(first.subtitle).to_have_text(f"Aisha Rahman {MIDDOT} Bukit View Primary")
    first.close()
    second = hq_apps.open("00410")
    expect(second.title).to_have_text("APP-2026-00410")
    expect(second.subtitle).to_have_text(f"Ryan Lim {MIDDOT} Bukit View Primary")
    assert "00412" not in second.text()


def test_tc_113_filters_and_search_stay_after_the_drawer_closes(hq_apps):
    """TC-113 Filters and search stay after the drawer closes."""
    hq_apps.set_filter("Status", "Pending")
    hq_apps.do_search("ryan")
    hq_apps.expect_ids(["00410"])
    hq_apps.open("00410").close()
    expect(hq_apps.search).to_have_value("ryan")
    expect(hq_apps.filter("Status").locator("option:checked")).to_have_text("Pending")
    hq_apps.expect_ids(["00410"])
