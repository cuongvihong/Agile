# Role qalead, phần 2: hai workbook test case R1 và R9

Nguồn: D:\AIQA\Agileproject\roles\qalead\r1-education-account-test-cases-v2.1.xlsx và r9-outstanding-fees-payment-test-cases-v1.0.xlsx. Đọc ngày 2026-10-14.
Độ sâu đọc: mở bằng openpyxl, đọc cấu trúc 7 sheet của R1 và 8 sheet của R9, đọc toàn bộ sheet Summary, đọc tiêu đề và dòng đầu của từng sheet, đọc danh sách 31 scenario R1 và 26 scenario R9, tính lại các số đếm trực tiếp từ sheet Test cases của R9. Không đọc từng ô Steps và Expected Result của 147 case R1 và 162 case R9 trong lần này. Cần nội dung từng case thì mở workbook, đừng dựa vào file này.
Nhãn: [Dữ kiện] là điều thấy trong workbook, kèm tên sheet. [Suy luận] là điều tôi rút ra, kèm cách rút ra.
Cả hai workbook là sản phẩm của QA Lead, làm cùng Claude trong các phiên trước. Chưa case nào được chạy.

## 1. Quy tắc chung của cả hai workbook

[Dữ kiện] Review Status (hay Status) gồm Approve, Draft, Block, Reject. Approve nghĩa là expected result có nguồn rõ (FS, tender hoặc câu trả lời của client) hoặc giả định đã được giải quyết, khi đó Assumption Ref là N/A. Draft nghĩa là expected result dựa trên giả định còn mở, Assumption Ref ghi giả định và nguồn của nó. Block nghĩa là có thông tin nhưng không giả định nào giải quyết được (FS ghi Deferred hoặc hai nguồn mâu thuẫn). Reject nghĩa là không có expectation kiểm thử được, không viết Steps. Nguồn của quy tắc: người dùng 14/10/2026, ghi trong Learned Rules của CLAUDE.md. Ranh giới Block và Reject còn chờ người dùng xác nhận (đã ghi trong CLAUDE.md).
[Dữ kiện] Mọi giả định có ID (ASM-R1-xx, ASM-R9-xx), lý do, hậu quả nếu sai, trạng thái và một câu hỏi để xác nhận. Sheet Questions có 3 cột: Assumption Ref, Question, Answer. Cột Answer đang trống ở cả hai workbook, tức chưa câu hỏi nào có trả lời.
[Dữ kiện] Thang severity 1 đến 4 theo test plan v1.0.7. Priority Critical, High, Medium, Low. Mọi case chưa chạy: R1 ghi Not Executed ở cột Actual Result, R9 ghi Not Run ở cột Execution Status.
[Dữ kiện] Hai workbook loại trừ performance và security (R1 ghi rõ, thuộc PRQ và SEC). Dữ liệu student là dữ liệu tổng hợp.

## 2. r1-education-account-test-cases-v2.1.xlsx

[Dữ kiện] Tiêu đề: "R1 Education Account Test Cases v2.1" cho tender R1, baseline FS R1 V1.0 (file [Agile] FS R1V1.0.docx, nhãn nội bộ Version 1.2) và F03 của FS đầu tiên. Ngày version 2.1: 14/10/2026.
Bảy sheet: Summary, TestCases (A1:W148, 23 cột, 147 case), Scenarios (31 scenario), Checkpoint (24 checkpoint CP-R1-01 đến CP-R1-24), Assumptions (47 giả định ASM-R1-01 đến 47), Questions (44 câu hỏi), FS Trace (73 dòng, gồm 54 mục FS R1 V1.0 và 19 mục của FS đầu tiên).
Số liệu từ sheet Summary:
- Theo Status: Approve 88, Draft 50, Block 6, Reject 3, tổng 147.
- Theo Priority: Critical 33, High 74, Medium 36, Low 4. Theo Severity: 1 có 33, 2 có 76, 3 có 36, 4 có 2.
- Theo Sprint: Sprint 1 có 130 (Approve 88, Draft 38, Block 4), TBD có 17 (Draft 12, Block 2, Reject 3).
- Theo Test Type: Functional 94, Integration 53. Theo Type: positive 56, negative 46, boundary 27, exception 18.
- Giả định: Open 30, Resolved 8, Superseded 6, Not adopted 2, Agreed 1, tổng 47. Câu hỏi 44, chưa câu nào có trả lời.
- Checkpoint: Clear 5, Assumed 13, Open 6, tổng 24. FS R1 V1.0 54 mục, cả 54 đều có ít nhất một case trích dẫn.
Các scenario đáng chú ý (sheet Scenarios): SCN-R1-01 tạo tài khoản vào sinh nhật thứ 7 (BVA), SCN-R1-13 đóng ở sinh nhật thứ 16 khi truy cập backend, SCN-R1-14 số dư đóng chuyển sang CPF (12 case), SCN-R1-15 giao dịch pending khi đóng (2 case Reject), SCN-R1-18 và 19 quốc tịch nhận sau 7 hoặc mất trước 16, SCN-R1-20 công dân rời nước (Block), SCN-R1-22 ngoại lệ sau 16 (Reject), SCN-R1-24 đồng bộ ban đầu, SCN-R1-26 lỗi Government API và phục hồi job, SCN-R1-28 đến 31 kiểm tra đóng tài khoản ở mọi thao tác backend và trạng thái Closure Deferred.
[Dữ kiện] Quyết định của người dùng ngày 14/10 ghi trong Summary: F03 của FS đầu tiên ([Agile] FS.docx mục 1.3 và Closure Transfer Record mục 2.4) vẫn là quy tắc chuyển CPF, vì FS R1 V1.0 đã bỏ phần đó. Scenario 14 có 12 case (5 chuyển từ Block sang Draft, 7 mới), thêm ASM-R1-42 đến 47 và 6 câu hỏi.
[Dữ kiện] Ngày chạy: case tạo tài khoản dùng 15/10/2026, case đóng tài khoản dùng 28/10/2026. NRIC test có chữ T, bảy chữ số bắt đầu bằng 99.

Điều cần biết trước khi dùng hoặc gửi workbook này (đều quan sát được, tôi chưa sửa):
- [Dữ kiện] Sheet Summary có 85 ô lỗi #REF!. Hai bảng "Status by Lens" (hàng 55 đến 67) và "Status by Technique" (hàng 77 đến 84) dùng công thức COUNTIFS trỏ vào TestCases!#REF!. Nguyên nhân quan sát được: sheet TestCases không còn cột Lens và Technique (hai cột này nằm trong sheet Scenarios). [Suy luận] Cột bị bỏ khi đổi mẫu sang định dạng mới (TestCases hiện có 23 cột, trong khi Summary mục "Rules applied" nói mẫu 26 cột), dựa trên việc Summary còn hai bảng dựa vào cột đã không còn. Bảng Status by Type (hàng 69 đến 75) vẫn đúng. Các bảng khác trong Summary và các sheet còn lại không có ô lỗi (đã quét).
- [Dữ kiện] Summary nhắc "sheet Changes from v1", nhưng workbook không có sheet này.
- [Dữ kiện] Summary dùng "[Agile] FS.docx" (FS đầu tiên, đã được thay) làm nguồn cho CPF Transfer. File này không còn trong roles\ba trên máy người dùng (danh sách thư mục ngày 14/10/2026 có 7 file, không có tên này). Một bản chụp của nó (1,482,085 byte) còn trong thư mục làm việc tạm của phiên chat hiện tại, nhưng thư mục đó không giữ lại cho chat sau. Chat sau cần kiểm lại nguồn CPF thì phải hỏi người dùng đưa lại file.
- [Dữ kiện] Ghi chú quy tắc "Output follows the Self-Enrol Funding workbook: 26 column TestCases sheet". Mẫu này nằm ở "tài liệu chỉ mang tính tham khảo\Self-Enrol_Funding_Package". Số cột 26 không khớp 23 cột hiện có.

## 3. r9-outstanding-fees-payment-test-cases-v1.0.xlsx

[Dữ kiện] Tiêu đề: "R9 Outstanding Fees and Payment: Test Cases v1.0". Phạm vi: functional và integration cho Function 9 của e-Service Portal. Baseline: FS Function 9 Final ngày 14/10/2026 (BA). Format theo groundtruth\Templates.xlsx cập nhật 14/10/2026.
Tám sheet: "Test cases " (tên có dấu cách cuối, A1:AG957 nhưng chỉ 162 dòng có dữ liệu), Defect Reports (chỉ có dòng tiêu đề, chưa có defect), Summary, Scenarios (26 scenario TS-001 đến TS-026), Assumptions (38 giả định ASM-R9-xx), Questions (34), FS Trace (84 mục FS), Seed Data (khoảng 80 dòng).
Cột sheet Test cases: ID, Scenario ID, Title, Test Suite, Page, Severity, Priority, Execution Status, Test Type, Environment, Preconditions, Test Data, Test Steps, Expected Result, Actual Result, Assumption Ref, Defect ID, Traceability, Note, Review Status.
Số liệu tôi tính lại trực tiếp từ sheet Test cases:
- 162 case TC-001 đến TC-162. Review Status: Approve 105, Draft 56, Block 1. Execution Status: Not Run 162.
- Severity: S1 62, S2 60, S3 36, S4 4. Priority: Critical 62, High 60, Medium 36, Low 4.
- Test Type: Functional 96, Integration 31, API 15, Security 13, UI 5, Non-functional 2.
- Theo suite: F9.3 Payment method and eligibility 28, F9.7 Result, receipt and retry 20, Data rules and constraints 18, F9.1 Access and child list 17, F9.2 Outstanding invoices and EA balance 17, F9.4 Pay with Education Account 14, F9.4 and F9.5 Split payment 14, F9.6 Webhook and reconciliation 14, F9.4 and F9.5 Idempotency and concurrency 10, F9.5 Pay online 10.
- Giả định: 38, trong đó Open 34 và Resolved 4. Loại: Rule 19, Environment 6, Config 4, Data 4, UI 3, Dependency 1, Gap 1.
[Dữ kiện] Các ô số đếm trong Summary là công thức COUNTA và COUNTIF trên 'Test cases '!A2:A163 và các cột tương ứng, file chưa lưu giá trị tính sẵn. Mở trong Excel sẽ tự tính. Công cụ đọc không tính công thức sẽ thấy ô trống.
Điều cần biết trước khi chạy test R9 (từ mục "Points to know before executing" của Summary, [Dữ kiện]):
- ID TC-### và TS-### bắt đầu lại ở mỗi workbook, nên TC-001 của R9 trùng chữ với TC của workbook khác nếu gộp.
- FS 09 Final có split payment trong Sprint 1, còn Sprint Backlog TSK-R9-05 và TBD-06 hoãn split. Xem ba.md và dev.md.
- FS tự mâu thuẫn ở ba điểm làm đổi nhiều case, các case bị ảnh hưởng đều là Draft: (1) Parent có được giảm phần EA của split hay không, ASM-R9-01 (Step 4 và BR-F9-02 nói phần EA là toàn bộ số dư khả dụng và Parent không nhập, còn DA-08, BR-F9-10, bảng trường SCR-04 và AC-22 nói Parent chọn được số tiền; workbook theo AC-22 vì có ví dụ tính: phần EA bắt đầu bằng toàn bộ số dư, Parent giảm xuống bất kỳ giá trị lớn hơn 0 và nhỏ hơn số phải trả, phần online bằng số phải trả trừ phần EA). (2) Có đưa ra lựa chọn split khi số dư đủ trả hóa đơn hay không, ASM-R9-02. (3) SCR-02 liệt kê những trạng thái hóa đơn nào, ASM-R9-03.
- FS không mô tả màn hình, API hay quy trình để Operations xử lý payment ở trạng thái ReconciliationRequired, nên case này là case Block duy nhất của workbook (ASM-R9-22).
- Một số giá trị thời gian còn TBC trong FS: session portal (giả định 10 phút), session nhà cung cấp (10 phút), ngưỡng Pending, chu kỳ polling. Workbook dùng giá trị Dev cấu hình ở SIT (ASM-R9-05 đến 07).
- [Dữ kiện] Sheet Summary ghi nguồn FS là "roles/ba, file [Agile] FS (1).docx". Trên máy người dùng file hiện tên [Agile] FS 09.docx. Hai bản chụp từng được tải về phiên làm việc ("[Agile] FS (1).docx" và "[Agile] FS 09.docx") giống hệt từng byte (cmp, 829,498 byte), nên đây là cùng một file đã đổi tên.
- Bản sao: roles\qa\R9_Test_Cases.xlsx giống hệt từng byte với file này. Bản trong roles\qa đang mở trong Excel (có file khóa), không ghi đè.

## 4. Gợi ý khi chat sau cần làm việc với hai workbook

- Muốn thêm, sửa case: làm trên bản trong roles\qalead, giữ 7 hoặc 8 sheet và công thức. Với R1, nếu người dùng đồng ý, sửa lại hai bảng Lens và Technique trong Summary để trỏ đúng sheet Scenarios, hoặc bỏ hai bảng. Hỏi người dùng trước khi sửa.
- Khi BA trả lời một câu hỏi: đặt State của giả định thành Resolved, đặt Assumption Ref của case thành N/A, đổi Status thành Approve, rồi cập nhật Questions.
- Quy tắc mới của người dùng: khi xuất tài liệu cho người khác thì không nhắc bài học (Lesson), chỉ trích tender, backlog, FS.
- Cây yêu cầu R1 đến R10 trên artifact https://claude.ai/artifact/XjQeaHuJiYZHuNQUJ8GDdZ cần cập nhật khi có fact mới, nhưng ngoài phần R9 hiện cũ, chỉ cập nhật khi người dùng yêu cầu (CLAUDE.md).
