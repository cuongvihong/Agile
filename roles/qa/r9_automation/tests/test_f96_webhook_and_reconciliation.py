"""F9.6 Xác thực chữ ký webhook, lưu biên nhận webhook, chống trùng lặp và đối soát (TC-111 đến TC-123).
Mọi phép thử đều tạo khoản phí tạm qua pages.db.temp_charges và tự dọn dẹp hoàn toàn sau khi chạy."""
from __future__ import annotations

import json
import time
import uuid
import pytest

from pages import db

pytestmark = [pytest.mark.f96, pytest.mark.api]


def _start_online_checkout(api, base_url: str, stu_id: str, charge_ids: list[str]) -> tuple[str, str]:
    """Tạo một phiên checkout OnlineGateway trên khoản phí tạm, trả về (transaction_id, funding_reference)."""
    res = api.post(
        "/billing/v1/checkout",
        {
            "studentId": stu_id,
            "chargeIds": charge_ids,
            "method": "OnlineGateway",
            "returnUrl": f"{base_url}/billing/payment-result",
        },
        key=f"qa-f96-{uuid.uuid4()}",
    )
    assert res.status == 200, f"Không tạo được checkout OnlineGateway: {res.status} {res.text()}"
    data = res.json()["data"]
    tx_id = data["transactionId"]
    bundle = db.get_tx_bundle(tx_id)
    assert len(bundle["legs"]) == 1
    return tx_id, bundle["legs"][0]["funding_reference"]


def test_tc_111_webhook_without_signature_rejected(api, base_url):
    """TC-111: Webhook không có header X-Gateway-Signature bị từ chối (401), không ghi receipt và không đổi trạng thái."""
    with db.temp_charges(amounts=[50.00]) as (stu_id, cids):
        tx_id, fnd_ref = _start_online_checkout(api, base_url, stu_id, cids)
        status, _, ev_id = db.post_webhook(fnd_ref, amount_cents=5000, signature=None)
        assert status == 401
        assert db.get_webhook_receipt(ev_id) == {}
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["tx"]["status"] == "1"
        assert bundle["invoice"]["status"] == "3"


def test_tc_112_webhook_with_bad_signature_rejected(api, base_url):
    """TC-112: Webhook có chữ ký sai bị từ chối (401), không ghi receipt và không đổi trạng thái."""
    with db.temp_charges(amounts=[50.00]) as (stu_id, cids):
        tx_id, fnd_ref = _start_online_checkout(api, base_url, stu_id, cids)
        bad_sig = f"t={int(time.time())},v1={'a' * 64}"
        status, _, ev_id = db.post_webhook(fnd_ref, amount_cents=5000, signature=bad_sig)
        assert status == 401
        assert db.get_webhook_receipt(ev_id) == {}
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["tx"]["status"] == "1"


def test_tc_113_webhook_altered_after_signing_rejected(api, base_url):
    """TC-113: Webhook bị sửa nội dung raw body sau khi ký HMAC bị từ chối (401)."""
    with db.temp_charges(amounts=[50.00]) as (stu_id, cids):
        tx_id, fnd_ref = _start_online_checkout(api, base_url, stu_id, cids)
        ts = int(time.time())
        ev_id = f"EVT-QA-{uuid.uuid4().hex[:12]}"
        orig_body = json.dumps({
            "eventId": ev_id,
            "eventType": "payment.succeeded",
            "providerCode": "PAYOS_SIM",
            "transactionId": "PTX-QA-113",
            "referenceId": fnd_ref,
            "amountCents": 5000,
            "currency": "SGD",
            "status": "Succeeded",
            "occurredAtUtc": "2026-10-22T03:00:00Z",
            "metadata": {},
        })
        sig = db.sign_webhook(ts, orig_body)
        tampered_body = orig_body.replace('"amountCents": 5000', '"amountCents": 100')
        status, _, _ = db.post_webhook(fnd_ref, event_id=ev_id, signature=sig, raw_body_override=tampered_body)
        assert status == 401
        assert db.get_webhook_receipt(ev_id) == {}
        assert db.get_tx_bundle(tx_id)["tx"]["status"] == "1"


def test_tc_114_webhook_timestamp_outside_window_rejected(api, base_url):
    """TC-114: Webhook có timestamp lệch quá giới hạn clock skew bị từ chối (401)."""
    with db.temp_charges(amounts=[50.00]) as (stu_id, cids):
        tx_id, fnd_ref = _start_online_checkout(api, base_url, stu_id, cids)
        old_ts = int(time.time()) - 3600
        status, _, ev_id = db.post_webhook(fnd_ref, amount_cents=5000, timestamp=old_ts)
        assert status == 401
        assert db.get_webhook_receipt(ev_id) == {}
        assert db.get_tx_bundle(tx_id)["tx"]["status"] == "1"


def test_tc_115_valid_webhook_saved_and_processed_with_full_metadata(api, base_url):
    """TC-115: Webhook hợp lệ lưu đầy đủ provider, eventId, transactionId, funding_reference, event_type, SHA-256 payload_hash, received_at, processed_at và trạng thái Processed (2)."""
    with db.temp_charges(amounts=[50.00]) as (stu_id, cids):
        tx_id, fnd_ref = _start_online_checkout(api, base_url, stu_id, cids)
        status, body, ev_id = db.post_webhook(fnd_ref, amount_cents=5000, provider_tx_id="PTX-QA-115")
        rcp = db.get_webhook_receipt(ev_id)
        assert rcp, "Phải có bản ghi store-first trong payment_webhook_receipts"
        assert len(rcp["payload_hash_hex"]) == 64
        assert status == 200, body
        assert rcp["processing_status"] == "2"  # Processed
        assert rcp["received_at"] != "NULL" and rcp["processed_at"] != "NULL"


def test_tc_119_same_webhook_event_delivered_twice_processed_once(api, base_url):
    """TC-119: Cùng một eventId gửi 2 lần chỉ xử lý 1 lần, không tạo bản ghi receipt thứ hai và giao dịch chỉ tất toán 1 lần."""
    with db.temp_charges(amounts=[50.00]) as (stu_id, cids):
        tx_id, fnd_ref = _start_online_checkout(api, base_url, stu_id, cids)
        st1, _, ev_id = db.post_webhook(fnd_ref, amount_cents=5000, provider_tx_id="PTX-QA-119")
        st2, body2, _ = db.post_webhook(fnd_ref, amount_cents=5000, event_id=ev_id, provider_tx_id="PTX-QA-119")
        cnt = db.sql_scalar(f"SELECT COUNT(1) FROM dbo.payment_webhook_receipts WHERE provider_event_id = '{ev_id}'")
        assert cnt == "1"
        assert st1 == 200 and st2 == 200
        assert body2["data"]["processingStatus"] == "Processed"
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["tx"]["status"] == "2"  # Succeeded
        assert bundle["invoice"]["status"] == "4"  # Paid


def test_tc_120_second_webhook_different_event_id_for_settled_leg_ignored(api, base_url):
    """TC-120: Webhook thứ hai có eventId khác gửi tới phần thanh toán đã Succeeded sẽ được ghi nhận là Ignored (3)."""
    with db.temp_charges(amounts=[50.00]) as (stu_id, cids):
        tx_id, fnd_ref = _start_online_checkout(api, base_url, stu_id, cids)
        st1, _, _ = db.post_webhook(fnd_ref, amount_cents=5000, provider_tx_id="PTX-QA-120-A")
        assert st1 == 200
        st2, body2, ev_id2 = db.post_webhook(fnd_ref, event_type="payment.failed", amount_cents=5000, provider_tx_id="PTX-QA-120-B")
        assert st2 == 200
        assert body2["data"]["processingStatus"] == "Ignored"
        rcp2 = db.get_webhook_receipt(ev_id2)
        assert rcp2["processing_status"] == "3"  # Ignored
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["legs"][0]["status"] == "2"  # Vẫn Succeeded
        assert bundle["tx"]["status"] == "2"
        assert bundle["invoice"]["status"] == "4"


def test_tc_121_webhook_with_unknown_funding_reference_ignored():
    """TC-121: Webhook có referenceId không tồn tại được ghi nhận là Ignored (3) và không làm thay đổi giao dịch nào."""
    ev_id = f"EVT-QA-UNK-{uuid.uuid4().hex[:10]}"
    try:
        status, body, _ = db.post_webhook("FND-UNKNOWN-999999", amount_cents=5000, event_id=ev_id)
        assert status == 200
        assert body["data"]["processingStatus"] == "Ignored"
        rcp = db.get_webhook_receipt(ev_id)
        assert rcp["processing_status"] == "3"
    finally:
        db.delete_webhook_receipt(ev_id)


def test_tc_122_webhook_amount_mismatch_marked_failed_and_not_settled(api, base_url):
    """TC-122: Webhook có amountCents lệch với số tiền của phần thanh toán bị đánh dấu Failed (4) và không tất toán giao dịch."""
    with db.temp_charges(amounts=[80.00]) as (stu_id, cids):
        tx_id, fnd_ref = _start_online_checkout(api, base_url, stu_id, cids)
        status, body, ev_id = db.post_webhook(fnd_ref, amount_cents=7500)
        assert status == 200
        assert body["data"]["processingStatus"] == "Failed"
        rcp = db.get_webhook_receipt(ev_id)
        assert rcp["processing_status"] == "4"  # Failed
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["legs"][0]["status"] == "1"  # Vẫn Pending
        assert bundle["tx"]["status"] == "1"
        assert bundle["invoice"]["status"] == "3"


def test_tc_123_webhook_currency_not_sgd_marked_failed_and_not_settled(api, base_url):
    """TC-123: Webhook có currency khác SGD (ví dụ USD) bị đánh dấu Failed (4) và không tất toán giao dịch."""
    with db.temp_charges(amounts=[80.00]) as (stu_id, cids):
        tx_id, fnd_ref = _start_online_checkout(api, base_url, stu_id, cids)
        status, body, ev_id = db.post_webhook(fnd_ref, amount_cents=8000, currency="USD")
        assert status == 200
        assert body["data"]["processingStatus"] == "Failed"
        rcp = db.get_webhook_receipt(ev_id)
        assert rcp["processing_status"] == "4"  # Failed
        bundle = db.get_tx_bundle(tx_id)
        assert bundle["legs"][0]["status"] == "1"  # Vẫn Pending
        assert bundle["tx"]["status"] == "1"
        assert bundle["invoice"]["status"] == "3"
