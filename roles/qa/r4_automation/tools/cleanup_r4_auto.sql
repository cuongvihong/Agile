-- Soft-delete the MOEFAS schemes created by the R4 real UI suite (name starts with R4-AUTO).
-- There is no delete API for MOEFAS, the list hides rows with is_deleted = 1.
-- Run: run_r4_automation.cmd cleanup   (database name: set R4_FAS_DB when it is not FASDatabase; see SELECT name FROM sys.databases)
SET NOCOUNT ON;
SELECT COUNT(*) AS auto_schemes_before FROM dbo.moe_fas_schemes WHERE name LIKE 'R4-AUTO-%' AND is_deleted = 0;
UPDATE dbo.moe_fas_schemes SET is_deleted = 1 WHERE name LIKE 'R4-AUTO-%' AND is_deleted = 0;
SELECT COUNT(*) AS auto_schemes_after FROM dbo.moe_fas_schemes WHERE name LIKE 'R4-AUTO-%' AND is_deleted = 0;
GO
-- SBFAS schemes created by the School user tests (name starts with R4-AUTO). Table name taken from the SBFAS service; skipped when absent.
IF OBJECT_ID('dbo.sbfas_schemes') IS NOT NULL
BEGIN
    EXEC('UPDATE dbo.sbfas_schemes SET is_deleted = 1 WHERE name LIKE ''R4-AUTO-%'' AND is_deleted = 0');
    PRINT 'SBFAS schemes R4-AUTO soft-deleted';
END
ELSE PRINT 'dbo.sbfas_schemes not found in this database, check SELECT name FROM sys.tables WHERE name LIKE ''%sbfas%''';
GO
