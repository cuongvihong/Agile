# Giải thích các khái niệm / câu hỏi đã trao đổi

Ghi lại các giải thích cho câu hỏi anh đã hỏi trong buổi làm việc, để tra lại sau không cần đọc lại cả đoạn chat. Cập nhật thêm mỗi khi có câu hỏi mới cần giải thích.

## Khi nhận tender, agile làm gì trước

Thứ tự chung: đọc tender → làm rõ chỗ mơ hồ qua kick-off → BA/PO chuyển thành user story → cả team estimate → PO sắp backlog theo ưu tiên → PM chốt timeline → Scrum Master setup nhịp sprint → sprint đầu tiên chọn việc ưu tiên cao nhất vào làm.

## QA có phải chờ có FSD/user story mới làm được gì không

Không hoàn toàn. Tách làm 3 mức:

| Việc | Cần FSD/user story ổn định? |
|---|---|
| Test Strategy (chiến lược chung) | Không — chỉ cần tender + timeline là đủ |
| Test scenario cấp cao (liệt kê tình huống cần test) | Không bắt buộc, nhưng có thì tốt hơn |
| Test case chi tiết (từng bước, kết quả mong đợi) | **Có** — thiếu thì QA chỉ đoán, dễ phải viết lại khi requirement đổi |

Đây là tinh thần "shift-left testing": QA tham gia càng sớm càng tốt, nhưng việc càng chi tiết thì càng cần nền tảng requirement càng ổn định.

## Test Strategy khác Test Plan ở chỗ nào

| | Test Strategy | Test Plan |
|---|---|---|
| Phạm vi | Nguyên tắc chung, áp dụng xuyên suốt cả dự án | Cụ thể cho 1 chu kỳ/sprint/release |
| Nội dung | Mức độ test nào ai làm, cách test AI/ML, severity/priority, metrics | Lịch trình theo ngày/sprint, entry/exit criteria cụ thể, RACI có tên người |
| Có đổi theo thời gian không | Hiếm khi đổi, chỉ đổi khi có thay đổi lớn | Đổi mỗi chu kỳ/sprint |

File thật trong project: `roles/qalead/test-strategy.md` và `roles/qalead/test-plan.md`.

## Tại sao tách riêng "Blocking Register" và "Business Impact Register"

Khi phân tích tender tìm ra những chỗ chưa rõ, 2 loại rủi ro khác nhau hoàn toàn:

- **Blocking (chặn tiến độ)**: thiếu thông tin này thì team không build được, hoặc phải đoán kiến trúc rồi làm lại. Ví dụ: chưa có quyền truy cập SingPass sandbox thì không code/test được phần đăng nhập.
- **Business impact (ảnh hưởng nghiệp vụ)**: build được bình thường, nhưng nếu đoán sai thì gây hậu quả thật cho người dùng/tiền bạc/pháp lý. Ví dụ: không rõ số dư tài khoản đi đâu khi tự đóng ở tuổi 16 — vẫn build được tính năng đóng tài khoản, nhưng đoán sai thì phụ huynh mất tiền thật.

Gộp chung 2 loại này vào 1 bảng sẽ làm lẫn lộn "cái gì phải hỏi ngay để code được" với "cái gì phải hỏi trước khi release để khỏi gây hại" — 2 mức độ khẩn cấp khác nhau. File thật: `roles/qalead/assumptions-negotiation-register.md`.

## Phát hiện quan trọng từ backlog của PO: "training prototype"

Ban đầu tôi (QA Lead) xếp SingPass/API thu nhập/cổng thanh toán vào mức **Critical — chặn cả dự án**, với giả định đây là dự án giao hàng thật cho MOE, cần khách hàng cấp quyền truy cập thật.

Khi đọc backlog của PO mới phát hiện: đây là **bài tập mô phỏng (training prototype)**, các tích hợp này đều **giả lập**. Vậy 3 mục đó không còn là thứ phải "xin khách hàng" nữa, mà chỉ là "team tự thống nhất cách giả lập" — mức độ khẩn cấp giảm hẳn.

Bài học: luôn đọc kỹ xem dự án có phải "thật" hay "mô phỏng" trước khi đánh giá mức độ nghiêm trọng của một rủi ro — cùng 1 câu hỏi nhưng bối cảnh khác thì mức độ khẩn cấp khác hẳn.

## Vì sao Claude chỉ đóng vai QA và QA Lead trong project này

Theo yêu cầu của anh: các role khác (BA, PO, PM, Scrum Master, Dev, Dev Lead) do người thật trong team đảm nhiệm. Claude chỉ đọc output của họ (đặt trong `roles/<role>/`) để làm input cho công việc QA, không tự viết thay nội dung của role khác. File `roles/pm/project-plan.md` là ngoại lệ — viết trước khi có quy định này, giữ lại làm tài liệu tham khảo thôi, không còn được cập nhật thêm.
