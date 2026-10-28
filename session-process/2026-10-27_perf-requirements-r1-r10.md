# Mở rộng performance requirements lên R1 đến R10, 2026-10-27

## 1. Giới thiệu
Anh hỏi performance test case đã đủ dữ kiện để làm chưa, rồi yêu cầu bổ sung cho các function còn lại, function 1 đến 10. Tài liệu gốc roles/qalead/performance-requirements.docx (v0.5) chỉ phủ R1, R3, R8, R9. Claude đọc hết v0.5, đọc FS02, FS04, FS05, FS06, FS10, mục 2 giải thích 10 requirement, Product Backlog của PM (PB-14 đến PB-25) và V2 của PO, rồi nâng tài liệu lên v0.6 phủ thêm R2, R4, R5, R6, R7, R10.

## 2. Kiến trúc
Giữ nguyên cấu trúc và nhãn Fact, Derived, Assumption, Open của v0.5. Số mục cũ 2.1 đến 2.8, 3.1 đến 3.5, 4.1 đến 4.5 không đổi để các tham chiếu chéo không vỡ. Phần mới nối tiếp: 2.9 đến 2.14 (yêu cầu PR theo function), 2.15 (cơ cấu tải trong FAS window), 3.6 đến 3.11 (kịch bản CS), 4.6 đến 4.11 (tiêu chí ra X). Các mục Common, Stress, Suspension cũ đổi số thành 4.12 đến 4.14 (không có nơi nào tham chiếu theo số này, đã kiểm).

## 3. File đã sửa
roles/qalead/performance-requirements.docx: sửa tại chỗ, v0.5 thành v0.6, 328 mã không trùng, mọi tham chiếu PR, CS, X, A, E đều có định nghĩa, 40 trang. Thêm 6 mục yêu cầu (tổng 66 dòng PR mới), 44 kịch bản CS mới (35 theo function và 9 CS-P, CS-E, CS-L2, CS-V, CS-B), 56 tiêu chí ra mới, 15 dòng ngưỡng, 12 tham số, E9 và E10, Open Question 20 đến 29, Assumption A-20 đến A-27, thêm nguồn và tham chiếu, câu Out of scope viết lại, câu Suspension bổ sung.
roles/qalead/test-plan-final-v1.0.docx: mục 3.9, câu phạm vi đổi từ R1, R3, R8, R9 thành R1 đến R10 và thêm scan reading, income lookup vào phần mô phỏng.
CLAUDE.md: thêm một dòng Session Log (CRLF).

## 4. File thêm
session-process/2026-10-27_perf-requirements-r1-r10.md (file này).

## 5. File xóa
Không có. Bản v0.5 được lưu tạm ngoài dự án trên máy để phòng lỗi, không nằm trong thư mục dự án.

## 6. Skill dùng
Không nạp skill. Dùng python-docx sao chép bảng mẫu của chính file (giữ định dạng), LibreOffice để dựng PDF kiểm tra bố cục. Không trích bài giảng khóa học trong tài liệu xuất.

## 7. Tham chiếu ngoài
Không dùng nguồn web. Căn cứ: FS02, FS04, FS05, FS06 (bản nháp), FS10, giai-thich/02-chi-tiet-10-requirement.md, pm/Product Backlog.xlsx (PB-14 đến PB-25, OQ-16), po/Product Backlog V2.xlsm (US-042, US-043), kết quả kiểm DataTest.zip ngày 27/10.

## Điểm suy luận và còn mở
Suy luận của QA, đều ghi là Assumption trong tài liệu: ngưỡng (10 phút cho batch và form close job, upload and read P95 10 giây), cơ cấu tải FAS window (65/15/10/3/2/5 cho phụ huynh, 25/33/25/17 cho HQ, 90/5/3/2 cho School), Level 1 cho 6 function mới, A tối thiểu 200 đơn, burst 20 phụ huynh trong 1 phút.
Còn mở (Open Question 20 đến 29): quy mô batch top-up, số đơn FAS mỗi năm, giới hạn export, email trong job và thanh toán trùng lúc áp subsidy, cut-off lúc form đóng, số tài liệu và số con trong đơn gia đình, định nghĩa số tiền đã dùng của R6, phạm vi R7 (PB-22), engine PB-25, đối chiếu PB với US.
Mâu thuẫn chưa xử lý: roles/qalead/test-strategy.md dòng 33 ghi Performance ngoài phạm vi 3 sprint, trong khi test plan §3.9 và tài liệu này có đo hiệu năng. Cần anh hoặc QA Lead quyết định rồi mới sửa test-strategy.
FS06 là bản nháp và R7 chưa có FS, nên R6 và R7 có độ tin cậy thấp hơn.
Chưa làm: Performance Test Plan theo template, script JMeter, mở rộng seed cho Level 1.
