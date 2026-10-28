"""F4.14 New scheme wizard (TC-181 to TC-213). Source: FS F4 v1.3 section 6.2 to 6.4 and 7.2.
TC-195 and TC-199 are not in the prototype case list. TC-188 and TC-193 to TC-194 depend on open assumptions."""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data import ui_text as T
from data.ui_text import ENDASH
from pages.schemes_page import SchemesPage, SchemeWizard

pytestmark = pytest.mark.f414

BLUE_DEFAULT = ("Form open 01/08/2027 " + ENDASH + " 31/12/2027 → the system ranks and assesses all applications "
                "after 31/12/2027 → subsidy applies from 01/01/2028.")
COMPONENTS = ["School fee", "Miscellaneous fee", "Enrichment Programme Fee", "Educational Excursion Fee",
              "School Transport Fee", "School Meal Fee"]


def no_type_or_level(wizard: SchemeWizard) -> None:
    for absent in ("Scheme type", "Level"):
        expect(wizard.main.locator("label").filter(has_text=re.compile(r"^" + absent))).to_have_count(0)


# ----------------------------------------------------------------- step 1
def test_tc_181_step_1_shows_the_fields_the_defaults_and_the_blue_note(hq_schemes):
    """TC-181 Step 1 shows the fields, the defaults and the blue note."""
    wizard = hq_schemes.new_scheme()
    assert wizard.step_label(1).startswith("1 General")
    assert wizard.step_label(2).startswith("2 Eligibility")
    assert wizard.step_label(3).startswith("3 Subsidy")
    for label, required in (("Scheme name", True), ("Form opens", True), ("Form closes", True),
                            ("Effective from", True), ("Effective to", False)):
        field = wizard.field(label)
        expect(field).to_have_count(1)
        if required:
            expect(field).to_contain_text("*")
    expect(wizard.name_input).to_have_attribute("placeholder", "e.g. MOEFAS 2028")
    expect(wizard.message("Must be after Form closes.")).to_be_visible()
    expect(wizard.message("No end date")).to_be_visible()
    no_type_or_level(wizard)
    expect(wizard.date_text("Form opens")).to_have_value("01/08/2027")
    expect(wizard.date_text("Form closes")).to_have_value("31/12/2027")
    expect(wizard.date_text("Effective from")).to_have_value("01/01/2028")
    expect(wizard.date_text("Effective to")).to_have_value("")
    expect(wizard.blue_note).to_have_text(BLUE_DEFAULT)


def test_tc_182_the_blue_note_follows_the_dates(hq_schemes):
    """TC-182 The blue note follows the dates."""
    wizard = hq_schemes.new_scheme()
    wizard.set_date("Form closes", "30/11/2027")
    wizard.set_date("Effective from", "01/12/2027")
    expect(wizard.blue_note).to_have_text(
        "Form open 01/08/2027 " + ENDASH + " 30/11/2027 → the system ranks and assesses all applications "
        "after 30/11/2027 → subsidy applies from 01/12/2027.")


def test_tc_183_scheme_name_is_required(hq, hq_schemes):
    """TC-183 Scheme name is required and the draft is not saved without it."""
    wizard = hq_schemes.new_scheme()
    expect(wizard.error(T.ERR_NAME)).to_be_visible()
    wizard.save_draft()
    expect(wizard.heading).to_be_visible()
    expect(hq.toast).to_have_count(0)


def test_tc_184_form_opens_and_form_closes_are_required(hq_schemes):
    """TC-184 Form opens and Form closes are required."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Dates")
    message = wizard.message("Enter Form opens and Form closes.")
    expect(message).to_have_count(0)
    wizard.set_date("Form opens", "")
    expect(message).to_be_visible()
    wizard.set_date("Form opens", "01/08/2027")
    expect(message).to_have_count(0)
    wizard.set_date("Form closes", "")
    expect(message).to_be_visible()


def test_tc_185_form_closes_may_equal_form_opens_but_not_be_earlier(hq_schemes):
    """TC-185 Form closes may equal Form opens but not be earlier."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Dates")
    message = wizard.message("Form closes must be on or after Form opens.")
    wizard.set_date("Form closes", "31/07/2027")
    expect(message).to_be_visible()
    for value in ("01/08/2027", "02/08/2027"):
        wizard.set_date("Form closes", value)
        expect(message).to_have_count(0)


def test_tc_186_effective_from_must_be_after_form_closes(hq_schemes):
    """TC-186 Effective from must be after Form closes."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Dates")
    message = wizard.message("Effective from must be after Form closes (applications are assessed after the form closes).")
    for value in ("30/12/2027", "31/12/2027"):
        wizard.set_date("Effective from", value)
        expect(message).to_be_visible()
    wizard.set_date("Effective from", "01/01/2028")
    expect(message).to_have_count(0)


def test_tc_187_effective_to_must_be_after_effective_from_and_may_be_empty(hq_schemes):
    """TC-187 Effective to must be after Effective from and may be empty."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Dates")
    message = wizard.message("Effective to must be after Effective from.")
    expect(message).to_have_count(0)
    expect(wizard.message("No end date")).to_be_visible()
    for value in ("31/12/2027", "01/01/2028"):
        wizard.set_date("Effective to", value)
        expect(message).to_be_visible()
    wizard.set_date("Effective to", "02/01/2028")
    expect(message).to_have_count(0)


@pytest.mark.draft
@pytest.mark.known_defect(reason="TC-188: the prototype ignores a typed value that is not a date and shows no message (ASM-R4-09)")
@pytest.mark.parametrize("value", ["32/13/2027", "abc", "1/8/2027", "2027-08-02"])
def test_tc_188_text_that_is_not_a_real_date_is_rejected(hq_schemes, value):
    """TC-188 Text that is not a real date is rejected. ASM-R4-09."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Dates")
    wizard.set_date("Form opens", value)
    expect(wizard.message("Enter a valid date (DD/MM/YYYY).")).to_be_visible()


def test_tc_189_messages_show_again_at_view_and_the_steps_get_a_warning_mark(hq_schemes):
    """TC-189 Messages show again at View and the step gets a warning mark."""
    wizard = hq_schemes.new_scheme()
    wizard.set_date("Form closes", "31/07/2027")          # earlier than Form opens
    wizard.next_button.click()
    wizard.next_button.click()
    wizard.view_button.click()
    assert wizard.has_warning(1) and wizard.has_warning(3)
    expect(wizard.page.get_by_text(re.compile(r"To publish, fix \d+ item\(s\) \(steps marked " + T.WARN + r"\)\."))
           ).to_be_visible()
    wizard.go_step(1)
    expect(wizard.error(T.ERR_NAME)).to_be_visible()


# ----------------------------------------------------------------- step 2
def test_tc_190_step_2_shows_nationalities_bands_and_match_rule_with_defaults(hq_schemes):
    """TC-190 Step 2 shows nationalities, bands and match rule with defaults."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Eligibility")
    wizard.go_step(2)
    expect(wizard.nationality("Singapore Citizen")).to_be_checked()
    for other in ("Singapore PR", f"International {ENDASH} ASEAN", f"International {ENDASH} non-ASEAN"):
        expect(wizard.nationality(other)).not_to_be_checked()
    expect(wizard.ghi_use).not_to_be_checked()
    expect(wizard.pci_use).to_be_checked()
    expect(wizard.pci_from).to_have_value("0")
    expect(wizard.pci_to).to_have_value("1100")
    expect(wizard.message("Empty = no upper limit")).to_have_count(2)
    options = [t.strip() for t in wizard.match_rule.locator("option").all_inner_texts()]
    assert options == ["Any selected income band is met", "All selected income bands are met"]


def test_tc_191_at_least_one_nationality_is_required(hq_schemes):
    """TC-191 At least one nationality is required."""
    wizard = hq_schemes.new_scheme()
    wizard.go_step(2)
    wizard.nationality("Singapore Citizen").uncheck()
    expect(wizard.error(T.ERR_NATIONALITY)).to_be_visible()


def test_tc_192_at_least_one_income_band_is_required(hq_schemes):
    """TC-192 At least one income band is required."""
    wizard = hq_schemes.new_scheme()
    wizard.go_step(2)
    wizard.pci_use.uncheck()
    expect(wizard.error(T.ERR_BAND)).to_be_visible()


@pytest.mark.draft
def test_tc_193_a_band_needs_from_and_to_may_be_empty(hq_schemes):
    """TC-193 A band needs From and To may be empty for no upper limit. ASM-R4-24."""
    wizard = hq_schemes.new_scheme()
    wizard.go_step(2)
    wizard.pci_to.fill("")
    expect(wizard.errors).to_have_count(0)
    wizard.pci_to.fill("1100")
    wizard.pci_from.fill("")
    expect(wizard.errors.first).to_be_visible()


@pytest.mark.draft
def test_tc_194_from_greater_than_to_is_not_allowed(hq_schemes):
    """TC-194 From greater than To is not allowed and Publish is blocked. ASM-R4-20."""
    wizard = hq_schemes.new_scheme()
    wizard.fill_valid_moefas("QA Band")
    wizard.go_step(2)
    wizard.pci_from.fill("2000")
    wizard.pci_to.fill("1000")
    expect(wizard.errors.first).to_be_visible()
    assert wizard.has_warning(2)
    wizard.go_step(3)
    wizard.view_button.click()
    expect(wizard.page.get_by_role("button", name="Publish", exact=True)).to_have_count(0)


# ----------------------------------------------------------------- step 3
def test_tc_196_moefas_step_3_shows_the_three_levels_and_the_value_type(hq_schemes):
    """TC-196 MOEFAS step 3 shows the three levels and the value type."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Subsidy")
    wizard.go_step(3)
    options = [t.strip() for t in wizard.value_type.locator("option").all_inner_texts()]
    assert options == ["Percentage of fee", "Fixed amount (S$)"]
    expect(wizard.value_type.locator("option:checked")).to_have_text("Percentage of fee")
    assert wizard.level_names() == ["Primary", "Secondary", "Pre-University"]
    expect(wizard.message("Select a fee component above to add it.")).to_be_visible()
    expect(wizard.error("Add at least one fee component.")).to_be_visible()


def test_tc_197_choosing_a_fee_component_adds_a_column_with_zero_in_every_row(hq_schemes):
    """TC-197 Choosing a fee component adds a column at once with 0 in every row."""
    wizard = hq_schemes.new_scheme()
    wizard.go_step(3)
    options = [t.strip() for t in wizard.component_select.locator("option").all_inner_texts() if t.strip()]
    assert [o for o in options if o != "Select to add"] == COMPONENTS
    wizard.add_component("School fee")
    assert wizard.component_columns() == ["SCHOOL FEE"]
    for level in ("Primary", "Secondary", "Pre-University"):
        expect(wizard.cell_input(level, 0)).to_have_value("0")
    options_after = [t.strip() for t in wizard.component_select.locator("option").all_inner_texts()]
    assert "School fee" not in options_after
    expect(wizard.error("Add at least one fee component.")).to_have_count(0)


def test_tc_198_components_can_be_added_and_removed_with_the_cross(hq_schemes):
    """TC-198 Several components can be added and a column can be removed with the cross."""
    wizard = hq_schemes.new_scheme()
    wizard.go_step(3)
    wizard.add_component("School fee")
    wizard.add_component("School Meal Fee")
    assert wizard.component_columns() == ["SCHOOL FEE", "SCHOOL MEAL FEE"]
    wizard.remove_component("School fee")
    assert wizard.component_columns() == ["SCHOOL MEAL FEE"]
    assert "School fee" in [t.strip() for t in wizard.component_select.locator("option").all_inner_texts()]
    wizard.remove_component("School Meal Fee")
    expect(wizard.error("Add at least one fee component.")).to_be_visible()


def test_tc_200_changing_the_value_type_changes_the_unit_of_the_cells(hq_schemes):
    """TC-200 Changing the value type changes the unit of the cells and the rule that checks them."""
    wizard = hq_schemes.new_scheme()
    wizard.go_step(3)
    wizard.add_component("School fee")
    for level, value in (("Primary", "100"), ("Secondary", "70"), ("Pre-University", "50")):
        wizard.cell_input(level, 0).fill(value)
        expect(wizard.unit(level, 0)).to_have_text("%")
    wizard.value_type.select_option(label="Fixed amount (S$)")
    for level in ("Primary", "Secondary", "Pre-University"):
        expect(wizard.unit(level, 0)).to_have_text("S$")
    wizard.cell_input("Primary", 0).fill("120")
    expect(wizard.valid_note).to_have_text("All amounts are valid.")


def test_tc_201_sbfas_step_3_shows_one_row_per_grade_of_the_school(bvp, bvp_schemes):
    """TC-201 SBFAS step 3 shows one row per grade the school offers."""
    wizard = bvp_schemes.new_scheme()
    wizard.name_input.fill("Tier 4")
    wizard.go_step(3)
    assert wizard.level_names() == ["P1", "P2", "P3", "P4", "P5", "P6"]
    wizard.cancel_button.click()
    bvp.log_out()
    bvp.sign_in_school("MRS-0012")
    bvp.go("SBFAS schemes")
    meridian = SchemesPage(bvp.page, "SBFAS schemes").new_scheme()
    meridian.name_input.fill("Tier 4")
    meridian.go_step(3)
    assert meridian.level_names() == ["S1", "S2", "S3", "S4"]


def test_tc_202_sbfas_component_columns_behave_like_moefas(bvp_schemes):
    """TC-202 SBFAS component columns behave like MOEFAS."""
    wizard = bvp_schemes.new_scheme()
    wizard.go_step(3)
    wizard.add_component("School fee")
    assert wizard.component_columns() == ["SCHOOL FEE"]
    for grade in ("P1", "P2", "P3", "P4", "P5", "P6"):
        expect(wizard.cell_input(grade, 0)).to_have_value("0")


def test_tc_203_sbfas_step_1_uses_a_tier_name_and_the_same_dates(bvp_schemes):
    """TC-203 SBFAS step 1 uses a tier name and the same dates as MOEFAS."""
    wizard = bvp_schemes.new_scheme()
    for label in ("Form opens", "Form closes", "Effective from", "Effective to"):
        expect(wizard.date_text(label)).to_be_visible()
    expect(wizard.blue_note).to_contain_text("the school reviews the applications")
    no_type_or_level(wizard)


def test_tc_204_percentage_cells_accept_0_and_100(hq_schemes):
    """TC-204 Percentage cells accept 0 and 100."""
    wizard = hq_schemes.new_scheme()
    wizard.go_step(3)
    wizard.add_component("School fee")
    for value in ("0", "100"):
        wizard.cell_input("Primary", 0).fill(value)
        expect(wizard.valid_note).to_have_text("All amounts are valid.")


@pytest.mark.parametrize("value", ["-1", "101", ""])
def test_tc_205_percentage_cells_reject_values_below_0_above_100_and_empty(hq_schemes, value):
    """TC-205 Percentage cells reject values below 0 and above 100 and empty cells."""
    wizard = hq_schemes.new_scheme()
    wizard.go_step(3)
    wizard.add_component("School fee")
    wizard.cell_input("Primary", 0).fill(value)
    expect(wizard.error("Primary · School fee: enter 0" + ENDASH + "100 %.")).to_be_visible()
    assert wizard.has_warning(3)


@pytest.mark.draft
def test_tc_206_percentage_cells_accept_at_most_two_decimals(hq_schemes):
    """TC-206 Percentage cells accept at most two decimals. ASM-R4-12."""
    wizard = hq_schemes.new_scheme()
    wizard.go_step(3)
    wizard.add_component("School fee")
    wizard.cell_input("Primary", 0).fill("33.33")
    expect(wizard.valid_note).to_have_text("All amounts are valid.")
    wizard.cell_input("Primary", 0).fill("33.333")
    expect(wizard.error("Primary · School fee")).to_be_visible()


@pytest.mark.draft
def test_tc_207_fixed_amount_cells_accept_0_or_more_and_reject_negative_values(hq_schemes):
    """TC-207 Fixed amount cells accept 0 or more and reject negative values. ASM-R4-12."""
    wizard = hq_schemes.new_scheme()
    wizard.go_step(3)
    wizard.value_type.select_option(label="Fixed amount (S$)")
    wizard.add_component("School fee")
    for value in ("0", "120.50", "1000000"):
        wizard.cell_input("Primary", 0).fill(value)
        expect(wizard.valid_note).to_have_text("All amounts are valid.")
    wizard.cell_input("Primary", 0).fill("-1")
    expect(wizard.error("Primary · School fee: enter an amount of 0 or more.")).to_be_visible()


@pytest.mark.draft
def test_tc_208_an_empty_fixed_amount_cell_is_rejected(hq_schemes):
    """TC-208 An empty fixed amount cell is rejected. ASM-R4-12."""
    wizard = hq_schemes.new_scheme()
    wizard.go_step(3)
    wizard.value_type.select_option(label="Fixed amount (S$)")
    wizard.add_component("School fee")
    wizard.cell_input("Primary", 0).fill("")
    expect(wizard.error("Primary · School fee")).to_be_visible()
    assert wizard.has_warning(3)


# ------------------------------------------------------- steps and drafts
def test_tc_209_steps_open_in_any_order_and_keep_their_values(hq_schemes):
    """TC-209 Steps can be opened in any order and keep their values."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Test 2028")
    wizard.go_step(2)
    wizard.nationality("Singapore PR").check()
    wizard.go_step(3)
    wizard.add_component("School fee")
    wizard.go_step(1)
    expect(wizard.name_input).to_have_value("QA Test 2028")
    wizard.go_step(3)
    assert wizard.component_columns() == ["SCHOOL FEE"]
    wizard.go_step(2)
    expect(wizard.nationality("Singapore PR")).to_be_checked()
    wizard.next_button.click()
    assert wizard.component_columns() == ["SCHOOL FEE"]
    wizard.back_button.click()
    expect(wizard.nationality("Singapore PR")).to_be_checked()


def test_tc_210_save_draft_with_a_name_creates_a_draft_row(hq, hq_schemes):
    """TC-210 Save draft with a name creates a Draft row."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Draft 2028")
    wizard.save_draft()
    hq.expect_toast(T.TOAST_DRAFT)
    assert "QA Draft 2028" in hq_schemes.names()
    expect(hq_schemes.cell("QA Draft 2028", "STATUS")).to_have_text("Draft")
    assert hq_schemes.actions("QA Draft 2028") == ["Edit"]
    expect(hq_schemes.card_value("Draft")).to_have_text("1")


def test_tc_211_draft_without_a_name_is_not_saved(hq_schemes):
    """TC-211 Draft without a name is not saved."""
    wizard = hq_schemes.new_scheme()
    wizard.save_draft()
    expect(wizard.error(T.ERR_NAME)).to_be_visible()
    wizard.cancel_button.click()
    assert len(hq_schemes.names()) == 3
    expect(hq_schemes.card_value("Draft")).to_have_text("0")


def test_tc_212_edit_reopens_the_draft_with_the_saved_values(hq_schemes):
    """TC-212 Edit reopens the draft with the saved values and saving again updates the same row."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Draft 2028")
    wizard.set_date("Form closes", "30/11/2027")
    wizard.set_date("Effective from", "01/12/2027")
    wizard.save_draft()
    hq_schemes.action("QA Draft 2028", "Edit").click()
    reopened = SchemeWizard(hq_schemes.page)
    expect(reopened.name_input).to_have_value("QA Draft 2028")
    expect(reopened.date_text("Form closes")).to_have_value("30/11/2027")
    expect(reopened.date_text("Effective from")).to_have_value("01/12/2027")
    assert reopened.has_warning(3)
    reopened.save_draft()
    assert hq_schemes.names().count("QA Draft 2028") == 1
    expect(hq_schemes.card_value("Draft")).to_have_text("1")


def test_tc_213_discard_and_cancel_leave_the_wizard_without_saving(hq_schemes):
    """TC-213 Discard and Cancel leave the wizard without saving."""
    wizard = hq_schemes.new_scheme()
    wizard.name_input.fill("QA Not Saved")
    wizard.discard_button.click()
    expect(hq_schemes.heading).to_be_visible()
    second = hq_schemes.new_scheme()
    second.name_input.fill("QA Not Saved")
    second.cancel_button.click()
    expect(hq_schemes.heading).to_be_visible()
    assert hq_schemes.names() == ["MOEFAS 2027", "MOEFAS 2026", "MOEFAS 2025"]
    expect(hq_schemes.card_value("Draft")).to_have_text("0")
