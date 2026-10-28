# R4 test cases sửa theo giao diện localhost

## Mục đích
Anh yêu cầu sửa R4_Test_Cases.xlsx theo UI thật: title rõ hơn, Environment là localhost, Test Data để sau, steps từng bước.

## Phần hệ thống liên quan
Admin Portal http://localhost:5173 (MOE HQ: Financial > MOEFAS; School: Financial > SBFAS schemes; FAS applications là trang Coming soon), e-Service http://localhost:5174 (form FAS của Parent). Build edufams-frontendsprint2vfinalfix.

## File sửa
- roles/qa/R4_Test_Cases.xlsx: sheet "Test cases " cột Title, Environment, Preconditions, Test Steps, Note của 267 case. Cột Test Data, Expected Result, Execution Status, Review Status và 7 sheet khác không đổi.

## File thêm
- roles/qa/R4_Test_Cases_before_localhost_revision.xlsx: bản gốc trước khi sửa, để quay lại.

## Quy tắc áp dụng
- 69 case có màn thật: steps viết theo nhãn nút và thông báo trong source; cột Note ghi chỗ build khác Expected (wizard 4 bước, không có Value type, không có Edit, không có Close form now (demo), chưa chặn overlap).
- 198 case còn lại: steps theo FS và prototype, Note ghi chưa kiểm chứng trên build.
- Preconditions: chỉ thay câu về prototype và tên người dùng mẫu bằng câu về localhost và vai trò.

## Việc còn lại
- Sheet Summary còn câu "216 trên 267 case chạy được trên prototype".
- Test Data đồng bộ sau khi có bộ seed đầy đủ.
- Có thể thiếu nhãn tiếng Anh cho menu Publish, Reactivate và các hộp thoại trạng thái trong resources.ts; cần xem trên màn thật.

## Skill đã dùng
Không dùng skill; dùng openpyxl để sửa workbook.

## Vòng 2: theo mẫu test case trong tài liệu tham khảo
Mẫu đối chiếu: tài liệu chỉ mang tính tham khảo/Self-Enrol_Funding_Package/Tender_TestCases_Defects_and_Regression.xlsx (sheet TestCases) và assignment1/TS01.xlsx.
Đã sửa R4_Test_Cases.xlsx: các bước quan sát dùng động từ Observe như mẫu (225 bước), thêm bốn cột cuối sheet Test cases là Scenario Name, Objective, Postcondition, Technique, lấy từ sheet Scenarios theo Scenario ID. Không đổi thứ tự cột cũ vì 327 công thức và tools/build_coverage.py đọc theo vị trí cột. Đã tính lại bằng LibreOffice: các sheet khác giữ nguyên giá trị, không có lỗi công thức.
Lưu ý: tools/build_coverage.py nhận biết case prototype bằng chữ Prototype ở đầu Environment, nên chạy lại sẽ coi mọi case là không phải prototype.

## Vòng 3: hoàn lại
Anh yêu cầu không sửa nữa và quay về bản cũ. Đã chép R4_Test_Cases_before_localhost_revision.xlsx đè lên R4_Test_Cases.xlsx, so sánh từng byte giống nhau. Bản đã sửa không còn trong roles/qa.
