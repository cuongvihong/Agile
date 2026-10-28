"""Smoke FS09: hai địa chỉ của hệ thống (e-service và admin portal) chạy, đăng nhập và ba bước thanh toán mở được.
Không bấm Authorize & pay, không đăng nhập admin, không ghi dữ liệu."""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from data import ui_text as T
from pages.admin_page import AdminLoginPage
from pages.catalog import live_smallest, need

pytestmark = pytest.mark.smoke


def test_smoke_sign_in_reaches_child_list(accounts):
    accounts.open()
    expect(accounts.heading).to_be_visible()


def test_smoke_child_list_has_at_least_one_child(accounts):
    accounts.open()
    assert accounts.read_cards(), "Danh sách con rỗng: phụ huynh này chưa liên kết với học sinh nào (kiểm tra R9_NRIC và dữ liệu mẫu)"


def test_smoke_child_page_shows_wallet_and_charges(billing, catalog):
    assert catalog.usable(), f"Không có học sinh nào tải được ví/tài khoản giáo dục! Catalog: {catalog.describe()}"
    child = catalog.usable()[0]
    billing.open(child.student_id)
    expect(billing.card(T.CARD_BALANCE)).to_be_visible()
    expect(billing.card(T.CARD_OUTSTANDING)).to_be_visible()


def test_smoke_payment_method_step_opens(billing, catalog):
    assert catalog.with_charges(), f"Không có học sinh nào có khoản phí chưa thanh toán! Catalog: {catalog.describe()}"
    child = catalog.with_charges()[0]
    (charge,), _ = live_smallest(billing, child)
    billing.select([charge.description]).to_method()
    expect(billing.page.get_by_role("radio").first).to_be_visible()


def test_smoke_review_step_opens_without_paying(billing, catalog, requests_log):
    assert catalog.with_charges(), f"Không có học sinh nào có khoản phí chưa thanh toán! Catalog: {catalog.describe()}"
    child = catalog.with_charges()[0]
    (charge,), _ = live_smallest(billing, child)
    billing.start([charge.description])
    expect(billing.authorize_button).to_be_visible()
    assert not requests_log.posts("/checkout"), "Smoke không được tạo giao dịch"


@pytest.mark.online
def test_smoke_payment_simulator_is_reachable(page):
    """Test online tự bỏ qua nếu simulator chưa chạy (fixture simulator_up)."""
    from data import seed
    response = page.request.get(seed.CHECKOUT_URL)
    assert response.ok, f"Simulator trả mã {response.status}"


@pytest.mark.admin
def test_smoke_admin_portal_login_page_is_reachable(anon_page, admin_url):
    """Admin portal (R9_ADMIN_URL, mặc định cổng 5173) mở được và hiện form đăng nhập. Không nhập tài khoản.
    Dùng trình duyệt chưa đăng nhập vì cookie localhost không phân biệt cổng."""
    login = AdminLoginPage(anon_page, admin_url).open()
    assert "Admin Portal" in login.title(), login.title()
    expect(login.username).to_be_visible()
    expect(login.password).to_be_visible()
    expect(login.sign_in_button).to_be_visible()


@pytest.mark.admin
def test_smoke_admin_portal_sends_a_visitor_without_session_to_sign_in(anon_page, admin_url):
    """Mở gốc admin portal khi chưa đăng nhập thì được đưa về /login."""
    anon_page.goto(admin_url)
    expect(anon_page).to_have_url(re.compile(r"/login"), timeout=20_000)
    expect(AdminLoginPage(anon_page, admin_url).heading).to_be_visible()


def test_smoke_the_two_portals_are_different_origins(base_url, admin_url):
    """Hai địa chỉ phải khác nhau. Nếu R9_BASE_URL và R9_ADMIN_URL trỏ cùng một chỗ thì cấu hình bị đặt nhầm."""
    assert base_url.rstrip("/") != admin_url.rstrip("/"), f"R9_BASE_URL và R9_ADMIN_URL cùng là {base_url}"
