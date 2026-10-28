# Ghi chú: chuyển R4 sang chạy trên UI thật

Ngày ghi: 21/10/2026. Trạng thái cập nhật 25/10/2026: đã làm phần F4.13 đến F4.16 trên bản code `codesprint2ending` (màn MOEFAS đã vào code này). Bộ thật nằm ở `tests\real`, bảng case và chỗ lệch xem `docs\REAL_COVERAGE.md`. Các mục 4.1, 4.2, 4.4, 4.5 bên dưới đã xử lý (từ chối chạy ngoài localhost, đăng nhập một lần lưu `artifacts\auth\moehq.json`, scheme tạo ra có tiền tố R4-AUTO và gắn `mutating`, tên file video theo mã TC). Chưa chạy thật trên máy này (không có Docker và trình duyệt), cần QA chạy và gửi dòng tổng kết pytest.

## 1. Vì sao có ghi chú

Lần chạy R4 ngày 20/10/2026 lúc 07:05 trên máy DESKTOP-FKJKREQ chạy trên prototype https://edusave.vercel.app, không phải UI thật. `pytest.ini` đặt `base_url` là địa chỉ prototype và README của r4_automation ghi suite viết cho prototype. Ảnh, trace và báo cáo trong `artifacts` là của prototype, nên không dùng làm bằng chứng cho UI thật.

## 2. Kết quả lần chạy 20/10 trên prototype

| Mục | Số |
|---|---|
| Tổng số mục | 290 |
| Pass | 183 |
| Fail | 25 |
| Xfail (known_defect) | 14 |
| Skip | 68 |

Nguồn: `roles\qa\r4_automation\artifacts\reports\junit.xml`. 25 mục fail chưa được phân tích.

## 3. UI thật có đến đâu (kiểm ngày 21/10/2026)

| Phần R4 | UI thật trong code mới |
|---|---|
| F4.1 đến F4.12, F4.18, F4.19 (danh sách đơn, lọc, xuất file, ngăn xem, duyệt, từ chối) | Chưa có. Ở develop, mục FAS application management trỏ tới trang Coming soon. FASService ở develop chỉ có endpoint `EvaluateFASApplication`. |
| F4.13 đến F4.16 (danh sách scheme MOEFAS, wizard tạo scheme, review và publish, add fee), 74 trên 267 case | Có trên nhánh `origin/feat/moe-fas_nathan_sprint2` (c-nathan.ho, 21/10), chưa vào develop. Chỉ phía MOE HQ, đường dẫn `/moe-hq/moefas-schemes`. Gọi API `/fas/v1/fas/moe-schemes`. SBFAS của trường chưa thấy. |
| F4.17 Close form now (demo) | Chưa thấy nút tương ứng. UI thật có thao tác suspend scheme. Suy luận: đây là nút demo riêng của prototype. |

Admin portal có hai chế độ đăng nhập. `VITE_ENVIRONMENT=API` dùng tài khoản và mật khẩu hoặc Microsoft. `VITE_ENVIRONMENT=MOCK` bỏ qua backend và cho chọn vai trò, nên cũng là giao diện giả, không dùng cho bộ thật.

## 4. Việc cần sửa khi làm

1. Thêm biến `R4_TARGET` (`prototype` hoặc `real`). Đầu mỗi lần chạy, báo cáo ghi địa chỉ đích, tiêu đề trang và commit của frontend. Script từ chối chạy bộ `real` nếu địa chỉ là edusave.vercel.app, và ngược lại.
2. Đăng nhập. Script không chứa mật khẩu. Thêm chế độ `login` mở Chrome có giao diện để anh tự đăng nhập một lần, lưu phiên vào `artifacts\auth` như R9, các test dùng lại phiên đó.
3. Viết lại lớp `pages\` cho phần scheme. Prototype dùng class CSS ngắn, UI thật là React với các bước General, Eligibility, Subsidy, Review. Đọc DOM thật khi chạy nhánh của Nathan. Tên test và mã TC giữ nguyên, chỉ đổi `pages\` và `data\ui_text.py`. Chữ lấy từ `packages\i18n`, chỗ nào lệch FS thì thành `known_defect`.
4. Dữ liệu. Prototype giữ dữ liệu trong bộ nhớ trình duyệt nên mỗi test sạch, UI thật ghi vào cơ sở dữ liệu. Tên scheme thêm hậu tố thời gian, test tạo scheme gắn `mutating` và cần cờ môi trường như R9. Case dựa vào dòng của sheet Seed Data (APP-2026-00398, Lan Nguyen BVP-0012) chuyển sang `not_automated` cho đến khi có seed.
5. Bằng chứng. Hiện chỉ chụp ảnh khi fail. Với bộ thật bật `--screenshot=on` và `--video=retain-on-failure`, đặt tên file theo mã TC.

## 5. Điều kiện để bắt đầu

1. Localhost chạy được, đăng nhập vào admin portal ở chế độ API. Hiện đăng nhập code mới còn lỗi 401, chờ Dev sửa.
2. Nhánh `feat/moe-fas_nathan_sprint2` vào develop, hoặc chạy nhánh đó ở một thư mục riêng.
3. Backend có endpoint `/fas/v1/fas/moe-schemes`. Chưa kiểm endpoint này nằm ở nhánh nào của backend.
4. Có dữ liệu seed cho FAS trong cơ sở dữ liệu.

## 6. Chưa kiểm

1. Chưa mở màn hình thật của nhánh Nathan, mới đọc tên file, đường dẫn và endpoint trong git.
2. Con số 74 case lấy từ tên suite F4.13 đến F4.16 trong `docs\COVERAGE.md`, chưa đối chiếu từng case với màn hình thật.
3. Đã tìm UI danh sách đơn trong develop, main, feat/func9-ui-enhancement và nhánh của Nathan, chỉ thấy manifest của fas-application-management. Chưa tìm ở các nhánh còn lại, và chưa đọc nội dung manifest trên nhánh Nathan.
4. Phần suy luận ghi ở mục 3 chưa có xác nhận từ Dev.
