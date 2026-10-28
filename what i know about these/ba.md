# Role ba: những gì tôi biết về các file

Nguồn: D:\AIQA\Agileproject\roles\ba (7 file). Đọc ngày 2026-10-14.
Cập nhật 2026-10-19: thêm mục 12 cho FS04.docx (FS F4 v1.3). Các mục 1 đến 11 không đọc lại.
Độ sâu đọc: đọc toàn bộ chữ của cả 7 file và xem cả 5 hình nhúng (sơ đồ High-Level Solution, swimlane FS 08, ba sơ đồ trong FS 09). Không đọc lại tài liệu gốc nào ngoài role ba để viết file này.
Nhãn dùng trong file này: [Dữ kiện] là điều ghi trực tiếp trong file nguồn, kèm tên file và mục hoặc ID. [Suy luận] là điều tôi rút ra, kèm cách rút ra. Điều không tìm thấy thì ghi rõ đã tìm ở đâu.
Khi cần chi tiết từng dòng (ví dụ mã lỗi, ID rule), đọc lại file gốc. File này chỉ là bản đồ để biết nên đọc file nào, mục nào.

## 1. Role ba là gì

Role ba chứa tài liệu của BA: bản đặc tả chức năng (FS) cho R1, R8, R9, biên bản kickoff, bảng câu hỏi đầu tiên gửi client, sổ theo dõi TBD sau buổi làm rõ 12/10, và tài liệu công khai về MOE FAS. Đây là nguồn yêu cầu chính để QA viết test case. Các FS viết bằng tiếng Việt, xen thuật ngữ tiếng Anh. Thông điệp hiển thị cho người dùng cuối viết tiếng Anh.

Thứ tự ưu tiên khi các tài liệu mâu thuẫn, theo FS 08 phần 1: Decision Log, rồi Story tickets, rồi FRD, rồi BRD. [Dữ kiện] FS 08 mục 1. Decision Log (D-03, D-19 đến D-22, D-28, D-31) không có trong bất kỳ file nào của roles. [Dữ kiện] đã tìm cụm "decision log" trong toàn bộ bản text của roles, chỉ FS 08 nhắc đến. Vì vậy các D-xx chỉ dùng được như nhãn, chưa kiểm được nội dung gốc.

## 2. Bảng tổng hợp 7 file

| File | Là gì | Ngày hoặc phiên bản | Dùng cho |
|---|---|---|---|
| MOE FAS.pdf | Tóm tắt công khai chương trình MOE FAS | hiệu lực từ 01/2026 | R4, R10, kiểm tra quy tắc FAS |
| First meeting questions.docx | 22 câu hỏi làm rõ gửi client trước kickoff, có sơ đồ High-Level Solution | không ghi ngày | R1 đến R10, ngữ cảnh giả định ban đầu |
| MoM Kickoff meeting 12_10.docx | Biên bản họp khởi động 12/10/2026 | do Daniel Tran soạn | Phạm vi Sprint 1, các action item |
| MOE_Sprint1_Clarifications_and_TBD_Register.xlsx | Sổ ASM, TBD, NEW sau buổi làm rõ 12/10 | cập nhật sau 12/10 | Trạng thái xác nhận của từng giả định |
| [Agile] FS R1V1.0.docx | FS R1: tạo và đóng Education Account | nội dung ghi Version 1.2 | R1, F01, F02 |
| [Agile] FS 08.docx | FS R8: Parent Portal, SingPass, xem EA, sửa thông tin | v0.4, 14/10/2026 | R8 |
| [Agile] FS 09.docx | FS R9: Outstanding Fees and Payment (Final) | 14/10/2026 | R9 |

Lưu ý tên file: file tên "FS R1V1.0" nhưng bên trong ghi "Version: 1.2 BA/Dev/QA Refinement Draft". [Dữ kiện] đầu tài liệu FS R1. Khi trích dẫn nên ghi cả hai.

## 3. MOE FAS.pdf

[Dữ kiện] Một trang tóm tắt chương trình MOE Financial Assistance Scheme.
Tiêu chí thu nhập, hiệu lực từ tháng 1 năm 2026: thu nhập hộ gia đình hằng tháng (GHI) không quá 4,000 SGD, hoặc thu nhập bình quân đầu người hằng tháng (PCI) không quá 1,000 SGD.
Quyền lợi theo cấp:
- Tiểu học: giảm 100% phí linh tinh, sách giáo khoa và đồng phục miễn phí, hỗ trợ ăn 7 bữa mỗi tuần học, hỗ trợ đi lại (xe buýt trường 70% cước tháng, hoặc phương tiện công cộng 21 SGD mỗi tháng, tối đa 252 SGD mỗi năm).
- Trung học: giảm 100% học phí và phí linh tinh, sách và đồng phục miễn phí, hỗ trợ ăn 10 bữa mỗi tuần, trợ cấp phương tiện công cộng 21 SGD mỗi tháng, tối đa 252 SGD mỗi năm.
- JC và Centralised Institute: giảm 100% học phí và phí linh tinh, học bổng 1,600 SGD mỗi năm (đã gồm trợ cấp đi lại).
Cách nộp đơn: nộp online hoặc nộp mẫu giấy tại trường. Gia đình có nhiều con ở các trường khác nhau chỉ cần nộp một đơn tại một trường bất kỳ. Trường nhận đơn sẽ báo kết quả.
Hỗ trợ thêm: trường có hỗ trợ tài chính riêng xét từng trường hợp, chương trình DigitalAccess@Home của IMDA, học bổng theo thành tích.
[Suy luận] File là trang web công khai được lưu thành PDF (dựa vào định dạng bảng và đường link), chưa kiểm nguồn URL. Đây là tham chiếu quy tắc thực tế, không phải yêu cầu của client cho dự án. Tài liệu client (TBD register NEW-09) nói ngưỡng thu nhập phải cấu hình được, không hard-code, nên không dùng các con số 4,000 và 1,000 làm giá trị cố định trong test.

## 4. First meeting questions.docx

[Dữ kiện] Gồm một hình High-Level Solution và ba nhóm câu hỏi, mỗi câu có ba cột: Gap, Working Assumption, Client Question.
Hình High-Level Solution (EAFAMS, Education Account and Financial Assistance Management System) gồm bảy khối theo thứ tự: Core Data Setup (Student Data, School Setup, Parent Links), Education Account Lifecycle (Eligibility Check, Auto Create hoặc Activate, Auto Close), Funding and Top-up (Individual, Batch, Top-up Rules), Fee Management (Fee Setup, Fee Assignment, Outstanding Fees), Parent e-Service (Singpass Login, Account View, Profile Update, Fee Payment), FAS Processing (Family Application, Offline Capture, Income hoặc Eligibility Check, MOEFAS hoặc SBFAS, Subsidy Applied), Monitoring and Support (Budget and Stats, User Simulation, Audit hoặc Notification, AI Support). Chú thích cuối hình: "Training prototype using mock data and simulated integrations."
Nhóm đầu (Q01 đến Q06, không có tiêu đề nhóm trong bản text): phạm vi Sprint 1 cho R1, R3, R8; vòng đời tài khoản (tự kích hoạt lúc 7 tuổi, đóng lúc 16 tuổi, số dư khi đóng chưa quyết); nguồn dữ liệu công dân; quan hệ Parent và Child sau Singpass; trường thông tin cá nhân được xem hoặc sửa, MyInfo, xác minh liên hệ; cấu trúc School, Level, Cohort, Class, Student và quyền.
Nhóm B "P1 Early Refinement / Architecture Dependencies" (Q07 đến Q18): vòng đời ghi danh, quan hệ Fee Type và Fee Component, quyền quản lý phí, danh mục component, quy tắc áp phí, điều kiện thanh toán bằng số dư, số dư không đủ (Q13), khoản phí còn nợ, cổng thanh toán, lỗi thanh toán và hoàn tiền, lịch sử giao dịch và sao kê PDF, audit dữ liệu gốc.
Nhóm C "P2 Later Sprint Clarification" (Q19 đến Q22): hiển thị FAS, xử lý khi AI không trả lời được, quản trị nội dung AI, đánh giá độ chính xác AI.
Điểm cần nhớ: Q13 giả định "no partial or split-payment behavior is assumed until confirmed". [Dữ kiện] Q13. Sau này FS 09 Final đưa chia đôi (split) vào phạm vi. Xem mục 9 về sự không khớp này.

## 5. MoM Kickoff meeting 12_10.docx

[Dữ kiện] Họp 12/10/2026 (thứ Hai) 13:30 qua Teams, kết thúc 14:00, soạn bởi Daniel Tran. Bảng 7 mục agenda, mỗi mục có tóm tắt và action item:
1. High-level solution: client thấy các khối chính đã đủ, xác nhận chi tiết sẽ làm trong workshop hoặc sprint. Mũi tên trong sơ đồ là luồng quy trình, không nhất thiết là xử lý tự động.
2. Sprint 1: tập trung parent xem Education Account của con, kèm backend và một phần admin portal. Số tham chiếu requirement chưa rõ, cần kiểm tra. Action: cập nhật phạm vi Sprint 1 và phụ thuộc.
3. Vòng đời tài khoản và dữ liệu nguồn: tuổi kích hoạt và đóng cần xác nhận với yêu cầu chính thức. Khi đóng, không còn giao dịch chờ và số dư còn lại chuyển sang CPF. Dữ liệu student: tên, ngày sinh, quốc tịch, địa chỉ nếu có. Action: xác nhận đủ trường dữ liệu từ bên thứ ba, ghi tài liệu cách xử lý khi đóng.
4. Eligibility và FAS: Education Account là tài khoản do chính phủ tài trợ cho chi phí giáo dục hợp lệ, không phải tài khoản đăng nhập. PR và học sinh nước ngoài có thể đi học không cần Education Account và trả phí bằng tiền của mình. Điều kiện EA và điều kiện FAS là hai tiêu chí riêng.
5. Parent access và cấu trúc trường: liên kết parent và student khi nạp dữ liệu, xác thực quan hệ sau Singpass. "Level" và "cohort" có thể dùng thay nhau, class là khái niệm riêng. MOE HQ quản lý mọi bản ghi, user trường quản lý bản ghi của trường mình và cấp thấp hơn. Trạng thái ghi danh và trạng thái EA phải tách riêng.
6. Fee management: dùng lại fee component (ví dụ cấu hình GST một lần). Ví dụ phí: học phí, phí linh tinh, hoạt động ngoại khóa hoặc chuyến đi, phí phát sinh như làm hỏng tài sản lớp học. Một số khoản chỉ áp cho level hoặc class nhất định.
7. Performance: ước lượng người dùng tổng thể khoảng 500 HQ, 300 trường mỗi trường khoảng 200 user, tối đa 2 triệu parent. Đây là tổng người dùng tiềm năng, không phải mục tiêu đồng thời. HQ và trường dùng 08:00 đến 19:00, cổng parent dùng 06:00 đến 02:00, không có giờ cao điểm cố định nhưng có thể tăng quanh kỳ thanh toán hóa đơn. Action: đề xuất mục tiêu concurrent user và kịch bản performance cho cả hai cổng.
Chú ý: dòng "Reference Document: Meeting's Transcript" trong MoM chỉ là ô liên kết, không có nội dung đi kèm trong file. [Dữ kiện].

## 6. MOE_Sprint1_Clarifications_and_TBD_Register.xlsx

[Dữ kiện] Năm sheet: Summary, About This Workbook, TBD Register, Clarification Log Updates, Meeting Q&A (12 Oct), MoE Agile File Q&A.
Nguồn của sổ: bản ghi buổi họp làm rõ 12/10/2026 (30 phút 13 giây), file MoE_Agile.md (hỏi đáp trước họp), sổ ASM/TBD của Master Test Plan v1.0 r1, MoE_MasterFile.md. Ba file nguồn sau không nằm trong roles. [Suy luận] Đã tìm theo tên trong thư mục roles, không thấy. Buổi "12 Oct" trong sổ có thể chính là buổi kickoff 13:30 đến 14:00 cùng ngày (cùng độ dài khoảng 30 phút), nhưng không có dòng nào trong hai file xác nhận điều này.
Quy ước ID: ASM-xx và TBD-xx là ID cố định từ Master Test Plan, không đánh số lại. NEW-xx là mục mới từ buổi 12/10, đề xuất gộp vào sổ TBD-18 trở đi ở bản v1.1.
Trạng thái sau 12/10 (tôi đã đếm lại từ sheet TBD Register và khớp sheet Summary): Confirmed 17, Partially confirmed 7, Still open 9, Closed 1, tổng 34 (20 mục MTP và 14 mục NEW).

Các quyết định đã xác nhận mà QA hay dùng:
- Student không có role, không đăng nhập (ASM-02). Parent trả bằng số dư của con.
- Đóng tài khoản chuyển số dư sang CPF, được dùng mock API (TBD-05). Chuyển thất bại: giữ quy tắc làm việc là đánh dấu xử lý tay bởi MOE HQ (AC-018-02).
- Số dư mở tài khoản luôn bằng 0, thường có top-up ngay sau khi mở (TBD-15).
- Nguồn quốc tịch là feed tin cậy từ MHA, file đầy đủ cộng thay đổi delta, tần suất cấu hình được hàng tuần hoặc hàng ngày (NEW-02, TBD-03). Cần hợp đồng mock feed cho Sprint 1.
- Công dân hai quốc tịch coi là người Singapore, không nhận hai trợ cấp (NEW-03).
- Công dân đang học ở nước ngoài vẫn kích hoạt tài khoản lúc 7 tuổi (NEW-04).
- Chỉ có hai quỹ: quỹ Education Account và quỹ MOE FAS (NEW-05). Chỉ tính phí sinh ra trong hệ thống (NEW-06).
- Top-up không cần bước duyệt, bước duyệt cấu hình bật tắt là điểm cộng (NEW-07). Mô hình top-up: số tiền cố định và hoặc điều kiện theo số dư với giới hạn trên cấu hình được (NEW-14).
- Phí nào được trả bằng EA phải cấu hình được (NEW-08). Điều kiện FAS phải cấu hình được (NEW-09).
- Dịch vụ thu nhập trả về số thành viên hộ, khoảng thu nhập hộ và khoảng thu nhập bình quân, không trả số chính xác, được dùng mock file (NEW-10).
- Trường do user MOE HQ tạo thủ công (NEW-11). "Cohort" nghĩa là level, không phải năm nhập học (NEW-12).
- Phương thức thanh toán: thẻ tín dụng, PayNow, NETS (TBD-06, một phần xác nhận). Chính sách hoàn tiền vẫn mở. Chia đôi vẫn "deferred pending confirmation".
- FAS: không hưởng cả hai, xét MOEFAS trước, chỉ khi không đủ điều kiện mới xét SBFAS (TBD-07).
- Phí chưa trả không chặn việc đóng tài khoản, nợ được đòi riêng từ phụ huynh (NEW-01). Chưa xác nhận số dư có trừ vào phí trước khi chuyển CPF hay không.

Các mục còn mở: ASM-01 (phạm vi Sprint 1 chốt cuối), ASM-03 (AI), TBD-02 (học sinh nghỉ học trước 16), TBD-04 (mất quốc tịch trước 16: xử lý tài khoản và số dư), TBD-08, TBD-09, TBD-12 (ma trận quyền), TBD-13, TBD-17.
Sheet "MoE Agile File Q&A" có một mục quan trọng: mục 10 ghi quy tắc "trả khoản phí cũ nhất trước" là quyết định của team, không phải client xác nhận. Mục 18 (ví dụ Edusave và GIRO) là ghi chú nghiên cứu nội bộ, không phải yêu cầu. [Dữ kiện] sheet "MoE Agile File Q&A" dòng 10 và 18.
Hai dòng quy tắc quy trình ở Meeting Q&A (mục 24 và 25): xin phép client trước khi ghi âm buổi họp, câu hỏi phải cụ thể và gộp, không hỏi lại điều user story đã trả lời, một khung 30 phút mỗi sprint.

## 7. [Agile] FS R1V1.0.docx (R1: vòng đời Education Account)

Cấu trúc: 1 Detailed Functions (1.1 F01 tạo và kích hoạt tự động, 1.2 F02 đóng tự động), 2 Business Data and Fields, 3 Cross-Function Boundaries, 4 Delivery Limitations. Phân loại quyết định: [CR] client xác nhận, [TD] quyết định của team với Dev, [WA] giả định làm việc của BA chờ team chấp nhận, [Deferred] đã biết nhưng chưa làm trong MVP.

F01 tạo và kích hoạt:
- Hai cơ chế: Initial Synchronization (lấy công dân Singapore từ đủ 7 đến dưới 16 tuổi từ Mock Government Citizen API) và Daily Incremental Synchronization (job hằng ngày 00:00 SGT, chạy cả cuối tuần và ngày lễ [WA], chỉ lấy người vừa đủ 7 tuổi trong ngày xử lý).
- Trường dữ liệu bắt buộc: NRIC, Full Name, DOB, Citizenship, Gender [WA]. Không bắt buộc: Race, địa chỉ, Father NRIC, Mother NRIC. Thiếu trường bắt buộc thì bỏ qua bản ghi và ghi exception.
- Kết quả tạo: Account Number duy nhất, Status Active, Balance SGD 0.00, Currency SGD, ghi Account Creation Date.
- Rule tuổi F01-BR01 đến BR05. Năm sinh 29/02 trong năm không nhuận dùng 28/02 [WA], F01 và F02 phải dùng cùng một rule. Mỗi công dân một tài khoản, NRIC là business identifier, tài khoản Closed vẫn chặn tạo mới, không có hard delete hoặc soft delete trong Sprint 1.
- Job Failure and Recovery (mục 1.1.9) ghi là "next sprint": lỗi xác thực thì không xử lý tiếp, timeout thì retry một lần sau 15 phút, lần chạy sau phải xử lý các ngày bị bỏ lỡ, bản ghi lỗi thì bỏ qua và ghi lý do. Tất cả là [WA].
- Exception: AF01 đến AF04, EF01 đến EF03. Acceptance Criteria F01-AC01 đến AC16, trong danh sách không có F01-AC11 (từ AC10 nhảy sang AC12). [Dữ kiện] mục 1.1.11, nên có 15 AC chứ không phải 16.
- Manual Account Creation và Bulk Re-synchronization là [Deferred] cho sprint sau.

F02 đóng tài khoản:
- [CR] đóng khi đủ 16 tuổi. [TD] kiểm tra điều kiện đóng do backend kích hoạt, không lưu Scheduled Closure Date. Mọi backend action đụng đến Education Account đều phải qua Closure Eligibility Check trước (F02-BR02), gồm xem chi tiết, số dư, lịch sử giao dịch, top-up, payment.
- Check gọi Mock Government Citizen API lấy DOB và Citizenship hiện tại. Đủ 16 tuổi HOẶC không còn là công dân Singapore thì xử lý đóng. Điều kiện mất quốc tịch là [TD] cần client xác nhận (F02-BR05).
- Pending transaction: giả định không có khi đóng [TD]. Số dư còn lại: [CR] phải chuyển CPF nhưng CPF Transfer là [Deferred]. Quy tắc MVP đề xuất [WA]: số dư bằng 0 thì cho đóng, số dư lớn hơn 0 mà CPF chưa làm thì "Closure Deferred": giữ số dư và chặn giao dịch tài chính mới. Đóng do mất quốc tịch chưa có xác nhận cách xử lý số dư.
- Quy tắc F02-BR01 đến BR14, AF01 đến AF05, EF01 đến EF05, F02-AC01 đến AC15 (đủ liên tục).
- Khi Government API lỗi hoặc không trả bản ghi hợp lệ thì không được kết luận đóng (F02-BR14, EF01, EF02) và không cho giao dịch tài chính cần kiểm tra điều kiện đi tiếp.

Phần dữ liệu (mục 2): bảng Student Information (NRIC, Full Name, DOB, Citizenship, Gender, Student Profile Status, Race, Block, Street, Unit, Postal Code, Country, Father NRIC, Mother NRIC), Education Account (Account Number, Account Holder Reference, Account Balance, Account Status Active hoặc Closed), Transaction (Reference Number, Related Account, Direction, Amount, Status, Description, Date, Transaction Type đề xuất gồm Top-Up, Payment, CPF Transfer). Quy tắc: tiền chính xác 2 chữ số thập phân, không hỗ trợ số dư âm [WA], giao dịch thất bại không đổi số dư [WA], Student Profile và Education Account là hai đối tượng độc lập, Student Profile Status không phản ánh Account Active hay Closed.
Mục 3 chia ranh giới giữa F01, F02, R8, xem chi tiết tài khoản, Top-up hoặc Payment, và các chức năng tương lai (tạo tay, đồng bộ hàng loạt, sửa chi tiết student, CPF Transfer).
Mục 4 nêu các giới hạn giao hàng và một quyết định kinh doanh còn mở: xử lý tài chính khi đóng do mất quốc tịch.

## 8. [Agile] FS 08.docx (R8: Parent Portal)

[Dữ kiện] Tên "FS-08: Parent Portal, SingPass, Education Account, Profile". Function FR-08 (R8), Epic EP-08. Người soạn Nguyễn Quốc Huy (PM). Đối tượng đọc Dev và QA. Lịch sử: 0.1 (13/10/2026) tạo mới, 0.2 residential address chỉ đọc (D-20), 0.3 (14/10) thêm tạo tài khoản lần đầu, Parent không có con vẫn đăng nhập, MSG-0808, bỏ chuông thông báo và AI assistant khỏi phạm vi, 0.4 (14/10) bỏ quét đồng bộ hằng đêm, thay bằng gọi API dữ liệu theo NRIC sau khi SingPass thành công, thêm MSG-0809 (D-31). Có link mockup artifact.
Phạm vi trong: (1) đăng nhập SingPass kèm tra cứu API và cập nhật dữ liệu Parent và con, (2) xem chi tiết EA, (3) cập nhật thông tin cá nhân cơ bản, Home. Ngoài phạm vi: thanh toán phí (FS-09), nộp FAS (FS-10), AI assistant (US-08.3).
Ba chức năng:
- FR-08.1 Đăng nhập SingPass: SingPass mock trả NRIC, họ tên, địa chỉ cư trú. Hệ thống gọi API dữ liệu (mock) bằng NRIC để lấy Parent và các con. Không tìm thấy Parent hoặc không có con: MSG-0801. SingPass lỗi hoặc hủy: MSG-0802. API lỗi hoặc quá 10 giây: MSG-0809. Lần đầu tạo tài khoản (UserId, IsActivate true) và liên kết các con, lần sau dùng lại. Cập nhật dữ liệu mới nhất của Parent và các con chỉ cho Parent vừa đăng nhập, phone, email, mailing address chỉ lấy lần đầu và không bị ghi đè sau. Session hết sau 15 phút không thao tác (D-22, MSG-0002). Ghi audit log.
- FR-08.2 Xem Education Account: số dư khả dụng chỉ tính giao dịch Completed, giao dịch Pending hiện riêng ở khung vàng. Trạng thái EA: Active, Due for closure, Closed, To be created, Not yet 7, Not eligible. Con đủ 16 tuổi chỉ xem, không thanh toán, không nộp FAS, và quy tắc áp dụng riêng từng con. Bảng giao dịch 20 dòng mỗi trang, lọc theo ngày, loại (Top-up, Fee payment, Refund, Closure transfer) và chiều tiền. Khối FAS hiện khi có.
- FR-08.3 Sửa thông tin: chỉ phone (8 chữ số bắt đầu 6, 8 hoặc 9), email (tối đa 150 ký tự), mailing address (block, unit tối đa 20, street tối đa 100, postal code 6 chữ số, country tối đa 100). Residential address, NRIC, họ tên chỉ đọc (D-20). Khi mọi con đều đủ 16 tuổi thì My details chỉ xem. Không gửi email khi đổi thông tin (D-28 chỉ áp dụng cho top-up, thanh toán, kết quả FAS). Mã lỗi MSG-0001, 0805, 0806, 0807, 0808.
Màn hình: Landing, Home (card từng con, thứ tự card theo mục 6.1, tối đa 3 khoản phí, dòng "+N more"), Education Account, My details. Phụ lục A là bảng Parent_Profile, phụ lục B là 12 mã message. Mục 8 có 28 tiêu chí nghiệm thu đánh số 1 đến 28. Phi chức năng: kiểm quyền server, không đưa NRIC đầy đủ vào URL, tải trang dưới 3 giây với 1,000 giao dịch, giao diện tiếng Anh, tiền SGD, ngày DD/MM/YYYY, dùng được trên điện thoại.
Sơ đồ swimlane (Parent, Our System, Government System) khớp với luồng chữ. Sơ đồ có chữ "PDF" ở bước xem EA ("số dư, giao dịch, lọc, PDF"). [Dữ kiện] tìm "pdf" trong bản text của FS 08 không có kết quả, nên phần chữ của FS 08 không có yêu cầu PDF cho sao kê EA. [Suy luận] đây là chi tiết sơ đồ chưa có yêu cầu đi kèm, cần hỏi BA nếu test liên quan.

## 9. [Agile] FS 09.docx (R9: Outstanding Fees and Payment, Final)

[Dữ kiện] Đề "FS Function 9 Outstanding Fees and Payment (Final)", ngày 14/10/2026. Phụ huynh xem invoice chưa trả của con và trả bằng EA, online, hoặc chia đôi EA và online.
Cấu trúc: 1 Introduction (Preface, Personas, Design Assumptions DA-01 đến DA-14, Limitations, Definitions, Exclusions, OOS List 9 mục), 2 Process Flow (sơ đồ swimlane và sơ đồ split payment), 3 Detailed Functions (sub-function F9.1 đến F9.7, Business Rules BR-F9-01 đến BR-F9-13, các bước 1 đến 7, ngoại lệ EX-01 đến EX-14), 4 Data Fields (bảng màn hình SCR-01 đến SCR-08, thực thể Invoice, InvoiceItem, Transaction, FundingLeg, WebhookReceipt, AuditLog), 5 Validation (13 mã lỗi, 22 AC là AC-01 đến AC-22), 6 Appendices (A trạng thái, B câu hỏi mở OQ và NQ, C danh sách màn hình).
Điểm thiết kế quan trọng cho QA:
- Đơn vị thanh toán là cả invoice, không trả từng dòng, không trả một phần (BR-F9-13). Chia đôi EA và online được phép, tổng hai phần bằng đúng số phải trả, mỗi nhánh lớn hơn 0.
- Thứ tự chia đôi: trừ EA trước, chỉ mở thanh toán online khi nhánh EA thành công, hoàn EA (reversal) nếu online lỗi, hủy, hết hạn. Không nằm trong một database transaction (DA-14).
- Idempotency key duy nhất theo Parent, nút xác nhận bị vô hiệu sau khi bấm, tối đa một transaction mở và một thành công cho mỗi invoice (BR-F9-04, BR-F9-09, DA-13).
- Webhook phải có chữ ký HMAC hợp lệ, ghi nhận Received ngay rồi xử lý bất đồng bộ, idempotent theo ProviderCode cộng ProviderEventId, chỉ lưu hash payload (BR-F9-06).
- Trạng thái ReconciliationRequired khi kết quả không rõ hoặc hoàn EA lỗi, invoice giữ PaymentPending, vận hành xử lý.
- Thanh toán online dùng sandbox giả lập, dữ liệu invoice và số dư là seed gắn nhãn mẫu (DA-01, DA-11).
Các điểm tôi thấy không khớp hoặc thiếu (tất cả là [Suy luận] từ việc đối chiếu hai mục trong cùng tài liệu hoặc giữa tài liệu, kèm vị trí):
- Bước 4 mục 3.1.2 nói "ba lựa chọn" nhưng chỉ liệt kê hai (Số dư EA, Thanh toán trực tuyến). Phụ lục C SCR-04 liệt kê đủ ba (EA, online, EA cộng online).
- Bước 4 nói khi chia đôi Parent không được nhập số EA (hệ thống tự lấy toàn bộ số dư khả dụng). AC-22 lại nói Parent có thể đổi phần EA thành số nhỏ hơn. BR-F9-10 nói Parent chủ động chọn số tiền từng phần. BR-F9-02 nói phần EA phải bằng số dư khả dụng. Cần hỏi BA quy tắc nào đúng.
- Bước 4 nói số dư lớn hơn hoặc bằng số phải trả thì Parent chỉ chọn EA hoặc online, trong khi BR-F9-02 nói chia đôi cần số dư lớn hơn 0 không nêu giới hạn trên.
- Session portal hết hạn: FS 09 EX-02 ghi 10 phút (TBC), FS 08 mục FR-08.1 và mục 7 ghi 15 phút (D-22).
- Có chuỗi tham chiếu (C1, C2, D1, D3, D4, D5, D8, VAL-18) không được định nghĩa ở nơi nào trong FS 09. Mục 5 nhảy từ 5.1 sang 5.3. Phụ lục B không có tiêu đề. Chữ "Refuned" trong định nghĩa Reversal. [Dữ kiện] đã tìm trong bản text của FS 09.
- Chia đôi: FS 09 Final đưa vào phạm vi, nhưng TBD register (TBD-06) vẫn ghi "split/combined payment still deferred pending confirmation" và Q13 của first meeting giả định không có split. [Suy luận] FS 09 là bản mới hơn (14/10) so với register (sau 12/10), nên chia đôi có thể là quyết định của team chưa phản ánh vào register. Không tìm thấy bằng chứng client đã xác nhận chia đôi trong role ba.
- Mức tối thiểu của từng phần khi chia đôi, thời hạn phiên online (đề xuất 10 phút), ngưỡng chuyển ReconciliationRequired chưa chốt (TBC, NQ-10, NQ-13, NQ-18).

Ba sơ đồ trong FS 09 đã xem: (1) swimlane Parent, E-Service System, Third-party Online Payment, (2) lưu đồ chia đôi (đặt phần EA, trừ EA, nếu OK thì mở phần online, chờ kết quả, nếu thất bại hoặc hết hạn thì hoàn EA, hoàn lỗi thì ReconciliationRequired), (3) sơ đồ trạng thái Transaction (Pending sang Succeeded, Failed, Cancelled, ReconciliationRequired) và Funding leg (Pending, Succeeded, Reversed, có thể Failed, Cancelled, ReconciliationRequired). Các sơ đồ khớp với Phụ lục A.

## 10. Quan hệ giữa các file trong role ba và cách dùng

- Kiểm tra giả định của FS: tra TBD register theo ID, rồi đối chiếu First meeting questions (câu hỏi gốc) và MoM (agenda).
- R1 (F01, F02) liên quan R8 (liên kết Parent và Student khi đăng nhập) và R9 (kiểm tra điều kiện đóng trước giao dịch tài chính). FS R1 mục 3 mô tả ranh giới.
- R8 gọi R9: card Home và trang EA có liên kết "View fee" sang trang phí (FS-09). Con đủ 16 tuổi chỉ xem, không thanh toán.
- Chỗ chưa khớp cần hỏi BA đã liệt kê ở mục 9, ngoài ra có thêm hai điểm giữa FS 08 và FS R1: FS 08 hiện "ngày đóng dự kiến" và trạng thái "Due for closure" (tính từ sinh nhật 16), còn FS R1 nói không lưu Scheduled Closure Date và đóng khi có backend action. [Suy luận] không nhất thiết mâu thuẫn vì ngày đóng có thể tính từ DOB, nhưng chưa có câu nào xác nhận. FS 08 liệt kê loại giao dịch "Closure transfer" trong khi FS R1 ghi CPF Transfer là Deferred.

## 11. [Agile] FS.docx (R4: đơn FAS, F4 FAS Applications v1.1)

Độ sâu đọc: toàn bộ chữ (697 dòng), chưa xem 7 hình minh họa. Đọc ngày 2026-10-18. File thêm vào roles\ba lúc 20:12 cùng ngày. Tên trùng với file "[Agile] FS.docx" cũ (FS đầu, nguồn F03 chuyển CPF) đã không còn trong roles\ba, nội dung khác hẳn.

[Dữ kiện] Đầu file ghi "FS F4 – FAS Applications, Oct 18, 2026, Version 1.1, @Huy". Màu vàng là phần đổi so với v1.0, màu xanh là phần mới ở v1.1. Bản v1.0 không có trong roles. Phạm vi: Admin Portal, School Admin và MOE HQ xem danh sách đơn FAS (MOEFAS và SBFAS), mở drawer xem chi tiết, duyệt hoặc từ chối, trợ cấp được áp vào phí EA của học sinh. Engine chấm điểm theo luật (Need Score 0 đến 100, tier gợi ý, ML risk Low, Medium, High) chỉ để tham khảo. Ngoài phạm vi: upload đơn giấy (F5), tạo và sửa scheme, màn hình Parent, đặt budget (F6), huấn luyện mô hình ML. Trạng thái chỉ có Pending, Approved, Rejected, FS nói rõ không có Auto-granted. Có 20 business rule (BR1 đến BR20), bảng thông báo và 35 kịch bản T1 đến T35 (không có T13, T32 nằm sau T19).

[Suy luận, bằng chứng nêu cạnh từng ý] Các điểm lệch cần hỏi BA:
- Tender hàng 4 viết MOEFAS "should be automatically granted" khi đạt tiêu chí và cây chức năng mục 4.5 cũng ghi tự động cấp, còn FS F4 bước 2, BR1 và T7 ghi MOE HQ quyết định mọi đơn MOEFAS, không tự động duyệt hay từ chối. CLAUDE.md quy định khi mâu thuẫn thì tin tender.
- Mục 6.1 dropdown Tier chỉ có Tier 1 đến 3 (mục 1.3 cũng định nghĩa 3 tier), nhưng mục 5.3 có Base Tier và Adjusted Tier 4, nên engine có thể gợi ý Tier 4 mà người duyệt không chọn được.
- Tender dùng chữ Machine Learning, FS gọi là ML nhưng nói engine là rule-based, xác định, không huấn luyện mô hình (mục 1.1 và 5).
- Kiểm tay T33: Need Score 0.70 x 0.75 + 0.05 x 0.75 + 0.10 x 0.80 + 0.10 x 0.50 + 0.05 x 0.10 = 0.6975, tức 69.75, khớp FS. Base Tier 1, Adjusted Tier 2, risk Medium cũng khớp bảng 5.3.
- BR16 quy định ngày DD/MM/YYYY, giờ HH:mm theo giờ Singapore (UTC+8). Chưa kiểm FS 08 và FS 09 có cùng quy định không.
- Phụ thuộc không có FS trong roles\ba: F5 upload, F6 budget, thiết lập scheme và nguồn dữ liệu thu nhập.

## 12. FS04.docx (R4: FS F4 v1.3, thêm 2026-10-19)

[Dữ kiện] File mới trong roles\ba, 19/10/2026, tác giả @Huy, có 15 hình nhúng. Tiêu đề FS F4 FAS Applications, có mục Changes from v1.2. Cấu trúc: 1 Introduction, 2 Process flow and statuses, 3 danh sách đơn, 4 Review drawer, 5 ML assessment, 6 dialog Approve và Reject, 7 FAS schemes (danh sách, wizard, publish, Add fee, Close form now), 8 After a decision, 9 Business rules BR1 đến BR13, 10 Test scenarios T1 đến T15.
[Dữ kiện] FS04 thay [Agile] FS.docx (FS F4 v1.1, mục 11). Điểm khác chính: MOEFAS do hệ thống tự xét sau khi form đóng theo thứ tự PCI thấp nhất, rồi GHI thấp nhất, rồi nộp sớm nhất. Đạt thì Approved bởi System (auto-approved). Không đạt thì SBFAS Pending nếu phụ huynh chọn Also consider SBFAS, ngược lại Rejected với lý do Not eligible for MOEFAS. PR và International vào thẳng SBFAS Pending. School Admin chỉ quyết SBFAS bằng cách chọn một scheme, MOE HQ chỉ xem. ML chỉ để xem. Điểm auto-grant mà mục 11 nêu đã được FS04 đóng.
[Dữ kiện] Độ sâu đọc: toàn bộ chữ (trích thành 126 mục FS để làm workbook test case). Hình nhúng không ghi nhận đã xem lại ở bước này.
[Suy luận] Mục 11 vẫn đúng cho FS v1.1 nhưng không còn là nguồn chính của R4. Dùng FS04 làm nguồn chính. Xem qa.md mục 11 cho bảng so sánh với prototype và test case.
