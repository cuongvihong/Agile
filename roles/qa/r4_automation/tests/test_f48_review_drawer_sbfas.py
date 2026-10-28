"""F4.8 Review drawer, SBFAS (TC-114 to TC-123). Source: FS F4 v1.3 section 5.
TC-119 and TC-123 need the F4 build and are listed in data/not_automated.py."""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data.ui_text import EMDASH, MIDDOT
from pages.base_page import soft
from pages.dialogs import ApproveDialog

pytestmark = pytest.mark.f48


@pytest.mark.draft
def test_tc_114_school_drawer_shows_all_blocks(bvp_apps):
    """TC-114 School Admin drawer shows student, parent, household, context, ML, documents and history."""
    drawer = bvp_apps.open("00398")
    expect(drawer.eyebrow).to_have_text("SBFAS REVIEW")
    expect(drawer.title).to_have_text("APP-2026-00398")
    expect(drawer.subtitle).to_have_text(f"Daniel Ong {MIDDOT} P2")
    names = drawer.section_names()
    assert names == ["STUDENT", "PARENT", "HOUSEHOLD AND INCOME", "CONTEXT", "ML RECOMMENDATION",
                     "DOCUMENTS", "HISTORY"], names
    drawer.expect_value("STUDENT", "Full name", "Daniel Ong")
    drawer.expect_value("STUDENT", "NRIC/FIN", "T1755501Q")
    drawer.expect_value("STUDENT", "Grade", "P2")
    expect(drawer.row("STUDENT", "Class")).to_be_visible()
    expect(drawer.row("STUDENT", "Citizenship")).to_be_visible()
    for label in ("NRIC/FIN", "Mobile", "Email"):
        expect(drawer.row("PARENT", label)).to_be_visible()
    H = "HOUSEHOLD AND INCOME"
    drawer.expect_value(H, "Gross household income", "S$ 2,600.00 / month")
    drawer.expect_value(H, "Household size", "3")
    drawer.expect_value(H, "Per capita income", "S$ 867.00")
    drawer.expect_value(H, "Income source", "API")
    expect(drawer.section("CONTEXT")).to_contain_text("No context given.")
    expect(drawer.section("DOCUMENTS")).to_contain_text("No documents.")
    drawer.expect_history_contains("SBFAS application (not eligible for MOEFAS by nationality)")
    assert "Submitted" in drawer.history_events()


def test_tc_115_hq_drawer_for_sbfas_shows_school_and_student_block(hq_apps):
    """TC-115 MOE HQ drawer for SBFAS shows the school in the header and the student block."""
    drawer = hq_apps.open("00398")
    expect(drawer.eyebrow).to_have_text("SBFAS REVIEW")
    expect(drawer.subtitle).to_have_text(f"Daniel Ong {MIDDOT} Bukit View Primary")
    expect(drawer.section("STUDENT")).to_contain_text("Bukit View Primary")


def test_tc_116_decided_sbfas_drawer_shows_tier_decider_and_history(bvp_apps):
    """TC-116 Decided SBFAS drawer shows Tier, from date, decider and the History row."""
    bvp_apps.open_tab("All")
    drawer = bvp_apps.open("00386")
    D = "DECISION"
    drawer.expect_value(D, "Tier", f"Tier 3 {MIDDOT} from 13/01/2026")
    drawer.expect_value(D, "Decided by", f"Lan Nguyen (BVP-0012) {MIDDOT} 13/01/2026 09:10")
    assert any("13/01/2026 09:10" in t and e == f"Approved {MIDDOT} Tier 3" for t, e in drawer.history())


@pytest.mark.draft
@pytest.mark.known_defect(reason="CMP-34: no parent relationship and the mobile number is masked (ASM-R4-10)")
def test_tc_117_parent_relationship_and_citizenship_use_readable_labels(bvp_apps):
    """TC-117 Parent relationship and citizenship use readable labels. ASM-R4-10."""
    bvp_apps.open_tab("All")
    first = bvp_apps.open("00398")
    failures = soft(
        lambda: first.expect_value("STUDENT", "Citizenship", "International Student"),
        lambda: expect(first.value("PARENT", "Name")).to_have_text(re.compile(r"Mother|Father|Guardian")),
        lambda: expect(first.value("PARENT", "Mobile")).not_to_have_text(re.compile(r"x{3}")),
    )
    first.close()
    second = bvp_apps.open("00386")
    failures += soft(
        lambda: second.expect_value("STUDENT", "Citizenship", "Singapore Citizen"),
        lambda: expect(second.value("PARENT", "Name")).to_have_text(re.compile(r"Mother|Father|Guardian")),
        lambda: expect(second.value("PARENT", "Mobile")).not_to_have_text(re.compile(r"x{3}")),
    )
    assert not failures, failures


def test_tc_118_ml_block_shows_tier_with_recommendation_only_tag(bvp_apps):
    """TC-118 ML recommendation block shows the tier only, with the tag Recommendation only."""
    bvp_apps.open_tab("All")
    decided = bvp_apps.open("00386")
    expect(decided.ml_tier).to_have_text("Tier 2")
    expect(decided.ml_tag).to_have_text("Recommendation only")
    decided.close()
    pending = bvp_apps.open("00398")
    expect(pending.ml_tier).to_have_text(EMDASH)
    expect(pending.ml_tag).to_have_text("Recommendation only")
    text = pending.text().lower()
    for word in ("need score", "confidence", "deny", "factor"):
        assert word not in text


@pytest.mark.draft
def test_tc_120_ml_recommendation_does_not_block_a_choice(bvp_apps_after_close):
    """TC-120 ML recommendation is information only and does not block a choice. ASM-R4-03."""
    apps = bvp_apps_after_close
    drawer = apps.open("00412")
    drawer.approve_button.click()
    dialog = ApproveDialog(apps.page)
    dialog.expect_open()
    dialog.choose_tier("Tier 1")
    dialog.confirm()
    dialog.expect_closed()
    apps.open_tab("All")
    decided = apps.open("00412")
    expect(decided.value("DECISION", "Tier")).to_contain_text("Tier 1")


# ------------------------------------------------------------ decision buttons
def test_tc_121_reject_and_approve_show_only_on_a_pending_sbfas(bvp_apps):
    """TC-121 Reject and Approve show only for the School Admin of the school on a Pending SBFAS."""
    pending = bvp_apps.open("00398")
    assert pending.action_buttons() == ["Reject", "Approve"]
    pending.close()
    bvp_apps.open_tab("All")
    decided = bvp_apps.open("00386")
    assert decided.action_buttons() == []


def test_tc_122_hq_drawers_have_no_decision_button_for_sbfas(hq_apps):
    """TC-122 MOE HQ drawers have no decision button for SBFAS."""
    for app_id in ("00398", "00386"):
        drawer = hq_apps.open(app_id)
        assert drawer.action_buttons() == []
        drawer.close()
