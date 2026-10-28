# Giải thích chi tiết 10 requirement trong tender

Giải thích đơn giản, dễ hiểu từng mục — không phải FSD kỹ thuật. Đánh số theo đúng số thứ tự trong tender (`groundtruth/592ba6ad-image.png`).

## #1 — Tài khoản giáo dục (Education Account)

Mỗi trẻ công dân Singapore tự động có 1 tài khoản khi tròn 7 tuổi. Tài khoản này giữ tiền để trả học phí trường công.

**Tự động deactivate (xác nhận 2026-10-11)**: tài khoản deactivate **1 ngày trước khi học sinh đủ 16 tuổi**, HOẶC **ngay khi mất quốc tịch Singapore** — cái nào xảy ra thì tính cái đó.

Câu hỏi vẫn chưa rõ: số dư còn lại khi tài khoản deactivate thì đi đâu — đây là điểm rủi ro tài chính lớn nhất của cả hệ thống (xem `roles/qalead/assumptions-negotiation-register.md` Table 2, hạng 2). Cũng chưa rõ: nếu trẻ trở thành công dân SAU tuổi 7 (nhập tịch), tài khoản có được tạo ngay lúc đó không (Table 1, hạng 8).

## #2 — Nạp tiền (Top-up)

MOE HQ nạp tiền vào tài khoản. Có 2 kiểu:
- **Cá nhân**: nạp cho 1 người cụ thể.
- **Hàng loạt (batch)**: nạp cho một nhóm người, chọn theo quy tắc (tuổi, số dư hiện tại, tình trạng đi học).

**"Schooling status" (tình trạng đi học) nghĩa là gì?**

Tender chỉ nhắc tên, không định nghĩa rõ. Đây là tiêu chí để HQ lọc nhóm nhận batch top-up, nhiều khả năng là 1 trong các hướng sau (hoặc kết hợp):

1. **Đang đi học hay không** — còn đang theo học (active) vs đã nghỉ/bỏ học/chưa vào lớp 1.
2. **Loại trường** — học trường công/được chính phủ tài trợ (MOE-funded) hay trường tư/ngoài hệ thống (non-MOE-funded). Đáng chú ý: hệ thống Edusave thật của Singapore **phân biệt rõ 2 loại này** — trẻ học trường MOE-funded nhận tiền từ lúc vào tiểu học tới hết trung học, còn trẻ KHÔNG học trường MOE-funded chỉ nhận theo mốc tuổi cố định 7–16 (xem `giai-thich/04-doi-chieu-thuc-te.md`). Nếu tender đi theo hướng này, top-up định kỳ có thể cũng cần phân biệt y như vậy.
3. **Cấp học** — tiểu học / trung học / dự bị đại học (pre-university). Hệ thống thật trả số tiền khác nhau theo cấp học ($230 tiểu học, $290 trung học).

Chưa rõ tender muốn theo hướng nào trong 3 hướng trên — đã có trong `roles/qalead/assumptions-negotiation-register.md` Table 2 hạng 5 (batch top-up rule operators), giờ bổ sung thêm 3 hướng cụ thể này để hỏi rõ hơn khi negotiate với khách hàng.

**Tiền nạp vào (top-up) lấy từ đâu?**

Tender không nói rõ. Transcript chỉ nhắc: top-up đột xuất (ad hoc) gắn với "có ngân sách đặc biệt được chính phủ duyệt" — nghĩa là nguồn tiền là **ngân sách chính phủ, nằm ngoài hệ thống**, không phải một "tài khoản nguồn" mà hệ thống tự quản lý.

Khác với FAS (#4) — có hẳn requirement #6 theo dõi ngân sách (budget tracking) — top-up (#2) **không có bất kỳ khái niệm ngân sách/nguồn tiền nào** trong tender. Điều này ảnh hưởng tới thiết kế dữ liệu: hệ thống có cần 1 "sổ nguồn tiền" để trừ mỗi lần top-up (có số dư riêng, giới hạn, lịch sử), hay chỉ đơn giản là cộng tiền vào tài khoản học sinh mà không trừ ở đâu cả (coi như tiền tự "xuất hiện" từ ngân sách chính phủ bên ngoài)?

Tham khảo hệ thống Edusave thật: chính phủ "contribute" (đóng góp) tiền vào tài khoản hàng năm, không thấy mô tả có 1 "tài khoản nguồn" nào bị trừ tương ứng trong hệ thống — gợi ý hướng đơn giản (không cần sổ nguồn) có thể là lựa chọn hợp lý. Nhưng đây vẫn chỉ là suy đoán, chưa phải câu trả lời chính thức — đã thêm vào `roles/qalead/assumptions-negotiation-register.md` Table 1, hạng 10.

Có thể nạp định kỳ (ví dụ mỗi năm 1 lần) hoặc đột xuất (khi chính phủ duyệt ngân sách đặc biệt).

**Top-up khác FAS (#4) ở chỗ nào?**

Dễ nhầm vì cả 2 đều "cho tiền", nhưng cơ chế khác hẳn:

| | Top-up (#2) | FAS (#4) |
|---|---|---|
| Ai khởi xướng | HQ chủ động nạp | Phụ huynh chủ động xin |
| Ai được nhận | Bất kỳ account holder thỏa quy tắc, không xét hoàn cảnh | Chỉ học sinh khó khăn tài chính, xét theo thu nhập |
| Tác động | Cộng vào **số dư tài khoản** | Trừ vào **học phí phải đóng** |
| Ngân sách | Không có trong tender | Có requirement #6 riêng |
| AI | Không | Có (risk tier) |

Nói ngắn gọn: top-up là "cho thêm tiền vào ví", FAS là "giảm giá hóa đơn" — không phải cùng 1 cơ chế.

## #3 — Dữ liệu trường học, lớp, học sinh, học phí

Đây là dữ liệu nền tảng: danh sách trường, các khối lớp, các lớp học, học sinh trong từng lớp, và các loại phí phải đóng. Không có dữ liệu này thì không tính được học phí của ai cả — mọi tính năng khác đều dựa vào đây.

## #4 — Trợ cấp tài chính (FAS — Financial Assistance Scheme)

Học sinh khó khăn có thể xin trợ cấp. 2 lớp:
- **MOEFAS**: trợ cấp cấp quốc gia, được cấp tự động nếu đủ điều kiện (dựa vào thu nhập hộ gia đình, thu nhập bình quân đầu người).
- **SBFAS**: nếu không được MOEFAS, trường có thể tự quyết định cấp trợ cấp riêng.

Có AI hỗ trợ: dự đoán mức độ khó khăn tài chính còn lại, chia 3 mức:
- **Low Risk**: nhiều khả năng tự trả nốt được phần còn lại
- **Medium Risk**: có thể gặp khó khăn
- **High Risk**: nhiều khả năng gặp khó khăn đáng kể

Đây là requirement phức tạp nhất trong cả 10 mục, nhiều câu hỏi chưa rõ nhất (xem file giải thích số 03, phần "Blocking vs Business Impact").

## #5 — Nộp đơn FAS bằng giấy (hardcopy)

Phụ huynh không có tài khoản SingPass thì điền đơn giấy, trường thu lại, scan, rồi nhập vào hệ thống. Vẫn đi qua luồng xét duyệt giống như nộp online (#4).

## #6 — Theo dõi ngân sách trợ cấp

MOE HQ theo dõi tổng chi cho MOEFAS. Từng trường theo dõi ngân sách SBFAS riêng của mình. Chưa rõ: hệ thống có tự động chặn khi vượt ngân sách không, hay chỉ báo cáo sau.

## #7 — MOE HQ xem hệ thống dưới góc nhìn người khác

Khi phụ huynh hoặc người trường học gặp khó khăn, nhân viên MOE HQ có thể "giả lập" xem màn hình giống như người đó đang thấy, để hỗ trợ. Chưa rõ: chỉ xem thôi, hay có thể thao tác thay luôn — đây là điểm quan trọng vì ảnh hưởng tới bảo mật/audit log.

## #8 — eService: đăng nhập, xem tài khoản, chatbot AI

Phụ huynh đăng nhập bằng SingPass, xem thông tin tài khoản giáo dục của con (số dư, lịch sử giao dịch), cập nhật thông tin cá nhân cơ bản (địa chỉ, số điện thoại). Có chatbot AI trả lời câu hỏi về cách dùng eService Portal, có thể hỏi lại để làm rõ ý phụ huynh.

## #9 — Xem và thanh toán học phí còn nợ

Phụ huynh xem học phí còn thiếu, chọn cách trả: dùng số dư tài khoản giáo dục, trả online (thẻ), hoặc kết hợp cả hai.

## #10 — Xin FAS theo đơn vị gia đình + AI tự điền form

Phụ huynh nộp 1 đơn FAS cho cả gia đình (không phải từng con riêng lẻ), vì việc xét duyệt dựa trên thu nhập cả hộ gia đình. AI tự điền sẵn form dựa vào hồ sơ có sẵn và các câu trả lời trước đó từ chatbot (#8), phụ huynh chỉ cần kiểm tra lại và nộp.
