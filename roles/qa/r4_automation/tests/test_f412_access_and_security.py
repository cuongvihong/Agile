"""F4.12 Access and security (TC-157 to TC-167). Source: FS F4 v1.3 section 8.
Only the cases a browser can show run here. TC-160 to TC-165 need the API or two sessions."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.applications_page import ApplicationsPage
from pages.flows import open_reject_dialog

pytestmark = pytest.mark.f412


def test_tc_157_hq_menu_has_fas_applications_and_moefas_schemes_only(hq):
    """TC-157 MOE HQ menu has FAS applications and MOEFAS schemes and no SBFAS schemes."""
    items = hq.nav_group("Financial assistance")
    assert items == ["FAS applications", "MOEFAS schemes", "Budget & statistics"]
    assert "SBFAS schemes" not in hq.nav_labels()


def test_tc_158_school_menu_has_fas_applications_and_sbfas_schemes_only(bvp):
    """TC-158 School menu has FAS applications and SBFAS schemes and no MOEFAS schemes."""
    labels = bvp.nav_labels()
    assert "FAS applications" in labels and "SBFAS schemes" in labels
    assert "MOEFAS schemes" not in labels


def test_tc_159_each_role_sees_the_data_and_actions_of_its_role(hq, hq_apps):
    """TC-159 Each role sees the data and actions of FS 1.2 and nothing else."""
    assert len(hq_apps.ids()) == 9
    for app_id in ("00412", "00398"):            # one MOEFAS and one SBFAS
        drawer = hq_apps.open(app_id)
        assert drawer.action_buttons() == []
        drawer.close()
    hq.log_out()
    hq.sign_in_school("BVP-0012")
    hq.go("FAS applications")
    school = ApplicationsPage(hq.page)
    school.open_tab("All")
    school.expect_ids(["00398", "00386"])
    assert school.open("00398").action_buttons() == ["Reject", "Approve"]


@pytest.mark.draft
def test_tc_166_reject_comment_with_markup_is_shown_as_text(bvp, bvp_apps):
    """TC-166 Reject comment with markup is stored and shown as text, for the school and for MOE HQ. ASM-R4-18."""
    text = '<img src=x onerror=alert(1)> & "quotes"'
    alerts = []
    bvp.page.on("dialog", lambda d: (alerts.append(d.message), d.dismiss()))
    dialog = open_reject_dialog(bvp_apps)
    dialog.choose_reason("Other")
    dialog.comment.fill(text)
    dialog.reject()
    dialog.expect_closed()
    bvp_apps.open_tab("Rejected")
    expect(bvp_apps.open("00398").value("DECISION", "Comment")).to_have_text(text)
    bvp.log_out()
    bvp.sign_in_hq()
    bvp.go("FAS applications")
    hq = ApplicationsPage(bvp.page)
    expect(hq.open("00398").value("DECISION", "Comment")).to_have_text(text)
    assert alerts == []


@pytest.mark.draft
def test_tc_167_scheme_name_with_markup_is_shown_as_text(bvp, bvp_schemes):
    """TC-167 Scheme name with markup is shown as text. ASM-R4-18."""
    name = "<b>Tier X</b><script>alert(1)</script>"
    alerts = []
    bvp.page.on("dialog", lambda d: (alerts.append(d.message), d.dismiss()))
    wizard = bvp_schemes.new_scheme()
    wizard.name_input.fill(name)
    wizard.save_draft()
    expect(bvp_schemes.heading).to_be_visible()
    assert name in bvp_schemes.names()
    bvp.go("FAS applications")
    expect(ApplicationsPage(bvp.page).filter("Tier")).to_be_visible()      # the list still renders
    assert alerts == []
