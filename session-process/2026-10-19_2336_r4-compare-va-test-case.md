# So sánh UI với FS F4 v1.3 và viết test case R4

Ngày: 2026-10-19 23:36.

## 1. Intro
Anh dặn trước: khi môi trường local xong thì so sánh UI với FS F4, validate rule và seed data, ra một bảng compare, rồi viết test case theo ba nguồn đó. Sau đó anh báo "CHECK ROLE BA TÔI MỚI UPDATE FS04". Nguồn chính của R4 vì thế là roles/ba/FS04.docx (FS F4 v1.3, 19/10/2026, @Huy). FS v1.1 ([Agile] FS.docx) bị thay thế. Môi trường để xem UI là prototype https://edusave.vercel.app/ vì bộ deploy/qa chưa có giao diện và chỉ có một endpoint FAS (evaluate).

Việc làm gồm ba phần: (a) đọc FS04 và so với prototype thành bảng compare, (b) viết workbook test case R4 theo mẫu workbook R9, (c) cập nhật cây requirement, session log và bản đồ role qa.

## 2. Architecture
FS04 (quy tắc) -> prototype (UI thật để quan sát) -> bảng compare (56 dòng UI) -> test case (267 case) -> sheet Seed Data trong chính workbook.
Phần R4 chạm: đơn FAS (MOEFAS tự động xét sau khi form đóng, SBFAS do School Admin chọn scheme), quản lý scheme (wizard 3 bước, overlap, Add fee, nút demo Close form now), thông tin ML chỉ để xem.
Prototype chạy hoàn toàn phía client, ngày cố định 18/10/2026, nút Reset data tải lại trang. Nên 216 case chạy được trên prototype và 51 case cần bản build F4 có API.

## 3. Files modified
- roles/qa/R4_UI_vs_FS_Compare.xlsx: thêm 4 câu hỏi Q-14 đến Q-17 vào sheet Questions for BA khi viết test case. Lý do: trong lúc viết case thấy 4 chỗ FS chưa nói. Q-14 cột export của School Admin, Q-15 đơn của trường khác, Q-16 khoảng lọc ngày Submitted, Q-17 dải thu nhập From/To. Autofilter đổi sang A1:F18, ô Summary B18 đổi thành "17 open questions (Q-01 to Q-17)".
- Cây requirement (artifact, version 22): nâng CUR lên 20, thêm log v20 ngày 19 Oct 2026 và topic mới "R4 FAS Applications: FS F4 v1.3, prototype and test cases" gồm 10 leaf mới. Thêm 2 leaf vào các nhóm sẵn có của cây: một fact mới (FS F4 v1.3 đóng lỗ hổng auto-grant) và một điểm còn mở. Lý do: rule 2026-10-14 yêu cầu cập nhật cây khi fact R1 đến R10 đổi.
- CLAUDE.md và sessionlog/agileproject.md: thêm một dòng Session Log, xoay vòng dòng cũ nhất không ghim sang archive.
- what i know about these/qa.md và README.md: ghi ngày, độ sâu đọc và hai file mới của role qa.

## 4. Files added
- roles/qa/R4_UI_vs_FS_Compare.xlsx: bảng so sánh UI prototype với FS04. 56 dòng UI: 47 Match, 8 Differs, 1 Not verified, không dòng nào High. Có phần khoảng trống backend và 17 câu hỏi cho BA. Làm trước để biết FS và UI khác nhau ở đâu rồi mới viết case.
- roles/qa/R4_Test_Cases.xlsx: workbook test case R4, 117,814 byte, theo mẫu R9 (sheet Test cases có dấu cách cuối tên, Defect Reports, Summary, Scenarios, Assumptions, Questions, FS Trace, Seed Data). 267 case, 56 scenario, 20 suite F4.1 đến F4.20, 24 assumption (đều Open) cộng 7 mục môi trường ENV-R4-01 đến 07, 30 câu hỏi, 126 mục FS đều có case phủ. Review: 198 Approve, 68 Draft, 1 Block, 0 Reject. Severity S1 91, S2 121, S3 49, S4 6. Test Type: Functional 230, Integration 17, Security 16, UI 4. 27 seed mới SEED-R4-N1 đến N27 và 12 case engine lấy từ seed cũ SD-09 Engine.
- Vòng làm và lỗi gặp khi dựng workbook (code ở thư mục tạm trên máy, không nằm trong project): (1) heredoc quá 10KB gây spawn E2BIG nên chia mọi file nội dung dưới 8KB. (2) Công cụ Write ghi vào container đám mây chứ không vào máy anh nên tạo lại file bằng device_bash. (3) Cột Test Type chứa tên kỹ thuật (Equivalence partitioning...) ở 158 case nên thêm hàm ánh xạ sang Functional, Integration, Security, UI. (4) Mục FS 3.4 Submitted chưa case nào trích nên sửa TS-056 đọc cột Submitted. (5) Ghi chú và case Block còn trỏ tới số câu hỏi của file compare (Q-02, Q-04, Q-14, Q-17) không có trong sheet Questions mới nên đổi sang ASM-R4-xx. (6) ENV-R4-01 có câu "stay Not Run" vô nghĩa cho mục Available nên đặt N/A.
- Kiểm tra: tính lại bằng LibreOffice, không có lỗi công thức, số liệu Summary, Scenarios và FS Trace khớp nhau, đã xem ảnh PDF của Summary và Seed Data.

## 5. Files deleted
Không có.

## 6. Skills used
- qa-course:working-protocol: bắt buộc cho mọi task trong project này. Dùng để làm task list, ghi Session Log, xoay vòng dòng cũ và áp rule cập nhật cây requirement, bản đồ role.
Không dùng skill khác. openpyxl, LibreOffice, pdftoppm và trình duyệt tích hợp được dùng như công cụ.

## 7. External references
- https://edusave.vercel.app/ : prototype UI của F4, nguồn để so sánh với FS và đọc dữ liệu seed hiện có (scheme MOEFAS 2025 đến 2027, SBFAS Tier 1 đến 3 của Bukit View Primary và Meridian Secondary). Chọn vì đây là UI duy nhất của R4 lúc này.
- Không tra cứu web khác.

## Còn mở
24 assumption cần BA hoặc Dev trả lời. Ca Block (hai đơn cùng học sinh và cùng scheme MOEFAS) cần rule của BA. 51 case chờ bản build F4 có API. Validation rule và seed data cũ vẫn theo FS v1.1, chưa cập nhật lên v1.3.
