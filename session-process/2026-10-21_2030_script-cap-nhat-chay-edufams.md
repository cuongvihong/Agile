# Script cập nhật code và chạy lại cả bộ EduFAMS

Ngày: 2026-10-21 20:30.

## 1. Intro
Anh hỏi có tạo được một script để chạy mỗi lần Dev cập nhật code không. Claude viết roles\qa\run_edufams_update.cmd gom các bước đã làm tay trong ngày: cập nhật backend, áp bản sửa QA cho đăng nhập, chạy MockPass, chạy frontend. Claude không có cmd, Docker hay dotnet nên không chạy được script, chỉ rà lại cú pháp.

## 2. Architecture
Backend mới chạy trong container edufams-qa-app (deploy\qa\docker-compose.yml, ApiGateway 5273, IAM 5290). MockPass chạy trên máy host ở cổng 5156 bằng npm. Frontend edugovernment-frontend chạy hai app Vite: e-service 5174 và admin-portal 5173. Đăng nhập đi qua e-service, MockPass, rồi IAM trong container gọi lại MockPass và EducationAccountService. Bản sửa QA gồm file IAMService.env (hai dòng override Singpass__BaseUrl và EduAccount__BaseUrl trỏ host.docker.internal) và proxy qa_eduaccount_proxy.js ở cổng 5016.

## 3. Files modified
- CLAUDE.md: thêm một dòng Session Log, trạng thái STILL. Các dòng không ghim vẫn là 4 dòng PASS nên không xoay vòng.
- what i know about these/dev.md: thêm mục 10 (thư mục edugovernment-frontend).
- what i know about these/qa.md: thêm mục 17 (script mới).
- what i know about these/README.md: ghi cập nhật lần 10 và bổ sung hai dòng trong bảng.

Các vòng làm việc, nguyên nhân rồi kết quả:
(1) Viết bản đầu 16160 byte, ghi ra bằng Python để chắc CRLF và ASCII (file kiểm ra DOS batch, CRLF).
(2) Rà cú pháp. Một dòng chú thích có %~nx0 và %~dp0 sẽ bị cmd tự thay giá trị nên viết lại thành chú thích không có ký tự phần trăm. Không có dấu chấm than lạ trong các dòng echo vì script bật delayed expansion. Tên workspace e-service và admin-portal khớp package.json của hai app.
(3) Khi thiếu package-lock.json thì npm ci sẽ lỗi nên đổi thành: có lock thì npm ci, không có thì npm install.

## 4. Files added
- roles/qa/run_edufams_update.cmd: script một lệnh cho mỗi lần Dev cập nhật code. Chế độ update, be, fe, status, login, logs, errors, fix, unfix, stop, down, help. Cài đặt đổi được bằng biến BACKEND_DIR, FRONTEND_DIR, BACKEND_URL, MOCKPASS_URL, QA_FIX.
- session-process/2026-10-21_2030_script-cap-nhat-chay-edufams.md: file này.

## 5. Files deleted
Không có. File tạm tạo script trong thư mục home đã xóa sau khi ghi xong.

## 6. Skills used
- qa-course:working-protocol: bắt buộc cho mọi task trong project. Dùng để làm task list, ghi Session Log, session-process và cập nhật bản đồ role.
Không dùng skill khác.

## 7. External references
Không tra cứu web. Nguồn là run_edufams_qa.cmd và run_edufams_all.cmd (mẫu cấu trúc), package.json gốc và của hai app trong edugovernment-frontend, deploy\qa của edufams-backend, roles\dev\qa_IAMService.env.reference và qa_eduaccount_proxy.js.

## Còn mở
- Script chưa chạy lần nào. Rủi ro đã biết: lệnh kiểm kết nối dùng bash trong container nên có thể báo cảnh báo sai nếu image không có bash; cổng 5156 trên host có thể bị Windows Firewall chặn container.
- Chưa biết bản sửa đăng nhập có hết lỗi Invalid or expired SingPass authorization code không. Nếu còn lỗi, chạy run_edufams_update.cmd login và gửi log IAM kèm đuôi log proxy.
- File override chép vào deploy\qa\config vì anh đã yêu cầu áp bản sửa. Khi Dev sửa xong thì chạy unfix.

## Cập nhật 21:15
Sau khi anh chạy script, Claude đăng nhập thử trên trình duyệt trong khung bằng persona S7890123F. Lỗi mã SingPass đã hết nhưng API singpass-login trả 400: SqlServerRetryingExecutionStrategy không hỗ trợ transaction tự mở. Nguyên nhân thuộc backend: docker-compose.yml dòng 134 bật EnableRetryOnFailure, EServiceSingpassLoginHandler dòng 151 và BffSessionService dòng 349 không bọc ExecuteStrategyAsync. Bản cũ không lỗi vì file override cũ EduFAMS\deploy\qa\config\IAMService.env có dòng tắt retry. Khi chuyển file ra roles\dev, Claude chỉ giữ 2 dòng nên thiếu. Claude bổ sung lại dòng thứ ba vào qa_IAMService.env.reference.

Anh gửi QA_BE.zip mới và HuongDanChaySqlScript.txt, nên Claude sửa run_edufams_update.cmd (thêm 5 phần): tự giải nén zip (dừng container cũ, thay hẳn thư mục QA_BE, giữ deploy\qa\.env), tìm backend ở QA_BE trước, chế độ unzip, seed (hai file seed của Dev qua sqlcmd trong edufams-qa-sqlserver, mật khẩu lấy từ biến MSSQL_SA_PASSWORD trong container, không ghi vào script) và payreset (reset_data.sql, gõ YES). Quét dấu ngoặc của script cân bằng, chưa chạy vì Claude không có cmd.

Còn mở bổ sung: không thấy frontend mới trong project (chỉ có bản develop 18/10 ở roles\dev\edugovernment-frontend, script dùng bản này và cảnh báo); chưa xác nhận lỗi 400 hết; chưa chạy các script SQL; tên cơ sở dữ liệu trong hướng dẫn của Dev (BillingPaymentDatabase) khác tên thật (BillingPaymentService).

Lúc 21:12 anh chạy seed và gặp Msg 1934 (QUOTED_IDENTIFIER) ở lệnh DELETE của seed_students_wallets.sql. Nguyên nhân là sqlcmd mặc định tắt QUOTED_IDENTIFIER, lỗi nằm ở lệnh gọi của script chứ không ở file SQL của Dev. Claude thêm cờ -I vào dòng sqlcmd trong run_sql.

Lúc 21:30 đăng nhập thành công. Màn hình chính báo Unable to load education accounts, Data is Null. Claude đăng nhập lại trên khung trình duyệt, thấy edu-account/students trả 500, gọi thẳng EducationAccountService qua proxy 5016 thì danh sách và accounts/S9000001A lỗi, còn accounts/S1234567A trả 200. Đối chiếu code: EducationAccountDbContext.cs dòng 82 đặt IsRequired cho updated_at trong khi cột và entity cho phép NULL, và seed của Dev để updated_at NULL. Lỗi của Dev. Claude thêm roles\qa\qa_seed_fix.sql (điền updated_at bằng created_at) và cho chế độ seed chạy file này sau seed của Dev. Chưa kiểm sau khi chạy.

Lúc 21:50 anh nhờ chụp hết màn hình liên quan FS09. Danh sách con đã hiện sau bản vá, nhưng trang phí báo Unable to load education account vì API ví trả 400. Đối chiếu: EducationAccountService trả updatedAt null, EduWalletDTO.UpdatedAt của IAM không cho null nên ném JsonException. Claude thêm lệnh cập nhật wallets.updated_at vào qa_seed_fix.sql, chờ anh chạy lại seed rồi mới chụp.
