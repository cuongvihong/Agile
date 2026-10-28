"""TS-09: Additional Findings from Extended Review (F25-F28) — official
186-test-case library.

Source of truth: TS09.xlsx at the workspace root, cross-checked against
docs/DEFECTS.md (BUG-06, BUG-07, BUG-08, BUG-09). This suite re-verifies
the same 4 findings from multiple angles (existence, boundary, comparison)
rather than one test per finding — several cases below deliberately
duplicate the underlying check in test_ts03/test_ts04 under their own
official TC ID, since that is how the source library itself is organized.

1 of the 18 official cases is recorded Failed (F27-003/BUG-08) — asserted
here per the FSD, so it is EXPECTED to fail for real.
"""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data.test_data import TD_TRAINER_001, with_overrides, without_keys

pytestmark = pytest.mark.ts09


# ============================================================
# TS09-F25: Relationship Enumeration Mismatch
# ============================================================

def test_tc_ts09_f25_001_verify_father_option_exists(form_page):
    """SCN001 — "Father" exists in the build though absent from the FSD."""
    form_page.select_emergency_relationship("Father")
    expect(form_page.emergency_relationship_select).to_have_value("Father")


def test_tc_ts09_f25_002_verify_mother_option_exists(form_page):
    """SCN002 — "Mother" exists in the build though absent from the FSD."""
    form_page.select_emergency_relationship("Mother")
    expect(form_page.emergency_relationship_select).to_have_value("Mother")


def test_tc_ts09_f25_003_verify_parent_option_missing(form_page):
    """SCN003 — "Parent" (the FSD's own single value) does not exist as an
    option in the build at all."""
    parent_option = form_page.emergency_relationship_select.locator(
        "option", has_text="Parent"
    )
    expect(parent_option).to_have_count(0)


def test_tc_ts09_f25_004_compare_enumeration_lists(form_page):
    """SCN004 — Compare the FSD's enumeration against the build's.

    FSD §4.3: Parent / Spouse / Sibling / Relative / Friend / Others (6).
    Build (observed here): Father / Mother / Spouse / Sibling / Relative /
    Friend / Others (7) — Parent split into two, matching BUG-06 exactly.
    """
    options = form_page.emergency_relationship_select.locator("option")
    texts = options.all_inner_texts()
    # Exclude the placeholder option (`<option value="">Select</option>`),
    # which has no `value` attribute the other options do either — real
    # selectable relationships are everything except that one literal text.
    build_values = {t.strip() for t in texts if t.strip() and t.strip() != "Select"}
    fsd_values = {"Parent", "Spouse", "Sibling", "Relative", "Friend", "Others"}
    assert build_values == {
        "Father", "Mother", "Spouse", "Sibling", "Relative", "Friend", "Others",
    }
    assert build_values != fsd_values  # documents the real mismatch


# ============================================================
# TS09-F26: Block Number Length Mismatch
# ============================================================

def test_tc_ts09_f26_001_enter_nine_characters(form_page):
    """SCN001 — 9 characters (the build's own maxlength). Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, block_number="123456789")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("blockNumber")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts09_f26_002_enter_ten_characters(form_page):
    """SCN002 — attempt 10 characters. Confirms BUG-07 (same as
    TS04-BLOCK SCN003): the build restricts entry to 9, one short of the
    FSD's stated 10."""
    data = with_overrides(TD_TRAINER_001, block_number="1234567890")
    form_page.fill_form(data)
    actual_value = form_page.block_number_input.input_value()
    assert len(actual_value) == 9, (
        f"BUG-07 evidence: expected maxlength=9 to truncate entry, got "
        f"{len(actual_value)} chars: {actual_value!r}"
    )


def test_tc_ts09_f26_003_compare_requirement(form_page):
    """SCN003 — Compare the FSD's stated limit against the build's actual
    HTML attribute. FSD §4.4.1: String/10. Build (observed): `maxlength="9"`."""
    actual_maxlength = form_page.block_number_input.get_attribute("maxlength")
    assert actual_maxlength == "9"
    fsd_stated_limit = 10
    assert int(actual_maxlength) != fsd_stated_limit  # documents the mismatch


# ============================================================
# TS09-F27: Singapore Phone Validation
# ============================================================

def test_tc_ts09_f27_001_seven_digits(form_page):
    """SCN001 — +65, 7 digits. Expected: validation error displayed."""
    data = with_overrides(TD_TRAINER_001, primary_phone_code="+65", primary_phone="1234567")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts09_f27_002_eight_digits(form_page):
    """SCN002 — +65, exactly 8 digits. Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, primary_phone_code="+65", primary_phone="12345678")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


@pytest.mark.known_defect
def test_tc_ts09_f27_003_nine_digits(form_page):
    """SCN003 — +65, 9 digits. FSD §6: phone fields are Numeric/8-15 with
    no per-country-code exception, so 9 digits under +65 should be
    accepted.

    Official Actual Result: FAILED (BUG-08) — same undocumented
    exactly-8-digit rule; this TC directly confirms F27.

    This test asserts the FSD-required behavior, so it is EXPECTED TO FAIL
    — documented evidence for BUG-08 on this third affected field/suite.
    """
    data = with_overrides(TD_TRAINER_001, primary_phone_code="+65", primary_phone="123456789")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts09_f27_004_fsd_rule_comparison(form_page):
    """SCN004 — Compare the FSD's general phone rule against the build's
    actual +65-specific behavior.

    FSD §6: Numeric/8-15, no per-country-code exception stated.
    Build (observed): enforces exactly 8 digits when code=+65, contrasted
    here against the same 9-digit value being genuinely accepted under a
    non-+65 code (+84) — demonstrating the undocumented +65-only rule
    exists, without re-asserting the FSD ideal itself (that is F27-003's job).
    """
    sg_data = with_overrides(TD_TRAINER_001, primary_phone_code="+65", primary_phone="123456789")
    form_page.fill_form(sg_data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_visible()  # +65 rejects 9 digits

    form_page.open(form_page.page.url)
    intl_data = with_overrides(TD_TRAINER_001, primary_phone_code="+84", primary_phone="123456789")
    form_page.fill_form(intl_data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_hidden()  # +84 accepts 9 digits


def test_tc_ts09_f27_005_international_number_boundary(form_page):
    """SCN005 — +84: 8/15 digits accepted, 16 digits rejected. Confirms
    the build's behavior matches its own implemented (non-+65) rule."""
    for phone, should_error in [("12345678", False), ("123456789012345", False)]:
        data = with_overrides(TD_TRAINER_001, primary_phone_code="+84", primary_phone=phone)
        form_page.fill_form(data)
        form_page.submit()
        if should_error:
            expect(form_page.error_locator("primaryPhone")).to_be_visible()
        else:
            expect(form_page.error_locator("primaryPhone")).to_be_hidden()
        form_page.open(form_page.page.url)

    data = with_overrides(TD_TRAINER_001, primary_phone_code="+84")
    form_page.fill_form(data)
    form_page.set_raw_value(form_page.primary_phone_input, "1234567890123456")
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_visible()


# ============================================================
# TS09-F28: Floor Number Validation
# ============================================================

def test_tc_ts09_f28_001_numeric_floor_number(form_page):
    """SCN001 — "12". Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, floor_number="12")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts09_f28_002_five_digit_boundary(form_page):
    """SCN002 — "12345" (5 digits, the build's own maxlength). Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, floor_number="12345")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts09_f28_003_six_digit_boundary(form_page):
    """SCN003 — 6 digits. Expected: validation error displayed (same
    `set_raw_value()` reasoning as TS04-FLOOR SCN003: HTML `maxlength="5"`
    would otherwise silently cap real typing at a valid 5-digit value)."""
    data = without_keys(TD_TRAINER_001, "floor_number")
    form_page.fill_form(data)
    form_page.set_raw_value(form_page.floor_number_input, "123456")
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts09_f28_004_alpha_numeric_value(form_page):
    """SCN004 — "B1". Confirms BUG-09: rejected by the digits-only regex
    despite the FSD placing no character restriction on Floor Number."""
    data = with_overrides(TD_TRAINER_001, floor_number="B1")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts09_f28_005_basement_style_value(form_page):
    """SCN005 — "B2" (a common basement notation). Confirms BUG-09 with a
    second real-world example."""
    data = with_overrides(TD_TRAINER_001, floor_number="B2")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts09_f28_006_requirement_comparison(form_page):
    """SCN006 — Compare the FSD's Floor Number definition against the
    build's validation logic.

    FSD §4.4.1: String/5, no character-type restriction stated.
    Build (observed): a valid 5-character alphanumeric-shaped value ("B1")
    is rejected, while a valid 5-digit numeric value ("12345") is accepted
    — demonstrating the build's digits-only rule is stricter than the FSD,
    without re-asserting the FSD ideal itself (that is F28-004/005's job).
    """
    data_letters = with_overrides(TD_TRAINER_001, floor_number="B1")
    form_page.fill_form(data_letters)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_visible()

    form_page.open(form_page.page.url)
    data_digits = with_overrides(TD_TRAINER_001, floor_number="12345")
    form_page.fill_form(data_digits)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_hidden()
