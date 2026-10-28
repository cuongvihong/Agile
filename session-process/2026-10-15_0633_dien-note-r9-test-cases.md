# Session process: điền cột Note của R9_Test_Cases.xlsx

Ngày 2026-10-15, kết thúc lúc 06:33 (giờ Việt Nam). Project: Agileproject, tag agileproject. Viết bằng tiếng Việt theo rule ngôn ngữ ngày 2026-10-14 trong CLAUDE.md.

## 1. Giới thiệu

Người dùng (Cường, QA Lead) yêu cầu điền cột Note (cột S) của roles\qa\R9_Test_Cases.xlsx cho các case anh chưa ghi, làm giống cách anh làm với TC-001 đến TC-007: xem Title, đối chiếu Traceability chỉ trong FS 09, và nếu Expected nhìn được trên UI thì kiểm trên UI mock https://eafams2-phi.vercel.app/ (test data khác nên không xét). Việc chạy kịch bản A đến G của Dev trên localhost được anh hoãn lại.

## 2. Kiến trúc

Không sửa code hay tài liệu của role khác. Task chỉ đọc FS 09 (roles\ba\[Agile] FS 09.docx) và 162 test case, chạy thử UI mock Eafams (trang Parent: Home, Education Account, Fees and Payments, sandbox thanh toán, Singpass mock chọn kịch bản, không cần mật khẩu), rồi ghi ghi chú vào cột S. Cách làm: trích FS 09 và workbook ra thư mục tạm của phiên, kiểm bằng script rằng mọi ID trong Traceability (DA, BR-F9, EX, AC, SCR, OQ, NQ, VAL, mã lỗi 5.1) có trong FS 09, đọc toàn bộ Title, Traceability và Expected, chạy UI mock bằng trình duyệt tích hợp (đọc cây trang, JavaScript đọc và nhập ô số tiền), soạn ghi chú, ghi bằng openpyxl vào bản sao.

## 3. File sửa

- CLAUDE.md: chỉ sửa Session Log, thêm một dòng cho task này và chuyển dòng cũ nhất không ghim ("Read CLAUDE.md under the working protocol and add the missing Learned Rules") sang sessionlog. Bốn dòng STILL ghim của ngày 2026-10-11 không đụng tới.
- sessionlog/agileproject.md: thêm nguyên văn dòng được chuyển, ở cuối bảng.
- roles/qa/R9_Test_Cases.xlsx: không sửa (file đang mở trong Excel, ghi đè sẽ thất bại và có thể mất thay đổi của anh).

## 4. File thêm

- roles/qa/R9_Test_Cases_notes.xlsx: bản sao của R9_Test_Cases.xlsx với cột S (Note) điền cho TC-008 đến TC-162. 155 ô đổi: 110 case có ghi chú riêng, 45 case ghi "xác nhận". 11 ô đã có ghi chú tiếng Anh được giữ và thêm dòng mới bên dưới. TC-001 đến TC-007 giữ nguyên ghi chú của anh. Đã mở lại file và so từng ô của cả 8 sheet với bản gốc: chỉ cột S của sheet "Test cases " khác; bảng, conditional formatting, data validation, ô gộp và công thức giữ nguyên.
- session-process/2026-10-15_0633_dien-note-r9-test-cases.md: file này.

## 5. File xóa

Không xóa file nào. Không commit hay push gì. Các file làm việc nằm trong thư mục tạm của phiên.

## 6. Skill dùng

- qa-course:working-protocol (đã gọi sớm trong phiên): quy tắc Session Log, xoay vòng dòng, evidence rule (nêu rõ phần chưa kiểm và phần suy luận).
Không dùng skill nào khác.

## 7. Tham chiếu ngoài

Không dùng nguồn bên ngoài project. Nguồn là FS 09 và UI mock Eafams mà anh chỉ định. Không nhập mật khẩu và không đụng trang admin: anh có đưa tài khoản admin, tôi không nhập vì không được nhập mật khẩu để đăng nhập; nếu cần xem trang admin thì anh tự đăng nhập trong trình duyệt và tôi chỉ đọc.

## Việc còn mở cho người dùng quyết

- Xem R9_Test_Cases_notes.xlsx rồi chép cột S sang file gốc (hoặc đóng Excel để tôi ghi đè).
- Điểm lệch cần BA hoặc Dev: nhãn trạng thái của mock (OVERDUE, AWAITING PAYMENT thay cho Issued và Pending, TC-018, 025, 026), câu EA_NOT_AVAILABLE nằm trong khung hồng (TC-038, ASM-R9-13), TC-076 kiểm hành vi Function 1 trong khi FS 09 mục 1.5 loại trừ, hai chỗ FS 09 khác nhau về việc Parent có được nhập phần EA khi chia đôi (Step 4 và AC-22).
- Một lỗi mock cần báo Dev: Refresh Status ở màn Payment In Progress đưa về trang chủ chưa đăng nhập.
- Chạy kịch bản A đến G của Dev trên localhost (đang hoãn); giữ hay bỏ f9qa-helper.ps1 và setup-function9.ps1 trong function9_14-10-26.
