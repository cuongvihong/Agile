# Bộ dữ liệu R9 bổ sung cho e-Service

Ngày 25/10/2026. Viết theo schema thật trong code Dev (thư mục codesprint2ending): cột snake_case, mã kiểu VARCHAR(50), các ràng buộc CHECK của hóa đơn, giao dịch, nguồn thanh toán. Script chưa được chạy thử trên DB của bạn. Mỗi phần chạy trong một transaction riêng, lỗi thì tự rollback phần đó.

## Vì sao cần

Persona S7890123F hiện có 6 con: Lucas Lim, Nathan Lim, Tan Wei Ming, Test Child One, Two, Three. Dữ liệu này thiếu nhiều tình huống mà bộ case cần (ví đủ tiền, ví thiếu để chia khoản, ví 0.00, ví Closed, không có ví, hóa đơn đang chờ, cần đối soát, thanh toán thất bại, con từ 16 tuổi, người giám hộ thứ hai, con của gia đình khác). Một số con hiện có còn lỗi ví nên các test dựa vào con đầu danh sách bị lỗi.

## Nguyên tắc của script

Chỉ thêm dòng mới, không sửa, không xóa dữ liệu có sẵn. Mọi dòng mới có mã bắt đầu bằng R9- nên dọn được chính xác bằng seed_r9_cleanup.sql. Chạy nhiều lần không bị trùng. Gặp NRIC đã tồn tại dưới id khác thì bỏ qua dòng đó và in ra. Ngày hạn của khoản phí tính theo ngày hiện tại giờ Singapore (quá hạn 10 ngày, còn 3 ngày, còn 30 ngày) nên luôn đúng nhãn Overdue và DueSoon.

## 14 con được thêm

| Mã | Tên | Ví | Khoản phí | Dùng cho kịch bản |
|---|---|---|---|---|
| R9-STU-01 | R9 Ample Tan | 1590.00 Active | 35 khoản: 27.25, 19.50, 12.00, 36.33 quá hạn, 22.23 sắp đến hạn và 30 khoản nhỏ Activity Fee 5.01 đến 5.30 để các test ghi chạy liên tiếp không hết khoản | Trả bằng EA đủ tiền, nhãn Overdue và DueSoon, nhiều khoản |
| R9-STU-02 | R9 Split Lim | 20.00 Active | 3 khoản: 30.00, 25.63, 15.00 (tổng 70.63) | Both: EA 20.00 cộng online 50.63 (TC-097) |
| R9-STU-03 | R9 Zero Lee | 0.00 Active | 21.26 và 19.66 | Chỉ còn Online Gateway |
| R9-STU-04 | R9 Empty Ng | 100.00 Active | không có | Trạng thái rỗng (TC-032) |
| R9-STU-05 | R9 Closed Goh | Closed, 0.00 | 27.25 | EA bị từ chối vì ví không hoạt động |
| R9-STU-06 | R9 NoWallet Chua | không có ví (PR) | 27.25 và 19.66 | Học sinh không có EA, trả online (TC-088) |
| R9-STU-07 | R9 Paid Koh | 500.00 | không còn khoản nào | 2 hóa đơn Paid (EA 27.25 và online 19.66) có biên nhận webhook |
| R9-STU-08 | R9 Pending Ho | 300.00 | không còn khoản nào | Hóa đơn PaymentPending, giao dịch và chân online Pending (TC-085, TC-127) |
| R9-STU-09 | R9 Recon Wee | 272.75 | không còn khoản nào | Giao dịch ReconciliationRequired, chân EA đã trừ 27.25 |
| R9-STU-10 | R9 Teen Yeo | 250.00 | 27.25 và 19.50 | Con từ 16 tuổi (sinh 2009), nút Pay không hiện (TC-175) |
| R9-STU-11 | R9 Mother Sim | 400.00 | 27.25 và 19.66 | mother_nric là S7890123F, cha là người khác: người giám hộ thứ hai (TC-009) |
| R9-STU-12 | R9 Other Pang | 400.00 | 27.25 và 12.00 | Không gắn với S7890123F: thử truy cập con của gia đình khác (TC-013, TC-016) |
| R9-STU-13 | R9 Failed Ong | 300.00 | 21.26 | Hóa đơn Cancelled từ giao dịch Failed, khoản vẫn còn nợ (TC-136) |
| R9-STU-14 | R9 Sandbox Teo | 1000.00 | không có | Con dùng riêng cho khoản phí tạm do test tự tạo và tự dọn (db.temp_charges), không lẫn với con khác |

Sổ cái ví (wallet_transactions) khớp số dư: mỗi ví có dòng cấp tiền và, nếu đã tiêu, dòng trừ tiền, nên tổng In trừ tổng Out bằng số dư. Phần verify có kiểm tra điều này.

## Cách chạy (PowerShell, trong thư mục r9_automation)

Bước 0. Xem tên DB thật, sửa dòng :setvar ở đầu file SQL nếu khác (mặc định EducationAccountDatabase, BillingPaymentDatabase, IAMDatabase):

```
docker exec -i edufams-qa-sqlserver bash -c '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -Q "SELECT name FROM sys.databases"'
```

Bước 1. Kiểm tra trạng thái trước khi nạp. Phần 1 của kết quả cho biết con nào của persona thiếu ví hoặc lệch mã (cột ghi_chu), tức nguyên nhân lỗi "Unable to load education account":

```
Get-Content tools\seed_r9_verify.sql | docker exec -i edufams-qa-sqlserver bash -c '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -b -I -W -s "|" -y 60' 2>&1 | Out-File -Encoding utf8 verify_before.txt
```

Bước 2. Nạp dữ liệu:

```
Get-Content tools\seed_r9_data.sql | docker exec -i edufams-qa-sqlserver bash -c '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -b -I' 2>&1 | Out-File -Encoding utf8 seed_output.txt
```

Bước 3. Kiểm tra lại, so với số dòng dự kiến (EA: 14 học sinh, 13 ví, 17 giao dịch ví; Billing: 54 khoản, 5 hóa đơn, 4 dòng hóa đơn, 5 giao dịch, 5 nguồn thanh toán, 2 biên nhận):

```
Get-Content tools\seed_r9_verify.sql | docker exec -i edufams-qa-sqlserver bash -c '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -b -I -W -s "|" -y 60' 2>&1 | Out-File -Encoding utf8 verify_after.txt
```

Bước 4. Chạy lại test: `.\run_r9_automation.cmd full`. Nếu cần nạp lại từ đầu: chạy seed_r9_cleanup.sql rồi bước 2.

## Hai việc phụ cần biết

Sửa con cũ thiếu ví. Nếu phần 1 của verify cho thấy Lucas Lim hoặc Nathan Lim ghi KHONG CO VI, đặt `:setvar REPAIR_MISSING_WALLETS 1` trong seed_r9_data.sql rồi chạy lại. Script sẽ thêm ví Active 300.00 cho đúng các con đó. Nếu ghi chú là student_id lệch thì đó là dữ liệu cũ của bản seed trước, cần Dev tạo lại DB (publish-all-databases với tham số Recreate), script này không tự sửa.

Người dùng IAM của giao dịch. Cột initiated_by_user_id lấy user của persona trong IAM nếu persona đã đăng nhập ít nhất một lần, nếu chưa thì dùng R9-PARENT-USER. Đăng nhập persona một lần rồi nạp lại sau khi dọn nếu muốn gắn đúng user.

## Chưa nằm trong seed và lý do

Trợ cấp FAS: code Dev hiện cố định subsidy 0 cho mọi khoản (GetOutstandingChargesHandler), nên TC-173 về trợ cấp từng dòng chưa có dữ liệu nào làm cho nó chạy được, đó là chức năng chưa có chứ không phải thiếu dữ liệu. Khoản DRAFT và VOID: các test tự tạo tạm và tự dọn. Tên S01 đến S25 trong R9_Seed_Data.xlsx: bộ này map theo kịch bản chứ không theo tên, vì giao diện thật dựa trên khoản phí và persona S7890123F.

## Lưu ý khi chạy test sau khi nạp

Các test ghi dữ liệu sẽ tiêu khoản phí và rút ví của con được chọn. Chạy lại toàn bộ lần hai thường sẽ có test bị skip vì hết khoản hoặc ví con R9 Split Lim đã về 0; muốn trả về như ban đầu thì chạy `reseed_r9.cmd` (cleanup rồi nạp lại, mất vài giây).
