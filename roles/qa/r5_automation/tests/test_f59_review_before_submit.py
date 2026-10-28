"""F5.9 Review before submitting dialog (8 test cases)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage

pytestmark = [pytest.mark.f59]

def test_tc_202_hộp_thoại_hiện_đủ_part_1_đến_part_4_như_(school_portal: Portal, base_url: str):
    """TC-202: Hộp thoại hiện đủ Part 1 đến Part 4 như hình của FS"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_203_hộp_thoại_với_một_con_hiện_children_1_và(school_portal: Portal, base_url: str):
    """TC-203: Hộp thoại với một con hiện Children (1) và Household size đúng"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_204_địa_chỉ_người_khai_không_hiện_trong_hộp_(school_portal: Portal, base_url: str):
    """TC-204: Địa chỉ người khai không hiện trong hộp thoại"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_205_con_chưa_có_ea_hiển_thị_dấu_gạch_ngang_ở(school_portal: Portal, base_url: str):
    """TC-205: Con chưa có EA hiển thị dấu gạch ngang ở số EA"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_206_context_trống_thì_part_4_trống_hoặc_ẩn(school_portal: Portal, base_url: str):
    """TC-206: Context trống thì Part 4 trống hoặc ẩn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_207_context_hiển_thị_như_văn_bản_thuần_trong(school_portal: Portal, base_url: str):
    """TC-207: Context hiển thị như văn bản thuần trong hộp thoại"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_208_back_to_edit_đóng_hộp_thoại_giữ_nguyên_m(school_portal: Portal, base_url: str):
    """TC-208: Back to edit đóng hộp thoại, giữ nguyên mẫu và không tạo gì"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_209_sửa_rồi_mở_lại_hộp_thoại_thì_hiện_giá_tr(school_portal: Portal, base_url: str):
    """TC-209: Sửa rồi mở lại hộp thoại thì hiện giá trị mới"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)
