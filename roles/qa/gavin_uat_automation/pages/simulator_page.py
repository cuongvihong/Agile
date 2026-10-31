"""Trang thanh toán giả lập (payment-checkout-simulator, cổng 5176): /checkout/<id>."""
from __future__ import annotations

import re

from playwright.sync_api import Locator, expect

from data import ui_text as T
from pages.base_page import BasePage


class SimulatorPage(BasePage):
    @property
    def heading(self) -> Locator:
        return self.page.get_by_role("heading", name=T.SIM_HEADING)

    def wait_loaded(self) -> "SimulatorPage":
        self.page.wait_for_url(re.compile(r"/checkout/[^/]+"), timeout=45_000)
        expect(self.heading).to_be_visible(timeout=20_000)
        return self

    def pay_successful(self) -> None:
        self.page.get_by_role("button", name=T.SIM_PAY_OK, exact=True).click()

    def pay_failed(self) -> None:
        """Bản build 30/10/2026 chỉ có một nút Pay gửi form với outcome ẩn là Succeeded (CheckoutApp.tsx, OutcomeActions).
        Muốn mô phỏng thất bại thì đặt outcome ẩn thành Failed rồi bấm Pay, endpoint complete nhận đúng hai giá trị Succeeded và Failed."""
        self.page.locator('form input[name="outcome"]').evaluate("el => { el.value = 'Failed'; }")
        self.page.get_by_role("button", name=T.SIM_PAY_FAIL, exact=True).click()

    def wait_return_to_merchant(self) -> None:
        """Sau khi bấm, simulator chuyển về returnUrl của e-service."""
        self.page.wait_for_url(re.compile(r"/payment-result"), timeout=45_000)
