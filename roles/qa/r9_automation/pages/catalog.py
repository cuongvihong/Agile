"""Khảo sát dữ liệu thật một lần mỗi phiên chạy: mỗi con có bao nhiêu khoản phí và số dư ví.

Test dùng Catalog để chọn con phù hợp với kịch bản (đủ tiền EA, thiếu tiền để chia khoản, ví 0, không còn phí)
thay vì gắn cứng tên. Không có con phù hợp thì test tự bỏ qua kèm lý do, không báo lỗi sai.
Catalog chỉ đọc, chụp trước khi bất kỳ test ghi dữ liệu nào chạy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

import pytest
from playwright.sync_api import Page

from pages.accounts_page import AccountsPage
from pages.billing_page import BillingPage, Charge


@dataclass
class Child:
    name: str
    code: str
    status: str
    student_id: str
    balance: Decimal
    wallet_status: str
    charges: list[Charge] = field(default_factory=list)
    error: str | None = None  # có giá trị khi trang của con này không tải được ví (con thiếu ví, ví lỗi...)

    @property
    def total(self) -> Decimal:
        return sum((c.net for c in self.charges), Decimal(0))

    def smallest(self, count: int = 1) -> list[Charge]:
        return sorted(self.charges, key=lambda c: (c.net, c.description))[:count]


@dataclass
class Catalog:
    children: list[Child]

    def usable(self) -> list[Child]:
        """Con tải được ví. Con lỗi ví (chưa có tài khoản giáo dục...) bị loại khỏi mọi bộ chọn bên dưới."""
        return [c for c in self.children if c.error is None]

    def broken(self) -> list[Child]:
        return [c for c in self.children if c.error is not None]

    def with_charges(self) -> list[Child]:
        return [c for c in self.usable() if c.charges]

    def ea_child(self) -> Child | None:
        """Có khoản phí và số dư đủ trả ít nhất khoản nhỏ nhất. Các test EA chỉ chọn vài khoản nhỏ nhất (live_smallest),
        nên không đòi ví đủ trả hết mọi khoản. Ưu tiên con có ví lớn nhất để còn đủ tiền cho nhiều lần thanh toán."""
        fits = [c for c in self.with_charges() if c.balance >= c.smallest(1)[0].net]
        return max(fits, key=lambda c: c.balance, default=None)

    def split_child(self) -> Child | None:
        """Có khoản phí, ví còn tiền nhưng không đủ trả hết: chọn hết thì được đề nghị Both.
        Ưu tiên con khác với ea_child (và lấy con đứng cuối danh sách), để test rút cạn ví không làm mất dữ liệu của test trả bằng EA."""
        candidates = [c for c in self.with_charges() if 0 < c.balance < c.total]
        ea = self.ea_child()
        others = [c for c in candidates if c is not ea]
        pool = others or candidates
        return pool[-1] if pool else None

    def zero_child(self) -> Child | None:
        """Có khoản phí nhưng ví 0.00: cần để thử bước phương thức chỉ có Online Gateway."""
        for c in self.with_charges():
            if c.balance <= 0:
                return c
        return None

    def zero_balance_child(self) -> Child | None:
        """Ví 0.00, kể cả con không còn khoản phí nào (chỉ cần để kiểm tra cách hiện số dư 0)."""
        for c in self.usable():
            if c.balance <= 0:
                return c
        return None

    def empty_child(self) -> Child | None:
        for c in self.usable():
            if not c.charges:
                return c
        return None

    def describe(self) -> str:
        return "; ".join(
            f"{c.name}: LỖI {c.error}" if c.error else f"{c.name}: {len(c.charges)} khoản, tổng {c.total}, ví {c.balance}"
            for c in self.children) or "không có con"


def build_catalog(page: Page, base_url: str) -> Catalog:
    accounts = AccountsPage(page, base_url).open()
    cards = accounts.read_all()
    billing = BillingPage(page, base_url)
    children: list[Child] = []
    for card in cards:
        try:
            billing.open(card["student_id"])
            children.append(Child(name=card["name"], code=card["code"], status=card["status"], student_id=card["student_id"],
                                  balance=billing.balance(), wallet_status=billing.wallet_status(), charges=billing.read_charges()))
        except Exception as exc:  # một con lỗi ví không được làm hỏng cả bảng khảo sát
            children.append(Child(name=card["name"], code=card["code"], status=card["status"], student_id=card["student_id"],
                                  balance=Decimal(0), wallet_status="", charges=[], error=str(exc).splitlines()[0][:120] if str(exc) else type(exc).__name__))
    return Catalog(children)


def need(item, what: str):
    """Bỏ qua test (không báo lỗi) nếu dữ liệu thật không có đối tượng phù hợp."""
    if item is None:
        print(f"\n[WARNING: TEST DATA MISSING] Skipping test because '{what}' is None.")
        pytest.skip(f"Dữ liệu hiện tại không có {what}")
    return item


def live_smallest(billing, child, count: int = 1, need_balance: bool = False):
    """Mở trang của con, đọc lại khoản phí và số dư đang có, trả (các khoản nhỏ nhất, số dư).

    Catalog chụp một lần đầu phiên, còn test ghi dữ liệu đã tiêu một số khoản, nên mọi test chọn khoản phí
    đều đọc lại từ trang. Không đủ khoản (hoặc không đủ tiền khi need_balance) thì bỏ qua test kèm lý do.
    """
    billing.open(child.student_id)
    charges = sorted(billing.read_charges(), key=lambda c: (c.net, c.description))
    balance = billing.balance()
    if len(charges) < count:
        pytest.skip(f"{child.name} còn {len(charges)} khoản phí, cần {count} (test trước có thể đã tiêu)")
    picked = charges[:count]
    if need_balance:
        total = sum((c.net for c in picked), type(balance)(0))
        if balance < total:
            pytest.skip(f"{child.name} chỉ còn ví {balance}, cần {total}")
    return picked, balance
