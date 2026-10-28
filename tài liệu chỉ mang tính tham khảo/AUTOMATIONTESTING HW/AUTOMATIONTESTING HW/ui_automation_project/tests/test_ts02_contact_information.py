"""TS-02: Contact Information — official 186-test-case library.

Source of truth: TS02.xlsx (TestCases + DataLibrary sheets) at the workspace
root, cross-checked against FSD_Trainer_Account_Creation.docx §4.2/§6 and
docs/DEFECTS.md (BUG-02, BUG-08). See test_ts01_personal_information.py's
module docstring for the shared methodology (known-defect tests are
expected to fail for real; Blocked cases are skipped with a cited reason).
"""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data.test_data import TD_TRAINER_001, with_overrides

pytestmark = pytest.mark.ts02


# ============================================================
# TS02-EMAIL: Primary Email Address
# ============================================================

def test_tc_ts02_email_001_valid_email(form_page):
    """SCN001 — Valid email "trainer@example.com". Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, primary_email="trainer@example.com")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryEmail")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts02_email_002_empty_email(form_page):
    """SCN002 — Empty email. Expected: mandatory validation displayed."""
    data = with_overrides(TD_TRAINER_001, primary_email="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryEmail")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts02_email_003_spaces_only(form_page):
    """SCN003 — Spaces only. Expected: field treated as empty."""
    data = with_overrides(TD_TRAINER_001, primary_email="   ")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryEmail")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts02_email_004_missing_at_symbol(form_page):
    """SCN004 — "trainerexample.com" (no @). Expected: format error."""
    data = with_overrides(TD_TRAINER_001, primary_email="trainerexample.com")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryEmail")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts02_email_005_missing_domain(form_page):
    """SCN005 — "trainer@" (no domain). Expected: format error."""
    data = with_overrides(TD_TRAINER_001, primary_email="trainer@")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryEmail")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


@pytest.mark.skip(
    reason=(
        "BLOCKED (official suite): precondition 'an existing trainer uses "
        "trainer@example.com' cannot be set up — this build has no "
        "persistence layer of any kind. Code review independently confirms "
        "zero duplicate-email-check logic in the Save handler "
        "(see docs/DEFECTS.md, BUG-02)."
    )
)
def test_tc_ts02_email_006_duplicate_email(form_page):
    """SCN006 — Duplicate email. Cannot be automated (see skip reason)."""


@pytest.mark.skip(
    reason=(
        "BLOCKED (official suite): same as SCN006 — additionally requires "
        "a persisted case-insensitive comparison, which the build cannot "
        "perform since it has no persistence layer at all (docs/DEFECTS.md, BUG-02)."
    )
)
def test_tc_ts02_email_007_duplicate_email_different_case(form_page):
    """SCN007 — Duplicate email, different case. Cannot be automated."""


def test_tc_ts02_email_008_maximum_length_100(form_page):
    """SCN008 — exactly 100-character email. Expected: accepted."""
    value = "a" * 88 + "@example.com"  # 88 + 12 = 100 chars, valid format
    assert len(value) == 100
    data = with_overrides(TD_TRAINER_001, primary_email=value)
    form_page.fill_form(data)
    expect(form_page.primary_email_input).to_have_value(value)
    form_page.submit()
    expect(form_page.error_locator("primaryEmail")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts02_email_009_above_maximum_length(form_page):
    """SCN009 — 101-character email attempted.

    Expected (official): "System does not allow value exceeding limit."
    Verified mechanism: `primaryEmail` has HTML `maxlength="100"`, which
    Playwright's `.fill()` genuinely respects (confirmed empirically before
    writing this test) — the browser itself truncates to 100 chars before
    the value ever reaches the field, so the attempted 101st character
    ("m" of ".com") never lands, leaving ".co" which is still a
    syntactically valid address under the build's own email regex.
    """
    attempted = "a" * 89 + "@example.com"  # 89 + 12 = 101 chars attempted
    assert len(attempted) == 101
    data = with_overrides(TD_TRAINER_001, primary_email=attempted)
    form_page.fill_form(data)
    actual_value = form_page.primary_email_input.input_value()
    assert len(actual_value) == 100, (
        f"expected browser maxlength=100 to cap the value, got "
        f"{len(actual_value)} chars: {actual_value!r}"
    )
    form_page.submit()
    expect(form_page.error_locator("primaryEmail")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


# ============================================================
# TS02-PCODE: Primary Contact Country Code
# ============================================================

def test_tc_ts02_pcode_001_default_country_code(form_page):
    """SCN001 — Form freshly opened. Expected: country code defaults to +65."""
    expect(form_page.primary_code_select).to_have_value("+65")


# ============================================================
# TS02-PPHONE: Primary Contact Number
# ============================================================

def test_tc_ts02_pphone_001_valid_singapore_number(form_page):
    """SCN001 — +65, "91234567". Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, primary_phone_code="+65", primary_phone="91234567")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts02_pphone_002_empty_phone_number(form_page):
    """SCN002 — Empty. Expected: validation message displayed."""
    data = with_overrides(TD_TRAINER_001, primary_phone="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts02_pphone_003_non_numeric_input(form_page):
    """SCN003 — "ABC12345". Expected: validation error displayed."""
    data = with_overrides(TD_TRAINER_001, primary_phone="ABC12345")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts02_pphone_004_singapore_seven_digits(form_page):
    """SCN004 — +65, 7 digits (below the build's exactly-8 rule). Expected: rejected."""
    data = with_overrides(TD_TRAINER_001, primary_phone_code="+65", primary_phone="1234567")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts02_pphone_005_singapore_eight_digits(form_page):
    """SCN005 — +65, exactly 8 digits. Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, primary_phone_code="+65", primary_phone="12345678")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


@pytest.mark.known_defect
def test_tc_ts02_pphone_006_singapore_nine_digits(form_page):
    """SCN006 — +65, 9 digits. FSD §6: phone fields are Numeric/8-15 with
    no per-country-code exception, so 9 digits under +65 should be accepted.

    Official Actual Result: FAILED (BUG-08) — the build enforces an
    undocumented exactly-8-digit rule for +65 and rejects this with
    "Enter a valid contact number."

    This test asserts the FSD-required behavior, so it is EXPECTED TO FAIL
    against the current build — documented evidence for BUG-08.
    """
    data = with_overrides(TD_TRAINER_001, primary_phone_code="+65", primary_phone="123456789")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts02_pphone_007_international_eight_digits(form_page):
    """SCN007 — +84, 8 digits. Expected: accepted (lower valid boundary)."""
    data = with_overrides(TD_TRAINER_001, primary_phone_code="+84", primary_phone="12345678")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts02_pphone_008_international_fifteen_digits(form_page):
    """SCN008 — +84, 15 digits. Expected: accepted (upper valid boundary)."""
    data = with_overrides(
        TD_TRAINER_001, primary_phone_code="+84", primary_phone="123456789012345"
    )
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts02_pphone_009_international_sixteen_digits(form_page):
    """SCN009 — +84, 16 digits. Expected: validation error (above max).

    `primaryPhone` has HTML `maxlength="15"`, which `.fill()` respects just
    like real typing would — silently capping at 15 chars and making the
    16-digit boundary untestable through normal interaction (confirmed
    empirically). Uses `set_raw_value()` to inject the full 16-digit value
    directly, so the JS length check (`value.length <= 15`) is the thing
    actually being exercised, matching the official TC's intent (BVA on the
    validation logic itself, not on what a text box will let you type).
    """
    data = with_overrides(TD_TRAINER_001, primary_phone_code="+84")
    form_page.fill_form(data)
    form_page.set_raw_value(form_page.primary_phone_input, "1234567890123456")
    form_page.submit()
    expect(form_page.error_locator("primaryPhone")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ============================================================
# TS02-SPHONE: Secondary Contact Number
# ============================================================

def test_tc_ts02_sphone_001_empty_secondary_number(form_page):
    """SCN001 — Left blank (optional field). Expected: account can be saved."""
    data = TD_TRAINER_001  # secondary_phone key intentionally absent -> stays blank
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("secondaryPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts02_sphone_002_valid_secondary_number(form_page):
    """SCN002 — "87654321" (default +65 code). Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, secondary_phone="87654321")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("secondaryPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts02_sphone_003_non_numeric(form_page):
    """SCN003 — "ABCD1234". Expected: validation error displayed."""
    data = with_overrides(TD_TRAINER_001, secondary_phone="ABCD1234")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("secondaryPhone")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()
