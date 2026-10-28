# Case R9 bị bỏ khi đối chiếu với FS Final

Ngày 22/10/2026. Anh gửi file Tổng hợp FS (FS Function 9 Final, ngày 14/10/2026) và dặn: chỉ giữ case có trong FS, case nào FS không nói thì bỏ. Văn bản của file này giống hệt `roles/ba/[Agile] FS 09.docx` mà bản rev hôm qua đã dùng, nên không có yêu cầu mới nào được thêm vào, chỉ có case bị bỏ.

Tiêu chí: một case được giữ khi kết quả mong đợi của nó được FS nêu trực tiếp (quy tắc BR, luồng bước, EX, AC, thông báo ở mục 5.1, bảng trường ở mục 4, trạng thái ở Appendix A). Một case bị bỏ khi kết quả mong đợi chỉ có được nhờ giả định lấp chỗ FS im lặng hoặc để TBC.

Kết quả: bản `R9_Test_Cases_final_FS09.xlsx` có **153 case** (bản rev 172, bỏ 19). Mã case không đánh số lại, nên các mã bên dưới vắng mặt trong sổ. Execution Status không đổi (Not Run 140, Passed 5, Failed 8); Review Status còn Approve 111, Draft 42, Block 0.

## 19 case đã bỏ

| Case | Tiêu đề | Test Suite | Review Status cũ | Vì sao bỏ |
|---|---|---|---|---|
| TC-026 | An invoice past its due date is listed and can be paid | F9.2 Outstanding invoices and EA balance | Draft | Quá hạn: FS để TBC cách hiển thị và không nêu hành vi (SCR-02 Due date, OQ-04, NQ-03). |
| TC-037 | Back from the payment method screen returns to the invoice list and creates nothing | F9.3 Payment method and eligibility | Draft | FS không nói nút Back của SCR-04 dẫn về đâu (Appendix C chỉ ghi 'quay lại'). |
| TC-044 | Balance one cent below the amount to pay offers split with an online part of 0.01 | F9.3 Payment method and eligibility | Draft | Dựa vào mức tối thiểu phần online của provider mà FS chưa chốt (NQ-13, TBC). |
| TC-059 | An EA part with more than two decimals or with text is refused | F9.3 Payment method and eligibility | Draft | VAL-18 không được mô tả; FS không nêu cách kiểm số thập phân hoặc chữ ở ô số tiền. |
| TC-060 | Online part exactly at the provider minimum is accepted | F9.3 Payment method and eligibility | Draft | Mức tối thiểu phần online của provider chưa chốt (NQ-13, TBC), không có giá trị để thử. |
| TC-061 | Online part just below the provider minimum is refused | F9.3 Payment method and eligibility | Draft | Mức tối thiểu phần online của provider chưa chốt (NQ-13, TBC), không có giá trị để thử. |
| TC-064 | Cancel on the review screen returns to the payment method screen and creates nothing | F9.4 Pay with Education Account | Draft | FS không nói nút Hủy của SCR-05 dẫn về đâu (Appendix C chỉ ghi 'hủy'). |
| TC-069 | The EA pays each of the four fee types | F9.4 Pay with Education Account | Draft | Loại phí nào được trả bằng EA là câu hỏi mở OQ-11; FS không nêu. |
| TC-093 | A provider that refuses to open the payment session fails the payment | F9.5 Pay online | Draft | FS chỉ nêu provider timeout hay lỗi mạng (EX-08); không nêu trường hợp provider từ chối tạo phiên thanh toán. |
| TC-106 | A provider that refuses the payment session after the EA debit returns the EA part | F9.4 and F9.5 Split payment | Draft | Như TC-093 nhưng sau khi đã ghi nợ EA: FS không nêu provider từ chối tạo phiên. |
| TC-116 | A new event for a payment that is already finished changes nothing | F9.6 Webhook and reconciliation | Draft | FS không nêu xử lý callback hợp lệ tới nhánh đã ở trạng thái cuối. |
| TC-117 | A valid callback that matches no payment is ignored | F9.6 Webhook and reconciliation | Draft | FS không nêu xử lý callback hợp lệ với FundingReference không có trong hệ thống. |
| TC-118 | A success callback with a different amount does not pay the invoice | F9.6 Webhook and reconciliation | Draft | FS không nêu xử lý callback báo số tiền khác số tiền của nhánh. |
| TC-124 | Operations resolves a payment in ReconciliationRequired | F9.6 Webhook and reconciliation | Block | FS không có màn hình, API hay quy trình cho bộ phận vận hành xử lý ReconciliationRequired (Appendix A chỉ ghi 'Bộ phận vận hành xử lý'). |
| TC-134 | Transaction references are unique and follow the proposed format | F9.7 Result, receipt and retry | Draft | Định dạng mã tham chiếu PAY-YYYYMMDD-XXXXXX chỉ là đề xuất (TBC, NQ-12). |
| TC-163 | API refuses a split when the balance already covers the whole invoice | F9.3 Payment method and eligibility | Draft | FS không nêu API từ chối chia đôi khi số dư đủ trả cả invoice (Bước 4 chỉ nói Parent không được chọn chia đôi). |
| TC-165 | Label of a child whose only open invoice is waiting for payment | F9.1 Access and child list | Draft | FS 4.1 SCR-01 chỉ nói nhãn tính từ invoice Issued; không nêu nhãn của con chỉ có invoice PaymentPending. |
| TC-170 | An Issued invoice cannot be edited and can only be cancelled | Data rules and constraints | Draft | FS chỉ nói invoice đã phát hành là bất biến (1.4, EX-14); không nêu trường nào bị khóa hay cách từ chối sửa. |
| TC-172 | An update that carries an old RowVersion is refused | Data rules and constraints | Draft | FS 4.2 chỉ nói RowVersion là token kiểm soát đồng thời; không nêu xử lý khi mang RowVersion cũ. |

## Giả định đã đóng

Mười giả định không còn case nào dựa vào, nên cột State ở sheet Assumptions chuyển sang Closed: ASM-R9-04, 11, 12, 20, 21, 22, 25, 33, 34, 35.

## Case còn giữ nhưng cần BA lưu ý

FS Final tự mâu thuẫn ở phần Education Account của chia đôi. Bước 4 và BR-F9-02 nói phần EA là toàn bộ số dư khả dụng và Parent không nhập số. Nhưng DA-08, BR-F9-10, bảng trường SCR-04 (EA amount, Nhập = Có), AC-22 và thông báo SPLIT_AMOUNT_INVALID (đánh dấu ô nhập) nói Parent chọn được số tiền. Các case TC-053 đến TC-058, TC-062 và các case chia đôi khác vẫn giữ vì có câu của FS đỡ cho chúng (ASM-R9-01), nhưng nếu BA chốt theo Bước 4 thì cả nhóm này phải bỏ. Bản build thật đang theo Bước 4 (không có ô nhập phần EA).

Sáu case còn giữ nhưng một phần kết quả mong đợi là giả định: TC-078 (lần gửi lại trả kết quả của lần đầu, ASM-R9-17; phần FS nêu là không thu hai lần, AC-05), TC-148 (huỷ invoice có giải phóng khoản phí không, ASM-R9-27), TC-081 và TC-080 (độ dài khóa, FS chỉ nói tối đa 100 ký tự), TC-143 (ngưỡng thời gian phiên TBC), TC-122 (ngưỡng đối soát do Dev cấu hình).

## Automation theo sổ mới

Ba test của case đã bỏ bị xóa khỏi r9_automation: TC-037, TC-044, TC-064. Độ phủ còn 73 trên 153 case, 96 test chạy được, 80 case chưa tự động hóa.
