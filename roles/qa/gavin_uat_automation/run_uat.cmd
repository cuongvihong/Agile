@echo off
rem Chay bo UAT Gavin (uat-master 30/10/2026, gom 3 case seed UAT-PRE va cac case UAT) tren LOCALHOST. Moi case co video quay lai TUNG BUOC, anh chup va ket qua PASS, FAIL, BLOCKED, GAP.
rem   run_uat.cmd hosted headed        MOT LENH, tu tang vong seed: seed truoc (UAT-PRE-01..04) roi TOAN BO 35 case owner Gavin cua uat-master (MOE 6, SCH 9, PAR-01 8, PAR-02 9, PAR-03 3) va 3 case UAT-031, UAT-031-E1, UAT-033. Ket qua o artifacts\uat_summary.csv
rem   run_uat.cmd all hosted           chay het moi case cua bo (ke ca case cu cua nguoi khac, khong thuoc master Gavin)
rem   run_uat.cmd case UAT-PAR-01      mot case (cho phep dau *, vi du UAT-PAR-* hoac UAT-MOE-05*)
rem   run_uat.cmd group par            mot nhom: par, moe, sch
rem   run_uat.cmd seed                chi chay 3 case tien dieu kien UAT-PRE-01 (top-up), UAT-PRE-02 (phi) va UAT-PRE-03 (FAS: R6 ngan sach, R10 phu huynh nop don, duyet tu ngay hieu luc). Chung LUON chay truoc moi lan chay UAT, co video. UAT_SEED=0 bo qua, UAT_SEED=plan chi doc, UAT_SEED_RUN_CAMPAIGN=1 chay chien dich top-up
rem   run_uat.cmd report               chi xuat CSV tu lan chay truoc (artifacts\uat_summary.csv, uat_steps.csv)
rem   them chu headed o cuoi de xem trinh duyet chay truc tiep, vi du: run_uat.cmd case UAT-PAR-01 headed
rem Dia chi mac dinh: Admin https://admin.20-255-158-192.sslip.io, e-Service https://eservice.20-255-158-192.sslip.io. Dat UAT_ADMIN_URL, UAT_PARENT_URL (vi du http://localhost:5173 va 5174) de chay localhost. Bien tuy chon: UAT_CHECKOUT_URL (mac dinh http://localhost:5176), UAT_SLOW_MO (ms, mac dinh 250), UAT_STEP_PAUSE (ms, mac dinh 1200), UAT_NO_DB=1
rem   them chu hosted de chay tren moi truong host san (Admin https://admin.20-255-158-192.sslip.io, e-Service https://eservice.20-255-158-192.sslip.io), khong dung Docker/DB (UAT_NO_DB=1). Cong thanh toan gia lap mac dinh https://pay.20-255-158-192.sslip.io (doi bang UAT_CHECKOUT_URL).
rem   vi du: run_uat.cmd group par hosted   hoac   run_uat.cmd hosted headed
rem CHI CHAY TREN LOCALHOST, tru host nam trong UAT_ALLOW_HOSTS. Dia chi vercel.app bi chan, may khac localhost chi chay khi dat UAT_ALLOW_REMOTE=1.
setlocal EnableExtensions
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

if /i "%~1"=="report" goto :report

set "SEL=--uat-case UAT-MOE-01,UAT-MOE-04,UAT-MOE-05,UAT-MOE-05-E1,UAT-MOE-06,UAT-MOE-06-N1,UAT-SCH-01,UAT-SCH-01-N1,UAT-SCH-01-E1,UAT-SCH-02,UAT-SCH-02-N1,UAT-SCH-03,UAT-SCH-03-N1,UAT-SCH-04,UAT-SCH-04-E1,UAT-PAR-01,UAT-PAR-01-N1,UAT-PAR-01-N2,UAT-PAR-01-E1,UAT-PAR-01-N3,UAT-PAR-01-A1,UAT-PAR-01-N4,UAT-PAR-01-E2,UAT-PAR-02,UAT-PAR-02-N1,UAT-PAR-02-N2,UAT-PAR-02-E1,UAT-PAR-02-E2,UAT-PAR-02-A1,UAT-PAR-02-N3,UAT-PAR-02-A2,UAT-PAR-02-N4,UAT-PAR-03,UAT-PAR-03-A1,UAT-PAR-03-E1,UAT-031,UAT-031-E1,UAT-033"
if /i "%~1"=="all" set "SEL="
if /i "%~1"=="case" call :collect %*
if /i "%~1"=="case" set "SEL=--uat-case %CASES%"
if /i "%~1"=="group" set "SEL=--uat-case UAT-%~2-*"
if /i "%~1"=="seed" set "SEL=--uat-case UAT-PRE-*"
set "HEADED="
set "HOSTED="
for %%A in (%*) do if /i "%%~A"=="hosted" set "HOSTED=1"
if defined HOSTED (set "UAT_ADMIN_URL=https://admin.20-255-158-192.sslip.io" & set "UAT_PARENT_URL=https://eservice.20-255-158-192.sslip.io" & set "UAT_ALLOW_HOSTS=admin.20-255-158-192.sslip.io,eservice.20-255-158-192.sslip.io,pay.20-255-158-192.sslip.io" & set "UAT_NO_DB=1")
if defined HOSTED if not defined UAT_CHECKOUT_URL set "UAT_CHECKOUT_URL=https://pay.20-255-158-192.sslip.io"
for %%A in (%*) do if /i "%%~A"=="headed" set "HEADED=--headed"

rem Moi lan chay tu dong tang so vong seed (artifacts\seed_round.txt) de UAT-PRE tao bo khoan phi moi va nap lai vi EA. Muon giu nguyen vong dang dat thi set UAT_SEED_KEEP=1 (va UAT_SEED_ROUND).
if not "%UAT_SEED_KEEP%"=="1" call :nextround
echo Vong seed: %UAT_SEED_ROUND%
set "PYEXE="
if exist ".venv\Scripts\python.exe" set "PYEXE=.venv\Scripts\python.exe"
if not defined PYEXE if exist "..\r4_automation\.venv\Scripts\python.exe" set "PYEXE=..\r4_automation\.venv\Scripts\python.exe"
if not defined PYEXE (
  echo Dang tao moi truong ao .venv ...
  where py >nul 2>&1 && (py -3 -m venv .venv) || (python -m venv .venv)
  if errorlevel 1 (echo Khong tao duoc .venv & exit /b 1)
  set "PYEXE=.venv\Scripts\python.exe"
  "%PYEXE%" -m pip install -r requirements.txt || exit /b 1
  "%PYEXE%" -m playwright install chromium || exit /b 1
)

if not exist artifacts mkdir artifacts
if exist artifacts\allure-results rmdir /s /q artifacts\allure-results
echo.
echo Dang chay UAT. Video: artifacts\videos, anh: artifacts\screenshots, ket qua: artifacts\uat_results.json
"%PYEXE%" -m pytest %SEL% %HEADED% --alluredir artifacts\allure-results
set "RC=%ERRORLEVEL%"
:report
if not defined PYEXE (
  if exist ".venv\Scripts\python.exe" (set "PYEXE=.venv\Scripts\python.exe") else if exist "..\r4_automation\.venv\Scripts\python.exe" (set "PYEXE=..\r4_automation\.venv\Scripts\python.exe") else (set "PYEXE=python")
)
"%PYEXE%" tools\export_results.py
where allure >nul 2>&1 && (allure generate artifacts\allure-results -o artifacts\allure-report --clean >nul 2>&1 && echo Bao cao Allure: artifacts\allure-report\index.html)
exit /b %RC%

rem Danh sach case sau chu case: PowerShell bo dau nhay nen cmd tach dau phay thanh nhieu tham so, gom lai o day.
:collect
set "CASES="
shift
:cl
if "%~1"=="" goto :cdone
if /i "%~1"=="hosted" goto :cnext
if /i "%~1"=="headed" goto :cnext
if defined CASES (set "CASES=%CASES%,%~1") else set "CASES=%~1"
:cnext
shift
goto :cl
:cdone
exit /b 0

:nextround
set "N=5"
if not exist artifacts mkdir artifacts
if exist artifacts\seed_round.txt set /p N=<artifacts\seed_round.txt
set /a N=N+1
>artifacts\seed_round.txt echo %N%
set "UAT_SEED_ROUND=%N%"
exit /b 0
