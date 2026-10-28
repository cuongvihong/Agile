# Role qalead, phần 1: tài liệu kế hoạch, yêu cầu phi chức năng, sổ giả định

Nguồn: D:\AIQA\Agileproject\roles\qalead. Role qalead có 14 file, phần này nói về 12 file tài liệu (docx, md, txt). Hai workbook test case R1 và R9 nằm ở qalead-2-workbook.md. Đọc ngày 2026-10-14.
Độ sâu đọc: đọc toàn bộ chữ của security-requirements, performance-requirements, test-plan-final-v1.0, test-strategy, nfr-draft, assumptions register, po-backlog-review, questions-for-client-short. Với 4 cặp md và docx (register, nfr draft, po review, test strategy) tôi so từng từ hai bản, nội dung giống nhau, chỉ khác dấu câu (docx đã bỏ dấu gạch dài) và tên file được tham chiếu (md ghi .md, docx ghi .docx).
Nhãn: [Dữ kiện] là điều ghi trong file nguồn, kèm tên file và mục hoặc ID. [Suy luận] là điều tôi rút ra, kèm cách rút ra.
File này là bản đồ. Cần câu chữ hoặc số liệu chính xác thì đọc lại file gốc.

## 1. Role qalead là gì

Role qalead chứa tài liệu do QA Lead (người dùng, tên Cường) soạn: kế hoạch và chiến lược kiểm thử, sổ giả định cần thương lượng với client, yêu cầu security và performance, bản review backlog của PO, danh sách câu hỏi cho client, và hai workbook test case (R1, R9). Đây là nơi Claude ghi sản phẩm QA Lead của chính mình. Khi tạo file mới cho QA Lead thì đặt ở đây.

## 2. Bảng tổng hợp

| File | Là gì | Mã, phiên bản, ngày | Còn dùng không |
|---|---|---|---|
| assumptions-negotiation-register (.docx và .md) | Sổ giả định và điểm cần thương lượng, 2 bảng | ANR-MOE-FINANCE-001, cập nhật 11/10 | Còn dùng, nhưng chưa phản ánh vài kết luận về sau (mục 3) |
| po-backlog-review (.docx và .md) | QA Lead nhận xét backlog PO v0.1, 5 finding | Không ghi mã. Nhật ký Session Log ghi 11/10 | Lịch sử, backlog PM đã thay backlog PO |
| test-strategy (.docx và .md) | Chiến lược kiểm thử toàn dự án | TS-MOE-FINANCE-001, không ghi ngày | Cũ hơn test plan, có chỗ mâu thuẫn (mục 5) |
| nfr-security-performance-draft (.docx và .md) | Bản nháp đầu yêu cầu security và performance cho Dev | Không ghi mã, 11/10 theo Session Log | Đã bị thay bởi SEC và PRQ (mục 6) |
| security-requirements.docx | Yêu cầu security và exit criteria cho R1, R3, R8, R9 | SEC-MOE-FINANCE-001, version 0.3, 12/10 | Bản mới nhất trên đĩa |
| performance-requirements.docx | Yêu cầu performance và exit criteria cho R1, R3, R8, R9 | PRQ-MOE-FINANCE-001, version 0.5, 13/10 | Bản mới nhất trên đĩa |
| questions-for-client-short.txt | 20 câu hỏi cho buổi làm việc với client | QA Lead, 12/10 | Còn dùng, đã bỏ câu client trả lời |
| test-plan-final-v1.0.docx | Test plan v1.0 gửi client | "Draft 1", bìa ghi 19/08/2026, lịch sử ghi 12/10/2026 | Cũ hơn v1.0.7 trong roles\qa |

Tên file "test-plan-final" dễ gây hiểu nhầm. [Dữ kiện] Lịch sử bản trong file chỉ có version 1.0. Test plan mới hơn là version 1.0.7 trong roles\qa, xem qa.md.

## 3. assumptions-negotiation-register (ANR-MOE-FINANCE-001)

[Dữ kiện] Chủ sở hữu QA Lead. Dựng từ ảnh tender (groundtruth\592ba6ad-image.png) và transcript kickoff. Hai bảng tách riêng, mỗi mục chỉ nằm trong một bảng.
Bảng 1 Blocking Register, 10 dòng, xếp theo mức chặn toàn dự án: (1) sandbox SingPass và AD/SSO chưa xác nhận, Critical. (2) không có payment gateway trong tender, Critical. (3) API thu nhập bên thứ ba, Critical. (4) không có phần out of scope trong tender, High. (5) R7 mô phỏng chỉ xem hay được hành động thay user, High. (6) mô hình ML chỉ khuyến nghị hay tự quyết, High. (7) chưa nêu hệ thống nguồn DOB và quốc tịch, High. (8) R1 đã xác nhận một phần ngày 11/10: tài khoản deactivate 1 ngày trước khi đủ 16 tuổi hoặc ngay khi mất quốc tịch, còn mở là tạo tài khoản khi nhận quốc tịch sau 7 tuổi và số dư, High. (9) có pha UAT riêng sau Sprint 3 không, Medium. (10) nguồn tiền top-up không được mô hình hóa, High.
Bảng 2 Business Impact Register, 11 dòng, xếp theo hậu quả nếu giả định sai: (1) có cần rà soát PDPA không, Critical. (2) số dư khi đóng tài khoản, High. (3) FAS khi anh chị em học khác trường, High. (4) một đơn FAS cho cả nhà tự áp dụng cho mọi con hay xác nhận từng con, High. (5) toán tử rule top-up theo lô và "schooling status" chưa định nghĩa, Medium. (6) ai cấu hình mức phí, Medium. (7) chặn cứng khi vượt ngân sách FAS hay chỉ báo cáo, Medium. (8) cách chia khi trả kết hợp số dư và online, Medium. (9) chatbot có được giải thích điều kiện FAS không, Medium. (10) OCR cho đơn giấy, Low. (11) trả một lần cho nhiều con, Low.
Ghi chú tham chiếu thực tế: [Dữ kiện] hệ thống Edusave thật đóng tài khoản ở 17 tuổi hoặc khi rời trường MOE, và chuyển số dư sang PSEA. Tender đóng ở 16 và không có tài khoản nối tiếp, nên ghi chú này chỉ là gợi ý mặc định cho PO.
Điều cần nhớ khi dùng:
- [Dữ kiện] Bảng 1 hạng 1 đến 3 vẫn xếp Critical dù po-backlog-review Finding 1 chỉ ra backlog PO coi SingPass, income API, payment là mô phỏng. Ghi chú thực tế cuối sổ có nhắc "simulated per PO's backlog" nhưng bảng chưa đổi mức. [Suy luận] Chưa sửa, đúng như review ghi "I have not changed the register yet", dựa trên việc so Bảng 1 trong register với Finding 1.
- [Dữ kiện] Quy tắc 1 ngày trước 16 tuổi ở bảng 1 hạng 8 khác với zip Requirement analysis R1 (đóng khi đủ 16 tuổi) và test-plan-final v1.0 mục 5 (hỏi 16 hay ngày trước). Cần đối chiếu với FS R1 (role ba) và TBD register trước khi viết expected result về ngày đóng.
- [Dữ kiện] Sổ tham chiếu groundtruth\592ba6ad-image.png, giai-thich\04-doi-chieu-thuc-te.md và "roles/qalead/test-plan.md mục 2.3". Hai file đầu có trên đĩa. File test-plan.md không có trong roles\qalead (đã đối chiếu danh sách thư mục ngày 14/10). Test plan hiện có là docx với đánh số mục khác. Tham chiếu mục 2.3 không dùng được.

## 4. po-backlog-review

[Dữ kiện] Review file roles\po\EAFAMS_Initial_Product_Backlog_v0.1.xlsx (30 PBI), viết trước buổi estimation "chiều nay". Kết luận chung: cấu trúc tốt, có thể estimate sau khi xử lý các finding.
- Finding 1: backlog nói rõ đây là training prototype với tích hợp mô phỏng, nên 3 item Critical trong register nên hạ thành quyết định thiết kế nội bộ. Chưa sửa register, cần PM và PO xác nhận.
- Finding 2: PB-09 và PB-10 (Must) phụ thuộc PB-08 (Should) trong Sprint 2. Nên nâng PB-08 hoặc ghi rõ nó là Must thực tế.
- Finding 3: cả 6 PBI FAS (PB-18 đến PB-23) dồn vào Sprint 3, không có sprint đệm.
- Finding 4: câu hỏi của PB-21 (kích hoạt auto-grant bằng đơn nộp hay chủ động) chưa có trong register, nên thêm vào Bảng 1.
- Finding 5: PB-04 và PB-05 (Track B) phụ thuộc PB-03 (Track A) ngay trong Sprint 1, nên chốt hợp đồng API sớm hơn dự kiến.
[Dữ kiện] Finding 3 viết "4 trong số đó là Pending clarification" nhưng liệt kê 5 ID (PB-18, 19, 21, 22, 23). Tôi đối chiếu với backlog PO: cả 5 đều là Pending clarification, vậy con số 4 là lỗi đếm trong review. Các PB-xx trong review là số của backlog PO, khác số của backlog PM (xem po.md).

## 5. test-strategy (TS-MOE-FINANCE-001)

[Dữ kiện] Tài liệu chiến lược cấp dự án, 10 mục: mục tiêu chất lượng, test level và người chịu trách nhiệm, loại test, ưu tiên theo rủi ro, chuẩn thiết kế test, cách kiểm thử AI/ML, severity và priority, môi trường và dữ liệu, metric, quan hệ với tài liệu QA khác. Điểm chính: nguyên tắc rule-based trước, ML test như phân loại, chatbot và auto-fill test theo guardrail; mọi đầu ra AI làm đổi kết quả tài chính tối thiểu là Major; dữ liệu test phải là dữ liệu tổng hợp; priority P1 đến P4.
Chỗ mâu thuẫn với tài liệu mới hơn (đều là [Dữ kiện] có nguồn):
- Severity: strategy dùng thang Blocker, Critical, Major, Minor, Trivial (mục 7, theo "test-plan.md 2.5"). Test plan v1.0.7 dùng S1 đến S4 (Critical là S1, High là S2, Medium là S3, Low là S4). Workbook R1 và R9 dùng S1 đến S4 hoặc 1 đến 4.
- Performance: strategy mục 3 ghi "out of scope for the 3 sprint cycle". PRQ v0.5 và test plan v1.0.7 mục 3.9 có yêu cầu và kịch bản performance cho R1, R3, R8, R9.
- UAT: strategy ghi UAT chưa xác định. Test plan v1.0.7 ghi UAT client ngày 02/11.
- Tham chiếu "test-plan.md" các mục 2.2, 2.3, 2.5, 2.9, 3.2, 5.1 không còn khớp file hiện có.
[Suy luận] Strategy là bản cũ nhất của nhóm tài liệu QA Lead, dựa trên so ngày (strategy không ghi ngày, ghi nhận Track A và Track B theo project plan đầu) và việc test plan v1.0.7, PRQ và SEC đều mới hơn. Khi mâu thuẫn, ưu tiên test plan v1.0.7, SEC, PRQ.

## 6. nfr-security-performance-draft

[Dữ kiện] Bản nháp "DRAFT / PROPOSAL by QA Lead" gồm Phần 1 performance (5 flow: top-up theo lô, FAS, SingPass login và xem tài khoản, xem và trả phí, mô phỏng HQ; P95 2 đến 5 giây, P99 4 đến 8 giây, lỗi tối đa 1 phần trăm; top-up 1,000 tài khoản trong 10 phút; 50 VU, chỉ Benchmark/Load; khoảng 500 tài khoản, 10 trường) và Phần 2 security (5 nhóm: Authentication, Authorization, Sensitive Data, Session, Access Control; timeout 30 phút; thêm kiểm soát ngoài course, gắn nhãn External). Có 5 giả định A-P1 đến A-P3, A-S1, A-S2.
[Suy luận] Bản này bị thay bởi SEC-MOE-FINANCE-001 và PRQ-MOE-FINANCE-001: cùng chủ đề, phạm vi hẹp lại còn R1, R3, R8, R9, có mã tài liệu riêng, dùng cách tải khác (Level 1 và Level 2 thay cho 50 VU). Số liệu trong nfr draft (50 VU, top-up 1,000 tài khoản) không còn dùng. Dấu hiệu: không file nào trong SEC, PRQ, test plan nhắc nfr draft.

## 7. security-requirements.docx (SEC-MOE-FINANCE-001 v0.3, 12/10/2026)

[Dữ kiện] Bản nháp do QA Lead soạn để PM hoặc PO duyệt. Phạm vi R1, R3, R8, R9. Ngoài phạm vi R2, R4, R5, R6, R7, R10 (nên R7 và dữ liệu thu nhập R4 không được phủ). Nhãn: Fact, Derived, Assumption, Open.
Cấu trúc và số lượng:
- 41 yêu cầu: SR-1.1 đến 1.8 (R1, gồm chuyển số dư sang CPF), SR-3.1 đến 3.8 (R3, gồm GST), SR-8.1 đến 8.9 (R8, gồm chỉ parent đăng nhập), SR-9.1 đến 9.8 (R9, gồm thanh toán kết hợp và học sinh không có EA), SR-C.1 đến C.8 (chung, gồm session 30 phút, mã hóa, giới hạn request, kiểm tra input, injection).
- Entry criteria ES1 đến ES7. Exit criteria SE1.1 đến SE1.8, SE3.1 đến SE3.8, SE8.1 đến SE8.10, SE9.1 đến SE9.8, và 10 tiêu chí chung SC1 đến SC10. Tiêu chí tạm dừng: dữ liệu thật xuất hiện trong môi trường test, mô phỏng đổi hành vi giữa vòng, môi trường không sẵn sàng, lỗi chức năng chặn luồng.
- 15 câu hỏi mở (ví dụ ai được chạy job tạo và đóng tài khoản, nguồn DOB và quốc tịch, ma trận quyền, trường parent được sửa, phạm vi AI, hành vi khi thanh toán vượt số dư, timeout, giới hạn request, có rà soát PDPA không, ai duyệt giả định). Phụ lục A có 12 giả định A-S1 đến A-S12.
- Ví dụ giá trị chấp nhận: 0 lần truy cập chéo trường hoặc chéo gia đình, 0 lần trừ tiền hai lần, 100 phần trăm tác vụ tự động có bản ghi, lỗi bảo mật mức Critical hoặc High phải bằng 0 (SC8), tiêu chí dựa trên giả định chưa duyệt chỉ được ghi conditional pass (SC9).
[Dữ kiện] Nguồn đối chiếu: groundtruth\592ba6ad-image.png, transcript kickoff, Product Backlog PM (PB-01 đến PB-25), MoM 12/10, zip Requirement analysis, backlog PO v0.1 (chỉ cho hai câu về prototype và Definition of Done). Test plan v1.0.7 mục 1.6 nhắc SEC-MOE-FINANCE-001-v0.4.md. [Dữ kiện] File trên đĩa là version 0.3, không có bản 0.4. [Suy luận] Bản 0.4 có thể chưa được lưu vào roles hoặc nằm ở nơi khác. Mô tả của test plan về v0.4 (kiểm tra minimum data, import và sync, interface outbound chưa rõ) không khớp nội dung v0.3 (R1, R3, R8, R9, CPF, GST). Tôi chưa xác minh với người dùng.

## 8. performance-requirements.docx (PRQ-MOE-FINANCE-001 v0.5, 13/10/2026)

[Dữ kiện] Bản nháp QA Lead, cùng phạm vi và cùng nhãn như SEC. Lịch sử 0.1 đến 0.5. Bản 0.5 sửa cách đọc giờ dùng 06:00 đến 02:00 của parent: đó là giờ dùng dự kiến, không phải giờ mở cửa, và không có nguồn nói hệ thống đóng từ 02:00 đến 06:00.
Cấu trúc và số lượng:
- 37 yêu cầu: PR-1.1 đến 1.9 (job tạo và đóng tài khoản theo batch window T tối đa 10 phút, rerun không trùng, chuyển CPF mô phỏng), PR-3.1 đến 3.9, PR-8.1 đến 8.9, PR-9.1 đến 9.10.
- Thông số hợp nhất mục 2.5: Level 1 (10 nhân viên, 20 parent đọc, 5 parent cập nhật, 5 hội thoại AI, 5 thanh toán mỗi loại, 2 thanh toán trên cùng tài khoản), peak K bằng 2 lần normal, endurance 2 giờ ở Level 1 và 8 giờ ở Level 2 với giới hạn trôi 20 phần trăm, volume M bằng 5 lần N, hồi phục sau quá tải 5 phút, đo từ lúc công cụ gửi request đến khi nhận đủ response, không tính render trình duyệt.
- Ngưỡng hợp nhất mục 2.6: đọc P95 2 giây, P99 4 giây; ghi và thanh toán P95 3 giây, P99 5 giây; lỗi tối đa 1 phần trăm ở normal. Ở peak: đọc 3 và 6 giây, ghi 5 và 8 giây, lỗi tối đa 2 phần trăm. AI trả lời P95 10 giây khi đã xây (A-19, số này từ phân tích BA, chưa client xác nhận).
- Test type (mục 2.7): PT-1 stress, PT-2 endurance, PT-3 volume, PT-4 breakpoint (thông tin, không pass hay fail), PT-5 scalability không áp dụng, PT-6 hành vi vượt giới hạn.
- Mục 2.8 Level 2: từ ước lượng của client (500 HQ, 300 trường mỗi trường khoảng 200 user, tối đa 2 triệu parent) với 50 phần trăm nhân viên và 10 phần trăm parent hoạt động mỗi ngày, phiên 30 và 5 phút, tính ra normal 1,400 nhân viên và 800 parent đồng thời, peak 2,800 và 1,600. Các tỷ lệ này là giả định A-17, client chưa xác nhận.
- 31 kịch bản tải: CS-1.1 đến 1.6, CS-3.1 đến 3.4, CS-8.1 đến 8.4, CS-9.1 đến 9.7, CS-P.1 đến 3, CS-E.1, CS-L2.1 và 2, CS-V.1 đến 3, CS-B.1. Entry E1 đến E8, exit X (theo yêu cầu) và XS, XE, XV, XB, chung C1 đến C8.
- 19 câu hỏi mở (số 3 và 6 đã đóng) và 19 giả định A-1 đến A-19.
[Dữ kiện] Test plan v1.0.7 nhắc PRQ-MOE-FINANCE-001-v0.4.md. File trên đĩa là v0.5. Test plan ghi PRQ "không có cổng số mới tùy ý và không có ma trận thực thi cố định", trong khi v0.5 có Level 1, Level 2, K bằng 2, M bằng 5. [Suy luận] Hai tài liệu mô tả PRQ khác nhau, có thể do test plan 1.0.7 được chỉnh ở nơi khác (tên file có hậu tố Chan_1). Chưa xác minh với người dùng. Khi viết test performance thì dùng PRQ v0.5 trên đĩa và nói rõ điểm này.

## 9. questions-for-client-short.txt

[Dữ kiện] "Questions for the client session" cho tender requirement 1, 3, 8, 9, QA Lead, 12/10/2026, cập nhật sau MoM 12/10 và PM Product Backlog, đã bỏ câu client đã trả lời. 20 câu, chia ba nhóm.
- Cho PM và PO (Q1 đến Q8): số người dùng đồng thời (1,400 nhân viên và 800 parent normal, gấp 2 ở peak, ref OQ-17), ngày cao điểm, ngưỡng chậm ở peak, định nghĩa thao tác lỗi, endurance 8 giờ và 2 giờ, tăng trưởng dữ liệu (5 lần), scalability, timeout 30 phút.
- Cho PO và client (Q9 đến Q14): định dạng trường nhập (số điện thoại 8 chữ số bắt đầu 8 hoặc 9, mã bưu điện 6 chữ số), pending transaction khi đóng và giao diện chuyển CPF (OQ-13), ai tạo charge và có tạo hàng loạt không (OQ-04, OQ-10), GST (OQ-10), học sinh không có EA (OQ-11), quan hệ Parent và Child (OQ-02).
- Cho Dev Lead (Q15 đến Q20): giờ chạy job, giới hạn đăng nhập và thanh toán, kích thước dữ liệu mock, điểm đo thời gian, hành vi cố định của mô phỏng SingPass và thanh toán, kích thước môi trường test.
[Suy luận] Các con số đề xuất khớp với PRQ v0.5 (1,400, 800, peak gấp 2, ngưỡng peak, endurance 8 giờ và 2 giờ, 30 phút của SEC). Dựa trên so sánh trực tiếp các số trong file này với PRQ mục 2.6, 2.8 và SEC SR-C.1.
Chưa có câu trả lời nào được ghi trong file. [Dữ kiện] Cột trả lời không tồn tại trong file txt, không rõ câu nào đã gửi đi. Đã tìm trong toàn bộ roles, không thấy file ghi lại việc gửi.

## 10. test-plan-final-v1.0.docx

[Dữ kiện] Test plan version 1.0 cho client, trình bày tại phiên họp thứ Hai 12/10. Bìa ghi "Version Draft 1, Date 19 Aug 2026", còn lịch sử bản ghi 12 October 2026, nên ngày trên bìa là sót từ khuôn mẫu [Suy luận, vì lịch sử và nội dung đều nói tháng 10/2026].
Khác với v1.0.7 (roles\qa):
- Phạm vi Sprint 1: v1.0 có hai ứng viên chưa cam kết (backlog BA PB-01 đến PB-07, và bản nháp QA: school user tạo charge, parent liên kết thấy, gia đình khác bị chặn). v1.0.7 ghi R1, R3, R8, R9 do team chọn.
- Ngoài phạm vi: v1.0 ghi "Load and performance testing" ngoài phạm vi, nhưng mục 3.9 vẫn mô tả 5 loại performance test và tham chiếu PRQ. v1.0.7 chỉ coi PRQ là yêu cầu dài hạn.
- Regression: v1.0 chỉ ghi regression bắt buộc. v1.0.7 thêm regression tự động bắt buộc mỗi sprint và CI/CD.
- Exit UAT: v1.0 là không còn S1 mở. v1.0.7 là không còn S1 hoặc S2 mở, trừ ngoại lệ S2 chức năng có client duyệt bằng văn bản.
- Security và performance: v1.0 xếp loại "Optional, specialist team" trong bảng test type nhưng mục 3.8 và 3.9 mô tả kiểm tra áp dụng cho R1, R3, R8, R9. v1.0.7 gom về một đề xuất và ghi rõ SEC, PRQ là bản nháp cục bộ chưa client duyệt.
- Rủi ro mở: v1.0 có 7 dòng, có câu hỏi 16 tuổi hay ngày trước sinh nhật 16, có ngoại lệ sau 16, có SBFAS thay hay bổ sung MOEFAS. v1.0.7 có 11 dòng.
- Ước lượng công QA mỗi sprint trong v1.0 (nửa ngày phân tích, một ngày thiết kế case, một ngày rưỡi chạy test, nửa ngày regression và báo cáo) không có trong v1.0.7.
[Suy luận] Dùng v1.0.7 làm bản hiện hành, v1.0 làm lịch sử và nguồn của số ước lượng công.
