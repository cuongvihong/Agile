# Session process: đọc toàn bộ roles và tạo thư mục what i know about these

Ngày 2026-10-14, kết thúc lúc 18:17 (giờ Việt Nam). Project: Agileproject, tag agileproject. Viết bằng tiếng Việt theo rule ngôn ngữ ngày 2026-10-14 trong CLAUDE.md.

## 1. Giới thiệu

Người dùng (Cường, QA Lead) yêu cầu: đọc toàn bộ file trong roles, tạo thư mục `what i know about these` chứa các md giải thích nội dung file đã đọc để chat sau đọc thay vì đọc lại, đặt rule trong CLAUDE.md hướng dẫn chat sau dùng thư mục này, và viết README mô tả cấu trúc các thư mục trong Agileproject.
Kết quả: 8 file md mới, một Learned Rule và một ghi chú cấu trúc trong CLAUDE.md, một dòng Session Log mới, một dòng cũ chuyển sang sessionlog, và file này.
Chat này đã làm nhiều task trước đó (test case R9, đọc hai PDF của Dev, lưu Session Log, so sánh CLAUDE.md, bỏ rule prompt). File này chỉ ghi task hiện tại. Các task trước đã có dòng Session Log riêng.

## 2. Kiến trúc

Task này không đụng đến code hay hệ thống. Nó thêm một lớp tri thức giữa thư mục roles (đầu ra của từng vai trò) và các chat sau: roles, đọc qua các bản chuyển đổi văn bản, rồi ghi thành md trong `what i know about these`. CLAUDE.md trỏ tới README của thư mục này để chat sau biết bắt đầu từ đâu.
Quy trình đọc: chuyển docx, xlsx, pdf, zip thành text bằng pandoc, pdftotext, openpyxl, PIL; xem các hình nhúng và sơ đồ bằng mắt; viết md theo từng role; đối chiếu số liệu với nguồn; ghi vào máy người dùng qua cầu nối thiết bị.

## 3. File sửa

CLAUDE.md, ba lần sửa:
- Ghi chú đầu file: thêm đoạn nói về `what i know about these/` và `session-process/`. Lý do: chat mới phải biết hai thư mục này tồn tại.
- Learned Rules: thêm một rule (2026-10-14, agileproject) bắt chat mới đọc README trước, chỉ đọc md của role cần dùng, mở file gốc trước khi trích dẫn, cập nhật md khi roles đổi, không chép thông tin xác thực mẫu. Lý do: yêu cầu rõ của người dùng. Viết bằng tiếng Việt vì rule ngôn ngữ ngày 2026-10-14, các rule cũ bằng tiếng Anh giữ nguyên.
- Session Log: thêm một dòng cho task này, chuyển dòng cũ nhất không ghim ("Sinh test case R9") sang sessionlog. Lý do: quy tắc giữ 5 dòng không ghim mới nhất. Bốn dòng STILL ghim của ngày 2026-10-11 không đụng tới.
sessionlog/agileproject.md: thêm nguyên văn dòng "Sinh test case R9" ở cuối bảng. Lý do: xoay vòng Session Log.

## 4. File thêm

Trong `what i know about these/`:
- README.md: mục đích, cách chat mới dùng, bảng cấu trúc mọi thư mục Agileproject, danh sách md, thứ tự tin cậy khi nguồn mâu thuẫn, khi nào cập nhật, danh sách điểm lệch nguồn quan trọng.
- ba.md (7 file BA), dev.md (5 file Dev gồm 8 sơ đồ), pm.md (2 file), po.md (1 file), qa.md (7 file gồm zip và bản sao R9), qalead-1-tai-lieu.md (12 file tài liệu), qalead-2-workbook.md (hai workbook R1 và R9).
Mỗi md có dòng "Độ sâu đọc" và nhãn Dữ kiện hoặc Suy luận để chat sau biết điều nào có nguồn trực tiếp.
Trong `session-process/`: file này. Thư mục session-process chưa có trước đó.
Các vòng sửa khi viết (lỗi phát hiện, nguyên nhân, cách sửa):
- ba.md: đếm mã lỗi FS 09 ra 12, đếm lại ra 13, sửa.
- pm.md và po.md: kết luận quá mạnh về split và tuổi file. Đã grep nguồn, sửa theo kết quả. Câu so sánh sprint của PO sửa lại vì top-up và cập nhật thông tin cùng sprint ở cả hai file.
- dev.md: câu về mức sẵn sàng test R9 làm nhẹ lại thành "chưa chắc đã có bản build".
- qa.md: xóa một câu suy luận không có căn cứ về khác biệt giữa test plan và CLAUDE.md.
- qalead-1-tai-lieu.md: sửa số file (14 file, 12 tài liệu). Kiểm chứng bằng grep rằng không file nào nhắc nfr draft, không file nào nhắc questions-for-client, test plan v1.0.7 không có phần ước lượng công QA.
- qalead-2-workbook.md: chép chưa đủ ba điểm mâu thuẫn của FS 09 trong Summary R9, đọc lại ô nguồn và sửa. Bỏ một suy luận về tên file FS sau khi so sánh byte cho thấy hai bản chụp giống hệt nhau.

## 5. File xóa

Không xóa file nào.

## 6. Skill dùng

- qa-course:working-protocol (gọi sớm trong chat này): quy tắc Session Log, xoay vòng dòng, evidence rule, thông báo "Đã thêm vào Session Log" và "Đã chuyển dòng".
Không dùng skill nào khác cho task này. Skill qa-course-assistant được gọi trước đó trong chat cho task security và exit criteria, không dùng lại ở đây.

## 7. Tham chiếu ngoài

Không dùng nguồn bên ngoài project. Toàn bộ nội dung lấy từ các file trong Agileproject: roles (ba, dev, pm, po, qa, qalead), groundtruth, giai-thich, CLAUDE.md và sessionlog. Thư mục "tài liệu chỉ mang tính tham khảo" chỉ được liệt kê tên, chưa đọc nội dung.

## Việc còn mở cho người dùng quyết

- Sửa 85 ô #REF! trong Summary của workbook R1 v2.1 (bảng Lens và Technique), và sheet "Changes from v1" được nhắc nhưng không tồn tại.
- File "[Agile] FS.docx" (FS đầu, nguồn F03 chuyển CPF) không còn trong roles\ba. Cần đưa lại nếu muốn kiểm nguồn.
- Test plan v1.0.7 nhắc SEC và PRQ bản v0.4, trên đĩa là SEC v0.3 và PRQ v0.5.
- Test strategy cũ (thang severity 5 mức, performance ngoài phạm vi) mâu thuẫn với test plan v1.0.7.
- Sổ giả định chưa phản ánh Finding 1 của review backlog PO.
- Nhánh R9 của cây yêu cầu vẫn ở bản cũ, cập nhật khi người dùng yêu cầu.
