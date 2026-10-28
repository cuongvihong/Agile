# Đăng nhập thử trên code mới và dừng theo lời anh

Ngày: 2026-10-21 16:30.

## 1. Intro
Anh báo các lỗi khi đăng nhập code mới lặp lại lỗi của code cũ và nhờ sửa tương tự. Claude so sánh mã backend cũ với mới, rồi đăng nhập thử trong khung trình duyệt của ứng dụng (chạy trên máy anh, tới được localhost) bằng persona MockPass S7890123F, không nhập mật khẩu. Sau khi Claude đưa hướng sửa phía QA, anh dặn không đụng tới deploy nữa, việc này để Dev sửa rồi gửi lại. Phiên dừng ở chỗ đó, chưa có lần đăng nhập nào thành công trên code mới.

## 2. Architecture
Trình duyệt e-service (5174) gọi POST /api/iam/v1/auth/e-service/singpass-login qua ApiGateway (5273) tới IAMService (5290, chạy trong container edufams-qa-app). IAM đổi mã với MockPass (5156, chạy trên máy anh bằng npm), rồi gọi EducationAccountService (5006, cùng container) để tra con theo NRIC. EducationAccountService không có đăng nhập riêng, nó tin header X-User-Id, X-User-Roles do gateway gắn.

## 3. Files modified
- roles/dev/qa_eduaccount_proxy.js: bỏ vế "không có Authorization" trong điều kiện chèn header, cập nhật chú thích đầu file. Lý do: code mới gửi access token dạng Authorization Bearer, bản proxy cũ bỏ qua mọi request đã có Authorization nên sẽ không có tác dụng. Kiểm bằng node --check, chưa chạy proxy lần nào sau sửa. Đây là file QA, không phải mã nguồn Dev.
- CLAUDE.md: thêm một dòng Session Log, trạng thái STILL. Số dòng không ghim là 4 dòng PASS nên không xoay vòng.
- what i know about these/dev.md: thêm mục 9.
- what i know about these/README.md: ghi cập nhật lần 8 và sửa dòng dev.md trong bảng.

Vòng làm việc, nguyên nhân rồi cách xử lý:
(1) Click nút "Sign in with Singpass" trong khung trình duyệt không chuyển sang MockPass, và nút "Log in" của MockPass cũng không chuyển về callback. Cách xử lý: tự dựng đường dẫn authorize bằng JavaScript (giống hàm createSingpassAuthorizationUrl của e-service, lưu state vào sessionStorage), mở trang MockPass, lấy địa chỉ callback có mã trong giá trị của ô chọn persona, rồi mở thẳng địa chỉ đó.
(2) Callback trả 401 "Invalid or expired SingPass authorization code". Cách xử lý: gọi thử endpoint /singpass/token của MockPass từ chính trang MockPass (cùng origin). Kết quả 200, có id_token, children_birth_records là S1234567A. Vậy MockPass hoạt động, lỗi nằm ở bước IAM đổi mã.
(3) Claude đã tạo deploy/qa/config/IAMService.env (Singpass__BaseUrl và EduAccount__BaseUrl trỏ host.docker.internal) và đề nghị anh chạy proxy rồi restart container. Anh dặn không đụng deploy nữa. Claude đã chuyển file ra roles/dev/qa_IAMService.env.reference, thư mục deploy/qa/config giờ chỉ còn IAMService.env.example như lúc đầu. Claude không biết anh đã restart container trong lúc file còn nằm đó hay chưa. Nếu đã restart thì IAM đang đọc override cũ, cần restart lại để bỏ.

## 4. Files added
- roles/dev/qa_IAMService.env.reference: bản lưu hai dòng override QA, ghi để khi Dev sửa xong mà vẫn cần thì dùng lại. Không nằm trong deploy.
- session-process/2026-10-21_1630_dang-nhap-code-moi-va-dung-lai.md: file này.
Tạo rồi chuyển đi: deploy/qa/config/IAMService.env, xem mục 3.

## 5. Files deleted
Không có. IAMService.env được chuyển bằng lệnh mv, không xóa.

## 6. Skills used
- qa-course:working-protocol: bắt buộc cho mọi task trong project. Dùng để làm task list, ghi Session Log, session-process và cập nhật bản đồ role.
Không dùng skill khác. Khung trình duyệt của ứng dụng, grep, diff, node dùng như công cụ.

## 7. External references
Không tra cứu web. Nguồn là mã backend trong roles/dev/code/edufams-backend (IAMService, EducationAccountService, deploy/qa), mã e-service trong roles/dev/code/edufams-frontend, và nhật ký roles/dev/qa_eduaccount_proxy.log của lần chạy code cũ.

## Phát hiện cho Dev
[Dữ kiện] Đăng nhập Singpass trên code mới trả 401 "Invalid or expired SingPass authorization code" ở bước singpass-login. MockPass gọi trực tiếp từ trình duyệt thì trả token hợp lệ, có một con S1234567A, và seed của EducationAccountService (02_SeedStudentData.sql) có S1234567A.
[Suy luận] Nguyên nhân có thể là IAM trong container không tới được MockPass: appsettings.Example.json (Dockerfile dùng khi thiếu appsettings.json) đặt Singpass:BaseUrl là http://localhost:5156, mà localhost trong container là chính container, còn MockPass chạy trên máy anh. SingpassClient không bắt được lỗi này riêng, nó chỉ ghi log rồi trả null, và handler báo đúng thông điệp "Invalid or expired". Chưa xem log IAM nên chưa xác nhận. Chưa loại trừ khả năng mã hết hạn, vì Claude mở callback khoảng một phút sau khi MockPass sinh mã.
[Dữ kiện] So với code cũ, EServiceSingpassLoginHandler chuyển bước tra con (GetEduAccountDetail) từ trước khi tạo session sang sau khi tạo session, và truyền accessToken. EduAccountServiceClient gửi token đó dạng Authorization Bearer. Hàm AddIdentityHeadersFromToken có trong file nhưng GetAsync không gọi.
[Suy luận] EducationAccountService (AuthenticationExtension.cs) chỉ đọc Bearer khi không có header X-User-*, rồi đưa nguyên claim của JWT vào danh sách. JwtService của IAM ghi vai trò bằng JwtSecurityTokenHandler.CreateToken, nên khóa trong token là "role", còn identity lấy ClaimTypes.Role làm kiểu vai trò. Vì vậy [Authorize(Roles = "MOEHQ,SCHOOL,PARENT")] của GET /accounts/{nric} có thể không khớp và trả 403, rồi IAM báo không có tài khoản giáo dục. Chưa chạy nên chưa chắc. Bản cũ cần qa_eduaccount_proxy.js vì 401 ở bước này.
[Dữ kiện] File AuthenticationExtension.cs của EducationAccountService giống bản cũ ngoài việc thêm đọc X-User-School-Id.

## Còn mở
- Dev sửa và gửi lại, sau đó đăng nhập lại để xem lỗi kế tiếp (bước tra con, rồi tải hồ sơ và ví).
- Chưa có log IAM nên chưa phân biệt được IAM không tới MockPass với mã hết hạn.
- Kiểm xem anh đã restart container lúc file override còn nằm trong deploy chưa.
- Anh chưa quyết có gửi mục Phát hiện cho Dev hay không.
