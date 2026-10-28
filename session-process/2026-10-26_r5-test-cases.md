# Test case Function 5 (R5), 2026-10-26

## 1. Giới thiệu
Anh yêu cầu bắt đầu build test case cho F5, giữa chừng báo đã cập nhật Product Backlog trong role po. Sản phẩm là workbook R5_Test_Cases.xlsx theo mẫu R4 (8 sheet), căn cứ FS05 v1.2 và R5_FAS_Validation_Rules.docx.

## 2. Kiến trúc
Function 5 Đơn giấy (Paper Applications), Admin Portal, School user. Phủ danh sách Upload applications, hộp thoại Upload scans, màn Review application Part 1 đến Part 5, kiểm tra khi Review and submit, hộp thoại Review before submitting, nộp và phân luồng sang F4, xem và sửa đơn Pending, quyền truy cập và quy tắc máy chủ.

## 3. File đã sửa
CLAUDE.md: thêm một dòng Session Log (CRLF). Chưa xoay vòng dòng cũ, giữ như phiên trước.
Vòng sửa trong lúc dựng: (a) Product Backlog V2 thay PB-20 bằng US-042 và US-043, cột Traceability đổi theo mã mới. (b) Case thành viên không có dữ liệu thu nhập từng đặt Block trong khi ASM-R5-11 đã có giả định tính 0, kiểm tra tự động phát hiện, đổi sang Draft với kết quả theo ASM-R5-11. (c) Ba quy tắc VR-F5-S06, S08, S11 chưa có case nào trích dẫn, thêm mã vào Traceability của các case tương ứng. (d) Độ rộng cột Expected Result bị đọc sai do mẫu R4 gộp hai cột M và N cùng độ rộng, đặt lại 52.

## 4. File thêm
roles/qa/R5_Test_Cases.xlsx: 261 case, 52 scenario, 12 suite, 29 assumption và 7 mục môi trường, 29 câu hỏi, 65 mục FS Trace, Seed Data SEED-R5. Review 107 Approve, 150 Draft, 4 Block. Execution Status đều Not Run.
session-process/2026-10-26_r5-test-cases.md (file này).

## 5. File xóa
Không có. R4_Test_Cases.xlsx đang mở trong Excel nên chỉ đọc, không ghi.

## 6. Skill dùng
Không nạp skill. Workbook dựng bằng openpyxl theo kiểu dáng đọc từ R4_Test_Cases.xlsx, kiểm tra công thức bằng LibreOffice (0 lỗi), chữ cái kiểm tra NRIC theo thuật toán công khai cho dữ liệu SEED-R5.

## 7. Tham chiếu ngoài
Không dùng nguồn web. Căn cứ: FS05.md, R5_FAS_Validation_Rules.docx, Product Backlog V2.xlsm (US-042, US-043, US-049, US-050), R4_Test_Cases.xlsx (mẫu). Không chạy prototype trong Claude.

## Điểm suy luận và còn mở
Điểm mới O29 (ASM-R5-29): "đã có đơn trong năm nay" tính theo ngày nộp, năm scheme hay năm Application ID, chưa có trong tài liệu validation (28 điểm O1 đến O28). 4 case Block chờ ASM-R5-03 (NRIC người khai không tra ra), ASM-R5-07 (grade ngoài danh sách), ASM-R5-19 (School-based FAS là No với con không đủ điều kiện quốc tịch, US-050 chưa đủ để kết luận), ASM-R5-29. Backlog xếp US-042 và US-043 dưới nhóm R4 Financial Assistance trong khi yêu cầu thầu là R5, cần PO xác nhận. Seed SEED-R5 và các ngày biên (18/10/2019, 19/10/2019, 18/10/2009, 19/10/2009) là QA đề xuất, Dev cần nạp. Ba NRIC mẫu trong hình FS không đạt thuật toán nên ASM-R5-06 chỉ kiểm cấu trúc. Case hình FS ghi Note khi hình khác chữ (Phone number tô vàng, One application is one student). Workbook viết tiếng Việt, tên cột giữ tiếng Anh như mẫu. Chưa cập nhật artifact cây yêu cầu cho mapping backlog mới.
