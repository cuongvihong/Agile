"""Tạo data/not_automated.py và docs/COVERAGE.md từ sổ test case R9 và các file test.

Cách dùng: python tools/build_coverage.py duong_dan/R9_Test_Cases_final_FS09.xlsx [duong_dan/R9_Test_Cases_notes.xlsx]
Tham số thứ hai là sổ cũ trước khi sửa theo FS 09. Có nó thì COVERAGE.md thêm mục "case đã đổi ở bản rev và việc đã làm".
Sổ test case chỉ được đọc. Một case được tính là đã tự động hóa khi tên một hàm test bắt đầu bằng test_tc_NNN
(hoặc chứa nhiều mã như test_tc_004_tc_005_...). Case chưa tự động hóa phải có lý do trong REASONS bên dưới.
"""
from __future__ import annotations

import ast
import collections
import re
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent

G_DB = "Kiểm ràng buộc cơ sở dữ liệu (CHECK, UNIQUE, khóa ngoại, nhật ký). Cần truy cập SQL Server của QA, viết thành kịch bản SQL riêng, không thuộc bộ UI."
G_MODEL = "Mô hình hóa đơn của R9 không có trong UI thật: UI liệt kê khoản phí (charge), không có hóa đơn, dòng theo loại phí, GST hay trạng thái hóa đơn trước khi thanh toán (ASM-R9-UI-01)."
G_NOSPLIT = "UI không có ô nhập phần Education Account (phần chia do hệ thống tự tính, ASM-R9-UI-03) và API checkout không nhận số tiền từng phần, nên không có gì để thử."
G_FAULT = "Cần tiêm lỗi vào Function 1, cổng thanh toán hoặc hạ tầng (ngắt kết nối, hết hạn phiên, timeout, hoàn tiền lỗi). Simulator chỉ có hai nút Pay successful và Pay failed."
G_WEBHOOK = "Thuộc F9.6: cần gọi webhook có chữ ký của nhà cung cấp, đọc bảng webhook hoặc chạy job đối soát. Ngoài phạm vi kiểm thử qua giao diện."
G_PERSONA = "Cần phụ huynh thứ hai hoặc kịch bản đăng nhập thất bại hoặc bị hủy trên MockPass. Dữ liệu mẫu hiện chỉ map một persona (S7890123F)."

REASONS: dict[str, str] = {
    "TC-175": "UI không hiện ngày sinh hay tuổi của con và chưa có quy tắc 'từ 16 tuổi không có nút Pay' (quy tắc R8, điểm mở O22 trong tài liệu validation rules). Không có dữ liệu để kiểm, làm lại khi FS chốt quy tắc.",
    "TC-204": "Cần cách làm hỏng xử lý một callback hợp lệ để đọc thông báo lỗi được lưu (ENV-R9-05), Dev chưa cung cấp. Ngoài phạm vi kiểm thử qua giao diện và API.",
}
# Các case còn lại của R9_Test_Cases_final_FS09.xlsx (187 case) đều có ít nhất một test; một số test chỉ kiểm được một phần case, phần còn lại ghi trong docstring.


def load_cases(xlsx: str) -> list[dict]:
    sheet = openpyxl.load_workbook(xlsx, data_only=True).worksheets[0]
    cases = []
    for row in sheet.iter_rows(values_only=True):
        if row[0] and str(row[0]).startswith("TC-"):
            cases.append(dict(id=str(row[0]), title=str(row[2]).replace("\n", " "), suite=str(row[3]).replace("\n", " "),
                              page=str(row[4] or ""), assumption=str(row[15] or ""),
                              severity=str(row[5] or ""), review=str(row[19] or ""),
                              pre=str(row[10] or ""), data=str(row[11] or ""), expected=str(row[13] or ""),
                              priority=str(row[6] or ""), env=str(row[9] or ""), steps=str(row[12] or "")))
    return cases


A_NONE = "Thêm assert_nothing_created: không có POST /checkout, danh sách khoản và số dư EA giữ nguyên."
A_API = "Test mutating đọc thêm transaction, leg và invoice qua API (assert_backend_state)."
REV_ACTION = {
    "TC-015": "Không đổi test. API dùng mã lạ nên không có giao dịch TXN-B1 của gia đình khác; phần 'TXN-B1 vẫn Succeeded' cần phụ huynh thứ hai.",
    "TC-035": A_NONE, "TC-036": A_NONE, "TC-040": A_NONE + " Thêm bản ví giả lập 0.00 vì dữ liệu thật không có con ví 0 còn khoản phí.",
    "TC-041": A_NONE, "TC-043": A_NONE, "TC-050": A_NONE, "TC-100": A_NONE,
    "TC-042": A_NONE + " (ví giả lập, nên chỉ so danh sách khoản)",
    "TC-038": "Thêm kiểm tra không có POST /checkout. Trang bị lỗi ví chặn nên không đọc lại danh sách.",
    "TC-039": A_NONE + " (ví giả lập, nên chỉ so danh sách khoản)",
    "TC-063": "Thêm test màn xem lại EA chưa trừ gì (assert_nothing_created). Test known_defect về số dư sau thanh toán giữ nguyên.",
    "TC-067": A_API + " Thêm dòng nguồn tiền EA Succeeded, Invoice status Paid và số dòng 1, 2.",
    "TC-070": A_API, "TC-077": A_API + " Thêm tiêu đề Payment successful và Invoice status Paid.",
    "TC-078": A_API, "TC-080": A_API,
    "TC-081": "Thêm test mutating trên khoản thật: khóa sai bị từ chối, khoản còn nợ, số dư EA không đổi. Test dùng mã lạ giữ nguyên.",
    "TC-084": "Thêm kiểm tra tab sau không lưu mã giao dịch thứ hai, khoản đã trả không quay lại danh sách, số dư không đổi.",
    "TC-087": "Thêm kiểm tra màn xem lại chưa gửi POST /checkout. " + A_API,
    "TC-089": A_API + " Chỉ có leg online, không có leg EA.",
    "TC-101": "Thêm kiểm tra hai dòng nguồn tiền: EA Succeeded và online Pending. Câu 'EA đã bị trừ' vẫn là known_defect.",
    "TC-103": A_API + " Mong đợi transaction Failed, leg EA Reversed, leg online Failed, invoice Issued.",
    "TC-125": "Test đổi tên chỉ còn TC-125 (TC-128 tách riêng). Thêm kiểm tra dòng nguồn tiền online Pending.",
    "TC-126": "Mock chuyển sang leg online Succeeded. Thêm kiểm tra dòng nguồn tiền và Invoice status Paid.",
    "TC-128": "Thêm hai test: trạng thái ReconciliationRequired không nói thất bại và không có Try again; câu 'EA đã bị trừ' là known_defect.",
    "TC-129": "Giữ test mocked. Thêm ghi chú: số dư EA 150.00 không hiện trên màn kết quả, kiểm ở TC-065.",
    "TC-130": "Thêm Invoice status Paid ở test mocked. " + A_API,
    "TC-136": A_API + " Việc invoice trở lại Issued kiểm ở test TC-090 và TC-139.",
    "TC-137": "Thêm test transaction Failed với leg EA Reversed (known_defect: UI chỉ có câu 'đã hoàn' khi ReconciliationRequired). Test cũ thành extra.",
    "TC-141": "Thêm kiểm tra leg EA giữ Succeeded, leg online Failed và không có POST /checkout mới.",
    "TC-142": "Không đổi test. Phiên đã hết hạn nên không đọc được invoice và số dư; test chỉ kiểm không có POST /checkout.",
}


def changed_cases(old_xlsx: str, new_cases: list[dict]) -> dict[str, list[str]]:
    """Case có Preconditions, Test Data hoặc Expected Result khác giữa sổ cũ và sổ rev."""
    old = {c["id"]: c for c in load_cases(old_xlsx)}
    names = {"pre": "Preconditions", "data": "Test Data", "expected": "Expected Result"}
    out: dict[str, list[str]] = {}
    for c in new_cases:
        before = old.get(c["id"])
        if before is None:
            continue
        diff = [label for key, label in names.items() if before[key] != c[key]]
        if diff:
            out[c["id"]] = diff
    return out


def automated_map() -> dict[str, list[str]]:
    """Mã TC -> danh sách 'file::tên hàm' trong tests/test_f*.py."""
    found: dict[str, list[str]] = collections.defaultdict(list)
    for path in sorted((ROOT / "tests").glob("test_f*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_tc_"):
                head = re.match(r"((?:test_)?(?:tc_\d{3}_?)+)", node.name).group(1)
                for number in re.findall(r"tc_(\d{3})", head):
                    found["TC-" + number].append(f"{path.name}::{node.name}")
    return found


def main(xlsx: str, old_xlsx: str | None = None) -> None:
    cases = load_cases(xlsx)
    done = automated_map()
    ids = {c["id"] for c in cases}
    unknown = sorted(set(done) - ids)
    if unknown:
        print("CẢNH BÁO: test nhắc tới mã không có trong sổ:", unknown)
    todo = [c for c in cases if c["id"] not in done]
    case_lines = [f'"""Tiêu đề, suite, severity, review status và nội dung (tiền điều kiện, dữ liệu, bước, kết quả mong đợi) của {len(cases)} case trong {Path(xlsx).name}. Tạo bởi tools/build_coverage.py, dùng cho reporting.py."""',
                  "from __future__ import annotations", "", "CASES = {"]
    for c in cases:
        meta = dict(title=c["title"], suite=c["suite"], page=c["page"], severity=c["severity"], review=c["review"],
                    assumption=c["assumption"][:200].replace("\n", " "), priority=c["priority"], env=c["env"],
                    preconditions=c["pre"], test_data=c["data"], steps=c["steps"], expected=c["expected"])
        case_lines.append(f'    "{c["id"]}": {meta!r},')
    case_lines += ["}", ""]
    (ROOT / "data" / "cases.py").write_text("\n".join(case_lines), encoding="utf-8")
    missing = [c["id"] for c in todo if c["id"] not in REASONS]
    both = sorted(i for i in REASONS if i in done)
    if missing:
        print("CẢNH BÁO: chưa có lý do cho", missing)
    if both:
        print("CẢNH BÁO: đã tự động hóa nhưng vẫn có lý do bỏ qua:", both)

    lines = [f'"""Các case của {Path(xlsx).name} mà chưa test nào tự động hóa, kèm lý do. Tạo bởi tools/build_coverage.py."""',
             "from __future__ import annotations", "", "NOT_AUTOMATED = {"]
    for c in todo:
        lines.append(f'    "{c["id"]}": {REASONS.get(c["id"], "Chưa phân loại")!r},')
    lines += ["}", ""]
    (ROOT / "data" / "not_automated.py").write_text("\n".join(lines), encoding="utf-8")

    by_suite: dict[str, list[dict]] = collections.OrderedDict()
    for c in cases:
        by_suite.setdefault(c["suite"], []).append(c)
    out = [f"# Độ phủ của {Path(xlsx).name}", "",
           f"Số case trong sổ: {len(cases)}. Đã tự động hóa: {len(cases) - len(todo)}. Chưa tự động hóa: {len(todo)}.", "",
           "Một case tính là đã tự động hóa khi có ít nhất một test chạy được cho nó, kể cả test nhãn `known_defect` (kỳ vọng thất bại vì bản build lệch với R9),",
           "`mocked` (giả phản hồi), `mutating` (ghi dữ liệu thật) và `draft` (phụ thuộc giả định). Xem README để biết ý nghĩa từng nhãn.", "",
           "| Suite | Số case | Đã tự động hóa | Chưa |", "|---|---|---|---|"]
    for suite, items in by_suite.items():
        n_done = sum(1 for c in items if c["id"] in done)
        out.append(f"| {suite} | {len(items)} | {n_done} | {len(items) - n_done} |")
    out += ["", "## Case đã tự động hóa", "", "| Case | Tiêu đề | Test |", "|---|---|---|"]
    for c in cases:
        if c["id"] in done:
            out.append(f'| {c["id"]} | {c["title"]} | {"<br>".join(done[c["id"]])} |')
    out += ["", "## Case chưa tự động hóa", "", "| Case | Tiêu đề | Lý do |", "|---|---|---|"]
    for c in todo:
        out.append(f'| {c["id"]} | {c["title"]} | {REASONS.get(c["id"], "Chưa phân loại")} |')
    if old_xlsx:
        changed = changed_cases(old_xlsx, cases)
        automated_changed = [i for i in changed if i in done]
        out += ["", "## Case tự động hóa mà bản rev FS09 đã đổi", "",
                f"Bản rev đổi Preconditions, Test Data hoặc Expected Result của {len(changed)} case cũ, trong đó {len(automated_changed)} case có test. "
                "Cột cuối ghi việc đã làm ở test. Các hậu điều kiện về nhật ký, bảng ledger và số dư trên hệ thống ngoài e-service "
                "không có trên UI nên chưa kiểm.", "",
                "| Case | Phần đã đổi | Việc đã làm ở test |", "|---|---|---|"]
        for case_id in automated_changed:
            out.append(f'| {case_id} | {", ".join(changed[case_id])} | {REV_ACTION.get(case_id, "CHƯA XỬ LÝ")} |')
        unhandled = [i for i in automated_changed if i not in REV_ACTION]
        if unhandled:
            print("CẢNH BÁO: case đổi ở bản rev mà chưa ghi việc đã làm:", unhandled)
        not_changed_but_listed = [i for i in REV_ACTION if i not in changed]
        if not_changed_but_listed:
            print("Ghi chú: REV_ACTION có case không đổi nội dung ở sổ rev:", not_changed_but_listed)
        out += ["", "Các case chưa có test và đã đổi ở bản rev: " + (", ".join(i for i in changed if i not in done) or "không có") + ".", ""]
    (ROOT / "docs" / "COVERAGE.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"đã tự động hóa {len(cases) - len(todo)} / {len(cases)}; đã ghi data/cases.py, data/not_automated.py và docs/COVERAGE.md")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
