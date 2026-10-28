# Chuyển code sang codesprint1, giải nén codesprint2v1 và thiết lập script deploy một lệnh duy nhất (2026-10-22 13:03)

## 1. Giới thiệu
Thực hiện yêu cầu của người dùng: đổi thư mục `code` trong `roles/dev` thành `codesprint1`, giải nén gói zip mới tải về (`roles/dev/edufams-frontend.zip` chứa cả `edufams-backend` và `edufams-frontend`) vào thư mục mới `roles/dev/codesprint2v1`, và thiết lập một script chạy duy nhất để deploy và khởi chạy toàn bộ hệ thống không có lỗi.

## 2. Kiến trúc và luồng xử lý
1. Dừng stack Sprint 1 hiện hành (`run_edufams_update.cmd down`) và chuyển toàn bộ nội dung thư mục `roles/dev/code` (`edugovernment-frontend`, `QA_BE`, `QA_BE.zip`, `HuongDanChaySqlScript.txt`) sang `roles/dev/codesprint1`.
2. Giải nén `roles/dev/edufams-frontend.zip` vào `roles/dev/codesprint2v1`, thu được `codesprint2v1/edufams-backend` và `codesprint2v1/edufams-frontend`.
3. Xử lý hai lỗi chặn biên dịch trong bản `codesprint2v1`:
   - Gỡ dấu xung đột git `<<<<<<< HEAD` còn sót trong 4 file của `edufams-frontend` (`SchoolConfigPage.tsx`, `school-management.types.ts`, `SchoolDetailPage.tsx`, `Table.module.css`) và tạo các file `.env` chuẩn trỏ về `http://localhost:5273` và `http://localhost:5156/singpass/login`.
   - Khôi phục interface `LogService/LogService.Application/Contract/Service/v1/IAuditLogService.cs` bị xóa nhầm trong commit `2b0f947` của Dev để `LogService` biên dịch thành công trong Docker.
   - Chép bộ SQL seed scripts (`seed_students_wallets.sql`, `seed_student_charges.sql`, `reset_data.sql`) từ `codesprint1/QA_BE` sang `codesprint2v1/edufams-backend`.
4. Cập nhật `roles/qa/run_edufams_update.cmd` và liên kết với `roles/dev/run_edufams_all.cmd` cùng `roles/dev/codesprint2v1/run_edufams_all.cmd` để khi chạy một lệnh duy nhất, script thực hiện trọn vẹn 6 bước: kiểm tra môi trường, áp `IAMService.env` + bật QA proxy `5016` + bật MockPass `5156`, build và khởi chạy Docker backend `5273`, tự động nạp dữ liệu mẫu kèm `qa_seed_fix.sql`, cài đặt phụ thuộc npm và bật `e-service` (`5174`) cùng `admin-portal` (`5173`).

## 3. Các file đã sửa
- `roles/qa/run_edufams_update.cmd`
- `roles/dev/run_edufams_all.cmd`
- `roles/dev/codesprint2v1/edufams-frontend/apps/admin-portal/src/features/school-config/pages/SchoolConfigPage.tsx`
- `roles/dev/codesprint2v1/edufams-frontend/apps/admin-portal/src/features/school-management/api/school-management.types.ts`
- `roles/dev/codesprint2v1/edufams-frontend/apps/admin-portal/src/features/school-management/pages/SchoolDetailPage.tsx`
- `roles/dev/codesprint2v1/edufams-frontend/packages/ui/src/components/Table/Table.module.css`
- `what i know about these/dev.md`
- `what i know about these/qa.md`
- `what i know about these/README.md`
- `CLAUDE.md`
- `sessionlog/agileproject.md`

## 4. Các file đã thêm
- `roles/dev/codesprint1/run_edufams_sprint1.cmd`
- `roles/dev/codesprint2v1/run_edufams_all.cmd`
- `roles/dev/codesprint2v1/edufams-backend/LogService/LogService.Application/Contract/Service/v1/IAuditLogService.cs`
- `roles/dev/codesprint2v1/edufams-frontend/apps/e-service/.env`
- `roles/dev/codesprint2v1/edufams-frontend/apps/admin-portal/.env`
- `roles/dev/codesprint2v1/edufams-frontend/apps/payment-checkout-simulator/.env`
- `session-process/20261022_130300_setup_codesprint2v1_and_unified_runner.md`

## 5. Các file đã xóa
- Không xóa file dữ liệu nào (chuyển nội dung `roles/dev/code` sang `roles/dev/codesprint1`).

## 6. Skill đã dùng
- Không dùng skill ngoài.

## 7. Tham chiếu
- `roles/dev/edufams-frontend.zip`
- `roles/qa/run_edufams_update.cmd`
- `roles/dev/run_edufams_all.cmd`
