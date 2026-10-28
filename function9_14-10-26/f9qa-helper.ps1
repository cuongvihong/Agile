# f9qa-helper.ps1
# QA helper for Function 9. Listens on localhost only. Keep this window open while QA runs scenarios.
# Endpoints (GET):
#   /f9qa/reset     reset demo data of the demo student (QA-README section 9)
#   /f9qa/evidence  show invoices, items, transactions, funding legs, webhook receipts (QA-README section 12)
#   /f9qa/stop      stop this helper
param([int]$Port = 5199)
$ErrorActionPreference = 'Continue'
$Root = $PSScriptRoot
$compose = Join-Path $Root 'EduGovernment-Backend\deploy\docker\docker-compose.infra.yml'
if (-not (Test-Path $compose)) { Write-Host "FAIL: compose file not found: $compose"; exit 1 }
$text = Get-Content -Raw $compose
$m = [regex]::Match($text, 'MSSQL_SA_PASSWORD:\s*["'']?([^"''\r\n\s]+)')
if (-not $m.Success) { Write-Host 'FAIL: SA password not found in compose file'; exit 1 }
$sa = $m.Groups[1].Value
$container = 'template-sqlserver'

$resetSql = @'
USE [BillingPaymentService];
SET ANSI_NULLS ON;
SET ANSI_PADDING ON;
SET ANSI_WARNINGS ON;
SET ARITHABORT ON;
SET CONCAT_NULL_YIELDS_NULL ON;
SET QUOTED_IDENTIFIER ON;
SET NUMERIC_ROUNDABORT OFF;
SET XACT_ABORT ON;
DECLARE @StudentId UNIQUEIDENTIFIER = '11111111-1111-1111-1111-111111111111';
DECLARE @ids TABLE (Id VARCHAR(50));
INSERT INTO @ids SELECT Id FROM dbo.invoices WHERE StudentId = @StudentId;
BEGIN TRY
  BEGIN TRANSACTION;
  DELETE FROM dbo.payment_webhook_receipts WHERE FundingTransactionId IN (SELECT Id FROM dbo.transaction_funding_sources WHERE TransactionId IN (SELECT Id FROM dbo.transactions WHERE InvoiceId IN (SELECT Id FROM @ids)));
  DELETE FROM dbo.transaction_funding_sources WHERE TransactionId IN (SELECT Id FROM dbo.transactions WHERE InvoiceId IN (SELECT Id FROM @ids));
  DELETE FROM dbo.transactions WHERE InvoiceId IN (SELECT Id FROM @ids);
  DELETE FROM dbo.invoice_items WHERE InvoiceId IN (SELECT Id FROM @ids);
  DELETE FROM dbo.invoices WHERE Id IN (SELECT Id FROM @ids);
  COMMIT TRANSACTION;
END TRY
BEGIN CATCH
  IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
  THROW;
END CATCH;
PRINT 'reset done';
'@

$evidenceSql = @'
USE [BillingPaymentService];
SET NOCOUNT ON;
DECLARE @StudentId UNIQUEIDENTIFIER = '11111111-1111-1111-1111-111111111111';
DECLARE @InvoiceId VARCHAR(50) = (SELECT TOP 1 Id FROM dbo.invoices WHERE StudentId = @StudentId ORDER BY CreatedAt DESC);
PRINT '== invoices ==';
SELECT * FROM dbo.invoices WHERE Id = @InvoiceId;
PRINT '== invoice_items ==';
SELECT * FROM dbo.invoice_items WHERE InvoiceId = @InvoiceId ORDER BY LineNumber;
PRINT '== transactions ==';
SELECT * FROM dbo.transactions WHERE InvoiceId = @InvoiceId ORDER BY CreatedAt DESC;
PRINT '== transaction_funding_sources ==';
SELECT fs.* FROM dbo.transaction_funding_sources fs JOIN dbo.transactions tx ON tx.Id = fs.TransactionId WHERE tx.InvoiceId = @InvoiceId ORDER BY fs.SequenceNumber;
PRINT '== payment_webhook_receipts ==';
SELECT wr.* FROM dbo.payment_webhook_receipts wr JOIN dbo.transaction_funding_sources fs ON fs.Id = wr.FundingTransactionId JOIN dbo.transactions tx ON tx.Id = fs.TransactionId WHERE tx.InvoiceId = @InvoiceId ORDER BY wr.ReceivedAt;
PRINT '== counts for demo student ==';
SELECT (SELECT COUNT(*) FROM dbo.invoices WHERE StudentId = @StudentId) AS invoices, (SELECT COUNT(*) FROM dbo.invoice_items ii JOIN dbo.invoices i ON i.Id = ii.InvoiceId WHERE i.StudentId = @StudentId) AS invoice_items;
'@

function Invoke-Sql([string]$sql) {
  $f = Join-Path $env:TEMP 'f9qa-query.sql'
  [System.IO.File]::WriteAllText($f, $sql, (New-Object System.Text.UTF8Encoding($false)))
  cmd /c "docker cp ""$f"" ${container}:/tmp/f9qa-query.sql >nul 2>&1"
  $out = & docker exec $container /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P $sa -C -b -W -s '|' -w 400 -i /tmp/f9qa-query.sql 2>&1
  return @{ code = $LASTEXITCODE; text = ($out | Out-String) }
}

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")
try { $listener.Start() } catch { Write-Host "FAIL: cannot listen on port $Port : $($_.Exception.Message)"; exit 1 }
Write-Host "QA helper listening on http://localhost:$Port/f9qa/  (reset, evidence, stop). Keep this window open."
$stop = $false
while ($listener.IsListening -and -not $stop) {
  $ctx = $listener.GetContext()
  $path = $ctx.Request.Url.AbsolutePath
  $stamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss') + 'Z'
  switch ($path) {
    '/f9qa/reset'    { $r = Invoke-Sql $resetSql;    $body = "reset at $stamp, exit code $($r.code)`n$($r.text)" }
    '/f9qa/evidence' { $r = Invoke-Sql $evidenceSql; $body = "evidence at $stamp, exit code $($r.code)`n$($r.text)" }
    '/f9qa/stop'     { $body = 'stopping'; $stop = $true }
    default          { $body = 'unknown path' }
  }
  Write-Host "$stamp $path"
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
  $ctx.Response.ContentType = 'text/plain; charset=utf-8'
  $ctx.Response.ContentLength64 = $bytes.Length
  $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
  $ctx.Response.Close()
}
$listener.Stop()
