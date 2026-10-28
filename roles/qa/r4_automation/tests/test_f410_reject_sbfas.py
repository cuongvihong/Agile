"""F4.10 Reject SBFAS (TC-143 to TC-152). Source: FS F4 v1.3 section 5.
TC-151 needs the F4 build and is listed in data/not_automated.py."""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data.ui_text import MIDDOT
from pages.flows import open_reject_dialog, reject_sbfas

pytestmark = pytest.mark.f410

REASONS = ["Income above limit", "Not eligible nationality", "Incomplete documents", "Other"]
DECIDED_BY = re.compile(r"^Lan Nguyen \(BVP-0012\) " + MIDDOT + r" \d{2}/\d{2}/\d{4} \d{2}:\d{2}$")
COMMENT = "Household income is above the limit of every tier."


def test_tc_143_reject_dialog_shows_reasons_hint_and_disabled_button(bvp_apps):
    """TC-143 Reject dialog shows the reasons, the hint and the disabled button."""
    dialog = open_reject_dialog(bvp_apps)
    expect(dialog.title).to_have_text("Reject application")
    expect(dialog.subtitle).to_have_text(
        f"FUNCTION 4 {MIDDOT} SBFAS {MIDDOT} APP-2026-00398 {MIDDOT} Daniel Ong {MIDDOT} P2")
    assert dialog.reason_options() == ["Select reason"] + REASONS
    expect(dialog.reason.locator("option:checked")).to_have_text("Select reason")
    expect(dialog.reason_hint).to_have_text("Reasons: " + f" {MIDDOT} ".join(REASONS))
    expect(dialog.comment).to_be_visible()
    expect(dialog.counter).to_have_text("0/500")
    expect(dialog.reject_button).to_be_disabled()


def test_tc_144_reject_stays_disabled_until_reason_and_comment_are_filled(bvp_apps):
    """TC-144 Reject stays disabled until both reason and comment are filled."""
    dialog = open_reject_dialog(bvp_apps)
    expect(dialog.reject_button).to_be_disabled()                       # empty
    dialog.choose_reason("Other")
    expect(dialog.reject_button).to_be_disabled()                       # reason only
    dialog.choose_reason("Select reason")
    dialog.comment.fill("Some text")
    expect(dialog.reject_button).to_be_disabled()                       # comment only
    dialog.choose_reason("Other")
    dialog.comment.fill("     ")
    expect(dialog.reject_button).to_be_disabled()                       # spaces only
    dialog.comment.fill("Some text")
    expect(dialog.reject_button).to_be_enabled()                        # reason with comment


def test_tc_145_reject_comment_accepts_500_characters_and_blocks_501(bvp_apps):
    """TC-145 Reject comment accepts 500 characters and blocks 501."""
    dialog = open_reject_dialog(bvp_apps)
    dialog.choose_reason("Other")
    for length in (499, 500):
        dialog.comment.fill("a" * length)
        expect(dialog.counter).to_have_text(f"{length}/500")
        expect(dialog.reject_button).to_be_enabled()
    dialog.comment.fill("a" * 501)
    expect(dialog.counter).to_have_text("501/500")
    expect(dialog.reject_button).to_be_disabled()


@pytest.mark.parametrize("reason", REASONS)
def test_tc_146_each_reason_value_is_accepted(bvp, bvp_apps, reason):
    """TC-146 Each reason value is accepted (each test starts from the base state, like Reset data)."""
    reject_sbfas(bvp, "00398", reason=reason, comment="Checked by QA.")
    bvp_apps.open_tab("Rejected")
    drawer = bvp_apps.open("00398")
    drawer.expect_value("DECISION", "Reason", reason)


def test_tc_147_cancel_closes_the_reject_dialog_and_changes_nothing(bvp_apps):
    """TC-147 Cancel closes the reject dialog and changes nothing."""
    dialog = open_reject_dialog(bvp_apps)
    dialog.choose_reason("Other")
    dialog.comment.fill("Draft note")
    dialog.cancel()
    bvp_apps.expect_ids(["00398"])
    bvp_apps.expect_row("00398", STATUS="Pending")
    drawer = bvp_apps.open("00398")
    assert drawer.history_events() == ["Submitted", "SBFAS application (not eligible for MOEFAS by nationality)"]


def test_tc_148_reject_saves_reason_comment_and_decider(bvp, bvp_apps):
    """TC-148 Reject saves the reason, the comment and the decider."""
    reject_sbfas(bvp, "00398", reason="Income above limit", comment=COMMENT)
    bvp_apps.open_tab("Rejected")
    bvp_apps.expect_row("00398", STATUS="Rejected", TIER="")
    drawer = bvp_apps.open("00398")
    drawer.expect_value("DECISION", "Result", "Rejected")
    drawer.expect_value("DECISION", "Reason", "Income above limit")
    drawer.expect_value("DECISION", "Comment", COMMENT)
    expect(drawer.value("DECISION", "Decided by")).to_have_text(DECIDED_BY)


@pytest.mark.draft
def test_tc_149_history_lists_the_rejection_and_the_email_with_reason(bvp, bvp_apps):
    """TC-149 History lists the rejection and the email with the reason. ASM-R4-13."""
    reject_sbfas(bvp, "00398", reason="Income above limit", comment=COMMENT)
    bvp_apps.open_tab("Rejected")
    events = bvp_apps.open("00398").history_events()
    assert events[-2:] == [f"Rejected {MIDDOT} Income above limit", "Email with reason sent to parent"]


def test_tc_150_cards_and_tabs_update_after_the_rejection(bvp, bvp_apps):
    """TC-150 Cards and tabs update after the rejection."""
    reject_sbfas(bvp, "00398")
    bvp_apps.expect_cards({"Pending": "0", "SBFAS approved": "1", "SBFAS rejected": "1"})
    bvp_apps.expect_tabs({"All": 2, "Approved": 1, "Rejected": 1})
    expect(bvp_apps.tab_count("Pending")).to_have_count(0)


def test_tc_152_a_rejected_application_is_read_only(bvp, bvp_apps):
    """TC-152 A rejected application is read only."""
    reject_sbfas(bvp, "00398")
    bvp_apps.open_tab("Rejected")
    drawer = bvp_apps.open("00398")
    assert drawer.action_buttons() == []
    expect(drawer.root.locator("input, textarea, select")).to_have_count(0)
