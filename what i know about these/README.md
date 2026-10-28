# README: thư mục "what i know about these" và cấu trúc Agileproject

Tạo ngày 2026-10-14 theo yêu cầu của QA Lead (Cường). Viết bằng tiếng Việt theo rule ngôn ngữ trong CLAUDE.md.
Cập nhật lần 2 ngày 2026-10-14: dev.md (Database_Design đổi) và po.md (roles\po đổi file). Lần 3 cùng ngày: dev.md thêm mục 7 cho zip source Function 9. Các md còn lại giữ nguyên, trong đó pm.md và qalead-1-tai-lieu.md còn nhắc file PO v0.1 cũ như file hiện hành.
Cập nhật lần 4 ngày 2026-10-19: ba.md thêm mục 12 (FS04.docx, FS F4 v1.3) và qa.md thêm mục 11 (R4_UI_vs_FS_Compare.xlsx, R4_Test_Cases.xlsx). Các md còn lại giữ nguyên.
Cập nhật lần 5 ngày 2026-10-20: qa.md thêm mục 12 (thư mục r4_automation). Các md còn lại giữ nguyên.
Cập nhật lần 6 ngày 2026-10-21: qa.md thêm mục 13 (thư mục r9_automation) và mục 14 (sheet R8 TC trong Test_Cases_sprint_1_defects.xlsx). Các md còn lại giữ nguyên.
Cập nhật lần 7 ngày 2026-10-21: dev.md thêm mục 8 (thư mục roles\dev\code) và qa.md thêm mục 15 (FE_Merge_Conflict_Defect_Note.md). Các md còn lại giữ nguyên.
Cập nhật lần 8 ngày 2026-10-21: dev.md thêm mục 9 (đăng nhập thử trên code mới). Các md còn lại giữ nguyên.
Cập nhật lần 9 ngày 2026-10-21: qa.md thêm mục 16 (ghi chú chuyển R4 sang UI thật). Các md còn lại giữ nguyên.
Cập nhật lần 10 ngày 2026-10-21: dev.md thêm mục 10 (thư mục edugovernment-frontend) và qa.md thêm mục 17 (script run_edufams_update.cmd). Các md còn lại giữ nguyên.
Cập nhật lần 11 ngày 2026-10-21: dev.md thêm mục 11 (QA_BE.zip và hướng dẫn chạy SQL) và qa.md mục 17 bổ sung chế độ giải nén, seed, payreset. Các md còn lại giữ nguyên.
Cập nhật lần 12 ngày 2026-10-21: qa.md thêm mục 18 (R9_Test_Cases_rev_FS09.xlsx, thêm 10 case mới TC-163 đến TC-172, và ghi chú thay đổi). Các md còn lại giữ nguyên.
Cập nhật lần 14 ngày 2026-10-22: qa.md thêm mục 20 (R9 theo FS final, 153 case, 80 case chưa tự động). Các md còn lại giữ nguyên.
Cập nhật lần 14 ngày 2026-10-22: qa.md mục 19 thêm kết quả ba lần chạy thật của r9_automation và báo cáo theo từng case (reporting.py). Các md còn lại giữ nguyên.
Cập nhật lần 15 ngày 2026-10-22: dev.md thêm mục 12 (chuyển code sang codesprint1, giải nén codesprint2v1 và thiết lập script chạy một lệnh duy nhất) và cập nhật qa.md mục 20.

## 1. Thư mục này để làm gì

Chat mới không nhớ chat cũ. Thay vì đọc lại hàng chục file trong roles mỗi lần, chat mới đọc thư mục này trước. Mỗi file md giải thích nội dung của các file trong một role: file nào là gì, ai viết, ngày nào, số liệu chính, và chỗ nào các tài liệu mâu thuẫn nhau. Các file md này là bản đồ, không thay thế tài liệu gốc. Cần câu chữ chính xác, ID, số liệu để trích dẫn thì phải mở file gốc.

Nhãn dùng trong mọi md: [Dữ kiện] là điều ghi trong file nguồn, kèm tên file và mục hoặc ID. [Suy luận] là điều rút ra, kèm cách rút ra. Mỗi md ghi rõ độ sâu đã đọc ở đầu file. Hãy đọc dòng "Độ sâu đọc" trước khi tin một chi tiết.

## 2. Chat mới nên làm gì

1. Đọc CLAUDE.md ở gốc Agileproject (Project Facts, Learned Rules, Session Log).
2. Đọc README này.
3. Chọn md theo việc cần làm, chỉ đọc phần liên quan:
   - Viết test case cho R1, R8 hoặc R9, hoặc kiểm tra FS: đọc ba.md, rồi file gốc FS tương ứng trong roles\ba.
   - Hỏi về thiết kế dữ liệu, task của Dev, luồng đăng nhập, hoặc cách chạy source Function 9 local: đọc dev.md.
   - Hỏi về sprint, ưu tiên, câu hỏi mở của client, kế hoạch: đọc pm.md và po.md.
   - Hỏi về quy trình QA, test plan, entry và exit criteria: đọc qa.md và qalead-1-tai-lieu.md.
   - Làm việc với workbook R1 hoặc R9: đọc qalead-2-workbook.md.
   - Viết hay review yêu cầu security hoặc performance: đọc qalead-1-tai-lieu.md mục 7 và 8.
4. Trước khi khẳng định điều gì về yêu cầu, mở file gốc để kiểm tra. Nếu trả lời dựa vào md này, nói rõ đó là từ ghi chú và cho biết file gốc nào.
5. Khi file trong roles đổi hoặc có file mới, cập nhật md tương ứng (mục 6).

## 3. Cấu trúc thư mục Agileproject

Gốc: D:\AIQA\Agileproject. Cây dưới đây là trạng thái ngày 2026-10-14.

| Đường dẫn | Là gì | Ai viết, ai được sửa |
|---|---|---|
| CLAUDE.md | Bộ nhớ project theo Working Protocol: Project Facts, Learned Rules, Anti-patterns, Session Log. Chat nào cũng đọc đầu tiên | Chỉ người dùng được sửa Project Facts. Claude thêm Learned Rule và dòng Session Log khi người dùng yêu cầu hoặc cuối mỗi task |
| groundtruth | Nguồn sự thật của project: ảnh tender 10 requirement (592ba6ad-image.png), transcript kickoff (MOE_Finance_System_Agile_Kick-off_Transcript.md), bản tóm tắt MOE FAS dạng PDF (4bf1baf2-....pdf, giống hệt roles\ba\MOE FAS.pdf), mẫu test case và defect (Templates.xlsx, cập nhật 14/10/2026) | Người dùng cung cấp. Claude chỉ đọc. Khi mâu thuẫn, tender image đáng tin hơn transcript |
| roles | Đầu ra của từng vai trò trong team. Mỗi vai một thư mục con | Mỗi role do người đó viết. Claude chỉ đóng vai QA và QA Lead, sản phẩm của QA Lead nằm ở roles\qalead. Claude đọc các role khác làm input cho QA, không viết thay |
| roles\ba | FS R1, FS 08, FS 09, sổ TBD, MoM kickoff, câu hỏi đầu tiên, MOE FAS | BA |
| roles\dev | Thiết kế database (5 sheet: Func1, Fun3, Func4, Func8, Func9), Sprint Backlog, hai PDF luồng xác thực, flow.zip (8 sơ đồ), function9_14-10-26.zip (source code Function 9 kèm QA-README.md hướng dẫn setup), thư mục code chứa edufams-backend và edufams-frontend bản mới (thêm 2026-10-21) | Dev |
| roles\pm | Product Backlog.xlsx (25 PBI) và project-plan.md | PM. project-plan.md do Claude viết trước khi rule "không viết thay role khác" có hiệu lực |
| roles\po | Product Backlog.xlsx (giống file PM cộng 3 hàng đăng nhập không có ID) và Agile Glossary.docx. File EAFAMS_Initial_Product_Backlog_v0.1.xlsx (30 PBI) cũ không còn | PO |
| roles\qa | Test plan v1.0.7, gói Requirement analysis (zip), mẫu UAT, mẫu checkpoint, hướng dẫn Playwright, bản sao R9, tài liệu validation rule và seed data R4 bản tiếng Anh _EN (thêm 2026-10-18), bảng so sánh UI với FS và workbook test case R4 (thêm 2026-10-19), thư mục r4_automation chứa script Pytest Playwright cho R4 (thêm 2026-10-20), thư mục r9_automation chứa script Pytest Playwright cho Function 9 (thêm 2026-10-21), FE_Merge_Conflict_Defect_Note.md ghi lỗi dấu xung đột git của frontend (thêm 2026-10-21), R9_Test_Cases_rev_FS09.xlsx là workbook R9 sửa theo FS 09 kèm R9_Test_Cases_rev_FS09_changes.md (thêm 2026-10-21) | Nhóm QA |
| roles\qalead | Sản phẩm của QA Lead: sổ giả định, test strategy, SEC, PRQ, câu hỏi cho client, review backlog PO, test plan v1.0, workbook R1 và R9 | QA Lead cùng Claude |
| roles\scrummaster | Rỗng ngày 14/10/2026 | Scrum Master |
| roles (devlead) | Thư mục roles\devlead không tồn tại trên đĩa | Dev Lead |
| giai-thich | 4 file md tiếng Việt giúp người dùng hiểu tender: 01 tổng quan, 02 chi tiết 10 requirement, 03 giải thích khái niệm đã hỏi, 04 đối chiếu với hệ thống thật của Singapore (SFS, Edusave, FAS) | Claude viết để người dùng đọc hiểu. Không phải tài liệu kỹ thuật của team |
| sessionlog | agileproject.md: lưu trữ các dòng Session Log cũ đã chuyển ra khỏi CLAUDE.md | Claude, theo quy tắc xoay vòng 5 dòng mới nhất |
| session-process | Mỗi task kết thúc có một file YYYY-MM-DD_HHmm_ten-task.md gồm 7 phần (giới thiệu, kiến trúc, file sửa, file thêm, file xóa, skill dùng, tham chiếu). Theo rule toàn cục 2026-09-20 trong CLAUDE.md | Claude. Thư mục này được tạo ngày 2026-10-14 cùng lúc với thư mục what i know about these |
| what i know about these | Thư mục này | Claude, cập nhật khi roles đổi |
| tài liệu chỉ mang tính tham khảo | Tài liệu học và mẫu, không phải yêu cầu của dự án. Không dùng làm nguồn yêu cầu | Người dùng |
| tài liệu chỉ mang tính tham khảo\assignment1 | Bài tập khóa học: Analyze_Requirements, Defect_Reporting, Scope, Test_Case_Design, Test_Execution, Test_Plan, Test_Suite_Organization (docx) và TS01 đến TS09 (xlsx) | Người dùng |
| tài liệu chỉ mang tính tham khảo\AUTOMATIONTESTING HW | Bài tập tự động hóa UI: project Python Playwright và Pytest (pages, tests TS01 đến TS09, data, conftest.py, pytest.ini), thư mục hướng dẫn UI_Automation_Master_6_Sessions (6 file SESSION, README, MASTER_PROMPT và một trang HTML), ảnh chụp màn hình | Người dùng |
| tài liệu chỉ mang tính tham khảo\jmeter | Bài tập performance: Performancehw.jmx và ảnh chụp màn hình JMeter | Người dùng |
| tài liệu chỉ mang tính tham khảo\Performance_Test_Plan_Template.docx | Mẫu test plan performance | Người dùng |
| tài liệu chỉ mang tính tham khảo\Self-Enrol_Funding_Package | Gói mẫu của một bài khác: Regression_Plan_Self-Enrol_Funding.docx, Self-Enrol_Funding_Impact_Report.docx, Tender_TestCases_Defects_and_Regression.xlsx. Workbook R1 lấy định dạng từ gói này | Người dùng |

Phần "tài liệu chỉ mang tính tham khảo" tôi chưa đọc nội dung trong lần này. Mô tả ở trên dựa trên tên thư mục và tên file. Chỉ riêng gói Self-Enrol_Funding được workbook R1 nhắc làm mẫu định dạng.

## 4. Các file trong thư mục này

| File | Nội dung | Nguồn | Độ sâu đọc |
|---|---|---|---|
| ba.md | FS R1, FS 08, FS 09, FS F4 v1.1 (2026-10-18, mục 11), FS F4 v1.3 FS04.docx (2026-10-19, mục 12), sổ TBD, MoM kickoff, câu hỏi đầu, MOE FAS, danh sách mâu thuẫn trong tài liệu BA. FS03 có trên đĩa nhưng chưa có mục trong ba.md | roles\ba, 9 file | Toàn bộ chữ; FS F4 chưa xem 7 hình |
| dev.md | Database design (5 sheet, cập nhật lần 2 ngày 2026-10-14), Sprint Backlog (22 task), hai PDF xác thực, 8 sơ đồ flow.zip, zip source code Function 9 (mục 7), thư mục code bản mới (mục 8, 2026-10-21), đăng nhập thử trên code mới (mục 9), thư mục edugovernment-frontend (mục 10), QA_BE.zip và hướng dẫn chạy SQL (mục 11), chỗ lệch với FS | roles\dev, 6 mục | Toàn bộ chữ và 8 sơ đồ. Database đọc lại cả 5 sheet lần 2. Zip source đọc README và đối chiếu source, chạy phần frontend, không chạy backend |
| pm.md | Product Backlog (25 PBI, 17 OQ, 12 CD), project plan, chỗ lệch với PO | roles\pm, 2 file | Toàn bộ chữ |
| po.md | Product Backlog của PO (so từng ô với backlog PM), Agile Glossary, lịch sử file v0.1 cũ | roles\po, 2 file | Toàn bộ chữ 5 sheet và Glossary. Mục v0.1 chỉ dựa trên lần đọc đầu |
| qa.md | Test plan v1.0.7, zip Requirement analysis, mẫu UAT và checkpoint, hướng dẫn Playwright, bản sao R9, validation rule và seed data R4 (mục 10), so sánh UI với FS và test case R4 (mục 11), thư mục r4_automation (mục 12), thư mục r9_automation (mục 13), sheet R8 TC (mục 14), FE_Merge_Conflict_Defect_Note.md (mục 15), ghi chú chuyển R4 sang UI thật (mục 16), script run_edufams_update.cmd (mục 17), R9 sửa theo FS 09 (mục 18) | roles\qa, 7 file, 1 file khóa và hai thư mục r4_automation, r9_automation | Toàn bộ chữ |
| qalead-1-tai-lieu.md | Sổ giả định, review backlog PO, test strategy, nfr draft, SEC v0.3, PRQ v0.5, câu hỏi cho client, test plan v1.0 | roles\qalead, 12 file tài liệu | Toàn bộ chữ, so từng từ các cặp md và docx |
| qalead-2-workbook.md | Workbook R1 (147 case) và R9 (162 case), lỗi và điểm cần nhớ | roles\qalead, 2 xlsx | Cấu trúc, Summary, danh sách scenario. Không đọc từng ô Steps và Expected Result |

Tổng cộng 38 file trong roles đã đọc theo mức ghi trong bảng (7 ba, 6 dev, 2 pm, 2 po, 7 qa, 14 qalead), chưa kể 2 docx trong zip của qa và 8 sơ đồ trong flow.zip của dev. Zip function9 của dev (4342 file) chỉ đọc README và đối chiếu một phần source, xem dev.md mục 7.

## 5. Thứ tự tin cậy khi các nguồn mâu thuẫn

1. Rule người dùng nói trong chat, rồi CLAUDE.md.
2. Tender image (groundtruth\592ba6ad-image.png), rồi transcript kickoff.
3. Câu trả lời của client ghi trong MoM 12/10 và sổ TBD (nhãn [CR] là client đã xác nhận).
4. FS của BA (FS R1, FS 08, FS 09). Theo FS 08 mục 1, khi FS mâu thuẫn thì Decision Log đứng trước, nhưng Decision Log không có trong roles.
5. Backlog PM, backlog PO, Sprint Backlog của Dev. Đây là kế hoạch, không phải yêu cầu.
6. Tài liệu QA Lead (SEC, PRQ, test plan, strategy, sổ giả định). Đây là đề xuất, chưa client duyệt.
7. Tài liệu tham khảo.

[Suy luận] Thứ tự 4 đến 6 là do tôi sắp xếp dựa trên nhãn trạng thái trong các file (FS ghi Final hoặc Draft, SEC và PRQ ghi Draft proposal, backlog ghi "proposal"). Người dùng chưa duyệt thứ tự này.

## 6. Khi nào cập nhật thư mục này

- Có file mới hoặc file đổi trong roles: cập nhật md của role đó, ghi ngày và độ sâu đọc mới.
- Người dùng xác nhận một giả định hay trả lời một câu hỏi mở: sửa các dòng liên quan trong md.
- Phát hiện lỗi trong md này: sửa ngay và ghi trong Session Log.
- Không ghi mật khẩu hay thông tin xác thực mẫu có trong tài liệu gốc vào md. Chỉ ghi rằng chúng tồn tại.
- Không dùng dấu gạch dài hay gạch nối làm dấu câu. Dùng dấu "-" chỉ cho ký hiệu danh sách.

## 7. Những điểm lệch nguồn quan trọng nhất (chi tiết ở md trong ngoặc)

- Thanh toán chia đôi (split payment): FS 09 có trong Sprint 1, còn Sprint Backlog (TSK-R9-05) và TBD-06 hoãn, zip Requirement analysis (R9 G4) đề xuất không làm ở Sprint 1. (ba.md, dev.md, qa.md, qalead-2-workbook.md)
- Số tiền của hai phần trong split: FS 09 tự mâu thuẫn giữa Step 4, BR-F9-02 và AC-22, BR-F9-10. (ba.md, qalead-2-workbook.md)
- Thời hạn phiên: FS 08 ghi 15 phút, FS 09 ghi 10 phút (TBC), PDF Dev ghi Redis TTL 30 ngày và Access Token 15 phút, SEC đề xuất 30 phút idle. (ba.md, dev.md, qalead-1-tai-lieu.md)
- Ngày đóng tài khoản: sổ giả định ghi 1 ngày trước sinh nhật 16 hoặc ngay khi mất quốc tịch, zip và FS R1 ghi đúng 16 tuổi. (qalead-1-tai-lieu.md, ba.md)
- Chuyển số dư sang CPF: client đã xác nhận cần có, FS R1 hoãn, F03 của FS đầu được giữ trong workbook R1, Dev có TSK-R1-04. (ba.md, dev.md, qalead-2-workbook.md)
- Sprint của R9: backlog PM và backlog PO hiện tại đều đặt Sprint 1. Chỉ file PO v0.1 cũ (không còn trên đĩa) đặt Sprint 2. Backlog PO hiện tại giống PM, thêm 3 hàng đăng nhập không có ID. (pm.md, po.md)
- Đơn vị của một đơn FAS: Glossary của PO và PB-18 nói theo hộ gia đình (family unit), còn thiết kế Func4 của Dev nói mỗi học sinh một đơn mỗi năm học. (po.md, dev.md)
- Trợ cấp FAS và hóa đơn: sheet Func4 (mới) tính trợ cấp cho từng khoản phí và F9 lưu snapshot vào invoice_items.SubsidyAmount. FS-04 và Decision Log D-10 đến D-34 mà Func4 dựa vào không có trong roles. (dev.md)
- Test plan v1.0.7 nhắc SEC và PRQ bản v0.4, trên đĩa là SEC v0.3 và PRQ v0.5, mô tả không khớp. (qa.md, qalead-1-tai-lieu.md)
- Thang severity: test strategy dùng 5 mức, test plan và workbook dùng S1 đến S4. (qalead-1-tai-lieu.md)
- Workbook R1 v2.1: Summary có 85 ô lỗi #REF! (bảng Lens và Technique), nhắc sheet "Changes from v1" không tồn tại. (qalead-2-workbook.md)
- File "[Agile] FS.docx" (FS đầu, nguồn F03 chuyển CPF) không còn trong roles\ba. (qalead-2-workbook.md)
- Decision Log D-xx mà FS 08 dựa vào không có trong roles. (ba.md)
- Ba file của roles\qa (QA_Checkpoints_Funding, UAT_Case, UAT_Report) thuộc hệ thống khác, chỉ dùng làm mẫu định dạng. (qa.md)
