"""Portal: shell for the School Admin Portal with real localhost and prototype support."""
from __future__ import annotations

import json
import os
from pathlib import Path
from playwright.sync_api import Page, expect

from .base_page import BasePage


class Portal(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url.rstrip("/") + "/"
        target_env = os.environ.get("R5_TARGET", "").lower()
        self.is_real = (
            target_env == "real"
            or ("localhost" in self.base_url or "127.0.0.1" in self.base_url)
            and target_env != "prototype"
        )
        self.sidebar = page.locator("nav, aside")
        self.main = page.locator("main")

    def open(self) -> "Portal":
        self.page.goto(self.base_url)
        self.wait_for_ready()
        return self

    def sign_in_school(self, username: str = "school", password: str = "123456") -> "Portal":
        """Sign in as School Admin."""
        auth_file = Path("artifacts/auth/school_state.json")
        if auth_file.exists():
            try:
                with open(auth_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.page.context.add_cookies(data.get("cookies", []))
                self.page.goto(self.base_url)
                try:
                    self.page.wait_for_selector("nav", timeout=3000)
                    return self
                except Exception:
                    auth_file.unlink(missing_ok=True)
            except Exception:
                pass

        self.page.goto(f"{self.base_url}login")
        user_input = self.page.locator('input[autocomplete="username"], input[name="username"], input[type="text"]').first
        pass_input = self.page.locator('input[autocomplete="current-password"], input[name="password"], input[type="password"]').first
        user_input.wait_for(state="visible", timeout=10000)
        user_input.fill(username)
        pass_input.fill(password)
        self.page.locator('button[type="submit"]').click()
        expect(self.page.locator("nav").first).to_be_visible(timeout=15000)
        self.page.wait_for_timeout(1000)
        try:
            auth_file.parent.mkdir(parents=True, exist_ok=True)
            self.page.context.storage_state(path=str(auth_file))
        except Exception:
            pass
        return self

    def go_to_applications(self) -> None:
        """Navigate to FAS / Paper applications page."""
        try:
            link = self.page.locator("nav a").filter(has_text="FAS Application Management")
            if link.count() > 0 and link.first.is_visible():
                link.first.click()
                self.page.wait_for_load_state("domcontentloaded")
                return
        except Exception:
            pass
        self.page.goto(f"{self.base_url}fas-application-management")
        self.page.wait_for_load_state("domcontentloaded")
