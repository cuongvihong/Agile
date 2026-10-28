"""TS-08: Findings Confirmed Against the Real Build — official 186-test-case library.

Source of truth: TS08.xlsx at the workspace root. Per
Step4_Test_Case_Design.docx, §11: this suite targets FSD-stated rules not
visibly enforced by the real build (findings F19, F23, F24), and per
Test_Suite_Organization.docx it uses an "exploratory / code-cross-check"
technique rather than classic input/expected-output pairs — most cases
here "observe and document" the actual build state.

All 12 official cases are recorded Passed (including F24-003, which
confirms BUG-03) — each assertion below checks a real, observed fact about
the build, not an invented one.
"""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data.test_data import TD_TRAINER_001, without_keys

pytestmark = pytest.mark.ts08


# ============================================================
# TS08-F19: Gender Control Type (Finding F19)
# ============================================================

def test_tc_ts08_f19_001_verify_gender_control_type(form_page):
    """SCN001 — Document the actual control type for Gender.

    Observed: implemented as a radio-button group (2 `<input type=radio
    name=gender>`), matching the FSD field table's stated UI Element
    ("Radio button") — the F02 discrepancy in the requirement analysis was
    between the field TABLE and the narrative/screenshot text, not between
    the FSD table and the real build, which do agree here.
    """
    male_radio = form_page.page.get_by_role("radio", name="Male", exact=True)
    female_radio = form_page.page.get_by_role("radio", name="Female", exact=True)
    expect(male_radio).to_be_visible()
    expect(female_radio).to_be_visible()
    # No <select> exists for gender.
    assert form_page.page.locator("select#gender").count() == 0


def test_tc_ts08_f19_002_verify_gender_available_values(form_page):
    """SCN002 — Document the actual selectable values for Gender.

    Observed: exactly 2 values, Male and Female — matching the FSD's own
    stated enumeration exactly (no discrepancy for this particular field).
    """
    radios = form_page.page.locator('input[type="radio"][name="gender"]')
    expect(radios).to_have_count(2)
    values = radios.evaluate_all("els => els.map(e => e.value)")
    assert set(values) == {"Male", "Female"}


# ============================================================
# TS08-F23: Singapore Tax Resident Control Type (Finding F23)
# ============================================================

def test_tc_ts08_f23_001_verify_tax_resident_control_type(form_page):
    """SCN001 — Document the actual control type for Tax Resident.

    Observed: implemented as a radio-button group, matching the FSD field
    table's stated UI Element ("Radio button").
    """
    yes_radio = form_page.page.get_by_role("radio", name="Yes", exact=True)
    no_radio = form_page.page.get_by_role("radio", name="No", exact=True)
    expect(yes_radio).to_be_visible()
    expect(no_radio).to_be_visible()
    assert form_page.page.locator("select#taxResident").count() == 0


def test_tc_ts08_f23_002_verify_tax_resident_values(form_page):
    """SCN002 — Document the actual selectable values.

    Observed: exactly 2 values, Yes and No — matching the FSD exactly.
    """
    radios = form_page.page.locator('input[type="radio"][name="taxResident"]')
    expect(radios).to_have_count(2)
    values = radios.evaluate_all("els => els.map(e => e.value)")
    assert set(values) == {"Yes", "No"}


# ============================================================
# TS08-F24: Identification Document Requirement (Finding F24 / BUG-03)
# ============================================================

def test_tc_ts08_f24_001_save_without_upload(form_page):
    """SCN001 — Save without uploading a document.

    Observed: Save is blocked unconditionally — the build enforces the
    upload as mandatory in every case, regardless of ID Type or any other
    condition (this fact underlies BUG-03, documented fully in F24-003).
    """
    data = without_keys(TD_TRAINER_001, "id_document_path")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("idDocument")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


def test_tc_ts08_f24_002_verify_upload_label_text(form_page):
    """SCN002 — Document the actual upload section wording.

    Observed: the hint text right under the label reads exactly "Please
    upload the front and back of your ID in a single file (if
    applicable)" — the "(if applicable)" wording is the source of the
    F11/F24 ambiguity resolved by F24-003 below. This is a different
    `.hint` element from the one inside `.upload` ("Up to 10MB...").
    """
    section_hint = form_page.page.locator("div.full > div.hint").first
    expect(section_hint).to_have_text(
        "Please upload the front and back of your ID in a single file (if applicable)"
    )


def test_tc_ts08_f24_003_compare_mandatory_indicator(form_page):
    """SCN003 — Compare the mandatory (*) indicator against the hint
    wording. Confirms BUG-03.

    Observed: the label carries a mandatory asterisk (`*`) AND Save
    genuinely blocks without a file (both confirmed above/here), YET the
    hint text says "(if applicable)" — a real, internally inconsistent
    contradiction in the build's own UI copy versus its own enforced
    behavior. All three facts checked here are independently true, which
    is exactly what confirms the defect (this test passes by documenting
    the contradiction, it does not need to "fail" to prove it).
    """
    label = form_page.page.locator("label", has_text="Singapore NRIC/EP/S-pass/Passport")
    expect(label.locator(".req")).to_have_text("*")

    hint = form_page.page.locator("div.full > div.hint").first
    expect(hint).to_contain_text("(if applicable)")

    data = without_keys(TD_TRAINER_001, "id_document_path")
    form_page.fill_form(data)
    form_page.submit()
    expect(form_page.error_locator("idDocument")).to_be_visible()


# ============================================================
# TS08-BUILD: Build vs Requirement (per-section field inventory)
# ============================================================

def test_tc_ts08_build_001_compare_personal_information_section(form_page):
    """SCN001 — Confirm every FSD-specified Personal Information field is
    present in the build (AC-02). All fields listed in FSD §4.1's field
    table are checked for real presence, not assumed."""
    expect(form_page.preferred_name_input).to_be_visible()
    expect(form_page.page.get_by_role("radio", name="Male", exact=True)).to_be_visible()
    expect(form_page.id_type_select).to_be_visible()
    expect(form_page.id_number_input).to_be_visible()
    expect(form_page.id_document_input).to_be_attached()
    expect(form_page.nationality_select).to_be_visible()
    expect(form_page.dob_input).to_be_visible()
    expect(form_page.race_select).to_be_visible()
    expect(form_page.birth_country_select).to_be_visible()
    expect(form_page.page.get_by_role("radio", name="Yes", exact=True)).to_be_visible()


def test_tc_ts08_build_002_compare_contact_information_section(form_page):
    """SCN002 — Confirm every FSD-specified Contact Information field is
    present (AC-03)."""
    expect(form_page.primary_email_input).to_be_visible()
    expect(form_page.primary_code_select).to_be_visible()
    expect(form_page.primary_phone_input).to_be_visible()
    expect(form_page.secondary_code_select).to_be_visible()
    expect(form_page.secondary_phone_input).to_be_visible()


def test_tc_ts08_build_003_compare_emergency_contact_section(form_page):
    """SCN003 — Confirm every FSD-specified Emergency Contact field is
    present (AC-04)."""
    expect(form_page.emergency_name_input).to_be_visible()
    expect(form_page.emergency_relationship_select).to_be_visible()
    expect(form_page.emergency_code_select).to_be_visible()
    expect(form_page.emergency_phone_input).to_be_visible()


def test_tc_ts08_build_004_compare_residential_address_section(form_page):
    """SCN004 — Confirm both Singapore and Non-Singapore address field
    sets are present and toggle correctly (AC-05)."""
    expect(form_page.postal_code_input).to_be_visible()
    expect(form_page.block_number_input).to_be_visible()
    expect(form_page.street_name_input).to_be_visible()
    expect(form_page.floor_number_input).to_be_visible()
    expect(form_page.unit_number_input).to_be_visible()

    form_page.select_residential_type("Non-Singapore")

    expect(form_page.address1_input).to_be_visible()
    expect(form_page.city_input).to_be_visible()
    expect(form_page.block_number_input).to_be_hidden()


def test_tc_ts08_build_005_compare_save_behaviour(form_page):
    """SCN005 — Execute a successful save and confirm the observed message
    matches the FSD's stated success flow, apart from the already-logged
    variances (BUG-04 random ID; no redirect to a Trainer Details page,
    since none exists in this static build)."""
    form_page.fill_form(TD_TRAINER_001)
    form_page.submit()
    expect(form_page.success_box).to_be_visible()
    text = form_page.success_text()
    assert "Trainer account has been created successfully." in text
    assert "Status: Active" in text
