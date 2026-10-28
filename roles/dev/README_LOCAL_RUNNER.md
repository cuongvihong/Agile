# BỘ KHUNG MÔI TRƯỜNG & KHỞI ĐỘNG LOCALHOST (EDUFAMS LOCAL ENVIRONMENT HUB)

Bộ công cụ tiêu chuẩn giúp bạn quản lý, khởi động, kiểm tra sức khỏe và **gắn code mới vào là host được ngay** trên máy local.

Thư mục: `d:\AIQA\Agileproject\roles\dev\`

---

## ⚡ CÁC LỆNH SỬ DỤNG NHANH (POWERSHELL / CMD)

Mở PowerShell tại thư mục `d:\AIQA\Agileproject\roles\dev`:

### 1. Khởi động Localhost (1-Click Run)
```powershell
# Tự động bật Docker (SQL Server, RabbitMQ, Redis) + Backend Microservices + Frontends
.\start-localhost.cmd
```
*Tất cả service sẽ được tự động khởi động và lưu log vào thư mục `report/`.*

---

### 2. Kiểm tra sức khỏe hệ thống (Health Check)
```powershell
# Quét toàn bộ các port và hiển thị trạng thái [ONLINE] / [OFFLINE]
.\health-check.cmd
```
*Kiểm tra ngay xem cổng 5173 (Admin Portal), 5174 (e-Service), 5273 (Gateway), 1433 (SQL)... đã chạy ổn định chưa.*

---

### 3. Tắt sạch các Service đang chạy ngầm (Stop Localhost)
```powershell
# Giải phóng các port 5173, 5174, 5273, 5290, 5001-5008 (tránh lỗi đụng port)
.\stop-localhost.cmd
```

---

### 4. Gắn bộ Code mới và Host ngay (Switch Code Sprint)
Khi Dev gửi cho bạn một thư mục code mới (ví dụ `codesprint3` hoặc `sprint3_fix`), bạn chỉ cần:

**Cách 1: Dùng lệnh tự động (Khuyên dùng)**
```powershell
# Cú pháp: .\switch-code.cmd <tên_thư_mục_code_mới>
.\switch-code.cmd codesprint3
```
*Lệnh này sẽ tự động: lưu cấu hình code mới -> cài dependencies nếu cần -> tắt service cũ -> khởi động toàn bộ hệ thống trên code mới!*

**Cách 2: Đổi thủ công trong file cấu hình**
- Mở file [`active_code.txt`](active_code.txt) và gõ tên thư mục code mới (ví dụ: `codesprint3`).
- Chạy lại lệnh:
  ```powershell
  .\start-localhost.cmd
  ```

---

## 🌐 Danh sách các URL dịch vụ khi Host

| Dịch vụ | Địa chỉ URL | Ghi chú |
|---|---|---|
| **Admin Portal** | [`http://localhost:5173`](http://localhost:5173) | Đăng nhập: `moehq` / `123456` hoặc `school` / `123456` |
| **Parent e-Service** | [`http://localhost:5174`](http://localhost:5174) | Dành cho phụ huynh nộp đơn FAS / tài khoản học sinh |
| **API Gateway Swagger** | [`http://localhost:5273/swagger`](http://localhost:5273/swagger) | Tra cứu và test trực tiếp các API của hệ thống |
| **RabbitMQ Management** | [`http://localhost:15672`](http://localhost:15672) | Tài khoản mặc định: `guest` / `guest` |
| **MockPass (Singpass giả lập)** | [`http://localhost:5001`](http://localhost:5001) | Giả lập xác thực Singpass cho phụ huynh |

---

## 📁 Cấu trúc bộ khung

```text
roles/dev/
├── active_code.txt          # File cấu hình tên thư mục code đang được chọn chạy
├── start-localhost.cmd      # Script khởi động toàn bộ hệ thống (Docker + BE + FE)
├── stop-localhost.cmd       # Script tắt sạch tiến trình và giải phóng port
├── health-check.cmd         # Script kiểm tra trạng thái các port (xanh/đỏ)
├── health-check.ps1         # Logic kiểm tra TCP socket
├── switch-code.cmd          # Script chuyển sang sprint code mới và host ngay
├── README_LOCAL_RUNNER.md   # Hướng dẫn chi tiết này
└── codesprint2ending/       # Thư mục code sprint hiện tại
```
