# Script cmd chạy bộ EduFAMS QA bằng Docker

Ngày: 2026-10-19 21:25.

## 1. Intro
Anh yêu cầu deploy EduFAMS local theo deploy/qa/README.md. Môi trường của Claude không có Docker, dotnet và không truy cập được nuget, Docker Hub, mcr. Anh có Docker và dotnet trên máy nên yêu cầu một script để anh tự chạy trên cmd.

## 2. Architecture
deploy/qa/docker-compose.yml dựng 4 container: SQL Server, Redis, RabbitMQ và edufams-qa-app chứa toàn bộ service và simulation. Script chỉ gọi docker compose, không đụng vào code.

## 3. Files modified
Note roles/qa/EduFAMS_Zip_Dev_Review_Notes.md: sửa lại các mục EZ-04, EZ-06, EZ-07, EZ-08, EZ-09 và dòng RabbitMQ sau khi đọc deploy/qa, vì bộ QA ghi đè chuỗi kết nối, dựng đủ bốn service lõi, không có mockpass và .dockerignore loại bin, obj. CLAUDE.md và sessionlog/agileproject.md: dòng Session Log và xoay vòng.

## 4. Files added
roles/qa/run_edufams_qa.cmd: script cmd với các lệnh up, status, logs, errors, down, reset, help. Chạy up thì kiểm Docker, RAM, cổng bị chiếm, build, chờ edufams-qa-app healthy tối đa 20 phút rồi in địa chỉ. Chưa chạy thử được vì môi trường Claude không có cmd và Docker.

## 5. Files deleted
Không có.

## 6. Skills used
computer-use: đọc để xác định terminal chỉ cho click nên không gõ lệnh được.

## 7. External references
Không có.
