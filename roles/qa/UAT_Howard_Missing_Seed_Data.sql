/* =====================================================================
   UAT Howard - missing seed data (add-on to DataTest/seed-data-csv)
   Same rows as UAT_Howard_Missing_Seed_Data.xlsx. Generated 27/10/2026. SQL Server (T-SQL).

   HOW TO RUN
   - Run in SSMS / Azure Data Studio, or: sqlcmd -S <server> -U <user> -P <password> -C -i UAT_Howard_Missing_Seed_Data.sql
   - Run it AFTER the base seed. Safe to run again: each section first deletes the rows it inserts (by id), then inserts them.
   - One database per service (USE [ServiceName]). Change the names if your databases are named differently.
   - Table and column names follow the DataTest CSV files (dbo.<csv table name>). If the real tables use other names
     (for example dbo.Wallets / dbo.Transactions in the R8 script), rename them here first.
   - All values are written as text (N'...') so SQL Server converts them to the column type. Empty values are NULL.
   - CitizenSimulator and MockPass_Singpass sections are at the end. Skip them if those mocks read CSV/JSON files instead of a database.

   CODES TO CONFIRM WITH DEV (see the README sheet of the xlsx)
   - wallet_transactions.status 2 = Completed (as in the seed), 1 = Pending; direction 1 = In, 2 = Out
   - wallets.status 1 = Active, 2 = Due for closure, 3 = Closed; EA students.citizenship 1 = SC, 2 = PR
   - student_charges.status PAID / REFUNDED; applications.status SCHOOL_APPROVED / SCHOOL_REJECTED
   - sbfas_scheme_applications has no columns for tier / reason / comment. They are filled at the end of the FASService
     section ONLY IF Dev has added the columns; otherwise that step is skipped.
   ===================================================================== */
SET NOCOUNT ON;
SET XACT_ABORT ON;
GO

/* ---------------------------------------------------------------------
   StudentSchoolService
   --------------------------------------------------------------------- */
USE [StudentSchoolService];
GO
BEGIN TRANSACTION;
DELETE FROM dbo.[student_class_assignments] WHERE [id] IN (N'SCA-031', N'SCA-032', N'SCA-033', N'SCA-034', N'SCA-035', N'SCA-036', N'SCA-037', N'SCA-038', N'SCA-039');
DELETE FROM dbo.[student_school_enrollments] WHERE [id] IN (N'ENR-031', N'ENR-032', N'ENR-033', N'ENR-034', N'ENR-035', N'ENR-036', N'ENR-037', N'ENR-038', N'ENR-039');
DELETE FROM dbo.[students] WHERE [id] IN (N'STU-031', N'STU-032', N'STU-033', N'STU-034', N'STU-035', N'STU-036', N'STU-037', N'STU-038', N'STU-039');
DELETE FROM dbo.[school_classes] WHERE [id] IN (N'CLS-RI-S4-01', N'CLS-RI-JC1-01');
DELETE FROM dbo.[school_level_offerings] WHERE [id] IN (N'SLO-RI-2026-S4');

-- school_level_offerings (1 rows)
INSERT INTO dbo.[school_level_offerings] ([id], [code], [school_id], [academic_year_id], [academic_level_id], [is_active])
VALUES
    (N'SLO-RI-2026-S4', N'SLO-00009', N'SCH-001', N'AY-2026', N'AL-S4', N'1');

-- school_classes (2 rows)
INSERT INTO dbo.[school_classes] ([id], [code], [school_level_offering_id], [class_code], [class_name], [is_active])
VALUES
    (N'CLS-RI-S4-01', N'CLS-00024', N'SLO-RI-2026-S4', N'S4-01', N'Secondary 4-01', N'1'),
    (N'CLS-RI-JC1-01', N'CLS-00025', N'SLO-RI-2026-JC1', N'JC1-01', N'Junior College 1-01', N'1');

-- students (9 rows)
INSERT INTO dbo.[students] ([id], [code], [nric], [display_name], [date_of_birth], [source_system], [category], [is_active])
VALUES
    (N'STU-031', N'STU-00031', N'S1034578B', N'Henry Tan', N'2010-08-15', N'STUDENT_SERVICE', N'SC', N'1'),
    (N'STU-032', N'STU-00032', N'S1845623J', N'Megan Tan', N'2018-01-09', N'STUDENT_SERVICE', N'SC', N'1'),
    (N'STU-033', N'STU-00033', N'S1756234G', N'Rachel Tan', N'2017-06-12', N'STUDENT_SERVICE', N'PR', N'1'),
    (N'STU-034', N'STU-00034', N'S1967345F', N'Jonas Tan', N'2019-05-20', N'STUDENT_SERVICE', N'SC', N'1'),
    (N'STU-035', N'STU-00035', N'S0956812C', N'Jasmine Lee', N'2009-03-02', N'STUDENT_SERVICE', N'SC', N'1'),
    (N'STU-036', N'STU-00036', N'S1878456D', N'Kayden Ng', N'2018-06-21', N'STUDENT_SERVICE', N'SC', N'1'),
    (N'STU-037', N'STU-00037', N'S1989567Z', N'Sophie Ng', N'2019-09-30', N'STUDENT_SERVICE', N'SC', N'1'),
    (N'STU-038', N'STU-00038', N'S1790678Z', N'Zara Koh', N'2017-02-14', N'STUDENT_SERVICE', N'SC', N'1'),
    (N'STU-039', N'STU-00039', N'S1901789C', N'Ivy Chen', N'2019-12-02', N'STUDENT_SERVICE', N'SC', N'1');

-- student_school_enrollments (9 rows)
INSERT INTO dbo.[student_school_enrollments] ([id], [code], [student_id], [school_id], [enrolled_from], [enrolled_to_exclusive], [status], [is_active])
VALUES
    (N'ENR-031', N'ENR-00031', N'STU-031', N'SCH-001', N'2026-01-02', NULL, N'ENROLLED', N'1'),
    (N'ENR-032', N'ENR-00032', N'STU-032', N'SCH-003', N'2026-01-29', NULL, N'ENROLLED', N'1'),
    (N'ENR-033', N'ENR-00033', N'STU-033', N'SCH-003', N'2026-01-29', NULL, N'ENROLLED', N'1'),
    (N'ENR-034', N'ENR-00034', N'STU-034', N'SCH-003', N'2026-10-12', NULL, N'ENROLLED', N'1'),
    (N'ENR-035', N'ENR-00035', N'STU-035', N'SCH-001', N'2026-01-02', NULL, N'ENROLLED', N'1'),
    (N'ENR-036', N'ENR-00036', N'STU-036', N'SCH-003', N'2026-01-29', NULL, N'ENROLLED', N'1'),
    (N'ENR-037', N'ENR-00037', N'STU-037', N'SCH-004', N'2026-01-02', NULL, N'ENROLLED', N'1'),
    (N'ENR-038', N'ENR-00038', N'STU-038', N'SCH-003', N'2026-01-29', NULL, N'ENROLLED', N'1'),
    (N'ENR-039', N'ENR-00039', N'STU-039', N'SCH-003', N'2026-10-15', NULL, N'ENROLLED', N'1');

-- student_class_assignments (9 rows)
INSERT INTO dbo.[student_class_assignments] ([id], [enrollment_id], [school_class_id], [assigned_from], [assigned_to_exclusive], [status])
VALUES
    (N'SCA-031', N'ENR-031', N'CLS-RI-S4-01', N'2026-01-02', NULL, N'ACTIVE'),
    (N'SCA-032', N'ENR-032', N'CLS-RPS-2A1', N'2026-01-29', NULL, N'ACTIVE'),
    (N'SCA-033', N'ENR-033', N'CLS-RPS-3A1', N'2026-01-29', NULL, N'ACTIVE'),
    (N'SCA-034', N'ENR-034', N'CLS-RPS-1A2', N'2026-10-12', NULL, N'ACTIVE'),
    (N'SCA-035', N'ENR-035', N'CLS-RI-JC1-01', N'2026-01-02', NULL, N'ACTIVE'),
    (N'SCA-036', N'ENR-036', N'CLS-RPS-2A2', N'2026-01-29', NULL, N'ACTIVE'),
    (N'SCA-037', N'ENR-037', N'CLS-NYPS-P1A', N'2026-01-02', NULL, N'ACTIVE'),
    (N'SCA-038', N'ENR-038', N'CLS-RPS-3A2', N'2026-01-29', NULL, N'ACTIVE'),
    (N'SCA-039', N'ENR-039', N'CLS-RPS-1A2', N'2026-10-15', NULL, N'ACTIVE');
COMMIT TRANSACTION;
GO
SELECT t.TableName, t.Actual, t.Expected, CASE WHEN t.Actual = t.Expected THEN N'OK' ELSE N'MISMATCH' END AS Result
FROM (
    SELECT N'school_level_offerings' AS TableName, (SELECT COUNT(*) FROM dbo.[school_level_offerings] WHERE [id] IN (N'SLO-RI-2026-S4')) AS Actual, 1 AS Expected
UNION ALL
    SELECT N'school_classes' AS TableName, (SELECT COUNT(*) FROM dbo.[school_classes] WHERE [id] IN (N'CLS-RI-S4-01', N'CLS-RI-JC1-01')) AS Actual, 2 AS Expected
UNION ALL
    SELECT N'students' AS TableName, (SELECT COUNT(*) FROM dbo.[students] WHERE [id] IN (N'STU-031', N'STU-032', N'STU-033', N'STU-034', N'STU-035', N'STU-036', N'STU-037', N'STU-038', N'STU-039')) AS Actual, 9 AS Expected
UNION ALL
    SELECT N'student_school_enrollments' AS TableName, (SELECT COUNT(*) FROM dbo.[student_school_enrollments] WHERE [id] IN (N'ENR-031', N'ENR-032', N'ENR-033', N'ENR-034', N'ENR-035', N'ENR-036', N'ENR-037', N'ENR-038', N'ENR-039')) AS Actual, 9 AS Expected
UNION ALL
    SELECT N'student_class_assignments' AS TableName, (SELECT COUNT(*) FROM dbo.[student_class_assignments] WHERE [id] IN (N'SCA-031', N'SCA-032', N'SCA-033', N'SCA-034', N'SCA-035', N'SCA-036', N'SCA-037', N'SCA-038', N'SCA-039')) AS Actual, 9 AS Expected
) AS t;
GO

/* ---------------------------------------------------------------------
   IAMService
   --------------------------------------------------------------------- */
USE [IAMService];
GO
BEGIN TRANSACTION;
DELETE FROM dbo.[parent_profiles] WHERE [id] IN (N'PAR-S7623418C', N'PAR-S7934526A', N'PAR-S7745213C', N'PAR-S8034172E', N'PAR-S8256341E', N'PAR-S8145627E', N'PAR-S8367512H');
DELETE FROM dbo.[user_profiles] WHERE [id] IN (N'UPF-S7623418C', N'UPF-S7934526A', N'UPF-S7745213C', N'UPF-S8034172E', N'UPF-S8256341E', N'UPF-S8145627E', N'UPF-S8367512H');
DELETE FROM dbo.[user_roles] WHERE [id] IN (N'URL-S7623418C', N'URL-S7934526A', N'URL-S7745213C', N'URL-S8034172E', N'URL-S8256341E', N'URL-S8145627E', N'URL-S8367512H');
DELETE FROM dbo.[users] WHERE [id] IN (N'USR-S7623418C', N'USR-S7934526A', N'USR-S7745213C', N'USR-S8034172E', N'USR-S8256341E', N'USR-S8145627E', N'USR-S8367512H');

-- users (7 rows)
INSERT INTO dbo.[users] ([id], [code], [school_id], [username], [email], [provider], [is_active], [is_email_verified])
VALUES
    (N'USR-S7623418C', N'USR-00020', NULL, N's7623418c', N'hoe.s7623418c@example.com', N'singpass', N'1', N'1'),
    (N'USR-S7934526A', N'USR-00021', NULL, N's7934526a', N'ling.s7934526a@example.com', N'singpass', N'1', N'1'),
    (N'USR-S7745213C', N'USR-00022', NULL, N's7745213c', N'fong.s7745213c@example.com', N'singpass', N'1', N'1'),
    (N'USR-S8034172E', N'USR-00023', NULL, N's8034172e', N'keong.s8034172e@example.com', N'singpass', N'1', N'1'),
    (N'USR-S8256341E', N'USR-00024', NULL, N's8256341e', N'lian.s8256341e@example.com', N'singpass', N'1', N'1'),
    (N'USR-S8145627E', N'USR-00025', NULL, N's8145627e', N'huat.s8145627e@example.com', N'singpass', N'1', N'1'),
    (N'USR-S8367512H', N'USR-00026', NULL, N's8367512h', N'hua.s8367512h@example.com', N'singpass', N'1', N'1');

-- user_roles (7 rows)
INSERT INTO dbo.[user_roles] ([id], [code], [user_id], [role_id], [is_active])
VALUES
    (N'URL-S7623418C', N'URL-00020', N'USR-S7623418C', N'ROL-PARENT', N'1'),
    (N'URL-S7934526A', N'URL-00021', N'USR-S7934526A', N'ROL-PARENT', N'1'),
    (N'URL-S7745213C', N'URL-00022', N'USR-S7745213C', N'ROL-PARENT', N'1'),
    (N'URL-S8034172E', N'URL-00023', N'USR-S8034172E', N'ROL-PARENT', N'1'),
    (N'URL-S8256341E', N'URL-00024', N'USR-S8256341E', N'ROL-PARENT', N'1'),
    (N'URL-S8145627E', N'URL-00025', N'USR-S8145627E', N'ROL-PARENT', N'1'),
    (N'URL-S8367512H', N'URL-00026', N'USR-S8367512H', N'ROL-PARENT', N'1');

-- user_profiles (7 rows)
INSERT INTO dbo.[user_profiles] ([id], [code], [user_id], [first_name], [last_name], [full_name], [phone_number], [gender], [birth_date], [is_active], [is_verified])
VALUES
    (N'UPF-S7623418C', N'UPF-00020', N'USR-S7623418C', N'KAH HOE', N'TAN', N'TAN KAH HOE', N'+6581234501', N'Male', N'1984-04-21', N'1', N'1'),
    (N'UPF-S7934526A', N'UPF-00021', N'USR-S7934526A', N'SIEW LING', N'LOW', N'LOW SIEW LING', N'+6581234502', N'Female', N'1986-09-03', N'1', N'1'),
    (N'UPF-S7745213C', N'UPF-00022', N'USR-S7745213C', N'MEI FONG', N'LEE', N'LEE MEI FONG', N'+6581234503', N'Female', N'1979-12-11', N'1', N'1'),
    (N'UPF-S8034172E', N'UPF-00023', N'USR-S8034172E', N'CHEE KEONG', N'NG', N'NG CHEE KEONG', N'+6581234504', N'Male', N'1987-02-17', N'1', N'1'),
    (N'UPF-S8256341E', N'UPF-00024', N'USR-S8256341E', N'BEE LIAN', N'ONG', N'ONG BEE LIAN', N'+6581234505', N'Female', N'1989-07-25', N'1', N'1'),
    (N'UPF-S8145627E', N'UPF-00025', N'USR-S8145627E', N'BOON HUAT', N'KOH', N'KOH BOON HUAT', N'+6581234506', N'Male', N'1985-11-30', N'1', N'1'),
    (N'UPF-S8367512H', N'UPF-00026', N'USR-S8367512H', N'AI HUA', N'SEAH', N'SEAH AI HUA', N'+6581234507', N'Female', N'1988-05-08', N'1', N'1');

-- parent_profiles (7 rows)
INSERT INTO dbo.[parent_profiles] ([id], [code], [user_id], [nric], [full_name], [phone_number], [email], [residential_block], [residential_street], [residential_unit], [residential_postal_code], [residential_country], [mailing_block], [mailing_street], [mailing_unit], [mailing_postal_code], [mailing_country], [is_activate])
VALUES
    (N'PAR-S7623418C', N'PAR-00011', N'USR-S7623418C', N'S7623418C', N'TAN KAH HOE', N'+6581234501', N'hoe.s7623418c@example.com', N'74', N'LORONG 4 TOA PAYOH', N'09-122', N'310074', N'SINGAPORE', NULL, NULL, NULL, NULL, NULL, N'1'),
    (N'PAR-S7934526A', N'PAR-00012', N'USR-S7934526A', N'S7934526A', N'LOW SIEW LING', N'+6581234502', N'ling.s7934526a@example.com', N'74', N'LORONG 4 TOA PAYOH', N'09-122', N'310074', N'SINGAPORE', NULL, NULL, NULL, NULL, NULL, N'1'),
    (N'PAR-S7745213C', N'PAR-00013', N'USR-S7745213C', N'S7745213C', N'LEE MEI FONG', N'+6581234503', N'fong.s7745213c@example.com', N'231', N'BISHAN STREET 22', N'11-34', N'570231', N'SINGAPORE', NULL, NULL, NULL, NULL, NULL, N'1'),
    (N'PAR-S8034172E', N'PAR-00014', N'USR-S8034172E', N'S8034172E', N'NG CHEE KEONG', N'+6581234504', N'keong.s8034172e@example.com', N'456', N'JURONG WEST STREET 41', N'07-215', N'640456', N'SINGAPORE', NULL, NULL, NULL, NULL, NULL, N'1'),
    (N'PAR-S8256341E', N'PAR-00015', N'USR-S8256341E', N'S8256341E', N'ONG BEE LIAN', N'+6581234505', N'lian.s8256341e@example.com', N'456', N'JURONG WEST STREET 41', N'07-215', N'640456', N'SINGAPORE', NULL, NULL, NULL, NULL, NULL, N'1'),
    (N'PAR-S8145627E', N'PAR-00016', N'USR-S8145627E', N'S8145627E', N'KOH BOON HUAT', N'+6581234506', N'huat.s8145627e@example.com', N'629', N'HOUGANG AVENUE 8', N'04-48', N'530629', N'SINGAPORE', NULL, NULL, NULL, NULL, NULL, N'1'),
    (N'PAR-S8367512H', N'PAR-00017', N'USR-S8367512H', N'S8367512H', N'SEAH AI HUA', N'+6581234507', N'hua.s8367512h@example.com', N'629', N'HOUGANG AVENUE 8', N'04-48', N'530629', N'SINGAPORE', NULL, NULL, NULL, NULL, NULL, N'1');
COMMIT TRANSACTION;
GO
SELECT t.TableName, t.Actual, t.Expected, CASE WHEN t.Actual = t.Expected THEN N'OK' ELSE N'MISMATCH' END AS Result
FROM (
    SELECT N'users' AS TableName, (SELECT COUNT(*) FROM dbo.[users] WHERE [id] IN (N'USR-S7623418C', N'USR-S7934526A', N'USR-S7745213C', N'USR-S8034172E', N'USR-S8256341E', N'USR-S8145627E', N'USR-S8367512H')) AS Actual, 7 AS Expected
UNION ALL
    SELECT N'user_roles' AS TableName, (SELECT COUNT(*) FROM dbo.[user_roles] WHERE [id] IN (N'URL-S7623418C', N'URL-S7934526A', N'URL-S7745213C', N'URL-S8034172E', N'URL-S8256341E', N'URL-S8145627E', N'URL-S8367512H')) AS Actual, 7 AS Expected
UNION ALL
    SELECT N'user_profiles' AS TableName, (SELECT COUNT(*) FROM dbo.[user_profiles] WHERE [id] IN (N'UPF-S7623418C', N'UPF-S7934526A', N'UPF-S7745213C', N'UPF-S8034172E', N'UPF-S8256341E', N'UPF-S8145627E', N'UPF-S8367512H')) AS Actual, 7 AS Expected
UNION ALL
    SELECT N'parent_profiles' AS TableName, (SELECT COUNT(*) FROM dbo.[parent_profiles] WHERE [id] IN (N'PAR-S7623418C', N'PAR-S7934526A', N'PAR-S7745213C', N'PAR-S8034172E', N'PAR-S8256341E', N'PAR-S8145627E', N'PAR-S8367512H')) AS Actual, 7 AS Expected
) AS t;
GO

/* ---------------------------------------------------------------------
   EducationAccountService
   --------------------------------------------------------------------- */
USE [EducationAccountService];
GO
BEGIN TRANSACTION;
DELETE FROM dbo.[wallet_transactions] WHERE [id] IN (N'WTX-032-PRI', N'WTX-036-PRI', N'WTX-038-PRI', N'WTX-038-ENR', N'WTX-031-L01', N'WTX-031-L02', N'WTX-035-L01', N'WTX-035-L02', N'WTX-032T301', N'WTX-032T302', N'WTX-032-T4P', N'WTX-012T1MISC', N'WTX-012T1SPORTS', N'WTX-012T1FIELDT', N'WTX-012T1FIELDTR', N'WTX-012T2LIBRAR', N'WTX-012T2ART', N'WTX-012T2MISC', N'WTX-012T2SPORTS', N'WTX-012T2MUSIC', N'WTX-012T2COMPUT', N'WTX-012T2MUSICR', N'WTX-012T2UNIFOR', N'WTX-012T3MISC', N'WTX-012T3SPORTS', N'WTX-012T3CAMP', N'WTX-012T3ART', N'WTX-012T3CAMPR', N'WTX-012T3LIBRAR', N'WTX-012T3FIELDT', N'WTX-012T3MUSIC', N'WTX-007T1MISC', N'WTX-007T1STATIO', N'WTX-007T1UNIFOR', N'WTX-007T2MISC', N'WTX-007T2STATIO', N'WTX-007T2CAMP', N'WTX-007T3MISC', N'WTX-007T3STATIO', N'WTX-007T3FIELDT', N'WTX-007T3LIBRAR', N'WTX-01502');
DELETE FROM dbo.[top_up_batch_items] WHERE [id] IN (N'TBI-2026-PRI-032', N'TBI-2026-PRI-036', N'TBI-2026-PRI-038', N'TBI-2026-ENR-038');
DELETE FROM dbo.[wallets] WHERE [id] IN (N'WAL-STU-031', N'WAL-STU-032', N'WAL-STU-035', N'WAL-STU-036', N'WAL-STU-037', N'WAL-STU-038', N'WAL-STU-039');
DELETE FROM dbo.[students] WHERE [id] IN (N'STU-031', N'STU-032', N'STU-033', N'STU-034', N'STU-035', N'STU-036', N'STU-037', N'STU-038', N'STU-039');

-- students (9 rows)
INSERT INTO dbo.[students] ([id], [code], [student_id], [nric], [full_name], [date_of_birth], [citizenship], [gender], [status], [race], [block], [street], [unit], [postal_code], [country], [father_nric], [mother_nric], [created_at], [created_by])
VALUES
    (N'STU-031', N'EDU-01031', N'STU-031', N'S1034578B', N'Henry Tan', N'2010-08-15', N'1', N'1', N'1', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'Singapore', N'S7623418C', N'S7934526A', N'2026-01-02T08:00:00', N'AutoEnrollService'),
    (N'STU-032', N'EDU-01032', N'STU-032', N'S1845623J', N'Megan Tan', N'2018-01-09', N'1', N'2', N'1', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'Singapore', N'S7623418C', N'S7934526A', N'2026-01-29T08:00:00', N'AutoEnrollService'),
    (N'STU-033', N'EDU-01033', N'STU-033', N'S1756234G', N'Rachel Tan', N'2017-06-12', N'2', N'2', N'1', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'Singapore', N'S7623418C', N'S7934526A', N'2026-01-29T08:00:00', N'AutoEnrollService'),
    (N'STU-034', N'EDU-01034', N'STU-034', N'S1967345F', N'Jonas Tan', N'2019-05-20', N'1', N'1', N'1', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'Singapore', N'S7623418C', N'S7934526A', N'2026-10-12T08:00:00', N'AutoEnrollService'),
    (N'STU-035', N'EDU-01035', N'STU-035', N'S0956812C', N'Jasmine Lee', N'2009-03-02', N'1', N'2', N'1', N'Chinese', N'231', N'Bishan Street 22', N'#11-34', N'570231', N'Singapore', NULL, N'S7745213C', N'2026-01-02T08:00:00', N'AutoEnrollService'),
    (N'STU-036', N'EDU-01036', N'STU-036', N'S1878456D', N'Kayden Ng', N'2018-06-21', N'1', N'1', N'1', N'Chinese', N'456', N'Jurong West Street 41', N'#07-215', N'640456', N'Singapore', N'S8034172E', N'S8256341E', N'2026-01-29T08:00:00', N'AutoEnrollService'),
    (N'STU-037', N'EDU-01037', N'STU-037', N'S1989567Z', N'Sophie Ng', N'2019-09-30', N'1', N'2', N'1', N'Chinese', N'456', N'Jurong West Street 41', N'#07-215', N'640456', N'Singapore', N'S8034172E', N'S8256341E', N'2026-01-02T08:00:00', N'AutoEnrollService'),
    (N'STU-038', N'EDU-01038', N'STU-038', N'S1790678Z', N'Zara Koh', N'2017-02-14', N'1', N'2', N'1', N'Chinese', N'629', N'Hougang Avenue 8', N'#04-48', N'530629', N'Singapore', N'S8145627E', N'S8367512H', N'2026-01-29T08:00:00', N'AutoEnrollService'),
    (N'STU-039', N'EDU-01039', N'STU-039', N'S1901789C', N'Ivy Chen', N'2019-12-02', N'1', N'2', N'1', N'Chinese', N'162', N'Serangoon North Avenue 1', N'#11-402', N'550162', N'Singapore', N'S6789012F', N'S7890123G', N'2026-10-15T08:00:00', N'AutoEnrollService');

-- wallets (7 rows)
INSERT INTO dbo.[wallets] ([id], [code], [student_id], [currency], [balance], [status], [created_at], [created_by])
VALUES
    (N'WAL-STU-031', N'WA-01031', N'STU-031', N'SGD', N'120.00', N'2', N'2022-01-03T08:00:00', N'AutoEnrollService'),
    (N'WAL-STU-032', N'WA-01032', N'STU-032', N'SGD', N'468.50', N'1', N'2026-01-29T08:00:00', N'AutoEnrollService'),
    (N'WAL-STU-035', N'WA-01035', N'STU-035', N'SGD', N'0.00', N'3', N'2022-01-03T08:00:00', N'AutoEnrollService'),
    (N'WAL-STU-036', N'WA-01036', N'STU-036', N'SGD', N'500.00', N'1', N'2026-01-29T08:00:00', N'AutoEnrollService'),
    (N'WAL-STU-037', N'WA-01037', N'STU-037', N'SGD', N'0.00', N'1', N'2026-01-02T08:00:00', N'AutoEnrollService'),
    (N'WAL-STU-038', N'WA-01038', N'STU-038', N'SGD', N'650.00', N'1', N'2026-01-29T08:00:00', N'AutoEnrollService'),
    (N'WAL-STU-039', N'WA-01039', N'STU-039', N'SGD', N'0.00', N'1', N'2026-10-15T08:00:00', N'AutoEnrollService');

-- top_up_batch_items (4 rows)
INSERT INTO dbo.[top_up_batch_items] ([id], [batch_id], [wallet_id], [student_id], [student_nric], [student_name], [amount], [status], [transaction_id], [reason_or_error], [processed_at], [created_at])
VALUES
    (N'TBI-2026-PRI-032', N'TUB-2026-PRI', N'WAL-STU-032', N'STU-032', N'S1845623J', N'Megan Tan', N'500.00', N'2', N'WTX-032-PRI', NULL, N'2026-03-02T09:00:00', N'2026-03-02'),
    (N'TBI-2026-PRI-036', N'TUB-2026-PRI', N'WAL-STU-036', N'STU-036', N'S1878456D', N'Kayden Ng', N'500.00', N'2', N'WTX-036-PRI', NULL, N'2026-03-02T09:00:00', N'2026-03-02'),
    (N'TBI-2026-PRI-038', N'TUB-2026-PRI', N'WAL-STU-038', N'STU-038', N'S1790678Z', N'Zara Koh', N'500.00', N'2', N'WTX-038-PRI', NULL, N'2026-03-02T09:00:00', N'2026-03-02'),
    (N'TBI-2026-ENR-038', N'TUB-2026-ENR', N'WAL-STU-038', N'STU-038', N'S1790678Z', N'Zara Koh', N'150.00', N'2', N'WTX-038-ENR', NULL, N'2026-07-01T09:00:00', N'2026-07-01');

-- wallet_transactions (42 rows)
INSERT INTO dbo.[wallet_transactions] ([id], [code], [reference_id], [wallet_id], [direction], [amount], [status], [description], [created_at])
VALUES
    (N'WTX-032-PRI', N'WT-01041', N'BT-TUB-2026-PRI-032', N'WAL-STU-032', N'1', N'500.00', N'2', N'[Bulk Top-Up] Campaign: Primary Education Grant 2026 (Batch: TUB-2026-PRI)', N'2026-03-02T09:00:00'),
    (N'WTX-036-PRI', N'WT-01042', N'BT-TUB-2026-PRI-036', N'WAL-STU-036', N'1', N'500.00', N'2', N'[Bulk Top-Up] Campaign: Primary Education Grant 2026 (Batch: TUB-2026-PRI)', N'2026-03-02T09:00:00'),
    (N'WTX-038-PRI', N'WT-01043', N'BT-TUB-2026-PRI-038', N'WAL-STU-038', N'1', N'500.00', N'2', N'[Bulk Top-Up] Campaign: Primary Education Grant 2026 (Batch: TUB-2026-PRI)', N'2026-03-02T09:00:00'),
    (N'WTX-038-ENR', N'WT-01044', N'BT-TUB-2026-ENR-038', N'WAL-STU-038', N'1', N'150.00', N'2', N'[Bulk Top-Up] Campaign: Upper Primary Enrichment Top-Up 2026 (Batch: TUB-2026-ENR)', N'2026-07-01T09:00:00'),
    (N'WTX-031-L01', N'WT-01045', N'LEGACY-2025-TOPUP-031', N'WAL-STU-031', N'1', N'200.00', N'2', N'[Bulk Top-Up] Campaign: Secondary Education Grant 2025 (legacy, before this system)', N'2025-03-03T09:00:00'),
    (N'WTX-031-L02', N'WT-01046', N'LEGACY-2025-FEE-031', N'WAL-STU-031', N'2', N'80.00', N'2', N'[Fee Payment] Enrichment Programme 2025 (legacy, before this system)', N'2025-07-14T09:00:00'),
    (N'WTX-035-L01', N'WT-01047', N'LEGACY-2024-TOPUP-035', N'WAL-STU-035', N'1', N'150.00', N'2', N'[Bulk Top-Up] Campaign: Secondary Education Grant 2024 (legacy, before this system)', N'2024-03-04T09:00:00'),
    (N'WTX-035-L02', N'WT-01048', N'LEGACY-2024-FEE-035', N'WAL-STU-035', N'2', N'150.00', N'2', N'[Fee Payment] Enrichment Programme 2024 (legacy, before this system)', N'2024-07-15T09:00:00'),
    (N'WTX-032T301', N'WT-01049', N'CHG-STU-032-T3-01', N'WAL-STU-032', N'2', N'19.50', N'2', N'[Fee Payment] Standard Miscellaneous Fee - Term 3 2026 (CHG-STU-032-T3-01)', N'2026-07-10T10:00:00'),
    (N'WTX-032T302', N'WT-01050', N'CHG-STU-032-T3-02', N'WAL-STU-032', N'2', N'12.00', N'2', N'[Fee Payment] Stationery Fee - Term 3 2026 (CHG-STU-032-T3-02)', N'2026-07-10T10:00:00'),
    (N'WTX-032-T4P', N'WT-01051', N'INV-STU-032-T4', N'WAL-STU-032', N'2', N'31.50', N'1', N'[Fee Payment - Pending] Term 4 2026 fees (CHG-STU-032-01, CHG-STU-032-02) - online checkout not completed', N'2026-10-25T10:00:00'),
    (N'WTX-012T1MISC', N'WT-01052', N'CHG-STU-012-T1-MISC', N'WAL-STU-012', N'2', N'19.50', N'2', N'[Fee Payment] Standard Miscellaneous Fee - Term 1 2026 (CHG-STU-012-T1-MISC)', N'2026-03-05T10:00:00'),
    (N'WTX-012T1SPORTS', N'WT-01053', N'CHG-STU-012-T1-SPORTS', N'WAL-STU-012', N'2', N'25.00', N'2', N'[Fee Payment] Sports Fee - Term 1 2026 (CHG-STU-012-T1-SPORTS)', N'2026-03-05T10:00:00'),
    (N'WTX-012T1FIELDT', N'WT-01054', N'CHG-STU-012-T1-FIELDT', N'WAL-STU-012', N'2', N'45.00', N'2', N'[Fee Payment] Field Trip Fee - Term 1 2026 (CHG-STU-012-T1-FIELDT)', N'2026-03-12T10:00:00'),
    (N'WTX-012T1FIELDTR', N'WT-01055', N'RF-CHG-STU-012-T1-FIELDT', N'WAL-STU-012', N'1', N'45.00', N'2', N'[Refund] Field Trip Fee - Term 1 2026 - trip cancelled, full refund (CHG-STU-012-T1-FIELDT)', N'2026-03-26T15:00:00'),
    (N'WTX-012T2LIBRAR', N'WT-01056', N'CHG-STU-012-T2-LIBRAR', N'WAL-STU-012', N'2', N'8.00', N'2', N'[Fee Payment] Library Fee - Term 2 2026 (CHG-STU-012-T2-LIBRAR)', N'2026-04-02T10:00:00'),
    (N'WTX-012T2ART', N'WT-01057', N'CHG-STU-012-T2-ART', N'WAL-STU-012', N'2', N'15.00', N'2', N'[Fee Payment] Art Supplies Fee - Term 2 2026 (CHG-STU-012-T2-ART)', N'2026-04-02T10:00:00'),
    (N'WTX-012T2MISC', N'WT-01058', N'CHG-STU-012-T2-MISC', N'WAL-STU-012', N'2', N'19.50', N'2', N'[Fee Payment] Standard Miscellaneous Fee - Term 2 2026 (CHG-STU-012-T2-MISC)', N'2026-04-06T10:00:00'),
    (N'WTX-012T2SPORTS', N'WT-01059', N'CHG-STU-012-T2-SPORTS', N'WAL-STU-012', N'2', N'25.00', N'2', N'[Fee Payment] Sports Fee - Term 2 2026 (CHG-STU-012-T2-SPORTS)', N'2026-04-06T10:00:00'),
    (N'WTX-012T2MUSIC', N'WT-01060', N'CHG-STU-012-T2-MUSIC', N'WAL-STU-012', N'2', N'30.00', N'2', N'[Fee Payment] Music Fee - Term 2 2026 (CHG-STU-012-T2-MUSIC)', N'2026-04-20T10:00:00'),
    (N'WTX-012T2COMPUT', N'WT-01061', N'CHG-STU-012-T2-COMPUT', N'WAL-STU-012', N'2', N'18.00', N'2', N'[Fee Payment] Computer Lab Fee - Term 2 2026 (CHG-STU-012-T2-COMPUT)', N'2026-05-04T10:00:00'),
    (N'WTX-012T2MUSICR', N'WT-01062', N'RF-CHG-STU-012-T2-MUSIC', N'WAL-STU-012', N'1', N'10.00', N'2', N'[Refund] Music Fee - Term 2 2026 - 2 lessons cancelled, part refund (CHG-STU-012-T2-MUSIC)', N'2026-05-18T15:00:00'),
    (N'WTX-012T2UNIFOR', N'WT-01063', N'CHG-STU-012-T2-UNIFOR', N'WAL-STU-012', N'2', N'60.00', N'2', N'[Fee Payment] Uniform Fee - Term 2 2026 (CHG-STU-012-T2-UNIFOR)', N'2026-06-01T10:00:00'),
    (N'WTX-012T3MISC', N'WT-01064', N'CHG-STU-012-T3-MISC', N'WAL-STU-012', N'2', N'19.50', N'2', N'[Fee Payment] Standard Miscellaneous Fee - Term 3 2026 (CHG-STU-012-T3-MISC)', N'2026-07-06T10:00:00'),
    (N'WTX-012T3SPORTS', N'WT-01065', N'CHG-STU-012-T3-SPORTS', N'WAL-STU-012', N'2', N'25.00', N'2', N'[Fee Payment] Sports Fee - Term 3 2026 (CHG-STU-012-T3-SPORTS)', N'2026-07-06T10:00:00'),
    (N'WTX-012T3CAMP', N'WT-01066', N'CHG-STU-012-T3-CAMP', N'WAL-STU-012', N'2', N'85.00', N'2', N'[Fee Payment] Annual Camp Fee - Term 3 2026 (CHG-STU-012-T3-CAMP)', N'2026-07-15T10:00:00'),
    (N'WTX-012T3ART', N'WT-01067', N'CHG-STU-012-T3-ART', N'WAL-STU-012', N'2', N'15.00', N'2', N'[Fee Payment] Art Supplies Fee - Term 3 2026 (CHG-STU-012-T3-ART)', N'2026-07-22T10:00:00'),
    (N'WTX-012T3CAMPR', N'WT-01068', N'RF-CHG-STU-012-T3-CAMP', N'WAL-STU-012', N'1', N'20.00', N'2', N'[Refund] Annual Camp Fee - Term 3 2026 - meal portion refunded (CHG-STU-012-T3-CAMP)', N'2026-07-29T15:00:00'),
    (N'WTX-012T3LIBRAR', N'WT-01069', N'CHG-STU-012-T3-LIBRAR', N'WAL-STU-012', N'2', N'8.00', N'2', N'[Fee Payment] Library Fee - Term 3 2026 (CHG-STU-012-T3-LIBRAR)', N'2026-09-07T10:00:00'),
    (N'WTX-012T3FIELDT', N'WT-01070', N'CHG-STU-012-T3-FIELDT', N'WAL-STU-012', N'2', N'35.00', N'2', N'[Fee Payment] Field Trip Fee - Term 3 2026 (CHG-STU-012-T3-FIELDT)', N'2026-09-14T10:00:00'),
    (N'WTX-012T3MUSIC', N'WT-01071', N'CHG-STU-012-T3-MUSIC', N'WAL-STU-012', N'2', N'30.00', N'2', N'[Fee Payment] Music Fee - Term 3 2026 (CHG-STU-012-T3-MUSIC)', N'2026-09-28T10:00:00'),
    (N'WTX-007T1MISC', N'WT-01072', N'CHG-STU-007-T1-MISC', N'WAL-STU-007', N'2', N'19.50', N'2', N'[Fee Payment] Standard Miscellaneous Fee - Term 1 2026 (CHG-STU-007-T1-MISC)', N'2026-03-05T10:00:00'),
    (N'WTX-007T1STATIO', N'WT-01073', N'CHG-STU-007-T1-STATIO', N'WAL-STU-007', N'2', N'12.00', N'2', N'[Fee Payment] Stationery Fee - Term 1 2026 (CHG-STU-007-T1-STATIO)', N'2026-03-05T10:00:00'),
    (N'WTX-007T1UNIFOR', N'WT-01074', N'CHG-STU-007-T1-UNIFOR', N'WAL-STU-007', N'2', N'120.00', N'2', N'[Fee Payment] Uniform Fee - Term 1 2026 (CHG-STU-007-T1-UNIFOR)', N'2026-03-09T10:00:00'),
    (N'WTX-007T2MISC', N'WT-01075', N'CHG-STU-007-T2-MISC', N'WAL-STU-007', N'2', N'19.50', N'2', N'[Fee Payment] Standard Miscellaneous Fee - Term 2 2026 (CHG-STU-007-T2-MISC)', N'2026-04-06T10:00:00'),
    (N'WTX-007T2STATIO', N'WT-01076', N'CHG-STU-007-T2-STATIO', N'WAL-STU-007', N'2', N'12.00', N'2', N'[Fee Payment] Stationery Fee - Term 2 2026 (CHG-STU-007-T2-STATIO)', N'2026-04-06T10:00:00'),
    (N'WTX-007T2CAMP', N'WT-01077', N'CHG-STU-007-T2-CAMP', N'WAL-STU-007', N'2', N'180.00', N'2', N'[Fee Payment] Annual Camp Fee - Term 2 2026 (CHG-STU-007-T2-CAMP)', N'2026-05-11T10:00:00'),
    (N'WTX-007T3MISC', N'WT-01078', N'CHG-STU-007-T3-MISC', N'WAL-STU-007', N'2', N'19.50', N'2', N'[Fee Payment] Standard Miscellaneous Fee - Term 3 2026 (CHG-STU-007-T3-MISC)', N'2026-07-06T10:00:00'),
    (N'WTX-007T3STATIO', N'WT-01079', N'CHG-STU-007-T3-STATIO', N'WAL-STU-007', N'2', N'12.00', N'2', N'[Fee Payment] Stationery Fee - Term 3 2026 (CHG-STU-007-T3-STATIO)', N'2026-07-06T10:00:00'),
    (N'WTX-007T3FIELDT', N'WT-01080', N'CHG-STU-007-T3-FIELDT', N'WAL-STU-007', N'2', N'60.00', N'2', N'[Fee Payment] Field Trip Fee - Term 3 2026 (CHG-STU-007-T3-FIELDT)', N'2026-08-17T10:00:00'),
    (N'WTX-007T3LIBRAR', N'WT-01081', N'CHG-STU-007-T3-LIBRAR', N'WAL-STU-007', N'2', N'5.50', N'2', N'[Fee Payment] Library Fee - Term 3 2026 (CHG-STU-007-T3-LIBRAR)', N'2026-09-07T10:00:00'),
    (N'WTX-01502', N'WT-01082', N'CHG-STU-015-02', N'WAL-STU-015', N'2', N'12.00', N'2', N'[Fee Payment] Stationery Fee - Term 4 2026 (CHG-STU-015-02)', N'2026-10-05T10:00:00');

-- Updates to existing rows
-- 3 new Rosyth students (Megan Tan, Kayden Ng, Zara Koh) added to the batch (GAP-04, GAP-08, GAP-11)
UPDATE dbo.[top_up_batches] SET [total_targeted_accounts] = N'33', [success_count] = N'33', [total_disbursed_amount] = N'16500.00' WHERE [id] = N'TUB-2026-PRI';
-- Zara Koh (P3) added to the batch (GAP-11)
UPDATE dbo.[top_up_batches] SET [total_targeted_accounts] = N'11', [success_count] = N'11', [total_disbursed_amount] = N'1650.00' WHERE [id] = N'TUB-2026-ENR';
-- Fee payments added so the EA balance is SGD 40.00 for UAT-026/027 (GAP-12)
UPDATE dbo.[wallets] SET [balance] = N'40.00' WHERE [id] = N'WAL-STU-007';
-- 20 fee payment / refund rows added (22 rows total) (GAP-05)
UPDATE dbo.[wallets] SET [balance] = N'242.50' WHERE [id] = N'WAL-STU-012';
-- Term 4 stationery paid from EA (GAP-12)
UPDATE dbo.[wallets] SET [balance] = N'488.00' WHERE [id] = N'WAL-STU-015';
COMMIT TRANSACTION;
GO
SELECT t.TableName, t.Actual, t.Expected, CASE WHEN t.Actual = t.Expected THEN N'OK' ELSE N'MISMATCH' END AS Result
FROM (
    SELECT N'students' AS TableName, (SELECT COUNT(*) FROM dbo.[students] WHERE [id] IN (N'STU-031', N'STU-032', N'STU-033', N'STU-034', N'STU-035', N'STU-036', N'STU-037', N'STU-038', N'STU-039')) AS Actual, 9 AS Expected
UNION ALL
    SELECT N'wallets' AS TableName, (SELECT COUNT(*) FROM dbo.[wallets] WHERE [id] IN (N'WAL-STU-031', N'WAL-STU-032', N'WAL-STU-035', N'WAL-STU-036', N'WAL-STU-037', N'WAL-STU-038', N'WAL-STU-039')) AS Actual, 7 AS Expected
UNION ALL
    SELECT N'top_up_batch_items' AS TableName, (SELECT COUNT(*) FROM dbo.[top_up_batch_items] WHERE [id] IN (N'TBI-2026-PRI-032', N'TBI-2026-PRI-036', N'TBI-2026-PRI-038', N'TBI-2026-ENR-038')) AS Actual, 4 AS Expected
UNION ALL
    SELECT N'wallet_transactions' AS TableName, (SELECT COUNT(*) FROM dbo.[wallet_transactions] WHERE [id] IN (N'WTX-032-PRI', N'WTX-036-PRI', N'WTX-038-PRI', N'WTX-038-ENR', N'WTX-031-L01', N'WTX-031-L02', N'WTX-035-L01', N'WTX-035-L02', N'WTX-032T301', N'WTX-032T302', N'WTX-032-T4P', N'WTX-012T1MISC', N'WTX-012T1SPORTS', N'WTX-012T1FIELDT', N'WTX-012T1FIELDTR', N'WTX-012T2LIBRAR', N'WTX-012T2ART', N'WTX-012T2MISC', N'WTX-012T2SPORTS', N'WTX-012T2MUSIC', N'WTX-012T2COMPUT', N'WTX-012T2MUSICR', N'WTX-012T2UNIFOR', N'WTX-012T3MISC', N'WTX-012T3SPORTS', N'WTX-012T3CAMP', N'WTX-012T3ART', N'WTX-012T3CAMPR', N'WTX-012T3LIBRAR', N'WTX-012T3FIELDT', N'WTX-012T3MUSIC', N'WTX-007T1MISC', N'WTX-007T1STATIO', N'WTX-007T1UNIFOR', N'WTX-007T2MISC', N'WTX-007T2STATIO', N'WTX-007T2CAMP', N'WTX-007T3MISC', N'WTX-007T3STATIO', N'WTX-007T3FIELDT', N'WTX-007T3LIBRAR', N'WTX-01502')) AS Actual, 42 AS Expected
) AS t;
GO

/* ---------------------------------------------------------------------
   BillingPaymentService
   --------------------------------------------------------------------- */
USE [BillingPaymentService];
GO
BEGIN TRANSACTION;
DELETE FROM dbo.[student_charges] WHERE [id] IN (N'CHG-STU-032-01', N'CHG-STU-032-02', N'CHG-STU-033-01', N'CHG-STU-033-02', N'CHG-STU-034-01', N'CHG-STU-034-02', N'CHG-STU-036-01', N'CHG-STU-036-02', N'CHG-STU-037-01', N'CHG-STU-037-02', N'CHG-STU-038-01', N'CHG-STU-038-02', N'CHG-STU-039-01', N'CHG-STU-039-02', N'CHG-STU-032-T3-01', N'CHG-STU-032-T3-02', N'CHG-STU-012-T1-MISC', N'CHG-STU-012-T1-SPORTS', N'CHG-STU-012-T1-FIELDT', N'CHG-STU-012-T2-LIBRAR', N'CHG-STU-012-T2-ART', N'CHG-STU-012-T2-MISC', N'CHG-STU-012-T2-SPORTS', N'CHG-STU-012-T2-MUSIC', N'CHG-STU-012-T2-COMPUT', N'CHG-STU-012-T2-UNIFOR', N'CHG-STU-012-T3-MISC', N'CHG-STU-012-T3-SPORTS', N'CHG-STU-012-T3-CAMP', N'CHG-STU-012-T3-ART', N'CHG-STU-012-T3-LIBRAR', N'CHG-STU-012-T3-FIELDT', N'CHG-STU-012-T3-MUSIC', N'CHG-STU-007-T1-MISC', N'CHG-STU-007-T1-STATIO', N'CHG-STU-007-T1-UNIFOR', N'CHG-STU-007-T2-MISC', N'CHG-STU-007-T2-STATIO', N'CHG-STU-007-T2-CAMP', N'CHG-STU-007-T3-MISC', N'CHG-STU-007-T3-STATIO', N'CHG-STU-007-T3-FIELDT', N'CHG-STU-007-T3-LIBRAR', N'CHG-STU-007-OLT-01', N'CHG-STU-015-OLT-01');

-- student_charges (45 rows)
INSERT INTO dbo.[student_charges] ([id], [student_id], [enrollment_id], [school_id], [academic_year_id], [academic_level_id], [school_class_id], [student_category_snapshot], [fee_component_id], [fee_component_name_snapshot], [amount], [tax_amount], [total_amount], [charge_date], [due_date], [status])
VALUES
    (N'CHG-STU-032-01', N'STU-032', N'ENR-032', N'SCH-003', N'AY-2026', N'AL-P2', N'CLS-RPS-2A1', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 4 2026', N'19.50', N'0.00', N'19.50', N'2026-10-01', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-032-02', N'STU-032', N'ENR-032', N'SCH-003', N'AY-2026', N'AL-P2', N'CLS-RPS-2A1', N'SC', N'ffff0004-0000-0000-0000-000000000001', N'Stationery Fee - Term 4 2026', N'12.00', N'0.00', N'12.00', N'2026-10-01', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-033-01', N'STU-033', N'ENR-033', N'SCH-003', N'AY-2026', N'AL-P3', N'CLS-RPS-3A1', N'PR', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 4 2026', N'19.50', N'1.76', N'21.26', N'2026-10-01', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-033-02', N'STU-033', N'ENR-033', N'SCH-003', N'AY-2026', N'AL-P3', N'CLS-RPS-3A1', N'PR', N'ffff0004-0000-0000-0000-000000000003', N'Sports Fee - Term 4 2026', N'25.00', N'2.25', N'27.25', N'2026-10-01', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-034-01', N'STU-034', N'ENR-034', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A2', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 4 2026', N'19.50', N'0.00', N'19.50', N'2026-10-12', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-034-02', N'STU-034', N'ENR-034', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A2', N'SC', N'ffff0004-0000-0000-0000-000000000001', N'Stationery Fee - Term 4 2026', N'12.00', N'0.00', N'12.00', N'2026-10-12', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-036-01', N'STU-036', N'ENR-036', N'SCH-003', N'AY-2026', N'AL-P2', N'CLS-RPS-2A2', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 4 2026', N'19.50', N'0.00', N'19.50', N'2026-10-01', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-036-02', N'STU-036', N'ENR-036', N'SCH-003', N'AY-2026', N'AL-P2', N'CLS-RPS-2A2', N'SC', N'ffff0004-0000-0000-0000-000000000001', N'Stationery Fee - Term 4 2026', N'12.00', N'0.00', N'12.00', N'2026-10-01', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-037-01', N'STU-037', N'ENR-037', N'SCH-004', N'AY-2026', N'AL-P1', N'CLS-NYPS-P1A', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 4 2026', N'19.50', N'0.00', N'19.50', N'2026-10-01', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-037-02', N'STU-037', N'ENR-037', N'SCH-004', N'AY-2026', N'AL-P1', N'CLS-NYPS-P1A', N'SC', N'ffff0004-0000-0000-0000-000000000001', N'Stationery Fee - Term 4 2026', N'12.00', N'0.00', N'12.00', N'2026-10-01', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-038-01', N'STU-038', N'ENR-038', N'SCH-003', N'AY-2026', N'AL-P3', N'CLS-RPS-3A2', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 4 2026', N'19.50', N'0.00', N'19.50', N'2026-10-01', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-038-02', N'STU-038', N'ENR-038', N'SCH-003', N'AY-2026', N'AL-P3', N'CLS-RPS-3A2', N'SC', N'ffff0004-0000-0000-0000-000000000003', N'Sports Fee - Term 4 2026', N'25.00', N'0.00', N'25.00', N'2026-10-01', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-039-01', N'STU-039', N'ENR-039', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A2', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 4 2026', N'19.50', N'0.00', N'19.50', N'2026-10-15', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-039-02', N'STU-039', N'ENR-039', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A2', N'SC', N'ffff0004-0000-0000-0000-000000000001', N'Stationery Fee - Term 4 2026', N'12.00', N'0.00', N'12.00', N'2026-10-15', N'2026-11-30', N'POSTED'),
    (N'CHG-STU-032-T3-01', N'STU-032', N'ENR-032', N'SCH-003', N'AY-2026', N'AL-P2', N'CLS-RPS-2A1', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 3 2026', N'19.50', N'0.00', N'19.50', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-032-T3-02', N'STU-032', N'ENR-032', N'SCH-003', N'AY-2026', N'AL-P2', N'CLS-RPS-2A1', N'SC', N'ffff0004-0000-0000-0000-000000000001', N'Stationery Fee - Term 3 2026', N'12.00', N'0.00', N'12.00', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-012-T1-MISC', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 1 2026', N'19.50', N'0.00', N'19.50', N'2026-01-05', N'2026-03-31', N'PAID'),
    (N'CHG-STU-012-T1-SPORTS', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000003', N'Sports Fee - Term 1 2026', N'25.00', N'0.00', N'25.00', N'2026-01-05', N'2026-03-31', N'PAID'),
    (N'CHG-STU-012-T1-FIELDT', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000002', N'Field Trip Fee - Term 1 2026', N'45.00', N'0.00', N'45.00', N'2026-01-05', N'2026-03-31', N'REFUNDED'),
    (N'CHG-STU-012-T2-LIBRAR', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000004', N'Library Fee - Term 2 2026', N'8.00', N'0.00', N'8.00', N'2026-03-30', N'2026-04-30', N'PAID'),
    (N'CHG-STU-012-T2-ART', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000005', N'Art Supplies Fee - Term 2 2026', N'15.00', N'0.00', N'15.00', N'2026-03-30', N'2026-04-30', N'PAID'),
    (N'CHG-STU-012-T2-MISC', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 2 2026', N'19.50', N'0.00', N'19.50', N'2026-03-30', N'2026-04-30', N'PAID'),
    (N'CHG-STU-012-T2-SPORTS', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000003', N'Sports Fee - Term 2 2026', N'25.00', N'0.00', N'25.00', N'2026-03-30', N'2026-04-30', N'PAID'),
    (N'CHG-STU-012-T2-MUSIC', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000006', N'Music Fee - Term 2 2026', N'30.00', N'0.00', N'30.00', N'2026-03-30', N'2026-04-30', N'PAID'),
    (N'CHG-STU-012-T2-COMPUT', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000007', N'Computer Lab Fee - Term 2 2026', N'18.00', N'0.00', N'18.00', N'2026-03-30', N'2026-04-30', N'PAID'),
    (N'CHG-STU-012-T2-UNIFOR', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000008', N'Uniform Fee - Term 2 2026', N'60.00', N'0.00', N'60.00', N'2026-03-30', N'2026-04-30', N'PAID'),
    (N'CHG-STU-012-T3-MISC', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 3 2026', N'19.50', N'0.00', N'19.50', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-012-T3-SPORTS', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000003', N'Sports Fee - Term 3 2026', N'25.00', N'0.00', N'25.00', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-012-T3-CAMP', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000010', N'Annual Camp Fee - Term 3 2026', N'85.00', N'0.00', N'85.00', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-012-T3-ART', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000005', N'Art Supplies Fee - Term 3 2026', N'15.00', N'0.00', N'15.00', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-012-T3-LIBRAR', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000004', N'Library Fee - Term 3 2026', N'8.00', N'0.00', N'8.00', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-012-T3-FIELDT', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000002', N'Field Trip Fee - Term 3 2026', N'35.00', N'0.00', N'35.00', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-012-T3-MUSIC', N'STU-012', N'ENR-012', N'SCH-003', N'AY-2026', N'AL-P4', N'CLS-RPS-4A3', N'SC', N'ffff0004-0000-0000-0000-000000000006', N'Music Fee - Term 3 2026', N'30.00', N'0.00', N'30.00', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-007-T1-MISC', N'STU-007', N'ENR-007', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A1', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 1 2026', N'19.50', N'0.00', N'19.50', N'2026-01-05', N'2026-03-31', N'PAID'),
    (N'CHG-STU-007-T1-STATIO', N'STU-007', N'ENR-007', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A1', N'SC', N'ffff0004-0000-0000-0000-000000000001', N'Stationery Fee - Term 1 2026', N'12.00', N'0.00', N'12.00', N'2026-01-05', N'2026-03-31', N'PAID'),
    (N'CHG-STU-007-T1-UNIFOR', N'STU-007', N'ENR-007', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A1', N'SC', N'ffff0004-0000-0000-0000-000000000008', N'Uniform Fee - Term 1 2026', N'120.00', N'0.00', N'120.00', N'2026-01-05', N'2026-03-31', N'PAID'),
    (N'CHG-STU-007-T2-MISC', N'STU-007', N'ENR-007', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A1', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 2 2026', N'19.50', N'0.00', N'19.50', N'2026-03-30', N'2026-04-30', N'PAID'),
    (N'CHG-STU-007-T2-STATIO', N'STU-007', N'ENR-007', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A1', N'SC', N'ffff0004-0000-0000-0000-000000000001', N'Stationery Fee - Term 2 2026', N'12.00', N'0.00', N'12.00', N'2026-03-30', N'2026-04-30', N'PAID'),
    (N'CHG-STU-007-T2-CAMP', N'STU-007', N'ENR-007', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A1', N'SC', N'ffff0004-0000-0000-0000-000000000010', N'Annual Camp Fee - Term 2 2026', N'180.00', N'0.00', N'180.00', N'2026-03-30', N'2026-04-30', N'PAID'),
    (N'CHG-STU-007-T3-MISC', N'STU-007', N'ENR-007', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A1', N'SC', N'ffff0001-0000-0000-0000-000000000002', N'Standard Miscellaneous Fee - Term 3 2026', N'19.50', N'0.00', N'19.50', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-007-T3-STATIO', N'STU-007', N'ENR-007', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A1', N'SC', N'ffff0004-0000-0000-0000-000000000001', N'Stationery Fee - Term 3 2026', N'12.00', N'0.00', N'12.00', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-007-T3-FIELDT', N'STU-007', N'ENR-007', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A1', N'SC', N'ffff0004-0000-0000-0000-000000000002', N'Field Trip Fee - Term 3 2026', N'60.00', N'0.00', N'60.00', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-007-T3-LIBRAR', N'STU-007', N'ENR-007', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A1', N'SC', N'ffff0004-0000-0000-0000-000000000004', N'Library Fee - Term 3 2026', N'5.50', N'0.00', N'5.50', N'2026-06-29', N'2026-07-31', N'PAID'),
    (N'CHG-STU-007-OLT-01', N'STU-007', N'ENR-007', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A1', N'SC', N'ffff0004-0000-0000-0000-000000000009', N'Overseas Learning Trip Fee - Term 4 2026', N'100.00', N'0.00', N'100.00', N'2026-10-26', N'2026-12-15', N'POSTED'),
    (N'CHG-STU-015-OLT-01', N'STU-015', N'ENR-015', N'SCH-003', N'AY-2026', N'AL-P1', N'CLS-RPS-1A2', N'SC', N'ffff0004-0000-0000-0000-000000000009', N'Overseas Learning Trip Fee - Term 4 2026', N'100.00', N'0.00', N'100.00', N'2026-10-26', N'2026-12-15', N'POSTED');

-- Updates to existing rows
-- Isaac paid his Term 4 stationery from EA, so Need to pay = 60.00 after the 40% subsidy (GAP-12)
UPDATE dbo.[student_charges] SET [status] = N'PAID' WHERE [id] = N'CHG-STU-015-02';
COMMIT TRANSACTION;
GO
SELECT t.TableName, t.Actual, t.Expected, CASE WHEN t.Actual = t.Expected THEN N'OK' ELSE N'MISMATCH' END AS Result
FROM (
    SELECT N'student_charges' AS TableName, (SELECT COUNT(*) FROM dbo.[student_charges] WHERE [id] IN (N'CHG-STU-032-01', N'CHG-STU-032-02', N'CHG-STU-033-01', N'CHG-STU-033-02', N'CHG-STU-034-01', N'CHG-STU-034-02', N'CHG-STU-036-01', N'CHG-STU-036-02', N'CHG-STU-037-01', N'CHG-STU-037-02', N'CHG-STU-038-01', N'CHG-STU-038-02', N'CHG-STU-039-01', N'CHG-STU-039-02', N'CHG-STU-032-T3-01', N'CHG-STU-032-T3-02', N'CHG-STU-012-T1-MISC', N'CHG-STU-012-T1-SPORTS', N'CHG-STU-012-T1-FIELDT', N'CHG-STU-012-T2-LIBRAR', N'CHG-STU-012-T2-ART', N'CHG-STU-012-T2-MISC', N'CHG-STU-012-T2-SPORTS', N'CHG-STU-012-T2-MUSIC', N'CHG-STU-012-T2-COMPUT', N'CHG-STU-012-T2-UNIFOR', N'CHG-STU-012-T3-MISC', N'CHG-STU-012-T3-SPORTS', N'CHG-STU-012-T3-CAMP', N'CHG-STU-012-T3-ART', N'CHG-STU-012-T3-LIBRAR', N'CHG-STU-012-T3-FIELDT', N'CHG-STU-012-T3-MUSIC', N'CHG-STU-007-T1-MISC', N'CHG-STU-007-T1-STATIO', N'CHG-STU-007-T1-UNIFOR', N'CHG-STU-007-T2-MISC', N'CHG-STU-007-T2-STATIO', N'CHG-STU-007-T2-CAMP', N'CHG-STU-007-T3-MISC', N'CHG-STU-007-T3-STATIO', N'CHG-STU-007-T3-FIELDT', N'CHG-STU-007-T3-LIBRAR', N'CHG-STU-007-OLT-01', N'CHG-STU-015-OLT-01')) AS Actual, 45 AS Expected
) AS t;
GO

/* ---------------------------------------------------------------------
   FASService
   --------------------------------------------------------------------- */
USE [FASService];
GO
BEGIN TRANSACTION;
DELETE FROM dbo.[sbfas_scheme_applications] WHERE [id] IN (N'SSA-KOH-2026', N'SSA-SMITH-2026');
DELETE FROM dbo.[beneficiaries] WHERE [id] IN (N'BEN-TAN-01', N'BEN-TAN-02', N'BEN-TAN-03', N'BEN-KOH-01');
DELETE FROM dbo.[family_members] WHERE [id] IN (N'FMB-TAN-01', N'FMB-TAN-02', N'FMB-KOH-01', N'FMB-KOH-02');
DELETE FROM dbo.[applicants] WHERE [id] IN (N'APL-TAN-2026', N'APL-KOH-2026');
DELETE FROM dbo.[applications] WHERE [id] IN (N'APP-TAN-2026', N'APP-KOH-2026');
DELETE FROM dbo.[sbfas_scheme_subsidies] WHERE [id] IN (N'SBF-SUB-RPS-P1-9');
DELETE FROM dbo.[moe_fas_scheme_subsidies] WHERE [id] IN (N'MOE-SUB-007');

-- moe_fas_scheme_subsidies (1 rows)
INSERT INTO dbo.[moe_fas_scheme_subsidies] ([id], [code], [moe_scheme_id], [education_stage], [fee_component_id], [subsidy_percentage], [created_at])
VALUES
    (N'MOE-SUB-007', N'MSUB-00007', N'MOE-SCH-2026', N'PRIMARY', N'ffff0004-0000-0000-0000-000000000009', N'40.00', N'2026-01-01T00:00:00');

-- sbfas_scheme_subsidies (1 rows)
INSERT INTO dbo.[sbfas_scheme_subsidies] ([id], [code], [scheme_id], [academic_level_id], [fee_component_id], [subsidy_percentage], [created_at])
VALUES
    (N'SBF-SUB-RPS-P1-9', N'SSUB-01109', N'SBFAS-SCH-RPS-2026', N'AL-P1', N'ffff0004-0000-0000-0000-000000000009', N'40.00', N'2026-01-01T00:00:00');

-- applications (2 rows)
INSERT INTO dbo.[applications] ([id], [code], [status], [calculated_ghi], [calculated_pci], [evaluation_window_months], [evaluation_result], [moe_officer_code], [moe_signature], [moe_action_at], [current_state_entered_at], [submitted_at], [created_at])
VALUES
    (N'APP-TAN-2026', N'APP-01007', N'SUBMITTED', NULL, NULL, N'12', NULL, NULL, NULL, NULL, N'2026-10-22T09:40:00', N'2026-10-22T09:40:00', N'2026-10-22T09:40:00'),
    (N'APP-KOH-2026', N'APP-01008', N'SCHOOL_APPROVED', N'4600.00', N'1533.33', N'12', N'FAIL', NULL, NULL, NULL, N'2026-10-20T15:00:00', N'2026-10-14T08:15:00', N'2026-10-14T08:15:00');

-- applicants (2 rows)
INSERT INTO dbo.[applicants] ([id], [code], [application_id], [full_name], [nric], [date_of_birth], [gender], [nationality], [race], [relationship_to_beneficiary], [phone_number], [email], [address], [commitment_agreed], [forward_to_school_agreed], [created_at])
VALUES
    (N'APL-TAN-2026', N'APL-01007', N'APP-TAN-2026', N'Tan Kah Hoe', N'S7623418C', N'1984-04-21', N'MALE', N'SC', N'CHINESE', N'FATHER', N'+6581234501', N'hoe.s7623418c@example.com', N'Blk 74 Lorong 4 Toa Payoh #09-122 Singapore 310074', N'1', N'1', N'2026-10-22T09:40:00'),
    (N'APL-KOH-2026', N'APL-01008', N'APP-KOH-2026', N'Koh Boon Huat', N'S8145627E', N'1985-11-30', N'MALE', N'SC', N'CHINESE', N'FATHER', N'+6581234506', N'huat.s8145627e@example.com', N'Blk 629 Hougang Avenue 8 #04-48 Singapore 530629', N'1', N'1', N'2026-10-14T08:15:00');

-- family_members (4 rows)
INSERT INTO dbo.[family_members] ([id], [code], [application_id], [full_name], [nric], [date_of_birth], [gender], [has_income], [income_verified], [income_amount], [created_at])
VALUES
    (N'FMB-TAN-01', N'FMB-01011', N'APP-TAN-2026', N'Tan Kah Hoe', N'S7623418C', N'1984-04-21', N'MALE', N'1', N'1', N'3900.00', N'2026-10-22T09:40:00'),
    (N'FMB-TAN-02', N'FMB-01012', N'APP-TAN-2026', N'Low Siew Ling', N'S7934526A', N'1986-09-03', N'FEMALE', N'1', N'1', N'1300.00', N'2026-10-22T09:40:00'),
    (N'FMB-KOH-01', N'FMB-01013', N'APP-KOH-2026', N'Koh Boon Huat', N'S8145627E', N'1985-11-30', N'MALE', N'1', N'1', N'4600.00', N'2026-10-14T08:15:00'),
    (N'FMB-KOH-02', N'FMB-01014', N'APP-KOH-2026', N'Seah Ai Hua', N'S8367512H', N'1988-05-08', N'FEMALE', N'0', N'0', N'0.00', N'2026-10-14T08:15:00');

-- beneficiaries (4 rows)
INSERT INTO dbo.[beneficiaries] ([id], [code], [application_id], [full_name], [nric], [date_of_birth], [gender], [school_name], [class_level], [grade], [resolved_school_code], [academic_level_id], [resolved_at], [created_at])
VALUES
    (N'BEN-TAN-01', N'BEN-01014', N'APP-TAN-2026', N'Megan Tan', N'S1845623J', N'2018-01-09', N'FEMALE', N'Rosyth Primary School', N'PRIMARY', N'Primary 2', N'RPS-0201', N'AL-P2', N'2026-10-22T09:40:00', N'2026-10-22T09:40:00'),
    (N'BEN-TAN-02', N'BEN-01015', N'APP-TAN-2026', N'Rachel Tan', N'S1756234G', N'2017-06-12', N'FEMALE', N'Rosyth Primary School', N'PRIMARY', N'Primary 3', N'RPS-0201', N'AL-P3', N'2026-10-22T09:40:00', N'2026-10-22T09:40:00'),
    (N'BEN-TAN-03', N'BEN-01016', N'APP-TAN-2026', N'Jonas Tan', N'S1967345F', N'2019-05-20', N'MALE', N'Rosyth Primary School', N'PRIMARY', N'Primary 1', N'RPS-0201', N'AL-P1', N'2026-10-22T09:40:00', N'2026-10-22T09:40:00'),
    (N'BEN-KOH-01', N'BEN-01017', N'APP-KOH-2026', N'Zara Koh', N'S1790678Z', N'2017-02-14', N'FEMALE', N'Rosyth Primary School', N'PRIMARY', N'Primary 3', N'RPS-0201', N'AL-P3', N'2026-10-14T08:15:00', N'2026-10-14T08:15:00');

-- sbfas_scheme_applications (2 rows)
INSERT INTO dbo.[sbfas_scheme_applications] ([id], [code], [scheme_id], [application_id], [status], [created_at])
VALUES
    (N'SSA-KOH-2026', N'SSA-01008', N'SBFAS-SCH-RPS-2026', N'APP-KOH-2026', N'APPROVED', N'2026-10-14T08:15:00'),
    (N'SSA-SMITH-2026', N'SSA-01005', N'SBFAS-SCH-RPS-2026', N'APP-SMITH-2026', N'REJECTED', N'2026-10-10T09:00:00');

-- Updates to existing rows
-- Gives one rejected application with reason and comment (see SSA-SMITH-2026) (GAP-11)
UPDATE dbo.[applications] SET [status] = N'SCHOOL_REJECTED', [current_state_entered_at] = N'2026-10-15T11:30:00' WHERE [id] = N'APP-SMITH-2026';
-- KOH approval uses 19.50 (Zara: Standard Misc Fee 100%). Before-state for UAT-027 becomes 19.50 (GAP-11)
UPDATE dbo.[sbfas_scheme_budgets] SET [used_budget_amount] = N'19.50' WHERE [id] = N'SBF-BDG-RPS-2026';

-- SBFAS decision details (tier, reason, comment). Runs only when Dev has added these columns.
IF COL_LENGTH('dbo.sbfas_scheme_applications', 'tier') IS NOT NULL
BEGIN
    EXEC(N'UPDATE dbo.[sbfas_scheme_applications] SET [tier] = N''Tier 2'', [effective_from] = N''2026-10-20'', [decision_reason] = NULL, [decision_comment] = N''Household income is within the scheme band. Tier 2 approved.'', [decided_by] = N''USR-SCHOOL'', [decided_at] = N''2026-10-20T15:00:00'' WHERE [id] = N''SSA-KOH-2026'';');
    EXEC(N'UPDATE dbo.[sbfas_scheme_applications] SET [tier] = NULL, [effective_from] = NULL, [decision_reason] = N''Income above limit'', [decision_comment] = N''Household income S$ 9,500 is above the school scheme limit of S$ 5,000.'', [decided_by] = N''USR-SCHOOL'', [decided_at] = N''2026-10-15T11:30:00'' WHERE [id] = N''SSA-SMITH-2026'';');
END
ELSE
    PRINT N'sbfas_scheme_applications has no tier/decision columns yet - decision details skipped.';
COMMIT TRANSACTION;
GO
SELECT t.TableName, t.Actual, t.Expected, CASE WHEN t.Actual = t.Expected THEN N'OK' ELSE N'MISMATCH' END AS Result
FROM (
    SELECT N'moe_fas_scheme_subsidies' AS TableName, (SELECT COUNT(*) FROM dbo.[moe_fas_scheme_subsidies] WHERE [id] IN (N'MOE-SUB-007')) AS Actual, 1 AS Expected
UNION ALL
    SELECT N'sbfas_scheme_subsidies' AS TableName, (SELECT COUNT(*) FROM dbo.[sbfas_scheme_subsidies] WHERE [id] IN (N'SBF-SUB-RPS-P1-9')) AS Actual, 1 AS Expected
UNION ALL
    SELECT N'applications' AS TableName, (SELECT COUNT(*) FROM dbo.[applications] WHERE [id] IN (N'APP-TAN-2026', N'APP-KOH-2026')) AS Actual, 2 AS Expected
UNION ALL
    SELECT N'applicants' AS TableName, (SELECT COUNT(*) FROM dbo.[applicants] WHERE [id] IN (N'APL-TAN-2026', N'APL-KOH-2026')) AS Actual, 2 AS Expected
UNION ALL
    SELECT N'family_members' AS TableName, (SELECT COUNT(*) FROM dbo.[family_members] WHERE [id] IN (N'FMB-TAN-01', N'FMB-TAN-02', N'FMB-KOH-01', N'FMB-KOH-02')) AS Actual, 4 AS Expected
UNION ALL
    SELECT N'beneficiaries' AS TableName, (SELECT COUNT(*) FROM dbo.[beneficiaries] WHERE [id] IN (N'BEN-TAN-01', N'BEN-TAN-02', N'BEN-TAN-03', N'BEN-KOH-01')) AS Actual, 4 AS Expected
UNION ALL
    SELECT N'sbfas_scheme_applications' AS TableName, (SELECT COUNT(*) FROM dbo.[sbfas_scheme_applications] WHERE [id] IN (N'SSA-KOH-2026', N'SSA-SMITH-2026')) AS Actual, 2 AS Expected
) AS t;
GO

/* ---------------------------------------------------------------------
   CitizenSimulator
   --------------------------------------------------------------------- */
-- Mock data. Skip this section if the mock is loaded from CSV/JSON.
USE [CitizenSimulator];
GO
BEGIN TRANSACTION;
DELETE FROM dbo.[students] WHERE [nric] IN (N'S1034578B', N'S1845623J', N'S1756234G', N'S1967345F', N'S0956812C', N'S1878456D', N'S1989567Z', N'S1790678Z', N'S1901789C');
DELETE FROM dbo.[parents] WHERE [nric] IN (N'S7623418C', N'S7934526A', N'S7745213C', N'S8034172E', N'S8256341E', N'S8145627E', N'S8367512H', N'S8589346G');
DELETE FROM dbo.[all_citizens] WHERE [nric] IN (N'S7623418C', N'S7934526A', N'S7745213C', N'S8034172E', N'S8256341E', N'S8145627E', N'S8367512H', N'S8589346G', N'S1034578B', N'S1845623J', N'S1756234G', N'S1967345F', N'S0956812C', N'S1878456D', N'S1989567Z', N'S1790678Z', N'S1901789C');

-- all_citizens (17 rows)
INSERT INTO dbo.[all_citizens] ([record_type], [nric], [full_name], [date_of_birth], [gender], [race], [block], [street], [unit], [postal_code], [monthly_gross_income_cents], [monthly_gross_income_sgd], [household_size], [income_source], [father_nric], [mother_nric], [family_nrics], [household_key])
VALUES
    (N'PARENT', N'S7623418C', N'TAN KAH HOE', N'1984-04-21', N'Male', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'520000', N'5200.00', N'6', N'Salary', NULL, NULL, N'S7934526A;S1034578B;S1845623J;S1756234G;S1967345F', N'TAN'),
    (N'PARENT', N'S7934526A', N'LOW SIEW LING', N'1986-09-03', N'Female', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'520000', N'5200.00', N'6', N'Salary', NULL, NULL, N'S7623418C;S1034578B;S1845623J;S1756234G;S1967345F', N'TAN'),
    (N'PARENT', N'S7745213C', N'LEE MEI FONG', N'1979-12-11', N'Female', N'Chinese', N'231', N'Bishan Street 22', N'#11-34', N'570231', N'680000', N'6800.00', N'2', N'Salary', NULL, NULL, N'S0956812C', N'LEE'),
    (N'PARENT', N'S8034172E', N'NG CHEE KEONG', N'1987-02-17', N'Male', N'Chinese', N'456', N'Jurong West Street 41', N'#07-215', N'640456', N'300000', N'3000.00', N'4', N'Salary', NULL, NULL, N'S8256341E;S1878456D;S1989567Z', N'NG'),
    (N'PARENT', N'S8256341E', N'ONG BEE LIAN', N'1989-07-25', N'Female', N'Chinese', N'456', N'Jurong West Street 41', N'#07-215', N'640456', N'300000', N'3000.00', N'4', N'Salary', NULL, NULL, N'S8034172E;S1878456D;S1989567Z', N'NG'),
    (N'PARENT', N'S8145627E', N'KOH BOON HUAT', N'1985-11-30', N'Male', N'Chinese', N'629', N'Hougang Avenue 8', N'#04-48', N'530629', N'460000', N'4600.00', N'3', N'Salary', NULL, NULL, N'S8367512H;S1790678Z', N'KOH'),
    (N'PARENT', N'S8367512H', N'SEAH AI HUA', N'1988-05-08', N'Female', N'Chinese', N'629', N'Hougang Avenue 8', N'#04-48', N'530629', N'460000', N'4600.00', N'3', N'Salary', NULL, NULL, N'S8145627E;S1790678Z', N'KOH'),
    (N'PARENT', N'S8589346G', N'FARAH BINTE ISMAIL', N'1990-10-02', N'Female', N'Malay', N'512', N'Woodlands Drive 14', N'#12-77', N'730512', N'280000', N'2800.00', N'1', N'Salary', NULL, NULL, NULL, NULL),
    (N'STUDENT', N'S1034578B', N'Henry Tan', N'2010-08-15', N'Male', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'520000', N'5200.00', N'6', N'Salary', N'S7623418C', N'S7934526A', N'S7623418C;S7934526A', N'TAN'),
    (N'STUDENT', N'S1845623J', N'Megan Tan', N'2018-01-09', N'Female', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'520000', N'5200.00', N'6', N'Salary', N'S7623418C', N'S7934526A', N'S7623418C;S7934526A', N'TAN'),
    (N'STUDENT', N'S1756234G', N'Rachel Tan', N'2017-06-12', N'Female', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'520000', N'5200.00', N'6', N'Salary', N'S7623418C', N'S7934526A', N'S7623418C;S7934526A', N'TAN'),
    (N'STUDENT', N'S1967345F', N'Jonas Tan', N'2019-05-20', N'Male', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'520000', N'5200.00', N'6', N'Salary', N'S7623418C', N'S7934526A', N'S7623418C;S7934526A', N'TAN'),
    (N'STUDENT', N'S0956812C', N'Jasmine Lee', N'2009-03-02', N'Female', N'Chinese', N'231', N'Bishan Street 22', N'#11-34', N'570231', N'680000', N'6800.00', N'2', N'Salary', NULL, N'S7745213C', N'S7745213C', N'LEE'),
    (N'STUDENT', N'S1878456D', N'Kayden Ng', N'2018-06-21', N'Male', N'Chinese', N'456', N'Jurong West Street 41', N'#07-215', N'640456', N'300000', N'3000.00', N'4', N'Salary', N'S8034172E', N'S8256341E', N'S8034172E;S8256341E', N'NG'),
    (N'STUDENT', N'S1989567Z', N'Sophie Ng', N'2019-09-30', N'Female', N'Chinese', N'456', N'Jurong West Street 41', N'#07-215', N'640456', N'300000', N'3000.00', N'4', N'Salary', N'S8034172E', N'S8256341E', N'S8034172E;S8256341E', N'NG'),
    (N'STUDENT', N'S1790678Z', N'Zara Koh', N'2017-02-14', N'Female', N'Chinese', N'629', N'Hougang Avenue 8', N'#04-48', N'530629', N'460000', N'4600.00', N'3', N'Salary', N'S8145627E', N'S8367512H', N'S8145627E;S8367512H', N'KOH'),
    (N'STUDENT', N'S1901789C', N'Ivy Chen', N'2019-12-02', N'Female', N'Chinese', N'162', N'Serangoon North Avenue 1', N'#11-402', N'550162', N'320000', N'3200.00', N'5', N'Salary', N'S6789012F', N'S7890123G', N'S6789012F;S7890123G', N'CHEN');

-- parents (8 rows)
INSERT INTO dbo.[parents] ([nric], [full_name], [date_of_birth], [gender], [race], [block], [street], [unit], [postal_code], [monthly_gross_income_cents], [monthly_gross_income_sgd], [household_size], [income_source], [family_nrics], [household_key])
VALUES
    (N'S7623418C', N'TAN KAH HOE', N'1984-04-21', N'Male', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'520000', N'5200.00', N'6', N'Salary', N'S7934526A;S1034578B;S1845623J;S1756234G;S1967345F', N'TAN'),
    (N'S7934526A', N'LOW SIEW LING', N'1986-09-03', N'Female', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'520000', N'5200.00', N'6', N'Salary', N'S7623418C;S1034578B;S1845623J;S1756234G;S1967345F', N'TAN'),
    (N'S7745213C', N'LEE MEI FONG', N'1979-12-11', N'Female', N'Chinese', N'231', N'Bishan Street 22', N'#11-34', N'570231', N'680000', N'6800.00', N'2', N'Salary', N'S0956812C', N'LEE'),
    (N'S8034172E', N'NG CHEE KEONG', N'1987-02-17', N'Male', N'Chinese', N'456', N'Jurong West Street 41', N'#07-215', N'640456', N'300000', N'3000.00', N'4', N'Salary', N'S8256341E;S1878456D;S1989567Z', N'NG'),
    (N'S8256341E', N'ONG BEE LIAN', N'1989-07-25', N'Female', N'Chinese', N'456', N'Jurong West Street 41', N'#07-215', N'640456', N'300000', N'3000.00', N'4', N'Salary', N'S8034172E;S1878456D;S1989567Z', N'NG'),
    (N'S8145627E', N'KOH BOON HUAT', N'1985-11-30', N'Male', N'Chinese', N'629', N'Hougang Avenue 8', N'#04-48', N'530629', N'460000', N'4600.00', N'3', N'Salary', N'S8367512H;S1790678Z', N'KOH'),
    (N'S8367512H', N'SEAH AI HUA', N'1988-05-08', N'Female', N'Chinese', N'629', N'Hougang Avenue 8', N'#04-48', N'530629', N'460000', N'4600.00', N'3', N'Salary', N'S8145627E;S1790678Z', N'KOH'),
    (N'S8589346G', N'FARAH BINTE ISMAIL', N'1990-10-02', N'Female', N'Malay', N'512', N'Woodlands Drive 14', N'#12-77', N'730512', N'280000', N'2800.00', N'1', N'Salary', NULL, NULL);

-- students (9 rows)
INSERT INTO dbo.[students] ([nric], [full_name], [date_of_birth], [gender], [race], [block], [street], [unit], [postal_code], [monthly_gross_income_cents], [monthly_gross_income_sgd], [household_size], [income_source], [father_nric], [mother_nric], [family_nrics], [household_key])
VALUES
    (N'S1034578B', N'Henry Tan', N'2010-08-15', N'Male', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'520000', N'5200.00', N'6', N'Salary', N'S7623418C', N'S7934526A', N'S7623418C;S7934526A', N'TAN'),
    (N'S1845623J', N'Megan Tan', N'2018-01-09', N'Female', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'520000', N'5200.00', N'6', N'Salary', N'S7623418C', N'S7934526A', N'S7623418C;S7934526A', N'TAN'),
    (N'S1756234G', N'Rachel Tan', N'2017-06-12', N'Female', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'520000', N'5200.00', N'6', N'Salary', N'S7623418C', N'S7934526A', N'S7623418C;S7934526A', N'TAN'),
    (N'S1967345F', N'Jonas Tan', N'2019-05-20', N'Male', N'Chinese', N'74', N'Lorong 4 Toa Payoh', N'#09-122', N'310074', N'520000', N'5200.00', N'6', N'Salary', N'S7623418C', N'S7934526A', N'S7623418C;S7934526A', N'TAN'),
    (N'S0956812C', N'Jasmine Lee', N'2009-03-02', N'Female', N'Chinese', N'231', N'Bishan Street 22', N'#11-34', N'570231', N'680000', N'6800.00', N'2', N'Salary', NULL, N'S7745213C', N'S7745213C', N'LEE'),
    (N'S1878456D', N'Kayden Ng', N'2018-06-21', N'Male', N'Chinese', N'456', N'Jurong West Street 41', N'#07-215', N'640456', N'300000', N'3000.00', N'4', N'Salary', N'S8034172E', N'S8256341E', N'S8034172E;S8256341E', N'NG'),
    (N'S1989567Z', N'Sophie Ng', N'2019-09-30', N'Female', N'Chinese', N'456', N'Jurong West Street 41', N'#07-215', N'640456', N'300000', N'3000.00', N'4', N'Salary', N'S8034172E', N'S8256341E', N'S8034172E;S8256341E', N'NG'),
    (N'S1790678Z', N'Zara Koh', N'2017-02-14', N'Female', N'Chinese', N'629', N'Hougang Avenue 8', N'#04-48', N'530629', N'460000', N'4600.00', N'3', N'Salary', N'S8145627E', N'S8367512H', N'S8145627E;S8367512H', N'KOH'),
    (N'S1901789C', N'Ivy Chen', N'2019-12-02', N'Female', N'Chinese', N'162', N'Serangoon North Avenue 1', N'#11-402', N'550162', N'320000', N'3200.00', N'5', N'Salary', N'S6789012F', N'S7890123G', N'S6789012F;S7890123G', N'CHEN');

-- Updates to existing rows
-- PHAM VAN DUC: household GHI must be 2400 to match FAS family_members (2400 + 0) and UAT-014 (step 4). Same change in parents.csv / students.csv (GAP-10)
UPDATE dbo.[all_citizens] SET [monthly_gross_income_cents] = N'240000', [monthly_gross_income_sgd] = N'2400.00' WHERE [nric] = N'S7654321B';
-- PHAM VAN DUC: household GHI must be 2400 to match FAS family_members (2400 + 0) and UAT-014 (step 4). Same change in parents.csv / students.csv (GAP-10)
UPDATE dbo.[parents] SET [monthly_gross_income_cents] = N'240000', [monthly_gross_income_sgd] = N'2400.00' WHERE [nric] = N'S7654321B';
-- PHAM VAN DUC: household GHI must be 2400 to match FAS family_members (2400 + 0) and UAT-014 (step 4). Same change in parents.csv / students.csv (GAP-10)
UPDATE dbo.[students] SET [monthly_gross_income_cents] = N'240000', [monthly_gross_income_sgd] = N'2400.00' WHERE [nric] = N'S7654321B';
-- NGUYEN THI HOA: household GHI must be 2400 to match FAS family_members (2400 + 0) and UAT-014 (step 4). Same change in parents.csv / students.csv (GAP-10)
UPDATE dbo.[all_citizens] SET [monthly_gross_income_cents] = N'240000', [monthly_gross_income_sgd] = N'2400.00' WHERE [nric] = N'S3456789C';
-- NGUYEN THI HOA: household GHI must be 2400 to match FAS family_members (2400 + 0) and UAT-014 (step 4). Same change in parents.csv / students.csv (GAP-10)
UPDATE dbo.[parents] SET [monthly_gross_income_cents] = N'240000', [monthly_gross_income_sgd] = N'2400.00' WHERE [nric] = N'S3456789C';
-- NGUYEN THI HOA: household GHI must be 2400 to match FAS family_members (2400 + 0) and UAT-014 (step 4). Same change in parents.csv / students.csv (GAP-10)
UPDATE dbo.[students] SET [monthly_gross_income_cents] = N'240000', [monthly_gross_income_sgd] = N'2400.00' WHERE [nric] = N'S3456789C';
-- Liam Pham: household GHI must be 2400 to match FAS family_members (2400 + 0) and UAT-014 (step 4). Same change in parents.csv / students.csv (GAP-10)
UPDATE dbo.[all_citizens] SET [monthly_gross_income_cents] = N'240000', [monthly_gross_income_sgd] = N'2400.00' WHERE [nric] = N'S4744854C';
-- Liam Pham: household GHI must be 2400 to match FAS family_members (2400 + 0) and UAT-014 (step 4). Same change in parents.csv / students.csv (GAP-10)
UPDATE dbo.[parents] SET [monthly_gross_income_cents] = N'240000', [monthly_gross_income_sgd] = N'2400.00' WHERE [nric] = N'S4744854C';
-- Liam Pham: household GHI must be 2400 to match FAS family_members (2400 + 0) and UAT-014 (step 4). Same change in parents.csv / students.csv (GAP-10)
UPDATE dbo.[students] SET [monthly_gross_income_cents] = N'240000', [monthly_gross_income_sgd] = N'2400.00' WHERE [nric] = N'S4744854C';
-- Grace Pham: household GHI must be 2400 to match FAS family_members (2400 + 0) and UAT-014 (step 4). Same change in parents.csv / students.csv (GAP-10)
UPDATE dbo.[all_citizens] SET [monthly_gross_income_cents] = N'240000', [monthly_gross_income_sgd] = N'2400.00' WHERE [nric] = N'S6159230D';
-- Grace Pham: household GHI must be 2400 to match FAS family_members (2400 + 0) and UAT-014 (step 4). Same change in parents.csv / students.csv (GAP-10)
UPDATE dbo.[parents] SET [monthly_gross_income_cents] = N'240000', [monthly_gross_income_sgd] = N'2400.00' WHERE [nric] = N'S6159230D';
-- Grace Pham: household GHI must be 2400 to match FAS family_members (2400 + 0) and UAT-014 (step 4). Same change in parents.csv / students.csv (GAP-10)
UPDATE dbo.[students] SET [monthly_gross_income_cents] = N'240000', [monthly_gross_income_sgd] = N'2400.00' WHERE [nric] = N'S6159230D';
-- CHEN WEI JIE: Ivy Chen joins the household (transfer, 15/10/2026). Same change in parents.csv (GAP-13)
UPDATE dbo.[all_citizens] SET [household_size] = N'5', [family_nrics] = N'S7890123G;S3320821H;S1192619B;S1901789C' WHERE [nric] = N'S6789012F';
-- CHEN WEI JIE: Ivy Chen joins the household (transfer, 15/10/2026). Same change in parents.csv (GAP-13)
UPDATE dbo.[parents] SET [household_size] = N'5', [family_nrics] = N'S7890123G;S3320821H;S1192619B;S1901789C' WHERE [nric] = N'S6789012F';
-- CHEN WEI JIE: Ivy Chen joins the household (transfer, 15/10/2026). Same change in parents.csv (GAP-13)
UPDATE dbo.[students] SET [household_size] = N'5', [family_nrics] = N'S7890123G;S3320821H;S1192619B;S1901789C' WHERE [nric] = N'S6789012F';
-- LIM HUI MIN: Ivy Chen joins the household (transfer, 15/10/2026). Same change in parents.csv (GAP-13)
UPDATE dbo.[all_citizens] SET [household_size] = N'5', [family_nrics] = N'S6789012F;S3320821H;S1192619B;S1901789C' WHERE [nric] = N'S7890123G';
-- LIM HUI MIN: Ivy Chen joins the household (transfer, 15/10/2026). Same change in parents.csv (GAP-13)
UPDATE dbo.[parents] SET [household_size] = N'5', [family_nrics] = N'S6789012F;S3320821H;S1192619B;S1901789C' WHERE [nric] = N'S7890123G';
-- LIM HUI MIN: Ivy Chen joins the household (transfer, 15/10/2026). Same change in parents.csv (GAP-13)
UPDATE dbo.[students] SET [household_size] = N'5', [family_nrics] = N'S6789012F;S3320821H;S1192619B;S1901789C' WHERE [nric] = N'S7890123G';
-- Ivy Chen joins the CHEN household. Same change in students.csv (GAP-13)
UPDATE dbo.[all_citizens] SET [household_size] = N'5' WHERE [nric] = N'S3320821H';
-- Ivy Chen joins the CHEN household. Same change in students.csv (GAP-13)
UPDATE dbo.[parents] SET [household_size] = N'5' WHERE [nric] = N'S3320821H';
-- Ivy Chen joins the CHEN household. Same change in students.csv (GAP-13)
UPDATE dbo.[students] SET [household_size] = N'5' WHERE [nric] = N'S3320821H';
-- Ivy Chen joins the CHEN household. Same change in students.csv (GAP-13)
UPDATE dbo.[all_citizens] SET [household_size] = N'5' WHERE [nric] = N'S1192619B';
-- Ivy Chen joins the CHEN household. Same change in students.csv (GAP-13)
UPDATE dbo.[parents] SET [household_size] = N'5' WHERE [nric] = N'S1192619B';
-- Ivy Chen joins the CHEN household. Same change in students.csv (GAP-13)
UPDATE dbo.[students] SET [household_size] = N'5' WHERE [nric] = N'S1192619B';
COMMIT TRANSACTION;
GO
SELECT t.TableName, t.Actual, t.Expected, CASE WHEN t.Actual = t.Expected THEN N'OK' ELSE N'MISMATCH' END AS Result
FROM (
    SELECT N'all_citizens' AS TableName, (SELECT COUNT(*) FROM dbo.[all_citizens] WHERE [nric] IN (N'S7623418C', N'S7934526A', N'S7745213C', N'S8034172E', N'S8256341E', N'S8145627E', N'S8367512H', N'S8589346G', N'S1034578B', N'S1845623J', N'S1756234G', N'S1967345F', N'S0956812C', N'S1878456D', N'S1989567Z', N'S1790678Z', N'S1901789C')) AS Actual, 17 AS Expected
UNION ALL
    SELECT N'parents' AS TableName, (SELECT COUNT(*) FROM dbo.[parents] WHERE [nric] IN (N'S7623418C', N'S7934526A', N'S7745213C', N'S8034172E', N'S8256341E', N'S8145627E', N'S8367512H', N'S8589346G')) AS Actual, 8 AS Expected
UNION ALL
    SELECT N'students' AS TableName, (SELECT COUNT(*) FROM dbo.[students] WHERE [nric] IN (N'S1034578B', N'S1845623J', N'S1756234G', N'S1967345F', N'S0956812C', N'S1878456D', N'S1989567Z', N'S1790678Z', N'S1901789C')) AS Actual, 9 AS Expected
) AS t;
GO

/* ---------------------------------------------------------------------
   MockPass_Singpass
   --------------------------------------------------------------------- */
-- Mock data. Skip this section if the mock is loaded from CSV/JSON.
USE [MockPass_Singpass];
GO
BEGIN TRANSACTION;
DELETE FROM dbo.[singpass_personas] WHERE [nric] IN (N'S7623418C', N'S7934526A', N'S7745213C', N'S8034172E', N'S8256341E', N'S8145627E', N'S8367512H', N'S8478235A', N'S8589346G');

-- singpass_personas (9 rows)
INSERT INTO dbo.[singpass_personas] ([nric], [singpass_uuid], [full_name], [date_of_birth], [sex], [nationality], [email], [mobile_number], [block], [street], [unit], [postal_code], [household_key], [parent_role], [monthly_income_sgd], [children_nrics], [children_names])
VALUES
    (N'S7623418C', N'93bb9ea9-45d5-5a0f-aaf3-6672e5dd4ee4', N'TAN KAH HOE', N'1984-04-21', N'Male', N'SINGAPORE CITIZEN', N'hoe.s7623418c@example.com', N'+6581234501', N'74', N'LORONG 4 TOA PAYOH', N'09-122', N'310074', N'TAN', N'Father', N'5200.00', N'S1034578B, S1845623J, S1756234G, S1967345F', N'Henry Tan, Megan Tan, Rachel Tan, Jonas Tan'),
    (N'S7934526A', N'f77f737b-a874-5893-b40d-4a671f59f747', N'LOW SIEW LING', N'1986-09-03', N'Female', N'SINGAPORE CITIZEN', N'ling.s7934526a@example.com', N'+6581234502', N'74', N'LORONG 4 TOA PAYOH', N'09-122', N'310074', N'TAN', N'Mother', N'5200.00', N'S1034578B, S1845623J, S1756234G, S1967345F', N'Henry Tan, Megan Tan, Rachel Tan, Jonas Tan'),
    (N'S7745213C', N'e4ba1569-e7ea-5f7b-901f-4d9a123971ee', N'LEE MEI FONG', N'1979-12-11', N'Female', N'SINGAPORE CITIZEN', N'fong.s7745213c@example.com', N'+6581234503', N'231', N'BISHAN STREET 22', N'11-34', N'570231', N'LEE', N'Mother', N'6800.00', N'S0956812C', N'Jasmine Lee'),
    (N'S8034172E', N'4bd2f806-abe4-5576-aa05-207b6a478437', N'NG CHEE KEONG', N'1987-02-17', N'Male', N'SINGAPORE CITIZEN', N'keong.s8034172e@example.com', N'+6581234504', N'456', N'JURONG WEST STREET 41', N'07-215', N'640456', N'NG', N'Father', N'3000.00', N'S1878456D, S1989567Z', N'Kayden Ng, Sophie Ng'),
    (N'S8256341E', N'e37ea19f-d98a-5f3c-b4d1-7334e3c18c68', N'ONG BEE LIAN', N'1989-07-25', N'Female', N'SINGAPORE CITIZEN', N'lian.s8256341e@example.com', N'+6581234505', N'456', N'JURONG WEST STREET 41', N'07-215', N'640456', N'NG', N'Mother', N'3000.00', N'S1878456D, S1989567Z', N'Kayden Ng, Sophie Ng'),
    (N'S8145627E', N'b5142bbe-6227-52b6-be51-f76a2145d024', N'KOH BOON HUAT', N'1985-11-30', N'Male', N'SINGAPORE CITIZEN', N'huat.s8145627e@example.com', N'+6581234506', N'629', N'HOUGANG AVENUE 8', N'04-48', N'530629', N'KOH', N'Father', N'4600.00', N'S1790678Z', N'Zara Koh'),
    (N'S8367512H', N'ce32cfa5-c04a-54c5-a32e-281d1305bc10', N'SEAH AI HUA', N'1988-05-08', N'Female', N'SINGAPORE CITIZEN', N'hua.s8367512h@example.com', N'+6581234507', N'629', N'HOUGANG AVENUE 8', N'04-48', N'530629', N'KOH', N'Mother', N'4600.00', N'S1790678Z', N'Zara Koh'),
    (N'S8478235A', N'2ff36879-a7df-5f47-a196-6fc871b83cad', N'GOH WEI LIANG', N'1983-01-19', N'Male', N'SINGAPORE CITIZEN', N'goh.s8478235a@example.com', N'+6581234508', N'88', N'TAMPINES STREET 81', N'05-301', N'520088', NULL, NULL, NULL, NULL, NULL),
    (N'S8589346G', N'b165bb70-7120-5aa2-b4fd-d1293d2ff32c', N'FARAH BINTE ISMAIL', N'1990-10-02', N'Female', N'SINGAPORE CITIZEN', N'farah.s8589346g@example.com', N'+6581234509', N'512', N'WOODLANDS DRIVE 14', N'12-77', N'730512', NULL, NULL, NULL, NULL, NULL);

-- Updates to existing rows
-- Same household GHI as CitizenSimulator (GAP-10)
UPDATE dbo.[singpass_personas] SET [monthly_income_sgd] = N'2400.00' WHERE [nric] = N'S7654321B';
-- Same household GHI as CitizenSimulator (GAP-10)
UPDATE dbo.[singpass_personas] SET [monthly_income_sgd] = N'2400.00' WHERE [nric] = N'S3456789C';
-- Ivy Chen linked to both CHEN parents (GAP-13)
UPDATE dbo.[singpass_personas] SET [children_nrics] = N'S3320821H, S1192619B, S1901789C', [children_names] = N'Isaac Chen, Sophia Chen, Ivy Chen' WHERE [nric] = N'S6789012F';
-- Ivy Chen linked to both CHEN parents (GAP-13)
UPDATE dbo.[singpass_personas] SET [children_nrics] = N'S3320821H, S1192619B, S1901789C', [children_names] = N'Isaac Chen, Sophia Chen, Ivy Chen' WHERE [nric] = N'S7890123G';
COMMIT TRANSACTION;
GO
SELECT t.TableName, t.Actual, t.Expected, CASE WHEN t.Actual = t.Expected THEN N'OK' ELSE N'MISMATCH' END AS Result
FROM (
    SELECT N'singpass_personas' AS TableName, (SELECT COUNT(*) FROM dbo.[singpass_personas] WHERE [nric] IN (N'S7623418C', N'S7934526A', N'S7745213C', N'S8034172E', N'S8256341E', N'S8145627E', N'S8367512H', N'S8478235A', N'S8589346G')) AS Actual, 9 AS Expected
) AS t;
GO

/* ---------------------------------------------------------------------
   OPTIONAL - RESET COPIES. Run only on a separate copy of FASService, never on the shared UAT database.
   Reset copy A: UAT-HOWARD-014, 020, 024 step 1.   Reset copy B: UAT-HOWARD-026, 027.
   Remove the comment markers around the block you need.
   --------------------------------------------------------------------- */
/*  -- Reset copy A
USE [FASService];
DELETE FROM dbo.[beneficiaries]   WHERE [application_id] = N'APP-PHAM-2026';
DELETE FROM dbo.[family_members]  WHERE [application_id] = N'APP-PHAM-2026';
DELETE FROM dbo.[applicants]      WHERE [application_id] = N'APP-PHAM-2026';
DELETE FROM dbo.[moe_scheme_applications] WHERE [application_id] = N'APP-PHAM-2026';
DELETE FROM dbo.[applications]    WHERE [id] = N'APP-PHAM-2026';
*/
/*  -- Reset copy B
USE [FASService];
DELETE FROM dbo.[sbfas_scheme_applications] WHERE [application_id] = N'APP-RAHMAN-2026';
DELETE FROM dbo.[beneficiaries]   WHERE [application_id] = N'APP-RAHMAN-2026';
DELETE FROM dbo.[family_members]  WHERE [application_id] = N'APP-RAHMAN-2026';
DELETE FROM dbo.[applicants]      WHERE [application_id] = N'APP-RAHMAN-2026';
DELETE FROM dbo.[applications]    WHERE [id] = N'APP-RAHMAN-2026';
*/
