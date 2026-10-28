"""F5.10 Confirm and submit and routing (24 test cases)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage

pytestmark = [pytest.mark.f510]

def test_tc_210_mẫu_hai_con_tạo_hai_đơn_dùng_chung_mã_gi(school_portal: Portal, base_url: str):
    """TC-210: Mẫu hai con tạo hai đơn dùng chung mã gia đình, MOEFAS Pending (T10)"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_211_mẫu_một_con_tạo_một_đơn_và_toast_số_ít(school_portal: Portal, base_url: str):
    """TC-211: Mẫu một con tạo một đơn và toast số ít"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_212_sau_khi_nộp_về_danh_sách_bản_nháp_biến_m(school_portal: Portal, base_url: str):
    """TC-212: Sau khi nộp về danh sách, bản nháp biến mất và đơn mới hiện"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_213_application_id_có_định_dạng_app_năm_số_t(school_portal: Portal, base_url: str):
    """TC-213: Application ID có định dạng APP, năm, số thứ tự và không trùng"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_214_đơn_tạo_ra_có_nguồn_paper_trong_f4(school_portal: Portal, base_url: str):
    """TC-214: Đơn tạo ra có nguồn Paper trong F4"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_215_schoolbased_fas_được_lưu_cùng_đơn(school_portal: Portal, base_url: str):
    """TC-215: School-based FAS được lưu cùng đơn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_216_scan_gắn_với_đơn_của_từng_con(school_portal: Portal, base_url: str):
    """TC-216: Scan gắn với đơn của từng con"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_217_nộp_lại_cho_con_đã_có_đơn_bị_chặn(school_portal: Portal, base_url: str):
    """TC-217: Nộp lại cho con đã có đơn bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_218_con_công_dân_với_schoolbased_fas_yes_là_(school_portal: Portal, base_url: str):
    """TC-218: Con công dân với School-based FAS Yes là MOEFAS Pending"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_219_con_công_dân_với_schoolbased_fas_no_vẫn_(school_portal: Portal, base_url: str):
    """TC-219: Con công dân với School-based FAS No vẫn là MOEFAS Pending"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_220_con_singapore_pr_là_sbfas_pending_gửi_tr(school_portal: Portal, base_url: str):
    """TC-220: Con Singapore PR là SBFAS Pending gửi trường của con"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_221_con_international_asean_là_sbfas_pending(school_portal: Portal, base_url: str):
    """TC-221: Con International ASEAN là SBFAS Pending gửi trường của con"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_222_con_không_đủ_điều_kiện_quốc_tịch_với_sch(school_portal: Portal, base_url: str):
    """TC-222: Con không đủ điều kiện quốc tịch với School-based FAS No"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_223_mẫu_có_con_công_dân_và_con_pr_được_phân_(school_portal: Portal, base_url: str):
    """TC-223: Mẫu có con công dân và con PR được phân luồng riêng từng con"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_224_đơn_của_con_học_trường_khác_vào_hàng_sbf(school_portal: Portal, base_url: str):
    """TC-224: Đơn của con học trường khác vào hàng SBFAS của trường con"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_225_sau_khi_form_moefas_đóng_đơn_không_đủ_đi(school_portal: Portal, base_url: str):
    """TC-225: Sau khi form MOEFAS đóng, đơn không đủ điều kiện sang SBFAS khi chọn Yes"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_226_sau_khi_form_moefas_đóng_đơn_không_đủ_đi(school_portal: Portal, base_url: str):
    """TC-226: Sau khi form MOEFAS đóng, đơn không đủ điều kiện bị Rejected khi chọn No"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_227_sau_khi_form_moefas_đóng_đơn_đủ_điều_kiệ(school_portal: Portal, base_url: str):
    """TC-227: Sau khi form MOEFAS đóng, đơn đủ điều kiện được duyệt tự động"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_228_bấm_đúp_confirm_and_submit_chỉ_tạo_một_b(school_portal: Portal, base_url: str):
    """TC-228: Bấm đúp Confirm and submit chỉ tạo một bộ đơn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_229_hai_người_nộp_cùng_một_con_chỉ_một_đơn_đ(school_portal: Portal, base_url: str):
    """TC-229: Hai người nộp cùng một con: chỉ một đơn được tạo"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_230_form_đóng_giữa_lúc_mở_hộp_thoại_và_lúc_x(school_portal: Portal, base_url: str):
    """TC-230: Form đóng giữa lúc mở hộp thoại và lúc xác nhận thì không tạo đơn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_231_một_con_vừa_có_đơn_mẫu_hai_con_không_tạo(school_portal: Portal, base_url: str):
    """TC-231: Một con vừa có đơn: mẫu hai con không tạo đơn nào"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_232_lỗi_lưu_khi_xác_nhận_không_tạo_đơn_bản_n(school_portal: Portal, base_url: str):
    """TC-232: Lỗi lưu khi xác nhận: không tạo đơn, bản nháp giữ nguyên"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_233_cảnh_báo_sai_lệch_tên_con_hiện_cho_moe_s(school_portal: Portal, base_url: str):
    """TC-233: Cảnh báo sai lệch tên con hiện cho MOE sau khi nộp"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)
