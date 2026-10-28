# Tài liệu validation rule và seed data cho R4 (2026-10-18)

## 1. Giới thiệu

Anh yêu cầu hai sản phẩm cho Dev: tài liệu quy tắc kiểm tra hợp lệ có hình UI khoanh khung từng field kèm mục nhỏ cho từng field, và file Excel seed data trong đó mỗi bộ dữ liệu có tên theo mục đích, mỗi dòng chứa giá trị thật và dùng chung cho nhiều chức năng. Anh chọn làm R4 trước, lấy hình trong FS F4, định dạng Word.

## 2. Kiến trúc

Chức năng FAS Applications (R4, FS F4 v1.1): danh sách đơn, drawer Review, hộp thoại Approve và Reject, engine gợi ý tier. Seed data gắn với các bảng fas_* trong Database Design Func4 v0.1, chưa map tên cột vì bản của Dev (14/10) khác FS (18/10).

## 3. File đã sửa

CLAUDE.md: thêm 1 dòng Session Log, xoay dòng cũ nhất không ghim (2026-10-15 Điền cột Note R9) sang sessionlog/agileproject.md. what i know about these/qa.md: thêm mục 10 cho hai file mới. what i know about these/README.md: nhắc hai file mới ở dòng roles\qa và dòng qa.md. sessionlog/agileproject.md: nhận dòng xoay.

## 4. File thêm

roles/qa/R4_FAS_Validation_Rules.docx: 41 trang, 7 màn hình, 60 field, 20 điểm cần BA xác nhận. Hình khoanh khung tạo từ 7 hình trong FS F4 bằng script PIL (khung đỏ, số trùng mã field). roles/qa/R4_FAS_Seed_Data.xlsx: 17 sheet. session-process/2026-10-18_2036_validation-seed-r4.md (file này).

## 5. File xóa

Không có.

## 6. Skill dùng

Không nạp skill. Word dựng bằng python-docx (Times New Roman, tiêu đề 14, 13, 12, căn đều, ngắt trang giữa các màn hình), Excel bằng openpyxl. Kiểm layout bằng cách đổi sang PDF bằng LibreOffice rồi xem từng trang.

## 7. Tham chiếu ngoài

Không dùng nguồn web. Căn cứ: FS F4 v1.1, Database Design Func4 v0.1, Product Backlog (PB-17 đến PB-21, PB-24), hồ sơ thầu và cây chức năng. Checksum NRIC của Singapore tính theo thuật toán công khai (trọng số 2,7,6,5,4,3,2, bảng chữ cái cho S, T, F, G).

## Điểm suy luận và còn mở

Band thu nhập và phần trăm trợ cấp của tier ngoài Tier 3, đặc trưng engine của hộ gia đình, người dùng, trường và học sinh ngoài hình là QA đề xuất, đánh dấu bằng cột Nguồn giá trị. Các đặc trưng engine của 6 đơn trong hình được suy ngược để khớp số trong hình (Need Score 59.72, 52.13, Confidence 74, 84). NRIC trong hình không qua checksum, bộ dữ liệu có thêm cột NRIC đúng checksum. Hai phát hiện cần BA: Borderline của MOEFAS không thể xảy ra theo công thức (Need Score nhỏ nhất 50.50), và FS F4 v1.1 khác Database Design Func4 v0.1. Kiểm bằng phép tính độc lập (Fraction) 56 ca engine, 19 dòng phí, checksum NRIC, ma trận ngân sách: không lỗi.


## Vòng 2 (20:46): bản tiếng Anh

Anh yêu cầu hai file xuất bằng tiếng Anh và đổi cấu trúc: nút chỉ nêu chức năng và cơ chế, ô nhập có giới hạn ký tự, rule valid và invalid kỹ thuật (ký tự đặc biệt, script, JSON), message hai trường hợp, dropdown có bảng thông tin riêng. Đã tạo roles/qa/R4_FAS_Validation_Rules_EN.docx (39 trang) và roles/qa/R4_FAS_Seed_Data_EN.xlsx. Bản tiếng Việt cũ cùng thư mục không dùng nữa, chưa xóa vì chưa được yêu cầu. Message cấp field và các rule xử lý chuỗi nguy hiểm là QA đề xuất (mục O21). Kiểm lại bằng phép tính độc lập, không lỗi, không còn ký tự tiếng Việt trong hai file.
