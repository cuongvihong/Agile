# Tổng quan: Tender nói gì

File này giải thích cho người đọc hiểu, không phải tài liệu kỹ thuật cho team. Tài liệu kỹ thuật nằm trong `roles/`.

## Khách hàng là ai, muốn gì

Khách hàng: **Bộ Giáo dục Singapore (MOE)**. Họ cần một hệ thống tài chính giáo dục, gọi tắt trong project này là **EAFAMS** (tên xuất hiện trong file backlog của PO).

Hệ thống có 2 phần chính:

1. **Admin Portal** — dành cho người của MOE HQ và người của từng trường học dùng.
2. **eService Portal** — dành cho phụ huynh dùng.

## Nguồn thông tin, cái nào tin được hơn

| Nguồn | Là gì | Mức tin cậy |
|---|---|---|
| `groundtruth/592ba6ad-image.png` | Bảng 10 requirement, đây là **tender gốc** | Tin tuyệt đối — đây là nguồn chính |
| `groundtruth/MOE_Finance_System_Agile_Kick-off_Transcript.md` | Bản ghi âm buổi kick-off, người trình bày đọc lại nội dung tender | Chỉ dùng để hiểu thêm ngữ cảnh. Bị lỗi ghi âm ở vài chỗ (ví dụ ghi "SIMPASS" nhưng thực ra là **SingPass** — hệ thống định danh số quốc gia Singapore) |

Khi 2 nguồn khác nhau, luôn tin tender hơn transcript.

## Ý tưởng cốt lõi của hệ thống

Mỗi trẻ em công dân Singapore có một **tài khoản giáo dục** (Education Account), tự động mở năm 7 tuổi, tự động deactivate 1 ngày trước khi đủ 16 tuổi hoặc ngay khi mất quốc tịch Singapore (cái nào đến trước). Tài khoản này dùng để trả học phí ở trường công.

MOE HQ nạp tiền vào các tài khoản này (gọi là **top-up**), có thể nạp hàng loạt theo quy tắc, hoặc nạp riêng cho từng người.

Học sinh khó khăn tài chính có thể xin **trợ cấp (FAS — Financial Assistance Scheme)**. Có 2 lớp: trợ cấp cấp quốc gia (MOEFAS) và trợ cấp riêng của từng trường (SBFAS). Hệ thống có AI hỗ trợ: dự đoán mức độ khó khăn tài chính (Low/Medium/High Risk) để gợi ý mức trợ cấp phù hợp.

Phụ huynh vào eService Portal (đăng nhập bằng SingPass) để xem tài khoản, xem học phí còn nợ, thanh toán, và xin trợ cấp FAS. Có chatbot AI hỗ trợ trả lời câu hỏi và tự điền giúp form xin trợ cấp.

## Quan trọng: đây là bài tập mô phỏng (training prototype)

Theo file backlog của PO (`roles/po/EAFAMS_Initial_Product_Backlog_v0.1.xlsx`), đây là **project huấn luyện**, không phải dự án giao hàng thật cho MOE. Các tích hợp như SingPass, API thu nhập bên thứ 3, cổng thanh toán online đều là **giả lập (simulated/mock)**, không phải tích hợp thật với hệ thống chính phủ.

Điều này quan trọng vì: những thứ tưởng như "phải chờ khách hàng cấp quyền truy cập" (SingPass sandbox, API thật...) thực ra chỉ là quyết định nội bộ của team (tự thống nhất cách giả lập), không phải thứ phải đi xin khách hàng thật.

## 2 track làm song song

Team chia làm 2 nhóm, làm song song (không làm lần lượt):

- **Track A — Admin Portal**: 5 dev, 3 QA, làm phần MOE HQ/trường học (7 trong 10 requirement)
- **Track B — eService Portal**: 4 dev, 2 QA, làm phần phụ huynh (3 trong 10 requirement)

Timeline: 3 tuần, chia 3 sprint, mỗi sprint 1 tuần, bắt đầu 2026-10-11.
