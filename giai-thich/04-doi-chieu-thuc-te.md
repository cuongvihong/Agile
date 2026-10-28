# Đối chiếu với hệ thống thật của Singapore (SFS, Edusave, FAS)

Anh gửi 2 link tham khảo:
- SingPass developer docs — điều kiện để 1 tổ chức được tích hợp SingPass thật
- `studentfinance.moe.gov.sg/sfs` — hệ thống Student Finance System (SFS) thật của MOE Singapore

Đây là hệ thống thật mà tender của mình rõ ràng lấy cảm hứng theo. Đối chiếu dưới đây giúp hiểu sâu hơn, **không thay thế tender** — tender vẫn là nguồn quyết định, cái này chỉ là tham khảo để biết "ngoài đời người ta làm sao".

## SFS thật gồm những gì

SFS thật của MOE có 3 phần: **Edusave**, **PSEA (Post-Secondary Education Account)**, và **Financial Assistance**. Tender của mình rút gọn lại thành "Education Account" (gộp ý tưởng gần giống Edusave) và "FAS" (giống Financial Assistance), **không có PSEA** — đây là điểm đơn giản hóa so với thực tế, không phải thiếu sót.

## Edusave thật — đối chiếu với "Education Account" (#1)

| | Tender của mình | Edusave thật |
|---|---|---|
| Mở tài khoản | Tự động, công dân Singapore, lúc 7 tuổi | Tự động, công dân Singapore. Nếu học trường ngoài hệ thống MOE-funded: nhận tiền từ 7–16 tuổi |
| Đóng tài khoản | Tự động lúc **16 tuổi** | Đóng vào năm tròn **17 tuổi**, hoặc khi không còn học trường MOE-funded — **cái nào đến sau thì tính cái đó** |
| Số dư khi đóng | **Chưa rõ trong tender** (đây là câu hỏi lớn nhất của tôi — xem Business Impact Register) | Tự động **chuyển sang PSEA**, không bị mất |
| Lãi suất | Không nhắc tới | Có, theo lãi CPF Ordinary Account (hiện 2.5%/năm), cộng vào tháng 12 |

**Nhận xét quan trọng**: tender ghi 16 tuổi, thực tế Edusave là 17 tuổi — có thể tender cố tình đơn giản hóa con số, không nhất thiết sai. Nhưng câu hỏi "số dư đi đâu" thì thực tế có câu trả lời rõ ràng (chuyển sang 1 tài khoản kế tiếp), gợi ý một phương án hợp lý để đề xuất với PO/khách hàng: thay vì để trống hoặc mất tiền, có thể đề xuất "chuyển sang 1 trạng thái/tài khoản kế tiếp" dù tender hiện tại không có khái niệm PSEA.

## Financial Assistance thật — đối chiếu với FAS (#4)

Hệ thống thật xét theo **thu nhập hộ gia đình** và **số người trong hộ** (giống nguyên tắc per-capita income của tender), áp dụng cho học sinh công dân Singapore học ở trường chính phủ/được tài trợ — khớp với mô tả MOEFAS trong tender. Thực tế phân biệt nhiều loại trợ cấp khác nhau theo cấp học (FAS cho tiểu học/trung học, ISB cho independent school, SPED FAS cho giáo dục đặc biệt, HECB/HEB cho sau trung học) — tender của mình gộp chung lại thành 1 khái niệm FAS duy nhất, đơn giản hóa hợp lý cho bài tập.

## FAS thật — có quy định cụ thể không

Có. Dùng công cụ check online ngay trên trang MOE (`moe.gov.sg/financial-matters/financial-assistance`), tự nhập thử nhiều mức thu nhập để kiểm chứng (không chỉ đọc mô tả), kết quả xác nhận:

> **Đủ điều kiện MOE FAS nếu: thu nhập hộ gia đình ≤ $4,000/tháng, HOẶC thu nhập bình quân đầu người ≤ $1,000/tháng.**

Đã test 3 trường hợp để kiểm chứng logic thật:

| Thu nhập hộ | Số người | Bình quân đầu người | Kết quả |
|---|---|---|---|
| $1,500 | 4 | $375 | Đủ điều kiện |
| $4,000 | 4 | $1,000 | Đủ điều kiện (đúng biên, "$4,000 hoặc thấp hơn") |
| $10,000 | 4 | $2,500 | **Không** đủ điều kiện |
| $5,000 (vượt mốc hộ gia đình) | 10 | $500 (dưới mốc bình quân) | Vẫn đủ điều kiện — xác nhận đây là điều kiện **HOẶC**, không phải **VÀ** |

Nếu không đạt MOEFAS, trang web dẫn sang "trường có thể xét trợ cấp riêng, đánh giá từng trường hợp" — khớp đúng luồng SBFAS mô tả trong tender (#4).

**Lưu ý quan trọng**: đây là con số thật của Singapore ngoài đời, **không phải con số chính thức của tender** (tender của mình không công bố ngưỡng cụ thể). Nhưng rất hữu ích làm:
- Dữ liệu test mẫu thực tế cho EP/BVA (ngưỡng $4,000 và $1,000, kiểm cả biên trên/dưới)
- Gợi ý cho PO/khách hàng nếu họ cần 1 bộ số cụ thể để demo mà chưa tự nghĩ ra số nào

## Người nhập quốc tịch Singapore (naturalized) có được tính như công dân gốc không

Tìm trong FAQ chính thức của MOE (mục Financial Assistance Scheme) — **không có câu hỏi riêng nào** phân biệt "công dân từ khi sinh ra" với "công dân nhập tịch (naturalized)". Đây là dấu hiệu cho thấy chính sách chỉ quan tâm **trạng thái quốc tịch hiện tại** (đang là Singapore Citizen hay không), không quan tâm có được từ lúc sinh hay nhập tịch sau này. Về luật quốc tịch Singapore nói chung, người nhập tịch có đầy đủ quyền như công dân gốc, không bị phân biệt cho các chế độ như Edusave/FAS.

**Nhưng câu hỏi này lòi ra 1 edge case mới cho chính tender của mình**, chưa từng được hỏi trước đây: Education Account (#1) "tự động tạo khi tròn 7 tuổi" — vậy nếu 1 đứa trẻ **chưa phải công dân Singapore lúc 7 tuổi**, nhưng **trở thành công dân sau đó** (ví dụ nhập tịch lúc 10 tuổi, cha mẹ nhập tịch kéo theo con)? Tài khoản có được tạo ngay khi vừa có quốc tịch (dù đã qua tuổi 7), hay phải chờ một mốc nào khác? Tender hiện tại không nói tới trường hợp này — chỉ giả định ngầm là đứa trẻ đã là công dân từ trước tuổi 7.

Tôi đã thêm câu hỏi này vào `roles/qalead/assumptions-negotiation-register.md` Table 1 (Blocking Register) vì nó ảnh hưởng tới cách thiết kế: hệ thống cần theo dõi sự kiện "trở thành công dân" (event-driven), không chỉ check tuổi theo lịch (date-driven) — 2 cách thiết kế khác nhau, không thể patch sau.

## SingPass thật — điều kiện tích hợp (liên quan #8)

Tài liệu dev của SingPass nêu 3 điều kiện để 1 tổ chức được tích hợp thật:

1. Tổ chức phải đăng ký tại Singapore, có giấy phép ngành nếu thuộc lĩnh vực quản lý riêng.
2. Chỉ được xin đúng dữ liệu cần thiết, phải giải thích lý do xin từng loại dữ liệu, người dùng phải thấy rõ dữ liệu nào bị lấy.
3. **Không được bắt buộc dùng SingPass là cách duy nhất** — phải có ít nhất 1 cách thay thế (nhập tay, upload giấy tờ...).

Điểm 3 thú vị: tender của mình **đã có sẵn** cách thay thế — chính là nộp đơn FAS giấy (#5) cho người không có SingPass. Vậy về mặt nguyên tắc, thiết kế hiện tại của tender đã đi đúng hướng so với yêu cầu thật của SingPass, dù đây chỉ là mô phỏng.

## Dùng thông tin này để làm gì

Tôi (QA Lead) đã thêm ghi chú tham khảo này vào `roles/qalead/assumptions-negotiation-register.md` (mục số dư tài khoản khi đóng) — không tự ý coi đây là câu trả lời chính thức, vẫn cần PO/khách hàng xác nhận, nhưng giờ có 1 phương án thực tế để đề xuất thay vì đoán mù.
