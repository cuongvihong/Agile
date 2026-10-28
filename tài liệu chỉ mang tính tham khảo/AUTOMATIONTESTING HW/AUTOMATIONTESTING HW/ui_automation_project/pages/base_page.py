"""BasePage: reusable browser/page operations shared by every Page Object.

Only generic, cross-page concerns live here. Anything specific to the
Trainer Account form belongs in FormPage instead.
"""
from __future__ import annotations

from pathlib import Path


class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url: str) -> None:
        self.page.goto(url)

    def title(self) -> str:
        return self.page.title()

    def url(self) -> str:
        return self.page.url

    def screenshot(self, path: str, full_page: bool = True) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=path, full_page=full_page)
