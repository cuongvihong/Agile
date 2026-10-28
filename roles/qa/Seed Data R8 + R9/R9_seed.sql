/* =====================================================================
   FS-09 (R9) seed data – Billing & Payment database (BillingPaymentService). Built on the R4 FAS seed.
   Tables: invoices, invoice_items, transactions, transaction_funding_sources, payment_webhook_receipts.
   Generated 22/10/2026.

   Every invoice line is one R4 student_charges row (StudentChargeId = R4 id, gross = R4 total_amount incl. GST),
   plus 6 added charges (AX01–AX06, created by R4_addon.sql). SchoolId = R4 school id.
   Subsidy = R4 fas_charge_subsidies (Active row) for open invoices. R4 rule: paid charges get no subsidy.
   @ApplyFasSubsidy = 0 sets every subsidy to 0 (FS R9 BR-F9-08, Sprint 1 shows gross amounts).
   Payments exist only on invoices without a subsidy, so they are valid with either setting.

   Run R8_seed.sql in the Education Account DB too: EA legs point to its ledger rows (Transactions.Id).
   InitiatedByUserId = the R4 IAM user of the parent (IAM-PAR-S13 ...).
   Running it again deletes every billing row of the seed students (also rows QA created), then reloads.
   Times are UTC (SGT minus 8 hours).
   ===================================================================== */
SET NOCOUNT ON;
SET ANSI_NULLS ON; SET ANSI_PADDING ON; SET ANSI_WARNINGS ON; SET ARITHABORT ON;
SET CONCAT_NULL_YIELDS_NULL ON; SET QUOTED_IDENTIFIER ON; SET NUMERIC_ROUNDABORT OFF; SET XACT_ABORT ON;
DECLARE @ApplyFasSubsidy bit = 1;

DECLARE @Students TABLE (StudentId uniqueidentifier PRIMARY KEY);
INSERT INTO @Students VALUES
('099e7c9e-5fb0-5e4a-86d9-e83ac4dbd91f'),
('0c4b56e4-ccd1-5984-9b42-a230afce4da0'),
('268c34c2-fd39-53d9-84ec-1b73d9017eb8'),
('411830dc-c6e1-5369-ab7f-7f4b9f3f8bcb'),
('4bb745fa-f4f3-5649-9037-8af1ac4990d8'),
('fbd1f713-e3df-5f17-901a-e82ba802bab1'),
('5077e467-2178-5ed0-83eb-9ccbc7f62670'),
('9bbd2380-c031-5a59-b237-d5675039c4ba'),
('335a5f84-0d5d-5f52-ad35-2cb2a0624ad0'),
('f063b14b-8ec5-507d-84ad-9a9d36a79c26'),
('42d2b2a2-3667-5b78-98b4-0523ed57cc78'),
('1c184a76-640c-5ed3-94bf-662fbfde6b0a'),
('ab2ae1b9-d764-574d-8143-e1c53aa11684'),
('17a43e4c-1c02-506c-a1cd-8496050bded4'),
('0e607645-45cb-599e-8612-2a81b7ac6b14'),
('c7dfeb0f-001b-5629-8d6b-f24f03b5fe4c'),
('36da3b10-78ec-5e60-aa3a-36f6e68f1a9e'),
('2e336f0d-59ef-5573-b8dd-c954a7ee0f5c'),
('88f80eb3-c090-5bec-a88e-4fb152bf43c8'),
('30ae0708-2bc4-5fde-842f-f9cfade9d2ee'),
('6c32d7d8-255b-5fba-bfe0-75ba5ae9700a'),
('f92fc05c-82d3-5201-911a-89506354905e'),
('16757e15-60eb-57fa-b663-49d0f09c769e'),
('22341f5e-bd6b-518e-b041-047587501d61'),
('5c110cd2-87a3-5a26-b1db-89ceeb4fece8'),
('42a9c56e-48f4-5b97-b6d7-ace170bd9686'),
('b827b44a-b84d-5f7f-9655-15f0542b5e08'),
('3ce1818f-8347-5abf-8946-1ba0c147f8c6'),
('b22fbf63-0144-5bf1-9c87-e581fc6a5623'),
('a11d655d-de34-53cd-b571-abca5a125cab'),
('7b2a18a3-0026-5738-a049-508b46610042'),
('53d74451-35a6-57ec-96d0-0f2be42496fa'),
('df8ca327-fad8-54f2-862d-571b6709f84d'),
('ffdddb45-d5e1-59c3-bf4e-5a80c78dcfee'),
('0abf0daa-7cb9-53bf-9415-633df6fa0075'),
('60e588e9-d6c6-5874-89ac-6313f38f2a57'),
('846effd2-41d1-5065-b70d-3e0ff2fd6dc5'),
('58f65222-afff-5c05-80a6-d224c4896eea'),
('b46192b4-75b8-5aad-b33d-243368330c40'),
('86dfad05-d521-5a0f-a590-e34d8019900c'),
('8cca84ad-04f1-5104-955d-adceb4b4cf59'),
('96104658-0987-5736-a5ca-2db31eff79c9'),
('2ccf4f50-62b9-5a17-a3b7-4e406d65647d'),
('7d5c5252-dc16-5672-99a1-2a4384dee5af'),
('cf3b2867-2d47-57ba-8a7b-40096c05319f'),
('946a4b14-e29b-5c1e-a50a-fe387158e973'),
('d0afa544-b5e4-5f5b-964b-dc5b6c2ce1c9'),
('7517317f-a994-5ef0-bb50-6331156c2fac'),
('1e603d90-7019-5fd6-acc4-158f856d1a77'),
('08000000-0000-0000-0001-000000000101'),
('08000000-0000-0000-0001-000000000102'),
('08000000-0000-0000-0001-000000000103'),
('08000000-0000-0000-0001-000000000104'),
('08000000-0000-0000-0001-000000000105'),
('08000000-0000-0000-0001-000000000106');
DECLARE @Inv TABLE (Id varchar(50) PRIMARY KEY);
INSERT INTO @Inv SELECT Id FROM dbo.invoices WHERE StudentId IN (SELECT StudentId FROM @Students) OR Id LIKE 'R9-INV-%';

BEGIN TRY
BEGIN TRAN;
DELETE FROM dbo.payment_webhook_receipts
 WHERE FundingTransactionId IN (SELECT fs.Id FROM dbo.transaction_funding_sources fs JOIN dbo.transactions t ON t.Id = fs.TransactionId WHERE t.InvoiceId IN (SELECT Id FROM @Inv))
    OR Id LIKE 'R9-WHK-%';
DELETE FROM dbo.transaction_funding_sources WHERE TransactionId IN (SELECT Id FROM dbo.transactions WHERE InvoiceId IN (SELECT Id FROM @Inv));
DELETE FROM dbo.transactions WHERE InvoiceId IN (SELECT Id FROM @Inv);
DELETE FROM dbo.invoice_items WHERE InvoiceId IN (SELECT Id FROM @Inv);
DELETE FROM dbo.invoices WHERE Id IN (SELECT Id FROM @Inv);

INSERT INTO dbo.invoices (Id, StudentId, SchoolId, InvoiceNumber, CurrencyCode, GrossAmount, SubsidyAmount, NetAmount, Status, IssuedAt, DueDate, PaidAt, CancelledAt, CreatedAt, UpdatedAt) VALUES
('R9-INV-0101', '099e7c9e-5fb0-5e4a-86d9-e83ac4dbd91f', 'a82af704-e047-56b4-8490-cd68feb38d34', 'INV-2026-000101', 'SGD', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S01 Issued: Miscellaneous fee, Term 4 [CH01]
('R9-INV-0102', '0c4b56e4-ccd1-5984-9b42-a230afce4da0', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000102', 'SGD', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S02 Issued: Miscellaneous fee, Term 4 [CH02]
('R9-INV-0103', '0c4b56e4-ccd1-5984-9b42-a230afce4da0', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000103', 'SGD', 70.63, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 70.63 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-11-16', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T10:15:05.000'),  -- S02 Issued: School Meal Fee, Nov [CH03]
('R9-INV-0104', '268c34c2-fd39-53d9-84ec-1b73d9017eb8', '4a849167-7545-5bf8-b05b-e92a4438a636', 'INV-2026-000104', 'SGD', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S03 Issued: Miscellaneous fee, Term 4 [CH04]
('R9-INV-0105', '411830dc-c6e1-5369-ab7f-7f4b9f3f8bcb', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000105', 'SGD', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S04 Issued: Miscellaneous fee, Term 4 [CH05]
('R9-INV-0106', '4bb745fa-f4f3-5649-9037-8af1ac4990d8', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000106', 'SGD', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 3, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-21T08:40:10.000'),  -- S05 PaymentPending: Miscellaneous fee, Term 4 [CH06]
('R9-INV-0107', 'fbd1f713-e3df-5f17-901a-e82ba802bab1', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000107', 'SGD', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S06 Issued: Miscellaneous fee, Term 4 [CH07]
('R9-INV-0108', 'fbd1f713-e3df-5f17-901a-e82ba802bab1', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000108', 'SGD', 70.63, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 70.63 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-11-16', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S06 Issued: School Meal Fee, Nov [CH08]
('R9-INV-0109', '5077e467-2178-5ed0-83eb-9ccbc7f62670', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000109', 'SGD', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S07 Issued: Miscellaneous fee, Term 4 [CH09]
('R9-INV-0110', '5077e467-2178-5ed0-83eb-9ccbc7f62670', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000110', 'SGD', 10.90, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 10.90 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 5, '2026-10-19T01:00:00.000', '2026-10-30', NULL, '2026-10-12T02:00:00.000', '2026-10-19T00:00:00.000', '2026-10-12T02:00:00.000'),  -- S07 Cancelled: Service charge, Term 4 [AX03]
('R9-INV-0111', '9bbd2380-c031-5a59-b237-d5675039c4ba', 'a82af704-e047-56b4-8490-cd68feb38d34', 'INV-2026-000111', 'SGD', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 3, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-20T13:15:00.000'),  -- S08 PaymentPending: Miscellaneous fee, Term 4 [CH10]
('R9-INV-0112', '335a5f84-0d5d-5f52-ad35-2cb2a0624ad0', '4a849167-7545-5bf8-b05b-e92a4438a636', 'INV-2026-000112', 'SGD', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S09 Issued: Miscellaneous fee, Term 4 [CH11]
('R9-INV-0113', 'f063b14b-8ec5-507d-84ad-9a9d36a79c26', 'a82af704-e047-56b4-8490-cd68feb38d34', 'INV-2026-000113', 'SGD', 36.33, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 36.33 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-07-13T01:00:00.000', '2026-07-31', NULL, NULL, '2026-07-13T00:00:00.000', '2026-07-13T01:00:00.000'),  -- S10 Issued: Miscellaneous fee, Term 3 [AX01]
('R9-INV-0114', 'f063b14b-8ec5-507d-84ad-9a9d36a79c26', 'a82af704-e047-56b4-8490-cd68feb38d34', 'INV-2026-000114', 'SGD', 47.23, CASE WHEN @ApplyFasSubsidy = 1 THEN 25.00 ELSE 0.00 END, 47.23 - CASE WHEN @ApplyFasSubsidy = 1 THEN 25.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S10 Issued: Miscellaneous fee, Term 4 + Service charge, Term 4 [CH12, CH14]
('R9-INV-0115', 'f063b14b-8ec5-507d-84ad-9a9d36a79c26', 'a82af704-e047-56b4-8490-cd68feb38d34', 'INV-2026-000115', 'SGD', 36.33, CASE WHEN @ApplyFasSubsidy = 1 THEN 16.67 ELSE 0.00 END, 36.33 - CASE WHEN @ApplyFasSubsidy = 1 THEN 16.67 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-11-16', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S10 Issued: School Meal Fee, Nov [CH13]
('R9-INV-0116', 'f063b14b-8ec5-507d-84ad-9a9d36a79c26', 'a82af704-e047-56b4-8490-cd68feb38d34', 'INV-2026-000116', 'SGD', 36.33, CASE WHEN @ApplyFasSubsidy = 1 THEN 16.67 ELSE 0.00 END, 36.33 - CASE WHEN @ApplyFasSubsidy = 1 THEN 16.67 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-12-15', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S10 Issued: School Meal Fee, Dec [AX02]
('R9-INV-0117', '42d2b2a2-3667-5b78-98b4-0523ed57cc78', '4a849167-7545-5bf8-b05b-e92a4438a636', 'INV-2026-000117', 'SGD', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 12.50 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 12.50 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S11 Issued: Miscellaneous fee, Term 4 [CH15]
('R9-INV-0118', '1c184a76-640c-5ed3-94bf-662fbfde6b0a', 'a82af704-e047-56b4-8490-cd68feb38d34', 'INV-2026-000118', 'SGD', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 12.50 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 12.50 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S12 Issued: Miscellaneous fee, Term 4 [CH16]
('R9-INV-0119', 'ab2ae1b9-d764-574d-8143-e1c53aa11684', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000119', 'SGD', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 4, '2026-10-05T01:00:00.000', '2026-10-30', '2026-10-08T02:12:03.000', NULL, '2026-10-05T00:00:00.000', '2026-10-08T02:12:03.000'),  -- S13 Paid: Miscellaneous fee, Term 4 [CH17]
('R9-INV-0120', '17a43e4c-1c02-506c-a1cd-8496050bded4', 'a82af704-e047-56b4-8490-cd68feb38d34', 'INV-2026-000120', 'SGD', 21.80, CASE WHEN @ApplyFasSubsidy = 1 THEN 15.00 ELSE 0.00 END, 21.80 - CASE WHEN @ApplyFasSubsidy = 1 THEN 15.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S14 Issued: Miscellaneous fee, Term 4 [CH18]
('R9-INV-0121', 'c7dfeb0f-001b-5629-8d6b-f24f03b5fe4c', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000121', 'SGD', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 4, '2026-07-13T01:00:00.000', '2026-07-31', '2026-07-20T12:34:40.000', NULL, '2026-07-13T00:00:00.000', '2026-07-20T12:34:40.000'),  -- S16 Paid: Miscellaneous fee, Term 3 [CH20]
('R9-INV-0122', 'c7dfeb0f-001b-5629-8d6b-f24f03b5fe4c', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000122', 'SGD', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 14.63 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 14.63 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S16 Issued: Miscellaneous fee, Term 4 [CH19]
('R9-INV-0123', '2e336f0d-59ef-5573-b8dd-c954a7ee0f5c', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000123', 'SGD', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S18 Issued: Miscellaneous fee, Term 4 [CH21]
('R9-INV-0124', '88f80eb3-c090-5bec-a88e-4fb152bf43c8', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000124', 'SGD', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S19 Issued: Miscellaneous fee, Term 4 [CH22]
('R9-INV-0125', '30ae0708-2bc4-5fde-842f-f9cfade9d2ee', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000125', 'SGD', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S20 Issued: Miscellaneous fee, Term 4 [CH23]
('R9-INV-0126', '5c110cd2-87a3-5a26-b1db-89ceeb4fece8', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000126', 'SGD', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 25.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 25.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S25 Issued: Miscellaneous fee, Term 4 [CH24]
('R9-INV-0127', '5c110cd2-87a3-5a26-b1db-89ceeb4fece8', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000127', 'SGD', 70.63, CASE WHEN @ApplyFasSubsidy = 1 THEN 64.80 ELSE 0.00 END, 70.63 - CASE WHEN @ApplyFasSubsidy = 1 THEN 64.80 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-11-16', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S25 Issued: School Meal Fee, Nov [CH25]
('R9-INV-0128', 'b827b44a-b84d-5f7f-9655-15f0542b5e08', '11182d1f-64d9-52e2-9ab7-d86d82d0db0f', 'INV-2026-000128', 'SGD', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- S27 Issued: Miscellaneous fee, Term 4 [CH26]
('R9-INV-0129', '08000000-0000-0000-0001-000000000101', 'a82af704-e047-56b4-8490-cd68feb38d34', 'INV-2026-000129', 'SGD', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- X01 Issued: Miscellaneous fee, Term 4 [AX04]
('R9-INV-0130', '08000000-0000-0000-0001-000000000103', 'a82af704-e047-56b4-8490-cd68feb38d34', 'INV-2026-000130', 'SGD', 36.33, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 36.33 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000'),  -- X03 Issued: Miscellaneous fee, Term 4 [AX06]
('R9-INV-0131', '08000000-0000-0000-0001-000000000105', '4a849167-7545-5bf8-b05b-e92a4438a636', 'INV-2026-000131', 'SGD', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 2, '2026-10-19T01:00:00.000', '2026-10-30', NULL, NULL, '2026-10-19T00:00:00.000', '2026-10-19T01:00:00.000');  -- X05 Issued: Miscellaneous fee, Term 4 [AX05]

INSERT INTO dbo.invoice_items (Id, InvoiceId, LineNumber, StudentChargeId, GrossAmount, SubsidyAmount, NetAmount) VALUES
('R9-ITM-0001', 'R9-INV-0101', 1, '3752f7c8-2dd1-575f-93db-86b05c58881f', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH01 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0002', 'R9-INV-0102', 1, 'd41a5fcf-d3a3-524a-9933-e2cd68129261', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH02 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0003', 'R9-INV-0103', 1, '39daff2c-1310-589f-bb21-f215f90db6f1', 70.63, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 70.63 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH03 School Meal Fee, Nov (R4)
('R9-ITM-0004', 'R9-INV-0104', 1, '6046b530-cf4d-5d7e-9797-83c68a33f850', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH04 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0005', 'R9-INV-0105', 1, 'd86260eb-6290-572c-bf56-61d1cbeb1522', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH05 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0006', 'R9-INV-0106', 1, '5023c7f7-523d-5a96-be0b-1f8eb17dd7e4', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH06 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0007', 'R9-INV-0107', 1, '4cc2a6a2-65ab-513b-81c8-27dd1fc19df5', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH07 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0008', 'R9-INV-0108', 1, '98b134be-5493-5b6f-91ec-d595085f7b09', 70.63, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 70.63 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH08 School Meal Fee, Nov (R4)
('R9-ITM-0009', 'R9-INV-0109', 1, '2842e306-d17b-58dc-a292-7e72ba07b5a5', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH09 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0010', 'R9-INV-0110', 1, '08000000-0000-0000-0004-000000000003', 10.90, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 10.90 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- AX03 Service charge, Term 4 (Added)
('R9-ITM-0011', 'R9-INV-0111', 1, '2b57704b-21d2-5857-80f8-a5204385b48e', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH10 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0012', 'R9-INV-0112', 1, '3b9497d5-6e66-5742-8103-a522cf151ca4', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH11 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0013', 'R9-INV-0113', 1, '08000000-0000-0000-0004-000000000001', 36.33, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 36.33 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- AX01 Miscellaneous fee, Term 3 (Added)
('R9-ITM-0014', 'R9-INV-0114', 1, '5cbcfe65-079d-5a80-bb38-90a6713acf5b', 36.33, CASE WHEN @ApplyFasSubsidy = 1 THEN 25.00 ELSE 0.00 END, 36.33 - CASE WHEN @ApplyFasSubsidy = 1 THEN 25.00 ELSE 0.00 END),  -- CH12 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0015', 'R9-INV-0114', 2, 'be4ba0cd-78ac-53b3-a4a1-ff44248a702d', 10.90, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 10.90 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH14 Service charge, Term 4 (R4)
('R9-ITM-0016', 'R9-INV-0115', 1, '8eeaa461-b553-5080-8055-20f20cdf80cb', 36.33, CASE WHEN @ApplyFasSubsidy = 1 THEN 16.67 ELSE 0.00 END, 36.33 - CASE WHEN @ApplyFasSubsidy = 1 THEN 16.67 ELSE 0.00 END),  -- CH13 School Meal Fee, Nov (R4)
('R9-ITM-0017', 'R9-INV-0116', 1, '08000000-0000-0000-0004-000000000002', 36.33, CASE WHEN @ApplyFasSubsidy = 1 THEN 16.67 ELSE 0.00 END, 36.33 - CASE WHEN @ApplyFasSubsidy = 1 THEN 16.67 ELSE 0.00 END),  -- AX02 School Meal Fee, Dec (Added)
('R9-ITM-0018', 'R9-INV-0117', 1, 'fbb0b4d1-1b20-5353-91a2-4657b2c1b653', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 12.50 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 12.50 ELSE 0.00 END),  -- CH15 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0019', 'R9-INV-0118', 1, 'ecd03bf5-54a2-54d3-921d-5e6d0f1885f9', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 12.50 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 12.50 ELSE 0.00 END),  -- CH16 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0020', 'R9-INV-0119', 1, '36bb6540-402e-56d2-8f37-7c356eceb3a7', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH17 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0021', 'R9-INV-0120', 1, '897757fe-4109-551b-8089-c54881d54724', 21.80, CASE WHEN @ApplyFasSubsidy = 1 THEN 15.00 ELSE 0.00 END, 21.80 - CASE WHEN @ApplyFasSubsidy = 1 THEN 15.00 ELSE 0.00 END),  -- CH18 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0022', 'R9-INV-0121', 1, 'afc132ba-d40b-5c56-9d13-b70e8fffa64e', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH20 Miscellaneous fee, Term 3 (R4)
('R9-ITM-0023', 'R9-INV-0122', 1, '480228ee-b791-5c13-a78e-b7c936798855', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 14.63 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 14.63 ELSE 0.00 END),  -- CH19 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0024', 'R9-INV-0123', 1, '5a5a1fde-c391-57d0-b0c3-b3496184be17', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH21 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0025', 'R9-INV-0124', 1, 'eea83607-d2bb-5c07-9b0d-24fc5e7fd583', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH22 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0026', 'R9-INV-0125', 1, '7d019bdb-ebb8-505d-9d10-84674deafb01', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH23 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0027', 'R9-INV-0126', 1, '972d6e79-27cb-5dbd-b004-10b1d35efd3c', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 25.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 25.00 ELSE 0.00 END),  -- CH24 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0028', 'R9-INV-0127', 1, 'f5d85280-dca2-5b1d-969d-ac9e6e4a9e5d', 70.63, CASE WHEN @ApplyFasSubsidy = 1 THEN 64.80 ELSE 0.00 END, 70.63 - CASE WHEN @ApplyFasSubsidy = 1 THEN 64.80 ELSE 0.00 END),  -- CH25 School Meal Fee, Nov (R4)
('R9-ITM-0029', 'R9-INV-0128', 1, 'e281631d-1c0e-5433-82f9-12ecb21f1785', 21.26, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 21.26 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- CH26 Miscellaneous fee, Term 4 (R4)
('R9-ITM-0030', 'R9-INV-0129', 1, '08000000-0000-0000-0004-000000000004', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- AX04 Miscellaneous fee, Term 4 (Added)
('R9-ITM-0031', 'R9-INV-0130', 1, '08000000-0000-0000-0004-000000000006', 36.33, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 36.33 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END),  -- AX06 Miscellaneous fee, Term 4 (Added)
('R9-ITM-0032', 'R9-INV-0131', 1, '08000000-0000-0000-0004-000000000005', 27.25, CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END, 27.25 - CASE WHEN @ApplyFasSubsidy = 1 THEN 0.00 ELSE 0.00 END);  -- AX05 Miscellaneous fee, Term 4 (Added)

INSERT INTO dbo.transactions (Id, InvoiceId, InitiatedByUserId, TransactionReference, IdempotencyKey, RequestedAmount, SettledAmount, CurrencyCode, Status, CreatedAt, UpdatedAt, CompletedAt) VALUES
('R9-TXN-0001', 'R9-INV-0119', 'IAM-PAR-S13', N'PAY-20261008-000001', 'seed-r9-r9-inv-0119-1', 21.26, NULL, 'SGD', 3, '2026-10-08T02:05:00.000', '2026-10-08T02:05:06.000', '2026-10-08T02:05:06.000'),  -- S13 Failed
('R9-TXN-0002', 'R9-INV-0119', 'IAM-PAR-S13', N'PAY-20261008-000002', 'seed-r9-r9-inv-0119-2', 21.26, 21.26, 'SGD', 2, '2026-10-08T02:12:00.000', '2026-10-08T02:12:03.000', '2026-10-08T02:12:03.000'),  -- S13 Succeeded
('R9-TXN-0003', 'R9-INV-0121', 'IAM-PAR-S16', N'PAY-20260720-000003', 'seed-r9-r9-inv-0121-1', 21.26, 21.26, 'SGD', 2, '2026-07-20T12:30:00.000', '2026-07-20T12:34:40.000', '2026-07-20T12:34:40.000'),  -- S16 Succeeded
('R9-TXN-0004', 'R9-INV-0111', 'IAM-PAR-S08', N'PAY-20261020-000004', 'seed-r9-r9-inv-0111-1', 27.25, NULL, 'SGD', 1, '2026-10-20T13:15:00.000', '2026-10-20T13:15:00.000', NULL),  -- S08 Pending
('R9-TXN-0005', 'R9-INV-0106', 'IAM-PAR-S05', N'PAY-20261021-000005', 'seed-r9-r9-inv-0106-1', 27.25, NULL, 'SGD', 5, '2026-10-21T08:40:00.000', '2026-10-21T08:40:10.000', NULL),  -- S05 ReconciliationRequired
('R9-TXN-0006', 'R9-INV-0103', 'IAM-PAR-S02', N'PAY-20261019-000006', 'seed-r9-r9-inv-0103-1', 70.63, NULL, 'SGD', 3, '2026-10-19T10:02:00.000', '2026-10-19T10:15:05.000', '2026-10-19T10:15:05.000');  -- S02 Failed

INSERT INTO dbo.transaction_funding_sources (Id, TransactionId, SequenceNumber, FundingReference, Method, RequestedAmount, SettledAmount, Status, WalletId, EducationAccountTransactionId, EducationAccountReversalTransactionId, ProviderCode, ProviderTransactionId, FailureCode, FailureReason, CreatedAt, UpdatedAt, CompletedAt) VALUES
('R9-FND-0001', 'R9-TXN-0001', 1, N'FND-20261008-000001-1', 1, 21.26, NULL, 3, '08000000-0000-0000-0002-000000000013', NULL, NULL, NULL, NULL, 'EA_DEBIT_FAILED', N'Education Account service did not complete the debit. No amount was deducted.', '2026-10-08T02:05:00.000', '2026-10-08T02:05:06.000', '2026-10-08T02:05:06.000'),  -- S13 EducationAccount Failed
('R9-FND-0002', 'R9-TXN-0002', 1, N'FND-20261008-000002-1', 1, 21.26, 21.26, 2, '08000000-0000-0000-0002-000000000013', 8000046, NULL, NULL, NULL, NULL, NULL, '2026-10-08T02:12:00.000', '2026-10-08T02:12:03.000', '2026-10-08T02:12:03.000'),  -- S13 EducationAccount Succeeded (R8 ledger TXN-000046)
('R9-FND-0003', 'R9-TXN-0003', 1, N'FND-20260720-000003-1', 1, 10.00, 10.00, 2, '08000000-0000-0000-0002-000000000016', 8000056, NULL, NULL, NULL, NULL, NULL, '2026-07-20T12:30:00.000', '2026-07-20T12:30:03.000', '2026-07-20T12:30:03.000'),  -- S16 EducationAccount Succeeded (R8 ledger TXN-000056)
('R9-FND-0004', 'R9-TXN-0003', 2, N'FND-20260720-000003-2', 2, 11.26, 11.26, 2, NULL, NULL, NULL, 'SANDBOX', 'sbx_pi_2026072000004', NULL, NULL, '2026-07-20T12:30:00.000', '2026-07-20T12:34:40.000', '2026-07-20T12:34:40.000'),  -- S16 OnlineGateway Succeeded
('R9-FND-0005', 'R9-TXN-0004', 1, N'FND-20261020-000004-1', 2, 27.25, NULL, 1, NULL, NULL, NULL, 'SANDBOX', NULL, NULL, NULL, '2026-10-20T13:15:00.000', '2026-10-20T13:15:00.000', NULL),  -- S08 OnlineGateway Pending
('R9-FND-0006', 'R9-TXN-0005', 1, N'FND-20261021-000005-1', 1, 27.25, NULL, 5, '08000000-0000-0000-0002-000000000005', NULL, NULL, NULL, NULL, 'EA_DEBIT_UNKNOWN', N'No reply from Education Account service. Result of the debit is not known.', '2026-10-21T08:40:00.000', '2026-10-21T08:40:10.000', NULL),  -- S05 EducationAccount ReconciliationRequired
('R9-FND-0007', 'R9-TXN-0006', 1, N'FND-20261019-000006-1', 1, 20.00, 20.00, 4, '08000000-0000-0000-0002-000000000002', 8000024, 8000026, NULL, NULL, NULL, NULL, '2026-10-19T10:02:00.000', '2026-10-19T10:15:05.000', '2026-10-19T10:15:05.000'),  -- S02 EducationAccount Reversed (R8 ledger TXN-000024, reversal TXN-000026)
('R9-FND-0008', 'R9-TXN-0006', 2, N'FND-20261019-000006-2', 2, 50.63, NULL, 3, NULL, NULL, NULL, 'SANDBOX', 'sbx_pi_2026101900008', 'PAYMENT_DECLINED', N'The payment was declined on the payment page.', '2026-10-19T10:02:00.000', '2026-10-19T10:14:50.000', '2026-10-19T10:14:50.000');  -- S02 OnlineGateway Failed

INSERT INTO dbo.payment_webhook_receipts (Id, FundingTransactionId, ProviderCode, ProviderEventId, ProviderTransactionId, FundingReference, EventType, PayloadHash, ProcessingStatus, ReceivedAt, ProcessedAt, ErrorMessage) VALUES
('R9-WHK-0001', 'R9-FND-0004', 'SANDBOX', 'sbx_evt_2026072000001', 'sbx_pi_2026072000004', N'FND-20260720-000003-2', 'payment.succeeded', HASHBYTES('SHA2_256', N'seed-r9:sbx_evt_2026072000001'), 2, '2026-07-20T12:34:40.000', '2026-07-20T12:34:42.000', NULL),  -- S16 payment.succeeded
('R9-WHK-0002', 'R9-FND-0008', 'SANDBOX', 'sbx_evt_2026101900002', 'sbx_pi_2026101900008', N'FND-20261019-000006-2', 'payment.failed', HASHBYTES('SHA2_256', N'seed-r9:sbx_evt_2026101900002'), 2, '2026-10-19T10:14:50.000', '2026-10-19T10:14:52.000', NULL);  -- S02 payment.failed

COMMIT;
END TRY
BEGIN CATCH
  IF @@TRANCOUNT > 0 ROLLBACK;
  THROW;
END CATCH;

SELECT i.InvoiceNumber, i.StudentId, i.GrossAmount, i.SubsidyAmount, i.NetAmount,
       CASE i.Status WHEN 2 THEN 'Issued' WHEN 3 THEN 'PaymentPending' WHEN 4 THEN 'Paid' WHEN 5 THEN 'Cancelled' END AS InvoiceStatus
FROM dbo.invoices i WHERE i.Id LIKE 'R9-INV-%' ORDER BY i.Id;

/* =====================================================================
   Scenario helpers
   AC-21 Cancel S18 Zachary Lee's invoice while the Parent is on SCR-04/05:
     UPDATE dbo.invoices SET Status = 5, CancelledAt = SYSUTCDATETIME(), UpdatedAt = SYSUTCDATETIME() WHERE InvoiceNumber = 'INV-2026-000123';
   AC-16 Lower S02 Aisha Rahman's EA balance before the split is confirmed (Education Account DB, R8 tables; set back to 2000 after):
     UPDATE dbo.Wallets SET Balance = 1000 WHERE Id = '08000000-0000-0000-0002-000000000002';  -- SGD 10.00
   ===================================================================== */