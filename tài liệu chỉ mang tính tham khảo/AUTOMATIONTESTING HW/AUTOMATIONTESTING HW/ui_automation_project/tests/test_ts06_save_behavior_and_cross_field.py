"""TS-06: Save Behaviour and Cross-field Rules — official 186-test-case library.

Source of truth: TS06.xlsx at the workspace root, cross-checked against
FSD_Trainer_Account_Creation.docx §5 and docs/DEFECTS.md (BUG-02, BUG-04).

1 of the 23 official cases is recorded Failed (SAVE-002/BUG-04) — asserted
here per the FSD, so it is EXPECTED to fail for real. 4 are recorded
Blocked (DUP-001..004, all requiring a persistence layer this static-HTML
build does not have) — skipped with a cited reason, matching TS-01/TS-02's
duplicate-check cases.
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data.test_data import (
    TD_TRAINER_001,
    TD_TRAINER_002,
    TRAINER_PDF_OVER_10MB,
    TRAINER_UNSUPPORTED,
    with_overrides,
    without_keys,
)

pytestmark = pytest.mark.ts06

TRAINER_ID_PATTERN = re.compile(r"Trainer ID: TRN(\d{6})")


# ============================================================
# TS06-SAVE: Happy Path Save
# ============================================================

def test_tc_ts06_save_001_save_with_all_valid_data(form_page):
    """SCN001 — All fields valid. Expected: account saved, success message shown."""
    form_page.fill_form(TD_TRAINER_001)
    form_page.submit()
    expect(form_page.success_box).to_be_visible()
    text = form_page.success_text()
    assert "Trainer account has been created successfully." in text
    assert TRAINER_ID_PATTERN.search(text), text


@pytest.mark.known_defect
def test_tc_ts06_save_002_save_generates_trainer_id(form_page, aut_url):
    """SCN002 — Save twice, compare the two Trainer IDs.

    FSD §7: Trainer ID format is TRNXXXXXX, where XXXXXX is a six-digit
    SEQUENTIAL number.

    Official Actual Result: FAILED (BUG-04) — the build generates
    'TRN' + a random 6-digit number (`Math.random()`), with no sequence
    and no uniqueness check against previously issued IDs.

    This test asserts sequential generation (second ID = first ID + 1), so
    it is EXPECTED TO FAIL against the current build — documented evidence
    for BUG-04.
    """
    form_page.fill_form(TD_TRAINER_001)
    form_page.submit()
    first_match = TRAINER_ID_PATTERN.search(form_page.success_text())
    assert first_match, form_page.success_text()
    first_id = int(first_match.group(1))

    form_page.open(aut_url)
    form_page.fill_form(TD_TRAINER_001)
    form_page.submit()
    second_match = TRAINER_ID_PATTERN.search(form_page.success_text())
    assert second_match, form_page.success_text()
    second_id = int(second_match.group(1))

    assert second_id == first_id + 1, (
        f"BUG-04: expected the second Trainer ID to be exactly one more "
        f"than the first (sequential per FSD §7), got first={first_id}, "
        f"second={second_id} (both effectively random)"
    )


def test_tc_ts06_save_003_active_status_created(form_page):
    """SCN003 — Save. Expected: status displayed as Active."""
    form_page.fill_form(TD_TRAINER_001)
    form_page.submit()
    expect(form_page.success_box).to_be_visible()
    assert "Status: Active" in form_page.success_text()


# ============================================================
# TS06-MAND: Mandatory Validation
# ============================================================

def test_tc_ts06_mand_001_preferred_name_missing(form_page):
    """SCN001 — Preferred Name blank. Expected: "This field is required." """
    data = with_overrides(TD_TRAINER_001, preferred_name="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("preferredName")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts06_mand_002_id_number_missing(form_page):
    """SCN002 — ID Number blank. Expected: "This field is required." """
    data = with_overrides(TD_TRAINER_001, id_number="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("idNumber")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts06_mand_003_email_missing(form_page):
    """SCN003 — Email blank. Expected: validation message displayed."""
    data = with_overrides(TD_TRAINER_001, primary_email="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryEmail")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts06_mand_004_emergency_contact_missing(form_page):
    """SCN004 — Emergency Contact Name blank. Expected: validation message displayed."""
    data = with_overrides(TD_TRAINER_001, emergency_name="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("emergencyName")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts06_mand_005_singapore_address_mandatory_missing(form_page):
    """SCN005 — Singapore selected, Postal Code blank. Expected: validation displayed."""
    data = with_overrides(TD_TRAINER_001, postal_code="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("postalCode")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts06_mand_006_non_singapore_address_mandatory_missing(form_page):
    """SCN006 — Non-Singapore selected, Address Line 1 blank. Expected: validation displayed."""
    data = with_overrides(TD_TRAINER_002, address1="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("address1")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts06_mand_007_multiple_mandatory_fields_empty(form_page):
    """SCN007 — Form left largely empty. Validates Finding F14: whether
    multiple inline errors appear together or one at a time.

    Observed/documented behavior: the AUT is cumulative, not fail-fast —
    every applicable field's error is shown simultaneously (see
    docs/SESSION_01_ANALYSIS_AND_REQUIREMENTS.md §4), resolving F14.
    """
    form_page.submit()
    expect(form_page.error_locator("preferredName")).to_be_visible()
    expect(form_page.error_locator("gender")).to_be_visible()
    expect(form_page.error_locator("idType")).to_be_visible()
    expect(form_page.error_locator("primaryEmail")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ============================================================
# TS06-DUP: Duplicate Validation (all Blocked — no persistence layer)
# ============================================================

_DUP_SKIP_REASON = (
    "BLOCKED (official suite): precondition 'an existing trainer record "
    "exists' cannot be set up — this build has no persistence layer of "
    "any kind. Code review independently confirms zero duplicate-check "
    "logic in the Save handler (see docs/DEFECTS.md, BUG-02)."
)


@pytest.mark.skip(reason=_DUP_SKIP_REASON)
def test_tc_ts06_dup_001_duplicate_email(form_page):
    """SCN001 — Duplicate email. Cannot be automated (see skip reason)."""


@pytest.mark.skip(reason=_DUP_SKIP_REASON)
def test_tc_ts06_dup_002_duplicate_email_different_case(form_page):
    """SCN002 — Duplicate email, different case. Cannot be automated."""


@pytest.mark.skip(reason=_DUP_SKIP_REASON)
def test_tc_ts06_dup_003_duplicate_id_number(form_page):
    """SCN003 — Duplicate ID Number. Cannot be automated."""


@pytest.mark.skip(reason=_DUP_SKIP_REASON)
def test_tc_ts06_dup_004_duplicate_id_different_case(form_page):
    """SCN004 — Duplicate ID Number, different case. Cannot be automated."""


# ============================================================
# TS06-FORMAT: Format Validation
# ============================================================

def test_tc_ts06_format_001_invalid_email_format(form_page):
    """SCN001 — "trainer@" (no domain). Expected: email validation error."""
    data = with_overrides(TD_TRAINER_001, primary_email="trainer@")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryEmail")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts06_format_002_non_numeric_phone(form_page):
    """SCN002 — "ABC12345". Expected: phone validation error."""
    data = with_overrides(TD_TRAINER_001, primary_phone="ABC12345")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts06_format_003_unsupported_file_format(form_page):
    """SCN003 — trainer.exe. Expected: unsupported format error."""
    data = with_overrides(TD_TRAINER_001, id_document_path=TRAINER_UNSUPPORTED)
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("idDocument")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts06_format_004_oversized_file(form_page):
    """SCN004 — 10MB + 1 byte. Expected: file size validation displayed."""
    data = with_overrides(TD_TRAINER_001, id_document_path=TRAINER_PDF_OVER_10MB)
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("idDocument")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ============================================================
# TS06-CROSS: Cross-field Rules
# ============================================================

def test_tc_ts06_cross_001_singapore_requires_postal_code(form_page):
    """SCN001 — Singapore selected, Postal Code blank. Expected: validation displayed."""
    data = with_overrides(TD_TRAINER_001, postal_code="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("postalCode")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts06_cross_002_non_singapore_requires_address_line_1(form_page):
    """SCN002 — Non-Singapore selected, Address Line 1 blank. Expected: validation displayed."""
    data = with_overrides(TD_TRAINER_002, address1="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("address1")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts06_cross_003_floor_unit_not_applicable_selected(form_page):
    """SCN003 — Checkbox ticked, Floor/Unit blank. Expected: Save succeeds."""
    data = with_overrides(
        TD_TRAINER_001, floor_number="", unit_number="", floor_not_applicable=True
    )
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts06_cross_004_floor_unit_checkbox_not_selected(form_page):
    """SCN004 — Checkbox unticked, Floor/Unit blank. Expected: validation displayed."""
    data = with_overrides(TD_TRAINER_001, floor_number="", unit_number="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("floorUnit")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ============================================================
# TS06-NEG: Invalid Data Prevention
# ============================================================

def test_tc_ts06_neg_001_multiple_invalid_fields(form_page):
    """SCN001 — Invalid email + invalid phone + missing required fields.
    Expected: Trainer Account not created."""
    data = with_overrides(
        without_keys(TD_TRAINER_001, "preferred_name"),
        primary_email="not-an-email",
        primary_phone="ABC123",
    )
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("preferredName")).to_be_visible()
    expect(form_page.error_locator("primaryEmail")).to_be_visible()
    expect(form_page.error_locator("primaryPhone")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()
