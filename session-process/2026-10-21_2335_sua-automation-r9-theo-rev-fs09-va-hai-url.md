# Sửa automation R9 theo rev FS09 và hai URL

Ngày: 2026-10-21 23:35.

## 1. Intro
Anh yêu cầu sửa bộ automation R9 (roles\qa\r9_automation) dựa trên workbook mới R9_Test_Cases_rev_FS09.xlsx (172 case) và địa chỉ của hai trang: e-service và admin portal. Claude hiểu hai địa chỉ là e-service http://localhost:5174 và admin portal http://localhost:5173 (cả hai đang chạy, nhưng anh chưa xác nhận lại đây có đúng hai địa chỉ anh định nói không). Mục tiêu là để test, tiền điều kiện và hậu điều kiện trong code khớp với bản rev, và bộ test biết đến cả hai cổng.

## 2. Architecture
FS 09 viết theo hóa đơn (invoice), còn giao diện Dev thật chạy theo khoản phí (charge): chọn khoản ở /billing/:studentId, chọn phương thức, xem lại, rồi sang /payment-result, hóa đơn chỉ được tạo lúc checkout. Vì vậy phép ghép "invoice Issued = khoản còn trong danh sách nợ", "Paid = khoản biến mất và API invoice báo Paid", "không có transaction = không có POST /billing/v1/checkout" là suy luận của QA (ASM-R9-UI-01), không phải sự thật trong FS.
Hậu điều kiện được kiểm bằng API thật qua proxy /api của Vite: outstanding-charges, checkout (header Idempotency-Key), transactions/{id} (status, fundingSources theo sequenceNumber, method, status, invoiceId), invoices/{id} (status), wallet của edu-account. Gom vào một module mới pages/postconditions.py để các file test dùng chung.
Admin portal: trang /login (Welcome back, ô Username và Password). Form đòi tài khoản QA mà repo không có, và FS 09 là chức năng của phụ huynh nên không case nào cần quản trị. Bộ test chỉ kiểm hai thứ: trang /login mở được, và mở gốc khi chưa đăng nhập thì chuyển về /login.

## 3. Files modified
Vòng 1, xác nhận hệ thống thật: mở cả hai cổng trong khung trình duyệt của app Claude, đăng nhập MockPass bằng persona S7890123F (nút Sign in with Singpass trong khung không điều hướng, nên đặt state vào sessionStorage rồi đi thẳng MockPass và URL callback). Đi qua màn chọn khoản, chọn phương thức (Education Account, Online Gateway, Both chia 300.00 và 170.00), xem lại, kết quả. Đọc mã nguồn frontend để biết nhãn thật.
Vòng 2, dữ liệu: bộ dữ liệu hiện tại khác seed cũ (Test Child One 805.00, ví 300.00; Test Child Two 1390.00; Test Child Three 470.00; Tan Wei Ming 0 khoản, ví 0.00). Sửa pages/catalog.py để chọn con theo dữ liệu thay vì gắn tên: ea_child, split_child, zero_child, thêm zero_balance_child.
Vòng 3, hậu điều kiện: thêm assert_nothing_created, assert_backend_state vào các test F9.3, F9.4, F9.5, F9.7 theo 34 case đã đổi trong rev. Sửa lỗi tự gây: nhãn dt của dòng hóa đơn là "Line" chứ không phải "Line number" (tìm trong i18n resources.ts).
Vòng 4, case mới: TC-164 (lỗi hệ thống ở SCR-02) được tự động hóa dạng mocked, draft, known_defect. 9 case mới còn lại (TC-163, 165 đến 172) ghi lý do chưa tự động trong not_automated.
Vòng 5, sinh lại độ phủ: tools/build_coverage.py nhận workbook rev, bảng REV_ACTION, sinh lại data/not_automated.py (96 mục) và docs/COVERAGE.md (172 case, 76 tự động, 96 chưa).
Vòng 6, kiểm: cú pháp, pyflakes, pytest --collect-only đều qua (100 test chạy được và 96 test bỏ qua kèm lý do). Cố ý không chạy pytest vì máy ảo của Claude không truy cập được localhost của máy anh.
Sai sót đã sửa trong lúc làm: bản vá f93 đầu tiên lỗi vì lệch chữ ("khoản phí" so với "khoản"), assertion chặn nên chưa ghi gì, sửa chữ rồi chạy lại; comment trong run_r9_automation.cmd từng nói R9_EXPECTED_CHILDREN rỗng thì bỏ qua TC-006 (sai với cmd), sửa comment và README; README ghi 85 và 34 trong khi số đúng là 84 và 33, đã sửa.
File sửa trong roles\qa\r9_automation: data\seed.py (ADMIN_URL, biến R9_ADMIN_URL), conftest.py (fixture admin_url, thêm marker admin vào KIND_MARKERS), pytest.ini (marker admin), pages\catalog.py, pages\result_page.py (status_text, invoice_line_numbers, transaction_id), tests\test_00_smoke.py (hai test admin và một test hai cổng là hai origin khác nhau), test_f92, test_f93, test_f94, test_f95, test_f97, tools\build_coverage.py, data\not_automated.py, docs\COVERAGE.md, README.md, run_r9_automation.cmd (CRLF).

## 4. Files added
roles\qa\r9_automation\pages\admin_page.py: AdminLoginPage, cố ý không có hàm đăng nhập.
roles\qa\r9_automation\pages\postconditions.py: Snapshot, snapshot, assert_nothing_created, get_transaction, get_invoice, legs_by_method, assert_backend_state.
session-process\2026-10-21_2335_sua-automation-r9-theo-rev-fs09-va-hai-url.md: file này.

## 5. Files deleted
Không có.

## 6. Skills used
qa-course:working-protocol: ghi Session Log, session-process, cập nhật bản đồ role.
anthropic-skills:built-in-browser: mở e-service và admin portal trong khung trình duyệt của app Claude, đọc DOM thật.

## 7. External references
Không tra cứu web. Nguồn là R9_Test_Cases_rev_FS09.xlsx, roles\ba\[Agile] FS 09.docx, mã nguồn roles\dev\code\edugovernment-frontend (features/billing-payment, packages/i18n, apps/admin-portal) và hai địa chỉ localhost đang chạy.

## Còn mở
Pytest chưa chạy trên hệ thống thật. Anh chạy run_r9_automation.cmd (smoke trước, rồi read) và gửi artifacts\reports\junit.xml để sửa locator và gỡ known_defect khi xpass.
Ba test known_defect mới (TC-032 thiếu nút quay lại, TC-128, TC-137) và TC-164 đều suy ra từ mã nguồn, chưa thấy trên bản build. Cần xác nhận khi chạy.
13 Actual Result cũ cần chạy lại theo Expected mới: TC-063, 070, 087, 089, 098, 100, 107, 128, 129, 130, 136, 137, 141.
ASM-R9-33, 34, 35 chờ BA hoặc Dev. ASM-R9-UI-01 đến 04 là giả định của QA về ghép invoice với charge.
Quan sát chưa kiểm chứng: vào thẳng /education-accounts của admin portal khi chưa đăng nhập từng hiện "Unexpected Application Error ... reading 'trim' at AdminShell.tsx". Chưa tái hiện lại, không đưa vào defect.
Chưa làm theo thứ tự anh quyết: xác nhận sửa wallet.updated_at, chụp màn hình FS09, ghi chú lỗi cho Dev, chuyển R4 sang UI thật, tài liệu validation rule R9, automation R8.
