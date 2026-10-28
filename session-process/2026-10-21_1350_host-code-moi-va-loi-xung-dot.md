# Hướng dẫn host code mới và ghi lỗi dấu xung đột git của frontend

Ngày: 2026-10-21 13:50.

## 1. Intro
Anh đặt bản code mới của Dev vào roles/dev/code (hai repo edufams-backend và edufams-frontend) rồi nhờ host local theo bản này. Anh dặn thêm chưa sửa script automation, chỉ cần hướng dẫn. Khi chạy frontend gặp lỗi biên dịch, anh nhờ giải thích, mô tả lỗi để gửi Dev, ghi lại ngắn cho người không rành kỹ thuật, rồi dặn gỡ lỗi theo bản của Nito. Claude không có Docker và dotnet nên không tự host được backend, chỉ hướng dẫn và chuẩn bị file cấu hình.

## 2. Architecture
Trình duyệt, e-service Vite (cổng 5174) và admin portal (5173), proxy /api sang ApiGateway (5273), các service backend trong container edufams-qa-app của deploy/qa (cổng 5003 đến 5008, 5290), kèm SQL Server, Redis, RabbitMQ. MockPass (5156) chạy riêng bằng npm vì bộ QA Docker không có. Simulator thanh toán (5176 phía frontend, 5286 phía backend) chỉ cần cho test thanh toán online.

## 3. Files modified
- CLAUDE.md: thêm một dòng Session Log, trạng thái STILL. Số dòng không ghim vẫn là 4 dòng PASS nên không xoay vòng.
- what i know about these/dev.md: thêm mục 8 cho roles/dev/code.
- what i know about these/qa.md: thêm mục 15 cho FE_Merge_Conflict_Defect_Note.md.
- what i know about these/README.md: ghi cập nhật lần 7 và thêm thư mục code, file ghi lỗi vào bảng.
- 10 file trong roles/dev/code/edufams-frontend (3 file packages/ui và 7 file admin-portal): gỡ dấu xung đột, giữ phía HEAD (bản của Nito) ở cả 20 khối, giữ xuống dòng CRLF. Đây là sửa file trong source của Dev theo yêu cầu rõ ràng của anh, chưa commit, chỉ để QA chạy thử. Muốn quay lại: git checkout cfbe5d0 -- đường dẫn file.

Vòng sửa, nguyên nhân rồi cách xử lý:
(1) Claude gửi lệnh theo cú pháp cmd (cd /d) trong khi anh dùng PowerShell nên cd lỗi, npm báo không thấy package.json. Gửi lại lệnh PowerShell không có /d. Lẽ ra phải hỏi anh dùng cmd hay PowerShell từ đầu.
(2) Đã chạy một lệnh so sánh mã backend cũ và mới (IAMService, EducationAccountService, BillingPaymentService, ApiGateway), anh dừng lại và dặn chỉ hướng dẫn host. Phần đó chưa làm, nên chưa biết backend mới có sửa lỗi 401 giữa IAM và EducationAccountService (bản cũ phải dùng qa_eduaccount_proxy.js) hay chưa.
(3) Frontend không lên do dấu xung đột git trong commit cd7c1b2 và cfbe5d0. Tìm bằng git grep và grep, chia hai nhóm bằng so sánh sau khi bỏ khoảng trắng: 6 khối giống nhau (gói ui), 14 khối khác nhau (admin portal). Truy nguồn hai phía bằng cách tìm văn bản trong các commit 2269c37 và ca513b8.
(4) Chạy npm ci nền trên bản sao thì tiến trình bị dừng khi lệnh trả về, log rỗng. Chạy lại ở chế độ foreground thì xong trong 8 giây.

Ghi chú về số khối: tổng 20 khối, trong đó 6 khối nhóm giống nhau (1 khối index.ts, 4 khối DataTable.module.css, 1 khối Table.module.css) và 14 khối nhóm khác nhau (manifest 2, SchoolConfigPage 1, school-management.api 3, school-management.types 2, school-management.keys 1, use-school-management 2, SchoolDetailPage 3). Trong câu trả lời giải thích cho anh, Claude đã nói nhóm khác nhau có 16 khối, con số đúng là 14. Ghi chú lỗi gửi Dev dùng số khối từng file nên không sai.

## 4. Files added
- roles/dev/code/edufams-frontend/apps/e-service/.env và apps/admin-portal/.env: anh nhờ tạo. Trỏ backend http://localhost:5273, MockPass http://localhost:5156/singpass/login, admin ở chế độ API. File mẫu .env.example trỏ IP máy Dev nên không dùng được. Hai file nằm trong .gitignore của repo.
- roles/qa/FE_Merge_Conflict_Defect_Note.md: ghi chú lỗi để anh gửi Dev, tiếng Việt. Gồm tóm tắt, thông tin lỗi, bước tái hiện, bảng 10 file, hai bản là bản nào, đề nghị xử lý, cách kiểm, kết quả kiểm kiểu sau khi gỡ tạm.
- session-process/2026-10-21_1350_host-code-moi-va-loi-xung-dot.md: file này.
- Bản sao tạm trên máy ảo của Claude (fe_check, fe_base): để chạy tsc, không nằm trong project.

Kết quả kiểm kiểu bằng tsc trên bản sao: admin-portal 17 lỗi (bản sạch 2269c37 là 0), e-service 10 và api-client 2 (giống bản sạch), @edusave/ui, i18n, ui-showcase, payment-checkout-simulator 0 lỗi. 17 lỗi admin-portal chủ yếu là import hoặc biến không dùng và kiểu trong hai file test. Chưa mở UI để thử chức năng.

## 5. Files deleted
Không có.

## 6. Skills used
- qa-course:working-protocol: bắt buộc cho mọi task trong project. Dùng để làm task list, ghi Session Log, session-process và cập nhật bản đồ role.
Không dùng skill khác. Git, grep, node, npm, tsc dùng như công cụ.

## 7. External references
Không tra cứu web. Nguồn là README.md và deploy/qa của backend, package.json và .env.example của frontend, lịch sử git của repo edufams-frontend trong roles/dev/code.

## Còn mở
- Anh chạy backend Docker, MockPass, e-service và báo kết quả đăng nhập. Nếu bước tải tài khoản báo 401 thì cần xem lại, vì bản cũ phải dùng qa_eduaccount_proxy.js.
- Anh gửi FE_Merge_Conflict_Defect_Note.md cho Dev (c-Nito Hoang).
- Cần chốt phiên bản giao diện để test: bản đã gỡ theo Nito, hay commit sạch 2269c37.
- Giao diện billing mới đổi (ô nhập phần Education Account, eaAmount thay walletId, bộ lọc Overdue và DueSoon, ẩn cột hạn nộp) nên automation FS09 có thể cần chỉnh. Anh dặn chưa sửa.
- So sánh mã backend mới với bản cũ chưa làm.
