# Role pm: những gì tôi biết về các file

Nguồn: D:\AIQA\Agileproject\roles\pm (2 file: Product Backlog.xlsx, project-plan.md). Đọc ngày 2026-10-14.
Độ sâu đọc: đọc toàn bộ chữ của cả hai file (xlsx đọc đủ mọi ô không rỗng của 5 sheet).
Nhãn: [Dữ kiện] là điều ghi trong file nguồn, kèm tên file và sheet hoặc ID. [Suy luận] là điều tôi rút ra, kèm cách rút ra.
Cảnh báo quan trọng: đánh số PB-xx trong file này KHÔNG trùng với đánh số PB-xx của roles\po\EAFAMS_Initial_Product_Backlog_v0.1.xlsx. Cùng mã PB-05 hay PB-16 nhưng là hai story khác nhau. Sprint_Backlog của Dev dùng đánh số của file này. Xem mục 4.

## 1. Bảng tổng hợp

| File | Là gì | Dùng cho |
|---|---|---|
| Product Backlog.xlsx | Product Backlog 25 PBI kèm Sprint Tracker, 17 câu hỏi mở, 12 quyết định client, hướng dẫn | Biết story nào thuộc sprint nào, phụ thuộc, rủi ro, câu hỏi mở với client |
| project-plan.md | Kế hoạch dự án: mốc thời gian, cấu trúc đội, phân bổ phạm vi theo sprint, rủi ro, giao tiếp | Biết lịch sprint, quy mô đội, quy tắc phụ thuộc giữa hai track |

## 2. Product Backlog.xlsx

[Dữ kiện] Năm sheet: Product Backlog, Sprint Tracker, Open Questions, Client Decisions, Read Me.
Sheet Product Backlog: tiêu đề "EDUCATION ACCOUNT, PRODUCT BACKLOG". Cột: ID, Epic, Feature hoặc User Story, Description, Portal hoặc Actor, Source Requirement(s) (ánh xạ R1 đến R10), Target Sprint (đề xuất), Priority, Requirement basis, Readiness, Dev Status, Owner, Estimate SP, Dependencies, Open question hoặc risk, Acceptance hoặc Demo check, Dev Notes, Build Sequence. Có 25 PBI, PB-01 đến PB-25. Dev cập nhật các cột Status, Owner, Estimate, Notes. Toàn bộ Dev Status đang là "Not Started", Estimate SP, Owner và Notes đang để trống.
Phân bổ sprint (đề xuất, không phải cam kết): Sprint 1 có 11 PBI (PB-01 đến PB-11), Sprint 2 có 4 (PB-12 đến PB-15), Sprint 3 có 6 (PB-16 đến PB-21), chưa xếp lịch có 4 (PB-22 đến PB-25). Tôi đã đếm lại, khớp sheet Sprint Tracker.
Danh sách PBI:
- Sprint 1: PB-01 baseline hiệu năng và concurrency (NFR), PB-02 quản lý trường, level hoặc cohort, class, student (R3), PB-03 phân quyền HQ và School (R3), PB-04 lấy dữ liệu student từ nguồn ngoài (R1, R3, R8), PB-05 tạo và kích hoạt EA lúc 7 tuổi (R1), PB-06 đăng nhập Singpass (R8), PB-07 phân quyền Parent theo con (R8), PB-08 xem tài khoản, số dư, giao dịch của con (R8), PB-09 xem khoản phí chưa trả (R9), PB-10 trả phí bằng EA (R3, R9), PB-11 trả phí online (R9).
- Sprint 2: PB-12 quản lý fee type và component (R3), PB-13 tạo hoặc ghi nhận khoản phí cho student (R3, R9), PB-14 top-up cá nhân và theo lô (R2), PB-15 cập nhật thông tin cá nhân (R8).
- Sprint 3: PB-16 đóng EA lúc 16 tuổi, chuyển CPF (R1), PB-17 cấu hình FAS (R4), PB-18 nộp đơn FAS theo hộ (R10), PB-19 đánh giá FAS và áp trợ cấp (R4), PB-20 nhập đơn FAS giấy (R5), PB-21 ngân sách FAS (R6).
- Chưa xếp lịch: PB-22 mô phỏng view cho support (R7), PB-23 trợ lý AI, PB-24 điền sẵn đơn FAS bằng AI, PB-25 dự đoán rủi ro tài chính bằng ML.
Ghi chú sprint cuối trang tracker: "Sprint 1 targets all R9 options but charge source, payment gateway, ledger and business rules remain unresolved" là rủi ro cao. PB-22 đến PB-25 "Unscheduled is not cancelled".
Sheet Open Questions: OQ-01 đến OQ-17, tất cả trạng thái Open, cột câu trả lời của client trống. Mức khẩn: P1 Now (OQ-01 đến OQ-08, OQ-11, OQ-16), P2 Before Sprint 2 hoặc 3, P3 Later. Nội dung gồm nguồn dữ liệu student, nguồn quan hệ guardian, Singpass sandbox, nguồn khoản phí (OQ-04), nguồn số dư và giao dịch EA (OQ-05), cách kích hoạt lúc 7 tuổi, ma trận quyền HQ và School, dataset demo R9 và online live hay sandbox (OQ-08), quy tắc thanh toán EA và nhà cung cấp online (OQ-11), trường nào Parent sửa được, fee type và GST, quy tắc top-up theo lô, CPF khi đóng, ngưỡng FAS, ngân sách, phạm vi AI, mục tiêu concurrency (OQ-17).
[Suy luận] Các ID OQ-04, OQ-05, OQ-08, OQ-11 mà FS 09 Phụ lục B nhắc đến trùng nội dung với bốn câu hỏi này, nên FS 09 lấy đánh số từ sheet này.
Sheet Client Decisions: CD-01 đến CD-12, mỗi dòng có độ tin cậy ("Client explicitly clarified", "Client expressed preference", "Explicit non-approval", "Proposed scope discussed"). Dòng đầu cảnh báo: nguồn là bản ghi âm do AI chép, một số câu của team không phải quyết định client. Các điểm chính: EA không phải tài khoản đăng nhập (CD-01), số dư chuyển CPF khi đóng và client kỳ vọng không có giao dịch chờ (CD-02), trường dữ liệu student gợi ý (CD-03), level và cohort cùng nghĩa, class riêng (CD-04), HQ quản lý tất cả, School sửa từ level trở xuống (CD-05), trạng thái ghi danh và trạng thái EA tách riêng (CD-06), GST dùng chung là mong muốn nếu khả thi (CD-07), các ví dụ phí (CD-08), số liệu quy mô người dùng không phải concurrency (CD-09, CD-10), client chưa duyệt chi tiết thiết kế (CD-11), phạm vi Sprint 1 là đề xuất (CD-12). Cột nguồn dùng mốc thời gian trong bản ghi, ví dụ "Mtg 15:03 đến 16:30".
Sheet Read Me: hướng dẫn nhập vào Google Sheets, cập nhật cột nào, quy ước demo: "an online payment without gateway or sandbox must NOT count as Done" và "R9 is only fully satisfied when BOTH payment choices and view outstanding charges work". Mục 10 nói PBI ID đã đánh số lại từ PB-01 đến PB-25 theo Build Sequence và nhắc xem tab "ID Mapping". [Dữ kiện] Tab "ID Mapping" không có trong file (file chỉ có 5 sheet kể trên, không ẩn sheet nào). Không thể tra ID cũ sang ID mới.
Điểm cần nhớ cho QA:
- Cột "Requirement basis" cho biết một story có phải yêu cầu client xác nhận hay chỉ là đề xuất, ví dụ PB-07 "Proposed solution / implied", PB-13 "Gap / proposed solution". Không biến story đề xuất thành yêu cầu khi viết test.
- Cột "Readiness" có các giá trị "Needs AC", "Blocked / external", "At risk / dependency", "Needs client decision". Phần lớn story Sprint 1 chưa có acceptance criteria hoàn chỉnh theo file này.
- PB-10 ghi "Eligibility, partial-payment and insufficient-funds rules remain open". PB-11 ghi "PAYMENT GATE: gateway, permitted methods, test credentials, callbacks, payment confirmation, failed or cancelled payments, refund and reconciliation not yet defined". Chia đôi hay kết hợp hai nguồn không được nhắc trong file này. [Dữ kiện] đã tìm các từ "split" và "combin" trong cả file, không thấy.

## 3. project-plan.md

[Dữ kiện] Tiêu đề "PM Project Plan: Finance System for MOE". Nguồn dẫn: groundtruth\592ba6ad-image.png (tender 10 requirement) và groundtruth\MOE_Finance_System_Agile_Kick-off_Transcript.md (chỉ làm ngữ cảnh).
- Mô hình: Agile, 3 sprint, mỗi sprint 1 tuần, bắt đầu 2026-10-11, tổng 3 tuần. Sprint 1: 11 đến 17/10/2026. Sprint 2: 18 đến 24/10. Sprint 3: 25 đến 31/10.
- Đội: 2 track song song. Track A Admin Portal (5 Dev, 3 QA) lo tender #1 đến #7. Track B eService Portal (4 Dev, 2 QA) lo #8 đến #10. Tổng 9 Dev và 5 QA, cộng 1 Dev Lead và 1 QA Lead dùng chung.
- Quy tắc phụ thuộc: Track B không thể build với backend thật từ ngày đầu. Dev Lead phải công bố API contract cho account, billing, FAS vào ngày 1 đến 2 của Sprint 1, Track B build theo mock.
- Phân bổ phạm vi nháp theo sprint: Sprint 1 Track A gồm SSO hoặc AD login, kiến trúc, #1, #2, #3. Track B gồm Singpass login, UI, một phần #8. Sprint 2 Track A gồm #4 FAS engine, #5, #6, #7. Track B gồm #9 (xem phí và thanh toán bằng số dư, online hoặc kết hợp) và tiếp #8 với AI chatbot. Sprint 3 Track A hỗ trợ tích hợp. Track B gồm #10 và chuyển mock sang API thật.
- Rủi ro R1 đến R5 (thời gian eo hẹp với 3 tính năng AI, API thu nhập bên thứ ba, sandbox Singpass và AD/SSO, không có tuyên bố out of scope trong tender, hợp đồng API giữa hai track lệch). Giả định, kế hoạch giao tiếp (standup hằng ngày, planning thứ Hai, review và retro thứ Sáu), 4 câu hỏi mở cho khách hàng.
- Lưu ý ký hiệu: "R1" đến "R5" trong mục Risk Register là mã rủi ro, không phải requirement R1 đến R5 của tender. [Dữ kiện] bảng Risk Register dùng cột ID R1 đến R5.

## 4. Không khớp giữa các tài liệu (tất cả là [Suy luận], kèm nguồn đối chiếu)

- Vị trí của R9 theo sprint: Product Backlog của PM đặt PB-09, PB-10, PB-11 (R9) ở Sprint 1. Dev Sprint_Backlog có 5 task R9 trong sprint hiện tại. FS 09 Final nhắm R9 trong Sprint 1 (các hạng mục khác "Sprint sau"). Nhưng project-plan.md đặt #9 ở Sprint 2 và roles\po\EAFAMS_Initial_Product_Backlog_v0.1.xlsx cũng đặt R9 ở S2. project-plan.md tự ghi là "Draft only", file PO tự ghi là "provisional". Cần hỏi PM hoặc PO nguồn nào là hiện hành. Các file không ghi ngày bên trong. Ngày sửa file trên đĩa: project-plan.md 10/10/2026, file PO 10/10/2026, Product Backlog của PM 12/10/2026 (UTC). Ngày trên đĩa có thể là ngày sao chép, chỉ là bằng chứng yếu rằng hai file kia cũ hơn.
- Đánh số PB: file PM (PB-01 đến PB-25) và file PO (PB-01 đến PB-30) dùng cùng định dạng mã nhưng khác nội dung. Dev Sprint_Backlog dùng đánh số của file PM (ví dụ TSK-R1-04 gắn PB-16, "Close Education Account at age 16"). Khi trích dẫn phải ghi rõ "PB-xx của file PM" hay "của file PO".
- Phân track: project-plan xếp R1, R2, R3 vào Track A và R8, R9, R10 vào Track B. Sprint_Backlog của Dev chia việc theo requirement cho từng cặp người (Kevin và Hugh cho R1, Nito và Tyson cho R3, Ryan và Nathan cho R8, Lucas và Arthur cho R9, Christian cho R4) mà không nhắc track. Không mâu thuẫn trực tiếp.
- Tính năng chia đôi (split payment) có trong FS 09 và thiết kế bảng Func9. Trong các file khác: project-plan.md dòng Sprint 2 ghi #9 gồm "pay via balance / online / combination", tức có kết hợp hai nguồn. File PO chỉ nhắc ở sheet Requirement Coverage: "Partial/split payments and failure handling TBD". PM Product Backlog và Dev Sprint_Backlog không nhắc (đã tìm "split" và "combin"). Nghĩa là chia đôi xuất hiện ở tầng kế hoạch và đặc tả nhưng chưa thành story hay task riêng.
