"""Trang /payment-result: kết quả giao dịch và biên lai. Tương ứng SCR-06, SCR-07, SCR-08 của R9."""
from __future__ import annotations

import re

from playwright.sync_api import Locator, expect

from data import ui_text as T
from pages.base_page import GUID_RE, BasePage, dl_value, money, norm, read_dl

FINAL_TITLE = re.compile(rf"^({T.RESULT_SUCCEEDED}|{T.RESULT_FAILED}|{T.RESULT_CANCELLED}|{T.RESULT_REVIEW})$")


class ResultPage(BasePage):
    @property
    def h1(self) -> Locator:
        return self.page.get_by_role("heading", name=T.H_RESULT, level=1)

    @property
    def status_heading(self) -> Locator:
        return self.page.get_by_role("heading", level=2).first

    @property
    def print_button(self) -> Locator:
        return self.page.get_by_role("button", name=T.PRINT)

    @property
    def home_link(self) -> Locator:
        return self.page.get_by_role("link", name=re.compile(r"^(Back to home|Home)$", re.I)).first

    @property
    def missing_alert(self) -> Locator:
        return self.page.get_by_role("alert").filter(has_text=T.RESULT_MISSING)

    def open(self) -> "ResultPage":
        self.page.goto(self.url("/payment-result"))
        return self

    def wait_final(self, timeout: int = 90_000) -> "ResultPage":
        """Chờ tới trạng thái cuối. Trang tự làm mới mỗi 2 giây khi giao dịch còn Pending."""
        expect(self.page.get_by_role("heading", name=FINAL_TITLE)).to_be_visible(timeout=timeout)
        return self

    def title(self) -> str:
        return norm(self.status_heading.inner_text())

    def facts(self) -> list[tuple[str, str]]:
        return read_dl(self.content())

    def fact(self, label: str) -> str | None:
        return dl_value(self.facts(), label)

    def funding_rows(self) -> list[tuple[str, str]]:
        """Các dòng nguồn tiền, ví dụ ('Education Account — Succeeded', 'Requested amount: ...; Settled amount: ...')."""
        return [(k, v) for k, v in self.facts() if " — " in k and ("Education Account" in k or "Online Gateway" in k)]

    def text(self) -> str:
        return self.main_text()

    def invoice_item_count(self) -> int:
        return self.page.get_by_role("list", name="Invoice items").get_by_role("listitem").count()

    def status_text(self) -> str:
        """Khối trạng thái ở đầu thẻ kết quả: tiêu đề, mô tả và câu cảnh báo về Education Account (không gồm các dòng nguồn tiền)."""
        return norm(self.status_heading.locator("xpath=..").inner_text())

    def invoice_line_numbers(self) -> list[str]:
        """Số dòng (nhãn "Line" trên biên lai) của từng dòng hóa đơn, theo thứ tự hiển thị."""
        items = self.page.get_by_role("list", name="Invoice items").get_by_role("listitem")
        return [dl_value(read_dl(item), "Line") or "" for item in items.all()]

    def transaction_id(self) -> str:
        value = self.fact("Transaction ID") or ""
        assert GUID_RE.match(value), f"Mã giao dịch trên màn kết quả không phải GUID: {value!r}"
        return value

    def amount(self, label: str):
        return money(self.fact(label) or "")
