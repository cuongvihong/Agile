"""F4.15 Review and publish on the real admin portal (localhost). All tests here create data (prefix R4-AUTO).

Real flow: step 4 Review is a page step of the wizard (not a dialog). Publish sends status Published to the backend.
Overlap rules (TC-219 to TC-221): the backend has no overlap check, see known_defect reasons.
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from pages import real_api
from pages.real_schemes import LEVELS, us_date

pytestmark = [pytest.mark.f415, pytest.mark.mutating]


def test_tc_214_review_shows_general_eligibility_and_subsidy(wiz, page, need_components):
    """TC-214 The Review step lists General, Eligibility and Subsidy with the values entered."""
    need_components(1)
    win = real_api.window()
    name = real_api.unique_name("review")
    wiz.fill_general(name, win, budget="1234.5")
    wiz.go_next()
    wiz.fill_eligibility()
    wiz.go_next()
    comp = wiz.pick(1)[0]
    wiz.fill_levels(comp, ("10", "20", "30"))
    wiz.go_next()
    expect(page.get_by_role("heading", level=2, name="Review", exact=True)).to_be_visible()
    for section in ("General", "Eligibility", "Subsidy"):
        expect(page.get_by_role("heading", level=3, name=section, exact=True)).to_be_visible()
    body = page.locator("form").inner_text()
    for must in (name, us_date(win["opens"]), us_date(win["closes"]), us_date(win["eff_from"]), us_date(win["eff_to"]),
                 "Singapore Citizen", "S$ 1,234.50", comp, "10%", "20%", "30%"):
        assert must in body, f"{must!r} missing on the Review step"
    expect(wiz.publish_btn).to_be_visible()


def test_tc_215_publish_creates_a_published_scheme(wiz, page, api, base, need_components):
    """TC-215 Publish returns to the list and the new scheme is no longer a Draft; View and Add fees are offered."""
    need_components(1)
    name = real_api.unique_name("publish")
    wiz.complete(name, real_api.window())
    wiz.publish_btn.click()
    try:
        page.wait_for_url(re.compile(r"/moe-hq/moe-fas$"), timeout=15_000)
    except Exception:
        pytest.fail("Publish did not leave the wizard. Check the alert 'Could not save the scheme' (backend refused).")
    saved = [s for s in real_api.list_schemes(api, base) if s["name"] == name]
    assert len(saved) == 1
    assert saved[0]["status"].upper() != "DRAFT", f"status is {saved[0]['status']}"
    from pages.real_schemes import SchemeList
    lst = SchemeList(page, base)
    lst.wait_loaded()
    items = lst.actions(name)
    assert "View" in items and "Add fees" in items and not any(i.startswith("Edit") for i in items), items


def test_tc_216_back_from_review_keeps_the_values(wiz, need_components):
    """TC-216 Back from Review returns to Subsidy with the percentages kept."""
    need_components(1)
    chosen = wiz.complete(real_api.unique_name("back"), real_api.window(), pct=("11", "22", "33"))
    wiz.back_btn.click()
    assert wiz.current_step() == "Subsidy"
    assert wiz.cell(chosen[0], "Primary").input_value() == "11"
    assert wiz.cell(chosen[0], "Pre-University").input_value() == "33"


def test_tc_217_a_scheme_with_errors_cannot_reach_publish(wiz, page):
    """TC-217 Step 3 without a fee component blocks Next, so the Review step and Publish are not reachable."""
    wiz.to_subsidy()
    wiz.go_next()
    expect(page.get_by_role("heading", level=2, name="Review", exact=True)).to_have_count(0)
    expect(wiz.publish_btn).to_have_count(0)
    assert wiz.step_has_error_mark("Subsidy")


# --------------------------------------------------------------- overlap rules
@pytest.mark.known_defect(reason="No overlap check for the effective period: FASService CreateMOEFASSchemeHandler/Validator only check the name, the front end validation.ts has a TODO for it")
def test_tc_219_effective_period_overlap_is_blocked(make_scheme, api, base, components):
    """TC-219 A MOEFAS scheme whose effective period overlaps another published scheme is refused."""
    first = make_scheme("ovl-a", status="Published")
    ok, data, message = real_api.create_scheme(api, base, name=real_api.unique_name("ovl-b"), win=first["win"],
                                               component_ids=first["component_ids"], status="Published")
    assert not ok, f"second scheme with the same periods was accepted ({data.get('code')})"


@pytest.mark.known_defect(reason="No overlap check for the form period (same cause as TC-219)")
def test_tc_220_form_period_overlap_is_blocked(make_scheme, api, base):
    """TC-220 A MOEFAS scheme whose form period overlaps another form period is refused."""
    first = make_scheme("ovf-a", status="Published")
    y = int(first["win"]["opens"][:4])
    win = {"opens": first["win"]["opens"], "closes": first["win"]["closes"],
           "eff_from": f"{y + 5}-01-01", "eff_to": f"{y + 5}-12-31"}
    ok, data, _ = real_api.create_scheme(api, base, name=real_api.unique_name("ovf-b"), win=win,
                                         component_ids=first["component_ids"], status="Published")
    assert not ok, f"second scheme with the same form period was accepted ({data.get('code')})"


def test_tc_221_periods_that_touch_without_overlapping_are_allowed(make_scheme, api, base):
    """TC-221 The next scheme may start the day after the earlier one ends."""
    first = make_scheme("touch-a", status="Published")
    y = int(first["win"]["opens"][:4])
    win = {"opens": f"{y + 1}-07-01", "closes": f"{y + 1}-12-15", "eff_from": f"{y + 2}-01-01", "eff_to": f"{y + 2}-12-31"}
    ok, data, message = real_api.create_scheme(api, base, name=real_api.unique_name("touch-b"), win=win,
                                               component_ids=first["component_ids"], status="Published")
    assert ok, f"back to back periods were refused: {message}"
