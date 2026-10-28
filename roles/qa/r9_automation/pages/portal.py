"""Đăng nhập Singpass qua MockPass và điều hướng chung của e-service.

MockPass chạy ở cổng 5156. Trang đăng nhập có ô chọn persona (#persona-select) và nút #btn-login-selected,
không cần nhập mật khẩu. Địa chỉ MockPass lấy từ VITE_MOCKPASS_BASE_URL của máy chạy e-service, có thể là IP Radmin.
"""
from __future__ import annotations

import re

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

from pages.base_page import BasePage


class Portal(BasePage):
    def __init__(self, page: Page, base_url: str, nric: str):
        super().__init__(page, base_url)
        self.nric = nric

    def sign_in(self) -> "Portal":
        page = self.page
        page.goto(self.url("/parent/login"))
        button = page.get_by_role("button", name=re.compile(r"singpass", re.I)).or_(
            page.get_by_role("link", name=re.compile(r"singpass", re.I)))
        button.first.click()
        page.wait_for_url(re.compile(r"/singpass/login"), timeout=45_000)
        select = page.locator("#persona-select")
        select.wait_for(timeout=20_000)
        options = [t.strip() for t in select.locator("option").all_inner_texts()]
        match = [t for t in options if self.nric in t]
        assert match, f"MockPass không có persona {self.nric}. Các persona có: {options}"
        select.select_option(label=match[0])
        page.locator("#btn-login-selected").click()
        page.wait_for_url(lambda u: "/parent/callback" not in u and "/parent/login" not in u,
                          timeout=60_000)
        return self

    def is_signed_in(self) -> bool:
        """Mở /billing; nếu app đẩy về /parent/login thì chưa đăng nhập."""
        self.page.goto(self.url("/billing"))
        try:
            self.page.wait_for_url(re.compile(r"/parent/login"), timeout=5_000)
            return False
        except PlaywrightTimeoutError:
            return True

    def open_fees_and_payments(self) -> None:
        """Vào Fees & Payments bằng link hoặc điều hướng trực tiếp /billing."""
        fee_link = self.page.get_by_role("link", name=re.compile(r"fees & payments|billing|view bills", re.I))
        if fee_link.count() > 0 and fee_link.first.is_visible():
            fee_link.first.click()
        else:
            self.page.goto(self.url("/billing"))
        expect(self.page).to_have_url(re.compile(r"/billing"))
