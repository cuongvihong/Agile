# Role po: những gì tôi biết về các file

Nguồn: D:\AIQA\Agileproject\roles\po (2 file: Product Backlog.xlsx và Agile Glossary.docx). Đọc ngày 2026-10-14, viết lại lần 2 cùng ngày vì thư mục đổi nội dung. Lần đọc đầu chỉ có 1 file là EAFAMS_Initial_Product_Backlog_v0.1.xlsx (30 PBI). Lần này liệt kê đệ quy thư mục thấy đúng 2 file nói trên, không còn file v0.1.
Độ sâu đọc: Product Backlog.xlsx đọc toàn bộ chữ của cả 5 sheet, và đối chiếu từng ô sheet Product Backlog với roles\pm\Product Backlog.xlsx. Agile Glossary.docx đọc toàn bộ chữ (trích bằng pandoc), không có hình nhúng cần xem.
Nhãn: [Dữ kiện] là điều ghi trong file nguồn, kèm sheet hoặc ID. [Suy luận] là điều tôi rút ra, kèm cách rút ra.
Cảnh báo: số PB-xx trong Product Backlog.xlsx của PO hiện nay GIỐNG số PB-xx của roles\pm\Product Backlog.xlsx (và của Dev Sprint_Backlog). Số PB-xx của file v0.1 cũ (mục 3) thì khác hẳn, nên khi gặp trích dẫn cũ như "PB-03 là tạo và kích hoạt EA" phải hiểu là file v0.1 cũ.

## 1. Product Backlog.xlsx

[Dữ kiện] Năm sheet: Product Backlog (A1:R208), Sprint Tracker, Open Questions, Client Decisions, Read Me. Tiêu đề sheet đầu "EDUCATION ACCOUNT | PRODUCT BACKLOG". Ngày sửa file trên đĩa muộn hơn file PM.

Quan hệ với file PM (chi tiết nội dung xem pm.md, không lặp lại ở đây): [Dữ kiện] tôi so từng ô của sheet Product Backlog hai file sau khi ghép thẳng hàng. Nội dung giống hệt, 25 PBI từ PB-01 đến PB-25, cùng cột, cùng Target Sprint, cùng mô tả. Chỉ khác ba hàng chèn thêm vào file PO (mục dưới) và dải ô công thức của Sprint Tracker. Các sheet Open Questions (OQ-01 đến OQ-17), Client Decisions (CD-01 đến CD-12) và Read Me giống hệt file PM. [Suy luận] file PO này là bản của PM thêm ba hàng đăng nhập, không phải một backlog độc lập. Không có ngày bên trong file nên không biết ai thêm, bao giờ.

Ba hàng thêm (hàng 17 đến 19, nằm giữa PB-11 và PB-12):
- Không có ID PB. Epic "User Authentication & Access Management".
- Ba tên: "Admin Portal Login" (R3, ghi "Inferred, supporting capability"), "Parent Login via SingPass" (R8), "School User Login" (R3, cũng "Inferred"). Cả ba Target Sprint 1, Priority P1 High, mô tả theo mẫu "As a ..., I want ..., so that ...".
- Các cột Requirement basis, Readiness, Dev Status, Owner, Estimate SP, Open question, Acceptance, Build Sequence đều trống. Chỉ hàng đầu có Dependencies "User authentication mechanism, user roles and permissions".
- [Suy luận] hai hàng trùng ý với PB-06 "Parent authentication via SingPass" (R8) và PB-03 "HQ vs School role-based permissions" (R3). "Admin Portal Login" và "School User Login" cũng chồng nhau vì School User là một nhóm của Admin Portal. Cần hỏi PO có tách thành story riêng hay gộp vào PB-03 và PB-06.
- [Suy luận] vì ba hàng này không có ID nên Dev Sprint_Backlog (cột PBI Ref dùng mã PB-xx) không thể gắn task vào chúng.

Sprint Tracker: [Dữ kiện] công thức đếm trải dài tới hàng 208 (file PM tới hàng 205). Sprint 1 hiện đếm 14 mục (11 PBI cộng 3 hàng mới), trong đó 11 mục Not Started. [Suy luận] ba hàng mới được tính vào số "Items" nhưng không được tính ở cột Not Started vì ô Dev Status của chúng trống, nên tổng các cột trạng thái (11) nhỏ hơn Items (14). Nếu đo tiến độ Sprint 1 bằng tracker thì tỷ lệ Completion sẽ bị lệch.

Read Me: [Dữ kiện] dòng 13 nói các ID đã đánh lại từ PB-01 đến PB-25 và "See ID Mapping for old-to-new references", nhưng workbook không có sheet ID Mapping (file PM cũng không có). Không thể đối chiếu mã cũ với mã mới bằng workbook này. [Suy luận] đây là lý do mã PB của file v0.1 cũ không dò ngược được từ file hiện tại.

## 2. Agile Glossary.docx

[Dữ kiện] "Glossary: Education Account + FAS System", dự án ghi "Agile Training Practice, Cohort 3, 10/2026". Viết tiếng Việt, thuật ngữ giữ tiếng Anh. Câu mở đầu: "Team đề xuất bổ sung qua comment". Không ghi tác giả hay ngày. Nằm trong roles\po. [Suy luận] do PO viết, căn cứ vị trí thư mục, chưa có nơi nào xác nhận.

Năm phần:
- 1. Roles và người dùng: MOE, MOE HQ users (Top-Up, cấu hình scheme, ngân sách và thống kê MOEFAS, simulate views), School users (master data cấp trường, quyết định SBFAS, nhập đơn hardcopy, ngân sách SBFAS), Parents (SingPass, xem account, trả phí, nộp FAS), Students (Singapore Citizens).
- 2. Systems và integrations: Admin Portal, e-Service Portal, SingPass, Third-party income API, Online payment methods hoặc Payment gateway.
- 3. Business terms: Education Account (tạo và kích hoạt lúc 7 tuổi, đóng lúc 16), Top-Up (batch hoặc specific, regular hoặc ad-hoc), Batch top-up rules (lọc theo tuổi, số dư, schooling status), Master data, Level/Cohort, Fee type, Fee component, FAS, Scheme, MOEFAS (auto-grant), SBFAS, Funding source, Eligibility criteria, Household và Per-capita income band, Tier, Subsidy amount, Application outcome, Fees payable, Outstanding charges, Hardcopy application, Family unit, Budget and statistics, Simulate views.
- 4. AI terms: Rule-based logic, ML risk classification (Low, Medium, High), Assistance tier recommendation (School user quyết định cuối), AI chatbot, Dynamic follow-up questions, Auto-fill form.
- 5. Agile/BA terms: User Story, Acceptance Criteria (Given/When/Then), MoSCoW, Sprint (chu kỳ 1 tuần, 3 sprint), DoR/DoD, Product backlog, Walking skeleton, MVP, Mock/Stub, Vertical slice.

Điểm đáng chú ý cho QA (đều có nguồn):
- [Dữ kiện] Glossary định nghĩa "Family unit": một đơn FAS đánh giá tất cả anh chị em trong hộ chung một kết quả. [Dữ kiện] sheet Func4 của Dev (dev.md mục 2) thiết kế "mỗi học sinh một đơn trong một năm học (D-25)", thu nhập hộ lấy từ API cho từng đơn. Backlog PB-18 ghi "Online FAS application by family unit". [Suy luận] hai nguồn lệch nhau về đơn vị của một đơn FAS (cả hộ hay từng con). Định nghĩa trong Glossary là của PO, tôi chưa thấy câu nào của client xác nhận nó (các md bản đồ không nhắc "family unit" hay "household"). Cần hỏi BA và PO nguồn nào là hiện hành.
- [Dữ kiện] Glossary ghi "Students (Singapore Citizens)". Func4 thiết kế SBFAS cho Citizen và PR (D-11), và cho phép tạo đơn của học sinh không phải Citizen hoặc PR (NotEligibleForAnyScheme). Glossary không nhắc PR.
- [Dữ kiện] Glossary ghi "Level / Cohort: Khối/niên khóa". Client nói cohort nghĩa là level (Client Decisions CD-04). [Suy luận] "niên khóa" thường hiểu là năm nhập học, khác level, nên cách dịch có thể gây hiểu nhầm.
- [Dữ kiện] Glossary ghi "Product backlog: do BA duy trì cùng PO". Bản Product Backlog.xlsx trong roles\pm giống hệt (trừ ba hàng). Chưa rõ ai giữ bản gốc.
- [Dữ kiện] Phần Agile nhắc sheet "Agile requirements" với tab "User Stories + AC" và "Sprint Plan". Tìm tên file trong roles không thấy workbook nào như vậy (chỉ thấy "[Agile] FS R1V1.0.docx" ở roles\ba, là FS R1). Nên chưa đọc được AC dạng Gherkin của team.
- [Dữ kiện] Glossary mô tả Education Account "tự động đóng khi đủ 16 tuổi", không nhắc điều kiện mất quốc tịch hay chuyển số dư sang CPF.

## 3. Lịch sử: EAFAMS_Initial_Product_Backlog_v0.1.xlsx (không còn trong roles\po)

File này không còn trên đĩa nên mục này chỉ dựa trên lần đọc đầu ngày 14/10 và không kiểm lại được. Còn cần vì roles\qalead\po-backlog-review.docx và .md (QA Lead review, 5 finding) nói về file này.
- [Dữ kiện lúc đọc đầu] 4 sheet: Overview, Product Backlog, Sprint 1 Candidates, Requirement Coverage. 30 PBI: Sprint 1 có 7, Sprint 2 có 10, Sprint 3 có 6, về sau có 7. Mọi dòng Effort, Dev/QA feasibility, Team decision, Owner là "TBD".
- Đánh số khác file hiện tại: PB-03 là "tự tạo và kích hoạt EA", PB-06 là "tự đóng EA khi đủ điều kiện" (Must*), trong khi file hiện tại PB-03 là phân quyền HQ và School, PB-16 là đóng EA.
- R9 nằm ở Sprint 2 trong file v0.1, ở Sprint 1 trong file hiện tại (PB-09, PB-10, PB-11). R1 đóng tài khoản nằm ở Sprint 1 trong v0.1 (với dấu Must*), ở Sprint 3 trong file hiện tại (PB-16). Master data R3 ở Sprint 2 trong v0.1, Sprint 1 trong file hiện tại (PB-02, PB-03).
- Sheet Requirement Coverage của file v0.1 ghi chi tiết còn thiếu cho R9 là "Partial/split payments and failure handling TBD". File hiện tại không có sheet đó.
- [Suy luận] file hiện tại thay file v0.1, căn cứ chỉ có file hiện tại trong thư mục và qalead-1-tai-lieu.md ghi "backlog PM đã thay backlog PO". Không có ngày bên trong để chứng minh.

## 4. Điểm cần nhớ khi dùng thư mục này

- Đây là kế hoạch, không phải yêu cầu. [Dữ kiện] sheet Sprint Tracker ghi Sprint 1 đến 3 là "PO recommendation; Dev owns capacity / feasibility".
- Cần chi tiết từng PBI, Open Questions, Client Decisions: đọc pm.md, vì nội dung giống hệt. Phần khác của file PO là ba hàng đăng nhập, Sprint Tracker và Glossary.
- Các md khác còn nhắc file v0.1 như file PO hiện hành (pm.md đầu file và mục 4, qalead-1-tai-lieu.md) là ghi chú cũ chưa cập nhật lần này. Khi đọc, hiểu "file PO" ở đó là v0.1 cũ.
- Không có thư mục roles\scrummaster hay roles\devlead chứa tài liệu (scrummaster rỗng, devlead không có trên đĩa).
