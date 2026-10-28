# QUY TẮC KIỂM TRA HỢP LỆ (VALIDATION RULES)
## Requirement R6, Function 6: FAS Budget & Statistics (Quản lý Ngân sách & Thống kê Trợ cấp FAS)

> **Dành cho:** Development Team & QA Team  
> **Dự án:** Agileproject – Hệ thống Quản lý Tài chính Giáo dục (EduFAMS)  
> **Căn cứ tài liệu:** 
> - `FS06.md` – Functional Specification R6: FAS Budget & Statistics (Draft v0.1)
> - Cấu trúc cơ sở dữ liệu hệ thống: `fas_budgets`, `fas_budget_adjustments`, `fas_schemes`  
> **Cổng thông tin áp dụng:** Administration Portal (`http://localhost:5173`)  
> **Phiên bản tài liệu:** v1.0 – Ngày 26/10/2026  

---

## 1. PHẠM VI VÀ ĐỐI TƯỢNG

Tài liệu này quy định toàn bộ các quy tắc kiểm tra tính hợp lệ dữ liệu (Validation Rules - VR) ở cả phía giao diện người dùng (Client-side / Frontend) và máy chủ (Server-side / Backend API / Database Constraints) cho Requirement **R6 – FAS Budget & Statistics**, bao gồm 3 phân hệ chức năng:
1. **R6.1 – Budget Management:** Thiết lập và quản lý hạn mức ngân sách cho chương trình MOEFAS (Bộ GD quản lý) và SBFAS (Trường học quản lý).
2. **R6.2 – Subsidy Statistics:** Tổng hợp và hiển thị thống kê tổng số tiền trợ cấp FAS đã được cấp (Granted).
3. **R6.3 – Budget Tracking & Warning:** Theo dõi tiến độ giải ngân, tỷ lệ sử dụng ngân sách, số dư còn lại và phát cảnh báo phi ngăn chặn (Non-blocking warning) khi ngân sách chạm ngưỡng hoặc cạn kiệt.

### Đối tượng người dùng (Actors & Scopes):
* **MOE HQ User (Quản trị viên Bộ GD):** Có quyền thiết lập ngân sách `MOEFAS` toàn hệ thống và xem thống kê, theo dõi sử dụng ngân sách MOEFAS trên phạm vi toàn quốc.
* **School User (Quản trị viên Trường - School Admin):** Có quyền thiết lập ngân sách `SBFAS` thuộc trường mình phụ trách; chỉ được xem thống kê và theo dõi ngân sách SBFAS của đúng trường đó (`SchoolId`), tuyệt đối không được truy cập chéo dữ liệu của trường khác.

---

## 2. QUY ƯỚC & ĐỊNH DẠNG CHUẨN

* **Định dạng tiền tệ:** Đô la Singapore (`S$ #,##0.00`). Ví dụ: `S$ 50,000.00`, `S$ 0.00`.
* **Kiểu dữ liệu số tiền trong CSDL:** `DECIMAL(18, 2)` (không dùng kiểu `FLOAT` hoặc `DOUBLE` để tránh sai số dấu phẩy động).
* **Định dạng tỷ lệ phần trăm:** `#0.0%` hoặc `#0.00%`. Ví dụ: `75.5%`, `100.0%`, `112.4%`.
* **Cắt khoảng trắng (Trim):** Mọi trường nhập văn bản hoặc số đều phải tự động cắt bỏ khoảng trắng thừa ở đầu và cuối trước khi kiểm tra hợp lệ.
* **Mã quy tắc kiểm tra (Validation Rule IDs):**
  - `VR-R6-BMxx`: Quy tắc cho Budget Management (Thiết lập ngân sách).
  - `VR-R6-STxx`: Quy tắc cho Subsidy Statistics (Thống kê trợ cấp).
  - `VR-R6-TRxx`: Quy tắc cho Budget Tracking & Warnings (Theo dõi & Cảnh báo ngân sách).
  - `VR-R6-SECxx`: Quy tắc bảo mật, phân quyền và cách ly dữ liệu (Security & Isolation).
  - `VR-R6-SYSxx`: Quy tắc kỹ thuật máy chủ, CSDL và xử lý tương tranh (System & Database).

---

## 3. MÀN HÌNH A: QUẢN LÝ NGÂN SÁCH (BUDGET MANAGEMENT - SCR-R6-01)

### 3.1. Danh mục thành phần giao diện (UI Elements)

| Mã UI | Tên phần tử | Loại điều khiển | Bắt buộc | Mô tả |
| :--- | :--- | :--- | :---: | :--- |
| **UI-R6-001** | FAS Type | Label / Read-only | Có | Loại trợ cấp (`MOEFAS` đối với MOE HQ, `SBFAS` đối với School User). |
| **UI-R6-002** | Academic Year | Dropdown / Label | Có | Năm học áp dụng ngân sách (Mặc định năm hiện tại, vd: `2026`). |
| **UI-R6-003** | School Name | Label / Read-only | Có (SBFAS) | Tên trường tương ứng (Chỉ hiển thị với School User, cố định theo phiên làm việc). |
| **UI-R6-004** | Budget Amount | Numeric Textbox | Có | Ô nhập số tiền ngân sách được phân bổ (`AllocatedBudgetAmount`). |
| **UI-R6-005** | Save Button | Button (Primary) | - | Nút lưu thiết lập ngân sách. |
| **UI-R6-006** | Cancel Button | Button (Secondary) | - | Hủy thao tác nhập liệu và quay lại màn hình trước. |
| **UI-R6-007** | Configured Budget Amount | Display Field | - | Hiển thị ngân sách hiện đang áp dụng sau khi lưu thành công. |
| **UI-R6-008** | Edit Budget Button | Button (Secondary) | - | Mở chế độ chỉnh sửa / điều chỉnh ngân sách đã cấu hình. |
| **UI-R6-009** | Adjustment Reason | Textarea (Modal) | Tùy chọn/Có khi sửa | Lý do điều chỉnh ngân sách (ghi nhận vào `fas_budget_adjustments`). |

---

### 3.2. Quy tắc kiểm tra hợp lệ chi tiết từng trường

#### Quy tắc trường A1: `Budget Amount` (UI-R6-004)

| Mã quy tắc | Tên quy tắc | Điều kiện hợp lệ | Điều kiện vi phạm | Hành vi hệ thống & Thông báo lỗi | Nguồn FS |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **VR-R6-BM01** | Bắt buộc nhập | Giá trị số không được để trống | Ô nhập trống, toàn dấu cách hoặc `null` | Nút **Save** bị vô hiệu hóa hoặc báo lỗi inline:<br>`"Budget amount is required."` | FS 5.1.3 |
| **VR-R6-BM02** | Kiểu dữ liệu số | Chỉ chứa các chữ số `0-9` và tối đa 1 dấu chấm thập phân `.` | Chứa ký tự chữ (`abc`), ký tự đặc biệt (`$`, `@`, `,`, `-`), chữ cái khoa học (`1e5`) | Ngăn nhập trực tiếp trên bàn phím hoặc báo lỗi:<br>`"Budget amount must be a valid number."` | FS 5.1.3 |
| **VR-R6-BM03** | Giá trị số dương | Giá trị $> 0.00$ (hoặc $\ge 0.00$ nếu thiết lập ngân sách ban đầu bằng 0) | Nhập số âm ($< 0$) | Báo lỗi inline:<br>`"Budget amount must be greater than or equal to 0."` | BR6.03 |
| **VR-R6-BM04** | Độ chính xác thập phân | Tối đa 2 chữ số phần thập phân sau dấu chấm (cents) | Nhập từ 3 chữ số thập phân trở lên (vd: `50000.125`) | Tự động làm tròn hoặc hiển thị cảnh báo:<br>`"Budget amount can have at most 2 decimal places."` | G10 |
| **VR-R6-BM05** | Giới hạn ngân sách tối đa | Giá trị $\le 999,999,999.99$ SGD (phù hợp giới hạn `DECIMAL(18,2)`) | Nhập vượt quá $999,999,999.99$ SGD | Chặn nhập thêm ký tự hoặc báo lỗi:<br>`"Budget amount cannot exceed S$ 999,999,999.99."` | Database Schema |
| **VR-R6-BM06** | Khoảng trắng đầu/cuối | Tự động loại bỏ dấu cách đầu/cuối chuỗi nhập | Chuỗi có dấu cách như `"  75000  "` | Hệ thống tự động `trim()` thành `"75000"` trước khi validate và gửi API | Standard |

#### Quy tắc thao tác A2: `Save & Edit Budget` (UI-R6-005, UI-R6-008, UI-R6-009)

| Mã quy tắc | Tên quy tắc | Điều kiện | Phản ứng của hệ thống | Nguồn FS |
| :--- | :--- | :--- | :--- | :--- |
| **VR-R6-BM07** | Bất biến loại FAS | Khi người dùng ở form tạo/sửa ngân sách | `FAS Type` là cố định (`Read-only`), không được phép thay đổi giá trị giữa `MOEFAS` và `SBFAS`. | FS 5.1.3, 5.2.3 |
| **VR-R6-BM08** | Cố định trường học cho School User | School User thiết lập ngân sách SBFAS | Trường học (`SchoolId`) tự động gắn cứng theo trường của người dùng đang đăng nhập, không có ô chọn trường khác. | BR6.01, FS 5.2.3 |
| **VR-R6-BM09** | Chỉnh sửa ngân sách (Budget Adjustment) | Người dùng chỉnh sửa ngân sách đã có | Hệ thống hiển thị hộp thoại xác nhận; nếu số tiền mới khác số tiền cũ, hệ thống tạo một bản ghi lịch sử điều chỉnh vào bảng `fas_budget_adjustments` ghi nhận `AdjustmentAmount`, `PreviousAllocatedAmount`, `NewAllocatedAmount`, `Reason` và `ApprovedByUserId`. | FS 5.1.6, G2 |
| **VR-R6-BM10** | Chống bấm đúp (Debouncing) | Người dùng bấm nút Save nhiều lần liên tục | Nút Save chuyển sang trạng thái Disabled kèm spinner hiển thị `"Saving..."`, ngăn chặn gửi trùng request lên backend. | Standard UX |

---

## 4. MÀN HÌNH B: THỐNG KÊ TRỢ CẤP ĐÃ CẤP (SUBSIDY STATISTICS - SCR-R6-02)

### 4.1. Danh mục thành phần giao diện (UI Elements)

| Mã UI | Tên phần tử | Loại điều khiển | Mô tả |
| :--- | :--- | :--- | :--- |
| **UI-R6-010** | Statistics Page Title | Label | Tiêu đề trang (`MOEFAS Subsidy Statistics` hoặc `SBFAS Subsidy Statistics`). |
| **UI-R6-011** | Scope Indicator | Label / Badge | Chỉ thị phạm vi (`National / All Schools` hoặc tên cụ thể của trường). |
| **UI-R6-012** | Total Subsidy Amount Granted | Metric Card / Summary | Tổng số tiền trợ cấp đã được cấp chính thức (`Granted`). |
| **UI-R6-013** | Academic Year Filter | Dropdown Filter | Lọc theo năm học áp dụng. |
| **UI-R6-014** | Subsidy Statistics Table | Data Table | Bảng chi tiết thống kê các đợt grant/khoản trợ cấp. |
| **UI-R6-015** | Empty State View | UI Component | Hiển thị thông báo khi chưa có dữ liệu trợ cấp nào được cấp trong kỳ. |

---

### 4.2. Quy tắc kiểm tra tính hợp lệ & Tổng hợp thống kê

| Mã quy tắc | Tên quy tắc | Nội dung quy tắc & Công thức nghiệp vụ | Phản ứng hệ thống & Định dạng | Nguồn FS |
| :--- | :--- | :--- | :--- | :--- |
| **VR-R6-ST01** | Điều kiện tổng hợp trợ cấp | Chỉ tổng hợp các khoản trợ cấp đã có trạng thái `Granted` (hoặc `Approved`). | Các khoản đơn ở trạng thái `Draft`, `Pending`, `Under Review`, `Rejected` tuyệt đối **không** được cộng vào `Total Subsidy Amount Granted`. | BR6.04, FS 5.6.1 |
| **VR-R6-ST02** | Định dạng số tiền tổng hợp | Hiển thị số tiền với dấu ngăn cách hàng nghìn và 2 chữ số thập phân. | Ví dụ: `S$ 124,500.00`. Nếu số tiền bằng 0, hiển thị `S$ 0.00`. | FS 5.6.2, G10 |
| **VR-R6-ST03** | Xử lý dữ liệu rỗng (Empty State) | Khi năm học hoặc trường học chưa có bất kỳ khoản trợ cấp nào được duyệt. | Không hiển thị lỗi kết nối hay giá trị `null`/`NaN`. Hiển thị Card `Total Subsidy: S$ 0.00` và bảng rỗng kèm thông báo: `"No subsidy grant records found for the selected academic year."` | Robustness |
| **VR-R6-ST04** | Cô lập dữ liệu thống kê của School | School User truy cập trang thống kê SBFAS. | Câu truy vấn backend bắt buộc lọc cứng theo `school_id` của tài khoản; không trả về tổng số tiền hoặc dòng dữ liệu của trường khác. | BR6.01, BR6.02, FS 5.5.4 |
| **VR-R6-ST05** | Tổng hợp toàn diện cho MOE HQ | MOE HQ User truy cập trang thống kê MOEFAS. | Dữ liệu tổng hợp phản ánh toàn bộ các khoản trợ cấp MOEFAS trên tất cả các trường học trực thuộc trong năm tài chính. | FS 5.4.5 |
| **VR-R6-ST06** | Phân trang & Giới hạn tải dữ liệu | Bảng danh sách chi tiết trợ cấp có nhiều dòng. | Hỗ trợ phân trang chuẩn (`PageSize` mặc định 10 hoặc 20 dòng/trang). Không tải dồn toàn bộ gây đơ giao diện. | Performance |

---

## 5. MÀN HÌNH C: THEO DÕI SỬ DỤNG NGÂN SÁCH & CẢNH BÁO (BUDGET TRACKING - SCR-R6-03)

### 5.1. Danh mục thành phần giao diện (UI Elements)

| Mã UI | Tên phần tử | Loại điều khiển | Mô tả |
| :--- | :--- | :--- | :--- |
| **UI-R6-016** | Allocated Budget Amount | Summary Card | Số tiền ngân sách đã được thiết lập ban đầu (`AllocatedBudgetAmount`). |
| **UI-R6-017** | Subsidy Amount Used | Summary Card | Tổng số tiền trợ cấp được tính là đã sử dụng ngân sách (`CommittedSubsidyAmount` / `DisbursedSubsidyAmount`). |
| **UI-R6-018** | Remaining Budget | Summary Card | Ngân sách còn lại của kỳ (`RemainingBudgetAmount`). |
| **UI-R6-019** | Budget Utilization Rate | Progress Bar / % Metric | Tỷ lệ sử dụng ngân sách tính theo phần trăm. |
| **UI-R6-020** | Budget Alert Banner | Warning / Alert Box | Biển cảnh báo khi ngân sách sắp hết hoặc đã vượt hạn mức. |

---

### 5.2. Quy tắc tính toán & Quy tắc cảnh báo (Tracking & Non-blocking Alert Rules)

| Mã quy tắc | Tên quy tắc | Công thức & Điều kiện kích hoạt | Phản ứng hệ thống & Giao diện | Nguồn FS |
| :--- | :--- | :--- | :--- | :--- |
| **VR-R6-TR01** | Công thức Ngân sách còn lại | $\text{Remaining Budget} = \text{Budget Amount} - \text{Subsidy Amount Used}$ | Hiển thị giá trị tiền tệ `S$ #,##0.00`. Được tính tự động theo cột tính toán trong CSDL: `[AllocatedBudgetAmount] - [CommittedSubsidyAmount]`. | FS 5.9.2, CSDL |
| **VR-R6-TR02** | Công thức Tỷ lệ sử dụng | $\text{Utilization (\%)} = \left(\frac{\text{Subsidy Amount Used}}{\text{Budget Amount}}\right) \times 100\%$ | - Nếu $\text{Budget Amount} > 0$: Hiển thị tỷ lệ định dạng `##0.0%` (vd: `84.5%`).<br>- Nếu $\text{Budget Amount} = 0$ và $\text{Used} = 0$: Hiển thị `0.0%`.<br>- Nếu $\text{Budget Amount} = 0$ và $\text{Used} > 0$: Hiển thị `N/A` hoặc `>100%` (không để crash lỗi chia cho 0). | FS 5.7.3, G9 |
| **VR-R6-TR03** | Hiển thị Ngân sách âm (Vượt ngân sách) | Khi $\text{Subsidy Amount Used} > \text{Budget Amount}$ ($\text{Remaining Budget} < 0$) | Số tiền còn lại hiển thị dạng âm với màu đỏ nổi bật: `-S$ 12,500.00` hoặc `(S$ 12,500.00)` kèm nhãn trạng thái **Deficit / Over-budget**. | Accounting Standards |
| **VR-R6-TR04** | Cảnh báo ngưỡng ngân sách sắp hết | Khi $80\% \le \text{Utilization} < 100\%$ (hoặc còn dưới 20% ngân sách) | Hiển thị Warning Banner màu vàng (Warning):<br>`"Warning: Budget is approaching exhaustion (X% utilized)."` | R6-11, BR6.06 |
| **VR-R6-TR05** | Cảnh báo hết/vượt ngân sách | Khi $\text{Remaining Budget} \le 0$ (hoặc $\text{Utilization} \ge 100\%$) | Hiển thị Alert Banner màu cam đỏ (Exhaustion Alert):<br>`"Alert: The configured budget for this scheme has been fully exhausted."` | R6-11, BR6.06, G3 |
| **VR-R6-TR06** | **QUY TẮC KHÔNG CHẶN CẤP TRỢ CẤP (NON-BLOCKING GRANT RULE)** | Khi đơn đăng ký FAS được duyệt/cấp trong khi ngân sách đã hết ($\text{Remaining Budget} \le 0$) | **Hệ thống hiển thị thông báo cảnh báo thông tin nhưng TUYỆT ĐỐI KHÔNG CHẶN thao tác Approve / Grant của School Admin hoặc MOE Officer.** Thao tác grant vẫn hoàn tất thành công và ghi nhận số tiền vượt hạn mức. | **BR6.06, R6-11, G3 (BẮT BUỘC)** |
| **VR-R6-TR07** | Đồng bộ số liệu tức thời (Real-time Sync) | Ngay khi một đơn FAS được phê duyệt hoặc thay đổi khoản trợ cấp | Giá trị `CommittedSubsidyAmount` và `RemainingBudgetAmount` phải được cập nhật ngay lập tức vào bảng `fas_budgets` thông qua Trigger hoặc Domain Event để màn hình thống kê phản ánh tức thời. | G11, CSDL |
| **VR-R6-TR08** | Điều chỉnh khi thu hồi trợ cấp (Grant Revocation) | Khi một khoản FAS đã grant bị hủy hoặc điều chỉnh giảm | Hệ thống tự động trừ tương ứng trong `CommittedSubsidyAmount`, làm tăng `RemainingBudgetAmount` trở lại. | FS 5.7.5, G7 |

---

## 6. QUY TẮC BẢO MẬT & PHÂN QUYỀN MÁY CHỦ (SERVER-SIDE SECURITY & AUTHORIZATION)

| Mã quy tắc | Tên quy tắc | Đối tượng & Hành động | Quy tắc kiểm soát & Phản ứng API | Nguồn FS |
| :--- | :--- | :--- | :--- | :--- |
| **VR-R6-SEC01** | Quyền hạn MOE HQ User | MOE HQ User thao tác trên hệ thống | - Có quyền truy cập endpoint `/api/fas/v1/budgets/moefas` (Xem & Cập nhật).<br>- Có quyền xem thống kê toàn hệ thống.<br>- Bị từ chối (403 Forbidden) nếu cố tình thiết lập ngân sách SBFAS cụ thể thay cho trường mà không qua cơ chế ủy quyền. | BR6.01, FS 1.2 |
| **VR-R6-SEC02** | Quyền hạn School User | School User thao tác trên hệ thống | - Chỉ được truy cập `/api/fas/v1/budgets/sbfas` với `SchoolId` khớp đúng với Claim trong JWT Token.<br>- **Bị từ chối ngay lập tức (403 Forbidden)** nếu truyền `SchoolId` của trường khác hoặc cố tình gọi API của `MOEFAS`.<br>- Thông báo lỗi: `"Access denied. You can only manage SBFAS budget for your assigned school."` | BR6.01, FS 1.2 |
| **VR-R6-SEC03** | Kiểm tra lại toàn bộ quy tắc ở Server (Zero-Trust Client) | Client gửi payload JSON lên API | Server-side validation bắt buộc kiểm tra lại: `AllocatedBudgetAmount >= 0`, `AcademicYearId` tồn tại và hợp lệ, `SchemeId` thuộc `MOEFAS` hoặc `SBFAS`. Nếu không hợp lệ, trả về mã lỗi HTTP `400 Bad Request` kèm danh sách chi tiết lỗi. | Security Standard |
| **VR-R6-SEC04** | Kiểm soát phiên đăng nhập | Token người dùng hết hạn hoặc không có quyền | Trả về mã lỗi HTTP `401 Unauthorized` và điều hướng về trang đăng nhập của Admin Portal. | Security Standard |

---

## 7. BẢNG TỔNG HỢP TOÀN BỘ CÁC THÔNG BÁO LỖI VÀ CẢNH BÁO CHUẨN (STANDARD MESSAGES CATALOG)

| Mã thông báo | Loại | Ngữ cảnh xuất hiện | Nội dung thông báo hiển thị (Tiếng Anh chuẩn UI) |
| :--- | :--- | :--- | :--- |
| **MSG-R6-E01** | Lỗi | Ô Budget Amount để trống khi lưu | `Budget amount is required.` |
| **MSG-R6-E02** | Lỗi | Ô Budget Amount nhập chữ hoặc ký tự lạ | `Budget amount must be a valid numeric value.` |
| **MSG-R6-E03** | Lỗi | Nhập số tiền âm | `Budget amount must be greater than or equal to 0.` |
| **MSG-R6-E04** | Lỗi | Nhập quá 2 chữ số thập phân | `Budget amount can have at most 2 decimal places.` |
| **MSG-R6-E05** | Lỗi | Nhập số tiền vượt hạn mức tối đa | `Budget amount cannot exceed S$ 999,999,999.99.` |
| **MSG-R6-E06** | Lỗi | Cố tình truy cập hoặc chỉnh sửa dữ liệu trường khác | `Access denied. You do not have permission to access or modify this budget record.` |
| **MSG-R6-E07** | Lỗi | Lỗi xung đột dữ liệu (Conflict / Concurrency) | `The budget record has been modified by another user. Please refresh and try again.` |
| **MSG-R6-W01** | Cảnh báo | Ngân sách sử dụng đạt từ 80% đến dưới 100% | `Warning: SBFAS budget utilization has reached {rate}%. Remaining balance: {remaining}.` |
| **MSG-R6-W02** | Cảnh báo | Ngân sách đã hết hoặc vượt quá 100% | `Alert: The budget allocation for this scheme has been exhausted. Additional grants will result in a deficit.` |
| **MSG-R6-W03** | Cảnh báo | Khi Admin bấm Grant trợ cấp trong lúc ngân sách đã cạn | `Budget Limit Notice: Current budget balance is insufficient ({remaining}), but granting is permitted under policy rules. Proceed to grant?` |
| **MSG-R6-S01** | Thành công | Lưu thiết lập ngân sách thành công | `Budget amount has been successfully configured and saved.` |
| **MSG-R6-S02** | Thành công | Lưu điều chỉnh ngân sách thành công | `Budget adjustment has been recorded successfully.` |

---

## 8. MA TRẬN TRUY VẾT YÊU CẦU (REQUIREMENT TRACEABILITY MATRIX - RTM)

| Mục trong FS06 | Mã Requirement | Tên chức năng | Quy tắc kiểm tra hợp lệ tương ứng |
| :--- | :--- | :--- | :--- |
| **Mục 2** | R6-01, R6-02, R6-03 | Quản lý ngân sách MOEFAS & SBFAS theo Actor | `VR-R6-BM01`, `VR-R6-BM07`, `VR-R6-BM08`, `VR-R6-SEC01`, `VR-R6-SEC02` |
| **Mục 2** | R6-04 | Lưu và hiển thị Budget Amount | `VR-R6-BM01` đến `VR-R6-BM06`, `VR-R6-SYS01` |
| **Mục 2** | R6-05, R6-06, R6-07 | Thống kê khoản trợ cấp đã granted theo phạm vi | `VR-R6-ST01`, `VR-R6-ST02`, `VR-R6-ST04`, `VR-R6-ST05` |
| **Mục 2** | R6-08, R6-10 | Tình hình sử dụng ngân sách & Remaining Budget | `VR-R6-TR01`, `VR-R6-TR02`, `VR-R6-TR03`, `VR-R6-TR07` |
| **Mục 2, 3**| R6-11, BR6.06 | Cảnh báo hết ngân sách nhưng không chặn Grant | **`VR-R6-TR04`, `VR-R6-TR05`, `VR-R6-TR06` (Non-blocking)** |
| **Mục 8** | G1, G2, G10 | Budget period, Budget editing & Currency formatting | `VR-R6-BM02`, `VR-R6-BM04`, `VR-R6-BM09`, `VR-R6-ST02` |

---
*Tài liệu quy tắc validation R6 được biên soạn phục vụ đối chiếu trực tiếp cho các kỹ sư Backend, Frontend và QA Automation/Manual Test Cases.*
