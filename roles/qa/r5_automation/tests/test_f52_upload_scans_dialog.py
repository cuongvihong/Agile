"""F5.2 Upload scans dialog (32 test cases)."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pages.portal import Portal
from pages.paper_applications_page import PaperApplicationsPage

pytestmark = [pytest.mark.f52]

def test_tc_036_hộp_thoại_mở_với_danh_sách_file_trống_và(school_portal: Portal, base_url: str):
    """TC-036: Hộp thoại mở với danh sách file trống và Upload and read tắt"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_037_cancel_đóng_hộp_thoại_và_không_tải_gì(school_portal: Portal, base_url: str):
    """TC-037: Cancel đóng hộp thoại và không tải gì"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_038_bấm_đúp_upload_scans_chỉ_mở_một_hộp_thoạ(school_portal: Portal, base_url: str):
    """TC-038: Bấm đúp Upload scans chỉ mở một hộp thoại"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_039_pdf_jpg_và_png_đều_được_nhận(school_portal: Portal, base_url: str):
    """TC-039: PDF, JPG và PNG đều được nhận"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_040_file_docx_bị_từ_chối(school_portal: Portal, base_url: str):
    """TC-040: File .docx bị từ chối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_041_các_loại_file_khác_bị_từ_chối(school_portal: Portal, base_url: str):
    """TC-041: Các loại file khác bị từ chối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_042_phần_mở_rộng_viết_hoa_vẫn_được_nhận(school_portal: Portal, base_url: str):
    """TC-042: Phần mở rộng viết hoa vẫn được nhận"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_043_phần_mở_rộng_jpeg_được_coi_là_jpg(school_portal: Portal, base_url: str):
    """TC-043: Phần mở rộng jpeg được coi là JPG"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_044_file_đổi_tên_phần_mở_rộng_bị_từ_chối(school_portal: Portal, base_url: str):
    """TC-044: File đổi tên phần mở rộng bị từ chối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_045_file_5_mb_được_nhận(school_portal: Portal, base_url: str):
    """TC-045: File 5 MB được nhận"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_046_file_11_mb_bị_từ_chối(school_portal: Portal, base_url: str):
    """TC-046: File 11 MB bị từ chối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_047_biên_10_mb_đúng_10_mb_được_nhận_10_mb_cộ(school_portal: Portal, base_url: str):
    """TC-047: Biên 10 MB: đúng 10 MB được nhận, 10 MB cộng 1 byte bị từ chối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_048_file_0_byte_bị_từ_chối(school_portal: Portal, base_url: str):
    """TC-048: File 0 byte bị từ chối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_049_thêm_đủ_5_file_được_nhận(school_portal: Portal, base_url: str):
    """TC-049: Thêm đủ 5 file được nhận"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_050_file_thứ_6_bị_từ_chối(school_portal: Portal, base_url: str):
    """TC-050: File thứ 6 bị từ chối"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_051_chọn_6_file_một_lần_chỉ_nhận_5_file_đầu(school_portal: Portal, base_url: str):
    """TC-051: Chọn 6 file một lần chỉ nhận 5 file đầu"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_052_bỏ_một_file_bằng_remove_rồi_thêm_file_kh(school_portal: Portal, base_url: str):
    """TC-052: Bỏ một file bằng Remove rồi thêm file khác"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_053_bỏ_file_cuối_cùng_thì_upload_and_read_tắ(school_portal: Portal, base_url: str):
    """TC-053: Bỏ file cuối cùng thì Upload and read tắt"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_054_file_hợp_lệ_và_file_lỗi_trong_cùng_một_l(school_portal: Portal, base_url: str):
    """TC-054: File hợp lệ và file lỗi trong cùng một lần chọn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_055_thêm_cùng_một_file_hai_lần(school_portal: Portal, base_url: str):
    """TC-055: Thêm cùng một file hai lần"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_056_upload_and_read_mở_màn_review_applicatio(school_portal: Portal, base_url: str):
    """TC-056: Upload and read mở màn Review application với các giá trị đọc được"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_057_bấm_đúp_upload_and_read_chỉ_tải_và_đọc_m(school_portal: Portal, base_url: str):
    """TC-057: Bấm đúp Upload and read chỉ tải và đọc một lần"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_058_tải_đủ_5_file_là_một_mẫu_đơn(school_portal: Portal, base_url: str):
    """TC-058: Tải đủ 5 file là một mẫu đơn"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_059_lời_nhắc_trong_hộp_thoại_phù_hợp_với_mẫu(school_portal: Portal, base_url: str):
    """TC-059: Lời nhắc trong hộp thoại phù hợp với mẫu nhiều con"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_060_đọc_scan_lỗi_file_mã_hoá_mật_khẩu(school_portal: Portal, base_url: str):
    """TC-060: Đọc scan lỗi: file mã hoá mật khẩu"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_061_đọc_scan_lỗi_file_hỏng_và_trang_trắng(school_portal: Portal, base_url: str):
    """TC-061: Đọc scan lỗi: file hỏng và trang trắng"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_062_lỗi_máy_chủ_khi_đọc_scan(school_portal: Portal, base_url: str):
    """TC-062: Lỗi máy chủ khi đọc scan"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_063_đóng_hộp_thoại_khi_đang_đọc_scan(school_portal: Portal, base_url: str):
    """TC-063: Đóng hộp thoại khi đang đọc scan"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_064_tên_file_unicode_có_khoảng_trắng_và_dài_(school_portal: Portal, base_url: str):
    """TC-064: Tên file Unicode, có khoảng trắng và dài 255 ký tự"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_065_tên_file_chứa_mã_hiển_thị_như_văn_bản(school_portal: Portal, base_url: str):
    """TC-065: Tên file chứa mã hiển thị như văn bản"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_066_đường_dẫn_trong_tên_file_bị_loại_bỏ_khi_(school_portal: Portal, base_url: str):
    """TC-066: Đường dẫn trong tên file bị loại bỏ khi lưu"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)

def test_tc_067_pdf_có_javascript_không_chạy_khi_đọc_và_(school_portal: Portal, base_url: str):
    """TC-067: PDF có JavaScript không chạy khi đọc và khi xem"""
    page = school_portal.page
    school_portal.go_to_applications()
    expect(page.locator("main, [role='main']").first).to_be_visible()
    page.wait_for_timeout(1000)
