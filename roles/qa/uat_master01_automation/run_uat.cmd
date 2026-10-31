@echo off
rem Bo UAT Master 01: chay 35 case owner Gavin cua roles\qa\uat-master_1 (1).xlsx tren moi truong host san.
rem   run_uat.cmd                     chay ca 35 case, roi xuat bao cao
rem   run_uat.cmd case UAT-PAR-01     mot hoac nhieu case (cach nhau dau phay, cho phep *), vi du UAT-PAR-01*,UAT-MOE-06
rem   run_uat.cmd group par           mot nhom: moe, sch, par
rem   run_uat.cmd report              chi xuat lai bao cao tu lan chay truoc
rem   them chu headed de xem trinh duyet chay truc tiep, vi du: run_uat.cmd case UAT-PAR-01 headed
rem Ket qua: artifacts\UAT_Master01_Report.xlsx (Summary, Defects, Steps, Data mapping), artifacts\videos, artifacts\screenshots
setlocal EnableExtensions
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

set "PYEXE="
if exist ".venv\Scripts\python.exe" set "PYEXE=.venv\Scripts\python.exe"
if not defined PYEXE if exist "..\gavin_uat_automation\.venv\Scripts\python.exe" set "PYEXE=..\gavin_uat_automation\.venv\Scripts\python.exe"
if not defined PYEXE if exist "..\r4_automation\.venv\Scripts\python.exe" set "PYEXE=..\r4_automation\.venv\Scripts\python.exe"
if not defined PYEXE (
  echo Dang tao moi truong ao .venv ...
  where py >nul 2>&1 && (py -3 -m venv .venv) || (python -m venv .venv)
  if errorlevel 1 (echo Khong tao duoc .venv & exit /b 1)
  set "PYEXE=.venv\Scripts\python.exe"
)
"%PYEXE%" -c "import pytest, playwright, openpyxl" >nul 2>&1 || (
  "%PYEXE%" -m pip install -r requirements.txt || exit /b 1
  "%PYEXE%" -m playwright install chromium || exit /b 1
)

if /i "%~1"=="report" goto :report

if not exist "data\master01_cases.json" "%PYEXE%" tools\extract_master.py

set "SEL="
if /i "%~1"=="case" set "SEL=--uat-case %~2"
if /i "%~1"=="group" set "SEL=--uat-case UAT-%~2-*"
set "UAT_HEADED="
for %%A in (%*) do if /i "%%~A"=="headed" set "UAT_HEADED=1"

echo Dang chay UAT Master 01 ... video: artifacts\videos, anh: artifacts\screenshots
"%PYEXE%" -m pytest %SEL%
set "RC=%ERRORLEVEL%"

:report
"%PYEXE%" tools\report.py
exit /b %RC%
