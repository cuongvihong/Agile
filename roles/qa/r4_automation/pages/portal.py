"""Portal: the shell of the prototype or real hosted portal (view switch, sign in, sidebar, toast, reset)."""
from __future__ import annotations

import os
import re

from playwright.sync_api import Page, expect

from data import ui_text as T
from .base_page import BasePage, norm


class Portal(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url.rstrip("/") + "/"
        target_env = os.environ.get("R4_TARGET", "").lower()
        self.is_real = (
            target_env == "real"
            or ("localhost" in self.base_url or "127.0.0.1" in self.base_url or "devtunnels" in self.base_url or "pinggy" in self.base_url)
            and target_env != "prototype"
        )
        self.reset_button = page.get_by_role("button", name="Reset data")
        # In real UI navigation is inside <nav>, in prototype it is <aside class="sidebar">
        self.sidebar = page.locator("nav, aside.sidebar")
        self.main = page.locator("main")
        self.toast = page.locator(".toast, [role='status'], [role='alert']")
        self.modal = page.locator(".modal, [role='dialog']")

    # ------------------------------------------------------------------ start
    def open(self) -> "Portal":
        self.page.goto(self.base_url)
        if self.is_real:
            self.page.wait_for_load_state("domcontentloaded")
        else:
            expect(self.reset_button).to_be_visible()
        return self

    def reset_data(self) -> None:
        """Reset data reloads the page and signs the user out."""
        if self.is_real:
            self.page.context.clear_cookies()
            try:
                self.page.evaluate("() => localStorage.clear()")
            except Exception:
                pass
            self.page.goto(f"{self.base_url}login")
            return

        self.reset_button.click()
        self.page.wait_for_load_state("load")
        expect(self.page.get_by_role("button", name=T.SIGN_IN_HQ)).to_be_visible()

    # --------------------------------------------------------------- sign in
    def sign_in_hq(self) -> "Portal":
        """Switch to MOE HQ view and sign in."""
        if self.is_real:
            from pathlib import Path
            import json
            auth_file = Path("artifacts/auth/moehq_state.json")
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
            user_input.fill("moehq")
            pass_input.fill("123456")
            self.page.locator('button[type="submit"]').click()
            expect(self.page.locator("nav").first).to_be_visible(timeout=15000)
            self.page.wait_for_timeout(1000)
            try:
                auth_file.parent.mkdir(parents=True, exist_ok=True)
                self.page.context.storage_state(path=str(auth_file))
            except Exception:
                pass
            return self

        self.page.get_by_role("button", name=T.VIEW_HQ).click()
        button = self.page.get_by_role("button", name=T.SIGN_IN_HQ)
        if button.is_visible():
            button.click()
        expect(self.sidebar).to_contain_text(T.HQ_USER)
        return self

    def sign_in_school(self, school_id: str = "BVP-0012") -> "Portal":
        """Switch to School user view and sign in."""
        if self.is_real:
            from pathlib import Path
            import json
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
            user_input.fill("school")
            pass_input.fill("123456")
            self.page.locator('button[type="submit"]').click()
            expect(self.page.locator("nav").first).to_be_visible(timeout=15000)
            self.page.wait_for_timeout(1000)
            try:
                auth_file.parent.mkdir(parents=True, exist_ok=True)
                self.page.context.storage_state(path=str(auth_file))
            except Exception:
                pass
            return self

    def log_out(self) -> None:
        if self.is_real:
            self.page.context.clear_cookies()
            try:
                self.page.evaluate("() => localStorage.clear()")
            except Exception:
                pass
            self.page.goto(f"{self.base_url}login")
            return

        self.sidebar.get_by_role("button", name="Log out").click()
        expect(self.sidebar).to_have_count(0)

    # ------------------------------------------------------------ navigation
    def nav_button(self, label: str):
        # the sidebar button text ends with a small tag such as "F4", so match the start
        return self.sidebar.get_by_role("button", name=re.compile(r"^" + re.escape(label)))

    def go(self, label: str, heading: str | None = None) -> None:
        if self.is_real:
            mapping = {
                "MOEFAS schemes": ["/moe-hq/moe-fas", "MOEFAS"],
                "MOEFAS": ["/moe-hq/moe-fas", "MOEFAS"],
                "FAS applications": ["/fas-application-management", "FAS"],
                "FAS": ["/fas-application-management", "FAS"],
                "SBFAS schemes": ["/sbfas-schemes", "SBFAS"],
                "SBFAS": ["/sbfas-schemes", "SBFAS"],
            }
            target = mapping.get(label)
            if target:
                route, link_text = target
                nav_link = self.page.locator(f"nav a[href*='{route}'], a[href*='{route}'], nav a:has-text('{link_text}')").first
                if nav_link.is_visible():
                    nav_link.click()
                    self.page.wait_for_timeout(1000)
                    return
                self.page.goto(f"{self.base_url}{route.lstrip('/')}")
                self.page.wait_for_timeout(1000)
                return
            link = self.page.locator(f"nav a:has-text('{label}'), a:has-text('{label}')").first
            if link.is_visible():
                link.click()
                self.page.wait_for_timeout(1000)
                return

        self.nav_button(label).click()
        expect(self.page.get_by_role("heading", level=1, name=heading or label)).to_be_visible()

    def nav_labels(self) -> list[str]:
        """Visible sidebar items without the F-tag, in order."""
        labels = []
        for text in self.sidebar.get_by_role("button").all_inner_texts():
            text = norm(text)
            labels.append(re.sub(r"F\d+$", "", text).strip())
        return labels

    def nav_group(self, title: str) -> list:
        """Items of one menu group, for example 'Financial assistance', without the F-tag."""
        group = self.sidebar.locator(".nav-group").filter(
            has=self.page.locator(".nav-label", has_text=re.compile("^" + re.escape(title) + "$", re.I)))
        return [re.sub(r"F\d+$", "", norm(t)).strip() for t in group.get_by_role("button").all_inner_texts()]

    def heading(self):
        return self.main.get_by_role("heading", level=1)

    # ----------------------------------------------------------------- toast
    def expect_toast(self, text: str) -> None:
        expect(self.toast).to_contain_text(text)

    # ------------------------------------------------------------ dialog helpers
    def close_modal(self) -> None:
        self.modal.get_by_role("button", name=T.TIMES, exact=True).click()
        expect(self.modal).to_have_count(0)

