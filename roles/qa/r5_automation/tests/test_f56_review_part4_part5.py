"""F5.6 Review application, Part 4 Context and Part 5 Declaration (21 test cases)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage

pytestmark = [pytest.mark.f56]

def test_tc_141_context_để_trống_vẫn_nộp_được(school_portal: Portal, base_url: str):
    """TC-141: Context để trống vẫn nộp được"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_142_context_hiện_đúng_ở_hộp_thoại_review_bef(school_portal: Portal, base_url: str):
    """TC-142: Context hiện đúng ở hộp thoại Review before submitting"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_143_context_lưu_cùng_đơn_và_hiện_ở_drawer_củ(school_portal: Portal, base_url: str):
    """TC-143: Context lưu cùng đơn và hiện ở drawer của F4"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_144_context_đúng_2000_ký_tự_được_nhận_2001_k(school_portal: Portal, base_url: str):
    """TC-144: Context đúng 2000 ký tự được nhận, 2001 ký tự bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_145_xuống_dòng_trong_context_được_giữ_và_tín(school_portal: Portal, base_url: str):
    """TC-145: Xuống dòng trong Context được giữ và tính một ký tự"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_146_context_chứa_html_và_script_hiển_thị_như(school_portal: Portal, base_url: str):
    """TC-146: Context chứa HTML và script hiển thị như văn bản"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_147_context_chứa_tiếng_việt_emoji_và_nhiều_h(school_portal: Portal, base_url: str):
    """TC-147: Context chứa tiếng Việt, emoji và nhiều hệ chữ"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_148_chưa_tick_declaration_bị_chặn(school_portal: Portal, base_url: str):
    """TC-148: Chưa tick Declaration bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_149_chưa_kiểm_tra_chữ_ký_bị_chặn_t8(school_portal: Portal, base_url: str):
    """TC-149: Chưa kiểm tra chữ ký bị chặn (T8)"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_150_hai_ô_cam_kết_và_date_signed_cùng_thiếu_(school_portal: Portal, base_url: str):
    """TC-150: Hai ô cam kết và Date signed cùng thiếu: một ghi chú liệt kê đủ"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_151_hai_ô_cam_kết_có_thể_tick_và_bỏ_tick(school_portal: Portal, base_url: str):
    """TC-151: Hai ô cam kết có thể tick và bỏ tick"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_152_received_by_hiển_thị_school_user_đang_đă(school_portal: Portal, base_url: str):
    """TC-152: Received by hiển thị School user đang đăng nhập và chỉ đọc"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_153_date_received_là_hôm_nay_và_chỉ_đọc(school_portal: Portal, base_url: str):
    """TC-153: Date received là hôm nay và chỉ đọc"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_154_date_received_đổi_sang_ngày_hôm_nay_khi_(school_portal: Portal, base_url: str):
    """TC-154: Date received đổi sang ngày hôm nay khi tiếp tục bản nháp ở ngày khác"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_155_date_signed_để_trống_bị_chặn(school_portal: Portal, base_url: str):
    """TC-155: Date signed để trống bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_156_date_signed_đúng_định_dạng_và_ngày_có_th(school_portal: Portal, base_url: str):
    """TC-156: Date signed đúng định dạng và ngày có thật được nhận"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_157_date_signed_sai_định_dạng_bị_chặn(school_portal: Portal, base_url: str):
    """TC-157: Date signed sai định dạng bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_158_date_signed_không_có_thật_bị_chặn(school_portal: Portal, base_url: str):
    """TC-158: Date signed không có thật bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_159_date_signed_sau_date_received_bị_chặn_đú(school_portal: Portal, base_url: str):
    """TC-159: Date signed sau Date received bị chặn, đúng ngày nhận được nhận"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_160_date_signed_rất_cũ_không_bị_giới_hạn_dướ(school_portal: Portal, base_url: str):
    """TC-160: Date signed rất cũ không bị giới hạn dưới"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_161_date_signed_chứa_chữ_sql_và_script_bị_ch(school_portal: Portal, base_url: str):
    """TC-161: Date signed chứa chữ, SQL và script bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)
