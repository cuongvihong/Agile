"""BasePage và các hàm đọc chữ, đọc tiền dùng chung cho mọi Page Object.

Thứ tự định vị: role, label, text, rồi mới tới CSS ngắn. UI e-service dùng thư viện @edusave/ui
nên hầu hết điều khiển có role và tên truy cập được (xem Developer_Guide_Accessible_UI_for_Playwright.docx).
"""
from __future__ import annotations

import re
from decimal import Decimal
from pathlib import Path

from playwright.sync_api import Locator, Page

# Intl.NumberFormat có thể ra "$1,000.00" hoặc "SGD 1,000.00" tùy ngôn ngữ của app.
MONEY_RE = re.compile(r"(?:S\$|SGD|\$)\s*(-?[\d,]+(?:\.\d+)?)")
GUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)


def norm(text: str) -> str:
    """Gộp mọi khoảng trắng thành một dấu cách và cắt hai đầu."""
    return re.sub(r"\s+", " ", text or "").strip()


def money(text: str) -> Decimal | None:
    """Số tiền đầu tiên trong chuỗi, hoặc None nếu không có."""
    match = MONEY_RE.search(text or "")
    return Decimal(match.group(1).replace(",", "")) if match else None


def all_money(text: str) -> list[str]:
    """Mọi cụm tiền trong chuỗi, giữ nguyên chữ để kiểm định dạng."""
    return [m.group(0) for m in MONEY_RE.finditer(text or "")]


def two_decimals(token: str) -> bool:
    """Cụm tiền có đúng hai chữ số thập phân và dấu phẩy ngăn nghìn đúng chỗ."""
    match = MONEY_RE.search(token or "")
    return bool(match and re.fullmatch(r"-?(\d{1,3}(,\d{3})+|\d+)\.\d{2}", match.group(1)))


def read_dl(scope: Locator) -> list[tuple[str, str]]:
    """Mọi cặp (dt, dd) trong phạm vi, theo thứ tự xuất hiện."""
    pairs = scope.locator("dl > div").evaluate_all(
        "els => els.map(e => [(e.querySelector('dt')||{}).innerText||'', (e.querySelector('dd')||{}).innerText||''])")
    return [(norm(a), norm(b)) for a, b in pairs]


def dl_value(pairs: list[tuple[str, str]], label: str) -> str | None:
    """Giá trị của cặp đầu tiên có nhãn khớp chính xác (không phân biệt hoa thường)."""
    for key, value in pairs:
        if key.lower() == label.lower():
            return value
    return None


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def screenshot(self, path: str, full_page: bool = True) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=path, full_page=full_page)

    def content(self) -> Locator:
        """Vùng nội dung chính: thẻ main nếu trang có, nếu không thì cả body."""
        main = self.page.locator("main")
        return main.first if main.count() else self.page.locator("body")

    def main_text(self) -> str:
        return norm(self.content().inner_text())


def soft(*checks) -> list[str]:
    """Chạy nhiều kiểm tra độc lập và gom lỗi thay vì dừng ở lỗi đầu. Dùng: assert not soft(lambda: ..., lambda: ...)."""
    failures: list[str] = []
    for check in checks:
        try:
            check()
        except AssertionError as err:
            text = str(err).strip()
            failures.append(text.splitlines()[0] if text else "check failed")
    return failures


def wait_until(page: Page, predicate, timeout: float = 10.0, interval: float = 0.25, what: str = "điều kiện") -> None:
    """Chờ predicate() thành True. Python Playwright chưa có expect.poll nên tự lặp.

    Phải chờ bằng page.wait_for_timeout, không dùng time.sleep, vì bộ xử lý page.route và page.on chỉ chạy
    khi Playwright được phép xử lý sự kiện.
    """
    import time
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return
        page.wait_for_timeout(int(interval * 1000))
    raise AssertionError(f"Hết {timeout:.0f} giây mà {what} chưa xảy ra")


def snippet(response, limit: int = 240) -> str:
    """Đoạn đầu của thân phản hồi API, dùng trong thông báo assert. Không in header hay cookie."""
    try:
        return re.sub(r"\s+", " ", response.text())[:limit]
    except Exception:  # noqa: BLE001
        return "<không đọc được thân phản hồi>"
