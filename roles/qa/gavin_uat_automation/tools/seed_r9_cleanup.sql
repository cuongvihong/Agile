/*
    R9 SEED CLEANUP: xoa DUNG cac dong co ma R9- do seed_r9_data.sql tao. Khong dung vao dong nao khac.
    Chi chay khi can don sach de nap lai tu dau. Thu tu xoa theo khoa ngoai: Billing truoc, EA sau.
    Chay:
      Get-Content tools\seed_r9_cleanup.sql | docker exec -i edufams-qa-sqlserver bash -c '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -b -I' 2>&1 | Out-File -Encoding utf8 cleanup_output.txt
    Giao dich/hoa don do test tao ra trong luc chay tren cac con R9 (ma khong bat dau bang R9-) cung bi xoa o day, vi chung gan voi cac khoan phi R9.
*/
:setvar EDU_DB EducationAccountDatabase
:setvar BILLING_DB BillingPaymentDatabase
GO
USE [$(BILLING_DB)];
GO
SET NOCOUNT ON;
SET XACT_ABORT ON;
BEGIN TRY
    BEGIN TRANSACTION;
    DECLARE @Inv TABLE (id VARCHAR(50));
    INSERT INTO @Inv SELECT id FROM dbo.invoices WHERE id LIKE 'R9-INV-%' OR student_id LIKE 'R9-STU-%';
    DECLARE @Txn TABLE (id VARCHAR(50));
    INSERT INTO @Txn SELECT id FROM dbo.transactions WHERE invoice_id IN (SELECT id FROM @Inv);
    DECLARE @Fs TABLE (id VARCHAR(50));
    INSERT INTO @Fs SELECT id FROM dbo.transaction_funding_sources WHERE transaction_id IN (SELECT id FROM @Txn);

    DELETE FROM dbo.checkout_payment_sagas WHERE transaction_id IN (SELECT id FROM @Txn) OR invoice_id IN (SELECT id FROM @Inv) OR student_id LIKE 'R9-STU-%';
    DELETE FROM dbo.payment_webhook_receipts WHERE funding_transaction_id IN (SELECT id FROM @Fs) OR id LIKE 'R9-WH-%';
    DELETE FROM dbo.transaction_funding_sources WHERE id IN (SELECT id FROM @Fs);
    DELETE FROM dbo.transactions WHERE id IN (SELECT id FROM @Txn);
    DELETE FROM dbo.invoice_items WHERE invoice_id IN (SELECT id FROM @Inv);
    DELETE FROM dbo.invoices WHERE id IN (SELECT id FROM @Inv);
    DELETE FROM dbo.student_charge_adjustments WHERE student_charge_id IN (SELECT id FROM dbo.student_charges WHERE student_id LIKE 'R9-STU-%' OR id LIKE 'R9-CHG-%');
    DELETE FROM dbo.student_charges WHERE student_id LIKE 'R9-STU-%' OR id LIKE 'R9-CHG-%';
    COMMIT TRANSACTION;
    PRINT 'Da xoa du lieu R9 trong Billing.';
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;
    PRINT CONCAT('LOI: ', ERROR_MESSAGE());
    THROW;
END CATCH;
GO
USE [$(EDU_DB)];
GO
SET NOCOUNT ON;
SET XACT_ABORT ON;
BEGIN TRY
    BEGIN TRANSACTION;
    DELETE FROM dbo.wallet_transactions WHERE id LIKE 'R9-WTX-%' OR wallet_id LIKE 'R9-WAL-%';
    DELETE FROM dbo.wallets WHERE id LIKE 'R9-WAL-%' OR student_id LIKE 'R9-STU-%';
    DELETE FROM dbo.students WHERE id LIKE 'R9-STU-%';
    COMMIT TRANSACTION;
    PRINT 'Da xoa du lieu R9 trong Education Account.';
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;
    PRINT CONCAT('LOI: ', ERROR_MESSAGE());
    THROW;
END CATCH;
GO
