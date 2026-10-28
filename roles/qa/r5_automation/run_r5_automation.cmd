@echo off
rem ============================================================================
rem  R5 (FS F5 Paper Applications) UI Automation Runner
rem  Supports Localhost (http://localhost:5173), Allure single-file report & ~5s videos
rem ============================================================================
rem   run_r5_automation.cmd                 default: real UI tests on localhost
rem   run_r5_automation.cmd real            run real hosted portal tests (TC-001..TC-006)
rem   run_r5_automation.cmd smoke           smoke test: school login & applications navigation
rem   run_r5_automation.cmd full            run all 12 suites (261 test cases)
rem   run_r5_automation.cmd suite 1         run suite F5.1 (1 to 12)
rem   run_r5_automation.cmd tc 001          run specific test case (e.g. TC-001)
rem   run_r5_automation.cmd allure          generate/open single-file Allure report with videos
rem   Add 'headed' at the end to run in visible browser mode: run_r5_automation.cmd real headed
rem ============================================================================
setlocal EnableExtensions
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

set "MODE=%~1"
if "%MODE%"=="" set "MODE=real"
set "ARG=%~2"
set "HEADED="
for %%A in (%*) do if /i "%%~A"=="headed" set "HEADED=--headed --slowmo 150"

if /i "%MODE%"=="allure" (
    if exist "artifacts\allure-report\index.html" (
        echo Opening Allure report...
        start "" "artifacts\allure-report\index.html"
        exit /b 0
    )
    if exist "artifacts\allure-results" (
        echo Generating Allure report...
        call allure generate artifacts\allure-results -o artifacts\allure-report --clean --single-file
        start "" "artifacts\allure-report\index.html"
        exit /b 0
    )
    echo No allure-results found. Please run tests first.
    exit /b 1
)

set "SEL=tests/test_real_hosted_portal.py"
if /i "%MODE%"=="real" set "SEL=tests/test_real_hosted_portal.py"
if /i "%MODE%"=="smoke" set "SEL=tests/test_00_smoke.py"
if /i "%MODE%"=="full" set "SEL=tests"
if /i "%MODE%"=="suite" set "SEL=tests -m f5%ARG%"
if /i "%MODE%"=="tc" set "SEL=tests -k tc_%ARG%"

:: Locate virtual environment (prefer local, fallback to sibling r4_automation virtualenv)
set "VPY="
if exist ".venv\Scripts\python.exe" set "VPY=.venv\Scripts\python.exe"
if "%VPY%"=="" if exist "..\r4_automation\.venv\Scripts\python.exe" set "VPY=..\r4_automation\.venv\Scripts\python.exe"
if "%VPY%"=="" if exist "..\r9_automation\.venv\Scripts\python.exe" set "VPY=..\r9_automation\.venv\Scripts\python.exe"

if "%VPY%"=="" (
    where py >nul 2>&1 && (set "PY=py -3") || (set "PY=python")
    echo Creating virtual environment...
    %PY% -m venv .venv || goto :fail
    set "VPY=.venv\Scripts\python.exe"
    echo Installing requirements...
    "%VPY%" -m pip install --quiet --disable-pip-version-check -r requirements.txt || goto :fail
)

echo ============================================================================
echo  EduFAMS R5 Automation Runner
echo  Target: [http://localhost:5173]
echo  Executing: pytest %SEL% --browser-channel chrome %HEADED%
echo ============================================================================
"%VPY%" -m pytest %SEL% --browser-channel chrome %HEADED%
set "RC=%ERRORLEVEL%"
echo.
echo Pytest finished with exit code %RC%

where allure >nul 2>&1
if not errorlevel 1 (
    echo.
    echo Generating Allure report ^(single-file mode with embedded videos^)...
    call allure generate artifacts\allure-results -o artifacts\allure-report --clean --single-file
    echo Allure report: artifacts\allure-report\index.html
) else (
    echo Note: 'allure' CLI not found in PATH. Results saved in artifacts\allure-results
)

if exist "artifacts\allure-report\index.html" (
    echo HTML reports ready:
    echo   - Allure report [with videos]: artifacts\allure-report\index.html
    echo   - Pytest HTML report:          artifacts\reports\report.html
)
exit /b %RC%

:fail
echo Setup failed. Check that Python 3.9+ is installed and network connectivity is active.
exit /b 1
