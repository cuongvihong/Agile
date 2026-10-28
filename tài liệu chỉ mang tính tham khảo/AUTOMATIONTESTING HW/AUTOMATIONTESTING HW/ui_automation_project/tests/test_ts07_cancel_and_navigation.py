"""TS-07: Cancel and Navigation — official 186-test-case library.

Source of truth: TS07.xlsx at the workspace root, cross-checked against
FSD_Trainer_Account_Creation.docx §5.4. All 12 official cases are recorded
Passed or Blocked — none Failed, so nothing in this file is expected to
fail. 2 are Blocked (CANCEL-001, DIALOG-002): both have a compound
Expected Result whose second half ("returned to Trainer Listing page")
cannot be verified because this standalone static-HTML build has no
separate Trainer Listing page at all — only the Create Trainer form
exists. Skipped with a cited reason, not asserted around.
"""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data.test_data import TD_TRAINER_001, TRAINER_PDF, with_overrides

pytestmark = pytest.mark.ts07

_NO_LISTING_PAGE_SKIP = (
    "BLOCKED (official suite): this standalone build has no separate "
    "Trainer Listing page to navigate to/from — only the Create Trainer "
    "form exists. The other half of this TC's Expected Result (no warning "
    "for CANCEL-001; data discarded for DIALOG-002) is independently "
    "testable and IS covered elsewhere in this suite, but the compound "
    "Expected Result as officially written cannot be verified in full."
)


# ============================================================
# TS07-CANCEL: Cancel Navigation
# ============================================================

@pytest.mark.skip(reason=_NO_LISTING_PAGE_SKIP)
def test_tc_ts07_cancel_001_cancel_without_changes(form_page):
    """SCN001 — Cancel with no data entered. Cannot be fully automated
    (see skip reason). The "no warning shown" half is covered by
    test_ts01..06's own Cancel-without-data checks in prior sessions."""


def test_tc_ts07_cancel_002_cancel_after_preferred_name_entered(form_page):
    """SCN002 — Enter Preferred Name, click Cancel. Expected: unsaved
    changes confirmation dialog displayed (native browser confirm())."""
    form_page.set_preferred_name("John Tan")
    dialog_seen = []
    form_page.page.once("dialog", lambda d: (dialog_seen.append(d.message), d.dismiss()))
    form_page.cancel()
    assert dialog_seen, "expected a confirm() dialog to fire"


def test_tc_ts07_cancel_003_cancel_after_full_form_entry(form_page):
    """SCN003 — Populate multiple fields, click Cancel. Expected: unsaved
    changes confirmation dialog displayed."""
    form_page.fill_form(TD_TRAINER_001)
    dialog_seen = []
    form_page.page.once("dialog", lambda d: (dialog_seen.append(d.message), d.dismiss()))
    form_page.cancel()
    assert dialog_seen, "expected a confirm() dialog to fire"


# ============================================================
# TS07-DIALOG: Confirmation Dialog
# ============================================================

def test_tc_ts07_dialog_001_select_stay(form_page):
    """SCN001 — Enter data, Cancel, select Stay (dismiss the confirm).
    Expected: dialog closes, user remains, entered data preserved."""
    form_page.set_preferred_name("John Tan")
    form_page.page.once("dialog", lambda d: d.dismiss())
    form_page.cancel()
    expect(form_page.preferred_name_input).to_have_value("John Tan")


@pytest.mark.skip(reason=_NO_LISTING_PAGE_SKIP)
def test_tc_ts07_dialog_002_select_leave(form_page):
    """SCN002 — Enter data, Cancel, select Leave. Cannot be fully
    automated (see skip reason). The "data discarded" half is covered by
    test_tc_ts07_nav_001_open_form_again_after_leave below."""


def test_tc_ts07_dialog_003_dialog_message_validation(form_page):
    """SCN003 — FSD §5.4 states the exact message. Expected: the build's
    native confirm() text matches it exactly."""
    form_page.set_preferred_name("John Tan")
    dialog_message = []
    form_page.page.once("dialog", lambda d: (dialog_message.append(d.message), d.dismiss()))
    form_page.cancel()
    assert dialog_message == [
        "You have unsaved changes. Are you sure you want to leave this page?"
    ]


# ============================================================
# TS07-STATE: Unsaved Change Detection
# ============================================================

def test_tc_ts07_state_001_text_field_change(form_page):
    """SCN001 — Enter Preferred Name, Cancel. Expected: warning appears."""
    form_page.set_preferred_name("John Tan")
    dialog_seen = []
    form_page.page.once("dialog", lambda d: (dialog_seen.append(True), d.dismiss()))
    form_page.cancel()
    assert dialog_seen


def test_tc_ts07_state_002_email_field_change(form_page):
    """SCN002 — Enter email, Cancel. Expected: warning appears."""
    form_page.set_primary_email("trainer@example.com")
    dialog_seen = []
    form_page.page.once("dialog", lambda d: (dialog_seen.append(True), d.dismiss()))
    form_page.cancel()
    assert dialog_seen


def test_tc_ts07_state_003_date_field_change(form_page):
    """SCN003 — Select Date of Birth, Cancel. Expected: warning appears."""
    form_page.set_dob("1990-01-01")
    dialog_seen = []
    form_page.page.once("dialog", lambda d: (dialog_seen.append(True), d.dismiss()))
    form_page.cancel()
    assert dialog_seen


def test_tc_ts07_state_004_file_upload_change(form_page):
    """SCN004 — Upload identification document, Cancel. Expected: warning
    appears (the AUT's hasData check explicitly includes the file input's
    files.length, not just text/email/date fields)."""
    form_page.upload_id_document(TRAINER_PDF)
    dialog_seen = []
    form_page.page.once("dialog", lambda d: (dialog_seen.append(True), d.dismiss()))
    form_page.cancel()
    assert dialog_seen


# ============================================================
# TS07-NAV: Post Cancel State
# ============================================================

def test_tc_ts07_nav_001_open_form_again_after_leave(form_page):
    """SCN001 — Enter data, Cancel, select Leave (accept the confirm),
    reopen. Expected: form loads without previously entered data."""
    form_page.set_preferred_name("John Tan")
    form_page.page.once("dialog", lambda d: d.accept())
    form_page.cancel()  # accept() triggers location.reload()
    expect(form_page.preferred_name_input).to_have_value("")


def test_tc_ts07_nav_002_stay_then_continue_editing(form_page):
    """SCN002 — Enter data, Cancel, select Stay, keep editing. Expected:
    existing values remain available and editable."""
    data = with_overrides(TD_TRAINER_001, preferred_name="John Tan")
    form_page.fill_form(data)
    form_page.page.once("dialog", lambda d: d.dismiss())
    form_page.cancel()
    expect(form_page.preferred_name_input).to_have_value("John Tan")
    # Continue editing: the field must still accept new input afterward.
    form_page.set_preferred_name("Jane Tan")
    expect(form_page.preferred_name_input).to_have_value("Jane Tan")
