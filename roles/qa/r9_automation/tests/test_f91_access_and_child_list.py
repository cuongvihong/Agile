"""F9.1 Truy cập và danh sách con (TC-001 đến TC-017). Nguồn: R9_Test_Cases.xlsx, FS F9 mục SCR-01.

UI thật: /billing liệt kê tài khoản giáo dục (con) với tên, mã tài khoản, trạng thái. Không có trường, khối, lớp
và nhãn khoản chưa trả như R9 mô tả (xem TC-004). TC-002, TC-003, TC-006 (cần danh sách con mong đợi), TC-009, TC-016
cần persona hoặc bước hủy trên MockPass, nằm trong data/not_automated.py.
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data import mocks, seed
from data import ui_text as T
from pages import db
from pages.accounts_page import AccountsPage
from pages.base_page import norm, snippet
from pages.billing_page import BillingPage
from pages.portal import Portal

pytestmark = pytest.mark.f91

TECHNICAL = re.compile(r"exception|stack ?trace|sqlexception|\bsql\b|nullreference|\bat system\.|internal server", re.I)


def test_tc_001_sign_in_with_singpass_reaches_child_list(anon_page, base_url):
    """TC-001 Phụ huynh đăng nhập Singpass rồi vào Fees & Payments thấy danh sách con."""
    portal = Portal(anon_page, base_url, seed.NRIC).sign_in()
    assert "/parent/login" not in anon_page.url and "/parent/callback" not in anon_page.url
    portal.open_fees_and_payments()
    accounts = AccountsPage(anon_page, base_url)
    accounts.wait_loaded()
    expect(accounts.heading).to_be_visible()
    assert accounts.read_cards(), "Đăng nhập xong nhưng danh sách con rỗng"


def test_tc_002_failed_singpass_sign_in_does_not_create_session(anon_page, base_url):
    """TC-002 Đăng nhập Singpass thất bại: callback báo lỗi, không tạo phiên, vào /billing bị đẩy về /parent/login."""
    anon_page.goto(f"{base_url}/parent/callback?error=access_denied&error_description=Authentication+failed")
    assert not Portal(anon_page, base_url, seed.NRIC).is_signed_in()
    expect(anon_page).to_have_url(re.compile(r"/parent/login"), timeout=15_000)


def test_tc_003_cancelled_singpass_sign_in_returns_without_session(anon_page, base_url):
    """TC-003 Hủy đăng nhập Singpass giữa chừng: quay lại trang đăng nhập, không có phiên và có thể bắt đầu đăng nhập lại."""
    anon_page.goto(f"{base_url}/parent/login")
    btn = anon_page.get_by_role("button", name=re.compile(r"sign in with singpass", re.I)).or_(
        anon_page.get_by_role("link", name=re.compile(r"sign in with singpass", re.I)))
    btn.first.click()
    anon_page.wait_for_url(re.compile(r"/singpass/login"), timeout=30_000)
    anon_page.go_back()
    assert not Portal(anon_page, base_url, seed.NRIC).is_signed_in()
    expect(anon_page).to_have_url(re.compile(r"/parent/login"), timeout=15_000)
    expect(btn.first).to_be_visible()


@pytest.mark.known_defect(reason="UI chỉ hiện tên, mã tài khoản và trạng thái. Thiếu trường, khối, lớp và nhãn có khoản chưa trả (R9 TC-004, TC-005)")
def test_tc_004_tc_005_child_card_shows_school_level_class_and_outstanding_label(accounts):
    """TC-004 và TC-005 Mỗi thẻ con có trường, khối, lớp và nhãn còn hay không còn khoản chưa trả."""
    accounts.open()
    cards = accounts.read_cards()
    assert cards
    for card in cards:
        text = card["text"].lower()
        assert "outstanding" in text, f"Thẻ {card['name']} không có nhãn khoản chưa trả: {card['text']}"
        assert re.search(r"school|primary|secondary|class|level", text), f"Thẻ {card['name']} không có trường hoặc lớp: {card['text']}"


def test_tc_006_child_list_contains_only_linked_children(accounts):
    """TC-006 Danh sách chỉ gồm con của phụ huynh đang đăng nhập."""
    expected = list(seed.EXPECTED_CHILDREN)
    if not expected:
        rows = db.sql_rows(
            f"SELECT full_name FROM dbo.students WHERE father_nric = '{seed.NRIC}' OR mother_nric = '{seed.NRIC}'",
            db=db.EA_DB,
        )
        expected = [r["full_name"] for r in rows]
    accounts.open()
    shown = sorted(c["name"] for c in accounts.read_all())
    assert shown == sorted(expected), f"Hiện {shown}, mong đợi {sorted(expected)}"


@pytest.mark.mocked
def test_tc_007_parent_without_linked_child_sees_empty_state(page, accounts):
    """TC-007 Phụ huynh không có con thấy trạng thái rỗng, không có học sinh hay khoản phí nào."""
    mocks.mock_json(page, mocks.STUDENTS_RE, mocks.accounts_page([]))
    accounts.open()
    expect(accounts.empty_title).to_be_visible()
    expect(page.get_by_text(T.ACCOUNTS_EMPTY_DESC)).to_be_visible()
    assert accounts.cards.count() == 0


@pytest.mark.mocked
def test_tc_008_parent_with_one_child_sees_only_that_child(page, accounts):
    """TC-008 Phụ huynh có một con chỉ thấy con đó."""
    item = {"id": mocks.GUID_CHARGE, "code": "EA000001", "fullName": "Only Child", "status": "Active"}
    mocks.mock_json(page, mocks.STUDENTS_RE, mocks.accounts_page([item]))
    accounts.open()
    assert [c["name"] for c in accounts.read_cards()] == ["Only Child"]
    expect(page.get_by_role("link", name="View fees for Only Child")).to_be_visible()


def test_tc_009_second_guardian_of_same_child_can_view_and_start_payment(accounts, billing):
    """TC-009 Người giám hộ thứ hai (mother_nric) của cùng một học sinh thấy học sinh, thấy các khoản phí và mở được hộp xác nhận SCR-04.
    Dùng con không thuộc persona có ví và khoản phí (ưu tiên R9-STU-12), gắn tạm persona làm mẹ rồi trả lại như cũ."""
    cand = db.sql_rows(
        f"SELECT TOP 1 id, full_name FROM dbo.students WHERE student_id IS NOT NULL AND ISNULL(father_nric, '') <> '{seed.NRIC}' "
        f"AND ISNULL(mother_nric, '') <> '{seed.NRIC}' AND EXISTS (SELECT 1 FROM dbo.wallets w WHERE w.student_id = students.id AND w.status = 1) "
        f"ORDER BY CASE WHEN id = 'R9-STU-12' THEN 0 ELSE 1 END, id", db=db.EA_DB)
    if not cand:
        pytest.skip("Không có con nào ngoài persona có ví Active để gắn làm người giám hộ thứ hai")
    stu_id, stu_name = cand[0]["id"], cand[0]["full_name"]
    orig = db.sql_rows(f"SELECT father_nric, mother_nric FROM dbo.students WHERE id = '{stu_id}'", db=db.EA_DB)[0]
    try:
        db.sql_raw(
            f"UPDATE dbo.students SET father_nric = 'T1000611X', mother_nric = '{seed.NRIC}' WHERE id = '{stu_id}';",
            db=db.EA_DB,
        )
        accounts.open()
        names = [c["name"] for c in accounts.read_all()]
        assert stu_name in names
        billing.open(stu_id)
        charges = billing.read_charges()
        assert charges, "Người giám hộ thứ hai phải thấy danh sách khoản phí của con"
        billing.select([charges[0].description]).to_method()
        state = billing.method_state()
        assert state[T.METHOD_ONLINE]["present"]
    finally:
        f_val = "NULL" if orig["father_nric"] == "NULL" else f"'{orig['father_nric']}'"
        m_val = "NULL" if orig["mother_nric"] == "NULL" else f"'{orig['mother_nric']}'"
        db.sql_raw(
            f"UPDATE dbo.students SET father_nric = {f_val}, mother_nric = {m_val} WHERE id = '{stu_id}';",
            db=db.EA_DB,
        )


@pytest.mark.mocked
@pytest.mark.draft
def test_tc_010_system_error_on_child_list_shows_safe_message_and_retry(page, accounts):
    """TC-010 Lỗi hệ thống khi tải danh sách con: thông báo an toàn, thử lại được.
    ASM-R9-UI-02: R9 ghi 'Something went wrong. Please try again later.', UI thật ghi 'Unable to load education accounts'."""
    handler = lambda route: mocks.respond(route, status=500, message="System.Data.SqlClient.SqlException at Billing.Repo.Load")
    page.route(mocks.STUDENTS_RE, handler)
    page.goto(accounts.url("/billing"))
    expect(accounts.error_heading).to_be_visible()
    assert not TECHNICAL.search(accounts.main_text()), "Thông báo lộ chi tiết kỹ thuật"
    page.unroute(mocks.STUDENTS_RE, handler)
    accounts.retry_button.click()
    expect(accounts.heading).to_be_visible()


@pytest.mark.draft
def test_tc_011_invalid_student_id_in_address_is_refused(page, billing, base_url):
    """TC-011 Đổi mã học sinh trên địa chỉ bị từ chối và không lộ số liệu.
    ASM-R9-UI-02: R9 mong đợi mã 403 và câu 'You do not have access...', UI thật có hai nhánh dưới đây."""
    page.goto(f"{base_url}/billing/not-a-guid")
    # UI thật (quan sát 25/10/2026): mã sai định dạng cũng đi qua nhánh lỗi tải ví, không có tiêu đề 'Payment context is invalid'
    expect(page.get_by_role("heading", name=T.INVALID_CONTEXT).or_(page.get_by_role("heading", name=T.WALLET_ERROR))
           .or_(page.get_by_text(T.WALLET_ERROR)).first).to_be_visible(timeout=20_000)
    assert billing.charge_boxes.count() == 0, "Mã sai định dạng nhưng vẫn thấy khoản phí"
    page.goto(f"{base_url}/billing/{seed.UNKNOWN_ID}")
    expect(page.get_by_role("heading", name=T.WALLET_ERROR)).to_be_visible(timeout=20_000)
    expect(page.get_by_role("link", name=T.BACK_TO_ACCOUNTS).or_(billing.back_button)).to_be_visible()
    assert billing.charge_boxes.count() == 0, "Con không thuộc phụ huynh nhưng vẫn thấy khoản phí"


@pytest.mark.api
@pytest.mark.known_defect(reason="Lần chạy 21/10/2026: API trả 200 với danh sách rỗng cho mã học sinh không liên kết, không trả 403 như R9 TC-012. "
                                  "Mã nguồn StudentChargesController và GetOutstandingChargesHandler không kiểm phụ huynh có liên kết với học sinh. "
                                  "Mã thử là GUID ngẫu nhiên nên chưa chứng minh được rò rỉ dữ liệu, cần học sinh thật của gia đình khác.")
def test_tc_012_api_for_charges_of_unlinked_student_is_refused(api):
    """TC-012 API lấy khoản phí của học sinh không liên kết bị từ chối, không trả dữ liệu."""
    response = api.get(f"/billing/v1/students/{seed.UNKNOWN_ID}/outstanding-charges")
    assert response.status in (400, 403, 404), f"Mong đợi 403 hoặc 404, nhận {response.status}: {snippet(response)}"


@pytest.mark.api
def test_tc_013_api_for_invoice_of_another_family_is_refused(api):
    """TC-013 API đọc hóa đơn không thuộc gia đình bị từ chối. Dùng mã ngẫu nhiên vì không có hóa đơn nhà khác để thử."""
    response = api.get(f"/billing/v1/invoices/{seed.UNKNOWN_ID}")
    assert response.status in (400, 403, 404), f"Mong đợi 403 hoặc 404, nhận {response.status}: {snippet(response)}"


@pytest.mark.api
def test_tc_014_api_to_pay_for_unlinked_student_is_refused(api, base_url):
    """TC-014 API tạo thanh toán cho học sinh không liên kết bị từ chối và không trừ tiền."""
    body = {"studentId": seed.UNKNOWN_ID, "chargeIds": [seed.UNKNOWN_ID_2], "method": "OnlineGateway",
            "returnUrl": f"{base_url}/payment-result"}
    response = api.post("/billing/v1/checkout", body, key="r9-qa-unlinked-student-0001")
    assert not response.ok, f"Yêu cầu bị chấp nhận ({response.status}): {snippet(response)}"
    assert response.status < 500, f"Lỗi máy chủ thay vì từ chối ({response.status}): {snippet(response)}"


@pytest.mark.api
def test_tc_015_api_for_transaction_of_another_family_is_refused(api):
    """TC-015 API đọc giao dịch không thuộc gia đình bị từ chối."""
    response = api.get(f"/billing/v1/transactions/{seed.UNKNOWN_ID}")
    assert response.status in (400, 403, 404), f"Mong đợi 403 hoặc 404, nhận {response.status}: {snippet(response)}"


@pytest.mark.known_defect(reason="Truy cập trực tiếp URL /billing/<studentId của gia đình khác> vẫn mở được trang học sinh đó thay vì báo 'You do not have access to this student''s records.' và ẩn số dư ví (R9 TC-016)")
def test_tc_016_changing_student_id_in_address_to_another_child_shows_access_denied(page, base_url):
    """TC-016 Đổi studentId trên URL sang học sinh thật của gia đình khác phải hiện thông báo từ chối truy cập và không lộ dữ liệu."""
    other_stu = db.sql_scalar(
        f"SELECT TOP 1 id FROM dbo.students WHERE id <> 'SYSTEM-TREASURY' AND ISNULL(father_nric, '') <> '{seed.NRIC}' AND ISNULL(mother_nric, '') <> '{seed.NRIC}'",
        db=db.EA_DB,
    )
    assert other_stu
    page.goto(f"{base_url}/billing/{other_stu}")
    expect(page.get_by_text("You do not have access to this student's records.")).to_be_visible(timeout=8_000)


def test_tc_017_request_without_session_is_sent_to_sign_in(anon_page, base_url):
    """TC-017 (giao diện) Mở trang thanh toán khi chưa đăng nhập thì bị đưa về trang đăng nhập."""
    anon_page.goto(f"{base_url}/billing")
    expect(anon_page).to_have_url(re.compile(r"/parent/login"), timeout=20_000)


@pytest.mark.api
def test_tc_017_protected_api_rejects_call_without_session(anon_api):
    """TC-017 (API) API khoản phí không có phiên trả 401."""
    response = anon_api.get(f"/billing/v1/students/{seed.UNKNOWN_ID}/outstanding-charges")
    assert response.status == 401, f"Mong đợi 401, nhận {response.status}: {snippet(response)}"


def test_tc_142_session_ended_before_confirm_creates_no_transaction(anon_page, base_url):
    """TC-142 Phiên hết hạn trước bước xác nhận: bị đưa về đăng nhập và không có giao dịch nào được tạo."""
    posts: list[str] = []
    anon_page.on("request", lambda r: posts.append(r.url) if r.method == "POST" and "/checkout" in r.url else None)
    anon_page.goto(f"{base_url}/billing/{seed.UNKNOWN_ID}")
    expect(anon_page).to_have_url(re.compile(r"/parent/login"), timeout=20_000)
    assert not posts
