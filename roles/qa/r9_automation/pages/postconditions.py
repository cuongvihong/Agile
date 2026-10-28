"""Kiểm tra hậu điều kiện của R9 bản rev FS09 (trạng thái transaction, từng leg, invoice và số dư EA sau thao tác).

Bản build thật dùng mô hình khoản phí (charge), không có hóa đơn trước khi thanh toán. Cách ghép:
  invoice Issued       khoản phí vẫn nằm trong danh sách còn nợ
  invoice Paid         khoản phí đã biến mất khỏi danh sách và API hóa đơn báo Paid
  no transaction       không có POST /checkout nào được gửi trong phiên của trang
  transaction, leg     đọc qua GET /billing/v1/transactions/{id}
  EA balance           số dư trên trang của con
Ghép này là suy luận của QA (xem ASM-R9-UI-01), không phải bản đồ chính thức của BA.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from pages.base_page import snippet


@dataclass
class Snapshot:
    descriptions: list[str]
    balance: Decimal


def snapshot(billing) -> Snapshot:
    """Chụp danh sách khoản còn nợ và số dư từ trang /billing/:studentId đang mở ở bước chọn khoản."""
    return Snapshot(sorted(c.description for c in billing.read_charges()), billing.balance())


def assert_nothing_created(billing, requests_log, child, before: Snapshot, *, check_balance: bool = True) -> None:
    """Hậu điều kiện 'không có transaction nào được tạo, invoice vẫn Issued, số dư EA không đổi'.
    Mở lại trang của con để đọc trạng thái hiện tại. check_balance=False khi số dư đã bị giả lập bằng page.route."""
    assert not requests_log.posts("/checkout"), f"Đã gửi yêu cầu tạo thanh toán: {requests_log.posts('/checkout')}"
    billing.open(child.student_id)
    after = snapshot(billing)
    assert after.descriptions == before.descriptions, f"Danh sách khoản đổi: trước {before.descriptions}, sau {after.descriptions}"
    if check_balance:
        assert after.balance == before.balance, f"Số dư đổi: trước {before.balance}, sau {after.balance}"


def get_transaction(api, transaction_id: str) -> dict:
    response = api.get(f"/billing/v1/transactions/{transaction_id}")
    assert response.ok, f"Không đọc được giao dịch {transaction_id} ({response.status}): {snippet(response)}"
    return response.json()["data"]


def get_invoice(api, invoice_id: str) -> dict:
    response = api.get(f"/billing/v1/invoices/{invoice_id}")
    assert response.ok, f"Không đọc được hóa đơn {invoice_id} ({response.status}): {snippet(response)}"
    return response.json()["data"]


def legs_by_method(transaction: dict) -> dict[str, str]:
    """{'EducationAccount': 'Succeeded', 'OnlineGateway': 'Pending'} theo sequenceNumber."""
    ordered = sorted(transaction["fundingSources"], key=lambda f: f["sequenceNumber"])
    return {f["method"]: f["status"] for f in ordered}


def assert_backend_state(api, transaction_id: str, *, status: str, legs: dict[str, str], invoice: str | None = None) -> dict:
    """Đọc transaction (và invoice nếu cần) từ API và so với hậu điều kiện.
    legs là các leg phải có đúng như vậy: một method không nêu thì phải không có leg nào của method đó."""
    tx = get_transaction(api, transaction_id)
    assert tx["status"] == status, f"Transaction {transaction_id}: trạng thái {tx['status']}, mong đợi {status}"
    actual = legs_by_method(tx)
    assert actual == legs, f"Các leg của transaction: {actual}, mong đợi {legs}"
    if invoice is not None:
        inv = get_invoice(api, tx["invoiceId"])
        assert inv["status"] == invoice, f"Invoice {tx['invoiceId']}: trạng thái {inv['status']}, mong đợi {invoice}"
    return tx
