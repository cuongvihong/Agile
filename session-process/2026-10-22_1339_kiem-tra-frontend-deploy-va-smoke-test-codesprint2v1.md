# Session Process: Kiểm tra lại frontend và hướng dẫn deploy, hoàn thiện script chạy 1 lần và đạt 9 trên 9 smoke test trên codesprint2v1

## 1. Giới thiệu (Intro)
Người dùng yêu cầu kiểm tra lại toàn bộ frontend của `codesprint2v1`, đối chiếu với hướng dẫn deploy trong source code và hoàn thiện một script chạy 1 lần duy nhất không lỗi.

## 2. Kiến trúc hệ thống tác động (Architecture)
1. **Frontend Monorepo (`roles/dev/codesprint2v1/edufams-frontend`)**:
   * Gồm các ứng dụng Vite: `e-service` (cổng `5174`), `admin-portal` (cổng `5173`), `payment-checkout-simulator` (cổng `5176`), `@edusave/ui-showcase` (cổng `5175`), và các gói `@edusave/ui`, `@edusave/i18n`, `@edusave/api-client`.
2. **Backend & QA Overrides (`roles/dev/codesprint2v1/edufams-backend`, `roles/dev/`, `roles/qa/`)**:
   * Cơ chế cấu hình ghi đè theo từng service trong `deploy/qa/entrypoint.sh` thông qua `/app/config/<ServiceName>.env` (`deploy/qa/config/IAMService.env`, `deploy/qa/config/EducationAccountService.env`).
   * Proxy trung gian `roles/dev/qa_eduaccount_proxy.js` (cổng `5016`) chuyển tiếp sang `EducationAccountService` (cổng `5006`).
3. **Unified Runner & Smoke Automation (`roles/qa/run_edufams_update.cmd`, `roles/qa/r9_automation`)**:
   * Script chạy một lần khởi tạo toàn bộ backend Docker, MockPass, QA proxy, nạp dữ liệu mẫu và 3 ứng dụng frontend (`5174`, `5173`, `5176`).

## 3. Các file đã chỉnh sửa (Files Modified)
* `D:\AIQA\Agileproject\roles\qa\run_edufams_update.cmd`:
  * **Lý do**: Bổ sung tự động chép `qa_EducationAccountService.env.reference` vào `deploy\qa\config\EducationAccountService.env`, tự động khởi chạy và kiểm tra thêm `payment-checkout-simulator` ở cổng `5176` cùng với `e-service` (`5174`) và `admin-portal` (`5173`).
* `D:\AIQA\Agileproject\roles\dev\qa_IAMService.env.reference`:
  * **Lý do**: Bổ sung `Singpass__ClientId=template-iam-service` và `Singpass__ClientSecret=` để tránh phụ thuộc giá trị placeholder trong `appsettings.Example.json`.
* `D:\AIQA\Agileproject\roles\dev\qa_eduaccount_proxy.js`:
  * **Lý do**: Khi `IAMService` gọi `GET /api/v1/accounts` với header `x-user-roles: PARENT`, `GetAllStudentProfilesEndpoint.cs` trong `codesprint2v1` thiếu quyền `PARENT` gây lỗi `403 Forbidden`. Đã cập nhật proxy gán `x-user-roles: MOEHQ,PARENT` cho các truy vấn tra cứu tài khoản và ví.
* `D:\AIQA\Agileproject\roles\dev\codesprint2v1\edufams-backend\EducationAccountService\EducationAccountService.API\Controllers\v1\Account\GetAllStudentProfilesEndpoint.cs`:
  * **Lý do**: Khôi phục `[Authorize(Roles = "MOEHQ, SCHOOL, PARENT")]` đồng bộ với các endpoint khác của `EducationAccountService`.
* `D:\AIQA\Agileproject\roles\dev\codesprint2v1\edufams-frontend\package.json`:
  * **Lý do**: Sửa tên workspace `ui-showcase` thành `@edusave/ui-showcase` khớp với `apps/showcase-ui/package.json`.
* `D:\AIQA\Agileproject\roles\dev\codesprint2v1\edufams-frontend\apps\e-service\src\features\billing-payment\pages\BillingAccountSelectionPage.tsx`:
  * **Lý do**: Sửa `data.totalPages` thành `data.metadata.totalPages` theo cấu trúc `EducationAccountPage` mới.
* `D:\AIQA\Agileproject\roles\dev\codesprint2v1\edufams-frontend\apps\e-service\src\features\billing-payment\pages\BillingPaymentPage.tsx`:
  * **Lý do**: Bỏ comment đoạn hiển thị mô tả tên học sinh và dòng `Student ID` kèm `Status` của ví.
* `D:\AIQA\Agileproject\roles\dev\codesprint2v1\edufams-frontend\apps\admin-portal\src\features\moe-hq-fas-schemes\lib\code-maps.ts`, `components\detail\MoeFasDetailView.tsx`, `pages\CreateMoeFasPage.tsx`:
  * **Lý do**: Sửa đường dẫn import tương đối bị sai, thêm `return` trong hàm `band()` của `MoeFasDetailView.tsx`, và sửa so sánh `"DRAFT"` thành `"Draft"`.
* Dọn các import/biến thừa trong `create-router.tsx`, `mappers.ts`, `get-education-accounts.ts`, `transaction-history/types/index.ts`, `fee-management/manifest.ts`, `FeeManagementHomePage.tsx`, `SchoolConfigAcademicLevelDetail.tsx`, `SchoolConfigHeader.tsx`, `school-management.types.ts`, `fee-management.api.test.ts` để `npm run typecheck` trên cả 3 ứng dụng frontend đạt 0 lỗi.
* `D:\AIQA\Agileproject\roles\qa\r9_automation\pages\admin_page.py` và `pages\billing_page.py`:
  * **Lý do**: Cập nhật locator tiêu đề trang đăng nhập Admin Portal hỗ trợ cả Sprint 1 (`"Welcome back"`) và Sprint 2 (`"Login"`), thêm `exact=True` cho nút `"Sign in"` và tránh treo khi đọc `wallet_line`.
* `D:\AIQA\Agileproject\what i know about these\dev.md`, `qa.md`, `D:\AIQA\Agileproject\CLAUDE.md`, `D:\AIQA\Agileproject\sessionlog\agileproject.md`:
  * **Lý do**: Cập nhật bản đồ tri thức và nhật ký phiên làm việc.

## 4. Các file đã thêm mới (Files Added)
* `D:\AIQA\Agileproject\roles\dev\qa_EducationAccountService.env.reference`: File cấu hình ghi đè cung cấp `CPFSimulation__BaseUrl=http://localhost:5287/` và `GovernmentSimulation__BaseUrl=http://localhost:5287/` cho `EducationAccountService`.
* `D:\AIQA\Agileproject\roles\dev\codesprint2v1\edufams-frontend\apps\payment-checkout-simulator\.env`: File môi trường cho ứng dụng giả lập cổng thanh toán (`5176`).
* `D:\AIQA\Agileproject\session-process\2026-10-22_1339_kiem-tra-frontend-deploy-va-smoke-test-codesprint2v1.md`: File nhật ký chi tiết quá trình xử lý task này.

## 5. Các file đã xóa (Files Deleted)
* Không xóa file nào trong dự án.

## 6. Skills đã sử dụng (Skills Used)
* Không sử dụng skill bên ngoài, tuân thủ quy trình trong `CLAUDE.md`.

## 7. Tài liệu tham chiếu bên ngoài (External References)
* Không tra cứu nguồn bên ngoài; đối chiếu trực tiếp với `deploy/qa/README.md`, `deploy/README.md`, `edufams-frontend/docs/development/GETTING_STARTED.md` và mã nguồn trong `codesprint2v1`.
