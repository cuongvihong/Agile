"""Smoke tests: the setup works, both roles can sign in, the F4 screens open.
Run these first: pytest -m smoke
"""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from data import seed

pytestmark = pytest.mark.smoke


def test_smoke_prototype_opens(portal):
    expect(portal.page.get_by_text("Sample data")).to_be_visible()
    expect(portal.page.get_by_text(seed.SAMPLE_TODAY)).to_be_visible()


def test_smoke_hq_list_has_nine_rows(hq_apps):
    hq_apps.expect_ids(seed.ALL_IDS)
    assert hq_apps.footer_text() == "Showing 1–9 of 9"


def test_smoke_school_list_pending_tab(bvp_apps):
    bvp_apps.expect_active_tab("Pending")
    bvp_apps.expect_ids(["00398"])


def test_smoke_hq_schemes_list(hq_schemes):
    assert hq_schemes.names() == ["MOEFAS 2027", "MOEFAS 2026", "MOEFAS 2025"]


def test_smoke_school_schemes_list(bvp_schemes):
    assert len(bvp_schemes.names()) == 6


def test_smoke_wizard_opens(hq_schemes):
    wizard = hq_schemes.new_scheme()
    expect(wizard.name_input).to_be_visible()
