"""F4.4 Applications list, School Admin (TC-059 to TC-068). Source: FS F4 v1.3 section 3.1 to 3.3."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data import seed
from data.ui_text import EMDASH

pytestmark = pytest.mark.f44

SCHOOL_NOTE = ("Tier is the SBFAS scheme your school grants. MOEFAS applications and income details are "
               "visible to MOE HQ only.")


def test_tc_059_school_admin_sees_only_sbfas_of_own_school(bvp_apps):
    """TC-059 School Admin sees only SBFAS applications of the own school."""
    bvp_apps.open_tab("All")
    bvp_apps.expect_ids(seed.BVP_IDS)
    for other in ("00412", "00410", "00390", "00301", "00377", "00328", "00381"):
        expect(bvp_apps.row(other)).to_have_count(0)


def test_tc_060_school_without_sbfas_sees_an_empty_list(mrs_apps):
    """TC-060 School Admin of a school without SBFAS applications sees an empty list."""
    mrs_apps.expect_empty()
    mrs_apps.expect_cards({"Pending": "0", "SBFAS approved": "0", "SBFAS rejected": "0"})
    expect(mrs_apps.row("00377")).to_have_count(0)


@pytest.mark.draft
def test_tc_061_school_cards_show_pending_approved_rejected(bvp_apps):
    """TC-061 School cards show Pending, SBFAS approved and SBFAS rejected for this year. ASM-R4-16."""
    bvp_apps.expect_cards(seed.BVP_CARDS)
    expect(bvp_apps.card_hint("Pending")).to_have_text("Pending SBFAS")
    expect(bvp_apps.card_hint("SBFAS approved")).to_have_text("This year")
    expect(bvp_apps.card_hint("SBFAS rejected")).to_have_text("This year")


def test_tc_063_school_tabs_open_on_pending_with_counts(bvp_apps):
    """TC-063 School tabs open on Pending and show counts (Rejected has no count)."""
    bvp_apps.expect_active_tab("Pending")
    bvp_apps.expect_tabs({"Pending": 1, "All": 2, "Approved": 1})
    expect(bvp_apps.tab_count("Rejected")).to_have_count(0)
    bvp_apps.expect_ids(["00398"])
    bvp_apps.open_tab("All")
    bvp_apps.expect_ids(["00398", "00386"])
    bvp_apps.open_tab("Approved")
    bvp_apps.expect_ids(["00386"])
    bvp_apps.open_tab("Rejected")
    bvp_apps.expect_empty()


def test_tc_065_school_table_columns_tier_before_ml(bvp_apps):
    """TC-065 School table has the columns with Tier before ML recommendation and no School, Scheme, System check."""
    assert bvp_apps.column_names() == seed.SCHOOL_COLUMNS + [""]
    for absent in ("SCHOOL", "SCHEME", "SYSTEM CHECK"):
        assert absent not in bvp_apps.column_names()


def test_tc_066_review_for_pending_and_view_for_decided(bvp_apps):
    """TC-066 Review shows for Pending SBFAS and View for decided ones. (The primary style is not asserted.)"""
    bvp_apps.open_tab("All")
    expect(bvp_apps.row_button("00398")).to_have_text("Review")
    expect(bvp_apps.row_button("00386")).to_have_text("View")
    drawer = bvp_apps.open("00386")
    assert drawer.action_buttons() == []
    expect(drawer.approve_button).to_have_count(0)
    expect(drawer.reject_button).to_have_count(0)


def test_tc_067_school_table_values_of_a_pending_and_an_approved_row(bvp_apps):
    """TC-067 School table values for a pending and an approved SBFAS row."""
    bvp_apps.open_tab("All")
    bvp_apps.expect_row("00398", GRADE="P2", SUBMITTED="14/10/2026", TIER="", ML_RECOMMENDATION=EMDASH,
                        ML_RISK="Medium", STATUS="Pending")
    bvp_apps.expect_row("00386", GRADE="P4", SUBMITTED="12/11/2025", TIER="Tier 3", ML_RECOMMENDATION="Tier 2",
                        ML_RISK="Medium", STATUS="Approved")


def test_tc_068_school_note_explains_tier_and_hq_only_data(bvp_apps):
    """TC-068 School list note explains Tier and MOE HQ only data."""
    expect(bvp_apps.note).to_have_text(SCHOOL_NOTE)
