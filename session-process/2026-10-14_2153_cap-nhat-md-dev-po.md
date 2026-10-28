# Session process: cập nhật dev.md và po.md theo ba file roles đổi

Ngày 2026-10-14, kết thúc lúc 21:53 (giờ Việt Nam). Project: Agileproject, tag agileproject. Viết bằng tiếng Việt theo rule ngôn ngữ ngày 2026-10-14 trong CLAUDE.md.

## 1. Giới thiệu

Người dùng (Cường, QA Lead) yêu cầu đọc CLAUDE.md và toàn bộ tài liệu theo hướng dẫn để nắm context. Khi đọc, tôi thấy ba file trong roles mới hơn các md bản đồ trong `what i know about these`: Database_Design__Function_Specification.xlsx (roles\dev), Product Backlog.xlsx và Agile Glossary.docx (roles\po, file EAFAMS_Initial_Product_Backlog_v0.1.xlsx không còn). Theo Learned Rule ngày 2026-10-14 (cập nhật md khi roles đổi), tôi hỏi và người dùng trả lời "có". Task này cập nhật dev.md, po.md, vài dòng cũ trong README, thêm dòng Session Log và file này.
Chat này đã làm các việc khác trước đó (đọc CLAUDE.md và bản đồ). File này chỉ ghi task cập nhật.

## 2. Kiến trúc

Không đụng code hay hệ thống. Task sửa lớp tri thức `what i know about these` (bản đồ của roles) cho khớp với nguồn mới. Thứ tự: xác định file nào đổi bằng ngày sửa file trên đĩa so với thời điểm viết bản đồ, đọc lại nguồn, đối chiếu với md cũ, viết lại phần sai, ghi vào máy người dùng qua cầu nối thiết bị.
Cách đọc: openpyxl đọc từng ô của các xlsx (kể cả công thức), pandoc trích chữ docx, so sánh ô theo ô hai bản Product Backlog (PO và PM) sau khi ghép thẳng hàng với 3 hàng lệch.

## 3. File sửa

- what i know about these/dev.md: viết lại mục 2 (Database_Design) vì file Dev đổi. Sửa dòng nguồn và độ sâu đọc (ghi rõ lần 2 chỉ đọc lại Database_Design), bảng tổng hợp, và dòng ở mục 3 nhắc "đánh số của file PO v0.1 khác hẳn". Lý do từng chỗ: số liệu cũ sai (Balance và Amount nay là DECIMAL chứ không phải BIGINT, Transactions.Id nay là UUID, Fun3 nay có đủ cột thay vì chỉ tên bảng), thêm sheet Func4 và bảng Sync Job Log. Các nhận xét cũ không còn đúng được viết lại: mâu thuẫn BIGINT với DECIMAL đã hết, ghi chú "Niên khóa" của Cohorts không còn vì Cohorts bị thay bằng academic_levels. Func8 bỏ mẫu cũ Parent's Details nên bỏ mô tả đó. Các điểm còn đúng giữ lại (không có FundingReference, không có số tài khoản, ghi chú R8 lệch với FS 08).
- what i know about these/po.md: viết lại toàn bộ vì thư mục roles\po đổi file. Giữ một mục lịch sử ngắn về file v0.1 cũ (đánh dấu chỉ dựa lần đọc đầu, không kiểm lại được), vì review của QA Lead trong roles\qalead vẫn nói về file đó.
- what i know about these/README.md: sửa các chỗ sau: dòng roles\dev, dòng roles\po, hai dòng trong bảng md (dev.md, po.md), tổng số file (36 thành 37, po từ 1 thành 2), mục "Sprint của R9" (nay hai backlog cùng Sprint 1), thêm hai điểm lệch nguồn mới (đơn vị của đơn FAS; FS-04 và Decision Log không có trong roles), và một dòng ghi ngày cập nhật lần 2.
- CLAUDE.md: chỉ sửa phần Session Log: thêm một dòng cho task này, chuyển dòng cũ nhất không ghim ("Đọc hai file PDF Dev gửi trong roles/dev") sang sessionlog. Bốn dòng STILL ghim của ngày 2026-10-11 không đụng tới. Không sửa phần nào khác.
- sessionlog/agileproject.md: thêm nguyên văn dòng "Đọc hai file PDF Dev gửi trong roles/dev" ở cuối bảng. Lý do: xoay vòng Session Log (giữ 5 dòng không ghim mới nhất).
Vòng sửa khi viết:
- Dòng cuối mục Func4 trong dev.md ban đầu viết "backlog chưa có task cho FAS (R4 chỉ có TSK-R4-01 và R4-02)", tự mâu thuẫn. Sửa lại thành mô tả đúng: Sprint_Backlog có 2 task R4, chưa rõ có phủ thiết kế Func4 hay không.
- po.md bản nháp có hai câu khẳng định "đã tìm" mà tôi chưa chạy tìm (cột PBI Ref của Sprint_Backlog, workbook Agile requirements). Đã bỏ câu thứ nhất thành suy luận, câu thứ hai chạy tìm theo tên file trong roles rồi mới ghi.

## 4. File thêm

- session-process/2026-10-14_2153_cap-nhat-md-dev-po.md: file này, theo rule toàn cục ngày 2026-09-20.
Không thêm md bản đồ mới.

## 5. File xóa

Không xóa file nào. Không commit hay push gì.

## 6. Skill dùng

- qa-course:working-protocol (đã gọi sớm trong chat này): quy tắc Session Log (5 dòng không ghim mới nhất, dòng STILL ghim), cách xoay vòng sang sessionlog, thông báo "Đã thêm vào Session Log" và "Đã chuyển dòng", evidence rule (phân biệt dữ kiện và suy luận, nêu bằng chứng cho phần vắng mặt).
Không dùng skill nào khác.

## 7. Tham chiếu ngoài

Không dùng nguồn bên ngoài project. Nguồn gồm các file trong Agileproject: roles\dev\Database_Design__Function_Specification.xlsx, roles\po\Product Backlog.xlsx, roles\po\Agile Glossary.docx, roles\pm\Product Backlog.xlsx (để so sánh), và các md bản đồ cũ.

## Việc còn mở cho người dùng quyết

- pm.md (đầu file và mục 4) và qalead-1-tai-lieu.md (bảng tài liệu, mục review backlog PO) vẫn nhắc roles\po\EAFAMS_Initial_Product_Backlog_v0.1.xlsx như file hiện hành. Chưa sửa vì người dùng chỉ duyệt dev.md và po.md. Đã ghi chú trong po.md và README.
- Hỏi Dev: kiểu Citizenship (NVARCHAR(50) ở Func1 nhưng ENUM Student_Citizenships ở Func3 và Func4), các cột nhắc trong ràng buộc của fee_publications nhưng thiếu trong danh sách cột, độ chính xác DECIMAL của Func1, giá trị của job_name và trigger_type trong Sync Job Log.
- Hỏi PO và BA: ba hàng đăng nhập không có ID (tách riêng hay gộp vào PB-03 và PB-06), đơn FAS tính theo hộ hay theo từng con (Glossary và PB-18 so với Func4 D-25), vị trí workbook "Agile requirements" mà Glossary nhắc.
- Các việc mở cũ vẫn giữ: bốn dòng STILL ngày 2026-10-11, 85 ô #REF! trong workbook R1, nhánh R9 của cây yêu cầu, định nghĩa Block và Reject, ba assumption ASM-R9-01 đến 03, file "[Agile] FS.docx" không còn.
