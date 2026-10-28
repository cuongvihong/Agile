# R4 trên UI thật: case nào đã tự động, case nào chưa, chỗ nào lệch sổ case

Ngày: 25/10/2026. Đích: admin portal `http://localhost:5173` (bản code `roles\dev\codesprint2ending`), tài khoản `moehq` của seed IAM. Chưa chạy thật (môi trường soạn không có Docker và trình duyệt), mới kiểm cú pháp và thu thập được 51 test.

## 1. Đã tự động (tests\real)

| Suite | Case | Test | Loại | Ghi chú |
|---|---|---|---|---|
| Smoke | TC-901 đến TC-906 | test_real_00_smoke.py | readonly | Đăng nhập MOE HQ và School, mở danh sách, wizard, FAS application, SBFAS |
| F4.13 | TC-168 | list khớp API | readonly | So tên trong bảng với `GET /fas/v1/fas/moe-schemes` |
| | TC-170 | subtitle | draft | UI thật chỉ có câu đầu của sổ case |
| | TC-171 | thẻ đếm theo trạng thái | draft | UI thật có 7 thẻ theo trạng thái gốc, sổ case có 4 thẻ |
| | TC-172 | cột và nội dung ô | readonly | So từng ô với dữ liệu API (ngày, eligibility, trạng thái) |
| | TC-174 | sắp xếp Effective from mới nhất trước | readonly | Code front end không sắp xếp, phụ thuộc thứ tự API |
| | TC-178, 229, 231 | hành động theo trạng thái | draft | Xem mục 3 |
| | TC-229 | View mở trang chi tiết chỉ đọc | readonly | |
| F4.14 | TC-181 đến 187, 189 | bước General | readonly, TC-181 draft | |
| | TC-190 đến 194 | bước Eligibility | readonly, TC-190 và 193 draft | |
| | TC-196 đến 199, 204 | bước Subsidy | readonly, TC-196 draft | TC-199 so danh sách với API billing |
| | TC-205 (2 giá trị), 206 | ô phần trăm | known_defect | Xem mục 4 |
| | TC-209 | giữ giá trị khi Next và Back | readonly | |
| | TC-210 | Draft tạo dòng Draft | mutating | |
| | TC-211, 213 | Draft không tên, Discard | readonly | |
| F4.15 | TC-214 đến 217 | Review và Publish | mutating | Review là bước 4 của wizard, không phải hộp thoại |
| | TC-219, 220 | chặn chồng lấn giai đoạn | known_defect, mutating | Xem mục 4 |
| | TC-221 | giai đoạn nối tiếp được phép | mutating | |
| F4.16 | TC-231 đến 234, 236 | Add fees | mutating | Scheme tạo bằng API, Add fees là trang riêng |

Dữ liệu tạo ra có tên bắt đầu bằng `R4-AUTO` và giai đoạn năm 2100 trở đi. Không có API xóa MOEFAS, dùng `run_r4_automation.cmd cleanup` để xóa mềm.

## 2. Chưa có màn hình thật hoặc chưa tự động

| Case | Lý do |
|---|---|
| TC-001 đến 167 (F4.1 đến F4.12), TC-245 đến 267 (F4.18 đến F4.20) | Màn đơn FAS ở develop vẫn là trang stub hoặc chưa có. Giữ bộ prototype cho đến khi có màn |
| TC-224 | Cần tài khoản School của trường thứ hai, seed chỉ có một (`school`), test là placeholder not_automated |

## SBFAS (School user), test_real_f4s_sbfas.py, lệnh `run_r4_automation.cmd sbfas`

| Case | Test | Ghi chú |
|---|---|---|
| TC-169 | test_tc_169 | So bảng với API của trường, không có scheme MOEFAS. Phần trường thứ hai chưa làm |
| TC-173 | test_tc_173 | known_defect BUG-R4-012: hàng scheme có ngày dạng YYYY-MM-DD và không có chữ Approved by school |
| TC-201 | test_tc_201 | Bước 3 liệt kê đúng các lớp active của trường (Junior College 1, Secondary 1) |
| TC-202 | test_tc_202 | draft: giá trị đầu của ô (ca nói 0, MOEFAS để trống) |
| TC-203 | test_tc_203 | draft: bước 1 |
| TC-222 | test_tc_222, test_tc_222b | Bị chặn vì trùng tên; thông báo overlap theo FS là known_defect |
| TC-223 | test_tc_223 | Khác tên cùng kỳ được phép |
| TC-228 | test_tc_228 | known_defect: build không cho trùng tên trong trường |
| TC-241 | test_tc_241 | Hộp Add fee: phí còn thiếu, dòng theo lớp, lưu thành công, số phí thành 2 |
| TC-175 | Cần đồng hồ chỉnh được |
| TC-179, TC-242 đến 244 (F4.17) | Không có nút Close form now (demo) trên UI thật |
| TC-188 | Ô ngày là input type=date, không gõ được chữ không phải ngày |
| TC-195, 218, 239, 240 | Cần chức năng khác (nộp đơn F10, hạn mức đơn, hóa đơn F3) |
| TC-200, 207, 208 | Bản thật chỉ có giá trị phần trăm, không có loại số tiền cố định |
| TC-212 | Không có nút Edit cho Draft trên UI thật |
| TC-226, 227 | Cần quy tắc kế thừa kỳ (BUG-R4-011 chặn trùng tên, BUG-R4-003 chưa có kiểm tra chồng lấn) |
| TC-230, 235, 237, 238 | Cần gọi API trực tiếp hoặc scheme Closed, chưa viết |

## Quy tắc validate (R4_FAS_Validation_Rules_EN.docx), test_real_f4v_validation.py, lệnh `run_r4_automation.cmd validation`

Mỗi case một hàm `test_tc_NNN`. Case API gửi request bằng cookie đăng nhập (school cho SBFAS, moehq cho MOEFAS), case UI gõ vào wizard.
Tên scheme bắt đầu bằng R4-AUTO. Bản nháp SBFAS tự xóa cuối test, MOEFAS không có API xóa nên dọn bằng `cleanup`.

| Case | Nội dung | Ghi chú |
|---|---|---|
| TC-161 | Không đăng nhập thì cả hai danh sách trả 401 | readonly |
| TC-165 | School đọc MOEFAS phải bị 403, MOE HQ đọc SBFAS phải bị 403 | known_defect BUG-R4-013 |
| TC-225 | Hai Draft trùng kỳ được lưu, Published trùng kỳ phải bị chặn | known_defect BUG-R4-003 |
| TC-268 đến 276, 279 đến 285 | SBFAS API: tên, ngày, ngân sách, quốc tịch, nhóm thu nhập, luật khớp, mô tả, phí, phần trăm, trùng phí và lớp | Đạt |
| TC-277, 278 | SBFAS API: From của PCI và GHI phải bắt buộc khi bật | known_defect BUG-R4-007 |
| TC-286, 287, 292 | Fee component hoặc lớp không tồn tại phải bị từ chối (SBFAS, MOEFAS, Add fee) | known_defect BUG-R4-008 |
| TC-288 | Mỗi lớp phải có giá trị | known_defect BUG-R4-009 |
| TC-289 đến 291 | Add fee API: khoảng phần trăm, số thập phân, thiếu item, trùng lớp, phí đã có (409) | Đạt |
| TC-293, 294, 296 đến 300, 302, 303 | MOEFAS API: tên, thứ tự ngày, trạng thái, thu nhập, quốc tịch, subsidy, phần trăm, ngân sách, trùng tên | Đạt |
| TC-295 | MOEFAS nhận ngày trong quá khứ, SBFAS thì chặn | known_defect BUG-R4-010 |
| TC-301 | MOEFAS nhận phần trăm 3 chữ số thập phân | known_defect BUG-R4-002 |
| TC-304 đến 306, 308, 311 | Wizard SBFAS: thông báo bắt buộc, thứ tự ngày, tên tối đa 150, quốc tịch và nhóm thu nhập, hộp Add fee | Đạt |
| TC-307, 309 | Thông báo sai lý do cho ngân sách và ô phần trăm | known_defect BUG-R4-014 |
| TC-310 | Trùng tên chỉ hiện toast chung, không nói lý do | known_defect BUG-R4-015 |
| TC-312, 313 | Wizard MOEFAS: tên tối đa 150, số âm và To nhỏ hơn From | Đạt |
| TC-314 | Wizard MOEFAS: trùng tên | draft, chưa có chữ chốt từ BA |
| TC-315 đến 331 | Ô tìm kiếm, ô comment duyệt và từ chối, thông báo chung | Chưa tự động: cần màn hình đơn FAS (ENV-R4-02), đồng hồ và request lỗi (ENV-R4-03, 04) |

## 3. Chỗ UI thật khác sổ case (chờ BA hoặc Dev chốt, các test đánh dấu `draft`)

1. Thẻ trạng thái: UI thật có 7 thẻ (Draft, Published, Application open, Application closed, Effective, Suspended, Closed). Sổ case có 4 thẻ Active, Upcoming, Closed, Draft.
2. Bảng có hai cột Form from và Form to, sổ case có một cột Application form kèm huy hiệu Open.
3. Add fees: code cho phép với Draft, Published, Application open, Application closed, Suspended, không cho với Effective và Closed (hộp thoại ghi "thêm phí đến một ngày trước ngày hiệu lực"). Sổ case ghi Add fee cho Active và Upcoming. Với Application open, hệ thống hỏi tạm ngưng scheme trước.
4. Wizard: ngày không điền sẵn, phải điền tổng ngân sách, không có ô loại giá trị, quy tắc khớp chỉ là dòng chữ cố định (không chọn được), ô To của dải thu nhập bắt buộc nhập, ô From để trống tính là 0. Sổ case ghi ngược lại các điểm này.
5. Không có toast "Draft saved" hay "Scheme published". Sau khi lưu, trang quay về danh sách.
6. Nút Discard thoát ngay, không hỏi xác nhận (code còn TODO).

## 4. Lỗi nghi ngờ đã đối chiếu với code (test đánh dấu known_defect)

| Test | Điều đọc được trong code | Cách xác nhận trên màn hình |
|---|---|---|
| TC-205, TC-234b | `SubsidyMatrix.tsx` và `validation.ts` dùng khóa `errors.amountRange`, `resource.ts` chỉ định nghĩa `errors.amountInvalid`. Khóa thiếu bản dịch nên thông báo có thể hiện chuỗi khóa thô. Thông báo thiếu mức tối thiểu cũng dùng chung khóa này | Nhập -1 hoặc 101 vào ô phần trăm, đọc dòng đỏ dưới bảng |
| TC-206 | `isAmountInvalid` chỉ kiểm 0 đến 100, không giới hạn hai chữ số thập phân | Nhập 33.333 |
| TC-219, 220 | FASService không có kiểm tra chồng lấn thời gian hiệu lực hay thời gian mở đơn (tìm "overlap" không thấy), front end `validation.ts` còn TODO. Backend chỉ chặn trùng tên | Tạo hai scheme cùng giai đoạn rồi Publish |

Ngoài ra, mã đọc thêm hai điểm chưa viết test: ô phần trăm toàn 0 qua validation (chỉ cần "đã điền") nhưng `toSubsidyRequests` bỏ giá trị 0 nên có thể gửi lên danh sách subsidy rỗng; khóa `descriptionTooLong` không có trong `resource.ts` của MOEFAS (ô mô tả đã giới hạn 500 ký tự nên khó chạm tới).

## 5. Việc QA cần làm khi chạy

1. Chạy stack, kiểm đăng nhập `moehq` / `123456` (đổi bằng `R4_HQ_USER`, `R4_HQ_PASS`).
2. `.\run_r4_automation.cmd` (smoke) trước, rồi `.\run_r4_automation.cmd readonly`, cuối cùng `.\run_r4_automation.cmd mutating`.
3. Gửi dòng tổng kết pytest và danh sách test fail. Selector chưa kiểm trên DOM thật (nhãn checkbox, tên accessible của bảng và hộp thoại), nên vài test có thể cần chỉnh lần đầu.
4. Chạy `.\run_r4_automation.cmd cleanup` sau khi xong.
