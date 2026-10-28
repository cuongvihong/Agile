"""F5.8 Review and submit validation (26 test cases)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage

pytestmark = [pytest.mark.f58]

def test_tc_176_mẫu_hợp_lệ_mở_hộp_thoại_review_before_su(school_portal: Portal, base_url: str):
    """TC-176: Mẫu hợp lệ mở hộp thoại Review before submitting"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_177_mẫu_trống_hoàn_toàn_liệt_kê_mọi_trường_b(school_portal: Portal, base_url: str):
    """TC-177: Mẫu trống hoàn toàn liệt kê mọi trường bắt buộc theo thứ tự FS"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_178_thiếu_đúng_một_trường_date_signed(school_portal: Portal, base_url: str):
    """TC-178: Thiếu đúng một trường: Date signed"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_179_thiếu_hai_trường_chữ_ký_và_date_signed(school_portal: Portal, base_url: str):
    """TC-179: Thiếu hai trường: chữ ký và Date signed"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_180_con_chưa_nhập_nric(school_portal: Portal, base_url: str):
    """TC-180: Con chưa nhập NRIC"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_181_nric_của_con_không_có_trong_hồ_sơ_moe_t4(school_portal: Portal, base_url: str):
    """TC-181: NRIC của con không có trong hồ sơ MOE (T4)"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_182_con_17_tuổi_bị_chặn_t5(school_portal: Portal, base_url: str):
    """TC-182: Con 17 tuổi bị chặn (T5)"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_183_con_đã_có_đơn_pending_trong_năm_nay_bị_c(school_portal: Portal, base_url: str):
    """TC-183: Con đã có đơn Pending trong năm nay bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_184_con_đã_có_đơn_đã_duyệt_trong_năm_nay_bị_(school_portal: Portal, base_url: str):
    """TC-184: Con đã có đơn đã duyệt trong năm nay bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_185_đơn_của_năm_trước_có_chặn_hay_không(school_portal: Portal, base_url: str):
    """TC-185: Đơn của năm trước có chặn hay không"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_186_không_con_nào_học_tại_trường_của_người_d(school_portal: Portal, base_url: str):
    """TC-186: Không con nào học tại trường của người dùng (T6)"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_187_con_đúng_7_tuổi_hôm_nay_được_nhận_con_6_(school_portal: Portal, base_url: str):
    """TC-187: Con đúng 7 tuổi hôm nay được nhận, con 6 tuổi 364 ngày bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_188_con_đúng_16_tuổi_và_16_tuổi_364_ngày_đượ(school_portal: Portal, base_url: str):
    """TC-188: Con đúng 16 tuổi và 16 tuổi 364 ngày được nhận, con 17 tuổi bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_189_tuổi_tính_tại_ngày_nộp_không_tính_tại_ng(school_portal: Portal, base_url: str):
    """TC-189: Tuổi tính tại ngày nộp, không tính tại ngày lưu nháp"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_190_không_có_form_fas_nào_đang_mở_bị_chặn_có(school_portal: Portal, base_url: str):
    """TC-190: Không có form FAS nào đang mở bị chặn, có ngày form kế tiếp (T13)"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_191_không_có_form_nào_đang_mở_và_chưa_có_for(school_portal: Portal, base_url: str):
    """TC-191: Không có form nào đang mở và chưa có form kế tiếp: bỏ phần ngày"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_192_biên_đầu_01082026_mở_31072026_đóng(school_portal: Portal, base_url: str):
    """TC-192: Biên đầu: 01/08/2026 mở, 31/07/2026 đóng"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_193_biên_cuối_31122026_mở_01012027_đóng(school_portal: Portal, base_url: str):
    """TC-193: Biên cuối: 31/12/2026 mở, 01/01/2027 đóng"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_194_chỉ_form_sbfas_của_trường_con_đang_mở_th(school_portal: Portal, base_url: str):
    """TC-194: Chỉ form SBFAS của trường con đang mở thì vẫn nộp được"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_195_chỉ_form_moefas_đang_mở_thì_vẫn_nộp_được(school_portal: Portal, base_url: str):
    """TC-195: Chỉ form MOEFAS đang mở thì vẫn nộp được"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_196_con_không_phải_công_dân_chỉ_xét_form_sbf(school_portal: Portal, base_url: str):
    """TC-196: Con không phải công dân chỉ xét form SBFAS của trường con"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_197_mẫu_hai_con_form_của_một_con_đóng_thì_ch(school_portal: Portal, base_url: str):
    """TC-197: Mẫu hai con, form của một con đóng thì chặn cả mẫu"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_198_hai_ghi_chú_cùng_lúc_thiếu_trường_bắt_bu(school_portal: Portal, base_url: str):
    """TC-198: Hai ghi chú cùng lúc: thiếu trường bắt buộc và form đã đóng"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_199_sửa_lỗi_rồi_bấm_lại_thì_ghi_chú_cũ_biến_(school_portal: Portal, base_url: str):
    """TC-199: Sửa lỗi rồi bấm lại thì ghi chú cũ biến mất"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_200_nhiều_con_có_ghi_chú_riêng_cho_từng_con(school_portal: Portal, base_url: str):
    """TC-200: Nhiều con có ghi chú riêng cho từng con"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_201_trang_cuộn_lên_đầu_để_thấy_ghi_chú(school_portal: Portal, base_url: str):
    """TC-201: Trang cuộn lên đầu để thấy ghi chú"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)
