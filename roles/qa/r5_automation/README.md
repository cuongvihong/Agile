# R5 Paper Applications (Upload Applications) UI Automation

Bộ kiểm thử tự động (End-to-End & Acceptance) cho **Function 5 (R5): Đơn giấy (Paper Applications - Upload Applications)** thuộc hệ thống EduFAMS Admin Portal.

Xây dựng theo chuẩn kiến trúc của bộ **R4 Automation** và **R9 Automation**:
- **Playwright + Pytest**
- **Allure Single-file Report** có đính kèm video WebM (~5s/case) và screenshot khi lỗi
- Hỗ trợ chạy trực tiếp trên **Localhost Admin Portal (`http://localhost:5173`)**
- Cover toàn bộ **261 test cases / 12 Test Suites** trong [R5_Test_Cases.xlsx](file:///d:/AIQA/Agileproject/roles/qa/R5_Test_Cases.xlsx)

---

## 1. Quick Start (Lệnh chạy nhanh trong PowerShell / CMD)

Mở PowerShell tại thư mục `roles\qa\r5_automation`:

```powershell
cd d:\AIQA\Agileproject\roles\qa\r5_automation
```

### A. Chạy Smoke Test (Kiểm tra nhanh đăng nhập School Admin & mở màn hình)
```powershell
.\run_r5_automation.cmd smoke
```

### B. Chạy bộ Test Real UI trên Localhost (`http://localhost:5173`)
```powershell
# Chạy 6 test case thực tế (TC-001 đến TC-006) có video ~5s và Allure report:
.\run_r5_automation.cmd real

# Chạy mở trình duyệt thấy màn hình (Headed mode):
.\run_r5_automation.cmd real headed
```

### C. Chạy theo từng Suite hoặc Test Case cụ thể
```powershell
# Chạy Suite F5.1 (Upload applications list):
.\run_r5_automation.cmd suite 1

# Chạy Suite F5.2 (Upload scans dialog):
.\run_r5_automation.cmd suite 2

# Chạy đích danh 1 Test Case (ví dụ TC-001):
.\run_r5_automation.cmd tc 001

# Chạy đích danh TC-005 (Kiểm tra upload file scan PDF):
.\run_r5_automation.cmd tc 005
```

### D. Chạy toàn bộ 261 Test Cases
```powershell
.\run_r5_automation.cmd full
```

### E. Mở Báo cáo Allure (Single-File Report có video nhúng)
```powershell
.\run_r5_automation.cmd allure
```
File báo cáo tạo tại: `artifacts\allure-report\index.html` và `artifacts\reports\report.html`.

---

## 2. Cấu trúc thư mục Framework

```
roles/qa/r5_automation/
│── artifacts/
│   ├── allure-report/     # Báo cáo Allure single-file (index.html)
│   ├── allure-results/    # Kết quả Allure thô (JSON, attachments)
│   ├── auth/              # Cookie phiên đăng nhập (school_state.json)
│   ├── reports/           # Báo cáo Pytest HTML (report.html, junit.xml)
│   └── videos/            # Video quay màn hình ~5s/case (<TC-ID>.webm)
│── data/
│   ├── __init__.py
│   ├── cases.py           # Metadata 261 test cases sinh từ R5_Test_Cases.xlsx
│   └── seed.py            # Fixtures người dùng, học sinh mẫu SEED-R5
│── docs/                  # Tài liệu hướng dẫn chi tiết
│── pages/
│   ├── __init__.py
│   ├── base_page.py       # Page Object nền tảng (common waits, helpers)
│   ├── portal.py          # Quản lý đăng nhập School Admin & navigation
│   └── paper_applications_page.py # Page Object chức năng Đơn giấy F5
│── tests/
│   ├── test_00_smoke.py   # Smoke test
│   ├── test_real_hosted_portal.py # 6 Live tests chạy thật trên localhost:5173
│   ├── test_f51_upload_applications_list.py   # Suite F5.1 (TC-001..TC-035)
│   ├── test_f52_upload_scans_dialog.py        # Suite F5.2 (TC-036..TC-067)
│   ├── test_f53_review_part1_applicant.py     # Suite F5.3 (TC-068..TC-101)
│   ├── test_f54_review_part2_children.py      # Suite F5.4 (TC-102..TC-114)
│   ├── test_f55_review_part3_family.py        # Suite F5.5 (TC-115..TC-140)
│   ├── test_f56_review_part4_part5.py         # Suite F5.6 (TC-141..TC-161)
│   ├── test_f57_drafts.py                     # Suite F5.7 (TC-162..TC-175)
│   ├── test_f58_validation_rules.py           # Suite F5.8 (TC-176..TC-201)
│   ├── test_f59_review_before_submit.py       # Suite F5.9 (TC-202..TC-209)
│   ├── test_f510_routing_and_submit.py        # Suite F5.10 (TC-210..TC-233)
│   ├── test_f511_view_edit_submitted.py       # Suite F5.11 (TC-234..TC-250)
│   └── test_f512_access_and_security.py       # Suite F5.12 (TC-251..TC-261)
│── tools/
│   ├── build_cases.py     # Parser đọc R5_Test_Cases.xlsx -> data/cases.py
│   └── build_suite_tests.py # Bộ sinh mã test functions tự động
│── conftest.py            # Playwright fixtures, video pacing ~5s, Allure hooks
│── pytest.ini             # Cấu hình Pytest, base_url, markers, addopts
│── requirements.txt       # Danh sách thư viện Python
│── run_r5_automation.cmd  # Script chạy 1-click tiêu chuẩn
└── README.md              # Tài liệu này
```

---

## 3. Danh sách 12 Phân hệ (Suites)

| Suite | Tên phân hệ | Số lượng case | Dải mã test case |
| :---: | :--- | :---: | :---: |
| **F5.1** | Upload applications list | 35 | `TC-001` .. `TC-035` |
| **F5.2** | Upload scans dialog | 32 | `TC-036` .. `TC-067` |
| **F5.3** | Review application, Part 1 Applicant | 34 | `TC-068` .. `TC-101` |
| **F5.4** | Review application, Part 2 Children | 13 | `TC-102` .. `TC-114` |
| **F5.5** | Review application, Part 3 Family and household | 26 | `TC-115` .. `TC-140` |
| **F5.6** | Review application, Part 4 Context & Part 5 Declaration | 21 | `TC-141` .. `TC-161` |
| **F5.7** | Drafts (Bản nháp) | 14 | `TC-162` .. `TC-175` |
| **F5.8** | Review and submit validation | 26 | `TC-176` .. `TC-201` |
| **F5.9** | Review before submitting dialog | 8 | `TC-202` .. `TC-209` |
| **F5.10** | Confirm and submit and routing | 24 | `TC-210` .. `TC-233` |
| **F5.11** | View and edit submitted application | 17 | `TC-234` .. `TC-250` |
| **F5.12** | Access, API and data | 11 | `TC-251` .. `TC-261` |
| **Tổng cộng** | **12 Suites** | **261 Test Cases** | `TC-001` .. `TC-261` |
