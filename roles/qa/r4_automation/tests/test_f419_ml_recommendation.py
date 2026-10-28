"""F4.19 ML recommendation and risk (TC-249 to TC-263). Source: FS F4 v1.3 section 9 and the F4 ML annex.
Only TC-249, TC-250, TC-251 and TC-255 can be checked on the prototype. The scoring engine cases need the build."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data.ui_text import EMDASH

pytestmark = pytest.mark.f419


def test_tc_249_recommended_tier_is_the_first_candidate_scheme_the_household_meets(bvp_apps):
    """TC-249 The recommended tier is the first candidate scheme the household meets (00386, PCI 940)."""
    bvp_apps.open_tab("All")
    bvp_apps.expect_row("00386", ML_RECOMMENDATION="Tier 2")
    drawer = bvp_apps.open("00386")
    expect(drawer.ml_tier).to_have_text("Tier 2")
    expect(drawer.ml_tag).to_have_text("Recommendation only")


def test_tc_250_a_household_above_the_lower_bands_gets_tier_3(bvp_apps_after_close):
    """TC-250 A household above the lower bands gets Tier 3 (00412 and 00410 after the demo close)."""
    apps = bvp_apps_after_close
    apps.expect_row("00412", ML_RECOMMENDATION="Tier 3")
    apps.expect_row("00410", ML_RECOMMENDATION="Tier 3")


def test_tc_251_no_tier_is_recommended_when_the_nationality_is_not_allowed(bvp_apps):
    """TC-251 No tier is recommended when the nationality is not allowed (00398)."""
    bvp_apps.expect_row("00398", ML_RECOMMENDATION=EMDASH)
    drawer = bvp_apps.open("00398")
    expect(drawer.ml_tier).to_have_text(EMDASH)
    expect(drawer.ml_tag).to_have_text("Recommendation only")


@pytest.mark.draft
def test_tc_255_ml_risk_of_the_sample_rows_follows_their_need_score(hq_apps):
    """TC-255 ML risk of the sample rows follows their Need Score. ASM-R4-14."""
    for app_id, risk in (("00377", "Medium"), ("00412", "Medium"), ("00390", "High"), ("00328", "Low")):
        hq_apps.expect_row(app_id, ML_RISK=risk)
