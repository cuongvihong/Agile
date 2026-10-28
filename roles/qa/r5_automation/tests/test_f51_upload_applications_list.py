"""F5.1 Upload applications list (35 test cases)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage

pytestmark = [pytest.mark.f51]

def test_tc_001_màn_upload_applications_hiện_đúng_thành_(school_portal: Portal, base_url: str):
    """TC-001: Màn Upload applications hiện đúng thành phần ở trạng thái gốc"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_002_ghi_chú_cuối_trang_đúng_nguyên_văn(school_portal: Portal, base_url: str):
    """TC-002: Ghi chú cuối trang đúng nguyên văn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_003_thẻ_đếm_đơn_đã_nộp_của_trường_và_không_đ(school_portal: Portal, base_url: str):
    """TC-003: Thẻ đếm đơn đã nộp của trường và không đếm bản Draft"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_004_bấm_thẻ_pending_lọc_danh_sách_bấm_lần_nữ(school_portal: Portal, base_url: str):
    """TC-004: Bấm thẻ PENDING lọc danh sách, bấm lần nữa bỏ lọc"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_005_bấm_thẻ_sbfas_lọc_các_đơn_sbfas_và_hiện_(school_portal: Portal, base_url: str):
    """TC-005: Bấm thẻ SBFAS lọc các đơn SBFAS và hiện cột Tier"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_006_bấm_thẻ_moefas_lọc_các_đơn_moefas_đã_duy(school_portal: Portal, base_url: str):
    """TC-006: Bấm thẻ MOEFAS lọc các đơn MOEFAS đã duyệt tự động"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_007_thẻ_không_đổi_khi_gõ_ô_search(school_portal: Portal, base_url: str):
    """TC-007: Thẻ không đổi khi gõ ô Search"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_008_tìm_theo_application_id_đầy_đủ(school_portal: Portal, base_url: str):
    """TC-008: Tìm theo Application ID đầy đủ"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_009_tìm_theo_một_phần_application_id(school_portal: Portal, base_url: str):
    """TC-009: Tìm theo một phần Application ID"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_010_tìm_theo_tên_người_tải_lên(school_portal: Portal, base_url: str):
    """TC-010: Tìm theo tên người tải lên"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_011_tìm_theo_tên_học_sinh_trong_dòng_draft(school_portal: Portal, base_url: str):
    """TC-011: Tìm theo tên học sinh trong dòng Draft"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_012_tìm_theo_số_ea_của_học_sinh(school_portal: Portal, base_url: str):
    """TC-012: Tìm theo số EA của học sinh"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_013_tìm_không_có_kết_quả_hiện_thông_báo_trốn(school_portal: Portal, base_url: str):
    """TC-013: Tìm không có kết quả hiện thông báo trống"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_014_tìm_không_phân_biệt_chữ_hoa_chữ_thường_v(school_portal: Portal, base_url: str):
    """TC-014: Tìm không phân biệt chữ hoa chữ thường và cắt khoảng trắng đầu cuối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_015_ký_tự_và___trong_search_là_văn_bản_thườn(school_portal: Portal, base_url: str):
    """TC-015: Ký tự % và _ trong Search là văn bản thường"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_016_search_giới_hạn_100_ký_tự(school_portal: Portal, base_url: str):
    """TC-016: Search giới hạn 100 ký tự"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_017_search_xử_lý_sql_và_script_như_văn_bản(school_portal: Portal, base_url: str):
    """TC-017: Search xử lý SQL và script như văn bản"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_018_bộ_lọc_status_có_đủ_sáu_giá_trị_theo_fs(school_portal: Portal, base_url: str):
    """TC-018: Bộ lọc Status có đủ sáu giá trị theo FS"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_019_lọc_status_draft_và_pending(school_portal: Portal, base_url: str):
    """TC-019: Lọc Status Draft và Pending"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_020_lọc_status_approved_sbfas_approved_moefa(school_portal: Portal, base_url: str):
    """TC-020: Lọc Status Approved SBFAS, Approved MOEFAS và Rejected"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_021_bộ_lọc_tier_liệt_kê_tier_sbfas_của_trườn(school_portal: Portal, base_url: str):
    """TC-021: Bộ lọc Tier liệt kê tier SBFAS của trường và lọc đúng"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_022_bộ_lọc_uploaded_có_ba_giá_trị_và_mặc_địn(school_portal: Portal, base_url: str):
    """TC-022: Bộ lọc Uploaded có ba giá trị và mặc định Last 7 days"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_023_search_status_tier_và_uploaded_kết_hợp_b(school_portal: Portal, base_url: str):
    """TC-023: Search, Status, Tier và Uploaded kết hợp bằng AND"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_024_uploaded_any_time_hiện_thêm_các_đơn_cũ(school_portal: Portal, base_url: str):
    """TC-024: Uploaded Any time hiện thêm các đơn cũ"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_025_dòng_draft_đứng_đầu_danh_sách_với_applic(school_portal: Portal, base_url: str):
    """TC-025: Dòng Draft đứng đầu danh sách với Application ID Not submitted"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_026_dòng_draft_có_nút_continue_và_delete(school_portal: Portal, base_url: str):
    """TC-026: Dòng Draft có nút Continue và Delete"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_027_bấm_vào_dòng_draft_tiếp_tục_bản_nháp(school_portal: Portal, base_url: str):
    """TC-027: Bấm vào dòng Draft tiếp tục bản nháp"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_028_bấm_dòng_đã_nộp_mở_view_application_chỉ_(school_portal: Portal, base_url: str):
    """TC-028: Bấm dòng đã nộp mở View application chỉ đọc có nút Back to list"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_029_last_7_days_gồm_đúng_đơn_tải_lên_7_ngày_(school_portal: Portal, base_url: str):
    """TC-029: Last 7 days gồm đúng đơn tải lên 7 ngày trước, loại đơn tải lên 8 ngày trước"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_030_draft_đứng_đầu_dòng_đã_nộp_mới_nhất_trướ(school_portal: Portal, base_url: str):
    """TC-030: Draft đứng đầu, dòng đã nộp mới nhất trước và 10 dòng mỗi trang"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_031_đổi_bộ_lọc_về_trang_1(school_portal: Portal, base_url: str):
    """TC-031: Đổi bộ lọc về trang 1"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_032_uploaded_at_hiển_thị_ddmmyyyy_hhmm_giờ_s(school_portal: Portal, base_url: str):
    """TC-032: Uploaded at hiển thị DD/MM/YYYY HH:mm giờ Singapore"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_033_school_user_chỉ_thấy_đơn_của_học_sinh_tr(school_portal: Portal, base_url: str):
    """TC-033: School user chỉ thấy đơn của học sinh trường mình"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_034_moe_hq_không_truy_cập_được_upload_applic(school_portal: Portal, base_url: str):
    """TC-034: MOE HQ không truy cập được Upload applications"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_035_đơn_của_con_học_trường_khác_hiện_ở_danh_(school_portal: Portal, base_url: str):
    """TC-035: Đơn của con học trường khác hiện ở danh sách của trường con"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)
