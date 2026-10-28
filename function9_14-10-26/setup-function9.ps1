# Function 9 local setup for QA (follows QA-README.md in function9_14-10-26.zip).
# Usage: extract the zip, copy this file into the extracted root (the folder that contains
# EduGovernment-Backend and EduGovernment-FrontEnd), then in PowerShell run:
#   powershell -ExecutionPolicy Bypass -File .\setup-function9.ps1
# It installs nothing. It checks prerequisites, starts SQL Server in Docker, opens one window
# each for Billing API, Payment Simulator API and the two frontends, then runs health checks.

param([string]$Root = $PSScriptRoot)

# Continue (not Stop): Windows PowerShell 5.1 turns native stderr text (docker, npm) into terminating errors under Stop.
# Every native command below is checked through $LASTEXITCODE instead.
$ErrorActionPreference = 'Continue'
$backend  = Join-Path $Root 'EduGovernment-Backend'
$frontend = Join-Path $Root 'EduGovernment-FrontEnd'
$compose  = Join-Path $backend 'deploy\docker\docker-compose.infra.yml'

function Fail($msg) { Write-Host "FAIL: $msg" -ForegroundColor Red; exit 1 }
function Ok($msg)   { Write-Host "OK:   $msg" -ForegroundColor Green }

function Wait-Url($url, $seconds) {
    $end = (Get-Date).AddSeconds($seconds)
    while ((Get-Date) -lt $end) {
        try {
            $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
            if ($r.StatusCode -eq 200) { return $true }
        } catch { }
        Start-Sleep -Seconds 3
    }
    return $false
}

# 1. Folder layout
if (-not (Test-Path $backend))  { Fail "Not found: $backend. Put this script in the extracted package root." }
if (-not (Test-Path $frontend)) { Fail "Not found: $frontend" }
if (-not (Test-Path $compose))  { Fail "Not found: $compose" }
Ok "Package layout found at $Root"

# 2. Prerequisites (not installed by this script)
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { Fail 'docker not found. Install and start Docker Desktop.' }
function Test-DockerEngine { cmd /c 'docker info >nul 2>&1'; return ($LASTEXITCODE -eq 0) }
if (-not (Test-DockerEngine)) {
    $dd = Join-Path $env:ProgramFiles 'Docker\Docker\Docker Desktop.exe'
    if (Test-Path $dd) { Write-Host 'Docker engine is not running. Starting Docker Desktop...'; Start-Process $dd }
    else { Write-Host 'Docker engine is not running. Start Docker Desktop manually.' }
    $up = $false
    for ($i = 0; $i -lt 60; $i++) {
        Start-Sleep -Seconds 5
        if (Test-DockerEngine) { $up = $true; break }
        Write-Host '  waiting for Docker engine...'
    }
    if (-not $up) { Fail 'Docker engine did not start within 5 minutes. Open Docker Desktop, finish its first-run steps (terms, WSL), then run this script again.' }
}
Ok 'Docker engine is running'

if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) { Fail 'dotnet not found. As Administrator run: winget install --id Microsoft.DotNet.SDK.10 --exact --source winget, then open a new PowerShell.' }
$sdks = (& dotnet --list-sdks) -join "`n"
if ($sdks -notmatch '(?m)^10\.') { Fail ".NET 10 SDK not found. Installed SDKs:`n$sdks" }
Ok '.NET 10 SDK found'

if (-not (Get-Command node -ErrorAction SilentlyContinue)) { Fail 'node not found. Install Node.js 22.12 or newer.' }
$nodeVer = [version]((& node -v).TrimStart('v'))
if ($nodeVer -lt [version]'22.12.0') { Fail "Node $nodeVer is too old. Need 22.12 or newer." }
Ok "Node $nodeVer"
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { Fail 'npm not found.' }

# 3. SQL Server container (same compose file as QA-README section 4)
Push-Location $backend
& docker compose -f '.\deploy\docker\docker-compose.infra.yml' up -d sqlserver
if ($LASTEXITCODE -ne 0) { Pop-Location; Fail 'docker compose up failed. Check that port 1433 is free.' }
Pop-Location

$healthy = $false
for ($i = 0; $i -lt 40; $i++) {
    $state = (cmd /c 'docker inspect --format {{.State.Health.Status}} template-sqlserver 2>nul')
    if ($state -eq 'healthy') { $healthy = $true; break }
    Start-Sleep -Seconds 5
}
if (-not $healthy) { Fail 'template-sqlserver did not become healthy within 200 seconds. Run: docker logs template-sqlserver' }
Ok 'SQL Server container is healthy'

# SA password is read from the compose file so it is not duplicated here.
$composeText = Get-Content $compose -Raw
$m = [regex]::Match($composeText, 'MSSQL_SA_PASSWORD:\s*["'']?([^"''\r\n\s]+)')
if (-not $m.Success) { Fail 'Could not read MSSQL_SA_PASSWORD from the compose file.' }
$sa = $m.Groups[1].Value
$conn = "Server=localhost,1433;Database=BillingPaymentService;User Id=sa;Password=$sa;TrustServerCertificate=True;MultipleActiveResultSets=True;"

# 4. Billing API and Payment Simulator API, one window each (QA-README sections 5 and 6)
$billingCmd = "`$env:Database__ConnectionString='$conn'; `$env:Database__AutoMigrate='true'; Set-Location '$backend'; dotnet run --project .\BillingPaymentService\API\BillingPaymentService.API.csproj --launch-profile http"
Start-Process powershell -ArgumentList @('-NoExit', '-Command', $billingCmd)
$simCmd = "Set-Location '$backend'; dotnet run --project .\Simulation\OnlinePaymentGatewaySimulation\OnlinePaymentGatewaySimulation.csproj --launch-profile http"
Start-Process powershell -ArgumentList @('-NoExit', '-Command', $simCmd)

# 5. Frontend install, then two dev servers (QA-README section 7)
Push-Location $frontend
& npm ci
if ($LASTEXITCODE -ne 0) { Pop-Location; Fail 'npm ci failed.' }
Pop-Location
Start-Process powershell -ArgumentList @('-NoExit', '-Command', "Set-Location '$frontend'; npm run dev:payment-checkout")
Start-Process powershell -ArgumentList @('-NoExit', '-Command', "Set-Location '$frontend'; npm run dev:eservice")

# 6. Health checks (first dotnet build can take a few minutes)
Write-Host 'Waiting for services (up to 4 minutes each)...'
if (Wait-Url 'http://localhost:5008/health' 240) { Ok 'Billing API  http://localhost:5008/health' } else { Write-Host 'FAIL: Billing API not healthy. See its window.' -ForegroundColor Red }
if (Wait-Url 'http://localhost:5286/health' 240) { Ok 'Simulator API http://localhost:5286/health' } else { Write-Host 'FAIL: Simulator API not healthy. See its window.' -ForegroundColor Red }
if (Wait-Url 'http://localhost:5174' 120) { Ok 'E-service FE  http://localhost:5174' } else { Write-Host 'FAIL: e-service not reachable.' -ForegroundColor Red }
if (Wait-Url 'http://localhost:5176' 120) { Ok 'Simulator FE  http://localhost:5176' } else { Write-Host 'FAIL: simulator FE not reachable.' -ForegroundColor Red }

# 7. Seed data check (QA-README section 8): expect 3 charges, total 470.00
try {
    $charges = Invoke-RestMethod -ErrorAction Stop 'http://localhost:5008/api/v1/students/11111111-1111-1111-1111-111111111111/outstanding-charges'
    Write-Host 'Outstanding charges response (expect 3 charges: 210.00, 140.00, 120.00):'
    $charges | ConvertTo-Json -Depth 6
} catch {
    Write-Host "FAIL: outstanding-charges request failed: $($_.Exception.Message)" -ForegroundColor Red
}

Start-Process 'http://localhost:5174'
Write-Host 'Done. Reset demo data before each scenario (QA-README section 9).'
