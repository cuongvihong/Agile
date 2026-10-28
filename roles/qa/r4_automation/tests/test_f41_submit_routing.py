"""F4.1 Submit routing (TC-001 to TC-006). Source: roles/qa/R4_Test_Cases.xlsx, FS F4 v1.3 sections 1.3, 2.1, 7.1."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data import seed
from data.ui_text import EMDASH

pytestmark = pytest.mark.f41


def test_tc_001_waiting_moefas_shows_pending_and_waiting(hq_apps):
    """TC-001 Waiting MOEFAS application shows Pending and System check Waiting."""
    hq_apps.do_search("00412")
    hq_apps.expect_ids(["00412"])
    hq_apps.expect_row("00412", SCHEME="MOEFAS", SUBMITTED="17/10/2026", SYSTEM_CHECK="Waiting",
                       STATUS="Pending", TIER=EMDASH, ML_RECOMMENDATION=EMDASH)


def test_tc_002_waiting_drawer_explains_wait_and_records_submit(hq_apps):
    """TC-002 Waiting MOEFAS drawer explains the wait and records the submit in History."""
    drawer = hq_apps.open("00412")
    events = drawer.history()
    assert any(t == "17/10/2026 09:12" and "Uploaded by Lan Nguyen" in e for t, e in events)
    assert any(t == "17/10/2026 09:20" and e == "Submitted" for t, e in events)
    assert events[-1][1] == "Waiting for the MOEFAS form to close on 31/12/2026"
    expect(drawer.row("DECISION", "Result")).to_have_count(0)
    assert drawer.action_buttons() == []
    drawer.close()
    hq_apps.expect_row("00412", STATUS="Pending")


def test_tc_003_waiting_moefas_not_visible_to_school_admin(bvp_apps):
    """TC-003 Waiting MOEFAS application is not visible to the School Admin."""
    bvp_apps.open_tab("All")
    bvp_apps.expect_ids(["00398", "00386"])
    bvp_apps.do_search("00412")
    bvp_apps.expect_empty()
    bvp_apps.do_search("")
    bvp_apps.expect_cards({"Pending": "1"})
    bvp_apps.expect_tabs({"Pending": 1})


def test_tc_004_international_student_is_sbfas_pending(hq_apps):
    """TC-004 International student application is SBFAS Pending for the school."""
    hq_apps.do_search("00398")
    hq_apps.expect_row("00398", SCHEME="SBFAS", SYSTEM_CHECK=EMDASH, STATUS="Pending")
    drawer = hq_apps.open("00398")
    assert drawer.history_events()[-1] == "SBFAS application (not eligible for MOEFAS by nationality)"
    expect(drawer.root).not_to_contain_text("Priority")
    expect(drawer.root).not_to_contain_text("auto-approved")


def test_tc_006_citizen_application_is_not_routed_to_sbfas(hq_apps):
    """TC-006 Singapore Citizen application is not routed to SBFAS at submit."""
    hq_apps.set_filter("Scheme", "MOEFAS")
    hq_apps.set_filter("Status", "Pending")
    hq_apps.expect_ids(seed.WAITING_MOEFAS)
    for app_id in seed.WAITING_MOEFAS:
        hq_apps.expect_row(app_id, SCHEME="MOEFAS", SYSTEM_CHECK="Waiting")
