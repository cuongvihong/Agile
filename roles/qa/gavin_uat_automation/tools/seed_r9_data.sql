/*
    R9 SEED DATA (them du lieu con thieu cho e-Service, chay duoc nhieu lan)
    ------------------------------------------------------------------------
    Viet theo schema that trong code Dev (codesprint2ending): ten cot snake_case, id kieu VARCHAR(50).
    Chi THEM dong moi. Khong sua, khong xoa du lieu co san. Moi dong cua script nay co ma bat dau bang R9-
    (student R9-STU-xx, wallet R9-WAL-xx, charge R9-CHG-xx, invoice R9-INV-xx...), nen don dep bang
    seed_r9_cleanup.sql ma khong dung vao du lieu khac.

    Gan cac con R9 vao persona MockPass S7890123F (cot father_nric hoac mother_nric), nen dang nhap bang
    persona nay se thay them cac con tuong ung tung kich ban:

      R9-STU-01  R9 Ample Tan      vi 1590.00 Active, 5 khoan (co khoan qua han, khoan sap den han)  -> tra bang EA du tien
      R9-STU-02  R9 Split Lim      vi 20.00 Active, 3 khoan tong 70.63                              -> Both, EA 20.00 + online 50.63
      R9-STU-03  R9 Zero Lee       vi 0.00 Active, 2 khoan (21.26 + 19.66)                          -> chi con Online Gateway
      R9-STU-04  R9 Empty Ng       vi 100.00 Active, khong co khoan nao                             -> man hinh trong
      R9-STU-05  R9 Closed Goh     vi Closed (4), so du 0.00, 1 khoan 27.25                         -> EA bi tu choi, vi khong hoat dong
      R9-STU-06  R9 NoWallet Chua  PR, khong co vi, 2 khoan                                         -> hoc sinh khong co EA
      R9-STU-07  R9 Paid Koh       vi 500.00, 2 hoa don Paid (EA 27.25, online 19.66) co bien lai   -> lich su, khong con khoan nao
      R9-STU-08  R9 Pending Ho     vi 300.00, hoa don PaymentPending, giao dich Pending, online Pending -> dang cho thanh toan
      R9-STU-09  R9 Recon Wee      vi 272.75, hoa don PaymentPending, giao dich ReconciliationRequired  -> doi soat
      R9-STU-10  R9 Teen Yeo       16 tuoi tro len, vi 250.00, 2 khoan                              -> nut Pay khong hien (TC-175)
      R9-STU-11  R9 Mother Sim     mother_nric = S7890123F, father_nric la phu huynh khac, vi 400.00, 2 khoan -> nguoi giam ho thu hai
      R9-STU-12  R9 Other Pang     KHONG gan voi S7890123F, vi 400.00, 2 khoan                      -> thu truy cap con cua nguoi khac
      R9-STU-13  R9 Failed Ong     vi 300.00, hoa don Cancelled tu giao dich Failed, khoan van con no -> thanh toan that bai
      R9-STU-14  R9 Sandbox Teo    vi 1000.00, khong co khoan nao -> con dung rieng cho khoan phi tam do test tu tao (pages/db.py temp_charges)
      Con R9-STU-01 co them 30 khoan nho (Activity Fee 01 den 30) de nhieu test ghi dung lien tiep khong het khoan.

    CACH CHAY (PowerShell, trong thu muc r9_automation). Sua ten DB neu khac, xem dong :setvar ben duoi:
      Get-Content tools\seed_r9_data.sql | docker exec -i edufams-qa-sqlserver bash -c '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -b -I' 2>&1 | Out-File -Encoding utf8 seed_output.txt
      Get-Content seed_output.txt

    Neu bao loi giua chung, gui lai seed_output.txt. Moi phan (EA, Billing) chay trong transaction rieng, loi la rollback phan do.
    Chua chay thu tren DB cua ban: hay doc seed_output.txt va chay tools\seed_r9_verify.sql de doi chieu.
*/
:setvar EDU_DB EducationAccountDatabase
:setvar BILLING_DB BillingPaymentDatabase
:setvar IAM_DB IAMDatabase
:setvar REPAIR_MISSING_WALLETS 0
GO

/* ================= PHAN A: Education Account ($(EDU_DB)) ================= */
USE [$(EDU_DB)];
GO
SET NOCOUNT ON;
SET QUOTED_IDENTIFIER ON;
SET ANSI_NULLS ON;
SET XACT_ABORT ON;
PRINT 'A. Education Account: them hoc sinh, vi, so cai vi cho cac con R9';

DECLARE @Parent VARCHAR(9) = 'S7890123F';

DECLARE @S TABLE (id VARCHAR(50), nric VARCHAR(9), full_name NVARCHAR(150), dob DATE, citizenship INT, gender INT,
                  father_nric VARCHAR(9), mother_nric VARCHAR(9));
INSERT INTO @S VALUES
('R9-STU-01', 'S9100001A', N'R9 Ample Tan',     '2017-05-04', 1, 1, @Parent,    NULL),
('R9-STU-02', 'S9100002B', N'R9 Split Lim',     '2017-08-19', 1, 2, @Parent,    NULL),
('R9-STU-03', 'S9100003C', N'R9 Zero Lee',      '2018-02-11', 1, 1, @Parent,    NULL),
('R9-STU-04', 'S9100004D', N'R9 Empty Ng',      '2018-09-23', 1, 2, @Parent,    NULL),
('R9-STU-05', 'S9100005E', N'R9 Closed Goh',    '2016-12-02', 1, 1, @Parent,    NULL),
('R9-STU-06', 'S9100006F', N'R9 NoWallet Chua', '2017-03-30', 2, 2, @Parent,    NULL),
('R9-STU-07', 'S9100007G', N'R9 Paid Koh',      '2016-07-14', 1, 1, @Parent,    NULL),
('R9-STU-08', 'S9100008H', N'R9 Pending Ho',    '2017-10-06', 1, 2, @Parent,    NULL),
('R9-STU-09', 'S9100009I', N'R9 Recon Wee',     '2018-01-27', 1, 1, @Parent,    NULL),
('R9-STU-10', 'S9100010J', N'R9 Teen Yeo',      '2009-03-15', 1, 2, @Parent,    NULL),
('R9-STU-11', 'S9100011K', N'R9 Mother Sim',    '2017-11-08', 1, 2, 'S7000011R', @Parent),
('R9-STU-12', 'S9100012L', N'R9 Other Pang',    '2017-06-21', 1, 1, 'S7000012R', NULL),
('R9-STU-13', 'S9100013M', N'R9 Failed Ong',    '2018-04-17', 1, 2, @Parent,    NULL),
('R9-STU-14', 'S9100014N', N'R9 Sandbox Teo',   '2017-12-12', 1, 1, @Parent,    NULL);

DECLARE @W TABLE (id VARCHAR(50), student_id VARCHAR(50), balance DECIMAL(18,2), status INT);
INSERT INTO @W VALUES
('R9-WAL-01', 'R9-STU-01', 1590.00, 1),
('R9-WAL-02', 'R9-STU-02',   20.00, 1),
('R9-WAL-03', 'R9-STU-03',    0.00, 1),
('R9-WAL-04', 'R9-STU-04',  100.00, 1),
('R9-WAL-05', 'R9-STU-05',    0.00, 4),
-- R9-STU-06 co chu dich khong co vi
('R9-WAL-07', 'R9-STU-07',  500.00, 1),
('R9-WAL-08', 'R9-STU-08',  300.00, 1),
('R9-WAL-09', 'R9-STU-09',  272.75, 1),
('R9-WAL-10', 'R9-STU-10',  250.00, 1),
('R9-WAL-11', 'R9-STU-11',  400.00, 1),
('R9-WAL-12', 'R9-STU-12',  400.00, 1),
('R9-WAL-13', 'R9-STU-13',  300.00, 1),
('R9-WAL-14', 'R9-STU-14', 1000.00, 1);

-- So cai: moi vi co mot dong In (cap tien) va, neu da tieu, mot dong Out, de so du = tong In tru tong Out.
-- direction 1 = In, 2 = Out. status 2 = Success.
DECLARE @T TABLE (id VARCHAR(50), reference_id VARCHAR(100), wallet_id VARCHAR(50), direction INT, amount DECIMAL(18,2), description VARCHAR(255));
INSERT INTO @T VALUES
('R9-WTX-01-1', 'R9-GRANT-01',  'R9-WAL-01', 1, 1590.00, 'R9 seed: government grant top-up'),
('R9-WTX-02-1', 'R9-GRANT-02',  'R9-WAL-02', 1,   20.00, 'R9 seed: government grant top-up'),
('R9-WTX-03-1', 'R9-GRANT-03',  'R9-WAL-03', 1,  100.00, 'R9 seed: government grant top-up'),
('R9-WTX-03-2', 'R9-SPEND-03',  'R9-WAL-03', 2,  100.00, 'R9 seed: earlier fee payments used the whole balance'),
('R9-WTX-04-1', 'R9-GRANT-04',  'R9-WAL-04', 1,  100.00, 'R9 seed: government grant top-up'),
('R9-WTX-05-1', 'R9-GRANT-05',  'R9-WAL-05', 1,   80.00, 'R9 seed: government grant top-up'),
('R9-WTX-05-2', 'R9-SPEND-05',  'R9-WAL-05', 2,   80.00, 'R9 seed: balance paid out before the account was closed'),
('R9-WTX-07-1', 'R9-GRANT-07',  'R9-WAL-07', 1,  527.25, 'R9 seed: government grant top-up'),
('R9-WTX-07-2', 'R9-PAYEA-07',  'R9-WAL-07', 2,   27.25, 'R9 seed: school fee paid from Education Account'),
('R9-WTX-08-1', 'R9-GRANT-08',  'R9-WAL-08', 1,  300.00, 'R9 seed: government grant top-up'),
('R9-WTX-09-1', 'R9-GRANT-09',  'R9-WAL-09', 1,  300.00, 'R9 seed: government grant top-up'),
('R9-WTX-09-2', 'R9-PAYEA-09',  'R9-WAL-09', 2,   27.25, 'R9 seed: EA debit whose outcome is under reconciliation'),
('R9-WTX-10-1', 'R9-GRANT-10',  'R9-WAL-10', 1,  250.00, 'R9 seed: government grant top-up'),
('R9-WTX-11-1', 'R9-GRANT-11',  'R9-WAL-11', 1,  400.00, 'R9 seed: government grant top-up'),
('R9-WTX-12-1', 'R9-GRANT-12',  'R9-WAL-12', 1,  400.00, 'R9 seed: government grant top-up'),
('R9-WTX-13-1', 'R9-GRANT-13',  'R9-WAL-13', 1,  300.00, 'R9 seed: government grant top-up'),
('R9-WTX-14-1', 'R9-GRANT-14',  'R9-WAL-14', 1, 1000.00, 'R9 seed: government grant top-up');

BEGIN TRY
    BEGIN TRANSACTION;

    -- Ma NRIC da co duoi id khac: bo qua dong do va bao, khong ghi de.
    SELECT s.id AS bo_qua_vi_nric_da_ton_tai_voi_id_khac, s.nric, e.id AS id_hien_co
    FROM @S s INNER JOIN dbo.students e ON e.nric = s.nric AND e.id <> s.id;

    INSERT INTO dbo.students (id, student_id, nric, full_name, date_of_birth, citizenship, gender, status, race,
                              block, street, unit, postal_code, country, father_nric, mother_nric, created_at, created_by)
    SELECT s.id, s.id, s.nric, s.full_name, s.dob, s.citizenship, s.gender, 1, N'Chinese',
           N'418', N'Serangoon Central', N'#09-321', '550418', N'Singapore', s.father_nric, s.mother_nric,
           SYSUTCDATETIME(), 'R9Seed'
    FROM @S s
    WHERE NOT EXISTS (SELECT 1 FROM dbo.students e WHERE e.id = s.id OR e.nric = s.nric OR e.student_id = s.id);
    PRINT CONCAT('  students them moi: ', @@ROWCOUNT);

    INSERT INTO dbo.wallets (id, student_id, currency, balance, status, created_at, created_by)
    SELECT w.id, w.student_id, 'SGD', w.balance, w.status, SYSUTCDATETIME(), 'R9Seed'
    FROM @W w
    INNER JOIN dbo.students st ON st.id = w.student_id
    WHERE NOT EXISTS (SELECT 1 FROM dbo.wallets e WHERE e.id = w.id OR e.student_id = w.student_id);
    PRINT CONCAT('  wallets them moi: ', @@ROWCOUNT);

    INSERT INTO dbo.wallet_transactions (id, reference_id, wallet_id, direction, amount, status, description, created_at, created_by)
    SELECT t.id, t.reference_id, t.wallet_id, t.direction, t.amount, 2, t.description, SYSUTCDATETIME(), 'R9Seed'
    FROM @T t
    INNER JOIN dbo.wallets w ON w.id = t.wallet_id
    WHERE NOT EXISTS (SELECT 1 FROM dbo.wallet_transactions e WHERE e.id = t.id);
    PRINT CONCAT('  wallet_transactions them moi: ', @@ROWCOUNT);

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;
    PRINT CONCAT('LOI PHAN A: ', ERROR_MESSAGE());
    THROW;
END CATCH;
GO

/* ===== PHAN A2 (tuy chon, mac dinh tat): them vi cho con cua S7890123F dang thieu vi =====
   Bat bang -v hoac sua :setvar REPAIR_MISSING_WALLETS 1. Chi tac dong con khong co vi va khong phai R9-.
   Vi them vao Active, so du 300.00, kem dong cap tien tuong ung. Bao lai tung con duoc them. */
SET NOCOUNT ON;
IF '$(REPAIR_MISSING_WALLETS)' = '1'
BEGIN
    DECLARE @Fix TABLE (student_id VARCHAR(50), full_name NVARCHAR(150));
    INSERT INTO @Fix
    SELECT s.id, s.full_name FROM dbo.students s
    WHERE (s.father_nric = 'S7890123F' OR s.mother_nric = 'S7890123F')
      AND s.id NOT LIKE 'R9-%'
      AND NOT EXISTS (SELECT 1 FROM dbo.wallets w WHERE w.student_id = s.id);

    INSERT INTO dbo.wallets (id, student_id, currency, balance, status, created_at, created_by)
    SELECT 'R9-WAL-FIX-' + f.student_id, f.student_id, 'SGD', 300.00, 1, SYSUTCDATETIME(), 'R9Seed' FROM @Fix f;

    INSERT INTO dbo.wallet_transactions (id, reference_id, wallet_id, direction, amount, status, description, created_at, created_by)
    SELECT 'R9-WTX-FIX-' + f.student_id, 'R9-GRANT-FIX-' + f.student_id, 'R9-WAL-FIX-' + f.student_id, 1, 300.00, 2,
           'R9 seed: wallet added for a child that had none', SYSUTCDATETIME(), 'R9Seed' FROM @Fix f;

    SELECT student_id AS da_them_vi_cho, full_name FROM @Fix;
END
ELSE PRINT '  A2 bo qua (REPAIR_MISSING_WALLETS = 0). Neu verify cho thay con co NRIC cua persona nhung thieu vi, chay lai voi gia tri 1.';
GO

/* ================= PHAN B: Billing ($(BILLING_DB)) ================= */
USE [$(BILLING_DB)];
GO
SET NOCOUNT ON;
SET QUOTED_IDENTIFIER ON;
SET ANSI_NULLS ON;
SET XACT_ABORT ON;
PRINT 'B. Billing: them khoan phi, hoa don, giao dich, nguon thanh toan, bien nhan webhook';

-- Cac thanh phan phi dung chung phai co san (do 00_SeedFeeTypesAndComponents tao khi publish).
IF (SELECT COUNT(*) FROM dbo.fee_components WHERE id IN
    ('ffff0001-0000-0000-0000-000000000002','ffff0004-0000-0000-0000-000000000001','ffff0004-0000-0000-0000-000000000002',
     'ffff0004-0000-0000-0000-000000000003','ffff0004-0000-0000-0000-000000000004')) < 5
    THROW 51901, 'Thieu fee_components ffff0001-...0002 hoac ffff0004-...0001 den 0004. Chay publish-all-databases (seed 00) truoc.', 1;

DECLARE @Today DATE = CAST(DATEADD(HOUR, 8, SYSUTCDATETIME()) AS DATE);   -- ngay hien tai theo gio Singapore
DECLARE @Now DATETIME2(3) = SYSUTCDATETIME();

-- Nguoi dung khoi tao giao dich: lay user cua persona trong IAM neu da dang nhap it nhat mot lan.
DECLARE @UserId VARCHAR(50) = 'R9-PARENT-USER';
IF DB_ID('$(IAM_DB)') IS NOT NULL
BEGIN
    DECLARE @u VARCHAR(50);
    BEGIN TRY
        EXEC sp_executesql N'SELECT TOP 1 @u = user_id FROM [$(IAM_DB)].dbo.parent_profiles WHERE nric = ''S7890123F''', N'@u VARCHAR(50) OUTPUT', @u = @u OUTPUT;
        IF @u IS NOT NULL SET @UserId = @u;
    END TRY
    BEGIN CATCH
        PRINT CONCAT('  Khong doc duoc IAM parent_profiles: ', ERROR_MESSAGE());
    END CATCH
END
PRINT CONCAT('  initiated_by_user_id dung cho giao dich: ', @UserId,
             CASE WHEN @UserId = 'R9-PARENT-USER' THEN ' (chua tim thay user cua persona trong IAM, dang nhap persona mot lan roi chay lai neu can)' ELSE '' END);

-- Khoan phi. due: OVERDUE = qua han 10 ngay, SOON = con 3 ngay, LATER = con 30 ngay.
DECLARE @C TABLE (id VARCHAR(50), student_id VARCHAR(50), comp VARCHAR(50), comp_name NVARCHAR(100), amount DECIMAL(18,2), due_kind VARCHAR(8));
INSERT INTO @C VALUES
('R9-CHG-01-01','R9-STU-01','ffff0001-0000-0000-0000-000000000002',N'Standard Miscellaneous Fee',27.25,'LATER'),
('R9-CHG-01-02','R9-STU-01','ffff0004-0000-0000-0000-000000000001',N'Stationery Fee',19.50,'LATER'),
('R9-CHG-01-03','R9-STU-01','ffff0004-0000-0000-0000-000000000003',N'Sports Fee',12.00,'LATER'),
('R9-CHG-01-04','R9-STU-01','ffff0004-0000-0000-0000-000000000004',N'Library Fee',36.33,'OVERDUE'),
('R9-CHG-01-05','R9-STU-01','ffff0004-0000-0000-0000-000000000002',N'Field Trip Fee',22.23,'SOON'),
('R9-CHG-02-01','R9-STU-02','ffff0004-0000-0000-0000-000000000003',N'Sports Fee',30.00,'LATER'),
('R9-CHG-02-02','R9-STU-02','ffff0001-0000-0000-0000-000000000002',N'Standard Miscellaneous Fee',25.63,'LATER'),
('R9-CHG-02-03','R9-STU-02','ffff0004-0000-0000-0000-000000000001',N'Stationery Fee',15.00,'SOON'),
('R9-CHG-03-01','R9-STU-03','ffff0001-0000-0000-0000-000000000002',N'Standard Miscellaneous Fee',21.26,'LATER'),
('R9-CHG-03-02','R9-STU-03','ffff0004-0000-0000-0000-000000000001',N'Stationery Fee',19.66,'SOON'),
('R9-CHG-05-01','R9-STU-05','ffff0001-0000-0000-0000-000000000002',N'Standard Miscellaneous Fee',27.25,'LATER'),
('R9-CHG-06-01','R9-STU-06','ffff0001-0000-0000-0000-000000000002',N'Standard Miscellaneous Fee',27.25,'LATER'),
('R9-CHG-06-02','R9-STU-06','ffff0004-0000-0000-0000-000000000001',N'Stationery Fee',19.66,'SOON'),
('R9-CHG-07-01','R9-STU-07','ffff0001-0000-0000-0000-000000000002',N'Standard Miscellaneous Fee',27.25,'LATER'),
('R9-CHG-07-02','R9-STU-07','ffff0004-0000-0000-0000-000000000001',N'Stationery Fee',19.66,'LATER'),
('R9-CHG-08-01','R9-STU-08','ffff0001-0000-0000-0000-000000000002',N'Standard Miscellaneous Fee',21.26,'LATER'),
('R9-CHG-09-01','R9-STU-09','ffff0001-0000-0000-0000-000000000002',N'Standard Miscellaneous Fee',27.25,'LATER'),
('R9-CHG-10-01','R9-STU-10','ffff0001-0000-0000-0000-000000000002',N'Standard Miscellaneous Fee',27.25,'LATER'),
('R9-CHG-10-02','R9-STU-10','ffff0004-0000-0000-0000-000000000001',N'Stationery Fee',19.50,'SOON'),
('R9-CHG-11-01','R9-STU-11','ffff0001-0000-0000-0000-000000000002',N'Standard Miscellaneous Fee',27.25,'LATER'),
('R9-CHG-11-02','R9-STU-11','ffff0004-0000-0000-0000-000000000004',N'Library Fee',19.66,'LATER'),
('R9-CHG-12-01','R9-STU-12','ffff0001-0000-0000-0000-000000000002',N'Standard Miscellaneous Fee',27.25,'LATER'),
('R9-CHG-12-02','R9-STU-12','ffff0004-0000-0000-0000-000000000001',N'Stationery Fee',12.00,'LATER'),
('R9-CHG-13-01','R9-STU-13','ffff0001-0000-0000-0000-000000000002',N'Standard Miscellaneous Fee',21.26,'LATER');

-- 30 khoan nho cho R9-STU-01 (5.01 den 5.30), han con 60 ngay de nam sau cac khoan khac trong danh sach phan trang
;WITH n AS (SELECT TOP (30) ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS i FROM sys.all_objects)
INSERT INTO @C
SELECT 'R9-CHG-01-' + RIGHT('00' + CAST(i + 5 AS VARCHAR(3)), 2), 'R9-STU-01',
       'ffff0004-0000-0000-0000-00000000000' + CAST(((i - 1) % 4) + 1 AS VARCHAR(1)),
       N'Activity Fee ' + RIGHT('00' + CAST(i AS VARCHAR(3)), 2), CAST(5.00 + i / 100.0 AS DECIMAL(18,2)), 'FAR'
FROM n;

-- Hoa don: status 3 = PaymentPending, 4 = Paid, 5 = Cancelled. invoice_number de trigger tu sinh.
DECLARE @I TABLE (id VARCHAR(50), student_id VARCHAR(50), amount DECIMAL(18,2), status INT);
INSERT INTO @I VALUES
('R9-INV-07-1','R9-STU-07',27.25,4),
('R9-INV-07-2','R9-STU-07',19.66,4),
('R9-INV-08',  'R9-STU-08',21.26,3),
('R9-INV-09',  'R9-STU-09',27.25,3),
('R9-INV-13',  'R9-STU-13',21.26,5);

BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO dbo.student_charges (id, fee_publication_id, student_id, enrollment_id, school_id, academic_year_id, academic_level_id,
        school_class_id, student_category_snapshot, fee_component_id, fee_component_name_snapshot, fee_rate_rule_id, pricing_date,
        period_start, period_end_exclusive, charge_date, due_date, base_amount, tax_amount, total_amount, currency_code, status,
        posted_at, voided_at, void_reason, idempotency_key)
    SELECT c.id, NULL, c.student_id, 'ENR-' + c.student_id, 'SCH-003', 'AY-2026', 'AL-P3',
        NULL, CASE WHEN c.student_id = 'R9-STU-06' THEN 'PR' ELSE 'SC' END, c.comp, c.comp_name + N' - Term 4 2026', NULL, @Today,
        '2026-10-01', '2027-01-01', '2026-10-01',
        CASE c.due_kind WHEN 'OVERDUE' THEN DATEADD(DAY, -10, @Today) WHEN 'SOON' THEN DATEADD(DAY, 3, @Today) WHEN 'FAR' THEN DATEADD(DAY, 60, @Today) ELSE DATEADD(DAY, 30, @Today) END,
        c.amount, 0.00, c.amount, 'SGD', 'POSTED', @Now, NULL, NULL, NULL
    FROM @C c
    WHERE NOT EXISTS (SELECT 1 FROM dbo.student_charges e WHERE e.id = c.id);
    PRINT CONCAT('  student_charges them moi: ', @@ROWCOUNT);

    INSERT INTO dbo.invoices (id, student_id, school_id, invoice_number, currency_code, gross_amount, subsidy_amount, net_amount, status,
                              issued_at, due_date, paid_at, cancelled_at, created_at, updated_at)
    SELECT i.id, i.student_id, 'SCH-003', NULL, 'SGD', i.amount, 0.00, i.amount, i.status,
        CASE WHEN i.status IN (3,4) THEN DATEADD(DAY, -5, @Now) END,
        CASE WHEN i.status IN (3,4) THEN DATEADD(DAY, 14, @Today) END,
        CASE WHEN i.status = 4 THEN DATEADD(DAY, -4, @Now) END,
        CASE WHEN i.status = 5 THEN DATEADD(DAY, -2, @Now) END,
        DATEADD(DAY, -5, @Now), @Now
    FROM @I i
    WHERE NOT EXISTS (SELECT 1 FROM dbo.invoices e WHERE e.id = i.id);
    PRINT CONCAT('  invoices them moi: ', @@ROWCOUNT);

    -- Hoa don Cancelled (R9-INV-13) khong co dong chi tiet: khoan phi da duoc tra ve trang thai con no.
    INSERT INTO dbo.invoice_items (id, invoice_id, line_number, student_charge_id, gross_amount, subsidy_amount, net_amount)
    SELECT v.id, v.invoice_id, 1, v.charge_id, v.amount, 0.00, v.amount
    FROM (VALUES
        ('R9-ITM-07-1','R9-INV-07-1','R9-CHG-07-01',27.25),
        ('R9-ITM-07-2','R9-INV-07-2','R9-CHG-07-02',19.66),
        ('R9-ITM-08',  'R9-INV-08',  'R9-CHG-08-01',21.26),
        ('R9-ITM-09',  'R9-INV-09',  'R9-CHG-09-01',27.25)
    ) v(id, invoice_id, charge_id, amount)
    WHERE EXISTS (SELECT 1 FROM dbo.invoices i WHERE i.id = v.invoice_id)
      AND NOT EXISTS (SELECT 1 FROM dbo.invoice_items e WHERE e.id = v.id OR e.student_charge_id = v.charge_id);
    PRINT CONCAT('  invoice_items them moi: ', @@ROWCOUNT);

    -- Giao dich: status 1 Pending, 2 Succeeded, 3 Failed, 5 ReconciliationRequired.
    INSERT INTO dbo.transactions (id, invoice_id, initiated_by_user_id, transaction_reference, idempotency_key, requested_amount,
                                  settled_amount, currency_code, status, created_at, updated_at, completed_at)
    SELECT v.id, v.invoice_id, @UserId, v.ref, v.idem, v.amount,
           CASE WHEN v.status = 2 THEN v.amount END, 'SGD', v.status,
           DATEADD(DAY, -5, @Now), @Now,
           CASE WHEN v.status IN (2,3) THEN DATEADD(DAY, -4, @Now) END
    FROM (VALUES
        ('R9-TXN-07-1','R9-INV-07-1','PAY-R9-07-1','R9-IDEM-07-1',27.25,2),
        ('R9-TXN-07-2','R9-INV-07-2','PAY-R9-07-2','R9-IDEM-07-2',19.66,2),
        ('R9-TXN-08',  'R9-INV-08',  'PAY-R9-08',  'R9-IDEM-08',  21.26,1),
        ('R9-TXN-09',  'R9-INV-09',  'PAY-R9-09',  'R9-IDEM-09',  27.25,5),
        ('R9-TXN-13',  'R9-INV-13',  'PAY-R9-13',  'R9-IDEM-13',  21.26,3)
    ) v(id, invoice_id, ref, idem, amount, status)
    WHERE EXISTS (SELECT 1 FROM dbo.invoices i WHERE i.id = v.invoice_id)
      AND NOT EXISTS (SELECT 1 FROM dbo.transactions e WHERE e.id = v.id OR e.transaction_reference = v.ref);
    PRINT CONCAT('  transactions them moi: ', @@ROWCOUNT);

    -- Nguon thanh toan: method 1 = EducationAccount, 2 = OnlineGateway.
    -- status 1 Pending, 2 Succeeded, 3 Failed, 5 ReconciliationRequired.
    INSERT INTO dbo.transaction_funding_sources (id, transaction_id, sequence_number, funding_reference, method, requested_amount, settled_amount,
        status, wallet_id, provider_code, provider_transaction_id, failure_code, failure_reason, created_at, updated_at, completed_at,
        education_account_transaction_id, education_account_reversal_transaction_id)
    SELECT v.id, v.txn, 1, v.fref, v.method, v.amount, CASE WHEN v.status = 2 THEN v.amount END,
           v.status, v.wallet, v.provider, v.provider_txn, v.fail_code, v.fail_reason,
           DATEADD(DAY, -5, @Now), @Now, CASE WHEN v.status IN (2,3) THEN DATEADD(DAY, -4, @Now) END,
           v.ea_txn, NULL
    FROM (VALUES
        ('R9-FS-07-1','R9-TXN-07-1','FR-R9-07-1',1,27.25,2,'R9-WAL-07',NULL,        NULL,          NULL,              NULL,                        'R9-WTX-07-2'),
        ('R9-FS-07-2','R9-TXN-07-2','FR-R9-07-2',2,19.66,2,NULL,       'PAYOS_SIM', 'R9-PRV-07-2', NULL,              NULL,                        NULL),
        ('R9-FS-08',  'R9-TXN-08',  'FR-R9-08',  2,21.26,1,NULL,       'PAYOS_SIM', NULL,          NULL,              NULL,                        NULL),
        ('R9-FS-09',  'R9-TXN-09',  'FR-R9-09',  1,27.25,5,'R9-WAL-09',NULL,        NULL,          NULL,              NULL,                        'R9-WTX-09-2'),
        ('R9-FS-13',  'R9-TXN-13',  'FR-R9-13',  2,21.26,3,NULL,       'PAYOS_SIM', NULL,          'PAYMENT_DECLINED','Card declined (R9 seed data)', NULL)
    ) v(id, txn, fref, method, amount, status, wallet, provider, provider_txn, fail_code, fail_reason, ea_txn)
    WHERE EXISTS (SELECT 1 FROM dbo.transactions t WHERE t.id = v.txn)
      AND NOT EXISTS (SELECT 1 FROM dbo.transaction_funding_sources e WHERE e.id = v.id OR e.funding_reference = v.fref);
    PRINT CONCAT('  transaction_funding_sources them moi: ', @@ROWCOUNT);

    -- Bien nhan webhook da xu ly (processing_status 2 = Processed).
    INSERT INTO dbo.payment_webhook_receipts (id, funding_transaction_id, provider_code, provider_event_id, provider_transaction_id,
        funding_reference, event_type, payload_hash, processing_status, received_at, processed_at, error_message)
    SELECT v.id, v.fs, 'PAYOS_SIM', v.evt, v.ptx, v.fref, v.etype, CONVERT(VARBINARY(32), HASHBYTES('SHA2_256', v.evt)), 2,
           DATEADD(DAY, -4, @Now), DATEADD(DAY, -4, @Now), NULL
    FROM (VALUES
        ('R9-WH-07-2','R9-FS-07-2','R9-EVT-07-2','R9-PRV-07-2','FR-R9-07-2','payment.succeeded'),
        ('R9-WH-13',  'R9-FS-13',  'R9-EVT-13',  'R9-PRV-13',  'FR-R9-13',  'payment.failed')
    ) v(id, fs, evt, ptx, fref, etype)
    WHERE EXISTS (SELECT 1 FROM dbo.transaction_funding_sources f WHERE f.id = v.fs)
      AND NOT EXISTS (SELECT 1 FROM dbo.payment_webhook_receipts e WHERE e.id = v.id OR e.provider_event_id = v.evt);
    PRINT CONCAT('  payment_webhook_receipts them moi: ', @@ROWCOUNT);

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;
    PRINT CONCAT('LOI PHAN B: ', ERROR_MESSAGE());
    THROW;
END CATCH;
GO
PRINT 'Xong. Chay tools\seed_r9_verify.sql de doi chieu.';
GO
