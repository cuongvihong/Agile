# Audit assertion R9 automation — case nào có thể "pass giả"

Soát tĩnh (không chạy pytest, container này không vào được localhost của anh). Đối chiếu từng test trong
`tests/test_f91_*.py` đến `test_f99_*.py` với cột Title/Expected Result của `R9_Test_Cases_final_FS09.xlsx`
(sheet `Test cases `, 187 dòng, khớp số case COVERAGE.md khai 185/187 automated), cùng `pages/db.py`,
`pages/postconditions.py`, `conftest.py`, `reporting.py`, `artifacts/reports/r9_case_report.csv`.

## Tóm tắt số liệu

- Test function đọc: toàn bộ 9 file `test_f91` đến `test_f99` (khoảng 240 lượt tham chiếu TC-id, nhiều case có 2 test: 1 qua UI/mutating + 1 qua API self-cleaning).
- **9 TC-id xác nhận bằng tay là mã test KHÔNG còn khớp với case hiện hành cùng ID** (chi tiết mục 1) — do số case bị dịch sau các lần "rút gọn"/thêm case (19 case bỏ ngày 22/10, rồi thêm TC-173→206 ngày 25/10) mà automation không được remap lại toàn bộ, chỉ xóa đúng 3 test cho 3 ID bị xóa hẳn (TC-037, TC-044, TC-064 theo session log 22/10). Đây là audit tĩnh có chọn mẫu theo cụm (TC-066→076, TC-094→099, TC-166), **chưa rà hết 187 case** — khả năng còn mismatch khác ngoài cụm đã kiểm.
- **7 test xfail (`known_defect`) đọc file `.cs` theo đường dẫn tuyệt đối Windows `D:\AIQA\...`** — không chạy được trên máy khác, và vì `strict=False` nên khi file không tồn tại, lỗi mở file cũng bị tính là XFAIL giống như khi defect thật tồn tại (mục 2).
- **3 test "audit log" chỉ kiểm bảng có tên chứa `audit` tồn tại** (`SELECT COUNT(1) FROM sys.tables WHERE name LIKE '%audit%'`), không kiểm có dòng audit nào được ghi cho đúng giao dịch (mục 3) — đúng kiểu assertion lỏng anh lo ngại, và cả 2 trong 3 test này (TC-071, TC-076) còn trùng với finding mục 1 (ID đã lệch sang case khác).
- `xfail(strict=False)`: XPASS không làm fail suite, nhưng `reporting.py` có xử lý riêng, hiện rõ dòng "XPASS, có thể đã hết lỗi" trong report — nên không mất tín hiệu nếu đọc report, chỉ mất nếu chỉ nhìn exit code pytest thô.
- Report CSV gần nhất (`artifacts/reports/r9_case_report.csv`) toàn bộ 187 dòng là "KHÔNG CHẠY LẦN NÀY" — đây là lần collect, **chưa phải bằng chứng ĐẠT/FAIL thật**, khớp với session log (mode `rules` chưa chạy trên máy anh).
- Có 1 bằng chứng viết sẵn trong code xác nhận đúng loại lỗi anh hỏi đã từng xảy ra thật: known_defect reason của TC-028/030 (`test_f92`, dòng 150) ghi "Trước đó test báo đạt giả vì mặc định 'Active'" — tức từng có test pass sai vì gán cứng giá trị mặc định, đã bị phát hiện và sửa ngày 25/10/2026.

## 1. ID đã lệch — test gắn nhãn TC-xxx nhưng kiểm case khác (nhóm trọng tâm: audit/idempotency TC-066→076, both/split TC-094→099, TC-166)

| Test (file:line) | Nội dung test đang kiểm | Workbook TC-id đó hiện là | Đánh giá |
|---|---|---|---|
| `test_f94...:294 test_tc_068_paying_one_of_two_open_charges_leaves_the_other_open` | Trả 1 trong 2 khoản phí, khoản còn lại vẫn mở | TC-068 = "Balance equal to the amount to pay is paid and the balance becomes 0.00" | **Lệch hẳn.** Nội dung test lại khớp với TC-066 hiện tại ("Status changes... audit log" — không, thực ra khớp ý "trả hết 1 khoản, khoản 2 còn mở" gần với không ID nào liền kề rõ — cần BA/QA đối chiếu lại thủ công) |
| `test_f94...:256 test_tc_066_pay_invoice_in_full_with_ea_when_balance_equals_invoice` | Ví = đúng số tiền khoản phí → về 0.00 | TC-066 hiện là "Status changes of an EA payment follow Appendix A and are **written to the audit log**" | **Lệch.** Test không kiểm audit log nào, chỉ kiểm số dư 0.00. Nội dung test lại khớp nghĩa với TC-068 hiện tại ("balance equal to amount... becomes 0.00") |
| `test_f94...:309 test_tc_071_audit_entry_written_when_ea_payment_succeeds` | Chỉ kiểm bảng tên chứa `audit` tồn tại | TC-071 hiện là "Balance falling below the amount before confirm **fails the EA leg** and changes nothing" | **Lệch hẳn + assertion yếu** (xem mục 3) |
| `test_f94...:331 test_tc_073_when_ea_service_unreachable_payment_shows_safe_message` | Đọc source `.cs`, tìm câu thông báo khi EA service không phản hồi/timeout | TC-073 hiện là "**Unclear debit result** with Function 1 confirming nothing was debited fails the leg" | **Lệch tiền điều kiện.** Test giả định "service không phản hồi", case hiện tại là "Function 1 trả lời rõ là chưa trừ" — khác tình huống |
| `test_f94...:339 test_tc_074_if_saving_payment_fails_after_ea_deducted_deduction_is_reversed` | Giả định: lưu DB lỗi sau khi đã trừ EA → hoàn tiền | TC-074 hiện là "Unclear debit result **with Function 1 confirming the debit** leads to a reversal" | **Lệch tiền điều kiện** (tương tự trên, chung chủ đề reversal nhưng nguyên nhân khác) |
| `test_f94...:347 test_tc_075_if_ea_reversal_also_fails_payment_marked_for_manual_review` | Giả định: hoàn tiền EA cũng thất bại | TC-075 hiện là "Unclear debit result **that stays unclear** moves to ReconciliationRequired" | **Lệch tiền điều kiện** (cùng đích ReconciliationRequired, khác nguyên nhân) |
| `test_f94...:354 test_tc_076_audit_entry_written_when_ea_deduction_is_reversed` | Chỉ kiểm bảng tên chứa `audit` tồn tại | TC-076 hiện là "**Function 1 treats the same FundingReference as one debit**" (chống trùng lặp debit) | **Lệch hẳn + assertion yếu** (xem mục 3) |
| `test_f95...:306 test_tc_094_when_provider_cannot_create_session_payment_fails_cleanly` | Đọc source, tìm `invoice.Status = InvoiceStatus.Issued` khi không mở được phiên cổng | TC-094 hiện là "**Closing the browser** on the provider page keeps the payment Pending until the result arrives" | **Lệch hẳn.** Case hiện tại nói về đóng trình duyệt giữ Pending, không phải lỗi tạo phiên |
| `test_f95...:357 test_tc_098_funding_parts_and_audit_entries_for_both_recorded_in_order` | Kiểm sequence 1=EA, 2=Online + bảng `audit` tồn tại | TC-098 hiện là "**The EA is debited before the online payment session is created**" | **Lệch, nhưng gần đúng chủ đề kế bên.** Nội dung test khớp đúng với `test_tc_099` (dòng 375) đang kiểm — tức cụm 098/099 lệch 1 số, và phần audit trong test_098 vẫn là assertion yếu (mục 3) |
| `test_f94...:466 test_tc_166_editing_invoice_while_payment_in_progress_triggers_ea_reversal` | Đọc source, tìm dòng tắt `IsRowVersion()` để suy ra xung đột version khi sửa invoice đang thanh toán | TC-166 hiện là "A **second guardian** pays an invoice of the shared child and the payment is recorded for that guardian" | **Lệch hẳn**, không liên quan gì đến second guardian |

Ghi chú: TC-065 và TC-067 KHÔNG đưa vào bảng trên — số tiền trong test (`120.00`, `80.00+70.00`) khác số tiền minh họa trong Expected Result (`27.25`, `22.23`) nhưng đúng là cùng loại rule đang kiểm (trả 1 khoản EA hết nợ; trả hóa đơn 2 dòng bằng EA), nên không tính là lệch case — chỉ là dùng seed/temp_charges thế số khác với ví dụ trong FS.

**Khuyến nghị:** dựng lại bảng map TC-id ↔ tên hàm test cho toàn bộ 187 case (không chỉ cụm đã kiểm ở trên) rồi đối chiếu bằng tay hoặc bằng BA/QA Lead, vì ít nhất 2 lần sửa workbook (22/10 bỏ 19 case, 25/10 thêm case) có khả năng đã dịch số nhiều case khác ngoài 2 cụm này mà audit tĩnh lần này không có thời gian rà hết.

## 2. Test known_defect đọc file theo đường dẫn tuyệt đối Windows (không chạy được, không phản ánh đúng hệ thống thật)

7 test, toàn bộ nhãn `known_defect` (xfail strict=False), mở trực tiếp:
`D:\AIQA\Agileproject\roles\dev\code\QA_BE\BillingPaymentService\...\CreateCheckoutHandler.cs` hoặc
`...\InvoiceModelCreating.cs`:

- `test_f94_pay_with_ea.py:333, 341, 349, 468` (TC-073, TC-074, TC-075, TC-166)
- `test_f95_online_and_split.py:308, 453, 461` (TC-094, TC-105, TC-107)

**Vấn đề:** nếu đường dẫn này không tồn tại trên máy chạy pytest (ví dụ máy khác của anh, máy CI, hay sau khi dọn `roles/dev/code`), lệnh `open(...)` ném `FileNotFoundError`. Vì test này đã bị đánh `xfail(strict=False)`, pytest coi exception đó như "thất bại dự kiến" — **XFAIL hiện ra giống hệt trường hợp defect thật còn tồn tại**, dù thực ra test chưa từng đọc được dòng code nào để xác nhận. Đây là dạng "pass giả" nguy hiểm hơn cả assertion lỏng: kết quả test hoàn toàn không phản ánh trạng thái hệ thống thật, chỉ phản ánh máy đang chạy pytest có đúng đường dẫn `D:\AIQA\...` hay không.

**Khuyến nghị:** đổi sang đường dẫn tương đối từ root automation hoặc biến môi trường (`R9_BACKEND_SRC`), và thêm bước kiểm `assert os.path.exists(path)` tách riêng khỏi assertion chính để FileNotFoundError không bị nuốt chung vào xfail.

## 3. Assertion "audit log" chỉ kiểm sự tồn tại của bảng, không kiểm bản ghi thật

3 chỗ:
- `test_f94_pay_with_ea.py:309-312` (TC-071 theo nhãn cũ)
- `test_f94_pay_with_ea.py:354-357` (TC-076 theo nhãn cũ)
- `test_f95_online_and_split.py:357-371` (TC-098 theo nhãn cũ, phần cuối hàm)

Cả 3 đều chỉ chạy:
```sql
SELECT COUNT(1) FROM sys.tables WHERE name LIKE '%audit%'
```
rồi `assert int(cnt or "0") > 0`. Test này **pass ngay cả khi không có bản ghi audit nào được tạo cho giao dịch đang test** — chỉ cần schema có một bảng tên chứa "audit" ở bất kỳ đâu trong DB là đủ đỗ. Không kiểm: đúng loại event (`F9_PAYMENT_INITIATED`/`F9_PAYMENT_COMPLETED` như docstring TC-071 cũ nêu), đúng `transaction_id`, đúng thời điểm. Đây là assertion yếu thật sự, đúng với lo ngại anh nêu ("chỉ cần có gì đó là pass").

**Khuyến nghị:** nếu có bảng audit thật (cần xác nhận tên bảng — hiện code chỉ biết nó "có tên chứa audit"), sửa thành `SELECT COUNT(1) FROM dbo.<tên bảng> WHERE transaction_id = '...' AND event_type IN (...)`. Nếu DB chưa có bảng audit cho billing (nhiều khả năng — comment gốc nói "DB BillingPaymentService chưa có bảng lưu nhật ký audit cho thanh toán F9"), 3 case này nên ở trạng thái Block/known_defect rõ ràng là "chưa thể kiểm vì thiếu audit log", không nên pass im lặng.

## 4. Nhóm payment/webhook/split/reconciliation (trọng tâm câu hỏi của anh) — ngoài 2 mục trên, phần còn lại ĐÃ KIỂM VÀ TỐT

Đọc toàn bộ `test_f94_pay_with_ea.py`, `test_f95_online_and_split.py`, `test_f96_webhook_and_reconciliation.py`,
`test_f97_result_and_receipt.py` cùng `pages/postconditions.py::assert_backend_state` và `pages/db.py::sign_webhook/post_webhook`.
Trừ các case đã nêu ở mục 1-3, các test fail-payment còn lại đều kiểm **đúng lý do và đúng hệ quả cụ thể**, không chỉ "có lỗi là pass":

- Webhook: kiểm đúng mã trạng thái (401 cho thiếu/sai chữ ký, HMAC SHA-256 tính lại đúng công thức `t.{raw_body}`; 200 + `processingStatus` cụ thể Processed/Ignored/Failed), đúng `processing_status` số (2/3/4) trong `payment_webhook_receipts`, đúng transaction/invoice KHÔNG đổi khi bị từ chối (`test_tc_111` đến `test_tc_114`).
- Online payment fail (`test_tc_136`): kiểm đúng tiêu đề Failed, đúng câu thông báo, đúng leg Online = Failed qua `assert_backend_state`, đúng số dư EA không đổi — không chỉ "status != success".
- Split/Both (`test_tc_097`, `test_tc_103`): kiểm đúng từng leg theo method, đúng số tiền từng phần, đúng invoice Paid/Issued, đúng số dư ví về đúng giá trị kỳ vọng (không phải chỉ "khác 0" hay "có thay đổi").
- `assert_backend_state` (`pages/postconditions.py:59-69`) so khớp field-by-field (status transaction, dict legs theo method, status invoice) — không có nhánh nào "bỏ qua nếu không khớp".

Đây là phần đáng tin cậy nhất của bộ automation hiện tại.

## 5. Các điểm phụ (mức độ thấp hơn)

- `status in (400, 403, 404)` / `(400, 409, 422)` / `(400, 413, 422)` — xuất hiện ở `test_f91`, `test_f93`, `test_f98`, `test_f99` cho case validation. Chấp nhận được vì khoảng mã không lẫn với mã thành công (200), nhưng không chốt đúng 1 mã cụ thể — nếu BA/Dev muốn chốt mã chính xác cho từng case thì cần thu hẹp.
- `post_webhook()` (`pages/db.py:355`) luôn gửi `"status": "Succeeded" if event_type == "payment.succeeded" else "Failed"` trong payload — với `payment.cancelled`/`payment.expired` trường `status` gửi đi vẫn là `"Failed"`, có thể không đúng với format gateway thật gửi cho các event đó (chưa xác nhận được vì không có mẫu payload thật của gateway).

## 6. Case khai automate nhưng có thể không có assertion ý nghĩa — không phát hiện thêm ngoài mục 3

Không thấy test nào có thân hàm trống, `assert True`, hay `except: pass` nuốt lỗi trong các file `tests/`. 2 chỗ `except Exception: pass` nằm trong `pages/accounts_page.py` (dòng 57-58, 98-99), là code đọc UI phụ trợ (page object), không phải assertion của test — cần xem thêm nếu lỗi bị nuốt ở đây làm test sau đọc dữ liệu rỗng mà không báo, nhưng chưa thấy triệu chứng cụ thể trong lần đọc này.
