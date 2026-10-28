# Sửa test case R9 theo seed mới và rule mới

## 1. Mục đích
Anh gửi R9_Seed_Data.xlsx và bảo sửa R9_Test_Cases_final_FS09.xlsx cho phù hợp rule mới (R9_FAS_Validation_Rules.docx) và seed mới.

## 2. Phần hệ thống liên quan
Function 9, dữ liệu kiểm thử (seed R4, R8, R9), sheet Test cases, Summary, Scenarios, Assumptions, FS Trace, Seed Data.

## 3. File thêm
roles/qa/R9_Test_Cases_final_FS09_before_new_seed.xlsx (bản sao file cũ).

## 4. File sửa
roles/qa/R9_Test_Cases_final_FS09.xlsx (156 case), CLAUDE.md (thêm một dòng Session Log).

## 5. Điểm cần nhớ
Seed mặc định @ApplyFasSubsidy = 1, trái với BR-F9-08 (Sprint 1 trợ cấp bằng 0), nên TC-020 chạy với cờ bằng 0 (helper H-FLAG0) còn TC-173 và TC-174 chỉ chạy khi BA xác nhận có hiện trợ cấp (ASM-R9-36, O19). Seed không có phí School fee và Extracurricular, không có hạn nộp theo dòng (TC-022 không kiểm được dòng sớm nhất), không có invoice Draft (helper H-DRAFT, SQL cần thống nhất với Dev). TC-007 dùng PAR-X02 nhưng R8 chặn đăng nhập bằng MSG-0801 (ASM-R9-37). Con từ 16 tuổi X01 là con của PAR-S25 (ASM-R9-38). Execution Status, Actual Result và Defect Reports giữ nguyên từ lần chạy 22/10 trên dữ liệu cũ, phải chạy lại. Số tiền nhỏ 2.25 và 5.83 có thể bị sandbox từ chối (mức tối thiểu của nhà cung cấp chưa biết). r9_automation/data/seed.py chưa sửa.

## 6. Nguồn tham khảo
R9_Seed_Data.xlsx, R8_Seed_Data.xlsx, R9_seed.sql, R9_FAS_Validation_Rules.docx.

## 7. Vòng 2: phủ toàn bộ validation rule
Anh hỏi test case đã phủ hết validation rule chưa, rồi bảo phủ cả rule QA đề xuất vì rule đó sẽ vào FS. Đối chiếu từng mục của R9_FAS_Validation_Rules.docx (A1 đến G6, H1 đến H23, 15 thông báo) với 156 case. Thêm 31 case TC-176 đến TC-206 (tổng 187), sheet Rules Trace (92 rule, tất cả có case), ASM-R9-39 và helper H-DESC trong sheet Seed Data. Case mới đều Draft và Not Run, kết quả mong đợi theo rules doc. Còn trống: mức tối thiểu của provider (O4) và hiển thị quá hạn (O7) vì chưa có quyết định. Đã sửa ví dụ C3 trong rules doc (20.5 vượt số dư 20.00 thành 10.5). Bản 156 case giữ ở R9_Test_Cases_final_FS09_156cases.xlsx.
