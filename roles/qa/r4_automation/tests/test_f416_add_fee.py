"""F4.16 Add fee to a published scheme (TC-231 to TC-241). Source: FS F4 v1.3 section 6.6 and 7.4.
TC-235, TC-239 and TC-240 need the F4 build. TC-231 builds its own Draft row with the wizard (SEED-R4-N18)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data import ui_text as T
from data.ui_text import MIDDOT
from pages.dialogs import AddFeeDialog

pytestmark = pytest.mark.f416

EXISTING_2026 = ["SCHOOL FEE", "MISCELLANEOUS FEE", "SCHOOL TRANSPORT FEE", "SCHOOL MEAL FEE"]


def open_add_fee(schemes, name: str, index: int = 0) -> AddFeeDialog:
    schemes.action(name, "Add fee", index=index).click()
    dialog = AddFeeDialog(schemes.page)
    dialog.expect_open()
    return dialog


def test_tc_231_add_fee_is_offered_on_active_and_upcoming_schemes_only(hq_schemes):
    """TC-231 Add fee is offered on Active and Upcoming schemes only (the Draft row is built with the wizard)."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Draft 2028")
    wizard.save_draft()
    expect(hq_schemes.heading).to_be_visible()
    assert "Add fee" in hq_schemes.actions("MOEFAS 2027")
    assert "Add fee" in hq_schemes.actions("MOEFAS 2026")
    assert hq_schemes.actions("MOEFAS 2025") == ["View"]
    assert hq_schemes.actions("QA Draft 2028") == ["Edit"]


def test_tc_232_add_fee_dialog_lists_missing_components_and_shows_the_others_read_only(hq_schemes):
    """TC-232 Add fee dialog lists only components not yet in the scheme and shows the others read only."""
    dialog = open_add_fee(hq_schemes, "MOEFAS 2026")
    expect(dialog.title).to_have_text("Add fee components")
    expect(dialog.subtitle).to_have_text(f"FUNCTION 4 {MIDDOT} MOEFAS 2026 {MIDDOT} Active")
    expect(dialog.blue_note).to_be_visible()
    assert dialog.component_options() == ["Enrichment Programme Fee", "Educational Excursion Fee"]
    assert dialog.column_names()[1:] == EXISTING_2026
    expect(dialog.table.locator("input")).to_have_count(0)
    expect(dialog.remove_buttons).to_have_count(0)
    expect(dialog.add_button).to_be_disabled()


def test_tc_233_choosing_a_component_adds_an_editable_column_that_can_be_removed(hq_schemes):
    """TC-233 Choosing a component adds an editable column that can be removed."""
    dialog = open_add_fee(hq_schemes, "MOEFAS 2026")
    dialog.add_component("Enrichment Programme Fee")
    assert dialog.column_names()[-1] == "ENRICHMENT PROGRAMME FEE"
    for level in ("Primary", "Secondary", "Pre-University"):
        expect(dialog.cell_input(level)).to_have_value("0")
    expect(dialog.table.locator(".cell-edit span").first).to_have_text("%")
    expect(dialog.add_button).to_be_enabled()
    dialog.remove_buttons.click()
    assert dialog.column_names()[1:] == EXISTING_2026
    expect(dialog.add_button).to_be_disabled()


@pytest.mark.parametrize("value", ["101", "-1", "100.5", ""])
def test_tc_234_add_to_scheme_stays_disabled_for_invalid_new_cells(hq_schemes, value):
    """TC-234 Add to scheme stays disabled for invalid new cells (percentage)."""
    dialog = open_add_fee(hq_schemes, "MOEFAS 2026")
    dialog.add_component("Enrichment Programme Fee")
    dialog.cell_input("Primary").fill(value)
    expect(dialog.errors.filter(has_text="Enter 0–100 % for every new cell.")).to_be_visible()
    expect(dialog.add_button).to_be_disabled()


@pytest.mark.parametrize("value", ["100", "0"])
def test_tc_234_the_limits_0_and_100_are_accepted(hq_schemes, value):
    """TC-234 (limits) 100 and 0 are accepted."""
    dialog = open_add_fee(hq_schemes, "MOEFAS 2026")
    dialog.add_component("Enrichment Programme Fee")
    dialog.cell_input("Primary").fill(value)
    expect(dialog.add_button).to_be_enabled()
    expect(dialog.errors).to_have_count(0)


def add_enrichment_fee(hq, schemes) -> None:
    dialog = open_add_fee(schemes, "MOEFAS 2026")
    dialog.add_component("Enrichment Programme Fee")
    for level, value in (("Primary", "100"), ("Secondary", "70"), ("Pre-University", "50")):
        dialog.cell_input(level).fill(value)
    dialog.add_button.click()
    dialog.expect_closed()
    hq.expect_toast(T.TOAST_FEES_ADDED)


def test_tc_236_add_to_scheme_saves_the_new_component_and_shows_the_toast(hq, hq_schemes):
    """TC-236 Add to scheme saves the new component and shows the toast."""
    add_enrichment_fee(hq, hq_schemes)
    view = hq_schemes.open_view("MOEFAS 2026")
    heads = [h.strip() for h in view.table.locator("thead th").all_inner_texts()]
    assert heads[-1] == "ENRICHMENT PROGRAMME FEE"
    assert heads[1:-1] == EXISTING_2026
    for level, value in (("Primary", "100%"), ("Secondary", "70%"), ("Pre-University", "50%")):
        row = view.table.locator("tbody tr").filter(has_text=level)
        assert [t.strip() for t in row.locator("td").all_inner_texts()] == [level] + [value] * 5


@pytest.mark.draft
def test_tc_237_the_addition_is_recorded_with_the_date_and_the_user(hq, hq_schemes):
    """TC-237 The addition is recorded with the date and the user in the Audit log. ASM-R4-21."""
    add_enrichment_fee(hq, hq_schemes)
    hq.nav_button("Audit log").click()
    for text in ("Mei Lin Tan (MOE HQ)", "Scheme fee components added",
                 f"MOEFAS 2026 {MIDDOT} Enrichment Programme Fee"):
        expect(hq.main.get_by_text(text).first).to_be_visible()


def test_tc_238_existing_components_cannot_be_changed_after_the_addition(hq, hq_schemes):
    """TC-238 Existing components cannot be changed after the addition."""
    add_enrichment_fee(hq, hq_schemes)
    dialog = open_add_fee(hq_schemes, "MOEFAS 2026")
    assert dialog.column_names()[1:] == EXISTING_2026 + ["ENRICHMENT PROGRAMME FEE"]
    expect(dialog.table.locator("input")).to_have_count(0)
    expect(dialog.remove_buttons).to_have_count(0)
    assert dialog.component_options() == ["Educational Excursion Fee"]


def test_tc_241_add_fee_works_the_same_on_an_sbfas_scheme(bvp, bvp_schemes):
    """TC-241 Add fee works the same on an SBFAS scheme (Tier 1 of 2027)."""
    dialog = open_add_fee(bvp_schemes, "Tier 1", index=0)
    options = dialog.component_options()
    assert options, "the dialog offers at least one missing component"
    dialog.add_component(options[0])
    rows = dialog.level_names()
    assert rows == ["P1", "P2", "P3", "P4", "P5", "P6"]
    for grade in rows:
        dialog.cell_input(grade).fill("50")
    dialog.add_button.click()
    dialog.expect_closed()
    bvp.expect_toast(T.TOAST_FEES_ADDED)
