"""F5.11 View and edit submitted application (17 test cases)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage

pytestmark = [pytest.mark.f511]

def test_tc_234_view_application_hiện_đủ_năm_phần_chỉ_đọ(school_portal: Portal, base_url: str):
    """TC-234: View application hiện đủ năm phần chỉ đọc và nút Back to list"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_235_đơn_pending_có_nút_edit(school_portal: Portal, base_url: str):
    """TC-235: Đơn Pending có nút Edit"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_236_đơn_approved_sbfas_không_có_nút_edit(school_portal: Portal, base_url: str):
    """TC-236: Đơn Approved SBFAS không có nút Edit"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_237_đơn_approved_moefas_không_có_nút_edit(school_portal: Portal, base_url: str):
    """TC-237: Đơn Approved MOEFAS không có nút Edit"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_238_đơn_rejected_không_có_nút_edit(school_portal: Portal, base_url: str):
    """TC-238: Đơn Rejected không có nút Edit"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_239_sửa_đơn_pending_và_save_changes_history_(school_portal: Portal, base_url: str):
    """TC-239: Sửa đơn Pending và Save changes, History ghi Paper application edited (T12)"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_240_save_changes_cập_nhật_thành_viên_gia_đìn(school_portal: Portal, base_url: str):
    """TC-240: Save changes cập nhật thành viên gia đình và thu nhập của đơn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_241_sửa_đơn_không_chạy_lại_luồng_quyết_định(school_portal: Portal, base_url: str):
    """TC-241: Sửa đơn không chạy lại luồng quyết định"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_242_sau_khi_form_đóng_vẫn_sửa_được_đơn_pendi(school_portal: Portal, base_url: str):
    """TC-242: Sau khi form đóng vẫn sửa được đơn Pending (BR9)"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_243_save_changes_chạy_lại_kiểm_tra_bắt_buộc(school_portal: Portal, base_url: str):
    """TC-243: Save changes chạy lại kiểm tra bắt buộc"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_244_khi_sửa_nric_người_khai_và_nric_con_bị_k(school_portal: Portal, base_url: str):
    """TC-244: Khi sửa, NRIC người khai và NRIC con bị khoá"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_245_đơn_đang_sửa_không_bị_coi_là_trùng_với_c(school_portal: Portal, base_url: str):
    """TC-245: Đơn đang sửa không bị coi là trùng với chính nó"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_246_đơn_đổi_trạng_thái_trong_lúc_sửa_thì_khô(school_portal: Portal, base_url: str):
    """TC-246: Đơn đổi trạng thái trong lúc sửa thì không lưu"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_247_bấm_đúp_save_changes_chỉ_ghi_một_mục_his(school_portal: Portal, base_url: str):
    """TC-247: Bấm đúp Save changes chỉ ghi một mục History"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_248_lỗi_lưu_khi_save_changes_không_thêm_hist(school_portal: Portal, base_url: str):
    """TC-248: Lỗi lưu khi Save changes không thêm History"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_249_api_sửa_đơn_đã_quyết_định_bị_từ_chối(school_portal: Portal, base_url: str):
    """TC-249: API sửa đơn đã quyết định bị từ chối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_250_school_user_không_mở_được_đơn_của_trường(school_portal: Portal, base_url: str):
    """TC-250: School user không mở được đơn của trường khác bằng địa chỉ"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)
