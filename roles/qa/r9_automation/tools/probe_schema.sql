/* CHỈ ĐỌC. Không sửa, không xóa, không thêm gì trong cơ sở dữ liệu.
   Mục đích: cho Claude biết cấu trúc bảng và dữ liệu đang có trong DB QA cục bộ, để soạn script nạp dữ liệu R9 đúng với DB đang chạy.
   Chạy (PowerShell, trong thư mục r9_automation), kết quả ghi ra probe_output.txt:
     Get-Content tools\probe_schema.sql | docker exec -i edufams-qa-sqlserver bash -c '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -I -W -s "|" -y 160' > probe_output.txt
   Gửi lại file probe_output.txt. */
SET NOCOUNT ON;

PRINT '=== 1. Danh sách database';
SELECT name FROM sys.databases WHERE database_id > 4 ORDER BY name;

PRINT '=== 2. Bảng và số dòng (BillingPaymentService)';
USE BillingPaymentService;
SELECT t.name AS table_name, SUM(p.rows) AS row_count FROM sys.tables t JOIN sys.partitions p ON p.object_id = t.object_id AND p.index_id IN (0,1) GROUP BY t.name ORDER BY t.name;

PRINT '=== 3. Cột các bảng thanh toán (BillingPaymentService)';
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH AS len, NUMERIC_PRECISION AS prec, NUMERIC_SCALE AS scale, IS_NULLABLE AS nullable
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN ('student_charges','invoices','invoice_items','transactions','transaction_funding_sources','payment_webhook_receipts','checkout_payment_sagas','fas_charge_subsidies')
ORDER BY TABLE_NAME, ORDINAL_POSITION;

PRINT '=== 4. Khoản phí theo học sinh (BillingPaymentService)';
IF OBJECT_ID('dbo.student_charges') IS NOT NULL
  EXEC('SELECT student_id, COUNT(*) AS charges, SUM(total_amount) AS total, MIN(status) AS min_status, MAX(status) AS max_status FROM dbo.student_charges GROUP BY student_id ORDER BY student_id');

PRINT '=== 5. Hóa đơn và giao dịch hiện có';
IF OBJECT_ID('dbo.invoices') IS NOT NULL
  EXEC('SELECT TOP 40 * FROM dbo.invoices ORDER BY 1');
IF OBJECT_ID('dbo.transactions') IS NOT NULL
  EXEC('SELECT TOP 40 * FROM dbo.transactions ORDER BY 1');

PRINT '=== 6. Bảng và số dòng (EducationAccountDatabase)';
USE EducationAccountDatabase;
SELECT t.name AS table_name, SUM(p.rows) AS row_count FROM sys.tables t JOIN sys.partitions p ON p.object_id = t.object_id AND p.index_id IN (0,1) GROUP BY t.name ORDER BY t.name;

PRINT '=== 7. Cột các bảng học sinh và ví (EducationAccountDatabase)';
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH AS len, NUMERIC_PRECISION AS prec, NUMERIC_SCALE AS scale, IS_NULLABLE AS nullable
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN ('students','wallets','wallet_transactions','Student_Profile','Wallets','Transactions','Parent_Profile')
ORDER BY TABLE_NAME, ORDINAL_POSITION;

PRINT '=== 8. Học sinh và ví hiện có';
IF OBJECT_ID('dbo.students') IS NOT NULL
  EXEC('SELECT * FROM dbo.students ORDER BY 1');
IF OBJECT_ID('dbo.wallets') IS NOT NULL
  EXEC('SELECT * FROM dbo.wallets ORDER BY 1');

PRINT '=== 9. Các database còn lại: bảng người dùng (IAM) và phụ huynh';
SELECT d.name AS db FROM sys.databases d WHERE d.database_id > 4 AND d.name NOT IN ('BillingPaymentService','EducationAccountDatabase');
