"""Quy tắc kiểm tra dữ liệu bổ sung vào FS 09 (TC-173 đến TC-206). Nguồn: R9_Test_Cases_final_FS09.xlsx và R9_FAS_Validation_Rules.docx.

Chạy riêng bằng: run_r9_automation.cmd rules. Mỗi test mang thêm nhãn của nhóm F9.x mà case thuộc về (f91 đến f98),
nên run_r9_automation.cmd suite 3 cũng chạy các test F9.3 ở file này.

CHỈ CHẠY TRÊN LOCALHOST (xem data/seed.py: assert_local). Không test nào mở một địa chỉ ngoài máy đang host hệ thống.

Cách chọn dữ liệu. Sổ case viết theo bộ seed R9 (S01, S02, S10, S25...), còn UI thật liệt kê khoản phí (charge) của các con
mà persona S7890123F có. Vì vậy test không gắn cứng mã seed: nó chọn con và khoản phí phù hợp qua Catalog như các file F9.1 đến F9.8
và tự bỏ qua kèm lý do khi dữ liệu không có đối tượng đó. Con số cụ thể của sổ (27.25, 1,590.00...) chỉ kiểm khi chạy trên bộ seed R9;
ở đây test kiểm quy tắc đứng sau con số. Test dựng khoản phí tạm bằng db.temp_charges tự dọn dẹp và cần Docker (SQL Server của QA);
không có Docker thì tự bỏ qua.

Case chưa tự động hóa: TC-175 (UI không có ngày sinh, không có quy tắc tuổi từ 16) và TC-204 (cần cách làm hỏng xử lý callback do Dev
cung cấp, ENV-R9-05). Phần không tự động hóa của từng test được ghi trong docstring.
"""
from __future__ import annotations

import re
import uuid
from decimal import Decimal
from urllib.parse import quote

import pytest
from playwright.sync_api import expect

from data import mocks, seed
from data import ui_text as T
from pages import db
from pages.base_page import all_money, snippet, two_decimals
from pages.catalog import live_smallest, need
from pages.postconditions import assert_nothing_created, snapshot

pytestmark = pytest.mark.rules

F91, F92, F93, F94, F95 = (pytest.mark.f91, pytest.mark.f92, pytest.mark.f93, pytest.mark.f94, pytest.mark.f95)
F96, F97, F98 = pytest.mark.f96, pytest.mark.f97, pytest.mark.f98

TECHNICAL = re.compile(r"exception|stack ?trace|sqlexception|\bsql\b|nullreference|\bat system\.|internal server|syntax error", re.I)
REFUSED = (400, 403, 404, 409, 422)
GUID = "f063b14b-8ec5-507d-84ad-9a9d36a79c26"


# ------------------------------------------------------------------ dùng chung
def require_db() -> None:
    """Test dùng SQL cần container edufams-qa-sqlserver. Không có Docker hoặc container thì bỏ qua."""
    try:
        code, out = db.sql_raw("SELECT 1 AS ok")
    except Exception as err:  # noqa: BLE001  docker không cài
        pytest.skip(f"Không chạy được SQL Server của QA ({err})")
    if code != 0:
        pytest.skip(f"Không chạy được SQL Server của QA: {out[:160]}")


def pick_child(catalog):
    """Con có ví, dùng làm chủ của khoản phí tạm. Ưu tiên con có ví đủ trả, nếu không thì con đầu tiên."""
    return need(catalog.ea_child() or (catalog.usable()[0] if catalog.usable() else None), "con nào có ví Education Account")


def wallet_balance(student_id: str) -> Decimal:
    return Decimal(db.sql_scalar(f"SELECT balance FROM dbo.wallets WHERE student_id = '{student_id}'", db=db.EA_DB))


def charge_used(charge_id: str) -> int:
    return int(db.sql_scalar(f"SELECT COUNT(1) FROM dbo.invoice_items WHERE student_charge_id = '{charge_id}'") or "0")


def checkout_body(student_id: str, charge_ids: list[str], method, base_url: str) -> dict:
    return {"studentId": student_id, "chargeIds": charge_ids, "method": method, "returnUrl": f"{base_url}/payment-result"}


def loading_indicator(page):
    """Dấu hiệu đang tải: progressbar, status, aria-busy hoặc chữ Loading. Hình dạng cụ thể chưa được Dev ghi lại (draft)."""
    return page.locator('[role="progressbar"], [role="status"], [aria-busy="true"], [data-loading="true"]').or_(
        page.get_by_text(re.compile(r"^\s*loading", re.I)))


def hold_requests(page, pattern):
    """Giữ mọi request khớp pattern lại (thay cho độ trễ 3 giây trong sổ case). Trả danh sách route đang giữ."""
    held: list = []
    page.route(pattern, lambda route: held.append(route))
    return held


def release_requests(page, pattern, held) -> None:
    for route in held:
        try:
            route.continue_()
        except Exception:  # noqa: BLE001  route đã được Playwright xử lý
            pass
    try:
        page.unroute(pattern)
    except Exception:  # noqa: BLE001
        pass


def open_split(billing, catalog):
    child = need(catalog.split_child(), "con có ví còn tiền nhưng không đủ trả hết khoản (cần để thử Both)")
    db.ensure_split_state(child.student_id)
    billing.open(child.student_id)
    balance, total = billing.balance(), billing.outstanding_total()
    if not 0 < balance < total:
        pytest.skip(f"{child.name} không còn ở trạng thái chia khoản (ví {balance}, nợ {total}). Chạy reseed_r9.cmd rồi chạy lại")
    billing.select_all().to_method()
    return child


def split_input(page):
    region = page.get_by_label(T.SPLIT_LABEL)
    box = region.get_by_role("spinbutton").or_(region.get_by_role("textbox"))
    assert box.count() >= 1, "SCR-04 không có ô nhập phần EA"
    return box.first


def show(page, base_url, tx, inv=None):
    mocks.open_result(page, base_url, tx, inv)


def online_pending(amount=27.25):
    return mocks.transaction("Pending", funding=[mocks.funding("OnlineGateway", "Pending", amount, None)],
                             requested=amount, completed_at=None)


# =================================================================== F9.1 Truy cập và danh sách con
@F91
@pytest.mark.draft
@pytest.mark.known_defect(reason="Danh sách con trên SCR-01 không sắp theo thứ tự chữ cái mà theo thứ tự bản ghi trong DB (R9 TC-176)")
def test_tc_176_children_are_listed_in_alphabetical_order(accounts):
    """TC-176 Các con được liệt kê theo thứ tự chữ cái của tên (A đến Z), không theo thứ tự trong dữ liệu."""
    names = [card["name"] for card in accounts.open().read_all()]
    need(names if len(names) >= 2 else None, "phụ huynh có từ hai con")
    assert names == sorted(names, key=str.casefold), f"Thứ tự đang hiện: {names}"


@F91
def test_tc_177_double_click_on_child_card_opens_the_fee_page_once(page, accounts, billing):
    """TC-177 Nhấp đúp vào thẻ của con mở trang khoản phí đúng một lần: Back một lần quay về danh sách, không báo lỗi."""
    cards = accounts.open().read_cards()
    card = need(cards[0] if cards else None, "con nào")
    page.get_by_role("link", name=f"View fees for {card['name']}").dblclick()
    page.wait_for_url(re.compile(r"/billing/[^/?]+$"))
    billing.wait_ready()
    expect(billing.table_error).to_have_count(0)
    page.go_back()
    expect(accounts.heading).to_be_visible()
    assert re.search(r"/billing/?(\?.*)?$", page.url), f"Back một lần chưa về danh sách con: {page.url}"


@F91
@pytest.mark.known_defect(reason="Thẻ con chỉ hiện tên, mã tài khoản và trạng thái, không có nhãn 'Has outstanding invoices' / 'No outstanding invoices' (R9 TC-004, TC-005, TC-178)")
def test_tc_178_debt_label_counts_issued_invoices_only(accounts, catalog):
    """TC-178 Nhãn nợ trên thẻ con: có khoản chưa trả thì 'Has outstanding invoices', không thì 'No outstanding invoices'.
    Phần 'PaymentPending không tính là nợ' không kiểm được trên UI khoản phí (ASM-R9-UI-01)."""
    by_id = {c.student_id: c for c in catalog.children}
    problems = []
    for card in accounts.open().read_all():
        child = by_id.get(card["student_id"])
        expected = "Has outstanding invoices" if child and child.charges else "No outstanding invoices"
        if expected.lower() not in card["text"].lower():
            problems.append(f"{card['name']}: cần '{expected}', thẻ: {card['text']}")
    assert not problems, "; ".join(problems)


@F91
@pytest.mark.draft
def test_tc_179_loading_state_is_shown_while_the_child_list_loads(page, base_url, accounts):
    """TC-179 Trong lúc danh sách con đang tải có dấu hiệu đang tải, không hiện trạng thái rỗng, sau đó mới hiện thẻ.
    Độ trễ 3 giây được thay bằng giữ request lại cho tới khi test thả ra."""
    held = hold_requests(page, mocks.STUDENTS_RE)
    page.goto(f"{base_url}/billing", wait_until="commit")
    expect(loading_indicator(page).first).to_be_visible(timeout=5_000)
    expect(accounts.empty_title).to_have_count(0)
    assert accounts.cards.count() == 0, "Đã hiện thẻ con trước khi danh sách về"
    release_requests(page, mocks.STUDENTS_RE, held)
    accounts.wait_loaded()
    assert accounts.read_cards(), "Danh sách con rỗng sau khi tải xong"


@F91
@pytest.mark.api
@pytest.mark.known_defect(reason="Lần chạy 25/10/2026: API khoản phí trả 200 với danh sách rỗng cho mã sai định dạng ('abc') và GUID thừa ký tự, không từ chối 400/404 (R9 TC-180)")
def test_tc_180_malformed_or_hostile_ids_are_refused_without_a_server_error(api, base_url):
    """TC-180 Mã sai định dạng hoặc có nội dung độc hại trong đường dẫn và thân yêu cầu bị từ chối (400, 403 hoặc 404),
    không có lỗi 5xx, không trả dữ liệu, không lộ stack trace hay lỗi SQL, không phản chiếu thẻ HTML.
    Phần 'có nhật ký bảo mật' không kiểm được qua UI và API."""
    bad = {"abc": "abc", "guid_plus_one": quote(GUID + "0"), "sql": quote("' OR 1=1 --", safe=""),
           "script": quote("<script>alert(1)</script>", safe=""), "null_byte": quote(GUID) + "%00", "len51": "x" * 51}
    problems: list[str] = []
    for label, enc in bad.items():
        calls = {"charges": api.get(f"/billing/v1/students/{enc}/outstanding-charges"),
                 "wallet": api.get(f"/education-account/v1/edu-account/students/{enc}/wallet"),
                 "invoice": api.get(f"/billing/v1/invoices/{enc}"),
                 "transaction": api.get(f"/billing/v1/transactions/{enc}"),
                 "checkout": api.post("/billing/v1/checkout", checkout_body(bad_raw(label), [seed.UNKNOWN_ID_2], T.METHOD_ONLINE, base_url),
                                      key=f"r9-qa-tc180-{uuid.uuid4()}")}
        for name, response in calls.items():
            text = response.text()
            if response.status >= 500:
                problems.append(f"{label}/{name}: lỗi máy chủ {response.status}")
            elif response.status not in REFUSED:
                problems.append(f"{label}/{name}: mã {response.status}, mong đợi bị từ chối: {snippet(response, 100)}")
            if TECHNICAL.search(text):
                problems.append(f"{label}/{name}: thân phản hồi lộ chi tiết kỹ thuật: {snippet(response, 100)}")
            if "<script>" in text:
                problems.append(f"{label}/{name}: thân phản hồi phản chiếu thẻ script")
    assert not problems, "; ".join(problems)


def bad_raw(label: str) -> str:
    """Giá trị thô của từng mã xấu, dùng trong thân JSON."""
    return {"abc": "abc", "guid_plus_one": GUID + "0", "sql": "' OR 1=1 --", "script": "<script>alert(1)</script>",
            "null_byte": GUID + "\u0000", "len51": "x" * 51}[label]


@F91
@pytest.mark.api
@pytest.mark.known_defect(reason="Lần chạy 21/10/2026: API khoản phí trả 200 với danh sách rỗng cho mã học sinh lạ, không trả 403 FORBIDDEN_CHILD (R9 TC-012). "
                                  "Nên câu trả lời cho mã của gia đình khác và mã không tồn tại có thể khác nhau")
def test_tc_181_answer_for_another_family_equals_answer_for_unknown_id(api):
    """TC-181 Mã học sinh của gia đình khác và mã không tồn tại nhận cùng mã trạng thái và cùng thân phản hồi (403), để không lộ mã nào có thật."""
    require_db()
    other = db.sql_scalar(
        f"SELECT TOP 1 id FROM dbo.students WHERE id <> 'SYSTEM-TREASURY' AND ISNULL(father_nric, '') <> '{seed.NRIC}' "
        f"AND ISNULL(mother_nric, '') <> '{seed.NRIC}'", db=db.EA_DB)
    need(other or None, "học sinh của gia đình khác")
    problems = []
    for template in ("/billing/v1/students/{id}/outstanding-charges", "/education-account/v1/edu-account/students/{id}/wallet"):
        a, b = api.get(template.format(id=other)), api.get(template.format(id=seed.UNKNOWN_ID))
        body_a, body_b = a.text().replace(other, "<ID>"), b.text().replace(seed.UNKNOWN_ID, "<ID>")
        if a.status != b.status or body_a != body_b:
            problems.append(f"{template}: mã khác {a.status} và {b.status}, thân: {body_a[:80]!r} và {body_b[:80]!r}")
        if a.status not in (403, 404):
            problems.append(f"{template}: gia đình khác nhận mã {a.status}, mong đợi 403")
    assert not problems, "; ".join(problems)


# =================================================================== F9.2 Khoản phí còn nợ và số dư
@F92
@pytest.mark.draft
def test_tc_173_subsidy_is_shown_and_net_is_gross_minus_subsidy(billing, catalog):
    """TC-173 Trợ cấp FAS của từng dòng hiện ra và Net = Gross trừ Subsidy làm tròn lên ở chữ số thứ hai; tổng nợ của con bằng tổng Net.
    Con số cụ thể của S10 (36.33, 25.00, 11.33) chỉ có trên bộ seed R9, ở đây kiểm quy tắc."""
    child = need(next((c for c in catalog.with_charges()), None), "con có khoản phí chưa trả")
    billing.open(child.student_id)
    charges = billing.read_charges()
    problems = []
    for c in charges:
        if c.subsidy < 0 or c.subsidy > c.gross:
            problems.append(f"{c.description}: subsidy {c.subsidy} ngoài khoảng 0 đến {c.gross}")
        if c.net != (c.gross - c.subsidy).quantize(Decimal("0.01")):
            problems.append(f"{c.description}: net {c.net} khác {c.gross} trừ {c.subsidy}")
    assert not problems, "; ".join(problems)
    assert billing.outstanding_total() == sum((c.net for c in charges), Decimal(0)), "Tổng nợ khác tổng Net của các dòng"


@F92
@pytest.mark.draft
def test_tc_174_charge_fully_covered_by_subsidy_still_has_amount_to_pay_and_ea_option(billing, catalog):
    """TC-174 Khoản được trợ cấp nhiều vẫn còn số tiền phải trả (phần GST) lớn hơn 0 và vẫn chọn được Education Account khi ví đủ.
    Số 2.25 và 5.83 của S25 chỉ có trên bộ seed R9. Phần trả thật và số dư giảm đúng bằng Net đã có ở TC-065 và TC-067."""
    pairs = [(c, ch) for c in catalog.with_charges() for ch in c.charges if ch.subsidy > 0 and c.balance >= ch.net]
    child, charge = need(max(pairs, key=lambda p: p[1].subsidy / p[1].gross, default=None), "khoản có trợ cấp mà ví con đủ trả")
    assert charge.net > 0, f"{charge.description}: Net bằng 0.00 dù còn GST"
    billing.open(child.student_id)
    billing.select([charge.description]).to_method()
    state = billing.method_state()[T.METHOD_EA]
    assert state["present"] and not state["disabled"], f"Education Account bị khóa: {state}"


@F92
def test_tc_182_html_in_a_line_description_is_shown_as_text(page, billing, catalog):
    """TC-182 Mô tả khoản phí chứa HTML được hiện đúng như chữ, không in đậm, không chạy script (không có hộp thoại alert).
    Test sửa tên khoản của một khoản phí TẠM (db.temp_charges tự xóa)."""
    require_db()
    child = pick_child(catalog)
    payload = "<b>Fees</b><script>alert(1)</script>"
    dialogs: list[str] = []
    page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))
    with db.temp_charges(student_id=child.student_id, amounts=[27.25]) as (stu_id, cids):
        db.sql_raw(f"UPDATE dbo.student_charges SET fee_component_name_snapshot = N'{payload}' WHERE id = '{cids[0]}';")
        billing.open(stu_id)
        shown = [c.description for c in billing.read_charges()]
        assert payload in shown, f"Mô tả không hiện như chữ: {shown}"
        assert billing.table.locator("tbody b, tbody script").count() == 0, "HTML trong mô tả được dựng thành thẻ"
        assert not dialogs, f"Script đã chạy: {dialogs}"


@F92
def test_tc_183_double_click_on_continue_moves_to_the_method_step_once(billing, catalog, requests_log):
    """TC-183 Nhấp đúp Continue ở bước chọn khoản chỉ sang bước phương thức một lần, không nhảy tiếp sang bước xem lại,
    chưa có giao dịch nào. (Bản build chọn khoản rồi Continue, không có nút Pay trên từng hóa đơn.)"""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    (charge,), _ = live_smallest(billing, child)
    before = snapshot(billing)
    billing.select([charge.description])
    billing.continue_button.dblclick()
    expect(billing.summary_heading).to_be_visible()
    expect(billing.review_heading).to_have_count(0)
    assert_nothing_created(billing, requests_log, child, before)


@F92
@pytest.mark.draft
@pytest.mark.known_defect(reason="Lần chạy 25/10/2026: trang khoản phí của con có khoản phí không có liên kết 'Back to education accounts' trong nội dung trang, liên kết chỉ có ở trang lỗi tải ví (R9 TC-184)")
def test_tc_184_back_to_child_list_link_works_on_the_fee_page(page, billing, catalog):
    """TC-184 (phần 1) Trang khoản phí có nút quay về danh sách con và bấm vào mở đúng danh sách."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    billing.open(child.student_id)
    back = page.get_by_role("link", name=T.BACK_TO_ACCOUNTS).or_(
        page.get_by_role("button", name=re.compile(r"back to (the )?(child|education account)", re.I)))
    assert back.count() >= 1, "Trang khoản phí không có nút quay về danh sách con"
    back.first.click()
    page.wait_for_url(re.compile(r"/billing/?(\?.*)?$"))


@F92
@pytest.mark.known_defect(reason="Trạng thái rỗng thật không có liên kết quay về danh sách con trong nội dung trang, chỉ có menu bên (quan sát 21/10/2026, R9 TC-032, TC-033, TC-184)")
def test_tc_184_back_to_child_list_link_works_on_the_empty_state(page, billing, catalog):
    """TC-184 (phần 2) Trạng thái rỗng của con không còn khoản phí có nút quay về danh sách con."""
    child = need(catalog.empty_child(), "con không còn khoản phí")
    billing.open(child.student_id)
    back = page.get_by_role("main").get_by_role("link", name=re.compile("back|child|education account", re.I))
    assert back.count() >= 1, "Trạng thái rỗng không có nút quay về danh sách con"


@F92
@pytest.mark.draft
def test_tc_185_loading_state_is_shown_while_the_fee_list_loads(page, billing, catalog):
    """TC-185 Trong lúc danh sách khoản phí đang tải có dấu hiệu đang tải và chưa hiện câu 'No outstanding charges'."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    held = hold_requests(page, mocks.CHARGES_RE)
    page.goto(f"{billing.base_url}/billing/{child.student_id}", wait_until="commit")
    expect(loading_indicator(page).first).to_be_visible(timeout=5_000)
    expect(billing.empty_state).to_have_count(0)
    release_requests(page, mocks.CHARGES_RE, held)
    billing.wait_ready()
    assert billing.read_charges(), "Không có khoản phí sau khi tải xong"


@F92
@pytest.mark.draft
def test_tc_200_balance_is_shown_with_thousand_separator_and_two_decimals(billing, catalog):
    """TC-200 (phần 1) Số tiền hiện có dấu phẩy ngăn nghìn và hai chữ số thập phân (1,590.00)."""
    children = need(catalog.usable() or None, "con nào")
    problems = []
    for child in children:
        billing.open(child.student_id)
        for token in all_money(billing.card_text(T.CARD_BALANCE)) + all_money(billing.card_text(T.CARD_OUTSTANDING)):
            if not two_decimals(token):
                problems.append(f"{child.name}: {token}")
    assert not problems, "; ".join(problems)


@F92
@pytest.mark.draft
@pytest.mark.known_defect(reason="Lần chạy 25/10/2026: bảng khoản phí không có cột ngày hạn nộp, cột Status chỉ hiện Overdue, Due soon hoặc Upcoming (R9 TC-200 phần 2)")
def test_tc_200_due_dates_follow_dd_mm_yyyy(catalog):
    """TC-200 (phần 2) Hạn nộp hiện theo DD/MM/YYYY (30/10/2026)."""
    charges = [(c.name, ch.description, ch.due) for c in catalog.with_charges() for ch in c.charges]
    need(charges or None, "khoản phí nào")
    bad = [f"{n}/{d}: {due!r}" for n, d, due in charges if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", due)]
    assert not bad, "; ".join(bad[:8])


# =================================================================== F9.3 Phương thức thanh toán
def assert_default(billing, expected: str) -> None:
    state = billing.method_state()
    checked = [m for m, v in state.items() if v["present"] and v["checked"]]
    assert checked == [expected], f"Phương thức đang chọn: {checked}, mong đợi {expected}; {state}"
    expect(billing.continue_button).to_be_enabled()


@F93
def test_tc_186_education_account_is_preselected_when_the_balance_is_enough(billing, catalog, requests_log):
    """TC-186 (ví đủ) Education Account được gợi ý và chọn sẵn, chưa trừ gì."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    before = snapshot(billing)
    billing.select([charge.description]).to_method()
    assert_default(billing, T.METHOD_EA)
    assert_nothing_created(billing, requests_log, child, before)


@F93
@pytest.mark.draft
def test_tc_186_both_is_preselected_and_ea_only_is_disabled_when_the_balance_is_short(billing, catalog):
    """TC-186 (ví thiếu) Both được chọn sẵn và nút chỉ Education Account bị khóa."""
    require_db()
    child = pick_child(catalog)
    with db.temp_charges(student_id=child.student_id, amounts=[40.00, 30.00], balance=20.00) as (stu_id, _cids):
        billing.open(stu_id)
        billing.select_all().to_method()
        assert billing.method_state()[T.METHOD_EA]["disabled"]
        assert_default(billing, T.METHOD_BOTH)


@F93
@pytest.mark.mocked
def test_tc_186_online_is_the_only_and_selected_method_when_there_is_no_balance(page, billing, catalog):
    """TC-186 (không có ví hoặc ví 0) Online Gateway là phương thức duy nhất và được chọn sẵn. Ví 0.00 được giả lập."""
    child = need(catalog.with_charges()[0] if catalog.with_charges() else None, "con có khoản phí chưa trả")
    (charge,), _ = live_smallest(billing, child)
    mocks.mock_json(page, mocks.WALLET_RE, mocks.wallet(child.student_id, child.name, 0.0))
    billing.open(child.student_id)
    billing.select([charge.description]).to_method()
    assert_default(billing, T.METHOD_ONLINE)
    assert billing.method_state()[T.METHOD_EA]["disabled"]


def fill_ea(box, value: str) -> bool:
    """Gõ giá trị vào ô phần EA. Trả False nếu trình duyệt tự từ chối (ô số không nhận chữ, dấu cách...)."""
    try:
        box.fill(value)
    except Exception:  # noqa: BLE001  ô type=number từ chối ký tự không phải số
        return False
    return True


def accepted(billing, box, value: str) -> bool:
    """Giá trị coi là được nhận nếu gõ được và nút Continue vẫn bật. UI thật khóa Continue khi phần EA không hợp lệ."""
    return fill_ea(box, value) and billing.continue_button.is_enabled()


@F93
def test_tc_187_ea_part_rejects_values_that_are_not_numbers(page, billing, catalog, requests_log):
    """TC-187 Phần EA từ chối giá trị không phải số, giữ nguyên bước phương thức, không tạo giao dịch.
    UI thật dùng ô type=number: chữ bị trình duyệt chặn, giá trị sai làm nút Continue bị khóa (quan sát 25/10/2026)."""
    open_split(billing, catalog)
    box, problems = split_input(page), []
    for value in ["", "abc", "S$20", "-5", "1e2", "20,5", "   "]:
        if accepted(billing, box, value):
            problems.append(f"{value!r} được nhận")
    assert not problems and not requests_log.posts("/checkout"), "; ".join(problems)


@F93
def test_tc_188_ea_part_follows_length_decimal_and_space_rules(page, billing, catalog):
    """TC-188 Phần EA: 20.001, 13 ký tự và dấu cách giữa bị từ chối; số nguyên và dạng .00 được nhận và phần online = tổng trừ phần EA.
    Dấu cách hai đầu không gõ được vào ô số của trình duyệt nên không thử (R9 mong đợi cắt dấu cách)."""
    open_split(billing, catalog)
    box, total = split_input(page), billing.total_to_pay()
    whole = int(min(billing.method_balance(), total - 1))
    problems = []
    for value in ["20.001", "1234567890.12", "2 0"]:
        if accepted(billing, box, value):
            problems.append(f"{value!r} được nhận")
    for value in [f"{whole}", f"{whole}.00"]:
        if not fill_ea(box, value):
            problems.append(f"{value!r} không gõ được")
            continue
        online = billing.split_parts()[1]
        if online != total - whole:
            problems.append(f"{value!r}: phần online {online}, mong đợi {total - whole}")
    assert not problems, "; ".join(problems)


@F93
def test_tc_189_ea_part_treats_script_and_special_characters_as_text(page, billing, catalog, requests_log):
    """TC-189 Phần EA coi script, SQL và ký tự đặc biệt là chữ: bị từ chối, không chạy gì, không lỗi 5xx."""
    open_split(billing, catalog)
    dialogs: list[str] = []
    page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))
    box, problems = split_input(page), []
    for value in ["' OR 1=1 --", "<script>alert(1)</script>", '{"a":1}', "${7*7}", "../../etc/passwd", "\u0000", "😀"]:
        if accepted(billing, box, value):
            problems.append(f"{value!r} được nhận")
    assert not problems and not dialogs and not requests_log.posts("/checkout"), f"{problems} {dialogs}"


@F93
@pytest.mark.known_defect(reason="Lần chạy 25/10/2026: hạ phần EA từ 20.00 xuống 19.00, đổi sang Online rồi về Both thì phần EA vẫn giữ 19.00, không về mặc định 20.00 (R9 TC-190)")
def test_tc_190_ea_part_goes_back_to_default_when_method_changes(page, billing, catalog):
    """TC-190 Hạ phần EA, đổi sang Online rồi về Both thì phần EA và phần online về mặc định."""
    open_split(billing, catalog)
    box = split_input(page)
    default_ea = box.input_value()
    box.fill(str(max(Decimal("0.01"), Decimal(default_ea or "1") - 1)))
    billing.choose_method(T.METHOD_ONLINE).choose_method(T.METHOD_BOTH)
    assert split_input(page).input_value() == default_ea, "Phần EA không về mặc định sau khi đổi phương thức"
    assert Decimal(default_ea) == billing.method_balance(), "Mặc định của Both phải là toàn bộ số dư"


@F93
@pytest.mark.known_defect(reason="Lần chạy 25/10/2026: nhấp đúp Continue ở bước phương thức làm yêu cầu POST /checkout được gửi đi, nghĩa là cú nhấp thứ hai rơi vào nút Authorize & pay vừa hiện ra ở cùng vị trí (R9 TC-191 phần 2). Cần Dev xác nhận")
def test_tc_191_double_click_on_continue_opens_the_review_step_once(billing, catalog, requests_log):
    """TC-191 (phần 2) Nhấp đúp Continue ở bước phương thức chỉ sang bước xem lại một lần và chưa có giao dịch."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    before = snapshot(billing)
    billing.select([charge.description]).to_method()
    billing.continue_button.dblclick()
    expect(billing.review_heading).to_be_visible()
    assert billing.authorize_button.count() == 1
    assert_nothing_created(billing, requests_log, child, before)


@F93
def test_tc_191_failed_check_on_continue_keeps_the_screen_and_changes_nothing(page, billing, catalog, requests_log):
    """TC-191 (phần 1) Phần EA lớn hơn số dư: không sang bước xem lại, có thông báo thiếu số dư, không có giao dịch mới.
    UI thật khóa nút Continue thay vì cho bấm rồi báo lỗi."""
    open_split(billing, catalog)
    split_input(page).fill(str(billing.method_balance() + 5))
    expect(billing.continue_button).to_be_disabled()
    expect(billing.review_heading).to_have_count(0)
    assert re.search(r"not enough|pay the rest online|no more than your Education Account balance", billing.main_text(), re.I), "Không có thông báo thiếu số dư"
    assert not requests_log.posts("/checkout")


@F93
def test_tc_192_back_on_the_method_step_returns_to_the_charge_list_and_changes_nothing(billing, catalog, requests_log):
    """TC-192 Back ở bước phương thức (nhấp đúp) quay về danh sách khoản đúng một lần; khoản vẫn còn, số dư không đổi, không có giao dịch.
    Đích quay về là đề xuất của QA (FS không nêu)."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    before = snapshot(billing)
    billing.select([charge.description]).to_method()
    billing.back_button.dblclick()
    expect(billing.charges_heading).to_be_visible()
    expect(billing.summary_heading).to_have_count(0)
    assert charge.description in [c.description for c in billing.read_charges()]
    assert_nothing_created(billing, requests_log, child, before)


@F94
@pytest.mark.known_defect(reason="Màn xem lại (Review & authorize) chỉ có Back và Authorize & pay trong Page Object; chưa thấy nút Cancel (R9 TC-193, đích Cancel là đề xuất của QA). Cần xác nhận trên bản build")
def test_tc_193_cancel_on_the_review_step_leaves_without_paying(page, billing, catalog, requests_log):
    """TC-193 (phần 1) Có nút Cancel ở bước xem lại, bấm vào rời đi không thanh toán, khoản còn nợ và số dư không đổi.
    Phần 2 (Cancel bị khóa sau Confirm, cần thanh toán thật) không tự động hóa vì timing của trạng thái Processing."""
    child = need(catalog.ea_child(), "con có ví đủ trả khoản phí nhỏ nhất")
    (charge,), _ = live_smallest(billing, child, need_balance=True)
    before = snapshot(billing)
    billing.start([charge.description], T.METHOD_EA)
    cancel = page.get_by_role("button", name=re.compile(r"^cancel", re.I))
    assert cancel.count() == 1, "Bước xem lại không có nút Cancel"
    cancel.click()
    assert_nothing_created(billing, requests_log, child, before)


# =================================================================== F9.4 và F9.5 Khóa idempotency, thanh toán
@F94
@pytest.mark.api
@pytest.mark.draft
@pytest.mark.known_defect(reason="Lần chạy 25/10/2026 (mỗi khóa thử trên một khoản phí riêng): khóa có dấu cách giữa, nháy đơn, chấm phẩy, HTML và JSON đều được nhận với mã 200, không bị từ chối 400 (R9 TC-194)")
def test_tc_194_idempotency_key_with_not_allowed_characters_is_refused(api, base_url, catalog):
    """TC-194 Khóa có dấu cách, nháy, chấm phẩy, HTML, JSON, ký tự điều khiển hoặc emoji bị từ chối 400 và không bị sửa im lặng;
    khóa UUID và a-b_c9 được nhận. Chạy trên khoản phí TẠM. Khóa có dấu cách đầu hoặc cuối không thử được vì HTTP tự cắt khoảng trắng hai đầu giá trị header."""
    require_db()
    child = pick_child(catalog)
    refused = {"dấu cách giữa": "key 1", "nháy đơn": "key'1", "chấm phẩy": "key;1", "html": "<b>k</b>", "json": '{"k":1}',
               "ký tự điều khiển": "key\x01x", "emoji": "key\U0001F600"}
    n = len(refused)
    # Mỗi khóa sai dùng một khoản phí riêng (1.00): nếu khóa đầu được nhận và tạo hóa đơn thì các lần sau trả 409 vì khoản đã bị dùng,
    # che mất kết quả thật của các khóa còn lại. Hai khoản cuối (35.00 và 20.00) dành cho hai khóa hợp lệ.
    with db.temp_charges(student_id=child.student_id, amounts=[1.00] * n + [35.00, 20.00], balance=300.00) as (stu_id, cids):
        problems, unsendable = [], []
        for (label, key), cid in zip(refused.items(), cids):
            try:
                response = api.post("/billing/v1/checkout", checkout_body(stu_id, [cid], T.METHOD_EA, base_url), key=key)
            except Exception:  # noqa: BLE001  client không gửi được header này
                unsendable.append(label)
                continue
            if response.status not in (400, 422):
                problems.append(f"{label}: mã {response.status}")
        assert not problems, "; ".join(problems)
        assert all(charge_used(c) == 0 for c in cids[:n]) and wallet_balance(stu_id) == Decimal("300.00"), "Khóa sai vẫn tạo giao dịch hoặc trừ ví"
        ok1 = api.post("/billing/v1/checkout", checkout_body(stu_id, [cids[n]], T.METHOD_EA, base_url), key=str(uuid.uuid4()))
        ok2 = api.post("/billing/v1/checkout", checkout_body(stu_id, [cids[n + 1]], T.METHOD_EA, base_url), key="a-b_c9")
        assert ok1.status == 200 and ok2.status == 200, f"Khóa hợp lệ bị từ chối: {ok1.status} {ok2.status}: {snippet(ok1)} {snippet(ok2)}"
        assert wallet_balance(stu_id) == Decimal("245.00")


@F94
@pytest.mark.api
@pytest.mark.draft
@pytest.mark.known_defect(reason="Lần chạy 25/10/2026: gửi lại cùng khóa với khoản phí khác trả 200 'Checkout already created (idempotent)' và trả giao dịch cũ, không từ chối 409 (R9 TC-195, đề xuất của QA)")
def test_tc_195_same_key_with_different_content_is_refused(api, base_url, catalog):
    """TC-195 Cùng khóa nhưng khác khoản phí hoặc khác phương thức bị từ chối bằng mã xung đột (đề xuất của QA) và không tạo giao dịch.
    Bước gửi lại đúng nội dung cũ không kiểm ở đây vì đã có TC-078 và TC-080 (hiện là known_defect)."""
    require_db()
    child = pick_child(catalog)
    with db.temp_charges(student_id=child.student_id, amounts=[21.26, 70.63], balance=405.00) as (stu_id, cids):
        key = f"r9-qa-tc195-{uuid.uuid4()}"
        first = api.post("/billing/v1/checkout", checkout_body(stu_id, [cids[0]], T.METHOD_EA, base_url), key=key)
        assert first.status == 200, f"Yêu cầu đầu bị từ chối: {first.status} {snippet(first)}"
        other_charge = api.post("/billing/v1/checkout", checkout_body(stu_id, [cids[1]], T.METHOD_EA, base_url), key=key)
        other_method = api.post("/billing/v1/checkout", checkout_body(stu_id, [cids[0]], T.METHOD_ONLINE, base_url), key=key)
        assert other_charge.status in (400, 409, 422), f"Khác khoản: mã {other_charge.status} {snippet(other_charge)}"
        assert other_method.status in (400, 409, 422), f"Khác phương thức: mã {other_method.status} {snippet(other_method)}"
        assert charge_used(cids[1]) == 0, "Khoản thứ hai bị tạo hóa đơn dù khóa trùng"
        assert wallet_balance(stu_id) == Decimal("383.74"), "Số dư khác 405.00 trừ 21.26"


@F93
@pytest.mark.api
@pytest.mark.draft
def test_tc_201_wrong_method_values_are_refused_and_create_nothing(api, base_url, catalog):
    """TC-201 Phương thức sai (0, 99, -1, chữ lạ, rỗng, null) bị từ chối và không tạo giao dịch. Số lượng và thứ tự leg của sổ case
    không có trong API checkout (API nhận method và eaAmount, không nhận danh sách leg) nên phần đó không tự động hóa."""
    require_db()
    child = pick_child(catalog)
    with db.temp_charges(student_id=child.student_id, amounts=[21.26], balance=300.00) as (stu_id, cids):
        problems = []
        for method in (0, 99, -1, "Foo", "", None):
            response = api.post("/billing/v1/checkout", checkout_body(stu_id, cids, method, base_url), key=f"r9-qa-tc201-{uuid.uuid4()}")
            if response.status not in (400, 422):
                problems.append(f"method={method!r}: mã {response.status}")
        assert not problems, "; ".join(problems)
        assert charge_used(cids[0]) == 0 and wallet_balance(stu_id) == Decimal("300.00"), "Phương thức sai vẫn tạo giao dịch"


# =================================================================== F9.7 Kết quả, biên lai
@F97
@pytest.mark.mocked
def test_tc_196_waiting_screen_shows_pending_status_and_leg(page, base_url, result):
    """TC-196 (phần 1) Màn chờ hiện trạng thái Pending, leg online 27.25 Pending, không có Print receipt."""
    show(page, base_url, online_pending())
    expect(result.status_heading).to_have_text(T.RESULT_PENDING)
    rows = result.funding_rows()
    assert rows and rows[0][0].startswith("Online Gateway") and "Pending" in rows[0][0], rows
    assert "27.25" in rows[0][1], rows
    assert result.print_button.count() == 0


@F97
@pytest.mark.mocked
def test_tc_196_reconciliation_required_screen_says_being_checked_not_failed(page, base_url, result):
    """TC-196 (phần 2 và 3) ReconciliationRequired: tiêu đề cần xem lại, leg EA ReconciliationRequired, không nói thất bại,
    không hiện màn thất bại."""
    funding = [mocks.funding("EducationAccount", "ReconciliationRequired", 27.25, 27.25)]
    show(page, base_url, mocks.transaction("ReconciliationRequired", funding=funding, requested=27.25, settled=None))
    expect(result.status_heading).to_have_text(T.RESULT_REVIEW)
    assert not re.search(r"failed|could not be completed", result.status_text(), re.I), result.status_text()
    assert "Reconciliation" in result.funding_rows()[0][0], result.funding_rows()


@F97
@pytest.mark.mocked
@pytest.mark.known_defect(reason="Màn kết quả hiện Transaction ID dạng GUID, không có mã tham chiếu PAY-YYYYMMDD-XXXXXX (TC-196; xem test extra về TRX-<UUID> ở F9.7)")
def test_tc_196_waiting_screen_shows_the_payment_reference(page, base_url, result):
    """TC-196 (phần 1) Mã tham chiếu PAY-YYYYMMDD-XXXXXX (tối đa 50 ký tự) hiện trên màn chờ."""
    show(page, base_url, online_pending())
    expect(result.status_heading).to_have_text(T.RESULT_PENDING)
    assert re.search(r"PAY-\d{8}-\d{6}", result.text()), "Không có mã tham chiếu PAY-YYYYMMDD-XXXXXX"


@F97
@pytest.mark.mocked
@pytest.mark.known_defect(reason="Màn chờ tự làm mới mỗi 2 giây và không có nút 'Refresh status' (suy ra từ mã nguồn PaymentResultPage; R9 TC-197)")
def test_tc_197_refresh_status_button_is_disabled_for_a_moment_after_a_click(page, base_url, result, requests_log):
    """TC-197 Nút Refresh status chỉ đọc trạng thái, bị khóa vài giây sau khi bấm và nhấp đúp chỉ gửi một yêu cầu."""
    show(page, base_url, online_pending())
    refresh = page.get_by_role("button", name=re.compile(r"refresh", re.I))
    assert refresh.count() == 1, "Màn chờ không có nút Refresh status"
    refresh.click()
    expect(refresh).to_be_disabled()
    assert not requests_log.posts("/checkout")


@F97
@pytest.mark.mocked
def test_tc_198_success_screen_has_a_button_back_to_the_fee_list(page, base_url, result):
    """TC-198 Màn thành công có nút về danh sách khoản phí. (Phần 'danh sách rỗng sau khi trả hết' cần thanh toán thật, đã có ở TC-084.)"""
    show(page, base_url, mocks.transaction("Succeeded", funding=[mocks.funding("EducationAccount", "Succeeded", 27.25, 27.25)], settled=27.25),
         mocks.invoice(27.25))
    expect(result.status_heading).to_have_text(T.RESULT_SUCCEEDED)
    back = page.get_by_role("link", name=re.compile(r"fee|charge|outstanding", re.I)).or_(
        page.get_by_role("button", name=re.compile(r"fee|charge|outstanding", re.I)))
    assert back.count() >= 1, "Không có nút về danh sách khoản phí"


@F97
@pytest.mark.mocked
@pytest.mark.parametrize("status,legs,printable", [
    ("Succeeded", [mocks.funding("EducationAccount", "Succeeded", 27.25, 27.25)], True),
    ("Failed", [mocks.funding("EducationAccount", "Failed", 27.25, None)], False),
    ("Pending", [mocks.funding("OnlineGateway", "Pending", 27.25, None)], False),
    ("ReconciliationRequired", [mocks.funding("EducationAccount", "ReconciliationRequired", 27.25, 27.25)], False),
], ids=["succeeded", "failed", "pending", "reconciliation"])
def test_tc_199_receipt_button_exists_only_for_a_succeeded_payment(page, base_url, result, status, legs, printable):
    """TC-199 (phần 1) Nút biên lai chỉ có khi giao dịch Succeeded; Failed, Pending và ReconciliationRequired không có.
    Phần 'yêu cầu biên lai của giao dịch không thành công bị API từ chối' chưa có đường dẫn API biên lai trên bản build nên chưa kiểm."""
    show(page, base_url, mocks.transaction(status, funding=legs, requested=27.25, settled=27.25 if printable else None),
         mocks.invoice(27.25) if printable else None)
    expect(page.get_by_role("heading", level=2).first).to_be_visible()
    assert (result.print_button.count() == 1) is printable, f"Print receipt: {result.print_button.count()} với trạng thái {status}"


@F97
@pytest.mark.mocked
@pytest.mark.known_defect(reason="Biên lai chỉ có nút Print receipt (gọi window.print), không tải file receipt_<mã>.pdf (R9 TC-131, TC-132, TC-199)")
def test_tc_199_receipt_file_is_named_receipt_reference_pdf(page, base_url, result):
    """TC-199 (phần 2) Tải biên lai ra file receipt_<mã tham chiếu>.pdf."""
    show(page, base_url, mocks.transaction("Succeeded", funding=[mocks.funding("EducationAccount", "Succeeded", 27.25, 27.25)], settled=27.25),
         mocks.invoice(27.25))
    with page.expect_download(timeout=5_000) as download:
        result.print_button.click()
    assert re.fullmatch(r"receipt_.+\.pdf", download.value.suggested_filename), download.value.suggested_filename


@F97
@pytest.mark.mocked
@pytest.mark.draft
@pytest.mark.known_defect(reason="Lần chạy 25/10/2026: màn kết quả hiện giờ hoàn tất theo kiểu Mỹ 'Oct 21, 2026, 12:30 PM' (giờ Singapore đúng, định dạng không phải DD/MM/YYYY HH:mm 24 giờ) (R9 TC-200 phần 3)")
def test_tc_200_paid_at_time_is_shown_as_dd_mm_yyyy_hh_mm_in_singapore_time(page, base_url, result):
    """TC-200 (phần 3) Giờ hoàn tất hiện 21/10/2026 12:30 (24 giờ, giờ Singapore) cho 04:30 UTC."""
    show(page, base_url, mocks.transaction("Succeeded", funding=[mocks.funding("EducationAccount", "Succeeded", 27.25, 27.25)], settled=27.25,
                                           completed_at="2026-10-21T04:30:00Z"), mocks.invoice(27.25))
    shown = result.fact("Completed at") or ""
    assert re.search(r"21/10/2026,? 12:30\b", shown), f"Giờ hiển thị: {shown!r}"


# =================================================================== F9.6 Webhook
def start_online_checkout(api, base_url: str, stu_id: str, charge_ids: list[str]) -> tuple[str, str]:
    response = api.post("/billing/v1/checkout", checkout_body(stu_id, charge_ids, T.METHOD_ONLINE, base_url), key=f"r9-qa-f99-{uuid.uuid4()}")
    assert response.status == 200, f"Không tạo được checkout online: {response.status} {snippet(response)}"
    tx_id = response.json()["data"]["transactionId"]
    legs = db.get_tx_bundle(tx_id)["legs"]
    assert len(legs) == 1
    return tx_id, legs[0]["funding_reference"]


@F96
@pytest.mark.api
def test_tc_202_callback_that_matches_no_leg_is_ignored_and_changes_nothing(api, base_url, catalog):
    """TC-202 (callback A) Callback hợp lệ nhưng không khớp leg nào được lưu với trạng thái Ignored; leg và hóa đơn không đổi."""
    require_db()
    child = pick_child(catalog)
    with db.temp_charges(student_id=child.student_id, amounts=[21.26]) as (stu_id, cids):
        tx_id, _ = start_online_checkout(api, base_url, stu_id, cids)
        status, body, ev_id = db.post_webhook(f"NOT-A-LEG-{uuid.uuid4().hex[:10]}", amount_cents=2126)
        try:
            assert status == 200 and body["data"]["processingStatus"] == "Ignored", (status, body)
            assert db.get_webhook_receipt(ev_id)["processing_status"] == "3"
            bundle = db.get_tx_bundle(tx_id)
            assert bundle["legs"][0]["status"] == "1" and bundle["invoice"]["status"] == "3", "Leg hoặc hóa đơn đã đổi"
        finally:
            db.delete_webhook_receipt(ev_id)


@F96
@pytest.mark.api
@pytest.mark.known_defect(reason="TC-122 đã ghi nhận: callback lệch số tiền chỉ đánh dấu biên nhận Failed và để leg Pending, chưa chuyển leg sang ReconciliationRequired (đề xuất của QA trong TC-202)")
def test_tc_202_callback_with_another_amount_needs_reconciliation(api, base_url, catalog):
    """TC-202 (callback B) Callback có số tiền khác (20.00 thay vì 21.26) đưa leg online sang ReconciliationRequired; hóa đơn không Paid."""
    require_db()
    child = pick_child(catalog)
    with db.temp_charges(student_id=child.student_id, amounts=[21.26]) as (stu_id, cids):
        tx_id, ref = start_online_checkout(api, base_url, stu_id, cids)
        status, _, ev_id = db.post_webhook(ref, amount_cents=2000)
        try:
            assert status == 200
            tx = api.get(f"/billing/v1/transactions/{tx_id}").json()["data"]
            assert {f["method"]: f["status"] for f in tx["fundingSources"]} == {T.METHOD_ONLINE: "ReconciliationRequired"}, tx["fundingSources"]
            assert db.get_tx_bundle(tx_id)["invoice"]["status"] != "4", "Hóa đơn đã Paid"
        finally:
            db.delete_webhook_receipt(ev_id)


@F96
@pytest.mark.api
@pytest.mark.draft
@pytest.mark.parametrize("field,limit", [("eventId", 128), ("transactionId", 128), ("referenceId", 50)])
def test_tc_203_callback_text_field_accepts_its_maximum_length(field, limit):
    """TC-203 (giới hạn) Giá trị dài đúng giới hạn được nhận và lưu đủ. Dùng mã leg không tồn tại nên callback chỉ thành biên nhận Ignored."""
    require_db()
    value = "Q" * limit
    kwargs = {"eventId": {"event_id": value, "reference_id": f"NOT-A-LEG-{uuid.uuid4().hex[:8]}"},
              "transactionId": {"provider_tx_id": value, "reference_id": f"NOT-A-LEG-{uuid.uuid4().hex[:8]}"},
              "referenceId": {"reference_id": value}}[field]
    status, _, ev_id = db.post_webhook(**kwargs)
    try:
        assert status == 200, f"{field} dài {limit} bị từ chối với mã {status}"
        assert db.get_webhook_receipt(ev_id), f"{field} dài {limit} không được lưu đủ"
    finally:
        db.delete_webhook_receipt(ev_id)


@F96
@pytest.mark.api
@pytest.mark.draft
@pytest.mark.known_defect(reason="Lần chạy 25/10/2026: callback có trường văn bản dài hơn giới hạn một ký tự trả 500 thay vì 400/422 (R9 TC-203)")
@pytest.mark.parametrize("field,limit", [("eventId", 128), ("transactionId", 128), ("referenceId", 50), ("providerCode", 40), ("eventType", 50)])
def test_tc_203_callback_text_field_refuses_one_more_character(field, limit):
    """TC-203 (giới hạn cộng 1) Giá trị dài hơn giới hạn một ký tự bị từ chối và không lưu biên nhận nào."""
    require_db()
    value = "Q" * (limit + 1)
    kwargs = {"eventId": {"event_id": value}, "transactionId": {"provider_tx_id": value}, "referenceId": {"reference_id": value},
              "providerCode": {"provider_code": value}, "eventType": {"event_type": value}}[field]
    kwargs.setdefault("reference_id", f"NOT-A-LEG-{uuid.uuid4().hex[:8]}")
    status, _, ev_id = db.post_webhook(**kwargs)
    receipt = db.get_webhook_receipt(ev_id)
    try:
        assert status in (400, 413, 422), f"{field} dài {limit + 1} nhận mã {status}"
        assert not receipt, f"{field} dài {limit + 1} vẫn được lưu biên nhận"
    finally:
        db.delete_webhook_receipt(ev_id)


# =================================================================== F9.8 Ràng buộc cơ sở dữ liệu
DB_SETUP = """
DECLARE @stu varchar(50) = (SELECT TOP 1 student_id FROM dbo.student_charges);
DECLARE @sch varchar(50) = (SELECT TOP 1 school_id FROM dbo.student_charges WHERE student_id = @stu);
"""


def invoice_sql(var: str, number: str | None = None) -> str:
    cols = "id, student_id, school_id, currency_code, gross_amount, subsidy_amount, net_amount, status, issued_at, due_date"
    vals = f"{var}, @stu, @sch, 'SGD', 100.00, 0.00, 100.00, 2, SYSUTCDATETIME(), '2026-12-15'"
    if number is not None:
        cols, vals = "invoice_number, " + cols, f"'{number}', " + vals
    return f"DECLARE {var} varchar(50) = CONVERT(varchar(50), NEWID()); INSERT INTO dbo.invoices ({cols}) VALUES ({vals});"


def transaction_sql(var_invoice: str, reference: str, status: int, tag: str) -> str:
    # CK_transactions_StatusAmounts: 2 Succeeded cần settled = requested và completed_at; 3 và 4 cần completed_at, settled rỗng hoặc 0;
    # 1 và 5 không có completed_at. Trạng thái 0 và 6 vẫn bị CK_transactions_Status từ chối.
    settled = "100.00" if status == 2 else "NULL"
    completed = "SYSUTCDATETIME()" if status in (2, 3, 4) else "NULL"
    return (f"INSERT INTO dbo.transactions (id, invoice_id, initiated_by_user_id, transaction_reference, idempotency_key, requested_amount, "
            f"settled_amount, currency_code, status, completed_at) "
            f"VALUES (CONVERT(varchar(50), NEWID()), {var_invoice}, 'qa-user', '{reference}', 'idem-qa-{tag}-' + CONVERT(varchar(36), NEWID()), "
            f"100.00, {settled}, 'SGD', {status}, {completed});")


@F98
@pytest.mark.draft
def test_tc_205_invoice_number_accepts_50_characters_and_refuses_51():
    """TC-205 Số hóa đơn dài 50 ký tự được nhận, 51 ký tự bị từ chối. Chạy trong giao dịch SQL có ROLLBACK, không để lại dữ liệu.
    Phần 3 (hiện trên một dòng ở SCR-02) không tự động hóa vì hóa đơn chưa có trước khi thanh toán trên UI."""
    require_db()
    res = db.sql_check_steps(steps=[("ok_50", invoice_sql("@i50", "INV-2026-" + "X" * 41)),
                                    ("bad_51", invoice_sql("@i51", "INV-2026-" + "X" * 42))], setup_sql=DB_SETUP)
    assert res.get("ok_50") == "OK", f"50 ký tự bị từ chối: {res.get('ok_50')}"
    assert res.get("bad_51", "OK").startswith("ERR"), "51 ký tự vẫn được nhận"


@F98
@pytest.mark.draft
def test_tc_206_transaction_reference_is_unique_and_status_accepts_only_1_to_5():
    """TC-206 Mã giao dịch không được trùng; Status chỉ nhận 1 đến 5 (0 và 6 bị từ chối). Chạy trong giao dịch SQL có ROLLBACK.
    Mỗi giao dịch thử dùng một hóa đơn riêng để không đụng ràng buộc một giao dịch đang mở trên mỗi hóa đơn."""
    require_db()
    steps = [("first_ok", invoice_sql("@a1") + transaction_sql("@a1", "PAY-20261025-000901", 1, "a")),
             ("duplicate", invoice_sql("@a2") + transaction_sql("@a2", "PAY-20261025-000901", 1, "b"))]
    for n in range(0, 7):
        steps.append((f"status_{n}", invoice_sql(f"@s{n}") + transaction_sql(f"@s{n}", f"PAY-20261025-0009{n + 10}", n, f"s{n}")))
    res = db.sql_check_steps(steps=steps, setup_sql=DB_SETUP)
    assert res.get("first_ok") == "OK", f"Giao dịch đầu bị từ chối: {res.get('first_ok')}"
    assert res.get("duplicate", "OK").startswith("ERR"), "Mã giao dịch trùng vẫn được nhận"
    wrong = [f"status {n}: {res.get(f'status_{n}')}" for n in range(1, 6) if res.get(f"status_{n}") != "OK"]
    wrong += [f"status {n} được nhận" for n in (0, 6) if res.get(f"status_{n}") == "OK"]
    assert not wrong, "; ".join(wrong)
