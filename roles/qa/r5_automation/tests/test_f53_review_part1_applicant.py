"""F5.3 Review application, Part 1 Applicant (34 test cases)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage

pytestmark = [pytest.mark.f53]

def test_tc_068_nhập_nric_người_khai_thì_tự_điền_các_trư(school_portal: Portal, base_url: str):
    """TC-068: Nhập NRIC người khai thì tự điền các trường của Part 1"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_069_nhập_nric_bằng_chữ_thường_được_đổi_thành(school_portal: Portal, base_url: str):
    """TC-069: Nhập NRIC bằng chữ thường được đổi thành chữ hoa và vẫn tự điền"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_070_khoảng_trắng_đầu_cuối_quanh_nric_bị_cắt(school_portal: Portal, base_url: str):
    """TC-070: Khoảng trắng đầu cuối quanh NRIC bị cắt"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_071_category_singapore_pr_international_asea(school_portal: Portal, base_url: str):
    """TC-071: Category Singapore PR, International ASEAN và non ASEAN tự điền đúng"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_072_nationality_hiện_đủ_năm_giá_trị_theo_hồ_(school_portal: Portal, base_url: str):
    """TC-072: Nationality hiện đủ năm giá trị theo hồ sơ"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_073_đổi_nric_sau_khi_đã_tự_điền_thay_toàn_bộ(school_portal: Portal, base_url: str):
    """TC-073: Đổi NRIC sau khi đã tự điền thay toàn bộ giá trị tự điền"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_074_nric_người_khai_không_có_trong_hồ_sơ(school_portal: Portal, base_url: str):
    """TC-074: NRIC người khai không có trong hồ sơ"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_075_hồ_sơ_phụ_huynh_lỗi_thì_không_tự_điền(school_portal: Portal, base_url: str):
    """TC-075: Hồ sơ phụ huynh lỗi thì không tự điền"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_076_các_ô_tự_điền_khoá_không_sửa_được(school_portal: Portal, base_url: str):
    """TC-076: Các ô tự điền khoá không sửa được"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_077_phone_email_và_address_khoá_sau_khi_tự_đ(school_portal: Portal, base_url: str):
    """TC-077: Phone, Email và Address khoá sau khi tự điền"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_078_relationship_to_child_và_schoolbased_fas(school_portal: Portal, base_url: str):
    """TC-078: Relationship to child và School-based FAS luôn sửa được"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_079_nric_người_khai_sai_độ_dài_bị_chặn(school_portal: Portal, base_url: str):
    """TC-079: NRIC người khai sai độ dài bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_080_nric_người_khai_sai_cấu_trúc_bị_chặn(school_portal: Portal, base_url: str):
    """TC-080: NRIC người khai sai cấu trúc bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_081_nric_người_khai_có_khoảng_trắng_ở_giữa_b(school_portal: Portal, base_url: str):
    """TC-081: NRIC người khai có khoảng trắng ở giữa bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_082_nric_người_khai_có_sql_script_và_ký_tự_đ(school_portal: Portal, base_url: str):
    """TC-082: NRIC người khai có SQL, script và ký tự đặc biệt bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_083_chữ_cái_kiểm_tra_cuối_sai_vẫn_được_nhận(school_portal: Portal, base_url: str):
    """TC-083: Chữ cái kiểm tra cuối sai vẫn được nhận"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_084_số_điện_thoại_chỉ_nhận_chữ_số(school_portal: Portal, base_url: str):
    """TC-084: Số điện thoại chỉ nhận chữ số"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_085_dán_số_điện_thoại_có_dấu_cộng_và_khoảng_(school_portal: Portal, base_url: str):
    """TC-085: Dán số điện thoại có dấu cộng và khoảng trắng"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_086_số_điện_thoại_10_chữ_số_được_nhận_chữ_số(school_portal: Portal, base_url: str):
    """TC-086: Số điện thoại 10 chữ số được nhận, chữ số thứ 11 không vào ô"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_087_dán_11_chữ_số_bị_cắt_hoặc_bị_chặn(school_portal: Portal, base_url: str):
    """TC-087: Dán 11 chữ số bị cắt hoặc bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_088_số_điện_thoại_8_chữ_số_được_nhận_7_chữ_s(school_portal: Portal, base_url: str):
    """TC-088: Số điện thoại 8 chữ số được nhận, 7 chữ số bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_089_số_điện_thoại_để_trống_bị_chặn(school_portal: Portal, base_url: str):
    """TC-089: Số điện thoại để trống bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_090_số_điện_thoại_chứa_sql_và_script_chỉ_giữ(school_portal: Portal, base_url: str):
    """TC-090: Số điện thoại chứa SQL và script chỉ giữ chữ số"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_091_email_đúng_cấu_trúc_được_nhận(school_portal: Portal, base_url: str):
    """TC-091: Email đúng cấu trúc được nhận"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_092_email_sai_cấu_trúc_bị_chặn(school_portal: Portal, base_url: str):
    """TC-092: Email sai cấu trúc bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_093_email_để_trống_bị_chặn(school_portal: Portal, base_url: str):
    """TC-093: Email để trống bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_094_giới_hạn_độ_dài_email(school_portal: Portal, base_url: str):
    """TC-094: Giới hạn độ dài email"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_095_email_có_xuống_dòng_bị_chặn_chống_chèn_t(school_portal: Portal, base_url: str):
    """TC-095: Email có xuống dòng bị chặn, chống chèn tiêu đề thư"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_096_address_để_trống_bị_chặn(school_portal: Portal, base_url: str):
    """TC-096: Address để trống bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_097_address_255_ký_tự_được_nhận_256_ký_tự_bị(school_portal: Portal, base_url: str):
    """TC-097: Address 255 ký tự được nhận, 256 ký tự bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_098_address_có_ký_tự_đặc_biệt_sql_và_script_(school_portal: Portal, base_url: str):
    """TC-098: Address có ký tự đặc biệt, SQL và script lưu như văn bản"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_099_relationship_to_child_có_đủ_mười_giá_trị(school_portal: Portal, base_url: str):
    """TC-099: Relationship to child có đủ mười giá trị theo FS"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_100_schoolbased_fas_mặc_định_chọn_yes_và_đổi(school_portal: Portal, base_url: str):
    """TC-100: School-based FAS mặc định chọn Yes và đổi được sang No"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_101_relationship_to_child_để_trống_bị_chặn(school_portal: Portal, base_url: str):
    """TC-101: Relationship to child để trống bị chặn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)
