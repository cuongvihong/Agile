# Kiểm tra dữ liệu test của Dev (DataTest.zip), 2026-10-27

## 1. Giới thiệu
Anh yêu cầu vào role Dev kiểm tra file dữ liệu test. File là roles/dev/DataTest.zip (UAT seed). Claude giải nén ra thư mục tạm trên máy, chạy 6 script kiểm tra (tính toàn vẹn, checksum NRIC, tuổi theo lớp, khóa ngoại, nhất quán số liệu FAS, ví và top up, so sánh xlsx với csv). Không sửa file của Dev.

## 2. Kiến trúc
DataTest.zip gồm seed-data-csv (thư mục theo service: IAM, StudentSchool, EducationAccount, BillingPayment, FAS, Announcement, Log, CitizenSimulator, MockPass_Singpass, BulkImportTemplates, UAT_Overview), seed-data-xlsx (cùng nội dung dạng xlsx), uat-seed-data.csv/.xlsx gộp 56 bảng, và nhiều bản sao phẳng. Kết quả so sánh: xlsx khớp csv từng bảng (0 lệch số dòng), uat-seed-data trùng 00_UAT_Overview, các xlsx ở gốc trùng byte với seed-data-xlsx.

## 3. File đã sửa
CLAUDE.md: thêm một dòng Session Log (CRLF).

## 4. File thêm
session-process/2026-10-27_dev-seed-data-check.md (file này). Không tạo file kết quả riêng, báo cáo trả lời trong chat.

## 5. File xóa
Không có.

## 6. Skill dùng
Không nạp skill. Kiểm tra bằng Python (csv, openpyxl). Thuật toán checksum NRIC: trọng số 2,7,6,5,4,3,2, cộng 4 cho T/G, bảng chữ ST và FG.

## 7. Tham chiếu ngoài
Không dùng nguồn web. Đối chiếu với R5_Test_Cases.xlsx, R6_Test_Cases.xlsx, FS03, FS04, FS06, FS09. Không chạy prototype trong Claude.

## Điểm suy luận và còn mở
Suy luận: NRIC sai checksum được coi là lỗi dữ liệu, chưa rõ Dev có chủ ý dùng NRIC giả không hợp lệ cho demo. Liam Pham 6 tuổi có đơn và ví được coi là bất thường theo quy tắc tuổi FS01, cần BA xác nhận. Chưa kiểm: Announcement và Log service (chỉ đếm bảng), so khớp với prototype. Chưa gửi phản hồi cho Dev, chờ anh quyết định.
