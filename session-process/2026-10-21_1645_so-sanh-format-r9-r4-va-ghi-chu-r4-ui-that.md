# So sánh format R9 với R4 và ghi chú chuyển R4 sang UI thật

Ngày: 2026-10-21 16:45.

## 1. Intro
Sau khi anh dặn không đụng tới deploy nữa, Claude quay lại automation R9. Anh hỏi script R9 đã có format chưa, rồi làm rõ là muốn so format hiện tại của R9 với R4. Sau đó anh nhắc lần chạy R4 hôm trước đo trên giao diện giả (prototype) chứ không phải UI thật và hỏi sửa ra sao. Claude trả lời cách sửa, anh dặn ghi lại để sửa sau khi localhost chạy được. Phiên này không sửa file script nào của R4 hay R9.

## 2. Architecture
Hai bộ automation trong roles\qa: r4_automation (chạy trên https://edusave.vercel.app) và r9_automation (chạy trên e-service localhost 5174). UI thật của R4 nằm ở admin portal (5173) của roles\dev\code\edufams-frontend, nhưng ở develop mục FAS application management chỉ là trang Coming soon.

## 3. Files modified
- CLAUDE.md: thêm một dòng Session Log, trạng thái STILL. Số dòng không ghim vẫn là 4 dòng PASS nên không xoay vòng.
- what i know about these/qa.md: thêm mục 16.
- what i know about these/README.md: ghi cập nhật lần 9 và sửa dòng qa.md trong bảng.

Các vòng làm việc, nguyên nhân rồi kết quả:
(1) Anh hỏi "format" của R9. Claude đọc là định dạng code, chạy ruff trên bản đã giao: 21 trên 26 file chưa theo chuẩn ruff format, 180 dòng dài hơn 120 ký tự, 3 import không dùng, 1 import chưa sắp xếp. Anh làm rõ là muốn so với R4, nên Claude so cấu trúc, cấu hình, tên test, docstring, marker, ngôn ngữ, độ dài dòng. Kết quả ở mục Phát hiện bên dưới.
(2) Anh hỏi sửa R4 ra sao khi đã chạy trên giao diện giả. Claude đọc junit.xml, README, conftest, rồi tìm UI thật trong git của edufams-frontend và các endpoint của FASService.

## 4. Files added
- roles/qa/r4_automation/docs/REAL_UI_RETARGET.md: ghi chú tiếng Việt về việc chuyển R4 sang UI thật, gồm kết quả lần chạy 20/10, bảng UI thật có đến đâu, 5 việc cần sửa, điều kiện bắt đầu, phần chưa kiểm.
- session-process/2026-10-21_1645_so-sanh-format-r9-r4-va-ghi-chu-r4-ui-that.md: file này.
Ruff cài trong môi trường của Claude bằng pip để kiểm, không nằm trong project.

## 5. Files deleted
Không có.

## 6. Skills used
- qa-course:working-protocol: bắt buộc cho mọi task trong project. Dùng để làm task list, ghi Session Log, session-process và cập nhật bản đồ role.
Không dùng skill khác. Ruff, openpyxl, git, grep dùng như công cụ.

## 7. External references
Không tra cứu web. Nguồn là roles\qa\r4_automation (README, conftest, pytest.ini, artifacts\reports\junit.xml), roles\qa\r9_automation, roles\qa\R4_Test_Cases.xlsx và R9_Test_Cases.xlsx (tiêu đề case), git của edufams-frontend và edufams-backend trong roles\dev\code.

## Phát hiện: format R9 so với R4
Giống nhau: cấu trúc thư mục, addopts của pytest.ini, requirements, runner .cmd CRLF, bảng phủ sinh tự động, mỗi test một mã TC kèm docstring.
Khác nhau:
Ngôn ngữ. R4 dùng tiếng Anh cho comment, docstring, marker và README. R9 dùng tiếng Việt, 170 trên 188 dòng comment và docstring. Docstring R9 do Claude dịch, trong khi tiêu đề trong R9_Test_Cases.xlsx là tiếng Anh, còn R4 chép đúng tiêu đề workbook, nên R9 khó tra ngược sang workbook.
Marker và file. R4 có một marker và một file test cho mỗi suite F4.1 đến F4.20 (21 file). R9 có 6 marker f91 đến f97 và 8 file, trong khi workbook R9 có 10 suite.
Test gộp. R9 có test gộp nhiều case như test_tc_004_tc_005, R4 hầu như một test một case.
Độ dài dòng. R4 có 55 trên 4123 dòng dài hơn 120 ký tự, dài nhất 177. R9 có 180 trên 2479 dòng, dài nhất 243.
Formatter. Cả hai chưa có file cấu hình format.
Khác có chủ ý: R9 thêm marker loại (readonly, mocked, api, mutating, online, destructive, extra), cờ môi trường, data\mocks.py, reset_payment_data.sql và README dài hơn, vì R9 ghi dữ liệu thật.

## Còn mở
- Anh chưa quyết có chỉnh R9 cho khớp R4 không. Đề xuất của Claude: đổi docstring về đúng tiêu đề workbook tiếng Anh, tách test gộp, chạy ruff format với dòng tối đa 120, rồi chạy lại bản giả lập để chắc kết quả không đổi. README và comment giữ tiếng Việt.
- R4 chuyển sang UI thật: để sau, xem roles\qa\r4_automation\docs\REAL_UI_RETARGET.md.
- Chưa phân tích 25 mục fail của lần chạy R4 ngày 20/10.
