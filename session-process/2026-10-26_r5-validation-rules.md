# Quy tắc validation cho Function 5 (R5), 2026-10-26

## 1. Giới thiệu
Anh yêu cầu đọc fs05, sau đó tham khảo các validate rule hiện có để cung cấp validate rule cho function này. Sản phẩm là tài liệu Word cho Dev và BA, theo mẫu của R4 và R9.

## 2. Kiến trúc
Function 5 Đơn giấy (Paper Applications), Admin Portal, School user. Gồm danh sách Upload applications, hộp thoại Upload scans, màn Review application (Part 1 đến Part 5), kiểm tra khi Review and submit, hộp thoại Review before submitting, xem và sửa đơn Pending. Chuyển đơn sang Function 4.

## 3. File đã sửa
CLAUDE.md: thêm một dòng Session Log. Chưa xoay vòng dòng cũ vì bảng hiện có nhiều dòng PASS và DONE cũ đã vượt 5 dòng từ các phiên trước, để anh quyết có dọn không.

## 4. File thêm
roles/qa/R5_FAS_Validation_Rules.docx: 30 trang, Times New Roman, tiêu đề 14, 13, 12, bảng Mục và Quy tắc, 5 hình có khung đỏ trùng mã trường. session-process/2026-10-26_r5-validation-rules.md (file này).

## 5. File xóa
Không có.

## 6. Skill dùng
Không nạp skill. Word dựng bằng python-docx, hình đánh dấu bằng PIL, kiểm layout bằng LibreOffice đổi sang PDF.

## 7. Tham chiếu ngoài
Không dùng nguồn web. Căn cứ: FS05.md, FS01.md (F01-BR02, F02), R4_FAS_Validation_Rules_EN.docx, R9_FAS_Validation_Rules.docx. Chữ cái kiểm tra NRIC theo thuật toán công khai (trọng số 2,7,6,5,4,3,2), tính độc lập cho ba NRIC trong hình.

## Điểm suy luận và còn mở
28 điểm mở O1 đến O28 trong mục 11 của tài liệu. Quan trọng nhất: O1 tuổi 7 đến 16 so với FS01, O2 mâu thuẫn một mẫu một con, O3 NRIC người khai không tra ra, O6 chữ cái kiểm tra NRIC, O9 con học trường khác, O20 School-based FAS là No với con không đủ điều kiện quốc tịch. Giá trị ngày sinh của con thứ hai trong hình không đọc rõ, nên O1 chỉ nói khoảng 16 tuổi. Giới hạn 100, 255, 2000 ký tự ngoài Context là Đề xuất QA. Bản này viết tiếng Việt, chưa có bản tiếng Anh như R4.
