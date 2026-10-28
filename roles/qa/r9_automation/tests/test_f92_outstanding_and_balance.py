"""F9.2 Khoản phí còn nợ và số dư EA (TC-018 đến TC-034, TC-164). Nguồn: R9_Test_Cases_final_FS09.xlsx, FS F9 mục SCR-02, SCR-03.

UI thật liệt kê khoản phí (charge) với mô tả, gross, subsidy, amount due, due date. Chưa có hóa đơn trước khi thanh toán
(hóa đơn chỉ tạo khi bấm Authorize & pay), nên các case về số hóa đơn, nhóm theo loại phí và GST không có chỗ để kiểm.
ASM-R9-UI-01: R9 viết theo mô hình hóa đơn, bản build chọn theo khoản phí, chưa ai xác nhận cách ánh xạ.
"""
from __future__ import annotations

import re
from decimal import Decimal

import pytest
from playwright.sync_api import expect

from data import mocks
from data import ui_text as T
from pages import db
from pages.base_page import all_money, two_decimals
from pages.catalog import need

pytestmark = pytest.mark.f92

TECHNICAL = re.compile(r"exception|stack ?trace|sqlexception|\bsql\b|nullreference|\bat system\.|internal server", re.I)
DUE_STATUS = re.compile(r"overdue|due soon|upcoming", re.I)  # UI thật không có cột ngày hạn, chỉ có cột Status tính từ hạn nộp
DUE_DATE = re.compile(r"\d{4}-\d{2}-\d{2}|\d{1,2} \w{3,9} \d{4}|\d{2}/\d{2}/\d{4}")


@pytest.mark.known_defect(reason="SCR-02 liệt kê từng khoản phí phẳng, không có hóa đơn mở rộng theo nhóm Fee Type (Tuition/School/Miscellaneous) và không hiển thị dòng GST (R9 TC-019)")
def test_tc_019_invoice_lines_grouped_by_fee_type_and_show_gst(billing, catalog):
    """TC-019 Mở rộng hóa đơn trên SCR-02 hiện các dòng gom theo loại phí (Tuition, School, Miscellaneous) và dòng GST."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    billing.open(child.student_id)
    text = billing.main_text().lower()
    assert "gst" in text and "invoice" in text, "SCR-02 thiếu nhóm dòng hóa đơn và thông tin GST"


@pytest.mark.known_defect(reason="SCR-02 liệt kê từng khoản phí riêng lẻ trước khi thanh toán, chưa gom thành hóa đơn nhiều dòng kèm hạn nộp sớm nhất trên bảng SCR-02 (R9 TC-022)")
def test_tc_022_invoice_with_several_lines_shows_sum_and_earliest_due_date(billing, catalog):
    """TC-022 Hóa đơn nhiều dòng trên SCR-02 hiển thị mã hóa đơn INV-..., tổng tiền các dòng và hạn nộp sớm nhất."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    billing.open(child.student_id)
    assert re.search(r"\bINV[-0-9]+\b", billing.main_text()), "SCR-02 không hiển thị dòng tổng hợp theo mã hóa đơn INV"


def test_tc_024_paid_cancelled_and_draft_items_not_shown_in_open_list(billing, catalog):
    """TC-024 Khoản phí ở trạng thái DRAFT, VOID hoặc đã gắn vào hóa đơn Paid/Cancelled không xuất hiện trong danh sách còn nợ trên SCR-02."""
    stu_id = need(catalog.usable()[0] if catalog.usable() else None, "con nào đó").student_id
    with db.temp_charges(student_id=stu_id, amounts=[77.77], charge_status="DRAFT") as (_, draft_ids), \
         db.temp_charges(student_id=stu_id, amounts=[88.88], charge_status="VOID") as (_, void_ids):
        billing.open(stu_id)
        descriptions = [c.description for c in billing.read_charges()]
        assert not any("QA" in d and ("77.77" in d or "88.88" in d) for d in descriptions)
        main_txt = billing.main_text()
        assert "77.77" not in main_txt and "88.88" not in main_txt


@pytest.mark.known_defect(reason="Khoản phí đang trong hóa đơn PaymentPending bị ẩn khỏi danh sách SCR-02 thay vì hiển thị với nhãn trạng thái Pending và khóa chọn lại (R9 TC-025)")
def test_tc_025_payment_pending_item_shown_as_pending_and_disabled(billing, api, base_url):
    """TC-025 Khoản phí đang chờ kết quả cổng thanh toán (PaymentPending) vẫn hiện trên SCR-02 với nhãn Pending và không cho tích chọn."""
    with db.temp_charges(amounts=[65.00]) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc025-{cids[0]}",
        )
        assert res.status == 200
        billing.open(stu_id)
        assert "65.00" in billing.main_text() and "pending" in billing.main_text().lower()


@pytest.mark.known_defect(reason="SCR-02 không có nhãn báo dữ liệu mẫu / demo data (R9 TC-027)")
def test_tc_027_sample_data_notice_is_visible_on_fees_and_balance_screen(billing, catalog):
    """TC-027 Màn hình SCR-02 hiển thị nhãn thông báo dữ liệu mẫu (Sample / Demo data)."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    billing.open(child.student_id)
    assert re.search(r"\b(sample data|demo data|prototype|mock data)\b", billing.main_text(), re.I), "SCR-02 thiếu nhãn Sample/Demo data"


@pytest.mark.known_defect(reason="Học sinh chỉ có khoản đang PaymentPending bị ẩn khoản đó nên rơi vào màn hình rỗng SCR-03 thay vì hiện dòng Pending trên SCR-02 (R9 TC-034)")
def test_tc_034_child_with_only_payment_pending_invoice_does_not_see_empty_state(billing, catalog, api, base_url):
    """TC-034 Học sinh chỉ có 1 khoản đang ở trạng thái PaymentPending thì không hiện màn hình rỗng SCR-03 mà hiện dòng Pending bị khóa chọn."""
    empty_kid = need(catalog.empty_child(), "con không còn khoản phí nào")
    with db.temp_charges(student_id=empty_kid.student_id, amounts=[45.00]) as (stu_id, cids):
        res = api.post(
            "/billing/v1/checkout",
            {"studentId": stu_id, "chargeIds": cids, "method": "OnlineGateway", "returnUrl": f"{base_url}/billing/payment-result"},
            key=f"qa-tc034-{cids[0]}",
        )
        assert res.status == 200
        billing.open(stu_id)
        assert not billing.empty_state.is_visible(), "Học sinh có khoản PaymentPending nhưng lại hiện màn hình rỗng SCR-03"


@pytest.mark.draft
def test_tc_018_open_charges_are_listed_with_description_due_date_and_amounts(billing, catalog):
    """TC-018 Khoản phí còn nợ hiện đủ mô tả, hạn nộp và số tiền, tổng nợ bằng tổng các khoản. ASM-R9-UI-01."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    billing.open(child.student_id)
    assert billing.table_headers() in (T.TABLE_HEADERS, T.TABLE_HEADERS_V3)
    charges = billing.read_charges()
    assert charges, "Bảng không có dòng nào"
    for charge in charges:
        assert charge.description, "Dòng thiếu mô tả"
        assert DUE_DATE.search(charge.due) or DUE_STATUS.search(charge.due), f"Hạn nộp lạ: {charge.due!r} của {charge.description}"
        assert charge.net > 0
    assert billing.outstanding_total() == sum((c.net for c in charges), Decimal(0)), "Tổng nợ khác tổng các khoản"
    assert {c.description for c in charges} == {c.description for c in child.charges}, "Danh sách đổi giữa hai lần đọc"


@pytest.mark.draft
def test_tc_020_gross_subsidy_zero_and_net_equal_gross(billing, catalog):
    """TC-020 Subsidy 0.00 và Net bằng Gross cho mọi khoản (dữ liệu mẫu chưa có trợ cấp FAS). ASM-R9-UI-01."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    billing.open(child.student_id)
    for charge in billing.read_charges():
        assert charge.subsidy == 0, f"{charge.description}: subsidy {charge.subsidy}"
        assert charge.net == charge.gross, f"{charge.description}: net {charge.net}, gross {charge.gross}"


def test_tc_021_amounts_are_in_sgd_with_two_decimals(billing, catalog):
    """TC-021 Mọi số tiền có ký hiệu SGD và đúng hai chữ số thập phân."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    billing.open(child.student_id)
    tokens = all_money(billing.main_text())
    assert tokens, "Không tìm thấy số tiền nào trên trang"
    bad = [t for t in tokens if not two_decimals(t)]
    assert not bad, f"Số tiền sai định dạng: {bad}"


def test_tc_023_switching_to_another_child_changes_the_charge_list(billing, catalog, api):
    """TC-023 Chuyển sang con khác thì danh sách khoản phí đổi theo, không lẫn của con trước.
    Hai con có thể cùng tên khoản (ví dụ School Fee - Term 1), nên so từng danh sách trên màn với API của đúng con đó,
    không đòi hai danh sách rời nhau (lần chạy 21/10/2026 làm test cũ thất bại vì hai con có chung hai tên khoản)."""
    kids = catalog.with_charges()
    if len(kids) < 2:
        pytest.skip("Cần ít nhất hai con có khoản phí")
    first, second = kids[0], kids[1]
    seen = []
    for kid in (first, second):
        billing.open(kid.student_id)
        name = kid.name  # tên lấy từ danh sách con; thẻ 'Child' của trang khoản phí không phải lúc nào cũng có
        shown = sorted(c.description for c in billing.read_charges())
        expected = sorted(c["description"] for c in mocks.items_of(api.get(f"/billing/v1/students/{kid.student_id}/outstanding-charges").json()["data"]))
        assert shown == expected, f"Danh sách trên màn của {name} khác API của đúng con đó. Màn: {shown}. API: {expected}"
        seen.append((name, shown))
    assert seen[0][0] != seen[1][0], "Hai con hiện cùng một tên"
    assert seen[0][1] != seen[1][1], "Hai con có danh sách khoản phí y hệt nhau, test không phân biệt được việc danh sách có đổi theo con"


@pytest.mark.known_defect(reason="Lần chạy 25/10/2026: trang khoản phí không hiện tên con, mã học sinh và trạng thái ví. Khối này bị chú thích trong BillingPaymentPage.tsx (R9 TC-028, TC-030). Trước đó test báo đạt giả vì mặc định 'Active'")
def test_tc_028_active_account_shows_balance_and_status(billing, catalog):
    """TC-028 Tài khoản EA Active hiện số dư và trạng thái."""
    child = need(next((c for c in catalog.usable() if c.status.lower() == "active"), None), "con có tài khoản trạng thái Active")
    billing.open(child.student_id)
    assert billing.wallet_status().lower() == "active", "Trang khoản phí không hiện trạng thái ví"
    expect(billing.card(T.CARD_BALANCE)).to_contain_text(re.compile(r"\d+\.\d{2}"))


def test_tc_031_zero_balance_is_shown_as_0_00(billing, catalog):
    """TC-031 Số dư 0 hiện là 0.00. Con ví 0 không cần còn khoản phí."""
    child = need(catalog.zero_balance_child(), "con có ví số dư 0")
    billing.open(child.student_id)
    assert billing.balance() == 0
    expect(billing.card(T.CARD_BALANCE)).to_contain_text("0.00")


@pytest.mark.mocked
def test_tc_032_child_without_charges_shows_empty_state_and_no_payment_option(page, billing, catalog):
    """TC-032 Con không còn khoản nào: hiện thông báo rỗng, không có lựa chọn thanh toán. Giả lập danh sách khoản rỗng."""
    child = need(catalog.usable()[0] if catalog.usable() else None, "con nào")
    mocks.mock_json(page, mocks.CHARGES_RE, [])
    billing.open(child.student_id)
    expect(billing.empty_state).to_be_visible()
    expect(page.get_by_text(T.EMPTY_CHARGES_DESC)).to_be_visible()
    expect(billing.continue_button).to_be_disabled()
    assert billing.charge_boxes.count() == 0 and page.get_by_role("radio").count() == 0


def test_tc_032_real_child_without_charges_shows_empty_state_and_no_payment_option(billing, catalog):
    """TC-032 (dữ liệu thật) Con không còn khoản nào: hiện thông báo rỗng, nút Continue bị khóa, không có lựa chọn thanh toán.
    Cần một con thật không có khoản phí (bản chạy 21/10/2026 có Tan Wei Ming). Không có thì bỏ qua."""
    child = need(catalog.empty_child(), "con không còn khoản phí nào")
    billing.open(child.student_id)
    expect(billing.empty_state).to_be_visible()
    expect(billing.page.get_by_text(T.EMPTY_CHARGES_DESC)).to_be_visible()
    expect(billing.continue_button).to_be_disabled()
    assert billing.charge_boxes.count() == 0 and billing.page.get_by_role("radio").count() == 0
    assert billing.outstanding_total() == 0


@pytest.mark.known_defect(reason="Trạng thái rỗng thật (quan sát ngày 21/10/2026 trên con không có khoản phí) không có liên kết quay về danh sách con trong nội dung trang, chỉ có menu bên (R9 TC-032 bước 2, TC-033)")
def test_tc_032_tc_033_real_empty_state_links_back_to_child_list(billing, catalog):
    """TC-032 và TC-033 (dữ liệu thật) Trạng thái rỗng có liên kết về danh sách con để chọn con khác."""
    child = need(catalog.empty_child(), "con không còn khoản phí nào")
    billing.open(child.student_id)
    expect(billing.empty_state).to_be_visible()
    link = billing.content().get_by_role("link", name=re.compile(r"education accounts|child list|choose|back", re.I))
    assert link.count() >= 1, "Không có liên kết quay về danh sách con trong trang"


@pytest.mark.mocked
@pytest.mark.known_defect(reason="Trạng thái rỗng không có liên kết quay về danh sách con trong nội dung trang, chỉ có menu bên (R9 TC-032 bước 2, TC-033)")
def test_tc_032_tc_033_empty_state_links_back_to_child_list(page, billing, catalog):
    """TC-032 và TC-033 Trạng thái rỗng có liên kết về danh sách con để chọn con khác."""
    child = need(catalog.usable()[0] if catalog.usable() else None, "con nào")
    mocks.mock_json(page, mocks.CHARGES_RE, [])
    billing.open(child.student_id)
    expect(billing.empty_state).to_be_visible()
    link = billing.content().get_by_role("link", name=re.compile(r"education accounts|child list|choose|back", re.I))
    assert link.count() >= 1, "Không có liên kết quay về danh sách con trong trang"


@pytest.mark.mocked
@pytest.mark.known_defect(reason="Lần chạy 25/10/2026: API ví giả lập trạng thái Closed nhưng trang vẫn hiện Active (R9 TC-030). Cần Dev xác nhận UI có đọc trạng thái ví hay không")
def test_tc_030_closed_education_account_shows_status_closed(page, billing, catalog):
    """TC-030 Ví có trạng thái Closed hiện đúng trạng thái Closed."""
    child = need(catalog.usable()[0] if catalog.usable() else None, "con nào đó")
    mocks.mock_json(page, mocks.WALLET_RE, mocks.wallet(child.student_id, child.name, 0, "Closed"))
    billing.open(child.student_id)
    assert billing.wallet_status() == "Closed", billing.wallet_line()


@pytest.mark.mocked
@pytest.mark.known_defect(reason="Học sinh chưa có Education Account: API ví trả 404 và UI hiện lỗi tải, không có ghi chú 'chưa có tài khoản' và không có số dư (R9 TC-029). Suy ra từ mã nguồn")
def test_tc_029_child_without_education_account_shows_a_note_instead_of_balance(page, billing, catalog):
    """TC-029 Con không có EA: không hiện số dư, có ghi chú rõ ràng, trang không báo lỗi."""
    child = need(catalog.usable()[0] if catalog.usable() else None, "con nào đó")
    mocks.mock_json(page, mocks.WALLET_RE, None, status=404, message="Wallet not found")
    page.goto(f"{billing.base_url}/billing/{child.student_id}")
    expect(page.get_by_text(re.compile(r"no education account|does not have an education account", re.I)).first).to_be_visible(timeout=15_000)
    assert page.get_by_role("alert").filter(has_text=T.WALLET_ERROR).count() == 0, "Trang báo lỗi tải thay vì ghi chú"


@pytest.mark.mocked
@pytest.mark.draft
@pytest.mark.known_defect(reason="Lỗi 5xx của API khoản phí được hiển thị nguyên văn từ danh sách errors (getBillingPaymentErrorMessage, api-error.ts), có thể lộ chi tiết kỹ thuật (R9 TC-164). Suy ra từ mã nguồn, chưa thấy trên bản build")
def test_tc_164_system_error_on_charge_list_shows_safe_message_and_retry(page, billing, catalog, requests_log):
    """TC-164 (rev FS09) Lỗi hệ thống khi tải danh sách khoản (SCR-02): thông báo an toàn, thử lại được, không đổi dữ liệu.
    ASM-R9-UI-02: R9 ghi 'Something went wrong. Please try again later.', UI thật ghi tiêu đề 'Unable to load billing information'."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    handler = lambda route: mocks.respond(route, status=500, message="Internal Server Error",
                                          errors=["System.Data.SqlClient.SqlException: Timeout expired at Billing.Repo.ListOutstanding"])
    page.route(mocks.CHARGES_RE, handler)
    page.goto(f"{billing.base_url}/billing/{child.student_id}")
    expect(billing.table_error).to_be_visible(timeout=20_000)
    assert billing.charge_boxes.count() == 0, "Danh sách khoản vẫn hiện khi API lỗi"
    assert not TECHNICAL.search(billing.main_text()), f"Thông báo lộ chi tiết kỹ thuật: {billing.main_text()[:300]}"
    page.unroute(mocks.CHARGES_RE, handler)
    page.get_by_role("button", name=T.RETRY).click()
    expect(billing.charge_boxes.first).to_be_visible(timeout=20_000)
    assert {c.description for c in billing.read_charges()} == {c.description for c in child.charges}, "Sau khi thử lại danh sách khác ban đầu"
    assert not requests_log.posts("/checkout"), "Lỗi tải danh sách đã tạo giao dịch"
