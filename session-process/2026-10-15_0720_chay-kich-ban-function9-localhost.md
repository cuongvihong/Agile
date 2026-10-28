# Session process: chạy 7 kịch bản Function 9 của Dev trên localhost

Ngày 2026-10-15, kết thúc khoảng 07:20 (giờ Việt Nam). Project: Agileproject, tag agileproject. Viết tiếng Việt theo rule ngôn ngữ ngày 2026-10-14.

## 1. Giới thiệu

Cường (QA Lead) yêu cầu chạy lại source code Function 9 của Dev trên máy local và chạy các kịch bản A đến G trong QA-README mục 10, rồi cập nhật kết quả vào test case. Chạy các kịch bản đã hoãn từ phiên trước. Lần 1 dùng trình duyệt tích hợp, sau đó anh đề nghị Claude tự chạy tiếp trên Chrome của anh: A anh tự làm, tôi chạy C đến G và lấy evidence DB, rồi ghi vào test case.

## 2. Kiến trúc

Chạm vào gói Dev function9_14-10-26: backend .NET 10 (BillingPaymentService cổng 5008, OnlinePaymentGatewaySimulation cổng 5286), SQL Server trong Docker (container template-sqlserver), frontend Vite (e-service 5174, payment-checkout-simulator 5176). Luồng: e-service gọi POST /api/billing/v1/checkout, nhận checkoutUrl của simulator, simulator gọi webhook về Billing API, trang /payment-result đọc GET transactions/{id}. QA điều khiển bằng trình duyệt tích hợp, đọc DB qua helper f9qa-helper.ps1 (HttpListener cổng 5199, /f9qa/reset, /f9qa/evidence).

## 3. File sửa

- CLAUDE.md: chỉ sửa Session Log. Thêm một dòng, chuyển dòng cũ nhất không ghim ("Bỏ rule bắt buộc prompt, đổi rule ngôn ngữ tài liệu") nguyên văn sang sessionlog. Lần đầu script chọn nhầm một dòng Learned Rule (cùng tag agileproject và cùng định dạng ngày) và chuyển nó đi; phát hiện ngay khi xem kết quả, đã đưa dòng đó về đúng vị trí cũ trong Learned Rules và bỏ khỏi sessionlog, rồi xoay vòng lại đúng dòng Session Log. Bốn dòng STILL ghim của 2026-10-11 không đụng tới.
- sessionlog/agileproject.md: thêm nguyên văn dòng "Bỏ rule bắt buộc prompt..." ở cuối.
- roles/qa/F9_Dev_Local_Run_Results.md: sau lần chạy Chrome, sửa mục 2.4 (trước đó ghi sai returnUrl DEV là lỗi, thật ra do trình duyệt tích hợp chặn chuyển trang), thay mục 3 bằng danh sách case đã ghi vào Excel, cập nhật mục 4 và cách chạy G.
- roles/qa/R9_Test_Cases_notes.xlsx: ghi cột Execution Status (H) và Actual Result (O) cho 24 case (5 Passed, 8 Failed, 11 giữ Not Run); kiểm bằng openpyxl chỉ cột H và O của sheet Test cases đổi (37 ô: 24 ô O và 13 ô H), bảng, định dạng có điều kiện và data validation giữ nguyên. File này là bản sao của tôi (đã có cột Note), file gốc R9_Test_Cases.xlsx không đụng. Cột Summary dùng COUNTIFS sẽ tự tính lại khi mở Excel.

## 4. File thêm

- roles/qa/F9_Dev_Local_Run_Results.md (sửa sau, xem mục 3): bảng kết quả A đến G, bằng chứng DB, 8 điểm lệch cần hỏi Dev, ánh xạ suy luận sang R9.
- session-process/2026-10-15_0720_chay-kich-ban-function9-localhost.md: file này.
- function9_14-10-26/f9qa-helper.ps1 và setup-function9.ps1 (tạo từ phiên trước, nay dùng thật): helper reset DB và đọc bằng chứng; script dựng môi trường. Chưa chốt giữ hay bỏ trong hồ sơ project.

## 5. File xóa

Không xóa file nào. Không commit hay push. Reset DB bằng helper nhiều lần giữa các kịch bản (DB dev của Docker, dữ liệu mẫu, không phải dữ liệu thật).

## 6. Skill dùng

- qa-course:working-protocol: quy tắc Session Log, xoay vòng, nêu rõ phần suy luận và phần chưa kiểm.
- anthropic-skills:chrome-browser: đọc trước khi dùng Claude in Chrome (mở tab mới, quyền site, tránh hộp thoại), vì anh yêu cầu chạy trên Chrome của anh.
Không dùng skill nào khác.

## 7. Tham chiếu ngoài

Không dùng nguồn ngoài project. Nguồn: QA-README.md, source frontend và backend trong gói Dev. Không nhập mật khẩu nào; mật khẩu SQL do helper tự đọc từ file compose trên máy anh và không được chép vào tài liệu.

## Việc còn mở cho người dùng quyết

- Duyệt ánh xạ Dev scenario sang case R9 và 8 case đã đánh Failed (TC-090, 100, 103, 131, 136, 137, 139, 140), rồi tạo Defect nếu đồng ý; chép cột H và O sang R9_Test_Cases.xlsx gốc.
- Hỏi Dev 8 điểm trong F9_Dev_Local_Run_Results.md mục 2, quan trọng nhất: không thanh toán lại được sau thất bại online, và EA không được hoàn khi online thất bại.
- Ghi đè R9_Test_Cases.xlsx hay anh chép cột S từ R9_Test_Cases_notes.xlsx; giữ hay bỏ f9qa-helper.ps1 và setup-function9.ps1.
- Có thể tắt helper (cửa sổ PowerShell đang chạy) và dừng container khi xong.
