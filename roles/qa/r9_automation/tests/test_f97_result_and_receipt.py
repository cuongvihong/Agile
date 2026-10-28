"""F9.7 Màn kết quả và biên lai (TC-125 đến TC-144). Nguồn: R9_Test_Cases_final_FS09.xlsx, FS F9 mục SCR-06, SCR-07, SCR-08.

Toàn bộ test trong file này giả lập phản hồi GET /billing/v1/transactions/{id} và /invoices/{id} bằng page.route,
nên không tạo giao dịch thật và chạy lại được. Các trạng thái Pending, Failed, ReconciliationRequired khó gây ra bằng dữ liệu thật.
UI thật chỉ có hai nút ở màn kết quả: Print receipt (khi thành công và đã có hóa đơn) và Back to home.
Bản rev FS09 ghi thêm trạng thái transaction, leg và invoice vào Expected. Màn kết quả hiện được trạng thái transaction (tiêu đề),
trạng thái từng leg (dòng nguồn tiền) và trạng thái invoice (chỉ khi transaction Succeeded). Số dư EA và nhật ký ngoài màn này.
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data import mocks
from data import ui_text as T
from pages import db
from pages.base_page import GUID_RE, wait_until
from pages.catalog import live_smallest, need

pytestmark = [pytest.mark.f97, pytest.mark.mocked]

TECHNICAL = re.compile(r"exception|stack ?trace|sqlexception|\bsql\b|nullreference|\bat system\.|internal server|gateway-\d", re.I)


def ea_ok(amount=120.0):
    return mocks.funding("EducationAccount", "Succeeded", amount, amount)


def show(page, base_url, tx, inv=None):
    mocks.open_result(page, base_url, tx, inv)


# ------------------------------------------------------------------ đang xử lý
def test_tc_125_pending_screen_says_processing_and_offers_no_failure_or_retry(page, base_url, result):
    """TC-125 Màn chờ báo đang xử lý, có mã giao dịch và nút về trang chủ, không nói thất bại, không có Try again.
    Hậu điều kiện rev FS09: transaction Pending và leg online Pending (invoice PaymentPending không hiện trên màn này)."""
    show(page, base_url, mocks.transaction("Pending", funding=[mocks.funding("OnlineGateway", "Pending", 120.0, None)], completed_at=None))
    expect(result.status_heading).to_have_text(T.RESULT_PENDING)
    assert [k for k, _ in result.funding_rows()] == ["Online Gateway — Pending"], result.funding_rows()
    expect(page.get_by_text("Your payment is still being confirmed", exact=False)).to_be_visible()
    assert result.fact("Transaction ID") == mocks.GUID_TX
    expect(result.home_link).to_be_visible()
    assert not re.search(r"failed|could not be completed", result.text(), re.I), result.text()
    assert page.get_by_role("button", name=re.compile("try again|retry", re.I)).count() == 0
    assert result.print_button.count() == 0, "Chưa thành công mà đã cho in biên lai"


def test_tc_126_waiting_screen_turns_into_success_without_reload(page, base_url, result):
    """TC-126 Màn chờ tự chuyển sang thành công khi kết quả về, không cần tải lại trang (trang hỏi lại mỗi 2 giây)."""
    calls = {"n": 0}

    def handler(route):
        calls["n"] += 1
        if calls["n"] <= 2:
            mocks.respond(route, mocks.transaction("Pending", funding=[mocks.funding("OnlineGateway", "Pending", 120.0, None)], completed_at=None))
        else:
            mocks.respond(route, mocks.transaction("Succeeded", funding=[mocks.funding("OnlineGateway", "Succeeded", 120.0, 120.0)], settled=120.0))

    page.add_init_script(f"sessionStorage.setItem('edusave.billingPayment.transactionId', '{mocks.GUID_TX}');")
    page.route(mocks.TRANSACTION_RE, handler)
    mocks.mock_json(page, mocks.INVOICE_RE, mocks.invoice(120.0))
    page.goto(f"{base_url}/payment-result")
    expect(result.status_heading).to_have_text(T.RESULT_PENDING)
    expect(result.status_heading).to_have_text(T.RESULT_SUCCEEDED, timeout=30_000)
    assert calls["n"] >= 3
    # Rev FS09: sau khi kết quả về, leg online và transaction Succeeded, invoice Paid.
    expect(page.get_by_text("Paid", exact=True)).to_be_visible(timeout=15_000)
    assert [k for k, _ in result.funding_rows()] == ["Online Gateway — Succeeded"], result.funding_rows()
    assert result.fact("Invoice status") == "Paid", result.facts()


@pytest.mark.known_defect(reason="Màn chờ của thanh toán chia khoản chỉ hiện dòng nguồn tiền, không có câu nói phần Education Account đã được giữ (R9 TC-101). Suy ra từ mã nguồn PaymentResultPage")
def test_tc_101_pending_split_says_education_account_part_is_already_taken(page, base_url, result):
    """TC-101 Khi phần online còn chờ, màn hình nói rõ phần Education Account đã được trừ."""
    funding = [mocks.funding("EducationAccount", "Succeeded", 20.0, 20.0, seq=1), mocks.funding("OnlineGateway", "Pending", 30.0, None, seq=2)]
    show(page, base_url, mocks.transaction("Pending", funding=funding, requested=50.0, settled=None, completed_at=None))
    expect(result.status_heading).to_have_text(T.RESULT_PENDING)
    # Rev FS09 bước 4: transaction Pending, leg EA Succeeded, leg online Pending. Phần này UI đã hiện đúng.
    assert [k for k, _ in result.funding_rows()] == ["Education Account — Succeeded", "Online Gateway — Pending"], result.funding_rows()
    assert re.search(r"education account.{0,60}(already|taken|deducted|reserved)", result.text(), re.I), result.text()


# ------------------------------------------------------------------ thành công
def test_tc_129_success_screen_of_education_account_payment_shows_reference_time_part_and_total(page, base_url, result):
    """TC-129 Màn thành công của thanh toán EA hiện mã giao dịch, thời gian, phần EA và tổng."""
    show(page, base_url, mocks.transaction("Succeeded", funding=[ea_ok()], settled=120.0), mocks.invoice(120.0))
    expect(result.status_heading).to_have_text(T.RESULT_SUCCEEDED)
    expect(result.print_button).to_be_visible()
    assert GUID_RE.match(result.fact("Transaction ID") or "")
    assert result.fact("Completed at") not in (None, "—")
    assert str(result.amount("Requested amount")) == "120.00" and str(result.amount("Settled amount")) == "120.00"
    assert [k for k, _ in result.funding_rows()] == ["Education Account — Succeeded"]
    assert result.fact("Invoice status") == "Paid" and result.fact("Invoice number") == "INV000001"
    # Rev FS09 bước 3: transaction và leg EA Succeeded, invoice Paid (số dư EA 150.00 không hiện trên màn này, xem TC-065).


def test_tc_130_success_screen_of_split_payment_shows_both_parts(page, base_url, result):
    """TC-130 Màn thành công của thanh toán chia khoản hiện cả phần EA và phần online."""
    funding = [mocks.funding("EducationAccount", "Succeeded", 20.0, 20.0, seq=1),
               mocks.funding("OnlineGateway", "Succeeded", 30.0, 30.0, seq=2)]
    show(page, base_url, mocks.transaction("Succeeded", funding=funding, requested=50.0, settled=50.0), mocks.invoice(50.0))
    expect(result.status_heading).to_have_text(T.RESULT_SUCCEEDED)
    rows = dict(result.funding_rows())
    assert set(rows) == {"Education Account — Succeeded", "Online Gateway — Succeeded"}, rows
    assert "20.00" in rows["Education Account — Succeeded"] and "30.00" in rows["Online Gateway — Succeeded"], rows
    assert str(result.amount("Settled amount")) == "50.00"
    assert result.fact("Invoice status") == "Paid", result.facts()


@pytest.mark.known_defect(reason="Biên lai chỉ có nút Print receipt, không có tải PDF (R9 TC-131, TC-132). Suy ra từ mã nguồn PaymentResultPage")
def test_tc_131_tc_132_receipt_pdf_can_be_downloaded(page, base_url, result):
    """TC-131 và TC-132 Biên lai có nút tải PDF."""
    show(page, base_url, mocks.transaction("Succeeded", funding=[ea_ok()], settled=120.0), mocks.invoice(120.0))
    expect(result.status_heading).to_have_text(T.RESULT_SUCCEEDED)
    target = page.get_by_role("button", name=re.compile(r"download|pdf", re.I)).or_(page.get_by_role("link", name=re.compile(r"download|pdf", re.I)))
    assert target.count() >= 1, "Không có nút hay liên kết tải PDF"


def test_tc_133_print_receipt_opens_the_print_dialog(page, base_url, result):
    """TC-133 Nút Print receipt gọi lệnh in của trình duyệt (window.print được thay bằng bộ đếm để khỏi mở hộp thoại thật)."""
    page.add_init_script("window.__printCalls = 0; window.print = () => { window.__printCalls += 1; };")
    show(page, base_url, mocks.transaction("Succeeded", funding=[ea_ok()], settled=120.0), mocks.invoice(120.0))
    result.print_button.click()
    assert page.evaluate("window.__printCalls") == 1


def test_tc_135_completed_time_is_shown_in_singapore_time(page, base_url, result):
    """TC-135 Giờ hoàn tất hiển thị theo giờ Singapore: 04:30 UTC là 12:30."""
    show(page, base_url, mocks.transaction("Succeeded", funding=[ea_ok()], settled=120.0, completed_at="2026-10-21T04:30:00Z"), mocks.invoice(120.0))
    expect(result.status_heading).to_have_text(T.RESULT_SUCCEEDED)
    shown = result.fact("Completed at") or ""
    assert re.search(r"\b12:30\b", shown), f"Giờ hiển thị: {shown!r}"
    assert not re.search(r"\b04:30\b", shown), f"Còn hiện giờ UTC: {shown!r}"


# ------------------------------------------------------------------ thất bại
def test_tc_136_failure_screen_shows_message_and_actions_without_receipt(page, base_url, result):
    """TC-136 Màn thất bại hiện thông báo, nguồn tiền thất bại và nút về trang chủ, không có Print receipt."""
    show(page, base_url, mocks.transaction("Failed", funding=[mocks.funding("OnlineGateway", "Failed", 120.0, None, reason="provider declined")],
                                           settled=None))
    expect(result.status_heading).to_have_text(T.RESULT_FAILED)
    expect(page.get_by_text("Your payment could not be completed", exact=False)).to_be_visible()
    assert [k for k, _ in result.funding_rows()] == ["Online Gateway — Failed"]
    expect(result.home_link).to_be_visible()
    assert result.print_button.count() == 0


@pytest.mark.known_defect(reason="Màn thất bại không hiển thị lý do (failureReason) cho phụ huynh (R9 TC-136 yêu cầu có lý do). Suy ra từ mã nguồn PaymentResultPage")
def test_tc_136_failure_screen_shows_the_reason(page, base_url, result):
    """TC-136 (phần lý do) Lý do thất bại được báo cho phụ huynh bằng ngôn ngữ dễ hiểu."""
    show(page, base_url, mocks.transaction("Failed", funding=[mocks.funding("OnlineGateway", "Failed", 120.0, None, reason="Card declined by issuer")]))
    expect(result.status_heading).to_have_text(T.RESULT_FAILED)
    assert re.search(r"declined|reason|because|insufficient", result.text(), re.I), "Không có lý do thất bại trên màn hình"


@pytest.mark.extra
def test_extra_reconciliation_after_reversal_says_education_account_payment_was_reversed(page, base_url, result):
    """Bổ sung (nhánh ReconciliationRequired với leg EA Reversed trong mã nguồn) Màn hình nói rõ khoản Education Account đã được hoàn
    và không nói còn bị trừ. Khác với TC-137 bản rev FS09, nơi transaction là Failed."""
    funding = [mocks.funding("EducationAccount", "Reversed", 20.0, 20.0, seq=1), mocks.funding("OnlineGateway", "Failed", 30.0, None, seq=2)]
    show(page, base_url, mocks.transaction("ReconciliationRequired", funding=funding, requested=50.0, settled=None))
    expect(result.status_heading).to_have_text(T.RESULT_REVIEW)
    expect(page.get_by_text(T.EA_REVERSED, exact=False)).to_be_visible()
    assert T.EA_MAY_BE_DEDUCTED not in result.text()
    assert "Education Account — Refunded" in [k for k, _ in result.funding_rows()]


def test_tc_141_reconciliation_with_education_account_still_taken_warns_and_offers_no_retry(page, base_url, result, requests_log):
    """TC-141 Phần EA chưa được hoàn: báo 'có thể vẫn bị trừ' và không có nút thử lại, không gửi yêu cầu tạo thanh toán mới.
    Hậu điều kiện rev FS09: transaction ReconciliationRequired, leg EA giữ nguyên Succeeded (không bị hoàn), không có transaction mới."""
    funding = [mocks.funding("EducationAccount", "Succeeded", 20.0, 20.0, seq=1), mocks.funding("OnlineGateway", "Failed", 30.0, None, seq=2)]
    show(page, base_url, mocks.transaction("ReconciliationRequired", funding=funding, requested=50.0, settled=None))
    expect(result.status_heading).to_have_text(T.RESULT_REVIEW)
    expect(page.get_by_text(T.EA_MAY_BE_DEDUCTED, exact=False)).to_be_visible()
    assert page.get_by_role("button", name=re.compile("try again|retry|pay again", re.I)).count() == 0
    assert [k for k, _ in result.funding_rows()] == ["Education Account — Succeeded", "Online Gateway — Failed"], result.funding_rows()
    assert not requests_log.posts("/checkout"), "Màn đối soát đã gửi yêu cầu tạo thanh toán mới"


def test_tc_128_verifying_state_does_not_say_the_payment_failed_and_offers_no_retry(page, base_url, result):
    """TC-128 (rev FS09) Trạng thái đang đối soát: tiêu đề cần kiểm tra, không nói thất bại, không có Try again.
    Mock theo tiền điều kiện của R9: transaction và leg EA ReconciliationRequired, leg online Failed."""
    funding = [mocks.funding("EducationAccount", "ReconciliationRequired", 20.0, 20.0, seq=1),
               mocks.funding("OnlineGateway", "Failed", 30.0, None, seq=2)]
    show(page, base_url, mocks.transaction("ReconciliationRequired", funding=funding, requested=50.0, settled=None))
    expect(result.status_heading).to_have_text(T.RESULT_REVIEW)
    status_text = result.status_text()
    assert not re.search(r"failed|could not be completed", status_text, re.I), f"Phần trạng thái nói thất bại: {status_text}"
    assert page.get_by_role("button", name=re.compile("try again|retry|pay again", re.I)).count() == 0
    assert result.print_button.count() == 0
    assert [k for k, _ in result.funding_rows()][0].startswith("Education Account — "), result.funding_rows()


@pytest.mark.known_defect(reason="Leg EA ở ReconciliationRequired (R9 rev TC-128) không được nói là đã bị trừ: UI chỉ hiện câu 'may still have been deducted' khi leg EA là Succeeded. Suy ra từ mã nguồn PaymentResultPage")
def test_tc_128_verifying_state_names_the_education_account_part_that_was_taken(page, base_url, result):
    """TC-128 bước 2 (rev FS09) Trạng thái đang đối soát nêu rõ phần EA đã bị trừ."""
    funding = [mocks.funding("EducationAccount", "ReconciliationRequired", 20.0, 20.0, seq=1),
               mocks.funding("OnlineGateway", "Failed", 30.0, None, seq=2)]
    show(page, base_url, mocks.transaction("ReconciliationRequired", funding=funding, requested=50.0, settled=None))
    expect(result.status_heading).to_have_text(T.RESULT_REVIEW)
    assert re.search(r"education account.{0,80}(deducted|taken)", result.status_text(), re.I), result.status_text()


@pytest.mark.known_defect(reason="Transaction Failed có leg EA Reversed (R9 rev TC-137, TC-103) chỉ hiện dòng 'Education Account — Refunded', không có câu nói phần EA đã trả lại: UI chỉ hiện câu đó khi transaction ở ReconciliationRequired. Suy ra từ mã nguồn PaymentResultPage")
def test_tc_137_failed_split_with_returned_education_account_part_says_the_amount_was_returned(page, base_url, result):
    """TC-137 (rev FS09) Thanh toán chia khoản thất bại và phần EA đã hoàn: màn hình báo thất bại và nói số tiền lấy từ EA đã được trả lại."""
    funding = [mocks.funding("EducationAccount", "Reversed", 20.0, 20.0, seq=1), mocks.funding("OnlineGateway", "Failed", 30.0, None, seq=2)]
    show(page, base_url, mocks.transaction("Failed", funding=funding, requested=50.0, settled=None))
    expect(result.status_heading).to_have_text(T.RESULT_FAILED)
    assert [k for k, _ in result.funding_rows()] == ["Education Account — Refunded", "Online Gateway — Failed"], result.funding_rows()
    assert re.search(r"returned|reversed", result.status_text(), re.I), f"Không có câu nói EA đã trả lại: {result.status_text()}"


@pytest.mark.known_defect(reason="Lỗi 5xx của API trạng thái giao dịch được hiển thị nguyên văn từ danh sách errors (packages/api-client/src/api-error.ts), có thể lộ chi tiết kỹ thuật (R9 TC-138). Suy ra từ mã nguồn, chưa thấy trên bản build")
def test_tc_138_server_error_on_result_hides_technical_details(page, base_url, result):
    """TC-138 Lỗi máy chủ khi đọc kết quả không lộ chi tiết kỹ thuật."""
    page.add_init_script(f"sessionStorage.setItem('edusave.billingPayment.transactionId', '{mocks.GUID_TX}');")
    mocks.mock_json(page, mocks.TRANSACTION_RE, None, status=500, message="Internal Server Error",
                    errors=["System.Data.SqlClient.SqlException: Timeout expired at BillingPaymentService.Repository.GetAsync"])
    page.goto(f"{base_url}/payment-result")
    expect(page.get_by_role("alert")).to_be_visible(timeout=30_000)
    assert not TECHNICAL.search(result.text()), f"Lộ chi tiết kỹ thuật: {result.text()[:300]}"


@pytest.mark.known_defect(reason="Không có nút Try again trên màn thất bại để tạo giao dịch mới (R9 TC-140; F9_Dev_Local_Run_Results.md: không thử lại được)")
def test_tc_140_failure_screen_offers_try_again(page, base_url, result):
    """TC-140 Màn thất bại có nút Try again để thử lại bằng giao dịch mới."""
    show(page, base_url, mocks.transaction("Failed", funding=[mocks.funding("OnlineGateway", "Failed", 120.0, None)]))
    expect(result.status_heading).to_have_text(T.RESULT_FAILED)
    assert page.get_by_role("button", name=re.compile("try again|retry|pay again", re.I)).count() >= 1


# ------------------------------------------------------------------ lỗi khi xác nhận và mã giao dịch
@pytest.mark.known_defect(reason="Lỗi 5xx khi xác nhận thanh toán hiện nguyên văn danh sách errors của máy chủ (api-error.ts), có thể lộ chi tiết kỹ thuật (R9 TC-144). Suy ra từ mã nguồn, chưa thấy trên bản build")
def test_tc_144_server_error_on_confirm_shows_safe_message_and_creates_nothing(page, billing, catalog, requests_log):
    """TC-144 Lỗi hệ thống khi xác nhận: thông báo an toàn, không chuyển trang, không đổi dữ liệu."""
    child = need(catalog.ea_child(), "con có ví đủ trả hết khoản phí")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    billing.start([charge.description], T.METHOD_EA)
    mocks.mock_json(page, mocks.CHECKOUT_RE, None, status=500, message="Internal Server Error", method="POST",
                    errors=["Microsoft.Data.SqlClient.SqlException: Deadlock victim at PaymentSaga.Execute"])
    billing.authorize()
    expect(billing.checkout_error_alert).to_be_visible(timeout=30_000)
    assert "/billing/" in page.url
    assert not TECHNICAL.search(billing.checkout_error_alert.inner_text()), billing.checkout_error_alert.inner_text()


def test_extra_result_without_transaction_reference_shows_missing_notice(page, base_url, result):
    """Bổ sung: mở /payment-result khi không có mã giao dịch thì báo thiếu mã, có đường về trang chủ."""
    page.goto(f"{base_url}/payment-result")
    expect(result.missing_alert).to_be_visible()
    expect(result.home_link).to_be_visible()


def test_extra_result_with_malformed_transaction_reference_shows_missing_notice_and_clears_it(page, base_url, result):
    """Bổ sung: mã giao dịch sai định dạng trong sessionStorage bị coi như thiếu và bị xóa."""
    page.add_init_script("sessionStorage.setItem('edusave.billingPayment.transactionId', 'not-a-guid');")
    page.goto(f"{base_url}/payment-result")
    expect(result.missing_alert).to_be_visible()
    wait_until(page, lambda: page.evaluate("sessionStorage.getItem('edusave.billingPayment.transactionId')") is None,
               what="xóa mã giao dịch sai")


@pytest.mark.known_defect(reason="API chặn thanh toán lần 2 trên khoản đang PaymentPending với mã 409, nhưng UI SCR-02 ẩn luôn khoản đó thay vì hiển thị trạng thái Pending và khóa tích chọn (R9 TC-127)")
def test_tc_127_coming_back_to_pending_invoice_cannot_start_second_payment(billing, api, base_url):
    """TC-127 Quay lại màn SCR-02 khi khoản đang chờ kết quả cổng: API chặn tạo giao dịch thứ hai (409) và UI hiện dòng Pending bị khóa."""
    with db.temp_charges(amounts=[55.00]) as (stu_id, cids):
        r1 = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc127-1-{cids[0]}",
        )
        assert r1.status == 200
        r2 = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc127-2-{cids[0]}",
        )
        assert r2.status == 409
        billing.open(stu_id)
        assert "55.00" in billing.main_text() and "pending" in billing.main_text().lower()


@pytest.mark.extra
@pytest.mark.known_defect(reason="Mã tham chiếu giao dịch dùng TRX-<UUIDv7> thay vì TRX-YYYY-NNNNNN và màn kết quả chưa có nút tải lại biên lai PDF")
def test_extra_transaction_reference_follows_trx_yyyy_nnnnnn_and_receipt_downloadable(page, base_url, result):
    """TC-134 Mã tham chiếu giao dịch có định dạng TRX-YYYY-NNNNNN và biên lai có thể tải lại dưới dạng PDF."""
    show(page, base_url, mocks.transaction("Succeeded", funding=[ea_ok()], settled=120.0), mocks.invoice(120.0))
    expect(result.status_heading).to_have_text(T.RESULT_SUCCEEDED)
    ref_text = result.text()
    assert re.search(r"\bTRX-\d{4}-\d{6}\b", ref_text), f"Không thấy mã TRX-YYYY-NNNNNN trên biên lai: {ref_text[:300]}"


def test_tc_143_session_ending_after_confirm_does_not_stop_payment_from_finishing(api, base_url):
    """TC-143 Phiên đăng nhập của phụ huynh kết thúc sau khi đã chuyển sang cổng thanh toán không ngăn webhook hoàn tất giao dịch."""
    with db.temp_charges(amounts=[60.00]) as (stu_id, cids):
        r1 = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc143-{cids[0]}",
        )
        assert r1.status == 200
        tx_id = r1.json()["data"]["transactionId"]
        fnd_ref = db.get_tx_bundle(tx_id)["legs"][0]["funding_reference"]
        # Gửi webhook trực tiếp không kèm bất kỳ cookie/token phiên phụ huynh nào
        status, body, ev_id = db.post_webhook(fnd_ref, amount_cents=6000, provider_tx_id="PTX-QA-143")
        assert db.get_webhook_receipt(ev_id), "Webhook phải được nhận dù không có phiên phụ huynh"
        assert status == 200, body
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["tx"]["status"] == "2" and bundle["invoice"]["status"] == "4"
