/*
    R9 SEED VERIFY (chi doc, khong sua gi)
    Cho thay: cac con cua persona S7890123F, vi, khoan phi con no, va so dong R9 da co so voi so dong du kien.
    Chay:
      Get-Content tools\seed_r9_verify.sql | docker exec -i edufams-qa-sqlserver bash -c '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -b -I -W -s "|" -y 60' 2>&1 | Out-File -Encoding utf8 verify_output.txt
      Get-Content verify_output.txt
*/
:setvar EDU_DB EducationAccountDatabase
:setvar BILLING_DB BillingPaymentDatabase
GO
USE [$(EDU_DB)];
GO
SET NOCOUNT ON;
PRINT '=== 1. Cac con cua S7890123F (cha hoac me) va vi cua tung con. Cot ghi_chu bao con nao se loi "Unable to load education account" ===';
SELECT s.id, s.full_name, s.citizenship, s.status AS student_status,
       CASE WHEN s.father_nric = 'S7890123F' THEN 'father' ELSE 'mother' END AS quan_he,
       w.id AS wallet_id, w.status AS wallet_status, w.balance,
       (SELECT ISNULL(SUM(CASE direction WHEN 1 THEN amount ELSE -amount END), 0) FROM dbo.wallet_transactions t WHERE t.wallet_id = w.id AND t.status = 2) AS so_cai,
       CASE WHEN w.id IS NULL THEN 'KHONG CO VI'
            WHEN w.status <> 1 THEN 'vi khong Active'
            WHEN s.student_id IS NULL THEN 'student_id NULL (Billing khong khop)'
            WHEN s.student_id <> s.id THEN 'student_id khac id'
            ELSE 'ok' END AS ghi_chu
FROM dbo.students s
LEFT JOIN dbo.wallets w ON w.student_id = s.id
WHERE s.father_nric = 'S7890123F' OR s.mother_nric = 'S7890123F'
ORDER BY s.full_name;

PRINT '=== 2. Vi co so du khac so cai (chi liet ke dong sai) ===';
SELECT w.id, w.student_id, w.balance,
       (SELECT ISNULL(SUM(CASE direction WHEN 1 THEN amount ELSE -amount END), 0) FROM dbo.wallet_transactions t WHERE t.wallet_id = w.id AND t.status = 2) AS so_cai
FROM dbo.wallets w
WHERE w.id LIKE 'R9-WAL-%'
  AND w.balance <> (SELECT ISNULL(SUM(CASE direction WHEN 1 THEN amount ELSE -amount END), 0) FROM dbo.wallet_transactions t WHERE t.wallet_id = w.id AND t.status = 2);

PRINT '=== 3. So dong R9 trong EA (du kien: students 14, wallets 13, wallet_transactions 17) ===';
SELECT (SELECT COUNT(*) FROM dbo.students WHERE id LIKE 'R9-STU-%') AS students,
       (SELECT COUNT(*) FROM dbo.wallets WHERE id LIKE 'R9-WAL-%') AS wallets,
       (SELECT COUNT(*) FROM dbo.wallet_transactions WHERE id LIKE 'R9-WTX-%') AS wallet_transactions;
GO
USE [$(BILLING_DB)];
GO
SET NOCOUNT ON;
PRINT '=== 4. Khoan phi con no (POSTED va chua vao hoa don nao) theo hoc sinh ===';
SELECT c.student_id, COUNT(*) AS so_khoan, SUM(c.total_amount) AS tong,
       SUM(CASE WHEN c.due_date < CAST(DATEADD(HOUR, 8, SYSUTCDATETIME()) AS DATE) THEN 1 ELSE 0 END) AS qua_han
FROM dbo.student_charges c
WHERE c.status = 'POSTED' AND NOT EXISTS (SELECT 1 FROM dbo.invoice_items i WHERE i.student_charge_id = c.id)
GROUP BY c.student_id ORDER BY c.student_id;

PRINT '=== 5. Hoa don, giao dich, nguon thanh toan R9 ===';
SELECT i.id AS invoice, i.invoice_number, i.student_id, i.net_amount, i.status AS invoice_status,
       t.transaction_reference, t.status AS txn_status, f.method, f.status AS leg_status
FROM dbo.invoices i
LEFT JOIN dbo.transactions t ON t.invoice_id = i.id
LEFT JOIN dbo.transaction_funding_sources f ON f.transaction_id = t.id
WHERE i.id LIKE 'R9-INV-%' ORDER BY i.id;

PRINT '=== 6. So dong R9 trong Billing (du kien: charges 54, invoices 5, items 4, transactions 5, legs 5, receipts 2) ===';
SELECT (SELECT COUNT(*) FROM dbo.student_charges WHERE id LIKE 'R9-CHG-%') AS charges,
       (SELECT COUNT(*) FROM dbo.invoices WHERE id LIKE 'R9-INV-%') AS invoices,
       (SELECT COUNT(*) FROM dbo.invoice_items WHERE id LIKE 'R9-ITM-%') AS items,
       (SELECT COUNT(*) FROM dbo.transactions WHERE id LIKE 'R9-TXN-%') AS transactions,
       (SELECT COUNT(*) FROM dbo.transaction_funding_sources WHERE id LIKE 'R9-FS-%') AS legs,
       (SELECT COUNT(*) FROM dbo.payment_webhook_receipts WHERE id LIKE 'R9-WH-%') AS receipts;
GO
