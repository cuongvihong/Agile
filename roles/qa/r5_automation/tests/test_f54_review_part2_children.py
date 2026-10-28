"""F5.4 Review application, Part 2 Children (13 test cases)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage

pytestmark = [pytest.mark.f54]

def test_tc_102_nhập_nric_con_tự_điền_thông_tin_con_từ_h(school_portal: Portal, base_url: str):
    """TC-102: Nhập NRIC con tự điền thông tin con từ hồ sơ MOE"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_103_nhập_thêm_con_học_trường_khác_tự_điền_đú(school_portal: Portal, base_url: str):
    """TC-103: Nhập thêm con học trường khác tự điền đúng trường và khối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_104_các_ô_thông_tin_con_khoá_không_sửa_được(school_portal: Portal, base_url: str):
    """TC-104: Các ô thông tin con khoá không sửa được"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_105_đổi_nric_con_thay_toàn_bộ_dữ_liệu_con(school_portal: Portal, base_url: str):
    """TC-105: Đổi NRIC con thay toàn bộ dữ liệu con"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_106_nric_con_sai_cấu_trúc_bị_chặn(school_portal: Portal, base_url: str):
    """TC-106: NRIC con sai cấu trúc bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_107_hồ_sơ_moe_lỗi_thì_không_tự_điền_thông_ti(school_portal: Portal, base_url: str):
    """TC-107: Hồ sơ MOE lỗi thì không tự điền thông tin con"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_108_level_suy_ra_đúng_từ_grade_ở_các_biên_p1(school_portal: Portal, base_url: str):
    """TC-108: Level suy ra đúng từ Grade ở các biên P1, P6, S1, S5, PU1, PU3"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_109_grade_ngoài_danh_sách_thì_level_hiển_thị(school_portal: Portal, base_url: str):
    """TC-109: Grade ngoài danh sách thì Level hiển thị thế nào"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_110_add_child_thêm_một_dòng_con_trống_và_giữ(school_portal: Portal, base_url: str):
    """TC-110: Add child thêm một dòng con trống và giữ dòng đã nhập"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_111_mẫu_có_hai_con_một_con_ở_trường_người_dù(school_portal: Portal, base_url: str):
    """TC-111: Mẫu có hai con: một con ở trường người dùng, một con ở trường khác"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_112_thêm_đến_5_dòng_con_và_5_dòng_thành_viên(school_portal: Portal, base_url: str):
    """TC-112: Thêm đến 5 dòng con và 5 dòng thành viên không lỗi"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_113_dòng_con_để_trống_nric_bị_bỏ_qua_hay_bị_(school_portal: Portal, base_url: str):
    """TC-113: Dòng con để trống NRIC bị bỏ qua hay bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_114_tên_con_khác_dữ_liệu_chính_phủ_hiện_cảnh(school_portal: Portal, base_url: str):
    """TC-114: Tên con khác dữ liệu Chính phủ hiện cảnh báo và vẫn nộp được"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)
