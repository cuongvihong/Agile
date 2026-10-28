"""Trang /billing/:studentId: chọn khoản phí, chọn phương thức, xem lại và xác nhận.

Ba bước nằm trên cùng một trang: selection (Outstanding charges), method (Payment summary), review (Review payment).
Tương ứng SCR-02, SCR-04, SCR-05 của R9, nhưng UI thật chọn khoản phí (charge), không chọn hóa đơn.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal

from playwright.sync_api import Locator, expect

from data import ui_text as T
from pages.base_page import BasePage, dl_value, money, norm, read_dl


@dataclass
class Charge:
    description: str
    gross: Decimal
    subsidy: Decimal
    net: Decimal
    due: str


class BillingPage(BasePage):
    def open(self, student_id: str) -> "BillingPage":
        self.page.goto(self.url(f"/billing/{student_id}"))
        self.wait_ready()
        return self

    # ------------------------------------------------------------ vị trí
    @property
    def h1(self) -> Locator:
        return self.page.get_by_role("heading", name=T.H_PAY, level=1)

    @property
    def charges_heading(self) -> Locator:
        return self.page.get_by_role("heading", name=T.H_CHARGES, level=2)

    @property
    def table(self) -> Locator:
        return self.page.locator("table").filter(has=self.page.locator("caption", has_text="Outstanding charges for"))

    @property
    def charge_boxes(self) -> Locator:
        return self.page.get_by_role("checkbox", name=re.compile(r"^Select charge: "))

    @property
    def select_all_box(self) -> Locator:
        return self.page.get_by_role("checkbox", name=T.SELECT_ALL)

    @property
    def empty_state(self) -> Locator:
        return self.page.get_by_text(T.EMPTY_CHARGES, exact=True)

    @property
    def table_error(self) -> Locator:
        return self.page.get_by_role("heading", name="Unable to load billing information")

    @property
    def continue_button(self) -> Locator:
        return self.page.get_by_role("button", name="Continue")

    @property
    def back_button(self) -> Locator:
        return self.page.get_by_role("button", name="Back").last

    @property
    def authorize_button(self) -> Locator:
        return self.page.get_by_role("button", name=re.compile(r"^Authorize & pay"))

    @property
    def summary_heading(self) -> Locator:
        return self.page.get_by_role("heading", name=T.H_SUMMARY, level=2)

    @property
    def review_heading(self) -> Locator:
        return self.page.get_by_role("heading", name=T.H_REVIEW, level=2)

    @property
    def selected_count(self) -> Locator:
        return self.page.get_by_text(re.compile(r"^\d+ charge\(s\) selected$"))

    def alert(self, heading: str) -> Locator:
        return self.page.get_by_role("alert").filter(has_text=heading)

    @property
    def stale_alert(self) -> Locator:
        return self.alert(T.STALE_TITLE)

    @property
    def checkout_error_alert(self) -> Locator:
        return self.alert(T.CHECKOUT_ERROR_TITLE)

    def radio(self, method: str) -> Locator:
        return self.page.locator(f'input[type="radio"][value="{method}"]')

    # ------------------------------------------------------------ chờ và đọc
    def wait_ready(self, timeout: int = 20_000) -> None:
        expect(self.h1).to_be_visible(timeout=timeout)
        err = self.page.get_by_role("heading", name=T.WALLET_ERROR).or_(self.page.get_by_role("heading", name=T.INVALID_CONTEXT))
        expect(self.charges_heading.or_(err).first).to_be_visible(timeout=timeout)
        if err.count() > 0 and err.first.is_visible():
            return
        expect(self.charge_boxes.first.or_(self.empty_state).or_(self.table_error).first).to_be_visible(timeout=timeout)

    def read_charges(self) -> list[Charge]:
        rows = self.table.locator("tbody tr").filter(has=self.page.get_by_role("checkbox"))
        out: list[Charge] = []
        for row in rows.all():
            cells = [norm(c) for c in row.locator("td").all_inner_texts()]
            if len(cells) >= 7:
                # Sprint 3 format: [checkbox, desc, gross, subsidy, reason, net, status, details]
                out.append(Charge(description=cells[1], gross=money(cells[2]) or Decimal(0),
                                  subsidy=money(cells[3]) or Decimal(0),
                                  net=money(cells[5]) or Decimal(0), due=cells[6]))
            elif len(cells) >= 6:
                out.append(Charge(description=cells[1], gross=money(cells[2]) or Decimal(0),
                                  subsidy=money(cells[3]) or Decimal(0),
                                  net=money(cells[4]) or Decimal(0), due=cells[5]))
        return out

    def table_headers(self) -> list[str]:
        return [norm(h) for h in self.table.locator("thead th").all_inner_texts()]

    def card(self, heading: str) -> Locator:
        summary_card = self.page.locator('[data-tour="billing-summary"]').locator("article, div").filter(has_text=heading)
        if summary_card.count() > 0 and summary_card.first.is_visible():
            return summary_card.first
        by_role = self.page.get_by_role("article", name=heading, exact=True)
        if by_role.count() > 0 and by_role.first.is_visible():
            return by_role.first
        return self.page.locator("article").filter(has_text=heading).first

    def card_text(self, heading: str) -> str:
        c = self.card(heading)
        if c.count() > 0:
            return norm(c.inner_text())
        return ""

    def balance(self) -> Decimal:
        value = money(self.card_text(T.CARD_BALANCE))
        assert value is not None, "Thẻ Education Account balance không có số tiền"
        return value

    def outstanding_total(self) -> Decimal:
        value = money(self.card_text(T.CARD_OUTSTANDING))
        assert value is not None, "Thẻ Outstanding fees không có số tiền"
        return value

    def child_name(self) -> str:
        caption_loc = self.table.locator("caption")
        if caption_loc.count() > 0:
            caption_text = norm(caption_loc.first.inner_text())
            m = re.search(r"Outstanding charges for\s+(.+)$", caption_text, re.I)
            if m:
                return m.group(1).strip()
        header_desc = self.page.locator('header, [data-tour-page="billing"]')
        if header_desc.count() > 0:
            m = re.search(r"charges for\s+(.+?)\s+to pay", norm(header_desc.first.inner_text()), re.I)
            if m:
                return m.group(1).strip()
        return norm(self.card_text(T.CARD_CHILD).replace(T.CARD_CHILD, "", 1))

    def wallet_line(self) -> str:
        loc = self.page.get_by_text(re.compile(r"^Student ID: "))
        return norm(loc.first.inner_text()) if loc.count() > 0 else ""

    def wallet_status(self) -> str:
        match = re.search(r"Status:\s*(.+)$", self.wallet_line())
        return match.group(1).strip() if match else ""  # bản build 25/10/2026 không hiện dòng 'Student ID ... Status' (đã bị chú thích trong BillingPaymentPage.tsx)

    def student_id(self) -> str:
        return self.page.url.rstrip("/").rsplit("/", 1)[-1].split("?")[0]

    # ------------------------------------------------------------ bước 1: chọn khoản
    def select(self, descriptions: list[str]) -> "BillingPage":
        for description in descriptions:
            self.page.get_by_role("checkbox", name=T.SELECT_CHARGE.format(description=description), exact=True).check()
        return self

    def select_all(self) -> "BillingPage":
        self.select_all_box.check()
        return self

    def to_method(self) -> "BillingPage":
        expect(self.continue_button).to_be_enabled()
        self.continue_button.click()
        expect(self.summary_heading).to_be_visible()
        return self

    # ------------------------------------------------------------ bước 2: phương thức
    def method_facts(self) -> list[tuple[str, str]]:
        card = self.page.locator("article").filter(has=self.summary_heading)
        return read_dl(card)

    def total_to_pay(self) -> Decimal:
        return money(dl_value(self.method_facts(), T.TOTAL_TO_PAY) or "") or Decimal(0)

    def method_balance(self) -> Decimal:
        """Số dư EA hiện trên bước phương thức (thẻ Payment summary)."""
        return money(dl_value(self.method_facts(), T.CARD_BALANCE) or "") or Decimal(0)

    def selected_lines(self) -> list[tuple[str, Decimal]]:
        items = self.page.get_by_role("list", name=T.SELECTED_LIST).get_by_role("listitem").all()
        out: list[tuple[str, Decimal]] = []
        for item in items:
            spans = [norm(s) for s in item.locator("span").all_inner_texts()]
            out.append((spans[0], money(spans[1]) or Decimal(0)))
        return out

    def split_facts(self) -> dict[str, Decimal]:
        """Chỉ có khi chọn Both: số tiền phần Education Account và phần Online Gateway."""
        pairs = read_dl(self.page.get_by_label(T.SPLIT_LABEL))
        return {k: money(v) or Decimal(0) for k, v in pairs}

    def split_parts(self) -> tuple[Decimal | None, Decimal | None]:
        """(phần Education Account, phần Online) của Both. Phần EA có thể là ô nhập nên đọc cả giá trị ô."""
        region = self.page.get_by_label(T.SPLIT_LABEL)
        ea = online = None
        for key, value in read_dl(region):
            if "online" in key.lower():
                online = money(value)
            elif "education" in key.lower() and money(value) is not None:
                ea = money(value)
        if ea is None:
            box = region.get_by_role("spinbutton").or_(region.get_by_role("textbox"))
            if box.count() > 0:
                ea = money(box.first.input_value())
        return ea, online

    def choose_method(self, method: str) -> "BillingPage":
        label = T.METHOD_LABEL[method]
        self.page.get_by_role("radio", name=re.compile(rf"^{re.escape(label)}")).check(force=True)
        return self

    def method_state(self) -> dict[str, dict]:
        """Với mỗi phương thức: có hiện không, có bị khóa không, có đang chọn không."""
        out: dict[str, dict] = {}
        for method in (T.METHOD_EA, T.METHOD_ONLINE, T.METHOD_BOTH):
            radio = self.radio(method)
            present = radio.count() > 0
            out[method] = {"present": present,
                           "disabled": radio.is_disabled() if present else None,
                           "checked": radio.is_checked() if present else None}
        return out

    def to_review(self) -> "BillingPage":
        self.continue_button.click()
        expect(self.review_heading).to_be_visible()
        return self

    # ------------------------------------------------------------ bước 3: xem lại
    def review_facts(self) -> list[tuple[str, str]]:
        return read_dl(self.page.get_by_role("article", name=T.H_REVIEW_AUTH, exact=True))

    def review_total(self) -> Decimal:
        card = self.page.locator("article").filter(has=self.review_heading)
        return money(dl_value(read_dl(card), T.TOTAL_TO_PAY) or "") or Decimal(0)

    def authorize(self) -> None:
        expect(self.authorize_button).to_be_enabled()
        self.authorize_button.click()

    def go_back(self) -> "BillingPage":
        self.back_button.click()
        return self

    # ------------------------------------------------------------ luồng gộp
    def start(self, descriptions: list[str], method: str | None = None) -> "BillingPage":
        """Chọn khoản, sang bước phương thức, chọn phương thức nếu cần, sang bước xem lại."""
        self.select(descriptions).to_method()
        if method:
            self.choose_method(method)
        return self.to_review()
