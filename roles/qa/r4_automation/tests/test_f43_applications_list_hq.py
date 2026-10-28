"""F4.3 Applications list, MOE HQ (TC-045 to TC-058). Source: FS F4 v1.3 section 3.1 to 3.3."""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data import seed
from data.ui_text import EMDASH

pytestmark = pytest.mark.f43

HQ_SUBTITLE = ("All schools. MOEFAS is assessed automatically by the system after its application form closes. "
               "SBFAS is decided by each school.")
HQ_NOTE = re.compile(
    r"^MOEFAS has no tiers\.\s*Its applications wait until the application form closes[.;]\s*"
    r"the system then ranks them by need \(lowest per capita income first\) and approves or rejects them automatically\.\s*"
    r"SBFAS is decided by each school \(view only here\)\.?$",
    re.IGNORECASE,
)


def test_tc_045_hq_list_shows_subtitle_export_and_note(hq_apps):
    """TC-045 MOE HQ list shows the subtitle, Export button and note."""
    expect(hq_apps.heading).to_be_visible()
    expect(hq_apps.subtitle).to_have_text(HQ_SUBTITLE)
    expect(hq_apps.export_button).to_be_visible()
    expect(hq_apps.note).to_have_text(HQ_NOTE)


def test_tc_046_hq_cards_show_base_counts_and_ignore_filters(hq_apps):
    """TC-046 MOE HQ cards show the base counts and ignore filters and search."""
    hq_apps.expect_cards(seed.HQ_CARDS)
    expect(hq_apps.card_hint("Total applications")).to_have_text("All schools")
    expect(hq_apps.card_hint("MOEFAS approved")).to_have_text("Approved automatically")
    expect(hq_apps.card_hint("Approved")).to_have_text("MOEFAS and SBFAS")
    expect(hq_apps.card_hint("Rejected")).to_have_text("MOEFAS and SBFAS")
    hq_apps.set_filter("School", "Riverside Secondary")
    hq_apps.do_search("lee")
    hq_apps.expect_ids(["00328", "00381"])
    hq_apps.expect_cards(seed.HQ_CARDS)


def test_tc_047_hq_tabs_show_counts_and_open_on_all(hq_apps):
    """TC-047 MOE HQ tabs show the counts and open on All."""
    hq_apps.expect_tabs(seed.HQ_TABS)
    hq_apps.expect_active_tab("All")
    assert [re.sub(r"\d+$", "", t.strip()) for t in hq_apps.tabs.all_inner_texts()] == [
        "Pending", "All", "Approved", "Rejected"]
    hq_apps.open_tab("Pending")
    hq_apps.expect_ids(["00377", "00412", "00410", "00398"])
    hq_apps.open_tab("Approved")
    hq_apps.expect_ids(["00390", "00386", "00381", "00301"])
    hq_apps.open_tab("Rejected")
    hq_apps.expect_ids(["00328"])


@pytest.mark.draft
def test_tc_048_tab_counts_stay_fixed_when_filters_or_search_change(hq_apps):
    """TC-048 Tab counts stay fixed when filters or search change the rows. ASM-R4-06."""
    hq_apps.set_filter("School", "Riverside Secondary")
    hq_apps.expect_tabs(seed.HQ_TABS)
    hq_apps.set_filter("School", "School: All")
    hq_apps.do_search("aisha")
    hq_apps.expect_ids(["00412"])
    hq_apps.expect_tabs(seed.HQ_TABS)


def test_tc_049_hq_table_has_the_columns_in_order(hq_apps):
    """TC-049 MOE HQ table has the 12 columns in the right order."""
    assert hq_apps.column_names() == seed.HQ_COLUMNS + [""]
    expect(hq_apps.row_button("00412")).to_have_text("View")


def test_tc_050_application_and_student_cells_use_the_required_formats(hq_apps):
    """TC-050 Application and Student cells use the required formats."""
    row = hq_apps.row("00412")
    expect(row.locator("td").nth(0)).to_have_text(re.compile(r"^APP-\d{4}-\d{5}$"))
    expect(row.locator("td").nth(0)).to_have_text("APP-2026-00412")
    expect(row.locator("td").nth(1).locator("strong")).to_have_text("Aisha Rahman")
    expect(row.locator("td").nth(1).locator("small")).to_have_text("T1801177H")


def test_tc_051_system_check_by_scheme_and_status(hq_apps):
    """TC-051 System check shows Waiting, Pass, Fail or a dash by scheme and status."""
    for app_id, text in (("00377", "Waiting"), ("00390", "Pass"), ("00328", "Fail"), ("00398", EMDASH)):
        hq_apps.expect_row(app_id, SYSTEM_CHECK=text)


def test_tc_052_tier_and_ml_recommendation_follow_scheme_and_decision(hq_apps):
    """TC-052 Tier and ML recommendation follow the scheme and the decision."""
    hq_apps.expect_row("00386", TIER="Tier 3", ML_RECOMMENDATION="Tier 2")
    hq_apps.expect_row("00398", TIER="", ML_RECOMMENDATION=EMDASH)
    hq_apps.expect_row("00377", TIER=EMDASH, ML_RECOMMENDATION=EMDASH)


def test_tc_053_grade_shows_a_dash_without_class(hq_apps):
    """TC-053 Grade shows a dash when the student has no class."""
    hq_apps.expect_row("00328", GRADE=EMDASH)
    hq_apps.expect_row("00381", GRADE=EMDASH)
    hq_apps.expect_row("00412", GRADE="P3")


def test_tc_054_ml_risk_and_status_show_only_allowed_values(hq_apps):
    """TC-054 ML risk and Status show only the allowed values."""
    for app_id, values in seed.APPS.items():
        hq_apps.expect_row(app_id, ML_RISK=values["risk"], STATUS=values["status"])
    risks = [hq_apps.cell_text(i, "ML RISK") for i in seed.ALL_IDS]
    assert risks.count("High") == 1 and risks.count("Low") == 1 and risks.count("Medium") == 7
    assert {hq_apps.cell_text(i, "STATUS") for i in seed.ALL_IDS} <= {"Pending", "Approved", "Rejected"}


def test_tc_055_list_is_sorted_by_submitted_newest_first(hq_apps):
    """TC-055 List is sorted by Submitted, newest first."""
    hq_apps.expect_ids(["00377", "00412", "00410", "00398", "00390", "00386", "00328", "00381", "00301"])
    for app_id, values in seed.APPS.items():
        hq_apps.expect_row(app_id, SUBMITTED=values["submitted"])
    first = hq_apps.open("00377")
    assert any("17/10/2026" in t and "10:05" in t and e == "Submitted" for t, e in first.history())
    first.close()
    second = hq_apps.open("00412")
    assert any("17/10/2026" in t and "09:20" in t and e == "Submitted" for t, e in second.history())


def test_tc_056_footer_shows_row_range_and_paging_buttons(hq_apps):
    """TC-056 Footer shows the row range and paging buttons for one page."""
    assert hq_apps.footer_text() == "Showing 1–9 of 9"
    assert hq_apps.page_buttons() == ["‹ Previous", "1", "Next ›"]
    for name in ("Previous", "Next"):
        button = hq_apps.pager.filter(has_text=name)
        if button.is_enabled():
            button.click()
    assert hq_apps.footer_text() == "Showing 1–9 of 9"
    hq_apps.expect_ids(seed.ALL_IDS)


def test_tc_058_empty_result_shows_message_and_empty_footer(hq_apps):
    """TC-058 Empty result shows the message and an empty footer."""
    hq_apps.do_search("zzzz")
    hq_apps.expect_empty()
    expect(hq_apps.footer).to_contain_text("Showing 0–0 of 0")
