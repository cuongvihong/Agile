"""Trang /billing: chọn tài khoản giáo dục (con) để xem phí. Tương ứng SCR-01 Choose child của R9."""
from __future__ import annotations

import re

from playwright.sync_api import Locator, expect

from data import ui_text as T
from pages.base_page import BasePage, norm


class AccountsPage(BasePage):
    PATH = "/billing"

    @property
    def heading(self) -> Locator:
        return self.page.get_by_role("heading", name=T.H_ACCOUNTS, level=1)

    @property
    def account_list(self) -> Locator:
        return self.page.get_by_role("list", name=T.LIST_ACCOUNTS)

    @property
    def cards(self) -> Locator:
        return self.account_list.get_by_role("listitem")

    @property
    def error_heading(self) -> Locator:
        return self.page.get_by_role("heading", name=T.ACCOUNTS_ERROR)

    @property
    def empty_title(self) -> Locator:
        return self.page.get_by_text(T.ACCOUNTS_EMPTY, exact=True)

    @property
    def retry_button(self) -> Locator:
        return self.page.get_by_role("button", name=T.RETRY)

    def open(self) -> "AccountsPage":
        self.page.goto(self.url(self.PATH))
        self.wait_loaded()
        return self

    def wait_loaded(self, timeout: int = 20_000) -> None:
        """Chờ một trong ba trạng thái: có danh sách, lỗi tải, hoặc rỗng."""
        tour_btn = self.page.get_by_role("button", name=re.compile(r"Let me explore|Close welcome dialog", re.I))
        if tour_btn.count() > 0 and tour_btn.first.is_visible():
            tour_btn.first.click()
        loading = self.page.locator('[data-tour-page="billing-accounts"][data-tour-state="loading"]')
        if loading.count() > 0 and loading.first.is_visible():
            try:
                self.page.locator(
                    '[data-tour-page="billing-accounts"][data-tour-state="ready"],'
                    '[data-tour-page="billing-accounts"][data-tour-state="error"],'
                    '[data-tour-page="billing-accounts"][data-tour-state="empty"]'
                ).first.wait_for(state="visible", timeout=timeout)
            except Exception:
                pass
        expect(self.account_list.or_(self.error_heading).or_(self.empty_title).first).to_be_visible(timeout=timeout)

    def read_cards(self) -> list[dict]:
        """Mỗi thẻ: name, code, status, student_id (từ liên kết), text (toàn bộ chữ của thẻ)."""
        out: list[dict] = []
        for card in self.cards.all():
            text = norm(card.inner_text())
            href = card.get_by_role("link").first.get_attribute("href") or ""
            code = re.search(r"Account\s+(\S+)", text)
            status = re.search(r"Status:\s*(.+?)(?:\s+View fees|$)", text)
            out.append({"name": norm(card.get_by_role("heading").first.inner_text()),
                        "code": code.group(1) if code else "",
                        "status": status.group(1).strip() if status else "",
                        "student_id": href.split("?")[0].rstrip("/").rsplit("/", 1)[-1],
                        "text": text})
        return out

    def read_all(self) -> list[dict]:
        """Đọc mọi con, qua các trang nếu có phân trang (6 con mỗi trang)."""
        out: list[dict] = []
        seen_names: set[str] = set()
        for _ in range(20):
            self.wait_loaded()
            cards = self.read_cards()
            for c in cards:
                if c["name"] not in seen_names:
                    seen_names.add(c["name"])
                    out.append(c)
            nxt = self.page.get_by_role("button", name=re.compile(r"^next", re.I))
            if nxt.count() == 0 or nxt.first.is_disabled():
                break
            first_name = cards[0]["name"] if cards else ""
            nxt.first.click()
            try:
                self.page.wait_for_function(
                    "(oldName) => { const h2 = document.querySelector('h2'); return h2 && h2.innerText !== oldName; }",
                    arg=first_name,
                    timeout=5_000,
                )
            except Exception:
                pass
            self.wait_loaded()
        return out

    def open_child(self, name: str) -> None:
        self.page.get_by_role("link", name=f"View fees for {name}").click()
        self.page.wait_for_url(re.compile(r"/billing/[^/]+$"))
