"""Shared fixtures for the Curricula Trainer Account UI automation project.

Session 01 analysis confirmed the AUT is a single static HTML file with no
external resources and no network calls, so it is loaded directly via a
file:// URL. No local server is required.
"""
from pathlib import Path

import pytest

from pages.form_page import FormPage

# The supplied HTML lives in the sibling prompt-package folder, one level
# above this project's root. Resolved relative to this file so the suite
# runs the same regardless of where the workspace is checked out.
AUT_HTML_PATH = (
    Path(__file__).resolve().parent.parent
    / "UI_Automation_Master_6_Sessions"
    / "curricula_trainer_account.html"
)


@pytest.fixture
def aut_url() -> str:
    """file:// URL for the Curricula Trainer Account form."""
    if not AUT_HTML_PATH.exists():
        pytest.fail(f"AUT HTML not found at {AUT_HTML_PATH}")
    return AUT_HTML_PATH.as_uri()


@pytest.fixture
def form_page(page, aut_url) -> FormPage:
    """A FormPage Page Object already navigated to the AUT, fresh per test.

    `page` comes from pytest-playwright (handles browser/context lifecycle
    automatically — no manual setup/teardown needed in tests or Page Objects).
    """
    return FormPage(page).open(aut_url)
