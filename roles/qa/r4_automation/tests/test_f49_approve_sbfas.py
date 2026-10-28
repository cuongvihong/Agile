"""F4.9 Approve SBFAS (TC-124 to TC-142). Source: FS F4 v1.3 section 5.
TC-125, TC-126, TC-133 and TC-138 need the F4 build and are listed in data/not_automated.py."""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data import ui_text as T
from data.ui_text import MIDDOT
from pages.applications_page import ApplicationsPage
from pages.flows import approve_sbfas, open_approve_dialog

pytestmark = pytest.mark.f49

DECIDED_BY = re.compile(r"^Lan Nguyen \(BVP-0012\) " + MIDDOT + r" \d{2}/\d{2}/\d{4} \d{2}:\d{2}$")


def test_tc_124_approve_dialog_shows_subtitle_candidate_tiers_and_buttons(bvp_apps):
    """TC-124 Approve dialog shows the subtitle, the candidate tiers and the buttons."""
    dialog = open_approve_dialog(bvp_apps)
    expect(dialog.title).to_have_text("Approve SBFAS")
    expect(dialog.subtitle).to_have_text(
        f"FUNCTION 4 {MIDDOT} SBFAS {MIDDOT} APP-2026-00398 {MIDDOT} Daniel Ong {MIDDOT} P2")
    assert dialog.tier_options() == ["Tier 1", "Tier 2", "Tier 3"]
    expect(dialog.counter).to_have_text("0/500")
    expect(dialog.cancel_button).to_be_visible()
    expect(dialog.confirm_button).to_be_visible()


def test_tc_127_candidate_tiers_are_sorted_by_name(bvp_apps):
    """TC-127 Candidate tiers are sorted by name."""
    dialog = open_approve_dialog(bvp_apps)
    options = dialog.tier_options()
    assert options == sorted(options) == ["Tier 1", "Tier 2", "Tier 3"]


def test_tc_128_cancel_closes_the_dialog_and_changes_nothing(bvp_apps):
    """TC-128 Cancel closes the dialog and changes nothing."""
    dialog = open_approve_dialog(bvp_apps)
    dialog.choose_tier("Tier 2")
    dialog.comment.fill("Draft note")
    dialog.cancel()
    bvp_apps.open_tab("All")
    bvp_apps.expect_row("00398", STATUS="Pending", TIER="")
    drawer = bvp_apps.open("00398")
    assert drawer.history_events() == ["Submitted", "SBFAS application (not eligible for MOEFAS by nationality)"]


def test_tc_129_ml_tier_is_preselected_with_a_hint(bvp_apps_after_close):
    """TC-129 ML tier is pre-selected with a hint (00412, ML Tier 3, after the demo close)."""
    dialog = open_approve_dialog(bvp_apps_after_close, "00412")
    assert dialog.selected_tier() == "Tier 3"
    expect(dialog.tier_hint).to_have_text("ML suggests Tier 3")


def test_tc_130_without_ml_tier_last_scheme_is_preselected_and_no_hint(bvp_apps):
    """TC-130 Without an ML tier the last scheme is pre-selected and no hint is shown."""
    dialog = open_approve_dialog(bvp_apps, "00398")
    assert dialog.selected_tier() == "Tier 3"
    expect(dialog.tier_hint).to_have_count(0)


@pytest.mark.draft
def test_tc_131_school_admin_may_choose_a_tier_other_than_the_recommendation(bvp_apps_after_close):
    """TC-131 The School Admin may choose a tier other than the recommendation. ASM-R4-03."""
    apps = bvp_apps_after_close
    dialog = open_approve_dialog(apps, "00412")
    dialog.choose_tier("Tier 2")
    dialog.confirm()
    dialog.expect_closed()
    apps.open_tab("All")
    apps.expect_row("00412", TIER="Tier 2", ML_RECOMMENDATION="Tier 3", STATUS="Approved")
    expect(apps.open("00412").value("DECISION", "Tier")).to_contain_text("Tier 2")


@pytest.mark.draft
def test_tc_132_household_that_meets_no_scheme_can_still_be_approved(bvp_apps):
    """TC-132 A household that meets no scheme can still be approved by the school. ASM-R4-03."""
    dialog = open_approve_dialog(bvp_apps, "00398")
    dialog.confirm()
    dialog.expect_closed()
    bvp_apps.open_tab("All")
    bvp_apps.expect_row("00398", STATUS="Approved", TIER="Tier 3")
    expect(bvp_apps.open("00398").value("DECISION", "Tier")).to_contain_text("Tier 3")


def test_tc_134_comment_is_optional(bvp, bvp_apps):
    """TC-134 Comment is optional: the approval is accepted and the Decision block has no Comment line."""
    approve_sbfas(bvp, "00398")
    bvp_apps.open_tab("All")
    drawer = bvp_apps.open("00398")
    expect(drawer.row("DECISION", "Result")).to_be_visible()
    expect(drawer.row("DECISION", "Comment")).to_have_count(0)


def test_tc_135_comment_accepts_500_characters_and_blocks_501(bvp_apps):
    """TC-135 Comment accepts 500 characters and blocks 501."""
    dialog = open_approve_dialog(bvp_apps)
    for length in (499, 500):
        dialog.comment.fill("a" * length)
        expect(dialog.counter).to_have_text(f"{length}/500")
        expect(dialog.confirm_button).to_be_enabled()
    dialog.comment.fill("a" * 501)
    expect(dialog.counter).to_have_text("501/500")
    expect(dialog.confirm_button).to_be_disabled()


@pytest.mark.draft
def test_tc_136_comment_with_markup_is_saved_as_plain_text(bvp_apps):
    """TC-136 Comment with markup is saved as plain text. ASM-R4-18."""
    text = "<b>ok</b><script>alert(1)</script>"
    alerts = []
    bvp_apps.page.on("dialog", lambda d: (alerts.append(d.message), d.dismiss()))
    dialog = open_approve_dialog(bvp_apps)
    dialog.comment.fill(text)
    dialog.confirm()
    dialog.expect_closed()
    bvp_apps.open_tab("All")
    expect(bvp_apps.open("00398").value("DECISION", "Comment")).to_have_text(text)
    assert alerts == []


def test_tc_137_confirm_approval_saves_tier_date_and_decider(bvp, bvp_apps):
    """TC-137 Confirm approval saves the tier, the date and the decider."""
    approve_sbfas(bvp, "00398", tier="Tier 2", comment="Approved after review")
    bvp.expect_toast(T.TOAST_SUBSIDY)
    expect(bvp_apps.page.locator("aside.drawer")).to_have_count(0)
    bvp_apps.open_tab("All")
    bvp_apps.expect_row("00398", TIER="Tier 2", STATUS="Approved")
    expect(bvp_apps.row_button("00398")).to_have_text("View")
    drawer = bvp_apps.open("00398")
    drawer.expect_value("DECISION", "Result", "Approved")
    drawer.expect_value("DECISION", "Tier", f"Tier 2 {MIDDOT} from 01/01/2027")
    drawer.expect_value("DECISION", "Comment", "Approved after review")
    expect(drawer.value("DECISION", "Decided by")).to_have_text(DECIDED_BY)


@pytest.mark.draft
def test_tc_139_history_lists_the_approval_and_the_email(bvp, bvp_apps):
    """TC-139 History lists the approval and the email. ASM-R4-13."""
    approve_sbfas(bvp, "00398", tier="Tier 2")
    bvp_apps.open_tab("All")
    events = bvp_apps.open("00398").history_events()
    assert events[-2:] == [f"Approved {MIDDOT} Tier 2 {MIDDOT} from 01/01/2027", "Email with result sent to parent"]


def test_tc_140_cards_and_tab_counts_update_after_the_approval(bvp, bvp_apps):
    """TC-140 Cards and tab counts update after the approval."""
    approve_sbfas(bvp, "00398", tier="Tier 2")
    bvp_apps.expect_cards({"Pending": "0", "SBFAS approved": "2", "SBFAS rejected": "0"})
    bvp_apps.expect_tabs({"All": 2, "Approved": 2})
    expect(bvp_apps.tab_count("Pending")).to_have_count(0)
    bvp_apps.open_tab("Pending")
    bvp_apps.expect_empty()


def test_tc_141_hq_counts_update_after_a_school_approval(bvp, bvp_apps):
    """TC-141 MOE HQ counts update after a school approval."""
    approve_sbfas(bvp, "00398", tier="Tier 2")
    bvp.log_out()
    bvp.sign_in_hq()
    bvp.go("FAS applications")
    hq = ApplicationsPage(bvp.page)
    hq.expect_cards({"Total applications": "9", "MOEFAS approved": "3", "Approved": "5", "Rejected": "1"})
    hq.expect_row("00398", STATUS="Approved", TIER="Tier 2")
    assert hq.open("00398").action_buttons() == []


def test_tc_142_an_approved_application_is_read_only(bvp, bvp_apps):
    """TC-142 An approved application is read only."""
    approve_sbfas(bvp, "00398", tier="Tier 2")
    bvp_apps.open_tab("All")
    drawer = bvp_apps.open("00398")
    assert drawer.action_buttons() == []
    expect(drawer.root.locator("input, textarea, select")).to_have_count(0)
