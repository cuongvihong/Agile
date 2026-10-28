"""Smoke of the real admin portal on localhost: sign in as MOE HQ and School user, open the main screens.
Replaces the old tests/test_real_hosted_portal.py (TC-901 to TC-906)."""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import Page, expect

from pages.real_schemes import LIST_PATH
from pages.real_login import HQ_PASS, HQ_USER, sign_in

pytestmark = [pytest.mark.smoke]


def test_tc_901_moehq_login_and_dashboard(page: Page, base: str, base_url: str):
    """TC-901 MOE HQ signs in with username and password and lands in the portal with the navigation visible."""
    page.context.clear_cookies()
    sign_in(page, base_url, HQ_USER, HQ_PASS)
    expect(page).not_to_have_url(re.compile(r"/login"))
    expect(page.locator("nav").first).to_be_visible()


def test_tc_902_moehq_schemes_list(page: Page, base: str):
    """TC-902 MOE HQ opens the MOEFAS list with the status cards, the table and the New scheme link."""
    page.goto(base + LIST_PATH)
    expect(page.get_by_role("heading", level=1, name="MOEFAS", exact=True)).to_be_visible()
    expect(page.get_by_role("list", name="MOEFAS schemes by status")).to_be_visible()
    expect(page.get_by_role("table")).to_be_visible()
    expect(page.get_by_role("link", name="New scheme")).to_be_visible()
    expect(page.locator("table tbody tr").first).to_be_visible(timeout=15_000)
    expect(page.get_by_text(re.compile(r"could not be loaded|server error", re.I))).to_have_count(0)


def test_tc_903_moehq_create_scheme_wizard(page: Page, base: str):
    """TC-903 MOE HQ opens the new scheme wizard with the four steps."""
    page.goto(base + LIST_PATH + "/new")
    expect(page.get_by_role("heading", level=1, name="Create new scheme")).to_be_visible()
    steps = page.get_by_role("list", name="Create scheme progress").locator("li")
    expect(steps).to_have_count(4)
    expect(page.locator("#moefas-create-name")).to_be_visible()


def test_tc_904_school_user_login(school_page: Page, base_url: str):
    """TC-904 School user is signed in on the admin portal (the login itself is done once by the school_state fixture)."""
    school_page.goto(base_url.rstrip("/") + "/")
    expect(school_page).not_to_have_url(re.compile(r"/login"))
    expect(school_page.locator("nav").first).to_be_visible()


def test_tc_905_school_fas_application_management(school_page: Page, base_url: str):
    """TC-905 School user opens FAS application management and sees the application view."""
    school_page.goto(base_url.rstrip("/") + "/fas-application-management")
    expect(school_page).to_have_url(re.compile(r"/fas-application-management"))
    expect(school_page.locator("main").first).to_be_visible()
    expect(school_page.get_by_role("heading", level=1)).to_be_visible()
    expect(school_page.get_by_text(re.compile(r"server error", re.I))).to_have_count(0)


def test_tc_906_school_sbfas_schemes(school_page: Page, base_url: str):
    """TC-906 School user opens the SBFAS schemes list and table."""
    school_page.goto(base_url.rstrip("/") + "/sbfas-schemes")
    expect(school_page).to_have_url(re.compile(r"/sbfas-schemes"))
    expect(school_page.locator("main").first).to_be_visible()
    expect(school_page.get_by_role("heading", level=1)).to_be_visible()
    expect(school_page.get_by_role("table")).to_be_visible(timeout=15_000)
    expect(school_page.locator("table tbody tr").first).to_be_visible(timeout=15_000)
    expect(school_page.get_by_text(re.compile(r"server error", re.I))).to_have_count(0)
