"""Trang đăng nhập của admin portal (apps/admin-portal, mặc định http://localhost:5173).

Chỉ mô tả những gì thấy được khi chưa đăng nhập. Không có hàm nhập tài khoản hay mật khẩu: bộ test R9 không giữ
thông tin đăng nhập quản trị và không được tự đặt. Locator lấy từ giao diện thật ngày 21/10/2026
(h1 "Welcome back", ô "Username", ô "Password", nút "Sign in").
"""
from __future__ import annotations

import re

from playwright.sync_api import Locator, Page, expect

from data import seed



class AdminLoginPage:
    def __init__(self, page: Page, admin_url: str | None = None):
        self.page = page
        self.base_url = (admin_url or seed.ADMIN_URL).rstrip("/")

    def url(self, path: str = "") -> str:
        return f"{self.base_url}{path}"

    def open(self) -> "AdminLoginPage":
        self.page.goto(self.url("/login"))
        expect(self.heading).to_be_visible(timeout=20_000)
        return self

    @property
    def heading(self) -> Locator:
        return self.page.get_by_role("heading", name=re.compile(r"^(Welcome back|Login)$"), level=1)

    @property
    def username(self) -> Locator:
        return self.page.get_by_label(re.compile(r"^Username"))

    @property
    def password(self) -> Locator:
        return self.page.get_by_label(re.compile(r"^Password"))

    @property
    def sign_in_button(self) -> Locator:
        return self.page.get_by_role("button", name="Sign in", exact=True)

    def title(self) -> str:
        return self.page.title()
