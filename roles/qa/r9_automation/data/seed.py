"""Cấu hình môi trường và dữ liệu mẫu của FS09. Mọi giá trị đổi được bằng biến môi trường.

CHỈ CHẠY TRÊN LOCALHOST. Bộ test này chạy trên hệ thống anh đang host ở máy mình (e-service, admin portal, simulator, webhook,
SQL Server trong Docker). Mọi địa chỉ phải là localhost, 127.0.0.1, [::1] hoặc tên có đuôi .localhost; địa chỉ khác (đặc biệt
*.vercel.app) làm pytest dừng ngay từ đầu, trước khi mở trình duyệt (xem assert_local ở cuối file). Chỉ máy khác trong mạng riêng
(ví dụ IP Radmin) mới được mở bằng R9_ALLOW_REMOTE=1; vercel.app thì không mở được bằng cách nào.

Hai địa chỉ của hệ thống đang kiểm thử:
  e-service     R9_BASE_URL   mặc định http://localhost:5174  (cổng phụ huynh, nơi chạy mọi test thanh toán)
  admin portal  R9_ADMIN_URL  mặc định http://localhost:5173  (cổng quản trị, hiện chỉ kiểm tra mở được và đòi đăng nhập)

Sổ case bản 187 case viết theo bộ seed R9 mới (R9_Seed_Data.xlsx: S01 đến S25, X01 đến X05, tên như Nur Aisyah, Ethan Chua), còn phần mô tả dưới đây là các lần quét cũ trên persona S7890123F.
Dữ liệu mẫu khác nhau giữa các lần nạp. Lần quét trên bản chạy local ngày 21/10/2026 (persona MockPass S7890123F):
Test Child One (10 khoản, tổng 805.00, ví 300.00), Test Child Two (5 khoản, 1390.00, ví 300.00),
Test Child Three (5 khoản, 470.00, ví 300.00) và Tan Wei Ming (không có khoản phí, ví 0.00).
Bản nạp cũ theo Function9FullFlowSetup.sql có Noah Lee và Ryan Hassan, ví 1000.00. Suite không gắn cứng tên con:
nó đọc danh sách con trên UI rồi tự chọn con phù hợp (xem pages/catalog.py).
"""
from __future__ import annotations

import os
from urllib.parse import urlparse

BASE_URL = os.environ.get("R9_BASE_URL", "http://localhost:5174")
# Cổng quản trị (apps/admin-portal). Chưa có test R9 nào thao tác trong đó: đăng nhập cần tài khoản thật của QA, không có trong repo.
ADMIN_URL = os.environ.get("R9_ADMIN_URL", "http://localhost:5173").rstrip("/")
# Persona MockPass, không phải mật khẩu. Đổi bằng R9_NRIC nếu máy anh map con sang persona khác.
NRIC = os.environ.get("R9_NRIC", "S7890123F")
# Trang thanh toán giả lập (npm run dev:payment-checkout). Chỉ cần cho test có nhãn online.
CHECKOUT_URL = os.environ.get("R9_CHECKOUT_URL", "http://localhost:5176")
# Danh sách con mong đợi, ngăn cách bằng dấu phẩy. Để trống thì bỏ qua TC-006.
EXPECTED_CHILDREN = [x.strip() for x in os.environ.get("R9_EXPECTED_CHILDREN", "").split(",") if x.strip()]
# Cho phép test ghi dữ liệu thật. Runner đặt biến này sau khi anh gõ xác nhận.
ALLOW_PAYMENTS = os.environ.get("R9_ALLOW_PAYMENTS") == "1"
# Cho phép test rút cạn ví của một con (thanh toán chia khoản Both). Cần thêm bước reset dữ liệu giữa các lần chạy.
ALLOW_DESTRUCTIVE = os.environ.get("R9_ALLOW_DESTRUCTIVE") == "1"

TRANSACTION_STORAGE_KEY = "edusave.billingPayment.transactionId"
API_PREFIX = "/api"

# GUID hợp lệ về định dạng nhưng không thuộc về ai, dùng cho test truy cập trái phép.
UNKNOWN_ID = "00000000-0000-4000-8000-000000000001"
UNKNOWN_ID_2 = "00000000-0000-4000-8000-000000000002"


# ------------------------------------------------------------------ chỉ cho chạy trên localhost
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", "[::1]"}
FORBIDDEN_SUFFIXES = (".vercel.app", ".vercel.sh", ".now.sh")
ALLOW_REMOTE = os.environ.get("R9_ALLOW_REMOTE") == "1"


def is_local(url: str) -> bool:
    host = (urlparse(url if "://" in url else f"http://{url}").hostname or "").lower()
    return (
        host in LOCAL_HOSTS
        or host.endswith(".localhost")
        or host.endswith(".devtunnels.ms")
        or "devtunnels" in host
        or "pinggy" in host
    )


def assert_local(name: str, url: str | None) -> None:
    """Dừng cả phiên chạy nếu địa chỉ không phải localhost. vercel.app bị chặn tuyệt đối, host khác cần R9_ALLOW_REMOTE=1."""
    if not url:
        return
    host = (urlparse(url if "://" in url else f"http://{url}").hostname or "").lower()
    if host.endswith(FORBIDDEN_SUFFIXES):
        raise RuntimeError(f"{name}={url!r} là địa chỉ Vercel. Bộ test R9 chỉ chạy trên localhost, không chạy trên Vercel.")
    if not is_local(url) and not ALLOW_REMOTE:
        raise RuntimeError(f"{name}={url!r} không phải localhost. Bộ test R9 chỉ chạy trên máy đang host hệ thống "
                           f"(localhost, 127.0.0.1, [::1]). Máy khác trong mạng riêng: đặt R9_ALLOW_REMOTE=1.")


def assert_all_local(extra: dict[str, str | None] | None = None) -> None:
    targets = {"R9_BASE_URL": BASE_URL, "R9_ADMIN_URL": ADMIN_URL, "R9_CHECKOUT_URL": CHECKOUT_URL}
    targets.update(extra or {})
    for name, url in targets.items():
        assert_local(name, url)
