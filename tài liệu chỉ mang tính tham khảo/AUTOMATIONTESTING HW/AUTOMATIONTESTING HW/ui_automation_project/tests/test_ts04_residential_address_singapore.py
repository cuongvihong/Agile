"""TS-04: Residential Address, Singapore — official 186-test-case library.

Source of truth: TS04.xlsx at the workspace root, cross-checked against
FSD_Trainer_Account_Creation.docx §4.4.1 and docs/DEFECTS.md (BUG-07, BUG-09).

Unlike TS-01/TS-02, every one of these 25 official cases is recorded
"Passed" — including the two that confirm real defects (BLOCK-003/BUG-07,
FLOOR-004/BUG-09), because their own "Expected Result" text was written to
match the build's actual (defective) behavior rather than the FSD ideal.
So no test in this file is expected to fail; each asserts the real,
observed build behavior.
"""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data.test_data import TD_TRAINER_001, with_overrides, without_keys

pytestmark = pytest.mark.ts04


# ============================================================
# TS04-SG: Residential Type
# ============================================================

def test_tc_ts04_sg_001_default_singapore_selected(form_page):
    """SCN001 — Form freshly opened. Expected: Singapore selected by default."""
    assert form_page.is_radio_checked("Singapore")


# ============================================================
# TS04-COUNTRY: Country/Region
# ============================================================

def test_tc_ts04_country_001_country_disabled(form_page):
    """SCN001 — Singapore selected. Expected: Country auto-set to Singapore, disabled."""
    expect(form_page.country_region_select).to_have_value("Singapore")
    expect(form_page.country_region_select).to_be_disabled()


# ============================================================
# TS04-PC: Postal Code
# ============================================================

def test_tc_ts04_pc_001_valid_postal_code(form_page):
    """SCN001 — "120047". Expected: postal code accepted."""
    data = with_overrides(TD_TRAINER_001, postal_code="120047")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("postalCode")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts04_pc_002_empty_postal_code(form_page):
    """SCN002 — Blank. Expected: validation message displayed."""
    data = with_overrides(TD_TRAINER_001, postal_code="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("postalCode")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts04_pc_003_five_digits(form_page):
    """SCN003 — "12345" (5 digits). Expected: validation displayed (below the 6-digit rule)."""
    data = with_overrides(TD_TRAINER_001, postal_code="12345")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("postalCode")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts04_pc_004_six_digits(form_page):
    """SCN004 — "123456" (exactly 6 digits). Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, postal_code="123456")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("postalCode")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts04_pc_005_seven_digits(form_page):
    """SCN005 — "1234567" (7 digits). Expected: validation displayed (above the 6-digit rule)."""
    data = with_overrides(TD_TRAINER_001, postal_code="1234567")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("postalCode")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts04_pc_006_alphabet_characters(form_page):
    """SCN006 — "ABCDEF". Expected: validation displayed (numeric only)."""
    data = with_overrides(TD_TRAINER_001, postal_code="ABCDEF")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("postalCode")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ============================================================
# TS04-AUTO: Auto Population
# ============================================================

def test_tc_ts04_auto_001_known_postal_code(form_page):
    """SCN001 — "120047" (known code). Expected: Block/Street auto-populated."""
    form_page.set_postal_code("120047")
    expect(form_page.block_number_input).to_have_value("142")
    expect(form_page.street_name_input).to_have_value("Commonwealth Drive")


def test_tc_ts04_auto_002_unknown_postal_code(form_page):
    """SCN002 — "999999" (unknown code). Expected: no auto-population."""
    form_page.set_postal_code("999999")
    expect(form_page.block_number_input).to_have_value("")
    expect(form_page.street_name_input).to_have_value("")


def test_tc_ts04_auto_003_manual_override_retained(form_page):
    """SCN003 — Auto-populated Block Number is then manually edited.

    Expected: the user-modified value is retained (auto-fill only runs on
    the postal-code blur event, so a later explicit edit is never
    overwritten by it).
    """
    form_page.set_postal_code("120047")
    expect(form_page.block_number_input).to_have_value("142")  # auto-filled first
    form_page.set_block_number("999")
    data = with_overrides(
        TD_TRAINER_001, postal_code="120047", block_number="999"
    )
    # Re-fill the rest of the baseline (street/floor/unit already valid),
    # then Save, to reach a state where the Block Number's final value can
    # be checked post-submit.
    form_page.fill_form(without_keys(data, "postal_code"))
    form_page.submit()
    expect(form_page.block_number_input).to_have_value("999")
    expect(form_page.success_box).to_be_visible()


# ============================================================
# TS04-BLOCK: Block/Building Number
# ============================================================

def test_tc_ts04_block_001_empty_block_number(form_page):
    """SCN001 — Blank. Expected: validation message displayed."""
    data = with_overrides(TD_TRAINER_001, block_number="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("blockNumber")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts04_block_002_nine_characters(form_page):
    """SCN002 — 9 characters (the build's own maxlength). Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, block_number="123456789")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("blockNumber")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts04_block_003_ten_characters(form_page):
    """SCN003 — attempt 10 characters. Confirms BUG-07.

    FSD §4.4.1 states Block/Building Number is String/10, but the build's
    HTML `maxlength="9"` truncates entry one character short. This test's
    own official Expected Result already matches that real behavior
    ("Build restricts entry to 9 characters"), so it is expected to PASS —
    it documents/confirms BUG-07, it does not assert the FSD ideal.
    """
    data = with_overrides(TD_TRAINER_001, block_number="1234567890")
    form_page.fill_form(data)
    actual_value = form_page.block_number_input.input_value()
    assert len(actual_value) == 9, (
        f"BUG-07 evidence: expected the build's maxlength=9 to truncate "
        f"entry, got {len(actual_value)} chars: {actual_value!r}"
    )


# ============================================================
# TS04-STREET: Street Name
# ============================================================

def test_tc_ts04_street_001_empty_street_name(form_page):
    """SCN001 — Blank. Expected: validation displayed."""
    data = with_overrides(TD_TRAINER_001, street_name="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("streetName")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ============================================================
# TS04-FLOOR: Floor Number
# ============================================================

def test_tc_ts04_floor_001_empty_floor_number(form_page):
    """SCN001 — Blank, checkbox unchecked. Expected: validation displayed."""
    data = with_overrides(TD_TRAINER_001, floor_number="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts04_floor_002_five_digits(form_page):
    """SCN002 — "12345" (5 digits, the build's own maxlength). Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, floor_number="12345")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts04_floor_003_six_digits(form_page):
    """SCN003 — 6 digits. Expected: validation displayed (above the 5-char limit).

    `floorNumber` has HTML `maxlength="5"`, which `.fill()` respects just
    like real typing — silently capping keyboard entry at 5 digits (a
    valid value, which would otherwise be wrongly accepted). Uses
    `set_raw_value()` to inject the full 6-digit value directly, so the
    Save-time regex (`/^\\d{1,5}$/`, anchored) is the thing actually
    exercised, matching this TC's own note about a pasted/injected value.
    """
    data = without_keys(TD_TRAINER_001, "floor_number")
    form_page.fill_form(data)
    form_page.set_raw_value(form_page.floor_number_input, "123456")
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts04_floor_004_alpha_numeric_floor(form_page):
    """SCN004 — "B1". Confirms BUG-09.

    FSD §4.4.1 states Floor Number is String/5 with no character-type
    restriction, but the build's Save-time regex (`/^\\d{1,5}$/`) accepts
    digits only. This TC's official Expected Result already matches that
    real behavior ("B1" rejected), so it is expected to PASS — it
    documents/confirms BUG-09, it does not assert the FSD ideal.
    """
    data = with_overrides(TD_TRAINER_001, floor_number="B1")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ============================================================
# TS04-UNIT: Unit Number
# ============================================================

def test_tc_ts04_unit_001_empty_unit_number(form_page):
    """SCN001 — Blank, checkbox unchecked. Expected: validation displayed."""
    data = with_overrides(TD_TRAINER_001, unit_number="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts04_unit_002_nine_digits(form_page):
    """SCN002 — 9 digits (the build's own maxlength). Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, unit_number="123456789")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


# ============================================================
# TS04-CHECK: Floor/Unit Not Applicable
# ============================================================

def test_tc_ts04_check_001_checkbox_checked_disables_fields(form_page):
    """SCN001 — Tick the checkbox. Expected: Floor and Unit become disabled."""
    data = without_keys(TD_TRAINER_001, "floor_number", "unit_number")
    form_page.fill_form(data)
    form_page.set_floor_not_applicable(True)
    expect(form_page.floor_number_input).to_be_disabled()
    expect(form_page.unit_number_input).to_be_disabled()


def test_tc_ts04_check_002_checkbox_checked_save_allowed(form_page):
    """SCN002 — Checkbox checked, Floor/Unit left empty. Expected: Save allowed."""
    data = with_overrides(
        TD_TRAINER_001, floor_number="", unit_number="", floor_not_applicable=True
    )
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts04_check_003_checkbox_unchecked_fields_mandatory_again(form_page):
    """SCN003 — Checkbox checked then unticked, Floor/Unit still empty.
    Expected: Floor and Unit become mandatory again."""
    data = without_keys(TD_TRAINER_001, "floor_number", "unit_number")
    form_page.fill_form(data)
    form_page.set_floor_not_applicable(True)
    form_page.set_floor_not_applicable(False)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ============================================================
# TS04-STATE: Singapore Address State Transition (Finding F09)
# ============================================================

def test_tc_ts04_state_001_singapore_to_non_singapore(form_page):
    """SCN001 — Complete a valid Singapore address, then switch to
    Non-Singapore. Validates Finding F09 (undefined retention behavior).

    Observed/documented behavior: the AUT hides the Singapore-only fields
    via CSS rather than clearing their values, so the previously entered
    Block Number is still present in the DOM (though not visible or
    submitted) after switching. This is the actual, empirically confirmed
    answer to F09 for this field, not an assumption.
    """
    data = with_overrides(TD_TRAINER_001, block_number="120", street_name="Bukit Merah Central")
    form_page.fill_form(data)
    expect(form_page.block_number_input).to_have_value("120")

    form_page.select_residential_type("Non-Singapore")

    expect(form_page.block_number_input).to_be_hidden()
    assert form_page.block_number_input.input_value() == "120", (
        "F09 evidence: Block Number's value is retained in the DOM after "
        "switching to Non-Singapore, even though the field is hidden"
    )
