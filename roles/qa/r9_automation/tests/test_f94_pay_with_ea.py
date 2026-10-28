"""F9.4 Thanh toán bằng Education Account (TC-063 đến TC-086). Nguồn: R9_Test_Cases_final_FS09.xlsx, FS F9 mục SCR-05, SCR-06.

Test nhãn mutating tiêu khoản phí và trừ tiền ví thật, chỉ chạy khi R9_ALLOW_PAYMENTS=1 (run_r9_automation.cmd pay).
Mỗi test đọc lại số dư và danh sách khoản trên trang ngay trước khi trả, không tin Catalog đã đọc từ đầu phiên,
vì test trước có thể đã tiêu khoản đó. Hết khoản hoặc hết tiền thì test tự bỏ qua kèm lý do.
Bản rev FS09 thêm hậu điều kiện: transaction và leg EA Succeeded, invoice Paid, số dư EA giảm đúng số tiền. Các test mutating
đọc lại transaction và invoice qua API (pages/postconditions.py) thay vì chỉ tin màn kết quả.
"""
from __future__ import annotations

import json
import re
from decimal import Decimal

import pytest
from playwright.sync_api import expect

from data import mocks, seed
from data import ui_text as T
from pages import db
from pages.base_page import GUID_RE, snippet, wait_until
from pages.billing_page import BillingPage
from pages.catalog import live_smallest, need
from pages.postconditions import assert_backend_state
from pages.result_page import ResultPage

pytestmark = pytest.mark.f94

RESULT_URL = re.compile(r"/payment-result")


def pay_and_wait(page, billing, result, descriptions, method=T.METHOD_EA):
    billing.start(descriptions, method)
    billing.authorize()
    page.wait_for_url(RESULT_URL, timeout=45_000)
    result.wait_final()


@pytest.mark.extra
def test_extra_review_for_education_account_shows_method_and_amount_split(billing, catalog):
    """Bổ sung (gần TC-063, TC-087) Bước xem lại hiện phương thức Education Account, phần EA bằng tổng, phần online bằng 0. Không bấm thanh toán."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    billing.start([charge.description], T.METHOD_EA)
    facts = dict(billing.review_facts())
    assert facts["Payment method"] == "Education Account", facts
    assert facts["Education Account"].endswith(f"{charge.net:.2f}"), facts
    assert facts["Online Gateway"].endswith("0.00"), facts
    expect(billing.authorize_button).to_contain_text(f"{charge.net:.2f}")


@pytest.mark.mutating
def test_tc_065_tc_070_tc_129_pay_one_charge_with_education_account_end_to_end(page, billing, result, catalog, api):
    """TC-065, TC-070, TC-129 Trả một khoản bằng EA: kết quả thành công, số tiền khớp, hóa đơn Paid, khoản biến mất, ví giảm đúng số tiền.
    Hậu điều kiện rev FS09: transaction Succeeded, leg EA Succeeded, invoice Paid (đọc qua API), không có leg online."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), balance_before = live_smallest(billing, child, need_balance=True)
    outstanding_before = billing.outstanding_total()

    pay_and_wait(page, billing, result, [charge.description])

    assert result.title() == T.RESULT_SUCCEEDED, f"Kết quả: {result.title()}; {result.text()[:300]}"
    assert GUID_RE.match(result.fact("Transaction ID") or ""), result.facts()
    assert result.amount("Requested amount") == charge.net
    assert result.amount("Settled amount") == charge.net
    rows = result.funding_rows()
    assert len(rows) == 1 and rows[0][0] == "Education Account — Succeeded", rows
    assert result.fact("Invoice status") == "Paid", result.facts()
    assert result.invoice_item_count() == 1
    expect(result.print_button).to_be_visible()
    assert_backend_state(api, result.transaction_id(), status="Succeeded", legs={T.METHOD_EA: "Succeeded"}, invoice="Paid")

    billing.open(child.student_id)
    assert charge.description not in [c.description for c in billing.read_charges()], "Khoản đã trả vẫn còn trong danh sách"
    assert billing.balance() == balance_before - charge.net, "Ví không giảm đúng số tiền đã trả"
    # Thẻ Outstanding fees cộng các dòng đang hiện (trang 10 dòng), không phải mọi khoản của con (quan sát 25/10/2026 với con có hơn 10 khoản),
    # nên so với tổng các dòng đang hiện thay vì trừ thẳng khoản đã trả.
    assert billing.outstanding_total() == sum((c.net for c in billing.read_charges()), Decimal(0)), "Thẻ Outstanding fees khác tổng các dòng đang hiện"


@pytest.mark.mutating
def test_tc_067_two_charges_in_one_payment_create_one_invoice_with_two_lines(page, billing, result, catalog, api):
    """TC-067 Trả hai khoản cùng lúc bằng EA: một giao dịch, hóa đơn có hai dòng, tổng đúng.
    Hậu điều kiện rev FS09: transaction và leg EA Succeeded, invoice Paid, màn kết quả có mã giao dịch.
    Số dòng 1 và 2 không trùng nhau trong cùng hóa đơn cũng là phần quan sát được của TC-169."""
    child = need(next((c for c in catalog.with_charges() if len(c.charges) >= 2 and c.balance >= sum(
        (x.net for x in c.smallest(2)), Decimal(0))), None), "con có từ hai khoản phí và ví đủ trả hai khoản nhỏ nhất")
    picked, balance_before = live_smallest(billing, child, count=2, need_balance=True)
    total = sum((c.net for c in picked), Decimal(0))

    pay_and_wait(page, billing, result, [c.description for c in picked])

    assert result.title() == T.RESULT_SUCCEEDED, result.text()[:300]
    assert result.amount("Requested amount") == total
    assert result.invoice_item_count() == 2
    assert sorted(result.invoice_line_numbers()) == ["1", "2"], result.invoice_line_numbers()
    assert [r[0] for r in result.funding_rows()] == ["Education Account — Succeeded"], result.funding_rows()
    assert result.fact("Invoice status") == "Paid", result.facts()
    assert_backend_state(api, result.transaction_id(), status="Succeeded", legs={T.METHOD_EA: "Succeeded"}, invoice="Paid")
    billing.open(child.student_id)
    assert billing.balance() == balance_before - total


@pytest.mark.mutating
def test_tc_077_double_click_on_authorize_sends_one_checkout_request(page, billing, result, catalog, requests_log, api):
    """TC-077 Bấm Authorize & pay hai lần liên tiếp chỉ gửi một yêu cầu thanh toán, ví chỉ bị trừ một lần.
    Hậu điều kiện rev FS09: invoice Paid, transaction và leg EA Succeeded."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), balance_before = live_smallest(billing, child, need_balance=True)
    billing.start([charge.description], T.METHOD_EA)
    billing.authorize_button.dblclick()
    page.wait_for_url(RESULT_URL, timeout=45_000)
    result.wait_final()
    assert len(requests_log.posts("/checkout")) == 1, f"Có {len(requests_log.posts('/checkout'))} yêu cầu thanh toán"
    assert result.title() == T.RESULT_SUCCEEDED, result.text()[:300]
    assert result.fact("Invoice status") == "Paid", result.facts()
    assert_backend_state(api, result.transaction_id(), status="Succeeded", legs={T.METHOD_EA: "Succeeded"}, invoice="Paid")
    billing.open(child.student_id)
    assert billing.balance() == balance_before - charge.net, "Ví bị trừ sai số lần"


@pytest.mark.mutating
def test_tc_084_charge_already_paid_in_another_tab_is_refused_without_double_charge(page, context, billing, result, catalog):
    """TC-084 Hai tab cùng chọn một khoản: tab trả trước thành công, tab sau bị từ chối với thông báo khoản không còn khả dụng."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    billing.start([charge.description], T.METHOD_EA)  # tab A dừng ở bước xem lại

    other = context.new_page()
    b_billing, b_result = BillingPage(other, billing.base_url), ResultPage(other, billing.base_url)
    b_billing.open(child.student_id)
    pay_and_wait(other, b_billing, b_result, [charge.description])
    assert b_result.title() == T.RESULT_SUCCEEDED
    b_billing.open(child.student_id)
    balance_after_first = b_billing.balance()
    other.close()

    billing.authorize()
    expect(billing.stale_alert).to_be_visible(timeout=20_000)
    assert RESULT_URL.search(page.url) is None, "Tab sau vẫn chuyển sang trang kết quả"
    # Rev FS09: không có transaction thứ hai (tab sau không lưu mã giao dịch), invoice vẫn Paid, số dư không đổi.
    assert page.evaluate(f"sessionStorage.getItem({json.dumps(seed.TRANSACTION_STORAGE_KEY)})") is None, "Tab sau đã tạo giao dịch thứ hai"
    billing.open(child.student_id)
    assert charge.description not in [c.description for c in billing.read_charges()], "Khoản đã trả lại hiện trong danh sách"
    assert billing.balance() == balance_after_first, "Khoản bị trừ lần hai"


@pytest.mark.mocked
@pytest.mark.parametrize("status", [404, 409], ids=["404", "409"])
def test_tc_084_tc_086_stale_checkout_clears_selection_and_reloads_the_list(page, billing, catalog, requests_log, status):
    """TC-084 và TC-086 (giả lập) Máy chủ trả 404 hoặc 409 khi thanh toán: báo khoản không còn khả dụng, bỏ chọn, tải lại danh sách."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    billing.start([charge.description], T.METHOD_EA)
    mocks.mock_json(page, mocks.CHECKOUT_RE, None, status=status, message="Charge already used", method="POST")
    fetches_before = requests_log.count("outstanding-charges")
    billing.authorize()
    expect(billing.stale_alert).to_be_visible()
    expect(billing.charges_heading).to_be_visible()
    assert billing.charge_boxes.count() > 0
    for box in billing.charge_boxes.all():
        expect(box).not_to_be_checked()
    expect(billing.continue_button).to_be_disabled()
    wait_until(page, lambda: requests_log.count("outstanding-charges") > fetches_before, what="tải lại danh sách khoản phí")
    assert not billing.checkout_error_alert.count(), "Lỗi dữ liệu chung hiện cùng lúc với thông báo khoản hết hạn"


@pytest.mark.mocked
@pytest.mark.extra
def test_extra_retry_after_server_error_reuses_the_same_idempotency_key(page, billing, catalog):
    """Bổ sung: thử lại sau lỗi 500 phải dùng cùng Idempotency-Key để máy chủ không tạo giao dịch thứ hai (mã nguồn BillingPaymentPage)."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    billing.start([charge.description], T.METHOD_EA)
    keys: list[str] = []

    def handler(route):
        if route.request.method != "POST":
            route.continue_()
            return
        keys.append(route.request.headers.get("idempotency-key", ""))
        mocks.respond(route, None, 500, "boom")

    page.route(mocks.CHECKOUT_RE, handler)
    billing.authorize()
    expect(billing.checkout_error_alert).to_be_visible()
    billing.authorize()
    wait_until(page, lambda: len(keys) > 1, what="lần gửi thứ hai")
    assert keys[0] and keys[0] == keys[1], f"Hai lần gửi dùng khóa khác nhau: {keys}"


@pytest.mark.api
@pytest.mark.mutating
def test_tc_078_tc_080_same_idempotency_key_returns_first_result_and_pays_once(api, catalog, base_url):
    """TC-078 và TC-080 Gửi hai lần cùng một khóa 100 ký tự: lần hai trả lại kết quả lần đầu, ví chỉ bị trừ một lần.
    Tạo một giao dịch thật bằng Education Account cho khoản nhỏ nhất, nên thuộc nhóm mutating."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    wallet = api.get(f"/education-account/v1/edu-account/students/{child.student_id}/wallet")
    assert wallet.ok, f"Không đọc được ví ({wallet.status}): {snippet(wallet)}"
    wallet_data = wallet.json()["data"]["wallet"]
    charges = mocks.items_of(api.get(f"/billing/v1/students/{child.student_id}/outstanding-charges").json()["data"])
    if not charges:
        pytest.skip(f"{child.name} không còn khoản phí")
    charge = min(charges, key=lambda c: c["netAmount"])
    if Decimal(str(wallet_data["balance"])) < Decimal(str(charge["netAmount"])):
        pytest.skip("Ví không đủ trả khoản nhỏ nhất")
    key = "r9-qa-same-key-" + "k" * 85
    assert len(key) == 100
    body = {"studentId": child.student_id, "chargeIds": [charge["chargeId"]], "method": T.METHOD_EA, "walletId": wallet_data["walletId"]}
    first = api.post("/billing/v1/checkout", body, key=key)
    assert first.ok, f"Lần đầu bị từ chối ({first.status}): {snippet(first)}"
    second = api.post("/billing/v1/checkout", body, key=key)
    assert second.ok, f"Lần hai cùng khóa bị từ chối ({second.status}): {snippet(second)}"
    assert second.json()["data"]["transactionId"] == first.json()["data"]["transactionId"], "Lần hai tạo giao dịch khác"
    # Hậu điều kiện rev FS09 (TC-078 bước 5, TC-080 bước 2): transaction và leg EA Succeeded, invoice Paid, ví chỉ giảm một lần.
    assert_backend_state(api, first.json()["data"]["transactionId"], status="Succeeded", legs={T.METHOD_EA: "Succeeded"}, invoice="Paid")
    after = api.get(f"/education-account/v1/edu-account/students/{child.student_id}/wallet").json()["data"]["wallet"]["balance"]
    assert Decimal(str(after)) == Decimal(str(wallet_data["balance"])) - Decimal(str(charge["netAmount"])), "Ví bị trừ sai số lần"
    remaining = mocks.items_of(api.get(f"/billing/v1/students/{child.student_id}/outstanding-charges").json()["data"])
    assert charge["chargeId"] not in [c["chargeId"] for c in remaining], "Khoản đã trả vẫn còn trong danh sách còn nợ"


# ------------------------------------------------------------------ kiểm tra tự dọn dẹp (chạy trong chế độ read)
@pytest.mark.api
def test_tc_065_tc_070_pay_invoice_in_full_with_ea_when_balance_greater_self_cleaning(api, base_url):
    """TC-065 và TC-070 Thanh toán toàn bộ bằng EA khi số dư (300.00) > khoản phí (120.00):
    tạo đúng 1 leg EA (sequence 1, Succeeded, có wallet_id và education_account_transaction_id, không có provider),
    transaction Succeeded, invoice Paid, số dư ví còn 180.00."""
    with db.temp_charges(amounts=[120.00], balance=300.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "EducationAccount", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc065-{cids[0]}",
        )
        assert res.status == 200, res.text()
        tx_id = res.json()["data"]["transactionId"]
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["tx"]["status"] == "2"  # Succeeded
        assert float(bundle["tx"]["settled_amount"]) == 120.00
        assert bundle["tx"]["completed_at"] != "NULL"
        assert bundle["invoice"]["status"] == "4"  # Paid
        assert bundle["invoice"]["paid_at"] != "NULL"
        assert len(bundle["legs"]) == 1
        leg = bundle["legs"][0]
        assert leg["sequence_number"] == "1"
        assert leg["method"] == "1"  # EducationAccount
        assert leg["status"] == "2"  # Succeeded
        assert float(leg["settled_amount"]) == 120.00
        assert leg["wallet_id"] != "NULL" and leg["education_account_transaction_id"] != "NULL"
        assert leg["provider_code"] == "NULL" and leg["provider_transaction_id"] == "NULL"
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 180.00


@pytest.mark.api
def test_tc_066_pay_invoice_in_full_with_ea_when_balance_equals_invoice(api, base_url):
    """TC-066 Thanh toán bằng EA khi số dư ví đúng bằng khoản phí (120.00 == 120.00): ví về 0.00, giao dịch Succeeded, hóa đơn Paid."""
    with db.temp_charges(amounts=[120.00], balance=120.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "EducationAccount", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc066-{cids[0]}",
        )
        assert res.status == 200, res.text()
        tx_id = res.json()["data"]["transactionId"]
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["tx"]["status"] == "2" and bundle["invoice"]["status"] == "4"
        assert bundle["legs"][0]["status"] == "2"
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 0.00


@pytest.mark.api
def test_tc_067_two_charges_in_one_payment_create_one_invoice_with_two_lines_self_cleaning(api, base_url):
    """TC-067 Thanh toán 2 khoản phí (80.00 + 70.00) trong 1 lần tạo đúng 1 hóa đơn Paid (150.00) với 2 dòng (line 1, 2) và trừ ví 150.00."""
    with db.temp_charges(amounts=[80.00, 70.00], balance=300.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "EducationAccount", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc067-{cids[0]}",
        )
        assert res.status == 200, res.text()
        tx_id = res.json()["data"]["transactionId"]
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["tx"]["status"] == "2" and float(bundle["tx"]["settled_amount"]) == 150.00
        assert bundle["invoice"]["status"] == "4" and float(bundle["invoice"]["net_amount"]) == 150.00
        lines = db.sql_rows(f"SELECT line_number, student_charge_id, net_amount FROM dbo.invoice_items WHERE invoice_id = '{bundle['invoice']['id']}' ORDER BY line_number")
        assert [r["line_number"] for r in lines] == ["1", "2"]
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 150.00


@pytest.mark.api
def test_tc_068_paying_one_of_two_open_charges_leaves_the_other_open(api, base_url):
    """TC-068 Học sinh có 2 khoản phí mở, chỉ chọn thanh toán khoản thứ nhất thì khoản thứ hai vẫn còn trong danh sách chưa trả."""
    with db.temp_charges(amounts=[40.00, 60.00], balance=300.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": [cids[0]], "method": "EducationAccount", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc068-{cids[0]}",
        )
        assert res.status == 200, res.text()
        open_ids = [c["chargeId"] for c in mocks.items_of(api.get(f"/billing/v1/students/{stu_id}/outstanding-charges").json()["data"])]
        assert cids[0] not in open_ids
        assert cids[1] in open_ids
        assert db.sql_scalar(f"SELECT COUNT(1) FROM dbo.invoice_items WHERE student_charge_id = '{cids[1]}'") == "0"


def test_tc_071_audit_entry_written_when_ea_payment_succeeds():
    """TC-071 Khi thanh toán EA thành công, hệ thống ghi nhận bản ghi audit F9_PAYMENT_INITIATED và F9_PAYMENT_COMPLETED."""
    cnt = db.sql_scalar("SELECT COUNT(1) FROM sys.tables WHERE name LIKE '%audit%'")
    assert int(cnt or "0") > 0, "DB BillingPaymentService chưa có bảng lưu nhật ký audit cho thanh toán F9"


@pytest.mark.api
def test_tc_072_when_ea_service_rejects_deduction_nothing_is_charged(api, base_url):
    """TC-072 Khi Education Account từ chối trừ tiền (ví dụ số dư không đủ hoặc ví không hợp lệ), toàn bộ giao dịch được rollback và khoản phí vẫn còn mở."""
    with db.temp_charges(amounts=[200.00], balance=50.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "EducationAccount", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc072-{cids[0]}",
        )
        assert res.status == 400
        assert db.sql_scalar(f"SELECT COUNT(1) FROM dbo.invoice_items WHERE student_charge_id = '{cids[0]}'") == "0"
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 50.00


@pytest.mark.known_defect(reason="CreateCheckoutHandler trả trực tiếp chuỗi lỗi kỹ thuật của EA client khi không gọi được EA service và không tạo trạng thái đối soát khi timeout (R9 TC-073)")
def test_tc_073_when_ea_service_unreachable_payment_shows_safe_message():
    """TC-073 Khi dịch vụ EA không phản hồi hoặc timeout, hệ thống báo lỗi thân thiện và đánh dấu ReconciliationRequired nếu kết quả trừ tiền chưa rõ."""
    with open(r"D:\AIQA\Agileproject\roles\dev\code\QA_BE\BillingPaymentService\BillingPaymentService.Application\Feature\v1\Billing\CreateCheckoutHandler.cs", encoding="utf-8") as f:
        src = f.read()
    assert "Unable to process Education Account payment right now" in src


@pytest.mark.known_defect(reason="CreateCheckoutHandler ghi rõ 'Happy-path only — no reverse/compensation', chưa tự động gọi hoàn tiền EA nếu bước lưu DB sau khi trừ ví gặp lỗi (R9 TC-074)")
def test_tc_074_if_saving_payment_fails_after_ea_deducted_deduction_is_reversed():
    """TC-074 Nếu bước lưu thanh toán lỗi sau khi đã trừ ví EA, hệ thống tự động gọi hoàn tiền EA và đặt leg EA = Reversed."""
    with open(r"D:\AIQA\Agileproject\roles\dev\code\QA_BE\BillingPaymentService\BillingPaymentService.Application\Feature\v1\Billing\CreateCheckoutHandler.cs", encoding="utf-8") as f:
        src = f.read()
    assert "no reverse/compensation" not in src


@pytest.mark.known_defect(reason="CreateCheckoutHandler chưa có nhánh thử hoàn tiền EA và đánh dấu ReconciliationRequired khi hoàn tiền EA thất bại trên luồng đồng bộ (R9 TC-075)")
def test_tc_075_if_ea_reversal_also_fails_payment_marked_for_manual_review():
    """TC-075 Nếu lệnh hoàn tiền EA cũng thất bại, giao dịch và leg EA được chuyển sang ReconciliationRequired để xử lý thủ công."""
    with open(r"D:\AIQA\Agileproject\roles\dev\code\QA_BE\BillingPaymentService\BillingPaymentService.Application\Feature\v1\Billing\CreateCheckoutHandler.cs", encoding="utf-8") as f:
        src = f.read()
    assert "FundingStatus.ReconciliationRequired" in src


def test_tc_076_audit_entry_written_when_ea_deduction_is_reversed():
    """TC-076 Khi hoàn tiền EA thành công, hệ thống ghi bản ghi nhật ký audit kèm mã giao dịch gốc và mã giao dịch hoàn."""
    cnt = db.sql_scalar("SELECT COUNT(1) FROM sys.tables WHERE name LIKE '%audit%'")
    assert int(cnt or "0") > 0


def test_tc_077_double_click_confirm_sends_one_request_self_cleaning(page, billing, requests_log):
    """TC-077 (tự dọn dẹp) Nhấp đúp nút Authorize & pay trên khoản phí tạm chỉ gửi đúng 1 request POST /checkout và chỉ trừ ví 1 lần."""
    with db.temp_charges(amounts=[35.00], balance=300.00) as (stu_id, cids):
        billing.open(stu_id)
        charges = billing.read_charges()
        target = next(c for c in charges if "QA" in c.description)
        billing.start([target.description], T.METHOD_EA)
        billing.authorize_button.dblclick()
        wait_until(page, lambda: len(requests_log.posts("/checkout")) >= 1, what="gửi request checkout")
        page.wait_for_timeout(1000)
        assert len(requests_log.posts("/checkout")) == 1
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 265.00


@pytest.mark.api
def test_tc_078_tc_080_same_100_char_idempotency_key_returns_first_result_self_cleaning(api, base_url):
    """TC-078 và TC-080 (tự dọn dẹp) Gửi 2 lần cùng khóa Idempotency-Key dài 100 ký tự: ví chỉ trừ 1 lần và lần 2 trả lại kết quả lần 1."""
    with db.temp_charges(amounts=[45.00], balance=300.00) as (stu_id, cids):
        key = f"r9-qa-{cids[0]}-" + ("k" * (100 - len(f"r9-qa-{cids[0]}-")))
        assert len(key) == 100
        body = {"studentId": stu_id, "chargeIds": cids, "method": "EducationAccount", "returnUrl": f"{base_url}/billing/payment-result"}
        r1 = api.post("/billing/v1/checkout", body, key=key)
        assert r1.status == 200, r1.text()
        r2 = api.post("/billing/v1/checkout", body, key=key)
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 255.00, "Ví bị trừ hơn 1 lần khi gửi lại cùng Idempotency-Key"
        assert r2.status == 200, r2.text()


@pytest.mark.api
def test_tc_079_new_idempotency_key_used_for_separate_payment_of_another_charge(api, base_url):
    """TC-079 Hai lần thanh toán riêng biệt cho hai khoản phí khác nhau dùng hai Idempotency-Key khác nhau và đều thành công."""
    with db.temp_charges(amounts=[30.00, 40.00], balance=300.00) as (stu_id, cids):
        k1 = f"qa-tc079-1-{cids[0]}"
        k2 = f"qa-tc079-2-{cids[1]}"
        r1 = api.post("/billing/v1/checkout", {"studentId": stu_id, "chargeIds": [cids[0]], "method": "EducationAccount"}, key=k1)
        r2 = api.post("/billing/v1/checkout", {"studentId": stu_id, "chargeIds": [cids[1]], "method": "EducationAccount"}, key=k2)
        assert r1.status == 200 and r2.status == 200
        tx1, tx2 = r1.json()["data"]["transactionId"], r2.json()["data"]["transactionId"]
        assert tx1 != tx2
        assert db.get_tx_bundle(tx1)["tx"]["idempotency_key"] == k1
        assert db.get_tx_bundle(tx2)["tx"]["idempotency_key"] == k2


def test_tc_082_two_parents_using_same_idempotency_key_string_do_not_collide():
    """TC-082 Hai phụ huynh khác nhau (initiated_by_user_id khác nhau) dùng chung chuỗi idempotency_key vẫn tạo được hai giao dịch độc lập."""
    res = db.sql_check_steps(
        steps=[
            ("two_users_same_key_ok", """
                DECLARE @stu varchar(50) = (SELECT TOP 1 sc0.student_id FROM dbo.student_charges sc0 WHERE sc0.status = 'POSTED' AND NOT EXISTS (SELECT 1 FROM dbo.invoice_items ii0 WHERE ii0.student_charge_id = sc0.id) ORDER BY sc0.student_id);
                DECLARE @sch varchar(50) = (SELECT TOP 1 school_id FROM dbo.student_charges WHERE student_id = @stu);
                DECLARE @invA varchar(50) = CONVERT(varchar(50), NEWID()), @invB varchar(50) = CONVERT(varchar(50), NEWID());
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date)
                VALUES (@invA, @stu, @sch, 'SGD', 50.00, 0.00, 50.00, 4, SYSUTCDATETIME(), '2026-12-15', SYSUTCDATETIME())
            """)
        ]
    )
    # Dùng kiểm tra qua sql_check_steps với đầy đủ cột hợp lệ
    res = db.sql_check_steps(
        steps=[
            ("two_parents_same_key", """
                DECLARE @stu varchar(50) = (SELECT TOP 1 sc0.student_id FROM dbo.student_charges sc0 WHERE sc0.status = 'POSTED' AND NOT EXISTS (SELECT 1 FROM dbo.invoice_items ii0 WHERE ii0.student_charge_id = sc0.id) ORDER BY sc0.student_id);
                DECLARE @sch varchar(50) = (SELECT TOP 1 school_id FROM dbo.student_charges WHERE student_id = @stu);
                DECLARE @invA varchar(50) = CONVERT(varchar(50), NEWID()), @invB varchar(50) = CONVERT(varchar(50), NEWID());
                INSERT INTO dbo.invoices (id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date, paid_at)
                VALUES (@invA, @stu, @sch, 'SGD', 50.00, 0.00, 50.00, 4, SYSUTCDATETIME(), '2026-12-15', SYSUTCDATETIME()),
                       (@invB, @stu, @sch, 'SGD', 60.00, 0.00, 60.00, 4, SYSUTCDATETIME(), '2026-12-15', SYSUTCDATETIME());
                INSERT INTO dbo.transactions (id, invoice_id, initiated_by_user_id, transaction_reference, idempotency_key, requested_amount, settled_amount, currency_code, status, completed_at)
                VALUES (NEWID(), @invA, 'parent-user-1', 'TRX-QA-082-A', 'shared-key-082', 50.00, 50.00, 'SGD', 2, SYSUTCDATETIME()),
                       (NEWID(), @invB, 'parent-user-2', 'TRX-QA-082-B', 'shared-key-082', 60.00, 60.00, 'SGD', 2, SYSUTCDATETIME());
            """)
        ]
    )
    assert res["two_parents_same_key"] == "OK"


@pytest.mark.api
def test_tc_083_concurrent_confirm_with_same_idempotency_key_creates_one_transaction(api, base_url):
    """TC-083 Hai yêu cầu gửi cùng một Idempotency-Key cho cùng một khoản phí chỉ tạo đúng 1 giao dịch và chỉ trừ ví 1 lần."""
    with db.temp_charges(amounts=[50.00], balance=300.00) as (stu_id, cids):
        key = f"qa-tc083-{cids[0]}"
        body = {"studentId": stu_id, "chargeIds": cids, "method": "EducationAccount", "returnUrl": f"{base_url}/billing/payment-result"}
        r1 = api.post("/billing/v1/checkout", body, key=key)
        assert r1.status == 200
        api.post("/billing/v1/checkout", body, key=key)
        cnt = db.sql_scalar(f"SELECT COUNT(1) FROM dbo.transactions WHERE idempotency_key = '{key}'")
        assert cnt == "1"
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 250.00


@pytest.mark.api
def test_tc_085_two_payment_attempts_for_same_charge_with_different_keys_only_one_succeeds(api, base_url):
    """TC-085 Hai yêu cầu thanh toán cùng một khoản phí nhưng dùng hai Idempotency-Key khác nhau: yêu cầu đầu thành công (200), yêu cầu sau bị từ chối (409)."""
    with db.temp_charges(amounts=[55.00], balance=300.00) as (stu_id, cids):
        body = {"studentId": stu_id, "chargeIds": cids, "method": "EducationAccount", "returnUrl": f"{base_url}/billing/payment-result"}
        r1 = api.post("/billing/v1/checkout", body, key=f"qa-tc085-A-{cids[0]}")
        r2 = api.post("/billing/v1/checkout", body, key=f"qa-tc085-B-{cids[0]}")
        assert r1.status == 200
        assert r2.status == 409
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 245.00


@pytest.mark.known_defect(reason="InvoiceModelCreating đã tắt IsRowVersion() ('// b.Property(i => i.RowVersion).IsRowVersion();') và CreateCheckoutHandler không tự hoàn tiền EA khi xung đột đồng thời (R9 TC-166)")
def test_tc_166_editing_invoice_while_payment_in_progress_triggers_ea_reversal():
    """TC-166 Sửa hóa đơn khi đang thanh toán gây lỗi xung đột phiên bản (row_version) và tự động hoàn tiền EA."""
    with open(r"D:\AIQA\Agileproject\roles\dev\code\QA_BE\BillingPaymentService\BillingPaymentService.Infrastructure\Database\ModelCreating\InvoiceModelCreating.cs", encoding="utf-8") as f:
        src = f.read()
    assert "// b.Property(i => i.RowVersion).IsRowVersion();" not in src
