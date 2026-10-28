"""TS-03: Emergency Contact Information — official 186-test-case library.

Source of truth: TS03.xlsx at the workspace root, cross-checked against
FSD_Trainer_Account_Creation.docx §4.3 and docs/DEFECTS.md (BUG-06, BUG-08,
BUG-10). 3 of the 24 official cases are recorded Failed (REL-001/BUG-06,
NAME-005/BUG-10, PHONE-006/BUG-08) — asserted here per the FSD, so all 3
are EXPECTED to fail for real, same methodology as earlier suites.
"""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data.test_data import TD_TRAINER_001, with_overrides, without_keys

pytestmark = pytest.mark.ts03


# ============================================================
# TS03-NAME: Emergency Contact Name
# ============================================================

def test_tc_ts03_name_001_valid_contact_name(form_page):
    """SCN001 — "David Tan". Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, emergency_name="David Tan")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyName")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts03_name_002_empty_contact_name(form_page):
    """SCN002 — Blank. Expected: "This field is required." """
    data = with_overrides(TD_TRAINER_001, emergency_name="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyName")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts03_name_003_spaces_only(form_page):
    """SCN003 — Spaces only. Expected: field treated as empty."""
    data = with_overrides(TD_TRAINER_001, emergency_name="   ")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyName")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts03_name_004_maximum_length_100(form_page):
    """SCN004 — exactly 100 characters. Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, emergency_name="A" * 100)
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyName")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


@pytest.mark.known_defect
def test_tc_ts03_name_005_above_maximum_length(form_page):
    """SCN005 — 101 characters. FSD §4.3: Emergency Contact Name is String/100.

    Official Actual Result: FAILED (BUG-10) — same class of defect as
    TS01-PI SCN005 (Preferred Name): no JS length check, only HTML
    `maxlength="255"` applies, so a 101-character value is accepted in full.

    This test asserts the FSD-required cap, so it is EXPECTED TO FAIL —
    documented evidence for BUG-10 on this second affected field.
    """
    value = "A" * 101
    data = with_overrides(TD_TRAINER_001, emergency_name=value)
    form_page.fill_form(data)
    form_page.submit()
    actual_value = form_page.emergency_name_input.input_value()
    assert len(actual_value) <= 100, (
        f"BUG-10: expected Emergency Contact Name capped at 100 chars per "
        f"FSD §4.3, got {len(actual_value)} chars accepted"
    )


# ============================================================
# TS03-REL: Relationship
# ============================================================

@pytest.mark.known_defect
def test_tc_ts03_rel_001_parent_relationship(form_page):
    """SCN001 — Select "Parent". FSD §4.3 enumeration: Parent / Spouse /
    Sibling / Relative / Friend / Others (6 values, single "Parent").

    Official Actual Result: FAILED (BUG-06) — the build's dropdown splits
    Parent into "Father" and "Mother" (7 values total) and has no generic
    "Parent" option at all, so it cannot be selected.

    This test asserts the FSD-required option exists, so it is EXPECTED TO
    FAIL — documented evidence for BUG-06.
    """
    try:
        # A short explicit timeout: the option is already known not to
        # exist (that is the defect being documented), so there is no
        # reason to wait through Playwright's full default 30s retry
        # window before failing.
        form_page.emergency_relationship_select.select_option(
            label="Parent", timeout=3000
        )
    except Exception as exc:  # noqa: BLE001 - deliberately converting a
        # Playwright "option not found" error into a clear, cited assertion
        # failure, since that error IS the defect evidence for BUG-06.
        pytest.fail(
            f"BUG-06: expected a generic 'Parent' option per FSD §4.3, but "
            f"the build's dropdown has no such option (only Father/Mother "
            f"split exist instead): {exc}"
        )
    expect(form_page.emergency_relationship_select).to_have_value("Parent")


def test_tc_ts03_rel_002_spouse_relationship(form_page):
    """SCN002 — Select Spouse. Expected: selected successfully."""
    form_page.select_emergency_relationship("Spouse")
    expect(form_page.emergency_relationship_select).to_have_value("Spouse")


def test_tc_ts03_rel_003_sibling_relationship(form_page):
    """SCN003 — Select Sibling. Expected: selected successfully."""
    form_page.select_emergency_relationship("Sibling")
    expect(form_page.emergency_relationship_select).to_have_value("Sibling")


def test_tc_ts03_rel_004_relative_relationship(form_page):
    """SCN004 — Select Relative. Expected: selected successfully."""
    form_page.select_emergency_relationship("Relative")
    expect(form_page.emergency_relationship_select).to_have_value("Relative")


def test_tc_ts03_rel_005_friend_relationship(form_page):
    """SCN005 — Select Friend. Expected: selected successfully."""
    form_page.select_emergency_relationship("Friend")
    expect(form_page.emergency_relationship_select).to_have_value("Friend")


def test_tc_ts03_rel_006_others_relationship(form_page):
    """SCN006 — Select Others. Expected: selected successfully."""
    form_page.select_emergency_relationship("Others")
    expect(form_page.emergency_relationship_select).to_have_value("Others")


def test_tc_ts03_rel_007_no_relationship_selected(form_page):
    """SCN007 — Left unselected. Expected: validation message on Save."""
    data = without_keys(TD_TRAINER_001, "emergency_relationship")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyRelationship")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts03_rel_008_father_option_in_build(form_page):
    """SCN008 — Finding F25: "Father" exists in the build though not in the
    FSD's enumeration. Expected (and actual): the option exists and is
    selectable — this documents the build's real enumeration, it does not
    assert FSD compliance (that is REL-001's job)."""
    form_page.select_emergency_relationship("Father")
    expect(form_page.emergency_relationship_select).to_have_value("Father")


def test_tc_ts03_rel_009_mother_option_in_build(form_page):
    """SCN009 — Finding F25: "Mother" exists in the build though not in the
    FSD's enumeration. Same documentation intent as REL-008."""
    form_page.select_emergency_relationship("Mother")
    expect(form_page.emergency_relationship_select).to_have_value("Mother")


# ============================================================
# TS03-CODE: Emergency Contact Country Code
# ============================================================

def test_tc_ts03_code_001_default_country_code(form_page):
    """SCN001 — Form freshly opened. Expected: country code defaults to +65."""
    expect(form_page.emergency_code_select).to_have_value("+65")


# ============================================================
# TS03-PHONE: Emergency Contact Number
# ============================================================

def test_tc_ts03_phone_001_valid_singapore_phone(form_page):
    """SCN001 — +65, "91234567". Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, emergency_phone_code="+65", emergency_phone="91234567")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts03_phone_002_empty_emergency_phone(form_page):
    """SCN002 — Blank. Expected: validation message displayed."""
    data = with_overrides(TD_TRAINER_001, emergency_phone="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyPhone")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts03_phone_003_non_numeric_input(form_page):
    """SCN003 — "ABC12345". Expected: validation error displayed."""
    data = with_overrides(TD_TRAINER_001, emergency_phone="ABC12345")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyPhone")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts03_phone_004_seven_digits_singapore(form_page):
    """SCN004 — +65, 7 digits. Expected: validation error (below the build's exactly-8 rule)."""
    data = with_overrides(TD_TRAINER_001, emergency_phone_code="+65", emergency_phone="1234567")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyPhone")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts03_phone_005_eight_digits_singapore(form_page):
    """SCN005 — +65, exactly 8 digits. Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, emergency_phone_code="+65", emergency_phone="12345678")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


@pytest.mark.known_defect
def test_tc_ts03_phone_006_nine_digits_singapore(form_page):
    """SCN006 — +65, 9 digits. FSD §6: phone fields are Numeric/8-15 with
    no per-country-code exception, so 9 digits under +65 should be accepted.

    Official Actual Result: FAILED (BUG-08) — same undocumented
    exactly-8-digit rule for +65 as TS02-PPHONE SCN006.

    This test asserts the FSD-required behavior, so it is EXPECTED TO FAIL
    — documented evidence for BUG-08 on this second affected field.
    """
    data = with_overrides(TD_TRAINER_001, emergency_phone_code="+65", emergency_phone="123456789")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts03_phone_007_international_minimum_length(form_page):
    """SCN007 — +84, 8 digits. Expected: accepted (lower valid boundary)."""
    data = with_overrides(TD_TRAINER_001, emergency_phone_code="+84", emergency_phone="12345678")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts03_phone_008_international_maximum_length(form_page):
    """SCN008 — +84, 15 digits. Expected: accepted (upper valid boundary)."""
    data = with_overrides(
        TD_TRAINER_001, emergency_phone_code="+84", emergency_phone="123456789012345"
    )
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts03_phone_009_international_above_maximum(form_page):
    """SCN009 — +84, 16 digits. Expected: validation error (above max).

    `emergencyPhone` has HTML `maxlength="15"`, same as `primaryPhone` —
    uses `set_raw_value()` to inject the full 16-digit value directly, so
    the JS length check itself is exercised (see
    test_ts02_contact_information.py's PPHONE-009 for the same, empirically
    confirmed reasoning).
    """
    data = with_overrides(TD_TRAINER_001, emergency_phone_code="+84")
    form_page.fill_form(data)
    form_page.set_raw_value(form_page.emergency_phone_input, "1234567890123456")
    form_page.submit()
    expect(form_page.error_locator("emergencyPhone")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()
