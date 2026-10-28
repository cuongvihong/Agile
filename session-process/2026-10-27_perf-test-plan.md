# Tạo Performance Test Plan từ performance requirements v0.6, 2026-10-27

## 1. Giới thiệu
Anh yêu cầu tạo một performance plan dựa trên performance requirements mới (v0.6, R1 đến R10). Claude dùng template tài liệu chỉ mang tính tham khảo/Performance_Test_Plan_Template.docx, đọc lại performance-requirements.docx v0.6, project-plan.md của PM và README_LOCAL_RUNNER.md của Dev, rồi dựng Performance Test Plan bằng tiếng Anh theo đúng cấu trúc template.

## 2. Kiến trúc
Giữ nguyên 6 mục của template: Introduction, Roles and Responsibilities, Test Strategy (3.1 đến 3.6), Test Environment, Test Case Details, Test Deliverables. Plan thực thi PRQ chứ không lặp lại: ngưỡng ở mục 3.6 được đọc thẳng từ bảng Section 2.6 của PRQ (28 dòng, cột Applicable thêm theo trạng thái xây dựng của tính năng), 19 kịch bản ở mục 5 (16 hành trình người dùng, 3 batch) trỏ về mã CS của PRQ. Bảng phân bổ tải Level 1 gồm 16 nhóm, tổng 90 VU (peak 180 VU). Template gốc không có TOC cache nên script tự điền mục lục kèm số trang lấy từ PDF.

## 3. File đã sửa
CLAUDE.md: thêm một dòng Session Log (CRLF).

## 4. File thêm
roles/qalead/performance-test-plan.docx (26 trang, Times New Roman, bản v0.1).
session-process/2026-10-27_perf-test-plan.md (file này).

## 5. File xóa
Không có. Template gốc giữ nguyên.

## 6. Skill dùng
Không nạp skill. Dùng python-docx nhân bản hàng và bảng của template để giữ định dạng, LibreOffice để dựng PDF kiểm tra bố cục, pdftotext để kiểm tra chữ. Đã bỏ màu xám và chữ nghiêng của placeholder, thay dấu gạch trong dòng danh sách bằng dấu hai chấm. Không trích bài giảng khóa học.

## 7. Tham chiếu ngoài
Không dùng nguồn web. Căn cứ: performance-requirements.docx v0.6, pm/project-plan.md (mốc sprint, đội ngũ), dev/README_LOCAL_RUNNER.md (cổng dịch vụ), kết quả kiểm DataTest.zip ngày 27/10, Performancehw.jmx (JMeter 5.6.3). Đã đối chiếu 104 mã (CS, X, E, A, PB) trong plan với PRQ, đều có định nghĩa.

## Điểm suy luận và còn mở
Suy luận của QA, đều ghi là đề xuất cần duyệt: think time (5 đến 10 giây phụ huynh, 10 đến 20 giây nhân viên), ramp up, ramp down, thời gian chạy đo 15 phút, bước tăng tải breakpoint 45 VU mỗi 5 phút, tốc độ burst 20 phụ huynh mỗi phút, lịch 28 đến 31/10, phân chia vòng 1 và vòng 2, cấu hình tối thiểu máy chạy JMeter. Các ngưỡng và số liệu Level 1 vẫn là Assumption của PRQ.
Lịch 28 đến 31/10 rất chặt và phụ thuộc điều kiện vào: duyệt plan, mở rộng seed (seed hiện có khoảng 10 phụ huynh và 6 đơn, chưa đủ 200 đơn Pending), mock cố định. Nếu chưa đạt thì lùi theo ngày.
Level 2 cần môi trường đủ cỡ, hiện chưa có. Máy Dev chạy một máy, JMeter nên chạy máy riêng, nếu không kết quả chỉ mang tính tham khảo.
Mục lục là field Word, mở file trong Word có thể hỏi cập nhật. Số trang trong mục lục tính từ bản PDF LibreOffice, có thể lệch vài trang so với Word.
Mâu thuẫn chưa xử lý: roles/qalead/test-strategy.md dòng 33 vẫn ghi Performance ngoài phạm vi 3 sprint.
Chưa làm: ghi tên người duyệt thật (đang để To be confirmed), script JMeter, mở rộng seed, gửi Open Question 11, 12, 14, 17 và 20 đến 29 cho PM, PO, Dev Lead.
