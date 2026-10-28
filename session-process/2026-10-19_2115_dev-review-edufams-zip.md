# Review EduFAMS.zip vai Dev và ghi chú lỗi tương lai

Ngày: 2026-10-19 21:15.

## 1. Intro
Anh yêu cầu kiểm tra roles/dev/EduFAMS.zip như Dev, sau đó yêu cầu không sửa gì và chỉ ghi lại các lỗi có thể xảy ra về sau.

## 2. Architecture
Hệ thống EduFAMS: .NET 10, các service IAM, StudentSchool, EducationAccount, FAS, BillingPayment, Announcement, Log, ApiGateway (YARP), Worker, MessageBroker (RabbitMQ), Simulation, deploy Docker và k8s.

## 3. Files modified
Không có file nào bị sửa trong zip hay thư mục roles/dev. CLAUDE.md: thêm dòng Session Log và chuyển dòng cũ nhất không ghim sang sessionlog/agileproject.md theo quy tắc xoay vòng. sessionlog/agileproject.md: thêm dòng bị xoay vòng.

## 4. Files added
roles/qa/EduFAMS_Zip_Dev_Review_Notes.md: ghi chú 11 lỗi đã thấy và bảng lỗi có thể xảy ra về sau. session-process/2026-10-19_2115_dev-review-edufams-zip.md: file này.

## 5. Files deleted
Không có. Thư mục giải nén tạm trên máy của anh đã xóa sau khi review xong, nằm ngoài thư mục project.

## 6. Skills used
Không dùng skill nào.

## 7. External references
Không tra cứu bên ngoài. Điều về RabbitMQ guest chỉ chạy từ localhost là kiến thức chung, ghi trong note là chưa kiểm.
