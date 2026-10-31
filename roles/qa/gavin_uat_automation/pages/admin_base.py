"""BasePage: generic browser operations shared by every Page Object.

Locator order used in this project (same rule as the course project):
role, label, text, placeholder, stable CSS. The prototype is a React app made
with Figma Make. Many controls have no label, no role and no test id (filters,
dialogs, toast, stat cards). For those the Page Objects use the short CSS class
of the prototype and say so in a comment. These are the only places to change
when the front end gets accessible names (see roles/qa/Developer_Guide_Accessible_UI_for_Playwright.docx).
"""
from __future__ import annotations

import re
from pathlib import Path

from playwright.sync_api import Page


def norm(text: str) -> str:
    """Collapse every run of white space into one space and trim the ends."""
    return re.sub(r"\s+", " ", text or "").strip()


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def screenshot(self, path: str, full_page: bool = True) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=path, full_page=full_page)

    def text_of(self, locator) -> str:
        return norm(locator.inner_text())


def soft(*checks) -> list:
    """Run several checks and collect the failures instead of stopping at the first one.
    Use it for a case with independent parts: assert not soft(lambda: ..., lambda: ...)."""
    failures = []
    for check in checks:
        try:
            check()
        except AssertionError as err:
            failures.append(str(err).strip().splitlines()[0] if str(err).strip() else "check failed")
    return failures
