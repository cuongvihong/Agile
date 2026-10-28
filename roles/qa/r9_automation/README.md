# Automation R9: FS09 Thanh toán phí còn nợ (Fees & Payments)

Bộ test Python, Pytest, Playwright (Page Object) cho giao diện e-service thật của chức năng 9. Nguồn case là `roles/qa/R9_Test_Cases_final_FS09.xlsx` (187 case: 153 case gốc theo FS 09 bản final "Tổng hợp FS" ngày 22/10/2026, cộng TC-173 đến TC-206 bổ sung ngày 25/10/2026 cho các quy tắc kiểm tra dữ liệu; 19 case đã bỏ kèm lý do ở `roles/qa/R9_Test_Cases_final_FS09_removed.md`). Bản `R9_Test_Cases_rev_FS09.xlsx` (172 case) và `R9_Test_Cases_notes.xlsx` (162 case) đã được thay thế.
Cấu trúc và cách chạy giống `roles/qa/r4_automation`, nhưng R4 chạy trên prototype tự chứa dữ liệu, còn R9 chạy trên hệ thống thật nên dữ liệu nằm ở backend.

## Chỉ chạy trên localhost

Bộ test chỉ chạy trên hệ thống anh đang host ở máy mình, không chạy trên Vercel hay máy chủ nào khác. `data/seed.py` (hàm `assert_local`) và `conftest.py` (`pytest_configure`) kiểm mọi địa chỉ trước khi mở trình duyệt:
`R9_BASE_URL`, `R9_ADMIN_URL`, `R9_CHECKOUT_URL` và `--base-url` phải là `localhost`, `127.0.0.1`, `[::1]` hoặc tên có đuôi `.localhost`.
Địa chỉ `*.vercel.app` làm pytest dừng ngay với thông báo rõ và không có biến nào mở được; địa chỉ khác localhost chỉ mở được khi đặt `R9_ALLOW_REMOTE=1` (máy khác trong mạng riêng, ví dụ IP Radmin).
Runner `run_r9_automation.cmd` kiểm lại ba biến đó trước khi cài thư viện. SQL Server và webhook cũng ở máy anh (`docker exec edufams-qa-sqlserver`, `http://localhost:5008`).
Cần khởi động trước khi chạy: e-service 5174, gateway 5273, MockPass 5156; thêm admin portal 5173 cho smoke, simulator 5176 (`npm run dev:payment-checkout`) cho test `online`, Docker với `edufams-qa-sqlserver` cho test dùng SQL.

## Hai địa chỉ của hệ thống

| Cổng | Địa chỉ mặc định | Biến môi trường | Vai trò trong bộ test |
|---|---|---|---|
| e-service (phụ huynh) | `http://localhost:5174` | `R9_BASE_URL` | nơi chạy mọi test thanh toán của FS 09 |
| admin portal (quản trị) | `http://localhost:5173` | `R9_ADMIN_URL` | hai test smoke: trang `/login` mở được, mở gốc khi chưa đăng nhập thì về `/login` |

Admin portal chưa được dùng cho gì hơn. Lý do: FS 09 là chức năng của phụ huynh nên không case nào trong 187 case cần thao tác quản trị; form đăng nhập admin đòi username và password của tài khoản QA mà repo không có (bộ test không tự đặt mật khẩu); các màn quản lý phí và nạp tiền của admin portal ở bản này mới là trang giữ chỗ nên chưa thể phát hành hóa đơn từ đó.
Khi có tài khoản và màn phát hành hóa đơn, đó là chỗ để tạo hóa đơn Issued đúng tiền điều kiện của FS 3.1.1 thay cho dữ liệu khoản phí có sẵn.

## Tình trạng hiện tại (đọc trước)

1. Ngày 21/10/2026 đã mở e-service (5174) và admin portal (5173) trong trình duyệt của app Claude, đăng nhập MockPass bằng persona `S7890123F`, đi qua các bước chọn khoản, chọn phương thức (Education Account, Online Gateway, Both với phần chia 300.00 và 170.00) và xem lại, rồi dừng trước nút Authorize & pay. Tiêu đề, bảng khoản phí, ô chọn `Select charge: ...`, ba lựa chọn phương thức, ô `Payment split` và các dòng của bước xem lại khớp với locator và `data/ui_text.py`. Chưa có giao dịch nào được tạo trong lần xem đó.
2. **Chưa chạy pytest trên hệ thống thật.** Máy ảo của Claude không truy cập được localhost của máy anh nên chưa có kết quả đạt hay không đạt. Bản sửa theo rev FS09 mới được kiểm cú pháp bằng pyflakes và thu thập test bằng `pytest --collect-only` (96 test chạy được, 80 test bỏ qua kèm lý do sau khi rút gọn theo FS final). Chạy `smoke` rồi `read` trên máy thật và gửi lại `artifacts/reports/junit.xml`.

   **Lần chạy thật đầu tiên (`read`, 21/10/2026 23:51):** 182 test, 12 đạt, 21 thất bại, 35 lỗi, 96 bỏ qua (case chưa tự động), 18 `known_defect`, 0 xpass. Phần lớn thất bại và lỗi là một nguyên nhân: e-service giữ phụ huynh đăng nhập ở cookie `IAM_Session` và ở `sessionStorage` khóa `edusave.parent-auth.user`; `storage_state` của Playwright chỉ lưu cookie, nên mọi test dùng lại phiên bị đưa về `/parent/login` (35 lỗi ở bước chuẩn bị, 9 thất bại smoke, 8 thất bại ở màn kết quả). Đã sửa trong `conftest.py` (`seed_parent_session`). Vì lỗi đăng nhập nên 18 kết quả `known_defect` của lần chạy này chưa đáng tin (test thất bại vì trang đăng nhập cũng được tính là thất bại đúng kỳ vọng); chạy lại rồi xem `xpass` và lý do. Hai thất bại thật không do đăng nhập: TC-012 (API trả 200 danh sách rỗng thay vì 403 cho mã học sinh không liên kết) và TC-081 với khóa 101 ký tự (máy chủ không kiểm độ dài, yêu cầu đi tới bước tìm khoản phí rồi trả 404); cả hai đã chuyển sang `known_defect`, riêng khóa 101 ký tự bị gỡ khỏi test `mutating` vì máy chủ có thể nhận khóa đó và thanh toán khoản phí thật.

   **Lần chạy thứ hai (`read`, 22/10/2026 07:23, sau khi sửa phiên đăng nhập):** 182 test, 64 đạt, 1 thất bại, 0 lỗi, 97 bỏ qua (96 chưa tự động, TC-040 thiếu dữ liệu ví 0.00 còn khoản phí), 20 `known_defect` đều thất bại đúng lý do ghi trong báo cáo, 0 xpass. Thất bại duy nhất là TC-023: hai con có chung hai tên khoản (School Fee - Term 1, Standard Miscellaneous Fee) nên điều kiện hai danh sách rời nhau sai; đã đổi sang so từng danh sách trên màn với API của đúng con đó.
3. Lần chạy thử trước đây trên một bản giả lập nhỏ (86 test, trước bản sửa này): 63 đạt, 15 `known_defect` thất bại đúng kỳ vọng, 4 bỏ qua vì dữ liệu, 4 cần đăng nhập thật. Lần đó chỉ chứng minh mã Python và luồng thao tác đúng với DOM suy ra từ mã nguồn. Bản sửa này chưa chạy lại trên bản giả lập.
4. Các test `known_defect` có hai nguồn: lỗi đã ghi trong `roles/qa/F9_Dev_Local_Run_Results.md`, hoặc suy ra từ mã nguồn (ghi rõ "Suy ra từ mã nguồn" trong lý do). Loại thứ hai chưa thấy trên bản build, cần xác nhận khi chạy. Riêng trạng thái rỗng không có liên kết về danh sách con đã quan sát thật trên Tan Wei Ming ngày 21/10/2026.

## Bổ sung ngày 25/10/2026: 34 case quy tắc kiểm tra dữ liệu (TC-173 đến TC-206)

File mới `tests/test_f99_validation_rules.py`, nhãn `rules` (chạy riêng bằng `run_r9_automation.cmd rules`), mỗi test mang thêm nhãn nhóm f91 đến f98 nên `suite N` cũng chạy.
33 test cho 32 case, 2 case chưa tự động (TC-175 và TC-204, lý do ở `docs/NOT_AUTOMATED.md`). Sổ case viết theo bộ seed R9 (S01, S10, S25...), còn UI thật liệt kê khoản phí của các con mà persona có,
nên test **không gắn cứng mã seed**: chọn con qua Catalog, kiểm quy tắc đứng sau con số (Net = Gross trừ Subsidy, định dạng, thứ tự, trạng thái mặc định...) và tự bỏ qua khi dữ liệu không có đối tượng đó.
Con số của sổ (27.25, 1,590.00...) chỉ đối chiếu được khi nạp đúng bộ seed R9. Test dựng khoản phí bằng `db.temp_charges` (tự dọn dẹp) và cần Docker; không có thì bỏ qua.

| Nhóm | Case | Cách kiểm |
|---|---|---|
| Chỉ đọc, giao diện | 173, 174, 176, 177, 183, 184, 185, 186, 191, 192, 200 | đọc UI, giữ request bằng `page.route` để thấy trạng thái đang tải |
| `mocked` | 186 (ví 0), 196 đến 199, 200 giờ hoàn tất | giả phản hồi giao dịch như F9.7 |
| `api` | 180, 181, 194, 195, 201 | gửi yêu cầu sai, đọc mã trạng thái và thân phản hồi |
| Webhook | 202, 203 | `db.post_webhook` có chữ ký, đọc biên nhận trong SQL |
| SQL có ROLLBACK | 205, 206 | `db.sql_check_steps`, không để lại dữ liệu |
| `known_defect` dự kiến | 178, 181, 184 (rỗng), 187 đến 190, 191 (phần 1), 193, 196 (mã PAY), 197, 198, 199 (tên file), 202 (callback B) | UI hoặc API chưa có (ô nhập phần EA, nhãn nợ, nút Cancel, nút Refresh...); XPASS nghĩa là đã sửa |
| Chưa tự động hóa | 175, 204 | không có tuổi trên UI; cần cách làm hỏng xử lý callback |

Chưa chạy các test này trên hệ thống thật (xem mục dưới). Dự kiến một số thất bại là lệch thật cần ghi nhận, và vài test `draft` (dấu hiệu đang tải, định dạng ngày, khóa idempotency) phụ thuộc cách UI hiện thực; xem lý do trong từng docstring.

## Dữ liệu hiện có trên bản chạy local (quét ngày 21/10/2026, persona S7890123F)

| Con | Khoản phí | Tổng nợ | Ví EA | Dùng cho |
|---|---|---|---|---|
| Test Child One | 10 | 805.00 | 300.00 | trả bằng EA (`ea_child`), ví đủ trả các khoản nhỏ |
| Test Child Two | 5 (có Overseas Learning Trip Fee 800.00) | 1390.00 | 300.00 | ví thiếu, đề nghị Both |
| Test Child Three | 5 | 470.00 | 300.00 | ví thiếu, đề nghị Both (`split_child` ưu tiên con này để test rút cạn ví không làm mất dữ liệu của Test Child One) |
| Tan Wei Ming | 0 | 0.00 | 0.00 | trạng thái rỗng thật, số dư 0.00 |

Không con nào vừa ví 0.00 vừa còn khoản phí, nên TC-040 bản dữ liệu thật tự bỏ qua; bản ví giả lập vẫn chạy. Dữ liệu có thể khác sau lần nạp lại: bộ test đọc danh sách con trên giao diện chứ không gắn cứng tên (`pages/catalog.py`).

## Bộ test gồm gì

| Mục | Số lượng |
|---|---|
| Case trong sổ R9 final FS09 | 187 |
| Case có test tự động | 185 |
| Case chưa tự động, hiện dưới dạng test bị bỏ qua kèm lý do | 2 |
| Test thu thập được (kể cả 2 test bỏ qua) | 239 |
| Test chỉ đọc, không đổi dữ liệu (nhãn readonly, gồm cả test chạy SQL tự dọn) | 107 |
| Test `known_defect` | 75 |
| Test `draft` | 35 |
| Test `mocked` (giả một phản hồi bằng `page.route`) | 38 |
| Test `api` không ghi dữ liệu (yêu cầu mong đợi bị từ chối) | 9 |
| Test `api` và `mutating` (gửi yêu cầu thật trên khoản phí thật) | 4 |
| Test `mutating` qua giao diện, không cần simulator | 4 |
| Test `mutating` cần simulator cổng 5176 (trong đó 2 test `destructive`) | 5 |
| Test `online` chỉ kiểm simulator truy cập được | 1 |
| Test `admin` (chỉ mở trang đăng nhập admin portal) | 2 |

Bảng ánh xạ TC sang test và lý do từng case chưa tự động nằm ở `docs/COVERAGE.md`, kèm mục "Case tự động hóa mà bản rev FS09 đã đổi".
Hai case chưa tự động hóa là TC-175 và TC-204 (lý do ở `docs/NOT_AUTOMATED.md`). Các số liệu 73/80 case ở các bản trước không còn đúng: sau khi thêm test F9.6 và F9.8 mọi case gốc đều có test.

## Đối chiếu với bản rev FS09

Lưu ý: phần này mô tả đợt sửa theo bản rev (172 case). Sau đó FS final loại 19 case, trong đó 3 case từng có test (TC-037, TC-044, TC-064) nên test đã bị xóa.

Bản rev đổi Preconditions, Test Data hoặc Expected Result của 84 trong 162 case cũ (33 case trong số đó đã có test; TC-051 chỉ đổi Note) và thêm TC-163 đến TC-172. Việc đã làm ở test:

1. Hậu điều kiện "không có transaction nào được tạo, invoice vẫn Issued, số dư EA không đổi" cho mọi case dừng ở bước phương thức và bước xem lại: hàm `assert_nothing_created` trong `pages/postconditions.py`. "Invoice vẫn Issued" được hiểu là khoản phí vẫn nằm trong danh sách còn nợ (ASM-R9-UI-01, suy luận của QA).
2. Hậu điều kiện "transaction và leg Succeeded, invoice Paid" cho các test thanh toán thật: hàm `assert_backend_state` đọc `GET /billing/v1/transactions/{id}` và `GET /billing/v1/invoices/{id}`.
3. Màn kết quả giả lập (F9.7) kiểm thêm dòng trạng thái từng leg và `Invoice status`. TC-128 và TC-137 viết lại theo rev: trạng thái đối soát không nói thất bại; transaction Failed có leg EA Reversed. Hai chỗ UI không đáp ứng được ghi là `known_defect` (suy ra từ mã nguồn `PaymentResultPage.tsx`).
4. Trong 10 case mới chỉ TC-164 (lỗi tải danh sách khoản, `mocked`, `draft`, `known_defect`) có test. Chín case còn lại cần SQL, phụ huynh thứ hai hoặc dữ liệu mà UI không có; lý do nằm trong `docs/COVERAGE.md`.
5. Số dư EA, nhật ký audit và ledger trong Expected không đọc được từ e-service nên chưa kiểm, ngoài phần số dư hiện trên trang của con.
6. 13 case có Actual Result cũ cần chạy lại sau khi sửa Expected (TC-063, 070, 087, 089, 098, 100, 107, 128, 129, 130, 136, 137, 141). Bộ test này chưa chạy lần nào trên hệ thống thật nên chưa đổi được Actual Result nào.

## Điều kiện để chạy

1. Chạy cả stack EduFAMS như hướng dẫn (`run_edufams_update.cmd` hoặc compose QA): e-service ở `http://localhost:5174`, admin portal ở `http://localhost:5173`, gateway ở 5273, MockPass ở 5156.
2. Dữ liệu mẫu đã nạp cho persona MockPass `S7890123F` (xem bảng dữ liệu ở trên). Bản nạp cũ theo `Function9FullFlowSetup.sql` (Noah Lee và Ryan Hassan, ví 1000.00) cũng chạy được vì bộ test không gắn cứng tên con.
3. Test `online` cần simulator cổng thanh toán: trong `edugovernment-frontend` chạy `npm run dev:payment-checkout` (cổng 5176). `run_edufams_all.cmd` hiện không chạy cái này. Mở e-service bằng `localhost`, không dùng IP Radmin, vì simulator chỉ cho phép quay về `localhost:5174` và `localhost:5176`.
4. Python 3.9 trở lên và Google Chrome.

## Chạy trên Windows bằng Chrome của máy

Bấm đúp `run_r9_automation.cmd` hoặc chạy trong cmd. Lần đầu runner tạo `.venv` và cài thư viện.

| Lệnh | Chạy gì | Ghi dữ liệu thật? |
|---|---|---|
| `run_r9_automation.cmd` | 9 test smoke (e-service, admin portal, simulator), chạy đầu tiên | Không |
| `run_r9_automation.cmd read` | mọi test chỉ đọc, giả lập và API bị từ chối | Không |
| `run_r9_automation.cmd pay` | thêm 11 test thanh toán thật (3 test trong đó cần simulator) và 1 test kiểm simulator | **Có.** Phải gõ `PAY` để xác nhận |
| `run_r9_automation.cmd destructive` | 2 test chia khoản Both, rút cạn ví một con | **Có.** Phải gõ `DRAIN` để xác nhận |
| `run_r9_automation.cmd rules` | 34 case quy tắc kiểm tra dữ liệu mới (TC-173 đến TC-206) | không (khoản phí tạm tự dọn) |
| `run_r9_automation.cmd suite 3` | một nhóm, ở đây F9.3 (1 đến 5 và 7) | tùy nhóm |
| `run_r9_automation.cmd tc 046` | một case, ở đây TC-046 | tùy case |
| `run_r9_automation.cmd draft` | case phụ thuộc giả định | không |
| `run_r9_automation.cmd defects` | case kỳ vọng thất bại vì lệch với R9 | không |
| thêm `headed` ở cuối | xem trình duyệt, ví dụ `run_r9_automation.cmd suite 3 headed` | |

Chế độ `full` chạy hết mọi test, kể cả thanh toán thật và rút cạn ví, không hỏi xác nhận (đặt R9_ALLOW_PAYMENTS=1 và R9_ALLOW_DESTRUCTIVE=1 trong lệnh). Chạy xong cần nạp lại dữ liệu mới chạy lại được. Test online vẫn tự bỏ qua nếu simulator cổng 5176 chưa chạy.

Thứ tự đề nghị: `smoke`, rồi `read`, gửi lại `junit.xml`. Chỉ chạy `pay` sau khi `read` ổn và đã đồng ý dùng dữ liệu thật.

### Dữ liệu bị tiêu khi chạy `pay` và `destructive`

Thanh toán thật tiêu khoản phí và trừ tiền ví, không hoàn lại được. Một lần `pay` dùng khoảng 9 khoản nhỏ nhất của con có ví lớn nhất (Test Child One trên dữ liệu 21/10/2026):
TC-065 một khoản, TC-067 hai, TC-077 một, TC-078 và TC-080 một, TC-084 một, TC-087 một, TC-136 một, TC-090 một; TC-081 trên khoản thật chỉ tiêu khoản nếu máy chủ nhận nhầm khóa sai. Ước tính các test trả bằng EA trừ khoảng 260.00 trong ví 300.00 (theo thứ tự khoản nhỏ nhất),
nên test cuối có thể tự bỏ qua vì hết tiền. Test tự đọc lại khoản và số dư đang có ngay trước khi thanh toán, hết khoản hoặc hết tiền thì tự bỏ qua kèm lý do, không báo lỗi sai.
`destructive` rút cạn ví của con đứng cuối trong nhóm ví thiếu (Test Child Three trên dữ liệu 21/10/2026), nên chỉ chạy được một test mỗi lần nạp dữ liệu: chạy xong một test thì phải reset rồi mới chạy test thứ hai.

Để đưa dữ liệu về lúc đầu: chạy `tools/reset_payment_data.sql` (xóa bản ghi thanh toán của các con, các khoản phí hiện lại). File này viết cho bản nạp cũ (Noah Lee, Ryan Hassan) nên cần sửa tên con trước khi dùng với dữ liệu hiện tại. Số dư ví không được hoàn;
khối "BƯỚC 2" trong file đó, đang tắt, đặt ví về 1000.00 bằng cách sửa thẳng cột balance. Chỉ bật khi đồng ý với chủ dữ liệu. File này chưa được chạy lần nào.

## Biến môi trường

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `R9_BASE_URL` | `http://localhost:5174` | địa chỉ e-service |
| `R9_ADMIN_URL` | `http://localhost:5173` | địa chỉ admin portal |
| `R9_NRIC` | `S7890123F` | persona MockPass dùng để đăng nhập (không phải mật khẩu) |
| `R9_CHECKOUT_URL` | `http://localhost:5176` | simulator cổng thanh toán |
| `R9_EXPECTED_CHILDREN` | để trống (TC-006 tự lấy danh sách con của persona từ DB) | chỉ đặt khi muốn ép một danh sách tên cụ thể, cách nhau bằng dấu phẩy |
| `R9_MIN_VIDEO_SECONDS` | `5` | thời lượng tối thiểu của video mỗi test; 0 tắt phần chờ thêm |
| `R9_ALLOW_REMOTE` | | đặt `1` để cho phép địa chỉ không phải localhost (máy khác trong mạng riêng). Địa chỉ vercel.app luôn bị chặn |
| `R9_ALLOW_PAYMENTS` | | runner tự đặt `1` sau khi anh gõ `PAY` |
| `R9_ALLOW_DESTRUCTIVE` | | runner tự đặt `1` sau khi anh gõ `DRAIN` |

Nếu MockPass ở máy anh dùng địa chỉ khác localhost (ví dụ IP Radmin), `Portal.sign_in()` vẫn chạy được vì nó theo đường chuyển hướng của app,
nhưng phần thanh toán online sẽ bị simulator từ chối. Dùng `localhost` cho cả bộ test.

## Kết quả

| File | Nội dung |
|---|---|
| `artifacts/allure-report/index.html` | **báo cáo Allure một file** (như r4_automation): từng case có tiêu đề, suite, màn hình, severity, tiền điều kiện, dữ liệu, bước, kết quả mong đợi, nhãn loại test và **video** thao tác. Dựng bằng `allure generate`; runner tự dựng nếu có lệnh `allure`, hoặc gõ `run_r9_automation.cmd allure` |
| `artifacts/videos/` | video 1280x720 của từng test có trình duyệt, tên `TC-xxx__ten_test.webm`, tối thiểu 5 giây (đổi bằng `R9_MIN_VIDEO_SECONDS`, 0 là tắt). Test chỉ gọi SQL hoặc API không có video |
| `artifacts/allure-results/` | dữ liệu thô JSON của Allure |
| `artifacts/reports/r9_case_report.html` | **báo cáo theo từng case R9**, tự mở khi runner xong: mã case, tiêu đề, severity, kết quả, lý do, mục "Cần xử lý" nằm trên cùng |
| `artifacts/reports/r9_case_report.csv` | cùng nội dung, mở bằng Excel (UTF-8 có BOM) |
| `artifacts/reports/report.html` | báo cáo theo tên test của pytest-html, có thêm cột Case R9 |
| `artifacts/reports/junit.xml` | kết quả cho máy đọc, gửi lại cho QA để chỉnh locator |
| `artifacts/test-results/` | ảnh chụp và trace của test lỗi (`playwright show-trace trace.zip`) |
| `artifacts/auth/` | phiên đăng nhập đã lưu, đã đưa vào `.gitignore`, xóa đi để đăng nhập lại |

| Kết quả | Ý nghĩa |
|---|---|
| passed | bản build hành xử đúng như case |
| failed | lỗi locator hoặc thời gian trong script, hoặc lỗi thật chưa đánh dấu |
| xfailed | test `known_defect` thất bại như dự kiến, lệch còn đó |
| xpassed | test `known_defect` lại đạt: lệch đã được sửa, gỡ nhãn `known_defect` |
| skipped | không đủ dữ liệu, thiếu simulator, thiếu quyền ghi, hoặc case chưa tự động. Lý do nằm trong thông báo |

### Đọc báo cáo theo case

`reporting.py` gom kết quả theo mã TC-xxx (lấy từ tên hàm test, và từ tham số `case_id` của case chưa tự động), rồi gắn tiêu đề, suite, severity, review status từ `data/cases.py` (sinh từ workbook). Mỗi case có một kết luận:

| Kết luận | Khi nào | Việc cần làm |
|---|---|---|
| FAIL, cần xem | có test thất bại hoặc lỗi | chạy lại riêng `run_r9_automation.cmd tc <số>`, so Expected với màn thật: màn đúng mà test sai thì sửa test, màn sai thì ghi lỗi cho Dev. Có link ảnh chụp và trace |
| XPASS, có thể đã hết lỗi | test `known_defect` lại đạt | kiểm lại rồi gỡ nhãn `known_defect` |
| LỖI ĐÃ BIẾT, chờ sửa | test `known_defect` thất bại đúng kỳ vọng | đưa Dev hoặc BA. Báo cáo ghi cả lý do lệch và thông báo quan sát được lần chạy này |
| ĐẠT | mọi test của case đạt | không |
| BỎ QUA | có test nhưng không chạy được (thiếu dữ liệu, thiếu cờ) | đọc lý do |
| CHƯA TỰ ĐỘNG HÓA | case không có test, lý do ở `data/not_automated.py` | xem `docs/NOT_AUTOMATED.md` |
| KHÔNG CHẠY LẦN NÀY | bị lọc bằng `-m` hoặc `-k`, hoặc chế độ `read` bỏ test ghi dữ liệu thật | chạy `pay` hoặc `destructive` nếu cần |

Mục "Cần xử lý" xếp FAIL trước, rồi XPASS, rồi LỖI ĐÃ BIẾT, mỗi nhóm theo severity S1 đến S4. Một case có nhiều test thì lấy kết luận xấu nhất. Sau mỗi lần chạy, cửa sổ lệnh in số lượng từng loại và danh sách case FAIL. Khi sổ case đổi, chạy lại `tools/build_coverage.py` để làm mới `data/cases.py`.

## Giả định mở (draft)

| Mã | Nội dung | Cần ai xác nhận |
|---|---|---|
| ASM-R9-UI-01 | R9 viết theo hóa đơn có dòng, GST, trạng thái. UI thật liệt kê khoản phí (charge) và chỉ tạo hóa đơn khi bấm Authorize & pay. Bộ test ánh xạ "hóa đơn" sang "khoản phí". Đây là suy luận của QA | BA, Dev |
| ASM-R9-UI-02 | Câu chữ thông báo của R9 khác UI thật (ví dụ TC-010 ghi "Something went wrong..." còn UI ghi "Unable to load education accounts"). Test so theo UI thật | BA |
| ASM-R9-UI-03 | R9 cho phụ huynh hạ phần EA của Both (TC-051 đến TC-062). UI thật tự tính và khóa phần chia ("The payment split is calculated automatically and cannot be edited") | BA |
| ASM-R9-UI-04 | TC-081 kiểm khóa Idempotency-Key bằng mã học sinh không tồn tại để khỏi tạo giao dịch. Nếu máy chủ kiểm mã thực thể trước khóa thì sẽ báo 404 và test cần đọc lại | Dev |

## Lệch giữa bản build và R9 mà bộ test kỳ vọng (known_defect)

| Case | Lệch | Nguồn |
|---|---|---|
| TC-004, TC-005 | thẻ con không có trường, khối, lớp, nhãn còn hay không còn khoản chưa trả | quan sát UI qua mã nguồn |
| TC-029, TC-038 | học sinh chưa có EA (ví 404): UI báo lỗi tải cả trang, không cho trả online | suy ra từ mã nguồn |
| TC-032, TC-033 | trạng thái rỗng không có liên kết về danh sách con | suy ra từ mã nguồn |
| TC-039 | ví Closed vẫn cho chọn Education Account vì UI chỉ so số dư | suy ra từ mã nguồn |
| TC-041, TC-046 | không có câu giải thích vì sao Education Account bị khóa | suy ra từ mã nguồn |
| TC-051 | không hạ được phần EA của Both | suy ra từ mã nguồn, i18n `split.readOnlyDescription` |
| TC-063 | màn xem lại không có số dư sau thanh toán | `F9_Dev_Local_Run_Results.md` |
| TC-090, TC-139 | sau khi cổng thất bại, khoản phí không quay lại danh sách | `F9_Dev_Local_Run_Results.md` |
| TC-101 | màn chờ chia khoản không nói phần EA đã bị giữ | suy ra từ mã nguồn |
| TC-103, TC-137 | phần online thất bại không hoàn phần EA | `F9_Dev_Local_Run_Results.md` |
| TC-131, TC-132 | biên lai chỉ có In, không tải PDF | suy ra từ mã nguồn |
| TC-136 (lý do) | màn thất bại không hiện lý do | suy ra từ mã nguồn |
| TC-138, TC-144 | lỗi 5xx hiện nguyên văn danh sách `errors` của máy chủ, có thể lộ chi tiết kỹ thuật (`packages/api-client/src/api-error.ts`) | suy ra từ mã nguồn |
| TC-140 | không có nút Try again ở màn thất bại | `F9_Dev_Local_Run_Results.md` |

## Cấu trúc

```
allure_support.py        báo cáo Allure và video từng case (cùng kiểu r4_automation)
conftest.py              đăng nhập MockPass một lần mỗi phiên (chép cả người dùng trong sessionStorage vào mỗi tab), fixture trang, Catalog, API, ghi nhận request
pytest.ini               nhãn f91 đến f98, rules, smoke, readonly, mocked, api, mutating, online, admin, destructive, draft, known_defect, extra
data/seed.py             địa chỉ e-service và admin portal, persona, các cổng bật ghi dữ liệu
data/ui_text.py          câu chữ cố định của UI (lấy từ packages/i18n/src/resources.ts)
data/mocks.py            phong bì API giả, ví giả, giao dịch giả, hóa đơn giả
data/not_automated.py    sinh tự động bởi tools/build_coverage.py
data/cases.py            tiêu đề, suite, severity, review status của 187 case, sinh tự động bởi tools/build_coverage.py
reporting.py             plugin pytest: báo cáo theo từng case (r9_case_report.html, .csv) và cột Case R9 trong report.html
pages/                   Page Object: portal (đăng nhập), accounts_page, billing_page, result_page, simulator_page, admin_page (trang đăng nhập admin), catalog, postconditions (hậu điều kiện rev FS09)
tests/                   test_00_smoke, test_f91 đến test_f99 (f99 = TC-173 đến TC-206), test_not_automated
tools/build_coverage.py  dựng lại data/not_automated.py và docs/COVERAGE.md từ sổ case
tools/reset_payment_data.sql  đưa dữ liệu hai con về lúc đầu (chạy tay, chưa chạy lần nào)
docs/COVERAGE.md         ánh xạ TC sang test và lý do case chưa tự động
```

Dựng lại bảng phủ khi thêm test: `python tools/build_coverage.py ..\R9_Test_Cases_final_FS09.xlsx ..\R9_Test_Cases_notes.xlsx` (tham số thứ hai là sổ cũ, có thì COVERAGE.md thêm mục case đã đổi).

## Quy ước

1. Một case một test, tên `test_tc_NNN_<tiêu đề>`. Test gộp nhiều case ghi `test_tc_004_tc_005_...`. Docstring bắt đầu bằng mã case. `tools/build_coverage.py` đọc mã từ tên hàm.
2. Thứ tự định vị: role, label, text, rồi mới CSS ngắn. UI dùng thư viện `@edusave/ui` nên hầu hết điều khiển có role và tên truy cập được. Locator chỉ nằm trong `pages/`.
3. Không dùng sleep. Chờ bằng `expect(...)` hoặc `wait_until(page, ...)`.
4. Không gắn cứng tên con. `Catalog` đọc danh sách con, số dư, khoản phí một lần đầu phiên rồi chọn con hợp kịch bản; test ghi dữ liệu đọc lại trên trang ngay trước khi thanh toán.
5. `@pytest.mark.known_defect(reason=...)` biến test thành xfail không nghiêm ngặt. Lý do nói rõ nguồn của lệch.
6. Test mutating không bao giờ chạy nếu chưa có `R9_ALLOW_PAYMENTS=1`; test destructive cần thêm `R9_ALLOW_DESTRUCTIVE=1`.
7. Bộ test không sửa sổ case R9 và không sửa mã Dev.
8. Không lưu hay gõ mật khẩu. Đăng nhập chỉ chọn persona MockPass.

## Việc còn lại

1. Chạy `smoke` và `read` trên máy thật, gửi `junit.xml` để chỉnh locator và xác nhận các lệch suy ra từ mã nguồn.
2. Việc có thể làm tiếp: TC-085 (giữ giao dịch Pending), TC-079, TC-083 và TC-166 (phụ huynh thứ hai), TC-082 (song song, nên dùng k6 hoặc JMeter), TC-002 và TC-003 (đăng nhập thất bại, hủy trên MockPass), phần chưa kiểm của TC-193 (Cancel bị khóa sau Confirm), TC-199 (API biên lai) và TC-201 (thứ tự leg).
3. Test SQL của F9.8 (và TC-205, TC-206) dùng student cố định hoặc lấy dòng đầu của `student_charges`; kiểm lại với bộ seed R9 mới khi chạy lần đầu.
4. Bốn test cần đăng nhập thật bằng MockPass trong trình duyệt sạch (TC-001, TC-017 hai test, TC-142) chưa được thử ở đâu, kể cả bản giả lập.
5. Khi có tài khoản admin của QA và màn phát hành hóa đơn ở admin portal: thêm bước tạo hóa đơn Issued bằng admin cho các case có tiền điều kiện FS 3.1.1, và đọc số dư EA từ trang quản lý tài khoản giáo dục của admin để kiểm hậu điều kiện số dư.
6. Hỏi Dev về `reset_payment_data.sql` cho dữ liệu mới (Test Child One, Two, Three) trước khi chạy `pay` lần nữa.

## Dữ liệu seed R9 (bổ sung ngày 25/10/2026)

Bộ dữ liệu còn thiếu cho e-Service nằm ở `tools/seed_r9_data.sql` (thêm 13 con R9 cho persona S7890123F, kèm ví, khoản phí, hóa đơn, giao dịch). Kiểm tra bằng `tools/seed_r9_verify.sql`, dọn bằng `tools/seed_r9_cleanup.sql`. Chi tiết và lệnh chạy xem `docs/SEED_R9.md`.

Tên DB tự nhận: biến `R9_BILLING_DB` và `R9_EA_DB` có thể ép tên; mặc định thử lần lượt `BillingPaymentDatabase`, `BillingPaymentService` và `EducationAccountDatabase`, `EduAccount` theo DB có thật trong container.
