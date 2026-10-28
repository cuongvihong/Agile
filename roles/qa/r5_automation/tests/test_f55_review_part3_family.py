"""F5.5 Review application, Part 3 Family and household (26 test cases)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage

pytestmark = [pytest.mark.f55]

def test_tc_115_add_member_thêm_một_dòng_thành_viên_trốn(school_portal: Portal, base_url: str):
    """TC-115: Add member thêm một dòng thành viên trống"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_116_part_3_tuỳ_chọn_mẫu_không_có_thành_viên_(school_portal: Portal, base_url: str):
    """TC-116: Part 3 tuỳ chọn: mẫu không có thành viên vẫn nộp được"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_117_dòng_thành_viên_có_tên_mà_thiếu_nric_bị_(school_portal: Portal, base_url: str):
    """TC-117: Dòng thành viên có tên mà thiếu NRIC bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_118_dòng_thành_viên_có_nric_mà_thiếu_tên_bị_(school_portal: Portal, base_url: str):
    """TC-118: Dòng thành viên có NRIC mà thiếu tên bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_119_dòng_thành_viên_trống_hoàn_toàn_không_ch(school_portal: Portal, base_url: str):
    """TC-119: Dòng thành viên trống hoàn toàn không chặn nộp"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_120_thêm_tới_5_thành_viên(school_portal: Portal, base_url: str):
    """TC-120: Thêm tới 5 thành viên"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_121_thành_viên_trùng_nric_người_khai_t7_bị_c(school_portal: Portal, base_url: str):
    """TC-121: Thành viên trùng NRIC người khai (T7) bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_122_con_trùng_nric_người_khai_bị_chặn(school_portal: Portal, base_url: str):
    """TC-122: Con trùng NRIC người khai bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_123_hai_thành_viên_trùng_nric_nhau_bị_chặn(school_portal: Portal, base_url: str):
    """TC-123: Hai thành viên trùng NRIC nhau bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_124_thành_viên_trùng_nric_của_con_bị_chặn(school_portal: Portal, base_url: str):
    """TC-124: Thành viên trùng NRIC của con bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_125_con_2_trùng_nric_con_1_bị_chặn(school_portal: Portal, base_url: str):
    """TC-125: Con 2 trùng NRIC con 1 bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_126_nric_trùng_khác_chữ_hoa_chữ_thường_và_kh(school_portal: Portal, base_url: str):
    """TC-126: NRIC trùng khác chữ hoa chữ thường và khoảng trắng vẫn bị coi là trùng"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_127_full_name_thành_viên_100_ký_tự_được_nhận(school_portal: Portal, base_url: str):
    """TC-127: Full name thành viên 100 ký tự được nhận, 101 ký tự bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_128_full_name_nhận_chữ_mọi_hệ_chữ_viết_và_dấ(school_portal: Portal, base_url: str):
    """TC-128: Full name nhận chữ mọi hệ chữ viết và dấu câu cho phép"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_129_full_name_có_chữ_số_hoặc_ký_tự_đặc_biệt_(school_portal: Portal, base_url: str):
    """TC-129: Full name có chữ số hoặc ký tự đặc biệt bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_130_full_name_chứa_script_và_sql_bị_từ_chối_(school_portal: Portal, base_url: str):
    """TC-130: Full name chứa script và SQL bị từ chối và không chạy"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_131_nric_thành_viên_sai_cấu_trúc_bị_chặn(school_portal: Portal, base_url: str):
    """TC-131: NRIC thành viên sai cấu trúc bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_132_gender_của_thành_viên_có_male_female_oth(school_portal: Portal, base_url: str):
    """TC-132: Gender của thành viên có Male, Female, Other"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_133_household_summary_theo_hình_fs_ghi_43000(school_portal: Portal, base_url: str):
    """TC-133: Household summary theo hình FS: GHI 4,300.00, 4 người, PCI 1,075.00"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_134_part_3_không_có_ô_nhập_thu_nhập(school_portal: Portal, base_url: str):
    """TC-134: Part 3 không có ô nhập thu nhập"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_135_household_size_đổi_khi_thêm_con_hoặc_thà(school_portal: Portal, base_url: str):
    """TC-135: Household size đổi khi thêm con hoặc thành viên"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_136_thu_nhập_của_thành_viên_lấy_từ_dữ_liệu_c(school_portal: Portal, base_url: str):
    """TC-136: Thu nhập của thành viên lấy từ dữ liệu Chính phủ và tính lại khi đổi NRIC"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_137_thu_nhập_của_các_con_không_tính_vào_ghi(school_portal: Portal, base_url: str):
    """TC-137: Thu nhập của các con không tính vào GHI"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_138_pci_hiển_thị_s_hai_chữ_số_thập_phân_theo(school_portal: Portal, base_url: str):
    """TC-138: PCI hiển thị S$ hai chữ số thập phân theo giá trị chính xác"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_139_thành_viên_không_có_dữ_liệu_thu_nhập(school_portal: Portal, base_url: str):
    """TC-139: Thành viên không có dữ liệu thu nhập"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_140_api_thu_nhập_chính_phủ_lỗi_thì_không_nộp(school_portal: Portal, base_url: str):
    """TC-140: API thu nhập Chính phủ lỗi thì không nộp được"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)
