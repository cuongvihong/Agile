-- Soft-delete the schemes created by the Gavin UAT suite (name starts with UAT-GAVIN-).
-- The UI has no delete for MOEFAS schemes and no delete for published SBFAS schemes. The lists hide rows with is_deleted = 1.
-- Run it against the FAS database (name: SELECT name FROM sys.databases). Example with the container of the stack:
--   docker exec -i edufams-qa-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -d FASDatabase -i /dev/stdin < tools/cleanup_uat_schemes.sql
SET NOCOUNT ON;
SELECT COUNT(*) AS uat_moefas_before FROM dbo.moe_fas_schemes WHERE name LIKE 'UAT-GAVIN-%' AND is_deleted = 0;
UPDATE dbo.moe_fas_schemes SET is_deleted = 1 WHERE name LIKE 'UAT-GAVIN-%' AND is_deleted = 0;
SELECT COUNT(*) AS uat_moefas_after FROM dbo.moe_fas_schemes WHERE name LIKE 'UAT-GAVIN-%' AND is_deleted = 0;
GO
IF OBJECT_ID('dbo.sbfas_schemes') IS NOT NULL
BEGIN
    EXEC('UPDATE dbo.sbfas_schemes SET is_deleted = 1 WHERE name LIKE ''UAT-GAVIN-%'' AND is_deleted = 0');
    PRINT 'SBFAS schemes UAT-GAVIN soft-deleted';
END
ELSE PRINT 'dbo.sbfas_schemes not found in this database';
GO
