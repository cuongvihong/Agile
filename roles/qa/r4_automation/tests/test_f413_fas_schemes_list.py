"""F4.13 FAS schemes list (TC-168 to TC-180). Source: FS F4 v1.3 section 6.1 and 7.1.
TC-175 and TC-176 need the F4 build. TC-178 builds its own Draft row with the wizard (SEED-R4-N18)."""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data.ui_text import MIDDOT
from pages.schemes_page import SchemesPage

pytestmark = pytest.mark.f413

HQ_SUBTITLE = ("View existing MOEFAS schemes and create a new one when changes are needed. One MOEFAS scheme covers "
               "all levels, it has no tiers. SBFAS schemes are configured by each school for itself.")
SCHOOL_SUBTITLE = ("Your school's own SBFAS schemes. Each scheme is one tier (e.g. Tier 1, Tier 2). View existing "
                   "schemes and create a new scheme when changes are needed.")
COLUMNS = ["SCHEME", "ELIGIBILITY", "APPLICATION FORM", "EFFECTIVE FROM", "EFFECTIVE TO", "STATUS", ""]


def test_tc_168_hq_sees_the_three_moefas_schemes_only(hq_schemes):
    """TC-168 MOE HQ sees the three MOEFAS schemes only."""
    assert hq_schemes.names() == ["MOEFAS 2027", "MOEFAS 2026", "MOEFAS 2025"]


def test_tc_169_school_admin_sees_the_own_sbfas_schemes_only(bvp, bvp_schemes):
    """TC-169 A School Admin sees the own SBFAS schemes only."""
    assert bvp_schemes.names() == ["Tier 1", "Tier 2", "Tier 3"] * 2
    bvp.log_out()
    bvp.sign_in_school("MRS-0012")
    bvp.go("SBFAS schemes")
    meridian = SchemesPage(bvp.page, "SBFAS schemes")
    assert not [n for n in meridian.names() if n.startswith("MOEFAS")]


def test_tc_170_page_subtitle_states_the_role_scope(hq, hq_schemes):
    """TC-170 The page subtitle states the role scope."""
    expect(hq_schemes.subtitle).to_have_text(HQ_SUBTITLE)
    hq.log_out()
    hq.sign_in_school("BVP-0012")
    hq.go("SBFAS schemes")
    expect(SchemesPage(hq.page, "SBFAS schemes").subtitle).to_have_text(SCHOOL_SUBTITLE)


def test_tc_171_scheme_cards_count_active_upcoming_closed_and_draft(hq_schemes):
    """TC-171 Scheme cards count Active, Upcoming, Closed and Draft."""
    for label, value in (("Active", "1"), ("Upcoming", "1"), ("Closed", "1"), ("Draft", "0")):
        expect(hq_schemes.card_value(label)).to_have_text(value)
    expect(hq_schemes.card_hint("Upcoming")).to_have_text("Published, not yet in effect")


def test_tc_172_columns_and_cells_of_the_moefas_scheme_list(hq_schemes):
    """TC-172 Table columns and cell contents of the MOEFAS scheme list (the date format is in the next test)."""
    assert hq_schemes.column_names() == COLUMNS
    cell = lambda column: hq_schemes.cell("MOEFAS 2027", column)          # noqa: E731
    expect(cell("SCHEME")).to_contain_text("MOEFAS 2027")
    expect(cell("SCHEME")).to_contain_text("Approved automatically")
    expect(cell("ELIGIBILITY")).to_have_text("Singapore Citizen " + MIDDOT + " GHI ≤ S$ 4,200.00 or PCI ≤ S$ 1,050.00")
    expect(cell("APPLICATION FORM")).to_contain_text("01/08/2026 – 31/12/2026")
    expect(cell("APPLICATION FORM")).to_contain_text("Open")
    expect(cell("APPLICATION FORM")).to_contain_text("3 waiting")
    expect(cell("EFFECTIVE TO")).to_have_text("No end date")
    expect(cell("STATUS")).to_have_text("Upcoming")


@pytest.mark.known_defect(reason="TC-265: the scheme list shows 1 Jan 2027, the FS format is DD/MM/YYYY")
def test_tc_172_effective_from_is_shown_as_dd_mm_yyyy(hq_schemes):
    """TC-172 (date part) Effective from 01/01/2027."""
    expect(hq_schemes.cell("MOEFAS 2027", "EFFECTIVE FROM")).to_have_text("01/01/2027")


def test_tc_173_sbfas_list_shows_approved_by_school_and_the_pci_band(bvp_schemes):
    """TC-173 SBFAS list shows Approved by school and the PCI band (Tier 2 of 2027 is the second row)."""
    cell = lambda column: bvp_schemes.cell("Tier 2", column, index=0)       # noqa: E731
    expect(cell("SCHEME")).to_contain_text("Approved by school")
    expect(cell("ELIGIBILITY")).to_have_text("Citizen and PR " + MIDDOT + " PCI S$ 601 – 1,000")
    expect(cell("APPLICATION FORM")).to_contain_text("01/08/2026 – 31/12/2026")
    expect(cell("APPLICATION FORM")).to_contain_text("Open")
    expect(cell("EFFECTIVE TO")).to_have_text("No end date")
    expect(cell("STATUS")).to_have_text("Upcoming")
    for word in ("waiting", "Assessed"):
        expect(cell("APPLICATION FORM")).not_to_contain_text(word)


def test_tc_174_sort_is_effective_from_newest_first_then_name(hq, hq_schemes):
    """TC-174 Sort is Effective from newest first, then name."""
    assert hq_schemes.names() == ["MOEFAS 2027", "MOEFAS 2026", "MOEFAS 2025"]
    hq.log_out()
    hq.sign_in_school("BVP-0012")
    hq.go("SBFAS schemes")
    school = SchemesPage(hq.page, "SBFAS schemes")
    assert school.names() == ["Tier 1", "Tier 2", "Tier 3", "Tier 1", "Tier 2", "Tier 3"]
    expect(school.cell("Tier 1", "STATUS", index=0)).to_have_text("Upcoming")
    expect(school.cell("Tier 1", "STATUS", index=1)).to_have_text("Active")


def test_tc_177_moefas_rows_show_waiting_count_or_assessed_date(hq_schemes):
    """TC-177 MOEFAS rows show the waiting count or the Assessed date."""
    form = lambda name: hq_schemes.cell(name, "APPLICATION FORM")          # noqa: E731
    expect(form("MOEFAS 2027")).to_contain_text("Open")
    expect(form("MOEFAS 2027")).to_contain_text("3 waiting")
    expect(form("MOEFAS 2026")).to_contain_text("Closed")
    expect(form("MOEFAS 2026")).to_contain_text("Assessed 01/01/2026")
    expect(form("MOEFAS 2025")).to_contain_text("Closed")
    expect(form("MOEFAS 2025")).to_contain_text("Assessed 01/01/2025")


def test_tc_178_actions_follow_the_scheme_status(hq_schemes):
    """TC-178 Actions follow the scheme status (the Draft row is created with the wizard, SEED-R4-N18)."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Draft 2028")
    wizard.save_draft()
    expect(hq_schemes.heading).to_be_visible()
    assert hq_schemes.actions("MOEFAS 2027") == ["View", "Add fee", "Close form now (demo)"]
    assert hq_schemes.actions("MOEFAS 2026") == ["View", "Add fee"]
    assert hq_schemes.actions("MOEFAS 2025") == ["View"]
    assert hq_schemes.actions("QA Draft 2028") == ["Edit"]


def test_tc_179_close_form_now_shows_only_for_hq_on_an_open_moefas_form(hq, hq_schemes):
    """TC-179 Close form now (demo) shows only for HQ on a MOEFAS scheme with the form Open."""
    buttons = [n for n in hq_schemes.names() if hq_schemes.actions(n).count("Close form now (demo)")]
    assert buttons == ["MOEFAS 2027"]
    hq.log_out()
    hq.sign_in_school("BVP-0012")
    hq.go("SBFAS schemes")
    school = SchemesPage(hq.page, "SBFAS schemes")
    expect(school.rows.get_by_role("button", name="Close form now (demo)")).to_have_count(0)


def test_tc_180_new_scheme_has_no_type_or_level_field(hq, hq_schemes):
    """TC-180 New scheme creates MOEFAS for HQ and SBFAS for a school with no type choice."""
    wizard = hq_schemes.new_scheme()
    expect(wizard.message("One MOEFAS scheme covers Primary, Secondary and Pre-University.")).to_be_visible()
    for absent in ("Scheme type", "Level"):
        expect(wizard.main.locator("label").filter(has_text=re.compile(r"^" + absent))).to_have_count(0)
    wizard.cancel_button.first.click()
    hq.log_out()
    hq.sign_in_school("BVP-0012")
    hq.go("SBFAS schemes")
    school_wizard = SchemesPage(hq.page, "SBFAS schemes").new_scheme()
    expect(school_wizard.name_input).to_have_attribute("placeholder", re.compile(r"Tier"))
    for absent in ("Scheme type", "Level"):
        expect(school_wizard.main.locator("label").filter(has_text=re.compile(r"^" + absent))).to_have_count(0)

