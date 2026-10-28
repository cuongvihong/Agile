"""BasePage: common Playwright operations and assertions."""
from __future__ import annotations

import re
from playwright.sync_api import Page, Locator, expect


def norm(text: str) -> str:
    """Normalize whitespace so assertions match regardless of line breaks or extra spaces."""
    return re.sub(r"\s+", " ", text).strip()


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def wait_for_ready(self, timeout: float = 10000):
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
        except Exception:
            pass

    def wait_for_network_idle(self, timeout: float = 5000):
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception:
            pass
