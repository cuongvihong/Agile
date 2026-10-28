"""Fixtures của bộ automation FS09 (Fees & Payments) trên e-service thật.

Khác với r4_automation (prototype tự chứa dữ liệu trong trình duyệt), ở đây dữ liệu nằm trong backend thật,
nên suite đọc dữ liệu hiện có (Catalog) và chia test theo nhãn loại:
  readonly  chỉ đọc, chạy lại được (mặc định)
  mocked    giả một phản hồi bằng page.route, dữ liệu thật không đổi
  api       gửi yêu cầu API mong đợi bị từ chối
  mutating  ghi dữ liệu thật, chỉ chạy khi R9_ALLOW_PAYMENTS=1
  online    cần simulator thanh toán cổng 5176
  admin     chỉ chạm trang đăng nhập của admin portal (cổng 5173), không đăng nhập
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import APIRequestContext, APIResponse, Page

from allure_support import VIDEO_ARGS
from data import seed
from pages.accounts_page import AccountsPage
from pages.base_page import snippet  # noqa: F401
from pages.billing_page import BillingPage
from pages.catalog import Catalog, build_catalog, need  # noqa: F401  need được test import từ đây cho gọn
from pages.portal import Portal
from pages.result_page import ResultPage
from pages.simulator_page import SimulatorPage

ROOT = Path(__file__).resolve().parent
pytest_plugins = ("reporting", "allure_support")  # reporting: r9_case_report.html/.csv; allure_support: Allure + video từng case (như r4_automation)

AUTH_DIR = ROOT / "artifacts" / "auth"
CONTEXT_ARGS = {"viewport": {"width": 1440, "height": 900}, "locale": "en-SG",
                "timezone_id": "Asia/Singapore", "accept_downloads": True}
KIND_MARKERS = ("readonly", "mocked", "api", "mutating", "online", "admin")


# ------------------------------------------------------------------ chỉ cho chạy trên localhost
def pytest_configure(config):
    """Chặn mọi địa chỉ không phải localhost (nhất là *.vercel.app) trước khi pytest mở trình duyệt hay gửi yêu cầu nào."""
    try:
        seed.assert_all_local({"--base-url": config.getoption("base_url", default=None) or config.getini("base_url")})
    except RuntimeError as err:
        raise pytest.UsageError(str(err)) from err


# ------------------------------------------------------------------ gán nhãn
def pytest_itemcollected(item):
    """Test không có nhãn loại là readonly. Test online tự đòi fixture simulator_up."""
    if not any(item.get_closest_marker(name) for name in KIND_MARKERS):
        item.add_marker(pytest.mark.readonly)
    if item.get_closest_marker("online"):
        item.add_marker(pytest.mark.usefixtures("simulator_up"))


def pytest_collection_modifyitems(items):
    for item in items:
        marker = item.get_closest_marker("known_defect")
        if marker is not None:
            reason = marker.kwargs.get("reason") or (marker.args[0] if marker.args else "known defect")
            item.add_marker(pytest.mark.xfail(reason=reason, strict=False))
        if item.get_closest_marker("mutating") and not seed.ALLOW_PAYMENTS:
            item.add_marker(pytest.mark.skip(
                reason="Test ghi dữ liệu thật (tiêu khoản phí, trừ tiền ví). Chạy bằng run_r9_automation.cmd pay"))
        if item.get_closest_marker("destructive") and not seed.ALLOW_DESTRUCTIVE:
            item.add_marker(pytest.mark.skip(
                reason="Test rút cạn ví của một con (thanh toán chia khoản). Chạy bằng run_r9_automation.cmd destructive rồi reset dữ liệu"))


# ------------------------------------------------------------------ cấu hình
@pytest.fixture(autouse=True)
def _reseed_each(request):
    """Đặt R9_RESEED_EACH=1 (hoặc thêm chữ each khi chạy run_r9_automation.cmd) để nạp lại seed R9 trước MỖI test ghi dữ liệu,
    nên không test nào phụ thuộc vào dữ liệu mà test trước đã tiêu. Mỗi lần nạp lại mất vài chục giây."""
    if os.environ.get("R9_RESEED_EACH") != "1":
        return
    if not (request.node.get_closest_marker("mutating") or request.node.get_closest_marker("destructive")):
        return
    from pages import db
    ok, note = db.reseed()
    if not ok:
        pytest.skip(f"Không nạp lại được seed R9 trước test này ({note})")


@pytest.fixture(scope="session")
def admin_url() -> str:
    """Địa chỉ admin portal. R9_ADMIN_URL ghi đè mặc định http://localhost:5173."""
    return seed.ADMIN_URL


@pytest.fixture(scope="session")
def base_url(base_url):
    """R9_BASE_URL ghi đè --base-url và base_url của pytest.ini."""
    url = (os.environ.get("R9_BASE_URL") or base_url or seed.BASE_URL).rstrip("/")
    seed.assert_local("base_url", url)
    return url


# e-service giữ phụ huynh đăng nhập ở HAI nơi: cookie IAM_Session (playwright lưu được) và sessionStorage
# "edusave.parent-auth.user" (playwright KHÔNG lưu trong storage_state). Thiếu mục thứ hai thì route guard
# đẩy về /parent/login dù cookie còn, nên mọi test dùng lại phiên bị rơi về trang đăng nhập (lần chạy 21/10/2026).
USER_STORAGE_KEY = "edusave.parent-auth.user"
SEEDED_FLAG = "r9.session-seeded"


def _user_file(auth_state_path: str) -> Path:
    return Path(auth_state_path).with_suffix(".user.json")


def seed_parent_session(context, auth_state_path: str, base_url: str) -> None:
    """Chép người dùng đã đăng nhập vào sessionStorage của mỗi tab mới (chỉ một lần mỗi tab).
    Cờ SEEDED_FLAG giữ để test đăng xuất hoặc xóa phiên không bị chép lại sau khi tải lại trang."""
    file = _user_file(auth_state_path)
    if not file.exists():
        return
    user_json = file.read_text(encoding="utf-8")
    script = (
        "(() => { try {"
        f" if (location.origin !== {json.dumps(base_url)}) return;"
        f" if (sessionStorage.getItem({json.dumps(SEEDED_FLAG)})) return;"
        f" sessionStorage.setItem({json.dumps(SEEDED_FLAG)}, '1');"
        f" if (!sessionStorage.getItem({json.dumps(USER_STORAGE_KEY)}))"
        f"   sessionStorage.setItem({json.dumps(USER_STORAGE_KEY)}, {json.dumps(user_json)});"
        f" const u = JSON.parse({json.dumps(user_json)});"
        f" if (u && u.id) localStorage.setItem('edusave.e-service-tour-choice-v1:' + encodeURIComponent(u.id), 'done');"
        " } catch (e) {} })();"
    )
    context.add_init_script(script)


@pytest.fixture(scope="session")
def auth_state(browser, base_url) -> str:
    """Đăng nhập Singpass (MockPass) một lần mỗi phiên chạy, lưu cookie và người dùng để mọi test dùng lại."""
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    path = AUTH_DIR / f"parent_{seed.NRIC}.json"
    context = browser.new_context(**CONTEXT_ARGS)
    page = context.new_page()
    page.set_default_timeout(20_000)
    try:
        Portal(page, base_url, seed.NRIC).sign_in()
        context.storage_state(path=str(path))
        user = page.evaluate("key => sessionStorage.getItem(key)", USER_STORAGE_KEY)
        assert user, ("Đăng nhập xong nhưng sessionStorage không có " + USER_STORAGE_KEY
                      + ". Giao diện đổi cách giữ phiên, cần sửa seed_parent_session trong conftest.py")
        _user_file(str(path)).write_text(user, encoding="utf-8")
    finally:
        context.close()
    return str(path)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, auth_state):
    return {**browser_context_args, **CONTEXT_ARGS, **VIDEO_ARGS, "storage_state": auth_state}


_PW_FIXTURES = {"page", "context", "accounts", "billing", "result", "simulator", "api", "requests_log"}


@pytest.fixture(autouse=True)
def _default_timeout(request):
    if not (_PW_FIXTURES & set(request.fixturenames)):
        return
    context = request.getfixturevalue("context")
    auth_state = request.getfixturevalue("auth_state")
    base_url = request.getfixturevalue("base_url")
    context.set_default_timeout(15_000)
    context.set_default_navigation_timeout(45_000)
    seed_parent_session(context, auth_state, base_url)


# ------------------------------------------------------------------ trang và dữ liệu
@pytest.fixture
def anon_page(browser, base_url) -> Page:
    """Trình duyệt chưa đăng nhập."""
    context = browser.new_context(**CONTEXT_ARGS, **VIDEO_ARGS)
    context.set_default_timeout(20_000)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="session")
def catalog(browser, base_url, auth_state) -> Catalog:
    """Số liệu thật của từng con, đọc một lần trước mọi test ghi dữ liệu."""
    context = browser.new_context(**CONTEXT_ARGS, storage_state=auth_state)
    context.set_default_timeout(20_000)
    seed_parent_session(context, auth_state, base_url)
    page = context.new_page()
    try:
        return build_catalog(page, base_url)
    finally:
        context.close()


@pytest.fixture
def accounts(page, base_url) -> AccountsPage:
    return AccountsPage(page, base_url)


@pytest.fixture
def billing(page, base_url) -> BillingPage:
    return BillingPage(page, base_url)


@pytest.fixture
def result(page, base_url) -> ResultPage:
    return ResultPage(page, base_url)


@pytest.fixture
def simulator(page, base_url) -> SimulatorPage:
    return SimulatorPage(page, base_url)


@pytest.fixture(scope="session")
def simulator_up():
    """Bỏ qua test online nếu trang giả lập thanh toán chưa chạy (npm run dev:payment-checkout)."""
    try:
        urllib.request.urlopen(seed.CHECKOUT_URL, timeout=4)
    except Exception as err:  # noqa: BLE001
        pytest.skip(f"Simulator thanh toán không truy cập được tại {seed.CHECKOUT_URL}: {err}")


# ------------------------------------------------------------------ ghi nhận request và API
class RequestLog:
    """Ghi lại request của một trang để kiểm tra 'không có giao dịch nào được tạo'."""

    def __init__(self, page: Page):
        self.items: list[tuple[str, str]] = []
        page.on("request", lambda r: self.items.append((r.method, r.url)))

    def posts(self, fragment: str) -> list[str]:
        return [url for method, url in self.items if method == "POST" and fragment in url]

    def count(self, fragment: str, method: str = "GET") -> int:
        return len([1 for m, u in self.items if m == method and fragment in u])


@pytest.fixture
def requests_log(page) -> RequestLog:
    return RequestLog(page)


class Api:
    """Gọi API qua cùng origin của e-service (Vite proxy /api sang gateway), dùng cookie phiên của trang."""

    def __init__(self, request: APIRequestContext, base_url: str):
        self.request = request
        self.base = f"{base_url}{seed.API_PREFIX}"

    def get(self, path: str) -> APIResponse:
        return self.request.get(f"{self.base}{path}")

    def post(self, path: str, body: dict, key: str | None = "") -> APIResponse:
        """key=None gửi không có header Idempotency-Key, chuỗi rỗng cũng gửi header rỗng."""
        headers = {"Content-Type": "application/json"}
        if key is not None:
            headers["Idempotency-Key"] = key
        return self.request.post(f"{self.base}{path}", data=json.dumps(body), headers=headers)


@pytest.fixture
def api(page, base_url) -> Api:
    return Api(page.request, base_url)


@pytest.fixture
def anon_api(playwright, base_url):
    """API không có cookie phiên."""
    request = playwright.request.new_context(base_url=base_url)
    yield Api(request, base_url)
    request.dispose()


def pytest_report_header(config):
    """Ghi tên DB thật mà test đang dùng và kiểu cột id để nhìn một dòng là biết có đang ghi nhầm DB hay không."""
    try:
        from pages import db
        b, e = db._real_db(db.BILLING_DB), db._real_db(db.EA_DB)
        typ = db.sql_scalar("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'student_charges' AND COLUMN_NAME = 'student_id'", db=db.BILLING_DB)
        seeded = db.sql_scalar("SELECT COUNT(*) FROM dbo.student_charges WHERE id LIKE 'R9-CHG-%'", db=db.BILLING_DB)
        return f"R9 DB: billing={b} (student_id {typ}, khoản phí R9 seed: {seeded}), education account={e}"
    except Exception as exc:  # không có docker hoặc SQL Server thì chỉ bỏ dòng này
        return f"R9 DB: không đọc được ({str(exc)[:80]})"
