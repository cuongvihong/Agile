/* =====================================================================
   R4 add-on for the R8/R9 seed. Run in the database where R4_FAS_Seed_Data.sql was loaded, AFTER it.
   It adds what R8/R9 need and R4 does not have; it changes no R4 values except naming 5 household rows.
     - 4 school_classes, 6 Student_Profile rows (X01–X06), 5 enrollments
     - 6 student_charges (AX01–AX06) and 1 fas_charge_subsidies row (AX02, Ethan Chua, MOEFAS Tier 2, 50%)
     - fas_household_members: the rows "Sibling 1/2 of Nadia Karim", "Sibling 1 of Ethan Chua", "Sibling 1 of Nur Aisyah"
       get the name and NRIC of the added child; "Spouse of Nadia Karim (Father)" gets an NRIC.
   Safe to run again (deletes its own rows first). Generated 22/10/2026.
   ===================================================================== */
SET QUOTED_IDENTIFIER ON; SET ANSI_NULLS ON; SET NOCOUNT ON; SET XACT_ABORT ON;
DECLARE @Today date = CAST(GETDATE() AS date);
BEGIN TRANSACTION;
DELETE FROM dbo.fas_charge_subsidies WHERE StudentChargeId IN ('08000000-0000-0000-0004-000000000001', '08000000-0000-0000-0004-000000000002', '08000000-0000-0000-0004-000000000003', '08000000-0000-0000-0004-000000000004', '08000000-0000-0000-0004-000000000005', '08000000-0000-0000-0004-000000000006');
DELETE FROM dbo.student_charges WHERE id IN ('08000000-0000-0000-0004-000000000001', '08000000-0000-0000-0004-000000000002', '08000000-0000-0000-0004-000000000003', '08000000-0000-0000-0004-000000000004', '08000000-0000-0000-0004-000000000005', '08000000-0000-0000-0004-000000000006');
DELETE FROM dbo.student_school_enrollments WHERE Id IN ('08000000-0000-0000-0006-000000000101', '08000000-0000-0000-0006-000000000103', '08000000-0000-0000-0006-000000000104', '08000000-0000-0000-0006-000000000105', '08000000-0000-0000-0006-000000000106');
DELETE FROM dbo.Student_Profile WHERE Id IN ('08000000-0000-0000-0001-000000000101', '08000000-0000-0000-0001-000000000102', '08000000-0000-0000-0001-000000000103', '08000000-0000-0000-0001-000000000104', '08000000-0000-0000-0001-000000000105', '08000000-0000-0000-0001-000000000106');
DELETE FROM dbo.school_classes WHERE Id IN ('08000000-0000-0000-0005-000000000001', '08000000-0000-0000-0005-000000000002', '08000000-0000-0000-0005-000000000003', '08000000-0000-0000-0005-000000000004');

INSERT INTO dbo.school_classes (Id, SchoolId, Level, Name) VALUES
('08000000-0000-0000-0005-000000000001', 'a82af704-e047-56b4-8490-cd68feb38d34', N'Sec 4', N'Sec 4 Harmony'),  -- Meridian Secondary
('08000000-0000-0000-0005-000000000002', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', N'P1', N'P1 Joy'),  -- Bukit View Primary
('08000000-0000-0000-0005-000000000003', '4a849167-7545-5bf8-b05b-e92a4438a636', N'Sec 4', N'Sec 4 Grace'),  -- Riverside Secondary
('08000000-0000-0000-0005-000000000004', '4a849167-7545-5bf8-b05b-e92a4438a636', N'Sec 5', N'Sec 5 Resilience');  -- Riverside Secondary

INSERT INTO dbo.Student_Profile (Id, Code, Nric, FullName, DateOfBirth, Citizenship, Status) VALUES
('08000000-0000-0000-0001-000000000101', N'X01', N'T1023401D', N'Hakim Karim', DATEADD(year, -16, @Today), N'Citizen', N'Active'),  -- R4 household "Sibling 1 of Nadia Karim"
('08000000-0000-0000-0001-000000000102', N'X02', N'T2123402D', N'Sara Karim', '2021-04-14', N'Citizen', N'Active'),  -- R4 household "Sibling 2 of Nadia Karim"
('08000000-0000-0000-0001-000000000103', N'X03', N'T1223403H', N'Emma Chua', '2012-11-11', N'Citizen', N'Active'),  -- R4 household "Sibling 1 of Ethan Chua" (twin)
('08000000-0000-0000-0001-000000000104', N'X04', N'T1923404A', N'Nur Iman', '2019-03-10', N'Citizen', N'Active'),  -- R4 household "Sibling 1 of Nur Aisyah"
('08000000-0000-0000-0001-000000000105', N'X05', N'T0923405A', N'Lim Wei Jie', '2009-04-12', N'Citizen', N'Active'),  -- Added (R4 has no child aged 16+)
('08000000-0000-0000-0001-000000000106', N'X06', N'T1023406E', N'Lim Hui Ling', '2010-09-01', N'Citizen', N'Active');  -- Added (R4 has no child aged 16+)

INSERT INTO dbo.student_school_enrollments (Id, StudentId, SchoolId, AcademicYearId, ClassId) VALUES
('08000000-0000-0000-0006-000000000101', '08000000-0000-0000-0001-000000000101', 'a82af704-e047-56b4-8490-cd68feb38d34', '5bf3e77a-6cb4-5de8-8dc0-7d4810719647', '08000000-0000-0000-0005-000000000001'),  -- Hakim Karim
('08000000-0000-0000-0006-000000000103', '08000000-0000-0000-0001-000000000103', 'a82af704-e047-56b4-8490-cd68feb38d34', '5bf3e77a-6cb4-5de8-8dc0-7d4810719647', '29a604c5-ed5b-5b8f-8845-3c54af4fcbce'),  -- Emma Chua
('08000000-0000-0000-0006-000000000104', '08000000-0000-0000-0001-000000000104', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', '5bf3e77a-6cb4-5de8-8dc0-7d4810719647', '08000000-0000-0000-0005-000000000002'),  -- Nur Iman
('08000000-0000-0000-0006-000000000105', '08000000-0000-0000-0001-000000000105', '4a849167-7545-5bf8-b05b-e92a4438a636', '5bf3e77a-6cb4-5de8-8dc0-7d4810719647', '08000000-0000-0000-0005-000000000004'),  -- Lim Wei Jie
('08000000-0000-0000-0006-000000000106', '08000000-0000-0000-0001-000000000106', '4a849167-7545-5bf8-b05b-e92a4438a636', '5bf3e77a-6cb4-5de8-8dc0-7d4810719647', '08000000-0000-0000-0005-000000000003');  -- Lim Hui Ling

INSERT INTO dbo.student_charges (id, student_id, enrollment_id, fee_component_id, school_id, academic_year_id, base_amount, tax_amount, total_amount, currency_code, status, period_start, period_end_exclusive) VALUES
('08000000-0000-0000-0004-000000000001', 'f063b14b-8ec5-507d-84ad-9a9d36a79c26', 'ba489887-1cc7-5f38-9a9a-a702634bb6cf', 'ac40bbe6-6ba0-5c33-a56c-55463fb2563d', 'a82af704-e047-56b4-8490-cd68feb38d34', '5bf3e77a-6cb4-5de8-8dc0-7d4810719647', 33.33, 3.00, 36.33, N'SGD', N'POSTED', '2026-07-13', '2026-09-19'),  -- AX01 Ethan Chua: Miscellaneous fee, Term 3
('08000000-0000-0000-0004-000000000002', 'f063b14b-8ec5-507d-84ad-9a9d36a79c26', 'ba489887-1cc7-5f38-9a9a-a702634bb6cf', 'af9b811e-fb34-5c5c-9f95-d920d16bcf17', 'a82af704-e047-56b4-8490-cd68feb38d34', '5bf3e77a-6cb4-5de8-8dc0-7d4810719647', 33.33, 3.00, 36.33, N'SGD', N'POSTED', '2026-12-01', '2027-01-01'),  -- AX02 Ethan Chua: School Meal Fee, Dec
('08000000-0000-0000-0004-000000000003', '5077e467-2178-5ed0-83eb-9ccbc7f62670', '2617ec33-62d1-5614-8cb4-aabb42abdc12', 'e91b9933-1ebe-52c7-b616-98b930dc7751', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', '5bf3e77a-6cb4-5de8-8dc0-7d4810719647', 10.00, 0.90, 10.90, N'SGD', N'CANCELLED', '2026-10-05', '2026-12-12'),  -- AX03 Priya Nair: Service charge, Term 4
('08000000-0000-0000-0004-000000000004', '08000000-0000-0000-0001-000000000101', '08000000-0000-0000-0006-000000000101', 'ac40bbe6-6ba0-5c33-a56c-55463fb2563d', 'a82af704-e047-56b4-8490-cd68feb38d34', '5bf3e77a-6cb4-5de8-8dc0-7d4810719647', 25.00, 2.25, 27.25, N'SGD', N'POSTED', '2026-10-05', '2026-12-12'),  -- AX04 Hakim Karim: Miscellaneous fee, Term 4
('08000000-0000-0000-0004-000000000005', '08000000-0000-0000-0001-000000000105', '08000000-0000-0000-0006-000000000105', 'ac40bbe6-6ba0-5c33-a56c-55463fb2563d', '4a849167-7545-5bf8-b05b-e92a4438a636', '5bf3e77a-6cb4-5de8-8dc0-7d4810719647', 25.00, 2.25, 27.25, N'SGD', N'POSTED', '2026-10-05', '2026-12-12'),  -- AX05 Lim Wei Jie: Miscellaneous fee, Term 4
('08000000-0000-0000-0004-000000000006', '08000000-0000-0000-0001-000000000103', '08000000-0000-0000-0006-000000000103', 'ac40bbe6-6ba0-5c33-a56c-55463fb2563d', 'a82af704-e047-56b4-8490-cd68feb38d34', '5bf3e77a-6cb4-5de8-8dc0-7d4810719647', 33.33, 3.00, 36.33, N'SGD', N'POSTED', '2026-10-05', '2026-12-12');  -- AX06 Emma Chua: Miscellaneous fee, Term 4

INSERT INTO dbo.fas_charge_subsidies (Id, ApplicationId, StudentChargeId, FeeComponentId, BaseAmount, CurrencyCode, SubsidyPercent, SubsidyAmount, Status, CalculatedAt) VALUES
('08000000-0000-0000-0007-000000000001', 'c1d337d7-fef6-5cfa-9d15-5eae74b5d5d6', '08000000-0000-0000-0004-000000000002', 'af9b811e-fb34-5c5c-9f95-d920d16bcf17', 33.33, N'SGD', 50.0, 16.67, N'Active', '2026-10-19T00:30:00.000');  -- AX02 Ethan Chua, APP-2026-00423 Tier 2

UPDATE dbo.fas_household_members SET FullName = N'Hakim Karim', IdNumber = N'T1023401D' WHERE Id = '61d7aebf-be2e-53ef-932b-74c2663e9231';  -- was Sibling 1 of Nadia Karim
UPDATE dbo.fas_household_members SET FullName = N'Sara Karim', IdNumber = N'T2123402D' WHERE Id = '4d773e0c-4db2-52d5-bb7c-ea7ac371abfd';  -- was Sibling 2 of Nadia Karim
UPDATE dbo.fas_household_members SET FullName = N'Emma Chua', IdNumber = N'T1223403H' WHERE Id = 'c8475f8e-0f6c-5da8-b6df-9850f8729b1d';  -- was Sibling 1 of Ethan Chua
UPDATE dbo.fas_household_members SET FullName = N'Nur Iman', IdNumber = N'T1923404A' WHERE Id = '94ad37cb-b912-5e75-87f9-fe9ac223367b';  -- was Sibling 1 of Nur Aisyah
UPDATE dbo.fas_household_members SET IdNumber = N'S7912340D' WHERE Id = 'cb418ee3-1bfe-54e5-aee4-00bddbe78a60';  -- Spouse of Nadia Karim (Father)

COMMIT TRANSACTION;
/* Undo by hand: run R4_FAS_Seed_Data.sql again on an empty database, or delete the rows above by Id. */