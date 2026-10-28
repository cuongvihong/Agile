/*
    CHỈ DÙNG TAY, CHỈ TRÊN CƠ SỞ DỮ LIỆU QA CỤC BỘ. Không chạy trên dữ liệu dùng chung.

    Mục đích: đưa hai con Noah Lee và Ryan Hassan về trạng thái trước khi chạy `run_r9_automation.cmd pay`,
    để các khoản phí hiện lại trong danh sách. Script này theo cùng cách với
    roles/dev/edufams-backend/.../Scripts/ResetPaymentTestData.sql (Dev), mở rộng cho cả hai con.

    Bước 1 (mặc định): xóa mọi bản ghi thanh toán của hai con theo thứ tự
        checkout_payment_sagas (thêm so với script của Dev) -> payment_webhook_receipts -> transaction_funding_sources -> transactions -> invoice_items -> invoices.
        Các khoản phí (student_charges) không bị xóa, chúng hiện lại vì không còn dòng hóa đơn nào trỏ tới.
    Bước 2 (tùy chọn, đang tắt): đưa số dư ví EA của hai con về 1000.00 như Function9FullFlowSetup.sql yêu cầu.
        Bước này sửa thẳng cột balance, KHÔNG xóa các dòng sổ cái hay giao dịch ví của Function 1. Chỉ bật khi đồng ý
        với chủ dữ liệu. Bỏ dấu chú thích ở khối "BƯỚC 2" bên dưới.

    Chạy bằng SSMS, hoặc trong container QA:
        docker exec -i edufams-qa-sqlserver /opt/mssql-tools18/bin/sqlcmd   (image cũ dùng /opt/mssql-tools/bin/sqlcmd)
        -S localhost -U sa -P "<SQL_SA_PASSWORD>" -C -i /dev/stdin < tools/reset_payment_data.sql
    (mật khẩu lấy từ biến SQL_SA_PASSWORD của deploy/qa/docker-compose.yml, không ghi trong file này)

    Sau khi chạy, kiểm lại bằng: run_r9_automation.cmd read
*/
SET NOCOUNT ON;
SET QUOTED_IDENTIFIER ON;
SET ANSI_NULLS ON;
GO

USE [BillingPaymentService];
GO

DECLARE @Students TABLE (id UNIQUEIDENTIFIER);
INSERT INTO @Students VALUES
    ('01a13f49-4a3b-7238-a13f-19acf9415722'),  -- Noah Lee
    ('01a13f49-4bd8-72c6-b9f0-e89201cb66b7');  -- Ryan Hassan

DECLARE @ids TABLE (id VARCHAR(50));
INSERT INTO @ids SELECT id FROM [dbo].[invoices] WHERE student_id IN (SELECT id FROM @Students);

DECLARE @invoiceCount INT = (SELECT COUNT(*) FROM @ids);
PRINT CONCAT('Số hóa đơn của hai con sẽ bị xóa cùng giao dịch liên quan: ', @invoiceCount);

-- Trạng thái saga của các giao dịch sẽ bị xóa (không có khóa ngoại, nhưng để lại sẽ làm job quét hết hạn chạy trên giao dịch không còn).
DELETE FROM [dbo].[checkout_payment_sagas] WHERE student_id IN (SELECT CONVERT(VARCHAR(50), id) FROM @Students);

DELETE FROM [dbo].[payment_webhook_receipts] WHERE funding_transaction_id IN (SELECT id FROM [dbo].[transaction_funding_sources] WHERE transaction_id IN (SELECT id FROM [dbo].[transactions] WHERE invoice_id IN (SELECT id FROM @ids)));
DELETE FROM [dbo].[transaction_funding_sources] WHERE transaction_id IN (SELECT id FROM [dbo].[transactions] WHERE invoice_id IN (SELECT id FROM @ids));
DELETE FROM [dbo].[transactions] WHERE invoice_id IN (SELECT id FROM @ids);
DELETE FROM [dbo].[invoice_items] WHERE invoice_id IN (SELECT id FROM @ids);
DELETE FROM [dbo].[invoices] WHERE id IN (SELECT id FROM @ids);

PRINT 'Đã xóa dữ liệu thanh toán của Noah Lee và Ryan Hassan. Tiền đã trừ khỏi ví EA KHÔNG được hoàn.';
GO

/* ===================== BƯỚC 2 (tùy chọn, đang tắt) =====================
USE [EduAccount];
GO
UPDATE dbo.wallets
SET balance = CONVERT(decimal(18, 2), 1000.00)
WHERE student_id IN ('01a13f49-4a3b-7238-a13f-19acf9415722', '01a13f49-4bd8-72c6-b9f0-e89201cb66b7');
PRINT CONCAT('Số ví đã đặt lại 1000.00: ', @@ROWCOUNT);
GO
========================================================================= */

USE [BillingPaymentService];
SELECT sc.student_id, COUNT(*) AS charges, SUM(sc.total_amount) AS total_amount
FROM dbo.student_charges AS sc
WHERE sc.student_id IN ('01a13f49-4a3b-7238-a13f-19acf9415722', '01a13f49-4bd8-72c6-b9f0-e89201cb66b7')
  AND NOT EXISTS (SELECT 1 FROM dbo.invoice_items AS ii WHERE ii.student_charge_id = sc.id)
GROUP BY sc.student_id;
GO
