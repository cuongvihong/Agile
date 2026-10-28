"""Test suite for the Curricula "Create Trainer Account" form.

Scenario IDs (TS-xx) reference
docs/SESSION_01_ANALYSIS_AND_REQUIREMENTS.md, §5 — the source of truth for
expected behavior. Nothing here asserts a result that wasn't derived from
reading the AUT's actual markup/script.
"""
from __future__ import annotations

import datetime
import re

import pytest
from playwright.sync_api import expect

from data.test_data import (
    INVALID_TYPE_DOCUMENT,
    VALID_NON_SG_DATA,
    VALID_SG_DATA,
    with_overrides,
    without_keys,
)

TRAINER_ID_PATTERN = re.compile(r"Trainer ID: TRN\d{6}")


# ---------------------------------------------------------------- TS-01/02 --
def test_ts01_valid_submission_singapore_resident(form_page):
    # Arrange
    data = VALID_SG_DATA

    # Act
    form_page.fill_form(data)
    form_page.submit()

    # Assert
    expect(form_page.success_box).to_be_visible()
    text = form_page.success_text()
    assert "Trainer account has been created successfully." in text
    assert TRAINER_ID_PATTERN.search(text), text
    assert "Status: Active" in text
    # block/street were left out of VALID_SG_DATA on purpose, so a correct
    # value here also proves the AUT's own postal-code auto-fill ran
    # (Session 01 doc, §2) rather than the value being hardcoded by the test.
    expect(form_page.block_number_input).to_have_value("142")
    expect(form_page.street_name_input).to_have_value("Commonwealth Drive")


def test_ts02_valid_submission_non_singapore_resident(form_page):
    # Arrange
    data = VALID_NON_SG_DATA

    # Act
    form_page.fill_form(data)
    form_page.submit()

    # Assert
    expect(form_page.success_box).to_be_visible()
    assert TRAINER_ID_PATTERN.search(form_page.success_text())
    # TS-13: the postal code field stays visible in this branch but is never
    # required/validated, even though it was left blank.
    expect(form_page.error_locator("postalCode")).to_be_hidden()


# -------------------------------------------------------------------- TS-03 --
def test_ts03_all_required_fields_empty(form_page):
    # Arrange: page freshly loaded, nothing filled (default branch = Singapore)
    required_error_keys = [
        "preferredName", "gender", "idType", "idNumber", "idDocument",
        "nationality", "dob", "race", "birthCountry", "taxResident",
        "primaryEmail", "primaryPhone",
        "emergencyName", "emergencyRelationship", "emergencyPhone",
        "postalCode", "blockNumber", "streetName", "floorUnit",
    ]

    # Act
    form_page.submit()

    # Assert
    for key in required_error_keys:
        expect(form_page.error_locator(key)).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ------------------------------------------------------- single-field breaks --
# Each case starts from a fully valid dataset and breaks exactly one field,
# so the resulting error is unambiguous — avoids duplicating an entire
# form-filling dataset per scenario.
SINGLE_FIELD_BREAK_CASES = [
    pytest.param(
        {"primary_email": "not-an-email"}, "primaryEmail", id="ts04-invalid-email"
    ),
    pytest.param(
        {"primary_phone": "1234567"},  # 7 digits, +65 requires exactly 8
        "primaryPhone",
        id="ts05-primary-phone-wrong-length",
    ),
    pytest.param(
        {"secondary_phone": "123", "secondary_phone_code": "+65"},
        "secondaryPhone",
        id="ts07-secondary-phone-invalid",
    ),
    pytest.param(
        {"postal_code": "ABC123", "block_number": "10", "street_name": "Test Street"},
        "postalCode",
        id="ts09-invalid-postal-code-format",
    ),
    pytest.param(
        {"floor_number": "", "unit_number": ""},
        "floorUnit",
        id="ts10-floor-unit-blank",
    ),
    pytest.param(
        {"id_document_path": INVALID_TYPE_DOCUMENT},
        "idDocument",
        id="ts14-file-wrong-type",
    ),
]


@pytest.mark.parametrize("override, error_key", SINGLE_FIELD_BREAK_CASES)
def test_single_invalid_field_blocks_submission(form_page, override, error_key):
    # Arrange
    data = with_overrides(VALID_SG_DATA, **override)

    # Act
    form_page.fill_form(data)
    form_page.submit()

    # Assert
    expect(form_page.error_locator(error_key)).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# -------------------------------------------------------------------- TS-06 --
def test_ts06_secondary_phone_optional_when_blank(form_page):
    # Arrange: VALID_SG_DATA never sets secondary_phone at all
    data = VALID_SG_DATA

    # Act
    form_page.fill_form(data)
    form_page.submit()

    # Assert
    expect(form_page.error_locator("secondaryPhone")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


# -------------------------------------------------------------------- TS-08 --
def test_ts08_dob_in_future_is_rejected(form_page):
    # Arrange
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    data = with_overrides(VALID_SG_DATA, dob=tomorrow)

    # Act
    form_page.fill_form(data)
    form_page.submit()

    # Assert
    expect(form_page.error_locator("dob")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# -------------------------------------------------------------------- TS-11 --
def test_ts11_floor_not_applicable_checkbox_bypasses_validation(form_page):
    # Arrange
    data = with_overrides(
        VALID_SG_DATA, floor_number="", unit_number="", floor_not_applicable=True
    )

    # Act
    form_page.fill_form(data)

    # Assert (intermediate): checking the box disables both inputs
    expect(form_page.floor_number_input).to_be_disabled()
    expect(form_page.unit_number_input).to_be_disabled()

    # Act
    form_page.submit()

    # Assert
    expect(form_page.error_locator("floorUnit")).to_be_hidden()
    expect(form_page.success_box).to_be_visible()


# -------------------------------------------------------------------- TS-12 --
def test_ts12_non_singapore_required_fields_missing(form_page):
    # Arrange
    data = with_overrides(VALID_NON_SG_DATA, address1="", city="")

    # Act
    form_page.fill_form(data)
    form_page.submit()

    # Assert
    expect(form_page.error_locator("address1")).to_be_visible()
    expect(form_page.error_locator("city")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# -------------------------------------------------------------------- TS-15 --
def test_ts15_id_document_not_selected(form_page):
    # Arrange: remove the key entirely (not blank) — the input must never
    # receive set_input_files() at all for this scenario.
    data = without_keys(VALID_SG_DATA, "id_document_path")

    # Act
    form_page.fill_form(data)
    form_page.submit()

    # Assert
    expect(form_page.error_locator("idDocument")).to_be_visible()
    expect(form_page.success_box).to_be_hidden()


# ---------------------------------------------------------------- TS-16/17 --
def test_ts16_cancel_without_data_reloads_without_dialog(form_page):
    # Arrange: nothing typed/selected — the AUT's own hasData check should
    # be false, so no confirm() should fire at all.
    page = form_page.page
    dialogs_seen = []

    def record_and_dismiss(dialog):
        dialogs_seen.append(dialog.message)
        dialog.dismiss()

    page.on("dialog", record_and_dismiss)

    # Act
    with page.expect_navigation():
        form_page.cancel()

    # Assert
    assert dialogs_seen == []


def test_ts17_cancel_with_data_dismiss_keeps_value(form_page):
    # Arrange
    form_page.set_preferred_name("Temp Value")
    form_page.page.once("dialog", lambda dialog: dialog.dismiss())

    # Act
    form_page.cancel()

    # Assert: dismissing the confirm must leave the page (and value) as-is
    expect(form_page.preferred_name_input).to_have_value("Temp Value")


def test_ts17_cancel_with_data_accept_reloads_and_clears(form_page):
    # Arrange
    form_page.set_preferred_name("Temp Value")
    form_page.page.once("dialog", lambda dialog: dialog.accept())

    # Act
    with form_page.page.expect_navigation():
        form_page.cancel()

    # Assert: accepting the confirm reloads the page, clearing the value
    expect(form_page.preferred_name_input).to_have_value("")


# -------------------------------------------------------------------- TS-18 --
def test_ts18_postal_code_autofill_only_for_known_codes(form_page):
    # Arrange / Act
    form_page.set_postal_code("999999")

    # Assert
    expect(form_page.block_number_input).to_have_value("")
    expect(form_page.street_name_input).to_have_value("")
