"""F4.17 Close form now (demo) (TC-242 to TC-244). Source: FS F4 v1.3 section 6.7."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data import seed
from data.ui_text import ENDASH, MIDDOT
from pages.dialogs import CloseFormDialog
from pages.flows import close_form_now, open_hq_list

pytestmark = pytest.mark.f417


def test_tc_242_close_form_dialog_explains_what_will_happen(hq_schemes):
    """TC-242 Close form now (demo) dialog explains what will happen, Cancel changes nothing."""
    hq_schemes.action("MOEFAS 2027", "Close form now (demo)").click()
    dialog = CloseFormDialog(hq_schemes.page)
    dialog.expect_open()
    expect(dialog.title).to_have_text("Close the application form now?")
    expect(dialog.subtitle).to_have_text(f"DEMO ONLY {MIDDOT} MOEFAS 2027")
    expect(dialog.root).to_contain_text("In the real system this runs automatically when the form closes at the end "
                                        "of 31/12/2026.")
    expect(dialog.consequences).to_have_count(3)
    expect(dialog.consequences.nth(0)).to_contain_text("The form closes today. No more MOEFAS applications.")
    expect(dialog.consequences.nth(1)).to_contain_text("The system ranks the 3 waiting application(s) by need")
    expect(dialog.consequences.nth(2)).to_contain_text("rules met")
    expect(dialog.cancel_button).to_be_visible()
    expect(dialog.confirm_button).to_be_visible()
    dialog.cancel()
    expect(hq_schemes.cell("MOEFAS 2027", "APPLICATION FORM")).to_contain_text("3 waiting")


def test_tc_243_the_button_sets_form_closes_to_today_and_runs_the_assessment(hq):
    """TC-243 The button sets Form closes to today and runs the assessment."""
    schemes = close_form_now(hq)                       # also checks the toast text
    form = schemes.cell("MOEFAS 2027", "APPLICATION FORM")
    expect(form).to_contain_text(f"01/08/2026 {ENDASH} 18/10/2026")
    expect(form).to_contain_text("Assessed 18/10/2026")
    apps = open_hq_list(hq)
    apps.expect_cards(seed.HQ_CARDS_AFTER_CLOSE)
    apps.expect_tabs(seed.HQ_TABS_AFTER_CLOSE)


@pytest.mark.draft
def test_tc_244_the_button_is_offered_only_while_the_form_is_open(hq):
    """TC-244 The button is offered only while the form is Open. ASM-R4-01."""
    schemes = close_form_now(hq)
    assert "Close form now (demo)" not in schemes.actions("MOEFAS 2027")
