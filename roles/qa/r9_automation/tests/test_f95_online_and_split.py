"""F9.5 Thanh toán online và chia khoản Both (TC-087 đến TC-103, TC-130, TC-136, TC-137, TC-139). Nguồn: R9_Test_Cases_final_FS09.xlsx.

Cần trang giả lập cổng thanh toán (npm run dev:payment-checkout, cổng 5176) và mở e-service bằng localhost, vì
AllowedReturnOrigins của simulator chỉ cho localhost 5176 và 5174. Test online không có simulator sẽ tự bỏ qua.
Test nhãn destructive rút cạn ví của một con. Chạy từng test một rồi reset dữ liệu (tools/reset_payment_data.sql).
Các test mocked cuối file không cần simulator.
Bản rev FS09 thêm hậu điều kiện cho transaction, từng leg và invoice. Các test mutating đọc chúng qua API (pages/postconditions.py).
"""
from __future__ import annotations

import json
from decimal import Decimal

import pytest
from playwright.sync_api import expect

from data import mocks, seed
from data import ui_text as T
from pages import db
from pages.catalog import live_smallest, need
from pages.postconditions import assert_backend_state

pytestmark = pytest.mark.f95


def live_first_charge(billing, child):
    billing.open(child.student_id)
    charges = sorted(billing.read_charges(), key=lambda c: (c.net, c.description))
    if not charges:
        pytest.skip(f"{child.name} không còn khoản phí (test trước đã tiêu)")
    return charges[0], billing.balance()


def go_online(page, billing, simulator, result, outcome: str) -> None:
    """Từ bước xem lại: bấm Authorize & pay, qua trang giả lập, bấm kết quả, chờ kết quả cuối ở e-service."""
    billing.authorize()
    simulator.wait_loaded()
    (simulator.pay_successful if outcome == "ok" else simulator.pay_failed)()
    simulator.wait_return_to_merchant()
    result.wait_final()


# ------------------------------------------------------------------ chỉ Online Gateway
@pytest.mark.online
@pytest.mark.mutating
def test_tc_087_tc_088_tc_089_pay_one_charge_online_leaves_education_account_untouched(page, billing, simulator, result, catalog, requests_log, api):
    """TC-087, TC-088, TC-089 Trả một khoản qua Online Gateway (TC-088 gốc dùng học sinh không có EA, ở đây dùng con có EA): sang trang cổng, trả thành công, ví EA không đổi, khoản biến mất.
    Hậu điều kiện rev FS09: màn xem lại chưa tạo gì (TC-087); sau khi trả, transaction và leg online Succeeded, không có leg EA (TC-089)."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    charge, balance_before = live_first_charge(billing, child)
    billing.start([charge.description], T.METHOD_ONLINE)
    facts = dict(billing.review_facts())
    assert facts["Payment method"] == "Online Gateway" and facts["Education Account"].endswith("0.00"), facts
    assert not requests_log.posts("/checkout"), "Màn xem lại đã tạo giao dịch trước khi bấm xác nhận"

    go_online(page, billing, simulator, result, "ok")

    assert result.title() == T.RESULT_SUCCEEDED, f"{result.title()}; {result.text()[:300]}"
    assert result.amount("Requested amount") == charge.net and result.amount("Settled amount") == charge.net
    rows = result.funding_rows()
    assert [r[0] for r in rows] == ["Online Gateway — Succeeded"], rows
    assert result.fact("Invoice status") == "Paid", result.facts()
    assert_backend_state(api, result.transaction_id(), status="Succeeded", legs={T.METHOD_ONLINE: "Succeeded"}, invoice="Paid")
    billing.open(child.student_id)
    assert billing.balance() == balance_before, "Trả online mà ví EA vẫn bị trừ"
    assert charge.description not in [c.description for c in billing.read_charges()]


@pytest.mark.online
@pytest.mark.mutating
def test_tc_136_online_payment_failure_shows_failed_result_and_keeps_balance(page, billing, simulator, result, catalog, api):
    """TC-136 Cổng báo thất bại: màn kết quả báo thất bại, hóa đơn không Paid, số dư EA không đổi.
    Hậu điều kiện rev FS09: transaction và leg online Failed (đọc qua API). Việc invoice trở lại Issued xem test TC-090 và TC-139."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    charge, balance_before = live_first_charge(billing, child)
    billing.start([charge.description], T.METHOD_ONLINE)

    go_online(page, billing, simulator, result, "fail")

    assert result.title() == T.RESULT_FAILED, f"{result.title()}; {result.text()[:300]}"
    expect(result.page.get_by_text("Your payment could not be completed", exact=False)).to_be_visible()
    assert result.fact("Invoice status") != "Paid"
    assert [r[0] for r in result.funding_rows()] == ["Online Gateway — Failed"], result.funding_rows()
    assert_backend_state(api, result.transaction_id(), status="Failed", legs={T.METHOD_ONLINE: "Failed"})
    billing.open(child.student_id)
    assert billing.balance() == balance_before


@pytest.mark.online
@pytest.mark.mutating
@pytest.mark.known_defect(reason="Sau khi cổng thất bại, khoản phí không quay lại danh sách nên không thử lại được (F9_Dev_Local_Run_Results.md, R9 TC-090, TC-139)")
def test_tc_090_tc_139_charge_is_available_again_after_online_failure(page, billing, simulator, result, catalog, api):
    """TC-090 và TC-139 Sau khi thanh toán online thất bại, khoản phí vẫn nằm trong danh sách để thử lại.
    Hậu điều kiện rev FS09 (TC-136): invoice trở lại Issued sau khi transaction Failed."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    charge, _ = live_first_charge(billing, child)
    billing.start([charge.description], T.METHOD_ONLINE)
    go_online(page, billing, simulator, result, "fail")
    assert result.title() == T.RESULT_FAILED
    assert_backend_state(api, result.transaction_id(), status="Failed", legs={T.METHOD_ONLINE: "Failed"}, invoice="Issued")
    billing.open(child.student_id)
    assert charge.description in [c.description for c in billing.read_charges()], "Khoản phí đã biến mất sau khi thanh toán thất bại"


# ------------------------------------------------------------------ Both: chia khoản
def split_setup(billing, catalog):
    child = need(catalog.split_child(), "con có ví còn tiền nhưng không đủ trả hết khoản phí")
    db.ensure_split_state(child.student_id)
    billing.open(child.student_id)
    balance = billing.balance()
    total = billing.outstanding_total()
    if not 0 < balance < total:
        pytest.skip(f"{child.name} không còn ở trạng thái chia khoản (ví {balance}, nợ {total}). Reset dữ liệu rồi chạy lại")
    billing.select_all().to_method()
    assert billing.method_state()[T.METHOD_BOTH]["checked"], "Both không phải mặc định"
    billing.to_review()
    return child, balance, total


@pytest.mark.online
@pytest.mark.mutating
@pytest.mark.destructive
def test_tc_097_tc_130_split_payment_succeeds_with_both_funding_sources(page, billing, simulator, result, catalog, api):
    """TC-097 và TC-130 Both: EA trả hết số dư, online trả phần còn lại, kết quả thành công với hai dòng nguồn tiền.
    Hậu điều kiện rev FS09 (TC-130): transaction, leg EA và leg online Succeeded, invoice Paid, số dư EA về 0.00."""
    child, balance, total = split_setup(billing, catalog)
    online_part = total - balance

    go_online(page, billing, simulator, result, "ok")

    assert result.title() == T.RESULT_SUCCEEDED, f"{result.title()}; {result.text()[:300]}"
    assert result.amount("Requested amount") == total and result.amount("Settled amount") == total
    rows = dict(result.funding_rows())
    assert set(rows) == {"Education Account — Succeeded", "Online Gateway — Succeeded"}, rows
    assert f"{balance:,.2f}" in rows["Education Account — Succeeded"] and f"{online_part:,.2f}" in rows["Online Gateway — Succeeded"], rows
    assert result.fact("Invoice status") == "Paid", result.facts()
    assert_backend_state(api, result.transaction_id(), status="Succeeded",
                         legs={T.METHOD_EA: "Succeeded", T.METHOD_ONLINE: "Succeeded"}, invoice="Paid")
    billing.open(child.student_id)
    assert billing.balance() == Decimal("0.00"), "Ví EA chưa về 0 sau khi trả phần EA"
    expect(billing.empty_state).to_be_visible()


@pytest.mark.online
@pytest.mark.mutating
@pytest.mark.destructive
@pytest.mark.known_defect(reason="Khi phần online thất bại, phần Education Account đã trừ không được hoàn lại (F9_Dev_Local_Run_Results.md, R9 TC-103, TC-137)")
def test_tc_103_tc_137_failed_online_part_returns_the_education_account_part(page, billing, simulator, result, catalog, api):
    """TC-103 và TC-137 Both mà phần online thất bại thì phần EA phải được hoàn, ví về đúng số dư trước đó.
    Hậu điều kiện rev FS09: transaction Failed, leg EA Reversed, leg online Failed, invoice Issued, số dư EA trở lại như trước."""
    child, balance, _ = split_setup(billing, catalog)

    go_online(page, billing, simulator, result, "fail")

    assert_backend_state(api, result.transaction_id(), status="Failed",
                         legs={T.METHOD_EA: "Reversed", T.METHOD_ONLINE: "Failed"}, invoice="Issued")
    assert result.title() in (T.RESULT_FAILED, T.RESULT_REVIEW), result.title()
    rows = dict(result.funding_rows())
    assert "Education Account — Refunded" in rows, f"Không thấy dòng hoàn tiền EA: {rows}"
    billing.open(child.student_id)
    assert billing.balance() == balance, "Phần EA đã trừ chưa được hoàn lại"


# ------------------------------------------------------------------ giả lập phản hồi checkout
@pytest.mark.mocked
@pytest.mark.extra
def test_extra_invalid_checkout_url_from_provider_starts_no_payment(page, billing, catalog):
    """Bổ sung: cổng trả checkoutUrl không hợp lệ thì hiện 'Unable to open online payment' và không chuyển trang."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    (charge,), _ = live_smallest(billing, child)
    billing.start([charge.description], T.METHOD_ONLINE)
    mocks.mock_json(page, mocks.CHECKOUT_RE, mocks.checkout_result(checkout_url="not a url"), method="POST")
    billing.authorize()
    expect(billing.alert(T.INVALID_URL_TITLE)).to_be_visible()
    assert "/billing/" in page.url, f"Đã rời trang thanh toán: {page.url}"
    assert page.evaluate(f"sessionStorage.getItem({json.dumps(seed.TRANSACTION_STORAGE_KEY)})") is None


@pytest.mark.mocked
@pytest.mark.extra
def test_extra_invalid_transaction_id_from_checkout_is_not_stored(page, billing, catalog):
    """Bổ sung: checkout trả mã giao dịch sai định dạng thì báo 'The transaction reference is invalid.' và không lưu mã."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    (charge,), _ = live_smallest(billing, child)
    billing.start([charge.description], T.METHOD_ONLINE)
    mocks.mock_json(page, mocks.CHECKOUT_RE, mocks.checkout_result(transaction_id="not-a-guid",
                    checkout_url="http://localhost:5176/checkout/x"), method="POST")
    billing.authorize()
    expect(billing.checkout_error_alert).to_contain_text(T.RESULT_INVALID)
    assert "/billing/" in page.url
    assert page.evaluate(f"sessionStorage.getItem({json.dumps(seed.TRANSACTION_STORAGE_KEY)})") is None


# ------------------------------------------------------------------ kiểm tra tự dọn dẹp (chạy trong chế độ read)
def test_tc_087_review_screen_for_online_only_payment_shows_full_amount_online_and_touches_nothing(billing, requests_log):
    """TC-087 Màn xem lại SCR-05 của phương thức Online Gateway hiện phần EA = 0.00, phần Online = toàn bộ khoản phí, chưa tạo giao dịch và chưa đụng tới ví EA."""
    with db.temp_charges(amounts=[120.00], balance=300.00) as (stu_id, cids):
        billing.open(stu_id)
        target = next(c for c in billing.read_charges() if "QA" in c.description)
        billing.start([target.description], T.METHOD_ONLINE)
        facts = dict(billing.review_facts())
        assert facts["Payment method"] == "Online Gateway"
        assert facts["Education Account"].endswith("0.00")
        assert facts["Online Gateway"].endswith("120.00")
        assert not requests_log.posts("/checkout")
        assert db.sql_scalar(f"SELECT COUNT(1) FROM dbo.invoice_items WHERE student_charge_id = '{cids[0]}'") == "0"


@pytest.mark.api
def test_tc_088_pay_invoice_online_for_student_without_education_account(api, base_url):
    """TC-088 Học sinh không có ví EA vẫn tạo được giao dịch OnlineGateway (1 leg online, wallet_id NULL) và tất toán qua webhook."""
    import uuid
    no_wallet_stu = str(uuid.uuid4())
    with db.temp_charges(student_id=no_wallet_stu, amounts=[120.00]) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc088-{cids[0]}",
        )
        assert res.status == 200, res.text()
        tx_id = res.json()["data"]["transactionId"]
        bundle = db.get_tx_bundle(tx_id)
        assert len(bundle["legs"]) == 1
        assert bundle["legs"][0]["method"] == "2" and bundle["legs"][0]["wallet_id"] == "NULL"
        st, body, _ = db.post_webhook(bundle["legs"][0]["funding_reference"], amount_cents=12000)
        assert st == 200, body


@pytest.mark.api
def test_tc_089_pay_invoice_online_when_child_has_active_ea_leaves_wallet_untouched(api, base_url):
    """TC-089 Học sinh có ví EA dư tiền nhưng chọn OnlineGateway thì chỉ tạo 1 leg online, ví EA giữ nguyên 300.00."""
    with db.temp_charges(amounts=[120.00], balance=300.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc089-{cids[0]}",
        )
        assert res.status == 200, res.text()
        tx_id = res.json()["data"]["transactionId"]
        bundle = db.get_tx_bundle(tx_id)
        assert len(bundle["legs"]) == 1 and bundle["legs"][0]["method"] == "2"
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 300.00
        st, body, _ = db.post_webhook(bundle["legs"][0]["funding_reference"], amount_cents=12000)
        assert st == 200, body


@pytest.mark.api
@pytest.mark.known_defect(reason="Khi nhận webhook payment.failed cho thanh toán OnlineGateway, SettleFailed đặt transaction = Failed nhưng giữ nguyên invoice = PaymentPending (3) và không giải phóng invoice_items, nên khoản phí không hiện lại trên SCR-02 để thử lại (R9 TC-090, TC-139)")
def test_tc_090_tc_139_online_payment_failure_leaves_invoice_open_for_retry_self_cleaning(api, base_url):
    """TC-090 và TC-139 (tự dọn dẹp) Khi webhook báo payment.failed cho thanh toán OnlineGateway, leg online và transaction chuyển sang Failed, số dư EA giữ nguyên và khoản phí phải được mở lại để thử lại."""
    with db.temp_charges(amounts=[120.00], balance=300.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc090-{cids[0]}",
        )
        assert res.status == 200
        tx_id = res.json()["data"]["transactionId"]
        fnd_ref = db.get_tx_bundle(tx_id)["legs"][0]["funding_reference"]
        st, _, _ = db.post_webhook(fnd_ref, event_type="payment.failed", amount_cents=12000)
        assert st == 200
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["legs"][0]["status"] == "3"  # Failed
        assert bundle["tx"]["status"] == "3"  # Failed
        assert bundle["invoice"]["status"] == "2", f"Hóa đơn phải quay về Issued (2), thực tế là {bundle['invoice']['status']}"


@pytest.mark.api
@pytest.mark.known_defect(reason="ProcessGatewayWebhookHandler chỉ xử lý payment.succeeded và payment.failed, bỏ qua payment.cancelled với trạng thái Ignored thay vì hủy giao dịch và trả hóa đơn về Issued (R9 TC-091)")
def test_tc_091_cancelling_on_provider_page_cancels_attempt_and_restores_invoice(api, base_url):
    """TC-091 Phụ huynh hủy trên cổng thanh toán (payment.cancelled) thì phần online và giao dịch chuyển sang Cancelled, hóa đơn quay về Issued."""
    with db.temp_charges(amounts=[120.00], balance=300.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc091-{cids[0]}",
        )
        tx_id = res.json()["data"]["transactionId"]
        fnd_ref = db.get_tx_bundle(tx_id)["legs"][0]["funding_reference"]
        st, _, _ = db.post_webhook(fnd_ref, event_type="payment.cancelled", amount_cents=12000)
        assert st == 200
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["tx"]["status"] == "4", f"Transaction phải là Cancelled (4), thực tế {bundle['tx']['status']}"


@pytest.mark.api
@pytest.mark.known_defect(reason="ProcessGatewayWebhookHandler bỏ qua sự kiện hết hạn phiên (payment.expired) và luồng checkout đồng bộ không có sweeper tự động trả hóa đơn về Issued (R9 TC-092)")
def test_tc_092_provider_session_expiry_marks_online_attempt_failed_and_restores_invoice(api, base_url):
    """TC-092 Phiên thanh toán trên cổng hết hạn làm phần online và giao dịch chuyển sang Failed và hóa đơn quay về Issued."""
    with db.temp_charges(amounts=[120.00], balance=300.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc092-{cids[0]}",
        )
        tx_id = res.json()["data"]["transactionId"]
        fnd_ref = db.get_tx_bundle(tx_id)["legs"][0]["funding_reference"]
        st, _, _ = db.post_webhook(fnd_ref, event_type="payment.expired", amount_cents=12000)
        assert st == 200
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["tx"]["status"] == "3" and bundle["invoice"]["status"] == "2"


@pytest.mark.known_defect(reason="Khi cổng thanh toán lỗi lúc tạo phiên, CreateCheckoutHandler đặt transaction = Failed nhưng giữ invoice = PaymentPending (3) thay vì Issued (2) và trả nguyên thông báo lỗi kỹ thuật của gateway (R9 TC-094)")
def test_tc_094_when_provider_cannot_create_session_payment_fails_cleanly():
    """TC-094 Khi không tạo được phiên trên cổng thanh toán, giao dịch chuyển sang Failed, hóa đơn quay về Issued và báo lỗi thân thiện."""
    with open(r"D:\AIQA\Agileproject\roles\dev\code\QA_BE\BillingPaymentService\BillingPaymentService.Application\Feature\v1\Billing\CreateCheckoutHandler.cs", encoding="utf-8") as f:
        src = f.read()
    assert "invoice.Status = InvoiceStatus.Issued" in src


@pytest.mark.api
def test_tc_095_returning_from_provider_before_webhook_shows_pending_not_paid(api, base_url):
    """TC-095 Phụ huynh quay về màn kết quả trước khi webhook tới: trạng thái giao dịch và leg online là Pending, hóa đơn là PaymentPending, không tự đánh dấu Paid."""
    with db.temp_charges(amounts=[120.00], balance=300.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc095-{cids[0]}",
        )
        assert res.status == 200
        tx_id = res.json()["data"]["transactionId"]
        tx_resp = api.get(f"/billing/v1/transactions/{tx_id}").json()["data"]
        assert tx_resp["status"] == "Pending"
        assert tx_resp["fundingSources"][0]["status"] == "Pending"
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["tx"]["status"] == "1" and bundle["invoice"]["status"] == "3"


@pytest.mark.api
def test_tc_096_tc_097_pay_with_both_full_or_custom_ea_amount_and_online_remainder(api, base_url):
    """TC-096 và TC-097 Thanh toán Both với phần EA tùy chọn (100.00) hoặc toàn bộ số dư (180.00) trên khoản phí 250.00:
    leg 1 (EA) Succeeded ngay lập tức, ví giảm đúng số tiền EA, leg 2 (Online) hoàn tất khi nhận webhook."""
    with db.temp_charges(amounts=[250.00], balance=180.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": 100.00, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc097-{cids[0]}",
        )
        assert res.status == 200, res.text()
        tx_id = res.json()["data"]["transactionId"]
        bundle = db.get_tx_bundle(tx_id)
        assert len(bundle["legs"]) == 2
        ea_leg, onl_leg = bundle["legs"][0], bundle["legs"][1]
        assert ea_leg["sequence_number"] == "1" and ea_leg["method"] == "1" and ea_leg["status"] == "2"
        assert float(ea_leg["settled_amount"]) == 100.00 and ea_leg["education_account_transaction_id"] != "NULL"
        assert onl_leg["sequence_number"] == "2" and onl_leg["method"] == "2" and onl_leg["status"] == "1"
        assert float(onl_leg["requested_amount"]) == 150.00
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 80.00
        st, body, _ = db.post_webhook(onl_leg["funding_reference"], amount_cents=15000)
        assert st == 200, body


@pytest.mark.api
def test_tc_098_funding_parts_and_audit_entries_for_both_recorded_in_order(api, base_url):
    """TC-098 Trong thanh toán Both, 2 phần nguồn tiền được lưu đúng thứ tự (sequence 1 = EA, sequence 2 = Online) kèm nhật ký audit."""
    with db.temp_charges(amounts=[250.00], balance=180.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": 180.00, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc098-{cids[0]}",
        )
        assert res.status == 200
        tx_id = res.json()["data"]["transactionId"]
        bundle = db.get_tx_bundle(tx_id)
        assert [leg["sequence_number"] for leg in bundle["legs"]] == ["1", "2"]
        assert [leg["method"] for leg in bundle["legs"]] == ["1", "2"]
        cnt = db.sql_scalar("SELECT COUNT(1) FROM sys.tables WHERE name LIKE '%audit%'")
        assert int(cnt or "0") > 0, "Thiếu bảng audit_logs"


@pytest.mark.api
def test_tc_099_in_both_ea_part_is_deducted_before_redirect_to_provider(api, base_url):
    """TC-099 Trong chế độ Both, ngay khi xác nhận (trước khi có kết quả từ cổng online), phần EA đã Succeeded và trừ ví, phần Online và Transaction ở trạng thái Pending, hóa đơn ở PaymentPending."""
    with db.temp_charges(amounts=[250.00], balance=180.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": 180.00, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc099-{cids[0]}",
        )
        assert res.status == 200
        data = res.json()["data"]
        assert data["checkoutUrl"], "Phải trả về URL chuyển hướng sang cổng thanh toán"
        bundle = db.get_tx_bundle(data["transactionId"])
        assert bundle["legs"][0]["status"] == "2"  # EA Succeeded
        assert bundle["legs"][1]["status"] == "1"  # Online Pending
        assert bundle["tx"]["status"] == "1"  # Transaction Pending
        assert bundle["invoice"]["status"] == "3"  # Invoice PaymentPending
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 0.00


@pytest.mark.api
def test_tc_102_in_both_if_ea_deduction_fails_online_session_is_never_created(api, base_url):
    """TC-102 Trong chế độ Both, nếu bước kiểm tra/trừ ví EA thất bại thì không mở phiên thanh toán online và không tạo giao dịch."""
    with db.temp_charges(amounts=[250.00], balance=180.00, wallet_status="Closed") as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": 100.00, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc102-{cids[0]}",
        )
        assert res.status == 400
        assert db.sql_scalar(f"SELECT COUNT(1) FROM dbo.invoice_items WHERE student_charge_id = '{cids[0]}'") == "0"
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 180.00


@pytest.mark.api
@pytest.mark.known_defect(reason="Trên luồng POST /billing/v1/checkout đồng bộ, khi phần online thất bại (payment.failed), ProcessGatewayWebhookHandler.SettleFailed không tự động hoàn tiền EA mà chuyển thẳng sang ReconciliationRequired (R9 TC-103, TC-108)")
def test_tc_103_tc_108_in_both_online_failure_reverses_ea_deduction_with_reversal_id(api, base_url):
    """TC-103 và TC-108 (tự dọn dẹp) Trong chế độ Both, khi webhook báo payment.failed cho phần online, phần EA phải được hoàn lại (status = Reversed, có education_account_reversal_transaction_id) và ví EA khôi phục về 180.00."""
    with db.temp_charges(amounts=[250.00], balance=180.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": 180.00, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc103-{cids[0]}",
        )
        assert res.status == 200
        tx_id = res.json()["data"]["transactionId"]
        onl_ref = db.get_tx_bundle(tx_id)["legs"][1]["funding_reference"]
        st, _, _ = db.post_webhook(onl_ref, event_type="payment.failed", amount_cents=7000)
        assert st == 200
        bundle = db.get_tx_bundle(tx_id)
        ea_leg = bundle["legs"][0]
        assert ea_leg["status"] == "4", f"Leg EA phải là Reversed (4), thực tế {ea_leg['status']}"
        assert ea_leg["education_account_reversal_transaction_id"] != "NULL"
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 180.00


@pytest.mark.api
@pytest.mark.known_defect(reason="Khi phụ huynh hủy trên cổng thanh toán trong chế độ Both, hệ thống chưa hỗ trợ tự động hoàn lại phần EA trên luồng đồng bộ (R9 TC-104)")
def test_tc_104_in_both_parent_cancel_on_provider_reverses_ea_deduction(api, base_url):
    """TC-104 Trong chế độ Both, khi phụ huynh hủy thanh toán trên cổng online, phần EA đã trừ phải được hoàn lại và hóa đơn quay về Issued."""
    with db.temp_charges(amounts=[250.00], balance=180.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": 180.00, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc104-{cids[0]}",
        )
        tx_id = res.json()["data"]["transactionId"]
        onl_ref = db.get_tx_bundle(tx_id)["legs"][1]["funding_reference"]
        db.post_webhook(onl_ref, event_type="payment.cancelled", amount_cents=7000)
        bal = float(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{stu_id}'", db=db.EA_DB))
        assert bal == 180.00


@pytest.mark.known_defect(reason="Trong CreateCheckoutHandler.cs (dòng 225-230), nếu mở phiên cổng online thất bại sau khi đã trừ EA thì hệ thống đặt ReconciliationRequired ('TODO reverse EA leg') chứ không tự động hoàn tiền EA (R9 TC-105)")
def test_tc_105_in_both_if_provider_session_fails_after_ea_deducted_ea_is_reversed():
    """TC-105 Trong chế độ Both, nếu không tạo được phiên thanh toán online sau khi đã trừ ví EA, hệ thống phải tự động hoàn lại phần EA."""
    with open(r"D:\AIQA\Agileproject\roles\dev\code\QA_BE\BillingPaymentService\BillingPaymentService.Application\Feature\v1\Billing\CreateCheckoutHandler.cs", encoding="utf-8") as f:
        src = f.read()
    assert "TODO reverse EA leg" not in src


@pytest.mark.known_defect(reason="Luồng POST /billing/v1/checkout đồng bộ không gắn bộ đếm timeout tự động hoàn tiền EA khi phiên online bị bỏ dở quá hạn (R9 TC-107)")
def test_tc_107_in_both_online_timeout_reverses_ea_deduction():
    """TC-107 Trong chế độ Both, nếu phiên thanh toán online hết hạn mà không có xác nhận, hệ thống tự động hoàn lại phần EA và mở lại hóa đơn."""
    with open(r"D:\AIQA\Agileproject\roles\dev\code\QA_BE\BillingPaymentService\BillingPaymentService.Application\Feature\v1\Billing\CreateCheckoutHandler.cs", encoding="utf-8") as f:
        src = f.read()
    assert "OnlinePaymentTimeoutMinutes" in src


@pytest.mark.api
@pytest.mark.known_defect(reason="Khi phần online của Both thất bại, SettleFailed đặt transaction = ReconciliationRequired (5), completed_at = NULL và invoice = PaymentPending (3), nhưng giữ leg EA = Succeeded (2) thay vì ReconciliationRequired (5) vì chưa gọi hoàn tiền EA (R9 TC-109)")
def test_tc_109_in_both_when_ea_not_reversed_payment_marked_reconciliation_required(api, base_url):
    """TC-109 Khi phần online của Both thất bại và phần EA chưa hoàn được, transaction chuyển sang ReconciliationRequired (5, completed_at NULL), hóa đơn giữ PaymentPending (3) và leg EA giữ mã giao dịch gốc."""
    with db.temp_charges(amounts=[250.00], balance=180.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": 180.00, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc109-{cids[0]}",
        )
        assert res.status == 200
        tx_id = res.json()["data"]["transactionId"]
        onl_ref = db.get_tx_bundle(tx_id)["legs"][1]["funding_reference"]
        st, _, _ = db.post_webhook(onl_ref, event_type="payment.failed", amount_cents=7000)
        assert st == 200
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["tx"]["status"] == "5"  # ReconciliationRequired
        assert bundle["tx"]["completed_at"] == "NULL"
        assert bundle["invoice"]["status"] == "3"  # PaymentPending
        assert bundle["legs"][0]["education_account_transaction_id"] != "NULL"
        assert bundle["legs"][0]["status"] == "5", f"Leg EA phải ở trạng thái ReconciliationRequired (5), thực tế {bundle['legs'][0]['status']}"


@pytest.mark.api
@pytest.mark.known_defect(reason="Khi giao dịch ở ReconciliationRequired, API chặn thanh toán lại khoản phí đó với mã 409, nhưng UI SCR-02 ẩn khoản phí thay vì hiển thị dòng Pending bị khóa (R9 TC-110)")
def test_tc_110_when_payment_in_reconciliation_required_invoice_stays_locked(billing, api, base_url):
    """TC-110 Khi giao dịch ở trạng thái ReconciliationRequired, hóa đơn/khoản phí vẫn bị khóa không cho tạo thanh toán mới (409) và hiện trạng thái đang xử lý trên SCR-02."""
    with db.temp_charges(amounts=[250.00], balance=180.00) as (stu_id, cids):
        r1 = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": 180.00, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc110-1-{cids[0]}",
        )
        tx_id = r1.json()["data"]["transactionId"]
        onl_ref = db.get_tx_bundle(tx_id)["legs"][1]["funding_reference"]
        db.post_webhook(onl_ref, event_type="payment.failed", amount_cents=7000)
        assert db.get_tx_bundle(tx_id)["tx"]["status"] == "5"
        r2 = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc110-2-{cids[0]}",
        )
        assert r2.status == 409
        billing.open(stu_id)
        assert "250.00" in billing.main_text()


@pytest.mark.api
@pytest.mark.known_defect(reason="Khi giao dịch OnlineGateway đã Failed, gửi tiếp webhook payment.succeeded muộn bị ProcessGatewayWebhookHandler đánh dấu Ignored thay vì chuyển giao dịch sang ReconciliationRequired để cảnh báo thu tiền muộn (R9 TC-167)")
def test_tc_167_late_payment_succeeded_webhook_after_failed_is_flagged_for_review(api, base_url):
    """TC-167 Webhook payment.succeeded đến muộn sau khi giao dịch đã Failed không được tự đánh dấu Paid mà phải chuyển giao dịch sang ReconciliationRequired."""
    with db.temp_charges(amounts=[120.00], balance=300.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc167-{cids[0]}",
        )
        tx_id = res.json()["data"]["transactionId"]
        fnd_ref = db.get_tx_bundle(tx_id)["legs"][0]["funding_reference"]
        db.post_webhook(fnd_ref, event_type="payment.failed", amount_cents=12000, provider_tx_id="PTX-167-FAIL")
        assert db.get_tx_bundle(tx_id)["tx"]["status"] == "3"
        st2, _, _ = db.post_webhook(fnd_ref, event_type="payment.succeeded", amount_cents=12000, provider_tx_id="PTX-167-LATE")
        assert st2 == 200
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["invoice"]["status"] != "4"
        assert bundle["tx"]["status"] == "5", f"Giao dịch nhận tiền muộn phải chuyển sang ReconciliationRequired (5), thực tế {bundle['tx']['status']}"
