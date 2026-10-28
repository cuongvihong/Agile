# R4 UI Automation: FS F4 FAS Applications and Schemes

Hệ thống kiểm thử tự động Python + Pytest + Playwright cho chức năng **R4 FAS (Financial Assistance Scheme)**. Hỗ trợ chạy trên cả **UI thật đang host (`http://localhost:5173`)** và **Prototype Vercel (`https://edusave.vercel.app/`)**.

Tự động sinh **Báo cáo Allure dạng Single-File HTML** và **Quay video ~5s** cho mỗi test case.

---

## ⚡ BẢNG LỆNH COPY CHẠY NHANH (POWERSHELL / CMD)

> **Lưu ý trong PowerShell**: Hãy đứng tại thư mục `d:\AIQA\Agileproject\roles\qa\r4_automation` và luôn gõ tiền tố `.\` trước tên file: `.\run_r4_automation.cmd ...`

### 1. Chạy trên UI thật đang host (Localhost `http://localhost:5173`)

Bộ thật nằm ở `tests\real`, 51 test cho F4.13 đến F4.16 (danh sách, wizard, review và publish, add fee) cộng 6 test smoke TC-901 đến TC-906. Cần chạy sẵn stack (`run_edufams_update.cmd`). Đăng nhập tự động bằng tài khoản của seed IAM (`moehq`, `school`, mật khẩu `123456`), đổi bằng biến `R4_HQ_USER`, `R4_HQ_PASS`. Bộ này từ chối chạy nếu địa chỉ không phải localhost.

```powershell
.\run_r4_automation.cmd                 # smoke: đăng nhập và mở các màn chính
.\run_r4_automation.cmd real            # toàn bộ test thật (có test tạo dữ liệu, tên scheme bắt đầu bằng R4-AUTO)
.\run_r4_automation.cmd readonly        # chỉ test không tạo dữ liệu
.\run_r4_automation.cmd mutating        # chỉ test tạo dữ liệu
.\run_r4_automation.cmd suite 14        # một suite: 13, 14, 15 hoặc 16
.\run_r4_automation.cmd tc 183          # một case
.\run_r4_automation.cmd draft           # case chờ BA chốt (UI thật khác sổ case)
.\run_r4_automation.cmd defects         # case đã xác nhận lỗi qua code, báo xfail
.\run_r4_automation.cmd cleanup         # xóa mềm các scheme R4-AUTO trong FASDatabase
.\run_r4_automation.cmd real headed     # xem trực tiếp trên Chrome
```

Bảng case nào đã tự động trên UI thật, case nào chưa có màn hình, và những chỗ UI thật khác sổ case: xem `docs\REAL_COVERAGE.md`.

---

### 2. Mở Báo cáo Allure (Xem kết quả & Video ~5s từng case)

```powershell
# Tự động tạo và mở báo cáo Allure Report (single-file HTML có nhúng sẵn video)
.\run_r4_automation.cmd allure
```
*(Hoặc mở trực tiếp file `artifacts\allure-report\index.html` bằng trình duyệt).*

---

### 3. Chạy trên Prototype Vercel (`https://edusave.vercel.app`), chế độ cũ, không dùng cho stack thật

```powershell
# Chạy toàn bộ 296 test case trên Prototype Vercel
.\run_r4_automation.cmd protoall
```

```powershell
# Chạy riêng từng Suite tính năng trên Prototype (từ suite 1 đến suite 20):
.\run_r4_automation.cmd protosuite 1     # F4.1 Submit routing (TC-001 -> TC-009)
.\run_r4_automation.cmd protosuite 2     # F4.2 MOEFAS ranking & assessment (35 cases)
.\run_r4_automation.cmd protosuite 3     # F4.3 Applications list, MOE HQ
.\run_r4_automation.cmd protosuite 4     # F4.4 Applications list, School Admin
.\run_r4_automation.cmd protosuite 5     # F4.5 Filters and search (27 cases)
.\run_r4_automation.cmd protosuite 6     # F4.6 Export CSV
.\run_r4_automation.cmd protosuite 7     # F4.7 Review drawer, MOEFAS
.\run_r4_automation.cmd protosuite 8     # F4.8 Review drawer, SBFAS
.\run_r4_automation.cmd protosuite 9     # F4.9 Approve SBFAS
.\run_r4_automation.cmd protosuite 10    # F4.10 Reject SBFAS
.\run_r4_automation.cmd protosuite 11    # F4.11 One decision per application
.\run_r4_automation.cmd protosuite 12    # F4.12 Access and security
.\run_r4_automation.cmd protosuite 13    # F4.13 FAS schemes list
.\run_r4_automation.cmd protosuite 14    # F4.14 New scheme wizard (34 cases)
.\run_r4_automation.cmd protosuite 15    # F4.15 Review and publish (17 cases)
.\run_r4_automation.cmd protosuite 16    # F4.16 Add fee to a published scheme (11 cases)
.\run_r4_automation.cmd protosuite 17    # F4.17 Close form now (demo)
.\run_r4_automation.cmd protosuite 18    # F4.18 Effects after a decision
.\run_r4_automation.cmd protosuite 19    # F4.19 ML recommendation and risk (15 cases)
.\run_r4_automation.cmd protosuite 20    # F4.20 Formats
```

```powershell
# Chạy 1 test case cụ thể trên Prototype:
.\run_r4_automation.cmd prototc 001
.\run_r4_automation.cmd prototc 045
.\run_r4_automation.cmd prototc 168
```

---

### 4. Nhóm case đặc biệt của bộ thật

```powershell
.\run_r4_automation.cmd draft      # case chờ BA chốt vì UI thật khác sổ case
.\run_r4_automation.cmd defects    # case đã xác nhận lỗi qua code (xfail, hết lỗi thì thành xpass)
.\run_r4_automation.cmd cleanup    # dọn dữ liệu R4-AUTO sau khi chạy
# Thêm chữ headed vào cuối lệnh để xem trình duyệt chạy
.\run_r4_automation.cmd suite 14 headed
```

---

## 📁 Kết quả & Báo cáo sau khi chạy (Artifacts)

| Thư mục / Tập tin | Nội dung chi tiết |
|---|---|
| [`artifacts/allure-report/index.html`](artifacts/allure-report/index.html) | **Báo cáo Allure (Single-File)**: Đầy đủ Title, Severity, Steps, Expected Result và **video ~5s nhúng trực tiếp** trong từng case. |
| `artifacts/videos/` | Chứa các file video `.webm` (1280x720) thời lượng ~5-6s theo mã test case (`TC-901.webm`, `TC-001.webm`...) |
| `artifacts/reports/report.html` | Báo cáo HTML độc lập của Pytest |
| `artifacts/reports/junit.xml` | Báo cáo XML phục vụ tích hợp CI/CD |
| `artifacts/auth/` | Lưu phiên đăng nhập (`moehq.json`, bộ thật dùng lại cookie MOE HQ) để tái sử dụng cookie, tránh lỗi rate limit |

---

## 🛠️ Cấu trúc thư mục

```text
r4_automation/
├── run_r4_automation.cmd     # Script chạy tự động chính (Windows cmd / PowerShell)
├── pytest.ini                 # Cấu hình Pytest, base_url, markers
├── conftest.py                # Fixtures, điều tiết video ~5s, tự động đính kèm Allure
├── pages/                     # Page Object Models (Portal, Schemes, Applications, Dialogs)
├── data/
│   ├── cases.py               # Metadata đầy đủ của 273 test cases
│   └── ui_text.py             # Chuỗi văn bản giao diện cố định
├── tests/
│   ├── test_real_hosted_portal.py  # Test suite chạy trực tiếp trên UI thật localhost:5173
│   ├── test_00_smoke.py            # Smoke tests
│   └── test_f41_*.py -> test_f420_*.py # 20 suites kiểm thử chi tiết F4.1 -> F4.20
└── artifacts/                 # Thư mục chứa báo cáo Allure, video, xml
```
