"""Giả lập phản hồi API bằng page.route cho các test có nhãn mocked.

Hợp đồng lấy từ mã nguồn e-service: phong bì ApiResponse (packages/api-client/src/types/api-response.ts),
kiểu trong features/billing-payment/api/billing-payment.types.ts và features/education-accounts/types.
"""
from __future__ import annotations

import json
import re
from typing import Any, Callable

from playwright.sync_api import Page, Route

from data import seed

STUDENTS_RE = re.compile(r"/(?:iam|education-account|bff)/v1/edu-account/students(\?.*)?$")
WALLET_RE = re.compile(r"/(?:iam|education-account|bff)/v1/edu-account/students/[^/]+/wallet")
CHARGES_RE = re.compile(r"/billing/v1/students/[^/]+/outstanding-charges")
CHECKOUT_RE = re.compile(r"/billing/v1/checkout(\?.*)?$")
TRANSACTION_RE = re.compile(r"/billing/v1/transactions/[^/?]+")
INVOICE_RE = re.compile(r"/billing/v1/invoices/[^/?]+")

def items_of(data):
    """Danh sách khoản phí còn nợ: bản mới trả {items, metadata}, bản cũ trả thẳng danh sách."""
    return data["items"] if isinstance(data, dict) and "items" in data else data


GUID_TX = "11111111-aaaa-4aaa-8aaa-111111111111"
GUID_INV = "22222222-bbbb-4bbb-8bbb-222222222222"
GUID_CHARGE = "33333333-cccc-4ccc-8ccc-333333333333"


def envelope(data: Any, status: int = 200, message: str = "", errors: list[str] | None = None) -> dict:
    ok = status < 400
    return {"isSuccess": ok, "statusCode": status, "message": message or ("OK" if ok else "Error"),
            "data": data if ok else None, "errors": [] if ok else (errors if errors is not None else [message or "Error"]),
            "timestamp": "2026-10-21T00:00:00Z"}


def respond(route: Route, data: Any = None, status: int = 200, message: str = "", errors: list[str] | None = None) -> None:
    route.fulfill(status=status, content_type="application/json",
                  body=json.dumps(envelope(data, status, message, errors)))


def mock(page: Page, pattern: re.Pattern, handler: Callable[[Route], None]) -> None:
    page.route(pattern, handler)


def mock_json(page: Page, pattern: re.Pattern, data: Any = None, status: int = 200, message: str = "",
              method: str | None = None, errors: list[str] | None = None) -> None:
    """Trả về data cho mọi request khớp pattern (và đúng method nếu có). Request khác đi tiếp ra backend thật."""
    def handler(route: Route) -> None:
        if method and route.request.method != method:
            route.continue_()
            return
        respond(route, data, status, message, errors)
    page.route(pattern, handler)


def wallet(student_id: str, name: str, balance: float, status: str | None = "Active", currency: str = "SGD") -> dict:
    """Phản hồi GET /(?:iam|education-account)/v1/edu-account/students/{id}/wallet (EducationAccountWalletResponseDto)."""
    return {"wallet": {"walletId": "55555555-eeee-4eee-8eee-555555555555", "walletCode": "EA-QA-0001",
                       "studentId": student_id, "studentName": name, "currency": currency,
                       "balance": balance, "status": status}}


def accounts_page(items: list[dict]) -> dict:
    return {"items": items, "metadata": {"page": 1, "pageSize": 6, "totalRecords": len(items),
                                         "totalPages": 1 if items else 0, "hasPreviousPage": False, "hasNextPage": False}}


def transaction(status: str, *, funding: list[dict] | None = None, requested: float = 120.0,
                settled: float | None = None, completed_at: str | None = "2026-10-21T04:30:00Z",
                tx_id: str = GUID_TX, invoice_id: str = GUID_INV) -> dict:
    return {"transactionId": tx_id, "invoiceId": invoice_id, "status": status, "requestedAmount": requested,
            "settledAmount": settled, "currencyCode": "SGD", "completedAt": completed_at,
            "fundingSources": funding if funding is not None else []}


def funding(method: str, status: str, requested: float, settled: float | None, seq: int = 1,
            reason: str | None = None) -> dict:
    return {"sequenceNumber": seq, "method": method, "status": status, "requestedAmount": requested,
            "settledAmount": settled, "providerTransactionId": None, "failureReason": reason}


def checkout_result(*, transaction_id: str = GUID_TX, checkout_url: str | None = None, method: str = "OnlineGateway",
                    status: str = "Pending", amount: float = 10.0) -> dict:
    """Phản hồi POST /billing/v1/checkout (CheckoutResult trong billing-payment.types.ts)."""
    return {"transactionId": transaction_id, "transactionReference": "TXN000001", "invoiceId": GUID_INV,
            "invoiceNumber": "INV000001", "method": method, "requestedAmount": amount, "currencyCode": "SGD",
            "status": status, "checkoutUrl": checkout_url,
            "fundingSources": [{"sequenceNumber": 1, "method": method if method != "Both" else "EducationAccount",
                                "requestedAmount": amount, "status": status, "fundingReference": "ref-1",
                                "checkoutUrl": checkout_url}]}


def invoice(net: float = 120.0, status: str = "Paid", items: int = 1) -> dict:
    line = round(net / items, 2)
    return {"id": GUID_INV, "invoiceNumber": "INV000001", "studentId": GUID_CHARGE, "schoolId": GUID_CHARGE,
            "currencyCode": "SGD", "grossAmount": net, "subsidyAmount": 0, "netAmount": net, "status": status,
            "issuedAt": "2026-10-21T04:29:00Z", "dueDate": "2026-11-15",
            "items": [{"id": f"44444444-dddd-4ddd-8ddd-{n:012d}", "lineNumber": n, "studentChargeId": GUID_CHARGE,
                       "grossAmount": line, "subsidyAmount": 0, "netAmount": line} for n in range(1, items + 1)]}


def open_result(page: Page, base_url: str, tx: dict, inv: dict | None = None, stored_id: str | None = GUID_TX) -> None:
    """Mở /payment-result với một giao dịch giả. stored_id=None nghĩa là không có mã giao dịch trong sessionStorage."""
    if stored_id is not None:
        page.add_init_script(f"sessionStorage.setItem({json.dumps(seed.TRANSACTION_STORAGE_KEY)}, {json.dumps(stored_id)});")
    mock_json(page, TRANSACTION_RE, tx)
    if inv is not None:
        mock_json(page, INVOICE_RE, inv)
    page.goto(f"{base_url}/payment-result")
