# Prompt sửa bộ UAT Master 01 sau lần chạy đầu

Dán toàn bộ file này vào một phiên Claude Code mới, làm việc trong folder `roles/qa/uat_master01_automation`.

## 0. Quy tắc làm việc (đọc trước, bắt buộc)

1. Trước khi sửa bất cứ file nào, viết ra ý định: sẽ sửa gì, ở file nào, vì sao. Chờ người dùng đồng ý rồi mới sửa. Không vừa nói vừa sửa.
2. Chỉ sửa trong `roles/qa/uat_master01_automation`. Không sửa `gavin_uat_automation` (chỉ đọc làm mẫu). Sửa tại chỗ, không tạo bản `_v2` hay `_new`.
3. Không đổi Expected của master, không nới điều kiện check cho pass. Một check sai vì sản phẩm sai thì giữ FAIL. Chỉ sửa khi nguyên nhân là script không thao tác được.
4. Không tạo hay duyệt dữ liệu ngoài phạm vi README (mục "Dữ liệu bộ này tạo ra"). Khi đọc DOM bằng trình duyệt, không bấm Publish, Create, Approve, Submit, Authorize, Confirm.
5. Trả lời người dùng bằng tiếng Việt, không dùng dấu gạch ngang hay gạch dài làm dấu câu, và nêu thêm phương án thay thế bên cạnh phương án chính.
6. Khi xong: cập nhật `README.md` nếu hành vi đổi, thêm một dòng vào `sessionlog/agileproject.md`, cập nhật file `session-process/2026-10-31_1650_uat-master01-automation.md` tại chỗ (thêm mục "Vòng sửa 1").

## 1. Bối cảnh

Lần chạy đầu trên máy người dùng (35 case) dừng giữa chừng với nhiều FAIL. Đã đọc `artifacts/results.json` và ảnh từng bước. Kết luận: phần lớn FAIL là lỗi script, một phần là defect thật của sản phẩm. Mục tiêu vòng này là sửa các lỗi script để kết quả phản ánh đúng sản phẩm, rồi để người dùng chạy lại.

Mẫu tham khảo trong `roles/qa/gavin_uat_automation` (đã chạy ổn trên cùng môi trường). Đọc đúng đoạn nêu dưới đây, không đọc cả file:

| Việc | File mẫu | Đoạn |
|---|---|---|
| Đóng cửa sổ tour | `pages/accounts_page.py` | dòng 44 đến 48 (`Let me explore` hoặc `Close welcome dialog`) |
| Chờ trang tải xong | `pages/accounts_page.py` | dòng 44 đến 60, thuộc tính `data-tour-page` và `data-tour-state` |
| Chờ form FAS sẵn sàng | `pages/fas_form_page.py` | dòng 66 đến 100, chờ `#applicant-fullName` hiện |
| Mở hộp chọn fee component | `pages/real_schemes.py` | dòng 237 đến 270, dialog tên "Select fee components", mở mọi `details` |
| Tick checkbox bị ẩn | `pages/real_schemes.py` | dòng 41 đến 50, thử lại với force |
| Hộp Add fee components của SBFAS | `pages/real_sbfas.py` | dòng 117, 164 đến 177, 202 |

## 2. Việc cần sửa (mỗi mục: triệu chứng, nguyên nhân đã xác nhận, cách sửa, tiêu chí xong)

### F1. Cửa sổ "Welcome to E-Service" chặn mọi cú click

Triệu chứng: TimeoutError ở `View billing for Ethan Rahman`, `FAS Application`, `Open user options` (UAT-PAR-01, PAR-02, PAR-02-E1 và nhiều case khác).
Nguyên nhân: mỗi phiên trình duyệt mới đều hiện cửa sổ chào với ba nút "Start full tour", "Let me explore" và dấu ×.
Cách sửa:
1. `core/recorder.py`, hàm `actor`: sau `ctx.new_page()` gọi `page.add_locator_handler(page.get_by_role("button", name=re.compile(r"^Let me explore$", re.I)), lambda b: b.click())`. Handler này chỉ chạy khi một thao tác bị chặn.
2. `pages/eservice.py`: thêm `dismiss_tour(page)` (theo mẫu accounts_page.py dòng 46 đến 48, có thêm tên nút "Close welcome dialog" làm dự phòng). Gọi trong `wait_ready` (trước và sau khi chờ), trong `open_my_fas`.
3. `pages/auth.py`, `parent_login`: gọi `dismiss_tour` sau khi thấy "Education wallets".
Tiêu chí xong: `run_uat.cmd case UAT-PAR-01 headed` đi qua bước 2 mà không còn timeout do cửa sổ chào.

### F2. Hộp chọn fee component không tick được (MOE-04 bước 3, MOE-06 bước 4, SCH-01, SCH-02)

Triệu chứng: ERROR khi tick, bước Subsidy hiện "0 selected".
Nguyên nhân (đã xác nhận bằng DOM): các thành phần xếp theo loại phí trong thẻ `<details>/<summary>` (Enrichment Fee, Fee RAP Type, Miscellaneous Fee, School Tuition Fee). Nhóm đóng thì checkbox không hiện nên `check()` chờ mãi. Hộp là `dialog` tên "Select fee components" theo bộ cũ.
Cách sửa trong `pages/admin.py`:
1. Thêm `open_picker_groups(scope)` chạy `scope.evaluate("el => el.querySelectorAll('details:not([open])').forEach(d => { d.open = true })")`.
2. `moefas_pick_fee_component`: mở hộp, gọi `open_picker_groups`, chọn tên mong muốn hoặc tên đầu, tick, bấm Apply, rồi kiểm tra trang có chuỗi `[1-9]\d* selected`, nếu không thì `AssertionError`. Ưu tiên một thành phần thuộc nhóm "School Tuition Fee" nếu master nói về học phí.
3. `sbfas_pick_component`: cùng cách, trong `dialog` "Add fee components"; chờ `input:visible` sau khi mở nhóm.
4. Nếu `check()` vẫn lỗi, dùng cách thử lại với force của `real_schemes.py` dòng 46.
Tiêu chí xong: `run_uat.cmd case "UAT-MOE-04,UAT-MOE-06"` qua được bước tick và thấy "1 selected".

### F3. Form FAS đọc quá sớm (PAR-02-E2, PAR-02-E1, các case FAS khác)

Triệu chứng: `beneficiary_names` trả danh sách trống, ảnh form còn dòng "Loading the assistant's saved answers…" kèm cảnh báo "Some details were unavailable. Review the blank fields before submitting."
Nguyên nhân: script không chờ form dựng xong. Lưu ý khác với bộ cũ: trên build này dòng "Loading the assistant's saved answers…" **không bao giờ biến mất** (đã chờ 18 giây, API `/fas/parent/applications/prefill` trả lời sau 124 ms). Đây là defect ứng viên, nên script không được dùng dòng đó làm tín hiệu chờ.
Cách sửa trong `pages/eservice.py`:
1. Thêm `wait_form_loaded(page)`: chờ `#applicant-fullName` hiện (theo `fas_form_page.py` dòng 66 đến 80), rồi chờ có chữ `Beneficiary details:` (bắt lỗi nếu không có), rồi nghỉ 1,5 giây.
2. Gọi trong `open_new_application`.
3. Trong bước kiểm tra của case, ghi nhận (s.check hoặc s.note, theo cách case đang viết) rằng dòng loading còn tồn tại sau khi form đã có dữ liệu.
Tiêu chí xong: `beneficiary_names` trả đủ tên con của persona.

### F4. Nộp đơn FAS bị HTTP 400 (PAR-02 bước 6)

Triệu chứng: POST `/api/v1/fas/parent/applications` trả 400, `System.ValidationFailed`, màn hình về danh sách mà không có đơn mới.
Đã đọc cấu trúc form thật (persona S8901234H, chưa nộp): bắt buộc nhập tay gồm Gender và Race của người nộp, Relationship to beneficiary, Phone number, Email address, ô đồng ý declaration, **Gender của từng con** (Ethan, Leo) và **Gender của thành viên hộ gia đình** (SITI NURHALIZA BINTE OSMA). Các ô khác (họ tên, NRIC, ngày sinh, địa chỉ, trường, lớp) bị khóa.
Cách sửa:
1. `tests/fas_helpers.fill_form`: giữ `fill_empty_required_selects` (chọn lựa chọn thật đầu tiên), sau khi điền gọi `eservice.empty_required(page)` (hàm mới trong `pages/eservice.py`, liệt kê ô bắt buộc còn trống) và trả về trong `done["still_empty"]`. Ghi vào `s.note`.
2. `core/recorder.py`, hàm `on_response`: khi API trả 4xx hay 5xx, nối thêm 300 ký tự đầu của nội dung phản hồi vào chuỗi lỗi (để biết trường nào bị từ chối). Bỏ qua 401 của `/auth/me` và `/support/sessions/current` (chỉ là kiểm tra phiên trước khi đăng nhập).
3. Chạy lại PAR-02. Nếu mọi ô bắt buộc đã đủ mà vẫn 400 thì đó là **defect thật**: giữ FAIL, ghi trường bị từ chối vào Actual. Nếu 400 vì còn thiếu ô thì sửa tiếp.
Tiêu chí xong: biết chắc 400 do script thiếu ô hay do sản phẩm.

### F5. SCH-02 bước 6: không đọc được danh sách fee khi Add fee

Triệu chứng: `a component that is not yet in the scheme is offered` nhận danh sách trống.
Cách sửa trong `tests/test_04_sch.py`: sau khi mở hộp, chờ `select` trong dialog có hơn một option (`wait_for_function`), bỏ các option bắt đầu bằng "Choose", loại thành phần đã có trong scheme (so sánh bằng `startswith` vì tên có thể kèm mã), và đưa văn bản của dialog vào Actual khi vẫn trống. Tham khảo `real_sbfas.py` dòng 202 trở đi cho dialog "Add fee component".
Tiêu chí xong: bước chọn được một thành phần mới hoặc báo rõ vì sao không có.

### F6. Kiểm tra lại check "no SBFAS tick" (PAR-02 bước 4)

Triệu chứng: báo NOT OK với Actual trống.
Cách làm: xem ảnh `artifacts/screenshots/UAT-PAR-02/04-*`, xác định check sai do chuỗi tìm kiếm hay do thật sự còn ô tick. Nếu form không có chữ "also consider SBFAS" thì check phải PASS. Sửa nếu là lỗi script.

## 3. Defect ứng viên (KHÔNG sửa script để che, cần xác minh lại sau khi chạy)

1. SCH-01: tra phụ huynh khi ghi nhận đơn giấy trả HTTP 403, giao diện hiện "Could not look up this parent / Check your connection".
2. SCH-02-N1: tạo scheme trùng tên trả "A scheme with this name already exists for this school." (HTTP 409), master mong thông báo trùng kỳ.
3. PAR-01-N1: hủy đăng nhập hiện "The authentication link is invalid or has expired." thay vì MSG-0802 "Login was not completed. Try again."
4. PAR-01-N2: NRIC S0000999Z quay về trang đăng nhập, không thấy MSG-0801 hoặc MSG-0809 (kiểm tra thông báo thoáng qua trước khi kết luận).
5. PAR-02-N1: form không khóa đứa con đã có đơn.
6. Scheme SBFAS ở trạng thái Draft vẫn có hành động "Add fee" (master: chỉ Active hoặc Upcoming).
7. MOE-06: danh sách thiếu trạng thái "Approved automatically" (GAP, tính là FAIL theo quy tắc 30/10/2026).
8. Form FAS: dòng "Loading the assistant's saved answers…" không biến mất (xem F3), form hiện trường "Registered MOE School" và Grade 1 cho Ethan trong khi Home ghi Rosyth Primary School, Primary 2 2A1 (cần so lại, có thể khác nguồn dữ liệu).
9. Top-Up của phụ huynh hiện ghi chú nội bộ và khóa dịch chưa dịch `common.home`; My FAS hiện thô `PENDING_MOE_REVIEW`; chi tiết đơn ở school hiện ngày sinh 0001-01-01.

## 4. Kiểm tra sau khi sửa

1. `python -m pyflakes .` không báo lỗi; `python -m pytest --collect-only -q` ra đúng 35 test.
2. Chạy thử hai case qua `run_uat.cmd` trên máy người dùng (shell của Claude không vào được host): `case UAT-PAR-01 headed` rồi `case "UAT-MOE-04,UAT-MOE-06"`.
3. Chạy từng nhóm: `group moe`, `group par`, `group sch`, sau đó toàn bộ.
4. Phân loại kết quả bằng cách của skill `qa-automation-failure-triage`: mỗi FAIL ghi rõ là "lỗi script" hay "defect sản phẩm", kèm ảnh bước và đoạn video.
5. Báo cáo cho người dùng: bảng case, kết quả, phân loại, danh sách defect đã xác minh.

## 5. Phương án thay thế (nêu cho người dùng khi báo cáo)

1. Nếu cửa sổ chào còn lọt qua `add_locator_handler`, đặt cờ hoàn thành tour vào `localStorage` hoặc `sessionStorage` trước khi vào trang bằng `context.add_init_script`. Cần đọc đúng tên khóa trong ứng dụng.
2. Nếu hộp chọn fee còn khó, tạo scheme ở bước chuẩn bị bằng API của Admin (nếu có token), rồi để UI chỉ kiểm tra hiển thị.
3. Nếu muốn nhanh, chạy bằng chế độ `headed` từng case để xem trực tiếp rồi mới chạy cả bộ.
