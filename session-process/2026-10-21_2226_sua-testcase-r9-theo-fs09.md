# Sửa test case R9 theo FS 09

Ngày: 2026-10-21 22:26.

## 1. Intro
Anh yêu cầu sửa lại test case R9 cho đúng test data, tiền điều kiện và hậu điều kiện khi so với FS 09. Claude đọc toàn bộ roles\ba\[Agile] FS 09.docx (ngày 14/10/2026), rồi rà 162 case trong R9_Test_Cases_notes.xlsx và tạo bản mới R9_Test_Cases_rev_FS09.xlsx. Hai file gốc không bị sửa.

## 2. Architecture
FS 09 dùng mô hình invoice: ba lựa chọn EA, Online, Split; quy tắc BR-F9-02 cho EA và split; mục 3.1.1 có bốn nhóm hậu điều kiện (thành công, thất bại hoặc hủy, đang chờ, cần đối soát tay); Appendix A là bảng trạng thái. Workbook R9 có các sheet Test cases (tên có dấu cách cuối), Defect Reports, Summary, Scenarios, Assumptions, Questions, FS Trace, Seed Data. Mẫu không có cột hậu điều kiện riêng nên hậu điều kiện nằm trong Expected Result. Các công thức Summary và Scenarios đếm trên vùng cố định đến hàng 163, nên khi thêm case phải mở rộng vùng này.

## 3. Files modified
Không sửa file nào có sẵn. Bản mới sinh từ R9_Test_Cases_notes.xlsx.

Các vòng làm việc, nguyên nhân rồi kết quả:
(1) Đọc FS 09 và dump 162 case. Script đầu lỗi vì tên sheet Test cases có dấu cách cuối, đổi sang lấy sheet đầu tiên và so tên đã cắt khoảng trắng.
(2) Rà từng case với FS: thiếu hậu điều kiện, thiếu tiền điều kiện (Parent đã đăng nhập và liên kết, invoice Issued, giao dịch Pending), thiếu test data (idempotency key, số tiền invoice và callback), vài chỗ sai trạng thái.
(3) Sinh bản mới bằng openpyxl, chỉ sửa cột Preconditions, Test Data, Expected Result, Note của 85 case, cộng Summary A1, A3, A66, A79 và Seed Data D88. Mỗi case sửa có dòng Note bắt đầu bằng Rev 21/10 đối chiếu FS 09.
(4) Cờ nhầm: TC-103 chỉ đổi tiền điều kiện mà bị đánh dấu Actual Result cũ. Sửa để chỉ gắn cờ khi Expected đổi. Kết quả 13 case có Actual Result cũ cần đối chiếu lại.
(5) Kiểm bằng LibreOffice tính lại: 0 lỗi công thức, tổng vẫn 162 case, 26 scenario, Not Run 149, Passed 5, Failed 8. Kiểm số tiền invoice, mã học sinh, mã phụ huynh, số dư với sheet Seed Data: không lệch (TC-015 ghi số dư 410.00 là sau khi trả 90.00 từ 500.00, khớp).
(6) Viết ghi chú thay đổi R9_Test_Cases_rev_FS09_changes.md.
(7) Anh dặn nếu FS 09 chưa được phủ thì thêm case. Sheet FS Trace báo đủ 84 mục FS đều có case, nên đọc lại FS 09 từng câu và đối chiếu 162 case: tìm ra 10 chỗ có quy tắc rõ mà chưa có case kiểm đúng quy tắc. Viết TC-163 đến TC-172 ở cuối sheet (giữ nguyên ID cũ vì Defect Reports và automation dùng ID đó), thêm ASM-R9-33 đến 35 kèm 3 câu hỏi, mở rộng vùng công thức đến hàng 173, mở rộng danh sách chọn và tô màu, thêm ID case mới vào 23 mục FS Trace và vào cột case của ASM-R9-02 và ENV-R9-01 đến 06.
(8) Tự rà thấy TC-172 đặt invoice Issued kèm transaction Pending, trái Appendix A (invoice có transaction mở phải là PaymentPending). Sửa tiền điều kiện thành PaymentPending rồi đổi kết quả mong đợi cho khớp. Tính lại bằng LibreOffice: 0 lỗi, 172 case, Not Run 159, Approve 111, Draft 60, Block 1; 162 case cũ không đổi ô nào.

## 4. Files added
roles/qa/R9_Test_Cases_rev_FS09.xlsx: workbook R9 đã sửa theo FS 09, thêm 10 case mới ở vòng (7). 
roles/qa/R9_Test_Cases_rev_FS09_changes.md: ghi chú thay đổi theo nhóm, danh sách case, điểm FS còn mâu thuẫn.
session-process/2026-10-21_2226_sua-testcase-r9-theo-fs09.md: file này.

## 5. Files deleted
Không có. Thư mục tạm r9work trong máy ảo của Claude đã xóa.

## 6. Skills used
qa-course:working-protocol: bắt buộc cho mọi task trong project, dùng để ghi Session Log, session-process và cập nhật bản đồ role.
anthropic-skills:xlsx: sửa workbook bằng openpyxl, giữ định dạng và công thức, tính lại bằng LibreOffice để kiểm lỗi.

## 7. External references
Không tra cứu web. Nguồn là roles\ba\[Agile] FS 09.docx, R9_Test_Cases_notes.xlsx, F9_Dev_Local_Run_Results.md và mẫu groundtruth\Templates.xlsx.

## Còn mở
Ba assumption mới chờ trả lời: ASM-R9-33 (BA: nhãn SCR-01 của con chỉ có invoice PaymentPending), ASM-R9-34 (Dev: trường nào bị khóa sau khi invoice Issued), ASM-R9-35 (Dev: làm gì khi RowVersion cũ). Case API SPLIT với phần EA khác số dư chưa thêm vì phụ thuộc hoàn toàn ASM-R9-01. FS còn mâu thuẫn cần BA: phần EA có nhập được không, split khi số dư đã đủ, trạng thái SCR-02, lỗi gõ ở Step 4 và Appendix C. Dòng Expected của TC-107 và TC-128 về số dư EA 0.00 khi hoàn EA lỗi là suy luận từ EX-13 và Appendix A. Giao diện thật của Dev dùng mô hình charge, khác invoice của FS. Bộ automation r9_automation sinh từ R9_Test_Cases.xlsx, chưa đọc workbook rev này, nên 10 case mới chưa có test tự động.
