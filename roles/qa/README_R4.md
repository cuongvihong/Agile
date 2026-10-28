# HƯỚNG DẪN CHẠY R4 AUTOMATION (QUICK START COMMANDS)

Thư mục thực thi: `d:\AIQA\Agileproject\roles\qa\r4_automation`

> **Lưu ý khi mở PowerShell**:
> Di chuyển vào thư mục automation trước khi chạy:
> ```powershell
> cd d:\AIQA\Agileproject\roles\qa\r4_automation
> ```
> Luôn gõ tiền tố `.\` trước script: `.\run_r4_automation.cmd ...`

---

## 1. Chạy trên UI thật đang host (`http://localhost:5173`)

```powershell
# Chạy bộ test trên UI thật (6 cases giao diện localhost:5173)
.\run_r4_automation.cmd real
```

```powershell
# Chạy UI thật và mở trình duyệt Chrome để xem trực tiếp thao tác
.\run_r4_automation.cmd real headed
```

```powershell
# Chạy riêng từng test case trên UI thật:
.\run_r4_automation.cmd tc 901    # TC-901: MOE HQ Login & Dashboard
.\run_r4_automation.cmd tc 902    # TC-902: MOE HQ Quản lý Schemes MOEFAS
.\run_r4_automation.cmd tc 903    # TC-903: MOE HQ Wizard tạo Scheme 4 bước
.\run_r4_automation.cmd tc 904    # TC-904: School User Login & Dashboard
.\run_r4_automation.cmd tc 905    # TC-905: School Xem danh sách đơn FAS & Filter
.\run_r4_automation.cmd tc 906    # TC-906: School Xem danh sách SBFAS Schemes
```

---

## 2. Mở Báo cáo Allure (Có nhúng sẵn Video ~5s)

```powershell
# Mở báo cáo Allure (single-file HTML)
.\run_r4_automation.cmd allure
```
*(Hoặc mở trực tiếp file `artifacts\allure-report\index.html` trong thư mục `r4_automation`).*

---

## 3. Chạy trên Prototype Vercel (`https://edusave.vercel.app`)

```powershell
# Chạy toàn bộ 296 test case trên Prototype
.\run_r4_automation.cmd proto
```

```powershell
# Chạy riêng từng Suite tính năng trên Prototype (suite 1 đến suite 20):
.\run_r4_automation.cmd suite 1     # F4.1 Submit routing (TC-001 -> TC-009)
.\run_r4_automation.cmd suite 2     # F4.2 MOEFAS ranking & assessment (35 cases)
.\run_r4_automation.cmd suite 5     # F4.5 Filters and search (27 cases)
.\run_r4_automation.cmd suite 13    # F4.13 FAS schemes list (15 cases)
.\run_r4_automation.cmd suite 14    # F4.14 New scheme wizard (34 cases)
.\run_r4_automation.cmd suite 16    # F4.16 Add fee to a published scheme (11 cases)
```

```powershell
# Chạy 1 test case cụ thể trên Prototype:
.\run_r4_automation.cmd tc 001
.\run_r4_automation.cmd tc 045
.\run_r4_automation.cmd tc 168
```

---

## 4. Chạy các nhóm trường hợp đặc biệt

```powershell
# Chạy các case phụ thuộc giả định BA (draft)
.\run_r4_automation.cmd draft

# Chạy các case kiểm tra lỗi prototype (known defects)
.\run_r4_automation.cmd defects

# Thêm 'headed' để xem trình duyệt chạy trực tiếp:
.\run_r4_automation.cmd suite 1 headed
.\run_r4_automation.cmd tc 001 headed
```
