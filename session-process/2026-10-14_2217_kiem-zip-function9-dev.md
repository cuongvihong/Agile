# Session process: kiểm zip Function 9 của Dev (source code và hướng dẫn setup môi trường)

Ngày 2026-10-14, kết thúc lúc 22:17 (giờ Việt Nam). Project: Agileproject, tag agileproject. Viết bằng tiếng Việt theo rule ngôn ngữ ngày 2026-10-14 trong CLAUDE.md.

## 1. Giới thiệu

Người dùng (Cường, QA Lead) báo Dev vừa gửi một file zip, là source code và hướng dẫn setup môi trường, và yêu cầu kiểm tra. File là roles\dev\function9_14-10-26.zip. Mục tiêu của tôi: xác nhận zip chứa gì, README hướng dẫn có khớp source không, và phần nào của môi trường chạy được thật.

## 2. Kiến trúc

Không sửa code của Dev. Task chỉ đọc và chạy thử. Zip gồm backend .NET 10 (nhiều microservice, trong đó BillingPaymentService cổng 5008 và Payment Simulator cổng 5286, SQL Server 1433 trong Docker) và frontend React monorepo (e-service cổng 5174, payment checkout simulator cổng 5176). QA-README.md ở gốc zip hướng dẫn chạy 5 terminal và 7 scenario thủ công cho flow Fees & Payments.
Cách làm: chép zip từ máy người dùng qua cầu nối thiết bị, giải nén vào thư mục riêng trong thư mục tạm của phiên (không chạy script nào trong zip), đọc README, đối chiếu từng khẳng định với source bằng grep và đọc file, chạy phần frontend bằng npm. Container không có dotnet và mạng chặn tải SDK, nên không chạy backend.

## 3. File sửa

- what i know about these/dev.md: đổi dòng nguồn và độ sâu đọc, thêm một dòng vào bảng tổng hợp, thêm mục 7 cho zip. Lý do: Learned Rule 2026-10-14 yêu cầu cập nhật md khi roles có file mới.
- what i know about these/README.md: sửa dòng roles\dev, dòng dev.md trong bảng md, tổng số file (37 thành 38, dev từ 5 thành 6), hướng dẫn chọn md, và dòng ghi ngày cập nhật. Lý do: giữ README khớp dev.md.
- CLAUDE.md: chỉ sửa Session Log, thêm một dòng cho task này và chuyển dòng cũ nhất không ghim ("Lưu task của chat vào Session Log") sang sessionlog. Bốn dòng STILL ghim của ngày 2026-10-11 không đụng tới.
- sessionlog/agileproject.md: thêm nguyên văn dòng được chuyển, ở cuối bảng.

## 4. File thêm

- session-process/2026-10-14_2217_kiem-zip-function9-dev.md: file này.
Không thêm file nào vào thư mục của Dev. Các file giải nén và log chạy nằm trong thư mục tạm của phiên, không đưa vào project.

## 5. File xóa

Không xóa file nào. Không commit hay push gì.

## 6. Skill dùng

- qa-course:working-protocol (đã gọi sớm trong chat này): quy tắc Session Log, xoay vòng dòng, evidence rule (nêu rõ phần chưa kiểm và phần suy luận).
Không dùng skill nào khác.

## 7. Tham chiếu ngoài

Không dùng nguồn bên ngoài project. Nguồn là chính zip của Dev. Có thử tải .NET SDK để chạy backend, bị mạng chặn (mã 403), nên không có số liệu từ phía backend.

## Việc còn mở cho người dùng quyết

- Báo Dev sửa QA-README: lệnh docker compose ps, stop và down -v thiếu cùng tùy chọn -f với lệnh up (suy luận, cần chạy Docker để xác nhận).
- Báo Dev số unit test Billing: README backend ghi 7, đếm được 34 trong thư mục Tests.
- Chạy 7 scenario A đến G trên máy có Docker Desktop và .NET 10, lưu bằng chứng theo mục 15 của QA-README. Trước đó đối chiếu kỳ vọng với các case Both failure trong workbook R9.
- Chưa đọc docs\function 9 trong zip (schema md và sql, sơ đồ tuần tự, ui, auth) và docs\function 3.rar.
- Các việc mở cũ vẫn giữ: bốn dòng STILL ngày 2026-10-11, 85 ô #REF! trong workbook R1, nhánh R9 của cây yêu cầu, định nghĩa Block và Reject, ba assumption ASM-R9-01 đến 03, file "[Agile] FS.docx" không còn, pm.md và qalead-1-tai-lieu.md còn nhắc file PO v0.1 cũ.
