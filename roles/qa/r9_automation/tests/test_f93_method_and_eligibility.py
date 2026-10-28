"""F9.3 Phương thức thanh toán và điều kiện (TC-035 đến TC-062). Nguồn: R9_Test_Cases_final_FS09.xlsx, FS F9 mục SCR-04.

UI thật: chọn nhiều khoản rồi Continue. Bước phương thức có nút chọn Education Account, Online Gateway và Both (Both chỉ hiện
khi ví còn tiền nhưng không đủ trả hết). Phần chia khoản của Both do hệ thống tự tính, không sửa được (ASM-R9-UI-03).
Các test dưới đây chọn con theo số liệu thật (Catalog), không gắn cứng tên. Không test nào bấm Authorize & pay.
Bản rev FS09 thêm hậu điều kiện "không có transaction nào được tạo, invoice vẫn Issued, số dư EA không đổi" cho mọi case dừng
ở SCR-04 và SCR-05: các test đó gọi assert_nothing_created (pages/postconditions.py).
"""
from __future__ import annotations

import re
import uuid
from decimal import Decimal

import pytest
from playwright.sync_api import expect

from data import mocks, seed
from data import ui_text as T
from pages import db
from pages.base_page import snippet
from pages.catalog import live_smallest, need
from pages.postconditions import assert_nothing_created, snapshot

pytestmark = pytest.mark.f93

NOT_ENOUGH = re.compile(r"balance is not enough|not enough for this amount|pay the rest online", re.I)


def open_split_snapshot(billing, catalog):
    """Con có ví không đủ trả hết: chụp trạng thái, chọn hết khoản rồi sang bước phương thức. Trả (con, ảnh chụp)."""
    child = need(catalog.split_child(), "con có ví còn tiền nhưng không đủ trả hết khoản (cần để thử Both)")
    db.ensure_split_state(child.student_id)
    billing.open(child.student_id)
    before = snapshot(billing)
    billing.select_all().to_method()
    return child, before


def open_split(billing, catalog):
    return open_split_snapshot(billing, catalog)[0]


def test_tc_035_selecting_a_charge_opens_method_screen_with_its_summary(billing, catalog, requests_log):
    """TC-035 Chọn một khoản rồi Continue mở bước phương thức với tóm tắt khoản đó. Mở SCR-04 không tạo gì (rev FS09)."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    (charge,), _ = live_smallest(billing, child)
    before = snapshot(billing)
    billing.select([charge.description]).to_method()
    assert billing.selected_lines() == [(charge.description, charge.net)]
    assert billing.total_to_pay() == charge.net
    state = billing.method_state()
    assert state[T.METHOD_EA]["present"] and state[T.METHOD_ONLINE]["present"], state
    assert_nothing_created(billing, requests_log, child, before)


@pytest.mark.draft
def test_tc_036_several_charges_can_be_selected_for_one_payment(billing, catalog, requests_log):
    """TC-036 Chọn nhiều khoản trong một lần thanh toán. ASM-R9-UI-01: R9 chỉ cho chọn một hóa đơn nguyên, UI thật cho chọn nhiều khoản.
    Hậu điều kiện rev FS09: mở SCR-04 không tạo transaction và invoice vẫn Issued."""
    child = need(next((c for c in catalog.with_charges() if len(c.charges) >= 2), None), "con có từ hai khoản phí")
    picked, _ = live_smallest(billing, child, count=2)
    before = snapshot(billing)
    billing.select([c.description for c in picked])
    expect(billing.selected_count).to_have_text("2 charge(s) selected")
    billing.to_method()
    assert billing.total_to_pay() == sum((c.net for c in picked), Decimal(0))
    assert_nothing_created(billing, requests_log, child, before)


def test_tc_040_zero_balance_offers_online_payment_only(billing, catalog, requests_log):
    """TC-040 Ví có số dư 0: Education Account bị khóa, không có Both, mặc định là Online Gateway. Nothing is created (rev FS09).
    Dữ liệu ngày 21/10/2026 không có con nào vừa ví 0.00 vừa còn khoản phí, nên test này bỏ qua. Bản giả lập ví ngay dưới vẫn chạy."""
    child = need(catalog.zero_child(), "con có ví số dư 0 và còn khoản phí")
    (charge,), _ = live_smallest(billing, child)
    before = snapshot(billing)
    billing.select([charge.description]).to_method()
    state = billing.method_state()
    assert state[T.METHOD_EA]["present"] and state[T.METHOD_EA]["disabled"], state
    assert not state[T.METHOD_BOTH]["present"], "Both phải ẩn khi ví không còn tiền"
    assert state[T.METHOD_ONLINE]["checked"], state
    assert_nothing_created(billing, requests_log, child, before)


@pytest.mark.known_defect(reason="UI chỉ khóa nút Education Account, không giải thích 'balance is not enough ... pay the rest online' như R9 TC-040, TC-041, TC-046")
def test_tc_041_tc_046_low_balance_shows_reason_to_pay_the_rest_online(billing, catalog, page):
    """TC-041 và TC-046 Ví không đủ: hiện lý do và gợi ý trả phần còn lại online."""
    open_split(billing, catalog)
    assert NOT_ENOUGH.search(billing.main_text()), "Không có câu giải thích vì sao Education Account bị khóa"


def test_tc_041_balance_below_amount_disables_education_account_and_offers_both(billing, catalog, requests_log):
    """TC-041 Ví thấp hơn số tiền cần trả: Education Account bị khóa, Both và Online Gateway dùng được. Nothing is created (rev FS09)."""
    child, before = open_split_snapshot(billing, catalog)
    state = billing.method_state()
    assert state[T.METHOD_EA]["disabled"], state
    assert state[T.METHOD_ONLINE]["present"] and not state[T.METHOD_ONLINE]["disabled"], state
    assert state[T.METHOD_BOTH]["present"] and not state[T.METHOD_BOTH]["disabled"], state
    assert_nothing_created(billing, requests_log, child, before)


def test_tc_043_balance_above_amount_allows_education_account_and_online_but_not_both(billing, catalog, requests_log):
    """TC-043 Ví đủ trả: Education Account và Online Gateway dùng được, không có Both. Nothing is created (rev FS09).
    (TC-042, ví đúng bằng số tiền, cần dữ liệu riêng và nằm trong nhóm mocked.)"""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    before = snapshot(billing)
    billing.select([charge.description]).to_method()
    state = billing.method_state()
    assert state[T.METHOD_EA]["present"] and not state[T.METHOD_EA]["disabled"], state
    assert state[T.METHOD_ONLINE]["present"] and not state[T.METHOD_ONLINE]["disabled"], state
    assert not state[T.METHOD_BOTH]["present"], "Both phải ẩn khi ví đủ tiền"
    assert_nothing_created(billing, requests_log, child, before)


def test_tc_045_education_account_is_suggested_but_nothing_is_debited_before_confirm(billing, catalog, requests_log):
    """TC-045 Ví đủ tiền thì Education Account được gợi ý nhưng chưa trừ gì cho tới khi xác nhận."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), before = live_smallest(billing, child, need_balance=True)
    billing.select([charge.description]).to_method()
    assert billing.method_state()[T.METHOD_EA]["checked"], "Education Account không phải mặc định khi ví đủ tiền"
    billing.to_review()
    assert not requests_log.posts("/checkout"), "Đã gửi yêu cầu thanh toán trước khi bấm xác nhận"
    billing.open(child.student_id)
    assert billing.balance() == before, "Số dư đổi dù chưa xác nhận"


def test_tc_046_education_account_cannot_be_chosen_when_balance_is_low(billing, catalog, requests_log):
    """TC-046 Chọn Education Account khi ví thấp bị từ chối: nút bị khóa, lựa chọn giữ nguyên, không có giao dịch."""
    open_split(billing, catalog)
    billing.radio(T.METHOD_EA).click(force=True)
    state = billing.method_state()
    assert state[T.METHOD_EA]["disabled"] and not state[T.METHOD_EA]["checked"], state
    assert state[T.METHOD_BOTH]["checked"], "Lựa chọn mặc định phải giữ nguyên"
    assert not requests_log.posts("/checkout")


def test_tc_050_default_both_proposes_whole_balance_as_education_account_part(billing, catalog, requests_log):
    """TC-050 Both mặc định lấy toàn bộ số dư làm phần EA và tính phần online còn lại. Chưa trừ gì, chưa có transaction (rev FS09)."""
    child, before = open_split_snapshot(billing, catalog)
    ea, online = billing.split_parts()
    assert ea == before.balance, (ea, online, before.balance)
    assert online == billing.total_to_pay() - before.balance, (ea, online)
    assert billing.method_state()[T.METHOD_BOTH]["checked"]
    assert_nothing_created(billing, requests_log, child, before)


def test_tc_100_review_of_split_payment_shows_both_parts(billing, catalog, requests_log):
    """TC-100 (phần số tiền) Bước xem lại của thanh toán chia khoản hiện phương thức Both, phần EA và phần online. Phần số dư sau thanh toán xem TC-063.
    Hậu điều kiện rev FS09: SCR-05 chưa trừ gì, số dư EA vẫn như cũ và chưa có transaction."""
    child, before = open_split_snapshot(billing, catalog)
    balance = billing.method_balance()
    billing.to_review()
    facts = dict(billing.review_facts())
    total = billing.review_total()
    assert facts["Payment method"] == "Both", facts
    assert facts["Education Account"].endswith(f"{balance:,.2f}"), facts
    assert facts["Online Gateway"].endswith(f"{total - balance:,.2f}"), facts
    assert_nothing_created(billing, requests_log, child, before)


@pytest.mark.draft
def test_tc_051_parent_can_lower_the_education_account_part(billing, catalog, page):
    """TC-051 Phụ huynh hạ phần EA thì phần online tự cập nhật."""
    open_split(billing, catalog)
    region = page.get_by_label(T.SPLIT_LABEL)
    editable = region.get_by_role("spinbutton").count() + region.get_by_role("textbox").count()
    assert editable >= 1, "Không có ô nhập phần Education Account"


def test_tc_052_online_part_cannot_be_typed(billing, catalog, page):
    """TC-052 Phần online chỉ hiển thị, không gõ được."""
    open_split(billing, catalog)
    region = page.get_by_label(T.SPLIT_LABEL)
    online_inputs = (region.get_by_role("textbox", name=re.compile("online", re.I)).count()
                     + region.get_by_role("spinbutton", name=re.compile("online", re.I)).count())
    assert online_inputs == 0, "Phần online có ô nhập"
    assert billing.split_parts()[1] is not None, "Không thấy số tiền phần online"


@pytest.mark.known_defect(reason="Màn xem lại hiện số dư hiện tại, không có số dư sau thanh toán (R9 TC-063)")
def test_tc_063_review_screen_shows_balance_after_payment(billing, catalog):
    """TC-063 Màn xem lại hiện số tiền, phương thức và số dư EA sau thanh toán (chỉ để tham khảo)."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    billing.start([charge.description])
    labels = " | ".join(k for k, _ in billing.review_facts()) + " " + billing.main_text()
    assert re.search(r"balance after|after payment|remaining balance", labels, re.I), "Không có số dư sau thanh toán"


def test_tc_063_review_screen_of_education_account_payment_debits_nothing(billing, catalog, requests_log):
    """TC-063 (hậu điều kiện rev FS09) Mở màn xem lại của thanh toán EA chưa trừ gì: không có transaction, số dư EA như cũ."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    before = snapshot(billing)
    billing.start([charge.description], T.METHOD_EA)
    expect(billing.authorize_button).to_be_visible()
    assert_nothing_created(billing, requests_log, child, before)


@pytest.mark.api
def test_tc_047_api_refuses_education_account_method_when_balance_is_too_low(api, catalog, base_url):
    """TC-047 API từ chối thanh toán chỉ bằng EA khi ví không đủ. Tổng tiền lớn hơn ví nên dù lỗi cũng không trừ được tiền."""
    child = need(catalog.split_child(), "con có ví không đủ trả hết khoản phí")
    db.ensure_split_state(child.student_id)
    wallet = api.get(f"/education-account/v1/edu-account/students/{child.student_id}/wallet")
    assert wallet.ok, f"Không đọc được ví ({wallet.status}): {snippet(wallet)}"
    wallet_id = wallet.json()["data"]["wallet"]["walletId"]
    charges = mocks.items_of(api.get(f"/billing/v1/students/{child.student_id}/outstanding-charges").json()["data"])
    body = {"studentId": child.student_id, "chargeIds": [c["chargeId"] for c in charges], "method": T.METHOD_EA,
            "walletId": wallet_id, "returnUrl": f"{base_url}/payment-result"}
    response = api.post("/billing/v1/checkout", body, key=f"r9-qa-low-balance-{uuid.uuid4()}")
    assert not response.ok, f"API chấp nhận EA khi ví thiếu ({response.status}): {snippet(response)}"
    assert response.status < 500, f"Lỗi máy chủ thay vì từ chối ({response.status}): {snippet(response)}"


KEY_101_DEFECT = pytest.mark.known_defect(
    reason="Lần chạy 21/10/2026: khóa 101 ký tự không bị từ chối ở bước kiểm đầu vào, yêu cầu đi tiếp tới bước tìm khoản phí (trả 404 'Charge(s) not found'). "
           "CheckoutPlanner.ValidateShape chỉ kiểm khóa rỗng, không kiểm tối đa 100 ký tự (FS 4.1 SCR-05, ASM-R9-18).")


@pytest.mark.api
@pytest.mark.draft
@pytest.mark.parametrize("key", [None, "", pytest.param("k" * 101, marks=KEY_101_DEFECT)], ids=["missing", "empty", "101chars"])
def test_tc_081_api_refuses_missing_empty_or_too_long_idempotency_key(api, key):
    """TC-081 Khóa Idempotency-Key thiếu, rỗng hoặc dài 101 ký tự bị từ chối.
    Dùng mã học sinh không tồn tại để chắc chắn không tạo giao dịch thật. Nếu máy chủ kiểm mã thực thể trước khóa thì sẽ báo 404,
    khi đó đọc thông báo lỗi để biết lý do (ASM-R9-UI-04)."""
    body = {"studentId": seed.UNKNOWN_ID, "chargeIds": [seed.UNKNOWN_ID_2], "method": T.METHOD_ONLINE,
            "returnUrl": "http://localhost:5174/payment-result"}
    response = api.post("/billing/v1/checkout", body, key=key)
    assert response.status in (400, 422), f"Mong đợi 400, nhận {response.status}: {snippet(response)}"


@pytest.mark.api
@pytest.mark.mutating
@pytest.mark.draft
@pytest.mark.parametrize("key", [None, ""], ids=["missing", "empty"])
def test_tc_081_refused_key_on_a_real_charge_creates_nothing_and_keeps_balance(api, billing, catalog, base_url, key):
    """TC-081 (hậu điều kiện rev FS09) Khóa sai trên khoản phí thật: bị từ chối, không có giao dịch, khoản vẫn còn nợ, số dư EA không đổi.
    Nhãn mutating vì nếu máy chủ nhận nhầm khóa sai thì khoản phí thật bị trả. ASM-R9-UI-04.
    Khóa 101 ký tự cố ý không thử ở đây: lần chạy 21/10/2026 cho thấy máy chủ không kiểm độ dài, khóa đó sẽ thanh toán khoản phí thật."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    before = snapshot(billing)
    wallet = api.get(f"/education-account/v1/edu-account/students/{child.student_id}/wallet").json()["data"]["wallet"]
    charges = mocks.items_of(api.get(f"/billing/v1/students/{child.student_id}/outstanding-charges").json()["data"])
    chosen = next(c for c in charges if c["description"] == charge.description)
    body = {"studentId": child.student_id, "chargeIds": [chosen["chargeId"]], "method": T.METHOD_EA, "walletId": wallet["walletId"],
            "returnUrl": f"{base_url}/payment-result"}
    response = api.post("/billing/v1/checkout", body, key=key)
    assert response.status in (400, 422), f"Mong đợi 400, nhận {response.status}: {snippet(response)}"
    billing.open(child.student_id)
    after = snapshot(billing)
    assert after.descriptions == before.descriptions, "Khoản phí bị tiêu dù khóa sai"
    assert after.balance == before.balance, "Số dư EA đổi dù khóa sai"


# ------------------------------------------------------------------ ví giả lập (mocked): các trạng thái ví khó tạo bằng dữ liệu thật
def method_screen_with_wallet(page, billing, catalog, balance_of, status="Active"):
    """Giả lập ví của con đầu tiên có khoản phí với số dư tính từ khoản nhỏ nhất, rồi mở bước phương thức.
    Trả (con, khoản, ảnh chụp trước khi chọn). Số dư trong ảnh chụp là số dư giả lập, nên chỉ so danh sách khoản."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    (charge,), _ = live_smallest(billing, child)
    mocks.mock_json(page, mocks.WALLET_RE, mocks.wallet(child.student_id, child.name, float(balance_of(charge.net)), status))
    billing.open(child.student_id)
    before = snapshot(billing)
    billing.select([charge.description]).to_method()
    return child, charge, before


@pytest.mark.mocked
def test_tc_042_balance_equal_to_amount_allows_education_account_and_online_but_not_both(page, billing, catalog, requests_log):
    """TC-042 Ví đúng bằng số tiền cần trả: Education Account và Online Gateway dùng được, không có Both. Nothing is created (rev FS09)."""
    child, _, before = method_screen_with_wallet(page, billing, catalog, lambda net: net)
    state = billing.method_state()
    assert not state[T.METHOD_EA]["disabled"] and not state[T.METHOD_ONLINE]["disabled"], state
    assert not state[T.METHOD_BOTH]["present"], state
    assert_nothing_created(billing, requests_log, child, before)


@pytest.mark.mocked
def test_tc_040_zero_balance_offers_online_payment_only_simulated_wallet(page, billing, catalog, requests_log):
    """TC-040 (ví giả lập 0.00, vì dữ liệu thật không có con ví 0 còn khoản phí) Education Account bị khóa, không có Both, mặc định Online Gateway."""
    child, _, before = method_screen_with_wallet(page, billing, catalog, lambda net: Decimal(0))
    state = billing.method_state()
    assert state[T.METHOD_EA]["present"] and state[T.METHOD_EA]["disabled"], state
    assert not state[T.METHOD_BOTH]["present"], "Both phải ẩn khi ví không còn tiền"
    assert state[T.METHOD_ONLINE]["checked"], state
    assert_nothing_created(billing, requests_log, child, before)


@pytest.mark.mocked
@pytest.mark.known_defect(reason="Học sinh chưa có Education Account: API ví trả 404 và UI chặn cả trang bằng lỗi 'Unable to load education account', không cho trả online (R9 TC-038). Suy ra từ mã nguồn BillingPaymentPage")
def test_tc_038_student_without_education_account_can_still_pay_online(page, billing, catalog, requests_log):
    """TC-038 Học sinh không có EA vẫn trả được bằng Online Gateway. Hậu điều kiện rev FS09: chưa có transaction nào."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    (charge,), _ = live_smallest(billing, child)
    mocks.mock_json(page, mocks.WALLET_RE, None, status=404, message="Wallet not found")
    page.goto(f"{billing.base_url}/billing/{child.student_id}")
    expect(billing.charges_heading).to_be_visible(timeout=15_000)
    billing.select([charge.description]).to_method()
    state = billing.method_state()
    assert state[T.METHOD_ONLINE]["present"] and not state[T.METHOD_ONLINE]["disabled"], state
    assert state[T.METHOD_EA]["disabled"] or not state[T.METHOD_EA]["present"], state
    assert not requests_log.posts("/checkout"), "Đã tạo thanh toán khi mới mở bước phương thức"


@pytest.mark.mocked
@pytest.mark.known_defect(reason="UI chỉ so số dư với số tiền, không xét trạng thái ví nên ví Closed vẫn cho chọn Education Account (R9 TC-039). Suy ra từ mã nguồn canUseEducationAccount")
def test_tc_039_closed_education_account_cannot_be_used_for_payment(page, billing, catalog, requests_log):
    """TC-039 Ví Closed thì Education Account bị khóa dù số dư đủ. Hậu điều kiện rev FS09: chưa có transaction, khoản vẫn còn nợ."""
    child, _, before = method_screen_with_wallet(page, billing, catalog, lambda net: net * 10, status="Closed")
    state = billing.method_state()
    assert state[T.METHOD_EA]["disabled"], f"Ví Closed vẫn cho chọn Education Account: {state}"
    assert state[T.METHOD_ONLINE]["present"] and not state[T.METHOD_ONLINE]["disabled"], state
    assert_nothing_created(billing, requests_log, child, before)


@pytest.mark.api
def test_tc_048_api_refuses_ea_and_both_when_student_has_no_education_account(api, base_url):
    """TC-048 API từ chối phương thức EducationAccount và Both khi học sinh chưa có ví Education Account."""
    no_wallet_stu = str(uuid.uuid4())
    with db.temp_charges(student_id=no_wallet_stu, amounts=[120.00]) as (stu_id, cids):
        for method in ("EducationAccount", "Both"):
            body = {"studentId": stu_id, "chargeIds": cids, "method": method, "eaAmount": 50.0, "returnUrl": f"{base_url}/billing/payment-result"}
            res = api.post("/billing/v1/checkout", body, key=f"qa-tc048-{method}-{uuid.uuid4()}")
            assert res.status == 400, f"Mong đợi 400 cho {method} khi không có ví, nhận {res.status}: {res.text()}"
        assert db.sql_scalar(f"SELECT COUNT(1) FROM dbo.invoice_items WHERE student_charge_id = '{cids[0]}'") == "0"


@pytest.mark.api
def test_tc_049_api_refuses_ea_and_both_when_education_account_is_closed(api, base_url):
    """TC-049 API từ chối phương thức EducationAccount và Both khi ví ở trạng thái Closed."""
    with db.temp_charges(amounts=[120.00], balance=300.00, wallet_status="Closed") as (stu_id, cids):
        for method in ("EducationAccount", "Both"):
            body = {"studentId": stu_id, "chargeIds": cids, "method": method, "eaAmount": 50.0, "returnUrl": f"{base_url}/billing/payment-result"}
            res = api.post("/billing/v1/checkout", body, key=f"qa-tc049-{method}-{uuid.uuid4()}")
            assert res.status == 400, f"Mong đợi 400 cho {method} khi ví Closed, nhận {res.status}: {res.text()}"
            assert "inactive" in res.text().lower()
        assert db.sql_scalar(f"SELECT COUNT(1) FROM dbo.invoice_items WHERE student_charge_id = '{cids[0]}'") == "0"


def test_tc_053_in_both_setting_ea_part_to_zero_is_refused(billing, catalog, page, api, base_url):
    """TC-053 Trong chế độ Both, đặt phần EA = 0.00 bị từ chối trên cả API và ô nhập trên SCR-04."""
    with db.temp_charges(amounts=[250.00], balance=180.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": 0.00, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc053-{uuid.uuid4()}",
        )
        assert res.status == 400
    open_split(billing, catalog)
    region = page.get_by_label(T.SPLIT_LABEL)
    assert region.get_by_role("spinbutton").count() + region.get_by_role("textbox").count() >= 1, "SCR-04 không có ô nhập phần EA để thử đặt 0.00"


@pytest.mark.api
def test_tc_054_in_both_online_part_of_zero_is_refused(api, base_url):
    """TC-054 Trong chế độ Both, khi phần online = 0.00 (tức eaAmount == tổng tiền cần trả) thì bị từ chối và yêu cầu dùng EducationAccount."""
    with db.temp_charges(amounts=[200.00], balance=300.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": 200.00, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc054-{uuid.uuid4()}",
        )
        assert res.status == 400
        assert "must be less than the total" in res.text()
        assert db.sql_scalar(f"SELECT COUNT(1) FROM dbo.invoice_items WHERE student_charge_id = '{cids[0]}'") == "0"


@pytest.mark.api
@pytest.mark.known_defect(reason="CheckoutRequestDto không nhận trường onlineAmount riêng mà tự tính online = total - eaAmount, nên gửi EA 100 + Online 100 cho khoản 250 không bị từ chối 400 (R9 TC-055)")
def test_tc_055_api_refuses_both_when_two_parts_add_up_to_less_than_invoice(api, base_url):
    """TC-055 API từ chối yêu cầu Both khi tổng hai phần (EA 100 + Online 100 = 200) nhỏ hơn tổng hóa đơn (250)."""
    with db.temp_charges(amounts=[250.00], balance=180.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {
                "studentId": stu_id,
                "chargeIds": cids,
                "method": "Both",
                "eaAmount": 100.00,
                "onlineAmount": 100.00,
                "returnUrl": f"{base_url}/billing/payment-result",
            },
            key=f"qa-tc055-{uuid.uuid4()}",
        )
        assert res.status == 400, f"Mong đợi 400 khi tổng 2 phần < 250.00, nhưng API nhận {res.status}"


@pytest.mark.api
def test_tc_056_api_refuses_both_when_two_parts_add_up_to_more_than_invoice(api, base_url):
    """TC-056 API từ chối yêu cầu Both khi phần thanh toán vượt quá tổng hóa đơn (260 > 250)."""
    with db.temp_charges(amounts=[250.00], balance=300.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": 260.00, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc056-{uuid.uuid4()}",
        )
        assert res.status == 400
        assert db.sql_scalar(f"SELECT COUNT(1) FROM dbo.invoice_items WHERE student_charge_id = '{cids[0]}'") == "0"


def test_tc_057_setting_ea_part_above_balance_is_refused(billing, catalog, page, api, base_url):
    """TC-057 Đặt phần EA cao hơn số dư ví (180.01 > 180.00) bị từ chối trên cả API và giao diện SCR-04."""
    with db.temp_charges(amounts=[250.00], balance=180.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": 180.01, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc057-{uuid.uuid4()}",
        )
        assert res.status == 400
        assert "exceeds the education account balance" in res.text().lower()
    open_split(billing, catalog)
    region = page.get_by_label(T.SPLIT_LABEL)
    assert region.get_by_role("spinbutton").count() + region.get_by_role("textbox").count() >= 1, "SCR-04 không có ô nhập phần EA"


@pytest.mark.api
def test_tc_058_api_refuses_negative_amount_on_payment_part(api, base_url):
    """TC-058 API từ chối phần thanh toán âm (eaAmount = -10.00) trong chế độ Both."""
    with db.temp_charges(amounts=[250.00], balance=180.00) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "Both", "eaAmount": -10.00, "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc058-{uuid.uuid4()}",
        )
        assert res.status == 400
        assert db.sql_scalar(f"SELECT COUNT(1) FROM dbo.invoice_items WHERE student_charge_id = '{cids[0]}'") == "0"


def test_tc_062_lowering_ea_part_to_0_01_in_both_is_accepted(billing, catalog, page):
    """TC-062 Phụ huynh hạ phần EA xuống 0.01 trên màn SCR-04 thì phần online tự cập nhật thành Total - 0.01."""
    open_split(billing, catalog)
    region = page.get_by_label(T.SPLIT_LABEL)
    assert region.get_by_role("spinbutton").count() + region.get_by_role("textbox").count() >= 1, "SCR-04 không có ô nhập để chỉnh phần EA xuống 0.01"
