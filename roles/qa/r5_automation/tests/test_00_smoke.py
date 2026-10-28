"""Smoke tests for R5 Paper Applications automation suite."""
from __future__ import annotations

import re
import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage


@pytest.mark.smoke
@pytest.mark.real
def test_smoke_school_sign_in_and_navigation(portal: Portal):
    """Smoke: Verify school admin can sign in and access application management."""
    portal.sign_in_school("school", "123456")
    expect(portal.sidebar.first).to_be_visible()
    
    portal.go_to_applications()
    expect(portal.page).to_have_url(re.compile(r"fas-application-management|5173"))
    portal.page.wait_for_timeout(2000)
