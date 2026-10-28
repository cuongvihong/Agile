# Lệnh chạy automation R9 (copy và dán)

Mở PowerShell, vào thư mục bộ test:

```
cd D:\AIQA\Agileproject\roles\qa\r9_automation
```

Trong PowerShell phải có `.\` trước tên file. Trong cmd thường thì bỏ `.\`.

## Trước khi chạy

Bật e-service 5174, gateway 5273, MockPass 5156. Thêm Docker với edufams-qa-sqlserver cho test dùng SQL, simulator 5176 (`npm run dev:payment-checkout`) cho test online, admin portal 5173 cho smoke. Bộ test chỉ chạy trên localhost, địa chỉ vercel.app bị chặn.

## Chạy theo thứ tự đề nghị

```
.\run_r9_automation.cmd smoke
.\run_r9_automation.cmd read
.\run_r9_automation.cmd rules
```

## Các chế độ

| Lệnh | Chạy gì |
|---|---|
| `.\run_r9_automation.cmd smoke` | 9 test kiểm nhanh môi trường, chỉ đọc |
| `.\run_r9_automation.cmd read` | mọi test không ghi dữ liệu thật |
| `.\run_r9_automation.cmd rules` | 34 case quy tắc kiểm tra dữ liệu mới (TC-173 đến TC-206) |
| `.\run_r9_automation.cmd suite 3` | một nhóm, ở đây F9.3 (số 1 đến 8) |
| `.\run_r9_automation.cmd tc 186` | một case, ở đây TC-186 |
| `.\run_r9_automation.cmd defects` | các case kỳ vọng thất bại vì lệch với R9 |
| `.\run_r9_automation.cmd draft` | các case phụ thuộc giả định chưa được BA xác nhận |
| `.\run_r9_automation.cmd pay` | thêm thanh toán thật, phải gõ `PAY` để xác nhận |
| `.\run_r9_automation.cmd destructive` | rút cạn ví của một con, phải gõ `DRAIN` để xác nhận |
| `.\run_r9_automation.cmd full` | chạy hết mọi test, kể cả thanh toán thật và rút cạn ví, không hỏi xác nhận |
| `.\run_r9_automation.cmd allure` | mở lại báo cáo Allure đã có |

Thêm `headed` ở cuối để xem trình duyệt, ví dụ `.\run_r9_automation.cmd rules headed`.

## Tùy chọn

Tắt phần chờ thêm để chạy nhanh hơn (mặc định mỗi video tối thiểu 5 giây):

```
$env:R9_MIN_VIDEO_SECONDS=0
.\run_r9_automation.cmd read
```

Chạy sạch video cũ:

```
Remove-Item -Recurse -Force artifacts\videos
```

## Kết quả

| File | Nội dung |
|---|---|
| `artifacts\allure-report\index.html` | báo cáo Allure có video từng case (cần lệnh `allure` trong PATH) |
| `artifacts\videos\` | video từng test, tên `TC-xxx__ten_test.webm` |
| `artifacts\reports\r9_case_report.html` | báo cáo theo từng case, mục cần xử lý nằm trên cùng |
| `artifacts\reports\r9_case_report.csv` | cùng nội dung, mở bằng Excel |
| `artifacts\reports\junit.xml` | kết quả dạng XML, gửi lại cho Claude để chỉnh test |

Chi tiết đầy đủ ở `README.md`.

## Nạp dữ liệu seed R9 (làm trước khi chạy test)

Xem chi tiết ở docs/SEED_R9.md. Ba lệnh chính, chạy trong thư mục r9_automation:

```
Get-Content tools\seed_r9_verify.sql | docker exec -i edufams-qa-sqlserver bash -c '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -b -I -W -s "|" -y 60' 2>&1 | Out-File -Encoding utf8 verify_output.txt
Get-Content tools\seed_r9_data.sql | docker exec -i edufams-qa-sqlserver bash -c '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -b -I' 2>&1 | Out-File -Encoding utf8 seed_output.txt
Get-Content tools\seed_r9_cleanup.sql | docker exec -i edufams-qa-sqlserver bash -c '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -b -I' 2>&1 | Out-File -Encoding utf8 cleanup_output.txt
```

Dòng 1 chỉ đọc. Dòng 2 nạp dữ liệu. Dòng 3 chỉ dùng khi cần xóa đúng các dòng R9- để nạp lại.


## Tự nạp lại dữ liệu seed khi chạy

Các chế độ pay, destructive, full, rules, suite, tc và draft tự chạy reseed_r9.cmd trước khi chạy test, nên không cần gõ tay. Muốn bỏ bước này: đặt R9_NO_RESEED=1.

Muốn nạp lại trước MỖI test ghi dữ liệu (không test nào phụ thuộc vào dữ liệu test trước đã tiêu), thêm chữ each ở cuối:

    .\run_r9_automation.cmd full each

Chế độ each chậm hơn vì mỗi lần nạp lại mất vài chục giây. Dùng khi cần kết quả sạch, còn chạy hằng ngày thì để mặc định.
