@echo off
rem R4 UI automation runner for Windows with Allure report and video generation.
rem The suite runs on the REAL admin portal at http://localhost:5173 (tests/real). Start the stack first (run_edufams_update.cmd).
rem   run_r4_automation.cmd                 smoke: sign in and open the main screens
rem   run_r4_automation.cmd real            every real test (reads and creates data with the prefix R4-AUTO)
rem   run_r4_automation.cmd readonly        only tests that do not create data
rem   run_r4_automation.cmd mutating        only tests that create data
rem   run_r4_automation.cmd suite 14        one suite, F4.14 here (13 to 16 have real screens)
rem   run_r4_automation.cmd tc 183          one case, TC-183 here
rem   run_r4_automation.cmd sbfas          SBFAS schemes of the School user (TC-169, 173, 201 to 203, 222 to 228, 241)
rem   run_r4_automation.cmd validation     validation rules of the schemes (TC-161, 165, 225, 268 to 314: API and wizard messages)
rem   run_r4_automation.cmd draft           real tests whose expected result waits for a BA decision
rem   run_r4_automation.cmd defects         real tests that assert the FS against a defect confirmed in the code
rem   run_r4_automation.cmd cleanup         soft-delete the schemes created by the suite (name starts with R4-AUTO)
rem   run_r4_automation.cmd allure          open existing Allure report in browser
rem   run_r4_automation.cmd proto | protoall | protosuite N | prototc NNN   LEGACY prototype on Vercel (296 cases), not for the real stack
rem   add the word headed at the end to watch the browser, for example: run_r4_automation.cmd tc 183 headed
rem   R4_BASE_URL overrides the address, R4_HQ_USER and R4_HQ_PASS override the MOE HQ account of the seed.
setlocal EnableExtensions
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

set "MODE=%~1"
if "%MODE%"=="" set "MODE=smoke"
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

if /i "%MODE%"=="cleanup" goto :cleanup

set "SEL=tests/real"
if /i "%MODE%"=="smoke" set "SEL=tests/real -m smoke"
if /i "%MODE%"=="real" set "SEL=tests/real"
if /i "%MODE%"=="all" set "SEL=tests/real"
if /i "%MODE%"=="readonly" set "SEL=tests/real -m readonly"
if /i "%MODE%"=="mutating" set "SEL=tests/real -m mutating"
if /i "%MODE%"=="proto" call :legacy "tests --ignore=tests/real -m smoke"
if /i "%MODE%"=="protoall" call :legacy "tests --ignore=tests/real"
if /i "%MODE%"=="protosuite" call :legacy "tests --ignore=tests/real -m f4%ARG%"
if /i "%MODE%"=="prototc" call :legacy "tests --ignore=tests/real -k tc_%ARG%"
if /i "%MODE%"=="suite" set "SEL=tests/real -m f4%ARG%"
if /i "%MODE%"=="tc" set "SEL=tests/real -k tc_%ARG%"
if /i "%MODE%"=="sbfas" set "SEL=tests/real -m sbfas"
if /i "%MODE%"=="validation" set "SEL=tests/real -m validation"
if /i "%MODE%"=="draft" set "SEL=tests/real -m draft"
if /i "%MODE%"=="defects" set "SEL=tests/real -m known_defect"

where py >nul 2>&1 && (set "PY=py -3") || (set "PY=python")
if not exist ".venv\Scripts\python.exe" (
  echo Creating the virtual environment...
  %PY% -m venv .venv || goto :fail
)
set "VPY=.venv\Scripts\python.exe"
echo Installing the requirements...
"%VPY%" -m pip install --quiet --disable-pip-version-check -r requirements.txt || goto :fail

echo Running: pytest %SEL% --browser-channel chrome %HEADED%
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
echo Setup failed. Check that Python 3.9 or newer is installed and that pip can reach the internet.
exit /b 1

:cleanup
rem Soft-delete the schemes whose name starts with R4-AUTO (there is no delete API for MOEFAS).
set "FASDB=%R4_FAS_DB%"
if "%FASDB%"=="" set "FASDB=FASDatabase"
echo Cleaning R4-AUTO schemes in %FASDB% ...
docker exec -i edufams-qa-sqlserver bash -c "/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P \"$MSSQL_SA_PASSWORD\" -C -b -I -d %FASDB%" < tools\cleanup_r4_auto.sql
exit /b %ERRORLEVEL%

:legacy
set "SEL=%~1"
set "R4_BASE_URL=https://edusave.vercel.app"
set "R4_TARGET=prototype"
echo LEGACY mode: the prototype on Vercel. The localhost rule is for the real stack, do not use this mode as evidence for it.
exit /b 0
