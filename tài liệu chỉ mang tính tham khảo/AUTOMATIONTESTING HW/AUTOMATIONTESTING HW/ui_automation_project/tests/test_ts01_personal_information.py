"""TS-01: Personal Information — official 186-test-case library.

Source of truth: TS01.xlsx (TestCases + DataLibrary sheets) at the workspace
root, cross-checked against FSD_Trainer_Account_Creation.docx and
docs/DEFECTS.md (BUG-01..BUG-12, transcribed from Step7_Defect_Reporting.docx).
Every TC ID below is the official one — this file does not invent scenarios.

Per user decision (2026-09-22): where the official suite already executed a
case as Failed against a real, logged defect, the test here asserts the
FSD-required behavior, not the build's actual (defective) behavior — so it
is EXPECTED to fail for real, as documented evidence of that defect. This
matches the official Test_Execution.docx's own methodology, revision 2.

Blocked cases (no persistence layer in this static-HTML build) are marked
`pytest.mark.skip`, not silently omitted.
"""
from __future__ import annotations

import datetime

import pytest
from playwright.sync_api import expect

from data.test_data import (
    ID_TYPE_OPTION_MAP,
    TD_TRAINER_001,
    TRAINER_JPG,
    TRAINER_PDF,
    TRAINER_PDF_10MB,
    TRAINER_PDF_OVER_10MB,
    TRAINER_PNG,
    TRAINER_UNSUPPORTED as TRAINER_EXE,
    with_overrides,
    without_keys,
)

pytestmark = pytest.mark.ts01


# ============================================================
# TS01-PI: Preferred Name
# ============================================================

def test_tc_ts01_pi_001_valid_preferred_name(form_page):
    """SCN001 — Valid Preferred Name. Expected: Preferred Name is accepted."""
    form_page.fill_form(with_overrides(TD_TRAINER_001, preferred_name="John Tan"))
    form_page.submit()
    expect(form_page.error_locator("preferredName")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts01_pi_002_empty_preferred_name(form_page):
    """SCN002 — Empty Preferred Name. Expected: "This field is required." """
    data = with_overrides(TD_TRAINER_001, preferred_name="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("preferredName")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts01_pi_003_spaces_only(form_page):
    """SCN003 — Spaces Only. Expected: field treated as empty, validation shown."""
    data = with_overrides(TD_TRAINER_001, preferred_name="   ")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("preferredName")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts01_pi_004_maximum_length_boundary(form_page):
    """SCN004 — exactly 100 characters. Expected: value accepted."""
    data = with_overrides(TD_TRAINER_001, preferred_name="A" * 100)
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("preferredName")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


@pytest.mark.known_defect
def test_tc_ts01_pi_005_above_maximum_length(form_page):
    """SCN005 — 101 characters. FSD §4.1: Preferred Name is String/100.

    Official Actual Result: FAILED (BUG-10) — the real build has no JS
    length check; only HTML maxlength="255" applies, so a 101-character
    value is accepted in full instead of being rejected/truncated.

    This test asserts the FSD-required behavior (value must not exceed 100
    chars), so it is EXPECTED TO FAIL against the current build — that
    failure is the documented evidence for BUG-10, not a test bug.
    """
    value = "A" * 101
    data = with_overrides(TD_TRAINER_001, preferred_name=value)
    form_page.fill_form(data)
    form_page.submit()
    actual_value = form_page.preferred_name_input.input_value()
    assert len(actual_value) <= 100, (
        f"BUG-10: expected Preferred Name capped at 100 chars per FSD "
        f"§4.1, got {len(actual_value)} chars accepted"
    )


# ============================================================
# TS01-GEN: Gender
# ============================================================

def test_tc_ts01_gen_001_select_male(form_page):
    """SCN001 — Select Male. Expected: Male remains selected."""
    form_page.select_gender("Male")
    assert form_page.is_radio_checked("Male")


def test_tc_ts01_gen_002_select_female(form_page):
    """SCN002 — Select Female. Expected: Female remains selected."""
    form_page.select_gender("Female")
    assert form_page.is_radio_checked("Female")


def test_tc_ts01_gen_003_gender_empty(form_page):
    """SCN003 — Gender left unselected. Expected: validation message on Save."""
    data = TD_TRAINER_001  # fill_form only sets gender if present in dict
    form_page.fill_form(without_keys(data, "gender"))
    form_page.submit()
    expect(form_page.error_locator("gender")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ============================================================
# TS01-IDT: ID Type
# ============================================================

@pytest.mark.parametrize(
    "official_value",
    ["NRIC", "FIN", "Employment Pass", "Passport"],
    ids=["tc_ts01_idt_001", "tc_ts01_idt_002", "tc_ts01_idt_003", "tc_ts01_idt_004"],
)
def test_id_type_selection(form_page, official_value):
    """TS01-IDT SCN001-004 — each ID Type option can be selected and sticks.

    "Employment Pass" is mapped to the build's "EP" option per BUG-05 (the
    FSD's 4-value enumeration does not match the build's 5-value dropdown;
    see data/test_data.py's ID_TYPE_OPTION_MAP note). Selection itself
    succeeds in all 4 cases per the official suite (all Passed, with BUG-05
    separately noted against SCN003 as an enumeration-mismatch finding, not
    a selection failure) — this test only verifies the selection sticks.
    """
    build_option = ID_TYPE_OPTION_MAP[official_value]
    form_page.select_id_type(build_option)
    expect(form_page.id_type_select).to_have_value(build_option)


# ============================================================
# TS01-IDN: ID Number
# ============================================================

def test_tc_ts01_idn_001_valid_nric(form_page):
    """SCN001 — Valid NRIC "S1234567D". Expected: value accepted."""
    data = with_overrides(TD_TRAINER_001, id_type="NRIC", id_number="S1234567D")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("idNumber")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts01_idn_002_blank_id_number(form_page):
    """SCN002 — Blank ID Number. Expected: "This field is required." """
    data = with_overrides(TD_TRAINER_001, id_number="")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("idNumber")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts01_idn_003_spaces_only(form_page):
    """SCN003 — Spaces Only. Expected: value treated as empty."""
    data = with_overrides(TD_TRAINER_001, id_number="   ")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("idNumber")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


@pytest.mark.skip(
    reason=(
        "BLOCKED (official suite, Step6 Test_Execution.docx): precondition "
        "'an existing trainer uses this ID Number' cannot be set up — this "
        "build has no persistence layer / trainer list of any kind. "
        "Code review independently confirms zero duplicate-check logic in "
        "the Save handler (see docs/DEFECTS.md, BUG-02), but the scenario "
        "itself cannot be executed as written against this static mock."
    )
)
def test_tc_ts01_idn_004_duplicate_id_number(form_page):
    """SCN004 — Duplicate ID Number. Cannot be automated (see skip reason)."""


# ============================================================
# TS01-UPL: Identification Document
# ============================================================

@pytest.mark.parametrize(
    "file_path",
    [TRAINER_JPG, TRAINER_PNG, TRAINER_PDF],
    ids=["tc_ts01_upl_001_jpg", "tc_ts01_upl_002_png", "tc_ts01_upl_003_pdf"],
)
def test_upload_supported_format_accepted(form_page, file_path):
    """SCN001-003 — JPG/PNG/PDF uploads are accepted."""
    data = with_overrides(TD_TRAINER_001, id_document_path=file_path)
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("idDocument")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts01_upl_004_unsupported_format(form_page):
    """SCN004 — Unsupported format (.exe). Expected: format error."""
    data = with_overrides(TD_TRAINER_001, id_document_path=TRAINER_EXE)
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("idDocument")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts01_upl_005_file_size_exactly_10mb(form_page):
    """SCN005 — File size exactly 10 MB (10*1024*1024 bytes). Expected: accepted."""
    data = with_overrides(TD_TRAINER_001, id_document_path=TRAINER_PDF_10MB)
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("idDocument")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts01_upl_006_file_size_above_10mb(form_page):
    """SCN006 — File size 10 MB + 1 byte. Expected: file size validation shown."""
    data = with_overrides(TD_TRAINER_001, id_document_path=TRAINER_PDF_OVER_10MB)
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("idDocument")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ============================================================
# TS01-DOB: Date of Birth
# ============================================================

def test_tc_ts01_dob_001_valid_dob(form_page):
    """SCN001 — Valid DOB "01/01/1990". Expected: value accepted."""
    data = with_overrides(TD_TRAINER_001, dob="1990-01-01")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("dob")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


def test_tc_ts01_dob_002_future_date(form_page):
    """SCN002 — Future date. Expected: validation displayed."""
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    data = with_overrides(TD_TRAINER_001, dob=tomorrow)
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("dob")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ============================================================
# TS01-TAX: Tax Resident Status
# ============================================================

def test_tc_ts01_tax_001_tax_resident_yes(form_page):
    """SCN001 — Select Yes. Expected: selection retained."""
    form_page.select_tax_resident("Yes")
    assert form_page.is_radio_checked("Yes")


def test_tc_ts01_tax_002_tax_resident_no(form_page):
    """SCN002 — Select No. Expected: selection retained."""
    form_page.select_tax_resident("No")
    assert form_page.is_radio_checked("No")


def test_tc_ts01_tax_003_not_selected(form_page):
    """SCN003 — Left unselected. Expected: validation displayed on Save."""
    form_page.fill_form(without_keys(TD_TRAINER_001, "tax_resident"))
    form_page.submit()
    expect(form_page.error_locator("taxResident")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()
