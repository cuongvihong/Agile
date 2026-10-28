"""TS-05: Residential Address, Non-Singapore — official 186-test-case library.

Source of truth: TS05.xlsx at the workspace root, cross-checked against
FSD_Trainer_Account_Creation.docx §4.4.2 and docs/DEFECTS.md (BUG-11, BUG-12).

2 of the 23 official cases are recorded Failed (NSG-003/BUG-11,
PC-004/BUG-12) — both asserted here per the FSD, so both are EXPECTED to
fail for real, same methodology as TS-01/TS-02's known-defect tests.
"""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data.test_data import TD_TRAINER_002, with_overrides, without_keys

pytestmark = pytest.mark.ts05


# ============================================================
# TS05-NSG: Residential Type / Country Region
# ============================================================

def test_tc_ts05_nsg_001_switch_to_non_singapore(form_page):
    """SCN001 — Select Non-Singapore. Expected: Non-Singapore fields visible."""
    form_page.select_residential_type("Non-Singapore")
    expect(form_page.address1_input).to_be_visible()
    expect(form_page.city_input).to_be_visible()
    expect(form_page.block_number_input).to_be_hidden()


def test_tc_ts05_nsg_002_country_field_enabled(form_page):
    """SCN002 — Non-Singapore selected. Expected: Country/Region dropdown editable."""
    form_page.select_residential_type("Non-Singapore")
    expect(form_page.country_region_select).to_be_enabled()


@pytest.mark.known_defect
def test_tc_ts05_nsg_003_singapore_not_allowed(form_page):
    """SCN003 — Attempt to select "Singapore" while in Non-Singapore mode.

    FSD §4.4.2: "Country/Region must not allow Singapore when Non-Singapore
    is selected." Official Actual Result: FAILED (BUG-11) — the build keeps
    the "Singapore" option present and enabled; it is only rejected later
    at Save time, not made unavailable in the dropdown itself.

    This test asserts the FSD-required behavior (the option must be
    unavailable, e.g. disabled), so it is EXPECTED TO FAIL — documented
    evidence for BUG-11.
    """
    form_page.select_residential_type("Non-Singapore")
    singapore_option = form_page.country_region_select.locator(
        "option", has_text="Singapore"
    )
    expect(singapore_option).to_be_disabled()


def test_tc_ts05_nsg_004_valid_country_selected(form_page):
    """SCN004 — Select Malaysia. Expected: country saved successfully."""
    form_page.select_residential_type("Non-Singapore")
    form_page.select_country_region("Malaysia")
    expect(form_page.country_region_select).to_have_value("Malaysia")


# ============================================================
# TS05-PC: Postal Code (optional in Non-Singapore mode)
# ============================================================

def test_tc_ts05_pc_001_empty_postal_code(form_page):
    """SCN001 — Blank. Expected: account can be saved (optional here)."""
    data = without_keys(TD_TRAINER_002, "postal_code")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("postalCode")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts05_pc_002_valid_postal_code(form_page):
    """SCN002 — "75000". Expected: value accepted."""
    data = with_overrides(TD_TRAINER_002, postal_code="75000")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("postalCode")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts05_pc_003_maximum_length_20(form_page):
    """SCN003 — exactly 20 characters. Expected: accepted."""
    value = "1" * 20
    data = with_overrides(TD_TRAINER_002, postal_code=value)
    form_page.fill_form(data)
    expect(form_page.postal_code_input).to_have_value(value)
    form_page.submit()
    expect(form_page.error_locator("postalCode")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


@pytest.mark.known_defect
def test_tc_ts05_pc_004_above_maximum_length_21(form_page):
    """SCN004 — 21 characters attempted. FSD §4.4.2: Non-Singapore Postal
    Code is String/20.

    Official Actual Result: FAILED (BUG-12) — the build applies no length
    restriction to this field outside Singapore mode (only HTML
    `maxlength="255"` applies), so the full 21-character value is accepted.

    This test asserts the FSD-required cap (<=20 chars), so it is EXPECTED
    TO FAIL against the current build — documented evidence for BUG-12.
    """
    value = "1" * 21
    data = with_overrides(TD_TRAINER_002, postal_code=value)
    form_page.fill_form(data)
    actual_value = form_page.postal_code_input.input_value()
    assert len(actual_value) <= 20, (
        f"BUG-12: expected Non-Singapore Postal Code capped at 20 chars "
        f"per FSD §4.4.2, got {len(actual_value)} chars accepted"
    )


# ============================================================
# TS05-ADDR1: Address Line 1
# ============================================================

def test_tc_ts05_addr1_001_valid_address_line_1(form_page):
    """SCN001 — "123 Jalan Ampang". Expected: accepted."""
    data = with_overrides(TD_TRAINER_002, address1="123 Jalan Ampang")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("address1")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts05_addr1_002_blank_address_line_1(form_page):
    """SCN002 — Blank. Expected: validation message displayed."""
    data = with_overrides(TD_TRAINER_002, address1="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("address1")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts05_addr1_003_spaces_only(form_page):
    """SCN003 — Spaces only. Expected: treated as empty."""
    data = with_overrides(TD_TRAINER_002, address1="   ")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("address1")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts05_addr1_004_maximum_length_255(form_page):
    """SCN004 — exactly 255 characters (the build's own maxlength). Expected: accepted."""
    value = "A" * 255
    data = with_overrides(TD_TRAINER_002, address1=value)
    form_page.fill_form(data)
    expect(form_page.address1_input).to_have_value(value)
    form_page.submit()
    expect(form_page.error_locator("address1")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts05_addr1_005_above_maximum_length_256(form_page):
    """SCN005 — 256 characters attempted. Expected: input restricted.

    `address1` has HTML `maxlength="255"`, which `.fill()` respects —
    confirms the build itself restricts entry, matching this TC's
    Expected Result exactly (no FSD/build mismatch here).
    """
    attempted = "A" * 256
    data = with_overrides(TD_TRAINER_002, address1=attempted)
    form_page.fill_form(data)
    actual_value = form_page.address1_input.input_value()
    assert len(actual_value) == 255


# ============================================================
# TS05-ADDR2: Address Line 2 (optional)
# ============================================================

def test_tc_ts05_addr2_001_empty_address_line_2(form_page):
    """SCN001 — Blank (optional field). Expected: account can be saved."""
    data = TD_TRAINER_002  # address2 intentionally absent -> stays blank
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts05_addr2_002_valid_address_line_2(form_page):
    """SCN002 — "Apartment 18A". Expected: value accepted."""
    data = with_overrides(TD_TRAINER_002, address2="Apartment 18A")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.success_box).to_be_visible()


# ============================================================
# TS05-CITY: City
# ============================================================

def test_tc_ts05_city_001_valid_city(form_page):
    """SCN001 — "Kuala Lumpur". Expected: accepted."""
    data = with_overrides(TD_TRAINER_002, city="Kuala Lumpur")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("city")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts05_city_002_blank_city(form_page):
    """SCN002 — Blank. Expected: validation displayed."""
    data = with_overrides(TD_TRAINER_002, city="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("city")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts05_city_003_maximum_length_100(form_page):
    """SCN003 — exactly 100 characters (the build's own maxlength). Expected: accepted."""
    value = "A" * 100
    data = with_overrides(TD_TRAINER_002, city=value)
    form_page.fill_form(data)
    expect(form_page.city_input).to_have_value(value)
    form_page.submit()
    expect(form_page.error_locator("city")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts05_city_004_above_maximum_length_101(form_page):
    """SCN004 — 101 characters attempted. Expected: input restricted.

    `city` has HTML `maxlength="100"`, which `.fill()` respects — confirms
    the build itself restricts entry, matching this TC exactly.
    """
    attempted = "A" * 101
    data = with_overrides(TD_TRAINER_002, city=attempted)
    form_page.fill_form(data)
    actual_value = form_page.city_input.input_value()
    assert len(actual_value) == 100


# ============================================================
# TS05-STATE: State/Province (optional)
# ============================================================

def test_tc_ts05_state_001_empty_state_province(form_page):
    """SCN001 — Blank (optional field). Expected: account can be saved."""
    data = TD_TRAINER_002  # state_province intentionally absent -> stays blank
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts05_state_002_valid_state_province(form_page):
    """SCN002 — "Selangor". Expected: value accepted."""
    data = with_overrides(TD_TRAINER_002, state_province="Selangor")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.success_box).to_be_visible()


# ============================================================
# TS05-TRANS: Address Mode Transition
# ============================================================

def test_tc_ts05_trans_001_non_singapore_to_singapore(form_page):
    """SCN001 — Non-Singapore address entered, then switch to Singapore.
    Expected: Singapore fields displayed, Non-Singapore fields hidden."""
    data = with_overrides(TD_TRAINER_002, address1="123 Jalan Ampang", city="Kuala Lumpur")
    form_page.fill_form(data)
    expect(form_page.address1_input).to_be_visible()

    form_page.select_residential_type("Singapore")

    expect(form_page.block_number_input).to_be_visible()
    expect(form_page.street_name_input).to_be_visible()
    expect(form_page.address1_input).to_be_hidden()
    expect(form_page.city_input).to_be_hidden()


def test_tc_ts05_trans_002_data_retention_after_toggle(form_page):
    """SCN002 — Complete Non-Singapore address, switch to Singapore, then
    back to Non-Singapore. Validates Finding F09.

    Observed/documented behavior: the AUT hides fields via CSS rather than
    clearing their values, so Address Line 1 is still present after the
    round trip — the actual, empirically confirmed answer to F09 for this
    field, not an assumption.
    """
    data = with_overrides(TD_TRAINER_002, address1="123 Jalan Ampang", city="Kuala Lumpur")
    form_page.fill_form(data)
    expect(form_page.address1_input).to_have_value("123 Jalan Ampang")

    form_page.select_residential_type("Singapore")
    form_page.select_residential_type("Non-Singapore")

    assert form_page.address1_input.input_value() == "123 Jalan Ampang", (
        "F09 evidence: Address Line 1's value is retained across a "
        "Non-Singapore -> Singapore -> Non-Singapore round trip"
    )
