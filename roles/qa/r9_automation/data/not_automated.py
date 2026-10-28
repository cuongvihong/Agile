"""Các case của R9_Test_Cases_final_FS09.xlsx mà chưa test nào tự động hóa, kèm lý do. Tạo bởi tools/build_coverage.py."""
from __future__ import annotations

NOT_AUTOMATED = {
    "TC-175": "UI không hiện ngày sinh hay tuổi của con và chưa có quy tắc 'từ 16 tuổi không có nút Pay' (quy tắc R8, điểm mở O22 trong tài liệu validation rules). Không có dữ liệu để kiểm, làm lại khi FS chốt quy tắc.",
    "TC-204": 'Cần cách làm hỏng xử lý một callback hợp lệ để đọc thông báo lỗi được lưu (ENV-R9-05), Dev chưa cung cấp. Ngoài phạm vi kiểm thử qua giao diện và API.',
}
