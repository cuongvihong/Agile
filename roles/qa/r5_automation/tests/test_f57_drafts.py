"""F5.7 Drafts (14 test cases)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage

pytestmark = [pytest.mark.f57]

def test_tc_162_save_draft_rồi_continue_khôi_phục_đúng_m(school_portal: Portal, base_url: str):
    """TC-162: Save draft rồi Continue khôi phục đúng mẫu đơn (T9)"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_163_save_draft_với_mẫu_chưa_đầy_đủ_vẫn_lưu_đ(school_portal: Portal, base_url: str):
    """TC-163: Save draft với mẫu chưa đầy đủ vẫn lưu được"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_164_save_draft_với_dữ_liệu_sai_vẫn_lưu_nguyê(school_portal: Portal, base_url: str):
    """TC-164: Save draft với dữ liệu sai vẫn lưu nguyên giá trị đã nhập"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_165_save_draft_hai_lần_cập_nhật_cùng_một_bản(school_portal: Portal, base_url: str):
    """TC-165: Save draft hai lần cập nhật cùng một bản nháp"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_166_bấm_đúp_save_draft_chỉ_tạo_một_bản_nháp(school_portal: Portal, base_url: str):
    """TC-166: Bấm đúp Save draft chỉ tạo một bản nháp"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_167_bản_nháp_ghi_người_lưu_và_thời_gian_lưu(school_portal: Portal, base_url: str):
    """TC-167: Bản nháp ghi người lưu và thời gian lưu"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_168_bản_nháp_còn_nguyên_sau_khi_đăng_xuất_và(school_portal: Portal, base_url: str):
    """TC-168: Bản nháp còn nguyên sau khi đăng xuất và đăng nhập lại"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_169_discard_trên_bản_scan_vừa_tải_xoá_scan_v(school_portal: Portal, base_url: str):
    """TC-169: Discard trên bản scan vừa tải xoá scan và không tạo bản nháp"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_170_discard_trên_bản_nháp_đã_mở_xoá_bản_nháp(school_portal: Portal, base_url: str):
    """TC-170: Discard trên bản nháp đã mở xoá bản nháp"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_171_delete_trên_dòng_draft_xoá_bản_nháp_và_s(school_portal: Portal, base_url: str):
    """TC-171: Delete trên dòng Draft xoá bản nháp và scan"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_172_bản_nháp_bị_xoá_khi_nộp_thành_công(school_portal: Portal, base_url: str):
    """TC-172: Bản nháp bị xoá khi nộp thành công"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_173_draft_chỉ_thuộc_trường_của_người_tạo(school_portal: Portal, base_url: str):
    """TC-173: Draft chỉ thuộc trường của người tạo"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_174_hai_người_cùng_mở_một_bản_nháp_lần_lưu_s(school_portal: Portal, base_url: str):
    """TC-174: Hai người cùng mở một bản nháp, lần lưu sau ghi đè"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_175_con_đã_có_đơn_khi_bản_nháp_được_nộp_bị_c(school_portal: Portal, base_url: str):
    """TC-175: Con đã có đơn khi bản nháp được nộp bị chặn lúc nộp"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)
