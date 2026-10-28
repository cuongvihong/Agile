"""F4.11 One decision per application (TC-153 to TC-156). Source: FS F4 v1.3 section 5.
Only TC-155 runs on the prototype. TC-153, TC-154 and TC-156 need two sessions or the API."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.dialogs import ApproveDialog
from pages.review_drawer import ReviewDrawer

pytestmark = pytest.mark.f411


def test_tc_155_double_click_on_confirm_approval_saves_one_decision(bvp_apps):
    """TC-155 Double click on Confirm approval saves one decision."""
    page = bvp_apps.page
    drawer = bvp_apps.open("00398")
    drawer.approve_button.click()
    dialog = ApproveDialog(page)
    dialog.expect_open()
    dialog.confirm_button.dblclick()
    dialog.expect_closed()
    stray = ReviewDrawer(page)
    if stray.root.count():            # the second click may land on the row below the dialog
        stray.close()
    bvp_apps.open_tab("All")
    events = bvp_apps.open("00398").history_events()
    assert sum(1 for e in events if e.startswith("Approved")) == 1, events
    assert sum(1 for e in events if e == "Email with result sent to parent") == 1, events
    bvp_apps.expect_cards({"Pending": "0", "SBFAS approved": "2", "SBFAS rejected": "0"})
    expect(bvp_apps.tab_count("Approved")).to_have_text("2")
