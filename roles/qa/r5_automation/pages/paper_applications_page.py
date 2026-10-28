"""Page Object for Function 5 (R5) Paper Applications."""
from __future__ import annotations

from pathlib import Path
from playwright.sync_api import Page, Locator, expect

from .base_page import BasePage, norm


class PaperApplicationsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.table = page.locator("table")
        self.search_input = page.locator('input[placeholder*="Search"], input[type="search"]')
        self.upload_btn = page.locator('button:has-text("Upload"), button:has-text("Upload scans")')
        self.modal = page.locator('[role="dialog"], .modal')
        self.file_input = page.locator('input[type="file"]')
        self.submit_btn = page.locator('button:has-text("Submit"), button:has-text("Review and submit")')
        self.save_draft_btn = page.locator('button:has-text("Save draft"), button:has-text("Draft")')

    def open_list(self, base_url: str) -> "PaperApplicationsPage":
        url = base_url.rstrip("/") + "/fas-application-management"
        self.page.goto(url)
        self.wait_for_ready()
        return self

    def filter_tab(self, name: str) -> None:
        tab = self.page.locator(f'button[role="tab"]:has-text("{name}"), a:has-text("{name}")').first
        if tab.is_visible():
            tab.click()
            self.page.wait_for_timeout(500)

    def search(self, term: str) -> None:
        if self.search_input.is_visible():
            self.search_input.fill(term)
            self.page.keyboard.press("Enter")
            self.page.wait_for_timeout(800)

    def open_upload_dialog(self) -> None:
        if self.upload_btn.is_visible():
            self.upload_btn.click()
            self.modal.wait_for(state="visible", timeout=5000)

    def upload_scan_file(self, file_path: str | Path) -> None:
        p = Path(file_path)
        if not p.exists():
            # Create a mock file if it doesn't exist
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"%PDF-1.4 Mock FAS Paper Application Scan Content")
        self.file_input.set_input_files(str(p))
        self.page.wait_for_timeout(1000)
