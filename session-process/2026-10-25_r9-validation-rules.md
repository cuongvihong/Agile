# Tạo R9_FAS_Validation_Rules.docx

## 1. Mục đích
Anh yêu cầu làm một tài liệu quy tắc validation cho R9 tương tự tài liệu của R4.

## 2. Phần hệ thống liên quan
Function 9, e-Service Portal của Parent (chọn con, phí còn nợ, chọn cách thanh toán, xem lại, kết quả) và Billing API.

## 3. File thêm
roles/qa/R9_FAS_Validation_Rules.docx, khoảng 37 trang, 7 hình sơ đồ. Cấu trúc theo R4: mục đích, quy ước, từng màn có hình, bảng nút, ô nhập, ô chọn, trường chỉ hiển thị, thông báo chung, điểm mở, phụ lục. Thêm mục 10 cho quy tắc API, webhook, phiên và ràng buộc dữ liệu vì R9 gần như không có ô nhập.

## 4. File sửa
CLAUDE.md, thêm một dòng Session Log.

## 5. Điểm cần nhớ
FS 09 không có hình màn hình và e-service cổng 5174 không đăng nhập được (MockPass 5156 và gateway 5273 không kết nối được từ trình duyệt của app), nên hình là sơ đồ QA ghi rõ không phải ảnh chụp. FS không có mục 5.2 nên VAL-18 không có mô tả. Có 22 điểm mở, quan trọng nhất O1 (phần EA khi chia đôi sửa được không) và O2 (chia đôi khi số dư đủ trả).

## 6. Nguồn tham khảo
R4_FAS_Validation_Rules_EN.docx, FS09.md, R9_Test_Cases_final_FS09.xlsx (Defect Reports), R9_Seed_Data.xlsx, F9_Dev_Local_Run_Results.md, r9_automation README và data/ui_text.py.


Vòng 2: Cường gửi R4_FAS_Deliverables.zip và yêu cầu nội dung súc tích. Viết lại R9_FAS_Validation_Rules.docx theo mẫu bảng Mục/Quy tắc của R4 (Draft 0.4): 29 trang, khoảng 7.9k từ thay vì 13.6k, giữ 7 hình sơ đồ A đến G. Bản chi tiết cũ lưu thành R9_FAS_Validation_Rules_v1_chi_tiet.docx. Chưa tạo bản EN.


Vòng 3: anh yêu cầu lấy hình từ localhost đang host. Nút Sign in trong trình duyệt của app không tự chuyển trang sang MockPass (ERR_BLOCKED_BY_CLIENT với điều hướng do trang khởi tạo), nên QA dựng tay URL MockPass với tham số của e-service, lấy link callback của persona S7890123F rồi mở bằng công cụ navigate. Chụp 5 màn: danh sách con, danh sách phí, chọn phương thức, xem lại, lỗi /billing/null; đánh dấu mã trường và thay hình A đến D. Không bấm Authorize and pay nên không tạo giao dịch. Màn E đến G cần giao dịch thật, giữ sơ đồ. Ảnh gốc ở /tmp/w/shots, chưa lưu vào dự án.
