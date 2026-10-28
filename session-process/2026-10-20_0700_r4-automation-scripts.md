# Viết automation script cho R4

Ngày: 2026-10-20 07:00.

## 1. Intro
Anh yêu cầu "tạo automation testing scripts" sau khi bộ test case R4 xong. Claude hiểu theo mẫu ui_automation_project trong tài liệu tham khảo của project: Python, Pytest, Playwright, Page Object Model, báo cáo HTML và JUnit. Đây là cách hiểu của Claude, anh chưa xác nhận từng chữ. Khi Claude hỏi chạy thế nào, anh trả lời "đừng chạy edu save trên claude mở chrome mà chạy". Claude hiểu: không chạy prototype trong môi trường của Claude, bộ script phải chạy bằng Chrome thật trên máy anh. Claude chỉ dùng Chrome thật để đọc DOM.

## 2. Architecture
R4_Test_Cases.xlsx (267 case) -> data/not_automated.py và docs/COVERAGE.md (sinh bằng tools/build_coverage.py) -> tests (mỗi suite F4.x một file, mỗi case một hàm test_tc_NNN) -> pages (page object) -> prototype https://edusave.vercel.app/.
Prototype chạy hoàn toàn phía client, trạng thái nằm trong bộ nhớ. Context trình duyệt mới tương đương nút Reset data, nên mỗi test độc lập. Phiên MOE HQ giữ qua các lần chuyển view, phiên School thì không. Ngày mẫu cố định 18/10/2026.

## 3. Files modified
Không sửa file nào có sẵn trong project, ngoài các file sổ sách:
- CLAUDE.md: thêm một dòng Session Log (STILL, chờ anh chạy). Không phải xoay vòng vì số dòng không ghim vẫn là 4.
- what i know about these/qa.md: thêm mục 12 cho thư mục r4_automation, ghi ngày cập nhật.
- what i know about these/README.md: ghi cập nhật lần 5 và thêm thư mục mới vào bảng role qa.
Trong lúc viết script có nhiều vòng sửa file của chính thư mục r4_automation, ghi ở mục 4.

## 4. Files added
Thư mục roles/qa/r4_automation, 42 file.
- requirements.txt, pytest.ini, .gitignore, run_r4_automation.cmd, README.md: cấu hình và runner. Runner dùng .venv, cài requirements, chạy pytest với --browser-channel chrome và mở report.html. Chế độ smoke, all, suite N, tc NNN, draft, defects, thêm headed để xem trình duyệt.
- conftest.py: fixture portal, hq, hq_apps, hq_schemes, bvp, bvp_apps, bvp_schemes, mrs, hq_closed, bvp_apps_after_close. Hook đổi marker known_defect thành xfail không strict. Cỡ cửa sổ 1440 x 900, ngôn ngữ en-SG, múi giờ Asia/Singapore.
- data/ui_text.py, data/seed.py, data/not_automated.py: chữ trên giao diện, dữ liệu seed của prototype, danh sách 68 case bỏ qua kèm lý do (file sinh tự động).
- pages/base_page.py, portal.py, applications_page.py, review_drawer.py, dialogs.py, schemes_page.py, flows.py: page object và các luồng dùng chung. Thứ tự locator: role, label, text, placeholder, CSS ổn định. Không dùng sleep, chờ bằng expect.
- tests/: test_00_smoke.py, 19 file suite F4.1 đến F4.20 (không có F4.18 vì 4 case cần bản build) và test_not_automated.py (skip có tham số từ danh sách bỏ qua).
- tools/build_coverage.py, docs/COVERAGE.md: đọc R4_Test_Cases.xlsx, đối chiếu id case với tên hàm test, sinh bảng phủ. Lý do có tool: để bảng phủ không lệch với code.
Kết quả phủ: 199 trên 267 case có test, 222 mục chạy. 68 case bỏ qua: 51 cần bản build F4 có API, 16 cần seed SEED-R4-N1 đến N12, N23, N25 mà trạng thái gốc không có, 1 case Block.
Các vòng sửa và lỗi gặp khi viết (nguyên nhân rồi cách sửa):
(1) Locator lọc kiểu filter(has=...) dùng locator con nối từ locator cha nên history() của drawer trả về rỗng. Sửa bằng locator con gốc từ page. Bản DOM giả lập bắt được lỗi này.
(2) date_text("Form closes") khớp hai label vì gợi ý của Effective from có chữ Form closes. Sửa bằng field(label) neo bằng regex, TC-181 dùng hàm mới.
(3) TC-080 lấy sai chỉ số option, TC-134 gọi sai hàm, TC-128 có đường vòng khó đọc. Viết lại.
(4) AddFeeDialog tìm dòng theo thẻ strong, đổi sang has_text. Dọn import thừa và đoạn mã tạm.
(5) Một số lỗi của chính bản giả lập (history của drawer thứ hai, dữ liệu tĩnh của drawer, trạng thái select, header export, bộ lọc tier, đăng nhập MRS, nút demo) không phải lỗi script, đã sửa bản giả lập hoặc bỏ qua.
(6) Công cụ Chrome: chặn đầu ra dạng key:value, hàm async trả về {}, điều hướng khi đang đợi. Tách thành các lệnh riêng.
(7) Lệnh pkill -f trong cùng shell tự dừng shell (mã thoát 144). Lần sau dừng server theo PID.
Cách kiểm: pyflakes sạch, pytest --collect-only ra 290 mục, chạy một phần trên bản DOM giả lập (F4.5 pass 26 xfail 3, F4.3 và F4.7 phần lớn pass). Chưa chạy trên prototype thật. Bản giả lập và thư mục tạm không nằm trong project.
Chép sang máy anh bằng công cụ chép file, 42 file, kích thước khớp bản gốc, run_r4_automation.cmd giữ CRLF.

## 5. Files deleted
Không có.

## 6. Skills used
- qa-course:working-protocol: bắt buộc cho mọi task trong project này. Dùng để làm task list, ghi Session Log và cập nhật bản đồ role.
- anthropic-skills:chrome-browser: đọc DOM của prototype trong Chrome thật theo yêu cầu của anh, tạo tab mới, không dùng lại tab cũ.
Không dùng skill khác. Playwright, pytest, openpyxl và pyflakes dùng như công cụ.

## 7. External references
- https://edusave.vercel.app/ : prototype UI của F4. Chọn vì là giao diện duy nhất của R4. Chỉ đọc DOM bằng Chrome thật vì máy của Claude bị proxy chặn, không đi đường vòng.
- Không tra cứu web khác. Mẫu cấu trúc lấy từ ui_automation_project có sẵn trong project (tài liệu chỉ mang tính tham khảo).

## Còn mở
Anh chạy run_r4_automation.cmd (smoke trước, rồi all) và gửi artifacts/reports/junit.xml hoặc report.html. Sau đó sửa locator và thời gian chờ, gỡ known_defect khi xpass. Mục draft chờ BA trả lời 24 assumption. 51 case chờ bản build F4. Hai chỗ case mâu thuẫn cần anh quyết: TC-219 đến 221 về ngày, TC-173 với TC-264.
