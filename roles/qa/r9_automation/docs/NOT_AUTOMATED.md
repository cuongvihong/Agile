# Danh sách 2 case R9 chưa tự động hóa

Nguồn case: sổ test case R9 hiện hành (187 case, `data/cases.py`). Nguồn lý do: `data/not_automated.py`. Mỗi dòng ứng với một case, chép bảng sang Excel được ngay.

| STT | ID | Tiêu đề | Test Suite | Severity | Review Status | Assumption Ref | Nhóm lý do | Lý do chi tiết |
|---|---|---|---|---|---|---|---|---|
| 1 | TC-175 | A child aged 16 or older is listed with the invoice but the Pay button is not offered | F9.1 Access and child list | S3 | Draft | ASM-R9-38: the seed shows the invoice of a child aged 16 or  | Thiếu dữ liệu mẫu | UI không hiện ngày sinh hay tuổi của con và chưa có quy tắc 'từ 16 tuổi không có nút Pay' (quy tắc R8, điểm mở O22 trong tài liệu validation rules). Không có dữ liệu để kiểm, làm lại khi FS chốt quy tắc. |
| 2 | TC-204 | The stored error text of a failed callback is cleaned and at most 500 characters | F9.6 Webhook and reconciliation | S3 | Draft | ASM-R9-39: the rule checked here is a QA proposal of the R9  | Khác | Cần cách làm hỏng xử lý một callback hợp lệ để đọc thông báo lỗi được lưu (ENV-R9-05), Dev chưa cung cấp. Ngoài phạm vi kiểm thử qua giao diện và API. |

## Tổng theo nhóm lý do

| Nhóm lý do | Số case |
|---|---|
| Thiếu dữ liệu mẫu | 1 |
| Khác | 1 |
| Tổng | 2 |
