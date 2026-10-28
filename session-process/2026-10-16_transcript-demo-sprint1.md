# Tạo transcript buổi demo Sprint 1 với khách hàng (2026-10-16)

## 1. Giới thiệu

Anh báo trong groundtruth có file buổi demo hôm nay với khách hàng và muốn có script để đọc. Mục tiêu: chuyển bản ghi thành transcript đọc được.

## 2. Kiến trúc

Không đụng hệ thống dự án. Đầu vào là groundtruth/Sprint 1.m4a. Quy trình: ffmpeg đổi sang wav 16 kHz mono, Silero VAD cắt theo khoảng lặng, Whisper small (int8, sherpa-onnx) nhận dạng từng đoạn, ép tiếng Anh, chạy trên 2 CPU khoảng 8 phút.

## 3. File đã sửa

CLAUDE.md (thêm 2 dòng Session Log, xoay 2 dòng cũ nhất sang sessionlog), sessionlog/agileproject.md (nhận 2 dòng xoay).

## 4. File thêm

groundtruth/Sprint_1_Demo_Transcript.md: transcript có mốc thời gian, bảng phản hồi của khách, bảng chỗ máy nghe sai. File này là bản máy chưa đối chiếu với âm thanh.

## 5. File xóa

Không có. File tạm nằm ngoài thư mục dự án.

## 6. Skill dùng

Không nạp skill nào. Không có công cụ nhận dạng giọng nói sẵn nên tự dựng.

## 7. Tham chiếu ngoài

sherpa-onnx (GitHub k2-fsa/sherpa-onnx, bản phát hành asr-models: sherpa-onnx-whisper-small và silero_vad.onnx), chọn vì Hugging Face bị chặn còn GitHub thì tải được. Thử trước một đoạn 28 giây ở hai vị trí để kiểm chất lượng và chọn ép tiếng Anh vì tự nhận ngôn ngữ nhận nhầm tiếng Việt ở đoạn có tạp âm.

## Điểm suy luận và còn mở

Người nói được gán theo ngữ cảnh. Đoạn 04:06 đến 04:32 là âm thanh trống. Một đoạn có thể bị cắt vì công cụ chỉ đọc 30 giây đầu. Tên riêng và một số thuật ngữ nghe sai, liệt kê trong mục 3 của transcript.
