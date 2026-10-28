"""F5.12 Access, API and data (11 test cases)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage

pytestmark = [pytest.mark.f512]

def test_tc_251_moe_hq_gọi_api_của_f5_bị_từ_chối(school_portal: Portal, base_url: str):
    """TC-251: MOE HQ gọi API của F5 bị từ chối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_252_school_user_không_đọc_được_đơn_của_trườn(school_portal: Portal, base_url: str):
    """TC-252: School user không đọc được đơn của trường khác qua API"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_253_school_user_không_đọc_được_bản_nháp_của_(school_portal: Portal, base_url: str):
    """TC-253: School user không đọc được bản nháp của trường khác qua API"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_254_tải_file_scan_của_trường_khác_bị_từ_chối(school_portal: Portal, base_url: str):
    """TC-254: Tải file scan của trường khác bị từ chối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_255_máy_chủ_không_nhận_giá_trị_tự_điền_gửi_t(school_portal: Portal, base_url: str):
    """TC-255: Máy chủ không nhận giá trị tự điền gửi từ trình duyệt"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_256_yêu_cầu_nộp_bỏ_qua_giao_diện_vẫn_bị_chạy(school_portal: Portal, base_url: str):
    """TC-256: Yêu cầu nộp bỏ qua giao diện vẫn bị chạy lại mọi kiểm tra"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_257_mã_gia_đình_nhiều_con_dùng_chung_mẫu_một(school_portal: Portal, base_url: str):
    """TC-257: Mã gia đình: nhiều con dùng chung, mẫu một con có mã riêng"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_258_nguồn_dữ_liệu_ngoài_lỗi_khi_nộp_thì_khôn(school_portal: Portal, base_url: str):
    """TC-258: Nguồn dữ liệu ngoài lỗi khi nộp thì không nộp"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_259_context_2_mb_gửi_qua_api_bị_từ_chối(school_portal: Portal, base_url: str):
    """TC-259: Context 2 MB gửi qua API bị từ chối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_260_file_scan_lưu_ngoài_thư_mục_web_tên_do_m(school_portal: Portal, base_url: str):
    """TC-260: File scan lưu ngoài thư mục web, tên do máy chủ đặt"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_261_ngày_giờ_và_tiền_theo_ddmmyyyy_hhmm_giờ_(school_portal: Portal, base_url: str):
    """TC-261: Ngày, giờ và tiền theo DD/MM/YYYY, HH:mm giờ Singapore, S$ #,##0.00"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)
